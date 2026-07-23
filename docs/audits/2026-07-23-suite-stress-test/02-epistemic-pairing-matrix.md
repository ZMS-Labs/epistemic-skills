# 02 — Epistemic pairing matrix

**Packet:** `532a0ce86fea908113cbca2a600fb21238e473f1`  
**Subject baseline:** `9532a57199fc8d4747a91916d59d1ea86c34d838`  
**Subjects:** all eleven package skills  
**Evaluator columns:** the nine epistemic disciplines; Router and Helix are subjects, not evaluator disciplines.

`RUN` means the evaluator's observable trigger is present for that subject in this audit. `FIXTURE` means a current deterministic or repo-backed artifact is the correct bounded self-application. `SKIP_TRIGGER_ABSENT` means the positive trigger is absent. `SKIP_CONTRAINDICATED` means the discipline's negative trigger forbids invocation. A `RUN` cell is an applicability classification, not a claim that a proprietary-harness execution occurred. Shared suite-level work is not multiplied into eleven ceremonial invocations.

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

## Column derivations

| Column | Trigger and boundary | Rule applied to the eleven rows |
|---|---|---|
| `BP` | `blindspot-pass/SKILL.md`: unfamiliar, non-trivial territory triggers reconnaissance; the skip gate requires two concrete landmines and the canonical example from memory; the skill stops at a rewritten request. | All eleven subjects are `RUN`. The target did not hold the current tree, prior audit deltas, manifests, test surfaces, and PR history in context. One suite reconnaissance pass covered all rows. |
| `FR` | `applying-formal-rigor/SKILL.md`: two viable alternatives, correctness/comparative claims, or complexity questions trigger the seven-lens derivation; pure preference and single-option mechanical edits do not. | All eleven are `RUN` because every disposition required choosing among `SOUND`, `CONDITIONAL`, `CONTRADICTED`, or `UNTESTED` using observable properties. Shared derivations are recorded in reports 04 and 08. |
| `ER` | `evidence-research/SKILL.md`: material scholarly claims or any Consensus/Scite/library call trigger; engineering/source completion claims do not; the result is evidence, never a GO/NO-GO verdict. | `RUN` only for the evidence-research self-contract and write-goal's stated scholarly basis. A live capability probe found Consensus discovery available, Scite reception quota-exhausted, and no durable library action; therefore no complete triad conclusion is claimed. |
| `WG` | `write-goal/SKILL.md`: requires explicit goal-authoring or goal-start intent; ordinary “audit/fix this” requests are contraindicated. | All eleven are `SKIP_CONTRAINDICATED`; the packet requests immediate audit artifacts and a PR, not a persistent-goal contract. |
| `OS` | `outsource/SKILL.md`: external model/agent/process handoff produces a committed packet and pointer, not the delegated result. | The `outsource` self-row is `FIXTURE` through this exact committed packet and relay loop. The other rows lack a separate external boundary; multiplying packets would be duplication. |
| `GT` | `gauntlet/SKILL.md`: explicit gauntlet/stress-test or high-impact hard-to-verify decision triggers; low-stakes reversible work and deterministic failure triage do not. | `RUN` for Router, Helix, evidence-research, write-goal, outsource, and UAT because their contracts gate or transmit consequential action/evidence. The Gauntlet row is `FIXTURE` for its deterministic machinery; the required final suite-level panel is separately attempted and blocked at the isolation boundary. The remaining row-local source audits are below the gate. |
| `UA` | `evidence-locked-uat/SKILL.md`: only UI-facing work with a reachable rendered target; backend/docs/tests without runtime surface are contraindicated and missing preview is never replaced by source reading. | All eleven are `SKIP_CONTRAINDICATED`; this change set is Markdown, Python checks, and manifests with no rendered acceptance surface. The judge self-test is deterministic verification, not UAT. |
| `DL` | `decision-ledger/SKILL.md`: fires after a consequential decision/assumption/correction a named consumer will cite; entries never authorize or certify. | Ten rows are `RUN` because their dispositions affect review. The self-row is `FIXTURE`, backed by schema/examples plus this audit's append-only ledger. |
| `CV` | `continuity-verify/SKILL.md`: fires first on handoff/resumption when next action depends on remembered state; fresh unrelated work is excluded. | Ten rows are `RUN` because the handoff carried claims about their current state. The self-row is `FIXTURE`, backed by the committed resume battery and report 01's state digest. |

## Pairwise findings

1. Router and Helix are maps, not substitute implementations; the member skill's own trigger and boundary remain authoritative.
2. Research and verdict stay separated: evidence-research can feed Gauntlet but cannot emit a merge/product verdict.
3. Continuity precedes reconnaissance: packet/PR claims were re-anchored before unfamiliar-territory exploration.
4. Decision persistence is retrospective and cross-cutting; a ledger entry records but never validates a disposition.
5. Negative triggers are first-class evidence. The 45 non-RUN cells prevent invocation count from becoming a success proxy.
