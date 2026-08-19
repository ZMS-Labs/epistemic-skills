# Lens report — chesterton-gate (metatextual; deletion/legacy/incident-history)

Run: es-v6-rc2-gauntlet-kimi-2026-08-18. Subject: candidate C =
`6db8c50420b194aebbd09a2ea5f81c6a276897dc` (code tree), freeze packet C+1 =
`9aecd467236dfb927e9c13784d77a16d62f28f67` (`docs/v6/ES6-V6-CANDIDATE/`).
Citations name the tree they resolve against (C or C+1); `evidence/` refers to
this run's pinned evidence directory.

## Verdict recommendation: NO-GO against C as frozen (re-freeze class)

One release-blocking defect (CG-1 = FC-1, independently reproduced by this
seat) makes the packet's own operator-acceptance procedure uncompletable on
the sealed bytes, and its repair class (generator edit + packet regeneration)
produces a new SHA, so it cannot be condition-discharged on C. Everything
else my lens checked either discharges cleanly against the predecessor
ruling-set's own falsifiers or degrades to disclosed P3/P4 prose and platform
residuals. This is a NO-GO against an otherwise substantially healthy repair:
14 of 15 acceptance criteria are discharged or substance-discharged, and the
blocking defect is narrow, well-characterized, and loud.

## Reframing: what the real question is

The posed question is "does C discharge the 15 acceptance criteria." The real
question my lens keeps arriving at is narrower and stranger: **the predecessor
taught this program that its artifacts lie about themselves; rc2 answered by
building detectors — but did anyone check whether the detectors can testify
about the artifact that contains them?** The answer is: the machine layer
mostly yes (fail-closed digests, derived blocking claims, restamp refusal —
all verified below), and the prose layer no (three confirmed narration drifts,
CG-2). The freeze digests 158 files and binds nothing in its own narration;
every confirmed residual defect lives in the unsealed prose. The candidate's
remaining risk is not deceit and not engineering incompetence — it is
unverified self-description, the same genus as the predecessor's R5, at one
layer of remove.

## Findings (severity-ranked)

### CG-1 (P1) — The rebuilt immutability fence seals volatile artifacts and fails closed on the unmodified subject (confirms FC-1)

**Evidence.**
- [V] I ran `validate_v6_assurance.py` in the pristine C+1 worktree
  (bytecode-writing disabled; `git status --porcelain` clean before and
  after): exit 1, `AssertionError: R5 DIGEST MISMATCH … (absent)` listing
  `__pycache__/*.pyc` entries — reproduces `evidence/validator-c1-digest-failure.md`
  exactly, on a second host.
- [V C+1 `docs/v6/ES6-V6-CANDIDATE/source-inventory.json`] 158 `file_digests`
  entries; 17 are `__pycache__/*.pyc` (cpython-311 and -312).
- [V C `.github/scripts/v6_generate_candidate_packet.py:851-886`]
  `build_source_inventory` walks the FILESYSTEM
  (`(REPO_ROOT / "plugins/epistemic-skills/contracts").rglob("*")`,
  `p.is_file()`), which includes `.gitignore`d files; [V C
  `.github/scripts/v6_generate_candidate_packet.py:1202-1206`] `dirty_tree()`
  uses `git status --porcelain`, which respects `.gitignore`. The two tree
  models disagree on exactly the volatile-artifact class.
- [V] In-memory probe (this seat, reads only): with the 17 `.pyc` entries
  stripped from the loaded inventory, `validate_source_inventory` verifies
  the remaining **141/141 digests byte-exact from disk** at C+1. The
  substrate seal over real sources is intact; the defect is the inventory's
  tree model.
- [V C+1 `docs/v6/OPERATOR-ACCEPTANCE-PROCEDURE.md` item 4 (line 56-59)]
  requires "the assurance validator passes on the exact packet bytes at the
  candidate SHA" as a precondition the operator personally verifies. As
  sealed, no one — including the operator — can complete item 4.
- [I <- above + C+1 README "Regenerate" section] the packet's own
  regeneration recipe ends with the validator step; that step is red on any
  clean checkout, so the documented recipe cannot complete as written.

