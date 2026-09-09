> **Applies to:** epistemic-skills v7.0.0
>
> **Canonical source:** [released skill tree](https://github.com/ZMS-Labs/epistemic-skills/tree/v6.0.0/plugins/epistemic-skills/skills)

# Choosing a Skill

Choose from an observed trigger, not from the size of the task or a desire to be thorough. The default is ordinary work; additional process is justified only when it can expose an error that could change the action or completion claim.

## Start with this decision

| What you can observe | Next step |
|---|---|
| All four routine conditions hold | Use the bounded ordinary workflow; no special record. |
| Approach uncertain; claim about to bear load; contradiction; resume from summary | Invoke `metacognate`; silence is success when the routine gate clears. |
| State of a running system wanted, or health claim about to bear load | `health` |
| Specific thing broken/degraded; cause not established | `triage` |
| Change believed applied and something depends on it | `did-it-land` |
| Bound must be noticed unattended, or watcher must be proven | `watch` |
| Remembered summary/handoff controls the next action | `decision-ledger` resume mode |
| Request conflicts with territory, hides coupling, or risks fan-out | `recon` (brief) |
| Large foggy effort / backlog encodes unmade decisions | `recon` (initiative) |
| External project overlaps your own; adopt/replace/ignore | `recon` (candidate) |
| Material design/property claim needs a derivation | `resolve` (derivation) |
| Claim depends on research or a scholarly tool call | `resolve` (literature) |
| Live question cheaper to answer with a disposable build | `resolve` (probe) |
| Explicit persistent goal authoring | `write-goal` |
| Work crosses to an external model, agent, or process | `outsource` |
| One-way-door or high-blast-radius decision | `gauntlet` |
| Material UI-facing completion claim needs independent proof | `evidence-locked-uat` |
| Consequential decision/assumption/recurrent correction lacks durable record | `decision-ledger` |
| Operator asks for exhaustive interview, or irreversible fork with operator present | `open-questions` |
| Explicit audit / cross-layer instruction conflict / model-generation upgrade | `context-audit` |

If more than one positive trigger exists, each member's own description governs firing; `metacognate` names the unanswerable condition when the approach itself is the question. There is no inventory-holding router in v5.0.0.

## Pairing with a workflow layer

When a workflow-skill layer also runs, `metacognate` decides pairing at the moment it is needed. Historical [Helix](Helix-Central-Passage) is not a live seat.

## Keep the negative path real

The routine path is not a lesser result. It is the correct result when the four conditions hold after the two-read micro-recon, and it stays silent. [Routine Work and Proportionality](Routine-Work-and-Proportionality) defines the gate; [Skill Catalog](Skill-Catalog) provides the individual reference guides.

## Canonical references

- [`metacognate` at v5.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/plugins/epistemic-skills/skills/metacognate/SKILL.md)
- [Routine fast path at v5.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/plugins/epistemic-skills/skills/metacognate/reference/routine-fast-path.md)
- [Generated ROUTING.md at v6.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v6.0.0/plugins/epistemic-skills/ROUTING.md)
