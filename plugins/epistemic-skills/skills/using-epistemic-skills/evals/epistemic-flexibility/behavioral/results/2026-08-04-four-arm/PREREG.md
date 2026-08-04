# Preregistration — four-arm campaign run (recorded before any dispatch)

Run of the committed design (`../campaign-design-2026-08-04.md`) at the
**minimum valid size**: 4 arms × 6 scenarios × 3 repeats = 72 fresh,
context-isolated, blinded trials. Per the design's power-honesty rule this
size is **EXPLORATORY regardless of p-value** — it informs the v4.0.0
consolidation decision; it licenses no superiority claim (the claim gate
additionally requires the two real-incident scenarios, not yet authored).

- Seed: **20260804** (deterministic shuffle of the 72 (arm, scenario, repeat)
  cells; trial keys are opaque `T01..T72`).
- Arms: hash-pinned in `ARMS-MANIFEST.json`, committed before dispatch.
  Subject (arm D) epistemic-flexibility.md sha256: `098a2bcde6ca631e279b3db7555691c15230c7c3baa2431da4d34c163a5dbb20`.
- Every dispatch carries the FULL trace contract
  (`arms/SHARED-trace-contract.md`) with all closed vocabularies inline —
  the fix for the 2026-07-22 smoke's fatal under-specification.
- Scoring: shipped `score_behavior.py` unmodified, per cell.
- Analysis (from the design, restated): primary D>A on total passes, paired
  by (scenario, repeat), exact permutation, α=0.05 one-sided; guard
  co-primary: D's false-hold count on the clean control (06) ≤ A's + 1;
  secondaries (Holm): D-B, B-A, C-A, D-C. No interim looks; partial runs
  commit as BLOCKED.

## Predictions (falsifiable, before dispatch)

1. Arms remain **statistically indistinguishable at this size** (18 paired
   cells cannot separate plausible effects); primary p > 0.05.
2. Directionally, D ≥ A on total passes, with any separation concentrated in
   scenarios 02/03/05 (the goal/experiment/failure_chain scenarios the
   full-schema dispatch now makes winnable for every arm).
3. The uniform over-hold on the clean control (06) **persists in all four
   arms** (the smoke's real behavioral finding; schema fixes do not touch
   it).
4. Arm C (psychology language alone) shows no advantage over A anywhere.
5. All 72 trials produce parseable traces (the pinned contract carries, as
   in the 2026-08-04 epoch waves).
