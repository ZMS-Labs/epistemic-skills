#!/usr/bin/env python3
"""Deterministic scorer for watch trigger discipline and commission scope."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

ACTIONS = {"commission", "no-fire"}
STATES = {"DECLARED", "BLOCKED", "INERT", "PROVEN", "SUSPECT"}
DIRECTIONS = {"above", "below", "equals", "changes", "absent"}
BLOCK_REASONS = {
    "NO_EXECUTION_SUBSTRATE",
    "NO_REACHABLE_DESTINATION",
    "NO_AUTHORITY_TO_ENABLE",
    "NO_KILL_SWITCH",
    "KILL_SWITCH_UNPROVEN",
    "NO_SAFE_PROOF_CROSSING",
    "PROBE_UNAVAILABLE",
}
# The observer must be external: a value naming the skill, the session, the
# chat, the prompt, Markdown, or memory is refused even if it is mislabeled
# as an allowed substrate kind.
NON_EXTERNAL_TOKENS = ("skill", "session", "chat", "prompt", "markdown", "memory")
SILENT_FIELDS = ("state", "bound", "substrate_kind", "destination", "block_reason", "block_evidence", "proof", "failure")
BLOCK_EVIDENCE_FIELDS = ("detail", "observed_at", "receipt_ref")
FAILURE_FIELDS = ("kind", "detail", "observed_at", "receipt_ref")


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _check_proof(fid: str, row: dict, state: str, failures: list[str]) -> None:
    """A trusted proof is complete: production path, alert receipt, and a
    re-proof (freshness) boundary. A proof with no boundary silently becomes
    permanent."""
    proof = row.get("proof")
    if not isinstance(proof, dict):
        failures.append(f"{fid}: {state} requires a proof object — production_path, alert_receipt_ref and reproof_boundary")
        return
    if proof.get("production_path") is not True:
        failures.append(f"{fid}: {state} requires proof.production_path to be true — the production path is the proof path")
    if not _nonempty(proof.get("alert_receipt_ref")):
        failures.append(f"{fid}: {state} requires proof.alert_receipt_ref to be nonempty")
    if not _nonempty(proof.get("reproof_boundary")):
        failures.append(f"{fid}: {state} requires proof.reproof_boundary to be nonempty — a proof with no freshness boundary silently becomes permanent")


def score(fixtures: list[dict], responses: object) -> dict:
    failures: list[str] = []
    if not isinstance(responses, list):
        return {
            "pass": False,
            "failures": [f"responses must be an array of response objects, got {type(responses).__name__}"],
            "actions": {},
        }
    by_id = {
        row["id"]: row
        for row in responses
        if isinstance(row, dict) and isinstance(row.get("id"), str)
    }
    if len(by_id) != len(responses):
        failures.append("response ids missing or duplicated")
    fixture_ids = {fixture["id"] for fixture in fixtures}
    for rid in sorted(by_id):
        if rid not in fixture_ids:
            failures.append(f"{rid}: response id not in fixtures")
    actions: Counter = Counter()
    for fixture in fixtures:
        fid = fixture["id"]
        row = by_id.get(fid)
        if row is None:
            failures.append(f"{fid}: response missing")
            continue
        action = row.get("action")
        if not isinstance(action, str):
            failures.append(f"{fid}: action must be a string naming the discipline mode, got {type(action).__name__}")
            continue
        actions[action] += 1
        expected = fixture["expected_action"]
        if action not in ACTIONS:
            failures.append(f"{fid}: unknown action {action!r}")
            continue
        if action != expected:
            failures.append(f"{fid}: expected {expected}, got {action}")
            continue
        if expected == "no-fire":
            present = sorted(str(key) for key in row if key not in ("id", "action"))
            if present:
                failures.append(f"{fid}: no-fire must be silent — no commission fields, no explanation, nothing beyond id and action; present: {present}")
            continue
        # expected == "commission"
        state = row.get("state")
        if not isinstance(state, str):
            failures.append(f"{fid}: state must be a string naming a commission state, got {type(state).__name__}")
            continue
        if state not in STATES:
            failures.append(f"{fid}: unknown state {state!r}")
            continue
        expected_state = fixture.get("expected_state")
        if expected_state is not None and state != expected_state:
            failures.append(f"{fid}: expected state {expected_state}, got {state}")
        bound = row.get("bound")
        if not isinstance(bound, dict):
            failures.append(f"{fid}: bound must be an object with direction and threshold, got {type(bound).__name__}")
        else:
            direction = bound.get("direction")
            if not isinstance(direction, str) or direction not in DIRECTIONS:
                failures.append(f"{fid}: bound.direction must be one of 'above', 'below', 'equals', 'changes', 'absent', got {direction!r}")
            threshold = bound.get("threshold")
            if "threshold" not in bound or threshold is None or (isinstance(threshold, str) and not threshold.strip()):
                failures.append(f"{fid}: bound.threshold must be present")
            elif isinstance(threshold, (list, dict)):
                failures.append(f"{fid}: bound.threshold must be a scalar or string, got {type(threshold).__name__}")
        substrate = row.get("substrate_kind")
        if not _nonempty(substrate):
            failures.append(f"{fid}: substrate_kind must be a nonempty string naming the external observer kind")
        elif any(token in substrate.lower() for token in NON_EXTERNAL_TOKENS):
            failures.append(f"{fid}: substrate_kind {substrate!r} names the skill, session, chat, prompt, markdown or memory — the observer must be external")
        if not _nonempty(row.get("destination")):
            failures.append(f"{fid}: destination must be a nonempty string naming a reachable recipient or endpoint")
        if state == "BLOCKED":
            reason = row.get("block_reason")
            if not isinstance(reason, str) or reason not in BLOCK_REASONS:
                failures.append(f"{fid}: BLOCKED requires block_reason in the closed vocabulary, got {reason!r}")
            elif fixture.get("expected_block_reason") is not None and reason != fixture["expected_block_reason"]:
                failures.append(f"{fid}: expected block_reason {fixture['expected_block_reason']}, got {reason}")
            evidence = row.get("block_evidence")
            if not isinstance(evidence, dict):
                failures.append(f"{fid}: BLOCKED requires a block_evidence object — detail, observed_at, receipt_ref")
            else:
                for field in BLOCK_EVIDENCE_FIELDS:
                    if not _nonempty(evidence.get(field)):
                        failures.append(f"{fid}: BLOCKED requires block_evidence.{field} to be nonempty")
        elif state == "PROVEN":
            _check_proof(fid, row, state, failures)
        elif state == "INERT":
            _check_proof(fid, row, state, failures)
        elif state == "SUSPECT":
            failure = row.get("failure")
            if not isinstance(failure, dict):
                failures.append(f"{fid}: SUSPECT requires a failure object — kind, detail, observed_at, receipt_ref")
            else:
                for field in FAILURE_FIELDS:
                    if not _nonempty(failure.get(field)):
                        failures.append(f"{fid}: SUSPECT requires failure.{field} to be nonempty")
    return {"pass": not failures, "failures": failures, "actions": dict(actions)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("responses", type=Path)
    parser.add_argument("--fixtures", type=Path, default=Path(__file__).resolve().parent / "fixtures.json")
    args = parser.parse_args()
    fixtures = json.loads(args.fixtures.read_text(encoding="utf-8"))
    responses = json.loads(args.responses.read_text(encoding="utf-8"))
    report = score(fixtures, responses)
    print(json.dumps(report, indent=2))
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
