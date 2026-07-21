---
name: write-goal
description: Author or refine an evidence-bound completion contract for a persistent, multi-turn goal. Use only when the user explicitly asks to create, write, define, refine, or start a goal; asks what would count as done; or needs a durable objective, proof standard, scope boundary, blocker policy, stop rule, or optional token budget before extended work. Do not auto-create goals from ordinary tasks, and do not execute or certify the goal inside this skill.
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
| explicit user intent, de-risked context, and any evidence/design inputs | an approved, evidence-bound goal objective; optionally a started persistent goal | execute the work, judge its result, or call it complete | the runtime's goal executor, then independent verification |

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

Specify all three layers when they are relevant:

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

Revise until the user approves it, unless the user's original request already supplied a
complete contract and explicitly asked to start it.

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
