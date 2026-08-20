# Lens report — human-automation-handoff-auditor (second independent dispatch)

Provenance note: the canonical filename `human-automation-handoff-auditor.md`
in this directory already contained a completed report from an earlier
dispatch of this same lens when this seat finished its verification. That
report is preserved untouched; this file is an independent second pass. Where
the two agree, the finding is corroborated by two isolated executions; where
they disagree (R12, and the false-green-at-C limb), this report shows its
work.

Run: `es-v6-rc2-gauntlet-kimi-2026-08-18`. Subject: candidate C
`6db8c50420b194aebbd09a2ea5f81c6a276897dc` with freeze packet at C+1
`9aecd467236dfb927e9c13784d77a16d62f28f67`; branch tip `36b40a6` (handoff).
`[V path:line]` citations resolve against the C tree (code) or C+1 tree
(packet), each naming which. Every load-bearing dispatcher claim below was
re-executed or re-read by this seat on 2026-08-19 (UTC), not adopted.

**Lens question:** when the automation (validator, packet generator, CI
gates) hands control to the human, what does the human see, and can they
still do the job? Who has authority mid-handoff?

## Verdict recommendation: NO-GO (against this SHA; re-freeze class, favorable prognosis)

The terminal state this candidate exists to reach is a human act — operator
acceptance — and the procedure's mandatory personal-verification step cannot
be honestly walked at either relevant SHA: at C+1 the validator fails closed
on the untouched sealed packet (reproduced by this seat); at C it passes
against the PREDECESSOR's stale, NO-GO'd packet (false green, reproduced by
this seat). The one instrument the operator is told to trust either screams
about a tampering event that never happened or certifies the wrong candidate.
Repair requires editing an inventoried generator and regenerating the packet
— a new SHA — so the defect is not dischargeable as a condition on C, and
CONDITIONAL-at-this-SHA is unavailable on the predecessor's own logic.
Everything else in this lens's basin is discharged, retired, or minor; the
honesty structure (NOT_READY / NOT_RUN / refused self-certification /
blocking_claims naming this very gauntlet) is intact and must survive.

## Findings (priority-placed)

### F1 (P1) — The operator's personal-verification step is unexecutable as written: red at C+1, false-green at C

Confirms FC-1 (independently reproduced) and adds a limb neither the dossier
nor the first dispatch of this lens recorded: the procedure's literal reading
produces a false green against the wrong candidate.

**Evidence:**

- This seat ran the validator in the pristine C+1 worktree (bytecode writes
  disabled, tree left clean): exit 1, `AssertionError: R5 DIGEST MISMATCH:
  inventoried files changed after the packet was generated (restamp class)`
  naming 10 absent `__pycache__/*.pyc` entries. [V C+1
  `plugins/epistemic-skills/contracts/v6-assurance/validate_v6_assurance.py:183`;
  corroborates `evidence/validator-c1-digest-failure.md`]
- Script-computed on the C+1 worktree: `file_digests` = 158 entries, 17 are
  `__pycache__/*.pyc`; 16 inventoried files absent on the pristine checkout,
  ALL of them `.pyc`; zero absent non-`.pyc`. [V C+1
  `docs/v6/ES6-V6-CANDIDATE/source-inventory.json`, recomputed by this seat]
- In-memory probe by this seat (no file writes): with the 17 `.pyc` entries
  stripped from `file_digests` and the three listing fields,
  `validate_source_inventory` returns ZERO notices — the 141 real-source
  digests verify byte-exact. [V C+1, this seat's probe]
- **The false-green limb (new).** Acceptance procedure item 4 requires the
  operator to personally confirm "the assurance validator passes on the exact
  packet bytes at the candidate SHA" [V C+1
  `docs/v6/OPERATOR-ACCEPTANCE-PROCEDURE.md:56-59`]. Read literally, the
  acceptor checks out the candidate SHA — C. This seat ran the validator at
  C: exit 0, in LEGACY @1 mode, against the packet directory C carries —
  which is the PREDECESSOR's packet: schema `v6-promotion-packet@1`,
  `candidate_sha` = the NO-GO'd `00e5146e…`, readiness NOT_READY [V C
  `docs/v6/ES6-V6-CANDIDATE/promotion-packet.json`; validator run this seat:
  five LEGACY notices, rc=0]. The legacy-mode validator does not check the
  @2 bindings at all ("R1/R13 binding starts at @2", "no content digests").
  So the procedure's step 4 has two executions and both fail the human:
  literal reading → meaningless green on the wrong packet; intended reading
  (C+1) → permanent red.
