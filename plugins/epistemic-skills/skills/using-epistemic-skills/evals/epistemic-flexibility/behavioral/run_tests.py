#!/usr/bin/env python3
"""Run gold/bad pairs for the behavioral fixture scorer."""
from __future__ import annotations

import json
from pathlib import Path

from score_behavior import score

ROOT = Path(__file__).resolve().parent
FIXTURES = ROOT / "fixtures"


def main() -> int:
    rows: list[tuple[str, str, bool, bool, list[str]]] = []
    failures = 0
    for directory in sorted(path for path in FIXTURES.iterdir() if path.is_dir()):
        fixture = json.loads((directory / "scenario.json").read_text(encoding="utf-8"))
        for filename, expected_pass in (("gold.json", True), ("bad.json", False)):
            trace = json.loads((directory / filename).read_text(encoding="utf-8"))
            errors = score(fixture, trace)
            actual_pass = not errors
            ok = actual_pass == expected_pass
            failures += 0 if ok else 1
            rows.append((directory.name, filename, expected_pass, actual_pass, errors))

    print("# epistemic-flexibility behavioral fixture self-test")
    print("| fixture | trace | expected | actual | result | details |")
    print("|---|---|:--:|:--:|:--:|---|")
    for fixture, filename, expected, actual, errors in rows:
        details = "; ".join(errors) if errors else "—"
        print(
            f"| {fixture} | {filename} | {'PASS' if expected else 'FAIL'} | "
            f"{'PASS' if actual else 'FAIL'} | {'PASS' if expected == actual else 'FAIL'} | {details} |"
        )
    passed = len(rows) - failures
    print(f"\nRESULT: {'PASS' if failures == 0 else 'FAIL'} ({passed}/{len(rows)} traces)")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
