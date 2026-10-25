#!/usr/bin/env python3
"""Polarity tests for perspective trigger discipline and lens scope."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FIXTURE_IDS = [
    "focused-cache-assumption-fires", "explicit-different-lens-tradeoff-fires",
    "several-lenses-bounded-no-adjudication", "settled-evidence-no-fire",
    "routine-work-no-fire", "gauntlet-adjudication-no-fire",
    "adjacent-issue-no-fire", "reversibility-single-lens-fires",
    "metric-fitness-lens-fires", "implementation-not-authorized-no-fire",
    "evidence-unavailable-limit-fires", "no-material-finding-fires",
    "approval-verdict-no-fire",
]


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def load(name: str) -> list:
    return json.loads((ROOT / "examples" / f"{name}.json").read_text(encoding="utf-8"))


def main() -> int:
    score_path = ROOT / "score.py"
    require(score_path.is_file(), f"missing perspective trigger-and-scope scorer: {score_path}")
    spec = importlib.util.spec_from_file_location("perspective_scope", score_path)
    scorer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scorer)
    fixtures = json.loads((ROOT / "fixtures.json").read_text(encoding="utf-8"))
    require([f["id"] for f in fixtures] == FIXTURE_IDS, "perspective fixture inventory drifted")
    require(len({f["id"] for f in fixtures}) == len(fixtures), "fixture ids not unique")
    require(all(f["expected_action"] in scorer.ACTIONS for f in fixtures), "fixture expected_action outside the action vocabulary")
    require(sum(1 for f in fixtures if f.get("holdout")) == 3, "exactly 3 fixtures must be holdouts")
    require({f["id"] for f in fixtures if f.get("holdout")} == {
        "several-lenses-bounded-no-adjudication", "gauntlet-adjudication-no-fire",
        "evidence-unavailable-limit-fires",
    }, "perspective holdout set drifted")

    balanced_rows = load("balanced")
    balanced = scorer.score(fixtures, balanced_rows)
    require(balanced["pass"], balanced["failures"])
    require(balanced["actions"] == {"apply-lens": 7, "no-fire": 6}, balanced["actions"])

    for name in ("overfiring", "underfiring", "parody"):
        report = scorer.score(fixtures, load(name))
        require(not report["pass"], f"{name} parody unexpectedly passed")
    over = scorer.score(fixtures, load("overfiring"))
    require(sum("expected no-fire" in failure for failure in over["failures"]) == 6, over["failures"])
    under = scorer.score(fixtures, load("underfiring"))
    require(sum("expected apply-lens, got no-fire" in failure for failure in under["failures"]) == 7, under["failures"])
    parody = scorer.score(fixtures, load("parody"))
    require(sum("lens count is not adjudication" in failure for failure in parody["failures"]) == 7, parody["failures"])
    require(any("above the fixture maximum" in failure for failure in parody["failures"]), parody["failures"])

    by_fixture = {f["id"]: f for f in fixtures}
    by_row = {r["id"]: r for r in balanced_rows}

    # A verdict or an adjudication flag on a firing row is the boundary breach
    # this battery exists to catch, even when everything else is well-formed.
    verdict_row = dict(by_row["focused-cache-assumption-fires"], verdict="GO")
    report = scorer.score([by_fixture["focused-cache-assumption-fires"]], [verdict_row])
    require(any("lens count is not adjudication" in failure for failure in report["failures"]), report["failures"])
    adjudicated = dict(by_row["focused-cache-assumption-fires"], adjudication=True)
    report = scorer.score([by_fixture["focused-cache-assumption-fires"]], [adjudicated])
    require(any("lens count is not adjudication" in failure for failure in report["failures"]), report["failures"])

    single = dict(by_row["several-lenses-bounded-no-adjudication"], lenses_applied=1)
    report = scorer.score([by_fixture["several-lenses-bounded-no-adjudication"]], [single])
    require(any("below the fixture minimum" in failure for failure in report["failures"]), report["failures"])
    panel = dict(by_row["reversibility-single-lens-fires"], lenses_applied=3)
    report = scorer.score([by_fixture["reversibility-single-lens-fires"]], [panel])
    require(any("above the fixture maximum" in failure for failure in report["failures"]), report["failures"])
    wrong_finding = dict(by_row["no-material-finding-fires"], finding="insight")
    report = scorer.score([by_fixture["no-material-finding-fires"]], [wrong_finding])
    require(any("expected finding no-material-finding" in failure for failure in report["failures"]), report["failures"])
    noisy = {"id": "routine-work-no-fire", "action": "no-fire", "lens": "failure-mode lens"}
    report = scorer.score([by_fixture["routine-work-no-fire"]], [noisy])
    require(any("no-fire must be silent" in failure for failure in report["failures"]), report["failures"])
    zero = dict(by_row["focused-cache-assumption-fires"], lenses_applied=0)
    report = scorer.score([by_fixture["focused-cache-assumption-fires"]], [zero])
    require(any("lenses_applied must be an integer >= 1" in failure for failure in report["failures"]), report["failures"])
    wordy = dict(by_row["focused-cache-assumption-fires"], lenses_applied="one")
    report = scorer.score([by_fixture["focused-cache-assumption-fires"]], [wordy])
    require(any("lenses_applied must be an integer >= 1" in failure for failure in report["failures"]), report["failures"])
    no_lens = dict(by_row["focused-cache-assumption-fires"], lens="")
    report = scorer.score([by_fixture["focused-cache-assumption-fires"]], [no_lens])
    require(any("lens must be a nonempty string" in failure for failure in report["failures"]), report["failures"])
    bad_finding = dict(by_row["focused-cache-assumption-fires"], finding="verdict-go")
    report = scorer.score([by_fixture["focused-cache-assumption-fires"]], [bad_finding])
    require(any("unknown finding 'verdict-go'" in failure for failure in report["failures"]), report["failures"])

    # Malformed input fails closed with named failures, never a traceback.
    top_level = scorer.score(fixtures, True)
    require(not top_level["pass"], "non-list responses unexpectedly passed")
    require(any("responses must be an array" in failure for failure in top_level["failures"]), top_level["failures"])
    duplicated = scorer.score(fixtures, [
        {"id": "routine-work-no-fire", "action": "no-fire"},
        {"id": "routine-work-no-fire", "action": "no-fire"},
    ])
    require(any("response ids missing or duplicated" in failure for failure in duplicated["failures"]), duplicated["failures"])
    unknown = scorer.score(fixtures, [{"id": "routine-work-no-fire", "action": "convene-panel"}])
    require(any("unknown action 'convene-panel'" in failure for failure in unknown["failures"]), unknown["failures"])
    nonstring_action = scorer.score(fixtures, [{"id": "routine-work-no-fire", "action": ["no-fire"]}])
    require(any("action must be a string" in failure for failure in nonstring_action["failures"]), nonstring_action["failures"])
    nonstring_id = scorer.score(fixtures, [{"id": ["routine-work-no-fire"], "action": "no-fire"}])
    require(any("response ids missing or duplicated" in failure for failure in nonstring_id["failures"]), nonstring_id["failures"])
    missing = scorer.score(fixtures, [{"id": "routine-work-no-fire", "action": "no-fire"}])
    require(any("response missing" in failure for failure in missing["failures"]), missing["failures"])


    # Regression (2026-10-24, Dot review of the held branches): a response
    # whose id is outside the fixture inventory must fail by name, never be
    # silently ignored - the omission did-it-land's scorer was fixed for
    # (C4) was still present here.
    extra_rows = json.loads((ROOT / "examples" / "balanced.json").read_text(encoding="utf-8")) + [{"id": "nonexistent-trial", "action": "garbage"}]
    extra_report = scorer.score(fixtures, extra_rows)
    require(not extra_report["pass"], "an extra response with an unknown id unexpectedly passed")
    require(any("response id not in fixtures" in failure for failure in extra_report["failures"]), extra_report["failures"])
    print("perspective trigger-and-scope: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
