# 02 — Epistemic pairing matrix

**Subject:** all eleven package skills at `9532a57199fc8d4747a91916d59d1ea86c34d838`  
**Evaluator columns:** the nine epistemic disciplines; Router and Helix are subjects, not evaluator disciplines.  
**Classification semantics:** `RUN` means the evaluator's trigger is present for that subject in this audit; `FIXTURE` means a current deterministic or repo-backed artifact is the appropriate self-application; `SKIP_TRIGGER_ABSENT` means the trigger is observably absent; `SKIP_CONTRAINDICATED` means the skill's own negative trigger forbids the run.

A `RUN` cell is an applicability decision, not a claim that a live proprietary-harness run occurred. Shared suite-level passes are not multiplied into eleven ceremonial invocations.

## 99-cell matrix

| Subject skill | BP | FR | ER | WG | OS | GT | UA | DL | CV |
|---|---|---|---|---|---|---|---|---|---|
| `using-epistemic-skills` | `RUN` | `RUN` | `SKIP_TRIGGER_ABSENT` | `SKIP_CONTRAINDICATED` | `SKIP_TRIGGER_ABSENT` | `RUN` | `SKIP_CONTRAINDICATED` | `RUN` | `RUN` |
| `helix` | `RUN` | `RUN` | `SKIP_TRIGGER_ABSENT` | `SKIP_CONTRAINDICATED` | `SKIP_TRIGGER_ABSENT` | `RUN` | `SKIP_CONTRAINDICATED` | `RUN` | `RUN` |
| `blindspot-pass` | `RUN` | `RUN` | `SKIP_TRIGGER_ABSENT` | `SKIP_CONTRAINDICATED` | `SKIP_TRIGGER_ABSENT` | `SKIP_TRIGGER_ABSENT` | `SKIP_CONTRAINDICATED` | `RUN` | `RUN` |
| `applying-formal-rigor` | `RUN` | `RUN` | `SKIP_TRIGGER_ABSENT` | `SKIP_CONTRAINDICATED` | `SKIP_TRIGGER_ABSENT` | `SKIP_TRIGGER_ABSENT` | `SKIP_CONTRAINDICATED` | `RUN` | `RUN` |
| `evidence-research` | `RUN` | `RUN` | `RUN` | `SKIP_CONTRAINDICATED` | `SKIP_TRIGGER_ABSENT` | `RUN` | `SKIP_CONTRAINDICATED` | `RUN` | `RUN` |
| `write-goal` | `RUN` | `RUN` | `RUN` | `SKIP_CONTRAINDICATED` | `SKIP_TRIGGER_ABSENT` | `RUN` | `SKIP_CONTRAINDICATED` | `RUN` | `RUN` |
| `outsource` | `RUN` | `RUN` | `SKIP_TRIGGER_ABSENT` | `SKIP_CONTRAINDICATED` | `FIXTURE` | `RUN` | `SKIP_CONTRAINDICATED` | `RUN` | `RUN` |
| `gauntlet` | `RUN` | `RUN` | `SKIP_TRIGGER_ABSENT` | `SKIP_CONTRAINDICATED` | `SKIP_TRIGGER_ABSENT` | `FIXTURE` | `SKIP_CONTRAINDICATED` | `RUN` | `RUN` |
| `evidence-locked-uat` | `RUN` | `RUN` | `SKIP_TRIGGER_ABSENT` | `SKIP_CONTRAINDICATED` | `SKIP_TRIGGER_ABSENT` | `RUN` | `SKIP_CONTRAINDICATED` | `RUN` | `RUN` |
| `decision-ledger` | `RUN` | `RUN` | `SKIP_TRIGGER_ABSENT` | `SKIP_CONTRAINDICATED` | `SKIP_TRIGGER_ABSENT` | `SKIP_TRIGGER_ABSENT` | `SKIP_CONTRAINDICATED` | `FIXTURE` | `RUN` |
| `continuity-verify` | `RUN` | `RUN` | `SKIP_TRIGGER_ABSENT` | `SKIP_CONTRAINDICATED` | `SKIP_TRIGGER_ABSENT` | `SKIP_TRIGGER_ABSENT` | `SKIP_CONTRAINDICATED` | `RUN` | `FIXTURE` |

## Reconciliation

| Classification | Count |
|---|---:|
| `RUN` | 50 |
| `FIXTURE` | 4 |
| `SKIP_TRIGGER_ABSENT` | 23 |
| `SKIP_CONTRAINDICATED` | 22 |
| **Total** | **99** |

## Column derivations and citations

