#!/usr/bin/env python3
"""Deterministic scorer for metacognate trigger discipline and examination scope."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

ACTIONS = {"examine", "no-fire"}
# This verdict vocabulary is defined by THIS battery as its minimal observable
# output contract. It does not appear in metacognate's SKILL.md, which carries
# no verdict vocabulary; see README.md.
VERDICTS = {"approach-retained", "approach-corrected", "question-reframed", "confidence-recalibrated"}
EXAMINE_FIELDS = ("outcome_named", "decisive_assumption", "discriminating_observation", "verdict")


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
                failures.append(f"{fid}: no-fire must be silent — no examination fields, no explanation, nothing beyond id and action; present: {present}")
            continue
        # expected == "examine"
        if not _nonempty(row.get("outcome_named")):
            failures.append(f"{fid}: outcome_named must be nonempty — name the actual outcome, distinguished from its proxy")
        if not _nonempty(row.get("decisive_assumption")):
            failures.append(f"{fid}: decisive_assumption must be nonempty — name the assumption doing real work in the current approach")
        if not _nonempty(row.get("discriminating_observation")):
            failures.append(f"{fid}: discriminating_observation must be nonempty — name what observation would show this approach wrong")
        verdict = row.get("verdict")
        if not isinstance(verdict, str):
            failures.append(f"{fid}: verdict must be a string naming the examination outcome, got {type(verdict).__name__}")
            continue
        if verdict not in VERDICTS:
            failures.append(f"{fid}: unknown verdict {verdict!r}")
            continue
        expected_verdict = fixture.get("expected_verdict")
        if expected_verdict and verdict != expected_verdict:
            failures.append(f"{fid}: expected verdict {expected_verdict}, got {verdict}")
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
