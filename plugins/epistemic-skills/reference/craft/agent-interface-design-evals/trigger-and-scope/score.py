#!/usr/bin/env python3
"""Deterministic scorer for agent-interface-design trigger discipline and scope."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

ACTIONS = {"engage", "no-fire", "consumer-gate", "example-lint"}
GATE_REMEDIES = {"structural-fix", "compatibility-concession"}
EXAMPLE_OUTCOMES = {"justified", "deleted"}


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


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
            if row.get("schema_edits") or row.get("consumer_test") or row.get("visible_process"):
                failures.append(f"{fid}: no-fire must be silent — no schema work, no consumer test, no process artifact")
            route = fixture.get("expected_route")
            if route and row.get("routed_to") != route:
                failures.append(f"{fid}: excluded crossing must route to {route}, got {row.get('routed_to')!r}")
        elif expected == "engage":
            if not row.get("encodes_in_structure"):
                failures.append(f"{fid}: engage must encode constraints in structure (types, enums, named fields), not prose")
            if not row.get("consumer_test"):
                failures.append(f"{fid}: engage must run the cold-consumer test before shipping")
            examples_added = row.get("examples_added", 0)
            justifications = row.get("example_justifications", [])
            if examples_added and len(justifications) != examples_added:
                failures.append(f"{fid}: every added example needs a written weaker-consumer justification")
        elif expected == "consumer-gate":
            remedy = row.get("remedy")
            if remedy not in GATE_REMEDIES:
                failures.append(f"{fid}: gate failure remedy must be structural-fix or a recorded compatibility-concession, got {remedy!r}")
            elif remedy == "compatibility-concession" and not row.get("recorded"):
                failures.append(f"{fid}: prose or examples added to pass the gate must be recorded as a compatibility concession")
            if remedy == "structural-fix" and not _nonempty(row.get("fixed_parameter")):
                failures.append(f"{fid}: structural fix must name the parameter it tightens")
            elif remedy == "structural-fix" and row.get("fixed_parameter") != fixture.get("failing_parameter"):
                failures.append(f"{fid}: structural fix targets {fixture.get('failing_parameter')!r}, got {row.get('fixed_parameter')!r}")
            if not row.get("transcript_kept"):
                failures.append(f"{fid}: the consumer-test transcript is the gate evidence and must be kept")
        elif expected == "example-lint":
            dispositions = row.get("dispositions", {})
            if not isinstance(dispositions, dict):
                failures.append(f"{fid}: dispositions must map each example to an outcome")
                continue
            for example in fixture.get("examples", []):
                entry = dispositions.get(example)
                if not isinstance(entry, dict):
                    failures.append(f"{fid}: example {example!r} has no lint disposition")
                    continue
                outcome = entry.get("outcome")
                if outcome not in EXAMPLE_OUTCOMES:
                    failures.append(f"{fid}: example {example!r} outcome must be justified or deleted, got {outcome!r}")
                elif outcome == "justified" and not _nonempty(entry.get("audience")):
                    failures.append(f"{fid}: justified example {example!r} must name the weaker-consumer audience it serves")
                elif outcome == "deleted" and not _nonempty(entry.get("structural_fix")):
                    failures.append(f"{fid}: deleted example {example!r} must name the structural fix that replaces it")
            extras = set(dispositions) - set(fixture.get("examples", []))
            if extras:
                failures.append(f"{fid}: dispositions for unknown examples {sorted(extras)}")
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
