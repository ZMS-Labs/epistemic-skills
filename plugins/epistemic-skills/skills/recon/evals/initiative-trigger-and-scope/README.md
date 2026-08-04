# Wayfinding trigger-and-scope fixtures

This battery tests the trigger discipline and the map/frontier scope contract:
an explicit "chart this initiative" / "break this down" on a foggy effort, a
brief with materially different architectures still live, or a backlog whose
tickets encode unmade decisions all fire chart-map; resolved efforts (plan
decomposition), a single open decision, one-task recon, and goal-shaping never
fire — even when the trigger phrase is present but the fog is gone. State
transitions are covered deterministically: the frontier is recomputed from the
fixture's decision graph (unresolved nodes whose dependencies are all
resolved), only frontier decisions may be worked and each resolution carries
provenance, a fog-minted ticket with an unresolved upstream ancestor is pulled
back to the map, and a fog-free region mints a ticket carrying the three-fact
handoff (resolved lineage, observable behavior, invalidating decision).
Over-firing, minting from fog, and working non-frontier decisions are defects,
not extra rigor.

This battery is structural and trigger-level only: it scores declared actions
against fixture contracts and is NOT behavioral proof that a live agent
exercises the skill.

Run `python tests/run_tests.py`.

## Live-epoch response contract

Pinned before the first live epoch: `action` names the discipline mode that
fired — `chart-map`, `work-frontier`, `pull-ticket`, `mint-ticket`, or
`no-fire`. A `no-fire` is silent (no `map_artifact`, `minted_tickets`, or
`visible_process` fields). `chart-map` reports the durable `map_artifact`
(tracker ref), `nodes` (one entry per decision: `{"decision", "resolve_by"}`
with resolve_by one of derive/research/prototype/ask), the computed
`frontier` (unresolved decisions whose dependencies are all resolved),
`pulled_tickets` for any guess-encoding backlog tickets, and mints nothing
while fog stands. `work-frontier` reports the recomputed `frontier`,
`worked` (frontier decisions only), and `resolutions` (`{"decision",
"provenance"}` per worked decision). `pull-ticket` names `pulled_tickets`
and the `unresolved_ancestor`. `mint-ticket` returns a `ticket` object
carrying the three-fact handoff: `depends_on` (exactly the resolved
lineage), `observable_behavior`, `invalidating_decision` (or "none").

First live behavioral epoch: 2026-08-04, FAIL 11/13 — see
`results/2026-08-04/RESULTS.md`; both failures are reporting-layer
divergences over correct conduct (register: issue #77).
