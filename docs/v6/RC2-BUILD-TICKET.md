# RC2 BUILD ticket — repairs for the NO-GO rulings (run es-v6-candidate-freeze-2026-08-18)

Source of truth: the ruling-set@1 block in the gauntlet run's arbitration.md.
This file is the working checklist on the rc2 branch; acceptance criteria are
quoted VERBATIM from the ruling-set. Operator decisions D1-D15:
docs/v6/operator-decision-record-2026-08-18.md (RATIFIED, echo-certified).

Discipline: every repair edits committed artifacts, so the candidate SHA moves;
requalify everything at the final SHA. TDD where code changes: RED first.

## R1-terminal-gate-forgeable (P1, UPHELD, status open)

Basin: Terminal readiness gate has zero rejection power (self-written GO)

- [ ] AC1: promotion-packet.schema.json gains gauntlet_run_id, gauntlet_verdict_path, gauntlet_subject_sha; validate_v6_assurance.py additionally requires, for terminal readiness: blocking_claims == [] and an on-disk verdict artifact whose subject SHA equals candidate_sha. Generator's NOT_READY/NOT_RUN/refused defaults preserved unchanged.
  - falsifier: method: Re-run the recorded mutation probes on the re-submitted packet tree: (a) flip readiness to terminal + independent_gauntlet='GO' with blocking_claims left at 9 and no verdict artifact; (b) candidate_sha := '0'*40; (c) delete one cited evidence_paths file; run validate_v6_assurance.py after each. | threshold: Non-zero exit on every mutation, with the message naming the unresolved blockers, missing verdict binding, SHA mismatch, or missing evidence path. Any exit 0 leaves the defect standing. | timeframe: Before any packet re-submission is put before the operator; re-run on every subsequent packet.
  - owner: agent (implementer lineage), verified by the next independent panel

## R2-secret-scan-unclaimed-unrun (P1, UPHELD, status open)

Basin: Release-security full-history secret scan: no claim, no run, no disclosure

- [ ] AC1: CLM-SECRET-SCAN added to the class matrix (authority RELEASING.md item 6a; oracle: release-security full-history-secret-scan green at the exact candidate including the planted-secret positive control; status UNPROVED until such a run exists) and added to blocking_claims; KL-DRAFT-CI's skipped-job enumeration corrected to all five observed skipped gating jobs. Evidence, when produced, is a {workflow, run_id, job_id, head_sha, conclusion} record at the exact candidate ref via workflow_dispatch on a scratch branch — an act the operator must first classify under the two-stage boundary (see R3/gate act-hygiene note).
  - falsifier: method: Parse claim-to-proof-matrix.json and promotion-packet.json of the re-submitted packet for a claim/known_limit naming the full-history secret scan; if evidence is claimed, fetch the named run and compare head_sha to the candidate SHA and read the positive-control step conclusion. | threshold: At least one matrix row naming the scan with explicit status and release_consequence, present in blocking_claims while unrun; if marked satisfied, run record at the exact candidate SHA with positive control detected. Zero rows leaves the defect standing. | timeframe: Row and disclosure: at re-submission. Run evidence: before operator acceptance.
  - owner: agent adds row/disclosure; operator classifies and authorizes the branch-push + dispatch acts

## R3-build-window-merges-unreconciled (P1, UPHELD-WITH-QUALIFICATIONS, status open)

