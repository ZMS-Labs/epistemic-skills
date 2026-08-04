#!/usr/bin/env python3
"""Polarity tests for outsource trigger discipline and packet/relay scope."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXPECTED_IDS = [
    "explicit-superior-model-fires", "copy-paste-review-handoff-fires",
    "beyond-origin-surface-fires", "capable-target-preflight-fires",
    "in-session-subagent-no-fire", "self-handoff-local-task-no-fire",
    "colleague-agent-question-no-fire", "inbound-target-work-no-fire",
    "packet-before-prompt-state", "pointer-not-paste-state",
    "relay-claim-verified-state", "unpushed-packet-blocked-state",
    "readonly-target-preflight-blocked-state", "hidden-chat-context-blocked-state",
]


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    score_path = ROOT / "score.py"
    require(score_path.is_file(), f"missing outsource trigger-and-scope scorer: {score_path}")
    spec = importlib.util.spec_from_file_location("outsource_scope", score_path)
    scorer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scorer)
    fixtures = json.loads((ROOT / "fixtures.json").read_text(encoding="utf-8"))

    # Fixture schema sanity: pinned inventory, unique ids, known actions/triggers,
    # stated scenarios, known blocker vocabulary.
    ids = [f["id"] for f in fixtures]
    require(ids == EXPECTED_IDS, "outsource fixture inventory drifted")
    require(len(set(ids)) == len(ids), "fixture ids must be unique")
    for fixture in fixtures:
        require(fixture["expected_action"] in scorer.ACTIONS,
                f"{fixture['id']}: unknown expected_action {fixture['expected_action']!r}")
        require(fixture["trigger"] in {"explicit", "implicit", "none", "state"},
                f"{fixture['id']}: unknown trigger {fixture['trigger']!r}")
        require(isinstance(fixture["scenario"], str) and fixture["scenario"].strip(),
                f"{fixture['id']}: scenario must state the environment")
        if "expected_blocker" in fixture:
            require(fixture["expected_blocker"] in scorer.BLOCKERS,
                    f"{fixture['id']}: unknown expected_blocker {fixture['expected_blocker']!r}")

    # Balanced example passes with the expected mode census.
    balanced = scorer.score(fixtures, json.loads((ROOT / "examples" / "balanced.json").read_text(encoding="utf-8")))
    require(balanced["pass"], balanced["failures"])
    require(balanced["actions"] == {"publish-packet": 6, "no-fire": 4, "report-blocked": 3, "verify-relay": 1},
            balanced["actions"])

    # Every parody fails for its named polarity.
    for name in ("overfiring", "underfiring"):
        report = scorer.score(fixtures, json.loads((ROOT / "examples" / f"{name}.json").read_text(encoding="utf-8")))
        require(not report["pass"], f"{name} parody unexpectedly passed")

    over = scorer.score(fixtures, json.loads((ROOT / "examples" / "overfiring.json").read_text(encoding="utf-8")))
    require(sum("expected no-fire" in failure for failure in over["failures"]) == 4, over["failures"])
    require(sum("expected report-blocked, got publish-packet" in failure for failure in over["failures"]) == 3,
            over["failures"])

    under = scorer.score(fixtures, json.loads((ROOT / "examples" / "underfiring.json").read_text(encoding="utf-8")))
    require(sum("expected publish-packet" in failure for failure in under["failures"]) >= 3, under["failures"])
    require(any("40-character commit SHA" in failure for failure in under["failures"]), under["failures"])
    require(any("never pasted into it" in failure for failure in under["failures"]), under["failures"])
    require(any("before re-verification" in failure for failure in under["failures"]), under["failures"])
    require(any("must be an array of bare ids" in failure for failure in under["failures"]), under["failures"])

    # Scorer rejects an unknown action — including a relay exit status posing as a mode.
    unknown = scorer.score(fixtures, [{"id": "explicit-superior-model-fires", "action": "COMPLETE"}])
    require(any("unknown action 'COMPLETE'" in failure for failure in unknown["failures"]), unknown["failures"])

    # Scorer rejects duplicated response ids.
    dup = scorer.score(fixtures, [{"id": "in-session-subagent-no-fire", "action": "no-fire"},
                                  {"id": "in-session-subagent-no-fire", "action": "no-fire"}])
    require(any("missing or duplicated" in failure for failure in dup["failures"]), dup["failures"])

    # Fail-closed shape handling: non-list list-fields name the violation, never crash.
    balanced_rows = json.loads((ROOT / "examples" / "balanced.json").read_text(encoding="utf-8"))
    warped = []
    for row in balanced_rows:
        row = dict(row)
        if row["id"] == "capable-target-preflight-fires":
            row["capabilities_verified"] = True
        if row["id"] == "readonly-target-preflight-blocked-state":
            row["capabilities_failed"] = {"writable-checkout": "no"}
        warped.append(row)
    shape = scorer.score(fixtures, warped)
    require(any("capabilities_verified must be an array of bare ids, got bool" in f for f in shape["failures"]),
            shape["failures"])
    require(any("capabilities_failed must be an array of bare ids, got dict" in f for f in shape["failures"]),
            shape["failures"])

    # A handoff path without a work-id segment is off-contract.
    workless = [dict(balanced_rows[0], handoff_path="docs/outsource/HANDOFF.md")]
    pathreport = scorer.score(fixtures, workless)
    require(any("docs/outsource/<work-id>/HANDOFF.md" in f for f in pathreport["failures"]), pathreport["failures"])

    # Fail-closed on unhashable off-contract types: a list action, a list id,
    # and non-string entries inside a list field name the violation, never crash.
    hostile = scorer.score(fixtures, [{"id": "explicit-superior-model-fires", "action": ["publish-packet"]}])
    require(any("unknown action ['publish-packet']" in f for f in hostile["failures"]), hostile["failures"])
    hostile = scorer.score(fixtures, [{"id": ["explicit-superior-model-fires"], "action": "no-fire"}])
    require(any("missing or duplicated" in f for f in hostile["failures"]), hostile["failures"])
    warped_entries = []
    for row in balanced_rows:
        row = dict(row)
        if row["id"] == "relay-claim-verified-state":
            row["claims_checked"] = [{"claim": "tests-pass"}]
        warped_entries.append(row)
    entries = scorer.score(fixtures, warped_entries)
    require(any("claims_checked must be an array of bare ids, got dict entry" in f for f in entries["failures"]),
            entries["failures"])

    # Fail-closed on a non-list responses payload.
    notalist = scorer.score(fixtures, {"id": "explicit-superior-model-fires"})
    require(not notalist["pass"] and any("array of response objects" in f for f in notalist["failures"]),
            notalist["failures"])

    print("outsource trigger-and-scope: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
