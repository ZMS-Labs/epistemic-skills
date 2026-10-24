#!/usr/bin/env python3
"""Deterministic scorer for epistemic (the guide) trigger discipline and scope."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

ACTIONS = {"use-method", "no-fire"}
# The 16 substantive suite skills. The guide itself ("epistemic") is NOT a
# substantive method: it is permitted as a method value only on a fixture
# carrying "guide_question": true, where loading the guide IS the work asked for.
METHODS = {
    "context-audit", "decision-ledger", "did-it-land", "evidence-locked-uat",
    "gauntlet", "health", "manifest", "metacognate", "open-questions",
    "outsource", "perspective", "recon", "resolve", "triage", "watch",
    "write-goal",
}
METHOD_FIELDS = ("method", "instructions_loaded", "claimed_use", "contribution", "limit_stated")


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_bool(value: object) -> bool:
    return isinstance(value, bool)


def score(fixtures: list[dict], responses: object) -> dict:
    failures: list[str] = []
    if not isinstance(responses, list):
        return {
            "pass": False,
            "failures": [f"responses must be an array of response objects, got {type(responses).__name__}"],
            "actions": {},
        }
    by_id = {
        row["id"]: row
        for row in responses
        if isinstance(row, dict) and isinstance(row.get("id"), str)
    }
    if len(by_id) != len(responses):
        failures.append("response ids missing or duplicated")
    actions: Counter = Counter()
    for fixture in fixtures:
        fid = fixture["id"]
        row = by_id.get(fid)
        if row is None:
            failures.append(f"{fid}: response missing")
            continue
        action = row.get("action")
        if not isinstance(action, str):
            failures.append(f"{fid}: action must be a string naming the discipline mode, got {type(action).__name__}")
            continue
        actions[action] += 1
        expected = fixture["expected_action"]
        if action not in ACTIONS:
            failures.append(f"{fid}: unknown action {action!r}")
            continue
        if action != expected:
            failures.append(f"{fid}: expected {expected}, got {action}")
            continue
        if expected == "no-fire":
            present = [field for field in METHOD_FIELDS if field in row]
            if present:
                failures.append(f"{fid}: no-fire must be silent — method fields present: {present}")
            continue
        # expected == "use-method"
        method = row.get("method")
        if not isinstance(method, str):
            failures.append(f"{fid}: method must be a string naming a substantive suite skill, got {type(method).__name__}")
            continue
        if method == "epistemic":
            if not fixture.get("guide_question"):
                failures.append(f"{fid}: method 'epistemic' is permitted only on a guide question — the guide is not a substantive method")
        elif method not in METHODS:
            failures.append(f"{fid}: unknown method {method!r} — method must be one of the substantive suite skills")
        expected_method = fixture.get("expected_method")
        if expected_method and method != expected_method:
            failures.append(f"{fid}: expected method {expected_method}, got {method}")
        loaded = row.get("instructions_loaded")
        claimed = row.get("claimed_use")
        if not _is_bool(loaded):
            failures.append(f"{fid}: instructions_loaded must be a boolean, got {type(loaded).__name__}")
        if not _is_bool(claimed):
            failures.append(f"{fid}: claimed_use must be a boolean, got {type(claimed).__name__}")
        if claimed is True and loaded is not True:
            failures.append(f"{fid}: claimed_use true requires instructions_loaded true — never claim use without loading the actual instructions")
        if fixture.get("instructions_available") is False:
            if loaded is not False:
                failures.append(f"{fid}: instructions unavailable — instructions_loaded must be false, not a remembered name or summary")
            if claimed is not False:
                failures.append(f"{fid}: never claim use of unavailable instructions")
            if row.get("limit_stated") is not True:
                failures.append(f"{fid}: instructions unavailable — limit_stated must be true: state that limit and use an adequate available alternative")
        elif loaded is not True:
            failures.append(f"{fid}: instructions_loaded must be true — load the actual instructions; a remembered name, a summary or an announcement does not substitute for the method")
        if not _nonempty(row.get("contribution")):
            failures.append(f"{fid}: contribution must be nonempty — name the method's substantive contribution, or state explicitly that it returned no material finding")
    return {"pass": not failures, "failures": failures, "actions": dict(actions)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("responses", type=Path)
    parser.add_argument("--fixtures", type=Path, default=Path(__file__).resolve().parent / "fixtures.json")
    args = parser.parse_args()
    fixtures = json.loads(args.fixtures.read_text(encoding="utf-8"))
    responses = json.loads(args.responses.read_text(encoding="utf-8"))
    report = score(fixtures, responses)
    print(json.dumps(report, indent=2))
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
