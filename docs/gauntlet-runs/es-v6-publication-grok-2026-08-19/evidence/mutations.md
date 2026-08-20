# Mutation tests (working copy untouched)

## Assurance validator (validate_promotion_packet / derive_blocking / validate_source_inventory)

- Honest packet `independent_gauntlet=NOT_RUN` validates (baseline, exit 0).
- Bare `GO` enum with null ref: CATCHES (`requires independent_gauntlet_ref`).
- `GO` with missing on-disk verdict path: CATCHES (`verdict artifact not on disk`).
- `GO` with existing file that does not name the candidate SHA: CATCHES (`does not name the candidate SHA`).
- Emptying `blocking_claims` while matrix still derives `CLM-INDEPENDENT-GAUNTLET`: CATCHES (R12).
- Terminal readiness without GO: CATCHES (`cannot be operator-ready without independent Gauntlet GO`).
- Tampered inventoried digest: CATCHES (R5 DIGEST MISMATCH).
- Hole: validator does not require `packet.candidate_sha == HEAD`. Sealed tree hash `5355e26e625f5b8f2bd74b7cdd710cbafeff34f4` (freeze C) != HEAD tree `7407e26adb336f20cea91b863ea1b61c532c32fd`.

## DCO (`unsigned_commits`)

- New unsigned non-merge: CATCHES (returns the SHA).
- Closed-list 6th unsigned SHA: CATCHES.
- Prefix of an attested SHA: CATCHES (full 40-hex only).
- Exact attested SHA with no sign-off: ALLOWS (closed list, by design).
- Merge commit (`parents > 1`) whose message claims a conflict resolution and has no sign-off: ALLOWS. The checker never inspects the tree. Disclosed in D18 and in RELEASE-6.0.0.md.

## Ledger append-only

- Self-test PASS: append/no-op/born allowed; rewrite/delete/insert/reserialize CATCH (LEDGER-REWRITTEN / TRUNCATED); unresolvable git ref fails closed.
