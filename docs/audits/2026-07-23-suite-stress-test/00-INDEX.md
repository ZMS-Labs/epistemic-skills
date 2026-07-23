# Epistemic skills suite stress test — index

**Audit date:** 2026-07-23  
**Packet/base commit:** `9532a57199fc8d4747a91916d59d1ea86c34d838`  
**Package version:** `2.9.1`  
**Branch:** `audit/epistemic-suite-stress-test-2026-07-23`  
**Pull request:** `https://github.com/ZMS-Labs/epistemic-skills/pull/43`  
**Overall status:** **PARTIAL**

## Executive verdict

The eleven-skill suite is materially stronger than the prior v2.6.0 baseline: shared receipts, continuity verification, decision persistence, deterministic Gauntlet/UAT machinery, negative-trigger discipline, and repo-backed outsourcing are present and internally coherent. Three concrete integration defects were found and fixed through observed RED→GREEN cycles:

1. `GEMINI.md` advertised a stale eight/six inventory instead of eleven/nine.
2. README layout advertised ten canonical skill cores instead of eleven.
3. Canonical CI omitted deterministic continuity committed-result scoring and DCO policy unit tests.

The expanded clean-checkout workflow is green. The 99-cell epistemic matrix reconciles exactly. All seven requested harness surfaces were audited with explicit validation tiers. The v2.6.0 findings were reconciled.

The work is **not COMPLETE** because the target had no context-isolated role-agent primitive, so the required final frozen-subject Gauntlet stopped before panel execution. Native proprietary-harness discovery, live scholarly triad behavior, and rendered UAT were also unavailable. These are named capability/evidence gaps, not silently converted into passes.

## Requirement ledger

| Requirement | State | Primary evidence |
|---|---|---|
| `OUT-001` | `satisfied` | [01 — inventory and baseline](01-inventory-and-baseline.md) |
| `OUT-002` | `satisfied` | [02 — 99-cell epistemic pairing matrix](02-epistemic-pairing-matrix.md): 50 `RUN` + 4 `FIXTURE` + 23 absent-trigger + 22 contraindicated = 99 |
| `OUT-003` | `satisfied` | [03 — Superpowers v6.1.1 pairing](03-superpowers-pairing-matrix.md), pinned to `c984ea2e7aeffdcc865784fd6c5e3ab75da0209a` |
| `OUT-004` | `satisfied` as an audit/report obligation | [04 — trigger and boundary results](04-trigger-and-boundary-results.md); live trigger rates remain explicitly untested |
| `OUT-005` | `satisfied` as a system-property test/report obligation | [05 — system properties](05-system-properties.md); independence is OPEN and fail-closed |
| `OUT-006` | `satisfied` | [06 — cross-harness packaging](06-cross-harness-packaging.md), all seven surfaces tiered |
| `OUT-007` | `satisfied` | [07 — prior findings reconciliation](07-prior-findings-reconciliation.md) |
| `OUT-008` | `satisfied` | [08 — changes and verification](08-changes-and-verification.md), three observed RED→GREEN cycles |
| `OUT-009` | `open` | [Gauntlet blocked-attempt record](../../gauntlet-runs/epistemic-skills-suite-stress-test-2026-07-23/BLOCKED.md); no isolated lens contexts, no verdict |
| `OUT-010` | `satisfied` for deterministic suites | [09 — final verification](09-final-verification.md); expanded clean-checkout workflow green |
| `OUT-011` | `satisfied` | non-main branch and open reviewable PR #43; no merge/main push |
| `OUT-012` | `satisfied by outbound relay` | target returns only `outsource-relay@1` envelope |

## Skill dispositions

These are scoped dispositions, not universal efficacy claims.

