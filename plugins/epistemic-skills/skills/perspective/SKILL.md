---
name: perspective
description: Use when a focused concern, assumption or tradeoff would benefit from a different evidence-based lens, or on explicit request. Do not convene a panel for routine work or treat lens count as adjudication.
metadata:
  event-kinds: [review-forecast]
  eligible-when: [preregistered-prediction, correction-or-supersession]
  outcome-sources: [field-observation, supersession-chain]
  collection-mode: conditional
  sentinel-fixture: perspective-unexamined-assurance.json
---

# Perspective

Examine a bounded question through a useful lens and return the result to the
work it informs. Several lenses may be useful; their number does not turn this
method into Gauntlet. Gauntlet adds plural scrutiny and reasoned adjudication of
a common subject. Perspective has no automatic escalation or approval gate.

## Inputs and selection

Identify the live concern, subject/version, decision or action it informs,
existing evidence, scope and authority. Reuse adequate observations and prior
answers. Do not infer a new assignment from an interesting adjacent issue.

Use the shared [lens guidance](../../reference/lenses.md) and canonical
[registry](../gauntlet/roster/registry.json). Select by functional question and
evidence mechanism; read the selected method's actual procedure, limits and
revision conditions. Persona names are lookup aliases, not authority. A focused
reversibility question may need only rollback feasibility and the cost of undo.

Adapt a method to the actual case when needed. State consequential adaptations
and their limits; do not silently add a permanent library member. Multiple modes
of one method and repeated use of one source do not establish corroboration.

Activation discipline: design-argued; no shipped trigger battery as of this change.

## Method

1. **Bound the question.** Name the uncertainty or improvement sought and what
   result would change the next action. If the evidence already settles it,
   reuse that result rather than manufacture another investigation.
2. **Apply the lens.** Follow its evidence procedure on the subject. Distinguish
   observations, inferences, hypotheses and user-owned value choices. Describe
   missing evidence without fabricating stakeholder participation or findings.
3. **Test the contribution.** Check the finding's consequential premise and
   whether its proposed improvement preserves the need the subject meets.
   Seek a discriminating observation for empirical claims. For value tradeoffs,
   identify whose authorized criteria would change the choice; do not pretend
   a preference can be refuted by an unrelated technical metric.
4. **Adapt only for a remaining question.** Another lens may resolve a distinct
   uncertainty or inspect a revised candidate. Preserve unaffected evidence.
   Stop when the concern is adequately answered, evidence is unavailable, or
   additional examination would not affect the authorized action. Report a
   limit instead of turning exhaustion into assurance.
5. **Return and continue.** Briefly acknowledge Perspective and the lens used,
   declare the finding (per Output below: `insight`, `adjustment`,
   `supported-finding`, `no-material-finding` or `remaining-uncertainty`),
   and state its consequence. Continue the original authorized task.
   Assessment alone does not authorize implementation.

## Output: the declared finding

Every consideration of this method ends in exactly one of two discipline
modes:

- **`apply-lens`** — a lens was applied to a bounded question. The application
  declares the four fields below.
- **`no-fire`** — the method did not apply. A no-fire is **silent**: no lens,
  no question, no finding is declared. A declared field on a non-application
  is over-firing, not generosity.

An application declares:

- **`lens`** — the lens or method applied.
- **`question`** — the bounded question the lens was applied to.
- **`lenses_applied`** — the count of lenses actually applied, at least one.
  Several lenses may be applied to one bounded question; a focused
  reversibility question takes a single narrow lens.
- **`finding`** — exactly one of the five values below, quoted verbatim. A
  paraphrase or a coinage outside this vocabulary is a contract violation
  even when the examination itself was sound.

| Finding | The lens's examination found |
|---|---|
| `insight` | Something material that was not in view, surfaced by the lens. |
| `adjustment` | The lens's evidence supports a concrete change — to the subject, the plan, the measure it is judged by, or the next action. |
| `supported-finding` | The evidence through the lens supports the proposition under examination. |
| `no-material-finding` | The lens was applied on the available evidence and the concern did not stand: nothing material was found. |
| `remaining-uncertainty` | The lens cannot settle the bounded question — the evidence it needs is unavailable, or the question outruns what the lens can determine. The limit is reported, not converted into assurance. |

**Boundary rules for the finding.** Where the lens's evidence supports a
concrete change, the finding is `adjustment`. `remaining-uncertainty` is
reserved for what the lens cannot settle; it is never the resting place of
an examination whose evidence already points at a change. The distinction
from `no-material-finding` is whether the examination could run: a lens that
inspected the available evidence and found the concern empty reports
`no-material-finding`; a lens whose needed evidence does not exist reports
`remaining-uncertainty`, applied as far as the available evidence allows.

**Lens count is not adjudication.** An application never carries a verdict
or an adjudication, under any value. Where what is actually requested is
plural examination plus adjudication of a common subject, or an approval
verdict, that is not a Perspective application at all — it does not fire
here.

## Limits and evidence

A useful change of perspective is not an approval verdict, a complete review or
an independent expert's opinion. If the task requires plural examination and
adjudication, use Gauntlet on that basis, not because a lens-count threshold was
crossed. Shared context, models and evidence constrain independence.

## Evidence emission

Ordinary use requires no extra report or ledger. When an authorized evaluation
or existing evidence contract collects usage, append the established private format
to `runs/ledger.jsonl`:

```json
{"schema":"skill-run@1","ts":"<iso8601>","skill":"perspective","decision":"fired|declined","discipline_engaged":null,"action_changed":false}
```

Apply `../../contracts/skill-run-ledger.schema.json`; engagement telemetry does
not prove the lens improved the outcome.
