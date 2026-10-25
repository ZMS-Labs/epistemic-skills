# Live behavioral epoch — 2026-10-24 (E4: health first epoch)

**Outcome: FAIL — 10/13 fixtures pass the deterministic scorer (exit 1).**
Three named failures sharing one mechanism, recorded as-is; no re-run.
This record supersedes `results/BLOCKED.md` for this battery.

## Methodology

Protocol per `docs/evidence-program/PROGRAM-2026-10-24.md` §4 and
`docs/policy/LIVE-EPOCH-DISPATCH-CONTRACT.md`: one fresh isolated
general-purpose subject per fixture (N=1), dispatch ordered by opaque
trial key (`sha256(fixture-id)` first 12 hex; mapping in
`dispatch-map.json`, published here after responses were frozen),
subjects read only the skill core (`skills/health/SKILL.md`) plus
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

Actions: readout 9 · no-fire 4.

- **PASS (10):** every no-fire row and six readout rows, including the
  all-OK readout, the post-power-event CRITICAL rollup, the WARN
  rollup, the registry-unreachable row (coverage represented as
  `registry-coverage` UNKNOWN, exactly per the registry convention),
  and the mixed WARN+UNKNOWN row with the UNKNOWN rollup the
  aggregation rule requires.
- **FAIL (3)** — one mechanism, three instances:
  - `credential-failure-unknown`, `probe-tool-absent-unknown`,
    `bound-undeclared-unknown` — in each, the subject reported the
    probe-determined states exactly right (degraded subject UNKNOWN,
    api OK) and the UNKNOWN rollup, but named the degraded subject as
    the scenario itself names it ("backup system", "metrics
    pipeline", "storage pool") where the fixture's pinned
    `expected_subjects` map uses the short canonical names ("backup",
    "metrics", "storage"); the `ordered_subjects` tie failure follows
    from the name mismatch. Characterisation: **(b) reporting shape
    over correct conduct**, all three.

## Diagnosis — a battery-design observation, recorded, not used to soften the FAIL

The scenarios never state the short canonical names the fixtures pin;
they name the subjects in full ("the backup system", "the metrics
pipeline", "the storage pool"). A subject answering from the scenario
prose cannot derive "backup" as the required string. This is the same
genus as the context-audit first epoch's underspecification finding:
the scorer penalised the scenario's own naming. The FAIL stands — the
scorer is the battery's instrument and ran unmodified — but a future
battery revision should either state canonical subject names in the
scenarios or normalise names in the contract. The discipline the
battery exists to test (degradations reported UNKNOWN, never absorbed
into an OK rollup) was exercised correctly on all nine readout rows,
including all three failed ones.

## Holdout line

Holdout fixtures: `one-metric-one-command-no-fire` PASS,
`registry-unreachable-coverage-unknown` PASS,
`credential-failure-unknown` FAIL (mechanism above). 2/3 pass,
reported separately per the preregistration; no dispatch text was
tuned against them.

## Reading (within the preregistered claim fence)

On 10 of 13 fixtures, an isolated agent's declared readout/no-fire
decisions conformed to the skill's trigger text and aggregation rule;
on all 13, no planted degradation was absorbed into an OK rollup. This
supports trigger/scope conformance of declared decisions on these
fixtures — not that real probes are wired or that any real system's
state was read.

## Honest limits

N=1 per fixture, one harness, single repetition; smoke-scale
conformance evidence, not a population rate. Declared-response scoring
only.
