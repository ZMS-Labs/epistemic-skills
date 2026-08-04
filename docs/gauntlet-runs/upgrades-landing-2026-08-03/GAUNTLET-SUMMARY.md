# GAUNTLET SUMMARY: landing the stranded upgrade PRs (#65, #54, #50)

## Meta
- **Date:** 2026-08-03
- **Subject:** branch claude/epistemic-skills-upgrades-ew8r3v tree 4e49ba5f (6 commits over main e7de363) — full diff at evidence/diff.patch
- **Axis:** fixed-artifact gate
- **Triage:** passed — security-posture CI changes + high-risk integration, findings falsifiable
- **DeepReason root:** none (manual docket; hypotheses H1-H6 in the dossier)
- **Panel composition:** disgruntled-maintainer, chaos-monkey, cloud-native-purist, decision-rights-auditor, ecological-systems-analyst (subject-seeded wildcard); gate: red-lines-arbitrator; judge: pragmatic-judge
- **Depth:** standard
- **Docket mode:** manual-docket
- **Independence mode:** concurrent isolated role-agents
- **Role binding:** materialized-role

## Executive Verdict
- **Independence disclosure:** concurrent isolated role-agents; ALL seats same model family (Claude) — the different-family judge preference was not satisfiable in this harness; Step 7b external cross-family adjudication not run (operator-gated).
- **Computed Verdict:** CONDITIONAL
- **Summary:** the landed content is verified sound — 164/164 [V] anchors mechanically verified, 31/31 CI-equivalent battery, byte-identical tree across the DCO-clean history rebuild, and the panel's sole P1 (unverified action-SHA pins) was OVERRULED by live falsifier execution. Every open condition concerns the **merge step's accountability chain**, not the diff's content: the same single agent identity authored, integrated, and locally verified everything, and GitHub-side CI has not yet run.
- **Verdict gate applied:** zero P1 open (sole P1 OVERRULED via executed falsifier); five P2 open → CONDITIONAL. Red-lines gate PASS-WITH-NOTES imposes no cap.

## Durable records the conditions call for (written here at Step 8)

