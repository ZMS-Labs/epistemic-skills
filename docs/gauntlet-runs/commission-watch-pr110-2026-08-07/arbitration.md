# Arbitration — commission-watch PR #110

> **Current-status notice (2026-08-07):** This is a preserved frozen review
> artifact. Its cross-repository premises and current merge conditions are
> superseded by [POST-FREEZE-RECONCILIATION.md](POST-FREEZE-RECONCILIATION.md).
> Do not use statements below that Practical Agency does not exist, that no
> `manifest` skill exists, or that workflows created no jobs as current facts.


**Judge mode:** pragmatic synthesis over a degraded manual docket  
**Subject:** frozen `review/pr110-commission-watch-candidate-v2`

## Findings admitted

| Finding | Severity | Disposition |
|---|---:|---|
| External receipt truth is not established by shape validation | P3 / coverage | accepted; explicitly documented and assigned to trusted resolvers |
| Time/condition freshness is consumer-owned | P3 | accepted; monitor during Practical Agency implementation |
| Identifier guards are not a universal security scanner | P3 / coverage | accepted; security boundary requires allowlisted resolvers and data-only handling |
| Schema and semantic verifier could have drifted | P2 | resolved by exact parity test |
| Receipt refs could have been overread as authenticated facts | P2 | resolved by contract README and security boundary |
| GitHub PR workflows are `action_required` with zero jobs | P2 process | open external condition; cannot be called green |
| Practical Agency and `manifest` are not implemented | P2 program scope | open by explicit exclusion; blocks the larger program claim, not the commission-watch contract claim |
| Raw carrier would be too ceremonial for ordinary users | P3 future usability | assigned to compact Practical Agency status/adapters |
| Independent panel execution is degraded | P2 review integrity | open until a separate reviewer returns or the operator explicitly accepts the bounded degraded review |

## Conflict ledger

### Conflict 1 — Is the commission-watch implementation itself ready?

- **State-machine adversary:** yes, with residual downstream limits; no open P1/P2
  transition defect found.
- **Evidence-integrity lens:** artifact logic is strong, but exact candidate CI has
  not executed in GitHub because the runs are approval-blocked.
- **Usability/boundary lens:** the commission-watch boundary is coherent and
  appropriately scoped.

**Ruling:** the implementation is a credible merge candidate, not yet a verified
merge-ready candidate. Green source-level reasoning cannot replace the withheld
jobs.

### Conflict 2 — Does this PR satisfy the operator's request for a driver?

- **Usability lens:** the architecture recovers the correct one-command design.
- **Evidence lens:** only design and plans exist for Practical Agency.
- **State-machine lens:** the external watch contract can be consumed later but
  supplies no mission runtime itself.

**Ruling:** no. The PR resolves commission-watch and creates a durable Practical
Agency specification and execution plan. It does not make `manifest` operational.
The PR description and final report must preserve that distinction.

### Conflict 3 — Can the manual Gauntlet certify itself?

- The same ChatGPT session authored much of the change and performed the manual
  lens analysis.
- The lenses were separated in method and synthesized after a barrier, but they
  were not independent context-isolated actors.
- GitHub Copilot review was requested as a separate reviewer and was not present
  at dossier freeze.

**Ruling:** no self-certification. The manual docket can expose and resolve
findings, but independent acceptance remains an external condition.

## Computed verdict rule

```text
open P1                          -> NO-GO
no open P1, any open P2          -> CONDITIONAL
no open P1/P2 and gates complete -> GO
```

Open P2 conditions remain. Therefore the computed verdict is:

# CONDITIONAL

## Conditions to reach GO for merging PR #110

1. **C1 — Exact candidate execution.** Approve or otherwise execute the trusted
   PR workflows against the exact final head. Required jobs must be created and
   conclude successfully; `action_required` with zero jobs is not sufficient.
2. **C2 — Separate review.** Obtain a genuine independent PR review—GitHub
   Copilot, another model/session with repository access, or a human reviewer—and
   address every actionable P1/P2 finding. The operator may explicitly accept a
   bounded degraded-review waiver, but the record must call it a waiver rather
   than independence.
3. **C3 — Scope-honest PR text.** The PR must state that no production observer,
   Practical Agency repository, or live `manifest` skill exists in this change.
4. **C4 — DCO and repository gates.** Every final commit must retain an
   author-matching sign-off and the repository's inventory, JSON, sentinel,
   description-budget, public-content, and phantom-reference checks must remain
   green.

## Conditions for the larger Practical Agency program

These are not conditions for the commission-watch code to merge, but they are
required before saying the operator's one-command driver exists:

- create the separate `practical-agency` repository;
- implement and package its sole public `manifest` skill;
- validate mission state, authority, checkpoint, capability, and execution
  receipts;
- integrate `watch-commission@1` without weakening upstream semantics;
- prove at least one clean-install harness flow;
- demonstrate interruption/resumption without silent intent drift; and
- obtain independent acceptance of a completed mission flow.

## Bounded reinstatement

No rejected P1/P2 finding was reinstated. The schema-parity and receipt-truth
findings were resolved in the candidate before arbitration. Residual P3 limits
remain visible and must not be silently upgraded by future adapters.
