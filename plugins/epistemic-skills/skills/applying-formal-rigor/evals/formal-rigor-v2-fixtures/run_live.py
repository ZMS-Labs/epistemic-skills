#!/usr/bin/env python3
"""Resumable, no-retry live runner for the formal-rigor v2 battery."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import nullcontext
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import threading
from typing import Callable, NamedTuple
import uuid


ROOT = Path(__file__).resolve().parent
SKILL_ROOT = ROOT.parents[1]
REPO_ROOT = ROOT.parents[5]
FIXTURES_ROOT = ROOT / "fixtures"
PROMPTS_ROOT = ROOT / "prompts"
RED_BASELINE_ROOT = ROOT / "results" / "2026-07-24-red-baseline"
FLEET_BRIDGE_LOCK = threading.Lock()
EXACT_JSON_BOUNDARY = (
    "The first non-whitespace character must be `{`, and its matching top-level `}` "
    "must be the last non-whitespace character. Emit no draft object, repeated snapshot, "
    "second object, commentary, Markdown fence, or extra delimiter."
)
CONCISE_JSON = (
    "Keep the JSON concise: use short but sufficient strings and minimal arrays, with no "
    "repeated rationale, evidence, or restatement of packet contents."
)
JSON_SYNTAX_CHECK = (
    "Before returning, verify that the complete response parses as JSON: every object member "
    "and array element is comma-separated, every string is closed and escaped, and braces "
    "and brackets are balanced."
)
SILENT_OUTPUT_BOUNDARY = (
    "Do all analysis silently. Never emit analysis, planning, self-talk, a schema example, "
    "or a draft."
)
EMPIRICAL_TESTS_BOUNDARY = (
    "Every entry in `record.empirical_closure.tests` must be a JSON string, never an object."
)

PARODY_ARMS = (
    "parody-always-cautious",
    "parody-always-decide",
    "parody-closed-taxonomy",
    "parody-formal-only",
    "parody-full-ceremony",
    "parody-jargon-only",
)
ARM_PROMPTS = {
    "neutral": "neutral.txt",
    "v1-current": "v1-current.txt",
    "v2-candidate": "v2-candidate.txt",
    **{arm: f"{arm}.txt" for arm in PARODY_ARMS},
}
PARODY_HARNESSES = {
    "parody-always-cautious": "codex",
    "parody-always-decide": "agy",
    "parody-closed-taxonomy": "cursor",
    "parody-formal-only": "codex",
    "parody-full-ceremony": "agy",
    "parody-jargon-only": "cursor",
}
DEFAULT_PROVIDER_PLAN = "frozen-three-provider"
PROVIDER_PLANS = {
    "frozen-three-provider": {
        "candidate": {1: "codex", 2: "agy", 3: "cursor"},
        "parodies": PARODY_HARNESSES,
        "semantic": {
            1: {"a": "agy", "b": "cursor"},
            2: {"a": "cursor", "b": "codex"},
            3: {"a": "codex", "b": "agy"},
        },
    },
    "noncursor-degraded-v1": {
        "candidate": {1: "codex", 2: "agy", 3: "codex"},
        "parodies": {
            "parody-always-cautious": "codex",
            "parody-always-decide": "agy",
            "parody-closed-taxonomy": "codex",
            "parody-formal-only": "codex",
            "parody-full-ceremony": "agy",
            "parody-jargon-only": "agy",
        },
        "semantic": {
            1: {"a": "agy", "b": "agy"},
            2: {"a": "codex", "b": "codex"},
            3: {"a": "agy", "b": "agy"},
        },
    },
    "noncursor-degraded-v2": {
        "candidate": {1: "codex", 2: "agy", 3: "codex"},
        "parodies": {
            "parody-always-cautious": "codex",
            "parody-always-decide": "agy",
            "parody-closed-taxonomy": "codex",
            "parody-formal-only": "codex",
            "parody-full-ceremony": "agy",
            "parody-jargon-only": "agy",
        },
        "semantic": {
            1: {"a": "agy", "b": "agy"},
            2: {"a": "codex", "b": "codex"},
            3: {"a": "agy", "b": "agy"},
        },
    },
    "noncursor-degraded-v3": {
        "candidate": {1: "codex", 2: "agy", 3: "codex"},
        "parodies": {
            "parody-always-cautious": "codex",
            "parody-always-decide": "agy",
            "parody-closed-taxonomy": "codex",
            "parody-formal-only": "codex",
            "parody-full-ceremony": "agy",
            "parody-jargon-only": "agy",
        },
        "semantic": {
            1: {"a": "agy", "b": "agy"},
            2: {"a": "codex", "b": "codex"},
            3: {"a": "agy", "b": "agy"},
        },
    },
}
BASE_EXECUTION_POLICY = {
    "effort_by_phase": {
        "arms": {"codex": "high", "agy": "high", "cursor": "provider-model-default"},
        "semantic": {"codex": "high", "agy": "high", "cursor": "provider-model-default"},
    },
    "packet_root_policy": "output-adjacent-phase-specific;reject-sensitive-user-profile-path",
    "output_schema_delivery": {
        "arms": {
            "codex": "native-cli-output-schema", "agy": "packet-file",
            "cursor": "packet-file",
        },
        "semantic": {
            "codex": "native-cli-output-schema", "agy": "packet-file",
            "cursor": "packet-file",
        },
    },
}
V2_EXECUTION_POLICY = {
    **BASE_EXECUTION_POLICY,
    "effort_by_phase": {
        "arms": {"codex": "high", "agy": "medium", "cursor": "provider-model-default"},
        "semantic": {"codex": "high", "agy": "high", "cursor": "provider-model-default"},
    },
    "output_schema_delivery": {
        "arms": {
            "codex": "native-cli-output-schema",
            "agy": "exact-schema-in-immediate-prompt",
            "cursor": "exact-schema-in-immediate-prompt",
        },
        "semantic": {
            "codex": "native-cli-output-schema",
            "agy": "exact-schema-in-immediate-prompt",
            "cursor": "exact-schema-in-immediate-prompt",
        },
    },
}
V3_MODELS_BY_PHASE = {
    "arms": {
        "codex": "gpt-5.6-sol", "agy": "gemini-3.6-flash-medium",
        "cursor": "gpt-5.6-sol",
    },
    "semantic": {
        "codex": "gpt-5.6-sol", "agy": "gemini-3.1-pro-high",
        "cursor": "gpt-5.6-sol",
    },
}
HARNESS_PROVIDERS = {"codex": "OpenAI", "agy": "Google", "cursor": "Cursor"}
SEMANTIC_VERDICTS = {"VALID", "INVALID", "INCONCLUSIVE"}
OBLIGATION_STATES = {"SATISFIED", "VIOLATED", "INCONCLUSIVE"}
FLEET_BRIDGE_NODE_PROGRAM = r"""
const chunks = [];
process.stdin.setEncoding("utf8");
process.stdin.on("data", chunk => chunks.push(chunk));
process.stdin.on("end", async () => {
  try {
    const payload = JSON.parse(chunks.join(""));
    const allowed = new Set(["codex", "cursor_agent", "gemini"]);
    if (!allowed.has(payload.kind)) throw new Error(`unsupported surface kind: ${payload.kind}`);
    const response = await fetch(`http://127.0.0.1:8181/surfaces/${payload.kind}/stream`, {
      method: "POST",
      headers: {"content-type": "application/json"},
      body: JSON.stringify({
        prompt: payload.prompt,
        model: payload.model,
        task_id: payload.task_id,
        run_id: payload.run_id,
      }),
    });
    if (!response.ok) {
      process.stderr.write(`surface bridge HTTP ${response.status}: ${await response.text()}\n`);
      process.exitCode = 2;
      return;
    }
    for await (const chunk of response.body) process.stdout.write(chunk);
  } catch (error) {
    process.stderr.write(`${error && error.stack ? error.stack : error}\n`);
    process.exitCode = 2;
  }
});
""".strip()


class ArmTask(NamedTuple):
    arm: str
    repetition: int
    fixture: str


class SemanticTask(NamedTuple):
    repetition: int
    fixture: str
    seat: str


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def default_codex_executable() -> str:
    return "codex.cmd" if os.name == "nt" else "codex"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def validate_json_schema(value: object, schema: dict, path: str = "$") -> list[str]:
    """Validate the JSON Schema subset used by the frozen evaluation envelopes."""
    errors: list[str] = []

    for keyword in ("anyOf", "oneOf"):
        if keyword in schema:
            branch_errors = [validate_json_schema(value, branch, path) for branch in schema[keyword]]
            matched = sum(not branch for branch in branch_errors)
            if (keyword == "anyOf" and matched == 0) or (keyword == "oneOf" and matched != 1):
                detail = "; ".join(", ".join(branch) for branch in branch_errors if branch)
                return [f"{path}: does not satisfy {keyword}" + (f" ({detail})" if detail else "")]
            return []

    expected_type = schema.get("type")
    type_checks = {
        "object": lambda item: isinstance(item, dict),
        "array": lambda item: isinstance(item, list),
        "string": lambda item: isinstance(item, str),
        "null": lambda item: item is None,
        "boolean": lambda item: isinstance(item, bool),
        "integer": lambda item: isinstance(item, int) and not isinstance(item, bool),
        "number": lambda item: isinstance(item, (int, float)) and not isinstance(item, bool),
    }
    if expected_type and not type_checks[expected_type](value):
        return [f"{path}: expected {expected_type}"]
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: expected constant {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: value is not in the allowed enum")

    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path}: string is shorter than minLength")
        if schema.get("pattern") and re.search(schema["pattern"], value) is None:
            errors.append(f"{path}: string does not match required pattern")
    elif isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: array is shorter than minItems")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errors.append(f"{path}: array is longer than maxItems")
        if schema.get("uniqueItems"):
            serialized = [json.dumps(item, sort_keys=True, separators=(",", ":")) for item in value]
            if len(serialized) != len(set(serialized)):
                errors.append(f"{path}: array items are not unique")
        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(value):
                errors.extend(validate_json_schema(item, item_schema, f"{path}[{index}]"))
    elif isinstance(value, dict):
        properties = schema.get("properties", {})
        missing = set(schema.get("required", [])) - set(value)
        for name in sorted(missing):
            errors.append(f"{path}: missing required property {name!r}")
        if schema.get("additionalProperties") is False:
            for name in sorted(set(value) - set(properties)):
                errors.append(f"{path}: unexpected property {name!r}")
        for name, child_schema in properties.items():
            if name in value:
                errors.extend(validate_json_schema(value[name], child_schema, f"{path}.{name}"))
    return errors


def call_qualifies(record: dict) -> bool:
    base = (
        record.get("transport") == "completed"
        and record.get("json_parseable") is True
        and record.get("schema_valid") is True
        and record.get("secret_screen", {}).get("passed") is True
    )
    if not base:
        return False
    if record.get("provider_plan") == "noncursor-degraded-v3":
        return (
            record.get("phase") in ("arms", "semantic")
            and isinstance(record.get("model"), str) and bool(record.get("model"))
            and record.get("reasoning_effort") in ("medium", "high")
            and isinstance(record.get("preflight_sha256"), str)
            and len(record["preflight_sha256"]) == 64
            and isinstance(record.get("campaign_plan_sha256"), str)
            and len(record["campaign_plan_sha256"]) == 64
        )
    return True


def reasoning_effort_label(harness: str, *, bridge: bool) -> str:
    return "high" if not bridge and harness in ("codex", "agy") else "provider-model-default"


def response_evidence_errors(
    call_dir: Path, schema_path: Path, *, expected_identity: dict | None = None,
) -> list[str]:
    call_path = call_dir / "call.json"
    response_path = call_dir / "response.json"
    if not call_path.is_file():
        return ["qualifying call evidence is missing"]
    try:
        call = json.loads(call_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        return [f"call evidence is unreadable: {exc}"]
    errors = [] if call_qualifies(call) else ["call evidence is not completed and schema-valid"]
    if call.get("schema") != "formal-rigor-live-call@1":
        errors.append("call evidence has an invalid record schema")
    for key, expected in (expected_identity or {}).items():
        if call.get(key) != expected:
            errors.append(f"call identity {key!r} does not match expected value")
    if not response_path.is_file():
        return errors + ["response artifact is missing"]
    if call.get("response_sha256") != sha256_file(response_path):
        errors.append("response artifact does not match its terminal call hash")
    try:
        response = json.loads(response_path.read_text(encoding="utf-8"))
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        return errors + [f"response or schema is unreadable: {exc}"]
    errors.extend(validate_json_schema(response, schema))
    return errors


def materialize_qualified_response(
    call_dir: Path, destination: Path, schema_path: Path, *, expected_identity: dict,
) -> bool:
    if response_evidence_errors(
        call_dir, schema_path, expected_identity=expected_identity,
    ):
        return False
    response_path = call_dir / "response.json"
    if destination.is_file():
        return sha256_file(destination) == sha256_file(response_path)
    copy_file(response_path, destination)
    return True


def candidate_response_qualifies(
    output_root: Path, task: SemanticTask, *, provider_plan: str, source_commit: str,
    models_by_phase: dict[str, dict[str, str]] | None = None,
    preflight_sha256: str | None = None, campaign_plan_sha256: str | None = None,
) -> bool:
    run_dir = output_root / "arms" / "v2-candidate" / f"run-{task.repetition}"
    call_dir = run_dir / "calls" / task.fixture
    destination = run_dir / f"{task.fixture}.response.json"
    expected_identity = {
        "kind": "arm", "provider_plan": provider_plan, "source_commit": source_commit,
        "arm": "v2-candidate", "repetition": task.repetition, "fixture": task.fixture,
    }
    if provider_plan == "noncursor-degraded-v3":
        if models_by_phase is None or not preflight_sha256 or not campaign_plan_sha256:
            return False
        harness = candidate_harness(task.repetition, provider_plan)
        expected_identity.update({
            "phase": "arms", "model": models_by_phase["arms"][harness],
            "reasoning_effort": call_effort(
                provider_plan, phase="arms", harness=harness, bridge=False,
            ),
            "preflight_sha256": preflight_sha256,
            "campaign_plan_sha256": campaign_plan_sha256,
        })
    return materialize_qualified_response(
        call_dir, destination, ROOT / "formal-rigor-fixture-transport.schema.json",
        expected_identity=expected_identity,
    )


def fixture_ids() -> list[str]:
    return sorted(path.name for path in FIXTURES_ROOT.iterdir() if path.is_dir())


def full_arm_plan() -> list[ArmTask]:
    tasks: list[ArmTask] = []
    for arm in ("neutral", "v1-current"):
        for repetition in (2, 3):
            tasks.extend(ArmTask(arm, repetition, fixture) for fixture in fixture_ids())
    for repetition in (1, 2, 3):
        tasks.extend(ArmTask("v2-candidate", repetition, fixture) for fixture in fixture_ids())
    for arm in PARODY_ARMS:
        tasks.extend(ArmTask(arm, 1, fixture) for fixture in fixture_ids())
    return tasks


def full_semantic_plan() -> list[SemanticTask]:
    return [
        SemanticTask(repetition, fixture, seat)
        for repetition in (1, 2, 3)
        for fixture in fixture_ids()
        for seat in ("a", "b")
    ]


def provider_plan_config(provider_plan: str) -> dict:
    try:
        return PROVIDER_PLANS[provider_plan]
    except KeyError as exc:
        raise ValueError(f"unknown provider plan: {provider_plan}") from exc


def validate_live_provider_plan(provider_plan: str) -> None:
    provider_plan_config(provider_plan)
    if provider_plan != "noncursor-degraded-v3":
        raise ValueError(
            f"provider plan {provider_plan!r} is historical inspection-only; "
            "live execution requires 'noncursor-degraded-v3'"
        )


def validate_live_harness_executable(provider_plan: str, harness: str, executable: str) -> None:
    validate_live_provider_plan(provider_plan)
    if executable.startswith("fleet-bridge://"):
        raise ValueError(
            f"provider plan {provider_plan!r} requires direct {harness} execution; "
            "Fleet bridge routing requires a distinct preregistered protocol identity"
        )


def validate_live_harness_configuration(
    provider_plan: str, executables: dict[str, str],
) -> None:
    active_harnesses = {
        arm_harness(task, provider_plan) for task in full_arm_plan()
    } | {
        semantic_harness(task, provider_plan) for task in full_semantic_plan()
    }
    for harness in active_harnesses:
        validate_live_harness_executable(provider_plan, harness, executables[harness])


def execution_policy(provider_plan: str) -> dict:
    provider_plan_config(provider_plan)
    return (
        V2_EXECUTION_POLICY
        if provider_plan in ("noncursor-degraded-v2", "noncursor-degraded-v3")
        else BASE_EXECUTION_POLICY
    )


def call_effort(
    provider_plan: str, *, phase: str, harness: str, bridge: bool,
) -> str:
    if bridge:
        return "provider-model-default"
    return execution_policy(provider_plan)["effort_by_phase"][phase][harness]


def agy_preflight(
    agy: str, models_by_phase: dict[str, dict[str, str]], policy: dict,
) -> dict:
    version_call = subprocess.run(
        [agy, "--version"], text=True, encoding="utf-8", errors="replace",
        capture_output=True, check=False,
    )
    if version_call.returncode != 0 or version_call.stdout.strip() != "1.1.7":
        raise ValueError("V3 requires agy CLI version 1.1.7")
    models_call = subprocess.run(
        [agy, "models"], text=True, encoding="utf-8", errors="replace",
        capture_output=True, check=False,
    )
    if models_call.returncode != 0:
        raise ValueError("agy model catalog preflight failed")
    catalog = [line.strip() for line in models_call.stdout.splitlines() if line.strip()]
    if len(catalog) != len(set(catalog)):
        raise ValueError("agy model catalog contains duplicate identifiers")
    selected = {
        phase: models_by_phase[phase]["agy"] for phase in ("arms", "semantic")
    }
    expected_selected = {
        phase: V3_MODELS_BY_PHASE[phase]["agy"] for phase in ("arms", "semantic")
    }
    if selected != expected_selected:
        raise ValueError("AGY phase models do not match the registered V3 protocol")
    for phase, model in selected.items():
        effort = policy["effort_by_phase"][phase]["agy"]
        if model not in catalog:
            raise ValueError(f"agy model {model!r} is unavailable for {phase}")
        if not model.endswith(f"-{effort}"):
            raise ValueError(
                f"agy model {model!r} does not match configured {phase} effort {effort!r}"
            )
    return {
        "schema": "formal-rigor-agy-preflight@1",
        "agy_version": "1.1.7",
        "catalog_sha256": sha256_bytes(models_call.stdout.encode("utf-8")),
        "selected_models_by_phase": selected,
    }


def candidate_harness(repetition: int, provider_plan: str = DEFAULT_PROVIDER_PLAN) -> str:
    return provider_plan_config(provider_plan)["candidate"][repetition]


def arm_harness(task: ArmTask, provider_plan: str = DEFAULT_PROVIDER_PLAN) -> str:
    if task.arm in ("neutral", "v1-current", "v2-candidate"):
        return candidate_harness(task.repetition, provider_plan)
    return provider_plan_config(provider_plan)["parodies"][task.arm]


def semantic_harness(task: SemanticTask, provider_plan: str = DEFAULT_PROVIDER_PLAN) -> str:
    return provider_plan_config(provider_plan)["semantic"][task.repetition][task.seat]


def campaign_plan(
    *, provider_plan: str, source_commit: str, v1_commit: str,
    models: dict[str, str] | None = None,
    models_by_phase: dict[str, dict[str, str]] | None = None,
    preflight_receipt: dict | None = None,
) -> dict:
    provider_plan_config(provider_plan)
    arm_tasks = [
        {
            "arm": task.arm,
            "repetition": task.repetition,
            "fixture": task.fixture,
            "harness": arm_harness(task, provider_plan),
        }
        for task in full_arm_plan()
    ]
    semantic_tasks = [
        {
            "repetition": task.repetition,
            "fixture": task.fixture,
            "seat": task.seat,
            "harness": semantic_harness(task, provider_plan),
        }
        for task in full_semantic_plan()
    ]
    active_harnesses = [
        harness for harness in HARNESS_PROVIDERS
        if any(task["harness"] == harness for task in arm_tasks + semantic_tasks)
    ]
    if provider_plan == "noncursor-degraded-v3":
        if models_by_phase is None or preflight_receipt is None:
            raise ValueError("V3 campaign requires phase models and an AGY preflight receipt")
        if models_by_phase != V3_MODELS_BY_PHASE:
            raise ValueError("V3 campaign model matrix does not match the registered protocol")
        selected_models_by_phase = {
            phase: {
                harness: models_by_phase[phase][harness]
                for harness in HARNESS_PROVIDERS
                if any(task["harness"] == harness for task in tasks)
            }
            for phase, tasks in (("arms", arm_tasks), ("semantic", semantic_tasks))
        }
        for task in arm_tasks:
            task["model"] = selected_models_by_phase["arms"][task["harness"]]
            task["effort"] = call_effort(
                provider_plan, phase="arms", harness=task["harness"], bridge=False,
            )
        for task in semantic_tasks:
            task["model"] = selected_models_by_phase["semantic"][task["harness"]]
            task["effort"] = call_effort(
                provider_plan, phase="semantic", harness=task["harness"], bridge=False,
            )
        identity_fields = {
            "schema": "formal-rigor-live-campaign-plan@2",
            "selected_models_by_phase": selected_models_by_phase,
            "preflight_receipt": preflight_receipt,
            "preflight_sha256": sha256_bytes(canonical_json_bytes(preflight_receipt)),
        }
    else:
        if models is None:
            raise ValueError("historical campaign inspection requires harness models")
        if set(active_harnesses) - set(models):
            raise ValueError("campaign models must name every active harness")
        identity_fields = {
            "schema": "formal-rigor-live-campaign-plan@1",
            "selected_models": {harness: models[harness] for harness in active_harnesses},
        }
    return {
        **identity_fields,
        "provider_plan": provider_plan,
        "source_commit": source_commit,
        "v1_commit": v1_commit,
        "execution_policy": execution_policy(provider_plan),
        "arm_calls": len(arm_tasks),
        "arm_calls_by_harness": {
            harness: sum(task["harness"] == harness for task in arm_tasks)
            for harness in HARNESS_PROVIDERS
        },
        "semantic_calls": len(semantic_tasks),
        "semantic_calls_by_harness": {
            harness: sum(task["harness"] == harness for task in semantic_tasks)
            for harness in HARNESS_PROVIDERS
        },
        "arm_tasks": arm_tasks,
        "semantic_tasks": semantic_tasks,
    }


def ensure_campaign_plan(
    output_root: Path, *, provider_plan: str, source_commit: str, v1_commit: str,
    models: dict[str, str] | None = None,
    models_by_phase: dict[str, dict[str, str]] | None = None,
    preflight_receipt: dict | None = None,
) -> dict:
    expected = campaign_plan(
        provider_plan=provider_plan, source_commit=source_commit, v1_commit=v1_commit,
        models=models, models_by_phase=models_by_phase,
        preflight_receipt=preflight_receipt,
    )
    manifest_path = output_root / "campaign-plan.json"
    if manifest_path.is_file():
        actual = json.loads(manifest_path.read_text(encoding="utf-8"))
        if actual != expected:
            raise ValueError("existing campaign manifest identity does not match requested campaign")
        return actual
    if output_root.exists() and any(output_root.rglob("call.json")):
        raise ValueError("output root contains terminal calls but no campaign manifest")
    write_json(manifest_path, expected)
    return expected


def phase_status(
    *, phase: str, tasks: list, provider_plan: str, source_commit: str,
    completed: int, failed: int, models: dict[str, str] | None = None,
    models_by_phase: dict[str, dict[str, str]] | None = None,
    preflight_sha256: str | None = None, campaign_plan_sha256: str | None = None,
) -> dict:
    harness_for = arm_harness if phase == "arms" else semantic_harness
    status = {
        "schema": (
            "formal-rigor-live-phase-status@2"
            if provider_plan == "noncursor-degraded-v3"
            else "formal-rigor-live-phase-status@1"
        ),
        "phase": phase,
        "provider_plan": provider_plan,
        "source_commit": source_commit,
        "planned_by_harness": {
            harness: sum(harness_for(task, provider_plan) == harness for task in tasks)
            for harness in HARNESS_PROVIDERS
        },
        "planned": len(tasks),
        "completed": completed,
        "failed": failed,
    }
    if provider_plan == "noncursor-degraded-v3":
        if models_by_phase is None or not preflight_sha256 or not campaign_plan_sha256:
            raise ValueError("V3 phase status requires model and identity bindings")
        active_harnesses = {
            harness_for(task, provider_plan) for task in tasks
        }
        status.update({
            "selected_models_by_harness": {
                harness: models_by_phase[phase][harness]
                for harness in HARNESS_PROVIDERS if harness in active_harnesses
            },
            "effort_by_harness": {
                harness: execution_policy(provider_plan)["effort_by_phase"][phase][harness]
                for harness in HARNESS_PROVIDERS if harness in active_harnesses
            },
            "preflight_sha256": preflight_sha256,
            "campaign_plan_sha256": campaign_plan_sha256,
        })
    else:
        status["models"] = models
    return status


def filter_arm_tasks(
    tasks: list[ArmTask], *, arms: set[str] | None = None,
    fixtures: set[str] | None = None, repetitions: set[int] | None = None,
) -> list[ArmTask]:
    return [
        task for task in tasks
        if (arms is None or task.arm in arms)
        and (fixtures is None or task.fixture in fixtures)
        and (repetitions is None or task.repetition in repetitions)
    ]


def filter_semantic_tasks(
    tasks: list[SemanticTask], *, fixtures: set[str] | None = None,
    repetitions: set[int] | None = None, seats: set[str] | None = None,
) -> list[SemanticTask]:
    return [
        task for task in tasks
        if (fixtures is None or task.fixture in fixtures)
        and (repetitions is None or task.repetition in repetitions)
        and (seats is None or task.seat in seats)
    ]


def copy_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def build_arm_packet(
    destination: Path,
    arm: str,
    fixture_dir: Path,
    *,
    v1_source_dir: Path | None = None,
) -> None:
    if arm not in ARM_PROMPTS:
        raise ValueError(f"unknown arm: {arm}")
    destination.mkdir(parents=True, exist_ok=False)
    copy_file(fixture_dir / "scenario.md", destination / "scenario.md")
    shutil.copytree(fixture_dir / "artifacts", destination / "artifacts")
    copy_file(ROOT / "formal-rigor-fixture-response.schema.json", destination / "formal-rigor-fixture-response.schema.json")
    copy_file(ROOT / "formal-rigor-fixture-transport.schema.json", destination / "formal-rigor-fixture-transport.schema.json")
    copy_file(ROOT / "formal-rigor-record.schema.json", destination / "formal-rigor-record.schema.json")
    copy_file(PROMPTS_ROOT / ARM_PROMPTS[arm], destination / "ARM_PROMPT.txt")

    if arm == "v1-current":
        if v1_source_dir is None:
            raise ValueError("v1-current packet requires a pinned v1 source directory")
        copy_file(v1_source_dir / "SKILL.md", destination / "v1" / "SKILL.md")
        copy_file(v1_source_dir / "theory-battery.md", destination / "v1" / "theory-battery.md")
    elif arm == "v2-candidate" or arm in PARODY_ARMS:
        copy_file(SKILL_ROOT / "SKILL.md", destination / "candidate" / "SKILL.md")
        copy_file(SKILL_ROOT / "theory-battery.md", destination / "candidate" / "theory-battery.md")
        shutil.copytree(
            SKILL_ROOT / "reference" / "modules",
            destination / "candidate" / "reference" / "modules",
        )


def adjudication_rubric(truth: dict) -> dict:
    return {
        "fixture": truth["fixture_id"],
        "claims": [
            {
                "id": claim["id"],
                "proof_obligations": claim.get("proof_obligations", []),
                "forbidden_propositions": claim.get("forbidden_propositions", []),
            }
            for claim in truth["claims"]
        ],
    }


def build_adjudication_packet(
    destination: Path,
    fixture_dir: Path,
    candidate_response: Path,
    truth: dict,
) -> None:
    destination.mkdir(parents=True, exist_ok=False)
    copy_file(fixture_dir / "scenario.md", destination / "scenario.md")
    shutil.copytree(fixture_dir / "artifacts", destination / "artifacts")
    copy_file(candidate_response, destination / "candidate-response.json")
    write_json(destination / "rubric.json", adjudication_rubric(truth))
    copy_file(
        ROOT / "formal-rigor-semantic-adjudication.schema.json",
        destination / "formal-rigor-semantic-adjudication.schema.json",
    )


def packet_manifest(packet_dir: Path) -> dict[str, str]:
    return {
        path.relative_to(packet_dir).as_posix(): sha256_file(path)
        for path in sorted(packet_dir.rglob("*"))
        if path.is_file()
    }


def codex_command(
    *, codex: str, model: str, packet_dir: Path, response_path: Path, prompt: str,
    output_schema: Path | None = None, effort: str = "high",
) -> list[str]:
    command = [
        codex, "exec", "--ephemeral", "--ignore-user-config", "--ignore-rules",
        "--disable", "plugins", "--disable", "apps", "--disable", "remote_plugin",
        "--disable", "plugin_sharing", "--sandbox", "read-only",
        "--skip-git-repo-check", "--color", "never", "--json",
        "-c", f'model_reasoning_effort="{effort}"', "--model", model,
        "--cd", str(packet_dir), "--output-last-message", str(response_path),
    ]
    if output_schema is not None:
        command.extend(["--output-schema", output_schema.as_posix()])
    command.append(prompt)
    return command


def codex_prompt_transport(prompt: str) -> tuple[str, str]:
    """Keep the sealed prompt off argv and below Windows command-length limits."""
    return "-", prompt


def agy_command(
    *, agy: str, model: str, packet_dir: Path, response_path: Path, prompt: str,
    effort: str,
) -> list[str]:
    del packet_dir, response_path
    return [
        agy, "--sandbox", "--dangerously-skip-permissions", "--mode", "plan",
        "--add-dir", ".", "--model", model, "--effort", effort,
        "--print", prompt,
    ]


def cursor_command(
    *, cursor: str, model: str, packet_dir: Path, response_path: Path, prompt: str,
) -> list[str]:
    del response_path
    return [
        cursor, "--print", "--output-format", "text", "--mode", "ask",
        "--sandbox", "enabled", "--trust", "--workspace", str(packet_dir),
        "--model", model, prompt,
    ]


def harness_command(
    *, harness: str, executable: str, model: str, packet_dir: Path,
    response_path: Path, prompt: str, effort: str, output_schema: Path | None = None,
) -> list[str]:
    if harness == "codex":
        return codex_command(
            codex=executable, model=model, packet_dir=packet_dir,
            response_path=response_path, prompt=prompt, output_schema=output_schema,
            effort=effort,
        )
    if harness == "agy":
        return agy_command(
            agy=executable, model=model, packet_dir=packet_dir,
            response_path=response_path, prompt=prompt, effort=effort,
        )
    if harness == "cursor":
        return cursor_command(
            cursor=executable, model=model, packet_dir=packet_dir,
            response_path=response_path, prompt=prompt,
        )
    raise ValueError(f"unknown harness: {harness}")


def call_needed(result_dir: Path) -> bool:
    return not (result_dir / "call.json").is_file()


def sealed_packet_prompt(packet_dir: Path, prompt: str) -> str:
    files = {
        path.relative_to(packet_dir).as_posix(): path.read_text(encoding="utf-8")
        for path in sorted(packet_dir.rglob("*"))
        if path.is_file()
    }
    return f"""{prompt.rstrip()}

