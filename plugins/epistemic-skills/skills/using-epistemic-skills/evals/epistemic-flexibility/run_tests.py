#!/usr/bin/env python3
"""Run the deterministic epistemic-flexibility conformance fixtures."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from validate_trace import validate_trace

ROOT = Path(__file__).resolve().parent
FIXTURES = ROOT / "fixtures"


def main() -> int:
    cases = []
    failed = 0
    for path in sorted(FIXTURES.glob("*.json")):
        expected_valid = path.name.startswith("valid-")
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            errors = validate_trace(payload)
        except Exception as exc:  # fixture corruption should be visible, not hidden
            errors = [f"fixture load error: {exc}"]
        actual_valid = not errors
        passed = actual_valid == expected_valid
        failed += 0 if passed else 1
        cases.append((path.name, expected_valid, actual_valid, errors, passed))

    print("# epistemic-flexibility conformance battery")
    print("| fixture | expected | actual | result | details |")
    print("|---|:--:|:--:|:--:|---|")
    for name, expected, actual, errors, passed in cases:
        details = "; ".join(errors) if errors else "—"
        print(
            f"| {name} | {'valid' if expected else 'invalid'} | "
            f"{'valid' if actual else 'invalid'} | {'PASS' if passed else 'FAIL'} | {details} |"
        )
    print(f"\nRESULT: {'PASS' if failed == 0 else 'FAIL'} ({len(cases) - failed}/{len(cases)} fixtures)")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
