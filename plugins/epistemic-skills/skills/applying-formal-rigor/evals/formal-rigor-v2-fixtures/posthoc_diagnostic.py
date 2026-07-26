#!/usr/bin/env python3
"""Fail-closed, non-promotable structural view of excluded V3 arm evidence."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent
FIXTURES_ROOT = ROOT / "fixtures"
TRANSPORT_SCHEMA = ROOT / "formal-rigor-fixture-transport.schema.json"
NON_RELEASE_FIELDS = {
    "post_hoc": True,
    "source_epoch_excluded": True,
    "release_eligible": False,
    "release_credit": "none",
}
UNAVAILABLE_PARODY_ARMS = (
    "parody-always-decide",
    "parody-full-ceremony",
    "parody-jargon-only",
)
DIAGNOSTIC_PROVIDER_PLAN = "noncursor-degraded-v3"
SEMANTIC_MODELS = {
    "codex": "gpt-5.6-sol",
    "agy": "gemini-3.1-pro-high",
}
SEMANTIC_EFFORT = "high"
SEMANTIC_TIMEOUT_SECONDS = 720


class SemanticExtractionError(ValueError):
    def __init__(self, message: str, schema_errors: list[str], adjudication_errors: list[str]):
        super().__init__(message)
        self.schema_errors = schema_errors
        self.adjudication_errors = adjudication_errors


def _load_sibling(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / f"{name}.py")
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


score = _load_sibling("score")
run_live = _load_sibling("run_live")


def semantic_tasks(manifest: dict) -> list[dict]:
    """Return the two cross-provider diagnostic seats for every available candidate."""
    rows = manifest.get("rows")
    if rows is None and isinstance(manifest.get("inventory"), list):
        rows = manifest["inventory"]
    if not isinstance(rows, list):
        raise ValueError("view manifest rows are missing")
    candidates = [
        row for row in rows
        if isinstance(row, dict)
        and row.get("arm") == "v2-candidate"
        and row.get("classification") != "missing_no_content"
    ]
    candidates.sort(key=lambda row: (row.get("repetition"), row.get("fixture")))
    tasks: list[dict] = []
    seen: set[tuple[int, str]] = set()
    for row in candidates:
        repetition, fixture = row.get("repetition"), row.get("fixture")
        if not isinstance(repetition, int) or not isinstance(fixture, str):
            raise ValueError("candidate view has invalid coordinate")
        coordinate = (repetition, fixture)
        if coordinate in seen:
            raise ValueError("candidate view coordinate is duplicated")
        seen.add(coordinate)
        origin_harness = row.get("origin_harness")
        if origin_harness not in run_live.HARNESS_PROVIDERS:
            raise ValueError("candidate view has unknown origin harness")
        for seat in ("a", "b"):
            semantic = run_live.SemanticTask(repetition, fixture, seat)
            judge_harness = run_live.semantic_harness(semantic, DIAGNOSTIC_PROVIDER_PLAN)
            if judge_harness == origin_harness:
                raise ValueError("semantic judge must use a different provider harness")
            tasks.append({
                "repetition": repetition,
                "fixture": fixture,
                "seat": seat,
                "origin_harness": origin_harness,
                "origin_provider": row.get("origin_provider") or run_live.HARNESS_PROVIDERS[origin_harness],
                "judge_harness": judge_harness,
                "judge_provider": run_live.HARNESS_PROVIDERS[judge_harness],
                "model": SEMANTIC_MODELS[judge_harness],
                "effort": SEMANTIC_EFFORT,
                "source_view": row.get("view"),
                "view_sha256": row.get("view_sha256"),
            })
    harness_counts = Counter(task["judge_harness"] for task in tasks)
    candidate_counts = Counter(repetition for repetition, _fixture in seen)
    if harness_counts != {"codex": 42, "agy": 88}:
        raise ValueError(f"semantic seat map drifted: {dict(harness_counts)}")
    if candidate_counts != {1: 22, 2: 21, 3: 22}:
        raise ValueError(f"candidate availability drifted: {dict(candidate_counts)}")
    return tasks


def agy_semantic_command(
    *, agy: str, model: str, prompt: str, effort: str = SEMANTIC_EFFORT,
) -> list[str]:
    """Build the preregistered aggregate-JSON AGY semantic command."""
    return [
        agy, "--sandbox", "--dangerously-skip-permissions", "--mode", "plan",
        "--add-dir", ".", "--model", model, "--effort", effort,
        "--output-format", "json", "--print-timeout", "10m", "--print", prompt,
    ]


def semantic_preflight(
    executables: dict[str, str], *, runner: Callable[..., object] = subprocess.run,
) -> dict:
    """Capture the exact CLI versions and AGY catalog used by the frozen plan."""
    calls = {}
    for name, command in (
        ("codex", [executables["codex"], "--version"]),
        ("agy", [executables["agy"], "--version"]),
        ("agy_catalog", [executables["agy"], "models"]),
    ):
        result = runner(command, capture_output=True, check=False)
        if int(getattr(result, "returncode")) != 0:
            raise ValueError(f"{name} semantic preflight failed")
        calls[name] = _as_bytes(getattr(result, "stdout", b""))
    codex_version = calls["codex"].decode("utf-8", errors="replace").strip()
    agy_version = calls["agy"].decode("utf-8", errors="replace").strip()
    if codex_version != "codex-cli 0.144.6":
        raise ValueError("diagnostic requires Codex CLI 0.144.6")
    if agy_version != "1.1.7":
        raise ValueError("diagnostic requires AGY CLI 1.1.7")
    catalog = [
        line.strip()
        for line in calls["agy_catalog"].decode("utf-8", errors="replace").splitlines()
        if line.strip()
    ]
    if len(catalog) != len(set(catalog)):
        raise ValueError("AGY semantic model catalog contains duplicate identifiers")
    if SEMANTIC_MODELS["agy"] not in catalog:
        raise ValueError("registered AGY semantic model is unavailable")
    return {
        "codex": {"version": codex_version},
        "agy": {
            "version": agy_version,
            "catalog_sha256": sha256_bytes(calls["agy_catalog"]),
            "selected_model": SEMANTIC_MODELS["agy"],
        },
    }


def _json_coordinates(value: object, coordinate: str = "$", *, encoded: bool = False):
    if isinstance(value, dict):
        if "adjudication" in value:
            yield value, coordinate, encoded
        for key, child in value.items():
            child_coordinate = f"{coordinate}.{key}"
            yield from _json_coordinates(child, child_coordinate, encoded=encoded)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _json_coordinates(child, f"{coordinate}[{index}]", encoded=encoded)
    elif isinstance(value, str):
        stripped = value.strip()
        if stripped.startswith(("{", "[")):
            try:
                decoded = json.loads(stripped)
            except json.JSONDecodeError:
                return
            yield from _json_coordinates(decoded, coordinate, encoded=True)


def extract_agy_adjudication(raw: bytes, fixture: str) -> tuple[bytes, dict]:
    """Extract exactly one valid semantic envelope from AGY aggregate JSON."""
    try:
        aggregate = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("AGY aggregate response is not one UTF-8 JSON value") from exc
    candidates = list(_json_coordinates(aggregate))
    if len(candidates) != 1:
        raise ValueError(f"AGY aggregate must contain exactly one adjudication object; found {len(candidates)}")
    value, coordinate, encoded = candidates[0]
    schema_errors, adjudication_errors = _semantic_validation(value, fixture)
    errors = schema_errors + adjudication_errors
    if errors:
        raise SemanticExtractionError(
            f"AGY adjudication is invalid: {errors}",
            schema_errors, adjudication_errors,
        )

    direct = coordinate == "$" and not encoded
    response_bytes = raw.strip() if direct else _canonical_json_bytes(value)
    method = (
        "direct_json_object" if direct
        else "string_encoded_json_object" if encoded
        else "recursively_contained_json_object"
    )
    return response_bytes, {
        "json_coordinate": coordinate,
        "extraction_method": method,
        "aggregate_sha256": sha256_bytes(raw),
        "response_sha256": sha256_bytes(response_bytes),
    }


def _semantic_validation(value: object, fixture: str) -> tuple[list[str], list[str]]:
    schema = _read_json(
        ROOT / "formal-rigor-semantic-adjudication.schema.json",
        "frozen semantic adjudication schema",
    )
    truth = _read_json(FIXTURES_ROOT / fixture / "ground-truth.json", "fixture truth")
    schema_errors = run_live.validate_json_schema(value, schema)
    adjudication_errors = run_live.validate_adjudication(value, truth)
    if not isinstance(value, dict):
        return schema_errors, adjudication_errors
    expected_obligations = [
        (claim["id"], obligation)
        for claim in truth.get("claims", [])
        for obligation in claim.get("proof_obligations", [])
    ]
    actual_obligations = [
        (row.get("claim_id"), row.get("obligation"))
        for row in value.get("obligations", []) if isinstance(row, dict)
    ] if isinstance(value.get("obligations"), list) else []
    if Counter(actual_obligations) != Counter(expected_obligations):
        adjudication_errors.append("every expected obligation must occur exactly once")
    expected_forbidden = [
        (claim["id"], proposition)
        for claim in truth.get("claims", [])
        for proposition in claim.get("forbidden_propositions", [])
    ]
    actual_forbidden = [
        (row.get("claim_id"), row.get("proposition"))
        for row in value.get("forbidden_propositions", []) if isinstance(row, dict)
    ] if isinstance(value.get("forbidden_propositions"), list) else []
    if Counter(actual_forbidden) != Counter(expected_forbidden):
        adjudication_errors.append("every expected forbidden proposition must occur exactly once")
    obligation_rows = value.get("obligations")
    forbidden_rows = value.get("forbidden_propositions")
    if value.get("verdict") == "VALID" and isinstance(obligation_rows, list) and isinstance(forbidden_rows, list):
        if not all(isinstance(row, dict) and row.get("status") == "SATISFIED" for row in obligation_rows):
            adjudication_errors.append("VALID contains a non-satisfied obligation")
        if any(isinstance(row, dict) and row.get("present") for row in forbidden_rows):
            adjudication_errors.append("VALID contains a forbidden proposition")
    return schema_errors, adjudication_errors


def _semantic_plan(
    *, output_root: Path, tasks: list[dict], implementation_commit: str,
    preflight_receipt: dict,
) -> dict:
    manifest_path = output_root / "diagnostic-manifest.json"
    inventory_path = output_root / "arm-inventory.json"
    manifest = _read_json(manifest_path, "diagnostic manifest")
    schema_path = ROOT / "formal-rigor-semantic-adjudication.schema.json"
    schema_text = schema_path.read_text(encoding="utf-8")
    schema_hash = sha256_bytes(schema_path.read_bytes())
    rubric_hashes: dict[str, str] = {}
    frozen_tasks = []
    for task in tasks:
        fixture = task["fixture"]
        truth = _read_json(FIXTURES_ROOT / fixture / "ground-truth.json", "fixture truth")
        rubric_hashes[fixture] = sha256_bytes(
            _canonical_json_bytes(run_live.adjudication_rubric(truth))
        )
        base_prompt = run_live.semantic_prompt(fixture)
        prompt = run_live.execution_prompt(
            base_prompt, provider_plan=DIAGNOSTIC_PROVIDER_PLAN,
            phase="semantic", harness=task["judge_harness"],
            output_schema_text=schema_text,
        )
        frozen_tasks.append({**task, "prompt_sha256": sha256_bytes(prompt.encode("utf-8"))})
    return {
        "schema": "formal-rigor-posthoc-semantic-plan@1",
        **NON_RELEASE_FIELDS,
        "implementation_commit": implementation_commit,
        "source_coordinate": manifest.get("source_coordinate"),
        "source_commit": manifest.get("source_commit"),
        "source_tree_sha256": manifest.get("source_tree_sha256"),
        "diagnostic_manifest_sha256": sha256_bytes(manifest_path.read_bytes()),
        "view_manifest_sha256": sha256_bytes(inventory_path.read_bytes()),
        "semantic_schema_sha256": schema_hash,
        "rubric_sha256_by_fixture": dict(sorted(rubric_hashes.items())),
        "tasks": frozen_tasks,
        "model_effort_matrix": {
            harness: {"model": SEMANTIC_MODELS[harness], "effort": SEMANTIC_EFFORT}
            for harness in ("codex", "agy")
        },
        "cli_preflight": preflight_receipt,
        "agy_catalog_receipt": preflight_receipt.get("agy"),
        "command_policy": {
            "codex": "ephemeral-read-only-stdin-native-schema-no-user-config-rules-plugins-apps",
            "agy": "sandbox-plan-cwd-packet-aggregate-json-exact-schema-in-prompt",
        },
        "timeout_policy": {
            "subprocess_seconds": SEMANTIC_TIMEOUT_SECONDS,
            "agy_print_timeout": "10m",
            "retry_policy": "at-most-once",
        },
    }


def _task_call_path(output_root: Path, task: dict) -> Path:
    return (
        output_root / "semantic-diagnostic" / f"run-{task['repetition']}"
        / task["fixture"] / f"seat-{task['seat']}" / "call.json"
    )


def _validate_packet_root(packet_root: Path, source_coordinate: object) -> None:
    if not isinstance(source_coordinate, str) or not source_coordinate:
        raise ValueError("diagnostic manifest source coordinate is missing")
    source_root = Path(source_coordinate).resolve()
    if not source_root.is_dir():
        raise ValueError("diagnostic source coordinate is not an existing directory")
    packets = Path(packet_root).resolve(strict=False)
    if (
        packets == source_root
        or packets.is_relative_to(source_root)
        or source_root.is_relative_to(packets)
    ):
        raise ValueError("packet root must not equal, contain, or be contained by the source root")


def _verify_call_layout(
    output_root: Path, tasks: list[dict], plan_sha256: str, plan: dict,
) -> None:
    expected = {_task_call_path(output_root, task).resolve(): task for task in tasks}
    semantic_root = output_root / "semantic-diagnostic"
    if semantic_root.exists():
        for call_path in semantic_root.rglob("call.json"):
            if call_path.resolve() not in expected:
                raise ValueError(f"orphan semantic call seal: {call_path}")
            task = expected[call_path.resolve()]
            call = _read_json(call_path, "semantic call seal")
            for field in (
                "repetition", "fixture", "seat", "origin_harness", "origin_provider",
                "judge_harness", "judge_provider", "model", "effort", "source_view",
                "view_sha256", "prompt_sha256",
            ):
                if call.get(field) != task.get(field):
                    raise ValueError(f"semantic call identity {field!r} does not match plan")
            if call.get("semantic_plan_sha256") != plan_sha256:
                raise ValueError("semantic call plan hash does not match frozen plan")
            for field in (
                "implementation_commit", "source_coordinate", "source_commit",
                "source_tree_sha256",
            ):
                if call.get(field) != plan.get(field):
                    raise ValueError(f"semantic call binding {field!r} does not match plan")
            if call.get("retry_policy") != "at-most-once":
                raise ValueError("semantic call retry policy does not match frozen plan")
            for field, value in NON_RELEASE_FIELDS.items():
                if call.get(field) != value:
                    raise ValueError(f"semantic call non-release field {field!r} drifted")
            for artifact_name, hash_field in (
                ("stdout.bin", "stdout_sha256"),
                ("stderr.bin", "stderr_sha256"),
            ):
                artifact_path = call_path.parent / artifact_name
                if not artifact_path.is_file():
                    raise ValueError(f"semantic call retained artifact is missing: {artifact_name}")
                if sha256_bytes(artifact_path.read_bytes()) != call.get(hash_field):
                    raise ValueError(f"semantic call retained artifact hash mismatch: {artifact_name}")
            response_path = call_path.parent / "response.json"
            if call.get("response_sha256") is not None:
                if not response_path.is_file():
                    raise ValueError("semantic call retained response is missing")
                if sha256_bytes(response_path.read_bytes()) != call.get("response_sha256"):
                    raise ValueError("semantic call retained response hash mismatch")
            if call.get("packet_manifest_sha256") != sha256_bytes(
                _canonical_json_bytes(call.get("packet_manifest"))
            ):
                raise ValueError("semantic call packet manifest hash mismatch")
            attempt = _read_json(call_path.parent / "attempt.json", "semantic attempt reservation")
            if attempt.get("identity") != {
                field: task[field] for field in (
                    "repetition", "fixture", "seat", "origin_harness", "origin_provider",
                    "judge_harness", "judge_provider", "model", "effort", "source_view",
                    "view_sha256", "prompt_sha256",
                )
            } or attempt.get("semantic_plan_sha256") != plan_sha256:
                raise ValueError("semantic attempt reservation does not match task and plan")
        for attempt_path in semantic_root.rglob("attempt.json"):
            if not (attempt_path.parent / "call.json").is_file():
                raise ValueError(f"incomplete at-most-once semantic attempt: {attempt_path}")


def _as_bytes(value: object) -> bytes:
    if value is None:
        return b""
    if isinstance(value, bytes):
        return value
    return str(value).encode("utf-8", errors="replace")


def _exclusive_write_json(path: Path, value: object) -> None:
    """Atomically reserve an at-most-once identity without replacing evidence."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, sort_keys=True)
        stream.write("\n")


