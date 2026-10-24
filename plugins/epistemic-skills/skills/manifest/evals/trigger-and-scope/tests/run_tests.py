#!/usr/bin/env python3
"""Polarity tests for manifest trigger discipline and mission-custody scope."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def load(name: str) -> list:
    return json.loads((ROOT / "examples" / f"{name}.json").read_text(encoding="utf-8"))


def mutated(scorer, fixtures, balanced, fid, **changes):
    rows = copy.deepcopy(balanced)
    for row in rows:
        if row["id"] == fid:
            row.update(changes)
    return scorer.score(fixtures, rows)


def main() -> int:
    score_path = ROOT / "score.py"
    require(score_path.is_file(), f"missing manifest trigger-and-scope scorer: {score_path}")
    spec = importlib.util.spec_from_file_location("manifest_scope", score_path)
    scorer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scorer)
    fixtures = json.loads((ROOT / "fixtures.json").read_text(encoding="utf-8"))
    require([f["id"] for f in fixtures] == [
        "open-multisession-schema-migration", "open-cross-agent-handoff-relay",
        "explicit-manifest-this", "open-acceptance-path-unavailable",
        "resume-clean-after-interruption", "resume-drift-found",
        "verify-close-different-acceptor", "verify-self-acceptance-refused",
        "verify-scope-crossing-unacknowledged", "nofire-routine-one-step-lookup",
        "nofire-multistep-ticket-sufficient", "nofire-reanchor-decisions-decision-ledger",
        "nofire-resume-never-custodied",
    ], "manifest fixture inventory drifted")
    require(len({f["id"] for f in fixtures}) == len(fixtures), "fixture ids not unique")
    require(all(f["expected_action"] in scorer.ACTIONS for f in fixtures), "fixture expected_action outside the action vocabulary")
    require([f["id"] for f in fixtures if f["holdout"]] == [
        "open-cross-agent-handoff-relay", "resume-drift-found",
        "nofire-reanchor-decisions-decision-ledger",
    ], "manifest holdout set drifted — exactly 3 holdouts, spread across fire and no-fire")

    balanced = load("balanced")
    report = scorer.score(fixtures, balanced)
    require(report["pass"], report["failures"])
    require(report["actions"] == {
        "open-mission": 4, "resume-mission": 2, "verify-mission": 3, "no-fire": 4,
    }, report["actions"])

    for name in ("overfiring", "underfiring", "parody"):
        report = scorer.score(fixtures, load(name))
        require(not report["pass"], f"{name} example unexpectedly passed")
    over = scorer.score(fixtures, load("overfiring"))
    require(sum("expected no-fire" in failure for failure in over["failures"]) == 4, over["failures"])
    under = scorer.score(fixtures, load("underfiring"))
    require(any("expected open-mission, got no-fire" in failure for failure in under["failures"]), under["failures"])
    require(any("expected resume-mission, got no-fire" in failure for failure in under["failures"]), under["failures"])
    require(any("expected verify-mission, got no-fire" in failure for failure in under["failures"]), under["failures"])
    parody = scorer.score(fixtures, load("parody"))
    require(any("envelope.scope_in must be nonempty" in failure for failure in parody["failures"]), parody["failures"])
    require(any("an empty envelope field is unbounded" in failure for failure in parody["failures"]), parody["failures"])
    require(any("expected no-fire, got open-mission" in failure for failure in parody["failures"]), parody["failures"])
    require(any("expected resume-mission, got open-mission" in failure for failure in parody["failures"]), parody["failures"])
    require(any("do not open a mission whose acceptance path is unavailable" in failure for failure in parody["failures"]), parody["failures"])

    # Named contract rules, exercised as mutations of the balanced example.
    empty_env = mutated(scorer, fixtures, balanced, "open-multisession-schema-migration",
                        envelope={"scope_in": "", "scope_out": "x", "permissions": "x", "protected": "x"})
    require(any("an empty envelope field is unbounded" in failure for failure in empty_env["failures"]), empty_env["failures"])
    opened_anyway = mutated(scorer, fixtures, balanced, "open-acceptance-path-unavailable", mission_opened=True)
    require(any("do not open a mission whose acceptance path is unavailable" in failure for failure in opened_anyway["failures"]), opened_anyway["failures"])
    drift_ignored = mutated(scorer, fixtures, balanced, "resume-drift-found", continued=True)
    require(any("reconcile before anything else" in failure for failure in drift_ignored["failures"]), drift_ignored["failures"])
    self_accepted = mutated(scorer, fixtures, balanced, "verify-self-acceptance-refused", accepted=True)
    require(any("refuses self-acceptance" in failure for failure in self_accepted["failures"]), self_accepted["failures"])
    crossing_accepted = mutated(scorer, fixtures, balanced, "verify-scope-crossing-unacknowledged", accepted=True)
    require(any("scope crossings unacknowledged" in failure for failure in crossing_accepted["failures"]), crossing_accepted["failures"])
    crossing_acknowledged = mutated(scorer, fixtures, balanced, "verify-scope-crossing-unacknowledged",
                                    accepted=True, scope_acknowledged=True)
    require(crossing_acknowledged["pass"], crossing_acknowledged["failures"])
    noisy_negative = mutated(scorer, fixtures, balanced, "nofire-routine-one-step-lookup",
                             envelope={"scope_in": "x", "scope_out": "x", "permissions": "x", "protected": "x"})
    require(any("no-fire must be silent" in failure for failure in noisy_negative["failures"]), noisy_negative["failures"])

    # Malformed input fails closed with named failures, never a traceback.
    top_level = scorer.score(fixtures, True)
    require(not top_level["pass"], "non-list responses unexpectedly passed")
    require(any("responses must be an array" in failure for failure in top_level["failures"]), top_level["failures"])
    unknown = scorer.score(fixtures, [{"id": "explicit-manifest-this", "action": "certify-complete"}])
    require(any("unknown action 'certify-complete'" in failure for failure in unknown["failures"]), unknown["failures"])
    duplicated = scorer.score(fixtures, [
        {"id": "nofire-routine-one-step-lookup", "action": "no-fire"},
        {"id": "nofire-routine-one-step-lookup", "action": "no-fire"},
    ])
    require(any("response ids missing or duplicated" in failure for failure in duplicated["failures"]), duplicated["failures"])
    nonstring_action = scorer.score(fixtures, [{"id": "nofire-routine-one-step-lookup", "action": ["no-fire"]}])
    require(any("action must be a string" in failure for failure in nonstring_action["failures"]), nonstring_action["failures"])
    nonstring_id = scorer.score(fixtures, [{"id": ["nofire-routine-one-step-lookup"], "action": "no-fire"}])
    require(any("response ids missing or duplicated" in failure for failure in nonstring_id["failures"]), nonstring_id["failures"])
    bad_envelope = scorer.score(fixtures, [{
        "id": "explicit-manifest-this", "action": "open-mission",
        "instruction_verbatim": True, "envelope": "everything",
        "acceptance_path_checked": True, "mission_opened": True,
    }])
    require(any("envelope must be an object" in failure for failure in bad_envelope["failures"]), bad_envelope["failures"])
    bad_drift = scorer.score(fixtures, [{
        "id": "resume-clean-after-interruption", "action": "resume-mission",
        "mission_id": "archive-rebuild-2026", "drift_status": ["clean"], "continued": True,
    }])
    require(any("drift_status must be one of" in failure for failure in bad_drift["failures"]), bad_drift["failures"])

    print("manifest trigger-and-scope: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
