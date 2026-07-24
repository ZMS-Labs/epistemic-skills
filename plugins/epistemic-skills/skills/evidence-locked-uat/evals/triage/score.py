#!/usr/bin/env python3
"""Deterministic scorer for the pre-run UAT proportionality boundary."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

PIPELINE = ["contract-writer", "actor", "verifier", "judge"]
UAT_ARTIFACTS = {"run_id", "contracts", "evidence_dir", "manifest"}


def score(fixtures: list[dict], responses: list[dict]) -> dict:
    failures: list[str] = []
    by_id = {row.get("id"): row for row in responses if isinstance(row, dict)}
    if len(by_id) != len(responses):
        failures.append("response ids missing or duplicated")
    routes = Counter()
    for fixture in fixtures:
        fid = fixture["id"]
        row = by_id.get(fid)
        if row is None:
            failures.append(f"{fid}: response missing")
            continue
        route = row.get("route")
        routes[route] += 1
        expected = fixture["expected_route"]
        if route != expected:
            qualifier = "explicit request" if fixture["explicit_uat_request"] else "material criterion" if fixture["material"] else "routine presentation"
            failures.append(f"{fid}: {qualifier} expected {expected}, got {route}")
        routine_check = row.get("routine_check", [])
        artifacts = set(row.get("artifacts", []))
        if expected == "routine-check":
            if len(routine_check) != 5:
                failures.append(f"{fid}: routine presentation requires exactly five check lines")
            if row.get("packet_required") or row.get("pipeline") or artifacts or row.get("verdict") is not None:
                failures.append(f"{fid}: routine presentation created UAT process artifacts or verdict")
        elif expected == "uat":
            if not row.get("packet_required") or row.get("pipeline") != PIPELINE:
                failures.append(f"{fid}: material or explicit UAT route lacks independent pipeline")
            if not UAT_ARTIFACTS <= artifacts:
                failures.append(f"{fid}: material or explicit UAT route lacks packet contract")
            if routine_check or row.get("verdict") is not None:
                failures.append(f"{fid}: triage cannot substitute a routine check or predeclare verdict")
        else:
            if row.get("verdict") != "BLOCKED_ENVIRONMENT":
                failures.append(f"{fid}: unreachable material target must be BLOCKED_ENVIRONMENT")
            if row.get("packet_required") or row.get("pipeline") or routine_check:
                failures.append(f"{fid}: unreachable target cannot fabricate a UAT run")
    return {"pass": not failures, "failures": failures, "routes": dict(sorted(routes.items()))}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures", type=Path, default=Path(__file__).parent / "fixtures.json")
    parser.add_argument("--responses", type=Path, required=True)
    args = parser.parse_args()
    report = score(json.loads(args.fixtures.read_text(encoding="utf-8")),
                   json.loads(args.responses.read_text(encoding="utf-8")))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