- No portable green validation of the @2 packet exists anywhere: the five
  requalification runs are `workflow_dispatch` at head_sha == C [V live:
  this seat re-fetched run 32190035556, release-security success at C with
  the planted-secret step green], i.e. they exercised the validator only in
  legacy mode; the R8 drill predates the seal (F2).
- The alarm text asserts a post-freeze mutation on an untouched tree. A cold
  operator cannot distinguish "17 volatile bytecode artifacts" from real
  tampering using only what the packet supplies. Alert-to-context gap at the
  exact moment of transfer; alarm-fatigue class (the availability half of the
  failure R5 was created to kill).

**Falsifier:** Method: fresh `git worktree add`/clone of the freeze commit on
any OS; run the validator; then plant a one-byte edit in an inventoried
source file and re-run; separately, read the acceptance procedure and name
unambiguously which SHA step 4 targets. Threshold: exit 0 on the clean
checkout AND non-zero on the planted edit, AND procedure text whose literal
reading cannot validate a stale packet. Today the first limb fails everywhere
(this seat: exit 1) and the SHA target is ambiguous. Timeframe: before
operator acceptance; re-run on every packet regeneration.

**validation_kernel:** The fail-closed digest binding over the 141 real
sources verifies byte-exact on a clean checkout (this seat's strip-probe);
the validator self-test's planted post-freeze mutations fail closed (crib:
18/18 PASS at C); `candidate_tree_hash` binds C's git tree
(`152b1df0f177303175eca422424361e086e6f0d8` — this seat recomputed C's tree
id, match) and is portable. The defect is ONLY the inventory's tree model:
`build_source_inventory` walks the filesystem (`.gitignore`-blind) while
`dirty_tree()` uses `git status --porcelain` (`.gitignore`-respecting)
[V C `.github/scripts/v6_generate_candidate_packet.py` — walk ~:851-887,
dirt check ~:1202]. Any fix MUST preserve fail-closed semantics and the
digest layer.

**Suggested fix:** Intersect the inventory walk with `git ls-files` (or
exclude the volatile/`__pycache__` class) in the generator; regenerate the
packet (new SHA, re-freeze); amend procedure item 4 to name the freeze commit
explicitly; disclose the rc2 false-positive in KL-RESTAMP.

### F2 (P2) — The ready-mark takeover has never been practiced against the sealed packet, and lands red at the freeze head

R8's acceptance criterion is met as written (the drill transcript exists and
live-verifies), but the lens's load-bearing question — has the takeover the
operator will actually rely on ever succeeded? — answers NO.

**Evidence:**

- The drill ran 2026-08-18T20:45–20:46Z on throwaway PR #196 [V C+1
  `docs/v6/evidence/r8-ready-mark-drill-2026-08-18.md:18-44`]. The freeze
  commit C+1 was created 2026-08-18T21:57:38Z and C at 21:52:58Z [V `git
  show -s` of both SHAs, this seat]. **The drill predates the sealed packet
  by over an hour** — the drill head tree cannot have contained the @2
  packet, so no run of the drill ever executed the validator against it.
- This seat live-fetched drill run 32184104218: event `pull_request`, head
  `564a1e53…`, conclusion `failure`, and its `stdlib-checks` job failed at
  exactly the step `v6 workflow oracle audit (ES6-ORACLE-AUDIT)` [V live gh
  api, this seat]. In the workflow, that step precedes the validator step
  [V C `.github/workflows/epistemic-flexibility.yml:252` (oracle audit)
  vs :267-268 (`v6 assurance artifacts` / `validate_v6_assurance.py`)] —
  fail-fast meant the validator step never ran even in the drill.
- At the freeze PR's head (tip tree contains the @2 packet, byte-identical
  inventoried files per the zero-intersection diff this seat recomputed:
  `git diff --name-only C 36b40a6` = 13 packet files + 4, none inventoried),
  marking ready dispatches `stdlib-checks`, whose fresh CI checkout has no
  `__pycache__` — the validator step goes red per F1. [I <- V C+1 validator
  run; V workflow :268; V diff]
- KL-DRAFT-CI's statement "Marking the PR ready dispatches every one of them
  at the unchanged head" [V C+1 `promotion-packet.json` known_limits] is
  true about DISPATCH and silent about LANDING. The disclosure arms the
  human to expect a working takeover; the first live landing is a red
  required job with a misleading tamper message.

**Falsifier:** Method: after the F1 repair, open a throwaway draft PR whose
tree contains the regenerated sealed packet, mark ready with no push, list
runs at the unchanged head. Threshold: every gating workflow dispatches AND
`stdlib-checks` concludes SUCCESS including the `v6 assurance artifacts`
step. Today: untestable-green — the validator step cannot pass on any clean
checkout. Timeframe: one drill, under fifteen minutes, before re-submission.

