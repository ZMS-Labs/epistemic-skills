# Post-freeze reconciliation — PR #110 and Practical Agency

**Date:** 2026-08-07  
**Epistemic-skills subject:** PR #110  
**External baseline inspected:** `ZMS-Labs/practical-agency@e244d534a6e26bc9a352846a25ffce18b8d93a53`

This document is the authoritative current-status correction for the frozen
Gauntlet artifacts in this directory. Those reports remain preserved as review
history; statements below supersede their stale cross-repository premises and
merge conditions.

## Actual Practical Agency baseline

The separate public repository exists and its inspected `main` contains:

```text
.cursor-plugin/plugin.json
.gitignore
LICENSE
README.md
docs/mission-manifest.md
plugin.json
skills/manifest/SKILL.md
```

It publishes one initial public skill, `manifest`. The seed is prose-only relative
to the approved architecture. It has no deterministic Python mission kernel,
`mission-manifest@1` schema/validator, authority transition machine, atomic
checkpoint store, dynamic capability discovery, independent acceptor,
`watch-commission@1` adapter/intake, or verified `"helix it"` compatibility.
The current skill also declines invocation when a current manifest already
governs the task and permits closure through a steward-written completion block;
those behaviors are seed limitations, not the approved driver contract.

## Stale or contradictory assumptions corrected

| Prior premise in PR #110 | Current truth |
|---|---|
| Practical Agency could not be created / no repository exists | The repository exists at the inspected revision above. |
| No live or packaged `manifest` skill exists | One initial root skill exists; live harness loading was not verified by PR #110. |
| The implementation plan begins by creating README, LICENSE, metadata, and skill | Those artifacts already exist and must be adopted and modified in place. |
| `plugins/practical-agency/skills/manifest` is canonical | Root `skills/manifest/SKILL.md` is canonical; every harness metadata surface must point at it. |
| Task 7 RED is “no skill exists” | RED is the existing skill's missing driver modes, independent acceptance, checkpointing, compatibility intent, and kernel integration. |
| A current mission manifest means `manifest` should decline | The approved public entry must also resume, reconcile, advance, verify, and close existing missions. |
| `"helix it"` is already supported | It is approved target compatibility intent and is absent from the inspected seed. |
| `manifest` can retain or operate `watch-commission@1` | No intake, adapter, or verifier integration exists on inspected `main`. |
| Adding `manifest` to `watch.metadata.hands-to` is now correct | Still false: no admitted cross-package intake contract exists. |
| `handoff.on_crossing` denotes mission custody | It is a closed classification containing exactly `triage` and `decision-ledger`; order is non-semantic, each discipline still owns its trigger, and custody is separate outward transport. |
| Schema/verifier parity was already enforced | The frozen evidence report named a parity test that did not exist. PR #110 now contains the actual exact field/enum parity test. |
| Prose alone prevented a custody target in `handoff.on_crossing` | The schema and verifier accepted arbitrary strings, including `manifest`. PR #110 now rejects that and machine-enforces the documented boundary. |
| The raw-SHA clean-room checkout defect is still open | Closed: reconciliation run `31196648201` passed focused checks and exact-commit clean-room checkout before pushing the verified commit. |
| Temporary self-mutating workflows are product surfaces | They are absent from the reconciled PR tree and must remain absent. |

## Commission-watch / manifest boundary

- `watch` owns the epistemic commission: bound, substrate, external mechanism,
  safety controls, evidence receipts, current state, block evidence, and proof
  history.
- The external observer—not either Markdown skill—owns persistence between
  sessions.
- `handoff.on_crossing` and `watch.metadata.hands-to` are machine-closed to
  exactly `[triage, decision-ledger]` because they classify possible response
  after a real crossing. Ordering is not semantic, neither is compelled to fire,
  and neither field denotes custody.
- Optional mission-control custody is a separate outward transport concern. A
  future Practical Agency consumer may retain a validated commission, select an
  authorized adapter, checkpoint receipts, and reopen a mission. It may not
  synthesize `PROVEN`, weaken the upstream verifier, obey record fields as
  instructions, or treat receipt-reference shape as external truth.
- No automatic cross-package handoff exists until Practical Agency implements and
  verifies an intake contract. Generic outward handoff is therefore the correct
  current wording.

## Reconciliation completed in the PR

1. The commission-watch skill, schema, verifier, tests, examples, security
   boundary, README/health changes, and permanent contract CI remain intact.
2. `cleanroom_ci.sh` now supports a fresh detached checkout of an exact locally
   available commit instead of treating every ref as a branch or tag.
3. Temporary migration and verification workflows are absent from the final tree.
4. The design and implementation plan now start directly from the actual
   Practical Agency seed and preserve the root canonical skill.
5. Post-crossing response is explicitly separated from commission custody,
   and the schema/verifier reject `manifest` or arbitrary custody targets.
6. The schema/verifier field and closed-enum parity claim is backed by the actual
   executable test named in the review record.
7. The PR body and current-status review records distinguish proved
   commission-watch behavior from unimplemented Practical Agency behavior.

## Current blockers and recommendation

- **B1 — ordinary final-head gates:** branch-push verification is necessary
  evidence but does not substitute for required PR checks. The exact final-head
  branch run is recorded in the PR body; approve the ordinary PR-triggered
  workflows and require successful conclusions before merge.
- **B2 — independent acceptance:** no formal independent PR review is recorded.
  Obtain one and resolve actionable P1/P2 findings, or record an explicit bounded
  degraded-review waiver. A waiver is not independence.
- **B3 — hygiene guard:** temporary workflows are absent and the boundary text is
  truthful at the reconciled head; re-check after any later commit.

**Recommendation: NO-MERGE until B1 and B2 close and B3 remains true.** Once they
close, merge PR #110 for its bounded commission-watch change. Completion of the
separate Practical Agency kernel is not a prerequisite for this merge and must
not be implied by it.
