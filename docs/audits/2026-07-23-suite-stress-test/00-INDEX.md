# Epistemic skills suite stress test — index

**Audit date:** 2026-07-23  
**Packet commit:** `532a0ce86fea908113cbca2a600fb21238e473f1`  
**Subject baseline:** `9532a57199fc8d4747a91916d59d1ea86c34d838`  
**Prior draft PR:** #43, reviewed at stable head `03c16761d67f047b0ffb8a73b9d0b09b65045127` and left intact  
**Replacement branch:** `audit/epistemic-suite-stress-test-2026-07-23-r2`  
**Replacement pull request:** [#44](https://github.com/ZMS-Labs/epistemic-skills/pull/44)  
**Package version:** 2.9.1  
**Overall status:** **PARTIAL**

## Executive result

The eleven-skill suite is materially stronger than the prior v2.6.0 baseline. The current architecture has explicit route/skip traces, shared validity receipts, continuity re-anchoring, consequential-decision persistence, deterministic Gauntlet/UAT machinery, negative-trigger discipline, authority boundaries, and repo-backed outsourcing.

Independent continuation of PR #43 verified three concrete integration defects through observed RED→GREEN cycles and retained only their minimal fixes:

1. `GEMINI.md` advertised eight packages/six disciplines instead of eleven/nine.
2. README's layout advertised ten canonical skill cores instead of eleven.
3. Canonical CI omitted continuity committed-result scoring and DCO policy unit tests.

The continuation also found and corrected publication defects in PR #43: four linked artifacts were absent, the pinned Superpowers matrix omitted `writing-skills`, packet/baseline coordinates were conflated, and target scholarly capabilities were misstated. Because PR #43's commit identities failed DCO and no rewrite authority was granted, a clean replacement was built from the immutable packet/main commit with dual author-matching sign-offs; #43 was not modified.

The 99-cell epistemic matrix reconciles exactly, all fourteen pinned Superpowers v6.1.1 skills are accounted for, all seven harness surfaces are tiered, prior v2.6.0 findings are reconciled, and the clean replacement workflow is green.

The work is **not COMPLETE**. The target exposes no auditable context-isolated exact-role invocation primitive, so the required final frozen-subject Gauntlet stopped before panel execution. No reports, arbitration, run record, or verdict were fabricated. Native proprietary-harness behavior, complete Scite/holdings evidence, rendered UAT, and population-level trigger/judgment rates also remain unproved.

## Requirement ledger

| Requirement | State | Direct evidence |
|---|---|---|
| `OUT-001` | **satisfied** | [01 — inventory and baseline](01-inventory-and-baseline.md): immutable packet, stable PR re-resolution, all eleven skills, manifests, baseline commands/results. |
| `OUT-002` | **satisfied** | [02 — epistemic pairing matrix](02-epistemic-pairing-matrix.md): 50 RUN + 4 FIXTURE + 23 absent + 22 contraindicated = 99. |
| `OUT-003` | **satisfied** | [03 — Superpowers v6.1.1 map](03-superpowers-pairing-matrix.md), pinned to `c984ea2e7aeffdcc865784fd6c5e3ab75da0209a`, all fourteen entries including `writing-skills`. |
| `OUT-004` | **satisfied as a stress-test/report obligation** | [04 — trigger and boundary results](04-trigger-and-boundary-results.md); live trigger-rate measurement remains explicitly untested. |
| `OUT-005` | **satisfied as a property-test/report obligation** | [05 — system properties](05-system-properties.md); runtime independence is OPEN and fail-closed. |
| `OUT-006` | **satisfied** | [06 — cross-harness packaging](06-cross-harness-packaging.md), seven surfaces with explicit LIVE/DETERMINISTIC/SOURCE-ONLY/NOT TESTED tiers. |
| `OUT-007` | **satisfied** | [07 — prior findings reconciliation](07-prior-findings-reconciliation.md), every relevant v2.6.0 finding classified. |
| `OUT-008` | **satisfied** | [08 — changes and verification](08-changes-and-verification.md), three exact RED→GREEN cycles and minimal replacement source commits. |
| `OUT-009` | **open** | [Fail-closed Gauntlet attempt](../../gauntlet-runs/epistemic-skills-suite-stress-test-2026-07-23/BLOCKED.md); no isolated panel and no verdict. |
| `OUT-010` | **satisfied for deterministic suites** | [09 — final verification](09-final-verification.md); PR #44 Actions run `30016659027`, job `89238304953`, success on every named step. |
| `OUT-011` | **satisfied** | Non-main branch and open draft PR #44 contain source corrections, reports 00–09, ledger, and blocked attempt; no merge/main push. |
| `OUT-012` | **satisfied by outbound relay only** | Target returns the exact `outsource-relay@1` envelope with no preamble. |

## Scoped dispositions

| Skill | Disposition | Main direct basis | Residual |
|---|---|---|---|
| `using-epistemic-skills` | **SOUND — deterministic/source** | route/skip contracts and flexibility fixtures | native auto-trigger precision |
| `helix` | **CONDITIONAL** | complete source map and reconciled Superpowers precedence | live co-fire behavior |
| `blindspot-pass` | **CONDITIONAL** | concrete skip gate and suite reconnaissance | no blinded trigger/skip battery |
| `applying-formal-rigor` | **SOUND for three audited decisions; CONDITIONAL generally** | seven-lens derivations closed by RED/GREEN | broad behavioral evaluation |
| `evidence-research` | **CONDITIONAL** | live Consensus discovery; exact Scite quota failure; source contract | reception and durable holdings incomplete |
| `write-goal` | **CONDITIONAL; current skip SOUND** | explicit-intent negative trigger and evidence-bound boundary | no live approval/goal host primitive |
| `outsource` | **SOUND for repo-backed mechanics** | immutable packet, branch/PR, relay contract, integration tests | origin must re-verify result |
| `gauntlet` | **CONDITIONAL** | deterministic machinery green; isolation contract inspected | final independent panel unavailable |
| `evidence-locked-uat` | **CONDITIONAL; current skip SOUND** | judge self-test and no-render fail-closed contract | no rendered target/role contexts |
| `decision-ledger` | **SOUND — structural/deterministic** | schema/examples plus audit ledger | completeness and truth are consumer obligations |
| `continuity-verify` | **SOUND at smoke scale** | re-anchored digest and committed scorer polarity | no real-world catch-rate measurement |

## High-load findings

### What held

- Immutable provenance was re-established before resumed work.
- Negative triggers prevented invocation count from becoming a success proxy.
- Research, goals, ledger, outsource, Gauntlet, and UAT all stopped at their own boundaries.
- Every retained source change has observed RED before GREEN.
- One canonical skills tree remains shared across harness manifests.
- DCO was not weakened; problematic history was preserved and superseded cleanly.
- No ask-first action—merge, main push, release, version/settings change, history rewrite, spend, or private-data use—occurred.

### What remains open

- Independent current Gauntlet judgment (`OUT-009`).
- Native execution/discovery in all seven harness classes.
- Scite reception and durable-library holdings/deposit.
- Rendered UAT and isolated actor/verifier contexts.
- Population validity for triggers, timing, catch rates, and judgment quality.

## Exact source verification anchors

| Defect | RED | GREEN |
|---|---|---|
| Gemini stale inventory | commit `276a18592d675346e6b5e755fa7762e94c28c4f9`, run `30010658087`; intermediate RED `30010732005` | commit `c5cc63757b2bed8576be445181f03fae031329d0`, run `30010788937` |
| CI omitted continuity/DCO suites | commit `2a28035aeb90fd6455d3497659e839da94fb7133`, run `30011093669` | commit `16e633edbc1b945a846ab5d71af7d8662d87edf6`, run `30011183031` |
| README stale layout count | commit `67a975bec8b5e263af7a4f14c92d952274939130`, run `30011818244` | commit `ccd584a50d7179024619cfff134a9962e57c486e`, run `30012138873` |

Clean replacement source commits: `a56d77fdf274a8a37e3510cd0017830172abbce8`, `20af767e8caf67475379e869d720230e08216d17`, `5dda6424f84037f5392deb9537624c2721db0c31`, and `9642ef8b705370ca6d1ceebd6e812a82744bcff4`.

## Artifact map

1. [Inventory and baseline](01-inventory-and-baseline.md)
2. [99-cell epistemic pairing matrix](02-epistemic-pairing-matrix.md)
3. [Superpowers v6.1.1 pairing](03-superpowers-pairing-matrix.md)
4. [Trigger and boundary results](04-trigger-and-boundary-results.md)
5. [System properties](05-system-properties.md)
6. [Cross-harness packaging](06-cross-harness-packaging.md)
7. [Prior v2.6.0 findings reconciliation](07-prior-findings-reconciliation.md)
8. [Changes and RED/GREEN verification](08-changes-and-verification.md)
9. [Final deterministic verification](09-final-verification.md)
10. [Decision ledger](decision-ledger.jsonl)
11. [Fail-closed final Gauntlet attempt](../../gauntlet-runs/epistemic-skills-suite-stress-test-2026-07-23/BLOCKED.md)

## Review recommendation

Review PR #44 as a **PARTIAL but evidence-backed audit and integration-hardening change** that cleanly supersedes #43 without rewriting it. Do not infer COMPLETE from green CI. The one action capable of closing the MUST gap is a freshly frozen current-head Gauntlet executed with auditable context-isolated exact-role calls and committed mechanical verification.
