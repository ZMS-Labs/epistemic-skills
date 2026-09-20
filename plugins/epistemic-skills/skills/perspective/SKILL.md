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
   the insight, adjustment, supported finding, no-material-finding result or
   remaining uncertainty, and its consequence. Continue the original authorized
   task. Assessment alone does not authorize implementation.

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