The isolated packet is delivered below as a JSON map from packet-relative paths to exact UTF-8
file contents. Treat those entries exactly as if they were read-only files in the current packet
directory. Do not use tools, execute commands, or write files. Do not seek any information outside
this sealed packet. The packet contains no ground truth, scorer, thresholds, other-arm responses,
or prior results.

SEALED_PACKET_JSON
{json.dumps(files, ensure_ascii=False, sort_keys=True)}
END_SEALED_PACKET_JSON

{CONCISE_JSON}
{JSON_SYNTAX_CHECK}
{SILENT_OUTPUT_BOUNDARY}
The applicable top-level response or adjudication marker must appear exactly once in the entire output.
{EMPIRICAL_TESTS_BOUNDARY}
{EXACT_JSON_BOUNDARY}
"""


def codex_arm_packet_prompt(packet_dir: Path, prompt: str) -> str:
    """Embed mandatory arm inputs while leaving material module bodies demand-loaded."""
    paths = [packet_dir / "ARM_PROMPT.txt", packet_dir / "scenario.md"]
    paths.extend(sorted((packet_dir / "artifacts").rglob("*")))
    paths.extend(sorted((packet_dir / "v1").rglob("*")) if (packet_dir / "v1").is_dir() else [])
    for relative in (
        "candidate/SKILL.md",
        "candidate/theory-battery.md",
        "candidate/reference/modules/index.md",
    ):
        path = packet_dir / relative
        if path.is_file():
            paths.append(path)
    files = {
        path.relative_to(packet_dir).as_posix(): path.read_text(encoding="utf-8")
        for path in paths
        if path.is_file()
    }
    return f"""{prompt.rstrip()}

