#!/usr/bin/env python3
"""Polarity tests for Open Questions trigger discipline and auto-fire scope."""

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
    require(score_path.is_file(), f"missing Open Questions trigger-and-scope scorer: {score_path}")
    spec = importlib.util.spec_from_file_location("open_questions_scope", score_path)
    scorer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scorer)
    fixtures = json.loads((ROOT / "fixtures.json").read_text(encoding="utf-8"))
    require([f["id"] for f in fixtures] == [
        "explicit-phrase-full", "explicit-mid-execution-full", "fuzzy-brief-no-fire",
        "design-dialogue-defers", "reversible-fork-absent-park", "irreversible-fork-absent-hold",
        "irreversible-fork-present-fork-scoped", "fork-offer-declined-deferred",
        "fork-offer-accepted-walked", "explicit-release-parks",
    ], "Open Questions fixture inventory drifted")

    balanced = scorer.score(fixtures, json.loads((ROOT / "examples" / "balanced.json").read_text(encoding="utf-8")))
    require(balanced["pass"], balanced["failures"])
    require(balanced["actions"] == {"full-interview": 3, "no-fire": 2, "park-and-proceed": 1, "hold-escalate": 1, "fork-interview": 3}, balanced["actions"])

    for name in ("overfiring", "scope-creep", "lost-deferral"):
        report = scorer.score(fixtures, json.loads((ROOT / "examples" / f"{name}.json").read_text(encoding="utf-8")))
        require(not report["pass"], f"{name} parody unexpectedly passed")
    creep = scorer.score(fixtures, json.loads((ROOT / "examples" / "scope-creep.json").read_text(encoding="utf-8")))
    require(any("scope creep" in failure for failure in creep["failures"]), creep["failures"])
    lost = scorer.score(fixtures, json.loads((ROOT / "examples" / "lost-deferral.json").read_text(encoding="utf-8")))
    require(any("deferred with tracker_ref" in failure or "coverage_limits" in failure for failure in lost["failures"]), lost["failures"])
    require(any("parks EVERY remaining ledger item" in failure for failure in lost["failures"]), lost["failures"])

    # Regression for issue #277 (E11 scorer crash): a response carrying
    # `parked` as an integer count must score as a per-fixture shape
    # failure, never raise — one mistyped field must not void an epoch.
    import copy

    count = scorer.score(fixtures, json.loads((ROOT / "examples" / "parked-as-count.json").read_text(encoding="utf-8")))
    require(not count["pass"], "parked-as-count unexpectedly passed")
    require(count["failures"] and all(f.startswith("explicit-release-parks:") for f in count["failures"]), count["failures"])
    require(any("parked must be a list" in failure for failure in count["failures"]), count["failures"])
    require(sum(count["actions"].values()) == 10, count["actions"])  # every fixture still scored

    count2_rows = copy.deepcopy(json.loads((ROOT / "examples" / "balanced.json").read_text(encoding="utf-8")))
    for row in count2_rows:
        if row["id"] == "reversible-fork-absent-park":
            row["parked"] = 1
    count2 = scorer.score(fixtures, count2_rows)
    require(not count2["pass"], "park-and-proceed parked-as-count unexpectedly passed")
    require(any(f.startswith("reversible-fork-absent-park:") and "parked must be a list" in f for f in count2["failures"]), count2["failures"])

    # Synthetic response-contract regressions; not a model or native-host trial.
    for case in json.loads((ROOT / "v7-cases.json").read_text(encoding="utf-8")):
        report = scorer.score([case["fixture"]], [case["response"]])
        require(report["pass"], report["failures"])
        for mutation in case["reject_mutations"]:
            report = scorer.score([case["fixture"]], [dict(case["response"], **mutation)])
            require(not report["pass"], f"{case['fixture']['id']}: unsafe mutation passed: {mutation}")


    # Regression (2026-10-24, Dot review of the held branches): a response
    # whose id is outside the fixture inventory must fail by name, never be
    # silently ignored - the omission did-it-land's scorer was fixed for
    # (C4) was still present here.
    extra_rows = json.loads((ROOT / "examples" / "balanced.json").read_text(encoding="utf-8")) + [{"id": "nonexistent-trial", "action": "garbage"}]
    extra_report = scorer.score(fixtures, extra_rows)
    require(not extra_report["pass"], "an extra response with an unknown id unexpectedly passed")
    require(any("response id not in fixtures" in failure for failure in extra_report["failures"]), extra_report["failures"])
    print("Open Questions trigger-and-scope: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
