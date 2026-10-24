# Re-score of E11's frozen responses — fixed scorer (2026-10-24)

**What this record is.** After E11 closed, the shipped scorer was fixed
(issue #277): a non-list `parked` — an integer count, or any other
non-list form — now scores as a per-fixture reporting-shape failure
instead of raising `TypeError` and voiding the run. This directory
records the fixed scorer's reading of E11's **preserved frozen
responses** (`../responses.json`), run once, unmodified inputs, no new
subjects, no re-dispatch.

**What this record is not.** It is not a re-run of E11 and it does not
alter E11's record: the epoch's outcome stands as recorded in
`../RESULTS.md` — **FAIL, scorer exit 1 (crash), no fixture verdicts** —
per fix F3 (no silent re-runs). Nothing here replaces the epoch's
verdict, and the first-epoch baseline (FAIL 8/10, `../../2026-08-04/`)
remains this battery's latest *epoch-scored* line. This re-score is an
instrument-repair record subordinate to the epoch record.

## Result

Fixed scorer exit code **1**; all 10 fixtures received verdicts;
**0/10 fixtures pass** on the frozen responses as declared. Full
machine record: `scorer-report.json` in this directory.

| Fixture | Fixed-scorer failure | Class |
|---|---|---|
| explicit-phrase-full | full interview terminates on empty ledger plus closing probe, or operator release (neither declared) | (b) |
| explicit-mid-execution-full | same termination-evidence failure (`operator_release: false`, no closing probe / empty ledger declared) | (b) |
| fuzzy-brief-no-fire | unknown action `None` | (b) |
| design-dialogue-defers | unknown action `None` | (b) |
| reversible-fork-absent-park | park-and-proceed must announce parked items with defaults (none declared) | (b) |
| irreversible-fork-absent-hold | irreversible un-best-guessable fork must escalate, never apply a default (`escalated` not declared) | (b) |
| irreversible-fork-present-fork-scoped | unknown action `'fork-scoped-walk'` (pinned vocabulary: `fork-interview`) | (b) |
| fork-offer-declined-deferred | unknown action `'fork-scoped-walk'` | (b) |
| fork-offer-accepted-walked | unknown action `'auto-fire-fork-scoped-walk'` | (b) |
| explicit-release-parks | operator release parks each remaining item, named, with its default — `parked` was the integer `2` | (b) |

## Reading

- The crash row now scores exactly the failure the epoch record
  characterised in advance: **(b)** reporting shape over substantively
  matching conduct (the subject reported two parked items as a count;
  the contract's vocabulary is a list of identified items).
- The remaining nine failures are also declaration-level: the frozen
  responses are sparse declarations that do not populate the contract's
  evidence fields (termination probe, escalation flag, parked items,
  walked lineage), and five of ten name the fired mode outside the
  pinned action vocabulary — two with `action: null`, three with
  improvised fork-walk names. That is the same genus as the 2026-08-04
  epoch's two diagnosed reporting-contract failures, at larger scale.
  An observation, recorded as such: the E11 dispatch quoted the
  contract from the battery README, which names the modes in prose;
  the exact action strings live in the scorer and fixtures. Whether
  the dispatch text pinned the vocabulary inline is a Phase-2 dispatch
  question, not something this re-score can settle.
- No conduct claim follows from this record in either direction: the
  frozen responses declare too little to evidence the underlying
  conduct, and scoring declarations is all a re-score of frozen
  artifacts can do.
