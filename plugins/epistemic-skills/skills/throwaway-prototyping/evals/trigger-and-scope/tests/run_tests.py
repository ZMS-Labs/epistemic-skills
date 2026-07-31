#!/usr/bin/env python3
"""Polarity tests for throwaway-prototyping trigger discipline and disposal contract."""

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
    require(score_path.is_file(), f"missing throwaway-prototyping trigger-and-scope scorer: {score_path}")
    spec = importlib.util.spec_from_file_location("throwaway_prototyping_scope", score_path)
    scorer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scorer)
    fixtures = json.loads((ROOT / "fixtures.json").read_text(encoding="utf-8"))
    require([f["id"] for f in fixtures] == [
        "explicit-spike-fires", "option-set-try-it-fires", "debate-cost-exceeds-build-fires",
        "thin-build-discriminator-fires", "answerable-by-reading-no-fire",
        "answerable-by-derivation-no-fire", "answerable-by-literature-no-fire",
        "early-implementation-no-fire", "spike-against-live-infra-refused",
        "try-both-answerable-by-reading-no-fire", "promotion-attempt-refused",
        "answered-prototype-disposed",
    ], "throwaway-prototyping fixture inventory drifted")

    balanced = scorer.score(fixtures, json.loads((ROOT / "examples" / "balanced.json").read_text(encoding="utf-8")))
    require(balanced["pass"], balanced["failures"])
    require(balanced["actions"] == {
        "run-prototype": 4, "no-fire": 5, "refuse-live-target": 1,
        "refuse-promotion": 1, "record-and-dispose": 1,
    }, balanced["actions"])

    for name in ("overfiring", "underfiring"):
        report = scorer.score(fixtures, json.loads((ROOT / "examples" / f"{name}.json").read_text(encoding="utf-8")))
        require(not report["pass"], f"{name} parody unexpectedly passed")
    over = scorer.score(fixtures, json.loads((ROOT / "examples" / "overfiring.json").read_text(encoding="utf-8")))
    require(any("expected no-fire, got run-prototype" in failure for failure in over["failures"]), over["failures"])
    require(any("expected refuse-live-target" in failure for failure in over["failures"]), over["failures"])
    require(any("never promoted" in failure for failure in over["failures"]), over["failures"])
    under = scorer.score(fixtures, json.loads((ROOT / "examples" / "underfiring.json").read_text(encoding="utf-8")))
    require(any("expected run-prototype, got no-fire" in failure for failure in under["failures"]), under["failures"])
    require(any("recorded durably" in failure for failure in under["failures"]), under["failures"])

    print("throwaway-prototyping trigger-and-scope: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
