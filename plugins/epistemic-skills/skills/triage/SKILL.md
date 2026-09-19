---
name: triage
description: Use when a specific failure or unexpected behavior needs causal investigation. Reuse an adequate known diagnosis. Do not run a second investigation merely to apply a fix, or use diagnosis-only authority to authorize repair.
metadata:
  hands-to: [decision-ledger]
  event-kinds: [cause-verdict]
  eligible-when: [evaluation-case, sampled-field-incident]
  outcome-sources: [deterministic-fixture, field-observation]
  collection-mode: observational
  sentinel-fixture: triage-plausible-not-observed.json
---

# Triage: investigate the failure and return to the authorized task

> The expensive failure in diagnosis is not missing the cause. It is **naming a
> cause that was never observed** — a plausible story that fits the symptom,
> gets acted on, and leaves the real fault in place while everyone believes it
> is fixed.
>
> This skill owns one decision: **what is the cause of this specific failure,
> and what did I observe that rules the alternatives out?**

## The decision it owns

Per investigation, exactly one of four verdicts.

| Verdict | Meaning | Rule |
|---|---|---|
| `CAUSE` | an observation distinguishes this cause from the alternatives | must name the observation and what it ruled out |
| `NARROWED` | some candidates eliminated, cause not yet isolated | must name what was eliminated and by what observation |
| `UNKNOWN` | could not observe enough to eliminate anything | never dressed up as a most-likely cause |
| `NOT-BROKEN` | the report was wrong; the subject is within bounds | a real and common outcome, never an embarrassment |

**The rule that carries the skill:** a cause is established by an observation
that **would have come out differently** if the cause were something else. A
candidate that merely fits the symptom is a hypothesis, and calling it a cause is
the failure this exists to prevent.

## Trigger

Fires when:

- a specific subject is known broken, degraded, or behaving unexpectedly;
- a check went red, a deploy failed, a service is unreachable;
- a state readout named something wrong and the cause is not yet known;
- an observation contradicts what a tool or document asserts, and the
  disagreement itself is the thing to explain.

Does **not** fire when:

- you do not yet know whether anything is wrong — that is a health readout, and
  this skill consumes its output;
- the cause is already established and you are applying the remedy;
- the question is about a change you are making rather than a failure you face;
- the fault is deterministic and reproducible and one read of the error settles
  it — read it.

## One investigation, with an explicit provider

Prefer **Superpowers systematic-debugging** when available and applicable. Load
its current instructions and integrate the causal standards here into that
investigation. Briefly identify both methods actually used. If the provider is
unavailable or inadequate for the case, read
[standalone-debugging.md](reference/standalone-debugging.md) and use that procedure.
Do not claim to have used Superpowers when only this fallback was available.
The package remains usable without an external dependency.

Do not repeat a completed adequate investigation to produce another report.
Check that inherited observations concern this failure, revision and environment;
name what was inherited and what was newly observed. Reopen only the part whose
basis is stale, missing or contradicted.

## Method

1. **Establish the failure and scope.** Reuse the available readout and known
   diagnosis. If no adequate observation exists, reproduce or probe the minimum
   needed to bound the fault. State reproduction limits and whether evidence was
   inherited or gathered now. A direct discriminating error can settle a small
   investigation without manufactured alternatives.
2. **Separate observations from hypotheses.** For each plausible live explanation,
   identify evidence that would distinguish it from the others. Do not turn an
   unfalsifiable explanation into an eliminated candidate.
3. **Test the decisive difference.** Choose an informative, safe observation
   with proportionate cost. Observe at the level of the failure: source text does
   not settle a runtime claim, and a cache does not settle committed state.
   Change one relevant variable when feasible and inspect the result before
   adding another speculative fix.
4. **State the causal verdict.** Use CAUSE, NARROWED, UNKNOWN or NOT-BROKEN and
   name the evidence and remaining limits. A plausible explanation is not CAUSE.
5. **Continue within the original authority.** For an authorized repair task,
   apply the supported repair, check the original failure and relevant regression,
   and complete remaining integration work. A causal verdict alone is not a fixed
   system. For diagnosis-only work, return the verdict and stop at that boundary.
   Existing repair authority carries forward; do not request it again merely
   because this method reached a finding.

## Boundaries and return

- Investigative certainty does not expand authority. Destructive experiments or
  repairs outside the current scope need their actual authorization.
- A failed observation is a coverage limit; it does not establish a system fault.
- NOT-BROKEN requires an adequate direct observation of the reported behavior;
  a generic healthy readout cannot contradict a specific reproduced failure.
- Return the verdict, provider actually used, discriminating observation, repair
  status and verification limits to the task owner. Keep this brief for small work.
- Health supplies state observations; decision-ledger preserves consequential
  reasoning when its own trigger applies. Neither is a compulsory extra pass.

## Anti-rationalizations

| Thought | Reality |
|---|---|
| "This explains the symptom, so it is the cause" | So do the three you did not write down. Which observation rules them out? |
| "I know this system, it is always the disk" | Then the disk observation is cheap. Make it, and say what it showed. |
| "The logs are consistent with X" | Consistent-with is not distinguishes-from. Name the observation that would differ if not-X. |
| "I will just try several fixes and see" | A controlled, authorized intervention can test a hypothesis. Several unexplained changes obscure what caused the result. |
| "The config says it is set that way" | Configuration is a claim about a runtime. Observe the runtime. |
| "I could not reach it, so it is down" | You could not reach it. `UNKNOWN`. |
| "Narrowing to two is basically solved" | Then say `NARROWED` and name both. The wrong one of two is still wrong. |

## Degraded operation

| Condition | Behaviour |
|---|---|
| no readout available | probe minimally, and label the output self-probed |
| subject unreachable | `UNKNOWN (unreachable)`; never inferred as the fault |
| fault not reproducible | say so explicitly; an intermittent fault with one observation is `NARROWED` at best |
| observation would be destructive | use a safe alternative; otherwise hold that experiment pending actual scoped authority |
| the readout itself is suspect | that becomes the subject — a lying instrument is a fault, and a common one |

## Oracle

The failure mode is a confident wrong cause, so the check must plant one. A
fixture set presents symptoms consistent with several causes and asserts the run
returns `NARROWED` rather than `CAUSE` when no discriminating observation was
made — **and asserts it does not name the most plausible candidate as the cause**,
which is the assertion that matters and the one a naive suite omits.

At least one fixture must plant a **lying readout** — a report that says healthy
while the subject is broken — and assert the run treats the readout as suspect
rather than concluding `NOT-BROKEN`.

## Evidence emission

When an authorized evaluation or existing task evidence contract collects
engagement telemetry, use the local `runs/ledger.jsonl` format. Ordinary use
requires no separate process artifact:

```json
{"schema":"skill-run@1","ts":"<iso8601>","skill":"<this-skill>","decision":"fired|declined","discipline_engaged":"<name-or-null>","action_changed":true|false}
```

Telemetry is private runtime evidence of engagement, not proof of the outcome
or a replacement for a consequential decision record. Schema:
`plugins/epistemic-skills/contracts/skill-run-ledger.schema.json`.

## Local overlay

If a `LOCAL.md` exists alongside this file, read it after this one. It binds
site-specific fault catalogues, known-failure patterns, and probe commands. This
file must stay free of them: the moment a hostname, share path, or credential
name appears here, the skill stops being portable and becomes one site's runbook.
