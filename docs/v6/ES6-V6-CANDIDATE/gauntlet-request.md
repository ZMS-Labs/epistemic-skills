# Independent Gauntlet request — ES6-V6-CANDIDATE rc2

This is a request, not a verdict. The seat that produced this candidate
must not adjudicate it — and neither may the seat that adjudicated the
PREDECESSOR: that seat took the repair role under operator decision D2
(`docs/v6/operator-decision-record-2026-08-18.md`) and burned its
adjudication independence for this lineage. A **fresh seat** is required.

## Subject

- Program: ES6-V6-CANDIDATE (rc2 successor freeze)
- Tracker: epistemic-skills#191
- Candidate SHA (C): `promotion-packet.json → candidate_sha` — the freeze
  commit C+1's parent, per the C/C+1 layering in this directory's README
- Packet: `promotion-packet.json` (schema @2, verdict-bound)
- Predecessor verdicts of record (both stand as evidence; neither
  transfers to this SHA):
  1. NO-GO against `00e5146e43ff9011153452b83fedda706723c52b`
     (`docs/gauntlet-runs/es-v6-candidate-freeze-2026-08-18/arbitration.md`
     on `claude/epistemic-skills-v6-completion-nwptmc`; ruling-set@1,
     18 rulings, 15 acceptance criteria)
  2. NO-GO against `6db8c50420b194aebbd09a2ea5f81c6a276897dc`
     (`docs/gauntlet-runs/es-v6-rc2-gauntlet-kimi-2026-08-18/arbitration.md`
     on `kimi/es-v6-rc2-gauntlet-2026-08-18`; ruling-set@1, rulings
     S1–S10, 14 of 15 predecessor criteria discharged or retired)
- Review mode: **delta + blast radius by a fresh seat** (operator ruling
  2026-08-18, ledger id `v6-successor-review-delta-mode-20260818-19`; see
  KIMI-SEAT-HANDOFF.md "Review mode"). Three-panel lineage cap: two used.

## Step-0 truth gate

Premises to live-verify, never take from this file:

1. Every predecessor ruling's acceptance criterion claims discharge in this
   lineage — verify against the ruling-set's own falsifiers, not against
   this packet's self-description.
2. The operator decision record (D1–D15) is echo-certified; the ratified
   object's hash chain checks out (certification section names commit and
   sha256).
3. `origin/main` state: es#137 exposure (KL-MAIN-137) and the
   Public-content red (KL-MAIN-RED) — both decay; re-read live (PR #195
   may have merged).
4. The requalification evidence (`evidence/requalification.json`) names
   THIS candidate SHA and its run URLs resolve to real, green,
   `workflow_dispatch` runs at that SHA.
5. `blocking_claims` equals the validator's `derive_blocking` recomputation
   (CI enforces this; verify anyway).
6. The dormant/digest semantics of the public-content allowlist and the
   source-inventory digests hold on the tree you actually check out.

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
exactly: who accepts, what they personally verify, and the
`operator_acceptance` recording. BUILD-freeze acceptance authorizes
nothing beyond recording the state.

## Out of scope

Merge, tag, GitHub Release, wiki packet, ruleset changes, support-point
declaration. Those are PROMOTION, behind the operator's separate
`PROMOTION_RUN`.
