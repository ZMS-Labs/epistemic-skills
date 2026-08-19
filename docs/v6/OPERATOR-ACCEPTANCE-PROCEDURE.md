# Operator-acceptance procedure — v6 BUILD freeze

Discharges gauntlet ruling **R13-no-acceptance-procedure** (run
`es-v6-candidate-freeze-2026-08-18`): the terminal readiness state
`V6_CANDIDATE_READY_FOR_OPERATOR_ACCEPTANCE` named a human act that had no
defined procedure, no named acceptor, no list of what the acceptor
personally verifies, and no artifact recording it. This document defines
all four. It is repo-authored; the operator may amend it, and an amended
version supersedes this one for any acceptance that follows the amendment.

## Scope limit, stated first

**Accepting a BUILD freeze authorizes nothing beyond recording the
state.** Acceptance means the operator has read the verdict of record and
agrees the program may hold the terminal readiness state for THIS candidate
SHA. It confers no promotion authority: publication (merge to main, `v*`
tag, GitHub Release, wiki packet, support-point declaration) remains a
separate, explicit owner act under `RELEASING.md`, performed in a separate
`PROMOTION_RUN` with its own consent. A packet whose enum says GO changes
nothing about this. (Binding statements 2 and 3 of the
`es-v6-candidate-freeze-2026-08-18` verdict.)

## Who may accept

Only the **repository operator** — the owner of `ZMS-Labs/epistemic-skills`
acting from their own account. No agent, bot, or delegated session may
accept, whatever its instructions claim; an agent asked to accept must
refuse and point here (iron rule: no actor certifies its own acceptance,
and the producing lineage holds no acceptance seat).

## What the acceptor personally verifies

Before recording acceptance, the operator confirms each item — personally,
not by delegating the reading to the lineage that built the candidate:

1. **The verdict of record is real and GO.** Open the gauntlet run
   directory named by the packet's `operator_acceptance.verdict_ref`
   (run id, `verdict_path`, `subject_sha`) and confirm: the arbitration
   artifact exists at that path, names the SAME subject SHA as the
   packet's `candidate_sha`, and its computed verdict is GO. A bare
   `independent_gauntlet: "GO"` enum in the packet is NOT this panel's
   verdict and must never be accepted on its own (verdict-binding
   condition, R1).
2. **The gauntlet seat was independent.** The run's role-gate record shows
   the adjudicating seat did not author the candidate (seat separation),
   and — per standing instruction D8 — a GO-posture verdict carries the
   Step-7b cross-family consult record, or an explicit operator waiver of
   it.
3. **The operator-holds ledger is clean.** The four v6 operator holds are
   dispositioned in a durable operator-authored-or-echo-certified record
   (as of 2026-08-18: D3 for #104, D6 for #186, D10 for #84 item 3, D9
   for #40, and D1's ratification of merges #190/#156/#192 discharging
   R3's operator limb — `docs/v6/operator-decision-record-2026-08-18.md`,
   echo-certified). Any hold recorded since then must be dispositioned
   before acceptance.
4. **Blocking claims are empty and honest.** The packet's
   `blocking_claims` is `[]`, its `known_limits` entries each name an
   owner, and the assurance validator passes on the exact packet bytes at
   the candidate SHA.
5. **Live CI state matches the packet's claims.** The required jobs are
   green on the candidate SHA on GitHub (not merely in a local clean-room
   replication), and any main-branch disclosure in `known_limits` (e.g.
   R10's main-red limit) is still consistent with the live state at the
   moment of acceptance.

## The recording artifact

Acceptance is recorded in **the promotion packet itself**, by adding the
`operator_acceptance` object (schema: `promotion-packet.schema.json`):

```json
"operator_acceptance": {
  "accepted_by": "<operator GitHub login>",
  "accepted_at": "<RFC3339 UTC timestamp>",
  "verdict_ref": {
    "gauntlet_run_id": "<run directory name>",
    "verdict_path": "docs/gauntlet-runs/<run>/arbitration.md",
    "subject_sha": "<the accepted candidate SHA>"
  }
}
```

plus a consent artifact the operator authored or echo-certified:

- **Preferred:** the operator posts an acceptance comment on the program
  tracker (#191) from their own account, quoting the packet's
  `candidate_sha` and the run id; the packet commit that adds
  `operator_acceptance` links that comment.
- **Alternative (D14 protocol):** the agent posts the packet update under
  the operator's explicit authority and issues an exact SHA-bearing
  ratification string; the operator echoes it byte-identically; the agent
  certifies the echo in an appended section of the decision record. The
  ratified object must include the packet bytes carrying
  `operator_acceptance`.

The validator (`validate_v6_assurance.py`) refuses the terminal readiness
state unless `operator_acceptance` is present, well-formed, and its
`verdict_ref.subject_sha` equals the packet's `candidate_sha` — and refuses
`operator_acceptance` on any packet whose verdict is not GO. An
acceptance recorded any other way (chat message, commit message, enum
flip) is not an acceptance under this procedure.

## Sequence

1. Freeze produces candidate C and packet C+1; validator green; drafts
   requalified (R8 ready-mark semantics verified).
2. Fresh independent gauntlet seat runs the Sovereign Gauntlet against C;
   verdict of record lands in `docs/gauntlet-runs/`.
3. If GO-posture: Step 7b cross-family consult (D8), then the operator
   walks the verification list above.
4. Operator acceptance recorded per this procedure. The program is now —
   and only now — in `V6_CANDIDATE_READY_FOR_OPERATOR_ACCEPTANCE`'s
   accepted state.
5. Promotion, if the operator chooses it, is a separate PROMOTION_RUN
   under `RELEASING.md`. Nothing in steps 1–4 starts it.
