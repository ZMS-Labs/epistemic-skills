# Epistemic-flexibility v3 implementation plan

## Phase 1 — Functional integration — COMPLETE

- Add the cross-cutting definition without creating a new discipline.
- Bind each control to the existing skill that owns the relevant moment.
- Extend Decision Ledger for recurrent corrections.
- Preserve fail-closed and re-fire semantics.

## Phase 2 — Deterministic machinery — COMPLETE

- Add `epistemic-process-trace@1` protocol validator.
- Add planted defect fixtures and clean low-stakes controls.
- Add artifact-grounded behavioral scenario scorer and gold/bad self-test.
- Add CI covering new and relevant existing stdlib checks.

## Phase 3 — Independent review — PENDING DIFFERENT ENVIRONMENT

- Freeze final diff.
- Run standard gauntlet with isolated roles.
- Resolve P1/P2 findings without weakening the controls.

## Phase 4 — Behavioral ablation — PENDING MODEL/AGENT RUNNER

- Run baseline / v2.8.0 / psychology-language-only / integrated arms.
- Measure trap catches, clean-control regressions, calibration, tokens, latency, and user
  correction burden.
- Convert at least one real incident into a held-out fixture.

## Phase 5 — Release — DEFERRED

- Decide whether evidence supports a 3.0.0 release.
- Use a separate release PR for manifest/version changes.
- Preserve honest labels if evidence supports only protocol conformance, not superiority.
