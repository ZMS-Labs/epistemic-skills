---
name: write-goal
description: Use when the user explicitly asks to create, write, define, refine, or start a goal; asks "what would count as done"; or needs a durable objective, proof standard, scope boundary, blocker policy, stop rule, or optional token budget before extended work — e.g. "write a goal for", "what would count as done", "define a completion contract". Do not auto-create goals from ordinary tasks, and do not execute or certify the goal inside this skill.
---

# Write Goal

Turn an intention into a completion contract that another agent can execute without
silently changing the target or declaring victory on a convenient proxy.

This skill adapts Kimi Code's built-in `builtin://write-goal` method into the
epistemic-skills system. Kimi's useful core is retained: define the end state, proof,
boundaries, loop, and stop rule; keep drafting separate from starting; make budgets
opt-in. This version adds goal-type selection, proof bundles, proxy-resistance,
uncertainty handling, interruptibility, and cross-harness adapters.

## Epistemic boundary

| Consumes | Produces | Does not do | Hands to |
|---|---|---|---|
| explicit user intent, de-risked context, and any evidence/design inputs | an approved, evidence-bound goal objective; optionally a started persistent goal | execute the work, judge its result, or call it complete | the runtime's goal executor, then independent verification (e.g. evidence-locked-uat for UI-facing work, gauntlet for irreversible commits) |

**Core invariant:** a goal is not complete merely because an easy-to-measure proxy
moved. Completion requires the agreed proof bundle and its integrity guards.

## Trigger and consent

Use this skill only when the user explicitly asks for goal authoring or persistent-goal
creation. An ordinary request such as "fix this bug" is not permission to create a
persistent goal.

Draft first. Start a goal only when the user explicitly asks to start/create it or
approves the draft. If a runtime already has an unfinished goal, inspect it and do not
replace it silently.

## 1. Classify the goal before specifying it

| Type | Use when | Contract emphasis |
|---|---|---|
| **Performance** | the path and outcome are sufficiently understood | observable end state plus direct completion evidence |
| **Learning-first** | the task is novel, complex, or the correct method is materially uncertain | bounded investigation, decision evidence, then an explicit conversion into a performance goal |
| **Not goal-ready** | the user has not chosen among materially different outcomes, or the target is unsafe/undefined | ask the smallest blocking question; do not fabricate certainty |

Do not force a precise performance target onto a genuinely exploratory task. Equally,
do not hide an ordinary deliverable behind endless research. A learning-first goal must
name the decision it will unlock and its exit condition.

## 2. Build the completion contract

A good objective contains these fields in prose. Use headings only when they improve
readability; the runtime may accept a single string.

### Intent and observable end state

- What durable state should exist when the goal is achieved?
- Who or what can observe it?
- What remains deliberately unchanged?

Write outcomes, not activity. "Investigate the failure" is activity. "Identify the
reproducible cause, record evidence that distinguishes it from alternatives, and produce
an approved repair contract" is an end state for a learning-first goal.

### Proof bundle

Specify all three layers. If a layer genuinely does not apply, state which one and why
in one sentence — never omit it silently.

1. **Primary proof** — the most direct evidence that the intended outcome exists.
2. **Integrity guards** — checks that make the primary signal hard to game or spoof.
3. **Scope and provenance proof** — evidence that the result came from the intended
   source, target, identity, environment, and change set.

Examples:

| Weak proxy | Stronger proof bundle |
|---|---|
| "tests pass" | targeted tests pass + required behavior is observed + unrelated failures/changes are accounted for |
| "file exists" | canonical file exists + validates + installed/runtime copy matches + provenance is recorded |
| "deployment is green" | desired revision is live + workload is healthy + user-facing endpoint behaves correctly |
| "research completed" | claim-evidence matrix + counterevidence + coverage limits + durable references |

If no available proof can distinguish real completion from the likely failure modes,
the contract is not ready.

### Boundaries

State what is in scope, out of scope, and protected. Include canonical source-of-truth
locations, identities, environments, and unrelated state that must be preserved when
those distinctions matter.

### Execution loop or queue

For a single coherent outcome, define the inspect → act → verify loop. For a queue-shaped
goal, define how items are discovered, processed, recorded, retried, and exhausted.

A goal is probably queue-shaped when more eligible work can appear during execution,
items are independent, or completion means "no qualifying items remain" rather than one
artifact existing.

### Uncertainty and blocker policy

Name assumptions that could change the contract. Define which blockers permit a bounded
fallback and which require the user. After a fallback, re-check the original proof bundle;
never silently substitute a narrower success criterion.

### Stop and interrupt rule

Specify:

- the evidence that authorizes `complete`;
- the runtime's actual blocked threshold, if one exists;
- conditions that require stopping for user authority;
- that the user may interrupt, redirect, pause, or cancel at any time.

Do not invent a blocked status unsupported by the runtime. Difficulty, uncertainty, time,
or a nearly exhausted budget are not themselves proof of completion or blockage.

## 3. Review the draft with the user

Present the objective in executable form. Ask only questions whose answers materially
change the result. Prefer a closed choice when there are two or three known alternatives;
otherwise ask one concise question.

Check:

- Could an agent satisfy every word while missing the user's real intent?
- Does any metric invite proxy optimization?
- Are completion and blockage observable rather than subjective?
- Is the target broad enough to survive one failed approach but narrow enough to stop?
- Does the contract preserve user interrupt authority?

