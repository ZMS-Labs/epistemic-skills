# Run ledger — intrinsic evidence emission

`ledger.jsonl` is this skill's own append-only run record. Each line is one
engagement: `fired` or `declined`, which discipline ran (if any), and whether the
action changed.

This is **not** `.ledger/entries.jsonl` (decision records) and **not** an external
calibration MCP call. The append is part of the skill's own procedure. Schema:
`plugins/epistemic-skills/contracts/skill-run-ledger.schema.json`.

Synthetic exemplar lines carry `"example": true` and are documentation only.
