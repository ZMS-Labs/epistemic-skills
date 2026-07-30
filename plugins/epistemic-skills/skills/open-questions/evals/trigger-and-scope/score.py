#!/usr/bin/env python3
"""Deterministic scorer for Open Questions trigger discipline and auto-fire scope."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

ACTIONS = {"full-interview", "fork-interview", "park-and-proceed", "hold-escalate", "no-fire"}
DEFER_FIELDS = {"question", "tracker_ref", "default"}


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
            if row.get("questions_asked") or row.get("visible_process"):
                failures.append(f"{fid}: no-fire must be silent — no interview, no process artifact")
        elif expected == "park-and-proceed":
            parked = row.get("parked", [])
            if not parked:
                failures.append(f"{fid}: park-and-proceed must announce parked items with defaults")
            for item in parked:
                if not isinstance(item, dict) or not item.get("default"):
                    failures.append(f"{fid}: every parked item carries a best-guess default")
                    break
        elif expected == "hold-escalate":
            if not row.get("escalated") or row.get("applied_default"):
                failures.append(f"{fid}: irreversible un-best-guessable fork must escalate, never apply a default")
        elif expected == "full-interview":
            if not row.get("closing_probe") or not row.get("ledger_empty"):
                failures.append(f"{fid}: full interview terminates on empty ledger plus closing probe")
        elif expected == "fork-interview":
            lineage = set(fixture.get("fork_lineage", []))
            unrelated = set(fixture.get("unrelated_questions", []))
            walked = set(row.get("walked", []))
            if not lineage <= walked:
                failures.append(f"{fid}: fork lineage not fully walked")
            if walked & unrelated:
                failures.append(f"{fid}: auto-fire walked unrelated questions — scope creep")
            offers = row.get("offer_count", 0)
            if unrelated and offers != 1:
                failures.append(f"{fid}: exactly one offer is required when unrelated material questions surfaced")
            if fixture.get("offer_declined"):
                deferred = {d.get("question"): d for d in row.get("deferred", []) if isinstance(d, dict)}
                for q in unrelated:
                    entry = deferred.get(q)
                    if entry is None or not DEFER_FIELDS <= set(entry) or not all(entry.get(k) for k in DEFER_FIELDS):
                        failures.append(f"{fid}: declined question {q!r} must be deferred with tracker_ref and default")
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
