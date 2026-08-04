#!/usr/bin/env python3
"""Deterministic scorer for Wayfinding trigger discipline and map/frontier scope."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

ACTIONS = {"chart-map", "work-frontier", "pull-ticket", "mint-ticket", "no-fire"}
RESOLVE_METHODS = {"derive", "research", "prototype", "ask"}


def _frontier(graph: dict) -> set:
    """A decision is frontier iff it is unresolved and every dependency is resolved."""
    return {
        name
        for name, spec in graph.items()
        if not spec.get("resolved")
        and all(graph.get(dep, {}).get("resolved") for dep in spec.get("deps", []))
    }


def _nonempty_str(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _bare_str_set(value: object) -> tuple[set, bool]:
    """Coerce a response list-field to a set of bare strings.

    Returns (set, ok). ok=False marks a malformed shape (not a list, or a
    non-string entry) — the caller emits a NAMED failure instead of letting
    set() raise on an unhashable entry (fail closed; live-epoch lesson,
    2026-08-04 v4 Tier-1 run: a subject reported frontier as objects and
    the scorer crashed instead of failing).
    """
    if value is None:
        return set(), True
    if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
        return set(), False
    return set(value), True


def score(fixtures: list[dict], responses: list[dict]) -> dict:
    failures: list[str] = []
    if not isinstance(responses, list):
        return {
            "pass": False,
            "failures": [f"responses must be a JSON array of response records, got {type(responses).__name__}"],
            "actions": {},
        }
    by_id: dict = {}
    bad_ids = False
    for row in responses:
        rid = row.get("id") if isinstance(row, dict) else None
        if not isinstance(rid, str) or rid in by_id:
            bad_ids = True
            continue
        by_id[rid] = row
    if bad_ids or len(by_id) != len(responses):
        failures.append("response ids missing or duplicated")
    actions: Counter = Counter()
    for fixture in fixtures:
        fid = fixture["id"]
        row = by_id.get(fid)
        if row is None:
            failures.append(f"{fid}: response missing")
            continue
        action = row.get("action")
        actions[action if isinstance(action, str) else f"<{type(action).__name__}>"] += 1
        expected = fixture["expected_action"]
        if not isinstance(action, str) or action not in ACTIONS:
            failures.append(f"{fid}: unknown action {action!r}")
            continue
        if action != expected:
            failures.append(f"{fid}: expected {expected}, got {action}")
            continue
        graph = fixture.get("decision_graph", {})
        if expected == "no-fire":
            if row.get("map_artifact") or row.get("minted_tickets") or row.get("visible_process"):
                failures.append(f"{fid}: no-fire must be silent — no map, no tickets, no process artifact")
        elif expected == "chart-map":
            if not _nonempty_str(row.get("map_artifact")):
                failures.append(f"{fid}: chart-map requires one durable map artifact in the tracker")
            nodes = row.get("nodes", [])
            node_ids = {n.get("decision") for n in nodes if isinstance(n, dict)}
            if node_ids != set(graph):
                failures.append(f"{fid}: map nodes must be exactly the decisions — expected {sorted(graph)}, got {sorted(node_ids - {None})}")
            for node in nodes:
                if not isinstance(node, dict) or node.get("resolve_by") not in RESOLVE_METHODS:
                    failures.append(f"{fid}: every decision node names its cheapest resolution method (derive/research/prototype/ask)")
                    break
            resp_frontier, ok = _bare_str_set(row.get("frontier", []))
            if not ok:
                failures.append(f"{fid}: frontier must be an array of bare decision strings")
            elif resp_frontier != _frontier(graph):
                failures.append(f"{fid}: frontier wrong — expected {sorted(_frontier(graph))}, got {sorted(resp_frontier)}")
            if row.get("minted_tickets"):
                failures.append(f"{fid}: tickets minted from fog — unresolved decisions remain upstream")
            fog_tickets = set(fixture.get("fog_tickets", []))
            pulled, ok = _bare_str_set(row.get("pulled_tickets", []))
            if not ok:
                failures.append(f"{fid}: pulled_tickets must be an array of bare ticket ids")
            elif fog_tickets and not fog_tickets <= pulled:
                failures.append(f"{fid}: guess-encoding tickets must be pulled back to the map — missing {sorted(fog_tickets - pulled)}")
        elif expected == "work-frontier":
            frontier = _frontier(graph)
            resp_frontier, ok = _bare_str_set(row.get("frontier", []))
            if not ok:
                failures.append(f"{fid}: frontier must be an array of bare decision strings")
            elif resp_frontier != frontier:
                failures.append(f"{fid}: recomputed frontier wrong — expected {sorted(frontier)}, got {sorted(resp_frontier)}")
            worked_set, ok = _bare_str_set(row.get("worked", []))
            if not ok:
                failures.append(f"{fid}: worked must be an array of bare decision strings")
                worked_set = set()
            if not row.get("worked"):
                failures.append(f"{fid}: at least one frontier decision must be worked")
            off_frontier = worked_set - frontier
            if off_frontier:
                failures.append(f"{fid}: non-frontier decision worked {sorted(off_frontier)} — its answer will be re-litigated")
            resolutions = row.get("resolutions", [])
            recorded = (
                {r.get("decision"): r for r in resolutions if isinstance(r, dict)}
                if isinstance(resolutions, list) else {}
            )
            for decision in sorted(worked_set):
                entry = recorded.get(decision)
                if not entry or not _nonempty_str(entry.get("provenance")):
                    failures.append(f"{fid}: resolution of {decision!r} must be recorded on the map with provenance")
        elif expected == "pull-ticket":
            pulled, ok = _bare_str_set(row.get("pulled_tickets", []))
            if not ok:
                failures.append(f"{fid}: pulled_tickets must be an array of bare ticket ids")
            elif fixture["ticket"] not in pulled:
                failures.append(f"{fid}: fog-minted ticket {fixture['ticket']!r} must be pulled back to the map")
            if row.get("unresolved_ancestor") != fixture["unresolved_ancestor"]:
                failures.append(f"{fid}: the unresolved upstream ancestor must be named — expected {fixture['unresolved_ancestor']!r}")
            if row.get("minted_tickets"):
                failures.append(f"{fid}: no new tickets while an unresolved ancestor stands")
        elif expected == "mint-ticket":
            ticket = row.get("ticket")
            if not isinstance(ticket, dict):
                failures.append(f"{fid}: mint-ticket requires a ticket object carrying the three-fact handoff")
                continue
            depends, ok = _bare_str_set(ticket.get("depends_on", []))
            if not ok:
                failures.append(f"{fid}: ticket.depends_on must be an array of bare decision ids")
            elif depends != set(fixture.get("resolved_lineage", [])):
                failures.append(f"{fid}: ticket must link exactly its resolved decision lineage {sorted(fixture.get('resolved_lineage', []))}")
            if not _nonempty_str(ticket.get("observable_behavior")):
                failures.append(f"{fid}: ticket must state the observable behavior proving the slice works end-to-end")
            if not _nonempty_str(ticket.get("invalidating_decision")):
                failures.append(f"{fid}: ticket must name the upstream decision whose reversal invalidates it, or 'none'")
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
