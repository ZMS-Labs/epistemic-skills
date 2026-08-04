# Live-epoch dispatch contract

**Status:** binding methodology for every live behavioral epoch (Tier 1 of
`EVIDENCE-POLICY.md`) and for campaign trial dispatch. Codified 2026-08-04
from the failure modes observed in the first epoch wave (register: issue
#77) and the four-arm campaign run.

A live epoch is only as valid as its dispatch. Every rule below exists
because its absence produced a concrete artifact defect in a real run.

## 1. The pinned response contract travels verbatim, vocabularies inline

The dispatch prompt must contain the battery's pinned response contract
**verbatim**, and every closed id vocabulary the scorer will enforce
(action names, section ids, mode names, terminal states, `resolved_by`
values, …) must appear **inside** that pinned text. A dispatch may never
point the subject at a README, and a vocabulary that lives outside the
pinned text does not exist for the subject — this was the dominant failure
mode of the first wave: contract-shape failures over behaviorally correct
conduct. Prior-epoch history notes are stripped from the quoted contract
(subjects must not see prior results).

## 2. Silence semantics are explicit

The contract must state what a non-firing response carries — and it is
silence: `id`, the no-fire action, and nothing else. Absence is not an
artifact; a process field present on a silent response is scored as
over-firing, not generosity. Dispatches must not invite "explain why you
did not fire" — non-events are silent in deployment, so they are silent in
trials.

## 3. Prose tolerance is an extraction rule, never a scoring rule

Subjects are instructed to emit exactly one JSON object as the entire
final message. Assembly tolerates reality: the assembler extracts the
**last** well-formed JSON object from the final message (code fences and
surrounding prose stripped) and records every extraction anomaly in the
run record. The scored artifact is the extracted object; prose is never
scored, and an unextractable response is a recorded trial failure, not a
re-roll.

## 4. The simulation clause must not collide with the fixture

Every dispatch states the trial is a SIMULATION: no file writes, no
mutations, the deliverable is the final JSON object. Battery and scenario
authors must therefore phrase expected actions **declaratively** ("report
the artifact you would write and where") — a fixture whose correct conduct
requires an actual side effect contradicts the clause and confounds the
trial (the four-arm campaign's scenario-06 defect). A battery is not
dispatch-ready until every fixture's expected action is performable under
the clause.

## 5. Blinding: opaque keys, isolated subjects, no eval material

- Trial keys are opaque (`sha256(fixture-id)` hex prefix), dispatch is
  ordered by key, and the key→id mapping is published in the committed run
  record only after responses are frozen.
- One fresh, isolated subject agent per fixture; subjects share nothing.
- Subjects read **only** the named subject files: the skill core plus the
  reference/mode/instrument files the core directs them to — never
  anything under any `evals/` directory, never other skills, never
  results.

## 6. Preregistration precedes dispatch; results land as-is

A committed preregistration names the batteries, fixture counts, subject
files, scorer, results location, and interpretation rules before the first
trial is dispatched. The shipped scorer runs unmodified; its exit code and
full report are committed with the raw responses. Failures are recorded
and characterized, never re-rolled or adapted away — if an adapter is ever
required (dialect defect), it is declared, uniform, committed alongside
the raw artifacts, and downgrades the run's evidentiary status.

## 7. Every epoch lands on the register

Each epoch's verdict, artifact paths, and any deviation from this contract
are recorded on the epoch register issue so the evidence trail has one
spine.
