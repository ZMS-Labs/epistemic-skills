#!/usr/bin/env python3
"""Polarity tests for Open Questions trigger discipline and auto-fire scope."""

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
    require(score_path.is_file(), f"missing Open Questions trigger-and-scope scorer: {score_path}")
    spec = importlib.util.spec_from_file_location("open_questions_scope", score_path)
    scorer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scorer)
    fixtures = json.loads((ROOT / "fixtures.json").read_text(encoding="utf-8"))
    require([f["id"] for f in fixtures] == [
        "explicit-phrase-full", "explicit-mid-execution-full", "fuzzy-brief-no-fire",
        "design-dialogue-defers", "reversible-fork-absent-park", "irreversible-fork-absent-hold",
        "irreversible-fork-present-fork-scoped", "fork-offer-declined-deferred",
        "fork-offer-accepted-walked", "explicit-release-parks",
    ], "Open Questions fixture inventory drifted")

    balanced = scorer.score(fixtures, json.loads((ROOT / "examples" / "balanced.json").read_text(encoding="utf-8")))
    require(balanced["pass"], balanced["failures"])
    require(balanced["actions"] == {"full-interview": 3, "no-fire": 2, "park-and-proceed": 1, "hold-escalate": 1, "fork-interview": 3}, balanced["actions"])

    for name in ("overfiring", "scope-creep", "lost-deferral"):
        report = scorer.score(fixtures, json.loads((ROOT / "examples" / f"{name}.json").read_text(encoding="utf-8")))
        require(not report["pass"], f"{name} parody unexpectedly passed")
    creep = scorer.score(fixtures, json.loads((ROOT / "examples" / "scope-creep.json").read_text(encoding="utf-8")))
    require(any("scope creep" in failure for failure in creep["failures"]), creep["failures"])
    lost = scorer.score(fixtures, json.loads((ROOT / "examples" / "lost-deferral.json").read_text(encoding="utf-8")))
    require(any("deferred with tracker_ref" in failure or "coverage_limits" in failure for failure in lost["failures"]), lost["failures"])

    print("Open Questions trigger-and-scope: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
