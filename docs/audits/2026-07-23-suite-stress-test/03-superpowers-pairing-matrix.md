# 03 — Superpowers v6.1.1 pairing matrix

## Pin and precedence

This report uses Superpowers tag `v6.1.1`, commit `c984ea2e7aeffdcc865784fd6c5e3ab75da0209a`; no moving branch was consulted.

There is a superficial ordering tension that resolves at two different layers:

1. `using-superpowers` requires skill discovery before action and says process skills set the approach (`skills/using-superpowers/SKILL.md:20-33`).
2. Helix says that, **inside a paired workflow stage**, the epistemic member runs before the workflow member (`plugins/epistemic-skills/skills/helix/SKILL.md:26-33`).

Therefore the reproducible order is: discover both routers → Helix checks the stage's pair → the matched epistemic member runs → the Superpowers workflow stage executes. Example: `using-superpowers` selects brainstorming; Helix checks `blindspot-pass`; reconnaissance runs before brainstorming.

## Stage coverage

| Superpowers skill/stage | Pinned trigger/boundary | Epistemic integration in this audit | Validation |
|---|---|---|---|
| `using-superpowers` | Conversation/task entry; invoke relevant skills before action (`using-superpowers/SKILL.md:20-33`). | Paired with `using-epistemic-skills` and Helix discovery; neither router substitutes for member execution. | **SOURCE-ONLY** |
| `brainstorming` | Creative behavior/design work; design and approval before implementation (`brainstorming/SKILL.md:14-34`). | `blindspot-pass` runs before; `applying-formal-rigor` runs inside any ≥2-option choice; Gauntlet gates irreversible design approval. | **SOURCE-ONLY; applied minimally to fix choice** |
| `writing-plans` | Multi-step task with a spec, before code; tasks explicitly include RED, GREEN, commit (`writing-plans/SKILL.md:1-20,38-54`). | Consumes de-risked request/formal verdict; `write-goal` only if explicit persistent-goal intent; Gauntlet before risky plan commitments. | **DEGRADED** — audit packet itself served as authoritative plan; no separate plan document was needed for two tiny fixes. |
| `test-driven-development` | Any feature/bugfix/refactor/behavior change; failing test first (`test-driven-development/SKILL.md:1-16,18-39`). | Used for both verified defects: stale Gemini inventory and omitted deterministic CI suites. Exact RED and GREEN runs are in `08-changes-and-verification.md`. | **LIVE via GitHub Actions** |
| `systematic-debugging` | Failure diagnosis before proposing a fix. | Used on the first Gemini fix's still-red run: the exact substring assertion failed because `nine disciplines` was split by a newline; the source formatting, not the test intent, was corrected. | **LIVE/DETERMINISTIC evidence** |
| `using-git-worktrees` | Feature work needing isolation; prefer native worktree, then git fallback (`using-git-worktrees/SKILL.md:1-16,18-63`). | Native/local worktree APIs were unavailable. A non-main branch plus GitHub Actions clean checkout supplied repository isolation, but is **not reported as a worktree run**. | **DEGRADED** |
| `dispatching-parallel-agents` | Two or more independent tasks with isolated contexts and no shared state (`dispatching-parallel-agents/SKILL.md:1-16,38-48`). | Applicable to independent subject audits and required by Gauntlet/UAT role separation, but no isolated-agent primitive was available. No fake parallelism was claimed. | **NOT TESTED / capability absent** |
| `subagent-driven-development` / `executing-plans` | Execute a written plan task-by-task, with review checkpoints. | Not used: connector writes were sequential and the change set was two small, coupled regression cycles. Their review/independence benefits were unavailable. | **SKIP — trigger/capability absent** |
| `requesting-code-review` | After tasks/major features and before merge; reviewer gets focused context, not session history (`requesting-code-review/SKILL.md:14-48`). | A reviewable PR was opened, but no independent reviewer subagent was available. Human/other-agent review remains pending. | **PARTIAL** |
| `receiving-code-review` | Evaluate feedback technically before implementing it. | No reviewer feedback existed. Helix correctly maps design-claim feedback to formal rigor (`helix/SKILL.md:49-50`). | **SKIP_TRIGGER_ABSENT** |
| `verification-before-completion` | Fresh full command and output before any completion claim (`verification-before-completion/SKILL.md:18-52`). | Used through clean-checkout CI after each fix and after audit publication. Green CI is evidence for deterministic commands only, not a proxy for live harness or independent judgment. | **LIVE via GitHub Actions** |
| `finishing-a-development-branch` | Tests green, then choose merge/PR/keep/discard (`finishing-a-development-branch/SKILL.md:18-40,68-95`). | The packet pre-authorized branch + PR and forbade merge/main push; PR #43 was opened. Final Gauntlet would gate irreversible integration but is blocked. | **LIVE through PR creation; no merge** |