**Lens framing.** R5 ordered an immutability detector; the repair built one
on a tree model that seals noise. A fence that screams on the unmodified
subject is not a fence — it is the availability half of the alarm-fatigue
class R5 was created to kill: it trains every future verifier (including the
operator at acceptance) to wave past a red gate. The failure is loud, not
silent, so no false-green flows from it; the harm is that the acceptance
procedure's personal-verification step is impossible, and any acceptance that
proceeded anyway would require overriding a red check — the exact habit the
R5 architecture exists to prevent.

**Falsifier.** Method: fresh clone/worktree of the re-frozen freeze commit on
any OS; run `validate_v6_assurance.py`; then plant a one-byte edit in an
inventoried source and re-run. Threshold: exit 0 on the pristine checkout AND
non-zero on the planted edit. Timeframe: before any re-submitted packet is
put before the operator; re-run on every regeneration. Today the first limb
fails on two independent seats' hosts.

**Validation kernel (must survive repair).** The fail-closed direction is
correct and verified: tamper self-test 18/18 PASS at C (this seat ran
`test_v6_assurance_validator.py`, including planted bare-enum-GO and
post-freeze-mutation cases); `candidate_tree_hash` binds C's git tree and is
portable; the digest recomputation over the 141 real sources is byte-exact
(this seat's probe). Fix the tree model (track the git index, or exclude
volatile artifacts), never the fail-closed polarity.

**Suggested fix.** In `build_source_inventory`, enumerate inventoried files
from `git ls-files` (or filter the filesystem walk against it) so the
inventory's tree model equals the porcelain dirt-check's tree model;
regenerate the packet at the new C; re-freeze. This is a new-SHA repair: not
dischargeable as a condition on `6db8c50…`.

### CG-2 (P2) — The packet's prose layer is unsealed and has drifted from the tree it describes (confirms and extends FC-4)

**Evidence** (each instance confirmed by this seat's own execution, not the
dispatcher dossier's say-so):
- [V] The seat handoff instructs "the validator's digest recomputation proves
  it; run it yourself, trust nothing stamped" — the instruction to verify by
  running points at a verifier that exits 1 on the frozen object (CG-1).
- [V C+1 packet known_limits, KL-DRAFT-CI] states the clean-room "replicates
  52 of the 53 workflow python steps of ONE workflow." [V C
  `.github/workflows/epistemic-flexibility.yml`] the harness's own
  broad-count regex (`grep -cE '^[[:space:]]*(run: )?python3? [^ ]*\.py'`,
  C `.github/scripts/cleanroom_ci.sh`) counts **54** python-invoking lines at
  C, and this run's measured result is 51 pass / 2 fail / 1 ci-context-skip
  (`evidence/oracle-crib-2026-08-18.md`). The packet's central disclosed-gap
  limit is stale against the tree it is frozen with.
- [V] The handoff's "Expected loud skips … skip loudly on NT without symlink
  privilege" mischaracterizes privileged NT: this seat re-ran
  `test_custody_gate.py` at C and got the same two characterization-pin
  FAILs (`guard-lexical-realpath-lands-in-guarded-tree`,
  `guard-lexical-collapse-stays-textual`), exit 1 — FAIL, not SKIP, on a
  second privileged-NT host (confirms FC-2; the runner fails closed
  correctly — an earlier pipe-through-`tail` misread of mine showed rc=0;
  direct re-run gives rc=1).
- [V C+1 README "Honest gaps"] "the freeze pins are an operator one-liner"
  is stale against the live state: both pin tags exist on origin and peel to
  C and C+1 (verified live by this run's Step-0; I re-confirmed the
  requalification run set independently, below).

**Lens framing.** The machine layer is digest-bound; the narration is not.
Nothing in the freeze recomputes a sentence. Every confirmed residual defect
in this candidate lives in prose that was accurate at some earlier commit and
was not re-verified after the tree settled. This is R18's framing defect in
miniature, self-inflicted: the packet steers its verifiers toward checks whose
described behavior no longer matches reality, benignly but structurally.

**Falsifier.** Method: at the re-frozen SHA, execute the packet/handoff
verification instructions verbatim on a clean checkout and diff every
quantitative claim in KL-DRAFT-CI and the README against the harness's own
outputs. Threshold: zero instructions red on arrival; KL-DRAFT-CI's counts
equal the harness's broad count at that SHA. Timeframe: at re-freeze; the
marginal cost is one scripted pass.