The mandatory packet inputs are embedded below as exact UTF-8 file contents.
You must answer from these mandatory inputs now; a readiness acknowledgment or claim that no task
was supplied is invalid.
If the candidate module index routes to a material module, read only that module file from the
read-only packet directory before answering. Do not seek scorer, ground truth, thresholds, other
fixtures, other arms, or prior results.

MANDATORY_PACKET_JSON
{json.dumps(files, ensure_ascii=False, sort_keys=True)}
END_MANDATORY_PACKET_JSON
"""


def fleet_bridge_command(
    *, kubectl: str, context: str, namespace: str, pod: str,
) -> list[str]:
    return [
        kubectl, "--context", context, "-n", namespace, "exec", "-i", pod,
        "--", "node", "-e", FLEET_BRIDGE_NODE_PROGRAM,
    ]


def fleet_bridge_invocation(
    *, executable: str, harness: str, model: str, packet_dir: Path,
    prompt: str, identity: dict,
) -> dict:
    prefix = "fleet-bridge://"
    if not executable.startswith(prefix):
        raise ValueError("Fleet bridge executable must use fleet-bridge://context/namespace/pod")
    coordinates = executable[len(prefix):].split("/")
    if len(coordinates) != 3 or not all(coordinates):
        raise ValueError("Fleet bridge executable must identify context, namespace, and pod")
    if model != "auto":
        raise ValueError(
            "Fleet bridge stream does not forward model selection; use model 'auto' and record it honestly"
        )
    surface_kind = {"codex": "codex", "agy": "gemini", "cursor": "cursor_agent"}.get(harness)
    if surface_kind is None:
        raise ValueError(f"unknown harness: {harness}")
    context, namespace, pod = coordinates
    payload = {
        "kind": surface_kind,
        "model": model,
        "prompt": sealed_packet_prompt(packet_dir, prompt),
        "task_id": str(identity.get("fixture", "")),
        "run_id": "-".join(
            str(identity[key]) for key in ("kind", "arm", "repetition", "seat")
            if identity.get(key) not in (None, "")
        ),
    }
    return {
        "command": fleet_bridge_command(
            kubectl="kubectl", context=context, namespace=namespace, pod=pod,
        ),
        "stdin": json.dumps(payload, ensure_ascii=False),
        "metadata": {
            "adapter": "fleet-orchestrator-surface-bridge-stream",
            "context": context,
            "namespace": namespace,
            "pod": pod,
            "surface_kind": surface_kind,
            "model_selection": "surface-default-auto",
        },
    }


def parse_fleet_bridge_stream(events: str) -> tuple[str, int | None, str]:
    response_parts: list[str] = []
    exit_code: int | None = None
    stderr_parts: list[str] = []
    for raw_line in events.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        event = json.loads(line)
        if isinstance(event.get("delta"), str):
            response_parts.append(event["delta"])
        if event.get("done") is True:
            exit_code = event.get("code") if isinstance(event.get("code"), int) else 0
            if isinstance(event.get("stderr"), str) and event["stderr"]:
                stderr_parts.append(event["stderr"])
    return "".join(response_parts), exit_code, "\n".join(stderr_parts)


def normalize_fleet_bridge_response(response: str) -> tuple[str, str | None]:
    decoder = json.JSONDecoder()

    def envelope_identity(value: object) -> tuple[str, str] | None:
        if not isinstance(value, dict) or not isinstance(value.get("fixture"), str):
            return None
        response_marker = value.get("response")
        adjudication_marker = value.get("adjudication")
        if (
            response_marker == "formal-rigor-fixture-response@1"
            and adjudication_marker is None
        ):
            return response_marker, value["fixture"]
        if (
            adjudication_marker == "formal-rigor-semantic-adjudication@1"
            and response_marker is None
        ):
            return adjudication_marker, value["fixture"]
        return None

    values: list[object] = []
    spans: list[tuple[int, int]] = []
    offset = 0
    decode_failed = False
    while offset < len(response):
        while offset < len(response) and response[offset].isspace():
            offset += 1
        if offset >= len(response):
            break
        start = offset
        try:
            value, offset = decoder.raw_decode(response, offset)
        except json.JSONDecodeError:
            decode_failed = True
            break
        values.append(value)
        spans.append((start, offset))
    if not decode_failed and len(values) > 1 and all(value == values[0] for value in values[1:]):
        start, end = spans[0]
        return response[start:end], "deduplicated-identical-complete-json-values"
    envelopes: list[tuple[object, object]] = []
    if not decode_failed:
        for value in values:
            identity = envelope_identity(value)
            if identity is None:
                return response, None
            envelopes.append(identity)
        if len(values) > 1 and all(envelope == envelopes[0] for envelope in envelopes[1:]):
            start, end = spans[-1]
            return response[start:end], "selected-final-complete-json-snapshot"
        return response, None

    # Cursor's Fleet stream can contain an interrupted draft snapshot followed
    # by one complete final snapshot. Recover only the strict, observable form:
    # JSON-like snapshots begin at the stream boundary, every snapshot header
    # names the same recognized envelope and fixture, and the sole decodable
    # recognized object is the terminal value. Raw NDJSON remains in events.jsonl.
    candidates: list[tuple[int, int, dict[str, object]]] = []
    search_from = 0
    while True:
        start = response.find("{", search_from)
        if start < 0:
            break
        try:
            value, end = decoder.raw_decode(response, start)
        except json.JSONDecodeError:
            search_from = start + 1
            continue
        if isinstance(value, dict) and envelope_identity(value) is not None:
            candidates.append((start, end, value))
        search_from = start + 1

    if len(candidates) != 1:
        return response, None
    final_start, final_end, final_value = candidates[0]
    if response[final_end:].strip():
        return response, None
    final_identity = envelope_identity(final_value)
    if final_identity is None:
        return response, None
    final_marker, final_fixture = final_identity
    if not response[:final_start].rstrip().endswith("}"):
        return response, None

    header_pattern = re.compile(
        r'\{\s*"(?P<field>response|adjudication)"\s*:\s*'
        r'"(?P<marker>formal-rigor-(?:fixture-response|semantic-adjudication)@1)"\s*,'
        r'\s*"fixture"\s*:\s*"(?P<fixture>[^"\\]+)"'
    )
    headers = list(header_pattern.finditer(response))
    if len(headers) != 2 or headers[-1].start() != final_start:
        return response, None
    if response[:headers[0].start()].strip():
        return response, None
    if any(
        (
            header.group("field") == "response"
            and header.group("marker") != "formal-rigor-fixture-response@1"
        )
        or (
            header.group("field") == "adjudication"
            and header.group("marker") != "formal-rigor-semantic-adjudication@1"
        )
        or header.group("marker") != final_marker
        or header.group("fixture") != final_fixture
        for header in headers
    ):
        return response, None
    marker_count = len(re.findall(
        r'"(?:response|adjudication)"\s*:\s*'
        r'"formal-rigor-(?:fixture-response|semantic-adjudication)@1"',
        response,
    ))
    if marker_count != len(headers):
        return response, None
    return (
        response[final_start:final_end],
        "selected-final-complete-json-snapshot-after-malformed-prefix",
    )


def normalize_plain_text_response(response: str) -> tuple[str, str | None]:
    """Extract one recognized formal-rigor envelope from plain-text stdout."""
    decoder = json.JSONDecoder()
    recognized: list[tuple[int, int, object]] = []
    ambiguous = False
    offset = 0
    marker_patterns = (
        re.compile(r'"response"\s*:\s*"formal-rigor-fixture-response@1"'),
        re.compile(r'"adjudication"\s*:\s*"formal-rigor-semantic-adjudication@1"'),
    )
    while True:
        openings = [position for position in (
            response.find("{", offset), response.find("[", offset),
        ) if position >= 0]
        if not openings:
            break
        start = min(openings)
        try:
            value, end = decoder.raw_decode(response, start)
        except json.JSONDecodeError:
            offset = start + 1
            continue
        if isinstance(value, dict) and (
            value.get("response") == "formal-rigor-fixture-response@1"
            or value.get("adjudication") == "formal-rigor-semantic-adjudication@1"
        ):
            recognized.append((start, end, value))
        offset = end

    marker_count = sum(len(pattern.findall(response)) for pattern in marker_patterns)
    if marker_count != len(recognized):
        ambiguous = True

    distinct = {
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        for _, _, value in recognized
    }
    if ambiguous or len(recognized) != 1 or len(distinct) != 1:
        return response, None
    start, end, _ = recognized[-1]
    extracted = response[start:end]
    if response.strip() == extracted:
        return response, None
    return extracted, "extracted-single-recognized-json-envelope"


def arm_prompt(fixture: str) -> str:
    return f"""You are a context-isolated run agent for fixture {fixture}.
