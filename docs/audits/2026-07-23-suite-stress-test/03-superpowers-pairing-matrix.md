# 03 — Superpowers v6.1.1 pairing matrix

## Pin, inventory, and precedence

This report uses Superpowers tag `v6.1.1`, commit
`c984ea2e7aeffdcc865784fd6c5e3ab75da0209a`; no moving branch was substituted. The complete pinned skill set relevant to the packet contains fourteen entries:

`using-superpowers`, `brainstorming`, `writing-plans`, `test-driven-development`, `systematic-debugging`, `using-git-worktrees`, `dispatching-parallel-agents`, `subagent-driven-development`, `executing-plans`, `requesting-code-review`, `receiving-code-review`, `verification-before-completion`, `finishing-a-development-branch`, and `writing-skills`.

The earlier PR #43 matrix omitted `writing-skills`; this replacement corrects the inventory rather than treating a 13-row table as complete.

There is no real conflict between the two routers:

1. `using-superpowers` requires relevant skill discovery before action and gives process skills priority.
2. Helix says that **inside a matched workflow stage**, the epistemic member runs before the workflow member.

The reproducible order is therefore: discover both routers → Helix checks the stage pair → the matched epistemic discipline runs → the Superpowers workflow stage executes. Example: `using-superpowers` selects brainstorming; Helix checks `blindspot-pass`; reconnaissance precedes brainstorming.

## Complete stage coverage

| Superpowers skill | Pinned trigger/boundary | Epistemic integration in this audit | Validation / justified non-use |
|---|---|---|---|
| `using-superpowers` | At task/conversation entry; invoke applicable process skills before action. | Paired with the epistemic router and Helix discovery; neither router substitutes for the selected member. | **SOURCE-ONLY composition;** the packet itself required the methods. |
| `brainstorming` | Creative design work; explore alternatives and obtain design approval before implementation. | `blindspot-pass` runs before; formal rigor runs inside any two-option correctness/design choice; Gauntlet gates irreversible approval. | **DEGRADED.** No broad redesign was needed; three narrow corrections were derived rather than creatively expanded. |
| `writing-plans` | Multi-step implementation from a spec; tasks include explicit verification and RED/GREEN sequencing. | Consumes the de-risked request and formal/evidence decisions. `write-goal` remains separate and only fires on explicit persistent-goal intent. | **DEGRADED.** The packet was the authoritative plan; reports 01–09 are the execution ledger. |
| `test-driven-development` | Any behavior-changing feature, bugfix, or refactor; observe failure before production correction. | Applied to the stale Gemini inventory, omitted CI suites, and stale README core count. | **LIVE via GitHub Actions.** Exact RED and GREEN commits/runs are in report 08. |
| `systematic-debugging` | Diagnose a failing test from evidence before proposing another fix. | Applied when the first Gemini correction remained red because `nine disciplines` crossed a line break; the test was not weakened. | **LIVE deterministic evidence:** intermediate red run `30010732005`, then focused correction. |
| `using-git-worktrees` | Isolated feature work; native worktree first, then documented fallback. | Repository isolation was required, but no local worktree primitive was exposed. A branch based on the immutable packet plus GitHub Actions clean checkout supplied isolation. | **DEGRADED;** not claimed as a native worktree run. |
| `dispatching-parallel-agents` | Two or more independent tasks with isolated contexts and no shared mutable state. | Applicable to independent subject reviews and mandatory for Gauntlet/UAT role separation. | **NOT TESTED / capability absent.** No isolated-agent dispatch primitive was available; role labels in one context were rejected. |
| `subagent-driven-development` | Execute plan tasks with fresh subagents and review checkpoints. | Could have split independent reports, but the target lacks subagent contexts. | **SKIP_CAPABILITY_ABSENT;** no fake subagent execution. |
| `executing-plans` | Execute a written plan task-by-task with evidence and checkpoints. | The packet and audit index define tasks; connector writes were sequential and independently checked. | **DEGRADED.** Method shape followed, but no dedicated executing-plans runtime was present. |
| `requesting-code-review` | After implementation/major work and before merge, provide focused context to an independent reviewer. | A reviewable superseding PR is the handoff to an independent reviewer. | **PARTIAL.** PR review surface exists; no independent reviewer subagent was available in this target. |
| `receiving-code-review` | Evaluate review feedback technically before changing code. | Formal rigor would evaluate any correctness/design claim in feedback. | **SKIP_TRIGGER_ABSENT.** No review feedback existed during execution. |
| `verification-before-completion` | Run fresh full commands and inspect results before making completion claims. | Clean-checkout CI is used after source corrections and after publication; passing commands are not rounded into live-harness or independence proof. | **LIVE via Actions;** final state in report 09. |
| `finishing-a-development-branch` | With tests green, choose PR/merge/keep/discard according to authority. | Packet authorizes branch + PR and forbids merge/main push. Final Gauntlet would gate integration, but cannot run independently here. | **LIVE through clean branch/PR; no merge.** |
| `writing-skills` | Creating, editing, or verifying skills; process-documentation TDD requires no-guidance controls, fresh contexts, repeated pressure scenarios, and loophole closure. | The audit verifies skill contracts, but does not alter any `SKILL.md` semantics. Source/integration defects were tested with ordinary TDD. | **SKIP_TRIGGER_ABSENT for skill editing; capability absent for fresh-context pressure batteries.** The omission from PR #43's matrix was corrected here. |

