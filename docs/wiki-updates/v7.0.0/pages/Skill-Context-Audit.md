> **Applies to:** epistemic-skills v7.0.0.
> Source checks, loaded context, exercised workflows and comparative benefit are distinct.

# context-audit — audit the assembled context, not a file

'Use when auditing the instruction context an agent actually receives — on explicit request ("audit my context/CLAUDE.md/system prompt", "context audit", "prune my instructions"), when a cross-layer instruction conflict is detected mid-task (two active layers direct incompatible behavior), or after a model-generation upgrade invalidates guardrails written for a weaker model. Do NOT fire for auditing the prose quality of one document (ordinary editing), for designing NEW tool/agent interfaces (that is interface craft doctrine, not context hygiene), for pre-work recon on a task brief (recon owns the territory; this skill audits the map), or for tuning a prompt to improve the output of one specific task (that is prompt engineering, not context hygiene).'

Read the [canonical method](https://github.com/ZMS-Labs/epistemic-skills/blob/v7.0.0/plugins/epistemic-skills/skills/context-audit/SKILL.md) before applying it.
Use its required inputs, reusable evidence, stopping rule and return boundary.
Acknowledge actual use and continue the authorized task when the method returns.
The canonical source includes the full method, output contract and limitations.

[Choose a skill](Skill-Catalog.md) · [Current evidence](https://github.com/ZMS-Labs/epistemic-skills/blob/v7.0.0/docs/release/v7-evidence.md)
