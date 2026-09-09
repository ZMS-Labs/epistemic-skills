> **Applies to:** epistemic-skills v7.0.0
>
> **Canonical source:** [released Decision Ledger source](https://github.com/ZMS-Labs/epistemic-skills/blob/v6.0.0/plugins/epistemic-skills/skills/decision-ledger/SKILL.md)
>
> **v3.4.0 amendment:** 3.4.0 adds outcome reviews with the anti-hindsight boundary (prediction and result recorded as separate untouched facts; generalized lessons require operator approval) and prototype-finding capture. The tagged SKILL.md is the sole contract; this page defers to it where they differ.
>
> **v4.0.0 amendment:** decision-ledger absorbs [continuity-verify](Skill-Continuity-Verify) as its **resume mode** (a third, pre-arc trigger; the mode name continuity-verify survives; method at [`reference/mode-resume.md`](https://github.com/ZMS-Labs/epistemic-skills/blob/v6.0.0/plugins/epistemic-skills/skills/decision-ledger/reference/mode-resume.md)), and **outcome arrival is a first-class second trigger** (promoted 2026-08-04 by the creation-gate revisit): the skill fires when a ledgered decision's outcome becomes observable, not only when a decision is made. The tagged v4.0.0 SKILL.md is the sole contract; this page defers to it where they differ.

# Decision Ledger

## What it does

Decision Ledger protects the persistence moment: when later work will rely on a consequential decision, load-bearing assumption, or recurrent/operator correction, it ensures that judgment has one durable, re-anchorable home. The cheapest correct result is often reusing an adequate plan, ADR, issue, PR description, goal contract, or formal-rigor record rather than creating a parallel ledger.

Ledger entries are append-only prior judgment. They inform future consumers but never authorize action, establish truth, or carry a GO/NO-GO verdict.

## Use it when

Use it only when both conditions hold:

- A named downstream consumer—such as a future session, Continuity Verify, a Gauntlet dossier, Write Goal, or a later plan/implementation stage—will rely on the decision, assumption, or correction.
- No existing durable artifact already provides an outcome-shaped statement, resolvable provenance, current subject/revision where relevant, and a falsification, expiry, or review condition.

A recurrent correction fires when the failure can recur outside the artifact just fixed and future work needs the failure chain and replacement behavior.

## Do not use it when

- The routine-work fast path applies or a reversible self-contained choice has no future consumer.
- The corrected artifact and test fully embody a local non-recurring lesson.
- An assumption discharges entirely inside the current bounded check.
- An adequate durable artifact already satisfies the consumption contract.
- You are consuming prior decisions, recording Gauntlet run telemetry, or trying to turn a decision entry into authority.

No-op outcomes are silent: no skip line, duplicate entry, or end-of-session narrative database.

## Inputs and prerequisites

Identify the named future consumer and inspect the durable artifact it will actually read. Confirm whether the repository has adopted `.ledger/entries.jsonl`, another decision store, or a different adequate home. A local overlay may bind the substrate.

For a new entry, gather the outcome-shaped statement, resolvable evidence or derivation coordinates, subject/revision if relevant, superseded IDs, a concrete `revisit_when` condition, and durability status. If the correction can recur, gather the prompting event, vulnerabilities, ordered failure links, target failure, consequences, earliest interruptible link, replacement behavior, and rehearsal fixture.

## Normal workflow

1. Reuse before creating. If an existing artifact satisfies the future consumer, return that stable coordinate and stop.
2. Otherwise classify the record as `decision`, `assumption`, or `correction`.
3. Form one `ledger-entry@1` with required fields: `entry`, `id`, `at`, `type`, one-sentence `statement`, resolvable `because`, `supersedes`, `revisit_when`, and `durability`.
4. For recurrent corrections, set recurrence risk and include the complete failure chain, earliest interruption, replacement behavior, and rehearsal fixture.
5. Append under single-writer or locking discipline to the narrowest durable substrate the consumer already reads. Do not create a new `.ledger/` beside an adequate ADR or issue system without operator choice.
6. If no durable substrate is reachable, write session-only state and emit a named durability-gap record.
7. On later consumption, walk the acyclic supersedes graph to its unique head, honor `revisit_when`, and re-anchor every load-bearing fact.

## Outputs and durable artifacts

The output is exactly one durable coordinate: either an existing adequate artifact reference or a new append-only `ledger-entry@1`. A session-only entry is an explicit degraded result and must name the durability gap.

Corrections never edit history; a new entry links to superseded entries. The graph must be acyclic, have one head, and contain no dangling IDs. `revisit_when` provides the review/GC horizon. Ledger entries deliberately carry no trust-contract receipt, `valid_while`, or valid-until claim.

## Boundaries and failure modes

- Chat is not a durable decision home.
- `because` must contain resolvable coordinates, not narrative assurances.
- A malformed or unlinkable supersedes chain fails closed; every entry on it is stale-by-construction.
- A schema-valid verdict or instruction is still a human-review failure; schema validation does not enforce the non-authorizing boundary.
- Entry count is not success. Both missed consequential gaps and unnecessary duplicates are failures.
- This ledger is not `skills/gauntlet/runs/ledger.jsonl`, which stores non-governing review-run telemetry.

## Example prompts

- “We chose the queue-backed design in the committed formal record. Check whether that record already gives the future migration plan enough provenance and a revisit condition; do not duplicate it if it does.”
- “The operator corrected a recurring tendency to trust stale mirrors. Record the full failure chain, earliest interruptible link, replacement behavior, and rehearsal fixture.”
- “This local variable name was changed and tested. Apply the no-op gate and create no ledger artifact.”

## Related skills and handoffs

- Resume mode (the former [Continuity Verify](Skill-Continuity-Verify)) consumes ledger entries as leads and re-anchors them on resumption.
- [Resolve](Skill-Resolve)'s derivation records (the former [Applying Formal Rigor](Skill-Applying-Formal-Rigor)), [Write Goal](Skill-Write-Goal), and committed plans may already be adequate durable homes.
- [Gauntlet](Skill-Gauntlet) may consume a decision coordinate in its dossier, but its run telemetry is a separate ledger.
- [Using Epistemic Skills](Skill-Using-Epistemic-Skills) treats this as a retrospective, cross-cutting trigger rather than an arc stage.

## Canonical sources and evidence

- [Decision Ledger source at v4.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v4.0.0/plugins/epistemic-skills/skills/decision-ledger/SKILL.md)
- [Resume mode method at v4.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v4.0.0/plugins/epistemic-skills/skills/decision-ledger/reference/mode-resume.md)
- [`ledger-entry@1` schema at v4.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v4.0.0/plugins/epistemic-skills/skills/decision-ledger/reference/ledger-entry.schema.json)
- [Recurrent correction example at v4.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v4.0.0/plugins/epistemic-skills/skills/decision-ledger/reference/example-correction-with-chain.json)
- [Reference validation and human-review boundary at v4.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v4.0.0/plugins/epistemic-skills/skills/decision-ledger/reference/README.md)
- [Proportionality fixture suite at v4.0.0](https://github.com/ZMS-Labs/epistemic-skills/tree/v4.0.0/plugins/epistemic-skills/skills/decision-ledger/evals/proportionality)
