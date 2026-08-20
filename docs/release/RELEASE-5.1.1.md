# Release 5.1.1 — mission-custody security patch

**Patch release.** One subsystem changes: `mission-custody`. No skill is added,
renamed, or retired; the package still ships **fifteen** skills, and every other
contract is byte-identical to v5.1.0.

## Why this release exists

v5.1.0 shipped a custody guard that could be bypassed. The fixes have existed on
the development branch for some time, held behind a much larger release. Holding
a security fix behind an unrelated release is the wrong trade, so it ships here
on its own.

## What is fixed (es#137)

**Parent-segment traversal — false allow.** The guard matched the harness's
`file_path` as spelled. A path carrying `..` segments could resolve *inside* a
guarded tree while failing to match the guard's glob, so the write was allowed
when it should have been refused. Guard matching now collapses `..` before
matching.

Also closed: refusal-path gaps where the gate returned an ambiguous or silent
result instead of an explicit refusal, and hook-side handling that did not
propagate a refusal faithfully.

**What a refusal looks like now.** Paths that previously slipped through are
refused explicitly and fail closed. If a workflow depended on one of those
writes succeeding, it will now fail — that is the fix working, not a regression.

## What is NOT fixed — read this before relying on the guard

**`KL-GUARD-LEXICAL`.** The new `..` collapse is **lexical**. The operating
system resolves `..` only *after* following symlinks, so a write spelled through
a **symlinked parent** can still land inside a guarded tree without matching an
armed guard. This is a known, deliberate residual: resolving symlinks inside the
gate changes its failure modes on broken links and network filesystems, and that
change has not had a custody review. It is pinned by a test
(`test_guard_match_is_lexical_symlinked_parent_diverges`) so it cannot regress
silently.

**Hard links are detected, never resolved.** Scope comparison follows symlinks;
a hard link is a second name for one inode and `realpath` cannot see it.
Measured and documented in
`plugins/epistemic-skills/contracts/mission-custody/SECURITY.md`.

**Platform.** macOS default filesystems are case-insensitive, so two
contract-distinct filenames resolve to one physical file; custody distinctness
claims exclude case-insensitive filesystems. No native-Windows requalification
was run for this patch.

If mission-custody is the boundary you rely on to bound where an agent may
write, read those three limits first — they bound exactly the guarantee you are
upgrading for.

## Gate status for 5.1.1

This is a patch, gated in proportion: the deterministic suite, the custody
contract suites, the public-content gate, and full-history secret scanning at the
exact candidate. It carries **no** independent Gauntlet panel, no assurance
packet, and no publication-gate review — those belong to support points, and
5.1.1 does not claim to be one. **v5.1.0 remains the current support point;**
this patch supersedes it for installation only.

## Upgrading

Replace an older copy with a `v5.1.1` tagged checkout or plugin install, reload
the harness, and verify the skill count and source path — one install mechanism
per harness, never two. Nothing migrates on disk, so downgrading to v5.1.0 needs
no data step; the bypasses return with it.
