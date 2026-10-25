#!/usr/bin/env python3
"""Polarity tests for the triage behaviour-oracle corpus."""

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
    print("triage behaviour-oracle: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
