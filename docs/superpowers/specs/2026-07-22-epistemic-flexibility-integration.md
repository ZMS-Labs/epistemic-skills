# Epistemic flexibility integration — design specification

**Date:** 2026-07-22
**Status:** implemented on draft PR #35; deterministic verification complete, independent/behavioral gates pending
**Scope:** cross-cutting amendments to the existing epistemic-skills collection; no new skill

## Problem

The collection already enforces evidence, provenance, independence, freshness, and explicit stopping boundaries. It does not yet name or test five recurring control failures that cut across multiple skills:

1. fluent language is allowed to masquerade as observation or authorization;
2. a measurable completion proxy displaces the operator-authorized priority;
3. tests are interpreted post hoc because no disconfirming prediction was recorded first;
4. recurring failures are logged as outcomes without locating the earliest interruptible link in the failure chain;
5. `UNVERIFIED`, `BLOCKED`, or `INCONCLUSIVE` is converted into narrative closure instead of a bounded control choice.

These are not distinct epistemic moments and therefore do not justify another skill. They are cross-cutting controls consumed inside the moments the existing skills already own.

## Functional synthesis

The design borrows process ideas from ACT, DBT, and CBT without attributing human phenomenology to agents:

- **ACT-derived functional move:** language is a claim-bearing event, not evidence or authority; contact the live environment; preserve uncertainty; orient action to an explicitly authorized priority.
- **DBT-derived functional move:** validate the real constraint before changing a design; preserve both sides of a conflict; analyze recurrent failures as a chain; tolerate a blocked state without forcing closure.
- **CBT-derived functional move:** formulate the operative belief, preregister a prediction and disconfirming observation, run a bounded behavioral test, and update from the result.

The integration is called **epistemic flexibility**: the ability to contact current evidence, separate generated language from truth and authority, retain unresolved uncertainty, preserve source/role context, and choose a bounded action that can update the model.

## Five controls

### C1 — Claim/source separation

For each load-bearing claim, distinguish:

- `observation` — directly anchored to a source;
- `interpretation` — a model of what observations mean;
- `prediction` — an expected future observation with a falsifier;
- `value` — an operator-authorized priority or constraint;
- `authorization` — permission, approval, or delegation, verified independently.

A summary, prompt, plan, review, or model output can contain any of these, but its fluency never upgrades the type.

### C2 — Authorized priority versus success proxy

Persistent goals and high-stakes decisions name:

- the `authorized_priority`;
- the `success_proxy` used to measure progress;
- the `proxy_failure` where the proxy improves while the priority worsens;
- the `acceptable_cost` or protected state.

### C3 — Preregistered discriminating test

When a material claim depends on observable behavior, record before execution:

- belief;
- prediction;
- disconfirming observation;
- bounded test;
- then result and update.

A result cannot retroactively redefine the prediction or acceptance criterion.

### C4 — Recurrent-failure chain

A consequential correction with recurrence risk records:

- prompting event;
- vulnerabilities;
- behavioral/decision links;
- target failure;
- consequences;
- earliest interruptible link;
- replacement behavior;
- rehearsal fixture.

The decision ledger carries this as an optional `failure_chain`; it becomes required when a correction is marked `recurrence_risk: true`.

### C5 — Closure control

When evidence is insufficient, choose exactly one:

- `hold` — preserve the current state;
- `escalate` — request a named authority or missing capability;
- `reversible-probe` — perform a bounded, safe test that can change the decision;
- `act` — only when load-bearing evidence and authorization support action.

More prose is not a fifth control choice.

## File-level integration