def _execute_semantic_task(
    *, output_root: Path, task: dict, plan: dict, plan_sha256: str,
    executables: dict[str, str], runner: Callable[..., object], packet_root: Path,
) -> dict:
    call_path = _task_call_path(output_root, task)
    if call_path.is_file():
        return _read_json(call_path, "semantic call seal")
    call_dir = call_path.parent
    if call_dir.exists() and any(call_dir.iterdir()):
        raise ValueError(f"semantic call directory is incomplete and cannot be retried: {call_dir}")
    call_dir.mkdir(parents=True, exist_ok=True)
    identity = {
        key: task[key] for key in (
            "repetition", "fixture", "seat", "origin_harness", "origin_provider",
            "judge_harness", "judge_provider", "model", "effort", "source_view",
            "view_sha256", "prompt_sha256",
        )
    }
    try:
        _exclusive_write_json(call_dir / "attempt.json", {
            "schema": "formal-rigor-posthoc-semantic-attempt@1",
            **NON_RELEASE_FIELDS, "identity": identity,
            "semantic_plan_sha256": plan_sha256, "retry_policy": "at-most-once",
        })
    except FileExistsError as exc:
        raise ValueError("semantic call identity is already reserved") from exc
    packet_root.mkdir(parents=True, exist_ok=True)
    packet = Path(tempfile.mkdtemp(
        prefix=f"r{task['repetition']}-{task['fixture']}-{task['seat']}-",
        dir=packet_root,
    ))
    packet.rmdir()
    try:
        return _execute_semantic_task_in_packet(
            output_root=output_root, task=task, plan=plan,
            plan_sha256=plan_sha256, executables=executables, runner=runner,
            packet=packet, call_path=call_path, identity=identity,
        )
    finally:
        shutil.rmtree(packet, ignore_errors=True)


