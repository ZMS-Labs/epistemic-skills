# R15 guard-lexical residual — probe + characterization-pin evidence (2026-08-18)

Ruling: R15-custody-residual-undisclosed (gauntlet run
`es-v6-candidate-freeze-2026-08-18`). Disclosure repair only — **no
matching-behavior change** in this freeze, per the ruling's qualification.

## The divergence probe (falsifier re-run, rc2 tree)

Setup: guard `<T>/guarded/**` armed (enforce); symlink `<T>/link` →
`<T>/guarded/sub`; harness `file_path` = `<T>/link/../x.txt`.

- Kernel resolution: `os.path.realpath("<T>/link/../x.txt")` =
  `<T>/guarded/x.txt` — the write LANDS INSIDE the guarded tree.
- Gate evaluation: `evaluate(...)['matched']` = **False** (decision
  `allow`) — `_guard_norm_path` collapses `..` textually: `link/../x.txt`
  → `<T>/x.txt`, outside the glob.
- Control: direct spelling `<T>/guarded/x.txt` → `matched` = True.

Threshold per the ruling's falsifier: ≥ 1 divergence case demonstrated →
the residual is real and the disclosure (KL-GUARD-LEXICAL /
CLM-MC-GUARD-LEXICAL) ships; the rows cite this file.

## The characterization pin

`test_custody_gate.py::test_guard_match_is_lexical_symlinked_parent_diverges`
pins four assertions: realpath lands in the guarded tree; the guard does
NOT match the symlinked-parent spelling; the collapse stays textual
(`_guard_norm_path("<T>/link/../x.txt") == "<T>/x.txt"`); the direct
spelling still matches. Skips loudly where symlinks are unavailable
(NT unprivileged — consistent with KL-WINDOWS).

## RED-proof that the pin watches (scratch copy, never committed)

`_guard_norm_path` was patched in a scratch copy to resolve via
`os.path.realpath`. Result: `guard-lexical-symlinked-parent-not-matched`
**FAILED** (with expected collateral failures in the synthetic-drive
lexical glob tests, which realpath cannot serve) — proving the pin flips
loudly on any future resolution-aware change rather than passing
vacuously. The patch was discarded; the committed tree keeps lexical
matching and the full custody gate suite green ("all green").

## Deleted-rationale restoration

The safe-direction reasoning from `test_glob_overmatch_still_held`
(added by PR #128 commit `c561213`, deleted by the es#137 fix commit
`dc33de2`) is reinstated as INHERITED REASONING in the
`_collapse_parent_segments` docstring. The deleted ASSERTION is not
restored: under the current semantics it would demand a behavior change
this freeze forbids; the prose records why the trade was made and what
residual it left.
