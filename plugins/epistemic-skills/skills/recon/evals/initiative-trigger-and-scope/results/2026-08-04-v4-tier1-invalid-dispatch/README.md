# INVALID RUN — dispatch defect (not skill evidence)

This 2026-08-04 v4 Tier-1 dispatch sent each fixture's `scenario` sentence
only. Four of this battery's fixtures carry a `decision_graph` whose
canonical node ids and dependency structure the scenario text does not
state — the first epoch (see `../2026-08-04/RESULTS.md`) restated those
facts neutrally in the dispatch, this run did not. Subjects therefore
invented their own decision vocabularies; the scorer (correctly) rejected
them, and one frontier-of-objects response exposed a scorer crash instead
of a named failure (fixed in `score.py` the same day — fail-closed named
failures, semantics unchanged; the raw crash is preserved in
`scorer-report-crash.json`, the post-fix scoring in `scorer-report.json`).

Nothing here measures the skill: the run violates
`docs/policy/LIVE-EPOCH-DISPATCH-CONTRACT.md` rule 1 (the scorer's closed
vocabulary must reach the subject inside the pinned dispatch). It is
retained as the defect record. The corrected epoch — same fixtures, same
contract, decision graphs restated neutrally per the first epoch's
methodology — is the battery's valid v4 Tier-1 run in
`../2026-08-04-v4-tier1/`.
