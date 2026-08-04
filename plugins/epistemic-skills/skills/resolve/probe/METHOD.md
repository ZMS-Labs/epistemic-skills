<!-- resolve instrument: probe (throwaway-prototyping) — consolidated into resolve (v4.0.0, 2026-08-04); this file is the instrument's full method, formerly its standalone SKILL.md -->


# throwaway-prototyping — build to answer, then throw it away

Some decisions are cheapest to resolve empirically: build the thinnest thing
that makes the answer observable, observe it, record the answer, and delete
the build. The prototype is an *instrument*, not a first draft. This is the
constructive complement of blindspot-pass (which only reads) and the concrete
form of the "bounded reversible probe" closure control: when evidence is
insufficient and more prose will not close the uncertainty, a disposable
build is the honest next move.

The failure this skill prevents is promotion: prototype code quietly becoming
production code, carrying zero tests, zero design, and the false authority of
"it already works."

Provenance: distilled from the "prototype" patterns in ConnorGriffin/skills
(MIT) and the Pocock-framework community synthesis; re-derived and hardened
here (the disposal contract is the load-bearing addition).

## The contract (all four, before building)

1. **One named question.** The prototype answers exactly one decision-relevant
   question, written down first, with the observation that would answer it
   each way. No question → it is not a prototype, it is unplanned work.
2. **Disposal is declared at birth.** The build lives in a throwaway location
   (scratch branch, scratch dir, spike worktree) that cannot be merged by
   accident. Its lifetime ends when the answer is recorded.
3. **The answer outlives the build; the build does not outlive the answer.**
   Before deletion, the finding is captured durably — decision-ledger entry,
   ADR, or the owning tracker item — with what was built, what was observed,
   and what was decided. Deleting an unanswered prototype is waste; keeping
   an answered one is a landmine.
4. **Never promote.** Prototype code is never merged, adapted-in-place, or
   "cleaned up into" the real implementation. The real implementation is
   rebuilt under the normal discipline (tests, review, design); it may copy
   *ideas* freely and lines only with deliberate review. "It already works"
   is the rationalization to refuse: it worked as an instrument, under no
   contract.

## Variants

- **Logic probe** — a terminal-runnable state explorer for a behavioral or
  algorithmic question (fastest loop; no UI).
- **Comparative variants** — N thin builds of rival options, differing on the
  decision axis only. Distinctness gate: variants differing only in
  cosmetics are ONE variant. (Feeds gauntlet option-sets: a built option is
  evidence, a described one is hypothesis.)
- **Integration probe** — the thinnest end-to-end path through a doubted
  seam (does A actually talk to B), stubbing everything off-axis.

## Where this sits

| Slot | Skill | Relation |
|---|---|---|
| The question came from an option set | gauntlet (generator) | Its option-set contract names the cheapest discriminator; when that is a build, this skill runs it |
| The question came from the decision map | wayfinding | A frontier decision whose cheapest resolution is "prototype" dispatches here; the answer resolves the node |
| Recording the answer | decision-ledger | The capture in contract clause 3 is a ledger trigger — the prototype's finding is a consequential decision input |
| The real build afterward | workflow layer (TDD, plans) | Owns the production implementation; receives the *answer*, never the code |

## Falsifiable gate

A prototyping episode passed when: the pre-registered question has a recorded
answer with its observation, the throwaway location is gone (or archived
read-only), and no line of it reached a mergeable branch uncommented. Any
prototype found on a mergeable branch is a finding, not a shortcut.

## Common rationalizations

| Rationalization | Why it's wrong |
|---|---|
| "It already works, rewriting is waste" | It worked as an instrument. It carries no tests, no design, and unexamined shortcuts — promotion imports all three invisibly. |
| "I'll keep it around just in case" | An answered prototype is a landmine: the next reader can't tell instrument from implementation. The answer is kept; the build is not. |
| "Let me just build it properly the first time" | Then it is not a prototype — run the normal discipline. Prototyping exists for questions where building properly *first* means building the wrong thing properly. |
| "The prototype question can stay in my head" | An unwritten question drifts toward "whatever the build ends up showing." Pre-register it or you are doing exploratory coding, not answering a decision. |

## Handoff boundaries

Ends at a recorded answer plus a disposed build. Upstream: gauntlet
option-sets and wayfinding frontier decisions supply questions. Downstream:
decision-ledger holds the finding; the workflow layer builds the real thing
from the answer.

## Local overlay

If a `LOCAL.md` exists alongside this SKILL.md, read it after this file — it
binds the protocol to the local environment (scratch locations, spike-branch
naming, archive conventions). An overlay may add bindings and examples; it
never overrides the protocol.