**R1 — action-pin verification record (2026-08-03, verified twice: red-lines gate seat, then independently re-executed by the integrating session):**
- `actions/setup-python` v5.6.0 == `a26af69be951a213d495a4c3e4e4022e16d87065` (git ls-remote refs/tags/v5.6.0)
- `actions/setup-go` v5.0.2 == `0a12ed9d6a96ab950c8f026ed9f722fe0da7ef32` (git ls-remote refs/tags/v5.0.2)
- `actions/checkout` `34e114876b0b11c390a56381ad16ebd13914f8d5` == refs/tags/v4.3.1 (also already trusted by main's dco.yml)

**R3 — original-head provenance record:** the branch lands content from PR #65 head `a51c77b` (branch codex/address-codex-security-findings-and-prs; commit author SternOne, sign-off Codex) and PR #54 head `da3e013` (codex/coordinate-epistemic-skills-with-calibration-repo; author SternOne, no sign-off), plus a hand port of PR #50 (agent/issues-36-38-dogfood-enforcement, commits ad9cb1c..4b8502e, author SternOne). Squash-style integration was forced by the repo's author-matching DCO policy, which both original heads fail (evidence/dco-check.txt). The human certifying party for the merge is the operator taking the R4 merge decision.

**R9(a) — charter freshness check:** `git diff da3e013 HEAD -- docs/coordination/epistemic-calibration.md` is empty — the charter body is unchanged since PR #54's head; its formal-rigor record's subject-revision-unchanged predicate holds on this tree.

## Open conditions (blocking follow-ups for the merge — a CONDITIONAL is not a GO)
~~~json
[
 {
  "ruling": "R2-github-ci-execution",
  "condition": "All three workflows (epistemic-flexibility, dco, release-security) run green on GitHub-hosted runners against exactly tree 4e49ba5f, with run URLs attached to the run evidence or PR body, closing the dossier's second UNVERIFIED label.",
  "falsifier": {
   "method": "Open a draft PR (or push) from branch head 4e49ba5f and observe GitHub check-run conclusions for all three workflow files.",
   "threshold": "3/3 workflows green with zero action-resolution, runner-label, or timeout failures; any red confirms the finding and blocks merge.",
   "timeframe": "First CI cycle (~30 minutes), before merge."
  },
  "owner": "operator"
 },
 {
  "ruling": "R3-provenance-record",
  "condition": "Original-head authorship (a51c77b — SternOne; da3e013) and the human certifying party for the six agent-signed commits are recorded in at least one durable location: Co-authored-by trailers, the PR body, or a ledger entry — outside the integrator-only evidence file.",
  "falsifier": {
   "method": "Inspect commit trailers on origin/main..HEAD, the PR body, and .ledger/entries.jsonl for the original heads and a human-traceable certifier.",
   "threshold": "Both original heads and a named human certifying party present in >=1 durable location.",
   "timeframe": "Before merge."
  },
  "owner": "operator"
 },
 {
  "ruling": "R4-operator-merge-decision",
  "condition": "The merge is taken as an explicit operator decision: an operator-opened or operator-approved PR whose body names the re-scoped shape (workflows-only #65, #54, ported #50), surfaces the C9 override and the C13 scope interpretation, includes the R1 pin-verification record, and cites this gauntlet ruling; plus a durable ledger decision entry naming the operator as decider. Merge on harness authority alone fails this criterion.",
  "falsifier": {
   "method": "Check GitHub PR events for the operator-authored approval artifact and .ledger/entries.jsonl for the decision entry.",
   "threshold": "Artifact exists, explicitly acknowledges C9 and C13, names the operator as decider.",
   "timeframe": "At merge time; before the branch reaches main."
  },
  "owner": "operator (non-delegable)"
 },
 {
  "ruling": "R5-kernel-gate-coverage",
  "condition": "Either (a) CI validates real arbitration/ruling-set artifacts (glob docs/gauntlet-runs/**) so a kernel-less OVERRULED ruling in a real artifact fails the battery, or (b) a committed scope statement narrows the #37 enforcement claim to fixture-only coverage in writing. The chosen path is named in the R4 merge-decision record.",
  "falsifier": {
   "method": "Path (a): commit a real arbitration file containing an OVERRULED ruling without validation_kernel on a scratch branch and execute the full per-step battery. Path (b): locate the committed scope statement in README/docs.",
   "threshold": "(a) any battery step exits non-zero naming the file, or (b) the scope statement exists.",
   "timeframe": "Before merge, or in the first follow-up PR if so recorded in the merge decision."
  },
  "owner": "operator / first follow-up PR"
 },
 {
  "ruling": "R6-ledger-tamper-evidence",
  "condition": "Either (a) a CI append-only/byte-identity check compares committed ledger lines against merge-base (existing lines byte-identical, new lines append-only), or (b) the tamper-evidence gap and the backdated 2026-07-22 entry's legitimacy as a port of the PR #35-era decision are explicitly accepted in a durable ledger entry.",
  "falsifier": {
   "method": "Path (a): mutate one existing line of .ledger/entries.jsonl (schema-valid) on a scratch branch and run the full battery. Path (b): locate the residual-risk acceptance entry.",
   "threshold": "(a) any battery step fails on the mutated store, or (b) the acceptance entry exists naming both the gap and the backdated entry.",
   "timeframe": "With merge or in the first follow-up PR."
  },
  "owner": "operator / first follow-up PR"
 }
]
~~~

## P3/P4 follow-ups (non-blocking, tracked in the ruling set)
R7 ledger merge-ordering protection; R8 audit inventory tripwire + marker word-boundaries; R9(b) charter banner + revision-pinned schema handoff; R10 consumer-side accepted-gate binding before charter Phase 4; R11 dependabot github-actions config + pin-inventory owner; R12 validator root-discovery message.

## GO/CONDITIONAL coverage statement (required)
- **Capability families exercised:** security (insider/supply-chain), reliability/chaos, operability (cloud-native), governance-ethics (decision rights), systems-structure (ecological); categorical red-lines gate; evidence-weighted arbitration.
- **Material assumptions reviewed:** action-pin authenticity (resolved live), single-actor trust chain, DCO policy compliance, ledger store integrity, gate coverage claims, calibration-contract staleness.
- **Known unknowns / untested behavior:** GitHub-hosted runner behavior of the three modified workflows (uses-resolution, permissions, timeouts, triggers) — untested until the first push/PR CI cycle (condition R2); calibration-side adoption (out of scope per charter).
- **Evidence freshness:** all anchors frozen 2026-08-03 in the run's evidence root (pin 4dd15d61…); ls-remote checks executed 2026-08-03/04.
- **Residual uncertainty:** same-model-family panel and judge (disclosed above); ledger tamper-evidence gap (R6) and kernel-gate fixture-only coverage (R5) remain open with named cheap discharge paths.

## Honest labeling
Scores mean best-argued-in-the-bracket, not true. The heavy P2 surface on the accountability chain is the panel working as intended on a single-actor landing, not damage to the content verdict.
