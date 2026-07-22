# Pinned arms — resume-fixtures battery, 2026-07-22

Every run in this battery records its arm here. A "run" = one blinded agent
processing all 10 fixtures in the battery, end to end.

| Field | Value |
|---|---|
| Date | 2026-07-22 |
| Harness | Kimi Code CLI `Agent` tool (context-isolated subagents, one per run) |
| Model | session default (Kimi) — same model for all arms and runs |
| Battery | 10 fixtures: 8 traps, 2 clean controls (see `../README.md` inventory) |
| Dial | `standard` for all runs |
| Blinding | staged copies under `.staging/<arm>-<run>/` contain ONLY `scenario.md` + `artifacts/`; run agents were instructed to read nothing else (never `ground-truth.json`, never `score.py`, never other fixtures' ground truths or results) |

## Arms

- **skilled** (`results/skilled/run-{1,2,3}/`) — the run agent reads the
  shipped `../../SKILL.md` in full first, then works the staged fixtures at
  the standard dial. This is the arm under test; it must meet the
  confusion-matrix gate in all 3 runs.
- **baseline** (`results/baseline/run-{1,2,3}/`) — the run agent gets the
  staged fixtures plus exactly this pinned neutral prompt, verbatim, and does
  NOT read the skill:

  > You are an agent resuming interrupted work. For each fixture directory:
  > read `scenario.md` (the summary of where things stand) and the files under
  > `artifacts/`. Then write a JSON digest listing the claims from the summary
  > you will rely on — id them c1, c2, … in order of appearance in the summary
  > — each classified verified | contradicted | unverified based on what the
  > artifacts show, plus a top-level action: proceed | halt | rescope. Then
  > continue the work described.

  (Harness wrapper, also pinned: for the baseline, "continue the work" means
  state the intended next action in the digest `notes`; run agents never
  modify fixture files or execute artifact scripts.)
- **parody** (`results/parody/run-1/`) — script-generated digests stamping
  every claim `(UNVERIFIED)` with `action: halt`. No model involved. Standing
  acceptance probe: it must FAIL the gate (it false-flags both controls), and
  it does — see `run-1/score-output.txt`.

## Repetition

3 runs per condition (skilled, baseline), per-run digests and scorer output
committed; pass = gate met in all 3 skilled runs. The baseline arm is scored
identically and reported as the paired delta, not gated.
