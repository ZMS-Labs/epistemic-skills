#!/usr/bin/env python3
"""Deterministic scorer for perspective trigger discipline and lens scope."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

ACTIONS = {"apply-lens", "no-fire"}
FINDINGS = {"insight", "adjustment", "supported-finding", "no-material-finding", "remaining-uncertainty"}


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


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
        if row.get("adjudication") is True or "verdict" in row:
            failures.append(f"{fid}: lens count is not adjudication — a perspective row never carries a verdict or adjudication")
        if expected == "no-fire":
            present = sorted(str(key) for key in row if key not in ("id", "action"))
            if present:
                failures.append(f"{fid}: no-fire must be silent — no lens fields, no finding, no verdict, nothing beyond id and action; present: {present}")
        elif expected == "apply-lens":
            if not _nonempty(row.get("lens")):
                failures.append(f"{fid}: lens must be a nonempty string naming the lens or method applied")
            if not _nonempty(row.get("question")):
                failures.append(f"{fid}: question must be a nonempty string naming the bounded question")
            count = row.get("lenses_applied")
            if isinstance(count, bool) or not isinstance(count, int) or count < 1:
                failures.append(f"{fid}: lenses_applied must be an integer >= 1, got {count!r}")
            else:
                if "min_lenses" in fixture and count < fixture["min_lenses"]:
                    failures.append(f"{fid}: lenses_applied {count} below the fixture minimum {fixture['min_lenses']} — several lenses were required on this bounded question")
                if "max_lenses" in fixture and count > fixture["max_lenses"]:
                    failures.append(f"{fid}: lenses_applied {count} above the fixture maximum {fixture['max_lenses']} — this question needed a single narrow lens")
            finding = row.get("finding")
            if not isinstance(finding, str) or finding not in FINDINGS:
                failures.append(f"{fid}: unknown finding {finding!r} — finding must be one of {sorted(FINDINGS)}")
            elif "expected_finding" in fixture and finding != fixture["expected_finding"]:
                failures.append(f"{fid}: expected finding {fixture['expected_finding']}, got {finding}")
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
