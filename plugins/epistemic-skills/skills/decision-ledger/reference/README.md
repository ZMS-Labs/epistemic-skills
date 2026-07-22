# `ledger-entry@1` — schema, examples, and the human-enforced boundary

Files here:

- `ledger-entry.schema.json` — JSON Schema (draft 2020-12) for
  `ledger-entry@1`. **Structural only**: it enforces the required fields, the
  `id`/`at` shapes, the closed `type` / `durability` vocabularies, and the
  recurrent-correction failure-chain shape. It makes **no truth, verdict, or
  authorization claim** about an entry.
- `example-durable.json` — synthetic validating example, `durability:
  durable` (a decision).
- `example-session-only.json` — synthetic validating example, `durability:
  session-only` (an assumption; demonstrates the optional `session` field and
  a non-empty `supersedes` link — the linked id `cli-json-flag-behavior-
  20260721-003` is illustrative; chain integrity is a store-level invariant,
  not a per-file property).
- `example-correction-with-chain.json` — synthetic validating correction with
  `recurrence_risk: true` and the required failure-chain fields. The chain
  locates the earliest interruptible link and names a rehearsal fixture; it
  does not authorize an action.

## Recurrent-correction rule

`failure_chain` and `recurrence_risk` are correction-only fields. When a
correction has `recurrence_risk: true`, the schema requires:

- prompting event;
- vulnerabilities;
- ordered links;
- target failure;
- consequences;
- earliest interruptible link;
- replacement behavior;
- rehearsal fixture.

This is a structural completeness rule, not proof that the chain is causally
correct. Consumers still re-anchor its evidence.

## PR-review checklist item (human-enforced)

- [ ] **Never-instruct boundary held (human-enforced, not schema-checkable).**
  Read every new/changed ledger entry's `statement` and `because`: no verdict
  vocabulary (`GO`, `NO-GO`, `must`, `approved`), no instruction, no
  authorization. A verdict-carrying-but-well-formed entry **passes** the
  schema — it is caught by this review, never claimed as schema-rejected.
- [ ] **Failure chain remains descriptive.** `replacement_behavior` records the
  correction that was adopted; it does not independently authorize deployment,
  publication, spending, or other consequential action.

An optional lint for verdict vocabulary in `statement` is permitted, but any
such lint must be labeled **heuristic** — it is a review aid, not a contract.

All three synthetic examples validate against the schema (required fields
present, closed vocabularies respected, `additionalProperties: false`
satisfied).
