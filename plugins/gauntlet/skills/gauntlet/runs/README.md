# Run ledger — the lifecycle's data source

`ledger.jsonl` (created on first append) records one JSON line per **live gauntlet
run**. It is the ONLY data source for the lifecycle thresholds in
`reference/lens-registry.md` (probation → active after 20 eligible runs; deprecate/merge
when duplicate rate > 70% and unique upheld yield < 0.1/run). Without an appended
record, a run contributes nothing to any lens's track record — appending is part of
Step 8, not optional.

Aggregate + threshold check: `python scripts/lens_stats.py` (add `--json` for machine
output). This ledger lives in the durable repo (commit it with the run), never only in
the deployed skill cache (`~/.claude/skills` or your harness's equivalent).

## Record schema (one line per run)

```json
{
  "ts": "2026-07-14T02:30:00Z",
  "subject": "short-slug-of-subject",
  "depth": "quick|standard|deep|max",
  "registry_sha256": "<sha of roster/registry.json used>",
  "verdict": "GO|CONDITIONAL|NO-GO",
  "eligible": true,
  "lenses": [
    {
      "id": "chaos-monkey",
      "role": "evaluate|generate_options|gate|adjudicate",
      "lifecycle": "active|probation",
      "seat": "core|exploration",
      "findings_p1p2": 2,
      "upheld_unique": 1,
      "upheld_dup": 1,
      "overruled": 0,
      "unsupported": 0,
      "false_high": 0
    }
  ]
}
```

Field notes:
- `eligible` — counts toward probation windows: true for standard/deep/max runs that
  completed arbitration (Step 7). Quick-depth or aborted runs: false.
- `seat: "exploration"` — the probation SHADOW seat: ran with the panel, mechanically
  criticized, ledger-recorded — but its findings were EXCLUDED from arbitration and the
  verdict. Its `upheld_unique` means "found a real basin the core panel missed"
  (scored against the core panel's findings), not "upheld at arbitration".
- `upheld_unique` — this lens's upheld P1/P2 findings in a basin **no other seated lens
  reached** (fix-disjointness, same rule as admission). `upheld_dup` — upheld but
  another lens reached the same basin.
- `unsupported` — findings struck at mechanical criticism for evidence-tier failure
  (severity claimed on `[H]` or malformed anchors).
- `false_high` — findings the arbitrator struck under the FALSE-HIGH GATE (severity
  outran evidence/mechanism). Tracked per lens; a pattern here is a deprecation signal
  independent of yield.


## adjudications.jsonl — Step 7b external cross-family reads

`adjudications.jsonl` (created on first `consult_packet.py record`) holds one line per
external GPT-5.6 Pro adjudication of a computed verdict: `{run_id, request_id,
external_model, reading (CONCURRENCE|DISSENT), strongest_reason_verdict_wrong, confidence,
disposition}`. A DISSENT records `ESCALATE-TO-SOVEREIGN` — it never rewrites the gauntlet
verdict; the operator decides. Built + recorded by `scripts/consult_packet.py`
(manual-handoff default). See SKILL.md Step 7b.
