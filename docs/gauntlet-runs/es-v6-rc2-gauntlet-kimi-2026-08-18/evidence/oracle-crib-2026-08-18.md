# Oracle crib transcript — candidate C = 6db8c50420b194aebbd09a2ea5f81c6a276897dc

Run by the independent seat on 2026-08-18 in a pristine worktree of C
(detached HEAD, `git status` clean), Windows 11 host, Python 3.11, per the
handoff's verification crib. Every command was run TWICE (the first pass
piped through `tail` and was repeated with full logs — results identical
across passes, i.e. deterministic, not flaky).

## Green at C (exit 0, self-test + live where offered)

| oracle | result |
|---|---|
| contracts/v6-assurance/test_v6_assurance_validator.py | PASS (18 planted-defect cases fail closed, incl. bare-enum-GO, hand-edited blocking, post-freeze mutation, register crosswalk) |
| contracts/v6-assurance/validate_v6_assurance.py (at C) | PASS — LEGACY @1 notices (C's packet dir is the predecessor's stale @1 packet BY DESIGN; the @2 packet lives at C+1) |
| check_public_content.py --self-test | PASS (7 seeded RED controls) |
| check_public_content.py | PASS — "7 patterns, 37 allowlisted exact files digest-verified (1 dormant entries name files absent from this branch)" |
| sync_skill_surfaces.py --check | PASS — "15 skills, 14 disciplines" |
| check_no_phantom_skills.py --self-test / (live) | PASS / PASS |
| score_sentinels.py --self-test / (live) | PASS / PASS (15 fixtures; absence-as-success rejection) |
| check_skill_run_ledger.py --self-test / (live) | PASS / PASS (15 skills carry emission step) |
| test_v6_candidate_packet.py | PASS |
| test_v6_audit_workflow_oracles.py | PASS (incl. "planted whole-tree reader behind paths: filter fails closed" — the R7 oracle strengthening) |
| v6_audit_workflow_oracles.py (live) | `{"finding_count": 0}` |
| mission-custody/test_custody_hook.py | PASS (all green; one loud skip line: "unreadable workspace root, skipping: ValueError") |
| mission-custody/test_custody_cli.py | PASS (0 failures) |

## Red at C on this Windows host (3 clusters, mechanisms established)

### Cluster A — mission-custody/test_custody_gate.py: 2 FAIL (repeat failure)

`guard-lexical-realpath-lands-in-guarded-tree` and
`guard-lexical-collapse-stays-textual` FAIL on both runs. These are the R15
characterization-pin checks. Mechanism (reproduced with an isolated probe):
this host CAN create symlinks (no OSError → the test's only skip path is not
taken); on Windows `os.path.realpath("<tmp>/link/../x.txt")` collapses
`link/..` lexically to `<tmp>/x.txt` (does not follow the symlink first), and
`_guard_norm_path` case-folds to lowercase (drive letter and profile path)
while the test's expected string preserves case. Both FAILs are NT platform-semantics
artifacts, NOT a flip of the pinned invariant. The GATING Linux contract job
at C is green (run 32190028540, job `contract: success`). The handoff
predicted these tests would "skip loudly on NT without symlink privilege" —
correct for unprivileged NT, wrong for privileged NT: the skip guard keys on
`OSError` from `symlink_to` only. Disclosed platform class: KL-WINDOWS (no
native-Windows requalification claimed).

### Cluster B — sync_skill_surfaces.py --self-test: FAIL (repeat failure)

All 8 planted-drift cases error with `PermissionError: [Errno 13]` reading
`<tmp>\skills`. Mechanism (read at
`.github/scripts/sync_skill_surfaces.py:524`): `_selftest_copy` recreates the
root `skills` alias via `symlink_to("plugins/epistemic-skills/skills")`
WITHOUT `target_is_directory=True`. On POSIX this is harmless; on Windows
with symlink privilege it creates a FILE-type symlink whose target is a
directory, so `is_dir()` is False and `read_text()` (in
`test_epistemic_events.py:root_skills_reference`, line 36) raises
PermissionError. On unprivileged Windows the OSError fallback writes an alias
text file and the self-test passes. Failure set = {Windows ∧ symlink
privilege}. One-line fix class. The gating operation (`--check`) is green;
Linux CI at C is green (run 32190026236).

### Cluster C — validate_v6_assurance.py at C+1: FAIL (the material one)

See `validator-c1-digest-failure.md` — full transcript and root cause.
Summary: the @2 source inventory seals 17 `__pycache__/*.pyc` digests from
the generating host; the validator fails closed (`R5 DIGEST MISMATCH …
(absent)`) on ANY clean checkout of C+1, and a `.pyc` regenerates on import
(content-volatile), so the seal breaks even on the generating host. With the
17 `.pyc` entries stripped in a scratch probe, ALL validator stages pass at
C+1 (matrix, reconciliation, inventory digests of the remaining 141 files,
promotion-packet @2 rules, blocking derivation, candidate coverage, register
crosswalk).

## Clean-room — `bash .github/scripts/cleanroom_ci.sh 6db8c50…` (Git Bash, C worktree)

```
clean-room CI: replicated 51 of 54 workflow python steps
pass=51 fail=2 need-args=0 ci-context=1 missing-dep=0
failing:
  plugins/.../formal-rigor-v2-fixtures/tests/test_live_runner.py
  .github/scripts/sync_skill_surfaces.py --self-test
cleanroom rc=1
```

- The R9 numerator/denominator print and per-skip naming are present
  ("SKIP … (ci-context: needs GitHub event env)").
- `test_live_runner.py` failure: `ValueError: packet root must not be under a
  sensitive user-profile path` from `run_live.py:1274` — the clean-room's
  scratch copy lives under the host temp dir inside the user profile, and the
  runner's sensitive-path guard refuses it. Fail-closed guard vs harness
  tempdir location; passes on Linux CI (stdlib-checks green at C, run
  32190026236). Not observed to affect any gating Linux surface.
- The sync self-test failure is Cluster B repeated inside the clean-room.
- Notably the clean-room's own `validate_v6_assurance.py` step PASSes — it
  runs against C's tree, where the packet dir holds the LEGACY @1 packet
  (validator in legacy mode). The @2 digest binding is exercised nowhere in
  the clean-room.