**validation_kernel:** The trigger repair itself is real and verified by this
seat: all five gating workflows declare `types: [opened, synchronize,
reopened, ready_for_review]` with in-tree comments citing R7/R8 [V C
`.github/workflows/{epistemic-flexibility,release-security,
mission-custody-contract,commission-watch-contract,openai-bundles}.yml`
pull_request blocks]. Drafts still correctly refuse false green. The drill
methodology was correct for what it measured (dispatch). Do not respond by
weakening the drill criterion — respond by re-drilling against the sealed
packet.

**Suggested fix:** Lands with the F1 regeneration; re-run the R8 drill
against a tree carrying the new packet and retain the transcript; add one
KL-DRAFT-CI sentence distinguishing dispatch-proven from landing-proven.

### F3 (P3) — R12 residual: one operator-owned P2 decision still falls through both machine-readable channels

Contradicts the dossier's "R12 discharged" and the first dispatch's "zero
unlisted operator-owned claims" — against the criterion's own letter.

**Evidence:**

- R12's acceptance criterion: "every BLOCKED claim, every claim whose owner
  contains 'operator', and every claim whose release_consequence starts with
  P1 appears in blocking_claims or in a known_limits entry naming it";
  falsifier threshold: "any recurrence leaves the defect standing."
- This seat recomputed `derive_blocking` over the C+1 matrix in-memory:
  result `['CLM-INDEPENDENT-GAUNTLET']` == packet `blocking_claims` [V C+1
  `validate_v6_assurance.py:58-77` executed against C+1
  `claim-to-proof-matrix.json`]. Zero BLOCKED claims remain. The derivation
  mechanism is real and single-homed.
- But: `CLM-DESCRIPTION-BUDGET` — owner `operator`, status `LIMITED`,
  consequence_severity `P2` [V C+1 `claim-to-proof-matrix.json`] — appears in
  NEITHER `blocking_claims` NOR any `known_limits` entry [V C+1
  `promotion-packet.json`; this seat greped the known_limits blob for all
  four operator-owned non-PROVED claim ids: zero hits]. The implemented rule
  carves out `LIMITED` operator claims unless severity is sub-P3
  [V C+1 `validate_v6_assurance.py:68-76`], which silently swallows exactly
  the class R12 was written about: "the items that vanish from the
  machine-readable channel are exactly the ones requiring the operator to
  personally decide." The description-budget estate fork IS a live
  operator-personal decision (README honest-gaps names it in prose —
  misrouting, not concealment, as in the predecessor).
- The other three operator-owned non-PROVED claims (CLM-ISSUE-186, -40,
  CLM-PR-195) are PARTIAL/P3 and likewise unlisted, but each is covered by a
  durable ODR decision (D6/D9/D11) — the human's ledger catches those. The
  description-budget fork has no ODR disposition; the machine channel is the
  only place it would surface at acceptance, and it doesn't.

**Falsifier:** Method: grep the re-submitted `promotion-packet.json`
`blocking_claims` and `known_limits` for `CLM-DESCRIPTION-BUDGET` (or read a
recorded criterion amendment covering LIMITED operator claims). Threshold:
the claim id present in one machine-readable channel, or an explicit recorded
ruling that LIMITED+operator+P2 needs none. Today: absent from both, no
ruling. Timeframe: at the next re-submission; one command.

**validation_kernel:** The derivation-from-matrix architecture (one home, no
drift) is correct and now truthful for BLOCKED/P1 claims; the four
predecessor BLOCKED operator holds ARE dispositioned via the echo-certified
ODR. Fix by extending the rule or the limits list, never by re-hardcoding.

**Suggested fix:** Either drop the `LIMITED` carve-out for operator-class
owners at severity ≤ P2, or add a `KL-DESCRIPTION-BUDGET` known_limit naming
the claim and its owner.

### F4 (P3) — Privileged-NT host class: the handoff's triage rule directs the human to file platform artifacts as real findings

Confirms FC-2 (reproduced by this seat) and FC-3 (crib-supported, not
re-run); frames the handoff-context gap.

**Evidence:**

