> **Applies to:** epistemic-skills v7.0.0.

# Manifest

**Give interruption-sensitive work a durable chain of custody.**

Manifest records an explicitly bounded mission: authority, scope, protected state, receipted file effects, checkpoints, and the next permitted action. It supports opening, resuming, advancing, verifying, and closing that mission through a custody CLI.

**Use it when:** Work genuinely needs the mission-custody contract, or you explicitly ask to manifest it, and its acceptance path is available.

**Use something simpler when:** An ordinary task or existing record is sufficient. Having several steps alone does not justify mission ceremony.

### Illustrative request

> Manifest this migration with the agreed scope and protected files, and checkpoint it so another session can resume safely.

**What a useful result looks like:** Durable mission state and a resumable frontier. Resume checks receipted artifacts for drift; a clean check with no receipts proves no artifact coverage.

**Boundary:** This opt-in custody contract requires a distinct accepting actor and cannot be bypassed with a renamed identity. Recorded authority alone does not enforce tool permissions: runtime blocking depends on installed, armed guards. Case-insensitive POSIX custody limits remain documented.

[Decision Ledger](Skill-Decision-Ledger.md) preserves reasoning more lightly; [Write Goal](Skill-Write-Goal.md) defines done. See [known limitations](Testing-and-Evaluations.md).

[Read the canonical v7.0.0 method](https://github.com/ZMS-Labs/epistemic-skills/blob/v7.0.0/plugins/epistemic-skills/skills/manifest/SKILL.md) · [All methods](Skill-Catalog.md)
