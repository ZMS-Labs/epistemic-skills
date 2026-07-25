#!/usr/bin/env python3
"""Deterministic tests for the resumable live-battery runner."""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import tempfile
import threading


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
    require(runner.default_codex_executable() == ("codex.cmd" if os.name == "nt" else "codex"),
            "default Codex executable must use the runnable Windows command shim")
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
    semantic_instruction = runner.semantic_prompt("tm-01-false-mvd")
    require("Perform the task now; do not acknowledge readiness" in semantic_instruction,
            "semantic prompt does not reject readiness-only responses")
    require("Do not use a Markdown fence" in semantic_instruction,
            "semantic prompt does not reject fenced JSON")

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
        forbidden_names = {"ground-truth.json", "score.py", "semantic-adjudication.md", "RESULTS.md"}
        require(not any(path.name in forbidden_names for path in candidate_packet.rglob("*")),
                "candidate packet leaked scorer-only or prior-result material")

        sealed = runner.sealed_packet_prompt(candidate_packet, "Return exactly one JSON object.")
        require("Return exactly one JSON object." in sealed,
                "sealed bridge prompt omitted the task instruction")
        require('"scenario.md"' in sealed and '"candidate/SKILL.md"' in sealed,
                "sealed bridge prompt omitted packet-relative source files")
        require(not any(name in sealed for name in forbidden_names),
                "sealed bridge prompt leaked scorer-only or prior-result material")
        require("Do not use tools, execute commands, or write files" in sealed,
                "sealed bridge prompt omitted its no-tool isolation instruction")
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

        result_dir = tmp_root / "result"
        require(runner.call_needed(result_dir), "fresh call should be needed")
        result_dir.mkdir()
        (result_dir / "call.json").write_text('{"transport":"completed"}', encoding="utf-8")
        require(not runner.call_needed(result_dir), "completed call must not be retried")

    command = runner.codex_command(
        codex="codex", model="gpt-5.6-sol", packet_dir=Path("packet"),
        response_path=Path("response.json"), prompt="return JSON",
    )
    joined = " ".join(str(item) for item in command)
    for marker in (
        "exec", "--ephemeral", "--ignore-user-config", "--sandbox read-only",
        "--skip-git-repo-check", "--disable plugins", "--disable apps",
        "--disable remote_plugin", "--disable plugin_sharing",
    ):
        require(marker in joined, f"codex command missing isolation marker: {marker}")

    agy = runner.agy_command(
        agy="agy", model="gemini-3.1-pro-high", packet_dir=Path("packet"),
        response_path=Path("response.json"), prompt="return JSON",
    )
    agy_joined = " ".join(str(item) for item in agy)
    for marker in (
        "agy", "--print", "--sandbox", "--dangerously-skip-permissions",
        "--mode plan", "--add-dir packet", "--model gemini-3.1-pro-high",
    ):
        require(marker in agy_joined, f"agy command missing isolation marker: {marker}")
    require(agy == [
        "agy", "--sandbox", "--dangerously-skip-permissions", "--mode", "plan",
        "--add-dir", "packet", "--model", "gemini-3.1-pro-high",
        "--print", "return JSON",
    ], "agy must grant headless read tools only inside the sandboxed packet directory")

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
    distinct = (
        '{"response":"formal-rigor-fixture-response@1","fixture":"a"}'
        '{"response":"formal-rigor-fixture-response@1","fixture":"b"}'
    )
    unchanged, no_normalization = runner.normalize_fleet_bridge_response(distinct)
    require(unchanged == distinct and no_normalization is None,
            "Fleet bridge normalization must fail closed across distinct fixture envelopes")

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
