# mission-custody@1

Durable mission-custody contract family: `mission-manifest@1` (authority,
append-only instruction), `checkpoint@1` (revisioned snapshots,
`prev_checkpoint_sha256` chain), `receipt@1` (effect -> artifact hash binding),
`acceptance-verdict@1` (tiered acceptance; self-certification refused).

Provenance: FOLD cell of the practical-agency gauntlet decision rule; design
`docs/superpowers/specs/2026-08-11-mission-custody-contracts-design.md`.
practical-agency (ZMS-Labs) is parked prior art; its schemas seeded this family.

Validate: `python verify_mission_custody.py examples/valid-manifest-minimal.json`
Test: `python test_mission_custody.py` (exit 0 = green; every `invalid-*.json`
example MUST fail validation — the corpus is the regression suite).

Evolution: additive optional fields only within `@1`; anything else is a new
epoch with a documented migration. Acceptance tiers are closed:
`operator-accepted`, `declared-role-separation` — no `externally-proven` tier
exists until evidence could support one.
