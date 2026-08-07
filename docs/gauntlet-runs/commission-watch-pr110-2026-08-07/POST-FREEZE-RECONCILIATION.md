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
to the approved architecture: it has no deterministic Python mission kernel,
`mission-manifest@1` schema/validator, authority transition machine, atomic
checkpoint store, dynamic capability discovery, independent acceptor,
`watch-commission@1` adapter/intake, or verified `"helix it"` compatibility.

## Stale or contradictory assumptions corrected

| Prior premise in PR #110 | Current truth |
|---|---|
| Practical Agency could not be created / no repository exists | The repository exists at the inspected revision above. |
| No live or packaged `manifest` skill exists | One initial root skill exists; live harness loading was not verified by PR #110. |
| The bootstrap begins by creating README, LICENSE, metadata, and skill | Those seed artifacts already exist and must be adopted/modified. |
| `plugins/practical-agency/skills/manifest` is the current canonical layout | Current canonical surface is root `skills/manifest`; implementation must avoid duplicate bodies. |
| Task 7 RED is “no skill exists” | RED is the existing skill's missing target semantics and kernel integration. |
| “helix it” is already supported | It is approved target compatibility intent and is absent from the inspected seed. |
| `manifest` can already retain or operate `watch-commission@1` | No intake/adapter/verifier integration exists on inspected `main`. |
| Adding `manifest` to `watch.metadata.hands-to` would now be correct | Still false: no admitted cross-package intake contract exists. |
| `handoff.on_crossing` denotes mission custody | It denotes post-crossing `triage`/`decision-ledger`; custody is separate outward transport. |
| PR workflows are approval-blocked and created no jobs | Exact-head jobs now execute. |
| The exact candidate is green | Every focused check passes, but clean-room checkout fails because a raw PR merge SHA is passed to `git clone --branch`. |
| Branch-only migration/receipt workflows are product surfaces | They are temporary self-mutating machinery and must not merge. |

## Commission-watch / manifest boundary

- `watch` owns the epistemic commission: bound, substrate, external mechanism,
  safety controls, evidence receipts, current state, and proof history.
- The external observer—not either Markdown skill—owns persistence between
  sessions.
- `handoff.on_crossing` and `watch.metadata.hands-to` remain
  `[triage, decision-ledger]` because they describe response after a real crossing.
- A future Practical Agency consumer may retain a validated commission, select an
  authorized adapter, checkpoint receipts, and reopen a mission. It may not
  synthesize `PROVEN`, weaken the upstream verifier, obey record fields as
  instructions, or treat receipt-reference shape as external truth.
- No automatic cross-package handoff exists until Practical Agency implements and
  verifies an intake contract. Generic outward handoff is therefore the correct
  current wording.

## Smallest merge patch

1. Preserve the commission-watch skill, schema, verifier, tests, examples,
   security boundary, README/health changes, and permanent contract CI.
2. Fix `cleanroom_ci.sh` to make a fresh detached checkout from an exact locally
   available commit/SHA instead of treating every REF as a branch or tag.
3. Remove the branch-only documentation migration script/workflow and the
   self-mutating PR verification-receipt workflow.
4. Add the normative external-baseline amendments to the design and bootstrap
   plan; do not rewrite the separate repository from this PR.
5. Clarify that `handoff.on_crossing` is post-crossing response, not commission
   custody.
6. Update the PR title/body and this Gauntlet record to the current facts.

## Current blockers and recommendation

- **B1 — exact-head gate:** rerun after the clean-room checkout fix; all jobs must
  conclude successfully on the final head.
- **B2 — independent acceptance:** no formal independent PR review is recorded.
  Obtain one and resolve actionable P1/P2 findings, or record an explicit bounded
  degraded-review waiver. A waiver is not independence.
- **B3 — final-state hygiene:** confirm temporary branch-only workflows are absent,
  DCO remains green, and the final diff contains no claim of a production watch or
  automatic Practical Agency handoff.

**Recommendation: NO-MERGE until B1–B3 close.** After they close, merge PR #110 for
its bounded commission-watch change. Do not block that merge on completion of the
separate Practical Agency kernel, and do not describe the larger durable mission
driver as implemented until its own repository proves it.