**Validation kernel.** The honesty architecture is intact and must not be
"cured" by deletion: readiness NOT_READY, empty requested-acts,
blocking_claims naming this very gauntlet, UNPROVED self-labels [V C+1
`promotion-packet.json`]. The defect is drift, not steering.

**Suggested fix.** Add a prose-consistency step to the freeze recipe (extract
counts from the tools at freeze time rather than hand-typing them into
known_limits); re-date or strike stale environment notes.

### CG-3 (P3) — Fence-as-prohibition inversion in the PINS deferral rationale (resolves FC-5: substance discharged, letter unmet)

**Evidence.** [V C+1 README "Honest gaps"]: "PINS registration follows at
promotion (a post-freeze PINS edit would trip the digest guard by design)."
[V C+1 `source-inventory.json`] `check_pin_tags.py` IS an inventoried
`ci_scripts` file, so the rationale is structurally real: editing PINS on
this branch trips the seal. [V, live] both rc2 pin tags exist on origin and
peel to C and C+1. [V C+1 `docs/v6/operator-decision-record-2026-08-18.md:32-37`]
D4 classifies `pin/…` tags as BUILD-permitted; no operator ruling forbids
them or addresses PINS-registry timing.

**Adjudication of FC-5.** R5(a)'s falsifier threshold is disjunctive: tag
peels AND appears in PINS, or (operator ruling forbids + alternative durable
anchor recorded). Neither limb holds literally: no PINS entry, no forbidding
ruling. But the basin the criterion was written against — "the coordinate is
perishable, reachable only through a draft-PR branch" — is cured: two origin
tags peel to the exact SHAs, and the tree hash is recorded. The criterion's
own timeframe ("the tag/PINS check re-run again before any PROMOTION_RUN")
accommodates promotion-time registration. My call: substance discharged,
letter unmet; not a blocker.

**Lens framing.** The deferral rationale quietly converts a tripwire into a
prohibition. The digest guard exists to make post-freeze edits LOUD, not to
make them forbidden; "it would trip the guard by design" is a reason to
disclose-and-register, not a reason to abstain. And the guard cited as the
reason for inaction is the broken one (CG-1) — it currently fires on the
pristine tree. One fence's malfunction is being used as the load-bearing
justification for deferring another fence.

**Falsifier.** Method: at PROMOTION_RUN preparation, check whether the rc2
pins are registered in PINS or an operator ruling records otherwise.
Threshold: registration present (or ruling recorded) before PROMOTION_RUN.
If promotion proceeds with the pins unregistered and no ruling, the deferral
was avoidance, not sequencing, and this finding upgrades. Timeframe: the
criterion's own — re-checked before any PROMOTION_RUN.

**Validation kernel.** D4's tag authorization, the origin tags themselves,
and the digest guard's fail-closed design are all correct; do not "fix" this
by sealing the packet directory into the inventory or by rushing a registry
edit mid-freeze.

**Suggested fix.** None required for this verdict. At promotion, register the
pins in PINS on main and disclose the trip; optionally amend the README
rationale from "would trip the guard" to "registration is a promotion-time
act, re-checked per the R5 criterion."

### CG-4 (P3) — R5(c)'s omitted elements have a direction: the rebuilt packet asserts the confidence the deleted disclaimer existed to restrain

