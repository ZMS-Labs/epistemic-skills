#!/usr/bin/env python3
"""Deterministic scorer for intent-traced-merge trigger discipline and resolution scope."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

ACTIONS = {
    "trace-and-resolve",
    "escalate-decision",
    "review-provenance",
    "abort-restart",
    "mechanical-resolve",
    "regenerate",
    "no-fire",
}
RULINGS = {"both-preserved", "side-a-dropped", "side-b-dropped"}
DROPPED = {"side-a-dropped", "side-b-dropped"}


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _traced_ok(entry: object) -> bool:
    """A trace is complete when it cites both origins and carries a known ruling.
    A dropped-intent ruling additionally needs a reason and a ledger reference."""
    if not isinstance(entry, dict):
        return False
    if not (_nonempty(entry.get("origin_a")) and _nonempty(entry.get("origin_b"))):
        return False
    ruling = entry.get("ruling")
    if ruling not in RULINGS:
        return False
    if ruling in DROPPED and not (_nonempty(entry.get("reason")) and _nonempty(entry.get("ledger_ref"))):
        return False
    return True


def score(fixtures: list[dict], responses: list[dict]) -> dict:
    failures: list[str] = []
    by_id = {row.get("id"): row for row in responses if isinstance(row, dict)}
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
        actions[action] += 1
        expected = fixture["expected_action"]
        if action not in ACTIONS:
            failures.append(f"{fid}: unknown action {action!r}")
            continue
        if action != expected:
            failures.append(f"{fid}: expected {expected}, got {action}")
            continue
        if expected == "no-fire":
            if row.get("traced") or row.get("requested_rulings") or row.get("visible_process"):
                failures.append(f"{fid}: no-fire must be silent — no traces, no provenance demand, no process artifact")
        elif expected == "mechanical-resolve":
            trivial = set(fixture.get("trivial_hunks", []))
            mechanical = set(row.get("mechanical", []))
            if row.get("traced"):
                failures.append(f"{fid}: trivial conflict must not be traced — tracing here is over-firing")
            if not trivial <= mechanical:
                failures.append(f"{fid}: every trivial hunk is resolved mechanically — missing {sorted(trivial - mechanical)}")
        elif expected == "regenerate":
            if not row.get("regenerated"):
                failures.append(f"{fid}: regenerable artifact must be regenerated, not resolved")
            if row.get("hand_resolved"):
                failures.append(f"{fid}: hand-resolving a regenerable artifact is the named anti-pattern")
            if row.get("traced"):
                failures.append(f"{fid}: regenerable conflicts get no traces — regenerate instead of resolving")
        elif expected == "trace-and-resolve":
            nontrivial = set(fixture.get("nontrivial_hunks", []))
            trivial = set(fixture.get("trivial_hunks", []))
            traced = row.get("traced", {})
            traced = traced if isinstance(traced, dict) else {}
            traced_ids = set(traced)
            if not nontrivial <= traced_ids:
                failures.append(f"{fid}: non-trivial hunks not all traced — missing {sorted(nontrivial - traced_ids)}")
            if traced_ids - nontrivial:
                failures.append(f"{fid}: traced out-of-scope hunks {sorted(traced_ids - nontrivial)} — trivial hunks resolve mechanically, no trace")
            for hunk in sorted(nontrivial & traced_ids):
                if not _traced_ok(traced[hunk]):
                    failures.append(f"{fid}: hunk {hunk!r} ruling must cite both origins (dropped intents also need reason and ledger_ref)")
            expected_rulings = fixture.get("expected_rulings", {})
            for hunk, want in expected_rulings.items():
                got = traced.get(hunk, {}).get("ruling") if isinstance(traced.get(hunk), dict) else None
                if got != want:
                    failures.append(f"{fid}: hunk {hunk!r} expected ruling {want}, got {got}")
            mechanical = set(row.get("mechanical", []))
            if not trivial <= mechanical:
                failures.append(f"{fid}: trivial hunks resolve mechanically — missing {sorted(trivial - mechanical)}")
            checks = set(row.get("checks_run", []))
            origin_checks = set(fixture.get("origin_checks", []))
            if not origin_checks <= checks:
                failures.append(f"{fid}: both origins' motivating checks must run — missing {sorted(origin_checks - checks)}")
            if not row.get("recorded"):
                failures.append(f"{fid}: undocumented non-trivial resolution is unsanctioned drift — record each ruling")
        elif expected == "escalate-decision":
            if not row.get("escalated"):
                failures.append(f"{fid}: colliding intents are a decision, not a merge — escalate")
            if row.get("resolved"):
                failures.append(f"{fid}: a merge resolution must never be where a design decision gets made silently")
            intents = set(fixture.get("intents", []))
            named = set(row.get("intents", []))
            if not intents <= named:
                failures.append(f"{fid}: escalation names both intents — missing {sorted(intents - named)}")
            if not _nonempty(row.get("routed_to")):
                failures.append(f"{fid}: escalation routes to the decision's owner or the decision process")
        elif expected == "review-provenance":
            if not row.get("requested_rulings"):
                failures.append(f"{fid}: undocumented merge review must demand per-hunk rulings with origin references")
            if row.get("approved_without_provenance"):
                failures.append(f"{fid}: approving an undocumented resolution waves through unsanctioned drift")
        elif expected == "abort-restart":
            if not row.get("aborted"):
                failures.append(f"{fid}: an uncertain working tree is aborted — the abort is the return path, not a failure")
            if not row.get("traces_kept"):
                failures.append(f"{fid}: the traces are the work and survive the abort")
            if not row.get("restarted"):
                failures.append(f"{fid}: after aborting, restart the merge with the traces already learned")
            if row.get("forced_continue"):
                failures.append(f"{fid}: pressing on through an uncertain tree trades reversibility for pride")
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
