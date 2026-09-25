# Research-gap coverage-map fixtures

This battery pins the coverage-map contract in `../../reference/research-gap-matrix.md`
(METHOD.md §1 coverage frame, §4a, §9a): a sparse or empty cell is
`POTENTIAL GAP`, never proof of absence; placements are traceable to paper
IDs, exact passages, and source locations; a cell is handed forward only
after the validation gate runs (terminology, alternate designs, boundary
conditions, nulls, counterevidence, coverage limit); and a cell whose
validation searches were not run stays `unresolved` — it is never promoted to
a validated gap or a focused-question handoff.

The fixtures are structural: they score declared cell records and handoff
fields against required/forbidden markers, not whether a live agent's actual
coverage map was any good. Passing them is NOT behavioral proof.

Fixtures live in `fixtures.yaml` (`schema: research-gap-matrix-fixtures@1`).
No scorer or live epoch exists yet; the first scored run and its results
belong under `results/` with the response contract pinned before the epoch
(lesson of the context-audit 2026-08-04 epoch — see the trigger-and-scope
battery's README).