## Per-subject pairings

Positions use Helix vocabulary: `before`, `inside`, `cross-cutting`, `at approval`, `pre-merge`, or `is`.

| Subject skill | Applicable Superpowers pairings and positions | Material non-use |
|---|---|---|
| `using-epistemic-skills` | `using-superpowers` at entry; brainstorming after routed reconnaissance; planning after design/evidence; verification for routing/contract changes. | No core router behavior changed; no pressure-scenario skill edit. |
| `helix` | `using-superpowers` at entry; all workflow stage checks are its subject; BP `before`, formal rigor `inside`, research `cross-cutting`, Gauntlet `at approval`/`pre-merge`, UAT `is` UI verification. | Live auto-trigger/co-fire telemetry unavailable. |
| `blindspot-pass` | `before brainstorming`; before first parallel/subagent fan-out; rewritten request feeds planning. | No implementation inside recon; no SKILL.md edit. |
| `applying-formal-rigor` | `inside brainstorming`; inside debugging and received review when a fix rests on correctness/comparative claims. | No dedicated parallel/worktree pairing. |
| `evidence-research` | `cross-cutting` in brainstorming, planning, debugging, review, or verification when a scholarly premise bears load. | Only capability/discovery probing occurred; Scite reception and holdings were not completed. |
| `write-goal` | Before long-horizon/persistent goal execution; later verification consumes its proof bundle. | Explicit goal-authoring intent absent. |
| `outsource` | Before external delegation; packet publication precedes sending; TDD/verification cover packet/package behavior. | One suite packet is the bounded handoff; no per-subject re-outsourcing. |
| `gauntlet` | At irreversible approval and pre-merge; parallel isolated agents for lens reports; review/verification after computation; worktree isolation for implementation changes. | Final panel stopped because isolated exact-role contexts were unavailable. |
| `evidence-locked-uat` | `is` UI-facing verification; parallel isolated actor/verifier; TDD for deterministic judge behavior. | No rendered target, so UAT is contraindicated. |
| `decision-ledger` | TDD/verification for schema/validator behavior; review before append/supersedes semantics changes. | Not a workflow stage; appending a valid entry does not require brainstorming. |
| `continuity-verify` | Runs before resumed workflow; digest feeds routing/brainstorming; TDD/verification apply to scorer/fixture changes. | No resume-fixture semantics changed; committed results were replayed. |

## Execution trace

`continuity-verify → blindspot-pass → applying-formal-rigor → evidence-research only for material scholarly/capability claims → TDD RED/GREEN → systematic debugging where RED persisted → verification-before-completion → clean non-main branch/PR → final Gauntlet attempted and stopped at the isolation boundary.`

Non-use is part of the result: no persistent goal, no rendered UAT, no isolated agents, no native worktree, no SKILL.md behavior edit requiring `writing-skills`, and no merge.
