> **Applies to:** epistemic-skills v7.0.0.

# Outsource

**Make an external handoff understandable without the original chat.**

Outsource packages a bounded assignment in a durable repository record at an immutable reference. It includes the current state, evidence, constraints, allowed actions, deliverables, and the required return format. The short prompt is a pointer to that complete packet.

**Use it when:** An external worker or reviewer must operate independently of the originating conversation, or a returned relay needs to be recorded and checked.

**Use something simpler when:** You are delegating a small local subtask or asking a same-session question; neither needs a repository relay.

### Illustrative request

> Prepare a handoff for the external reviewer covering this API change, including the exact commit, unresolved concerns, and evidence required in the return.

**What a useful result looks like:** A target-readable packet and concise prompt, or a named access/publication blocker. Returned material is retained and its claims verified under the repository's normal gates.

**Boundary:** A local packet is not ready until it is committed, published within authority, and reachable to the intended target. Handoff preparation does not itself perform or certify the outsourced work.

[Decision Ledger](Skill-Decision-Ledger.md) supports continuity; [Manifest](Skill-Manifest.md) adds a mission contract when that tier is actually needed.

[Read the canonical v7.0.0 method](https://github.com/ZMS-Labs/epistemic-skills/blob/v7.0.0/plugins/epistemic-skills/skills/outsource/SKILL.md) · [All methods](Skill-Catalog.md)
