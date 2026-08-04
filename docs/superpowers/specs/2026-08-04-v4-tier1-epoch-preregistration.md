# Preregistration — v4.0.0 Tier-1 trigger epochs (post-consolidation)

**Date:** 2026-08-04, committed before any trial is dispatched.
**Policy basis:** `docs/policy/EVIDENCE-POLICY.md` Tier 1 — the v4.0.0
consolidation changed the trigger surfaces of `recon` and `resolve` (new
skill cores carrying mode/instrument selection), which re-arms their
batteries. **Protocol:** every dispatch follows
`docs/policy/LIVE-EPOCH-DISPATCH-CONTRACT.md` (contract verbatim with
vocabularies inline; silence semantics; extraction-only prose tolerance;
simulation clause; opaque keys; isolated subjects; results as-is).

## Batteries and subjects

| Battery | Fixtures | Subject (must read) | May additionally read |
|---|---|---|---|
| `recon/evals/brief-trigger-and-scope` | 14 | `skills/recon/SKILL.md` | any file under `skills/recon/reference/` |
| `recon/evals/initiative-trigger-and-scope` | 13 | `skills/recon/SKILL.md` | any file under `skills/recon/reference/` |
| `recon/evals/candidate-trigger-and-scope` | 14 | `skills/recon/SKILL.md` | any file under `skills/recon/reference/` |
| `resolve/literature/evals/trigger-and-scope` | 14 | `skills/resolve/SKILL.md` | any `METHOD.md`, `theory-battery.md`, or `reference/` file under `skills/resolve/` |
| `resolve/probe/evals/trigger-and-scope` | 12 | `skills/resolve/SKILL.md` | any `METHOD.md`, `theory-battery.md`, or `reference/` file under `skills/resolve/` |

The may-read lists mirror deployment: the core routes, the mode/instrument
files carry procedure, and the subject chooses what to open. Subjects never
read anything under any `evals/` or `results/` path, any `LOCAL.md*` file,
any other skill, or any prior epoch artifact.

All paths are relative to `plugins/epistemic-skills/`. The
`decision-ledger` resume-mode surface is **not** in this wave: its
`resume-fixtures` battery is artifact-corpus-based, not prompt-fixture
based, and its re-run is adjudicated separately.

## Mechanics (fixed before dispatch)

- One fresh isolated `general-purpose` subagent per fixture; 67 trials
  total; model family: claude-fable-5 (same-family caveat applies to every
  result).
- Trial keys: `sha256(fixture-id)` first 12 hex chars; dispatch ordered by
  key; mapping committed as `dispatch-map.json` in the results directory
  after responses are frozen.
- Response contracts: each battery README's pinned
  `## Live-epoch response contract` section, quoted verbatim minus any
  prior-epoch history note.
- Scorers: each battery's shipped `score.py`, unmodified; full report and
  exit code committed.
- Results land in `<battery>/results/2026-08-04-v4-tier1/` as
  `responses.json`, `scorer-report.json`, `dispatch-map.json`,
  `RESULTS.md` — committed as-is, no re-rolls, no adapters (an adapter
  would be declared and would downgrade the run).

## Interpretation rules (fixed before dispatch)

- A battery epoch **passes** only on scorer exit 0; any fixture failure is
  an epoch FAIL, recorded and characterized — never softened.
- Failure characterization classes: (a) conduct (wrong fire/no-fire or
  wrong action), (b) reporting shape over correct conduct, (c) **mode or
  instrument selection** — the novel post-consolidation class this wave
  exists to observe: the old batteries tested one-skill triggers; the new
  cores must additionally select the right mode/instrument.
- Non-binding expectation, stated for calibration only: the 2026-08-04
  pre-consolidation wave scored 94.6% under born-pinned contracts; we
  expect ≥ 90% per battery here, with class (c) as the plausible regression
  vector. This number is not a gate and its miss changes nothing about
  what gets committed.
- Register: every verdict lands on issue #77.
