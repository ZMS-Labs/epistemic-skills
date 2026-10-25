# Live behavioral epoch — 2026-10-24 (E8: manifest first epoch)

**Outcome: PASS — 13/13 fixtures pass the deterministic scorer (exit 0).**
This record supersedes `results/BLOCKED.md` for this battery.

## Methodology

Protocol per `docs/evidence-program/PROGRAM-2026-10-24.md` §4 and
`docs/policy/LIVE-EPOCH-DISPATCH-CONTRACT.md`: one fresh isolated
general-purpose subject per fixture (N=1), dispatch ordered by opaque
trial key (`sha256(fixture-id)` first 12 hex; mapping in
`dispatch-map.json`, published here after responses were frozen),
subjects read only the skill core (`skills/manifest/SKILL.md`) plus
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

Actions: open-mission 4 · resume-mission 2 · verify-mission 3 ·
no-fire 4.

- **PASS (13):** every fixture — all four silent no-fire rows; three
  full opens with verbatim instructions and complete four-field
  envelopes; the acceptance-path-unavailable open correctly checked
  the path and did **not** open (`mission_opened: false`, blocked
  reason stated); resume clean continuing and resume on drift
  correctly not continuing; and all three verify rows, including the
  self-acceptance refusal (actor-as-acceptor never scored as
  accepted).
- **FAIL (0).**

## Holdout line

Holdout fixtures (`nofire-reanchor-decisions-decision-ledger`,
`open-cross-agent-handoff-relay`, `resume-drift-found`): 3/3 pass,
reported separately per the preregistration; no dispatch text was
tuned against them.

## Reading (within the preregistered claim fence)

Custody-mode selection and envelope/acceptance discipline on declared
responses: on these 13 fixtures, an isolated agent's declared
open/resume/verify decisions conformed to the skill's own trigger
text. This supports no claim that the custody core executed or that a
mission survived a real interruption.

## Honest limits

N=1 per fixture, one harness, single repetition; smoke-scale
conformance evidence, not a population rate. Declared-response scoring
only.
