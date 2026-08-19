# Independent Gauntlet request — ES6-V6-CANDIDATE rc5

This is a request, not a verdict. The seat that produced this candidate
must not adjudicate it — and neither may any prior adjudicating seat of
this lineage: the original adjudicator took the repair role under operator
decision D2, and the rc2 (kimi), rc3 and rc4 panels are prior
adjudicators. A **fresh seat** is required.

## Subject

- Program: ES6-V6-CANDIDATE (rc5 re-cut)
- Tracker: epistemic-skills#191
- Candidate SHA (C): `promotion-packet.json → candidate_sha` — the freeze
  commit C+1's parent, per the C/C+1 layering in this directory's README
  (C's own tree carries no packet directory; R3-NF7)
- Packet: `promotion-packet.json` (schema @2, verdict-bound)
- Predecessor verdicts of record (all four stand as evidence; none
  transfers to this SHA):
  1. NO-GO against `00e5146e43ff9011153452b83fedda706723c52b`
     (`docs/gauntlet-runs/es-v6-candidate-freeze-2026-08-18/arbitration.md`
     on `claude/epistemic-skills-v6-completion-nwptmc`)
  2. NO-GO against `6db8c50420b194aebbd09a2ea5f81c6a276897dc` (rc2)
     (`docs/gauntlet-runs/es-v6-rc2-gauntlet-kimi-2026-08-18/arbitration.md`
     on `kimi/es-v6-rc2-gauntlet-2026-08-18`; S1–S10, all closed at rc4)
  3. NO-GO against `16b80ac6ada24a663e39b38ab06e8f2614d247f4` (rc3)
     (`docs/gauntlet-runs/es-v6-rc3-delta-review-2026-08-18/arbitration.md`
     on `claude/es-v6-rc3-delta-review`; R3-NF1..NF8, all closed at rc4)
  4. NO-GO against `7408a462b413d0ab41a08de1d37a10b9cdf2a6ea` (rc4)
     (`docs/gauntlet-runs/es-v6-rc4-delta-review-2026-08-19/arbitration.md`
     on `claude/es-v6-rc4-delta-review`; R4-NF1 (P1) + eight P4 — the
     subject of THIS candidate's delta)
- Review mode: **NARROW**, under recorded operator ruling D19 (ledger
  `v6-lineage-panel-cap-extension-two-20260819-23`). See
  SUCCESSOR-SEAT-HANDOFF.md "Review mode". Your verdict spends the second
  and final cap extension.

## Step-0 truth gate

Premises to live-verify, never take from this file:

1. R4-NF1's repair: run the shipped `check_dco.py` logic over PR #197's
   LIVE commit list — it must return zero unsigned commits — and confirm
   the attestation list is closed, full-40-hex, and prefix-safe.
2. The rc4 panel's eight P4 findings each claim a disposition here; verify
   against that arbitration's own letters, not this packet's summary.
3. **KL-SEAL-MAIN-COUPLING**: build the freeze PR's merge ref (candidate
   merged with current `origin/main`) and run the validator against it.
   Exit 0 is required. This is the check whose absence superseded rc4.
4. The ledger extends live `origin/main`'s bytes as an exact prefix
   (`check_ledger_append_only.py --base-git-ref` against a fresh fetch),
   and entries 22/23 record rulings D18/D19.
5. The requalification evidence names THIS candidate SHA; its runs resolve
   to real green (at gating-job level) `workflow_dispatch` runs at that
   SHA, with the ledger append-only step and the record-path narrowness
   control EXECUTED rather than skipped.
6. `blocking_claims` equals the validator's `derive_blocking`
   recomputation; every matrix owner is inside the closed vocabulary.
7. The digest/dormant semantics of the public-content allowlist, the
   anchored secret-scan exemption, and the source-inventory digests hold
   on the tree you actually check out.

## Required outputs

- GO / CONDITIONAL / NO-GO against **this exact SHA**
- P1/P2 release blockers named, if any
- Explicit refusal of any implementer-authored GO line in this packet
- **At GO posture:** run Step 7b (cross-family manual-handoff consult)
  BEFORE recording the verdict — standing operator instruction D8. The
  verdict must be recorded as an on-disk arbitration artifact naming this
  SHA; the packet's enum is bound to it via `independent_gauntlet_ref`
  (a bare enum flip fails `validate_v6_assurance.py`).

## After a GO verdict

Operator acceptance follows `docs/v6/OPERATOR-ACCEPTANCE-PROCEDURE.md`
exactly. BUILD-freeze acceptance authorizes nothing beyond recording the
state.

## Out of scope

Merge, tag, GitHub Release, wiki packet, ruleset changes, support-point
declaration. Those are PROMOTION, behind the operator's separate
`PROMOTION_RUN`.
