#!/usr/bin/env python3
"""Polarity tests for watch trigger discipline and commission scope."""

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


def mutate(rows: list, fid: str, **changes) -> list:
    return [dict(row, **changes) if row["id"] == fid else row for row in rows]


def main() -> int:
    score_path = ROOT / "score.py"
    require(score_path.is_file(), f"missing watch trigger-and-scope scorer: {score_path}")
    spec = importlib.util.spec_from_file_location("watch_scope", score_path)
    scorer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scorer)
    fixtures = json.loads((ROOT / "fixtures.json").read_text(encoding="utf-8"))
    require([f["id"] for f in fixtures] == [
        "nas-free-space-bound-declared", "cert-expiry-no-substrate-found",
        "backup-watch-kill-switch-unproven", "queue-observer-destination-unreachable",
        "replication-watch-reproved-proven", "disk-watch-delivery-failure-suspect",
        "migration-watch-proof-then-disabled", "current-disk-state-now-health",
        "lag-bound-crossed-cause-wanted-triage", "orphan-log-retention-no-action",
        "daily-human-check-shorter-than-harm", "auto-remediate-restart-request",
        "session-as-observer-proposal",
    ], "watch fixture inventory drifted")
    require(len({f["id"] for f in fixtures}) == len(fixtures), "fixture ids not unique")
    require(all(f["expected_action"] in scorer.ACTIONS for f in fixtures), "fixture expected_action outside the action vocabulary")
    require(all(f["trigger"] in {"explicit", "auto", "state", "none"} for f in fixtures), "fixture trigger outside the trigger vocabulary")
    require(all(isinstance(f["clause"], str) and f["clause"].strip() for f in fixtures), "every fixture carries a clause")
    require([f["id"] for f in fixtures if f["holdout"]] == [
        "cert-expiry-no-substrate-found", "disk-watch-delivery-failure-suspect",
        "orphan-log-retention-no-action",
    ], "watch holdout set drifted — exactly 3 holdouts, spread across fire and no-fire")
    require(all(f.get("expected_state") in scorer.STATES for f in fixtures if f["expected_action"] == "commission"),
            "every commission fixture carries an expected_state in the state vocabulary")
    require(all(f.get("expected_block_reason") in scorer.BLOCK_REASONS
                for f in fixtures if f.get("expected_state") == "BLOCKED"),
            "every BLOCKED fixture carries an expected_block_reason in the closed vocabulary")

    balanced = scorer.score(fixtures, load("balanced"))
    require(balanced["pass"], balanced["failures"])
    require(balanced["actions"] == {"commission": 7, "no-fire": 6}, balanced["actions"])

    for name in ("overfiring", "underfiring", "parody"):
        report = scorer.score(fixtures, load(name))
        require(not report["pass"], f"{name} responder unexpectedly passed")
    over = scorer.score(fixtures, load("overfiring"))
    require(sum("expected no-fire" in failure for failure in over["failures"]) == 6, over["failures"])
    under = scorer.score(fixtures, load("underfiring"))
    require(sum("expected commission, got no-fire" in failure for failure in under["failures"]) == 7, under["failures"])
    parody = scorer.score(fixtures, load("parody"))
    require(any("the observer must be external" in failure for failure in parody["failures"]), parody["failures"])
    require(any("PROVEN requires a proof object" in failure for failure in parody["failures"]), parody["failures"])
    require(any("expected no-fire, got commission" in failure for failure in parody["failures"]), parody["failures"])
    require(any("expected state" in failure for failure in parody["failures"]), parody["failures"])

    # State-shape regressions: each mutation must be named, never passed.
    balanced_rows = load("balanced")
    wrong_reason = scorer.score(fixtures, mutate(balanced_rows, "cert-expiry-no-substrate-found", block_reason="NO_KILL_SWITCH"))
    require(any("expected block_reason NO_EXECUTION_SUBSTRATE" in failure for failure in wrong_reason["failures"]), wrong_reason["failures"])
    no_evidence = scorer.score(fixtures, [
        {key: value for key, value in row.items() if key != "block_evidence"}
        if row["id"] == "backup-watch-kill-switch-unproven" else row
        for row in balanced_rows
    ])
    require(any("BLOCKED requires a block_evidence object" in failure for failure in no_evidence["failures"]), no_evidence["failures"])
    no_failure = scorer.score(fixtures, [
        {key: value for key, value in row.items() if key != "failure"}
        if row["id"] == "disk-watch-delivery-failure-suspect" else row
        for row in balanced_rows
    ])
    require(any("SUSPECT requires a failure object" in failure for failure in no_failure["failures"]), no_failure["failures"])
    session_substrate = scorer.score(fixtures, mutate(balanced_rows, "nas-free-space-bound-declared", substrate_kind="session"))
    require(any("the observer must be external" in failure for failure in session_substrate["failures"]), session_substrate["failures"])
    timeless_proof = scorer.score(fixtures, [
        dict(row, proof={"production_path": True, "alert_receipt_ref": "alert-receipt-2026-10-22-replication-01"})
        if row["id"] == "replication-watch-reproved-proven" else row
        for row in balanced_rows
    ])
    require(any("proof.reproof_boundary" in failure for failure in timeless_proof["failures"]), timeless_proof["failures"])
    bad_direction = scorer.score(fixtures, [
        dict(row, bound={"direction": "sideways", "threshold": 85})
        if row["id"] == "nas-free-space-bound-declared" else row
        for row in balanced_rows
    ])
    require(any("bound.direction must be one of" in failure for failure in bad_direction["failures"]), bad_direction["failures"])
    noisy_silence = scorer.score(fixtures, mutate(balanced_rows, "current-disk-state-now-health", state="DECLARED"))
    require(any("no-fire must be silent" in failure for failure in noisy_silence["failures"]), noisy_silence["failures"])

    # Malformed input fails closed with named failures, never a traceback.
    unknown = scorer.score(fixtures, [{"id": "nas-free-space-bound-declared", "action": "start-watching"}])
    require(any("unknown action 'start-watching'" in failure for failure in unknown["failures"]), unknown["failures"])
    duplicated = scorer.score(fixtures, [
        {"id": "auto-remediate-restart-request", "action": "no-fire"},
        {"id": "auto-remediate-restart-request", "action": "no-fire"},
    ])
    require(any("response ids missing or duplicated" in failure for failure in duplicated["failures"]), duplicated["failures"])
    top_level = scorer.score(fixtures, True)
    require(not top_level["pass"], "non-list responses unexpectedly passed")
    require(any("responses must be an array" in failure for failure in top_level["failures"]), top_level["failures"])
    nonstring_action = scorer.score(fixtures, [{"id": "auto-remediate-restart-request", "action": ["no-fire"]}])
    require(any("action must be a string" in failure for failure in nonstring_action["failures"]), nonstring_action["failures"])
    nonstring_state = scorer.score(fixtures, [{
        "id": "nas-free-space-bound-declared", "action": "commission", "state": ["DECLARED"],
        "bound": {"direction": "above", "threshold": 85}, "substrate_kind": "scheduler",
        "destination": "operator email inbox",
    }])
    require(any("state must be a string" in failure for failure in nonstring_state["failures"]), nonstring_state["failures"])
    nonstring_id = scorer.score(fixtures, [{"id": ["auto-remediate-restart-request"], "action": "no-fire"}])
    require(any("response ids missing or duplicated" in failure for failure in nonstring_id["failures"]), nonstring_id["failures"])

    print("watch trigger-and-scope: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
