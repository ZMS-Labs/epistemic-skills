#!/usr/bin/env python3
"""Polarity tests for intent-traced-merge trigger discipline and resolution scope."""

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
    require(score_path.is_file(), f"missing intent-traced-merge trigger-and-scope scorer: {score_path}")
    spec = importlib.util.spec_from_file_location("intent_traced_merge_scope", score_path)
    scorer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scorer)
    fixtures = json.loads((ROOT / "fixtures.json").read_text(encoding="utf-8"))
    require([f["id"] for f in fixtures] == [
        "semantic-overlap-trace", "ambiguous-textual-trace", "mixed-hunks-classify",
        "dropped-intent-recorded", "divergent-decisions-escalate", "undocumented-merge-review",
        "uncertain-tree-abort", "formatting-only-mechanical", "lockfile-regenerate",
        "generated-file-regenerate", "huge-lockfile-looks-semantic",
        "adjacent-disjoint-mechanical", "documented-merge-review-no-fire",
    ], "intent-traced-merge fixture inventory drifted")

    balanced = scorer.score(fixtures, json.loads((ROOT / "examples" / "balanced.json").read_text(encoding="utf-8")))
    require(balanced["pass"], balanced["failures"])
    require(balanced["actions"] == {
        "trace-and-resolve": 4, "escalate-decision": 1, "review-provenance": 1,
        "abort-restart": 1, "mechanical-resolve": 2, "regenerate": 3, "no-fire": 1,
    }, balanced["actions"])

    for name in ("overfiring", "underfiring"):
        report = scorer.score(fixtures, json.loads((ROOT / "examples" / f"{name}.json").read_text(encoding="utf-8")))
        require(not report["pass"], f"{name} parody unexpectedly passed")

    over = scorer.score(fixtures, json.loads((ROOT / "examples" / "overfiring.json").read_text(encoding="utf-8")))
    require(any("expected mechanical-resolve, got trace-and-resolve" in f for f in over["failures"]), over["failures"])
    require(any("traced out-of-scope hunks" in f for f in over["failures"]), over["failures"])
    require(any("made silently" in f for f in over["failures"]), over["failures"])
    require(any("hand-resolving a regenerable artifact" in f for f in over["failures"]), over["failures"])

    under = scorer.score(fixtures, json.loads((ROOT / "examples" / "underfiring.json").read_text(encoding="utf-8")))
    require(any("expected trace-and-resolve, got mechanical-resolve" in f for f in under["failures"]), under["failures"])
    require(any("non-trivial hunks not all traced" in f for f in under["failures"]), under["failures"])
    require(any("expected escalate-decision, got trace-and-resolve" in f for f in under["failures"]), under["failures"])
    require(any("expected review-provenance, got no-fire" in f for f in under["failures"]), under["failures"])
    require(any("ruling must cite both origins" in f for f in under["failures"]), under["failures"])
    require(any("motivating checks must run" in f for f in under["failures"]), under["failures"])
    require(any("unsanctioned drift" in f for f in under["failures"]), under["failures"])
    require(any("aborted" in f for f in under["failures"]), under["failures"])

    print("intent-traced-merge trigger-and-scope: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
