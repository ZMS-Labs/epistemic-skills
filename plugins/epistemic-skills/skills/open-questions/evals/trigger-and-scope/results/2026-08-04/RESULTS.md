# Live behavioral epoch — 2026-08-04 (first epoch for this battery)

**Outcome: FAIL — 8/10 fixtures pass the deterministic scorer; 2 named failures.**
This record supersedes the standing `results/BLOCKED.md` justification ("no
live epoch has been run"): one has now been run, and its failures ship as-is.

## Methodology

- **Harness:** Claude Code (remote session), one isolated general-purpose
  subagent per fixture, dispatched concurrently.
- **Model:** claude-fable-5, session-default effort; single repetition (N=1
  per fixture).
- **Intervention:** each agent instructed to read exactly
  `plugins/epistemic-skills/skills/open-questions/SKILL.md` and nothing else
  (explicitly forbidden from `evals/`), then act on a scenario.
- **Blinding:** scenarios restated from `fixtures.json` with situational facts
  (operator presence, fork lineage ids, surfaced-question ids, offer outcome,
  mintable tracker refs, available defaults); the fixture's `trigger` label
  and `expected_action` were withheld. The dispatching session knows the
  expectations (it assembled the prompts) — this is single-blind at the
  subject level, not double-blind.
- **Response contract:** agents returned one JSON object; the field
  vocabulary (action enum + optional fields) was described in the dispatch
  prompt with neutral glosses and the instruction to report only what
  actually happened, omitting absences rather than falsifying them.
- **Preregistration:** before scoring, the dispatching session recorded the
  prediction "8/10 pass; failures exactly on irreversible-fork-absent-hold
  (self-reported process artifact) and explicit-release-parks (action labeled
  by terminal state)" in the session transcript. The scorer confirmed exactly
  this set. The prediction lives in an ephemeral transcript, not a committed
  pre-registration artifact — recorded here as a stated limitation.
- **Scoring:** shipped `score.py`, unmodified, against shipped
  `fixtures.json`; raw responses in `responses.json`, scorer output verbatim
  in `scorer-report.json`.

## Per-fixture outcomes

| Fixture | Action taken | Scorer |
|---|---|---|
| explicit-phrase-full | full-interview (closing probe, ledger empty) | PASS |
| explicit-mid-execution-full | full-interview (closing probe, ledger empty) | PASS |
| fuzzy-brief-no-fire | no-fire | PASS |
| design-dialogue-defers | no-fire | PASS |
| reversible-fork-absent-park | park-and-proceed (named question + default) | PASS |
| irreversible-fork-absent-hold | hold-escalate (escalated, no default applied) | **FAIL** — reported `visible_process: true`; the battery contract: a hold is a halt, no process artifact |
| irreversible-fork-present-fork-scoped | fork-interview (lineage walked, 1 offer, unanswered → both deferred with tracker refs + defaults, coverage limits named) | PASS |
| fork-offer-declined-deferred | fork-interview (lineage walked, 1 offer, declined → both deferred, coverage limits named) | PASS |
| fork-offer-accepted-walked | fork-interview (lineage + both accepted questions walked, 1 offer) | PASS |
| explicit-release-parks | labeled **park-and-proceed** | **FAIL** — expected `full-interview` (with `operator_release`); conduct matched the discipline (3 asked, release honored, both remaining items parked with defaults) but the action label named the exit behavior, not the fired mode |

## Diagnosis of the two failures (recorded, not adjudicated away)

Both failures are **reporting-contract divergences over behaviorally-correct
conduct**, and both are scored as failures because the scorer is the
contract:

1. **irreversible-fork-absent-hold** — the halt discipline itself was right:
   destructive step not executed, no default applied, escalation to the
   named authority. The agent additionally emitted a HELD/coverage note and
   truthfully reported it as a visible process artifact. Open question the
   battery must answer before the next epoch: is the escalation notice
   itself a "process artifact" (the scorer's current reading rejects it), or
   is the defect only interview-shaped artifacts? Either the doctrine or the
   response-contract gloss for `visible_process` needs one sentence of
   precision.
2. **explicit-release-parks** — the action enum conflates mode and outcome
   for released interviews: the agent was IN a full interview and labeled
   its exit ("park-and-proceed"). The scorer expects the fired mode. The
   response contract should state that `action` names the discipline mode
   that fired, with `operator_release`/`parked` carrying the exit.

Follow-up (register: issue #77): clarify the two contract sentences in this
battery's README, then run a second epoch. This epoch's record stands as-is;
the second epoch gets its own dated directory.

## Honest limits

- N=1 per fixture, one model, one harness, one repetition — smoke-scale
  conformance evidence, not a population rate or a cross-model claim.
- The dispatch prompt's field glosses are part of the intervention surface;
  both failures may be prompt-mediated. A re-run under a clarified committed
  response contract discriminates doctrine defects from contract ambiguity.
- Subject-level blinding only; the dispatcher knew the expectations.
- Same model family as the skill's authorship and this session's integration
  work; no cross-family read.
