#!/usr/bin/env python3
"""Deterministic tests for blinded packet construction and scoring."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
BLINDED = HERE.parent
PARENT = BLINDED.parent
sys.path.insert(0, str(BLINDED))

from runner import REPO_ROOT, load, prepare, score_packets  # noqa: E402


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def response_from_result(result: dict[str, object]) -> dict[str, object]:
    return {
        "schema": "proportionality-fixture-response@1",
        **result,
    }


def main() -> int:
    arms = load(BLINDED / "arms.json")
    arm_ids = [arm["id"] for arm in arms["arms"]]
    require(
        arm_ids
        == [
            "main-80eb0827",
            "pr46-candidate-a4f2210f",
            "candidate-final-4e1945e",
            "full-ceremony",
            "always-routine",
        ],
        "the five required arms must remain pinned",
    )
    require(arms["invocation"]["settings"]["fresh_context_per_fixture"] is True, "isolation lost")

    scenarios = load(BLINDED / "scenarios.json")["scenarios"]
    fixtures = load(PARENT / "fixtures.json")["fixtures"]
    require(len(scenarios) == 18, "expected 18 self-contained scenarios")
    require({x["id"] for x in scenarios} == {x["id"] for x in fixtures}, "inventory drift")

    balanced = load(PARENT / "examples" / "balanced.json")
    with tempfile.TemporaryDirectory() as first_raw, tempfile.TemporaryDirectory() as second_raw:
        first = Path(first_raw)
        second = Path(second_raw)
        # Unit-test the pure packet projection after the source-verification
        # boundary. The CLI never exposes this bypass and always verifies the
        # checkout against the arm commit.
        prepare("candidate-final-4e1945e", 1, first, REPO_ROOT, _source_already_verified=True)
        prepare("candidate-final-4e1945e", 1, second, REPO_ROOT, _source_already_verified=True)
        require(load(first / "manifest.json") == load(second / "manifest.json"), "manifest not deterministic")

        for packet in (first / "packets").glob("*/input.json"):
            data = load(packet)
            serialized = json.dumps(data)
            for hidden in ("expected_paths", "required_skills", "require_escalation", "category"):
                require(hidden not in serialized, f"packet leaks scorer-only field {hidden}")
        for result in balanced["results"]:
            out = first / "responses" / f"{result['fixture_id']}.json"
            out.write_text(json.dumps(response_from_result(result)), encoding="utf-8")
        require(score_packets(first) == 0, "balanced raw responses must score PASS")
        evidence = load(first / "evidence.json")
        require(evidence["status"] == "PASS", "evidence status mismatch")
        require(len(evidence["response_hashes"]) == 18, "all raw responses must be hashed")

    blocked = (BLINDED / "results" / "BLOCKED.md").read_text(encoding="utf-8")
    require(blocked.count("`NOT_RUN`") == 5, "all live arms must be explicitly NOT_RUN")
    require("No live result is claimed" in blocked, "block record must reject fabricated evidence")

    print("blinded proportionality packets: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