def _execute_semantic_task_in_packet(
    *, output_root: Path, task: dict, plan: dict, plan_sha256: str,
    executables: dict[str, str], runner: Callable[..., object], packet: Path,
    call_path: Path, identity: dict,
) -> dict:
    call_dir = call_path.parent
    candidate = output_root / str(task["source_view"])
    if not candidate.is_file() or sha256_bytes(candidate.read_bytes()) != task["view_sha256"]:
        raise ValueError("candidate semantic view does not match frozen task hash")
    truth = _read_json(FIXTURES_ROOT / task["fixture"] / "ground-truth.json", "fixture truth")
    run_live.build_adjudication_packet(
        packet, FIXTURES_ROOT / task["fixture"], candidate, truth,
    )
    packet_files = run_live.packet_manifest(packet)
    schema_path = ROOT / "formal-rigor-semantic-adjudication.schema.json"
    schema_text = schema_path.read_text(encoding="utf-8")
    prompt = run_live.execution_prompt(
        run_live.semantic_prompt(task["fixture"]),
        provider_plan=DIAGNOSTIC_PROVIDER_PLAN, phase="semantic",
        harness=task["judge_harness"], output_schema_text=schema_text,
    )
    if sha256_bytes(prompt.encode("utf-8")) != task["prompt_sha256"]:
        raise ValueError("semantic prompt does not match frozen task hash")
    pending_response = call_dir / "codex-output.tmp"
    stdin = b""
    if task["judge_harness"] == "codex":
        prompt_arg, prompt_stdin = run_live.codex_prompt_transport(prompt)
        stdin = prompt_stdin.encode("utf-8")
        command = run_live.codex_command(
            codex=executables["codex"], model=task["model"], packet_dir=packet,
            response_path=pending_response, prompt=prompt_arg,
            output_schema=schema_path, effort=task["effort"],
        )
    else:
        command = agy_semantic_command(
            agy=executables["agy"], model=task["model"], prompt=prompt,
            effort=task["effort"],
        )
    started_at = run_live.utc_now()
    start = time.monotonic()
    stdout = stderr = b""
    exit_code: int | None = None
    transport = "failed"
    transport_error: str | None = None
    try:
        completed = runner(
            command, cwd=str(packet), input=stdin, capture_output=True,
            timeout=SEMANTIC_TIMEOUT_SECONDS, check=False,
        )
        stdout = _as_bytes(getattr(completed, "stdout", b""))
        stderr = _as_bytes(getattr(completed, "stderr", b""))
        exit_code = int(getattr(completed, "returncode"))
        transport = "completed" if exit_code == 0 else "failed"
    except subprocess.TimeoutExpired as exc:
        stdout, stderr = _as_bytes(exc.stdout), _as_bytes(exc.stderr)
        transport, transport_error = "timed_out", "subprocess timeout"
    except OSError as exc:
        transport_error = f"{type(exc).__name__}: {exc}"
    elapsed = time.monotonic() - start
    (call_dir / "stdout.bin").write_bytes(stdout)
    (call_dir / "stderr.bin").write_bytes(stderr)
    response_bytes: bytes | None = None
    extraction: dict | None = None
    parse_error: str | None = None
    schema_errors: list[str] = []
    adjudication_errors: list[str] = []
    if transport == "completed":
        try:
            if task["judge_harness"] == "agy":
                response_bytes, extraction = extract_agy_adjudication(stdout, task["fixture"])
            elif pending_response.is_file():
                response_bytes = pending_response.read_bytes().strip()
            else:
                parse_error = "Codex did not write --output-last-message"
        except ValueError as exc:
            parse_error = str(exc)
            schema_errors = list(getattr(exc, "schema_errors", []))
            adjudication_errors = list(getattr(exc, "adjudication_errors", []))
    if pending_response.exists():
        pending_response.unlink()
    value: object | None = None
    if response_bytes is not None:
        try:
            value = json.loads(response_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            parse_error = f"semantic response is not UTF-8 JSON: {exc}"
        else:
            schema_errors, adjudication_errors = _semantic_validation(value, task["fixture"])
    screened = b"\n".join((stdout, stderr, response_bytes or b"")).decode("utf-8", errors="replace")
    markers = run_live.sensitive_markers(screened)
    valid = (
        transport == "completed" and parse_error is None and not schema_errors
        and not adjudication_errors and not markers and isinstance(value, dict)
    )
    if valid and response_bytes is not None:
        (call_dir / "response.json").write_bytes(response_bytes)
    record = {
        "schema": "formal-rigor-posthoc-semantic-call@1",
        **NON_RELEASE_FIELDS,
        **identity,
        "implementation_commit": plan["implementation_commit"],
        "source_coordinate": plan["source_coordinate"],
        "source_commit": plan["source_commit"],
        "source_tree_sha256": plan["source_tree_sha256"],
        "semantic_plan_sha256": plan_sha256,
        "retry_policy": "at-most-once",
        "transport": transport,
        "transport_error": transport_error,
        "started_at": started_at,
        "finished_at": run_live.utc_now(),
        "elapsed_seconds": elapsed,
        "exit_code": exit_code,
        "stdout_sha256": sha256_bytes(stdout),
        "stderr_sha256": sha256_bytes(stderr),
        "response_sha256": sha256_bytes(response_bytes) if response_bytes is not None else None,
        "json_parseable": value is not None,
        "schema_valid": value is not None and not schema_errors,
        "adjudication_valid": valid,
        "parse_error": parse_error,
        "schema_errors": schema_errors,
        "adjudication_errors": adjudication_errors,
        "extraction": extraction,
        "secret_screen": {"passed": not markers, "markers": markers},
        "packet_manifest": packet_files,
        "packet_manifest_sha256": sha256_bytes(_canonical_json_bytes(packet_files)),
        "command_sha256": sha256_bytes(_canonical_json_bytes(command)),
        "prompt_transport": "stdin" if task["judge_harness"] == "codex" else "argv",
    }
    _write_json(call_path, record)
    return record


def run_semantic(
    output_root: Path, *, harness: str, executables: dict[str, str],
    implementation_commit: str, preflight_receipt: dict,
    runner: Callable[..., object] = subprocess.run,
    source_verifier: Callable[..., None] = run_live.verify_source_state,
    packet_root: Path | None = None,
) -> dict:
    """Freeze and execute one provider's diagnostic seats without retries."""
    output_root = Path(output_root)
    if harness not in ("codex", "agy"):
        raise ValueError("diagnostic semantic harness must be codex or agy")
    inventory = _read_json(output_root / "arm-inventory.json", "view manifest")
    tasks = semantic_tasks(inventory)
    diagnostic_manifest = _read_json(
        output_root / "diagnostic-manifest.json", "diagnostic manifest",
    )
    packets = packet_root or output_root.parent / f"{output_root.name}-packets" / "semantic-diagnostic"
    _validate_packet_root(packets, diagnostic_manifest.get("source_coordinate"))
    expected_plan = _semantic_plan(
        output_root=output_root, tasks=tasks,
        implementation_commit=implementation_commit,
        preflight_receipt=preflight_receipt,
    )
    plan_path = output_root / "semantic-plan.json"
    if plan_path.exists():
        if _read_json(plan_path, "semantic plan") != expected_plan:
            raise ValueError("existing semantic plan does not match frozen diagnostic identity")
    else:
        _write_json(plan_path, expected_plan)
    plan_sha = sha256_bytes(_canonical_json_bytes(expected_plan))
    _verify_call_layout(output_root, expected_plan["tasks"], plan_sha, expected_plan)
    selected = [task for task in expected_plan["tasks"] if task["judge_harness"] == harness]
    pending = [task for task in selected if not _task_call_path(output_root, task).is_file()]
    if pending:
        source_verifier(implementation_commit, require_clean=True)
    executed = 0
    for task in selected:
        if _task_call_path(output_root, task).is_file():
            continue
        _execute_semantic_task(
            output_root=output_root, task=task, plan=expected_plan,
            plan_sha256=plan_sha, executables=executables, runner=runner,
            packet_root=packets,
        )
        executed += 1
    if packets.exists() and not any(packets.iterdir()):
        packets.rmdir()
    terminal = sum(_task_call_path(output_root, task).is_file() for task in selected)
    return {
        "harness": harness, "planned": len(selected), "executed": executed,
        "terminal": terminal, "semantic_plan_sha256": plan_sha,
    }


def _semantic_outcome(verdicts: list[str], priority: str) -> str:
    if "INVALID" in verdicts:
        return "FAIL"
    if verdicts == ["VALID", "VALID"]:
        return "PASS"
    if priority == "P0":
        return "FAIL"
    return "ARBITRATION_REQUIRED"


def summarize_semantic_diagnostic(output_root: Path) -> dict:
    """Aggregate terminal diagnostic seats without inventing arbitration outcomes."""
    output_root = Path(output_root)
    plan = _read_json(output_root / "semantic-plan.json", "semantic plan")
    tasks = plan.get("tasks")
    if not isinstance(tasks, list):
        raise ValueError("semantic plan tasks are missing")
    plan_sha = sha256_bytes(_canonical_json_bytes(plan))
    _verify_call_layout(output_root, tasks, plan_sha, plan)
    truth = score.load_inventory(FIXTURES_ROOT)
    grouped: dict[tuple[int, str], list[dict]] = defaultdict(list)
    terminal_seats = valid_seats = 0
    validation_errors = []
    verdict_counts: Counter[str] = Counter()
    judge_breakdown: dict[str, Counter[str]] = defaultdict(Counter)
    for task in tasks:
        call_path = _task_call_path(output_root, task)
        entry = {"task": task, "verdict": "INCONCLUSIVE", "valid": False}
        if call_path.is_file():
            terminal_seats += 1
            call = _read_json(call_path, "semantic call seal")
            entry["call"] = call
            response_path = call_path.parent / "response.json"
            if call.get("adjudication_valid") is True and response_path.is_file():
                response_bytes = response_path.read_bytes()
                if sha256_bytes(response_bytes) != call.get("response_sha256"):
                    validation_errors.append({
                        "repetition": task["repetition"], "fixture": task["fixture"],
                        "seat": task["seat"], "judge_harness": task["judge_harness"],
                        "error": "response hash mismatch",
                    })
                else:
                    response = _read_json(response_path, "semantic response")
                    schema_errors, adjudication_errors = _semantic_validation(
                        response, task["fixture"],
                    )
                    markers = run_live.sensitive_markers(
                        response_bytes.decode("utf-8", errors="replace")
                    )
                    if schema_errors or adjudication_errors or markers:
                        validation_errors.append({
                            "repetition": task["repetition"], "fixture": task["fixture"],
                            "seat": task["seat"], "judge_harness": task["judge_harness"],
                            "error": "sealed response failed revalidation",
                            "schema_errors": schema_errors,
                            "adjudication_errors": adjudication_errors,
                            "secret_markers": markers,
                        })
                    else:
                        entry.update(verdict=response["verdict"], valid=True)
                        valid_seats += 1
                        verdict_counts[response["verdict"]] += 1
                        judge_breakdown[task["judge_provider"]][
                            f"verdict_{response['verdict']}"
                        ] += 1
            else:
                validation_errors.append({
                    "repetition": task["repetition"], "fixture": task["fixture"],
                    "seat": task["seat"], "judge_harness": task["judge_harness"],
                    "transport": call.get("transport"),
                    "parse_error": call.get("parse_error"),
                    "schema_errors": call.get("schema_errors", []),
                    "adjudication_errors": call.get("adjudication_errors", []),
                })
        judge_breakdown[task["judge_provider"]]["planned"] += 1
        judge_breakdown[task["judge_provider"]]["terminal"] += int(call_path.is_file())
        judge_breakdown[task["judge_provider"]]["valid"] += int(entry["valid"])
        grouped[(task["repetition"], task["fixture"])].append(entry)
    outcomes: Counter[str] = Counter()
    dissent = []
    p0_findings = []
    candidates = []
    origin_breakdown: dict[str, Counter[str]] = defaultdict(Counter)
    for (repetition, fixture), entries in sorted(grouped.items()):
        entries.sort(key=lambda entry: entry["task"]["seat"])
        verdicts = [entry["verdict"] for entry in entries]
        priority = truth[fixture].get("priority")
        outcome = _semantic_outcome(verdicts, priority)
        outcomes[outcome] += 1
        origin_provider = entries[0]["task"]["origin_provider"]
        origin_breakdown[origin_provider][outcome] += 1
        row = {
            "repetition": repetition, "fixture": fixture, "priority": priority,
            "origin_provider": origin_provider, "verdicts": verdicts,
            "outcome": outcome,
        }
        candidates.append(row)
        if len(set(verdicts)) > 1:
            dissent.append(row)
        if priority == "P0" and outcome != "PASS":
            p0_findings.append(row)
    expected = {
        (repetition, fixture)
        for repetition in (1, 2, 3)
        for fixture in sorted(truth)
    }
    missing = [
        {"repetition": repetition, "fixture": fixture, "reason": "source candidate unavailable"}
        for repetition, fixture in sorted(expected - set(grouped))
    ]
    report = {
        "schema": "formal-rigor-posthoc-semantic-diagnostic-report@1",
        **NON_RELEASE_FIELDS,
        "semantic_plan_sha256": plan_sha,
        "outcomes": dict(sorted(outcomes.items())),
        "verdicts": dict(sorted(verdict_counts.items())),
        "completion_coverage": {
            "planned_candidates": len(expected), "available_candidates": len(grouped),
            "missing_candidates": len(missing), "planned_seats": len(tasks),
            "terminal_seats": terminal_seats, "valid_seats": valid_seats,
        },
        "missing_candidates": missing,
        "candidates": candidates,
        "validation_errors": validation_errors,
        "dissent": dissent,
        "p0_findings": p0_findings,
        "by_origin_provider": {
            provider: dict(sorted(counts.items()))
            for provider, counts in sorted(origin_breakdown.items())
        },
        "by_judge_provider": {
            provider: dict(sorted(counts.items()))
            for provider, counts in sorted(judge_breakdown.items())
        },
    }
    _write_json(output_root / "semantic-diagnostic-report.json", report)
    return report


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def tree_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        file_hash = hashlib.sha256(path.read_bytes()).hexdigest().encode("ascii")
        digest.update(relative + b"\0" + file_hash + b"\n")
    return digest.hexdigest()


def _byte_offset(text: str, character_offset: int) -> int:
    return len(text[:character_offset].encode("utf-8"))


def extract_identical_frames(raw: bytes, fixture: str, schema: dict) -> tuple[bytes, dict]:
    """Return one byte-identical frame only from an unambiguous repeated stream."""
    if not raw:
        raise ValueError("empty response cannot contain repeated frames")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("response is not UTF-8") from exc
    decoder = json.JSONDecoder()
    index = 0
    frames: list[bytes] = []
    while True:
        while index < len(text) and text[index].isspace():
            index += 1
        if index == len(text):
            break
        start = index
        try:
            value, index = decoder.raw_decode(text, index)
        except json.JSONDecodeError as exc:
            raise ValueError("response has a non-JSON prefix, suffix, or frame") from exc
        frame = raw[_byte_offset(text, start):_byte_offset(text, index)]
        if not frame:
            raise ValueError("response contains an empty frame")
        errors = run_live.validate_json_schema(value, schema)
        if errors:
            raise ValueError(f"frame violates transport schema: {errors}")
        if not isinstance(value, dict) or value.get("response") != "formal-rigor-fixture-response@1":
            raise ValueError("frame response marker does not match frozen transport")
        if value.get("fixture") != fixture:
            raise ValueError("frame fixture identity does not match coordinate")
        frames.append(frame)
    if len(frames) < 2:
        raise ValueError("repeated-frame normalization requires at least two frames")
    if any(frame != frames[0] for frame in frames[1:]):
        raise ValueError("repeated frames are not byte-identical")
    return frames[0], {
        "normalization": "normalized_identical_repeated_frames",
        "frame_count": len(frames),
        "raw_sha256": sha256_bytes(raw),
        "frame_sha256": sha256_bytes(frames[0]),
        "all_frames_byte_identical": True,
    }


def _read_json(path: Path, label: str) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{label} is unreadable: {path}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object: {path}")
    return value


def _canonical_json_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _ensure_expected_identity(call: dict, task: dict, campaign: dict) -> None:
    expected = {
        "schema": "formal-rigor-live-call@1",
        "kind": "arm",
        "provider_plan": campaign.get("provider_plan"),
        "source_commit": campaign.get("source_commit"),
        "arm": task["arm"],
        "repetition": task["repetition"],
        "fixture": task["fixture"],
        "phase": "arms",
        "model": task.get("model"),
        "reasoning_effort": task.get("effort"),
    }
    if campaign.get("schema") == "formal-rigor-live-campaign-plan@2":
        expected.update({
            "preflight_sha256": campaign.get("preflight_sha256"),
            "campaign_plan_sha256": sha256_bytes(_canonical_json_bytes(campaign)),
        })
    for field, value in expected.items():
        if call.get(field) != value:
            raise ValueError(f"call identity {field!r} does not match campaign task")
    if call.get("secret_screen", {}).get("passed") is not True:
        raise ValueError("call secret screen did not pass")


def _ensure_qualifying_call(call: dict) -> None:
    if call.get("json_parseable") is not True or call.get("schema_valid") is not True:
        raise ValueError("single-frame call is not parseable and schema-valid")


def _ensure_completed_transport(call: dict) -> None:
    if call.get("transport") != "completed":
        raise ValueError("content-bearing call transport did not complete")


def _relative(source_root: Path, path: Path) -> str:
    return path.relative_to(source_root).as_posix()


def inventory_source_calls(source_root: Path, expected_pin: str) -> list[dict]:
    """Read every planned arm call without writing any derived artifact."""
    source_root = Path(source_root)
    if not source_root.is_dir():
        raise ValueError("source root is missing")
    if tree_sha256(source_root) != expected_pin:
        raise ValueError("source root content pin does not match")
    campaign = _read_json(source_root / "campaign-plan.json", "campaign plan")
    if campaign.get("schema") != "formal-rigor-live-campaign-plan@2":
        raise ValueError("diagnostic requires a V3 campaign plan")
    tasks = campaign.get("arm_tasks")
    if not isinstance(tasks, list) or not tasks:
        raise ValueError("campaign arm_tasks is missing or empty")
    schema = _read_json(TRANSPORT_SCHEMA, "frozen transport schema")
    known_fixtures = score.load_inventory(FIXTURES_ROOT)
    rows: list[dict] = []
    coordinates: set[tuple[str, int, str]] = set()
    for task in tasks:
        if not isinstance(task, dict):
            raise ValueError("campaign arm task is not an object")
        arm, repetition, fixture = task.get("arm"), task.get("repetition"), task.get("fixture")
        if not isinstance(arm, str) or not isinstance(repetition, int) or not isinstance(fixture, str):
            raise ValueError("campaign arm task has invalid coordinate")
        if fixture not in known_fixtures:
            raise ValueError(f"campaign names an unknown fixture: {fixture}")
        coordinate = (arm, repetition, fixture)
        if coordinate in coordinates:
            raise ValueError("campaign arm task coordinate is duplicated")
        coordinates.add(coordinate)
        call_dir = source_root / "arms" / arm / f"run-{repetition}" / "calls" / fixture
        call_path = call_dir / "call.json"
        raw_path = call_dir / "response.json"
        row: dict[str, Any] = {
            "arm": arm,
            "repetition": repetition,
            "fixture": fixture,
            "origin_harness": task.get("harness"),
            "origin_provider": None,
            "source_call": _relative(source_root, call_path),
            "source_raw": _relative(source_root, raw_path),
            "view": f"views/{arm}/run-{repetition}/{fixture}.response.json",
            "call_sha256": None,
            "raw_sha256": None,
            "view_sha256": None,
            "normalization": None,
            "normalization_proof": None,
            "exclusion_reason": None,
        }
        if not call_path.is_file() and not raw_path.is_file():
            row.update(classification="missing_no_content", exclusion_reason="no terminal call or response artifact")
            rows.append(row)
            continue
        if not call_path.is_file():
            raise ValueError(f"response exists without call evidence: {raw_path}")
        call = _read_json(call_path, "call evidence")
        row["call_sha256"] = sha256_bytes(call_path.read_bytes())
        row["origin_harness"] = call.get("harness", row["origin_harness"])
        row["origin_provider"] = call.get("provider")
        _ensure_expected_identity(call, task, campaign)
        if not raw_path.is_file() or raw_path.read_bytes() == b"":
            row.update(classification="missing_no_content", exclusion_reason="terminal call retained no model content")
            rows.append(row)
            continue
        _ensure_completed_transport(call)
        raw = raw_path.read_bytes()
        row["raw_sha256"] = sha256_bytes(raw)
        if call.get("response_sha256") != row["raw_sha256"]:
            raise ValueError(f"response hash does not match terminal call: {raw_path}")
        try:
            response = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            response = None
        if response is not None:
            _ensure_qualifying_call(call)
            errors = run_live.validate_json_schema(response, schema)
            if errors or not isinstance(response, dict) or response.get("response") != "formal-rigor-fixture-response@1" or response.get("fixture") != fixture:
                raise ValueError(f"original response is not a valid matching transport frame: {raw_path}")
            row.update(
                classification="original_qualifying",
                normalization="original_qualifying",
                normalization_proof={"raw_sha256": row["raw_sha256"], "frame_count": 1},
            )
        else:
            frame, proof = extract_identical_frames(raw, fixture, schema)
            row.update(
                classification="normalized_identical_repeated_frames",
                normalization=proof["normalization"],
                normalization_proof=proof,
                _view_bytes=frame,
            )
        rows.append(row)
    return rows


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def _counts(rows: list[dict]) -> dict[str, int]:
    content = [row for row in rows if row["classification"] != "missing_no_content"]
    scores = [row for row in content if isinstance(row.get("structural_score"), dict)]
    return {
        "planned": len(rows),
        "content_bearing": len(content),
        "normalized": sum(row["classification"] == "normalized_identical_repeated_frames" for row in rows),
        "structurally_scorable": len(scores),
        "structurally_passing": sum(score["structural_pass"] for score in (row["structural_score"] for row in scores)),
        "missing_no_content": sum(row["classification"] == "missing_no_content" for row in rows),
    }


def _group_counts(rows: list[dict], fields: tuple[str, ...]) -> dict[str, dict]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        label = "|".join(str(row.get(field)) for field in fields)
        groups[label].append(row)
    return {label: _counts(groups[label]) for label in sorted(groups)}


def _structural_report(rows: list[dict], source_pin: str, source_commit: str) -> dict:
    truth = score.load_inventory(FIXTURES_ROOT)
    enriched = []
    for row in rows:
        copied = dict(row)
        fixture_truth = truth.get(row["fixture"])
        copied["priority"] = fixture_truth.get("priority") if fixture_truth else None
        copied["fixture_kind"] = fixture_truth.get("kind") if fixture_truth else None
        enriched.append(copied)
    candidate = [row for row in enriched if row["arm"] == "v2-candidate"]
    candidate_available = [row for row in candidate if row["classification"] != "missing_no_content"]
    candidate_without_normalized = [row for row in candidate_available if row["classification"] == "original_qualifying"]
    parody_rows = [
        row for row in enriched
        if str(row["arm"]).startswith("parody-")
        and row["classification"] != "missing_no_content"
    ]
    observed_parodies = {}
    for arm in sorted({row["arm"] for row in parody_rows}):
        arm_rows = [row for row in parody_rows if row["arm"] == arm]
        observed_parodies[arm] = {
            **_counts(arm_rows),
            "intended_failure_evidence": [
                {"fixture": row["fixture"], "dimensions_failed": row["structural_score"].get("dimensions_failed", [])}
                for row in arm_rows if isinstance(row.get("structural_score"), dict)
                and not row["structural_score"].get("structural_pass")
            ],
        }
    candidate_gates = {}
    for label, selector in {
        "P0": lambda row: row.get("priority") == "P0",
        "trap": lambda row: row.get("fixture_kind") == "trap",
        "control": lambda row: row.get("fixture_kind") == "control",
    }.items():
        chosen = [row for row in candidate_available if selector(row)]
        candidate_gates[label] = _counts(chosen)
    return {
        "schema": "formal-rigor-posthoc-structural-report@1",
        **NON_RELEASE_FIELDS,
        "source_tree_sha256": source_pin,
        "source_commit": source_commit,
        "conditional_on_content": _counts([row for row in enriched if row["classification"] != "missing_no_content"]),
        "intent_to_test": _counts(enriched),
        "candidate_sensitivity_excluding_normalized": _counts(candidate_without_normalized),
        "candidate_available": _counts(candidate_available),
        "candidate_gate_components": candidate_gates,
        "by_arm": _group_counts(enriched, ("arm",)),
        "by_repetition": _group_counts(enriched, ("repetition",)),
        "by_fixture": _group_counts(enriched, ("fixture",)),
        "by_origin_provider": _group_counts(enriched, ("origin_provider",)),
        "by_priority": _group_counts(enriched, ("priority",)),
        "by_fixture_kind": _group_counts(enriched, ("fixture_kind",)),
        "observed_parody_failure_evidence": observed_parodies,
        "unavailable_parody_arms": list(UNAVAILABLE_PARODY_ARMS),
    }


def prepare_structural(source_root: Path, output_root: Path, expected_pin: str, source_commit: str) -> dict:
    """Create the diagnostic-only structural view after all source checks succeed."""
    source_root, output_root = Path(source_root), Path(output_root)
    if not source_root.is_dir():
        raise ValueError("source root is missing")
    source_resolved, output_resolved = source_root.resolve(), output_root.resolve()
    if output_resolved == source_resolved or output_resolved.is_relative_to(source_resolved):
        raise ValueError("diagnostic output must not be nested inside the source root")
    if output_root.exists() and any(output_root.iterdir()):
        raise ValueError("diagnostic output root must be new or empty")
    rows = inventory_source_calls(source_root, expected_pin)
    campaign = _read_json(source_root / "campaign-plan.json", "campaign plan")
    if campaign.get("source_commit") != source_commit:
        raise ValueError("requested source commit does not match campaign plan")
    if tree_sha256(source_root) != expected_pin:
        raise ValueError("source root changed during inventory")
    truth = score.load_inventory(FIXTURES_ROOT)
    output_root.mkdir(parents=True, exist_ok=True)
    for row in rows:
        if row["classification"] == "missing_no_content":
            continue
        raw_path = source_root / row["source_raw"]
        view_bytes = row.pop("_view_bytes", raw_path.read_bytes())
        view_path = output_root / row["view"]
        view_path.parent.mkdir(parents=True, exist_ok=True)
        view_path.write_bytes(view_bytes)
        row["view_sha256"] = sha256_bytes(view_bytes)
        response = json.loads(view_bytes.decode("utf-8"))
        if row["fixture"] not in truth:
            raise ValueError(f"unknown fixture in campaign: {row['fixture']}")
        row["structural_score"] = score.score_fixture(truth[row["fixture"]], response)
        score_path = output_root / "scores" / row["arm"] / f"run-{row['repetition']}" / f"{row['fixture']}.score.json"
        _write_json(score_path, {**NON_RELEASE_FIELDS, "source_coordinate": row["source_raw"], "score": row["structural_score"]})
    manifest = {
        "schema": "formal-rigor-posthoc-diagnostic-manifest@1",
        **NON_RELEASE_FIELDS,
        "source_coordinate": str(source_root.resolve()),
        "source_tree_sha256": expected_pin,
        "source_commit": source_commit,
        "planned_arm_calls": len(rows),
    }
    inventory = {"schema": "formal-rigor-posthoc-arm-inventory@1", **NON_RELEASE_FIELDS, "rows": rows}
    report = _structural_report(rows, expected_pin, source_commit)
    _write_json(output_root / "diagnostic-manifest.json", manifest)
    _write_json(output_root / "arm-inventory.json", inventory)
    _write_json(output_root / "structural-report.json", report)
    return {"manifest": manifest, "inventory": rows, "report": report}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    prepare = commands.add_parser("prepare-structural")
    prepare.add_argument("--source-root", type=Path, required=True)
    prepare.add_argument("--output-root", type=Path, required=True)
    prepare.add_argument("--expected-pin", required=True)
    prepare.add_argument("--source-commit", required=True)

    semantic = commands.add_parser("run-semantic")
    semantic.add_argument("--output-root", type=Path, required=True)
    semantic.add_argument("--harness", choices=("codex", "agy"), required=True)
    semantic.add_argument("--implementation-commit", required=True)
    semantic.add_argument("--codex", default=run_live.default_codex_executable())
    semantic.add_argument("--agy", default="agy")
    semantic.add_argument("--packet-root", type=Path)

    summary = commands.add_parser("summarize")
    summary.add_argument("--output-root", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "prepare-structural":
        result = prepare_structural(
            args.source_root, args.output_root, args.expected_pin, args.source_commit,
        )
        print(json.dumps(result["report"], indent=2, sort_keys=True))
        return 0
    if args.command == "run-semantic":
        executables = {"codex": args.codex, "agy": args.agy}
        receipt = semantic_preflight(executables)
        result = run_semantic(
            args.output_root, harness=args.harness, executables=executables,
            implementation_commit=args.implementation_commit,
            preflight_receipt=receipt, packet_root=args.packet_root,
        )
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    report = summarize_semantic_diagnostic(args.output_root)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