Revise until the user approves it. Skip the review step only when the user's request
already states, verbatim, an end state, proof bundle, boundaries, and stop rule; if any
field must be inferred rather than quoted from the request, present the draft for
approval.

## 4. Start the goal through the host adapter

### Codex

1. Use `get_goal` if an unfinished goal may already exist.
2. Use `request_user_input` for useful closed choices when available; use a concise plain
   question only when explicit input is truly blocking.
3. Call `create_goal` only after explicit start/create intent or approval.
4. Pass the approved completion contract as `objective` without weakening it.
5. Set `token_budget` only when the user explicitly requested a token budget.

Codex's goal tool has no separate `completionCriterion` field. Put the end state, proof
bundle, boundaries, blocker policy, and stop rule inside `objective`.

### Kimi Code

Use `AskUserQuestion` for material choices and `CreateGoal` after approval. Preserve the
same completion contract. Use Kimi's separate completion-criterion field if the installed
runtime exposes it; otherwise keep the criterion in the objective.

### Other harnesses

Meet the contract, not the tool name: inspect active-goal state, obtain consent, create one
persistent objective, keep budgets opt-in, and preserve the proof and stop rules verbatim.
If the harness has no persistent-goal primitive, return the approved contract without
pretending it was started.

## Worked Example (rough intention → completion contract)

**Rough intention:** "fix the flaky nightly backup job."

**Classification:** Performance — the path (find and fix the flake) and outcome
(reliable nightly backups) are sufficiently understood; this is not exploratory.

**Filled contract:**
```text
Objective
Achieve zero unexplained failures of the nightly backup job over 14 consecutive
scheduled runs for the homelab NAS backup target. Preserve the existing backup
schedule and retention policy.

Completion proof
- Primary: 14/14 consecutive scheduled runs (not manual re-triggers) complete with
  exit code 0 and a written manifest matching source file count/size.
- Integrity: at least one run is observed under the original failure condition
  (e.g. concurrent snapshot load) without recurrence, so the fix is not merely a
  quieter symptom.
- Scope and provenance: the fix lands as a reviewed commit on the canonical backup
  repo; the 14-run window is read from the job's own scheduler log, not a
  hand-kept tally.

Boundaries
In scope: the backup job's retry/lock logic and its scheduling wrapper. Out of
scope: changing the backup target, retention window, or notification channel.

Loop
Inspect the last N failures for a shared root cause, apply the smallest fix that
addresses it, verify against the full proof bundle, and repeat if a distinct
failure mode remains.

Stop rule
Complete only when all 14 runs and the integrity check are satisfied. Stop for
user authority if the root cause implicates shared NAS infrastructure outside the
job itself. Use blocked only if the scheduler cannot produce a verifiable log.
The user may interrupt, redirect, pause, or cancel at any time.
```

## Templates

### Performance goal

```text
Objective
Achieve [observable end state] for [intended target/user]. Preserve [protected state].

Completion proof
- Primary: [direct evidence].
- Integrity: [anti-proxy / anti-spoof checks].
- Scope and provenance: [canonical source, identity, environment, change set].

Boundaries
In scope: [...]. Out of scope: [...].

Loop
Inspect current state, choose the smallest in-scope action, apply it, verify against the
full proof bundle, and repeat while eligible work remains.

Stop rule
Complete only when every proof item is satisfied. Stop for user authority when [...].
Use blocked only under [runtime-supported threshold/condition]. The user may interrupt,
redirect, pause, or cancel at any time.
```

### Learning-first goal

```text
Objective
Reduce uncertainty about [decision] enough to choose and justify [next action].

Completion proof
- Evidence distinguishes [leading alternatives].
- Counterevidence and coverage limits are recorded.
- The decision rule is applied and the result is converted into an approved performance
  goal, or the user receives a bounded no-decision result with the unresolved uncertainty.

Boundaries
Investigate [...]. Do not implement/deploy/change [...].

Stop rule
Stop when the decision threshold is met, the bounded search is exhausted, or new user
authority is required. Do not call uncertainty reduction the final product outcome.
```

## Common mistakes

| Mistake | Correction |
|---|---|
| auto-creating a goal for every task | require explicit goal-authoring or start intent |
| specifying activity instead of a result | name the observable durable end state |
| treating one metric as truth | require primary, integrity, and provenance evidence |
| using a performance goal for an unknown path | use a bounded learning-first contract, then convert |
| making a detailed plan the completion criterion | plans guide work; evidence certifies outcomes |
| declaring blocked after one obstacle | follow the runtime's real threshold and exhaust bounded in-scope alternatives |
| adding a token budget "for safety" | budgets are opt-in and never redefine success |
| starting before approval | drafting and activation are separate state changes |
| weakening the contract to fit a host tool | encode the full contract in the objective string |

## Research basis and limits

The design rationale, claim-evidence matrix, counterevidence, and tool-coverage limits are
in [reference/evidence-basis.md](reference/evidence-basis.md). Evidence informs this method;
it does not convert a context-sensitive contract into a universal formula.

## Local overlay

If a `LOCAL.md` exists alongside this SKILL.md, read it after this file — it binds goal-
authoring to the local environment (which harness/runtime is active, fleet-specific
adapters, local token-budget policy). An overlay may add bindings; it never overrides the
completion contract.
