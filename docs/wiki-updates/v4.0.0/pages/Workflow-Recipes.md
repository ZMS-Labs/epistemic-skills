> **Applies to:** epistemic-skills v4.0.0
>
> **Canonical sources:** [router](https://github.com/ZMS-Labs/epistemic-skills/blob/v4.0.0/plugins/epistemic-skills/skills/using-epistemic-skills/SKILL.md), [routine path](https://github.com/ZMS-Labs/epistemic-skills/blob/v4.0.0/plugins/epistemic-skills/skills/using-epistemic-skills/reference/routine-fast-path.md), and [Helix](https://github.com/ZMS-Labs/epistemic-skills/blob/v4.0.0/plugins/epistemic-skills/skills/helix/SKILL.md)

# Workflow Recipes

These are task-shaped paths, not extra contracts. Start with the routine test; a discipline fires only on its released positive trigger. The canonical `SKILL.md` controls whenever this handbook summary differs from it.

## Central passage: workflow ↔ Helix ↔ epistemic disciplines

When a workflow-skill layer and this collection operate together, **Helix is the central passage**. It does not replace either router: the workflow router chooses how to carry out work, while `using-epistemic-skills` applies the routine gate and routes epistemic disciplines. For a positive pair, run the epistemic member first, then let the workflow stage consume its output. Record only a fired or authorized-overridden pair; routine work and absent pairs are silent.

`workflow skills  <->  Helix central passage  <->  epistemic router and disciplines`

See [Helix: Central Passage](Helix-Central-Passage) for the complete pairing map.

## Reversible local edit

- **Entry decision:** The work is reversible, local, directly checkable, and non-precedential.
- **Sequence:** Open the target artifact and nearest test or example; if both agree with the request, make the edit and run its bounded check.
- **Handoffs:** None. Do not create router, Helix, blindspot, formal-rigor, ledger, or UAT artifacts.
- **Stop condition:** The targeted check establishes the requested local behavior.
- **Routine alternative:** This is the routine path itself. Escalate only if the two reads expose a positive trigger.

## Unfamiliar task: two-read micro-recon exposes coupling

- **Entry decision:** A task initially looks routine, but the target plus nearest test/example exposes material hidden coupling, a map/territory mismatch, fuzzy scope, or fan-out risk.
- **Sequence:** Run `recon` (brief mode, the blindspot pass) read-only; use its rewritten request, context, landmines, and open questions before design or dispatch.
- **Handoffs:** Feed the rewritten request to the workflow design/planning stage; if the result creates a material multi-option decision, hand that decision to `resolve` (derivation instrument).
- **Stop condition:** Recon has reduced the uncertainty enough to take the next bounded action or has named the remaining blocker.
- **Routine alternative:** Mere unfamiliarity is not enough; if the two reads agree and the routine test still passes, edit and bounded-check without a full pass.

## Consequential design decision

- **Entry decision:** There are multiple viable software or systems alternatives with different measurable, correctness, safety, consistency, isolation, or complexity properties, or formal rigor is explicitly requested.
- **Sequence:** Run `resolve` (derivation instrument, the applying-formal-rigor method); keep a focused question inline (six bullets/250 visible words), or produce the appropriate revision-bound `formal-rigor-record@2` for standard/high-assurance work.
- **Handoffs:** If a premise is scholarly, run the literature instrument before it bears load. The derivation becomes input to planning, implementation, review, or Gauntlet as appropriate.
- **Stop condition:** The decision is derived at the required tier with a stated boundary, or evidence requires hold, escalation, or a reversible probe.
- **Routine alternative:** Do not formalize a pure preference, one-answer mechanical edit, or low-cost reversible choice.

## Research-backed design premise

- **Entry decision:** A claim or decision needs verifiable scholarly evidence, or a Consensus, Scite, or Zotero/library tool call is about to occur.
- **Sequence:** Run `resolve` (literature instrument, the evidence-research method): negotiate the live capabilities of all three layers, then check Zotero/equivalent holdings before rediscovery. Use Consensus for discovery, Scite for reception and retraction checks, and cross-validate the matrix across the engines and library. Only after selection, verification, and deduplication, deposit the final matrix papers into the durable library.
- **Handoffs:** Pass qualified evidence into the consuming discipline, usually the derivation instrument; distinguish evidence limits from the resulting engineering judgment.
- **Stop condition:** The premise is supported, qualified, refuted, or explicitly limited with provenance.
- **Routine alternative:** A general web search, completed engineering-work claim, or one already-trusted internal lookup does not invoke this discipline.

## Persistent goal contract

- **Entry decision:** The operator explicitly asks to create, define, refine, or start a goal, asks what counts as done, or needs a durable completion contract.
- **Sequence:** Run `write-goal` to select the goal type and agree direct proof, anti-proxy/provenance guards, scope, blockers, interruption, stop rule, and any opt-in budget.
- **Handoffs:** Begin persistent execution only after the approved contract. A consequential uncovered decision made during execution may later enter `decision-ledger`.
- **Stop condition:** The goal contract is approved; this skill neither executes nor certifies it.
- **Routine alternative:** Ordinary task execution or a long task alone is not goal-authoring intent.

## High-stakes design or pre-merge gate

- **Entry decision:** An architecture/design approval, irreversible infrastructure or security change, high-blast-radius one-way door, or hard-to-verify high-stakes claim reaches a Gauntlet trigger.
- **Sequence:** Freeze an establishable subject and run `gauntlet`: truth-gated dossier, falsifiers, isolated role-bound lenses, and independent arbitration with mechanical evidence checks.
- **Handoffs:** At design approval, use its computed result before plan writing. At pre-merge, select merge/push+PR first, then gate before execution. Preserve the Conflict Ledger and run record.
- **Stop condition:** Computed `GO`, `CONDITIONAL`, or `NO-GO` reaches the subject boundary; unresolved evidence remains visible rather than becoming a pass.
- **Routine alternative:** Ordinary code review, deterministic test triage, lookups, and reversible low-stakes work do not call Gauntlet.

## Material UI acceptance

- **Entry decision:** A stateful, interaction-sensitive, accessibility-sensitive, persistent, or otherwise hard-to-observe UI-facing change is about to be claimed done.
- **Sequence:** Run `evidence-locked-uat`: actor evidence, a separate blinded verifier, and a deterministic judge.
- **Handoffs:** Use the verdict as the completion gate; repair or investigate an `INCONCLUSIVE` result rather than rounding it to PASS.
- **Stop condition:** A supported verdict and evidence packet meet the acceptance boundary; `INCONCLUSIVE` is never PASS.
- **Routine alternative:** A reversible/local/directly-checkable presentation change uses its bounded preview or test, not a material UAT packet.

## Resumed work from a summary

- **Entry decision:** A compaction summary, handoff note, or prior-session state claim is load-bearing for the next action.
- **Sequence:** Run `decision-ledger`'s resume mode (continuity-verify) first; re-anchor each load-bearing claim to durable evidence and emit its state digest (quick mode for trivial resumptions).
- **Handoffs:** Route the re-anchored task normally. If the state cannot be established, stop at the uncertainty boundary.
- **Stop condition:** The next action rests on verified anchors or an explicit unresolved-state result.
- **Routine alternative:** Fresh work with no remembered-state dependency does not fire continuity verification.

## Consequential decision persistence

- **Entry decision:** A consequential decision, load-bearing assumption, or recurrent correction has just occurred and later work will rely on it.
- **Sequence:** Check first for a durable ADR, plan, issue, PR, goal, or derivation that already records it with resolvable provenance and revisit conditions. If none suffices, run `decision-ledger` and append `ledger-entry@1`.
- **Handoffs:** Future readers re-anchor to the ledger/artifact; it is not a verdict and does not replace the consumer's verification.
- **Stop condition:** An adequate durable carrier exists exactly once.
- **Routine alternative:** Do not log reversible choices, routine work, verdicts, ledger consumption, or duplicate durable records.

## Durable external model handoff

- **Entry decision:** Work is crossing to a different model, agent, or external process, or the operator asks for a durable handoff/copy-paste prompt.
- **Sequence:** Run `outsource` before sending. Create the context-complete `docs/outsource/<work-id>/HANDOFF.md`, commit it at an exact GitHub ref, publish/verify the target-readable packet, then send only the short pointer.
- **Handoffs:** Record every external response in the repository before it bears load; the origin re-verifies returned claims.
- **Stop condition:** The immutable packet is target-readable and the pointer is accurate; without that, return `BLOCKED`.
- **Routine alternative:** Same-harness subagent work is not this skill unless the operator requests a durable GitHub handoff.

## Workflow plus epistemic operation through Helix

- **Entry decision:** A workflow layer and epistemic-skills are both present, the task did not clear routine work, and a workflow stage has a positive member trigger (or ordering is ambiguous).
- **Sequence:** Apply routine first; ask the routers/member contract which discipline fires; use Helix to place it before, inside, at approval, pre-merge, cross-cutting, or as the acceptance stage. The epistemic member runs first.
- **Handoffs:** Emit `helix-check: <stage> → <pair> → fired(<artifact-ref>)` only for a co-fire; the member output is the workflow input.
- **Stop condition:** The paired workflow stage consumes the member output, or the member closes as hold/escalation/reversible probe.
- **Routine alternative:** A routine task, absent pair, or `(none mandatory)` row emits no Helix inventory or skip record.

## Canonical sources

- [Released routine fast path](https://github.com/ZMS-Labs/epistemic-skills/blob/v4.0.0/plugins/epistemic-skills/skills/using-epistemic-skills/reference/routine-fast-path.md)
- [Released Helix pairing map](https://github.com/ZMS-Labs/epistemic-skills/blob/v4.0.0/plugins/epistemic-skills/skills/helix/SKILL.md)
- [Released skill tree](https://github.com/ZMS-Labs/epistemic-skills/tree/v4.0.0/plugins/epistemic-skills/skills)
