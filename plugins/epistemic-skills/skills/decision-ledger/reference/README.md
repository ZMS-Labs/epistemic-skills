# `ledger-entry@1` — schema, examples, and the human-enforced boundary

Files here:

- `ledger-entry.schema.json` — JSON Schema (draft 2020-12) for
  `ledger-entry@1`. **Structural only**: it enforces the required fields, the
  `id`/`at` shapes, and the closed `type` / `durability` vocabularies. It
  makes **no semantic claim** about any entry.
- `example-durable.json` — synthetic validating example, `durability:
  durable` (a decision).
- `example-session-only.json` — synthetic validating example, `durability:
  session-only` (an assumption; demonstrates the optional `session` field and
  a non-empty `supersedes` link — the linked id `cli-json-flag-behavior-
  20260721-003` is illustrative; chain integrity is a store-level invariant,
  not a per-file property).

## PR-review checklist item (human-enforced)

- [ ] **Never-instruct boundary held (human-enforced, not schema-checkable).**
  Read every new/changed ledger entry's `statement` and `because`: no verdict
  vocabulary (`GO`, `NO-GO`, `must`, `approved`), no instruction, no
  authorization. A verdict-carrying-but-well-formed entry **passes** the
  schema — it is caught by this review, never claimed as schema-rejected.

An optional lint for verdict vocabulary in `statement` is permitted, but any
such lint must be labeled **heuristic** — it is a review aid, not a contract.

Both synthetic examples validate against the schema (required fields present,
closed vocabularies respected, `additionalProperties: false` satisfied).
