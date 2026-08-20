<!-- gauntlet-dossier@1
frozen_at: 2026-08-18T23:10:00Z
subject_path: docs/v6/ES6-V6-CANDIDATE
subject_revision: 6db8c50420b194aebbd09a2ea5f81c6a276897dc
evidence_root: evidence
evidence_root_sha256: 6f32a18863b2c713b7142af2ff5a9c395a05b419f791e085c6f72de6d23026ca
-->
# Dossier — ES6-V6-CANDIDATE rc2 independent Gauntlet (issue #191, BUILD freeze, successor)

## Seat declaration (independence)

This seat is **Kimi Code CLI (Moonshot model family)**, a fresh seat with no
prior context in this lineage. It did NOT author the candidate (produced by
the Claude-lineage repair seat under operator decision D2), did NOT adjudicate
the predecessor, and is a **different model family from the candidate's
authors** — disclosed per the handoff; this strengthens seat independence but
does NOT discharge D8 Step-7b. All lens seats and the judge in this run share
this seat's model family (single-family caveat carried into the verdict, as in
the predecessor run); the cross-family check is exactly what D8's Step-7b
manual-handoff consult exists to supply at GO posture.

## Subject (frozen)

**Decision under review:** compute **GO / CONDITIONAL / NO-GO against
candidate SHA `6db8c50420b194aebbd09a2ea5f81c6a276897dc` ("C")** — the
ES6-V6-CANDIDATE rc2 BUILD freeze — for issue #191's terminal state
`V6_CANDIDATE_READY_FOR_OPERATOR_ACCEPTANCE`.

