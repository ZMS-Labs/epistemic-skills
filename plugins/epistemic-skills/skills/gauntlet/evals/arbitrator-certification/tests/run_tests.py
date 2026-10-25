#!/usr/bin/env python3
"""Regression tests for the certified-arbitrator battery scorer."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def run_scorer(outputs: dict) -> subprocess.CompletedProcess:
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
        json.dump(outputs, handle)
        outputs_path = handle.name
    try:
        return subprocess.run(
            [sys.executable, str(ROOT / "score.py"), "--outputs", outputs_path],
            capture_output=True, text=True, check=False,
        )
    finally:
        Path(outputs_path).unlink(missing_ok=True)


def main() -> int:
    battery = json.loads((ROOT / "battery.json").read_text(encoding="utf-8"))
    case_ids = [case["id"] for case in battery["cases"]]
    require(len(case_ids) == 10, "arbitrator battery inventory drifted")

    empty = run_scorer({})
    require("is not in the battery" not in empty.stdout, empty.stdout)

    # Regression (2026-10-24, Dot review of the held branches): an output
    # whose case id is outside the battery must be named and must block
    # certification, never be silently ignored.
    bogus = run_scorer({"AC-99-no-such-case": {"verdict": "GO", "dispositions": [], "ledger_notes": ""}})
    require("AC-99-no-such-case" in bogus.stdout, bogus.stdout)
    require("is not in the battery" in bogus.stdout, bogus.stdout)
    require("NOT CERTIFIED" in bogus.stdout, bogus.stdout)
    require(bogus.returncode == 1, bogus.returncode)

    print("gauntlet arbitrator-certification scorer: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
