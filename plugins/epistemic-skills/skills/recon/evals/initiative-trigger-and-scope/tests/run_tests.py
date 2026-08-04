#!/usr/bin/env python3
"""Polarity tests for Wayfinding trigger discipline and map/frontier scope."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    score_path = ROOT / "score.py"
    require(score_path.is_file(), f"missing Wayfinding trigger-and-scope scorer: {score_path}")
    spec = importlib.util.spec_from_file_location("wayfinding_scope", score_path)
    scorer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scorer)
    fixtures = json.loads((ROOT / "fixtures.json").read_text(encoding="utf-8"))
    require([f["id"] for f in fixtures] == [
        "explicit-chart-initiative", "explicit-break-down-foggy", "foggy-brief-architectures-live",
        "backlog-guess-tickets", "resolved-effort-planning", "single-open-decision",
        "one-task-recon", "goal-shaping-request", "hard-neg-break-down-resolved",
        "hard-neg-stale-backlog", "frontier-recompute-after-resolution",
        "fog-minted-ticket-pull", "fog-free-region-mint",
    ], "Wayfinding fixture inventory drifted")

    balanced = scorer.score(fixtures, json.loads((ROOT / "examples" / "balanced.json").read_text(encoding="utf-8")))
    require(balanced["pass"], balanced["failures"])
    require(balanced["actions"] == {"chart-map": 4, "no-fire": 6, "work-frontier": 1, "pull-ticket": 1, "mint-ticket": 1}, balanced["actions"])

    for name in ("overfiring", "underfiring"):
        report = scorer.score(fixtures, json.loads((ROOT / "examples" / f"{name}.json").read_text(encoding="utf-8")))
        require(not report["pass"], f"{name} parody unexpectedly passed")
    over = scorer.score(fixtures, json.loads((ROOT / "examples" / "overfiring.json").read_text(encoding="utf-8")))
    require(any("expected no-fire, got chart-map" in failure for failure in over["failures"]), over["failures"])
    under = scorer.score(fixtures, json.loads((ROOT / "examples" / "underfiring.json").read_text(encoding="utf-8")))
    require(any("expected chart-map, got no-fire" in failure for failure in under["failures"]), under["failures"])
    require(any("expected pull-ticket, got no-fire" in failure for failure in under["failures"]), under["failures"])

    print("Wayfinding trigger-and-scope: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
