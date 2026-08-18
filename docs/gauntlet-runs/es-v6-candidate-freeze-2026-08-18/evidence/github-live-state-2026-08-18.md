# Live GitHub state snapshot — recorded 2026-08-18 (this session, via GitHub API)

Recorded by the independent Gauntlet seat before dossier freeze. All reads
performed live this session against ZMS-Labs/epistemic-skills; nothing below is
taken from the successor brief or from session memory.

## Check runs on PR #194 head (7de88fab412e56268b73371e1cd44138987911ae)

| Check | Conclusion | Run/Job id |
|---|---|---|
| stdlib-checks | **skipped** | job 95752519846 (run 32149796340) |
| contract (mission-custody) | **skipped** | job 95752519793 (run 32149796394) |
| contract-macos | skipped | job 95752550430 (run 32149796394) |
| DCO | skipped | job 95752518254 (run 32149795789) |
| full-history-secret-scan | **skipped** | job 95752520056 (run 32149796460) |
| build (openai-bundles) | skipped | job 95752520479 (run 32149796346) |
| Analyze (actions) | success | job 95752524861 (run 32149795213) |
| Analyze (javascript-typescript) | success | job 95752524860 (run 32149795213) |
| Analyze (python) | success | job 95752524839 (run 32149795213) |
| CodeQL | success | check 95752756272 |

## Check runs on PR #193 head (e8a476c730750a9b3e51ac1001b96825996187cc)

| Check | Conclusion | Run/Job id |
|---|---|---|
| stdlib-checks | **skipped** | job 95741598079 (run 32146557804) |
| contract (mission-custody) | **skipped** | job 95741597988 (run 32146557670) |
| contract-macos | skipped | job 95741638172 (run 32146557670) |
| DCO | skipped | job 95741621444 (run 32146554910) |
| full-history-secret-scan | **skipped** | job 95741646639 (run 32146557701) |
| build (openai-bundles) | skipped | job 95741598469 (run 32146557672) |
| Analyze (actions) | success | job 95741593150 (run 32146554033) |
| Analyze (javascript-typescript) | success | job 95741593165 (run 32146554033) |
| Analyze (python) | success | job 95741593220 (run 32146554033) |
| CodeQL | success | check 95741778707 |

Reading: on both draft PRs every gating suite job reports `skipped`; only the
CodeQL analyze matrices ran and succeeded. This confirms gauntlet-request
premise 2 at the live-API level, complementing the workflow-file `if:` lines.

## PR state

- PR #194: open, draft=true, head `cursor/v6-candidate-build-5c03` @ 7de88fa,
  base main @ a2b9c0d, mergeable_state clean, created 2026-08-18T14:39:47Z.
- PR #193: open, draft=true, head `cursor/custody-137-p1-false-allows-5c03`
  @ e8a476c, base main @ a2b9c0d, mergeable_state clean.

## Open tracker inventory (live, 2026-08-18)

41 open issues:
191, 186, 173, 170, 169, 168, 167, 166, 165, 164, 163, 162, 161, 160, 159,
158, 157, 154, 151, 150, 149, 148, 147, 145, 142, 141, 140, 139, 137, 136,
129, 124, 118, 105, 104, 95, 89, 84, 77, 40, 39.

5 open PRs: 194, 193, 176, 103, 100.

Operator-hold labels observed live: #104 carries `gate:operator`,
`work:decision`, `assurance:R0`; #84 carries `gate:operator`,
`work:dependency`, `work:decision`, `assurance:R2`; #40 carries
`gate:operator`, `gate:external`, `work:dependency`, `work:decision`,
`assurance:R3`. #186 carries no labels; its operator-owned remainder
(tag-ruleset decision) is recorded in the packet and RELEASING.md step 7.

Coverage check performed this session: the issue set and PR set in
`docs/v6/ES6-V6-CANDIDATE/issue-pr-reconciliation.json` and the
CLM-ISSUE-*/CLM-PR-* rows of `claim-to-proof-matrix.json` equal the live
open sets exactly (41 + 5, no missing, no extras).

## Issue #191 state

Open. Title: "v6.0 assurance program: exact-candidate qualification and
two-stage release gate". Terminal contract, two-stage boundary (BUILD /
PROMOTION, operator-approved 2026-08-17), and required reconciliation list as
described in the packet. The issue authorizes no merge/tag/release/settings
acts and does not approve PR #190 or the tag-governance questions.
