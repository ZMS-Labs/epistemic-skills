> **Historical page.** `helix` is not a live skill. Use **`metacognate (Tier 2 pairing judgment)`**. Deleted in v5.0.0; pair tables cannot hand control back.
>
> Body text below is retained for method vocabulary and migration; where it conflicts with a tagged `v5.0.0` contract, the tagged source controls.

# Helix: Central Passage

Helix is the sole guide to the central passage between a workflow-skill layer and the epistemic-skills collection. Workflow skills organize how work proceeds; epistemic skills define what counts as knowing the target, decision, evidence, or acceptance is sound. Helix pairs those strands around the task without merging them or replacing either router.

## What it does

Helix maps a positive epistemic trigger to the workflow stage that consumes it and specifies the position: before, inside, at approval, pre-merge, cross-cutting, or identical to the workflow gate for that surface. Once a pair fires, the epistemic member runs first and the workflow stage carries its result forward.

Helix does not route within either collection. `using-superpowers` or the equivalent workflow router remains authoritative for workflow; `using-epistemic-skills` remains authoritative for epistemic member selection and ordering. The paired member's full contract—not this map—governs the discipline.

## Use it when

- Both a workflow-skill layer and epistemic-skills are available, the task failed the routine fast path, and a workflow stage has a positive epistemic pairing trigger.
- Work crosses to an external model, agent, or process.
- Sequencing between the workflow and epistemic layers is ambiguous.
- A standalone epistemic output exists and you need to identify the workflow stage that will consume it.

## Do not use it when

- Work is reversible, local, directly checkable, and non-precedential; it exits through ordinary workflow and a bounded check.
- Only one collection is active.
- Both collections are installed but no positive member trigger exists.
- You want to enumerate absent pairs, emit skip records, or invent a twelfth discipline.
- You want Helix to soften, re-implement, or replace the paired member's trigger and output contract.

## Inputs and prerequisites

Apply the router's routine fast path first. For unfamiliar routine-looking work, read the target artifact and nearest test/example. Unfamiliarity alone is not a positive pair.

Inputs to pairing are the current workflow stage, the positive trigger established by the authoritative member skill, the member output reference, and any operator-authorized override. Cross-cutting claim/source separation, priority/proxy separation, preregistration, recurrent-failure chains, and closure control operate inside the member that consumes them; they do not create new pairing rows.

## Normal workflow

1. Exit routine work before Helix. Emit no pairing record for this path.
2. Let the epistemic router and member contracts establish positive triggers.
3. Use the pairing map to place the member:

| Workflow stage and positive condition | Epistemic pair | Position |
|---|---|---|
| Task start after micro-recon exposes a material map/territory mismatch, hidden coupling, or costly fan-out risk | Blindspot Pass | before brainstorming |
| Brainstorming a material multi-option design | Applying Formal Rigor | inside the decision point |
| Any stage where a premise rests on scholarly research or a scholarly connector call | Evidence Research | cross-cutting at the premise |
| Design approval or writing plans when Gauntlet's own trigger fires | Gauntlet | after the committed design, at approval, before plan writing |
| Explicit persistent/long-horizon goal authoring | Write Goal | before persistent execution |
| First material parallel/subagent dispatch when a wrong premise could multiply | Blindspot Pass | before first dispatch |
| External model, agent, or process handoff | Outsource | before sending |
| Clean TDD or implementation with no member trigger | none mandatory | no pair and no record |
| Systematic debugging whose fix rests on a correctness or complexity claim | Applying Formal Rigor | inside the claim |
| Material UI-facing verification | Evidence-Locked UAT | the stage is the discipline |
| Finishing a branch when Gauntlet's own pre-merge trigger fires | Gauntlet | after merge/push choice, before execution |
| Code-review feedback asserting a material design alternative or formal claim | Applying Formal Rigor | inside review handling |

4. Run and read the epistemic member before the workflow stage consumes it. Recon after design and evidence after verdict are invalid orderings.
5. For a fired pair, emit `helix-check: <stage> → <pair> → fired(<artifact-ref>)`. For an explicit authorized override, emit `helix-check: <stage> → <pair> → overridden(<authority-ref>: <bounded reason>)`.
6. Map stage names when the workflow layer is not Superpowers. Preserve semantics rather than inventing skip records.

Decision Ledger is not a map row because it fires retrospectively when a consequential uncovered decision, assumption, or recurrent correction occurs. Continuity Verify is pre-arc and runs before routing resumed work. Both still compose with workflow at their defined boundaries.

## Outputs and durable artifacts

A positive co-fire produces the member's own artifact plus one compact `helix-check` carrying stage-order custody. Helix does not duplicate the member output.

Routine work, `(none mandatory)` rows, absent triggers, and standalone single-layer routing are record-free at the Helix layer. Fire-nothing is a valid outcome: zero pairs, zero ceremony, zero proof that nothing fired.

## Boundaries and failure modes

- Running the workflow stage first and attaching its epistemic pair later turns recon into archaeology and evidence into rationalization.
- A pairing map entry never substitutes for reading the member skill.
- A local bounded dispatch with an explicit target and check does not need a report merely because another agent exists.
- External handoff is not ready until Outsource has a committed, pushed, target-readable packet at an immutable commit.
- Routine UI presentation changes use bounded direct verification, not a full UAT container.
- Missing load-bearing evidence closes as hold, escalation, or reversible probe; it cannot be upgraded by more explanation.
- An output no workflow stage consumes is a report no one reads; identify the consumer or stop.

## Example prompts

- “We are brainstorming a durable cache protocol and must choose between two consistency models. Pair the decision discipline inside brainstorming and preserve the derived record as its input.”
- “This label-spacing change is local, reversible, and snapshot-covered. Let it exit before Helix and emit no pairing line.”
- “Prepare to send this workload to an external model. Run the repo-backed handoff discipline before sending and record the fired pair with the immutable packet reference.”
- “The bug fix claims the new path is amortized O(1). Pause systematic debugging at that claim, derive it, then resume the workflow.”

## Related skills and handoffs

- [Using Epistemic Skills](Skill-Using-Epistemic-Skills) is the member router and routine-gate authority.
- [Blindspot Pass](Skill-Blindspot-Pass), [Applying Formal Rigor](Skill-Applying-Formal-Rigor), [Evidence Research](Skill-Evidence-Research), [Write Goal](Skill-Write-Goal), [Outsource](Skill-Outsource), [Gauntlet](Skill-Gauntlet), and [Evidence-Locked UAT](Skill-Evidence-Locked-UAT) are paired members.
- [Continuity Verify](Skill-Continuity-Verify) precedes the arc on resumption; [Decision Ledger](Skill-Decision-Ledger) persists consequential uncovered moments retrospectively.
- [Routine Work and Proportionality](Routine-Work-and-Proportionality) explains why installation does not imply invocation.

## Canonical sources and evidence

- [Helix source at v3.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/plugins/epistemic-skills/skills/helix/SKILL.md)
- [Router source at v3.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/plugins/epistemic-skills/skills/using-epistemic-skills/SKILL.md)
- [Routine fast path at v3.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/plugins/epistemic-skills/skills/using-epistemic-skills/reference/routine-fast-path.md)
- [Trust-contract carriers at v3.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/plugins/epistemic-skills/contracts/README.md)
