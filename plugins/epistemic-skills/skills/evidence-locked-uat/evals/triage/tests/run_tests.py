#!/usr/bin/env python3
"""Polarity tests for UAT proportionality triage."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    score_path = ROOT / "score.py"
    require(score_path.is_file(), f"missing UAT triage scorer: {score_path}")
    spec = importlib.util.spec_from_file_location("uat_triage_score", score_path)
    scorer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scorer)

    fixtures = json.loads((ROOT / "fixtures.json").read_text(encoding="utf-8"))
    require([f["id"] for f in fixtures] == [
        "routine-presentation", "stateful-keyboard", "explicit-uat-request", "unreachable-material-target"
    ], "UAT triage fixture inventory drifted")

    balanced = scorer.score(fixtures, json.loads((ROOT / "examples" / "balanced.json").read_text(encoding="utf-8")))
    require(balanced["pass"], balanced["failures"])
    require(balanced["routes"] == {"routine-check": 1, "uat": 2, "blocked-environment": 1}, balanced["routes"])

    ceremony = scorer.score(fixtures, json.loads((ROOT / "examples" / "always-uat.json").read_text(encoding="utf-8")))
    require(not ceremony["pass"], "always-UAT parody unexpectedly passed")
    require(any("routine" in failure.lower() for failure in ceremony["failures"]), ceremony["failures"])

    shortcut = scorer.score(fixtures, json.loads((ROOT / "examples" / "always-routine.json").read_text(encoding="utf-8")))
    require(not shortcut["pass"], "always-routine parody unexpectedly passed")
    require(any("material" in failure.lower() or "explicit" in failure.lower() for failure in shortcut["failures"]), shortcut["failures"])

    print("UAT proportionality triage: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
