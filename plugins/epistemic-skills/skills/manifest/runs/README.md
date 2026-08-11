# Run ledger — intrinsic evidence emission

`ledger.jsonl` is this skill's own append-only run record. Each line is one
engagement: `fired` or `declined`, which discipline ran (if any), and whether the
action changed.

This is **not** `.ledger/entries.jsonl` (decision records), **not** a mission's
`missions/<id>/` custody state (checkpoints/receipts belong to the mission, in
the worked repo), and **not** an external calibration MCP call. The append is
part of the skill's own procedure. Schema: `skill-run@1`, one JSON object per
line.
