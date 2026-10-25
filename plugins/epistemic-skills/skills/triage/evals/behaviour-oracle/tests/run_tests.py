#!/usr/bin/env python3
"""Polarity tests for the triage behaviour-oracle corpus."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    score_path = ROOT / "score.py"
    require(score_path.is_file(), f"missing triage behaviour-oracle scorer: {score_path}")
    spec = importlib.util.spec_from_file_location("triage_behaviour_oracle", score_path)
    scorer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scorer)
    fixtures = json.loads((ROOT / "fixtures.json").read_text(encoding="utf-8"))
    require([f["id"] for f in fixtures] == [
        "clause-known-broken-eliminates-one", "clause-check-red-cause-unknown",
        "clause-readout-named-wrong-cause-unknown", "clause-observation-contradicts-assertion",
        "degraded-no-readout-self-probed", "degraded-subject-unreachable",
        "degraded-fault-not-reproducible", "degraded-observation-would-be-destructive",
        "degraded-lying-readout", "core-plausible-cause-not-observed",
        "control-discriminating-observation-cause", "control-report-wrong-not-broken",
    ], "triage behaviour-oracle fixture inventory drifted")
    require(len({f["id"] for f in fixtures}) == len(fixtures), "fixture ids not unique")
    require(all(f["expected_verdict"] in scorer.VERDICTS for f in fixtures), "expected_verdict outside the verdict vocabulary")
    require(sum(1 for f in fixtures if f.get("holdout")) == 3, "holdout subset must be exactly 3 fixtures")
    # No NARROWED case may be shape-only: every NARROWED fixture pins the
    # eliminated candidate its scenario's observation eliminates, with the
    # canonical label disclosed in the scenario text (Dot P2, 2026-10-24 -
    # both degraded NARROWED fixtures previously pinned []).
    require(all(f.get("expected_eliminated") for f in fixtures if f["expected_verdict"] == "NARROWED"), "a NARROWED fixture pins no expected_eliminated")

    balanced = scorer.score(fixtures, json.loads((ROOT / "examples" / "balanced.json").read_text(encoding="utf-8")))
    require(balanced["pass"], balanced["failures"])
    # Counts reflect the 2026-10-24 ground-truth corrections: five
    # fixtures whose scenarios contain no eliminating observation
    # (clause-check-red-cause-unknown, degraded-observation-would-be-
    # destructive, degraded-no-readout-self-probed,
    # clause-observation-contradicts-assertion,
    # core-plausible-cause-not-observed) are pinned UNKNOWN, not
    # NARROWED, per triage's verdict definitions.
    require(balanced["verdicts"] == {"NARROWED": 3, "UNKNOWN": 7, "CAUSE": 1, "NOT-BROKEN": 1}, balanced["verdicts"])

    over = scorer.score(fixtures, json.loads((ROOT / "examples" / "overclaiming.json").read_text(encoding="utf-8")))
    require(not over["pass"], "overclaiming parody unexpectedly passed")
    require(any("most plausible candidate was named as the cause" in failure for failure in over["failures"]), over["failures"])
    require(any("CAUSE requires a discriminating observation" in failure for failure in over["failures"]), over["failures"])
    require(any("expected NARROWED, got CAUSE" in failure for failure in over["failures"]), over["failures"])
    require(any("expected NARROWED, got NOT-BROKEN" in failure for failure in over["failures"]), over["failures"])

    under = scorer.score(fixtures, json.loads((ROOT / "examples" / "underclaiming.json").read_text(encoding="utf-8")))
    require(not under["pass"], "underclaiming parody unexpectedly passed")
    require(any("expected CAUSE, got UNKNOWN" in failure for failure in under["failures"]), under["failures"])
    require(any("expected NOT-BROKEN, got UNKNOWN" in failure for failure in under["failures"]), under["failures"])

    unknown = scorer.score(fixtures, [{"id": "clause-check-red-cause-unknown", "verdict": "ROOT-CAUSE-CONFIRMED"}])
    require(any("unknown verdict 'ROOT-CAUSE-CONFIRMED'" in failure for failure in unknown["failures"]), unknown["failures"])

    duplicated = scorer.score(fixtures, [
        {"id": "degraded-subject-unreachable", "verdict": "UNKNOWN"},
        {"id": "degraded-subject-unreachable", "verdict": "UNKNOWN"},
    ])
    require(any("response ids missing or duplicated" in failure for failure in duplicated["failures"]), duplicated["failures"])

    top_level = scorer.score(fixtures, True)
    require(not top_level["pass"], "non-list responses unexpectedly passed")
    require(any("responses must be an array" in failure for failure in top_level["failures"]), top_level["failures"])

    nonstring_verdict = scorer.score(fixtures, [{"id": "clause-check-red-cause-unknown", "verdict": ["NARROWED"]}])
    require(any("verdict must be a string" in failure for failure in nonstring_verdict["failures"]), nonstring_verdict["failures"])


    # Regression (2026-10-24, Dot review of the held branches): a response
    # whose id is outside the fixture inventory must fail by name, never be
    # silently ignored - the omission did-it-land's scorer was fixed for
    # (C4) was still present here.
    extra_rows = json.loads((ROOT / "examples" / "balanced.json").read_text(encoding="utf-8")) + [{"id": "nonexistent-trial", "action": "garbage"}]
    extra_report = scorer.score(fixtures, extra_rows)
    require(not extra_report["pass"], "an extra response with an unknown id unexpectedly passed")
    require(any("response id not in fixtures" in failure for failure in extra_report["failures"]), extra_report["failures"])

    # Regression (2026-10-24, Dot P2 on the handoff-2 verification): the
    # scorer accepted a NARROWED response with `eliminated` and
    # `discriminating_observation` omitted entirely whenever the fixture
    # pinned no expected_eliminated - which was both degraded NARROWED
    # fixtures. NARROWED now requires at least one eliminated candidate
    # and the observation that eliminated it (the contract C5 enforces in
    # the triage trigger scorer); omitted, empty, and blank values all
    # fail, for every NARROWED fixture.
    balanced_rows = json.loads((ROOT / "examples" / "balanced.json").read_text(encoding="utf-8"))

    def mutated(rows: list, fid: str, key: str, value: object, omit: bool) -> list:
        rows = copy.deepcopy(rows)
        for row in rows:
            if row["id"] == fid:
                if omit:
                    row.pop(key, None)
                else:
                    row[key] = value
        return rows

    narrowed_ids = [f["id"] for f in fixtures if f["expected_verdict"] == "NARROWED"]
    require(narrowed_ids == ["clause-known-broken-eliminates-one", "degraded-fault-not-reproducible", "degraded-lying-readout"], narrowed_ids)
    for fid in narrowed_ids:
        for key, value, omit, fragment in [
            ("eliminated", None, True, "NARROWED requires at least one eliminated candidate"),
            ("eliminated", [], False, "NARROWED requires at least one eliminated candidate"),
            ("eliminated", [""], False, "NARROWED requires at least one eliminated candidate"),
            ("eliminated", ["   "], False, "must not contain empty ids"),
            ("discriminating_observation", None, True, "NARROWED requires a discriminating observation"),
            ("discriminating_observation", "", False, "NARROWED requires a discriminating observation"),
            ("discriminating_observation", "   ", False, "NARROWED requires a discriminating observation"),
        ]:
            report = scorer.score(fixtures, mutated(balanced_rows, fid, key, value, omit))
            require(not report["pass"], f"{fid}: NARROWED with {key} {'omitted' if omit else repr(value)} unexpectedly passed")
            require(any(fragment in failure for failure in report["failures"]), report["failures"])

    # Regression (2026-10-24, issue #282 - an independent-model
    # challenge of the frozen scorer, reproduced locally by Dot and
    # classified a blocking P2 on the held branches): the mirror image
    # of the C11 defect. C11 enforced what a verdict must carry;
    # nothing enforced what a verdict must NOT carry. An UNKNOWN
    # response naming eliminated candidates passed, contradicting
    # UNKNOWN's own definition - insufficient evidence to eliminate -
    # and a NOT-BROKEN response naming a cause passed, contradicting
    # the verdict itself. Both are now barred. The nuance Dot named
    # stands: an observation that eliminates nothing remains
    # compatible with UNKNOWN, so only the eliminated list is barred
    # there - proven below in both directions.
    unknown_ids = [f["id"] for f in fixtures if f["expected_verdict"] == "UNKNOWN"]
    require(unknown_ids == [
        "clause-check-red-cause-unknown", "clause-readout-named-wrong-cause-unknown",
        "clause-observation-contradicts-assertion", "degraded-no-readout-self-probed",
        "degraded-subject-unreachable", "degraded-observation-would-be-destructive",
        "core-plausible-cause-not-observed",
    ], unknown_ids)
    for fid in unknown_ids:
        report = scorer.score(fixtures, mutated(balanced_rows, fid, "eliminated", ["a candidate the evidence does not eliminate"], False))
        require(not report["pass"], f"{fid}: UNKNOWN with a nonempty eliminated list unexpectedly passed")
        require(any("UNKNOWN must not name eliminated candidates" in failure for failure in report["failures"]), report["failures"])
    # UNKNOWN + observation + eliminated fails on the eliminated list;
    # UNKNOWN + the same observation alone still passes.
    both = mutated(balanced_rows, "clause-check-red-cause-unknown", "discriminating_observation", "the failure output only: expected 104.10, got 104.09", False)
    both = mutated(both, "clause-check-red-cause-unknown", "eliminated", ["tax rounding change"], False)
    report = scorer.score(fixtures, both)
    require(not report["pass"], "UNKNOWN with an observation and an eliminated candidate unexpectedly passed")
    require(any("UNKNOWN must not name eliminated candidates" in failure for failure in report["failures"]), report["failures"])
    observation_only = mutated(balanced_rows, "clause-check-red-cause-unknown", "discriminating_observation", "the failure output only: expected 104.10, got 104.09", False)
    report = scorer.score(fixtures, observation_only)
    require(report["pass"], report["failures"])

    named_not_broken = mutated(balanced_rows, "control-report-wrong-not-broken", "named_cause", "export service truncates at 100 rows", False)
    report = scorer.score(fixtures, named_not_broken)
    require(not report["pass"], "NOT-BROKEN with a named cause unexpectedly passed")
    require(any("NOT-BROKEN never names a cause" in failure for failure in report["failures"]), report["failures"])
    print("triage behaviour-oracle: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
