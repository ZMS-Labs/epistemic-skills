# Corrections to the Wave 2 record (2026-10-24, post-close)

This addendum records every correction applied to the evidence
program's branch after the Wave 2 close (`383318c`), in response to
CI failures and Codex review findings on PR #273 (and the stacked
PRs #279–#281, whose threads raised findings against files this
branch adds). It follows the program's honesty rule: no epoch record
was silently rewritten, no preserved response file was altered, and
every instrument change below post-dates the epoch it affects — the
recorded verdicts were scored under the prior instrument versions
and stand as recorded. Where a fix's effect on the frozen responses
could be checked mechanically, it was, and the result is stated.

## C1 — Absolute paths in scorer-report wrappers (CI: public-content gate)

Thirteen `results/2026-10-24/scorer-report.json` files recorded the
scorer as an absolute build-machine path
(`/home/<user>/workspace/epistemic-skills-evidence/…` — angle brackets
added so this document itself passes the gate), which the
repo's public-content gate (`check_public_content.py`) rejects; this
one defect failed both the `stdlib-checks` and `contract` checks on
PR #273. **Fix (commit `11d029b`):** the prefix was stripped in all
13 files (14 occurrences, including one embedded crash-traceback
string in the open-questions record), leaving repo-relative paths.
Scorer identity and all epoch data are unchanged; the gate now
passes on the tree.

**Preventive finding.** No battery `score.py` writes that field — the
scorers print their report to stdout and write no path anywhere. The
`{"scorer": …, "exit_code": …, "report": …}` wrapper is assembled by
the epoch-run harness, and the traceback string is Python's own
formatting of an absolute-path invocation. The preventive rule is
therefore a harness rule, recorded here for every future epoch run:
(a) scorer-report wrappers record the scorer by its **repo-relative**
path; (b) scorers are invoked by repo-relative path so tracebacks
stay relative; (c) `check_public_content.py` runs before epoch
records are committed — the gate existed and caught this; the branch
was published without running it.

## C2 — No-fire silence was not fully enforced (six scorers)

`5cabfa0`. The trigger scorers for epistemic, metacognate, triage,
watch, manifest, and did-it-land checked no-fire rows only against an
enumerated field list, so an `explanation` (or any unlisted key)
passed. They now reject any key beyond `id` and `action`, mirroring
the health and perspective scorers; each battery's suite carries the
mutation as a regression. **Frozen-response check:** re-scoring the
preserved E1/E2/E3/E5/E7/E8/E9 responses under the strict scorers
changes no verdict (zero strictness failures; metacognate's two
failures are its recorded conduct failures).

## C3 — Manifest clean-resume outcome now fixed by the fixture

`3a7c3a0`. On the clean resume fixture (`drift: false`) the scorer
branched on the response's own claimed status, so invented drift with
`continued: false` passed. The fixture now sets the outcome:
`drift_status` must be `clean` and `continued` true. Regressions
cover both invented-drift mutations. **Frozen-response check:**
preserved E8 responses re-score PASS under the fixed scorer.

## C4 — did-it-land: unknown response ids; REVERTED needs an observation

`69489a1`. Extra responses with ids outside the fixture inventory
were silently ignored; they now fail by name. REVERTED required only
verdict + `persistence: "observed"`; it now requires a nonempty
`consumer_observation`, like LANDED. Regressions cover both.
**Frozen-response check:** preserved E9 responses re-score PASS.

## C5 — Triage trigger: NARROWED must name an eliminated candidate

`27c7bd1`. An empty `eliminated: []` satisfied the NARROWED shape
check; NARROWED now requires at least one nonempty eliminated entry.
Regression covers the mutation. **Frozen-response check:** preserved
E5 responses re-score PASS.

## C6 — Behaviour-oracle ground truths corrected (E6)

`c51f259`. Two fixtures (`clause-check-red-cause-unknown`,
`degraded-observation-would-be-destructive`) pinned NARROWED where
no eliminating observation occurs in the scenario; under triage's
verdict definitions the supported verdict is UNKNOWN. Both are
re-pinned for future epochs. The E6 epoch record's interpretation is
amended by a dated correction (the (a)-conduct characterisation of
those two cases is withdrawn); the epoch outcome (FAIL 4/12) and
response record are unmodified. A subordinate re-score of the frozen
responses under the corrected fixtures passes 6/12 and is recorded
at `plugins/epistemic-skills/skills/triage/evals/behaviour-oracle/results/2026-10-24/rescore/`;
it replaces no epoch verdict.

**Third fixture (follow-up adjudication, same principle; lands with
this note).** `degraded-no-readout-self-probed` — also named in
Codex's finding on PR #281's thread — pinned NARROWED with
`expected_eliminated: []` while its scenario states nothing
distinguishes the candidates (a full disk, a permissions change, a
storage-backend outage); the one probe, a test export failing with a
storage-write error, eliminates none of them. It is re-pinned
UNKNOWN on the identical rule; the balanced example and the suite's
verdict-count assertion follow (NARROWED 5 / UNKNOWN 5). The
(a)-conduct characterisation of this case is withdrawn in the same
dated correction to the E6 record, and the subordinate re-score
under the fully corrected fixtures moves from 6/12 to **7/12**. It
replaces no epoch verdict.

## C7 — Behaviour-oracle: canonical labels disclosed

`c51f259` (same commit as C6). The positive control's
`expected_cause` and the known-broken case's `expected_eliminated`
pinned exact strings the scenarios never supplied. Both scenarios
now disclose the canonical labels, expected values unchanged; the
battery README carries the revision note. E6 ran under the prior
revision, so its two exact-string naming failures are
instrument-attributable in that respect; the remedy is prospective.

## C8 — E10 record: cross-epoch model claim corrected

`e50a0d5`. The context-audit second-epoch record falsely asserted
both epochs used the same model family and harness. Baseline epoch:
claude-fable-5, Claude Code harness. This epoch: Muse Wonder
subagents. The record is corrected in place with a marked correction
section: the 8/14 → 11/14 difference mixes the model/harness change
with the epoch change and is not within-model improvement. Epoch
results and outcome unchanged.

## Adjudication recorded, no change on this branch

- **Health canonical subject names (Codex P2 on #273).** Valid
  against this branch: the health scorer requires exact subject-name
  equality while this branch's scenarios never supply the canonical
  names (E4's 10/13 includes three such false negatives). The fix
  exists downstream as PR #281, which states the canonical names in
  the nine readout scenarios. E4's FAIL stands against the prior
  battery revision; the revised battery has no live epoch yet.
