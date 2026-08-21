> **Applies to:** epistemic-skills v6.0.0
>
> **Canonical source:** [released Open Questions source](https://github.com/ZMS-Labs/epistemic-skills/blob/v6.0.0/plugins/epistemic-skills/skills/open-questions/SKILL.md)
>
> **v3.4.0 amendment:** 3.4.0 adds the frontier discipline for dependent docket items (ask only questions whose prerequisites are answered; recompute per round). The tagged SKILL.md is the sole contract; this page defers to it where they differ.
>
> **v4.0.0 note:** open-questions remains one of the eleven v4.0.0 skills; blindspot-pass, referenced below as the recon owner, was consolidated at v4.0.0 (2026-08-04) into [recon](Skill-Recon) as its brief mode (the seed-input handoff is unchanged in substance). See the [Skill Catalog](Skill-Catalog) for the full mapping; the tagged v4.0.0 sources are the sole contract.

# Open Questions

## What it does

Open Questions is an exhaustive serial clarification interview that gates work. It enumerates every open question whose answer could change the work into a numbered, append-allowed ledger, walks the ledger with the operator one question at a time, and lets work resume only when the ledger is empty and a closing probe surfaces nothing new — or the operator explicitly releases the gate.

Every sibling discipline terminates on something other than exhaustion: sufficiency, approval, a recon ceiling. This skill exists for the case where the operator wants the question set emptied. Its posture is the inverse of Blindspot Pass: where that skill converts questions into falsifiable best-guesses so work can proceed without the operator, this one converts best-guesses back into questions because the operator is present and has asked to decide.

## Use it when

- The operator explicitly asks to be interviewed: "ask me open questions one by one until none remain," "walk me through the open decisions," or equivalent.
- A load-bearing fork is irreversible or high-blast-radius, cannot be safely best-guessed, and the operator is interactively present (the narrow auto-trigger).

## Do not use it when

- A workflow design skill is running its own dialogue; that skill owns design-stage questioning.
- A fuzzy brief needs its initial question list; Blindspot Pass owns recon, and this skill consumes its Questions output as seed input.
- The moment calls for goal-shaping; Write Goal owns that.
- The operator is absent. Park reversible forks on announced best-guess defaults and proceed; hold and escalate an irreversible fork that cannot be safely best-guessed — the interview is never a reason to stall autonomous work, and a default is never a license to cross an un-best-guessable one-way door.

## Two modes, one ledger

**Docket mode** fits a known, finite decision set: present the full enumerated docket upfront — each item with one-sentence context, impact-if-unanswered, and a best-guess default — so the operator can triage, reorder, strike, or accept defaults wholesale, then walk the remainder serially, highest-impact first.

**Cascade mode** fits decisions that beget decisions: a serial laddering interview, one question per message, where answers append announced follow-ups to the ledger.

## Auto-fire scope (v3.2.0)

The full walk-everything-to-empty contract belongs to explicit invocation only. When the skill fires on the narrow auto-trigger, the interview is fork-scoped: it walks only the triggering fork and the questions its answers directly open. If other material questions surface, exactly one closing offer covers them; a declined or unanswered offer defers each one — recorded in the exit stamp's coverage limits and captured in the environment's durable tracker with its best-guess default, never memory-only. The skill ships a deterministic eval battery (`evals/trigger-and-scope/`) with parody polarity controls for over-firing, scope creep, and lost deferrals.

Modes may switch mid-run; the ledger is continuous across the switch.

## Termination

Work resumes when the ledger is empty AND one closing probe ("anything material I haven't asked about?") yields nothing new, or when the operator says "proceed." On release, remaining items are parked on their announced best-guess defaults — parked and struck items are recorded, never silently dropped. An un-best-guessable irreversible item with the operator gone is held and escalated, never defaulted through.

## Output

Exit emits the collection's canonical 4-field stamp — `subject.ref` (the gated stage and its ledger), `subject.revision` (the ledger's final state), `valid_while` (`session-continuous`), `coverage_limits` (parked and struck items with their applied defaults or strike rationale) — plus a one-line interview summary of mode(s) used and asked/answered count.

## Provenance

The two-mode structure, serial one-per-message walk, and run-length stopping criterion are grounded in the elicitation and saturation literature (structured interviews as the most effective elicitation technique; laddering and probing for answer-begotten questions; base-size/run-length stopping criteria in place of naive exhaustion; late-battery quality decay motivating triage order). The cited evidence run is recorded in the released design spec: [2026-07-29-open-questions-design.md](https://github.com/ZMS-Labs/epistemic-skills/blob/v6.0.0/docs/superpowers/specs/2026-07-29-open-questions-design.md).
