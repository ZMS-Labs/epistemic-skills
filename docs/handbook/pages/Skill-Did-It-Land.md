> **Applies to:** epistemic-skills v7.0.0.

# Did It Land

**Verify the effect where the change is actually consumed.**

Did It Land follows a change beyond the edited source to its consumer: the loaded plugin, running service, rendered interface, or distributed artifact. It asks what observable result would differ if the change had not taken effect.

**Use it when:** A deploy, configuration, guard, merge, or fix is about to support a completion claim and its effect is not directly established.

**Use something simpler when:** The local reversible change is already directly observable as it is made, or you are still deciding what to change.

### Illustrative request

> The new rule is committed. Confirm that this agent session actually loads it and describe what remains unverified.

**What a useful result looks like:** LANDED, REVERTED, or UNVERIFIED, scoped to the observed consumer and time. Present effect, persistence across a relevant restart or reconciliation, and future overwrite risk are reported separately.

**Boundary:** A successful command, diff, or source-only test cannot prove runtime effect. REVERTED requires an observed undo after an observed landing; merely identifying overwrite risk is insufficient.

[Health](Skill-Health.md) checks current operating state; [Evidence-Locked UAT](Skill-Evidence-Locked-UAT.md) evaluates material user-facing acceptance.

[Read the canonical v7.0.0 method](https://github.com/ZMS-Labs/epistemic-skills/blob/v7.0.0/plugins/epistemic-skills/skills/did-it-land/SKILL.md) · [All methods](Skill-Catalog.md)
