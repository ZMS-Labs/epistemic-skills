---
name: did-it-land
description: Use when a change is believed applied and something now depends on it being true — after a deploy, a config edit, a guard or hook installation, a merge, or a fix about to be called done. Also fires when a check is green but its oracle only read source. Do NOT fire when the change is local, reversible and directly observable in the same breath as making it, when nothing yet depends on it having landed, or when you are still deciding what to change.
metadata:
  hands-to: [decision-ledger]
---

# did-it-land — the change is real on the runtime, or it is not real

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
| `LANDED` | observed in effect at the runtime, after the revert window | requires a runtime observation, not a source read |
| `REVERTED` | landed, then undone — by a reconciler, a cache, a rebuild, another writer | names what undid it |
| `UNVERIFIED` | could not observe the runtime | **never** rendered as landed, never inferred from the diff |

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
4. **Check for an owner.** Something may reconcile, regenerate, or overwrite this
   — a GitOps controller, a scheduled job, a generator, another writer. If an
   owner exists and was not updated, the change is `REVERTED` on a timer even if
   it is present right now.
5. **Re-observe after the revert window.** A change observed once, immediately,
   has not survived anything. Where an owner exists, observe again past its
   reconcile interval.
6. **Report the verdict with the observation**, never the intent.

## Boundaries

- **Never infers landing from the diff, the commit, the PR, or the log line.**
  Those are records of intent to change, not evidence of change.
- **Never accepts a green check as landing** unless the check itself observed the
  runtime. Most do not.
- **Never repairs.** If it did not land, that is a finding; re-applying is a
  separate act.
- **Never reports `LANDED` for a subset.** Landed on one of three hosts is not
  landed.

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
| owner exists, reconcile interval unknown | `UNVERIFIED (revert window unknown)`; do not claim survival you did not wait for |
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

The last one is not hypothetical. In this estate a positive control passed while
production was broken, because the control created a symlink and every production
link was a Windows junction, for which the test returned False.

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
which artifact each runtime actually loads, known reconcilers and their
intervals, and the commands that observe them. This file must stay free of them.
