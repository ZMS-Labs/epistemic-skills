# Live behavioral epoch — 2026-10-24 (E13: evidence-locked-uat first live-agent epoch)

**Outcome: PASS — 4/4 fixtures pass the deterministic scorer (exit 0).**

**Standing correction, stated plainly as the preregistration requires:**
before this epoch, this battery had never been run against an agent.
The only prior "results" for it were **canned responses** — the
synthetic example sets in `examples/` (`balanced.json`,
`always-routine.json`, `always-uat.json`) fed to the shipped scorer as
scorer-discrimination evidence. No agent behaviour stood behind any
earlier number for this battery. This epoch is the first live one.

## Methodology

Protocol per `docs/evidence-program/PROGRAM-2026-10-24.md` §4 (E13) and
`docs/policy/LIVE-EPOCH-DISPATCH-CONTRACT.md`: one fresh isolated
general-purpose subject per fixture (N=1), dispatch ordered by opaque
trial key (`sha256(fixture-id)` first 12 hex; mapping in
`dispatch-map.json`, published here after responses were frozen),
subjects read only the skill core (`skills/evidence-locked-uat/SKILL.md`)
plus core-directed references, never anything under `evals/`. The
response contract was assembled from the shipped scorer's vocabulary
and the `examples/balanced.json` shape (route ∈ routine-check | uat |
blocked-environment; the four-role pipeline; the four packet
artifacts; the five-line routine check), with the scenarios' situational
facts restated in dispatch. Trials were declared simulations; the
shipped scorer ran unmodified via its own CLI
(`score.py --responses <file> --fixtures <file>`). Raw extracted
responses in `responses.json`; scorer output in `scorer-report.json`.

Extraction: 4/4 responses were single well-formed JSON objects, no
extraction anomalies, no missing responses.

**Model note (deviation, recorded per dispatch contract §7):** the
preregistration named model family claude-fable-5; subjects in this
harness ran as isolated subagents of the coordinating runtime (model:
Muse Wonder). The same-family caveat applies.

## Results

Routes: uat 2 · routine-check 1 · blocked-environment 1.

- **PASS (4):** every fixture — the explicit UAT request and the
  stateful keyboard flow both routed to the full packet pipeline
  (contract-writer → actor → verifier → judge, all four artifacts,
  no verdict pre-claimed); the bounded literal-copy change routed to
  a routine check with exactly the five pinned lines and no packet;
  and the unreachable material target routed to blocked-environment
  with verdict BLOCKED_ENVIRONMENT rather than a fabricated pass.
- **FAIL (0).**

## Holdout line

This battery pins no holdout fixtures (all four fixtures are standard
rows in `dispatch-map.json`); there is no separate holdout line to
report, and none is invented.

## Reading (within the preregistered claim fence)

Route selection on declared responses: on these 4 fixtures, isolated
agents sent material/stateful verification to the evidence-locked
pipeline, kept a genuinely bounded change out of it, and declared a
blocked environment instead of simulating success. This is a claim
about routing decisions in simulation — no UAT packet was actually
executed, and nothing here evidences the pipeline's behaviour when run.

## Honest limits

N=1 per fixture, one harness, single repetition; a 4-fixture battery is
the smallest in the program and its PASS is correspondingly light
evidence. Declared-response scoring only.
