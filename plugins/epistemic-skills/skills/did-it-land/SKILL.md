---
name: did-it-land
description: Use when a change is believed applied and something now depends on it being true — after a deploy, a config edit, a guard or hook installation, a merge, or a fix about to be called done. Also fires when a check is green but its oracle only read source. Do NOT fire when the change is local, reversible and directly observable in the same breath as making it, when nothing yet depends on it having landed, or when you are still deciding what to change.
metadata:
  hands-to: [decision-ledger]
  event-kinds: [landing-verdict]
  eligible-when: [evaluation-case, sampled-field-incident]
  outcome-sources: [deterministic-fixture, field-observation]
  collection-mode: observational
  sentinel-fixture: did-it-land-source-read-as-landed.json
---

# Did It Land: observe the intended effect at its consumer

> Writing a control is not installing one. The most expensive claim in this
> whole practice is **"it is fixed"** made by an agent that read the file it
> edited and never asked the running system.
>
> This skill owns one decision: **is the change in effect on the thing that
> actually runs — and what did I observe that would look different if it were
> not?**

## The decision it owns

| Verdict | Meaning | Rule |
|---|---|---|
| `LANDED` | intended effect observed at the consumer within the stated scope and time | name the observation and separately state persistence coverage |
| `REVERTED` | an observed effect was subsequently observed undone | show both observations; identify the writer only if supported |
| `UNVERIFIED` | intended effect not established for the requested scope | distinguish observed absence from inability to observe |

**`UNVERIFIED` is the default.** A change is not landed until observed landed.
The burden runs the other way from ordinary work, because the failure is silent:
nothing tells you the guard you wrote was never installed.

## Trigger

Fires when:

- a deploy, merge, config edit, guard, hook, or migration is believed applied;
- a fix is about to be called done and something depends on that;
- **a check is green but its oracle only read source** — the check proves the
  text changed, not that the behavior changed;
- an artifact is believed distributed to the place that consumes it.

Does **not** fire when:

- the change is local, reversible, and observable in the same breath as making
  it;
- nothing yet depends on it having landed;
- you are still deciding *what* to change.

## Method

1. **Name the observable before looking.** What, specifically, would be different
   at the runtime if this landed? If nothing observable differs, the change is
   either inert or the observable is not yet identified — say which.
2. **Identify what actually loads.** The thing that runs is frequently not the
   thing you edited: a cache rather than a checkout, a built image rather than a
   source tree, a deployed copy rather than a repository, a generated projection
   rather than its source. **Resolve which artifact the runtime reads, and verify
   that one.**
3. **Observe at the runtime.** Ask the running system. Reading a file, a
   manifest, or a diff is a claim *about* the runtime, not an observation *of*
   it.
4. **Check persistence risk.** Identify a reconciler, generator, cache or other
   writer that may overwrite the change. An unchanged source of authority creates
   a future reversal risk; it does not establish that reversal already happened.
5. **Observe the relevant persistence boundary.** Where the claim includes
   survival of reconciliation or restart, re-observe after that event. If the
   interval or event is unavailable, report the present observation and leave
   persistence unverified. Do not wait indefinitely or predict an observed result.
6. **Report current effect, persistence evidence and future risk separately.**
   A change may be LANDED now with future overwrite risk. REVERTED requires an
   observed undo after observed landing. Briefly acknowledge Did It Land and
   return the result to the work that depends on it.

## Boundaries

- **Never infers landing from the diff, the commit, the PR, or the log line.**
  Those are records of intent to change, not evidence of change.
- **Never accepts a green check as landing** unless the check itself observed the
  runtime. Most do not.
- **Verification does not create repair authority.** Return a failed landing
  observation to the task owner. Continue an already-authorized fix and verify it;
  an assessment-only request ends at the finding.
- **Scope every verdict.** LANDED on one checked consumer does not establish
  the requested effect on three. Report covered and uncovered sets; the full
  requested scope remains UNVERIFIED when coverage is partial.

## Anti-rationalizations

| Thought | Reality |
|---|---|
| "The commit is on main" | main is a record. Ask the runtime. |
| "The tests pass" | Do they exercise the runtime, or the source? If source, they cannot see this. |
| "I edited the file and re-read it" | You verified your own write. Which artifact does the runtime load? |
| "The deploy command exited 0" | Exit 0 means the command ran. It is not an observation of effect. |
| "I grepped and it returned nothing" | A search that matches nothing and a search that is broken are the same output. Prove the search can find something. |
| "It is there now" | Is anything reconciling it? Look again after the window. |
| "The generated file is correct" | Then the generator ran. Did the consumer reload? |
| "It worked on the node I checked" | Which one does production use? |

## Degraded operation

| Condition | Behaviour |
|---|---|
| runtime unreachable | `UNVERIFIED (unreachable)`; never `LANDED` |
| no observable identified | `UNVERIFIED (no oracle)` — and that is a finding about the change, not about this skill |
| owner exists, reconcile interval unknown | report observed current effect; persistence remains unverified and overwrite risk explicit |
| observed in one place of several | `UNVERIFIED (partial)` with the covered and uncovered sets named |
| the observation itself is the thing under test | escalate — a check verifying itself is the failure this skill exists to catch |

## Oracle

The failure is a false `LANDED`, so the check must manufacture one. A fixture set
must include:

- a change **present in source and absent from the runtime** — assert
  `UNVERIFIED`, not `LANDED`;
- a change **present now and reverted by an owner** after the window — assert
  `REVERTED`;
- a **broken observation** that returns empty because it is malformed rather than
  because nothing matched — assert the run refuses to read absence as success;
- a **positive control that exercises the same path production takes**. A control
  passing on a stand-in path proves the control works on the stand-in and nothing
  about production.

For example, a control exercising a symbolic link does not establish behavior
for a junction or another link type. Exercise the actual consuming path.

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
which artifact each runtime actually loads, known reconcilers and their
intervals, and the commands that observe them. This file must stay free of them.
