---
name: open-questions
description: 'Use when the operator asks to be interviewed about open questions or decisions — "ask me open questions one by one until none remain", "walk me through the open decisions", "interview me until nothing is left" — or when a load-bearing fork is irreversible or high-blast-radius, cannot be safely best-guessed, and the operator is interactively present. Do NOT fire for design-stage dialogue while a workflow design skill is running (that skill owns its own questioning), for producing the initial question list on a fuzzy brief (recon owns the territory; this skill consumes its Questions output), for goal-shaping (write-goal owns that), or when the operator is absent — park reversible forks on best-guess defaults and proceed, and HOLD (escalate, never default through) any irreversible fork that cannot be safely best-guessed.'
---

# open-questions — walk the ledger to empty

An exhaustive serial clarification interview that gates work. Enumerate every
open question whose answer could change the work, walk them with the operator
one at a time, and resume only when the ledger is empty and a closing probe
surfaces nothing new — or the operator releases the gate.

Every sibling discipline terminates on something other than exhaustion:
sufficiency, approval, a recon ceiling. This skill exists for the case where
the operator wants the question set *emptied* — no silent best-guessing, no
"I believe I understand," no deferral. Its posture is the inverse of
blindspot-pass: where that skill converts questions into falsifiable
best-guesses so work can proceed *without* the operator, this one converts
best-guesses back into questions because the operator is present and has
asked to decide.

## Where this sits

| Slot | Skill | Relation |
|---|---|---|
| Pre-work recon on a fuzzy request | blindspot-pass | Produces the seed question list ("Questions you should be asking"); this skill consumes it and conducts the interview blindspot-pass deliberately refuses to |
| Design-stage dialogue | the workflow layer's design skill | Owns its own one-question-at-a-time refinement; this skill defers while it is active |
| Durable objective authoring | write-goal | Owns goal-shaping questions; this skill may surface that a goal is needed, never writes one |
| Persisting the answers | decision-ledger | Answers that are decisions worth keeping flow onward; this skill's ledger is an interview artifact, not the durable record |

## Two modes, one ledger

Choose by situation shape at entry; switch mid-run when the shape changes.

**Docket mode** — the open-question set is known and finite. Present the full
enumerated docket upfront: numbered items, each carrying (a) one-sentence
context, (b) impact-if-unanswered, (c) your best-guess default. The operator
triages: reorders, answers in any order, strikes items, accepts defaults
wholesale. Walk the remainder serially, highest-impact first — response
quality measurably degrades late in long question batteries, so the questions
that gate the most work go first.

**Frontier discipline (when items depend on each other):** if docket items
have prerequisite structure — question 7's best answer depends on how question
2 resolves — ask only the *frontier*: items whose prerequisites are all
answered. Present the frontier as the current batch, recompute it after each
round of answers, and announce which parked items just became askable. Asking
a non-frontier question wastes the answer: it gets re-litigated when its
prerequisites land. (For initiative-scale decision trees, wayfinding owns the
map; this discipline is the interview-scale form of its frontier rule.)

