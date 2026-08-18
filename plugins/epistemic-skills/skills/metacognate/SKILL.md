---
name: metacognate
description: Use when the approach itself is uncertain rather than just the answer — before an irreversible or high-blast-radius act, when a claim is about to bear load ("it works", "it is done", "it is deployed", "it is fine"), when an observation contradicts what a tool or document just asserted, or when resuming from a summary, handoff, or remembered state. Do NOT fire for routine reversible work you can check directly, for lookups or mechanical edits, for a call the operator has already made, or from inside a discipline this would hand to.
metadata:
  hands-to: []
  event-kinds: [routing-decision]
  eligible-when: [evaluation-case, sampled-field-incident]
  outcome-sources: [independent-adjudication]
  collection-mode: observational
  sentinel-fixture: metacognate-over-under.json
---

# metacognate — decide how much process this deserves, and usually decide none

> This is the only seat you invoke by name. Everything else in this collection
> fires on its own description.
>
> It owns exactly one decision: **what would have to be true for this to be
> right, and which of those can I not currently answer?** The unanswerable one
> names the work. If every one is answerable, the correct output is silence.

**It carries a procedure, never an inventory.** No list of members appears in
this file, and none may be added. A seat that enumerates its members becomes a
hand-maintained projection of a directory, and every such projection in this
package has drifted: one shipped a description naming two skills that no longer
existed. Selection belongs to each member's own description, which is the only
text that governs firing. Adding a member must cost this file nothing.

## Tier 1 — IRON

No judgment. No waiver. These hold regardless of which layer currently has
control, including a workflow layer's own gates.

| Law | Meaning |
|---|---|
| **Consent precedes the irreversible** | No consequential or irreversible act without prior, scoped authorization. Escalate on ambiguity rather than act on a convenient reading. |
| **An oracle must be adequate to its claim** | A success claim must show the check actually exercises the asserted behavior. A green check whose oracle read the source does not establish a claim about the runtime. |
| **No actor certifies its own acceptance** | Whoever did the work does not rule on whether it is accepted. |
| **A hard gate is not overridable from the other side** | A workflow layer's gate is not waivable by this layer, and this layer's iron is not waivable by a workflow layer. Neither is a suggestion. |

Iron applies where being wrong is **irreversible**. That is the whole scope. It
is deliberately four lines, because a law nobody can recite is not a law.

## Tier 2 — WISE

Judgment. Bidirectional. Bounded.

1. **Does this clear the routine fast path?** Routine, reversible, locally
   checkable, non-precedential work → do the work, say nothing, **stop**.
   Silence is a success state, not a skipped step.
2. **What would have to be true for this to be right?** Name the conditions, not
   the tasks.
3. **Which of those can I not currently answer?** That one names the discipline.
   If all are answerable, engage nothing and return to the work.
4. **The named discipline runs bounded**, then hands control **back** to the
   point of interruption. It does not take over the task.
5. **Re-enter only on a new unanswerable condition**, never on a schedule and
   never to be thorough.

### Pairing with a workflow layer

Pairing is a judgment at a moment, not a table of stage-to-skill pairs. A table
cannot express the two things that actually matter: either side may interrupt,
and control must come **back**.

- Either strand may interrupt the other at any point. There is no owning layer.
- An interruption is bounded and returns control where it left.
- On conflict, Tier 1 governs both strands. Below Tier 1, the strand whose
  question is currently unanswerable proceeds.

## The cost that governs width

This file's `description` is always resident in every session; the body is not.
Description bytes are a **shared, rivalrous budget across the whole estate** —
measured 2026-08-06, adding three skills silently blanked the descriptions of
four unrelated ones, and a skill whose description is dropped cannot fire at all.

Two consequences bind any future edit:

- **The decline test must stay readable from the description alone.** If routine
  work cannot be declined without loading this body, a wide trigger stops being
  cheap and starts taxing every task.
- **Width is bought with concision, never with bytes.** If a trigger condition
  will not fit, narrow the trigger. Do not lengthen the description — that cost
  is invisible here and lands on a different skill's ability to fire.

## Anti-rationalizations

| Thought | Reality |
|---|---|
| "Engaging something shows rigor" | Extra process earns no credit unless it can expose an action-changing error. |
| "I should list the members so the reader knows what is available" | That list is a projection that will drift. Members announce themselves. |
| "The gate is inconvenient here" | Iron is scoped to the irreversible precisely so it is never negotiable inside that scope. |
| "I can answer all of these" | Above-chance self-knowledge that is not acted on is the documented failure mode. Ask what observation would show you wrong. |
| "It fired, so it should do something" | Declining is the most common correct outcome. A gate that never says no is not a gate. |
| "The workflow layer is in charge right now" | Neither layer is in charge. Iron binds both. |

## Output

Nothing, when the fast path clears — no artifact, no note, no announcement.

Otherwise: the unanswerable condition, the discipline it names, and the point to
return to. That is the entire contract.

## Evidence emission

After each engagement, append one line to `runs/ledger.jsonl` under this skill:

```json
{"schema":"skill-run@1","ts":"<iso8601>","skill":"<this-skill>","decision":"fired|declined","discipline_engaged":"<name-or-null>","action_changed":true|false}
```

The append is part of this procedure. It is not a call to an external calibration
service and it is not a `decision-ledger` entry. Schema:
`plugins/epistemic-skills/contracts/skill-run-ledger.schema.json`.

## Local overlay

If a `LOCAL.md` exists alongside this file, read it after this one. It may add
site-specific iron. It may never remove any.
