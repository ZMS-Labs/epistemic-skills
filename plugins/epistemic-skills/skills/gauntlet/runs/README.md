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

## Schema versions

Lines carry a `"schema"` field: `"ledger@2"` (current) or absent (v1, pre-2026-07-22).
**No backfill**: v1 lines stay as they are; readers (`lens_stats.py`, the selector's
rotation input) accept both. v2 lines are **emitted by `scripts/finalize_run.py`** from
the run record — never hand-authored.

## The data axis: committed projection vs local-only records

The ledger line is a **derived pointer projection**, not a second writable record.
Every fact that overlaps the run record (`dossier_sha256`, `docket_mode`,
`independence_mode`, per-lens `model`, verdict, depth) has exactly ONE writable home —
the run's own artifacts, hashed into `gauntlet-run-record@1` by `finalize_run.py` — and
is **derived** into the ledger line in the same pass. `scripts/verify_run.py`
re-checks the record against the run directory and hard-fails on any disagreement, so
the projection can never drift from its source silently.

- **Committed (this repo, public by design):** ledger lines only — the `run_dir`
  pointer, `dossier_sha256`, modes, verdict, and per-lens counts, with per-seat
  `model` at **family granularity**. Retention: indefinite, as lifecycle telemetry —
  the lifecycle thresholds consume counts over the full history.
- **Local-only (never committed):** run directories themselves — dossiers, reports,
  prompts, `run-record.json` — which may keep exact timestamps and per-seat EXACT
  model identity (`prompts/seats.json`) because they never leave the operator's
  machine. Run output roots (`outputs/` and equivalents) are gitignored.
- **Synthetic exemplar:** `examples/example-run/` ships one fully-worked synthetic
  run plus its ledger line marked `"example": true` (and `eligible: false`). Example
  lines are documentation, not telemetry: `lens_stats.py` and the selector's rotation
  input skip them mechanically.

The run record certifies the ENVELOPE only — artifact binding, replay, gate
arithmetic. It **never attests**: verdict-truth (the lenses/judge may be wrong),
independence-achieved (`independence_mode` is self-reported orchestration metadata),
or freshness beyond the record's `valid_while` coordinates (subject revision +
evidence-root pin).

## Record schema v2 (one line per run)

```json
{
  "schema": "ledger@2",
  "ts": "2026-07-22T00:00:00Z",
  "subject": "short-slug-of-subject",
  "depth": "quick|standard|deep|max",
  "registry_sha256": "<sha of roster/registry.json used>",
  "verdict": "GO|CONDITIONAL|NO-GO",
  "eligible": true,
  "run_dir": "<run directory name — pointer, content-bound via dossier_sha256>",
  "dossier_sha256": "<sha of the frozen dossier>",
  "docket_mode": "real-deepreason|mini-deepreason|manual-docket|skipped",
  "independence_mode": "independent|degraded — reason",
  "lenses": [
    {
      "id": "chaos-monkey",
      "role": "evaluate|generate_options|gate|adjudicate",
      "lifecycle": "active|probation",
      "seat": "core|exploration",
      "model": "<model FAMILY only, e.g. synthetic-family-a>",
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

## Record schema v1 (legacy — still valid, no backfill)

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
  completed arbitration (Step 7). Quick-depth or aborted runs: false. Lines marked
  `"example": true` are always ineligible and are skipped by aggregation and rotation.
- `seat: "exploration"` — the probation SHADOW seat: ran with the panel, mechanically
  criticized, ledger-recorded — but its findings were EXCLUDED from arbitration and the
  verdict. Its `upheld_unique` means "found a real basin the core panel missed"
  (scored against the core panel's findings), not "upheld at arbitration". In a
  `finalize_run.py`-derived line the shadow seat's counts are zero by construction —
  its findings never reached the ruling-set; score unique basins manually when they
  matter for an activation review.
- `upheld_unique` — this lens's upheld P1/P2 findings in a basin **no other seated lens
  reached** (fix-disjointness, same rule as admission). `upheld_dup` — upheld but
  another lens reached the same basin. Derived lines compute both from the ruling-set's
  `basin` fields; P3/P4 rulings never count.
- `unsupported` — findings struck at mechanical criticism for evidence-tier failure
  (severity claimed on `[H]` or malformed anchors; ruling `STRUCK-UNSUPPORTED`).
- `false_high` — findings the arbitrator struck under the FALSE-HIGH GATE (severity
  outran evidence/mechanism; ruling `STRUCK-FALSE-HIGH`). Tracked per lens; a pattern
  here is a deprecation signal independent of yield.


## adjudications.jsonl — Step 7b external cross-family reads

`adjudications.jsonl` (created on first `consult_packet.py record`) holds one line per
external GPT-5.6 Pro adjudication of a computed verdict: `{run_id, request_id,
external_model, reading (CONCURRENCE|DISSENT), strongest_reason_verdict_wrong, confidence,
disposition}`. A DISSENT records `ESCALATE-TO-SOVEREIGN` — it never rewrites the gauntlet
verdict; the operator decides. Built + recorded by `scripts/consult_packet.py`
(manual-handoff default). See SKILL.md Step 7b.