**Evidence.** [V C+1 `promotion-packet.json` known_limits] KL-RESTAMP
discloses the restamp class generically ("generated at one commit and mutated
at the freeze commit while still carrying the earlier stamp") and the C/C+1
discipline. It does NOT name (i) the post-freeze addition of
`clean-baseline.json`, nor (ii) restore the deleted README disclaimer's
substance (the SHA-is-an-observation / verify-don't-trust invariant) — the
two elements R5(c) specifically required; confirms the dossier's named
PARTIAL by my own read. [V C+1 README]: the same packet asserts "The
validator, running on C+1 or any descendant, recomputes every inventory
digest — a post-freeze edit to an inventoried file turns CI red" — true of
edits, silent on red-without-edits (CG-1).

**Lens framing.** The predecessor's restamp deleted the fence-warning with
the fence; R5(c) ordered the warning re-posted. What rc2 actually did is
tell the story of the wound ("this happened, here is the scar") while leaving
the warning sign in the drawer — and the sign was exactly the humility that
would have prevented CG-1's overclaim from shipping. Narration of an
incident is not remediation of its cause. The omission's direction is toward
overconfidence, which is why it matters more than its size suggests.

**Falsifier.** Method: grep the re-frozen packet's KL-RESTAMP for the two
named elements. Threshold: the limit names the `clean-baseline.json`
post-freeze addition AND carries the disclaimer's substance (the SHA stamp is
an observation to be independently verified, not a proof). Timeframe: at
re-freeze; zero-cost text change riding the CG-1 regeneration.

**Validation kernel.** KL-RESTAMP's generic class disclosure and the C/C+1
discipline statement are real and verified (RESTAMP_REFUSED / DIRTY_TREE_REFUSED
at C `v6_generate_candidate_packet.py:1228-1253`, "No override flag exists on
purpose"); keep them verbatim.

**Suggested fix.** Extend KL-RESTAMP with the two named elements when the
packet regenerates for CG-1.

### CG-5 (P4) — Discharge-table accuracy: R3's "both limbs" and the known_limit that isn't

**Evidence.** R3's acceptance condition requires, beyond the per-merge rows,
"a known_limit disclosing that the candidate's base was produced by
BUILD-window merges." [V C+1 `promotion-packet.json`] the known_limits set is
{KL-SELF-GO, KL-LIVE-ENV, KL-MACOS-162, KL-DRAFT-CI, KL-MAIN-137, KL-MAIN-RED,
KL-WINDOWS, KL-RESTAMP, KL-GUARD-LEXICAL} — none carries that disclosure;
"BUILD-window" appears only in the matrix (CLM-MERGE-190/156/192 statements,
C+1 `claim-to-proof-matrix.json:491,510,529`). The falsifier as written
("at least one packet row/limit names each") IS met — rows name each merge
and cite D1. The condition's extra clause is not. The dossier's discharge
table claims "discharged (both limbs)"; strictly, it is discharged against
the falsifier and short against the condition.

**Lens framing.** Small, but it is the same shape as R6's original defect
(strong statement, weaker backing): a discharge assertion one notch stronger
than its evidence. Naming it cheaply here is how the next panel avoids
re-deriving it.

**Falsifier.** Method: grep the re-frozen packet's known_limits for a base-
provenance entry. Threshold: present, or the criterion is amended to match
its own falsifier. Timeframe: at re-freeze or by operator waiver.

**Validation kernel.** The R3 substance is solid and independently confirmed
by this seat: D1 in the echo-certified ODR, and the ratification string
posted on issue #191 (2026-08-18T20:40:23Z) naming D1–D15 including the three
merges [V, live gh api read]. Provenance caveat, disclosed not litigated: the
GitHub record cannot distinguish operator-typed from agent-typed-under-
authority (one account); the ODR's echo certification is the provenance
claim, and D14's upgrade path was exercised on #191.

**Suggested fix.** One-line known_limit at regeneration, or criterion
amendment.

### Platform confirmations (P3, disclosed, non-gating) — FC-2 and FC-3

- FC-2 confirmed on a second privileged-NT host (this seat's run, above).
  The skip guard keys only on `OSError` from `symlink_to`; privileged NT
  diverges on `realpath`/case-fold semantics. Gating Linux surface green at C
  [V, live: run 32190028540 job `contract` success]. KL-WINDOWS discloses the
  class.
- FC-3 mechanism confirmed by reading [V C
  `.github/scripts/sync_skill_surfaces.py:524`]: `symlink_to(...)` without
  `target_is_directory=True`; the OSError fallback writes the alias text file
  only when the symlink call itself fails, so privileged NT takes the broken
  branch. One-line-fix class, non-gating (`--check` green at C per the crib).
- Falsifier (both): on a privileged-NT host at the re-frozen SHA,
  `test_custody_gate.py` prints SKIP-with-reason or PASS for the two
  characterization pins (never FAIL), and `sync_skill_surfaces.py
  --self-test` exits 0. Timeframe: next freeze; both are cheap.

## Per-criterion notes (R1–R15, against their own falsifiers)

- **R1 — discharged.** [V C `promotion-packet.schema.json:22,131,162-176`]
  @2 adds `independent_gauntlet_ref` and `operator_acceptance`
  (accepted_by/accepted_at/verdict_ref). This seat ran the validator
  self-test at C: 18/18 PASS including planted bare-enum-GO and
  hand-edited-blocking cases. Honest defaults (NOT_READY/refused/NOT_RUN)
  preserved [V C+1 `promotion-packet.json`].
- **R2 — discharged.** CLM-SECRET-SCAN PROVED row present [V C+1 matrix].
  This seat independently re-fetched run 32190035556: `workflow_dispatch`,
  head_sha == C, conclusion success, steps "Prove the scanner detects a
  planted secret" and "Scan the complete repository history" both success.
- **R3 — discharged against the falsifier; short against the condition's
  known_limit clause (CG-5).** Ratification string on #191; rows cite D1.
- **R4 — discharged.** C/C+1 layering confirmed by this run's Step-0 and
  spot-confirmed by me: every artifact stamps C [V C+1
  `promotion-packet.json` candidate_sha; `source-inventory.json`
  exact_start_sha]; pin tags peel; requal runs at C.
- **R5 — PARTIAL, carries the blocking residual.** (a) substance-discharged /
  letter-unmet (CG-3); (b) mechanism present and fail-closed on tamper but
  red on the pristine packet — **CG-1, the P1**; (c) two required elements
  omitted (CG-4); (d) discharged — RESTAMP_REFUSED/DIRTY_TREE_REFUSED, no
  override flag [V C `v6_generate_candidate_packet.py:1228-1253`].
- **R6 — discharged (path a).** CLM-DISPOSITION-CENSUS is honestly scoped as
  a census [V C+1 matrix]; `require_dispositions` fails closed on
  undispositioned items [V C `v6_generate_candidate_packet.py:792-802`].
- **R7 — discharged (path a).** No `paths:` on the whole-tree readers;
  in-tree comments cite the ruling and name the whole-tree-reader rationale
  [V C `epistemic-flexibility.yml:10-20`]; scoped readers (custody, bundles)
  keep filters with rationale. The oracle audit's self-test (planted
  whole-tree reader behind a filter fails closed) passes at C per the crib.
  Lens note on the deletion itself: the `paths:` fence's origin (CI cost) is
  documented in-place at deletion time — exemplary fence discipline; approved.
- **R8 — discharged.** `ready_for_review` on all five gating workflows [V C
  `.github/workflows/*.yml`]; drill transcript in-tree at both C and C+1 [V
  C `docs/v6/evidence/r8-ready-mark-drill-2026-08-18.md`]; this seat
  re-fetched drill run 32184104218 (pull_request, head 564a1e53, conclusion
  failure ≠ skipped — the takeover mechanism fired at an unchanged head).
- **R9 — discharged in substance; prose residual in CG-2.** Completeness
  assertion and accounting invariant present [V C `cleanroom_ci.sh:181-186`:
  numerator/denominator print, FATAL on non-summing accounting]; KL-DRAFT-CI
  names all five skipped jobs — but its "52 of the 53" is stale against the
  tree (54 at C).
- **R10 — discharged by live state.** This seat re-fetched: PR #195 merged
  2026-08-18T22:03:42Z by the operator's account (D11-authorized), merge
  commit 03b7724; main's push runs at 03b7724 green on both
  epistemic-flexibility and release-security. KL-MAIN-RED's retirement clause
  fired; acceptance-procedure item 5 re-checks live at acceptance. Lens note:
  main's green was obtained by allowlist extension — the silence-pattern R11
  criticized — but this time the scrub-vs-allowlist call was made by the
  operator (D7/D11), which is exactly the actor R11 reserved it to. No
  defect; the origin is recorded.
- **R11 — discharged; (d) defensible by design.** Gate green at C (this seat
  ran it: "7 patterns, 37 allowlisted exact files digest-verified (1
  dormant)"). Owner + cadence recorded [V C `check_public_content.py:67-69`
  region]; four inert entries retired with rationale; the one dormant entry
  is D7's review-trail file, absent from this branch, digest binding on
  landing — documented dormant semantics, not ossified cruft.
- **R12 — discharged.** `blocking_claims == ['CLM-INDEPENDENT-GAUNTLET']` [V
  C+1 `promotion-packet.json`], derived via the single `derive_blocking`
  home; unknown-issue hard failure verified at R6's anchor.
- **R13 — discharged as mechanism; uncompletable in fact while CG-1 stands.**
  Procedure exists, names acceptor and verification items [V C+1
  `docs/v6/OPERATOR-ACCEPTANCE-PROCEDURE.md`]; schema fields present. But its
  item 4 requires validator-green on the exact packet bytes, which CG-1 makes
  impossible at C+1 — the procedure and the defect intersect directly.
  Design note (not a defect): the packet directory is deliberately outside
  the digest seal [V C+1 `source-inventory.json` covers contracts/,
  workflows, ci_scripts only], so post-freeze verdict/acceptance recording
  commits do not break the seal — the freeze's identity discipline extends
  one commit upward by design.
- **R14 — discharged.** `requirement-register.json` with crosswalk exists;
  validator fails closed on planted register defects (self-test at C, this
  seat: "planted register-cites-missing-claim fails closed",
  "planted register-requirement-unmapped fails closed").
- **R15 — discharged (disclosure limbs).** KL-GUARD-LEXICAL +
  CLM-MC-GUARD-LEXICAL (LIMITED) present [V C+1]; the deleted safe-direction
  reasoning is reinstated as an "INHERITED REASONING" comment at
  `_collapse_parent_segments` with the incident, the residual direction, and
  a do-not-fix-without-review warning [V C
  `contracts/mission-custody/custody_gate.py:92-104`] — the single best piece
  of fence documentation in this candidate. Windows behavior is FC-2 (P3,
  disclosed).

## Deletions/simplifications in this candidate — lens adjudication

- `paths:` filters removed from whole-tree readers (R7 path A): origin known
  (CI-cost fence), removal ordered by the ruling, rationale committed in
  place. **Approved.**
- Four inert allowlist entries retired (R11d): provably dead (5.0.0-era
  receipts, zero pattern hits), rationale in the file header. **Approved.**
- One dormant allowlist entry kept: not cruft — a pre-committed digest
  binding that activates when D7's file lands via cross-branch merge.
  **Approved (documented).**
- CLM-TRACKER-RECONCILED demoted/renamed to CLM-DISPOSITION-CENSUS (R6 path
  a): an honest weakening of an over-strong statement. **Approved.**
- The predecessor restamp's deleted disclaimer: ordered restored by R5(c);
  narrated but NOT re-erected, and the omission leans toward overconfidence
  (CG-4). **Blocked pending CG-1's regeneration — zero-cost to carry.**

## Rival hypotheses

- **Supported:** "FC-1 is the sole release-blocking defect; the repair is
  otherwise sound." Every non-R5 criterion I re-verified held against its own
  falsifier; the R5(d)/R7/R8/R11/R15 repairs are real, in-tree, and
  origin-documented.
- **Supported with qualification:** "the packet's honesty structure is
  intact" — true of the machine layer; the prose layer drifts (CG-2).
- **Killed:** "the rc2 repairs are cosmetic relabeling." The deletions carry
  origins; the new detectors fail closed on planted defects (self-tests
  re-run by this seat); the drill and requalification runs are live-real
  (independently re-fetched).
- **Killed:** "the seat/dispatcher evidence is circular." Every load-bearing
  claim I sampled traced to my own execution or a live API read.

## The one question the operator most needs to answer

When the CG-1 regeneration produces a new candidate SHA: does this panel's
work transfer as evidence to a successor verdict on the new SHA (a scoped
continuation), or does the operator require a fresh full panel — and
equivalently, is the operator willing to amend acceptance-procedure item 4's
wording so that "validator passes on the exact packet bytes" can never again
be satisfiable-in-principle-but-impossible-in-fact? The R1/R4 SHA-binding
design says a verdict cannot transfer by construction; the cost of honoring
that strictly is a third freeze-plus-panel cycle over a one-line tree-model
fix. That trade-off is the operator's, not the panel's.

## Known unknowns

- I did not re-run the full clean-room harness (the seat ran it twice with
  identical results; I verified its accounting logic and the workflow line
  count instead).
- I did not re-execute the R8 drill (mutating act on a throwaway PR —
  operator-classified); I re-fetched its recorded runs instead.
- The 17th `.pyc` (validator's own) regenerates on import and
  content-mismatches even on the generating host — reported by the seat,
  mechanistically certain (mtime-embedded bytecode), not separately
  re-measured by me.
- Whether the generator's `git ls-files` fix has edge cases (submodules,
  symlinks under contracts/) — none exist in the inventory today [V C+1
  `source-inventory.json`], but the fix should assert it.
- Single-model-family caveat stands (all seats this run share one model
  family); D8 Step-7b cross-family consult is the designated mitigation at
  GO posture and is owed before any eventual acceptance.
