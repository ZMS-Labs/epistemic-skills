# Successor note — Role A closeout (independent Gauntlet, issue #191)

Seat: independent Gauntlet (Role A) per `docs/v6/ES6-V6-CANDIDATE/gauntlet-request.md`.
This seat did not author, co-author, or continue #193/#194 or commits
`dc33de2`/`e8a476c`/`00e5146` (produced by a Cursor background-agent
lineage). It judged; it did not implement, merge, tag, close, or mark
anything ready.

## Verdict of record

**NO-GO against candidate SHA `00e5146e43ff9011153452b83fedda706723c52b`**
for `V6_CANDIDATE_READY_FOR_OPERATOR_ACCEPTANCE` — computed from seven
open P1 rulings (`arbitration.md`, ruling-set@1; re-derived and
hash-chain-verified by `verify_run.py`, all legs PASS). The red-lines gate
(PASS-WITH-NOTES) independently caps this record at NO-GO pending the
operator's ratify-or-reverse of the three BUILD-window merges.

Explicit refusal, as the request requires: **no implementer-authored GO
line exists or may be written into this packet.** The committed validator
accepts a self-written `independent_gauntlet: "GO"` (R1), so the packet
field cannot authenticate a verdict; THIS run directory is the verdict's
home.

## What the candidate got right (kernels to preserve)

- The es#137 custody fixes survived adversarial probing (docket H6
  killed); R15 is a residual disclosure item, not a code defect.
- `self_certification: refused` is real and validator-enforced;
  `requested_irreversible_acts` is empty; main was left untouched;
  the two-stage boundary was respected by the BUILD freeze itself.
- The claim matrix states real falsifiers on its class claims — which is
  exactly why three of them could be attacked mechanically. Keep the
  falsifiers; fix the statuses.

## The blockers, named (owners in the ruling-set acceptance criteria)

P1: R1 terminal gate forgeable · R2 secret-scan surface unclaimed/unrun ·
R3 window merges #190/#156/#192 unratified + undisclosed (**operator
only**) · R4 exact-SHA binding failure at `00e5146` (no CI of any kind
ever evaluated it; the candidate tree cannot name itself) · R5
immutability without mechanism (undisclosed post-freeze mutation; README
disclaimer deleted; `--sha` stamps an asserted literal) · R6
CLM-TRACKER-RECONCILED proved-but-false on #191's strong reading · R8 the
"until the PR is marked ready" control does not exist (`ready_for_review`
absent from every gating workflow's trigger types; only dco.yml has it).

P2: R7 (CLM-WF-PATH-COVERAGE, SPLIT), R9 clean-room under-coverage, R10
rollback premise (main head `a2b9c0d` is live-red on its own
public-content gate), R11 allowlist widening, R12 operator alert channel
drops operator-owned blockers, R13 no acceptance procedure, R14 taxonomy
substitution / no requirement register, R15 custody residual disclosure.

## Fog-free BUILD ticket

The 15 acceptance criteria in `arbitration.md`'s ruling-set block are the
ticket — each bounded, with method/threshold/timeframe and an owner.
Sequencing per the judge's next_action: the operator's R3
ratify-or-reverse decision comes first (nothing else can discharge it),
together with classification of four currently-unclassified acts (pin
tag vs `forbidden_this_run`'s "tag"; scratch-branch push;
`workflow_dispatch` at the candidate; draft-PR ready-mark). Agent-side
repairs (R1/R2/R4–R6/R8 fixes and the P2 set) are BUILD work on the
freeze lineage; every one of them edits committed artifacts and therefore
produces a NEW candidate SHA that needs full requalification — do not
patch evidence in place.

## Proposed packet-field update (for the freeze lineage / Role B — NOT
performed by this seat)

In `docs/v6/ES6-V6-CANDIDATE/promotion-packet.json` on
`cursor/v6-candidate-build-5c03`:

```
"independent_gauntlet": "NO-GO (run docs/gauntlet-runs/es-v6-candidate-freeze-2026-08-18, subject 00e5146e43ff9011153452b83fedda706723c52b, 2026-08-18)"
```

`readiness` stays `NOT_READY`; `self_certification` stays `refused`. Note
the anti-counterfeit binding: the string is a POINTER to this run's
artifacts, not the verdict itself.

## Operator items surfaced by this run (beyond the standing holds #104/#186/#84/#40)

1. **R3:** ratify or reverse merges #190, #156, #192 in a durable
   operator-authored artifact; the packet then discloses the disposition.
2. **Act classification:** the four acts listed above.
3. **Run-record scrub decision:** `evidence/dossier-challenge-2026-08-18.json`
   in this run contains 2 occurrences of the private-fleet repo name
   (quoting the candidate's allowlist diff); it is frozen under the
   dossier's evidence pin — scrub-or-allowlist is the operator's call.
   Main's head is separately red on the same pattern class (R10).
4. **Step 7b:** no cross-family adjudication ran (operator authorization
   required). If the operator wants the cross-family tripwire on this
   verdict, `scripts/consult_packet.py` builds the manual-handoff packet.

## Stop line

This seat stops here, per the two-stage boundary: no merge, no tag, no
Release, no issue/PR closure, no settings change, no ready-mark, no
readiness flip. The packet still refuses self-certification; the
remaining blockers are the named P1/P2 set, the operator holds, the
live-environment limits, and PROMOTION itself.