## Per-subject pairing map

Positions use Helix's vocabulary: `before`, `inside`, `cross-cutting`, `at approval`, `pre-merge`, or `is`.

| Subject skill | Applicable Superpowers pairings and positions | Justified non-use |
|---|---|---|
| `using-epistemic-skills` | `using-superpowers` at entry; `brainstorming` after routed reconnaissance; `writing-plans` after routed design/evidence; `verification-before-completion` on routing/contract edits. | No per-row parallel agent; router source audit did not need implementation. |
| `helix` | `using-superpowers` at entry; all listed stage checks are Helix's subject; `brainstorming` after BP, formal rigor `inside`, evidence research `cross-cutting`, Gauntlet `at approval`/`pre-merge`, UAT `is` verification for UI. | Live auto-trigger and co-fire observation unavailable. |
| `blindspot-pass` | `before brainstorming`; `before` the first `dispatching-parallel-agents`/subagent dispatch; its rewritten request feeds `writing-plans`. | No implementation inside the skill; TDD applies only to changes to its contract/tests, and none were made. |
| `applying-formal-rigor` | `inside brainstorming`; `inside systematic-debugging` when a fix rests on correctness/complexity; `inside receiving-code-review` for asserted design claims. | No dedicated worktree/parallel pair. |
| `evidence-research` | `cross-cutting` inside brainstorming, planning, debugging, review, or verification whenever a scholarly premise bears load. | No Consensus/Scite/library tools were called, so the live research workflow did not run. |
| `write-goal` | `before` persistent/long-horizon goal execution; verification consumes its proof bundle after execution. | Explicit goal-authoring intent was absent, so the skill and any goal executor were correctly skipped. |
| `outsource` | `before` external delegation; context-erasure packet precedes sending. TDD/verification apply to packet behavior and package checks. | No second delegation per subject; the one suite packet is the bounded handoff. |
| `gauntlet` | `at approval` for irreversible designs; `pre-merge`; `dispatching-parallel-agents` for isolated lenses; `requesting-code-review`/verification after computation; worktree isolation for implementation changes. | Parallel isolated role contexts were unavailable, so final panel execution stopped rather than degrading into one-context self-review. |
| `evidence-locked-uat` | `is` the UI-facing instance of verification; parallel isolated actor/verifier pipeline; TDD for deterministic judge changes. | No rendered target, so UAT itself was contraindicated; only judge self-tests ran. |
| `decision-ledger` | TDD/verification for schema and validator behavior; review before changing append/supersedes semantics. | Not a workflow stage; no brainstorming/plan pair is mandatory for merely appending a valid entry. |
| `continuity-verify` | Runs before the workflow resumes; its digest feeds routing/brainstorming. TDD/verification apply to scorer/fixture changes. | No fresh fixture behavior was changed; committed scorer results were re-executed instead. |

## Execution record for this audit

`continuity-verify → blindspot-pass → applying-formal-rigor → [evidence-research only where scholarly claims were present; live triad unavailable] → test-driven-development RED/GREEN → verification-before-completion → branch/PR → Gauntlet attempted and stopped at the isolation boundary.`

The non-use decisions are material results: no persistent goal, no rendered UAT, no parallel/subagent execution, no merge, and no claim that branch isolation equals a native worktree.
