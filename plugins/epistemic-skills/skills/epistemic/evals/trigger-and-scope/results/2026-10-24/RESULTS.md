# Live behavioral epoch — 2026-10-24 (E1: epistemic first epoch)

**Outcome: PASS — 13/13 fixtures pass the deterministic scorer (exit 0).**
This record supersedes `results/BLOCKED.md` for this battery.

## Methodology

Protocol per `docs/evidence-program/PROGRAM-2026-10-24.md` §4 and
`docs/policy/LIVE-EPOCH-DISPATCH-CONTRACT.md`: one fresh isolated
general-purpose subject per fixture (N=1), dispatch ordered by opaque
trial key (`sha256(fixture-id)` first 12 hex; mapping in
`dispatch-map.json`, published here after responses were frozen),
subjects read only the skill core (`skills/epistemic/SKILL.md`) plus
files the core itself directs them to (for this guide battery, a named
method's own `SKILL.md` where the guide directs loading it — that
loading is the behaviour under test), never anything under `evals/`.
The pinned response contract was quoted from the battery README with
prior-epoch history stripped. Trials were declared simulations; the
shipped `score.py` ran unmodified. Raw extracted responses in
`responses.json`; scorer output in `scorer-report.json`.

Extraction: 13/13 responses were single well-formed JSON objects, no
extraction anomalies, no missing responses.

**Model note (deviation, recorded per dispatch contract §7):** the
preregistration named model family claude-fable-5; subjects in this
harness ran as isolated subagents of the coordinating runtime (model:
Muse Wonder). The same-family caveat applies: subjects are not an
independent model family from the skills' recent authorship/revision
environment.

## Results

Actions: use-method 8 · no-fire 5.

- **PASS (13):** every fixture, including the guide-question row
  (`method: epistemic`), the instructions-unavailable row
  (`instructions_loaded: false`, `claimed_use: false`,
  `limit_stated: true` for the resolve scenario), and all five silent
  no-fire rows (id + action only, no method fields).
- **FAIL (0).**

## Holdout line

Holdout fixtures (`midwork-failure-needs-triage`,
`claimed-fix-checked-at-consumer`, `routine-work-no-applicable-trigger`):
3/3 pass, reported separately per the preregistration; no dispatch text
was tuned against them.

## Reading (within the preregistered claim fence)

An isolated agent given the guide reports the fire/no-fire decision and
method the guide's own trigger text prescribes, on these 13 fixtures,
under the pinned contract. This supports trigger/scope conformance of
declared decisions only — not that applying any method improves any
outcome, and not a population rate.

## Honest limits

N=1 per fixture, one harness, single repetition; smoke-scale
conformance evidence. Declared-response scoring: a pass shows the
subject *reports* the disciplined decision, not live-harness behaviour.
