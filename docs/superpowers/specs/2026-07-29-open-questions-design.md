# open-questions — design

**Date:** 2026-07-29
**Status:** Approved (operator, this session)
**Type:** New skill (tenth discipline)

## Problem

The operator's recurring instruction — *"ask me open questions one by one until
none remain and then work can continue"* — has no owner in either collection.
An overlap audit against the nearest neighbors found partial coverage and a
genuine gap:

- **brainstorming** (workflow layer) owns serial one-question-per-message
  dialogue, but only at the design stage, and it terminates on the agent's
  *subjective sufficiency* ("once you believe you understand"). Its ambiguity
  rule actively resolves questions *without* asking ("pick one and make it
  explicit").
- **blindspot-pass** deliberately emits 3–5 best-guessed questions and refuses
  to conduct the interview ("this skill ends at understanding"). No consumer
  skill takes that list and walks it with the operator to zero.
- **write-goal** narrows to "only questions whose answers materially change the
  result" and terminates on draft approval, not exhaustion.
- Nothing anywhere (a) terminates on *the open-question set is empty*, (b)
  operates stage-independently — mid-execution, post-handoff, on resumption —
  or (c) maintains an enumerated question ledger that could be emptied.

## Decision

Add one skill, **`open-questions`**, to the epistemic-skills collection: an
exhaustive serial clarification interview that gates work. Enumerate every
open question whose answer could change the work, walk them with the operator
one at a time, and resume work only when the ledger is empty and a closing
probe surfaces nothing new.

One skill, two modes, one ledger (rejected alternative: two sibling skills —
duplicates the ledger/termination machinery and doubles integration cost).

## Evidence base

The design is grounded in an evidence-research run (2026-07-29; Consensus
discovery + Scite reception, filter-level; all load-bearing papers
DOI-confirmed, zero retraction/editorial notices; holdings UNVERIFIED — no
library substrate reachable that session; **deposited 2026-08-04**: the four
load-bearing DOIs live in the operator's Scite collection
`open-questions-design-2026-07-29-3KGVW` (id 379400; issue #63), making the
record durable rather than session-ephemeral):

1. **Interviews are the most effective elicitation technique, structured
   preferentially.** Davis et al. 2006, systematic review
   (doi:10.1109/re.2006.17; reception 5 supporting / 1 contrasting); Dieste &
   Juristo 2011, 30-study aggregation (doi:10.1109/tse.2010.33; 1/0).
2. **Batch and serial elicitation are complementary, not competing.** Obaidi
   et al. 2025 (RE'25): interviews maximize distinct needs per unit time;
   surveys maximize coverage with high redundancy; a hybrid is recommended.
   This is the two-mode structure.
3. **Answers-beget-questions is a named, measured discipline.** Laddering was
   the most productive elicitation technique across domains (Corbridge &
   Rugg 1994; Rugg et al. 2002; confirmed in the Dieste–Juristo aggregation);
   probing has a usable taxonomy (Robinson 2023, DICE: descriptive,
   idiographic, clarifying, explanatory); direct evidence exists for
   conversational agents asking algorithmic follow-ups (Hu et al. 2024).
4. **The saturation literature refutes naive "until none remain" and supplies
   a falsifiable replacement**: a stopping criterion of base size + run
   length + new-information threshold (Guest et al. 2020, PLoS ONE,
   metadata-level; Francis et al. 2010,
   doi:10.1080/08870440903194015 — stop after N consecutive probes yield
   nothing new; reception 49/1). Malterud 2016 "information power"
   (doi:10.1177/1049732315617444; 75/0) grounds why smaller, higher-quality
   dialogues can terminate earlier.
5. **Ordering matters; triage first.** Response quality degrades late in long
   question batteries (Jeong et al. 2022; Berenbon et al. 2024);
   one-question-per-message invites deeper cognition than grid presentation
   (Stefkovics et al. 2022). High-impact/blocking questions go first, and the
   docket view lets the operator reorder before the walk.

## The two modes

**Docket mode** — the open-question set is known and finite. Present the full
enumerated docket upfront: numbered items, each carrying (a) one-sentence
context, (b) impact-if-unanswered, (c) the agent's best-guess default. The
operator triages: reorders, answers in any order, strikes items, accepts
defaults wholesale. The remainder is walked serially, highest-impact first.

**Cascade mode** — answers beget questions. Serial laddering interview: one
question per message; each answer may append follow-ups to the ledger.
Appended items are announced ("your answer opened two new questions — added as
#7, #8"); the ledger never grows silently.

Mode is chosen by situation shape at entry and may switch mid-run: a docket
answer can open a cascade; a cascade can surface a batch worth docketing.

## The ledger mechanic

- Numbered, append-allowed, visible to the operator at all times.
- Every question enters with a **best-guess default** (inherited from
  blindspot-pass discipline: an unanswered question is a deferral; a
  best-guess is a falsifiable claim the operator can correct in one word).
- Entry bar: a question enters the ledger if its answer could change the work
  (materiality gates *entry*, never silent *skipping*).
- One question per message; multiple-choice preferred when the alternatives
  are known. Harness-agnostic in the core; a labeled Claude Code reference
  binding names AskUserQuestion.

## Termination (the skill's identity)

Work resumes when any of:

1. **Exhaustion + closing probe** — the ledger is empty AND one closing probe
   ("anything material I haven't asked about?") yields nothing new (the
   run-length stopping criterion, run length = 1 closing probe).
2. **Operator release** — the operator says "proceed" (or equivalent) at any
   point. Remaining items are then *parked*: logged with their best-guess
   defaults applied, announced in the exit stamp, never silently dropped.

Exit emits a 4-field stamp (per the collection's artifact-shape convention):
mode(s) used, questions asked/answered count, parked items with applied
defaults, and the stage the interview gated.

## Triggers and boundaries

**Fires on (explicit):** the operator's phrase and variants ("ask me open
questions one by one", "interview me until none remain", "walk me through the
open decisions", "/open-questions").

**Fires on (narrow auto):** a load-bearing fork that is irreversible or
high-blast-radius AND cannot be safely best-guessed AND the operator is
interactively present. Otherwise blindspot-pass's best-guess-and-proceed
posture wins — this skill must never become a permission-pause generator.

**Do NOT fire for:** design-stage dialogue while brainstorming is active
(brainstorming owns that; this skill defers); producing the *initial* question
list on a fuzzy brief (blindspot-pass owns recon; this skill *consumes* its
"Questions you should be asking" section as seed input); goal-shaping
(write-goal owns that); sessions where the operator is absent (park and
proceed on defaults instead).

## Integration (wiring)

- **Router** (`using-epistemic-skills`): handoff-boundary row — consumes
  blindspot-pass's Questions section (when present); produces an
  emptied-or-parked ledger + 4-field stamp; hands to whatever stage was gated;
  valid until `session-continuous`. Rows in the routing table, order-of-ops
  arc (cross-cutting, callable at any stage), and count strings (nine → ten
  disciplines).
- **helix**: pairing rows — *before* any gated workflow stage on explicit
  invocation; *inside* dispatch preparation when the narrow auto-trigger
  fires. Matching co-fire bullet.
- **Counts**: nine → ten disciplines, eleven → twelve skills, integration test
  `== 12`, README/GEMINI.md literals, CI step.
- **Core ends with the standard `## Local overlay` section.**

## Rollout

1. **Feature PR** (public repo): SKILL.md + router/helix/README/GEMINI.md
   count-and-table updates + integration-test bump + CI step + this spec.
   Authored LF; DCO signoff; canonical tree only (root `skills/` is a
   symlink — never create real root dirs).
2. **Release PR**: version bump to 3.1.0 across all manifest surfaces, per
   RELEASING.md (version alignment happens in the release PR, not the
   feature PR).
3. **Fleet layering deferred to an issue**: <private-fleet-repo> carries uncommitted
   work on another branch (cross-repo safety blocks touching it), and the
   fleet layer is already five skills behind the public collection
   (helix, write-goal, outsource, continuity-verify, decision-ledger). The
   catch-up issue covers all six, including the `open-questions` LOCAL.md
   (fleet bindings: operator autonomy preferences, AskUserQuestion binding,
   parked-item logging path).

## Anti-patterns (to be included in SKILL.md)

| Thought | Reality |
|---|---|
| "I'll batch three quick questions in one message" | Serial is the discipline. One per message; the docket view is for triage, not for answering. |
| "This question is minor, I'll skip it" | Materiality gates *entry*, not skipping. If it entered the ledger, it gets asked or explicitly parked. |
| "The ledger is empty, work continues" | Not until the closing probe. Empty-ledger is necessary, not sufficient. |
| "The operator seems busy, I'll just decide" | That's operator release only if the operator said so. Otherwise park with defaults and announce. |
| "Every fuzzy task needs this interview" | No. Explicit invocation or the narrow auto-trigger. Best-guess-and-proceed remains the default posture. |

## Out of scope

No changes to brainstorming or any workflow-layer skill. No new agents or
commands. No LOCAL.md shipped (overlay honored, none included). No evals in
the feature PR (an eval harness, if wanted, follows the fixed
`evals/` shape in a later PR).
