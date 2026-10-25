---
name: metacognate
description: Use when the approach, assumptions, evidence, confidence or success criteria need examination, or when explicitly requested. Skip routine directly checkable work and settled user choices unless new evidence changes their basis.
metadata:
  hands-to: []
  event-kinds: [routing-decision]
  eligible-when: [evaluation-case, sampled-field-incident]
  outcome-sources: [deterministic-fixture, field-observation]
  collection-mode: observational
  sentinel-fixture: metacognate-over-under.json
---

# Metacognate

Examine how the current reasoning could succeed or mislead. The result may be a
better question, a corrected assumption, a more adequate check, a calibrated
confidence statement, or confirmation that the existing approach is sound.
This is substantive reflection, directly invocable at any point. It is not the
suite's usage entry and need not dispatch another skill.

## Applicability and inputs

Use when evidence conflicts with an assertion, a proxy is about to stand for
success, confidence outruns its basis, or an uncertain assumption could change
what to do. Explicit reflection requests also qualify. A resume or consequential
act warrants reflection when its basis is uncertain, not merely because that
stage has arrived. Reuse the current task, user decisions, observations and
relevant prior reasoning; investigate missing facts rather than asking the user
to reconstruct available context. Where the governing criteria are already
present in the task context — the brief, the linked specification, the record
in hand — that is a cue to investigate, not a reflection trigger: the
examination does not fire over criteria the task already supplies.

Activation discipline: design-argued; no shipped trigger battery as of this change.

## Method

1. **Recover the actual outcome.** What does the user need, and what would count
   as success or failure? Distinguish the outcome from a convenient proxy and
   preserve the user's value choices and current authorization.
2. **Expose the reasoning.** Identify the assumptions doing real work, the
   evidence for them, plausible competing explanations and missing coverage.
   Separate observation, inference, preference and unresolved uncertainty.
3. **Challenge the decisive link.** What observation would show this approach
   wrong? Does the proposed check exercise the asserted behavior? Inspect the
   most consequential weak link; breadth must earn its cost. More process and
   more confidence are not independent evidence.
4. **Calibrate and adjust.** Say what the evidence supports, what it does not,
   and what would change the conclusion. Correct the question, approach or check
   when needed. If the existing approach is adequate, retain it. A distinct
   unresolved question may benefit from another available method, but that is
   optional and bounded by its actual applicability.
5. **Return to the task.** Briefly acknowledge Metacognate and the contribution
   or no-change result. Continue the authorized work from the point this result
   informs. Reopen settled reasoning only when a relevant condition changes.

## Evidence and authority

A source check does not establish a runtime effect; an action receipt does not
establish acceptance. Use checks adequate to the claim. Preserve consequential
uncertainty rather than converting absence of evidence into success.

The user can designate the reviewer, including the implementing agent. Report
actual reviewer identity, shared context and evidence limits. Self-checks do not
become independent or blinded merely by changing role names. Honor legitimate
task-specific custody, authorization and acceptance requirements without adding
a universal requirement for another actor or model family.

## Output: the declared outcome

Every consideration of this method ends in exactly one of two discipline
modes, and the mode is the first thing the output discipline fixes:

- **`examine`** — the approach, assumptions, evidence, confidence or success
  criteria were actually examined. The examination concludes by declaring the
  four fields below.
- **`no-fire`** — the method did not apply. A no-fire is **silent**: no
  report, no examination fields, and no explanation of why it did not fire.
  Nothing is filed for a method that did not apply, and silence is not a gap
  to be explained away.

An examination declares:

- **`outcome_named`** — the actual outcome the user needs, distinguished from
  any convenient proxy that might stand for it.
- **`decisive_assumption`** — the assumption doing real work in the current
  approach: the one whose failure would change the conclusion or what to do.
- **`discriminating_observation`** — what observation would show the approach
  wrong. The check proposed must exercise the behaviour asserted, not a
  stand-in for it.
- **`verdict`** — exactly one of the four values below, quoted verbatim. A
  paraphrase or a coinage outside this vocabulary is a contract violation
  even when the examination itself was sound.

| Verdict | The examination found |
|---|---|
| `approach-retained` | The existing approach was examined and is adequate; reflection changed nothing. A sound approach that survives challenge is retained. |
| `approach-corrected` | The approach, or the check it rests on, was corrected. |
| `question-reframed` | The question or success criterion itself was the defect — typically a proxy standing for the outcome. |
| `confidence-recalibrated` | The approach stands, but the stated confidence outran its basis and is brought back to what the basis supports. |

**Boundary rules for the verdict.** Where the approach rested on an assertion
the evidence contradicts, the verdict is `approach-corrected`: the defect is
in the approach and its check, and correcting them is the outcome.
`question-reframed` is reserved for a malformed question — where what was
asked, or the criterion by which success would be declared, is itself wrong.
A failed premise under a sound question is a correction, not a reframing.
Confidence is recalibrated only when the approach survives and the basis
supports less than was stated; if the basis supports nothing, that is a
correction, not a recalibration.

In ordinary work the declaration is carried in a short statement of the
reasoning examined, the supported conclusion or correction, remaining
material uncertainty and the action it informs — with the verdict quoted
from the vocabulary above. When actually used, a brief acknowledgment
remains appropriate even if nothing changes. Reflection alone cannot
supply missing observations or authorize an otherwise unauthorized act.

## Evidence emission

Ordinary reflection requires no separate process artifact. When an authorized
evaluation or existing task evidence contract collects engagement telemetry,
use the existing local `runs/ledger.jsonl` format:

```json
{"schema":"skill-run@1","ts":"<iso8601>","skill":"metacognate","decision":"fired|declined","discipline_engaged":null,"action_changed":false}
```

The schema is `plugins/epistemic-skills/contracts/skill-run-ledger.schema.json`.
Telemetry is private runtime state and is not proof of a reasoning benefit.

## Local overlay

If `LOCAL.md` exists alongside this file, read applicable local guidance. Resolve
conflicts using the host's instruction hierarchy and the user's current scope;
a local overlay does not create higher authority or negate explicit decisions.
