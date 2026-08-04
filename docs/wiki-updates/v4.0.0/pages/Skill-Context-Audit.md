> **Applies to:** epistemic-skills v3.3.0
>
> **Canonical source:** [released Context Audit source](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.3.0/plugins/epistemic-skills/skills/context-audit/SKILL.md)
>
> **v4.0.0 note:** context-audit remains one of the eleven v4.0.0 skills, but sibling names this guide references were consolidated at v4.0.0 (2026-08-04): blindspot-pass → [recon](Skill-Recon)'s brief mode; agent-interface-design is now [reference craft doctrine](Skill-Agent-Interface-Design) (`plugins/epistemic-skills/reference/craft/`), read on demand, no longer a routed skill. See the [Skill Catalog](Skill-Catalog) for the full mapping; the tagged v4.0.0 sources are the sole contract.

# Context Audit

## What it does

Context Audit audits the instruction context an agent actually receives — every layer the harness loads (system prompt, project/user instruction files, memory indexes, skill descriptions, command definitions, hook output, tool and MCP instructions) — as **one assembled set**, not file by file. It classifies every instruction into cut classes (CONFLICT, DUPLICATE, OBVIOUS, MODEL-HANDLES-THIS-NOW, OVER-VERIFY) or keep classes (GOTCHA, OPERATOR-PREFERENCE, ROUTING+THRESHOLD, NAMED-INTEGRATION, GOVERNANCE), and emits a cut list as a unified diff, a conflict ledger, and a re-baseline watch note. Apply is operator-gated, class-by-class, one version-control commit per class.

The prior it operates under: as models strengthen, most accumulated instruction is deletion-eligible — but every cut is treated as a cheap, reversible, watched experiment, never a quota. The magnitude headline (Anthropic's reported 80% system-prompt cut) is cited as direction only and marked unreplicated inside the skill itself.

## Use it when

- The operator explicitly asks for a context/instruction audit ("audit my CLAUDE.md", "prune my instructions", "context audit").
- Two active instruction layers direct incompatible behavior mid-task (a detected cross-layer conflict).
- A model-generation upgrade has plausibly invalidated guardrails written for a weaker model.

## Do not use it when

- A single document needs prose editing — that is ordinary editing, not an assembly audit.
- You are designing a NEW tool or agent-consumed interface — Agent Interface Design owns the outbound channel.
- You need pre-work recon on a task brief — Blindspot Pass audits the territory; this skill audits the map.
- You want to tune one prompt for one task's output — that is prompt engineering, not context hygiene.

## The one test

*"Would a strong model behave worse without this line?"* — applied line by line, with two hard guards: an instruction whose origin record (incident, postmortem, memory) exists may never be reclassified to a cut class without reading that record, and governance/generated layers are report-only (findings route upstream; projections are never edited in place).

## What makes the cut list falsifiable

The re-baseline gate: after apply, a watch note covers the following sessions. Any behavioral regression attributable to a cut line returns that line as KEEP:GOTCHA citing the new incident. A cut that survives the watch window is confirmed dead weight; a cut that comes back has minted a documented gotcha where an undocumented guardrail used to be — strictly better either way.

## Boundary and handoffs

Ends at an applied (or report-only) audit with its watch note recorded. Decision Ledger persists cut decisions and revisit conditions; Gauntlet takes any governance-adjacent cut before apply; Agent Interface Design owns fixing the tool-description side of any DUPLICATE whose surviving copy belongs in an interface. Extraction (progressive disclosure of needed-but-oversized content) is a sub-mode, not the main axis: extraction relocates cost, classification removes it.