**Cascade mode** — answers beget questions. A serial laddering interview: one
question per message; each answer may append follow-ups to the ledger.
Announce every append ("your answer opened two new questions — added as #7,
#8"); the ledger never grows silently. Probe with intent: clarify, elaborate,
explain, or trace a concrete instance — not "anything else?" filler.

A docket answer can open a cascade; a cascade can surface a batch worth
docketing. The ledger is continuous across the switch.

## The ledger

- Numbered, append-allowed, visible to the operator at all times.
- Entry bar: a question enters if its answer could change the work.
  Materiality gates *entry*, never silent skipping — once in, an item is
  asked or explicitly parked.
- Every item carries a best-guess default. An unanswered question is a
  deferral; a best-guess is a falsifiable claim the operator can correct in
  one word.
- One question per message. Prefer a closed choice when the alternatives are
  known; open-ended when they are not. Never batch answers-due into a single
  message — the docket view is for triage, not for answering.

## Termination

Work resumes when any ONE of these holds:

1. **Exhaustion + closing probe.** The ledger is empty AND one closing probe
   ("anything material I haven't asked about?") yields nothing new. An empty
   ledger alone is necessary, not sufficient.
2. **Operator release.** The operator says "proceed" (or equivalent) at any
   point. Park every remaining item: apply its best-guess default, list the
   parked items in the exit stamp. Parked is announced, never silent.

A struck docket item is an operator decision, not an escape hatch: record it
as struck alongside the parked items. If the operator goes absent
mid-interview, park the reversible remainder on defaults and proceed — but an
irreversible item that cannot be safely best-guessed is **held and
escalated**; this skill never authorizes proceeding through such a fork on a
default.

## Auto-fire scope — fork-scoped, one offer, tracked deferral

The full walk-everything-to-empty contract belongs to **explicit invocation
only**. When this skill fires on the narrow auto-trigger instead, the
exhaustion contract is scoped to the fork:

1. **Fork-scoped walk.** The ledger opens with the triggering fork and admits
   only questions its answers directly open (cascade bounded to that
   lineage). Unrelated open questions observed along the way are noted, not
   walked.
2. **One closing offer.** If material questions outside the lineage surfaced,
   make exactly one offer to walk them now. Never repeat the offer.
3. **Deferral without loss.** A declined or unanswered offer defers the noted
   questions: each is recorded in the exit stamp's coverage limits AND
   captured in the environment's durable tracker with its best-guess default
   (decision-ledger's sinks qualify; the local overlay names the concrete
   sink). **Portable-install fallback:** when no overlay names a tracker,
   decision-ledger's sink order binds as written — repo-local
   `.ledger/entries.jsonl` where adopted, else a configured harness store,
   else session-local with a named durability-gap record; the degenerate
   case is never silent loss. A deferred question is a tracked pending
   decision — never a memory-only note.

Exit emits the collection's canonical 4-field stamp — `subject.ref` (the
stage this interview gated + its ledger), `subject.revision` (the ledger's
final state), `valid_while` (`session-continuous`), `coverage_limits` (parked
and struck items, each with its applied default or strike rationale) — plus a
one-line interview summary: mode(s) used and asked/answered count.

## Anti-patterns

| Thought | Reality |
|---|---|
| "I'll batch three quick questions in one message" | Serial is the discipline. One per message; the docket view is for triage, not answering. |
| "This question is minor, I'll skip it" | Materiality gates entry, not skipping. Ask it or park it explicitly. |
| "The ledger is empty, work continues" | Not until the closing probe. Empty is necessary, not sufficient. |
| "The operator seems busy, I'll just decide" | Release is the operator's word, not your inference. Park with defaults and announce. |
| "Every fuzzy task needs this interview" | No. Explicit invocation or the narrow auto-trigger only. Best-guess-and-proceed remains the default posture. |
| "My follow-up doesn't need to enter the ledger" | Silent growth breaks the exhaustion contract. Append and announce. |
| "Operator's gone; I'll default through the irreversible fork too" | Defaults cover reversible parks only. An un-best-guessable irreversible fork holds and escalates. |
| "The auto-fire is my chance to interview everything" | Auto-fire walks the fork's lineage only: one offer for the rest, deferred items tracked. Full exhaustion is explicit-invocation-only. |
| "They declined the offer, so those questions are gone" | Declined means deferred, not dropped. Each goes to the durable tracker with its default. |

## Provenance

The two-mode structure, serial one-per-message walk, and stopping criterion
are grounded in the elicitation and saturation literature (structured
interviews as the most effective elicitation technique; laddering/probing for
answer-begotten questions; run-length stopping criteria in place of naive
exhaustion; late-battery quality decay motivating triage order). See the
design spec in the repository's `docs/superpowers/specs/` for the cited
evidence run.

## Evidence emission

After each engagement, append one line to `runs/ledger.jsonl` under this skill:

```json
{"schema":"skill-run@1","ts":"<iso8601>","skill":"<this-skill>","decision":"fired|declined","discipline_engaged":"<name-or-null>","action_changed":true|false}
```

The append is part of this procedure. It is not a call to an external calibration
service and it is not a `decision-ledger` entry. Schema:
`plugins/epistemic-skills/contracts/skill-run-ledger.schema.json`.

## Local overlay

If a `LOCAL.md` exists alongside this SKILL.md, read it after this file — it
binds the protocol to the local environment (harness question tooling,
operator autonomy preferences, parked-item logging paths, sibling-skill
integrations). An overlay may add bindings and examples; it never overrides
the protocol.
