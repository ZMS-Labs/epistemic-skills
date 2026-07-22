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

## Phase 3 — Independent review — COMPLETE; P1 REOPENED by Step-7b (2026-07-22)

> **UPDATE 1 — 2026-07-22 (cross-family Step-7b DISSENT, verified):** the first P1 "closure" (a keyword
> matcher) was **premature** — measured 100% false-negative rate on execution paraphrases. P1 REOPENED.
>
> **UPDATE 2 — 2026-07-22 (structural fix, verified):** P1 **genuinely resolved**. Enforcement moved off
> free-text parsing onto a declared `action_executes` boolean: a non-acting control (`hold`/`escalate`)
> must declare it, and `action_executes: true` under such a control is rejected — **paraphrase-proof**
> (the structural rule rejects 15/15 paraphrases regardless of wording; battery PASS). The keyword
> matcher is demoted to a secondary mis-declaration lint. **Stated residual:** a deliberate
> mis-declaration (false-while-executing, non-blatant text) is not caught — a single auditable field, a
> far smaller surface than free-text smuggling. protocol 11/11 → **12/12**, behavioral **12/12**.
> Not claiming a universal guarantee — resolution + stated residual. Re-review optional (operator).


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

## Phase 4 — Behavioral ablation — SMOKE RUN COMPLETE (2026-07-22); superiority UNESTABLISHED

- Ran baseline / v2.8.0-general / psychology-language-only / integrated arms: 6 scenarios × 4 arms × 1
  (24 fresh isolated agents), deterministic scoring. Record:
  `plugins/epistemic-skills/skills/using-epistemic-skills/evals/epistemic-flexibility/behavioral/results/2026-07-22/RESULTS.md`.
- Result: all arms 1/6, **indistinguishable** — but the smoke's harness under-specified the trace
  schema (no `goal`/`experiment`/`failure_chain`) and all arms over-held on the clean control, so it is
  **not a valid arm comparison**. **No behavioral superiority established. No integration-specific
  clean-control regression** (over-hold is uniform across baseline and integrated).
- Real value: the smoke functioned as an adversarial test of the Phase-3 P1 fix and **caught a
  false-positive** (naive check fired on incidental execution nouns in hold-actions). Fix redesigned to
  high-precision imperatives; protocol 10/10 → **11/11**, behavioral 12/12; **held-out regression
  fixture** added (`fixtures/valid-hold-with-stop-action.json`) — this converts a real incident into a
  fixture (the Phase-5 gate item).
- Follow-up (not run): full-schema arms + ≥3 repeats for a valid superiority measurement.

## Phase 5 — Release — DECISION: DO NOT bump 3.0.0 (2026-07-22)

Release gate status:
- protocol CI green — ✅ (PR #35 all checks green, incl. DCO).
- independent gauntlet GO/CONDITIONAL with conditions closed — **CONDITIONAL** (P1 closed), but P2
  conditions (real-ledger validation, `validation_kernel` teeth) **NOT closed**.
- four-arm smoke shows no material clean-control regression — **inconclusive** (harness under-specified);
  **superiority unestablished**.
- one real incident → held-out fixture — ✅ (`valid-hold-with-stop-action.json`).
- cross-family Step-7b adjudication — **owed, not run** (`external_gate_owed: true`).

**Decision:** the evidence supports only a **protocol-conformance improvement with real control/action
teeth**, not behavioral superiority. Keep the honest-labeled work on draft PR #35; **do not release
3.0.0.** A v3 release remains a separate PR gated on: P2 conditions closed, a corrected full-schema
four-arm run, and the owed cross-family adjudication.
