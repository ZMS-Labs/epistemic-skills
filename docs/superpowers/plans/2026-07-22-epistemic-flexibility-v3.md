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

## Phase 3 — Independent review — COMPLETE (2026-07-22)

- Froze final diff (HEAD `641ff2c`, bundle SHA256 `550bd8d6…`).
- Ran standard gauntlet with isolated concurrent role-lenses + separate arbitrator
  (`docs/gauntlet-runs/epistemic-flexibility-v3-2026-07-22/`). Verdict: **NO-GO** on one P1 —
  "fail-closed / enforced" was asserted but `validate_trace.py` never checked control↔action
  consistency (a `hold` control with a `deploy` action passed). `external_gate_owed: true` (a
  cross-family Step-7b read remains owed for the release decision).
- **Resolved P1 without weakening the controls (strengthened):** added the control/action
  consistency check to `validate_trace.py` (a non-acting control whose `action` asserts execution is
  rejected) + two adversarial bypass fixtures now caught; protocol battery 8/8 → **10/10**, behavioral
  **12/12** unchanged. Applied honest labels: added an "Enforcement status" section bounding what is
  mechanically checked vs structural-only vs human-policy; corrected the dossier's DCO description
  (email mismatch, not missing sign-off). P2 (real-ledger validation, `validation_kernel` teeth) and
  the dogfooding gap are carried forward as follow-ups, not release blockers.

## Phase 4 — Behavioral ablation — PENDING MODEL/AGENT RUNNER

- Run baseline / v2.8.0 / psychology-language-only / integrated arms.
- Measure trap catches, clean-control regressions, calibration, tokens, latency, and user
  correction burden.
- Convert at least one real incident into a held-out fixture.

## Phase 5 — Release — DEFERRED

- Decide whether evidence supports a 3.0.0 release.
- Use a separate release PR for manifest/version changes.
- Preserve honest labels if evidence supports only protocol conformance, not superiority.
