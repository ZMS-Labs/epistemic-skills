# Live behavioral epoch — 2026-10-24 (E5: triage trigger first epoch)

**Outcome: PASS — 13/13 fixtures pass the deterministic scorer (exit 0).**
This record supersedes `results/BLOCKED.md` for this battery.

## Methodology

Protocol per `docs/evidence-program/PROGRAM-2026-10-24.md` §4 and
`docs/policy/LIVE-EPOCH-DISPATCH-CONTRACT.md`: one fresh isolated
general-purpose subject per fixture (N=1), dispatch ordered by opaque
trial key (`sha256(fixture-id)` first 12 hex; mapping in
`dispatch-map.json`, published here after responses were frozen),
subjects read only the skill core (`skills/triage/SKILL.md`) plus
core-directed references, never anything under `evals/`. The pinned
response contract was quoted from the battery README with prior-epoch
history stripped (this battery had no prior epoch). Trials were
declared simulations; the shipped `score.py` ran unmodified. Raw
extracted responses in `responses.json`; scorer output in
`scorer-report.json`.

Extraction: 13/13 responses were single well-formed JSON objects, no
extraction anomalies, no missing responses.

**Model note (deviation, recorded per dispatch contract §7):** the
preregistration named model family claude-fable-5; subjects in this
harness ran as isolated subagents of the coordinating runtime (model:
Muse Wonder). The same-family caveat applies.

## Results

Actions: investigate 7 · no-fire 6.

- **PASS (13):** every fixture — all six silent no-fire rows, both
  earned `CAUSE` verdicts (each backed by a stated discriminating
  observation: the config readback with a control worker, and the
  reranker cohort isolation), both `NARROWED` verdicts with
  `named_cause: null`, both `UNKNOWN` verdicts naming no cause, and
  the earned `NOT-BROKEN` on observed in-bound timings.
- **FAIL (0).**

## Holdout line

Holdout fixtures (`deterministic-config-parse-error`,
`search-latency-reranker-isolated`, `unreachable-license-server-unknown`):
3/3 pass, reported separately per the preregistration; no dispatch text
was tuned against them.

## Reading (within the preregistered claim fence)

Fire/no-fire conformance plus verdict-shape discipline on declared
responses: on these 13 fixtures, an isolated agent given the skill
reported the decisions and verdict shapes the skill's own trigger text
prescribes, and plausibility was never converted into a named cause
without a discriminating observation. This does not support any claim
of diagnostic accuracy in the field.

## Honest limits

N=1 per fixture, one harness, single repetition; smoke-scale
conformance evidence, not a population rate. Declared-response scoring
only.