Basin: Three BUILD-window merges to main (#190/#156/#192) without resolvable authorization or packet disclosure

- [ ] AC1: The operator explicitly ratifies or reverses each of the three merges (#190, #156, #192) in a durable, operator-authored artifact (issue comment, review, or signed record), AND the packet adds reconciliation rows (or a closed-item ledger) for all three, citing the authorization artifact, plus a known_limit disclosing that the candidate's base was produced by BUILD-window merges.
  - falsifier: method: Read the named artifact for each merge (pull_request_read get_reviews/get_comments; issue #191 comments postdating 2026-08-18T00:37:06Z); grep the re-submitted packet for rows/limits naming #190/#156/#192. | threshold: An operator-authored ratify-or-reverse record exists for each of the three AND at least one packet row/limit names each. Either half missing leaves the defect standing; no agent-side evidence can discharge it. | timeframe: Before any acceptance-supporting verdict is recorded — this condition gates every acceptance path per the red-lines gate.
  - owner: operator (sole; explicitly not agent-dischargeable)

## R4-candidate-sha-binding-failure (P1, UPHELD, status open)

Basin: Exact-SHA requalification not met at 00e5146: the candidate cannot name itself and no required surface was evaluated there

- [ ] AC1: Re-freeze so that ONE SHA carries a self-consistent packet: either a format change (placeholder + digest manifest, SHA bound at verification) so the freeze names itself, or an explicit declaration that the packet-head tree is the reviewable subject; README names the subject SHA literally; every evidence_paths entry exists in that tree; required surfaces (stdlib-checks, mission-custody contract, release-security) evaluated at that exact SHA via workflow_dispatch on a scratch branch, with {run_id, job_id, head_sha, conclusion} recorded, read per RELEASING.md:114-124 required-job semantics.
  - falsifier: method: Check out the declared subject SHA in isolation; read exact_start_sha/candidate_sha from all five artifacts; verify evidence_paths existence; grep README for the literal SHA; fetch the named workflow runs and compare head_sha. | threshold: All artifacts stamp the subject SHA, zero dangling evidence paths, README contains the literal, and each required job executed (conclusion != skipped) at head_sha == subject SHA. Any mismatch leaves the defect standing. | timeframe: At the next freeze, before the replacement packet is submitted for an independent verdict.
  - owner: agent executes; operator classifies the scratch-branch-push and dispatch acts (default-deny until classified, per gate act-hygiene)

## R5-immutability-without-mechanism (P1, UPHELD, status open)

Basin: Immutable-packet claim has no anchor, no detector, an undisclosed post-freeze mutation, and a destructive regeneration recipe

- [ ] AC1: (a) A pin tag (repo pin/ convention) anchored to the subject SHA and registered in check_pin_tags.py PINS — created only after the operator resolves whether forbidden_this_run's 'tag' covers non-version pin tags; (b) per-file sha256 digests (or a packet manifest) plus the candidate tree SHA in source-inventory.json, verified by validate_v6_assurance.py alongside cross-artifact SHA agreement and evidence-path existence; (c) a KL-RESTAMP known_limit disclosing the 5-artifact restamp, the post-freeze addition of clean-baseline.json, and restoring the deleted disclaimer's substance; (d) the generator refuses to overwrite a committed packet whose candidate_sha differs, absent an explicit --restamp flag.
  - falsifier: method: Re-run the tamper probe (fabricate all SHA fields, delete a cited evidence file, run the validator); list origin tags and peel them; grep PINS; run the README Regenerate command verbatim in a scratch copy and git-diff the packet directory. | threshold: Validator exits non-zero on tampering; one origin tag peels to the subject SHA and appears in PINS (or a recorded operator ruling forbids the tag, with an alternative durable anchor recorded); regeneration is byte-stable or fails loudly naming the SHA mismatch. | timeframe: Before operator acceptance; the tag/PINS check re-run again before any PROMOTION_RUN.
  - owner: agent (manifest, validator, disclosure); operator (pin-tag classification and creation)

## R6-tracker-reconciliation-citation-only (P1, UPHELD-WITH-QUALIFICATIONS, status open)

Basin: CLM-TRACKER-RECONCILED PROVED on a strong statement its oracle cannot test; 46 tracker rows structurally incapable of failing

- [ ] AC1: Either (a) demote CLM-TRACKER-RECONCILED from PROVED and rewrite its statement to match what its oracle tests, relabeling the tracker section as a disposition census; or (b) keep the strong statement and populate per-item oracles distinct from release_consequence, materially differentiated falsifiers, resolvable evidence paths, and non-empty blocked_by on the 7 blocked-parent rows. Additionally: the generator fails (or loudly warns, with the count recorded in the artifact) on any tracker item absent from ISSUE_DISPOSITIONS.
  - falsifier: method: Parse the re-submitted matrix/reconciliation: count distinct falsifier strings, rows with oracle != release_consequence, rows with non-empty evidence_paths, blocked-parent rows with non-empty blocked_by; run the generator with a stub tracker containing an unknown issue number. | threshold: Path (a): status != PROVED and statement matches oracle. Path (b): distinct falsifiers >= 20, oracle != release_consequence on >= 40/46, non-empty evidence_paths on >= 40/46, 7/7 blocked-parent rows name a blocker. Both paths: unknown issue produces non-zero exit or a recorded warning count. Anything at or near 1/0/0/0-and-silent leaves the defect standing. | timeframe: At re-submission; reconciliation re-run (or re-dated) within 24h of operator acceptance since it decays from the next filed issue.
  - owner: agent

## R7-wf-path-coverage-proved-row (P2, SPLIT, status open)

Basin: CLM-WF-PATH-COVERAGE: PROVED row whose own falsifier fires (named factual conflict)

- [ ] AC1: Either (a) remove the paths: blocks from epistemic-flexibility.yml's pull_request/push triggers (matching the repo's own adjudicated treatment of release-security.yml), making the statement true; or (b) demote CLM-WF-PATH-COVERAGE to PARTIAL with a known_limit enumerating the 72 uncovered tracked files. In both paths: narrow the release_consequence to the property actually proved (path-filter dispatch coverage) and add a separate honest-status claim for draft-gating and fail-fast skip risk; strengthen v6_audit_workflow_oracles.py to classify whole-tree readers (git ls-files walks) as requiring unfiltered triggers.
  - falsifier: method: At the re-frozen tree: evaluate the changed-file set of a scratch PR confined to a previously-unfiltered file against the triggers (or re-run cnp's fnmatch evaluation); parse the matrix row's status and release_consequence. | threshold: Path (a): zero tracked files outside the filter (filter absent). Path (b): status == PARTIAL with the 72-file limit recorded. Both: release_consequence no longer claims silent-skip coverage. A PROVED status with the current statement and filter leaves the defect standing. | timeframe: At re-freeze; the row edit necessarily produces a new SHA, so it cannot be discharged as a condition on 00e5146.
  - owner: agent

## R8-ready-for-review-takeover-absent (P1, UPHELD, status open)

Basin: KL-DRAFT-CI's sole compensating control (ready-mark takeover) does not exist in the trigger configuration

- [ ] AC1: Add types: [opened, synchronize, reopened, ready_for_review] to the pull_request trigger of the five gating workflows (mirroring dco.yml), then drill once on a throwaway draft PR and retain the transcript. Until the drill transcript exists, strike 'until the PR is marked ready' from KL-DRAFT-CI and state that no pull-event path to required-job green exists on this branch without a new commit or PR.
  - falsifier: method: On a throwaway branch touching trigger paths, open a draft PR, record check-runs, mark ready with no push, re-list workflow runs/check-runs at the identical head SHA (haha's drill, verbatim). | threshold: At least one new workflow run created by the ready_for_review action for each gating workflow at the unchanged head SHA, gating job conclusion != skipped. Zero such runs — or an unamended KL-DRAFT-CI without the transcript — leaves the defect standing. | timeframe: Single drill, under fifteen minutes, before re-submission; branch deleted afterwards.
  - owner: agent (workflow edit + drill); operator classifies the ready-mark act itself in the two-stage boundary (unclassified acts are default-deny)

## R9-cleanroom-undercoverage (P2, UPHELD, status open)

Basin: Clean-room BUILD oracle under-coverage and KL-DRAFT-CI overstatement

- [ ] AC1: cleanroom_ci.sh (or the workflow-oracle audit) gains a completeness assertion — every python-invoking line in the workflow is either extracted or on an explicit, justified in-repo exclusion list, failing on divergence — and prints extracted-of-total plus the workflows it does not read; argparse-usage SKIPs counted into the headline; KL-DRAFT-CI rewritten to name all five skipped gating jobs and the measured scope (34 of 53 lines of one of six workflows), and to note that independent step execution cannot observe CI fail-fast ordering.
  - falsifier: method: Apply the extractor regex at the re-frozen tree against the workflow; diff extracted set vs full enumeration; grep for the completeness assertion and run the harness after commenting out one extractable step's indentation. | threshold: The harness fails (or lists the exclusion) when counts diverge, and its output states numerator and denominator; KL-DRAFT-CI enumerates 5/5 skipped jobs. A bare 'N passed' with a non-empty unlisted complement leaves the defect standing. | timeframe: At re-submission; re-check on every edit to epistemic-flexibility.yml.
  - owner: agent

## R10-rollback-premise-main-red (P2, UPHELD-WITH-QUALIFICATIONS, status open)

Basin: Rollback plan's safe harbour (main) is live-red on its required gate, undisclosed

- [ ] AC1: A known_limit (kind: integrity) recording that origin/main is red on required stdlib-checks at the Public-content step, that eleven downstream release-gate steps have not executed on main's head, and that this candidate line is the in-flight fix; the rollback sentence qualified accordingly.
  - falsifier: method: Grep the re-submitted packet's known_limits for the main-red disclosure; independently re-read the newest push run on main (list_workflow_runs branch=main, then job/step conclusions) at the moment of operator acceptance. | threshold: Disclosure present AND consistent with the live state at acceptance time (a subsequent green push to main retires the disclosure need and falsifies the finding). Missing disclosure with main still red leaves the defect standing. | timeframe: Disclosure at re-submission; live re-check at the moment of operator acceptance.
  - owner: agent

## R11-public-content-gate-silenced (P2, UPHELD, status open)

Basin: Public-content gate: whole-file permanent allowlist widening on a live generator; self-falsifying recorded evidence; pasted-stdout substrate

- [ ] AC1: (a) Either make allowlist entries pattern-scoped, or record a sha256 per allowlisted file at exemption time and fail closed when an allowlisted file changes without an allowlist-review update; or redact/relocate the parent_program string per the addendum's own disposition. (b) Correct CLM-PUBLIC-CONTENT's closure_path to state the true blast radius, and reconcile its falsifier text with its allowlist-scoped statement. (c) Regenerate evidence/public-content.json at the subject SHA on a clean tree (collector refuses on dirty git status), so stamped SHA and stdout are consistent. (d) Retire the three inert allowlist entries and record an owner/review cadence for the list.
  - falsifier: method: Re-run entropy-demon's seeded probe (append pattern-matching strings to an allowlisted, actively-edited file; run the gate and any accompanying guard); diff the evidence JSON's stamped SHA against its stdout allowlist count at that SHA; read the closure_path text. | threshold: Seeded content in an allowlisted file is detected by the gate or an accompanying integrity check; evidence SHA and stdout are mutually consistent; closure_path names both files and the exemption granularity. Gate exit 0 on the seeded probe with no guard leaves the defect standing. | timeframe: At re-submission; re-verify after any allowlist or scan_text change.
  - owner: agent implements; operator reviews the allowlist-policy decision (scrub vs allowlist is the operator's security call per the gate's RL-8 note)

## R12-operator-alert-channel (P2, UPHELD, status open)

Basin: Machine-readable blocker channel structurally drops operator-owned items

- [ ] AC1: blocking_claims and known_limits derived from the matrix: every BLOCKED claim, every claim whose owner contains 'operator', and every claim whose release_consequence starts with P1 appears in blocking_claims or in a known_limits entry naming it (owner field added to known_limits); an issue absent from ISSUE_DISPOSITIONS is a hard generator failure.
  - falsifier: method: Load the re-submitted promotion-packet.json and matrix; assert the derivation property over all claims; run the generator with a stub tracker containing an unknown gate:operator issue. | threshold: Zero unlisted BLOCKED / operator-owned / P1-consequence claims, and the unknown-issue run exits non-zero. Currently 4 BLOCKED unlisted, 2 holds without limits, 2 P1-consequence claims unlisted — any recurrence leaves the defect standing. | timeframe: At re-submission; one command against the committed artifacts.
  - owner: agent

## R13-no-acceptance-procedure (P2, UPHELD, status open)

Basin: The terminal state names a human act with no defined procedure, acceptor, or record

- [ ] AC1: A written operator-acceptance procedure in a repo- or operator-authored source: who may accept, what the acceptor personally verifies (the four operator holds and the R3 ratify-or-reverse decision among them), the artifact and schema fields (accepted_by, accepted_at, verdict provenance) recording it, and the explicit statement that BUILD-freeze acceptance authorizes nothing beyond recording the state.
  - falsifier: method: Grep the tree for the procedure document; inspect promotion-packet.schema.json for the acceptance/provenance fields; confirm the procedure names an acceptor and a recording artifact. | threshold: At least one procedure document naming acceptor + recorded-acceptance artifact, plus schema fields able to hold it. Observed today: none in tree, none in #191, none in schema. | timeframe: Before operator acceptance is requested of the replacement packet.
  - owner: operator (authors or approves); agent may draft

## R14-taxonomy-substitution-no-register (P2, UPHELD, status open)

Basin: #191's enumerated claim/evidence classes substituted by an implementer taxonomy with no crosswalk; no requirement register

- [ ] AC1: A committed requirement register / crosswalk keyed to #191's clause ids and RELEASING.md gate items, mapping each of the 8 claim classes and 16 evidence classes to covering claims or explicit NOT-APPLICABLE dispositions with reasons; a compatibility class claim added; validator fails on any registered requirement with neither claim nor disposition; CLM-REQUIRED-JOB's subject widened to all six workflows or its statement narrowed.
  - falsifier: method: For each enumerated class/gate item, search the register and matrix for the mapped claim or disposition; run the validator against a register entry with the mapping deleted. | threshold: Every named class maps to at least one claim or recorded N/A; validator exits non-zero on the deleted mapping. Any unmapped class (compatibility today) leaves the defect standing. | timeframe: Before the next candidate freeze is submitted.
  - owner: agent

## R15-custody-residual-undisclosed (P2, UPHELD-WITH-QUALIFICATIONS, status open)

Basin: es#137 fixes sound (H6 killed) but a residual lexical-vs-realpath false-allow class is undisclosed and its deleted rationale unrestored

- [ ] AC1: A known_limit plus a LIMITED matrix row recording that guard path matching is lexical and can diverge from filesystem resolution through symlinked parents, with the concrete probe as evidence; the deleted safe-direction reasoning reinstated as a comment at _collapse_parent_segments. No matching-behavior change in this freeze.
  - falsifier: method: Grep the re-submitted packet for the limit/row; run chesterton-gate's symlink-and-parent-segment battery in the candidate worktree comparing evaluate()['matched'] against realpath containment. | threshold: The limit and row exist and cite the probe; the battery still demonstrating >= 1 divergence case with no disclosure leaves the defect standing (zero divergence cases would instead falsify the finding itself). | timeframe: At re-submission; probe runs in under a second.
  - owner: agent

## D3 (operator): implement all four v5 design commitments

- [ ] Recon the v5 design spec; enumerate ROUTING.md / intrinsic ledgers /
      sentinel corpora / structural membership as concrete work items
- [ ] Implement each; every public claim matches shipped reality
