#!/usr/bin/env python3
"""Polarity tests for Decision Ledger proportionality."""

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
    require(score_path.is_file(), f"missing Decision Ledger proportionality scorer: {score_path}")
    spec = importlib.util.spec_from_file_location("decision_ledger_prop", score_path)
    scorer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scorer)
    fixtures = json.loads((ROOT / "fixtures.json").read_text(encoding="utf-8"))
    require([f["id"] for f in fixtures] == [
        "routine-no-op", "adequate-adr-reuse", "uncovered-consequential-decision", "recurrent-correction"
    ], "Decision Ledger fixture inventory drifted")

    balanced = scorer.score(fixtures, json.loads((ROOT / "examples" / "balanced.json").read_text(encoding="utf-8")))
    require(balanced["pass"], balanced["failures"])
    require(balanced["actions"] == {"create": 2, "no-op": 1, "reuse": 1}, balanced["actions"])

    for name in ("overlogging", "underlogging", "duplicate-store"):
        report = scorer.score(fixtures, json.loads((ROOT / "examples" / f"{name}.json").read_text(encoding="utf-8")))
        require(not report["pass"], f"{name} parody unexpectedly passed")
    duplicate = scorer.score(fixtures, json.loads((ROOT / "examples" / "duplicate-store.json").read_text(encoding="utf-8")))
    require(any("duplicate" in failure.lower() for failure in duplicate["failures"]), duplicate["failures"])

    print("Decision Ledger proportionality: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
