# Gauntlet — full DeepReason integration roadmap (phased, self-measured)

Full integration of **every useful DeepReason quality**, delivered under
DeepReason's own discipline applied recursively: **keep only what measures
cost-positive.** Each bundle is integrated, then the gauntlet is turned on a
**battery of past real gauntlet subjects** (the 2026-05-19 Plex/arr dry-run, the
2026-07-03 FO north-star gauntlet, …); a piece is kept only if it catches more
real defects or the same defects cheaper. Comprehensiveness *earned*, not
assumed — the recursion is what makes this the operator's tool, not a cargo-cult
of the repo.

## The four capability bundles

**Bundle 0 — the four disciplines (Phase 0; honest per-item status):**
falsifiability contract on every finding (SHIPPED — schema-enforced, structural
falsifier check) · compiled mechanical checks / judge-token-free refutation
(SHIPPED — verify_evidence.py, validate_roster.py, selector constraint fixtures)
· certified arbitrator (planted-flaw seat battery + degraded-control gate —
**BUILT + RUN 2026-07-17: 10/10 catch, certified at standard rigor** — `evals/arbitrator-certification/`) · replayable spend-accounted log (`meter==log`)
(SHIPPED — Workflow journal + selection replay records).

**Bundle A — Generation rigor (better findings):**
- **Verbalized Sampling** — each lens returns a *distribution* of candidate
  findings with typicality estimates, not one.
- **Stance rotation (decay) + problem turnover** — forces novelty/diversity
  across passes; turnover was DeepReason's only novelty-*raising* force.
- **Refuted-relapse gate + orbit/dryness detector** — never re-argue a killed
  finding; detect spinning (measured 4.3× token waste) and stop.

**Bundle B — Adjudication rigor (trustworthy verdict):**
- **Criterion-level forced-choice, both-orders, verbosity-penalized judging** —
  naive pairwise judging threw away 8/9 votes to position bias.
- **Grounded / Dung argumentation semantics with reinstatement** — a finding
  refuted by a later-refuted finding is mechanically reinstated; the formal
  backbone the Conflict Ledger currently does by hand.

**Bundle C — Measurement (quality-of-review as a number):**
- **Demarcation / hypervolume / reach measures** — how much risk space covered,
  how sharp the frontier.
- **Pareto-frontier + basin capture, schools/ladder** — turns "12 findings" into
  "3 basins of real risk."

**Bundle D — Substrate (auditable & robust):**
- Replayable log + `meter==log` + spend-on-every-exit-path (hardened in real
  mode) · content-addressed blobs/objects (integrity + dedup of equivalent
  findings) · schema-repair loop (tolerate models' off-JSON) · graduation
  contract (a prose-mode run's log is a valid engine root; no conversion).

## Phases

- **Phase 0 (largely done; two honest gaps):** the `/gauntlet` staple + docket
  modes + depth dial + aliases + registry/selector/validator (2026-07-10).
  Status: certified arbitrator **BUILT + RUN** (2026-07-17, 10/10 planted-flaw catch,
  `evals/arbitrator-certification/`); the past-subject behavioral regression battery has a
  **smoke subset run** (non-inferiority only; smoke notes are not shipped as a standalone
  file in this public package) with the full 24×4 sweep still unrun — no
  behavioral-superiority claim until it runs.
- **Phase 0.6 — Registry + selector (DONE 2026-07-10):** machine-readable
  `roster/registry.json` + lens.schema.json, four workflow roles, lifecycle
  states, deterministic constrained selector with replay records, generated
  roster views, mechanical validation (schema / collisions / 1000 fixtures /
  regressions).
- **Phase 1 — Generation rigor (Bundle A)** — measured against the battery.
- **Phase 2 — Adjudication rigor (Bundle B).**
- **Phase 3 — Measurement + substrate (Bundles C+D)** — full real-mode parity.

Each later phase = its own spec, gated by measured payoff on the battery. Design
provenance: the 3-agent bake-off design docs (2026-07-07); the design doc is
held in the operator's private repo and is not shipped in this package.
