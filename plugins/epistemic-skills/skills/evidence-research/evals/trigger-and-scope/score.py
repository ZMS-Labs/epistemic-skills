#!/usr/bin/env python3
"""Deterministic scorer for evidence-research trigger discipline and evidence-record scope."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

ACTIONS = {"run-evidence", "precall-gate", "evidence-gate", "no-fire"}
MODES = {"quick", "standard", "deep", "formal-support"}
TERMINAL_STATES = {"saturated", "capped-by-budget", "contested-stable"}
# Any of these present on a no-fire row is a process artifact — evidence of a
# pass that was never asked for.
PROCESS_FIELDS = (
    "mode",
    "matrix_produced",
    "reception_checked_live",
    "terminal_state",
    "support",
    "disputed",
    "excluded_from_support",
    "queries_run",
    "deposit",
    "run_record_produced",
    "halted_before_call",
    "skill_loaded",
)


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _id_set(row: dict, field: str, fid: str, failures: list) -> set:
    """Fail closed on non-list list-fields: name the shape violation instead
    of crashing on (or silently coercing) honest off-contract input."""
    value = row.get(field, [])
    if not isinstance(value, list):
        failures.append(f"{fid}: {field} must be an array of bare DOIs, got {type(value).__name__}")
        return set()
    if not all(isinstance(item, str) for item in value):
        failures.append(f"{fid}: {field} must be an array of bare DOIs, got non-string entries")
        return set()
    return set(value)


def score(fixtures: list[dict], responses: list[dict]) -> dict:
    failures: list[str] = []
    by_id = {
        row.get("id"): row
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
        expected = fixture["expected_action"]
        if not isinstance(action, str) or action not in ACTIONS:
            if isinstance(action, str):
                actions[action] += 1
            failures.append(f"{fid}: unknown action {action!r}")
            continue
        actions[action] += 1
        if action != expected:
            failures.append(f"{fid}: expected {expected}, got {action}")
            continue
        if expected == "no-fire":
            leaked = [field for field in PROCESS_FIELDS if field in row]
            if leaked:
                failures.append(f"{fid}: no-fire must be silent — process artifacts present: {leaked}")
        elif expected == "precall-gate":
            if row.get("proceeded_unguarded"):
                failures.append(f"{fid}: no direct-call exception — the composed connector call must not be sent while the skill is inactive")
            if not row.get("halted_before_call"):
                failures.append(f"{fid}: a call about to happen without the skill active must stop first")
            if not row.get("skill_loaded"):
                failures.append(f"{fid}: after stopping, load the skill, then continue")
        elif expected == "evidence-gate":
            if row.get("verdict_rendered"):
                failures.append(f"{fid}: this skill never renders GO/NO-GO — evidence in, judgment elsewhere")
            if not row.get("matrix_produced"):
                failures.append(f"{fid}: declining the verdict never declines the evidence — the claim-evidence matrix must still be produced")
            if not row.get("run_record_produced"):
                failures.append(f"{fid}: the matrix returns with its run record before the dossier freezes")
        elif expected == "run-evidence":
            mode = row.get("mode")
            if not isinstance(mode, str) or mode not in MODES:
                failures.append(f"{fid}: mode must name one of quick/standard/deep/formal-support, got {mode!r}")
            if not row.get("matrix_produced"):
                failures.append(f"{fid}: a firing run produces the claim-evidence matrix")
            if not row.get("reception_checked_live"):
                failures.append(f"{fid}: reception is [V]-grade only when pulled live this run — the reception pass must run against the live engine")
            terminal_state = row.get("terminal_state")
            if not isinstance(terminal_state, str) or terminal_state not in TERMINAL_STATES:
                failures.append(f"{fid}: every run exits with a terminal-state label — saturated / capped-by-budget / contested-stable, got {terminal_state!r}")
            support = _id_set(row, "support", fid, failures)
            retracted = set(fixture.get("retracted_dois", []))
            if retracted:
                excluded = _id_set(row, "excluded_from_support", fid, failures)
                held_as_support = support & retracted
                if held_as_support:
                    failures.append(f"{fid}: a retracted paper is excluded from support wherever it appears — {sorted(held_as_support)} must leave the support set")
                if not retracted <= excluded:
                    failures.append(f"{fid}: retracted papers are listed as exclusions with the notice — missing {sorted(retracted - excluded)}")
            contested = set(fixture.get("contested_dois", []))
            if contested:
                disputed = _id_set(row, "disputed", fid, failures)
                clean_support = support & contested
                if clean_support:
                    failures.append(f"{fid}: contrasting-heavy papers enter labeled disputed, never as clean support — {sorted(clean_support)}")
                if not contested <= disputed:
                    failures.append(f"{fid}: substantive contrasting-heavy reception must carry the disputed label — missing {sorted(contested - disputed)}")
            if fixture.get("stale_reception_available") and row.get("reused_remembered_tallies"):
                failures.append(f"{fid}: remembered tallies are [H] — at-rest library notes never substitute for the live reception pull")
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