| Column | Trigger/boundary used | Cell rule in this audit |
|---|---|---|
| `BP` | Unfamiliar, non-trivial territory triggers reconnaissance; skip only when two concrete landmines and the canonical example can be named from memory; the skill ends at a rewritten request, not edits (`plugins/epistemic-skills/skills/blindspot-pass/SKILL.md:44-70`). | All eleven subjects are `RUN`: this external context did not hold the full current tree, references, prior audit, and packaging surfaces from memory. One suite reconnaissance pass covered the rows. |
| `FR` | Any non-trivial decision with at least two viable options or a correctness/complexity claim triggers a seven-lens derivation; pure preference and single-option mechanical edits do not (`plugins/epistemic-skills/skills/applying-formal-rigor/SKILL.md:18-25,42-70`). | All eleven are `RUN`: every row required a four-way applicability classification and a sound/conditional/contradicted/untested disposition, which are alternatives distinguished by observable properties. |
| `ER` | Scholarly claims or any Consensus/Scite/library call trigger; general web/source inspection and engineering completion claims do not; the output is evidence, never a verdict (`plugins/epistemic-skills/skills/evidence-research/SKILL.md:36-59,61-90`). | `RUN` only for `evidence-research` self-consistency and `write-goal`'s stated research basis. Other rows make package/source claims, not scholarly claims, so they are `SKIP_TRIGGER_ABSENT`. Live triad execution was unavailable and is not claimed. |
| `WG` | Requires explicit goal-authoring or goal-start intent and may not execute or certify the goal (`plugins/epistemic-skills/skills/write-goal/SKILL.md:19-36`). | All rows are `SKIP_CONTRAINDICATED`: the packet requests an audit and PR, not creation of a persistent goal. |
| `OS` | Fires at an external model/agent/process boundary and produces the committed packet plus pointer, not the delegated result (`plugins/epistemic-skills/skills/outsource/SKILL.md:17-28,50-84`). | The `outsource` row is `FIXTURE`: this exact handoff and relay are its repo-backed self-application. Per-subject re-outsourcing is absent and would duplicate the one bounded workload, so the other ten are `SKIP_TRIGGER_ABSENT`. |
| `GT` | Fires for explicit gauntlet/stress-test requests and high-impact, hard-to-verify decisions; excludes reversible low-stakes work and deterministic failure triage (`plugins/epistemic-skills/skills/gauntlet/SKILL.md:43-65`). | `RUN` for the router, Helix, evidence-research, write-goal, outsource, and UAT because their contracts gate or transmit consequential action/evidence. `FIXTURE` for the Gauntlet self-row via its deterministic suite and frozen-run exemplar. Recon, formal-rigor, ledger, and continuity source audits are `SKIP_TRIGGER_ABSENT` at row scope; the final suite-level Gauntlet remains separately required and blocked, documented in the linked run attempt. |
| `UA` | Only UI-facing work with a reachable rendered surface; backend/docs/non-runtime changes are excluded, and no preview means `BLOCKED_ENVIRONMENT` rather than code-reading substitution (`plugins/epistemic-skills/skills/evidence-locked-uat/SKILL.md:16-26`). | All rows are `SKIP_CONTRAINDICATED`: this repository change is Markdown, Python checks, and manifests with no user-facing rendered acceptance surface. The deterministic judge self-test is verification, not UAT. |
| `DL` | Fires after consequential decisions/assumptions/corrections that future work will cite; entries never authorize and readers re-anchor (`plugins/epistemic-skills/skills/decision-ledger/SKILL.md:32-57,121-139`). | Ten rows are `RUN` because their dispositions are consequential inputs to merge review. The self-row is `FIXTURE`, backed by schema/examples plus this audit's append-only decision ledger. |
| `CV` | Fires first on a handoff/resumption and re-anchors every load-bearing remembered claim to durable state; fresh tasks are excluded (`plugins/epistemic-skills/skills/continuity-verify/SKILL.md:38-49,50-101,113-131`). | Ten rows are `RUN` because the packet carried claims about their current state. The self-row is `FIXTURE`, backed by the committed resume battery and the state digest in `01-inventory-and-baseline.md`. |

## Pairwise observations

1. **Router/Helix are maps, not substitute implementations.** Their self-application is evaluated through routing and co-fire records, while each selected member's own contract remains authoritative (`using-epistemic-skills/SKILL.md:10-16`; `helix/SKILL.md:19-24`).
2. **Evidence and verdict remain separated.** `evidence-research` can feed Gauntlet but cannot emit GO/NO-GO; the matrix therefore permits `ER→GT` without collapsing their boundaries.
3. **Continuity precedes reconnaissance.** The handoff was re-anchored first; blindspot reconnaissance then inspected unfamiliar current territory (`using-epistemic-skills/SKILL.md:98-111,138-150`).
4. **Decision persistence is retrospective.** Ledger applicability follows each consequential disposition; it is not an arc stage and it does not certify those dispositions.
5. **Negative triggers are first-class evidence.** Twenty-two UAT/write-goal contraindications and twenty-three absent-trigger skips prevent the matrix from becoming an invocation-count proxy.
