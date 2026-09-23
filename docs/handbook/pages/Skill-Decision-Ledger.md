> **Applies to:** epistemic-skills v7.0.0.

# Decision Ledger

**Keep important reasoning recoverable without duplicating records.**

Decision Ledger has three modes: persist a consequential decision, re-anchor prior claims when resuming, and compare an original prediction with its later outcome. A sufficient ADR, issue, plan, or goal contract can already be the right home.

**Use it when:** A future session or reader needs a decision or assumption that lacks durable provenance; resumed work depends on prior-state claims; or an outcome has become observable.

**Use something simpler when:** A routine choice has no downstream consequence, or an existing artifact already satisfies the persistence need. Reuse does not waive a needed freshness check.

### Illustrative request

> Resume from this handoff. Verify the facts needed for the next step and preserve the reasoning behind the selected approach.

**What a useful result looks like:** A durable reference, a re-anchored state summary, or an outcome record that preserves prediction and observation separately. New records state what would cause reconsideration.

**Boundary:** Records inform but never authorize. Do not rewrite old predictions after seeing the result or create a parallel ledger merely to demonstrate activity.

[Manifest](Skill-Manifest.md) adds mission custody; [Write Goal](Skill-Write-Goal.md) defines the completion contract.

[Read the canonical v7.0.0 method](https://github.com/ZMS-Labs/epistemic-skills/blob/v7.0.0/plugins/epistemic-skills/skills/decision-ledger/SKILL.md) · [All methods](Skill-Catalog.md)
