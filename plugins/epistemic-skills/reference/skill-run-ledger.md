# Intrinsic skill-run ledger — carrier semantics

Normative companion to D7 and `contracts/skill-run-ledger.schema.json`.

## Decision (issue #104 §2)

Every skill **must** append its own run record as part of its own procedure.
External calibration MCP calls are optional consumers, never the durability path.

## Portable carrier

| Field | Rule |
|---|---|
| Path | `plugins/epistemic-skills/skills/<name>/runs/ledger.jsonl` |
| Format | JSON Lines, one object per engagement |
| Schema | `skill-run@1` (`decision`: `fired` \| `declined`; `discipline_engaged`; `action_changed`) |
| Privacy | No prompts, transcripts, secrets, private paths, exact model IDs, or session IDs (same prohibition class as epistemic-event records) |
| Example lines | `"example": true` — documentation only; not live telemetry |

## Concurrency / append

- Append-only. Never rewrite historical lines.
- One writer per skill ledger per process; if concurrent agents share a working
  tree, serialize appends (open-append-fsync) or write to a run-scoped file and
  merge in a single commit.
- Failure to append is a **procedure failure**: surface it; do not pretend the
  engagement was recorded.

## Failure behavior

| Condition | Behavior |
|---|---|
| Ledger path unwritable | Stop at hold/escalate for consequential engagements; for declines, note the miss in-session and retry when writable |
| Malformed prior line | Leave it; append a valid new line; do not rewrite |
| External calibration unavailable | Irrelevant — intrinsic ledger does not call it |

## Relation to `.ledger/entries.jsonl`

Decision-ledger entries remain consequential *decisions*. Skill-run lines are
engagement telemetry. Do not mix the schemas.
