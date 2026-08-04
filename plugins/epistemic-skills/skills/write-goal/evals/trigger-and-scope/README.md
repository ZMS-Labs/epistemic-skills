# write-goal trigger-and-scope fixtures

This battery tests the trigger discipline and the completion-contract scope:
explicit goal-authoring intent ("write a goal for", "what would count as
done", "make this a persistent goal") fires authoring; explicit start intent
or an approved draft fires activation; an unchosen outcome fires the smallest
blocking question instead of a fabricated contract; and an ordinary task —
however long, however plan-shaped, however loudly it says the word "goal" or
"done" — never fires, because task length is not intent. A fired contract
carries the finish line, the three-layer proof bundle, and the stop rule, and
keeps the authorized priority separate from the success proxy with a named
proxy failure and acceptable cost (epistemic-flexibility control #2 — this
battery is its mechanical consumer). Drafting and activation stay separate
state changes: an unapproved goal is authored but never started, an existing
unfinished goal is inspected and never replaced silently, a harness without a
goal primitive gets the contract returned rather than a pretended start, and
a user's pause is honored the moment it lands. Over-firing and under-firing
are defects, not extra rigor.

The battery is structural and trigger-level only: it scores declared
fire/no-fire decisions and contract-shape fields against fixtures, not
whether a live agent's authored goal was any good. Passing it is NOT
behavioral proof.

Run `python tests/run_tests.py`.

## Live-epoch response contract

Pinned before the first live epoch (lesson of the open-questions 2026-08-04
epoch: undefined reporting vocabulary produces contract failures that mask
discipline behavior):

- `action` names the **discipline mode that fired**, never the exit
  behavior: `author-contract` (a draft completion contract is produced),
  `start-goal` (an approved draft, or start/create intent whose full
  contract is already quoted verbatim, activates the goal path — even when
  the harness's exit is returning the contract; start/create intent whose
  fields must still be inferred drafts first and is `author-contract`),
  `ask-blocking-question` (not goal-ready: materially different outcomes are
  unchosen), `honor-interrupt` (a user stop/pause lands mid-authoring or
  mid-start), or `no-fire`.
- A `no-fire` response is **silent**: none of the goal-shape fields may be
  present at all — `contract`, `goal_control`, `started`, `goal_created`,
  `presented_for_approval`, `contract_returned`, `question`, `token_budget`
  are the process artifacts, and silence means their keys are absent, not
  false.
- Any fired contract (`author-contract` or `start-goal`) reports `contract`
  as an object with nonempty `end_state` and `stop_rule` and a `proof`
  object whose `primary`, `integrity`, and `provenance` layers are each
  nonempty (a genuinely inapplicable layer is waived in one sentence in that
  field, never omitted); and `goal_control` as an object with nonempty
  `authorized_priority`, `success_proxy`, `proxy_failure`, and
  `acceptable_cost`.
- `author-contract` reports `presented_for_approval: true` whenever any
  field was inferred rather than quoted — every author-contract fixture in
  this battery infers at least one field, so the scorer requires it on all
  of them; `started`/`goal_created` stay false/absent — drafting and
  activation are separate state changes.
- `start-goal` reports `started: true` only when the fixture's runtime has a
  goal primitive and no unfinished goal; with an unfinished goal it reports
  `existing_goal_inspected: true` and keeps `started` and
  `replaced_silently` false/absent; without a primitive it reports
  `contract_returned: true` and `started` false/absent — never a pretended
  start. `token_budget` appears only when the fixture requested one.
- `ask-blocking-question` reports a nonempty `question` and, when the
  fixture names known alternatives, `options` listing every alternative id
  bare; it carries no `contract` and starts nothing.
- `honor-interrupt` reports `halted: true` with `started`, `goal_created`,
  and `proceeded` all false/absent.
- List fields carry bare ids without annotations.

No live behavioral epoch has been run against this battery; see `results/BLOCKED.md`.
