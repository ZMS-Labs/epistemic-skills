# Certified-arbitrator planted-flaw seat battery

Certifies that the gauntlet **arbitrator** catches the defect classes its discipline
requires it to catch. Each case in `inputs.json` feeds the arbitrator a frozen dossier +
lens reports containing ONE planted defect; the arbitrator returns a verdict + a
disposition per finding; `score.py` grades those against out-of-band ground truth in
`battery.json` (which the arbitrator never sees).

## Files
- `battery.json` — the 10 cases + planted-flaw ground truth + expected verdict (scorer-only).
- `inputs.json` — arbitrator-facing inputs ONLY (no answers).
- `score.py` — deterministic, stdlib-only scorer. Primary metric = planted-flaw catch.
- `results-2026-07-17.md` — the run: 10/10 catch, CERTIFIED at standard rigor.

## Run (any harness)
1. For each case in `inputs.json`, dispatch the `gauntlet-arbitrator` role-agent (blind to
   `battery.json`) with the dossier + findings; collect `{verdict, dispositions, ledger_notes}`
   into `outputs.json` keyed by case id. Use any concurrent-subagent primitive, or run them
   sequentially.
2. `python score.py --outputs outputs.json`

The planted flaws are the arbitrator's core job: fabricated citation, binary-file `[V]`,
correlated-as-independent, malformed falsifier, inadequate oracle, unresolved-P1 rounding,
shadow-seat leakage, false-high, prompt-injection, and polish-over-evidence.
