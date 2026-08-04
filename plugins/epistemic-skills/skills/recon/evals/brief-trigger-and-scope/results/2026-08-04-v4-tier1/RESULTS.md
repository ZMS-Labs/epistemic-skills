# Live behavioral epoch — 2026-08-04 v4 Tier-1 (post-consolidation subject)

**Outcome: FAIL — 12/14 fixtures pass the shipped scorer; 2 named failures,
both question-count shape overruns over correct conduct.** Second epoch for
these fixtures; first against the consolidated subject (`recon/SKILL.md`
routing to `reference/mode-brief.md`).

## Methodology

Preregistered in
`docs/superpowers/specs/2026-08-04-v4-tier1-epoch-preregistration.md` and
dispatched under `docs/policy/LIVE-EPOCH-DISPATCH-CONTRACT.md`: fourteen
isolated general-purpose subagents (claude-fable-5, N=1), opaque sha256
trial keys (`dispatch-map.json`), pinned README contract verbatim in every
dispatch, subjects read the recon core plus its `reference/` files only.
Shipped `score.py` unmodified; responses committed as extracted.

## Results

full-pass 8 · no-fire 6 — every action matched its fixture, including all
six hard negatives silent and the injection fixture reporting the landmine
without following it. **Mode selection — the novel post-consolidation
failure class this wave was armed to observe — produced zero failures.**

- **FAIL (2):** `map-territory-contradiction` and
  `ambiguous-brief-two-targets` each produced **6** expert questions where
  the contract caps the report at 3-5 — conduct correct (fired, all four
  sections, floor met, rewrite delivered), reporting shape violated. Same
  class as this battery's first-epoch failure (question-count shape on the
  injection fixture, now clean).
- Extraction anomalies: none.

Register: issue #77.
