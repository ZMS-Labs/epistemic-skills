# Independent Gauntlet request — ES6-V6-CANDIDATE rc4

This is a request, not a verdict. The seat that produced this candidate
must not adjudicate it — and neither may any prior adjudicating seat of
this lineage: the original adjudicator took the repair role under operator
decision D2 (`docs/v6/operator-decision-record-2026-08-18.md`), and the
rc2 (kimi) and rc3 (delta-review) panels are prior adjudicators. A
**fresh seat** is required.

## Subject

- Program: ES6-V6-CANDIDATE (rc4 repair freeze)
- Tracker: epistemic-skills#191
- Candidate SHA (C): `promotion-packet.json → candidate_sha` — the freeze
  commit C+1's parent, per the C/C+1 layering in this directory's README
  (C's own tree carries no packet directory; R3-NF7)
- Packet: `promotion-packet.json` (schema @2, verdict-bound)
- Predecessor verdicts of record (all three stand as evidence; none
  transfers to this SHA):
  1. NO-GO against `00e5146e43ff9011153452b83fedda706723c52b`
     (`docs/gauntlet-runs/es-v6-candidate-freeze-2026-08-18/arbitration.md`
     on `claude/epistemic-skills-v6-completion-nwptmc`; ruling-set@1,
     18 rulings, 15 acceptance criteria)
  2. NO-GO against `6db8c50420b194aebbd09a2ea5f81c6a276897dc` (rc2)
     (`docs/gauntlet-runs/es-v6-rc2-gauntlet-kimi-2026-08-18/arbitration.md`
     on `kimi/es-v6-rc2-gauntlet-2026-08-18`; ruling-set@1, rulings
     S1–S10)
  3. NO-GO against `16b80ac6ada24a663e39b38ab06e8f2614d247f4` (rc3)
     (`docs/gauntlet-runs/es-v6-rc3-delta-review-2026-08-18/arbitration.md`
     on `claude/es-v6-rc3-delta-review`; all ten S-rulings CLOSED; new
     findings R3-NF1 (P1) and R3-NF2..NF8, whose repairs are THIS
     candidate's delta)
- Review mode: **delta + blast radius by a fresh seat** under two recorded
  operator rulings (ledger ids `v6-successor-review-delta-mode-20260818-19`
  and `v6-lineage-panel-cap-extension-20260819-21`): the three-panel
  lineage cap, EXHAUSTED at the rc3 verdict, is extended by EXACTLY ONE
  panel scoped to this repair. See SUCCESSOR-SEAT-HANDOFF.md.

## Step-0 truth gate

Premises to live-verify, never take from this file:

1. The rc3 arbitration's findings each claim repair in this lineage —
   verify against that arbitration's own letter (its "Next action" items
   and per-finding text), not this packet's self-description.
2. The two 2026-08-19 operator rulings exist in `.ledger/entries.jsonl`
   (entries 20 and 21) and the ledger extends live `origin/main`'s bytes
   as an exact prefix — run `check_ledger_append_only.py --base-git-ref`
   against a fresh fetch yourself.
3. The operator decision record (D1–D15) is echo-certified; the ratified
   object's hash chain checks out.
4. `origin/main` state: the packet's dated facts (#195 merged 2026-08-18
   as `03b7724`; KL-MAIN-137 custody exposure) — re-read live.
5. The requalification evidence (`evidence/requalification.json`) names
   THIS candidate SHA and its run URLs resolve to real, green (at
   gating-job level), `workflow_dispatch` runs at that SHA — including
   the ledger append-only step EXECUTED in the stdlib-checks run.
6. `blocking_claims` equals the validator's `derive_blocking`
   recomputation (CI enforces this; verify anyway).
7. The digest/dormant semantics of the public-content allowlist and the
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
- Your verdict SPENDS the one-panel cap extension (ledger entry 21).

## After a GO verdict

Operator acceptance follows `docs/v6/OPERATOR-ACCEPTANCE-PROCEDURE.md`
exactly: who accepts, what they personally verify, and the
`operator_acceptance` recording. BUILD-freeze acceptance authorizes
nothing beyond recording the state.

## Out of scope

Merge, tag, GitHub Release, wiki packet, ruleset changes, support-point
declaration. Those are PROMOTION, behind the operator's separate
`PROMOTION_RUN`.
