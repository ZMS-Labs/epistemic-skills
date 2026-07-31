# Intent-Traced Merge trigger-and-scope fixtures

This battery tests the trigger discipline and the classification contract:
non-trivial conflict hunks (semantic overlap, ambiguous textual resolution,
divergent-decision branches) are traced to both origins, ruled explicitly,
verified against both sides' motivating checks, and recorded; trivial hunks
resolve mechanically with no trace; regenerable artifacts (lockfiles,
generated files) are regenerated, never hand-resolved; a genuinely open
design collision escalates instead of being decided inside the merge; an
undocumented merge commit under review has its rulings demanded; an
uncertain working tree is aborted with the traces kept. Tracing trivial
hunks, hand-resolving lockfiles, silently deciding designs, and bulk-side
selection are defects, not extra rigor.

Run `python tests/run_tests.py`.

Honest limits: this is a structural, trigger-level battery. It scores
whether a candidate's *structured* responses fire and scope the discipline
correctly on described scenarios; it is NOT behavioral proof that an agent
actually traces origins, runs both suites, or writes the merge-commit
provenance on a real repository.

No live behavioral epoch has been run against this battery; see
`results/BLOCKED.md`.
