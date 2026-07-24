#!/usr/bin/env python3
"""Deterministic tests for the resumable live-battery runner."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile


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
    require(len(runner.full_semantic_plan()) == 132,
            "semantic plan must contain two isolated seats for each of 66 candidate responses")
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
