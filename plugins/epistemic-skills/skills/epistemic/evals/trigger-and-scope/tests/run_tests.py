#!/usr/bin/env python3
"""Polarity tests for epistemic (the guide) trigger discipline and scope."""

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
    require(score_path.is_file(), f"missing epistemic trigger-and-scope scorer: {score_path}")
    spec = importlib.util.spec_from_file_location("epistemic_scope", score_path)
    scorer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scorer)
    fixtures = json.loads((ROOT / "fixtures.json").read_text(encoding="utf-8"))
    require([f["id"] for f in fixtures] == [
        "guide-question-how-to-use-suite", "midwork-failure-needs-triage",
        "explicit-skill-request-honoured-directly", "instructions-unavailable-limit-stated",
        "claimed-fix-checked-at-consumer", "method-returns-no-material-finding",
        "complementary-method-distinct-question", "midwork-decision-persisted",
        "guidance-already-loaded-work-resumes", "routine-work-no-applicable-trigger",
        "narrate-every-nonapplication", "second-dispatcher-added-alongside",
        "guide-asked-to-create-task-ledger",
    ], "epistemic fixture inventory drifted")
    require(len({f["id"] for f in fixtures}) == len(fixtures), "fixture ids not unique")
    require(all(f["expected_action"] in scorer.ACTIONS for f in fixtures), "fixture expected_action outside the action vocabulary")
    require(sum(1 for f in fixtures if f["holdout"]) == 3, "exactly three fixtures are holdout")
    require({f["id"] for f in fixtures if f["holdout"]} == {
        "midwork-failure-needs-triage", "claimed-fix-checked-at-consumer",
        "routine-work-no-applicable-trigger",
    }, "holdout set drifted")

    balanced = scorer.score(fixtures, json.loads((ROOT / "examples" / "balanced.json").read_text(encoding="utf-8")))
    require(balanced["pass"], balanced["failures"])
    require(balanced["actions"] == {"use-method": 8, "no-fire": 5}, balanced["actions"])

    for name in ("overfiring", "underfiring", "parody"):
        report = scorer.score(fixtures, json.loads((ROOT / "examples" / f"{name}.json").read_text(encoding="utf-8")))
        require(not report["pass"], f"{name} example unexpectedly passed")

    over = scorer.score(fixtures, json.loads((ROOT / "examples" / "overfiring.json").read_text(encoding="utf-8")))
    require(sum("expected no-fire" in failure for failure in over["failures"]) == 5, over["failures"])

    under = scorer.score(fixtures, json.loads((ROOT / "examples" / "underfiring.json").read_text(encoding="utf-8")))
    require(sum("expected use-method, got no-fire" in failure for failure in under["failures"]) == 8, under["failures"])

    parody = scorer.score(fixtures, json.loads((ROOT / "examples" / "parody.json").read_text(encoding="utf-8")))
    require(sum("expected no-fire" in failure for failure in parody["failures"]) == 5, parody["failures"])
    require(sum("claimed_use true requires instructions_loaded true" in failure for failure in parody["failures"]) == 8, parody["failures"])
    require(any("never claim use of unavailable instructions" in failure for failure in parody["failures"]), parody["failures"])
    require(any("expected method triage, got gauntlet" in failure for failure in parody["failures"]), parody["failures"])

    unknown = scorer.score(fixtures, [{"id": "routine-work-no-applicable-trigger", "action": "fire-everything"}])
    require(any("unknown action 'fire-everything'" in failure for failure in unknown["failures"]), unknown["failures"])

    duplicated = scorer.score(fixtures, [
        {"id": "routine-work-no-applicable-trigger", "action": "no-fire"},
        {"id": "routine-work-no-applicable-trigger", "action": "no-fire"},
    ])
    require(any("response ids missing or duplicated" in failure for failure in duplicated["failures"]), duplicated["failures"])

    # Off-contract shapes must produce named failures, never a traceback.
    top_level = scorer.score(fixtures, True)
    require(not top_level["pass"], "non-list responses unexpectedly passed")
    require(any("responses must be an array" in failure for failure in top_level["failures"]), top_level["failures"])
    nonstring_action = scorer.score(fixtures, [{"id": "routine-work-no-applicable-trigger", "action": ["no-fire"]}])
    require(any("action must be a string" in failure for failure in nonstring_action["failures"]), nonstring_action["failures"])
    nonstring_id = scorer.score(fixtures, [{"id": ["routine-work-no-applicable-trigger"], "action": "no-fire"}])
    require(any("response ids missing or duplicated" in failure for failure in nonstring_id["failures"]), nonstring_id["failures"])
    nonstring_method = scorer.score(fixtures, [{
        "id": "midwork-failure-needs-triage", "action": "use-method", "method": ["triage"],
        "instructions_loaded": True, "claimed_use": True, "contribution": "A contribution.",
    }])
    require(any("method must be a string" in failure for failure in nonstring_method["failures"]), nonstring_method["failures"])
    guide_as_method = scorer.score(fixtures, [{
        "id": "midwork-failure-needs-triage", "action": "use-method", "method": "epistemic",
        "instructions_loaded": True, "claimed_use": True, "contribution": "A contribution.",
    }])
    require(any("permitted only on a guide question" in failure for failure in guide_as_method["failures"]), guide_as_method["failures"])


    # Regression (2026-10-24, Codex P2): an "explanation" field on a no-fire
    # row is a silence breach - the scorer must reject any key beyond id and
    # action on no-fire rows, not only the battery's enumerated fields.
    explained = json.loads((ROOT / "examples" / "balanced.json").read_text(encoding="utf-8"))
    for row in explained:
        if isinstance(row, dict) and row.get("action") == "no-fire":
            row["explanation"] = "No applicable trigger; staying silent."
    explained_report = scorer.score(fixtures, explained)
    require(not explained_report["pass"], "no-fire rows carrying an explanation field unexpectedly passed")
    require(any("no-fire must be silent" in failure for failure in explained_report["failures"]), explained_report["failures"])


    # Regression (2026-10-24, Dot review of the held branches): a response
    # whose id is outside the fixture inventory must fail by name, never be
    # silently ignored - the omission did-it-land's scorer was fixed for
    # (C4) was still present here.
    extra_rows = json.loads((ROOT / "examples" / "balanced.json").read_text(encoding="utf-8")) + [{"id": "nonexistent-trial", "action": "garbage"}]
    extra_report = scorer.score(fixtures, extra_rows)
    require(not extra_report["pass"], "an extra response with an unknown id unexpectedly passed")
    require(any("response id not in fixtures" in failure for failure in extra_report["failures"]), extra_report["failures"])
    print("epistemic trigger-and-scope: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
