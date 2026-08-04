#!/usr/bin/env python3
"""Deterministic scorer for throwaway-prototyping trigger discipline and disposal contract."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

ACTIONS = {"run-prototype", "no-fire", "refuse-live-target", "refuse-promotion", "record-and-dispose"}
RESOLUTION_ROUTES = {"reading", "derivation", "literature", "normal-discipline"}


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def score(fixtures: list[dict], responses: list[dict]) -> dict:
    failures: list[str] = []
    by_id = {row.get("id"): row for row in responses if isinstance(row, dict)}
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
        actions[action] += 1
        expected = fixture["expected_action"]
        if action not in ACTIONS:
            failures.append(f"{fid}: unknown action {action!r}")
            continue
        if action != expected:
            failures.append(f"{fid}: expected {expected}, got {action}")
            continue
        if expected == "run-prototype":
            if not _nonempty(row.get("question")):
                failures.append(f"{fid}: the one named question must be pre-registered before building")
            if not _nonempty(row.get("throwaway_location")):
                failures.append(f"{fid}: disposal is declared at birth — a throwaway location must be named")
            if row.get("mergeable"):
                failures.append(f"{fid}: the throwaway location must not be mergeable by accident")
            options = set(fixture.get("options", []))
            if options:
                variants = set(row.get("variants", []))
                if not options <= variants:
                    failures.append(f"{fid}: comparative variants must cover every rival option — missing {sorted(options - variants)}")
        elif expected == "no-fire":
            route = fixture.get("resolution_route")
            if route not in RESOLUTION_ROUTES:
                failures.append(f"{fid}: fixture has unknown resolution_route {route!r}")
                continue
            if row.get("built") or _nonempty(row.get("throwaway_location")):
                failures.append(f"{fid}: no-fire builds nothing — no probe, no throwaway location")
            if row.get("resolved_by") != route:
                failures.append(f"{fid}: expected resolution via {route}, got {row.get('resolved_by')!r}")
        elif expected == "refuse-live-target":
            if not row.get("refused"):
                failures.append(f"{fid}: live/shared infrastructure is never a throwaway target — the build must be refused")
            if row.get("built"):
                failures.append(f"{fid}: nothing may be built against the shared/live target")
        elif expected == "refuse-promotion":
            if row.get("promoted"):
                failures.append(f"{fid}: prototype code is never promoted, merged, or adapted-in-place")
            if not row.get("answer_recorded"):
                failures.append(f"{fid}: the answer outlives the build — the recorded finding must be kept")
            if not row.get("rebuild_planned"):
                failures.append(f"{fid}: the real implementation is rebuilt under the normal discipline")
        elif expected == "record-and-dispose":
            answer = row.get("answer")
            recorded = (
                isinstance(answer, dict)
                and _nonempty(answer.get("question"))
                and _nonempty(answer.get("observation"))
                and _nonempty(answer.get("decision"))
                and _nonempty(row.get("record_ref"))
            )
            if not recorded:
                failures.append(f"{fid}: the answer must be recorded durably (question, observation, decision, record_ref) before disposal")
            if not row.get("disposed"):
                failures.append(f"{fid}: an answered prototype is a landmine — the build must be disposed")
            if row.get("kept_mergeable"):
                failures.append(f"{fid}: no line of the prototype may remain on a mergeable branch")
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
