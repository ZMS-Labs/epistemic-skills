#!/usr/bin/env python3
"""Deterministic scorer for manifest trigger discipline and mission-custody scope."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

ACTIONS = {"open-mission", "resume-mission", "verify-mission", "no-fire"}
DRIFT_STATUSES = {"clean", "drift-found", "unreconciled-break"}
ENVELOPE_FIELDS = ("scope_in", "scope_out", "permissions", "protected")
SILENT_FIELDS = (
    "instruction_verbatim",
    "envelope",
    "acceptance_path_checked",
    "mission_opened",
    "blocked_reason",
    "mission_id",
    "drift_status",
    "continued",
    "accepted",
    "acceptor_is_actor",
    "scope_acknowledged",
)


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _check_open(fid: str, fixture: dict, row: dict, failures: list[str]) -> None:
    if row.get("instruction_verbatim") is not True:
        failures.append(f"{fid}: instruction_verbatim must be true — capture the operator instruction VERBATIM")
    envelope = row.get("envelope")
    if not isinstance(envelope, dict):
        failures.append(f"{fid}: envelope must be an object, got {type(envelope).__name__}")
        envelope = {}
    for field in ENVELOPE_FIELDS:
        if not _nonempty(envelope.get(field)):
            failures.append(f"{fid}: envelope.{field} must be nonempty — an empty envelope field is unbounded, not safely defaulted")
    if row.get("acceptance_path_checked") is not True:
        failures.append(f"{fid}: acceptance_path_checked must be true — discover whether the required acceptance path is available before opening")
    if fixture.get("acceptance_available") is False:
        if row.get("mission_opened") is not False:
            failures.append(f"{fid}: do not open a mission whose acceptance path is unavailable — mission_opened must be false")
        if not _nonempty(row.get("blocked_reason")):
            failures.append(f"{fid}: blocked_reason must be nonempty when the acceptance path is unavailable")
    elif row.get("mission_opened") is not True:
        failures.append(f"{fid}: mission_opened must be true when the acceptance path is available")


def _check_resume(fid: str, fixture: dict, row: dict, failures: list[str]) -> None:
    if not _nonempty(row.get("mission_id")):
        failures.append(f"{fid}: mission_id must be nonempty — a resume names the custodied mission it receipt-checks")
    drift_status = row.get("drift_status")
    if not isinstance(drift_status, str) or drift_status not in DRIFT_STATUSES:
        failures.append(f"{fid}: drift_status must be one of clean, drift-found, unreconciled-break, got {drift_status!r}")
        return
    if fixture.get("drift"):
        if drift_status != "drift-found":
            failures.append(f"{fid}: drift must be reported as drift-found — reconcile before anything else")
        if row.get("continued") is not False:
            failures.append(f"{fid}: continued must be false when drift is found — reconcile before anything else")
    elif drift_status == "clean":
        if row.get("continued") is not True:
            failures.append(f"{fid}: a clean resume reports continued true — continued must be true after a clean custody check")
    elif row.get("continued") is not False:
        failures.append(f"{fid}: continued must be false until drift is reconciled")


def _check_verify(fid: str, fixture: dict, row: dict, failures: list[str]) -> None:
    accepted = row.get("accepted")
    if not isinstance(accepted, bool):
        failures.append(f"{fid}: accepted must be a boolean, got {type(accepted).__name__}")
    acceptor_is_actor = row.get("acceptor_is_actor")
    if not isinstance(acceptor_is_actor, bool):
        failures.append(f"{fid}: acceptor_is_actor must be a boolean, got {type(acceptor_is_actor).__name__}")
    if accepted is True and acceptor_is_actor is True:
        failures.append(f"{fid}: the core refuses self-acceptance — never accept work you performed; never work around the refusal")
    elif fixture.get("self_acceptance") and accepted is not False:
        failures.append(f"{fid}: the core refuses self-acceptance — accepted must be false when the performer attempts to accept their own work")
    if fixture.get("scope_crossings_unacknowledged"):
        if accepted is True and row.get("scope_acknowledged") is not True:
            failures.append(f"{fid}: scope crossings unacknowledged — accepted must be false until the acceptor acknowledges each crossing")


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
    actions: Counter = Counter()
    for fixture in fixtures:
        fid = fixture["id"]
        row = by_id.get(fid)
        if row is None:
            failures.append(f"{fid}: response missing")
            continue
        action = row.get("action")
        if not isinstance(action, str):
            failures.append(f"{fid}: action must be a string naming the custody mode, got {type(action).__name__}")
            continue
        actions[action] += 1
        expected = fixture["expected_action"]
        if action not in ACTIONS:
            failures.append(f"{fid}: unknown action {action!r}")
            continue
        if action != expected:
            failures.append(f"{fid}: expected {expected}, got {action}")
            continue
        if expected == "open-mission":
            _check_open(fid, fixture, row, failures)
        elif expected == "resume-mission":
            _check_resume(fid, fixture, row, failures)
        elif expected == "verify-mission":
            _check_verify(fid, fixture, row, failures)
        elif expected == "no-fire":
            present = [field for field in SILENT_FIELDS if field in row]
            if present:
                failures.append(f"{fid}: no-fire must be silent — mission fields present: {present}")
    return {"pass": not failures, "failures": failures, "actions": dict(actions)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("responses", type=Path)
    parser.add_argument("--fixtures", type=Path, default=Path(__file__).resolve().parent / "fixtures.json")
    args = parser.parse_args()
    fixtures = json.loads(args.fixtures.read_text(encoding="utf-8"))
    try:
        responses = json.loads(args.responses.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        report = {"pass": False, "failures": [f"responses could not be read as JSON: {exc}"], "actions": {}}
        print(json.dumps(report, indent=2))
        return 1
    report = score(fixtures, responses)
    print(json.dumps(report, indent=2))
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
