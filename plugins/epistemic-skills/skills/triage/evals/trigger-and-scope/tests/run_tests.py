#!/usr/bin/env python3
"""Polarity tests for triage trigger discipline and verdict scope."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def load(name: str) -> list:
    return json.loads((ROOT / "examples" / f"{name}.json").read_text(encoding="utf-8"))


def main() -> int:
    score_path = ROOT / "score.py"
    require(score_path.is_file(), f"missing triage trigger-and-scope scorer: {score_path}")
    spec = importlib.util.spec_from_file_location("triage_scope", score_path)
    scorer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scorer)
    fixtures = json.loads((ROOT / "fixtures.json").read_text(encoding="utf-8"))
    require([f["id"] for f in fixtures] == [
        "deploy-check-red-two-causes-left", "search-latency-reranker-isolated",
        "readout-flags-cache-cause-unobserved", "metrics-doc-contradicted-by-trace",
        "unreachable-license-server-unknown", "reported-print-delay-within-bounds",
        "intermittent-webhook-narrowed", "vague-unease-no-subject-health-first",
        "cause-known-remedy-underway", "queue-library-change-question",
        "deterministic-config-parse-error", "deploy-landed-verification-no-failure",
        "future-cert-expiry-watch-request",
    ], "triage fixture inventory drifted")
    require(len({f["id"] for f in fixtures}) == len(fixtures), "fixture ids not unique")
    require(all(f["expected_action"] in scorer.ACTIONS for f in fixtures), "fixture expected_action outside the action vocabulary")
    require(all(f["trigger"] in {"explicit", "auto", "state", "none"} for f in fixtures), "fixture trigger outside the trigger vocabulary")
    require(all(isinstance(f["clause"], str) and f["clause"].strip() for f in fixtures), "every fixture carries a clause")
    require([f["id"] for f in fixtures if f["holdout"]] == [
        "search-latency-reranker-isolated", "unreachable-license-server-unknown",
        "deterministic-config-parse-error",
    ], "triage holdout set drifted — exactly 3 holdouts, spread across fire and no-fire")
    require(all(f.get("expected_verdict") in scorer.VERDICTS for f in fixtures if f["expected_action"] == "investigate"),
            "every investigate fixture carries an expected_verdict in the verdict vocabulary")

    balanced = scorer.score(fixtures, load("balanced"))
    require(balanced["pass"], balanced["failures"])
    require(balanced["actions"] == {"investigate": 7, "no-fire": 6}, balanced["actions"])

    for name in ("overfiring", "underfiring", "parody"):
        report = scorer.score(fixtures, load(name))
        require(not report["pass"], f"{name} responder unexpectedly passed")
    over = scorer.score(fixtures, load("overfiring"))
    require(sum("expected no-fire" in failure for failure in over["failures"]) == 6, over["failures"])
    under = scorer.score(fixtures, load("underfiring"))
    require(sum("expected investigate, got no-fire" in failure for failure in under["failures"]) == 7, under["failures"])
    parody = scorer.score(fixtures, load("parody"))
    require(any("CAUSE requires a nonempty discriminating_observation" in failure for failure in parody["failures"]), parody["failures"])
    require(any("expected verdict" in failure for failure in parody["failures"]), parody["failures"])
    require(any("expected no-fire, got investigate" in failure for failure in parody["failures"]), parody["failures"])

    # Verdict-shape regressions: each mutation must be named, never passed.
    dressed_unknown = scorer.score(fixtures, [
        dict(row, verdict="UNKNOWN", named_cause="host hardware failure")
        if row["id"] == "unreachable-license-server-unknown" else row
        for row in load("balanced")
    ])
    require(any("never dressed up as a most-likely cause" in failure for failure in dressed_unknown["failures"]), dressed_unknown["failures"])
    bare_narrowed = scorer.score(fixtures, [
        {key: value for key, value in row.items() if key != "eliminated"}
        if row["id"] == "deploy-check-red-two-causes-left" else row
        for row in load("balanced")
    ])
    require(any("NARROWED requires an eliminated array" in failure for failure in bare_narrowed["failures"]), bare_narrowed["failures"])
    bare_not_broken = scorer.score(fixtures, [
        dict(row, discriminating_observation=None)
        if row["id"] == "reported-print-delay-within-bounds" else row
        for row in load("balanced")
    ])
    require(any("NOT-BROKEN requires a nonempty discriminating_observation" in failure for failure in bare_not_broken["failures"]), bare_not_broken["failures"])
    noisy_silence = scorer.score(fixtures, [
        dict(row, verdict="CAUSE") if row["id"] == "cause-known-remedy-underway" else row
        for row in load("balanced")
    ])
    require(any("no-fire must be silent" in failure for failure in noisy_silence["failures"]), noisy_silence["failures"])

    # Malformed input fails closed with named failures, never a traceback.
    unknown = scorer.score(fixtures, [{"id": "deploy-check-red-two-causes-left", "action": "certify-fixed"}])
    require(any("unknown action 'certify-fixed'" in failure for failure in unknown["failures"]), unknown["failures"])
    duplicated = scorer.score(fixtures, [
        {"id": "deterministic-config-parse-error", "action": "no-fire"},
        {"id": "deterministic-config-parse-error", "action": "no-fire"},
    ])
    require(any("response ids missing or duplicated" in failure for failure in duplicated["failures"]), duplicated["failures"])
    top_level = scorer.score(fixtures, True)
    require(not top_level["pass"], "non-list responses unexpectedly passed")
    require(any("responses must be an array" in failure for failure in top_level["failures"]), top_level["failures"])
    nonstring_action = scorer.score(fixtures, [{"id": "deterministic-config-parse-error", "action": ["no-fire"]}])
    require(any("action must be a string" in failure for failure in nonstring_action["failures"]), nonstring_action["failures"])
    nonstring_verdict = scorer.score(fixtures, [{
        "id": "search-latency-reranker-isolated", "action": "investigate", "verdict": ["CAUSE"],
        "discriminating_observation": "cohort comparison", "named_cause": "the reranker",
        "provider": "superpowers-systematic-debugging",
    }])
    require(any("verdict must be a string" in failure for failure in nonstring_verdict["failures"]), nonstring_verdict["failures"])
    nonstring_id = scorer.score(fixtures, [{"id": ["deterministic-config-parse-error"], "action": "no-fire"}])
    require(any("response ids missing or duplicated" in failure for failure in nonstring_id["failures"]), nonstring_id["failures"])


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

    print("triage trigger-and-scope: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
