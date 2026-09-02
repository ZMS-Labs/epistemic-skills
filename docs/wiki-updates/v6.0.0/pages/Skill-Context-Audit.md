> **Applies to:** epistemic-skills v6.0.0
>
> **Canonical source:** [released Context Audit source](https://github.com/ZMS-Labs/epistemic-skills/blob/v6.0.0/plugins/epistemic-skills/skills/context-audit/SKILL.md)

# Context Audit

## What it does

Context Audit audits the instruction context an agent actually receives — every layer the harness loads (system prompt, project/user instruction files, memory indexes, skill descriptions, command definitions, hook output, tool and MCP instructions) — as **one assembled set**, not file by file. It classifies every instruction into cut classes (CONFLICT, DUPLICATE, OBVIOUS, MODEL-HANDLES-THIS-NOW, OVER-VERIFY) or keep classes (GOTCHA, OPERATOR-PREFERENCE, ROUTING+THRESHOLD, NAMED-INTEGRATION, GOVERNANCE), and emits a cut list as a unified diff, a conflict ledger, and a re-baseline watch note. Apply is operator-gated, class-by-class, one version-control commit per class.

The prior it operates under: as models strengthen, most accumulated instruction is deletion-eligible — but every cut is treated as a cheap, reversible, watched experiment, never a quota. Magnitude headlines from vendor reports are direction only and marked unreplicated inside the skill itself.

## Use it when

- The operator explicitly asks for a context/instruction audit.
- Two active instruction layers direct incompatible behavior mid-task.
- A model-generation upgrade has plausibly invalidated guardrails written for a weaker model.

## Do not use it when

- A single document needs prose editing — that is ordinary editing, not an assembly audit.
- You are designing a NEW tool or agent-consumed interface — that is the outbound channel, retained as craft doctrine under [`agent-interface-design`](Skill-Agent-Interface-Design) (a retired seat, no longer routed).
- You need pre-work recon on a task brief — [`recon`](Skill-Recon) (brief mode) audits the territory; this skill audits the map.
- You want to tune one prompt for one task's output — that is prompt engineering, not context hygiene.

## The one test

*"Would a strong model behave worse without this line?"* — applied line by line, with two hard guards: an instruction whose origin record exists may never be reclassified to a cut class without reading that record, and governance/generated layers are report-only.

## Boundary and handoffs

Ends at an applied (or report-only) audit with its watch note recorded. [`decision-ledger`](Skill-Decision-Ledger) persists cut decisions; [`gauntlet`](Skill-Gauntlet) takes any governance-adjacent cut before apply.

## Canonical sources

- [SKILL.md at v5.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/plugins/epistemic-skills/skills/context-audit/SKILL.md)
