# Step-0 dossier challenge — 2026-08-18 (isolated read-only challenger seat)

Method: re-executed the dossier's load-bearing claims read-only against the
three worktrees (subject at C, freeze at C+1, run record), the predecessor
ruling-set, and live gh api reads. No mutations; all worktrees left clean.

## Defects (all accepted and amended pre-dispatch)

- **D-1 MATERIAL** — the dossier's "ready-mark drill transcript not located"
  unknown was mislabeled. Transcript exists at
  `docs/v6/evidence/r8-ready-mark-drill-2026-08-18.md` (both C and C+1;
  cited by the matrix R8 claim closure_path). Challenger live-verified:
  throwaway PR #196 (CLOSED unmerged, head 564a1e53); six runs at the
  identical head SHA, event=pull_request, conclusions != skipped — R8's
  falsifier threshold MET. Seat re-spot-checked run 32184104218
  (epistemic-flexibility, pull_request, head 564a1e53, conclusion failure —
  still satisfies "!= skipped": the drill proves the takeover MECHANISM).
  Minor packet note: the transcript's READY table transposes the
  custody/commission-watch run IDs (32184104140 is commission-watch,
  32184104186 is mission-custody per live API); substance intact.
- **D-2 MATERIAL** — truth-gate premise 1 was asserted but not documented for
  roughly half the ruling-set. Challenger spot checks: R1 fields present
  (@2 schema, independent_gauntlet_ref); R3 limb 2 satisfied via
  CLM-MERGE-190/156/192 rows citing D1; R6 discharged via path (a)
  (CLM-DISPOSITION-CENSUS; generator fails closed on undispositioned items —
  v6_generate_candidate_packet.py:792-802); R15 limbs present
  (KL-GUARD-LEXICAL + CLM-MC-GUARD-LEXICAL LIMITED). Named partials:
  **R5(c)** — KL-RESTAMP omits the two specifically-required elements
  (clean-baseline.json post-freeze addition; deleted disclaimer substance);
  **R11(d)** — one dormant allowlist entry remains. (Seat's later read:
  owner+cadence ARE recorded at check_public_content.py:67-69 and four inert
  entries were retired; the residual dormant entry names a file absent from
  this branch by construction and is digest-bound — downgraded to
  PARTIAL-minor in the discharge table.)
- **D-3 MINOR** — live-verification transcript elided 13 packet-dir files
  from a quoted diff without marking the elision. Annotated.
- **D-4 MINOR** — clean-room fraction discrepancy: packet KL-DRAFT-CI "52 of
  53" vs seat's measured 51-of-54. Flagged under FC-4.
- **D-5 MINOR** — PINS registry also guards v4.0.0; load-bearing claim
  (rc2 pins unregistered) unchanged. Footnoted.

## Claims that survived attack (independently re-verified by the challenger)

C/C+1 layering and identity; all five requalification runs (dispatch event,
head_sha == C, per-job conclusions, planted-secret positive control);
blocking_claims derivation (as labeled, probe-based); main state /
KL-MAIN-RED retirement (PR #195 merged 22:03:42Z as 03b7724; push runs
green; es#137 OPEN, fix commits not ancestors of main); ODR hash
verification (with the lineage nuance: d7c4178 is not an ancestor of C — the
file was copied into this lineage with the certification section appended,
decisions text untouched); allowlist digest semantics (37 exact files
digest-verified, 1 dormant); **FC-1 strongly** (validator failure reproduced
on pristine C+1; 158 = 141 + 17 .pyc; generator tree-model root cause
confirmed; .pyc volatility limb confirmed; no plausible alternate cause);
crib arithmetic; R7/R8 repairs; pin-tag peels; the evidence-root pin
(recomputed, matches the dossier header). No circular sourcing found:
every load-bearing claim traces to a live API read, an independent hash, or
a re-execution.

## Overall assessment

Fit after named amendments (all applied pre-dispatch). No defect threatened
the evidentiary core; FC-1 reproduces exactly with the stated mechanism.
