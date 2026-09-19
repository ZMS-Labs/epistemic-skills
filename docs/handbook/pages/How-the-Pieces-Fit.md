> **Applies to:** epistemic-skills v7.0.0.

# Different questions need different methods

The suite is organized around decisions an agent must make, not around a compulsory workflow. A method returns its result to the task owner, who continues the authorized work. The map below shows relationships, not a required sequence.

![Method families: frame the question, examine a decision, verify an outcome, and carry work forward. Choose the method for the question; these are not mandatory stages.](https://raw.githubusercontent.com/ZMS-Labs/epistemic-skills/main/docs/assets/method-map.svg)

*The diagram is a current editorial documentation asset. [The catalog](Skill-Catalog.md) provides the full text equivalent and links to every method.*

### Reflection, a lens, or a panel?

| Method | Distinct responsibility | Example |
|---|---|---|
| **Metacognate** | Examine the reasoning, assumptions, and meaning of success | “Does this benchmark represent the user experience?” |
| **Perspective** | Apply a useful lens to a bounded concern | “What makes this migration reversible?” |
| **Gauntlet** | Compare separate examinations and adjudicate material tensions | “Should this consequential migration proceed under these conditions?” |

Perspective can adapt or use several lenses. Gauntlet adds a shared subject, plural scrutiny, evidence checking, and adjudication. Counting lenses does not create that distinction.

### State, cause, effect, or continuity of observation?

| Method | What it establishes | What it cannot establish alone |
|---|---|---|
| **Health** | Current state within declared bounds | Cause or successful delivery of a particular change |
| **Triage** | Cause or narrowed explanations for a known failure | A completed repair |
| **Did It Land** | Intended effect at the consumer | Every user acceptance criterion or indefinite persistence |
| **Watch** | Commissioned external observation and alert delivery | Health inferred from silence or authority to remediate |
| **Evidence-Locked UAT** | Material acceptance against specified observations | Unobserved interactions or calibrated reliability |

### A record, a mission, or a goal?

**Decision Ledger** makes consequential reasoning recoverable and rechecks prior claims. It should reuse adequate ADRs or task records. **Manifest** is a heavier opt-in custody contract with receipted effects and distinct-actor acceptance. **Write Goal** defines the completion contract and adapts authorized activation to a native goal or loop. **Outsource** packages a task so a remote target can work without the conversation.

A project can need one of these without needing the others. Native goals do not automatically create missions; a durable ADR does not automatically activate an executor.

See [Design rationale](Design-Rationale.md) for the tradeoffs and [worked examples](Workflow-Recipes.md) for concrete combinations.
