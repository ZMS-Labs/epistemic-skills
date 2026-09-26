> **Applies to:** epistemic-skills v7.2.0.

# Different questions need different methods

Each method answers a different question an agent runs into. A method hands its result back to whoever owns the task, and they carry on with the work they were asked to do. The map groups the methods by the kind of question they answer.

<picture>
  <source media="(max-width: 600px)" srcset="https://raw.githubusercontent.com/ZMS-Labs/epistemic-skills/main/docs/assets/method-map-mobile.svg">
  <img src="https://raw.githubusercontent.com/ZMS-Labs/epistemic-skills/main/docs/assets/method-map.svg" alt="Method map in four groups. Frame the question: Metacognate, Recon, Resolve and Open Questions. Examine a decision: Perspective and Gauntlet. Verify an outcome: Health, Triage, Did It Land, Watch and Evidence-Locked UAT. Carry work forward: Write Goal, Decision Ledger, Manifest, Outsource and Context Audit. Epistemic is the shared usage guide. You can pick any method; the groups are not stages." width="1280">
</picture>

*The [Skill Catalog](Skill-Catalog.md) lists the same groups in text, with a link to every method.*

### Reflection, a lens, or a panel?

| Method | Distinct responsibility | Example |
|---|---|---|
| **Metacognate** | Examine the reasoning, assumptions, and meaning of success | “Does this benchmark represent the user experience?” |
| **Perspective** | Apply a useful lens to a bounded concern | “What makes this migration reversible?” |
| **Gauntlet** | Compare separate examinations and adjudicate material tensions | “Should this consequential migration proceed under these conditions?” |

Perspective can use one lens or several. Gauntlet adds more: every review looks at the same fixed version of the proposal or decision, the findings are checked against the evidence, and a final judgment weighs them against each other. Adding lenses to Perspective does not turn it into a Gauntlet.

### State, cause, effect, or continuity of observation?

| Method | What it establishes | What it cannot establish alone |
|---|---|---|
| **Health** | Current state within declared bounds | Cause or successful delivery of a particular change |
| **Triage** | Cause or narrowed explanations for a known failure | A completed repair |
| **Did It Land** | Intended effect at the consumer | Every user acceptance criterion or indefinite persistence |
| **Watch** | Commissioned external observation and alert delivery | Health inferred from silence or authority to remediate |
| **Evidence-Locked UAT** | Material acceptance against specified observations | Unobserved interactions or calibrated reliability |

### A record, a mission, or a goal?

Decision Ledger keeps the reasoning behind an important decision where a later session can find it and recheck it. If a decision record, issue or plan already holds that reasoning, it reuses that record instead of starting a new one.

Manifest is heavier, and it is used only when you opt in. It keeps a formal mission record, with a receipt for each file change made through it, and someone other than the agent that did the work must accept the mission before it closes.

Write Goal writes down what counts as done. It turns that into a goal or loop in your agent's app only if you allow it.

Outsource packages a task so another agent or tool can pick it up without this conversation — for a checked result you reintegrate, or for a full handover the receiver accepts on the record while you divest.

A project can need one of these without the others. Setting a goal does not open a mission, and writing a decision record does not set anything running.

[Design Rationale](Design-Rationale.md) explains the tradeoffs, and [Workflow Recipes](Workflow-Recipes.md) shows the methods used together.