NOT in scope: merge, tag, release, wiki packet, support-point declaration
(PROMOTION, operator's separate `PROMOTION_RUN`). Even a GO authorizes
nothing beyond its own record; acceptance belongs to the operator per
`docs/v6/OPERATOR-ACCEPTANCE-PROCEDURE.md`.

**The C/C+1 layering (how the subject is identified — VERIFIED, not
trusted):** C is the last code commit; the freeze commit C+1
(`9aecd467236dfb927e9c13784d77a16d62f28f67`) carries the packet and touches
ONLY `docs/v6/ES6-V6-CANDIDATE/` (verified: `git diff --name-only C C+1`, 13
files, zero outside the packet dir). Branch tip `36b40a6` adds the handoff +
a history-only merge of main; its diff against C touches **zero of the 158**
inventoried files (script-computed). Every packet artifact names C as
`candidate_sha`/`exact_start_sha` (spot-verified in `promotion-packet.json`,
`source-inventory.json`, `evidence/requalification.json`). Origin tag
`pin/es-v6-rc2-candidate-2026-08-18` peels to C; `pin/es-v6-rc2-freeze-…`
peels to C+1. The identity gap that decided the predecessor (R4) is closed
by construction and the closure was live-verified.

**Classification:** fixed-artifact gate (axis=fixed, depth=standard).
**Risk classes:** release-governance (one-way publication door downstream),
security (custody gate, public-content gate, secret scan),
integrity-of-evidence.

**Subject pins (immutable, git-content-addressed):**

- C `6db8c50420b194aebbd09a2ea5f81c6a276897dc`, tree `152b1df0f177303175eca422424361e086e6f0d8`.
- C+1 `9aecd467236dfb927e9c13784d77a16d62f28f67`, tree `3a6c51aa23f9d755f66cc5dce5a64a0012645507` — packet artifacts read here.
- Branch tip `36b40a6`, tree `c84cfc2f2410d7dbe13d0cef5160ff41fdb12bd1`.
- `[V path:line]` citations of repo files resolve against the C+1 tree
  (packet) or C's tree (code), each citation naming which. Run-local
  `evidence/` is pinned by the header `evidence_root_sha256`
  (`finalize_run.py --pin-evidence-root`; sha256 over sorted
  (relpath, file-sha256) pairs — anyone can recompute).

## Predecessor ruling-set (the fix ticket this candidate claims to discharge)

NO-GO against `00e5146e…`, run `es-v6-candidate-freeze-2026-08-18` on branch
`claude/epistemic-skills-v6-completion-nwptmc`: 18 rulings (7 P1, 8 P2, 3
P3/P4), 15 acceptance criteria with falsifiers. The seat read the full
ruling-set from that branch and verifies discharge claims against ITS
falsifiers, not the packet's self-description. Operator decisions D1–D15
(`docs/v6/operator-decision-record-2026-08-18.md`, echo-certified — hash
chain VERIFIED: the file at `d7c4178` sha256-matches the certification
section) ratify the R3 merges (D1) and set this run's rules.

## Step-0 live verifications (all performed by THIS seat on 2026-08-18; full transcripts in evidence/)

1. **Requalification evidence (premise 4): VERIFIED LIVE.** All five run URLs
   in `evidence/requalification.json` resolve to real, completed
   `workflow_dispatch` runs at head_sha == C, with the recorded per-JOB
   conclusions (custody: gating `contract` success, non-gating
   `contract-macos` failure = disclosed es#162 instance). The release-security
   run shows the planted-secret positive control step green (R2 limb).
2. **blocking_claims derivation (premise 5): VERIFIED.** Packet
   `blocking_claims == ['CLM-INDEPENDENT-GAUNTLET']`; the validator's
   `validate_blocking_derivation` passes on the C+1 artifacts (probe — see
   FC-1 evidence for why a probe was needed).
3. **main-branch state (premise 3): VERIFIED LIVE, DECAYED as predicted.**
   PR #195 merged 2026-08-18T22:03:42Z as `03b7724`; main head is GREEN on
   epistemic-flexibility and release-security push runs → KL-MAIN-RED's
   retirement clause has fired. es#137 remains OPEN and its fix commits are
   NOT on main → KL-MAIN-137 substance holds (disclosed, operator-owned,
   merge is PROMOTION).
4. **ODR echo certification (premise 2): VERIFIED.** sha256 of the ODR file
   at `d7c4178` equals the certification section's named hash.
5. **Allowlist dormant/digest semantics (premise 6, first half): VERIFIED at
   C.** `check_public_content.py` green: 7 patterns, 37 exact-file allowlist
   entries digest-verified, 1 dormant entry naming an absent file.
6. **Source-inventory digest semantics (premise 6, second half): FAILS —
   see FC-1.** This is the one Step-0 premise that did not survive contact.
7. **Oracle crib at C:** 15 of 18 command blocks green, including every
   self-test/positive control; three red clusters, all mechanistically
   diagnosed (evidence/oracle-crib-2026-08-18.md): two are Windows-platform
   artifacts on a symlink-privileged NT host (clusters A, B — disclosed
   KL-WINDOWS class, gating Linux surfaces green at C), one is material
   (cluster C = FC-1).
8. **Clean-room at C:** 51/54 steps replicated green; the 2 failures are
   cluster B and a sensitive-path guard refusing the harness's own
   user-profile tempdir (both pass on Linux CI at C; mechanisms in evidence).
9. **R7/R8 tree repairs: VERIFIED at C.** All five gating workflows declare
   `ready_for_review` trigger types; whole-tree-reader workflows dropped
   their `paths:` filters (path A), with in-tree comments citing the rulings.
10. **Pin tags: VERIFIED on origin** (peel to C and C+1); PINS registry
    registration deferred by disclosed design decision (README).

## Finding candidates carried to the panel (hypotheses with falsifiers, NOT rulings)

- **FC-1 (P1 candidate) — the @2 digest seal fails closed on every clean
  checkout.** 17 volatile `__pycache__/*.pyc` digests sealed into
  `source-inventory.json@2`; `validate_v6_assurance.py` at C+1 exits 1
  (`R5 DIGEST MISMATCH … (absent)`) on any pristine checkout and breaks even
  on the generating host after re-import. Blocks acceptance-procedure item 4;
  makes the R8 ready-mark takeover red on arrival; undisclosed (KL-RESTAMP
  claims the opposite posture). Repair requires editing an inventoried
  generator + regenerating the packet → new SHA → re-freeze class.
  Full mechanism, measurements, counterweights, and falsifier:
  `evidence/validator-c1-digest-failure.md`. **Kernel to preserve:** the
  fail-closed digest binding over the 141 real sources is correct and
  verified byte-exact; the defect is the inventory's tree model (filesystem
  walk includes `.gitignore`d files the porcelain dirt-check cannot see).
- **FC-2 (P3 candidate) — R15 characterization pin FAILs instead of SKIPs on
  privileged NT.** Skip guard keys only on `OSError`; NT-with-privilege hits
  divergent `realpath`/case-fold semantics. Gating Linux surface green at C;
  KL-WINDOWS discloses the platform class. Handoff's "skip loudly"
  expectation is inaccurate for this host class.
- **FC-3 (P3 candidate) — `sync_skill_surfaces.py --self-test` crashes on
  privileged NT** (`symlink_to` without `target_is_directory=True`,
  `.github/scripts/sync_skill_surfaces.py:524`). Deterministic, one-line-fix
  class, non-gating, same platform disclosure.
- **FC-4 (metatextual) — handoff/packet prose-vs-reality gaps:** "the
  validator's digest recomputation proves it" (handoff) and KL-RESTAMP's
  posture claim do not survive running them (FC-1); "expected loud skips"
  mischaracterizes FC-2/FC-3. The packet's own honesty structure is otherwise
  intact (NOT_READY / NOT_RUN / empty requested-acts / blocking_claims naming
  this very gauntlet).
- **FC-5 (open question for the panel) — R5(a) PINS deferral:** pin tags
  exist and peel correctly, but the criterion's falsifier names "appears in
  PINS (or a recorded operator ruling forbids the tag, with an alternative
  durable anchor recorded)". The rc2 pins are NOT in PINS; the deferral is
  disclosed in README with a digest-guard rationale. Does disclosed deferral
  + existing origin tags satisfy the falsifier's alternative-anchor clause?

## R18 method doctrine (applied)

Budgeted out-of-set search was performed BEFORE panel dispatch: the seat ran
oracles the packet did not name as expected-red (validator at C+1 — FC-1 is
an out-of-set find), probed the generator's tree model, and diffed the
branch tip against the inventory. Instruction-shaped subject text
(regeneration recipes in README, handoff "run all" crib) was treated as
DATA: every crib command was run in pristine worktrees, nothing was
regenerated in place, and no packet field was flipped (RL-6 discipline).

## Amendment record (pre-dispatch, disclosed)

A Step-0 dossier challenger (isolated read-only agent) attacked the first
freeze of this dossier and returned 2 MATERIAL + 3 MINOR defects; the seat
mechanically spot-verified each before amending (verdict: "fit after named
amendments"; no defect threatened the evidentiary core). Amendments applied:

- **D-1 (MATERIAL, accepted):** the "ready-mark drill transcript not located"
  unknown was mislabeled. The transcript EXISTS in-tree at
  `docs/v6/evidence/r8-ready-mark-drill-2026-08-18.md` (present at both C and
  C+1; cited by the matrix's R8 claim closure_path). Challenger live-verified
  the drill (throwaway PR #196, CLOSED unmerged, head `564a1e53`; six runs at
  the identical head SHA, `event=pull_request`, conclusions ≠ skipped) and the
  seat re-spot-checked one run (`32184104218`, epistemic-flexibility,
  pull_request event, head 564a1e53 — conclusion `failure`, which still
  satisfies R8's "≠ skipped" threshold: the takeover MECHANISM is what the
  drill proves). Relabeled VERIFIED. Minor packet note carried: the
  transcript's READY table transposes the custody/commission-watch run IDs
  (substance intact per live API).
- **D-2 (MATERIAL, accepted):** the per-criterion R1–R15 discharge accounting
  was asserted but not documented. Added below; R5(c) and R11(d) are named
  PARTIAL.
- **D-3 (MINOR, accepted):** the live-verification transcript showed the
  filtered 4-file tail of `git diff --name-only C 36b40a6` without marking
  the elision (actual output: 17 files = 13 packet + 4); annotated in
  evidence.
- **D-4 (MINOR, accepted):** fraction discrepancy noted — packet KL-DRAFT-CI
  says the clean-room replicates "52 of the 53" workflow python steps; this
  seat's run measured 51 pass of 54 (51+2 fail+1 ci-context-skip). Different
  count bases (the seat's failures are the two Windows-host clusters); flagged
  under FC-4 for the panel.
- **D-5 (MINOR, accepted):** PINS registry footnote — `check_pin_tags.py` at
  C+1 guards two pins (`pin/ecs-contract-2026-07-27`, `v4.0.0`); the
  load-bearing claim (rc2 pins not registered) is unchanged.
- **Challenger nuance adopted:** the ODR ratified object `d7c4178` is not an
  ancestor of C (it lives on the predecessor branch; the file was copied into
  this lineage with the certification section appended — decisions text
  untouched). The hash verification is exact; "hash chain" should not be read
  as implying in-lineage continuity.

## Predecessor-criterion discharge table (Step-0 accounting; panel re-adjudicates)

Discharge claims are verified against each ruling's OWN falsifier. "Discharged"
here means the seat found the criterion's threshold met on the evidence named;
the panel may demote any row.

| ruling | status | one-line evidence |
|---|---|---|
| R1 terminal-gate-forgeable | discharged (mechanism) | @2 schema gains `independent_gauntlet_ref` (run id/verdict path/subject SHA); validator self-test: planted bare-enum-GO / verdict-not-on-disk / wrong-SHA all fail closed (crib) |
| R2 secret-scan | discharged | CLM-SECRET-SCAN row + release-security run 32190035556 at C with planted-secret positive-control step green (live) |
| R3 merges-unreconciled | discharged (both limbs) | D1 ratification in echo-certified ODR (hash verified); matrix rows CLM-MERGE-190/156/192 cite D1 (challenger spot-check) |
| R4 SHA-binding | discharged | C/C+1 layering; every artifact stamps C; pin tag peels to C; requal runs at C (live) |
| R5 immutability | **PARTIAL — see FC-1 + FC-5** | (a) tags exist, PINS deferred (FC-5); (b) digest binding present but fails closed on clean checkout (FC-1); (c) KL-RESTAMP discloses the restamp class generically but omits the two specifically-required elements (clean-baseline.json post-freeze addition; deleted disclaimer substance) — challenger D-2, seat-confirmed by reading KL-RESTAMP; (d) generator restamp refusal: panel scope |
| R6 tracker-reconciliation | discharged (path a) | claim renamed CLM-DISPOSITION-CENSUS; statement matches oracle; generator fails closed on undispositioned items (`v6_generate_candidate_packet.py:792-802`, challenger) |
| R7 wf-path-coverage | discharged (path a) | paths filters removed from whole-tree readers; oracle audit self-test includes "planted whole-tree reader behind paths: filter fails closed" (crib) |
| R8 ready-mark takeover | discharged | ready_for_review types on all five gating workflows; drill transcript in-tree and live-verified (D-1) |
| R9 cleanroom coverage | discharged (substance) | completeness assertion + numerator/denominator + named skips observed in the seat's own clean-room run (51/54 print; exclusion list); KL-DRAFT-CI names all five skipped jobs (challenger + seat read) |
| R10 main-red | discharged (retired by live state) | main green at 03b7724 (live); KL-MAIN-RED carries its own retirement clause |
| R11 public-content gate | discharged; (d) **PARTIAL-minor** | digest-bound exact-file allowlist verified green at C (37 files); closure_path/falsifier reconciled (panel re-check); (d): owner+cadence recorded (`check_public_content.py:67-69`), four inert entries retired, ONE dormant entry remains by design (names a file absent from this branch, digest-bound) |
| R12 operator-alert channel | discharged (mechanism) | derive_blocking single home; validator self-test: planted hand-edited-blocking fails closed; blocking_claims == derived (probe) |
| R13 acceptance procedure | discharged | OPERATOR-ACCEPTANCE-PROCEDURE.md exists (read in full); schema @2 operator_acceptance fields; validator refuses terminal state without it (self-test) |
| R14 taxonomy/register | discharged (mechanism) | requirement register validates; planted register-cites-missing-claim and unmapped-requirement fail closed (crib self-test) |
| R15 custody residual | discharged (disclosure limbs) | KL-GUARD-LEXICAL + CLM-MC-GUARD-LEXICAL (LIMITED) present (challenger); characterization pin exists (its Windows behavior is FC-2) |

## Uncertainty labels / known unknowns

- **Verified:** items 1–10 above plus the drill transcript (D-1).
- **Source-supported:** packet's internal claim statuses (read, not
  independently re-derived per-row — panel scope).
- **Partial (named):** R5(c) disclosure completeness; R11(d) residual dormant
  entry; FC-5 PINS deferral (open question for the panel).
- **Incomplete:** per-row matrix falsifier re-execution beyond the crib
  (panel scope); R5(d) generator restamp-refusal probe (panel scope).
- **Out-of-scope:** macOS requalification (read-only per handoff; es#162
  disclosed), PROMOTION acts.
- Single-model-family caveat (all seats Kimi/Moonshot): recorded; D8 Step-7b
  is the designated mitigation at GO posture.
- The seat's host runs Windows WITH symlink privilege — a host class the
  handoff's environment notes did not anticipate; FC-2/FC-3 characterize it.

## Injection guard note

The handoff, gauntlet-request, README, and packet artifacts are implementer-
or operator-adjacent authored text: treated as DATA. No instruction in them
was executed that mutates the subject, the packet, or any shared state; the
"crib" was executed because the OPERATOR's dispatch order authorized the
handoff, and each command is read-only against the subject trees.
