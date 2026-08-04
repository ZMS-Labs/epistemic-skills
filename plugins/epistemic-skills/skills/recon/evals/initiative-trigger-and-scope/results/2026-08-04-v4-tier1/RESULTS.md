# Live behavioral epoch — 2026-08-04 v4 Tier-1, corrected dispatch

**Outcome: FAIL — 11/13 fixtures pass the shipped scorer; one repeated
reporting-vocabulary divergence and one genuine hard-negative over-fire —
the first over-fire on a hard negative in the entire epoch program.**
Second valid epoch for these fixtures; first against the consolidated
subject (`recon/SKILL.md` routing to `reference/mode-initiative.md`).

## Methodology

Preregistered in
`docs/superpowers/specs/2026-08-04-v4-tier1-epoch-preregistration.md`,
dispatched under `docs/policy/LIVE-EPOCH-DISPATCH-CONTRACT.md`. This is
the **corrected** dispatch: the first v4 attempt omitted the
decision-graph facts the scenarios do not state and is quarantined as a
defect record in `../2026-08-04-v4-tier1-invalid-dispatch/`; this run
restates each fixture's decision nodes, dependencies, and resolution
status neutrally in the scenario (the first epoch's methodology —
restatement is mechanical from `decision_graph`, applied to the five
fixtures that carry one, never naming frontier, trigger, or expected
action). Thirteen isolated general-purpose subagents (claude-fable-5,
N=1), opaque sha256 keys, pinned README contract verbatim, shipped
`score.py` unmodified (as fixed the same day to fail closed on malformed
list fields — semantics unchanged).

## Results

chart-map 3 · work-frontier 1 · pull-ticket 2 · mint-ticket 2 · no-fire 5.

- **PASS (11):** all three charted maps with exact node sets, correct
  frontiers, zero fog-minting; the frontier recompute worked exactly the
  two newly-workable decisions with per-resolution provenance and left
  the non-frontier node explicitly unworked; both fog-ticket pulls named
  their unresolved ancestors; the fog-free mint carried the exact bare
  lineage and the three-fact handoff (the first epoch's decorated-lineage
  failure did not recur); five hard negatives silent.
- **FAIL (2):**
  1. `backlog-guess-tickets` — conduct correct (map charted, tickets
     pulled, nothing minted) but `action` labeled by the pull performed
     rather than the `chart-map` mode that fired — the same
     mode-vs-outcome divergence as the first epoch, now persistent
     across subjects and subject versions.
  2. `hard-neg-break-down-resolved` — **conduct failure (over-fire).**
     On a fully-resolved design whose planning belongs to the workflow
     layer, the subject walked the falsifiable gate, found the region
     fog-free, and minted a ticket (prose-decorated lineage) instead of
     staying silent. The sibling hard negative `resolved-effort-planning`
     no-fired correctly with the right reasoning, so this is a boundary
     the consolidated core draws but did not hold for one subject. This
     is the first hard-negative over-fire across all epochs (previously
     0 on 51+ hard negatives program-wide).

Mode selection itself produced zero failures. Extraction anomalies: one
trial carried surrounding prose (extracted per contract rule 3).

Register: issue #77.
