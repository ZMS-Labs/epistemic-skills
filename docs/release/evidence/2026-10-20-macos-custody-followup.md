# Bounded macOS custody follow-up, 2026-10-20

Subject: released source `6f31811a173967568513d5deec316199c2df7669`.
This is a local follow-up, not an amendment to v7.3.0 or a new publication.
The documented non-gating limitation remains open as
[issue #162](https://github.com/ZMS-Labs/epistemic-skills/issues/162).
The historical failure is
[run 39360876704, macOS job 118426520315](https://github.com/ZMS-Labs/epistemic-skills/actions/runs/39360876704/job/118426520315).

## Causal result

Both reported lifecycle failures reproduce on the actual macOS filesystem:
`distinct-real-file-untouched` and `distinct-both-files-tracked-separately`.
The fixture assumes `straße.txt` and `strasse.txt` name two independent files.
On the measured filesystem the second spelling already exists after creating
only the first, `samefile` is true, and writing the second changes the first.
The lexical custody comparator returns false for that pair.

A controlled run changed only the filename pair to `real-artifact.txt` and
`decoy-artifact.txt`: all 18 assertions then passed. This isolates the cause of
these two failed assertions to a two-file fixture executed on a one-file pair.
It does not establish correct custody behavior for filesystem aliases.

There is also a real, separately measured implementation defect: the existing
`probe_case_insensitivity.py` reports filesystem case folding but no comparator
folding on this POSIX host. A write to `SECRETS.env` addresses the file excluded
as `secrets.env`, while `scope_consistency()` returns no findings. This is the
existing #162 false-clean direction, not a newly discovered release failure.

## Small local test corrections

1. Preserve the Unicode lexical comparison assertions. Before the two-file
   end-to-end regression, attempt exclusive creation of the Unicode pair in a
   disposable directory on the same workspace filesystem. If it aliases, print
   an explicit `LIMITED es#162` disclosure and run the same custody/obligation/
   tampering assertions with independent ASCII names. No assertion is skipped.
   On filesystems where the pair coexists, retain the original Unicode names.
2. The formerly skipped gate suite exposed another fixture assumption:
   `tempfile` supplied a `/var` spelling while `realpath` returned `/private/var`.
   The observed expected-path comparison was false before canonicalizing the
   temporary root and true afterward. Resolve that fixture root before building
   its symlink paths. The known lexical-guard divergence and direct-match control
   remain asserted; production guard behavior is unchanged.

Only tests are changed. Do not interpret a future green diagnostic job as a
fix or positive qualification of #162 or the existing #137 lexical-guard limit.
Retain the existing diagnostic probe and inspect its measured verdict.

## Verification and limits

Environment: actual Darwin host, Python 3.14.7. No Python 3.12 or new Linux
runtime was available for this bounded local investigation; no installation,
filesystem mount, security setting or GUI action was performed.

- Released lifecycle fixture: the exact two reported failures reproduced.
- Controlled distinct-name variant: 18 checks, no failures.
- Corrected complete mission lifecycle suite: exit 0, zero failures, with the
  explicit #162 limitation line.
- Formerly skipped CLI suite: exit 0.
- Gate suite: one temporary-root spelling failure before its fixture correction;
  complete suite green afterward.
- Concurrent-missions case-table, enforcement hook and three-process continuity
  suites: each exit 0.
- Independent source review accepted both bounded test corrections and ran the
  targeted lifecycle test and full gate suite on the same Mac. Review uses the
  same model family and task context; it is not independent-platform evidence.

These results do not establish new Linux/NTFS coverage, complete macOS custody
correctness, or closure of either production limitation. Historical CI evidence
and released artifacts remain unchanged.

## Production repair boundary

A production fix must model the workspace filesystem's identity semantics rather
than infer them from `os.name`. It must align scope checks, receipt/drift keys and
obligation discharge, including absent-yet-to-be-created paths, aliases and Unicode
collisions. Blind global `str.casefold()` is unsafe: on filesystems where the
Unicode spellings coexist it can merge distinct obligations and silently lose
coverage. Existing-file `samefile()` alone cannot classify nonexistent output
paths. This broader repair needs its own contract and case-sensitive/case-insensitive
runtime regressions; it is not implemented by these test corrections.

No push, PR, merge or release is authorized or performed for this follow-up.
