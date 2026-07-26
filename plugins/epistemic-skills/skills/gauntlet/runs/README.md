# Run ledger — non-governing observability

`ledger.jsonl` records one JSON line per **live gauntlet run**. It supports audit,
cost/yield review, and reproducibility. It never activates, withholds, retires, weights,
or selects a lens; those decisions come from the two-state registry and claim evidence.
Appending remains part of Step 8 so a completed run has a durable projection.

Aggregate observability: `python scripts/lens_stats.py` (add `--json` for machine
output). This ledger lives in the durable repo (commit it with the run), never only in
the deployed skill cache (`~/.claude/skills` or your harness's equivalent).

## Schema versions

Lines carry a `"schema"` field: `"ledger@2"` (current) or absent (v1, pre-2026-07-22).
**No backfill**: v1 lines stay as they are; `lens_stats.py` accepts both. The selector
does not read the ledger. v2 lines are **emitted by `scripts/finalize_run.py`** from
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
  `model` at **family granularity**. Retention is indefinite audit telemetry.
- **Local-only (never committed):** run directories themselves — dossiers, reports,
  prompts, `run-record.json` — which may keep exact timestamps and per-seat EXACT
  model identity (`prompts/seats.json`) because they never leave the operator's
  machine. Run output roots (`outputs/` and equivalents) are gitignored.
- **Synthetic exemplar:** `examples/example-run/` ships one fully-worked synthetic
  run plus its ledger line marked `"example": true` (and `eligible: false`). Example
  lines are documentation, not telemetry: `lens_stats.py` skips them mechanically.

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
      "lifecycle": "available",
      "seat": "core|wildcard",
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
      "lifecycle": "legacy-status",
      "seat": "legacy-seat",
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
- `eligible` — true for completed standard/deep/max runs and false for quick, aborted,
  or synthetic example runs. It is an analysis filter, not lifecycle authority.
- `seat: "wildcard"` — selected by deterministic subject-seeded exploration. It uses
  the same finding and arbitration contract as `core`; the label is replay metadata only.
- `upheld_unique` — this lens's upheld P1/P2 findings in a basin **no other seated lens
  reached** (fix-disjointness, same rule as admission). `upheld_dup` — upheld but
  another lens reached the same basin. Derived lines compute both from the ruling-set's
  `basin` fields; P3/P4 rulings never count.
- `unsupported` — findings struck at mechanical criticism for evidence-tier failure
  (severity claimed on `[H]` or malformed anchors; ruling `STRUCK-UNSUPPORTED`).
- `false_high` — findings the arbitrator struck under the FALSE-HIGH GATE (severity
  outran evidence/mechanism; ruling `STRUCK-FALSE-HIGH`). Tracked for review, never as
  automatic lifecycle or selection authority.


## adjudications.jsonl — Step 7b external cross-family reads

`adjudications.jsonl` (created on first `consult_packet.py record`) holds one line per
external GPT-5.6 Pro adjudication of a computed verdict: `{run_id, request_id,
external_model, reading (CONCURRENCE|DISSENT), strongest_reason_verdict_wrong, confidence,
disposition}`. A DISSENT records `ESCALATE-TO-SOVEREIGN` — it never rewrites the gauntlet
verdict; the operator decides. Built + recorded by `scripts/consult_packet.py`
(manual-handoff default). See SKILL.md Step 7b.