Perform the task now; do not acknowledge readiness or wait for another turn. Do not use a Markdown fence.
Read only files inside the current packet directory. Follow ARM_PROMPT.txt. The scenario is
scenario.md and its allowed evidence is under artifacts/. Public response contracts are the two
schema files. If candidate/ exists, read candidate/SKILL.md and the module registry, then load only
the module files you determine are material; do not treat module presence as proof.

Return exactly one formal-rigor-fixture-response@1 JSON object for fixture {fixture}. Emit no
Markdown fence, preamble, commentary, score, hidden class guess, or claims about files outside this
packet. Do not read or infer ground truth, thresholds, other fixtures, other arms, or prior results.
{CONCISE_JSON}
{JSON_SYNTAX_CHECK}
{SILENT_OUTPUT_BOUNDARY}
The response marker `formal-rigor-fixture-response@1` must appear exactly once in the entire output.
{EMPIRICAL_TESTS_BOUNDARY}
{EXACT_JSON_BOUNDARY}
"""


def semantic_prompt(fixture: str) -> str:
    return f"""You are one isolated, arm-blinded semantic adjudicator for fixture {fixture}.
Perform the task now; do not acknowledge readiness or wait for another turn. Do not use a Markdown fence.
Read only scenario.md, artifacts/, candidate-response.json, and rubric.json in this packet. Do not
infer arm identity, model identity, thresholds, prior results, or another adjudicator's report.
Judge whether the response actually satisfies every proof obligation and avoids every forbidden
proposition. Cite exact response coordinates. Structure and fluency are not proof.

