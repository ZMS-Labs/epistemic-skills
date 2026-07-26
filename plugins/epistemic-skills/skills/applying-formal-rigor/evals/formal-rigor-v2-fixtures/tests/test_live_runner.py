#!/usr/bin/env python3
"""Deterministic tests for the resumable live-battery runner."""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import tempfile
import threading
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "run_live.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_runner():
    require(RUNNER_PATH.is_file(), f"missing live runner: {RUNNER_PATH}")
    spec = importlib.util.spec_from_file_location("formal_rigor_live_runner", RUNNER_PATH)
    require(spec is not None and spec.loader is not None, "cannot load live runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    runner = load_runner()
    require(
        "api-key-prefix" not in runner.sensitive_markers("durable-loss-risk-adjusted"),
        "ordinary words ending in risk- must not trip the API-key screen",
    )
    synthetic_key = "s" + "k-" + ("x" * 24)
    require(
        "api-key-prefix" in runner.sensitive_markers(f"credential {synthetic_key}"),
        "standalone API-key-shaped values must still fail closed",
    )
    require(runner.default_codex_executable() == ("codex.cmd" if os.name == "nt" else "codex"),
            "default Codex executable must use the runnable Windows command shim")
    require(runner.DEFAULT_PROVIDER_PLAN == "frozen-three-provider",
            "the historical three-provider allocation must remain the named default plan")
    require(set(runner.PROVIDER_PLANS) == {
        "frozen-three-provider", "noncursor-degraded-v1", "noncursor-degraded-v2",
        "noncursor-degraded-v3",
    }, "the runner must expose the frozen plan and all degraded protocol identities")
    for historical_plan in (
        "frozen-three-provider", "noncursor-degraded-v1", "noncursor-degraded-v2",
    ):
        rejected_historical_live_plan = False
        try:
            runner.validate_live_provider_plan(historical_plan)
        except ValueError:
            rejected_historical_live_plan = True
        require(rejected_historical_live_plan,
                f"historical provider plan remained runnable: {historical_plan}")
    runner.validate_live_provider_plan("noncursor-degraded-v3")
    require(runner.candidate_harness(1, "noncursor-degraded-v1") == "codex" and
            runner.candidate_harness(2, "noncursor-degraded-v1") == "agy" and
            runner.candidate_harness(3, "noncursor-degraded-v1") == "codex",
            "degraded candidate allocation must use the declared non-Cursor rotation")
    require(runner.arm_harness(
        runner.ArmTask("parody-closed-taxonomy", 1, "tm-01-false-mvd"),
        "noncursor-degraded-v1",
    ) == "codex", "degraded parody allocation must use its named provider plan")
    require(runner.semantic_harness(
        runner.SemanticTask(1, "tm-01-false-mvd", "a"), "noncursor-degraded-v1",
    ) == "agy", "degraded semantic allocation must use its named provider plan")
    tasks = runner.full_arm_plan()
    counts: dict[str, int] = {}
    for task in tasks:
        counts[task.arm] = counts.get(task.arm, 0) + 1
    require(len(tasks) == 286, f"full arm plan count is {len(tasks)}, expected 286")
    require(counts["neutral"] == 44 and counts["v1-current"] == 44,
            "baseline plan must add exactly run-2 and run-3")
    require(counts["v2-candidate"] == 66, "candidate plan must contain three 22-fixture runs")
    require(sum(counts[arm] for arm in runner.PARODY_ARMS) == 132,
            "all six parody arms must contain 22 calls")
    provider_counts: dict[str, int] = {}
    for task in tasks:
        provider = runner.arm_harness(task)
        provider_counts[provider] = provider_counts.get(provider, 0) + 1
    require(provider_counts == {"codex": 66, "agy": 110, "cursor": 110},
            f"arm harness allocation drifted: {provider_counts}")
    require(len(runner.full_semantic_plan()) == 132,
            "semantic plan must contain two isolated seats for each of 66 candidate responses")
    semantic_provider_counts: dict[str, int] = {}
    for task in runner.full_semantic_plan():
        provider = runner.semantic_harness(task)
        semantic_provider_counts[provider] = semantic_provider_counts.get(provider, 0) + 1
        require(provider != runner.candidate_harness(task.repetition),
                "semantic seat must not use its candidate response's harness")
    require(semantic_provider_counts == {"codex": 44, "agy": 44, "cursor": 44},
            f"semantic harness allocation drifted: {semantic_provider_counts}")
    degraded_arm_counts = {
        harness: sum(runner.arm_harness(task, "noncursor-degraded-v1") == harness for task in tasks)
        for harness in runner.HARNESS_PROVIDERS
    }
    require(degraded_arm_counts == {"codex": 154, "agy": 132, "cursor": 0},
            f"degraded arm allocation drifted: {degraded_arm_counts}")
    degraded_semantic_counts = {
        harness: sum(
            runner.semantic_harness(task, "noncursor-degraded-v1") == harness
            for task in runner.full_semantic_plan()
        )
        for harness in runner.HARNESS_PROVIDERS
    }
    require(degraded_semantic_counts == {"codex": 44, "agy": 88, "cursor": 0},
            f"degraded semantic allocation drifted: {degraded_semantic_counts}")
    for provider_plan in (
        "noncursor-degraded-v1", "noncursor-degraded-v2", "noncursor-degraded-v3",
    ):
        arm_counts = {
            harness: sum(runner.arm_harness(task, provider_plan) == harness for task in tasks)
            for harness in runner.HARNESS_PROVIDERS
        }
        semantic_counts = {
            harness: sum(
                runner.semantic_harness(task, provider_plan) == harness
                for task in runner.full_semantic_plan()
            )
            for harness in runner.HARNESS_PROVIDERS
        }
        require(arm_counts == {"codex": 154, "agy": 132, "cursor": 0},
                f"{provider_plan} arm allocation drifted: {arm_counts}")
        require(semantic_counts == {"codex": 44, "agy": 88, "cursor": 0},
                f"{provider_plan} semantic allocation drifted: {semantic_counts}")
    for task in runner.full_semantic_plan():
        require(
            runner.semantic_harness(task, "noncursor-degraded-v1") !=
            runner.candidate_harness(task.repetition, "noncursor-degraded-v1"),
            "every degraded semantic seat must use the provider opposite its candidate response",
        )
    campaign_models = {
        "arms": {
            "codex": "gpt-5.6-sol", "agy": "gemini-3.6-flash-medium",
            "cursor": "gpt-5.6-sol",
        },
        "semantic": {
            "codex": "gpt-5.6-sol", "agy": "gemini-3.1-pro-high",
            "cursor": "gpt-5.6-sol",
        },
    }
    historical_campaign_models = {
        "codex": "gpt-5.6-sol", "agy": "gemini-3.1-pro-high",
        "cursor": "gpt-5.6-sol",
    }
    preflight_receipt = {
        "schema": "formal-rigor-agy-preflight@1", "agy_version": "1.1.7",
        "catalog_sha256": "c" * 64,
        "selected_models_by_phase": {
            "arms": "gemini-3.6-flash-medium", "semantic": "gemini-3.1-pro-high",
        },
    }
    preflight_sha256 = runner.sha256_bytes(runner.canonical_json_bytes(preflight_receipt))
    v3_campaign = runner.campaign_plan(
        provider_plan="noncursor-degraded-v3", source_commit="a" * 40,
        v1_commit="b" * 40, models_by_phase=campaign_models,
        preflight_receipt=preflight_receipt,
    )
    require(v3_campaign["schema"] == "formal-rigor-live-campaign-plan@2",
            "V3 must use the phase-model campaign schema")
    require(v3_campaign["arm_calls"] == 286 and v3_campaign["semantic_calls"] == 132,
            "v3 campaign identity must retain the exact 286/132 phase counts")
    require(v3_campaign["arm_calls_by_harness"] == {"codex": 154, "agy": 132, "cursor": 0}
            and v3_campaign["semantic_calls_by_harness"] == {
                "codex": 44, "agy": 88, "cursor": 0,
            }, "v3 campaign identity must retain its zero-Cursor allocation")
    require(v3_campaign["selected_models_by_phase"] == {
        "arms": {"codex": "gpt-5.6-sol", "agy": "gemini-3.6-flash-medium"},
        "semantic": {"codex": "gpt-5.6-sol", "agy": "gemini-3.1-pro-high"},
    }, "V3 campaign must pin exact models independently by phase")
    require(v3_campaign["preflight_sha256"] == preflight_sha256,
            "campaign identity must bind the AGY capability receipt")
    campaign_sha256 = runner.sha256_bytes(runner.canonical_json_bytes(v3_campaign))
    require(all("model" in task and "effort" in task for task in
                v3_campaign["arm_tasks"] + v3_campaign["semantic_tasks"]),
            "every planned task must pin model and effort")
    require(any(
        task["harness"] == "agy" and task["model"] == "gemini-3.6-flash-medium"
        and task["effort"] == "medium" for task in v3_campaign["arm_tasks"]
    ) and any(
        task["harness"] == "agy" and task["model"] == "gemini-3.1-pro-high"
        and task["effort"] == "high" for task in v3_campaign["semantic_tasks"]
    ), "planned AGY tasks do not retain the phase-specific model/effort matrix")
    rejected_v3_model_substitution = False
    substituted_models = json.loads(json.dumps(campaign_models))
    substituted_models["arms"]["agy"] = "gemini-3.5-flash-medium"
    try:
        runner.campaign_plan(
            provider_plan="noncursor-degraded-v3", source_commit="a" * 40,
            v1_commit="b" * 40, models_by_phase=substituted_models,
            preflight_receipt=preflight_receipt,
        )
    except ValueError:
        rejected_v3_model_substitution = True
    require(rejected_v3_model_substitution,
            "V3 campaign accepted a catalog-valid but unregistered model substitution")
    original_run = runner.subprocess.run
    def preflight_run(command, *args, **kwargs):
        if command == ["agy", "--version"]:
            return SimpleNamespace(returncode=0, stdout="1.1.7\n", stderr="")
        if command == ["agy", "models"]:
            return SimpleNamespace(
                returncode=0,
                stdout="gemini-3.6-flash-medium\ngemini-3.1-pro-high\n",
                stderr="",
            )
        raise AssertionError(f"unexpected preflight command: {command}")
    try:
        runner.subprocess.run = preflight_run
        observed_preflight = runner.agy_preflight(
            "agy", campaign_models, runner.execution_policy("noncursor-degraded-v3"),
        )
        require(observed_preflight["agy_version"] == "1.1.7" and
                observed_preflight["selected_models_by_phase"] == {
                    "arms": "gemini-3.6-flash-medium",
                    "semantic": "gemini-3.1-pro-high",
                }, "AGY preflight did not bind exact phase models")
        rejected_missing_catalog_model = False
        runner.subprocess.run = lambda command, *args, **kwargs: SimpleNamespace(
            returncode=0, stdout=("1.1.7\n" if command[-1] == "--version"
                                  else "gemini-3.1-pro-high\n"), stderr="",
        )
        try:
            runner.agy_preflight(
                "agy", campaign_models, runner.execution_policy("noncursor-degraded-v3"),
            )
        except ValueError:
            rejected_missing_catalog_model = True
        require(rejected_missing_catalog_model,
                "AGY preflight accepted a missing arm model")
        rejected_wrong_agy_version = False
        runner.subprocess.run = lambda command, *args, **kwargs: SimpleNamespace(
            returncode=0, stdout=("1.1.8\n" if command[-1] == "--version"
                                  else "gemini-3.6-flash-medium\ngemini-3.1-pro-high\n"),
            stderr="",
        )
        try:
            runner.agy_preflight(
                "agy", campaign_models, runner.execution_policy("noncursor-degraded-v3"),
            )
        except ValueError:
            rejected_wrong_agy_version = True
        require(rejected_wrong_agy_version,
                "AGY preflight accepted a CLI version outside the V3 protocol")
    finally:
        runner.subprocess.run = original_run
    execution_policy = v3_campaign["execution_policy"]
    require(execution_policy["effort_by_phase"]["arms"] == {
        "codex": "high", "agy": "medium", "cursor": "provider-model-default",
    }, "v2 campaign identity must pin arm effort by harness")
    require(execution_policy["effort_by_phase"]["semantic"] == {
        "codex": "high", "agy": "high", "cursor": "provider-model-default",
    }, "v2 campaign identity must pin semantic effort by harness")
    require(execution_policy["packet_root_policy"] ==
            "output-adjacent-phase-specific;reject-sensitive-user-profile-path",
            "campaign identity must pin packet-root delivery policy")
    require(execution_policy["output_schema_delivery"]["arms"] == {
        "codex": "native-cli-output-schema",
        "agy": "exact-schema-in-immediate-prompt",
        "cursor": "exact-schema-in-immediate-prompt",
    }, "v2 campaign identity must pin arm output-schema delivery by harness")
    require(execution_policy["output_schema_delivery"]["semantic"] == {
        "codex": "native-cli-output-schema",
        "agy": "exact-schema-in-immediate-prompt",
        "cursor": "exact-schema-in-immediate-prompt",
    }, "v2 campaign identity must pin semantic output-schema delivery by harness")
    with tempfile.TemporaryDirectory() as campaign_tmp:
        campaign_root = Path(campaign_tmp)
        campaign = runner.ensure_campaign_plan(
            campaign_root, provider_plan="noncursor-degraded-v1", source_commit="a" * 40,
            v1_commit="b" * 40, models=historical_campaign_models,
        )
        require(campaign["schema"] == "formal-rigor-live-campaign-plan@1",
                "campaign manifest must carry its stable schema marker")
        require(campaign["provider_plan"] == "noncursor-degraded-v1",
                "campaign manifest must record the selected provider plan")
        require(campaign["selected_models"] == {
            "codex": "gpt-5.6-sol", "agy": "gemini-3.1-pro-high",
        }, "campaign manifest must retain models only for active plan harnesses")
        require(campaign["arm_calls"] == 286 and campaign["semantic_calls"] == 132 and
                len(campaign["arm_tasks"]) == 286 and len(campaign["semantic_tasks"]) == 132,
                "campaign manifest must retain the exact full task allocation")
        require(campaign["arm_calls_by_harness"] == degraded_arm_counts and
                campaign["semantic_calls_by_harness"] == degraded_semantic_counts,
                "campaign manifest must retain the declared degraded provider counts")
        require(runner.ensure_campaign_plan(
            campaign_root, provider_plan="noncursor-degraded-v1", source_commit="a" * 40,
            v1_commit="b" * 40, models=historical_campaign_models,
        ) == campaign, "an identical campaign identity must be resumable")
        for changed_kwargs in (
            {"provider_plan": "frozen-three-provider"},
            {"source_commit": "c" * 40},
            {"v1_commit": "d" * 40},
            {"models": {**historical_campaign_models, "codex": "gpt-5.7-sol"}},
        ):
            rejected = False
            try:
                runner.ensure_campaign_plan(
                    campaign_root,
                    provider_plan=changed_kwargs.get("provider_plan", "noncursor-degraded-v1"),
                    source_commit=changed_kwargs.get("source_commit", "a" * 40),
                    v1_commit=changed_kwargs.get("v1_commit", "b" * 40),
                    models=changed_kwargs.get("models", historical_campaign_models),
                )
            except ValueError:
                rejected = True
            require(rejected, "campaign manifest must reject any identity mismatch before a call")
    with tempfile.TemporaryDirectory() as orphan_tmp:
        orphan_root = Path(orphan_tmp)
        orphan_call = orphan_root / "arms" / "v2-candidate" / "run-1" / "calls" / "fixture" / "call.json"
        orphan_call.parent.mkdir(parents=True)
        orphan_call.write_text("{}", encoding="utf-8")
        rejected = False
        try:
            runner.ensure_campaign_plan(
                orphan_root, provider_plan="noncursor-degraded-v1", source_commit="a" * 40,
                v1_commit="b" * 40, models=historical_campaign_models,
            )
        except ValueError:
            rejected = True
        require(rejected, "an output root with terminal calls and no campaign manifest must fail closed")
    phase_status = runner.phase_status(
        phase="arms", tasks=[runner.ArmTask("v2-candidate", 1, "tm-01-false-mvd")],
        provider_plan="noncursor-degraded-v1", source_commit="a" * 40,
        models=historical_campaign_models, completed=1, failed=0,
    )
    require(phase_status["provider_plan"] == "noncursor-degraded-v1",
            "phase-status records must retain the provider-plan identity")
    with tempfile.TemporaryDirectory() as phase_tmp:
        phase_root = Path(phase_tmp)
        complete_status = {
            "schema": "formal-rigor-live-phase-status@1",
            "phase": "arms",
            "provider_plan": campaign["provider_plan"],
            "source_commit": campaign["source_commit"],
            "planned_by_harness": campaign["arm_calls_by_harness"],
            "planned": campaign["arm_calls"],
            "completed": campaign["arm_calls"],
            "failed": 0,
        }
        runner.write_json(phase_root / "arm-run-status.json", complete_status)
        runner.verify_arm_phase_complete(phase_root, campaign)
        runner.write_json(phase_root / "arm-run-status.json", {**complete_status, "failed": 1})
        rejected_incomplete = False
        try:
            runner.verify_arm_phase_complete(phase_root, campaign)
        except ValueError:
            rejected_incomplete = True
        require(rejected_incomplete,
                "semantic phase gate accepted an arm status with terminal failures")
    source_commit = "a" * 40
    branch_name = "codex/v3-rigor-gauntlet"

    def source_state_run(remote_head: str, dco_trailers: str):
        def fake_run(command, *args, **kwargs):
            if command[-2:] == ["branch", "--show-current"]:
                return SimpleNamespace(stdout=f"{branch_name}\n")
            if command[-3:] == ["config", "--get", f"branch.{branch_name}.remote"]:
                return SimpleNamespace(stdout="origin\n")
            if command[-3:] == ["config", "--get", f"branch.{branch_name}.merge"]:
                return SimpleNamespace(stdout=f"refs/heads/{branch_name}\n")
            if "ls-remote" in command:
                return SimpleNamespace(stdout=f"{remote_head}\trefs/heads/{branch_name}\n")
            if "log" in command:
                return SimpleNamespace(stdout=dco_trailers)
            raise AssertionError(f"unexpected source-state command: {command}")
        return fake_run

    original_default_source_commit = runner.default_source_commit
    original_subprocess_run = runner.subprocess.run
    try:
        runner.default_source_commit = lambda: source_commit
        runner.subprocess.run = source_state_run(
            "b" * 40, "Signer <signer@example.com>\n",
        )
        rejected_remote = False
        try:
            runner.verify_source_state(source_commit, require_clean=False)
        except ValueError:
            rejected_remote = True
        require(rejected_remote,
                "live execution must reject a source commit that is not the fresh remote branch head")

        runner.subprocess.run = source_state_run(source_commit, "")
        rejected_unsigned = False
        try:
            runner.verify_source_state(source_commit, require_clean=False)
        except ValueError:
            rejected_unsigned = True
        require(rejected_unsigned,
                "live execution must reject a source commit without a valid DCO sign-off trailer")

        runner.subprocess.run = source_state_run(
            source_commit, "Signer <signer@example.com>\n",
        )
        runner.verify_source_state(source_commit, require_clean=False)
    finally:
        runner.default_source_commit = original_default_source_commit
        runner.subprocess.run = original_subprocess_run

    with tempfile.TemporaryDirectory() as summary_tmp:
        summary_root = Path(summary_tmp)
        runner.ensure_campaign_plan(
            summary_root, provider_plan="noncursor-degraded-v1", source_commit="a" * 40,
            v1_commit="b" * 40, models=historical_campaign_models,
        )
        rejected = False
        try:
            runner.summarize_semantic(summary_root, "frozen-three-provider")
        except ValueError:
            rejected = True
        require(rejected,
                "semantic summary must reject a CLI provider plan that disagrees with campaign-plan.json")
        matching_summary = runner.summarize_semantic(summary_root, "noncursor-degraded-v1")
        require(matching_summary["provider_plan"] == "noncursor-degraded-v1",
                "semantic summary must retain the matching campaign provider plan")
    smoke_tasks = runner.filter_arm_tasks(
        tasks, arms={"v2-candidate"}, fixtures={"tm-01-false-mvd"}, repetitions={1},
    )
    require(smoke_tasks == [runner.ArmTask("v2-candidate", 1, "tm-01-false-mvd")],
            "arm filters must select exactly one terminal smoke call")
    semantic_smoke = runner.filter_semantic_tasks(
        runner.full_semantic_plan(), fixtures={"tm-01-false-mvd"},
        repetitions={1}, seats={"a"},
    )
    require(semantic_smoke == [runner.SemanticTask(1, "tm-01-false-mvd", "a")],
            "semantic filters must select exactly one isolated smoke seat")
    arm_instruction = runner.arm_prompt("tm-01-false-mvd")
    require("Perform the task now; do not acknowledge readiness" in arm_instruction,
            "one-shot arm prompt does not reject readiness-only responses")
    require("Do not use a Markdown fence" in arm_instruction,
            "one-shot arm prompt does not reject fenced JSON")
    json_boundary = (
        "The first non-whitespace character must be `{`, and its matching top-level `}` "
        "must be the last non-whitespace character. Emit no draft object, repeated snapshot, "
        "second object, commentary, Markdown fence, or extra delimiter."
    )
    concise_json = (
        "Keep the JSON concise: use short but sufficient strings and minimal arrays, with no "
        "repeated rationale, evidence, or restatement of packet contents."
    )
    syntax_check = (
        "Before returning, verify that the complete response parses as JSON: every object member "
        "and array element is comma-separated, every string is closed and escaped, and braces "
        "and brackets are balanced."
    )
    silent_boundary = (
        "Do all analysis silently. Never emit analysis, planning, self-talk, a schema example, "
        "or a draft."
    )
    arm_marker_boundary = (
        "The response marker `formal-rigor-fixture-response@1` must appear exactly once in the "
        "entire output."
    )
    semantic_marker_boundary = (
        "The adjudication marker `formal-rigor-semantic-adjudication@1` must appear exactly once "
        "in the entire output."
    )
    empirical_tests_boundary = (
        "Every entry in `record.empirical_closure.tests` must be a JSON string, never an object."
    )
    require(json_boundary in arm_instruction,
            "arm prompt does not enforce one complete top-level JSON object")
    require(concise_json in arm_instruction,
            "arm prompt does not bound free-text JSON expansion")
    require(syntax_check in arm_instruction,
            "arm prompt does not require a complete JSON syntax check")
    require(silent_boundary in arm_instruction and arm_marker_boundary in arm_instruction,
            "arm prompt does not suppress intermediate output and require exactly one marker")
    require(empirical_tests_boundary in arm_instruction,
            "arm prompt does not require empirical_closure.tests entries to be strings")
    semantic_instruction = runner.semantic_prompt("tm-01-false-mvd")
    require("Perform the task now; do not acknowledge readiness" in semantic_instruction,
            "semantic prompt does not reject readiness-only responses")
    require("Do not use a Markdown fence" in semantic_instruction,
            "semantic prompt does not reject fenced JSON")
    require(json_boundary in semantic_instruction,
            "semantic prompt does not enforce one complete top-level JSON object")
    require(concise_json in semantic_instruction,
            "semantic prompt does not bound free-text JSON expansion")
    require(syntax_check in semantic_instruction,
            "semantic prompt does not require a complete JSON syntax check")
    require(silent_boundary in semantic_instruction and
            semantic_marker_boundary in semantic_instruction,
            "semantic prompt does not suppress intermediate output and require exactly one marker")

    output_root_probe = Path("C:/tmp/campaigns/formal-rigor-run")
    require(runner.default_packet_root(output_root_probe, "arms") ==
            Path("C:/tmp/campaigns/formal-rigor-run-packets/arms") and
            runner.default_packet_root(output_root_probe, "semantic") ==
            Path("C:/tmp/campaigns/formal-rigor-run-packets/semantic"),
            "default packet roots must be output-adjacent and phase-specific")
    for packet_root, packet_cwd in (
        (Path("C:/Users/example/formal-rigor-packets"), Path("C:/tmp")),
        (Path("../formal-rigor-packets"), Path("C:/Users/example/project")),
    ):
        rejected_sensitive_packet_root = False
        try:
            runner.canonical_packet_root(packet_root, cwd=packet_cwd)
        except ValueError:
            rejected_sensitive_packet_root = True
        require(rejected_sensitive_packet_root,
                f"runner accepted a profile-bound packet-root alias: {packet_root}")
    neutral_packet_root = runner.canonical_packet_root(
        runner.default_packet_root(output_root_probe, "arms"), cwd=Path("C:/tmp"),
    )
    require(neutral_packet_root == Path("C:/tmp/campaigns/formal-rigor-run-packets/arms").resolve(),
            "neutral output-adjacent packet root was not accepted and canonicalized")
    with tempfile.TemporaryDirectory(dir="C:\\tmp") as guard_tmp:
        guard_root = Path(guard_tmp)
        original_run = runner.subprocess.run
        runner.subprocess.run = lambda *args, **kwargs: SimpleNamespace(
            returncode=0, stdout="", stderr="",
        )
        try:
            for historical_plan in ("frozen-three-provider", "noncursor-degraded-v1"):
                packet_built = False
                def guarded_packet_builder(packet: Path) -> None:
                    nonlocal packet_built
                    packet_built = True
                    packet.mkdir()
                rejected_before_call = False
                try:
                    runner.execute_call(
                        result_dir=guard_root / historical_plan,
                        packet_root=guard_root / "packets",
                        packet_builder=guarded_packet_builder,
                        prompt="return JSON", harness="agy", executable="agy",
                        model="gemini-3.1-pro-high",
                        identity={
                            "kind": "arm", "provider_plan": historical_plan,
                            "fixture": "guard-probe",
                        },
                        source_commit="a" * 40, timeout_seconds=60,
                    )
                except ValueError:
                    rejected_before_call = True
                require(rejected_before_call and not packet_built,
                        f"historical plan reached packet/call setup: {historical_plan}")
        finally:
            runner.subprocess.run = original_run

    frozen_transport_schema = (
        ROOT / "formal-rigor-fixture-transport.schema.json"
    ).read_text(encoding="utf-8")
    v2_agy_prompt = runner.execution_prompt(
        arm_instruction, provider_plan="noncursor-degraded-v3", phase="arms", harness="agy",
        output_schema_text=frozen_transport_schema,
    )
    terminal_boundary = (
        f"{silent_boundary}\n{arm_marker_boundary}\n{json_boundary}"
    )
    require(frozen_transport_schema in v2_agy_prompt,
            "v2 non-native arm prompt omitted the exact frozen output schema")
    require(v2_agy_prompt.endswith(terminal_boundary),
            "v2 non-native arm prompt does not repeat silent/marker/JSON boundaries terminally")
    require(runner.execution_prompt(
        arm_instruction, provider_plan="noncursor-degraded-v1", phase="arms", harness="agy",
        output_schema_text=frozen_transport_schema,
    ) == arm_instruction, "v1 arm prompt delivery must remain unchanged")
    require(runner.execution_prompt(
        arm_instruction, provider_plan="noncursor-degraded-v3", phase="arms", harness="codex",
        output_schema_text=frozen_transport_schema,
    ) == arm_instruction, "native Codex output-schema prompt behavior must remain unchanged")
    frozen_semantic_schema = (
        ROOT / "formal-rigor-semantic-adjudication.schema.json"
    ).read_text(encoding="utf-8")
    v2_semantic_agy_prompt = runner.execution_prompt(
        semantic_instruction, provider_plan="noncursor-degraded-v3", phase="semantic",
        harness="agy", output_schema_text=frozen_semantic_schema,
    )
    semantic_terminal_boundary = (
        f"{silent_boundary}\n{semantic_marker_boundary}\n{json_boundary}"
    )
    require(frozen_semantic_schema in v2_semantic_agy_prompt,
            "v2 non-native semantic prompt omitted the exact frozen schema")
    require(v2_semantic_agy_prompt.endswith(semantic_terminal_boundary),
            "v2 semantic prompt does not repeat silent/marker/JSON boundaries terminally")

    schema_probe = {
        "type": "object",
        "additionalProperties": False,
        "required": ["tests"],
        "properties": {
            "tests": {"type": "array", "items": {"type": "string"}},
        },
    }
    require(not runner.validate_json_schema({"tests": ["probe"]}, schema_probe),
            "stdlib schema validator rejected a valid string test entry")
    schema_errors = runner.validate_json_schema({"tests": [{"test": "probe"}]}, schema_probe)
    require(any("$.tests[0]" in error and "string" in error for error in schema_errors),
            "stdlib schema validator accepted an object where the frozen schema requires a string")

    completed, failed = runner.run_parallel(
        ["schema-invalid"],
        lambda _task: {
            "transport": "completed", "json_parseable": True, "schema_valid": False,
            "secret_screen": {"passed": True},
        },
        1,
    )
    require((completed, failed) == (0, 1),
            "run_parallel must fail a parseable response that violates its output schema")
    completed, failed = runner.run_parallel(
        ["schema-unknown"],
        lambda _task: {
            "transport": "completed", "json_parseable": True,
            "secret_screen": {"passed": True},
        },
        1,
    )
    require((completed, failed) == (0, 1),
            "run_parallel must fail closed when schema-validation evidence is absent")
    require(runner.call_qualifies({
        "transport": "completed", "json_parseable": True, "schema_valid": True,
        "secret_screen": {"passed": True},
    }), "qualifying-call predicate rejected complete schema-valid evidence")
    require(not runner.call_qualifies({
        "transport": "completed", "json_parseable": True,
        "secret_screen": {"passed": True},
    }), "qualifying-call predicate accepted missing schema evidence")
    v3_qualifying_record = {
        "provider_plan": "noncursor-degraded-v3", "phase": "arms",
        "model": "gemini-3.6-flash-medium", "reasoning_effort": "medium",
        "preflight_sha256": preflight_sha256,
        "campaign_plan_sha256": campaign_sha256,
        "transport": "completed", "json_parseable": True, "schema_valid": True,
        "secret_screen": {"passed": True},
    }
    require(runner.call_qualifies(v3_qualifying_record),
            "V3 qualifying-call predicate rejected complete phase/model provenance")
    require(not runner.call_qualifies({**v3_qualifying_record, "preflight_sha256": None}),
            "V3 qualifying-call predicate accepted missing preflight binding")
    v3_phase_status = runner.phase_status(
        phase="arms", tasks=[runner.ArmTask("v2-candidate", 2, "tm-01-false-mvd")],
        provider_plan="noncursor-degraded-v3", source_commit="a" * 40,
        models_by_phase=campaign_models, completed=1, failed=0,
        preflight_sha256=preflight_sha256, campaign_plan_sha256=campaign_sha256,
    )
    require(v3_phase_status["schema"] == "formal-rigor-live-phase-status@2" and
            v3_phase_status["selected_models_by_harness"] == {
                "agy": "gemini-3.6-flash-medium",
            } and v3_phase_status["preflight_sha256"] == preflight_sha256 and
            v3_phase_status["campaign_plan_sha256"] == campaign_sha256,
            "V3 phase status omitted phase model and receipt/campaign bindings")

    fixture_dir = ROOT / "fixtures" / "tm-01-false-mvd"
    truth = json.loads((fixture_dir / "ground-truth.json").read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory() as tmp:
        tmp_root = Path(tmp)
        candidate_packet = tmp_root / "candidate"
        runner.build_arm_packet(candidate_packet, "v2-candidate", fixture_dir)
        require((candidate_packet / "scenario.md").is_file(), "candidate packet omits scenario")
        require((candidate_packet / "artifacts" / "facts.json").is_file(), "candidate packet omits artifacts")
        require((candidate_packet / "candidate" / "SKILL.md").is_file(), "candidate packet omits v2 skill")
        require((candidate_packet / "candidate" / "reference" / "modules" / "index.md").is_file(),
                "candidate packet omits module registry")
        require((candidate_packet / "formal-rigor-fixture-transport.schema.json").is_file(),
                "candidate packet omits the API-compatible arm output schema")
        forbidden_names = {"ground-truth.json", "score.py", "semantic-adjudication.md", "RESULTS.md"}
        require(not any(path.name in forbidden_names for path in candidate_packet.rglob("*")),
                "candidate packet leaked scorer-only or prior-result material")

        embedded_arm = runner.codex_arm_packet_prompt(candidate_packet, arm_instruction)
        require("Ranked-contact review" in embedded_arm,
                "Codex arm prompt omitted the mandatory scenario content")
        require('"candidate/SKILL.md"' in embedded_arm and
                '"candidate/reference/modules/index.md"' in embedded_arm,
                "Codex arm prompt omitted the candidate contract or module index")
        require('"candidate/reference/modules/relational-dependencies.md"' not in embedded_arm,
                "Codex arm prompt eagerly loaded unselected module bodies")
        require("You must answer from these mandatory inputs now" in embedded_arm,
                "Codex arm prompt does not reject readiness-only handshakes after input injection")

        sealed = runner.sealed_packet_prompt(candidate_packet, "Return exactly one JSON object.")
        require("Return exactly one JSON object." in sealed,
                "sealed bridge prompt omitted the task instruction")
        require('"scenario.md"' in sealed and '"candidate/SKILL.md"' in sealed,
                "sealed bridge prompt omitted packet-relative source files")
        require(not any(name in sealed for name in forbidden_names),
                "sealed bridge prompt leaked scorer-only or prior-result material")
        sealed_tail = sealed[sealed.index("END_SEALED_PACKET_JSON"):]
        require(silent_boundary in sealed_tail and empirical_tests_boundary in sealed_tail and
                "marker must appear exactly once" in sealed_tail,
                "sealed prompt does not repeat the output constraints after packet contents")
        require("Do not use tools, execute commands, or write files" in sealed,
                "sealed bridge prompt omitted its no-tool isolation instruction")
        require(sealed.rstrip().endswith(json_boundary),
                "sealed bridge prompt does not repeat the JSON boundary after packet contents")
        require(sealed.rfind(concise_json) > sealed.find("END_SEALED_PACKET_JSON"),
                "sealed bridge prompt does not repeat the concision rule after packet contents")
        require(sealed.rfind(syntax_check) > sealed.find("END_SEALED_PACKET_JSON"),
                "sealed bridge prompt does not repeat the syntax check after packet contents")
        bridge_invocation = runner.fleet_bridge_invocation(
            executable="fleet-bridge://default/fleet-orchestrator/surface-bridge-v2-0",
            harness="cursor", model="auto", packet_dir=candidate_packet,
            prompt="fixture-secret-payload",
            identity={"kind": "arm", "fixture": "tm-01-false-mvd"},
        )
        require("fixture-secret-payload" not in " ".join(bridge_invocation["command"]),
                "sealed evaluation payload leaked into the local process argv")
        bridge_payload = json.loads(bridge_invocation["stdin"])
        require(bridge_payload["kind"] == "cursor_agent" and bridge_payload["model"] == "auto",
                "Fleet bridge invocation did not preserve surface/model provenance")
        require("fixture-secret-payload" in bridge_payload["prompt"] and
                '"candidate/SKILL.md"' in bridge_payload["prompt"],
                "Fleet bridge invocation did not send the task and sealed packet over stdin")
        require(bridge_invocation["metadata"] == {
            "adapter": "fleet-orchestrator-surface-bridge-stream",
            "context": "default", "namespace": "fleet-orchestrator",
            "pod": "surface-bridge-v2-0", "surface_kind": "cursor_agent",
            "model_selection": "surface-default-auto",
        }, "Fleet bridge provenance metadata drifted")
        rejected_bridge_model = False
        try:
            runner.fleet_bridge_invocation(
                executable="fleet-bridge://default/fleet-orchestrator/surface-bridge-v2-0",
                harness="cursor", model="gpt-5.6-sol-high", packet_dir=candidate_packet,
                prompt="return JSON", identity={"kind": "arm"},
            )
        except ValueError:
            rejected_bridge_model = True
        require(rejected_bridge_model,
                "Fleet bridge accepted a falsely pinned model that its stream endpoint ignores")

        bridge_entered = threading.Event()
        runner.FLEET_BRIDGE_LOCK.acquire()
        waiter = threading.Thread(target=lambda: (
            runner.FLEET_BRIDGE_LOCK.acquire(), bridge_entered.set(), runner.FLEET_BRIDGE_LOCK.release()
        ))
        waiter.start()
        require(not bridge_entered.wait(0.05),
                "Fleet bridge lock did not serialize concurrent surface calls")
        runner.FLEET_BRIDGE_LOCK.release()
        require(bridge_entered.wait(1),
                "Fleet bridge lock did not release the next surface call")
        waiter.join(timeout=1)
        require("with (FLEET_BRIDGE_LOCK if bridge else nullcontext()):" in
                RUNNER_PATH.read_text(encoding="utf-8"),
                "live execution path does not use the Fleet bridge serialization lock")

        neutral_packet = tmp_root / "neutral"
        runner.build_arm_packet(neutral_packet, "neutral", fixture_dir)
        require(not (neutral_packet / "candidate").exists(), "neutral packet leaked candidate skill")

        closed_taxonomy_packet = tmp_root / "closed-taxonomy"
        runner.build_arm_packet(
            closed_taxonomy_packet, "parody-closed-taxonomy", fixture_dir
        )
        closed_taxonomy_prompt = (
            closed_taxonomy_packet / "ARM_PROMPT.txt"
        ).read_text(encoding="utf-8")
        require("Never emit unmapped" in closed_taxonomy_prompt,
                "closed-taxonomy parody lost its registered semantic defect")
        require("smallest schema-valid record" in closed_taxonomy_prompt,
                "closed-taxonomy parody does not bound its record complexity")

        candidate_response = tmp_root / "response.json"
        candidate_response.write_text(json.dumps({
            "response": "formal-rigor-fixture-response@1",
            "fixture": "tm-01-false-mvd",
            "invocation": "focused",
            "skip_reason": None,
            "claim_assessments": [{"id": "c1", "state": "refuted", "derivation_ids": []}],
            "focused_output": ["bounded result"],
            "record": None,
        }), encoding="utf-8")
        adjudication_packet = tmp_root / "adjudication"
        runner.build_adjudication_packet(adjudication_packet, fixture_dir, candidate_response, truth)
        rubric = json.loads((adjudication_packet / "rubric.json").read_text(encoding="utf-8"))
        require(set(rubric) == {"fixture", "claims"}, "adjudication rubric leaked non-required ground truth")
        require(set(rubric["claims"][0]) == {"id", "proof_obligations", "forbidden_propositions"},
                "adjudication claim rubric leaked class, priority, thresholds, or expected state")
        require(not (adjudication_packet / "ground-truth.json").exists(), "adjudication packet leaked ground truth file")
        require((adjudication_packet / "formal-rigor-semantic-adjudication.schema.json").is_file(),
                "adjudication packet omitted the enforceable output schema")
        semantic_schema = json.loads(
            (adjudication_packet / "formal-rigor-semantic-adjudication.schema.json").read_text(encoding="utf-8")
        )
        require(semantic_schema["properties"]["adjudication"].get("type") == "string",
                "Codex strict output schema requires an explicit type alongside const")

        result_dir = tmp_root / "result"
        require(runner.call_needed(result_dir), "fresh call should be needed")
        result_dir.mkdir()
        (result_dir / "call.json").write_text('{"transport":"completed"}', encoding="utf-8")
        require(not runner.call_needed(result_dir), "completed call must not be retried")

        captured: dict[str, object] = {}
        original_execute_call = runner.execute_call
        try:
            runner.execute_call = lambda **kwargs: captured.update(kwargs) or {}
            runner.run_arm_task(
                runner.ArmTask("v2-candidate", 1, "tm-01-false-mvd"),
                output_root=tmp_root / "arm-output",
                packet_root=tmp_root / "arm-packets",
                executables={"codex": "codex", "agy": "agy", "cursor": "cursor-agent"},
                models={"codex": "gpt-5.6-sol", "agy": "gemini-3.1-pro-high", "cursor": "auto"},
                provider_plan="noncursor-degraded-v1",
                source_commit="a" * 40,
                v1_source_dir=tmp_root / "v1",
                timeout_seconds=60,
            )
        finally:
            runner.execute_call = original_execute_call
        require(
            captured.get("output_schema_name") == "formal-rigor-fixture-transport.schema.json",
            "Codex arm calls must enforce the API-compatible fixture transport schema",
        )
        require(captured.get("identity", {}).get("provider_plan") == "noncursor-degraded-v1",
                "arm call records must retain the provider-plan identity")
        v3_captured: dict[str, object] = {}
        try:
            runner.execute_call = lambda **kwargs: v3_captured.update(kwargs) or {}
            runner.run_arm_task(
                runner.ArmTask("v2-candidate", 2, "tm-01-false-mvd"),
                output_root=tmp_root / "v3-arm-output",
                packet_root=tmp_root / "v3-arm-packets",
                executables={"codex": "codex", "agy": "agy", "cursor": "cursor-agent"},
                models_by_phase=campaign_models,
                provider_plan="noncursor-degraded-v3", source_commit="a" * 40,
                v1_source_dir=tmp_root / "v1", timeout_seconds=60,
                preflight_sha256=preflight_sha256,
                campaign_plan_sha256=campaign_sha256,
            )
        finally:
            runner.execute_call = original_execute_call
        require(v3_captured.get("model") == "gemini-3.6-flash-medium",
                "V3 arm dispatch did not select the arm-phase AGY model")
        require(v3_captured.get("identity", {}).get("phase") == "arms" and
                v3_captured.get("identity", {}).get("reasoning_effort") == "medium" and
                v3_captured.get("identity", {}).get("preflight_sha256") == preflight_sha256 and
                v3_captured.get("identity", {}).get("campaign_plan_sha256") == campaign_sha256,
                "V3 arm dispatch omitted phase/effort/preflight/campaign identity")

        semantic_output = tmp_root / "semantic-output"
        semantic_candidate = (
            semantic_output / "arms" / "v2-candidate" / "run-1" /
            "tm-01-false-mvd.response.json"
        )
        semantic_candidate.parent.mkdir(parents=True)
        semantic_candidate.write_text(candidate_response.read_text(encoding="utf-8"), encoding="utf-8")
        candidate_bytes = semantic_candidate.read_bytes()
        candidate_call_dir = (
            semantic_output / "arms" / "v2-candidate" / "run-1" / "calls" /
            "tm-01-false-mvd"
        )
        candidate_call_dir.mkdir(parents=True)
        (candidate_call_dir / "response.json").write_bytes(candidate_bytes)
        runner.write_json(candidate_call_dir / "call.json", {
            "schema": "formal-rigor-live-call@1", "kind": "arm",
            "provider_plan": "noncursor-degraded-v1", "source_commit": "a" * 40,
            "arm": "v2-candidate", "repetition": 1, "fixture": "tm-01-false-mvd",
            "transport": "completed", "json_parseable": True, "schema_valid": True,
            "schema_errors": [], "response_sha256": runner.sha256_bytes(candidate_bytes),
            "secret_screen": {"passed": True},
        })
        require(runner.candidate_response_qualifies(
            semantic_output, runner.SemanticTask(1, "tm-01-false-mvd", "a"),
            provider_plan="noncursor-degraded-v1", source_commit="a" * 40,
        ), "semantic candidate integrity check rejected matching arm evidence")
        semantic_candidate.write_text('{"tampered":true}', encoding="utf-8")
        require(not runner.candidate_response_qualifies(
            semantic_output, runner.SemanticTask(1, "tm-01-false-mvd", "a"),
            provider_plan="noncursor-degraded-v1", source_commit="a" * 40,
        ), "semantic candidate integrity check accepted a between-phase mutation")
        semantic_candidate.write_bytes(candidate_bytes)
        semantic_captured: dict[str, object] = {}
        try:
            runner.execute_call = lambda **kwargs: semantic_captured.update(kwargs) or {}
            runner.run_semantic_task(
                runner.SemanticTask(1, "tm-01-false-mvd", "a"),
                output_root=semantic_output, packet_root=tmp_root / "semantic-packets",
                executables={"codex": "codex", "agy": "agy", "cursor": "cursor-agent"},
                models={"codex": "gpt-5.6-sol", "agy": "gemini-3.1-pro-high", "cursor": "auto"},
                provider_plan="noncursor-degraded-v1", source_commit="a" * 40,
                timeout_seconds=60,
            )
        finally:
            runner.execute_call = original_execute_call
        require(semantic_captured.get("identity", {}).get("provider_plan") ==
                "noncursor-degraded-v1",
                "semantic call records must retain the provider-plan identity")

        summary_output = tmp_root / "summary-output"
        runner.ensure_campaign_plan(
            summary_output, provider_plan="noncursor-degraded-v1", source_commit="a" * 40,
            v1_commit="b" * 40, models=historical_campaign_models,
        )
        semantic_summary = runner.summarize_semantic(summary_output, "noncursor-degraded-v1")
        require(semantic_summary["provider_plan"] == "noncursor-degraded-v1" and
                json.loads((summary_output / "semantic-summary.json").read_text(
                    encoding="utf-8"
                ))["provider_plan"] == "noncursor-degraded-v1",
                "semantic summaries must retain the provider-plan identity")

        v3_summary_output = tmp_root / "v3-summary-output"
        runner.ensure_campaign_plan(
            v3_summary_output, provider_plan="noncursor-degraded-v3",
            source_commit="a" * 40, v1_commit="b" * 40,
            models_by_phase=campaign_models, preflight_receipt=preflight_receipt,
        )
        v3_semantic_summary = runner.summarize_semantic(
            v3_summary_output, "noncursor-degraded-v3"
        )
        require(v3_semantic_summary["provider_plan"] == "noncursor-degraded-v3",
                "semantic summary must accept and retain the V3 campaign identity")

    command = runner.codex_command(
        codex="codex", model="gpt-5.6-sol", packet_dir=Path("packet"),
        response_path=Path("response.json"), prompt="return JSON",
        output_schema=Path("packet/formal-rigor-semantic-adjudication.schema.json"),
    )
    joined = " ".join(str(item) for item in command)
    for marker in (
        "exec", "--ephemeral", "--ignore-user-config", "--sandbox read-only",
        "--skip-git-repo-check", "--disable plugins", "--disable apps",
        "--disable remote_plugin", "--disable plugin_sharing",
        "--output-schema packet/formal-rigor-semantic-adjudication.schema.json",
    ):
        require(marker in joined, f"codex command missing isolation marker: {marker}")
    argv_prompt, stdin_prompt = runner.codex_prompt_transport("sealed fixture payload")
    require(argv_prompt == "-" and stdin_prompt == "sealed fixture payload",
            "Codex sealed prompts must travel over stdin rather than process argv")

    agy = runner.agy_command(
        agy="agy", model="gemini-3.6-flash-medium", packet_dir=Path("packet"),
        response_path=Path("response.json"), prompt="return JSON", effort="medium",
    )
    agy_joined = " ".join(str(item) for item in agy)
    for marker in (
        "agy", "--print", "--sandbox", "--dangerously-skip-permissions",
        "--mode plan", "--add-dir .", "--model gemini-3.6-flash-medium", "--effort medium",
    ):
        require(marker in agy_joined, f"agy command missing isolation marker: {marker}")
    require(agy == [
        "agy", "--sandbox", "--dangerously-skip-permissions", "--mode", "plan",
        "--add-dir", ".", "--model", "gemini-3.6-flash-medium", "--effort", "medium",
        "--print", "return JSON",
    ], "v2 arm AGY argv must use packet cwd and explicit medium effort")
    semantic_agy = runner.agy_command(
        agy="agy", model="gemini-3.1-pro-high", packet_dir=Path("packet"),
        response_path=Path("response.json"), prompt="return JSON", effort="high",
    )
    require(semantic_agy[-4:] == ["--effort", "high", "--print", "return JSON"],
            "semantic AGY argv must carry explicit high effort")
    require(runner.call_effort(
        "noncursor-degraded-v3", phase="arms", harness="agy", bridge=False,
    ) == "medium" and runner.call_effort(
        "noncursor-degraded-v3", phase="semantic", harness="agy", bridge=False,
    ) == "high" and runner.call_effort(
        "noncursor-degraded-v1", phase="arms", harness="agy", bridge=False,
    ) == "high" and runner.call_effort(
        "noncursor-degraded-v3", phase="arms", harness="agy", bridge=True,
    ) == "provider-model-default",
            "reasoning-effort policy must distinguish v1, v2 phase, and bridge routing")
    rejected_bridge_identity = False
    try:
        runner.validate_live_harness_configuration(
            "noncursor-degraded-v3",
            {
                "codex": "codex.cmd",
                "agy": "fleet-bridge://default/fleet-orchestrator/surface-bridge-v2-0",
                "cursor": "cursor-agent",
            },
        )
    except ValueError:
        rejected_bridge_identity = True
    require(rejected_bridge_identity,
            "v2 direct-harness identity must reject Fleet bridge executable overrides")

    cursor = runner.cursor_command(
        cursor="cursor-agent", model="gpt-5.6-sol", packet_dir=Path("packet"),
        response_path=Path("response.json"), prompt="return JSON",
    )
    cursor_joined = " ".join(str(item) for item in cursor)
    for marker in (
        "cursor-agent", "--print", "--output-format text", "--mode ask",
        "--sandbox enabled", "--workspace packet", "--model gpt-5.6-sol",
    ):
        require(marker in cursor_joined, f"Cursor command missing isolation marker: {marker}")

    bridge_command = runner.fleet_bridge_command(
        kubectl="kubectl", context="default", namespace="fleet-orchestrator",
        pod="surface-bridge-v2-0",
    )
    bridge_joined = " ".join(bridge_command)
    for marker in (
        "kubectl --context default -n fleet-orchestrator exec -i surface-bridge-v2-0",
        "node -e",
    ):
        require(marker in bridge_joined, f"Fleet bridge command missing marker: {marker}")
    require("fixture-secret-payload" not in bridge_joined,
            "Fleet bridge command must receive the sealed prompt over stdin, not argv")

    bridge_events = "\n".join((
        json.dumps({"delta": "{\"fixture\":"}),
        json.dumps({"delta": "\"tm-01-false-mvd\"}"}),
        json.dumps({"done": True, "code": 0}),
    )) + "\n"
    bridge_response, bridge_code, bridge_stderr = runner.parse_fleet_bridge_stream(bridge_events)
    require(bridge_response == '{"fixture":"tm-01-false-mvd"}',
            "Fleet bridge deltas were not reconstructed losslessly")
    require(bridge_code == 0 and bridge_stderr == "",
            "Fleet bridge completion frame was not parsed")
    failed_response, failed_code, failed_stderr = runner.parse_fleet_bridge_stream(
        json.dumps({"done": True, "code": 124, "stderr": "idle timeout"}) + "\n"
    )
    require(failed_response == "" and failed_code == 124 and failed_stderr == "idle timeout",
            "Fleet bridge failure frame was not preserved")
    duplicated = '{"fixture":"tm-01-false-mvd"}{"fixture":"tm-01-false-mvd"}'
    normalized, normalization = runner.normalize_fleet_bridge_response(duplicated)
    require(normalized == '{"fixture":"tm-01-false-mvd"}' and
            normalization == "deduplicated-identical-complete-json-values",
            "Fleet bridge did not normalize its exact duplicate final JSON frame")
    snapshots = (
        '{"response":"formal-rigor-fixture-response@1","fixture":"a","value":"draft"}'
        '{"response":"formal-rigor-fixture-response@1","fixture":"a","value":"final"}'
    )
    final_snapshot, snapshot_normalization = runner.normalize_fleet_bridge_response(snapshots)
    require(final_snapshot ==
            '{"response":"formal-rigor-fixture-response@1","fixture":"a","value":"final"}' and
            snapshot_normalization == "selected-final-complete-json-snapshot",
            "Fleet bridge did not select the final snapshot for one recognized response envelope")
    snapshots_with_unmatched_closers = (
        '{"response":"formal-rigor-fixture-response@1","fixture":"a","value":"draft"}\n}'
        '{"response":"formal-rigor-fixture-response@1","fixture":"a","value":"final"}\n}'
    )
    unchanged, no_normalization = runner.normalize_fleet_bridge_response(
        snapshots_with_unmatched_closers
    )
    require(unchanged == snapshots_with_unmatched_closers and no_normalization is None,
            "Fleet bridge normalization must not repair unmatched model-output closers")
    ambiguous_closer_snapshots = (
        '{"response":"formal-rigor-fixture-response@1","fixture":"a","value":"draft"}\n}'
        '{"response":"formal-rigor-fixture-response@1","fixture":"b","value":"final"}\n}'
    )
    unchanged, no_normalization = runner.normalize_fleet_bridge_response(
        ambiguous_closer_snapshots
    )
    require(unchanged == ambiguous_closer_snapshots and no_normalization is None,
            "Fleet bridge normalization must reject unmatched-closer snapshots for different fixtures")
    malformed_then_final = (
        '{"response":"formal-rigor-fixture-response@1","fixture":"a","value":}'
        '{"response":"formal-rigor-fixture-response@1","fixture":"a","value":"final"}'
    )
    recovered_snapshot, recovery_normalization = runner.normalize_fleet_bridge_response(
        malformed_then_final
    )
    require(recovered_snapshot ==
            '{"response":"formal-rigor-fixture-response@1","fixture":"a","value":"final"}' and
            recovery_normalization == "selected-final-complete-json-snapshot-after-malformed-prefix",
            "Fleet bridge did not select the sole final snapshot after a malformed same-envelope prefix")
    ambiguous_malformed_prefix = (
        '{"response":"formal-rigor-fixture-response@1","fixture":"b","value":}'
        '{"response":"formal-rigor-fixture-response@1","fixture":"a","value":"final"}'
    )
    unchanged, no_normalization = runner.normalize_fleet_bridge_response(
        ambiguous_malformed_prefix
    )
    require(unchanged == ambiguous_malformed_prefix and no_normalization is None,
            "Fleet bridge normalization must reject a malformed prefix for another fixture")
    two_malformed_prefixes = (
        '{"response":"formal-rigor-fixture-response@1","fixture":"a","value":}'
        '{"response":"formal-rigor-fixture-response@1","fixture":"a","value":}'
        '{"response":"formal-rigor-fixture-response@1","fixture":"a","value":"final"}'
    )
    unchanged, no_normalization = runner.normalize_fleet_bridge_response(two_malformed_prefixes)
    require(unchanged == two_malformed_prefixes and no_normalization is None,
            "Fleet bridge normalization must reject multiple malformed snapshots")
    trailing_junk = malformed_then_final + "\nnot-a-snapshot"
    unchanged, no_normalization = runner.normalize_fleet_bridge_response(trailing_junk)
    require(unchanged == trailing_junk and no_normalization is None,
            "Fleet bridge normalization must reject content after the final envelope")
    nested_as_value = (
        '{"response":"formal-rigor-fixture-response@1","fixture":"a","value":'
        '{"response":"formal-rigor-fixture-response@1","fixture":"a","value":"final"}'
    )
    unchanged, no_normalization = runner.normalize_fleet_bridge_response(nested_as_value)
    require(unchanged == nested_as_value and no_normalization is None,
            "Fleet bridge normalization must reject a final object nested as an unfinished value")
    adjudication_final = (
        '{"adjudication":"formal-rigor-semantic-adjudication@1",'
        '"fixture":"a","value":"final"}'
    )
    adjudication_malformed = adjudication_final.replace('"value":"final"', '"value":', 1)
    recovered_snapshot, recovery_normalization = runner.normalize_fleet_bridge_response(
        adjudication_malformed + adjudication_final
    )
    require(recovered_snapshot == adjudication_final and
            recovery_normalization == "selected-final-complete-json-snapshot-after-malformed-prefix",
            "Fleet bridge malformed-prefix recovery did not cover adjudication envelopes")
    crossed_markers = (
        '{"response":"formal-rigor-semantic-adjudication@1","fixture":"a","value":"draft"}'
        '{"response":"formal-rigor-semantic-adjudication@1","fixture":"a","value":"final"}'
    )
    unchanged, no_normalization = runner.normalize_fleet_bridge_response(crossed_markers)
    require(unchanged == crossed_markers and no_normalization is None,
            "Fleet bridge normalization must reject a semantic marker under the response key")
    distinct = (
        '{"response":"formal-rigor-fixture-response@1","fixture":"a"}'
        '{"response":"formal-rigor-fixture-response@1","fixture":"b"}'
    )
    unchanged, no_normalization = runner.normalize_fleet_bridge_response(distinct)
    require(unchanged == distinct and no_normalization is None,
            "Fleet bridge normalization must fail closed across distinct fixture envelopes")

    fixture_envelope = (
        '{"response":"formal-rigor-fixture-response@1",'
        '"fixture":"cc-03-postgresql18-rationale-correct","focused_output":[]}'
    )
    agy_stdout = (
        "I evaluated the scenario and will return the requested envelope.\n\n"
        f"```json\n{fixture_envelope}\n```\n"
        "This is the complete response.\n"
    )
    normalized, normalization = runner.normalize_plain_text_response(agy_stdout)
    require(normalized == fixture_envelope and
            normalization == "extracted-single-recognized-json-envelope",
            "plain-text harness normalization did not extract one fenced fixture envelope")

    adjudication_envelope = (
        '{"adjudication":"formal-rigor-semantic-adjudication@1",'
        '"fixture":"cc-03-postgresql18-rationale-correct","verdict":"INCONCLUSIVE"}'
    )
    normalized, normalization = runner.normalize_plain_text_response(
        f"Adjudication follows:\n{adjudication_envelope}\nEnd."
    )
    require(normalized == adjudication_envelope and
            normalization == "extracted-single-recognized-json-envelope",
            "plain-text harness normalization did not recognize an adjudication envelope")

    unrecognized = 'Analysis only, plus metadata {"fixture":"cc-03-postgresql18-rationale-correct"}.'
    unchanged, no_normalization = runner.normalize_plain_text_response(unrecognized)
    require(unchanged == unrecognized and no_normalization is None,
            "plain-text normalization must fail closed when no recognized envelope exists")

    multiple_distinct = (
        fixture_envelope + "\n" + fixture_envelope.replace(
            '"fixture":"cc-03-postgresql18-rationale-correct"',
            '"fixture":"cc-02-comparison-bound-is-valid"',
        )
    )
    unchanged, no_normalization = runner.normalize_plain_text_response(multiple_distinct)
    require(unchanged == multiple_distinct and no_normalization is None,
            "plain-text normalization must fail closed across distinct recognized envelopes")

    repeated_identical = fixture_envelope + "\n" + fixture_envelope
    unchanged, no_normalization = runner.normalize_plain_text_response(repeated_identical)
    require(unchanged == repeated_identical and no_normalization is None,
            "plain-text normalization must fail closed across repeated identical envelopes")

    truncated_ambiguous = (
        fixture_envelope + '\n{"response":"formal-rigor-fixture-response@1","fixture":"unfinished"'
    )
    unchanged, no_normalization = runner.normalize_plain_text_response(truncated_ambiguous)
    require(unchanged == truncated_ambiguous and no_normalization is None,
            "plain-text normalization must fail closed when another recognized envelope is truncated")

    nested_envelope = f"[{fixture_envelope}]"
    unchanged, no_normalization = runner.normalize_plain_text_response(nested_envelope)
    require(unchanged == nested_envelope and no_normalization is None,
            "plain-text normalization must not extract a recognized object nested in another JSON value")

    nested_schema_echo = json.dumps({
        "schema": {
            "type": "object",
            "properties": {
                "response": {"const": "formal-rigor-fixture-response@1"},
            },
        },
    })
    unchanged, no_normalization = runner.normalize_plain_text_response(nested_schema_echo)
    require(unchanged == nested_schema_echo and no_normalization is None,
            "plain-text normalization must not mistake a nested schema/prompt echo for an envelope")

    reordered_truncated = (
        fixture_envelope +
        '\n{"fixture":"unfinished","details":{},'
        '"response":"formal-rigor-fixture-response@1"'
    )
    unchanged, no_normalization = runner.normalize_plain_text_response(reordered_truncated)
    require(unchanged == reordered_truncated and no_normalization is None,
            "plain-text normalization must detect truncated recognized envelopes regardless of field order")

    with tempfile.TemporaryDirectory(dir="C:\\tmp") as tmp:
        tmp_root = Path(tmp)
        result_dir = tmp_root / "agy-call"
        def build_schema_packet(packet: Path) -> None:
            packet.mkdir()
            runner.write_json(packet / "output.schema.json", {
                "type": "object",
                "required": ["response", "fixture", "focused_output"],
                "properties": {
                    "response": {"const": "formal-rigor-fixture-response@1"},
                    "fixture": {"type": "string"},
                    "focused_output": {"type": "array"},
                },
            })
        original_run = runner.subprocess.run
        executed_command: list[str] = []
        def fake_agy_run(command, *args, **kwargs):
            executed_command.extend(command)
            return SimpleNamespace(returncode=0, stdout=agy_stdout, stderr="")
        runner.subprocess.run = fake_agy_run
        try:
            record = runner.execute_call(
                result_dir=result_dir,
                packet_root=tmp_root / "packets",
                packet_builder=build_schema_packet,
                prompt="return JSON",
                harness="agy",
                executable="agy",
                model="gemini-3.6-flash-medium",
                identity={
                    "kind": "arm", "provider_plan": "noncursor-degraded-v3",
                    "fixture": "cc-03-postgresql18-rationale-correct",
                    "phase": "arms", "reasoning_effort": "medium",
                    "preflight_sha256": preflight_sha256,
                    "campaign_plan_sha256": campaign_sha256,
                },
                source_commit="a" * 40,
                timeout_seconds=60,
                output_schema_name="output.schema.json",
            )
        finally:
            runner.subprocess.run = original_run
        require((result_dir / "events.jsonl").read_text(encoding="utf-8") == agy_stdout,
                "agy raw stdout must remain losslessly retained in events.jsonl")
        require((result_dir / "response.json").read_text(encoding="utf-8") == fixture_envelope,
                "agy response.json did not materialize the single recognized envelope")
        require(record.get("json_parseable") is True,
                "normalized agy response was not recorded as JSON-parseable")
        require(record.get("schema_valid") is True and record.get("schema_errors") == [],
                "execute_call did not validate the normalized response against its packet schema")
        require(record.get("reasoning_effort") == "medium" and
                "--effort" in executed_command and
                executed_command[executed_command.index("--effort") + 1] == "medium",
                "v2 arm call did not record and invoke the same actual AGY effort")
        require(record.get("execution_policy") ==
                runner.execution_policy("noncursor-degraded-v3"),
                "terminal call omitted its pinned execution policy")
        require(record.get("phase") == "arms" and
                record.get("model") == "gemini-3.6-flash-medium" and
                record.get("preflight_sha256") == preflight_sha256 and
                record.get("campaign_plan_sha256") == campaign_sha256,
                "terminal call omitted its exact phase/model/preflight/campaign binding")
        require(record.get("packet_root") == str((tmp_root / "packets").resolve()),
                "terminal call omitted its canonical packet root")
        require('"required": [' in executed_command[-1] and
                executed_command[-1].rstrip().endswith(runner.EXACT_JSON_BOUNDARY),
                "v2 AGY arm call did not receive the exact schema and terminal boundary")
        require(record.get("response_normalization") ==
                "extracted-single-recognized-json-envelope",
                "agy call record omitted explicit response_normalization metadata")
        require(record.get("provider_plan") == "noncursor-degraded-v3",
                "every terminal call record must retain the provider-plan identity")

    valid_adjudication = {
        "adjudication": "formal-rigor-semantic-adjudication@1",
        "fixture": "tm-01-false-mvd",
        "verdict": "VALID",
        "obligations": [{
            "claim_id": "c1", "obligation": "paired attributes do not establish an independent-set MVD",
            "status": "SATISFIED", "response_coordinates": ["focused_output[0]"], "reason": "The response refutes it."
        }],
        "forbidden_propositions": [{
            "claim_id": "c1", "proposition": "fixed columns are inherently unindexable",
            "present": False, "response_coordinates": [], "reason": "The response does not assert it."
        }],
        "coverage_limits": [],
    }
    with tempfile.TemporaryDirectory() as evidence_tmp:
        evidence_dir = Path(evidence_tmp)
        response_bytes = json.dumps(valid_adjudication).encode("utf-8")
        (evidence_dir / "response.json").write_bytes(response_bytes)
        runner.write_json(evidence_dir / "call.json", {
            "schema": "formal-rigor-live-call@1", "kind": "semantic",
            "provider_plan": "noncursor-degraded-v1", "source_commit": "a" * 40,
            "repetition": 1, "fixture": "tm-01-false-mvd", "seat": "a",
            "transport": "completed", "json_parseable": True, "schema_valid": False,
            "schema_errors": ["forced regression"],
            "response_sha256": runner.sha256_bytes(response_bytes),
            "secret_screen": {"passed": True},
        })
        evidence_errors = runner.response_evidence_errors(
            evidence_dir, ROOT / "formal-rigor-semantic-adjudication.schema.json",
        )
        require(any("schema-valid" in error for error in evidence_errors),
                "semantic evidence accepted a call whose strict schema check failed")
        runner.write_json(evidence_dir / "call.json", {
            "schema": "formal-rigor-live-call@1", "kind": "semantic",
            "provider_plan": "noncursor-degraded-v1", "source_commit": "a" * 40,
            "repetition": 1, "fixture": "tm-01-false-mvd", "seat": "a",
            "transport": "completed", "json_parseable": True, "schema_valid": True,
            "schema_errors": [], "response_sha256": runner.sha256_bytes(response_bytes),
            "secret_screen": {"passed": True},
        })
        copied_seat_errors = runner.response_evidence_errors(
            evidence_dir, ROOT / "formal-rigor-semantic-adjudication.schema.json",
            expected_identity={
                "kind": "semantic", "provider_plan": "noncursor-degraded-v1",
                "source_commit": "a" * 40, "repetition": 1,
                "fixture": "tm-01-false-mvd", "seat": "b",
            },
        )
        require(any("seat" in error for error in copied_seat_errors),
                "semantic evidence from one seat can masquerade as the other seat")
        materialized = evidence_dir / "materialized.response.json"
        runner.write_json(evidence_dir / "call.json", {
            **json.loads((evidence_dir / "call.json").read_text(encoding="utf-8")),
            "response_sha256": "0" * 64,
        })
        copied = runner.materialize_qualified_response(
            evidence_dir, materialized,
            ROOT / "formal-rigor-semantic-adjudication.schema.json",
            expected_identity={"kind": "semantic", "seat": "a"},
        )
        require(copied is False and not materialized.exists(),
                "materialization accepted a response that no longer matches terminal evidence")
    require(runner.validate_adjudication(valid_adjudication, truth) == [],
            "valid semantic adjudication failed validation")
    invalid_adjudication = dict(valid_adjudication, verdict="PASS")
    require(runner.validate_adjudication(invalid_adjudication, truth),
            "invalid semantic verdict was accepted")
    rejected = False
    try:
        runner.verify_source_state("0" * 40, require_clean=False)
    except ValueError:
        rejected = True
    require(rejected, "runner accepted a source commit that is not checked-out HEAD")

    print("formal-rigor live runner: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
