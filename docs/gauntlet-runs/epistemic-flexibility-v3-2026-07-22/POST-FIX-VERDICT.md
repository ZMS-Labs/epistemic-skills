# Post-fix verdict recomputation (bounded reinstatement, 1 round)

**Date:** 2026-07-22 · **New HEAD:** `b7d1548` (was `641ff2c`) · **Prior verdict:** NO-GO

Per gauntlet Step 7 (bounded reinstatement), the P1's factual basis was attacked by new evidence
and recomputed:

## P1 — CLOSED
Original P1: `validate_trace.py` checks trace structure but never control↔action consistency, so a
`hold`/`escalate` control with an execution-asserting `action` passes (fluent-narrative bypass).

**Refutation (deterministic, not argued):** the control/action consistency check now exists in
`validate_trace.py`. Proof:
- `fixtures/invalid-hold-but-deploys.json` (control=hold, action "proceed with … deployment … publish
  the release") → REJECTED with the control/action error.
- `fixtures/invalid-escalate-but-executes.json` (control=escalate, action "… merge the release …") →
  REJECTED.
- protocol battery 8/8 → **10/10**; behavioral **12/12** unchanged (no legitimate trace regressed);
  negation/deferral-aware + word-boundary matched (no "emergency"→"merge" false-positive).
The P1 finding no longer holds against `b7d1548`. **P1: resolved.**

## Recomputed verdict: CONDITIONAL
P1 resolved; the following **P2 conditions remain open** (tracked, not release-blocking for Phase 3,
but must be closed before a v3 GO under the Phase-5 gate):
- C4 `failure_chain` and the ledger schema are validated only against synthetic fixtures — no
  CI/hook validates a real `.ledger/entries.jsonl`.
- gauntlet's `validation_kernel` idea shipped without teeth.
- "enforced" overloading — mitigated by the new Enforcement-status section, but a full audit of every
  use across the amended SKILL.md files is a follow-up.
- Dogfooding: the integration's own design decision is not logged as a `ledger-entry@1`.

## Residuals carried to Phase 5 (release)
- `external_gate_owed: true` — a cross-family Step-7b adjudication (different model family) is owed for
  the highest-stakes release read; not run on the autonomous path.
- Behavioral superiority remains **unestablished** until Phase 4 (four-arm ablation) runs.
- A full re-panel on the settled `b7d1548` diff is available if max rigor is wanted before release;
  the P1 closure above is deterministic and does not require it.
