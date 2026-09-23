> **Applies to:** epistemic-skills v7.1.0.

# Triage

**Distinguish an observed cause from a plausible story.**

Triage investigates one known failure using evidence that would differ between competing explanations. When the systematic-debugging skill from [Superpowers](https://github.com/obra/superpowers), a separate open-source skills library, is available and applies, the agent loads and uses it within the same investigation. A standalone procedure is available otherwise.

**Use it when:** Behavior is wrong or unexpected and the cause is not yet adequately established.

**Use something simpler when:** A direct error already settles the cause, or a current, adequate diagnosis exists and the remaining task is to apply its repair.

### Illustrative request

> The saved preference disappears after reload. Diagnose the cause, fix it within this task, and verify the original behavior.

**What a useful result looks like:** CAUSE, NARROWED, UNKNOWN, or NOT-BROKEN, with the discriminating observation and the actual debugging provider used. For an authorized repair task, the agent continues through repair and relevant verification.

**Boundary:** A diagnosis is not a completed repair. Diagnosis-only authority does not authorize mutation; existing repair authority does not need to be requested again.

[Health](Skill-Health.md) establishes the state of a system; [Did It Land](Skill-Did-It-Land.md) verifies that the repair reached the intended consumer.

[Read the canonical v7.1.0 method](https://github.com/ZMS-Labs/epistemic-skills/blob/v7.1.0/plugins/epistemic-skills/skills/triage/SKILL.md) · [All methods](Skill-Catalog.md)
