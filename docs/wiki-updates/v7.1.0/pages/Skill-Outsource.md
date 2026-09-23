> **Applies to:** epistemic-skills v7.1.0.

# Outsource

**Make an external handoff understandable without the original chat.**

Outsource packages work in a durable repository record at an immutable reference. It includes the current state, evidence, constraints, allowed actions, and the required return format. The short prompt is a pointer to that complete packet.

The skill has two modes, picked by what you actually asked for. **Delegate** sends a bounded assignment out and brings a checked result back; you keep owning the outcome. **Transfer** hands the work itself over: every open item, standing duty, and grant of authority is inventoried, the receiver reads the inventory back and accepts it on the record, and the giver divests — stops the watchers, hands over the keys, leaves the loops — before calling the handover done. A transfer is closed by that acceptance and divestiture, not by verified work product, because the giver can no longer verify work it no longer owns.

**Use it when:** An external worker or reviewer must operate independently of the originating conversation, a returned relay needs to be recorded and checked, or responsibility for a body of work is genuinely moving to another agent.

**Use something simpler when:** You are delegating a small local subtask or asking a same-session question; neither needs a repository relay. If you only meant "do this one thing and report back," that is a delegation, not a transfer.

### Illustrative request

> Prepare a handoff for the external reviewer covering this API change, including the exact commit, unresolved concerns, and evidence required in the return.

> I'm stepping away from this service. Hand all of it to the other agent — open incidents, the on-call rotation duty, the deploy key custody — and get its acceptance on the record before you stand down.

**What a useful result looks like:** A target-readable packet and concise prompt, or a named access/publication blocker. Delegated returns are retained and their claims verified under the repository's normal gates. Transfers end with a recorded acceptance read-back and a completed divestiture checklist, not a promise.

**Boundary:** A local packet is not ready until it is committed, published within authority, and reachable to the intended target. Handoff preparation does not itself perform or certify the outsourced work, and an accepted transfer certifies the handover, not the receiver's future stewardship.

[Decision Ledger](Skill-Decision-Ledger.md) supports continuity; [Manifest](Skill-Manifest.md) adds a mission contract when that tier is actually needed — consequential work should sit in one before it is transferred anywhere.

[Read the canonical v7.1.0 method](https://github.com/ZMS-Labs/epistemic-skills/blob/v7.1.0/plugins/epistemic-skills/skills/outsource/SKILL.md) · [All methods](Skill-Catalog.md)