| Skill | Disposition | Direct basis | Main residual |
|---|---|---|---|
| `using-epistemic-skills` | **SOUND — deterministic/source** | routing/skip contracts and protocol/behavioral fixtures green | native auto-trigger precision |
| `helix` | **CONDITIONAL** | complete source pairing map; precedence reconciled with Superpowers | live co-fire behavior |
| `blindspot-pass` | **CONDITIONAL** | crisp positive/negative gate and boundary; applied to suite reconnaissance | no blinded trigger/skip battery |
| `applying-formal-rigor` | **CONDITIONAL overall; SOUND for audited decisions** | seven-lens derivations selected minimal fixes; empirical closure by CI | broad behavioral evaluation |
| `evidence-research` | **CONDITIONAL** | triad/convergence/boundary source contract | no live Consensus/Scite/library run |
| `write-goal` | **CONDITIONAL; current skip SOUND** | explicit-intent negative trigger and host-adapter boundary | no live consent/persistent-goal primitive |
| `outsource` | **SOUND for repo-backed handoff mechanics** | exact packet, branch, PR, relay, integration tests | origin must still re-verify returned work |
| `gauntlet` | **CONDITIONAL** | deterministic selector/verifier/finalizer/arbitrator tests green | current final panel impossible without isolated contexts |
| `evidence-locked-uat` | **CONDITIONAL; current skip SOUND** | deterministic judge green; no-render fail-closed contract | no rendered environment or actor/verifier contexts |
| `decision-ledger` | **SOUND — structural/deterministic** | schema/examples validator and audit ledger | completeness and truth remain human/consumer obligations |
| `continuity-verify` | **SOUND at smoke scale** | scorer replay: skilled gates pass, baselines/parody retain expected polarity | no real-world rate measurement |

## High-load findings

### What held

- **Provenance discipline:** packet claims were re-anchored to immutable files, GitHub state, and clean-checkout runs before bearing load.
- **Negative triggers:** 45 matrix cells are explicit skips/contraindications, preventing invocation count from becoming a success proxy.
- **Boundary integrity:** research does not emit verdicts; goals do not execute; ledger entries do not authorize; outsource does not certify results; UAT cannot be replaced by source reading.
- **Test-first correction:** every source/integration defect has an observed failing run before its passing fix.
- **One canonical tree:** all harness packaging reuses the same skill cores; adapter counts are now regression-guarded.
- **Authority:** no merge, release, version bump, settings change, external spend, or main push occurred.

### What remains open

- **Independent adversarial judgment:** no valid final Gauntlet panel was run.
- **Live harness behavior:** Claude Code, Codex, Cursor, Gemini CLI, Antigravity, Kimi Code, and a generic loader were not executed natively.
- **Live scholarly evidence flow:** connector schemas/reception/holdings were not exercised.
- **Rendered acceptance:** no UI target existed.
- **Population validity:** fixture batteries are smoke/calibration evidence, not real-world rates.

## Changes and exact verification anchors

| Defect | RED evidence | GREEN evidence |
|---|---|---|
| Gemini stale inventory | commit `276a18592d675346e6b5e755fa7762e94c28c4f9`, run `30010658087`; first fix still red at run `30010732005` | commit `c5cc63757b2bed8576be445181f03fae031329d0`, run `30010788937` |
| CI omitted continuity/DCO suites | commit `2a28035aeb90fd6455d3497659e839da94fb7133`, run `30011093669` | commit `16e633edbc1b945a846ab5d71af7d8662d87edf6`, run `30011183031` |
| README stale layout count | commit `67a975bec8b5e263af7a4f14c92d952274939130`, run `30011818244` | commit `ccd584a50d7179024619cfff134a9962e57c486e`, run `30012138873` |

Latest green source-fix workflow URL recorded in the report set: `https://github.com/ZMS-Labs/epistemic-skills/actions/runs/30012138873`. The outbound relay carries the final publication-head run after all audit artifacts are committed.

## Artifact map

1. [Inventory and baseline](01-inventory-and-baseline.md)
2. [Epistemic pairing matrix](02-epistemic-pairing-matrix.md)
3. [Superpowers v6.1.1 pairing matrix](03-superpowers-pairing-matrix.md)
4. [Trigger and boundary results](04-trigger-and-boundary-results.md)
5. [System properties](05-system-properties.md)
6. [Cross-harness packaging](06-cross-harness-packaging.md)
7. [Prior findings reconciliation](07-prior-findings-reconciliation.md)
8. [Changes and verification](08-changes-and-verification.md)
9. [Final verification](09-final-verification.md)
10. [Decision ledger](decision-ledger.jsonl)
11. [Fail-closed final Gauntlet attempt](../../gauntlet-runs/epistemic-skills-suite-stress-test-2026-07-23/BLOCKED.md)

## Review recommendation

Review the PR as a **PARTIAL but evidence-backed audit and integration-hardening change**. Do not merge on the basis of deterministic CI alone if the packet's COMPLETE bar is required. The smallest next step that can change status is to freeze the audit subject at the chosen PR revision and execute the current Gauntlet with auditable context-isolated exact-role calls, then verify and commit the complete run record.
