#!/usr/bin/env python3
"""Deterministic scorer for health trigger discipline and readout scope."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

ACTIONS = {"readout", "no-fire"}
STATES = {"OK", "WARN", "CRITICAL", "UNKNOWN"}
RANK = {"CRITICAL": 0, "UNKNOWN": 1, "WARN": 2, "OK": 3}


def _expected_rollup(states: set) -> str:
    if "CRITICAL" in states:
        return "CRITICAL"
    if "UNKNOWN" in states:
        return "UNKNOWN"
    if "WARN" in states:
        return "WARN"
    return "OK"


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
                failures.append(f"{fid}: no-fire must be silent — no subjects, no rollup, no readout artifact, nothing beyond id and action; present: {present}")
            continue
        # expected == "readout"
        subjects = row.get("subjects")
        subjects_valid = isinstance(subjects, list) and len(subjects) > 0
        if not subjects_valid:
            failures.append(f"{fid}: subjects must be a nonempty array of name/state objects")
        row_map: dict[str, str] = {}
        if isinstance(subjects, list):
            for entry in subjects:
                if not isinstance(entry, dict) or not isinstance(entry.get("name"), str) or not entry.get("name"):
                    failures.append(f"{fid}: every subject must be an object with a nonempty string name")
                    subjects_valid = False
                    continue
                state = entry.get("state")
                if not isinstance(state, str) or state not in STATES:
                    failures.append(f"{fid}: subject {entry['name']!r} has unknown state {state!r} — state must be one of {sorted(STATES)}")
                    subjects_valid = False
                    continue
                if entry["name"] in row_map:
                    failures.append(f"{fid}: subject {entry['name']!r} reported more than once")
                    subjects_valid = False
                    continue
                row_map[entry["name"]] = state
        expected_subjects = fixture.get("expected_subjects")
        if subjects_valid and expected_subjects is not None and row_map != dict(expected_subjects):
            failures.append(f"{fid}: subjects must match the probe-determined states exactly — expected {dict(expected_subjects)}, got {row_map}")
        rollup = row.get("rollup")
        if not isinstance(rollup, str) or rollup not in STATES:
            failures.append(f"{fid}: unknown rollup {rollup!r} — rollup must be one of {sorted(STATES)}")
        elif subjects_valid and row_map:
            computed = _expected_rollup(set(row_map.values()))
            if rollup != computed:
                if computed == "CRITICAL":
                    failures.append(f"{fid}: any CRITICAL subject makes the rollup CRITICAL, got {rollup}")
                elif computed == "UNKNOWN":
                    failures.append(f"{fid}: a roll-up containing UNKNOWN is at best UNKNOWN — absence of evidence is not health, got rollup {rollup}")
                elif computed == "WARN":
                    failures.append(f"{fid}: rollup must be WARN when a subject is WARN and none is CRITICAL or UNKNOWN, got {rollup}")
                else:
                    failures.append(f"{fid}: rollup OK requires every subject OK — and is OK only then, got {rollup}")
        ordered = row.get("ordered_subjects")
        if not isinstance(ordered, list) or not ordered or any(not isinstance(name, str) for name in ordered):
            failures.append(f"{fid}: ordered_subjects must be a nonempty array of subject names")
        elif subjects_valid and row_map:
            if sorted(ordered) != sorted(row_map):
                failures.append(f"{fid}: ordered_subjects must be a permutation of the subject names — expected exactly {sorted(row_map)}, got {ordered}")
            else:
                ranks = [RANK[row_map[name]] for name in ordered]
                if ranks != sorted(ranks):
                    failures.append(f"{fid}: ordered_subjects must order CRITICAL first, then UNKNOWN, then WARN, then OK — got {ordered}")
                elif expected_subjects:
                    fixture_order = list(expected_subjects)
                    for rank in set(ranks):
                        got_group = [name for name in ordered if RANK[row_map[name]] == rank]
                        want_group = [name for name in fixture_order if name in row_map and RANK[row_map[name]] == rank]
                        if got_group != want_group:
                            failures.append(f"{fid}: ordered_subjects ties must follow fixture order — got {ordered}")
                            break
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