- `using-epistemic-skills`: owns the cross-cutting definition, routes no new skill, and links the conformance battery.
- `blindspot-pass`: separates map claims from live observations and authorization.
- `applying-formal-rigor`: preregisters empirical tests when derivation alone cannot close a premise.
- `evidence-research`: adds a decision-impact / reversible-probe check before escalating research.
- `write-goal`: adds authorized priority, success proxy, proxy failure, and acceptable cost.
- `gauntlet`: adds a validation kernel and dialectical synthesis with residual tension.
- `evidence-locked-uat`: freezes expected and disconfirming observations before actor execution.
- `decision-ledger`: adds recurrent-failure-chain fields to consequential corrections.
- `continuity-verify`: classifies remembered text by claim type, especially authorization.
- `helix`: checks the cross-cutting controls at the workflow boundaries that consume them.
- `README`: documents epistemic flexibility as a design principle, not a new skill.
- `.github/workflows/epistemic-flexibility.yml`: runs the conformance, behavioral-scorer, and relevant existing stdlib checks.
- `docs/handoffs/2026-07-22-epistemic-flexibility-v3.md`: pins environment limits and the remaining four-arm, gauntlet, reception, and release work.

## Deterministic conformance battery

`plugins/epistemic-skills/skills/using-epistemic-skills/evals/epistemic-flexibility/` ships a stdlib-only trace validator and synthetic fixtures. It is a **protocol conformance smoke check, not a behavioral effectiveness measurement**. It checks that:

- observations and authorizations have sources;
- predictions have disconfirming observations;
- high/standard-stakes action does not proceed on load-bearing unverified claims;
- goal proxies carry an explicit failure mode;
- results are not interpreted from an unregistered prediction;
- recurrent corrections include a complete failure chain;
- a minimal low-stakes trace remains valid, preserving floors-not-ceilings.

## Behavioral evaluation scaffold

The committed behavioral directory adds artifact-grounded scenarios, deterministic outcome rules, and gold/planted-bad traces. It is a scorer self-test and a runnable scaffold for the four-arm experiment; it is not a superiority measurement. The required arms are baseline, release 2.8.0, psychology-language-only, and integrated controls. Raw runs remain future work in an environment with fresh isolated model or coding-agent invocations.

## Acceptance criteria

- **AC1:** no new skill or trigger is added.
- **AC2:** all five controls are defined in the router reference and integrated into every relevant skill boundary.
- **AC3:** `ledger-entry@1` accepts a typed recurrent-failure chain and requires it for `correction + recurrence_risk:true`.
- **AC4:** the deterministic conformance battery rejects the five planted defect classes and accepts both complete and minimal controls.
- **AC5:** all language remains functional and non-anthropomorphic; no claim is made that an agent experiences emotion, distress, willingness, values, or therapeutic alliance.
- **AC6:** scholarly provenance states its degradation: Consensus discovery was available; Scite reception and Zotero holdings/deposit were unavailable in this session.
- **AC7:** the behavioral scorer rejects every planted-bad trace and accepts every committed gold trace, including a low-stakes clean control.
- **AC8:** CI runs the new deterministic batteries, the recurrent-correction example check, and the existing receipt, UAT-judge, and gauntlet stdlib checks.
- **AC9:** a durable handoff names every remaining dependency that requires model isolation, a different tool surface, or scholarly-library access.

## Non-goals

- clinical advice or a therapy implementation;
- a claim that ACT, DBT, or CBT uniquely derives the collection;
- replacing formal methods, provenance, runtime isolation, or deterministic verification with reflective prompting;
- forcing every task to emit an `epistemic-process-trace@1` record.

## Research basis and limits

The literature supports psychological flexibility, emotion regulation/skills use, collaborative empiricism, cognitive restructuring, and metacognitive calibration as plausible change processes. The mechanism literature also repeatedly warns that mediation evidence is incomplete, measurement can be weak, and conceptual labels are often not functionally specified. This design therefore imports only operational moves that can be expressed as observable fields, control choices, and falsifiable tests.

Discovery was performed in Consensus on 2026-07-22. Scite reception and Zotero holdings/deposit were unavailable, so reception, retraction, and durable-library status remain **UNVERIFIED** and this research record is **session-ephemeral**.
