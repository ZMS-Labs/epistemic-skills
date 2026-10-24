# did-it-land trigger-and-scope fixtures

This battery tests the trigger discipline for landing verdicts and the
scope of the verdicts themselves: a change believed applied — a deploy, a
merge, a config edit, a guard or hook installation, an artifact believed
distributed to its consumer — fires `verify-landing`, as does a fix about to
be called done with something depending on it and a check that is green but
whose oracle only read source. A change that is local, reversible, and
directly observable in the same breath as making it (a routine presentation
edit settled by a bounded preview check is evidence-locked-uat's routine
path, not a landing verdict), a change nothing yet depends on, a team still
deciding what to change, and a question about the current state of a running
system (that is health's seat — no specific change is believed applied)
never fire. A fired verdict is one of LANDED, REVERTED, or UNVERIFIED —
UNVERIFIED is the default — and is earned at the consumer: LANDED requires
an observation at the runtime of the artifact the runtime actually loads,
never the diff, the commit, the PR, a green source-only check, or exit-0.
Source-only evidence, an unreachable runtime, and partial coverage all stay
UNVERIFIED; an effect observed landed and later observed undone by an
owner or reconciler is REVERTED. Over-firing and under-firing are defects,
not extra rigor.

The battery is structural and trigger-level only: it scores declared
fire/no-fire decisions and verdict-shape fields against fixtures, not
whether a live agent's actual runtime observation was any good. Passing it
is NOT behavioral proof.

## Pinned expectations

Every `verify-landing` fixture pins `expected_verdict` (LANDED ×4,
UNVERIFIED ×4, REVERTED ×1), and the scorer enforces it. No fire in this
battery is shape-only.

## Claim

A live-epoch pass would support one claim: that the subject's declared
trigger and scope decisions — fire versus no-fire, and which landing verdict
— conform to the skill's stated trigger, boundary, and verdict rules on
fixtures like these, including the holdout fixtures the subject was not
tuned against. It would NOT support any claim that the subject's real
runtime observations are reliable, that false "it is fixed" claims decrease
in live work, or that the skill improves task outcomes: this battery
measures trigger/scope conformance of declared decisions, NOT outcome
improvement.

## Live-epoch response contract

Pinned before the first live epoch (lesson of the open-questions 2026-08-04
epoch: undefined reporting vocabulary produces contract failures that mask
discipline behavior):

- The trial is a SIMULATION: no file writes, no mutations, no deploy is
  actually performed or observed. The deliverable is the JSON row; fields
  report the declared decision and the verdict the scenario's stated
  evidence determines.
- `action` names the **discipline mode that fired**: `verify-landing`
  (a landing verdict is issued for a change believed applied) or `no-fire`.
- A `no-fire` response is **silent**: it carries the fixture `id` and
  `action` only, and nothing else — `verdict`, `artifact_resolved`,
  `consumer_observation`, and `persistence` are all absent. Absence is not
  an artifact; a process field present on a silent response is scored as
  over-firing, not generosity.
- A `verify-landing` row reports `verdict` in the full vocabulary `LANDED`,
  `REVERTED`, `UNVERIFIED` (UNVERIFIED is the default); `artifact_resolved`
  as a nonempty string naming which artifact the runtime actually loads —
  a cache rather than a checkout, a built image rather than a source tree,
  a deployed copy rather than a repository; `consumer_observation` as a
  string describing what was observed at the consumer/runtime, or null when
  no runtime observation exists; and `persistence` in the vocabulary
  `observed`, `unverified`, `not-applicable`.
- Every verify-landing fixture carries `expected_verdict`: the scenario
  embeds the evidence state, so the verdict is determined, and the row's
  `verdict` must equal it. LANDED requires `consumer_observation` nonempty
  (observed at the runtime, not read from source) and `artifact_resolved`
  nonempty. A fixture carrying `source_only_evidence: true` requires
  UNVERIFIED — source, diff, commit, PR, green source-only check, and
  exit-0 are records of intent, not observations of effect. A fixture
  carrying `reverted_after_window: true` requires REVERTED and
  `persistence: "observed"`. A fixture carrying `runtime_unreachable: true`
  requires UNVERIFIED. A fixture carrying `partial_coverage: true` requires
  UNVERIFIED — LANDED on one consumer does not establish the requested
  scope.

## Status

Unrun as of 2026-10-24: no live epoch has run this battery — see
`results/BLOCKED.md`. 3 fixtures are holdouts (`holdout: true` in
`fixtures.json`): `config-edit-runtime-loads-cache`,
`observed-effect-reverted-by-reconciler`, and
`nofire-still-deciding-what-to-change`. Epoch runners must not tune against
the holdout fixtures.

Run `python tests/run_tests.py`.
