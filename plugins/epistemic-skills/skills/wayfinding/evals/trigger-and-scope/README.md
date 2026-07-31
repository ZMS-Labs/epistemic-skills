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

No live behavioral epoch has been run against this battery; see
`results/BLOCKED.md`.
