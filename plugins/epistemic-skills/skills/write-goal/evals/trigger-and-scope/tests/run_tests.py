#!/usr/bin/env python3
"""Polarity tests for write-goal trigger discipline and completion-contract scope."""

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
    require(score_path.is_file(), f"missing write-goal trigger-and-scope scorer: {score_path}")
    spec = importlib.util.spec_from_file_location("write_goal_scope", score_path)
    scorer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scorer)
    fixtures = json.loads((ROOT / "fixtures.json").read_text(encoding="utf-8"))
    require([f["id"] for f in fixtures] == [
        "explicit-author-request-fires", "define-done-fires", "approved-start-fires",
        "unapproved-create-not-started", "proxy-metric-separation",
        "existing-goal-not-replaced", "no-primitive-returns-contract",
        "pause-honored-mid-start", "outcome-unchosen-blocking-question",
        "long-task-alone-no-fire", "plan-execution-no-fire",
        "scheduled-reminder-no-fire", "colloquial-goal-wording-no-fire",
        "definition-of-done-template-no-fire",
    ], "write-goal fixture inventory drifted")
    require(len({f["id"] for f in fixtures}) == len(fixtures), "fixture ids not unique")
    require(all(f["expected_action"] in scorer.ACTIONS for f in fixtures), "fixture expected_action outside the action vocabulary")

    balanced = scorer.score(fixtures, json.loads((ROOT / "examples" / "balanced.json").read_text(encoding="utf-8")))
    require(balanced["pass"], balanced["failures"])
    require(balanced["actions"] == {
        "author-contract": 4, "start-goal": 3, "ask-blocking-question": 1,
        "honor-interrupt": 1, "no-fire": 5,
    }, balanced["actions"])

    for name in ("overfiring", "underfiring"):
        report = scorer.score(fixtures, json.loads((ROOT / "examples" / f"{name}.json").read_text(encoding="utf-8")))
        require(not report["pass"], f"{name} parody unexpectedly passed")
    over = scorer.score(fixtures, json.loads((ROOT / "examples" / "overfiring.json").read_text(encoding="utf-8")))
    require(sum("expected no-fire" in failure for failure in over["failures"]) == 5, over["failures"])
    require(any("separate state changes" in failure for failure in over["failures"]), over["failures"])
    require(any("opt-in" in failure for failure in over["failures"]), over["failures"])
    require(any("never replaced silently" in failure for failure in over["failures"]), over["failures"])
    require(any("never pretend the goal was started" in failure for failure in over["failures"]), over["failures"])
    require(any("past the user's pause" in failure for failure in over["failures"]), over["failures"])
    require(any("expected ask-blocking-question, got author-contract" in failure for failure in over["failures"]), over["failures"])
    under = scorer.score(fixtures, json.loads((ROOT / "examples" / "underfiring.json").read_text(encoding="utf-8")))
    require(any("expected author-contract, got no-fire" in failure for failure in under["failures"]), under["failures"])
    require(any("expected start-goal, got author-contract" in failure for failure in under["failures"]), under["failures"])
    require(any("goal_control.authorized_priority" in failure for failure in under["failures"]), under["failures"])
    require(any("goal_control.proxy_failure" in failure for failure in under["failures"]), under["failures"])
    require(any("not silently dropped" in failure for failure in under["failures"]), under["failures"])
    require(any("expected ask-blocking-question, got no-fire" in failure for failure in under["failures"]), under["failures"])

    unknown = scorer.score(fixtures, [{"id": "explicit-author-request-fires", "action": "certify-complete"}])
    require(any("unknown action 'certify-complete'" in failure for failure in unknown["failures"]), unknown["failures"])

    duplicated = scorer.score(fixtures, [
        {"id": "long-task-alone-no-fire", "action": "no-fire"},
        {"id": "long-task-alone-no-fire", "action": "no-fire"},
    ])
    require(any("response ids missing or duplicated" in failure for failure in duplicated["failures"]), duplicated["failures"])

    malformed = scorer.score(fixtures, [{
        "id": "outcome-unchosen-blocking-question",
        "action": "ask-blocking-question",
        "question": "Which outcome should the goal target?",
        "options": "adopt-oidc",
    }])
    require(any("options must be an array of bare ids" in failure for failure in malformed["failures"]), malformed["failures"])

    # Off-contract shapes must produce named failures, never a traceback.
    top_level = scorer.score(fixtures, True)
    require(not top_level["pass"], "non-list responses unexpectedly passed")
    require(any("responses must be an array" in failure for failure in top_level["failures"]), top_level["failures"])
    unhashable_option = scorer.score(fixtures, [{
        "id": "outcome-unchosen-blocking-question",
        "action": "ask-blocking-question",
        "question": "Which outcome should the goal target?",
        "options": [{"id": "adopt-oidc"}, "patch-current-stack"],
    }])
    require(any("only bare string ids" in failure for failure in unhashable_option["failures"]), unhashable_option["failures"])
    nonstring_action = scorer.score(fixtures, [{"id": "long-task-alone-no-fire", "action": ["no-fire"]}])
    require(any("action must be a string" in failure for failure in nonstring_action["failures"]), nonstring_action["failures"])
    nonstring_id = scorer.score(fixtures, [{"id": ["long-task-alone-no-fire"], "action": "no-fire"}])
    require(any("response ids missing or duplicated" in failure for failure in nonstring_id["failures"]), nonstring_id["failures"])
    nonobject_contract = scorer.score(fixtures, [{
        "id": "explicit-author-request-fires",
        "action": "author-contract",
        "contract": "a big contract",
        "goal_control": False,
        "presented_for_approval": True,
    }])
    require(any("contract must be an object" in failure for failure in nonobject_contract["failures"]), nonobject_contract["failures"])
    require(any("goal_control must be an object" in failure for failure in nonobject_contract["failures"]), nonobject_contract["failures"])

    print("write-goal trigger-and-scope: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
