---
name: triage
description: Use when a specific thing is known broken or degraded and the cause is not yet established — a failed deploy, an unreachable service, a red check, a readout naming something wrong. Consumes an existing state readout rather than re-probing blind. Do NOT fire when you do not yet know whether anything is wrong (that is a health readout), when the cause is already established and you are applying the fix, or when the question is about a change you are making rather than a failure you are facing.
metadata:
  hands-to: [decision-ledger]
---

# triage — find the cause, and stop there

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

## Method

1. **Take the readout if one exists.** Do not re-probe from scratch. If no
   readout exists, probe the minimum needed to bound the fault **and say that you
   did** — a self-probed triage is not the same evidence as a consumed readout,
   and the output must not blur them.
2. **Enumerate candidate causes before observing.** Written down first, so the
   first plausible one cannot quietly become the only one considered.
3. **For each candidate, name the observation that would eliminate it.** If a
   candidate has no such observation, it is unfalsifiable here — record it as
   unexamined rather than pretending it was ruled out.
4. **Order by cost, not by suspicion.** Cheapest discriminating observation
   first. Suspicion decides what to test only when costs tie.
5. **Observe at the level the fault lives.** A claim about a running system is
   not settled by reading its source or its configuration; a claim about
   committed state is not settled by reading a cache.
6. **Stop at the cause.** Hand off. The remedy is a separate, consented act.

## Boundaries

- **Never repairs.** Naming the cause and fixing it are different acts with
  different authority. This skill does the first.
- **Never names a cause it did not observe.** "Probably X" is `NARROWED` with X
  listed, not `CAUSE`.
- **Never re-probes a subject a readout already covered** without saying why the
  readout was insufficient.
- **Never converts an unreachable subject into a failing one.** Could not look is
  `UNKNOWN`, not a fault.

## Composition

- **health** produces the ordered subject list this consumes. It answers *what
  state*; this answers *why*.
- **decision-ledger** takes any consequential decision made off the back of a
  verdict. The verdict is evidence, never a decision.
- **The remedy is out of scope and deliberately unowned here.** Nothing in this
  package applies fixes.

## Anti-rationalizations

| Thought | Reality |
|---|---|
| "This explains the symptom, so it is the cause" | So do the three you did not write down. Which observation rules them out? |
| "I know this system, it is always the disk" | Then the disk observation is cheap. Make it, and say what it showed. |
| "The logs are consistent with X" | Consistent-with is not distinguishes-from. Name the observation that would differ if not-X. |
| "I will just try the fix and see" | That is a remedy without a cause, and a green result after it proves nothing about why. |
| "The config says it is set that way" | Configuration is a claim about a runtime. Observe the runtime. |
| "I could not reach it, so it is down" | You could not reach it. `UNKNOWN`. |
| "Narrowing to two is basically solved" | Then say `NARROWED` and name both. The wrong one of two is still wrong. |

## Degraded operation

| Condition | Behaviour |
|---|---|
| no readout available | probe minimally, and label the output self-probed |
| subject unreachable | `UNKNOWN (unreachable)`; never inferred as the fault |
| fault not reproducible | say so explicitly; an intermittent fault with one observation is `NARROWED` at best |
| observation would be destructive | stop and escalate; diagnosis never earns a destructive act |
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

After each engagement, append one line to `runs/ledger.jsonl` under this skill:

```json
{"schema":"skill-run@1","ts":"<iso8601>","skill":"<this-skill>","decision":"fired|declined","discipline_engaged":"<name-or-null>","action_changed":true|false}
```

The append is part of this procedure. It is not a call to an external calibration
service and it is not a `decision-ledger` entry. Schema:
`plugins/epistemic-skills/contracts/skill-run-ledger.schema.json`.

## Local overlay

If a `LOCAL.md` exists alongside this file, read it after this one. It binds
site-specific fault catalogues, known-failure patterns, and probe commands. This
file must stay free of them: the moment a hostname, share path, or credential
name appears here, the skill stops being portable and becomes one site's runbook.
