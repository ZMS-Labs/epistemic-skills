# Finding candidate FC-1 — the @2 digest seal fails closed on every clean checkout

Transcript (freeze worktree = pristine checkout of C+1
`9aecd467236dfb927e9c13784d77a16d62f28f67`, 2026-08-18):

```
$ python plugins/epistemic-skills/contracts/v6-assurance/validate_v6_assurance.py
AssertionError: R5 DIGEST MISMATCH: inventoried files changed after the packet
was generated (restamp class): [
 'plugins/epistemic-skills/contracts/epistemic-events/__pycache__/test_epistemic_events.cpython-311.pyc (absent)',
 'plugins/epistemic-skills/contracts/epistemic-events/__pycache__/test_epistemic_events.cpython-312.pyc (absent)',
 'plugins/epistemic-skills/contracts/epistemic-events/__pycache__/verify_epistemic_event.cpython-311.pyc (absent)',
 'plugins/epistemic-skills/contracts/epistemic-events/__pycache__/verify_epistemic_event.cpython-312.pyc (absent)',
 'plugins/epistemic-skills/contracts/mission-custody/__pycache__/census_missions.cpython-311.pyc (absent)',
 'plugins/epistemic-skills/contracts/mission-custody/__pycache__/custody_cli.cpython-311.pyc (absent)',
 'plugins/epistemic-skills/contracts/mission-custody/__pycache__/custody_gate.cpython-311.pyc (absent)',
 'plugins/epistemic-skills/contracts/mission-custody/__pycache__/custody_gate.cpython-312.pyc (absent)',
 'plugins/epistemic-skills/contracts/mission-custody/__pycache__/custody_hook.cpython-311.pyc (absent)',
 'plugins/epistemic-skills/contracts/mission-custody/__pycache__/custody_mission.cpython-311.pyc (absent)']
rc=1
```

## Measurements (script-computed at C+1)

- `source-inventory.json@2` `file_digests`: 158 entries; **17 are
  `__pycache__/*.pyc`** (both cpython-311 and cpython-312 builds).
- On a pristine C+1 checkout: 16 inventoried files ABSENT (all `.pyc`; the
  17th, `v6-assurance/__pycache__/validate_v6_assurance.cpython-311.pyc`, was
  recreated by the seat's own import and then CONTENT-MISMATCHED the recorded
  digest — demonstrating `.pyc` volatility in-place).
- Of the 141 non-`.pyc` inventoried files: zero absent, zero
  content-mismatched at C+1. The substrate seal over real sources is intact.
- Scratch probe (in-memory only; subject untouched): with the 17 `.pyc`
  entries stripped from `file_digests` and the three listing fields, ALL
  validator stages pass at C+1 — matrix, reconciliation, source inventory,
  promotion-packet @2 rules, `validate_blocking_derivation`, candidate
  coverage, register crosswalk. Output: "ALL STAGES PASS with .pyc entries
  stripped (probe)."

## Root cause (read at C, `.github/scripts/v6_generate_candidate_packet.py`)

- `build_source_inventory` (lines ~851–887) walks the FILESYSTEM:
  `(REPO_ROOT / "plugins/epistemic-skills/contracts").rglob("*")` with
  `p.is_file()` — untracked and `.gitignore`d files included.
- `dirty_tree()` (line ~1202) uses `git status --porcelain`, which respects
  `.gitignore` — so `__pycache__/` is invisible to the clean-tree refusal but
  visible to the inventory walk. The two tree models disagree, and the
  disagreement is exactly the volatile-artifact class.
- `.pyc` content embeds the source file's mtime/size; any re-import
  regenerates it. A content digest over `.pyc` is a digest over noise.

## Why this is material (not environment noise)

1. The handoff's own premise — "the validator's digest recomputation proves
   [byte-identity]; run it yourself, trust nothing stamped" — FAILS when run:
   the validator cannot certify C+1 for anyone, including the operator.
   (The seat established byte-identity of inventoried files C..tip by direct
   `git diff` instead — zero changed — see live-verification.)
2. `OPERATOR-ACCEPTANCE-PROCEDURE.md` item 4 requires "the assurance
   validator passes on the exact packet bytes at the candidate SHA" as a
   precondition the operator personally verifies. As sealed, it cannot pass.
3. KL-RESTAMP's consequence text — "Any post-freeze edit to an inventoried
   file turns the validator red" — is silent on the validator being red on
   the UNMODIFIED sealed packet everywhere except the generating host's
   dirty tree. The restamp detector fires a permanent false positive,
   which is the availability half of the same alarm-fatigue class R5 was
   created to kill.
4. The R8 takeover makes this CI-visible: when the freeze PR is marked
   ready, `stdlib-checks` runs `validate_v6_assurance.py` on a fresh GitHub
   checkout (no `__pycache__`) → the required job goes RED. The freeze PR's
   only path to green required-checks is blocked by its own packet.
5. Repair requires a generator edit (`v6_generate_candidate_packet.py` is
   itself an inventoried `ci_scripts` file) + packet regeneration → a NEW
   candidate SHA. This is the re-freeze class: not dischargeable as a
   condition on `6db8c50…`.

## Counterweights (validation kernel — must survive any fix)

- The digest mechanism is correctly fail-CLOSED (absent/mutated → red); the
  141 real-source digests verify byte-exact on a clean checkout; the
  validator's self-test at C proves planted post-freeze mutations are caught
  (18/18 PASS). The defect is the inventory's tree model, not the concept.
- The failure is LOUD and self-revealing — it cannot silently pass, so no
  false-green risk flows from it.
- `candidate_tree_hash` in the @2 inventory binds C's git tree
  (`152b1df0…`), which IS portable and reproducible; the per-file digest
  layer is the broken half.

## Falsifier (for the panel's use)

- Method: fresh `git worktree add` (or `git clone`) of C+1 on any OS; run
  `validate_v6_assurance.py`; inspect which inventory entries are absent or
  mismatched.
- Threshold for discharge: validator exits 0 on a clean checkout of the
  freeze commit, AND a planted one-byte edit to an inventoried source file
  exits non-zero. Today: first limb fails everywhere.
- Timeframe: before operator acceptance; re-run on every packet regeneration.
