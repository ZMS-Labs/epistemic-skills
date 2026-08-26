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

    # ---- an explicit null is a SHAPE violation, not an absence ----------
    # `_bare_str_set` returned (set(), ok=True) for None, but every caller
    # passes `row.get(field, [])` -- so None reaches it ONLY as an explicit
    # JSON null, never as an absent field. Treating that as an empty list
    # certified an off-contract response instead of naming the shape.
    balanced_rows = json.loads(
        (ROOT / "examples" / "balanced.json").read_text(encoding="utf-8"))
    require(scorer.score(fixtures, balanced_rows)["pass"],
            "balanced example must pass before the null probe")
    # The discriminating case is a field the response may legitimately OMIT:
    # an absent `pulled_tickets` on a chart-map fixture with no fog tickets
    # passes, and so did an explicit `null` -- so `null` was indistinguishable
    # from absent while the helper's own contract calls non-list shapes
    # malformed. (Nulling a REQUIRED field fails for a different reason and
    # would not test this at all.)
    nulled = json.loads(
        (ROOT / "examples" / "balanced.json").read_text(encoding="utf-8"))
    patched = False
    for row in nulled:
        if row.get("action") == "chart-map" and "pulled_tickets" not in row:
            row["pulled_tickets"] = None
            patched = True
            break
    require(patched, "no chart-map row without pulled_tickets to null out")
    report = scorer.score(fixtures, nulled)
    require(not report["pass"],
            "an explicit null pulled_tickets scored as a PASS")

    print("Wayfinding trigger-and-scope: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
