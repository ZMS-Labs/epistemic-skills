# Live behavioral epoch — 2026-08-04 (first epoch for this battery)

**Outcome: FAIL — 11/13 fixtures pass the deterministic scorer; 2 named
failures.** Supersedes `results/BLOCKED.md`.

## Methodology

Protocol as the sibling 2026-08-04 epochs: thirteen fully isolated
general-purpose subagents (claude-fable-5, Claude Code harness, N=1), one
per fixture, subject-blinded (expected actions and trigger labels
withheld; decision graphs and situational facts restated neutrally),
subjects read exactly SKILL.md (evals/ forbidden), shipped `score.py`
unmodified. Preregistration before scoring: "11/13; failures exactly
backlog-guess-tickets (mode-vs-outcome labeling) and fog-free-region-mint
(decorated depends_on lineage)" — confirmed exactly.

## Results

chart-map 3 · pull-ticket 2 · work-frontier 1 · mint-ticket 1 · no-fire 6.

- **PASS (11):** all six no-fire hard negatives silent (including the two
  trigger-phrase-present-fog-gone traps); three charted maps with exact
  node sets, correct frontier computations, and zero fog-minting; the
  frontier recompute worked exactly the two newly-workable decisions with
  provenance per resolution; the fog-ticket pull named its unresolved
  ancestor.
- **FAIL (2):**
  1. `backlog-guess-tickets` — conduct was complete and correct (charted
     the map, exact node, correct frontier, pulled both guess-encoding
     tickets, minted nothing) but the agent labeled `action` by the pull
     it performed rather than the `chart-map` mode that fired — the same
     mode-vs-outcome vocabulary divergence as the open-questions and
     context-audit epochs, now observed in a third battery.
  2. `fog-free-region-mint` — the minted ticket carried the full
     three-fact handoff with a strong observable-behavior clause, but the
     agent decorated its `depends_on` entries
     ("storage-engine (RESOLVED, provenance linked on map)") where the
     scorer requires the bare decision ids — a formatting divergence, not
     a lineage error (both decisions present, nothing extra).

## Diagnosis

Both failures are reporting-layer, matching the cross-battery pattern:
across three failing epochs every single scorer failure (2 + 6 + 2) has
been a response-vocabulary or formatting divergence over
behaviorally-correct conduct, while every hard negative across all four
epochs (6 + 6 + 6 + 6) stayed silent. Suite-level implication for issue
#77: the batteries need one shared, versioned live-epoch response contract
(action = fired mode; bare-id list fields; silence semantics), or the
scorers need canonicalization at ingestion (e.g. id-prefix matching on
list fields). This epoch stands as-is; the second epoch runs after that
lands.

## Methodology incident (recorded)

One subject (`explicit-break-down-foggy`) exercised real side effects
during its trial: it wrote an actual map file into the repository
working tree (`docs/wayfinding/WAYMAP-001.md`). The artifact was removed
before landing — trial side effects are not repo content — and future
dispatch prompts must state that trials are simulations and may not
write files. The response itself remains valid (the scorer consumes the
JSON, not the side effect).

## Honest limits

Smoke-scale, N=1 per fixture, one model/harness, same model family
throughout; subject-level blinding only; dispatch glosses are part of the
intervention surface.
