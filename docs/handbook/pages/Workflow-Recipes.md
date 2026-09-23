> **Applies to:** epistemic-skills v7.0.0.

# Three worked examples

These scenarios are illustrative teaching examples, not reports of executed trials. They show what useful evidence could look like, and a repair that fits one of them may not fit your system.

## 1. A setting that disappears after reload

**Request:** “The notification setting looks saved, then resets after reload. Fix it and verify the persisted result.”

**Starting evidence:** the interface shows a success message. That message establishes feedback, not persisted state. Both a failed write and a stale read could explain the symptom.

| Step | Useful work | What it establishes |
|---|---|---|
| Bound the failure | Reproduce the save and reload on the affected revision with a disposable test account | The behavior, scope, and safe observation target |
| Investigate | Triage applies the systematic-debugging skill from [Superpowers](https://github.com/obra/superpowers), a separate open-source skills library, when it is available, or its own named standalone fallback | One investigation with explicit causal standards |
| Distinguish explanations | In this example, a direct read after save returns the old value, and the request omits the setting field | Evidence of a write-path problem rather than only stale rendering |
| Repair within authority | Correct the request mapping and check relevant neighboring settings | The scoped implementation change |
| Verify the user outcome | Save, reload, and observe the persisted value through the actual consumer | Evidence supporting the original completion criterion |

**Method contribution:** Triage supplied the causal distinction. Did It Land is useful when the repair must cross a build, deployment, or other delivery boundary; a direct local observation may already suffice. Material interaction acceptance can warrant UAT when a bounded check cannot cover it.

**Illustrative close-out:** “I used Triage with Systematic Debugging to isolate the omitted field. The repaired save and reload preserve the value; neighboring settings also passed their checks.”

**Stopping point:** the authorized repair and relevant verification are complete. No new mission, panel, or duplicate decision ledger is needed for this bounded case. If the runtime cannot be reached, the final answer must say the effect remains unverified.

## 2. A migration with a reversible-looking exit

**Request:** “We are considering a new storage service. Start by checking whether the proposed rollback really protects us.”

**Starting evidence:** the proposal contains a rollback command, but does not say what happens to writes made after migration. The user requested assessment, so analysis does not authorize the migration.

**Focused examination:** Perspective applies the reversibility method. It identifies the promised recovery point, inventories the writes and identities rollback must restore, and looks for a representative restoration result. In this example, the command restores application configuration but does not restore new records to the old store.

**Useful result:** “The rollback returns traffic, but the data recovery claim is unsupported. A tested reconciliation or restore path is needed before calling the migration reversible.” That is a bounded finding, not an overall NO-GO for every possible migration design.

**If the assignment expands:** the user may then ask whether the consequential migration should proceed, considering recoverability, cost, and operational complexity. That broader question can justify Gauntlet: freeze the proposal and evidence, obtain separate initial examinations, check findings, and adjudicate the actual tensions. Resolve may supply a missing empirical answer through a safely scoped disposable probe.

**Stopping point:** the focused question is answered, or the Gauntlet returns its scoped verdict, dissent, and coverage limits. A CONDITIONAL verdict must keep its conditions visible. No implementation follows an assessment-only grant. More lenses alone would not have created a Gauntlet review.

## 3. Resuming a change after an interrupted session

**Request:** “Continue the import repair from yesterday. The handoff says it is ready to merge.”

**Starting evidence:** the handoff links the branch, an ADR, the failing-case fixture, and a prior check result. These are useful leads. The phrase “ready to merge” does not establish current branch identity, passing current checks, or merge authority.

| Resume question | Proportionate action |
|---|---|
| What outcome and authority still apply? | Recover the user instruction and existing task record |
| What does the next step depend on? | Identify the expected branch, revision, test result, and unresolved decision |
| Are those claims current? | Decision Ledger resume mode checks the durable references and relevant live Git/check state |
| Has the subject changed? | In this example, a follow-up commit changed the parser; rerun the affected check rather than every historical investigation |
| Where is the reasoning preserved? | Reuse the adequate ADR; do not manufacture a duplicate ledger entry |
| What happens next? | Complete the authorized integration step or hold only an action whose authority remains missing |

**Illustrative close-out:** “I used Decision Ledger's resume mode to re-anchor the handoff. The parser changed after the recorded check, so I checked the current revision before continuing the authorized work.”

**Stopping point:** the requested resumed work and its verification are complete. If this were already a Manifest mission, resume through that custody contract and preserve its acceptance requirements. If an explicitly requested persistent goal is needed, Write Goal defines it and adapts only authorized activation to the available native interface.

[Find a method](Skill-Catalog.md) · [Understand the boundaries](How-the-Pieces-Fit.md) · [Inspect real project evidence](Testing-and-Evaluations.md)
