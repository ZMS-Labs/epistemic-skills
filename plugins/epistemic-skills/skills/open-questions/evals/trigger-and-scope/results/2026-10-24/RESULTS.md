# Live behavioral epoch — 2026-10-24 (E11: open-questions second epoch)

**Outcome: FAIL — the shipped scorer exited 1 without producing
fixture-level verdicts: it crashed on a mistyped response field.**
Reported **against** the first-epoch baseline
(`results/2026-08-04/RESULTS.md`, FAIL 8/10), which this record does not
overwrite. Per methodological-review fix F2, the baseline-comparable
line and the v7 scorer-validation line are reported separately below.
Per fix F3 (no silent rerun), this epoch is **not** re-run: the crash
is recorded as the epoch's result.

## Methodology

Protocol per `docs/evidence-program/PROGRAM-2026-10-24.md` §4 and
`docs/policy/LIVE-EPOCH-DISPATCH-CONTRACT.md`: one fresh isolated
general-purpose subject per fixture (N=1), dispatch ordered by opaque
trial key (`sha256(fixture-id)` first 12 hex; mapping in
`dispatch-map.json`, published here after responses were frozen),
subjects read only the skill core (`skills/open-questions/SKILL.md`)
plus core-directed references, never anything under `evals/`. The
pinned response contract was quoted from the battery README with
prior-epoch history stripped. Trials were declared simulations; the
shipped `score.py` ran unmodified against the frozen responses in
`responses.json`.

Extraction: 10/10 responses were single well-formed JSON objects, no
extraction anomalies, no missing responses. Dispatch completed
normally; the failure is downstream, at scoring.

**Model note (deviation, recorded per dispatch contract §7):** the
preregistration named model family claude-fable-5; subjects in this
harness ran as isolated subagents of the coordinating runtime (model:
Muse Wonder). The same-family caveat applies.

## What happened at scoring

The shipped scorer raised `TypeError: 'int' object is not iterable`
at `score.py` line 87 and exited 1; the full traceback is preserved
verbatim in `scorer-report.json`. The proximate cause is one frozen
response: for `explicit-release-parks`, the subject reported
`"parked": 2` — an integer count — where the scorer iterates `parked`
as a list of identified item objects. Because the crash occurs inside
the scoring loop over fixtures, **no fixture received a verdict**: the
baseline-comparable pass count for this epoch does not exist and none
is invented here.

Characterisation:

- At the response level: **(b)** reporting shape over substantively
  matching conduct — the subject's declared conduct (full interview,
  operator release obtained, two questions parked) matches the
  scenario's shape; the `parked` field's type diverged from the
  contract's list-of-items vocabulary.
- At the battery level, a scorer-robustness observation: a single
  mistyped field in one response aborts the entire scoring run instead
  of failing that fixture, voiding the epoch's verdicts. Epoch 1's
  record shows this same fixture (`explicit-release-parks`) was one of
  its two failures; this epoch it is again the problem row, by a
  different mechanism.

## v7 scorer-validation line (separate, per F2)

The 4 cases in `v7-cases.json` are **scorer-validation cases, not live
trials**: each ships a canned response that must pass and canned
mutations that must be rejected. Exercised through the shipped
`tests/run_tests.py`, unmodified: **PASS (exit 0)**. (The canned cases
are well-typed, so this line does not hit the crash above.) No agent
behaviour is claimed for this line.

## Reading (within the preregistered claim fence)

No conformance claim is available from this epoch: the instrument
produced no verdicts. What the epoch does evidence is narrower and
about the battery, not the skill — the shipped scorer is not robust to
a plausible response-shape deviation, and one subject in ten produced
that deviation on the battery's historically hardest fixture. The
baseline (FAIL 8/10) remains the latest scored epoch for this battery.

## Honest limits

The frozen responses stand as dispatched; any future epoch for this
battery needs either a scorer that fails a mistyped fixture instead of
crashing, or a dispatch contract that pins field types more sharply —
both are battery-design changes outside this program's no-edit rule,
so they are recorded here as findings, not applied.