Return exactly one JSON object with this shape and no prose outside it:
{{
  "adjudication": "formal-rigor-semantic-adjudication@1",
  "fixture": "{fixture}",
  "verdict": "VALID|INVALID|INCONCLUSIVE",
  "obligations": [{{"claim_id":"c1","obligation":"exact rubric string","status":"SATISFIED|VIOLATED|INCONCLUSIVE","response_coordinates":["path"],"reason":"..."}}],
  "forbidden_propositions": [{{"claim_id":"c1","proposition":"exact rubric string","present":false,"response_coordinates":[],"reason":"..."}}],
  "coverage_limits": []
}}
Include exactly one row for every rubric obligation and forbidden proposition.
{CONCISE_JSON}
{JSON_SYNTAX_CHECK}
{SILENT_OUTPUT_BOUNDARY}
The adjudication marker `formal-rigor-semantic-adjudication@1` must appear exactly once in the entire output.
{EXACT_JSON_BOUNDARY}
"""


def execution_prompt(
    prompt: str, *, provider_plan: str, phase: str, harness: str,
    output_schema_text: str,
) -> str:
    delivery = execution_policy(provider_plan)["output_schema_delivery"][phase][harness]
    if delivery != "exact-schema-in-immediate-prompt":
        return prompt
    marker_boundary = (
        "The response marker `formal-rigor-fixture-response@1` must appear exactly once in the entire output."
        if phase == "arms"
        else "The adjudication marker `formal-rigor-semantic-adjudication@1` must appear exactly once in the entire output."
    )
    return (
        f"{prompt.rstrip()}\n\n"
        "The exact frozen output schema for this call follows. Return an instance of it.\n"
        "BEGIN_EXACT_OUTPUT_SCHEMA\n"
        f"{output_schema_text}"
        "END_EXACT_OUTPUT_SCHEMA\n\n"
        f"{SILENT_OUTPUT_BOUNDARY}\n"
        f"{marker_boundary}\n"
        f"{EXACT_JSON_BOUNDARY}"
    )


def sensitive_markers(text: str) -> list[str]:
    lowered = text.lower()
    markers = []
    if "c:\\users\\" in lowered:
        markers.append("user-profile-path")
    if re.search(r"(?i)(?<![A-Za-z0-9_])sk-[A-Za-z0-9_-]{8,}", text):
        markers.append("api-key-prefix")
    if "bearer " in lowered:
        markers.append("bearer-token")
    return markers


def default_packet_root(output_root: Path, phase: str) -> Path:
    if phase not in ("arms", "semantic"):
        raise ValueError(f"unknown packet phase: {phase}")
    return output_root.parent / f"{output_root.name}-packets" / phase


def canonical_packet_root(packet_root: Path, *, cwd: Path | None = None) -> Path:
    base = (cwd or Path.cwd()).resolve()
    candidate = packet_root if packet_root.is_absolute() else base / packet_root
    canonical = candidate.resolve(strict=False)
    normalized = str(canonical).replace("/", "\\")
    if "user-profile-path" in sensitive_markers(normalized):
        raise ValueError("packet root must not be under a sensitive user-profile path")
    return canonical


def execute_call(
    *,
    result_dir: Path,
    packet_root: Path,
    packet_builder: Callable[[Path], None],
    prompt: str,
    harness: str,
    executable: str,
    model: str,
    identity: dict,
    source_commit: str,
    timeout_seconds: int,
    output_schema_name: str | None = None,
) -> dict:
    provider_plan = str(identity.get("provider_plan"))
    validate_live_provider_plan(provider_plan)
    validate_live_harness_executable(provider_plan, harness, executable)
    packet_root = canonical_packet_root(packet_root)
    bridge = executable.startswith("fleet-bridge://")
    phase = "arms" if identity.get("kind") == "arm" else "semantic"
    actual_effort = call_effort(
        provider_plan, phase=phase, harness=harness, bridge=bridge,
    )
    if (
        model != V3_MODELS_BY_PHASE[phase][harness]
        or
        identity.get("phase") != phase
        or identity.get("reasoning_effort") != actual_effort
        or not isinstance(identity.get("preflight_sha256"), str)
        or len(identity["preflight_sha256"]) != 64
        or not isinstance(identity.get("campaign_plan_sha256"), str)
        or len(identity["campaign_plan_sha256"]) != 64
    ):
        raise ValueError("V3 call identity is missing phase/effort/preflight/campaign binding")
    if not call_needed(result_dir):
        return json.loads((result_dir / "call.json").read_text(encoding="utf-8"))
    result_dir.mkdir(parents=True, exist_ok=True)
    packet_root.mkdir(parents=True, exist_ok=True)
    packet_dir = packet_root / f"packet-{uuid.uuid4().hex}"
    packet_builder(packet_dir)
    response_path = result_dir / "response.json"
    delivered_prompt = prompt
    if output_schema_name:
        delivered_prompt = execution_prompt(
            prompt, provider_plan=provider_plan, phase=phase, harness=harness,
            output_schema_text=(packet_dir / output_schema_name).read_text(encoding="utf-8"),
        )
    effective_prompt = (
        codex_arm_packet_prompt(packet_dir, delivered_prompt)
        if harness == "codex" and identity.get("kind") == "arm"
        else delivered_prompt
    )
    invocation_metadata: dict = {}
    stdin_text: str | None = None
    if bridge:
        invocation = fleet_bridge_invocation(
            executable=executable, harness=harness, model=model,
            packet_dir=packet_dir, prompt=effective_prompt, identity=identity,
        )
        command = invocation["command"]
        stdin_text = invocation["stdin"]
        invocation_metadata = invocation["metadata"]
    else:
        command_prompt = effective_prompt
        if harness == "codex":
            command_prompt, stdin_text = codex_prompt_transport(effective_prompt)
        command = harness_command(
            harness=harness, executable=executable, model=model, packet_dir=packet_dir,
            response_path=response_path, prompt=command_prompt,
            effort=actual_effort,
            output_schema=(packet_dir / output_schema_name) if output_schema_name and harness == "codex" else None,
        )
    started = utc_now()
    exit_code: int | None = None
    stdout = ""
    stderr = ""
    transport = "failed"
    try:
        with (FLEET_BRIDGE_LOCK if bridge else nullcontext()):
            completed = subprocess.run(
                command, cwd=packet_dir, text=True, encoding="utf-8", errors="replace",
                input=stdin_text, capture_output=True, timeout=timeout_seconds, check=False,
            )
        exit_code = completed.returncode
        stdout = completed.stdout
        stderr = completed.stderr
        if bridge and completed.returncode == 0:
            try:
                bridge_response, bridge_code, bridge_stderr = parse_fleet_bridge_stream(stdout)
                bridge_response, response_normalization = normalize_fleet_bridge_response(bridge_response)
                if response_normalization:
                    invocation_metadata["response_normalization"] = response_normalization
                if bridge_response:
                    response_path.write_text(bridge_response, encoding="utf-8", newline="\n")
                if bridge_stderr:
                    stderr = f"{stderr.rstrip()}\n{bridge_stderr}".lstrip()
                exit_code = bridge_code
                transport = "completed" if bridge_code == 0 else "failed"
            except (json.JSONDecodeError, TypeError, ValueError) as exc:
                stderr = f"{stderr.rstrip()}\ninvalid Fleet bridge stream: {exc}".lstrip()
                transport = "failed"
        else:
            transport = "completed" if completed.returncode == 0 else "failed"
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode("utf-8", errors="replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8", errors="replace")
        transport = "timeout"
    except OSError:
        shutil.rmtree(packet_dir, ignore_errors=True)
        raise
    (result_dir / "events.jsonl").write_text(stdout, encoding="utf-8", newline="\n")
    (result_dir / "stderr.txt").write_text(stderr, encoding="utf-8", newline="\n")
    response_normalization: str | None = None
    if not bridge and harness != "codex" and stdout and not response_path.is_file():
        response_text, response_normalization = normalize_plain_text_response(stdout)
        response_path.write_text(response_text, encoding="utf-8", newline="\n")
    parseable = False
    response_value: object = None
    response_hash = None
    if response_path.is_file():
        response_hash = sha256_file(response_path)
        try:
            response_value = json.loads(response_path.read_text(encoding="utf-8"))
            parseable = True
        except json.JSONDecodeError:
            pass
    schema_valid: bool | None = None
    schema_errors: list[str] = []
    if output_schema_name:
        if parseable:
            output_schema = json.loads((packet_dir / output_schema_name).read_text(encoding="utf-8"))
            schema_errors = validate_json_schema(response_value, output_schema)
            schema_valid = not schema_errors
        else:
            schema_errors = ["$: response is not parseable JSON"]
            schema_valid = False
    markers = sensitive_markers(stdout + "\n" + stderr + "\n" + (response_path.read_text(encoding="utf-8", errors="replace") if response_path.is_file() else ""))
    record = {
        "schema": "formal-rigor-live-call@1",
        **identity,
        "source_commit": source_commit,
        "provider": HARNESS_PROVIDERS[harness],
        "model": model,
        "reasoning_effort": actual_effort,
        "execution_policy": execution_policy(provider_plan),
        "packet_root": str(packet_root),
        "harness": harness,
        "harness_executable": executable,
        **({"transport_adapter": invocation_metadata} if invocation_metadata else {}),
        **({"response_normalization": response_normalization} if response_normalization else {}),
        "started_at": started,
        "completed_at": utc_now(),
        "transport": transport,
        "exit_code": exit_code,
        "json_parseable": parseable,
        **({"schema_valid": schema_valid, "schema_errors": schema_errors}
           if output_schema_name else {}),
        "response_sha256": response_hash,
        "packet_sha256": packet_manifest(packet_dir),
        "secret_screen": {"passed": not markers, "markers": markers},
        "retry_policy": "no-retry; call.json presence is terminal",
    }
    write_json(result_dir / "call.json", record)
    shutil.rmtree(packet_dir)
    return record


def prepare_v1_snapshot(destination: Path, commit: str) -> Path:
    destination.mkdir(parents=True, exist_ok=True)
    for filename in ("SKILL.md", "theory-battery.md"):
        target = destination / filename
        if target.is_file():
            continue
        repo_path = f"plugins/epistemic-skills/skills/applying-formal-rigor/{filename}"
        completed = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "show", f"{commit}:{repo_path}"],
            capture_output=True, check=True,
        )
        target.write_bytes(completed.stdout)
    return destination


def run_arm_task(
    task: ArmTask, *, output_root: Path, packet_root: Path,
    executables: dict[str, str], models: dict[str, str] | None = None,
    models_by_phase: dict[str, dict[str, str]] | None = None,
    provider_plan: str, source_commit: str, v1_source_dir: Path, timeout_seconds: int,
    preflight_sha256: str | None = None, campaign_plan_sha256: str | None = None,
) -> dict:
    run_dir = output_root / "arms" / task.arm / f"run-{task.repetition}"
    call_dir = run_dir / "calls" / task.fixture
    fixture_dir = FIXTURES_ROOT / task.fixture
    harness = arm_harness(task, provider_plan)
    model = (
        models_by_phase["arms"][harness]
        if models_by_phase is not None
        else models[harness]  # type: ignore[index]
    )
    identity = {
        "kind": "arm", "provider_plan": provider_plan, "arm": task.arm,
        "repetition": task.repetition, "fixture": task.fixture,
    }
    if provider_plan == "noncursor-degraded-v3":
        if not preflight_sha256 or not campaign_plan_sha256:
            raise ValueError("V3 arm call requires preflight and campaign identity hashes")
        identity.update({
            "phase": "arms",
            "reasoning_effort": call_effort(
                provider_plan, phase="arms", harness=harness, bridge=False,
            ),
            "preflight_sha256": preflight_sha256,
            "campaign_plan_sha256": campaign_plan_sha256,
        })
    record = execute_call(
        result_dir=call_dir,
        packet_root=packet_root,
        packet_builder=lambda packet: build_arm_packet(
            packet, task.arm, fixture_dir,
            v1_source_dir=v1_source_dir if task.arm == "v1-current" else None,
        ),
        prompt=arm_prompt(task.fixture),
        harness=harness,
        executable=executables[harness],
        model=model,
        identity=identity,
        source_commit=source_commit,
        timeout_seconds=timeout_seconds,
        output_schema_name="formal-rigor-fixture-transport.schema.json",
    )
    response = call_dir / "response.json"
    materialized = run_dir / f"{task.fixture}.response.json"
    expected_identity = {
        "kind": "arm", "provider_plan": provider_plan, "source_commit": source_commit,
        "arm": task.arm, "repetition": task.repetition, "fixture": task.fixture,
    }
    if provider_plan == "noncursor-degraded-v3":
        expected_identity.update({
            "phase": "arms", "model": model,
            "reasoning_effort": identity["reasoning_effort"],
            "preflight_sha256": preflight_sha256,
            "campaign_plan_sha256": campaign_plan_sha256,
        })
    if call_qualifies(record) and not materialize_qualified_response(
        call_dir, materialized, ROOT / "formal-rigor-fixture-transport.schema.json",
        expected_identity=expected_identity,
    ):
        raise ValueError(f"qualifying arm call has invalid materialized evidence: {task}")
    return record


def validate_adjudication(value: object, truth: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["root must be an object"]
    if value.get("adjudication") != "formal-rigor-semantic-adjudication@1":
        errors.append("invalid adjudication envelope")
    if value.get("fixture") != truth.get("fixture_id"):
        errors.append("fixture mismatch")
    if value.get("verdict") not in SEMANTIC_VERDICTS:
        errors.append("invalid verdict")
    expected_obligations = {
        (claim["id"], obligation)
        for claim in truth.get("claims", [])
        for obligation in claim.get("proof_obligations", [])
    }
    rows = value.get("obligations", [])
    if not isinstance(rows, list):
        rows = []
        errors.append("obligations must be an array")
    actual_obligations = set()
    for row in rows:
        if not isinstance(row, dict):
            errors.append("obligation row must be an object")
            continue
        actual_obligations.add((row.get("claim_id"), row.get("obligation")))
        if row.get("status") not in OBLIGATION_STATES:
            errors.append("invalid obligation status")
        if not isinstance(row.get("response_coordinates"), list) or not row.get("reason"):
            errors.append("obligation row lacks coordinates/reason")
    if actual_obligations != expected_obligations:
        errors.append("obligation set mismatch")
    expected_forbidden = {
        (claim["id"], proposition)
        for claim in truth.get("claims", [])
        for proposition in claim.get("forbidden_propositions", [])
    }
    forbidden_rows = value.get("forbidden_propositions", [])
    if not isinstance(forbidden_rows, list):
        forbidden_rows = []
        errors.append("forbidden_propositions must be an array")
    actual_forbidden = set()
    for row in forbidden_rows:
        if not isinstance(row, dict):
            errors.append("forbidden proposition row must be an object")
            continue
        actual_forbidden.add((row.get("claim_id"), row.get("proposition")))
        if not isinstance(row.get("present"), bool):
            errors.append("forbidden proposition present must be boolean")
        if not isinstance(row.get("response_coordinates"), list) or not row.get("reason"):
            errors.append("forbidden proposition row lacks coordinates/reason")
    if actual_forbidden != expected_forbidden:
        errors.append("forbidden proposition set mismatch")
    if not isinstance(value.get("coverage_limits"), list):
        errors.append("coverage_limits must be an array")
    return errors


def run_semantic_task(
    task: SemanticTask, *, output_root: Path, packet_root: Path,
    executables: dict[str, str], models: dict[str, str] | None = None,
    models_by_phase: dict[str, dict[str, str]] | None = None,
    source_commit: str, provider_plan: str, timeout_seconds: int,
    preflight_sha256: str | None = None, campaign_plan_sha256: str | None = None,
) -> dict:
    fixture_dir = FIXTURES_ROOT / task.fixture
    truth = json.loads((fixture_dir / "ground-truth.json").read_text(encoding="utf-8"))
    candidate_response = output_root / "arms" / "v2-candidate" / f"run-{task.repetition}" / f"{task.fixture}.response.json"
    call_dir = output_root / "semantic" / f"run-{task.repetition}" / task.fixture / f"seat-{task.seat}"
    if not candidate_response_qualifies(
        output_root, task, provider_plan=provider_plan, source_commit=source_commit,
        models_by_phase=models_by_phase, preflight_sha256=preflight_sha256,
        campaign_plan_sha256=campaign_plan_sha256,
    ):
        raise ValueError(f"candidate response does not match qualifying arm evidence: {candidate_response}")
    harness = semantic_harness(task, provider_plan)
    model = (
        models_by_phase["semantic"][harness]
        if models_by_phase is not None
        else models[harness]  # type: ignore[index]
    )
    identity = {
        "kind": "semantic", "provider_plan": provider_plan,
        "repetition": task.repetition, "fixture": task.fixture, "seat": task.seat,
    }
    if provider_plan == "noncursor-degraded-v3":
        if not preflight_sha256 or not campaign_plan_sha256:
            raise ValueError("V3 semantic call requires preflight and campaign identity hashes")
        identity.update({
            "phase": "semantic",
            "reasoning_effort": call_effort(
                provider_plan, phase="semantic", harness=harness, bridge=False,
            ),
            "preflight_sha256": preflight_sha256,
            "campaign_plan_sha256": campaign_plan_sha256,
        })
    record = execute_call(
        result_dir=call_dir,
        packet_root=packet_root,
        packet_builder=lambda packet: build_adjudication_packet(packet, fixture_dir, candidate_response, truth),
        prompt=semantic_prompt(task.fixture),
        harness=harness,
        executable=executables[harness],
        model=model,
        identity=identity,
        source_commit=source_commit,
        timeout_seconds=timeout_seconds,
        output_schema_name="formal-rigor-semantic-adjudication.schema.json",
    )
    response = call_dir / "response.json"
    expected_identity = {
        "kind": "semantic", "provider_plan": provider_plan, "source_commit": source_commit,
        "repetition": task.repetition, "fixture": task.fixture, "seat": task.seat,
    }
    if provider_plan == "noncursor-degraded-v3":
        expected_identity.update({
            "phase": "semantic", "model": model,
            "reasoning_effort": identity["reasoning_effort"],
            "preflight_sha256": preflight_sha256,
            "campaign_plan_sha256": campaign_plan_sha256,
        })
    errors = response_evidence_errors(
        call_dir, ROOT / "formal-rigor-semantic-adjudication.schema.json",
        expected_identity=expected_identity,
    )
    if not errors and response.is_file():
        try:
            errors = validate_adjudication(json.loads(response.read_text(encoding="utf-8")), truth)
        except json.JSONDecodeError as exc:
            errors = [f"invalid JSON: {exc}"]
    write_json(call_dir / "validation.json", {"valid": not errors, "errors": errors})
    return record


def run_parallel(tasks: list, worker: Callable[[object], dict], workers: int) -> tuple[int, int]:
    completed = 0
    failed = 0
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(worker, task): task for task in tasks}
        for future in as_completed(futures):
            task = futures[future]
            try:
                record = future.result()
                if call_qualifies(record):
                    completed += 1
                else:
                    failed += 1
                print(
                    f"{task}: {record.get('transport')} parseable={record.get('json_parseable')} "
                    f"schema_valid={record.get('schema_valid')}", flush=True,
                )
            except Exception as exc:  # fail-closed while allowing other independent calls to finish
                failed += 1
                print(f"{task}: ERROR {exc}", file=sys.stderr, flush=True)
    return completed, failed


def summarize_semantic(output_root: Path, provider_plan: str) -> dict:
    manifest_path = output_root / "campaign-plan.json"
    if not manifest_path.is_file():
        raise ValueError("semantic summary requires campaign-plan.json")
    campaign = json.loads(manifest_path.read_text(encoding="utf-8"))
    if campaign.get("schema") not in (
        "formal-rigor-live-campaign-plan@1",
        "formal-rigor-live-campaign-plan@2",
    ):
        raise ValueError("semantic summary requires a valid campaign manifest")
    if campaign.get("provider_plan") != provider_plan:
        raise ValueError("semantic summary provider plan does not match campaign manifest")
    results = []
    for repetition in (1, 2, 3):
        for fixture in fixture_ids():
            truth = json.loads((FIXTURES_ROOT / fixture / "ground-truth.json").read_text(encoding="utf-8"))
            seat_values = []
            seat_errors = []
            for seat in ("a", "b"):
                seat_dir = output_root / "semantic" / f"run-{repetition}" / fixture / f"seat-{seat}"
                response_path = seat_dir / "response.json"
                expected_identity = {
                    "kind": "semantic", "provider_plan": provider_plan,
                    "source_commit": campaign.get("source_commit"),
                    "repetition": repetition, "fixture": fixture, "seat": seat,
                }
                if campaign.get("schema") == "formal-rigor-live-campaign-plan@2":
                    harness = semantic_harness(
                        SemanticTask(repetition, fixture, seat), provider_plan,
                    )
                    expected_identity.update({
                        "phase": "semantic",
                        "model": campaign["selected_models_by_phase"]["semantic"][harness],
                        "reasoning_effort": execution_policy(provider_plan)[
                            "effort_by_phase"
                        ]["semantic"][harness],
                        "preflight_sha256": campaign["preflight_sha256"],
                        "campaign_plan_sha256": sha256_bytes(canonical_json_bytes(campaign)),
                    })
                evidence_errors = response_evidence_errors(
                    seat_dir, ROOT / "formal-rigor-semantic-adjudication.schema.json",
                    expected_identity=expected_identity,
                )
                if evidence_errors:
                    seat_values.append(None)
                    seat_errors.append(evidence_errors)
                    continue
                try:
                    value = json.loads(response_path.read_text(encoding="utf-8"))
                    errors = validate_adjudication(value, truth)
                except json.JSONDecodeError as exc:
                    value = None
                    errors = [f"invalid JSON: {exc}"]
                seat_values.append(value)
                seat_errors.append(errors)
            verdicts = [value.get("verdict") if isinstance(value, dict) and not errors else "INCONCLUSIVE" for value, errors in zip(seat_values, seat_errors)]
            if "INVALID" in verdicts:
                status = "FAIL"
            elif verdicts == ["VALID", "VALID"]:
                status = "PASS"
            elif truth.get("priority") == "P0":
                status = "FAIL"
            else:
                status = "ARBITRATION_REQUIRED"
            results.append({
                "repetition": repetition, "fixture": fixture, "priority": truth.get("priority"),
                "seat_verdicts": verdicts, "seat_errors": seat_errors, "status": status,
            })
    report = {
        "schema": "formal-rigor-semantic-summary@1",
        "provider_plan": provider_plan,
        "results": results,
        "pass": sum(row["status"] == "PASS" for row in results),
        "fail": sum(row["status"] == "FAIL" for row in results),
        "arbitration_required": sum(row["status"] == "ARBITRATION_REQUIRED" for row in results),
    }
    write_json(output_root / "semantic-summary.json", report)
    return report


def verify_arm_phase_complete(output_root: Path, campaign: dict) -> None:
    status_path = output_root / "arm-run-status.json"
    if not status_path.is_file():
        raise ValueError("semantic phase requires a complete arm-run-status.json")
    status = json.loads(status_path.read_text(encoding="utf-8"))
    expected = campaign["arm_calls"]
    campaign_sha256 = sha256_bytes(canonical_json_bytes(campaign))
    if (
        status.get("schema") != (
            "formal-rigor-live-phase-status@2"
            if campaign.get("schema") == "formal-rigor-live-campaign-plan@2"
            else "formal-rigor-live-phase-status@1"
        )
        or status.get("phase") != "arms"
        or status.get("provider_plan") != campaign.get("provider_plan")
        or status.get("source_commit") != campaign.get("source_commit")
        or status.get("planned") != expected
        or status.get("completed") != expected
        or status.get("failed") != 0
        or status.get("planned_by_harness") != campaign.get("arm_calls_by_harness")
        or (
            campaign.get("schema") == "formal-rigor-live-campaign-plan@2"
            and (
                status.get("selected_models_by_harness")
                != campaign.get("selected_models_by_phase", {}).get("arms")
                or status.get("preflight_sha256") != campaign.get("preflight_sha256")
                or status.get("campaign_plan_sha256") != campaign_sha256
            )
        )
    ):
        raise ValueError("semantic phase requires one complete qualifying arm epoch")


def default_source_commit() -> str:
    return subprocess.run(
        ["git", "-C", str(REPO_ROOT), "rev-parse", "HEAD"],
        text=True, encoding="utf-8", capture_output=True, check=True,
    ).stdout.strip()


def verify_source_state(source_commit: str, *, require_clean: bool = True) -> None:
    head = default_source_commit()
    if source_commit != head:
        raise ValueError(f"source commit {source_commit} is not checked-out HEAD {head}")
    branch = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "branch", "--show-current"],
        text=True, encoding="utf-8", capture_output=True, check=True,
    ).stdout.strip()
    if not branch:
        raise ValueError("live run requires a checked-out branch")
    remote = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "config", "--get", f"branch.{branch}.remote"],
        text=True, encoding="utf-8", capture_output=True, check=True,
    ).stdout.strip()
    merge_ref = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "config", "--get", f"branch.{branch}.merge"],
        text=True, encoding="utf-8", capture_output=True, check=True,
    ).stdout.strip()
    if not remote or remote == "." or not merge_ref.startswith("refs/heads/"):
        raise ValueError("live run requires a branch with a named remote head")
    remote_result = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "ls-remote", "--exit-code", "--heads", remote, merge_ref],
        text=True, encoding="utf-8", capture_output=True, check=True,
    ).stdout.splitlines()
    remote_heads = [
        line.split("\t", 1)[0]
        for line in remote_result
        if line.endswith(f"\t{merge_ref}")
    ]
    if len(remote_heads) != 1 or remote_heads[0] != source_commit:
        raise ValueError("live run source commit is not the fresh remote branch head")
    dco_trailers = subprocess.run(
        [
            "git", "-C", str(REPO_ROOT), "log", "-1",
            "--format=%(trailers:key=Signed-off-by,valueonly)", source_commit,
        ],
        text=True, encoding="utf-8", capture_output=True, check=True,
    ).stdout.splitlines()
    if not any(re.fullmatch(r"[^<>\r\n]+ <[^<>\s@]+@[^<>\s@]+>", trailer.strip())
               for trailer in dco_trailers):
        raise ValueError("live run source commit requires a valid DCO Signed-off-by trailer")
    if require_clean:
        status = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "status", "--porcelain"],
            text=True, encoding="utf-8", capture_output=True, check=True,
        ).stdout
        if status.strip():
            raise ValueError("live run requires a clean worktree")


def add_harness_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--codex", default=default_codex_executable())
    parser.add_argument("--codex-arm-model", default="gpt-5.6-sol")
    parser.add_argument("--codex-semantic-model", default="gpt-5.6-sol")
    parser.add_argument("--agy", default="agy")
    parser.add_argument("--agy-arm-model", default="gemini-3.6-flash-medium")
    parser.add_argument("--agy-semantic-model", default="gemini-3.1-pro-high")
    parser.add_argument("--cursor", default="cursor-agent")
    parser.add_argument("--cursor-arm-model", default="gpt-5.6-sol")
    parser.add_argument("--cursor-semantic-model", default="gpt-5.6-sol")


def harness_configuration(
    args: argparse.Namespace,
) -> tuple[dict[str, str], dict[str, dict[str, str]]]:
    return (
        {"codex": args.codex, "agy": args.agy, "cursor": args.cursor},
        {
            "arms": {
                "codex": args.codex_arm_model, "agy": args.agy_arm_model,
                "cursor": args.cursor_arm_model,
            },
            "semantic": {
                "codex": args.codex_semantic_model, "agy": args.agy_semantic_model,
                "cursor": args.cursor_semantic_model,
            },
        },
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    plan = sub.add_parser("plan")
    plan.add_argument("--provider-plan", choices=tuple(PROVIDER_PLANS), default=DEFAULT_PROVIDER_PLAN)

    arms = sub.add_parser("run-arms")
    arms.add_argument("--output-root", type=Path, required=True)
    arms.add_argument("--packet-root", type=Path, default=None)
    add_harness_arguments(arms)
    arms.add_argument("--workers", type=int, default=4)
    arms.add_argument("--timeout-seconds", type=int, default=600)
    arms.add_argument("--source-commit", default=None)
    arms.add_argument("--v1-commit", default=None)
    arms.add_argument("--provider-plan", choices=tuple(PROVIDER_PLANS), required=True)
    arms.add_argument("--arm", action="append", choices=tuple(ARM_PROMPTS))
    arms.add_argument("--fixture", action="append", choices=fixture_ids())
    arms.add_argument("--repetition", action="append", type=int, choices=(1, 2, 3))

    semantic = sub.add_parser("run-semantic")
    semantic.add_argument("--output-root", type=Path, required=True)
    semantic.add_argument("--packet-root", type=Path, default=None)
    add_harness_arguments(semantic)
    semantic.add_argument("--workers", type=int, default=4)
    semantic.add_argument("--timeout-seconds", type=int, default=600)
    semantic.add_argument("--source-commit", default=None)
    semantic.add_argument("--v1-commit", default=None)
    semantic.add_argument("--provider-plan", choices=tuple(PROVIDER_PLANS), required=True)
    semantic.add_argument("--fixture", action="append", choices=fixture_ids())
    semantic.add_argument("--repetition", action="append", type=int, choices=(1, 2, 3))
    semantic.add_argument("--seat", action="append", choices=("a", "b"))

    summary = sub.add_parser("summarize-semantic")
    summary.add_argument("--output-root", type=Path, required=True)
    summary.add_argument("--provider-plan", choices=tuple(PROVIDER_PLANS), required=True)
    args = parser.parse_args()

    if args.command == "plan":
        arm_counts = {
            harness: sum(arm_harness(task, args.provider_plan) == harness for task in full_arm_plan())
            for harness in HARNESS_PROVIDERS
        }
        semantic_counts = {
            harness: sum(semantic_harness(task, args.provider_plan) == harness for task in full_semantic_plan())
            for harness in HARNESS_PROVIDERS
        }
        print(json.dumps({
            "provider_plan": args.provider_plan,
            "arm_calls": len(full_arm_plan()), "arm_calls_by_harness": arm_counts,
            "semantic_calls": len(full_semantic_plan()),
            "semantic_calls_by_harness": semantic_counts,
            "maximum_before_arbitration": 418,
        }, indent=2))
        return 0
    if args.command == "summarize-semantic":
        report = summarize_semantic(args.output_root, args.provider_plan)
        print(json.dumps({key: report[key] for key in ("pass", "fail", "arbitration_required")}, indent=2))
        return 0

    validate_live_provider_plan(args.provider_plan)
    phase = "arms" if args.command == "run-arms" else "semantic"
    packet_root = canonical_packet_root(
        args.packet_root or default_packet_root(args.output_root, phase), cwd=Path.cwd(),
    )
    source_commit = args.source_commit or default_source_commit()
    verify_source_state(source_commit)
    executables, models_by_phase = harness_configuration(args)
    validate_live_harness_configuration(args.provider_plan, executables)
    preflight_receipt = agy_preflight(
        executables["agy"], models_by_phase, execution_policy(args.provider_plan),
    )
    baseline_manifest = json.loads((RED_BASELINE_ROOT / "manifest.json").read_text(encoding="utf-8"))
    v1_commit = args.v1_commit or baseline_manifest["repository_head"]
    campaign = ensure_campaign_plan(
        args.output_root, provider_plan=args.provider_plan, source_commit=source_commit,
        v1_commit=v1_commit, models_by_phase=models_by_phase,
        preflight_receipt=preflight_receipt,
    )
    preflight_sha256 = campaign["preflight_sha256"]
    campaign_plan_sha256 = sha256_bytes(canonical_json_bytes(campaign))
    preflight_path = args.output_root / "metadata" / "agy-preflight.json"
    if preflight_path.is_file():
        if json.loads(preflight_path.read_text(encoding="utf-8")) != preflight_receipt:
            raise ValueError("existing AGY preflight receipt does not match campaign identity")
    else:
        write_json(preflight_path, preflight_receipt)
    if args.command == "run-arms":
        v1_source = prepare_v1_snapshot(args.output_root / "metadata" / "v1-source", v1_commit)
        tasks = filter_arm_tasks(
            full_arm_plan(),
            arms=set(args.arm) if args.arm else None,
            fixtures=set(args.fixture) if args.fixture else None,
            repetitions=set(args.repetition) if args.repetition else None,
        )
        completed, failed = run_parallel(
            tasks,
            lambda task: run_arm_task(
                task, output_root=args.output_root, packet_root=packet_root,
                executables=executables, models_by_phase=models_by_phase,
                source_commit=source_commit,
                provider_plan=args.provider_plan, v1_source_dir=v1_source,
                timeout_seconds=args.timeout_seconds,
                preflight_sha256=preflight_sha256,
                campaign_plan_sha256=campaign_plan_sha256,
            ),
            args.workers,
        )
        write_json(args.output_root / "arm-run-status.json", phase_status(
            phase="arms", tasks=tasks, provider_plan=args.provider_plan,
            source_commit=source_commit, models_by_phase=models_by_phase,
            completed=completed, failed=failed, preflight_sha256=preflight_sha256,
            campaign_plan_sha256=campaign_plan_sha256,
        ))
        print(f"arms: planned={len(tasks)} completed={completed} failed={failed}")
        return 0 if failed == 0 else 1
    if args.command == "run-semantic":
        verify_arm_phase_complete(args.output_root, campaign)
        tasks = filter_semantic_tasks(
            full_semantic_plan(),
            fixtures=set(args.fixture) if args.fixture else None,
            repetitions=set(args.repetition) if args.repetition else None,
            seats=set(args.seat) if args.seat else None,
        )
        completed, failed = run_parallel(
            tasks,
            lambda task: run_semantic_task(
                task, output_root=args.output_root, packet_root=packet_root,
                executables=executables, models_by_phase=models_by_phase,
                source_commit=source_commit,
                provider_plan=args.provider_plan, timeout_seconds=args.timeout_seconds,
                preflight_sha256=preflight_sha256,
                campaign_plan_sha256=campaign_plan_sha256,
            ),
            args.workers,
        )
        write_json(args.output_root / "semantic-run-status.json", phase_status(
            phase="semantic", tasks=tasks, provider_plan=args.provider_plan,
            source_commit=source_commit, models_by_phase=models_by_phase,
            completed=completed, failed=failed, preflight_sha256=preflight_sha256,
            campaign_plan_sha256=campaign_plan_sha256,
        ))
        print(f"semantic: planned={len(tasks)} completed={completed} failed={failed}")
        return 0 if failed == 0 else 1
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
