#!/usr/bin/env python3
"""Polarity tests for metacognate trigger discipline and examination scope."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    score_path = ROOT / "score.py"
    require(score_path.is_file(), f"missing metacognate trigger-and-scope scorer: {score_path}")
    spec = importlib.util.spec_from_file_location("metacognate_scope", score_path)
    scorer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scorer)
    fixtures = json.loads((ROOT / "fixtures.json").read_text(encoding="utf-8"))
    require([f["id"] for f in fixtures] == [
        "evidence-conflicts-migration-assertion", "proxy-signups-stand-for-retention",
        "confidence-outruns-single-friendly-pilot", "uncertain-assumption-changes-cache-choice",
        "explicit-reflection-request-pricing", "sound-approach-survives-challenge",
        "routine-directly-checkable-spelling-fix", "settled-choice-no-new-evidence",
        "resume-stage-arrives-with-certain-basis", "reconstruct-context-available-in-task",
        "check-does-not-exercise-the-claim", "settled-choice-basis-changed-by-new-fees",
        "no-report-for-a-nonapplication",
    ], "metacognate fixture inventory drifted")
    require(len({f["id"] for f in fixtures}) == len(fixtures), "fixture ids not unique")
    require(all(f["expected_action"] in scorer.ACTIONS for f in fixtures), "fixture expected_action outside the action vocabulary")
    require(sum(1 for f in fixtures if f["holdout"]) == 3, "exactly three fixtures are holdout")
    require({f["id"] for f in fixtures if f["holdout"]} == {
        "proxy-signups-stand-for-retention", "sound-approach-survives-challenge",
        "settled-choice-no-new-evidence",
    }, "holdout set drifted")

    balanced = scorer.score(fixtures, json.loads((ROOT / "examples" / "balanced.json").read_text(encoding="utf-8")))
    require(balanced["pass"], balanced["failures"])
    require(balanced["actions"] == {"examine": 8, "no-fire": 5}, balanced["actions"])

    for name in ("overfiring", "underfiring", "parody"):
        report = scorer.score(fixtures, json.loads((ROOT / "examples" / f"{name}.json").read_text(encoding="utf-8")))
        require(not report["pass"], f"{name} example unexpectedly passed")

    over = scorer.score(fixtures, json.loads((ROOT / "examples" / "overfiring.json").read_text(encoding="utf-8")))
    require(sum("expected no-fire" in failure for failure in over["failures"]) == 5, over["failures"])

    under = scorer.score(fixtures, json.loads((ROOT / "examples" / "underfiring.json").read_text(encoding="utf-8")))
    require(sum("expected examine, got no-fire" in failure for failure in under["failures"]) == 8, under["failures"])

    parody = scorer.score(fixtures, json.loads((ROOT / "examples" / "parody.json").read_text(encoding="utf-8")))
    require(sum("expected no-fire" in failure for failure in parody["failures"]) == 5, parody["failures"])
    require(any("expected verdict approach-retained, got approach-corrected" in failure for failure in parody["failures"]), parody["failures"])
    require(any("expected verdict question-reframed, got approach-corrected" in failure for failure in parody["failures"]), parody["failures"])
    require(any("expected verdict confidence-recalibrated, got approach-corrected" in failure for failure in parody["failures"]), parody["failures"])

    unknown = scorer.score(fixtures, [{"id": "routine-directly-checkable-spelling-fix", "action": "reflect-deeply"}])
    require(any("unknown action 'reflect-deeply'" in failure for failure in unknown["failures"]), unknown["failures"])

    duplicated = scorer.score(fixtures, [
        {"id": "routine-directly-checkable-spelling-fix", "action": "no-fire"},
        {"id": "routine-directly-checkable-spelling-fix", "action": "no-fire"},
    ])
    require(any("response ids missing or duplicated" in failure for failure in duplicated["failures"]), duplicated["failures"])

    # Off-contract shapes must produce named failures, never a traceback.
    top_level = scorer.score(fixtures, True)
    require(not top_level["pass"], "non-list responses unexpectedly passed")
    require(any("responses must be an array" in failure for failure in top_level["failures"]), top_level["failures"])
    nonstring_action = scorer.score(fixtures, [{"id": "routine-directly-checkable-spelling-fix", "action": ["no-fire"]}])
    require(any("action must be a string" in failure for failure in nonstring_action["failures"]), nonstring_action["failures"])
    nonstring_id = scorer.score(fixtures, [{"id": ["routine-directly-checkable-spelling-fix"], "action": "no-fire"}])
    require(any("response ids missing or duplicated" in failure for failure in nonstring_id["failures"]), nonstring_id["failures"])
    nonstring_verdict = scorer.score(fixtures, [{
        "id": "evidence-conflicts-migration-assertion", "action": "examine",
        "outcome_named": "Records preserved intact.", "decisive_assumption": "Counts imply content.",
        "discriminating_observation": "Field-level mismatches in a sample.", "verdict": ["approach-corrected"],
    }])
    require(any("verdict must be a string" in failure for failure in nonstring_verdict["failures"]), nonstring_verdict["failures"])
    unknown_verdict = scorer.score(fixtures, [{
        "id": "evidence-conflicts-migration-assertion", "action": "examine",
        "outcome_named": "Records preserved intact.", "decisive_assumption": "Counts imply content.",
        "discriminating_observation": "Field-level mismatches in a sample.", "verdict": "case-closed",
    }])
    require(any("unknown verdict 'case-closed'" in failure for failure in unknown_verdict["failures"]), unknown_verdict["failures"])

    print("metacognate trigger-and-scope: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
