> **Applies to:** epistemic-skills v7.1.0.

# Watch

**Commission and prove a real observer that survives the session.**

Watch defines the condition that matters, the external mechanism that checks it, who receives a useful alert, and how that mechanism can be stopped. The skill itself does not stay running after the conversation.

**Use it when:** A meaningful bound must be noticed between sessions and someone will act when it is crossed.

**Use something simpler when:** You need a current-state readout, diagnosis, automatic remediation, or a notification nobody has agreed to receive.

### Illustrative request

> Notify the designated operator if this service misses the agreed freshness bound. Prove the complete alert path with a safe test and verify the disable control.

**What a useful result looks like:** A commission record with DECLARED, BLOCKED, INERT, PROVEN, or SUSPECT state and supporting receipts. PROVEN requires a persistent enabled observer, a safe crossing through the real path, and delivery to the destination.

**Boundary:** A configuration file, dry run, or silent channel does not establish an active watch. Failed observation or delivery remains visible; noticing a problem does not authorize fixing it.

[Health](Skill-Health.md) observes now; [Triage](Skill-Triage.md) investigates a reported failure.

[Read the canonical v7.1.0 method](https://github.com/ZMS-Labs/epistemic-skills/blob/v7.1.0/plugins/epistemic-skills/skills/watch/SKILL.md) · [All methods](Skill-Catalog.md)
