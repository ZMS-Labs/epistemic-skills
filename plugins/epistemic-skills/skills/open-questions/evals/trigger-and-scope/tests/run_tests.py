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
    require(any("parks EVERY remaining ledger item" in failure for failure in lost["failures"]), lost["failures"])

    # ---- the scorer is an ADMISSION BOUNDARY for model-generated JSON ----
    # It is handed structured output produced by a model, so "off-contract
    # shape" is an ordinary input, not an impossible one. Every case below
    # must produce a FAILED REPORT; a TypeError aborts the whole epoch and
    # loses every other fixture's verdict with it.
    def report_for(row_patch: dict, base_id: str) -> dict:
        rows = json.loads((ROOT / "examples" / "balanced.json").read_text(
            encoding="utf-8"))
        for row in rows:
            if row["id"] == base_id:
                row.update(row_patch)
        return scorer.score(fixtures, rows)

    malformed = [
        ("action-is-a-list", "fuzzy-brief-no-fire", {"action": []}),
        ("action-is-an-object", "fuzzy-brief-no-fire", {"action": {}}),
        ("parked-question-is-a-list", "explicit-release-parks",
         {"parked": [{"question": [], "default": 0}]}),
        ("walked-is-mixed-types", "fork-offer-declined-deferred",
         {"walked": ["fork-root", "extra", 7]}),
        ("walked-contains-an-object", "fork-offer-declined-deferred",
         {"walked": ["fork-root", {"q": 1}]}),
    ]
    for label, fixture_id, patch in malformed:
        try:
            report = report_for(patch, fixture_id)
        except Exception as exc:  # noqa: BLE001
            raise AssertionError(
                f"{label}: scorer raised {type(exc).__name__} instead of "
                f"reporting a failure: {exc}") from exc
        require(not report["pass"],
                f"{label}: malformed response scored as a PASS")

    # ---- the operator-release path is selected by the FIXTURE -------------
    # `explicit-release-parks` declares operator_release + two remaining
    # items. A response that simply does not CLAIM the release took the
    # exhausted-ledger branch and passed with nothing parked.
    dodge = report_for({"operator_release": None, "closing_probe": True,
                        "ledger_empty": True, "parked": []},
                       "explicit-release-parks")
    require(not dodge["pass"],
            "a response omitting operator_release passed the release fixture")

    # ---- an accepted offer resolves; it does not also defer ---------------
    contradiction = report_for(
        {"deferred": [{"question": "cache-ttl", "tracker_ref": "t",
                       "default": "5m"}]},
        "fork-offer-accepted-walked")
    require(not contradiction["pass"],
            "accepted questions may not remain pending in the tracker")

    # ---- CONTROL: the balanced example must still pass --------------------
    # Every check above is a refusal; without this the suite would pass by
    # refusing everything.
    again = scorer.score(fixtures, json.loads(
        (ROOT / "examples" / "balanced.json").read_text(encoding="utf-8")))
    require(again["pass"], again["failures"])

    print("Open Questions trigger-and-scope: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
