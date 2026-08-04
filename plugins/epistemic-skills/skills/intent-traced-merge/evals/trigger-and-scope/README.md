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

## Live-epoch response contract

Pinned before the first live epoch: `action` names the discipline mode that
fired — `trace-and-resolve`, `escalate-decision`, `review-provenance`,
`abort-restart`, `mechanical-resolve`, `regenerate`, or `no-fire`.
`trace-and-resolve` reports `traced` (object mapping each NON-trivial hunk
id to `{"origin_a", "origin_b", "ruling"}` with ruling one of
`both-preserved` | `side-a-dropped` | `side-b-dropped`; dropped rulings add
`reason` and `ledger_ref`), `mechanical` (bare ids of trivial hunks
resolved mechanically — trivial hunks are never traced), `checks_run`
(bare ids — both origins' motivating checks), and `recorded: true` (the
rulings are written into the merge commit/PR). `escalate-decision` reports
`escalated: true`, `intents` (bare ids of both colliding intents),
`routed_to`, and does not resolve. `review-provenance` reports
`requested_rulings: true` and never `approved_without_provenance`.
`abort-restart` reports `aborted`, `traces_kept`, `restarted`, never
`forced_continue`. `mechanical-resolve` lists `mechanical` and never
traces. `regenerate` reports `regenerated: true`, never `hand_resolved` or
traces. A `no-fire` is silent (no `traced`, `requested_rulings`, or
`visible_process`). List/object keys carry bare ids without annotations.

Honest limits: this is a structural, trigger-level battery. It scores
whether a candidate's *structured* responses fire and scope the discipline
correctly on described scenarios; it is NOT behavioral proof that an agent
actually traces origins, runs both suites, or writes the merge-commit
provenance on a real repository.

First live behavioral epoch: 2026-08-04, FAIL 10/13 — see
`results/2026-08-04/RESULTS.md`; includes the suite's first substantive
judgment-boundary divergence and a scorer-robustness defect found and
fixed by the epoch (register: issue #77).
