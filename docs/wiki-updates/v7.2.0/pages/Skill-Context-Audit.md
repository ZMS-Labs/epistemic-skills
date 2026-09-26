> **Applies to:** epistemic-skills v7.2.0.

# Context Audit

**Inspect the instructions the agent actually receives.**

Context Audit examines interactions among project rules, user guidance, skill descriptions, hooks, memory, and other accessible instruction layers. Its useful unit is the assembled context: two individually sensible files can still give conflicting directions.

**Use it when:** Active layers disagree, you explicitly request an instruction audit, or a model change makes an old guardrail worth testing again.

**Use something simpler when:** You only want prose editing, a better prompt for one task, or a review of an unfamiliar project.

### Illustrative request

> Find why the agent keeps asking for permission after I have already authorized this task. Trace the conflicting instruction layers.

**What a useful result looks like:** A scoped inventory, supported conflict or duplication findings, and a reviewable proposed change with rollback and regression conditions. It distinguishes source files, installed copies, observed loading, and actual application.

**Boundary:** Unobservable layers stay unobserved; an audit cannot certify them. Generated or governance instructions require maintenance at the proper source. Fewer tokens alone do not prove that a cut improves behavior.

[Metacognate](Skill-Metacognate.md) examines reasoning; [Did It Land](Skill-Did-It-Land.md) checks whether a corrected instruction reached its consumer.

[Read the canonical v7.2.0 method](https://github.com/ZMS-Labs/epistemic-skills/blob/v7.2.0/plugins/epistemic-skills/skills/context-audit/SKILL.md) · [All methods](Skill-Catalog.md)
