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
to reconstruct available context.

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

## Output and limits

Usually a short statement of the reasoning examined, the supported conclusion
or correction, remaining material uncertainty and the action it informs. No
report is required for a method that did not apply. When actually used, a brief
acknowledgment remains appropriate even if nothing changes. Reflection alone
cannot supply missing observations or authorize an otherwise unauthorized act.

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
