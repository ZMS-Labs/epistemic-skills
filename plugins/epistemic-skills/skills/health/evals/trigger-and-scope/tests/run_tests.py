#!/usr/bin/env python3
"""Polarity tests for health trigger discipline and readout scope."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FIXTURE_IDS = [
    "general-state-all-ok", "before-change-blast-radius-warn",
    "after-power-event-critical", "claim-about-to-bear-load",
    "feels-wrong-unnamed-unreachable", "credential-failure-unknown",
    "probe-tool-absent-unknown", "bound-undeclared-unknown",
    "registry-unreachable-coverage-unknown",
    "known-broken-cause-wanted-no-fire", "one-metric-one-command-no-fire",
    "change-question-not-state-no-fire",
    "routine-reversible-nothing-shared-no-fire",
]


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def load(name: str) -> list:
    return json.loads((ROOT / "examples" / f"{name}.json").read_text(encoding="utf-8"))


def main() -> int:
    score_path = ROOT / "score.py"
    require(score_path.is_file(), f"missing health trigger-and-scope scorer: {score_path}")
    spec = importlib.util.spec_from_file_location("health_scope", score_path)
    scorer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scorer)
    fixtures = json.loads((ROOT / "fixtures.json").read_text(encoding="utf-8"))
    require([f["id"] for f in fixtures] == FIXTURE_IDS, "health fixture inventory drifted")
    require(len({f["id"] for f in fixtures}) == len(fixtures), "fixture ids not unique")
    require(all(f["expected_action"] in scorer.ACTIONS for f in fixtures), "fixture expected_action outside the action vocabulary")
    require(sum(1 for f in fixtures if f.get("holdout")) == 3, "exactly 3 fixtures must be holdouts")
    require({f["id"] for f in fixtures if f.get("holdout")} == {
        "credential-failure-unknown", "registry-unreachable-coverage-unknown",
        "one-metric-one-command-no-fire",
    }, "health holdout set drifted")

    balanced_rows = load("balanced")
    balanced = scorer.score(fixtures, balanced_rows)
    require(balanced["pass"], balanced["failures"])
    require(balanced["actions"] == {"readout": 9, "no-fire": 4}, balanced["actions"])

    for name in ("overfiring", "underfiring", "parody"):
        report = scorer.score(fixtures, load(name))
        require(not report["pass"], f"{name} parody unexpectedly passed")
    over = scorer.score(fixtures, load("overfiring"))
    require(sum("expected no-fire" in failure for failure in over["failures"]) == 4, over["failures"])
    under = scorer.score(fixtures, load("underfiring"))
    require(sum("expected readout, got no-fire" in failure for failure in under["failures"]) == 9, under["failures"])
    parody = scorer.score(fixtures, load("parody"))
    require(sum("subjects must match the probe-determined states exactly" in failure for failure in parody["failures"]) == 8, parody["failures"])

    by_fixture = {f["id"]: f for f in fixtures}
    by_row = {r["id"]: r for r in balanced_rows}

    # The aggregation rule is the skill: each planted lie about the rollup
    # must fail with its named reason, even when the subjects are honest.
    greenwashed = dict(by_row["claim-about-to-bear-load"], rollup="OK")
    report = scorer.score([by_fixture["claim-about-to-bear-load"]], [greenwashed])
    require(any("at best UNKNOWN" in failure for failure in report["failures"]), report["failures"])
    softened = dict(by_row["after-power-event-critical"], rollup="WARN")
    report = scorer.score([by_fixture["after-power-event-critical"]], [softened])
    require(any("any CRITICAL subject makes the rollup CRITICAL" in failure for failure in report["failures"]), report["failures"])
    inflated = dict(by_row["general-state-all-ok"], rollup="WARN")
    report = scorer.score([by_fixture["general-state-all-ok"]], [inflated])
    require(any("rollup OK requires every subject OK" in failure for failure in report["failures"]), report["failures"])
    upgraded = copy.deepcopy(by_row["credential-failure-unknown"])
    for subject in upgraded["subjects"]:
        if subject["name"] == "backup":
            subject["state"] = "OK"
    upgraded["rollup"] = "OK"
    upgraded["ordered_subjects"] = ["api", "backup"]
    report = scorer.score([by_fixture["credential-failure-unknown"]], [upgraded])
    require(any("subjects must match the probe-determined states exactly" in failure for failure in report["failures"]), report["failures"])

    unordered = dict(by_row["before-change-blast-radius-warn"], ordered_subjects=["api", "disk", "database"])
    report = scorer.score([by_fixture["before-change-blast-radius-warn"]], [unordered])
    require(any("CRITICAL first, then UNKNOWN, then WARN, then OK" in failure for failure in report["failures"]), report["failures"])
    dropped = dict(by_row["before-change-blast-radius-warn"], ordered_subjects=["disk", "api"])
    report = scorer.score([by_fixture["before-change-blast-radius-warn"]], [dropped])
    require(any("must be a permutation of the subject names" in failure for failure in report["failures"]), report["failures"])
    bad_state = copy.deepcopy(by_row["general-state-all-ok"])
    bad_state["subjects"][0]["state"] = "FINE"
    report = scorer.score([by_fixture["general-state-all-ok"]], [bad_state])
    require(any("unknown state 'FINE'" in failure for failure in report["failures"]), report["failures"])
    bad_rollup = dict(by_row["general-state-all-ok"], rollup="FINE")
    report = scorer.score([by_fixture["general-state-all-ok"]], [bad_rollup])
    require(any("unknown rollup 'FINE'" in failure for failure in report["failures"]), report["failures"])
    noisy = {"id": "known-broken-cause-wanted-no-fire", "action": "no-fire", "rollup": "OK"}
    report = scorer.score([by_fixture["known-broken-cause-wanted-no-fire"]], [noisy])
    require(any("no-fire must be silent" in failure for failure in report["failures"]), report["failures"])

    # Malformed input fails closed with named failures, never a traceback.
    top_level = scorer.score(fixtures, True)
    require(not top_level["pass"], "non-list responses unexpectedly passed")
    require(any("responses must be an array" in failure for failure in top_level["failures"]), top_level["failures"])
    duplicated = scorer.score(fixtures, [
        {"id": "general-state-all-ok", "action": "no-fire"},
        {"id": "general-state-all-ok", "action": "no-fire"},
    ])
    require(any("response ids missing or duplicated" in failure for failure in duplicated["failures"]), duplicated["failures"])
    unknown = scorer.score(fixtures, [{"id": "general-state-all-ok", "action": "diagnose"}])
    require(any("unknown action 'diagnose'" in failure for failure in unknown["failures"]), unknown["failures"])
    nonstring_action = scorer.score(fixtures, [{"id": "general-state-all-ok", "action": ["readout"]}])
    require(any("action must be a string" in failure for failure in nonstring_action["failures"]), nonstring_action["failures"])
    nonstring_id = scorer.score(fixtures, [{"id": ["general-state-all-ok"], "action": "no-fire"}])
    require(any("response ids missing or duplicated" in failure for failure in nonstring_id["failures"]), nonstring_id["failures"])
    unhashable_state = scorer.score(fixtures, [{
        "id": "general-state-all-ok", "action": "readout",
        "subjects": [{"name": "api", "state": ["OK"]}],
        "rollup": "OK", "ordered_subjects": ["api"],
    }])
    require(any("unknown state" in failure for failure in unhashable_state["failures"]), unhashable_state["failures"])
    missing = scorer.score(fixtures, [{"id": "general-state-all-ok", "action": "no-fire"}])
    require(any("response missing" in failure for failure in missing["failures"]), missing["failures"])


    # Regression (2026-10-24, Dot review of the held branches): a response
    # whose id is outside the fixture inventory must fail by name, never be
    # silently ignored - the omission did-it-land's scorer was fixed for
    # (C4) was still present here.
    extra_rows = json.loads((ROOT / "examples" / "balanced.json").read_text(encoding="utf-8")) + [{"id": "nonexistent-trial", "action": "garbage"}]
    extra_report = scorer.score(fixtures, extra_rows)
    require(not extra_report["pass"], "an extra response with an unknown id unexpectedly passed")
    require(any("response id not in fixtures" in failure for failure in extra_report["failures"]), extra_report["failures"])
    print("health trigger-and-scope: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
