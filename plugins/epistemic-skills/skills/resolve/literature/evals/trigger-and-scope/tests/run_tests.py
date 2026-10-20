#!/usr/bin/env python3
"""Polarity tests for evidence-research trigger discipline and evidence-record scope."""

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
    require(score_path.is_file(), f"missing evidence-research trigger-and-scope scorer: {score_path}")
    spec = importlib.util.spec_from_file_location("evidence_research_scope", score_path)
    scorer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scorer)
    fixtures = json.loads((ROOT / "fixtures.json").read_text(encoding="utf-8"))
    require([f["id"] for f in fixtures] == [
        "research-says-premise-fires", "imminent-connector-call-fires",
        "explicit-lit-review-fires", "citation-verification-fires",
        "design-choice-no-scholarly-premise-no-fire", "own-code-claim-no-fire",
        "casual-paper-mention-no-fire", "news-web-search-no-fire",
        "trusted-internal-doc-no-fire", "fuzzy-recon-no-fire",
        "verdict-requested-matrix-declined", "retracted-paper-excluded",
        "contrasting-heavy-disputed", "reception-live-not-memory",
    ], "evidence-research fixture inventory drifted")
    ids = [f["id"] for f in fixtures]
    require(len(set(ids)) == len(ids), "fixture ids are not unique")
    for fixture in fixtures:
        require(fixture["expected_action"] in scorer.ACTIONS,
                f"{fixture['id']}: unknown expected_action {fixture['expected_action']!r}")
        require(fixture["trigger"] in {"explicit", "auto", "implicit", "none", "state"},
                f"{fixture['id']}: unknown trigger {fixture['trigger']!r}")

    balanced_rows = json.loads((ROOT / "examples" / "balanced.json").read_text(encoding="utf-8"))
    balanced = scorer.score(fixtures, balanced_rows)
    require(balanced["pass"], balanced["failures"])
    require(balanced["actions"] == {
        "run-evidence": 6, "no-fire": 6, "precall-gate": 1, "evidence-gate": 1,
    }, balanced["actions"])

    for name in ("overfiring", "underfiring"):
        report = scorer.score(fixtures, json.loads((ROOT / "examples" / f"{name}.json").read_text(encoding="utf-8")))
        require(not report["pass"], f"{name} parody unexpectedly passed")
    over = scorer.score(fixtures, json.loads((ROOT / "examples" / "overfiring.json").read_text(encoding="utf-8")))
    require(sum("expected no-fire, got run-evidence" in failure for failure in over["failures"]) == 6, over["failures"])
    require(any("never renders GO/NO-GO" in failure for failure in over["failures"]), over["failures"])
    require(any("must leave the support set" in failure for failure in over["failures"]), over["failures"])
    require(any("never as clean support" in failure for failure in over["failures"]), over["failures"])
    require(any("remembered tallies" in failure for failure in over["failures"]), over["failures"])
    under = scorer.score(fixtures, json.loads((ROOT / "examples" / "underfiring.json").read_text(encoding="utf-8")))
    require(any("expected run-evidence, got no-fire" in failure for failure in under["failures"]), under["failures"])
    require(any("expected precall-gate, got no-fire" in failure for failure in under["failures"]), under["failures"])
    require(any("never declines the evidence" in failure for failure in under["failures"]), under["failures"])
    require(any("disputed label" in failure for failure in under["failures"]), under["failures"])
    require(any("pulled live this run" in failure for failure in under["failures"]), under["failures"])

    # Scorer rejects an unknown action.
    mutated = copy.deepcopy(balanced_rows)
    mutated[0]["action"] = "audit-everything"
    report = scorer.score(fixtures, mutated)
    require(not report["pass"], "unknown action unexpectedly accepted")
    require(any("unknown action" in failure for failure in report["failures"]), report["failures"])

    # Scorer rejects a duplicated response id.
    duplicated = copy.deepcopy(balanced_rows) + [copy.deepcopy(balanced_rows[0])]
    report = scorer.score(fixtures, duplicated)
    require(not report["pass"], "duplicated response id unexpectedly accepted")
    require(any("missing or duplicated" in failure for failure in report["failures"]), report["failures"])

    # List-reading fields fail closed on off-contract shapes, never crash.
    misshapen = copy.deepcopy(balanced_rows)
    for row in misshapen:
        if row["id"] == "retracted-paper-excluded":
            row["support"] = "10.5555/vigil.2018.112"
            row["excluded_from_support"] = {"doi": "10.5555/vigil.2014.881"}
        if row["id"] == "contrasting-heavy-disputed":
            row["disputed"] = True
    report = scorer.score(fixtures, misshapen)
    require(not report["pass"], "misshapen list fields unexpectedly accepted")
    require(sum("must be an array of bare DOIs" in failure for failure in report["failures"]) == 3, report["failures"])

    # Off-contract scalar/element shapes (unhashable lists where strings belong,
    # objects inside DOI arrays) fail closed with named failures, never crash.
    unhashable = copy.deepcopy(balanced_rows)
    unhashable[0]["action"] = ["run-evidence"]
    unhashable[1]["id"] = ["imminent-connector-call-fires"]
    for row in unhashable:
        if row.get("id") == "contrasting-heavy-disputed":
            row["mode"] = ["deep"]
            row["terminal_state"] = ["contested-stable"]
        if row.get("id") == "retracted-paper-excluded":
            row["support"] = [{"doi": "10.5555/vigil.2018.112"}]
    report = scorer.score(fixtures, unhashable)
    require(not report["pass"], "off-contract scalar shapes unexpectedly accepted")
    require(any("unknown action" in failure for failure in report["failures"]), report["failures"])
    require(any("missing or duplicated" in failure for failure in report["failures"]), report["failures"])
    require(any("imminent-connector-call-fires: response missing" in failure for failure in report["failures"]), report["failures"])
    require(any("mode must name" in failure for failure in report["failures"]), report["failures"])
    require(any("terminal-state label" in failure for failure in report["failures"]), report["failures"])
    require(any("must be an array of bare DOIs" in failure for failure in report["failures"]), report["failures"])

    # Synthetic response-contract regressions; not a model or native-host trial.
    for case in json.loads((ROOT / "v7-cases.json").read_text(encoding="utf-8")):
        report = scorer.score([case["fixture"]], [case["response"]])
        require(report["pass"], report["failures"])
        for mutation in case["reject_mutations"]:
            report = scorer.score([case["fixture"]], [dict(case["response"], **mutation)])
            require(not report["pass"], f"{case['fixture']['id']}: unsafe mutation passed: {mutation}")

    # Incomplete provider outcomes have positive and fail-closed negative controls.
    for case in json.loads((ROOT / "v7.3-thread-cases.json").read_text()):
        report = scorer.score([case["fixture"]], [case["response"]])
        require(report["pass"], report["failures"])
        for mutation in case["reject_mutations"]:
            report = scorer.score([case["fixture"]], [dict(case["response"], **mutation)])
            require(not report["pass"], f"unsafe incomplete mutation passed: {mutation}")
        # A response cannot evade a complete fixture's evidence requirements
        # merely by relabeling itself as an incomplete Thread.
        ordinary = dict(case["fixture"])
        ordinary.pop("expected_terminal_state")
        ordinary.pop("provider_status")
        require(not scorer.score([ordinary], [case["response"]])["pass"],
                "incomplete outcome bypassed a complete fixture")

    # Partial verified holdings remain usable, but all evidence gates survive.
    case = json.loads((ROOT / "v7.3-thread-cases.json").read_text())[0]
    fixture = dict(case["fixture"], retracted_dois=["10.5555/retracted"],
                   contested_dois=["10.5555/contested"])
    partial = dict(case["response"], matrix_produced=True,
                   primary_content_checked=True, reception_checked_live=True,
                   support=["10.5555/verified"], disputed=["10.5555/contested"],
                   excluded_from_support=["10.5555/retracted"])
    require(scorer.score([fixture], [partial])["pass"], "verified partial evidence rejected")
    for mutation in ({"primary_content_checked": False}, {"reception_checked_live": False},
                     {"excluded_from_support": []}, {"disputed": []},
                     {"support": ["10.5555/retracted"]}, {"support": ["10.5555/contested"]}):
        require(not scorer.score([fixture], [dict(partial, **mutation)])["pass"],
                f"incomplete evidence gate bypassed: {mutation}")
    for field in ("provider_status", "coverage_limits", "primary_content_checked"):
        fixture = {"id": "silent", "expected_action": "no-fire"}
        require(not scorer.score([fixture], [{"id": "silent", "action": "no-fire", field: True}])["pass"],
                f"incomplete process field leaked into no-fire: {field}")

    case = json.loads((ROOT / "v7.3-thread-cases.json").read_text())[0]
    fixture = dict(case["fixture"], citation_check=True)
    unchecked = dict(case["response"], mode="citation-check", claim_result="unverified",
                     primary_content_checked=False, notices_checked=False,
                     artifact_persistence="repository")
    require(scorer.score([fixture], [unchecked])["pass"], "honest incomplete citation rejected")
    for mutation in ({"claim_result": "supported"}, {"claim_result": "qualified"},
                     {"claim_result": "unsupported"}, {"artifact_persistence": "none"},
                     {"claim_result": "supported", "primary_content_checked": True,
                      "notices_checked": True}):
        require(not scorer.score([fixture], [dict(unchecked, **mutation)])["pass"],
                f"incomplete citation falsely verified: {mutation}")

    print("evidence-research trigger-and-scope: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
