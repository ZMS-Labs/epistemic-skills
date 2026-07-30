#!/usr/bin/env python3
"""Deterministic scorer for Open Questions trigger discipline and auto-fire scope."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

ACTIONS = {"full-interview", "fork-interview", "park-and-proceed", "hold-escalate", "no-fire"}
OFFER_OUTCOMES = {"accepted", "declined", "unanswered", None}


def _identified(entry: object, *, needs_tracker: bool) -> bool:
    """An item is identified when its question is a non-empty string and its
    best-guess default is present and non-None (false-valued defaults such as
    ``false`` or ``0`` are legitimate). Deferred items also need a non-empty
    tracker_ref."""
    if not isinstance(entry, dict):
        return False
    if not (isinstance(entry.get("question"), str) and entry["question"].strip()):
        return False
    if "default" not in entry or entry["default"] is None:
        return False
    if needs_tracker and not (isinstance(entry.get("tracker_ref"), str) and entry["tracker_ref"].strip()):
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
            if row.get("questions_asked") or row.get("visible_process"):
                failures.append(f"{fid}: no-fire must be silent — no interview, no process artifact")
        elif expected == "park-and-proceed":
            parked = row.get("parked", [])
            if not parked:
                failures.append(f"{fid}: park-and-proceed must announce parked items with defaults")
            elif not all(_identified(item, needs_tracker=False) for item in parked):
                failures.append(f"{fid}: every parked item names its question and carries a best-guess default")
        elif expected == "hold-escalate":
            if not row.get("escalated") or row.get("applied_default"):
                failures.append(f"{fid}: irreversible un-best-guessable fork must escalate, never apply a default")
            if row.get("questions_asked") or row.get("visible_process"):
                failures.append(f"{fid}: hold-escalate is a halt, not an interview — no questions, no process artifact")
        elif expected == "full-interview":
            exhausted = row.get("closing_probe") and row.get("ledger_empty")
            released = row.get("operator_release")
            if released:
                parked = row.get("parked", [])
                remaining = set(fixture.get("remaining_items", []))
                parked_ids = {item.get("question") for item in parked if isinstance(item, dict)}
                if remaining and not remaining <= parked_ids:
                    failures.append(f"{fid}: operator release parks EVERY remaining ledger item — missing {sorted(remaining - parked_ids)}")
                if not all(_identified(item, needs_tracker=False) for item in parked):
                    failures.append(f"{fid}: operator release parks each remaining item, named, with its default")
            elif not exhausted:
                failures.append(f"{fid}: full interview terminates on empty ledger plus closing probe, or operator release")
        elif expected == "fork-interview":
            lineage = set(fixture.get("fork_lineage", []))
            unrelated = set(fixture.get("unrelated_questions", []))
            outcome = fixture.get("offer_outcome")
            if outcome not in OFFER_OUTCOMES:
                failures.append(f"{fid}: fixture has unknown offer_outcome {outcome!r}")
                continue
            walked = set(row.get("walked", []))
            if not lineage <= walked:
                failures.append(f"{fid}: fork lineage not fully walked")
            allowed = lineage | (unrelated if outcome == "accepted" else set())
            if walked - allowed:
                failures.append(f"{fid}: auto-fire walked out-of-scope questions {sorted(walked - allowed)} — scope creep")
            offers = row.get("offer_count", 0)
            if unrelated and offers != 1:
                failures.append(f"{fid}: exactly one offer is required when unrelated material questions surfaced")
            if outcome == "accepted":
                if not unrelated <= walked:
                    failures.append(f"{fid}: accepted offer means the surfaced questions are walked now")
            else:
                if unrelated:
                    # declined and unanswered offers defer identically
                    deferred = {d.get("question"): d for d in row.get("deferred", []) if isinstance(d, dict)}
                    coverage = set(row.get("coverage_limits", []))
                    for q in unrelated:
                        if not _identified(deferred.get(q), needs_tracker=True):
                            failures.append(f"{fid}: question {q!r} must be deferred with tracker_ref and default")
                        if q not in coverage:
                            failures.append(f"{fid}: deferred question {q!r} missing from exit-stamp coverage_limits")
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