- This seat ran `test_custody_gate.py` at C on this host (Windows WITH
  symlink privilege): the two R15 characterization-pin tests
  (`guard-lexical-realpath-lands-in-guarded-tree`,
  `guard-lexical-collapse-stays-textual`) FAIL, deterministically. [V this
  seat's run; corroborates `evidence/oracle-crib-2026-08-18.md` cluster A]
- The handoff arms the incoming human with: "re-run the exact file once; a
  repeat failure is real" [V tip
  `docs/v6/ES6-V6-CANDIDATE/KIMI-SEAT-HANDOFF.md:51-54` region] and
  "Expected loud skips … skip loudly on NT WITHOUT symlink privilege" [V tip
  handoff:58]. On this host class the failures repeat deterministically and
  nothing skips — the handoff's own procedure tells the human these are REAL
  findings. The privileged-NT class is unanticipated; the skip note is
  correctly scoped (it claims nothing about privileged NT), so the defect is
  an omission, not a false statement — concurring with the first dispatch's
  kill of FC-4's third limb.
- Containment: the gating Linux surfaces are green at C (custody contract job
  `success` in dispatch run 32190028540 per the live-verification transcript;
  the sync self-test's gating `--check` operation green). KL-WINDOWS
  discloses the platform class. Non-gating, one-line-fix class.

**Falsifier:** Method: on a Windows host with symlink privilege, run the two
R15 pin tests at C. Threshold: skip-with-reason or pass falsifies the
finding; today: deterministic FAIL. Timeframe: minutes; re-check after any
skip-guard edit.

**validation_kernel:** The R15 lexical-matching pins are green where they
gate (Linux CI at C); the fail-closed guards are correct behavior. Do not
weaken the pins to silence platform noise — fix the skip guard (capability
probe rather than `OSError`) and the sync self-test's missing
`target_is_directory=True` [V C `.github/scripts/sync_skill_surfaces.py:524`,
per crib cluster B].

**Suggested fix:** Capability-based skip guard in the R15 tests;
`target_is_directory=True` at sync_skill_surfaces.py:524; one handoff
sentence naming the privileged-NT failure signature as environment noise.

## Per-acceptance-criterion notes (lens scope)

"Discharged" = the criterion's own falsifier threshold is met on evidence
this seat re-ran or read in the frozen trees.

- **R1 — discharged (mechanism).** Schema @2 carries `independent_gauntlet_ref`
  and `operator_acceptance{accepted_by, accepted_at,
  verdict_ref{gauntlet_run_id, verdict_path, subject_sha}}`;
  `self_certification` const `refused` [V C+1
  `plugins/epistemic-skills/contracts/v6-assurance/promotion-packet.schema.json`].
  Crib self-test: 18 planted-defect cases fail closed incl. bare-enum-GO.
  Caveat: the mechanism only speaks after F1's alarm is fixed — ordering
  matters to the human.
- **R2 — discharged.** Run 32190035556 re-fetched live by this seat:
  `workflow_dispatch` at head_sha == C, `full-history-secret-scan` success,
  planted-secret positive-control step success.
- **R3 — discharged (operator limb).** D1 ratifies #190/#156/#192 in the ODR;
  this seat recomputed the echo-certification hash: sha256 of the ODR at
  `d7c4178` == the hash named in the certification section (…`5298827ea9…`).
  Authority mid-handoff is defined and durable.
- **R4 — discharged.** This seat recomputed: C+1 diff vs C = 13 files, all
  under the packet dir; C..tip adds only 4 non-inventoried files; zero
  intersection with the 158 inventoried paths; C's tree id matches
  `candidate_tree_hash`; pin tags peel to C and C+1 (live `git ls-remote`).
- **R5 — NOT discharged.** (b) present but broken on arrival (F1); (c)
  PARTIAL — KL-RESTAMP's statement covers the predecessor restamp and the
  C/C+1 discipline but omits the two specifically-required elements
  (clean-baseline.json's post-freeze addition; the deleted disclaimer's
  substance) and its consequence text is silent on the clean-checkout false
  positive [V C+1 `promotion-packet.json` known_limits, read in full];
  (a) PARTIAL — pins exist on origin and peel correctly [V live ls-remote,
  this seat] but PINS guards only `pin/ecs-contract-2026-07-27` and `v4.0.0`
  [V C+1 `.github/scripts/check_pin_tags.py:23-31`]; the falsifier's
  "appears in PINS or a recorded operator ruling forbids the tag with an
  alternative durable anchor" is met by neither limb cleanly. Note for the
  judge: the criterion's limbs are in self-tension BY DESIGN — PINS lives in
  an inventoried file, so a post-freeze registration trips the digest guard
  [V: check_pin_tags.py is in `file_digests`]; the README deferral
  rationale [V C+1 `README.md:64-66`] is structurally sound. Recommend:
  accept the deferral IF the regeneration registers both pins in PINS in the
  same commit. (d) not re-probed by this lens.
- **R6, R7, R9, R11, R14 — outside this lens's basin; not independently
  re-executed.** Dossier Step-0 readings (disposition census, trigger
  repairs, numerator/denominator clean-room print, allowlist digest
  semantics, register crosswalk) are consistent with what this seat read in
  passing; per-row falsifier re-execution belongs to the owning lenses.
  Carried discrepancy: KL-DRAFT-CI's "52 of the 53" vs the seat-measured
  51-of-54 clean-room fraction (D-4) — different count bases, worth one
  reconciling sentence in the regenerated packet.
- **R8 — criterion met as written; takeover substance NOT proven (F2).** The
  drill satisfies the falsifier's letter (new run per gating workflow at
  identical head, conclusion ≠ skipped — this seat re-fetched run
  32184104218 live), but the drill predates the seal and its stdlib-checks
  leg never reached the validator step. The discharge table's "discharged"
  should carry the F2 qualification.
