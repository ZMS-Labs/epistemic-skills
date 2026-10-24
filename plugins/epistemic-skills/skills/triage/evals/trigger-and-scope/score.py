#!/usr/bin/env python3
"""Deterministic scorer for triage trigger discipline and verdict scope."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

ACTIONS = {"investigate", "no-fire"}
VERDICTS = {"CAUSE", "NARROWED", "UNKNOWN", "NOT-BROKEN"}
SILENT_FIELDS = ("verdict", "discriminating_observation", "named_cause", "provider", "eliminated")


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _nullable_string(fid: str, row: dict, field: str, failures: list[str]) -> None:
    """A nullable contract field is a string or null/absent — nothing else."""
    if field in row and row.get(field) is not None and not isinstance(row.get(field), str):
        failures.append(f"{fid}: {field} must be a string or null, got {type(row.get(field)).__name__}")


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
                failures.append(f"{fid}: no-fire must be silent — no verdict fields, no explanation, nothing beyond id and action; present: {present}")
            continue
        # expected == "investigate"
        verdict = row.get("verdict")
        if not isinstance(verdict, str):
            failures.append(f"{fid}: verdict must be a string naming a triage verdict, got {type(verdict).__name__}")
            continue
        if verdict not in VERDICTS:
            failures.append(f"{fid}: unknown verdict {verdict!r}")
            continue
        expected_verdict = fixture.get("expected_verdict")
        if expected_verdict is not None and verdict != expected_verdict:
            failures.append(f"{fid}: expected verdict {expected_verdict}, got {verdict}")
        if not _nonempty(row.get("provider")):
            failures.append(f"{fid}: provider must be a nonempty string naming the investigation method actually used")
        _nullable_string(fid, row, "discriminating_observation", failures)
        _nullable_string(fid, row, "named_cause", failures)
        if "eliminated" in row:
            eliminated = row.get("eliminated")
            if not isinstance(eliminated, list) or any(not isinstance(item, str) for item in eliminated):
                failures.append(f"{fid}: eliminated must be an array of strings naming what was eliminated")
        if verdict == "CAUSE":
            if not _nonempty(row.get("discriminating_observation")):
                failures.append(f"{fid}: CAUSE requires a nonempty discriminating_observation — a candidate that merely fits the symptom is a hypothesis, not a cause")
            if not _nonempty(row.get("named_cause")):
                failures.append(f"{fid}: CAUSE requires a nonempty named_cause")
        elif verdict == "UNKNOWN":
            if row.get("named_cause") is not None:
                failures.append(f"{fid}: UNKNOWN requires named_cause to be null — an unobserved cause is never dressed up as a most-likely cause")
        elif verdict == "NARROWED":
            if not isinstance(row.get("eliminated"), list):
                failures.append(f"{fid}: NARROWED requires an eliminated array naming what was eliminated")
            if row.get("named_cause") is not None:
                failures.append(f"{fid}: NARROWED requires named_cause to be null — a narrowed candidate is not an established cause")
        elif verdict == "NOT-BROKEN":
            if not _nonempty(row.get("discriminating_observation")):
                failures.append(f"{fid}: NOT-BROKEN requires a nonempty discriminating_observation — adequate direct observation of the reported behaviour")
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
