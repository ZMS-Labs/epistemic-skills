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
            if set(row.get("frontier", [])) != _frontier(graph):
                failures.append(f"{fid}: frontier wrong — expected {sorted(_frontier(graph))}, got {sorted(set(row.get('frontier', [])))}")
            if row.get("minted_tickets"):
                failures.append(f"{fid}: tickets minted from fog — unresolved decisions remain upstream")
            fog_tickets = set(fixture.get("fog_tickets", []))
            if fog_tickets and not fog_tickets <= set(row.get("pulled_tickets", [])):
                failures.append(f"{fid}: guess-encoding tickets must be pulled back to the map — missing {sorted(fog_tickets - set(row.get('pulled_tickets', [])))}")
        elif expected == "work-frontier":
            frontier = _frontier(graph)
            if set(row.get("frontier", [])) != frontier:
                failures.append(f"{fid}: recomputed frontier wrong — expected {sorted(frontier)}, got {sorted(set(row.get('frontier', [])))}")
            worked = row.get("worked", [])
            if not worked:
                failures.append(f"{fid}: at least one frontier decision must be worked")
            off_frontier = set(worked) - frontier
            if off_frontier:
                failures.append(f"{fid}: non-frontier decision worked {sorted(off_frontier)} — its answer will be re-litigated")
            recorded = {r.get("decision"): r for r in row.get("resolutions", []) if isinstance(r, dict)}
            for decision in worked:
                entry = recorded.get(decision)
                if not entry or not _nonempty_str(entry.get("provenance")):
                    failures.append(f"{fid}: resolution of {decision!r} must be recorded on the map with provenance")
        elif expected == "pull-ticket":
            if fixture["ticket"] not in set(row.get("pulled_tickets", [])):
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
            if set(ticket.get("depends_on", [])) != set(fixture.get("resolved_lineage", [])):
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