- **R10 — retired by live state.** This seat re-read main: head `03b7724`,
  push runs `epistemic-flexibility` and `release-security` both SUCCESS. The
  disclosure's own retirement clause has fired.
- **R12 — PARTIAL (demoted).** Derivation recomputes clean (this seat), but
  one operator-owned P2 LIMITED claim surfaces in no machine-readable channel
  (F3) — against the criterion's letter.
- **R13 — discharged.** The procedure exists, names the sole acceptor
  (repository operator; agents must refuse), lists five personal-verification
  items, defines the recording artifact, states the scope limit first [V C+1
  `docs/v6/OPERATOR-ACCEPTANCE-PROCEDURE.md`, read in full]. This is the
  human-in-the-loop done right — which is exactly why F1 (its step 4
  unmeetable) is P1 and not noise.
- **R15 — discharged (disclosure limbs); pin behavior on privileged NT is
  F4.** KL-GUARD-LEXICAL + CLM-MC-GUARD-LEXICAL (LIMITED) present per the
  challenger; pin FAILs reproduced by this seat (platform artifact, not an
  invariant flip).

## Rival hypotheses

- **Most supported:** "the candidate discharges the fix ticket except one
  re-freeze-class seal defect" — F1 is decisive alone; R1/R2/R3/R4/R8(letter)/
  R10/R13 independently verified by this seat.
- **Killed:** "the packet's own verification story is internally sufficient"
  — no portable green validation of the @2 packet exists anywhere (requal ran
  at C in legacy mode; drill predates the seal). Also killed: the dossier's
  and first dispatch's unqualified "R12 discharged" (F3).
- **Confirmed against softening:** "the digest seal is conceptually unsound"
  stays killed — 141/141 real sources verify byte-exact; planted mutations
  fail closed; the defect is the tree model, not the mechanism.

## Minimum fix set (from this lens)

1. Generator: intersect the inventory walk with tracked files (or exclude the
   volatile class); regenerate the packet → new SHA → re-freeze. Preserve
   fail-closed semantics and all 141 real-source digests. (F1)
2. With the regeneration: procedure item 4 names the freeze commit
   explicitly; KL-RESTAMP gains the clean-checkout false-positive disclosure
   and the two missing R5(c) elements; both rc2 pins registered in PINS in
   the same commit (or an operator deferral ruling recorded). (F1, R5)
3. Re-run the R8 drill against a tree carrying the new sealed packet; retain
   the transcript; KL-DRAFT-CI distinguishes dispatch-proven from
   landing-proven. (F2)
4. Route CLM-DESCRIPTION-BUDGET into blocking_claims or a known_limit. (F3)
5. Independent of the freeze: capability-based skip guard for the R15 pins;
   `target_is_directory=True` in the sync self-test; one handoff sentence on
   the privileged-NT signature. (F4)

## Known unknowns / not verified by this lens

- R5(d) generator `--restamp` refusal — not re-probed.
- Full clean-room re-run (51/54 is the dispatcher's number) — not repeated;
  the fraction discrepancy (D-4) is carried, not resolved.
- The drill head's exact tree content — the drill commit object is not in the
  local object store; the predating inference rests on commit timestamps
  (20:46Z drill vs 21:57Z C+1) and is structural, not content-verified.
- Whether GitHub required-check settings would actually block merge on the
  red stdlib-checks — repo settings unreadable from this seat (same
  known-unknown as the predecessor run).
- Per-row matrix falsifier re-execution beyond R2/R12/R5 — panel scope.
- Single-model-family caveat (all seats this run Kimi/Moonshot): carried; D8
  Step-7b cross-family consult is the designated mitigation at GO posture —
  and per this lens's drill discipline, note that Step-7b itself has never
  been exercised; its first execution would be the real one.
