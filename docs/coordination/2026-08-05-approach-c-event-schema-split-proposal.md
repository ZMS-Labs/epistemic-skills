# Approach C — split the public event schema into core + producer-surface (parked proposal)

**Date:** 2026-08-05
**Charter:** `docs/coordination/epistemic-calibration.md` (change protocol, step 1 — *propose*)
**Status:** **PARKED — do not implement until the operator determines.** Recorded
so a future agent can pick it up on demand.
**Owner of the change:** `ZMS-Labs/epistemic-skills` (this repo owns the event
contract; calibration consumes it).

## Background

`epistemic-calibration` has shipped Approach A: it made its consumer side
invariant to our skills catalog. Its event record layer now treats
`producer.skill` and `event_kind` as opaque open tokens, and its cross-repo
contract lock is an `epistemic-skills-event-contract@2` **core-compatibility
gate** that projects the skill/kind surface out of our
`epistemic-event.schema.json` before hashing. The consequence, verified on both
sides: the gate is green against both the previously pinned commit
`8d9b2f85…` and current `HEAD`, even though our v4 refactor changed the
`producer.skill` and `event_kind` enum sets. Catalog churn no longer breaks
calibration.

Approach C is the **upstream** form of that same separation, owned here.

## Why this belongs to us

Per the charter ownership table, epistemic-skills **owns** the runtime schemas.
Today `epistemic-event.schema.json` mixes two very different things in one file:

- the **stable epistemic core** calibration actually scores against
  (`variant`, `forecast`, `observation`, evidence, provenance, privacy); and
- the **catalog-volatile surface** (`producer.skill` and `event_kind` value
  sets) that changes every time we add, rename, or reorganize skills.

Calibration currently separates these at *its* verification time via a
projection. Approach C encodes the separation at the source so the core is a
first-class, independently versioned artifact.

## Proposed change

1. Split `plugins/epistemic-skills/contracts/epistemic-events/epistemic-event.schema.json`
   into:
   - `epistemic-event-core.schema.json` — the stable core; no skill/kind
     enumeration.
   - `producer-surface.schema.json` — the `producer.skill` and `event_kind`
     value sets, versioned independently so catalog changes never bump the core.
   - Compose via `$ref`/`allOf` so the emitted event shape is unchanged and all
     existing valid/invalid fixtures still validate as before.
2. Keep `skill-event-map.json` on the producer-surface side.
3. Update the event-contract tests
   (`plugins/epistemic-skills/contracts/epistemic-events/`) and the
   `epistemic-flexibility` workflow steps that compile/validate them.

Non-goals: no change to the emitted event shape; no change to
`epistemic-product-calibration@1`; no runtime/submodule coupling to calibration.

## Consumer follow-on (already recorded there)

`epistemic-calibration` would point its `@2` gate at
`epistemic-event-core.schema.json` directly and drop its local projection step.
Its parked note:
`epistemic-calibration/docs/superpowers/specs/2026-08-05-approach-c-event-schema-split-followup.md`.

## Acceptance criteria

- Existing events validate unchanged; no producer has to change output.
- The core file alone determines calibration's `event_core_sha256` (today the
  equivalent projection is `52ccd576…`).
- Catalog edits touch only `producer-surface.schema.json`.
- Both repos' suites stay green, including this repo's `epistemic-flexibility`
  checks and `contracts/verify_calibration.py --self-test`, and calibration's
  `tools/check_epistemic_contract.py`.

## Process

Follow the charter change protocol: propose (this note) → freeze → run →
receive → **land independently** with reciprocal immutable links → recalibrate.
Neither repository may silently change the other's contract.
