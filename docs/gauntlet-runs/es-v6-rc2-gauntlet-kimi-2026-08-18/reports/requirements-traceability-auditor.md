# Lens report — requirements-traceability-auditor

- **Lens id:** requirements-traceability-auditor (stance: metatextual; object: the requirement→artifact→verification chain, orphans in all three directions)
- **Subject:** candidate C `6db8c50420b194aebbd09a2ea5f81c6a276897dc` (code tree) + freeze packet C+1 `9aecd467236dfb927e9c13784d77a16d62f28f67` (`docs/v6/ES6-V6-CANDIDATE/`)
- **Charge:** does C/C+1 truthfully discharge the predecessor ruling-set's 15 acceptance criteria (R1–R15) against THEIR OWN falsifiers?
- **Verdict recommendation: NO-GO** (one open P1 whose repair is re-freeze class; per the predecessor's own doctrine, a verdict against THIS SHA cannot be CONDITIONAL when the condition requires a new SHA)

All verification performed read-only against the two pristine worktrees (validator runs with bytecode-writing disabled; both worktrees `git status`-clean afterward). Evidence tiers: `[V path:line (tree)]` = directly verified by this lens; `[I <- V…]` = inference naming anchors; `[H]` = unverified.

## Reframing (what the real question is)

The dossier asks "did the repair seat fix the 15 rulings?" The traceability question is sharper: **for each criterion, does a chain requirement → implementing artifact → passing verification exist, and does the discharge table point at the same predicate the criterion's falsifier names?** The answer: 11 of 15 chains are intact end-to-end; four chains (R3, R4, R5, R12) have at least one link that is broken, relocated, or silently re-predicated — and the packet's flagship verification (the R5(b) digest seal) has zero possible green executions as sealed. The candidate's self-description is mostly honest about its gaps; the discharge table the panel was handed is less honest than the packet — it marks R4 and R12 "discharged" against falsifiers that, run as written, fire.

## Findings (priority-placed)

### RTA-1 (P1) — The R5(b) digest-seal verification is dead on arrival; the acceptance procedure's required step 4 cannot be completed on this candidate (FC-1 independently confirmed)

**Evidence:**
- [V docs/v6/ES6-V6-CANDIDATE/source-inventory.json (C+1 tree)] `file_digests` = 158 entries; 17 are `__pycache__/*.pyc`; ZERO of the 17 are in `git ls-files` at C+1 (this lens recomputed: 158 = 141 tracked + 17 untracked volatile).
- [V plugins/epistemic-skills/contracts/v6-assurance/validate_v6_assurance.py:183 (C+1 tree)] — this lens ran the validator in the pristine C+1 worktree: `AssertionError: R5 DIGEST MISMATCH … (absent)`, exit 1, listing the missing `.pyc` entries. Reproduces FC-1 exactly.
- [V .github/scripts/v6_generate_candidate_packet.py:851–858 (C tree)] inventory walks the FILESYSTEM (`rglob("*")`, `.gitignore`-blind); [V .github/scripts/v6_generate_candidate_packet.py:1202 (C tree)] `dirty_tree()` uses `git status --porcelain` (`.gitignore`-sighted). The two tree models disagree over exactly the volatile-artifact class.
- [V docs/v6/OPERATOR-ACCEPTANCE-PROCEDURE.md:58 (C+1 tree)] — acceptance item 4 requires "the assurance validator passes on the exact packet bytes at the candidate SHA" as a step the acceptor personally verifies. As sealed, no clean checkout anywhere can satisfy it.
- [V .github/workflows/epistemic-flexibility.yml:268 (C tree)] — stdlib-checks runs the validator; when the R8 ready-mark takeover fires on the freeze PR, a fresh GitHub checkout (no `__pycache__`) turns the required job red. The packet's own immutability alarm blocks the PR's only path to green required checks.
- [I <- V oracle-crib-2026-08-18.md (run evidence)] the clean-room's validator step executes against C's LEGACY @1 packet; the @2 digest binding has no green witness in ANY executed surface — an orphan verification in reverse: a required verification with zero passing executions.
- Traceability framing: the 17 `.pyc` digest entries are orphan verification entries — they verify content no requirement justifies (`.pyc` bytes embed mtime; a digest over them is a digest over noise), and their presence poisons the 141-entry seal that IS required.

**Falsifier:** Method: fresh `git worktree add`/clone of C+1 on any OS; run `validate_v6_assurance.py`. Threshold for discharge: exit 0 on the clean checkout AND a planted one-byte edit to an inventoried source exits non-zero. Timeframe: before operator acceptance; re-run on every regeneration. Today: first limb fails everywhere (this lens: reproduced, rc=1).

**Validation_kernel (must survive any fix):** the fail-CLOSED digest binding over the 141 real sources is correct and verified byte-exact on a clean checkout (strip-`.pyc` probe: all stages pass — [I <- V validator-c1-digest-failure.md, run evidence]); `candidate_tree_hash` (`152b1df0…`) binds C's git tree portably; the failure is loud, never silently green. The defect is the inventory's tree model, not the seal concept.

**Suggested fix:** generator change — inventory walks `git ls-files` (or excludes `.gitignore`d paths), never the raw filesystem; regenerate packet at the repair commit → new candidate SHA → re-freeze. Repair rides the same re-freeze as RTA-2.

### RTA-2 (P2) — R4's README-literal limb fails its own falsifier; the discharge table overclaims R4

**Evidence:**
- R4's criterion: "README names the subject SHA literally"; falsifier method: "grep README for the literal SHA"; threshold: "README contains the literal" (predecessor ruling-set, R4 acceptance_criteria).
- [V docs/v6/ES6-V6-CANDIDATE/README.md (C+1 tree)] `git grep -c 6db8c50420b194aebbd09a2ea5f81c6a276897dc` over the packet dir: README.md = **0** (nine sibling artifacts carry it, 1–7 occurrences each). README.md:29 instead defines C by indirection: "The exact C is `promotion-packet.json → candidate_sha`".
- [V] All other R4 limbs hold: every packet artifact stamps C (`candidate_sha`/`exact_start_sha`); `evidence_paths` 8/8 exist at C+1 (recomputed); requalification runs at head_sha == C [I <- V live-verification-2026-08-18.md]; pin tag peels to C [V `git ls-remote origin refs/tags/pin/*`].
- The dossier's discharge table marks "R4 discharged" without naming the README limb; the falsifier — the agreed oracle per this lineage's own adjudication doctrine (predecessor R7 ruling: "the claim's own falsifier is the correct oracle") — fires.

**Falsifier:** Method: `grep -c <full candidate SHA> docs/v6/ES6-V6-CANDIDATE/README.md` at the freeze tree. Threshold: count >= 1 discharges this finding. Timeframe: at the next freeze (the README lives in the packet dir, so the fix is a regeneration → new SHA — re-freeze class, same repair vehicle as RTA-1).

**Validation_kernel:** the C/C+1 indirection is documented, machine-checked (validator cross-artifact SHA agreement), and the identity binding itself is intact — this is a criterion-letter miss, not an identity gap. Do not "fix" by weakening the falsifier retroactively; either stamp the literal at generation time (HEAD == C at generation, so the generator CAN embed it) or get an explicit operator ruling amending the criterion.

**Suggested fix:** one-line generator/README change in the same regeneration RTA-1 forces; zero marginal cost.

### RTA-3 (P2) — R12's implemented derivation rule is a different, narrower function than the criterion specifies; the divergence is recorded nowhere

**Evidence:**
- Criterion letter: "every BLOCKED claim, every claim whose owner contains 'operator', and every claim whose release_consequence starts with P1 appears in blocking_claims or in a known_limits entry naming it"; falsifier threshold: "any recurrence leaves the defect standing" (predecessor ruling-set, R12).
- [V plugins/epistemic-skills/contracts/v6-assurance/validate_v6_assurance.py:58–74 (C+1 tree)] implemented `derive_blocking`: BLOCKED → block; severity-P1 → block **only if status != PROVED**; operator-class owner → block **only if status ∉ {PROVED, LIMITED} and severity != P3**. The status/severity qualifiers exist in no criterion text.
- [V own computation at C+1] derived == packet `blocking_claims == ['CLM-INDEPENDENT-GAUNTLET']` — internally consistent. But under the criterion's letter, 15 claims are in neither machine channel, including non-PROVED operator-owned `CLM-ISSUE-40` (PARTIAL, operator, sev P3), `CLM-PR-195` (PARTIAL, operator, sev P3), `CLM-ISSUE-186` (PARTIAL, operator+agent, sev P3), and `CLM-DESCRIPTION-BUDGET` (LIMITED, operator, sev P2).
- The four predecessor BLOCKED operator holds (#104/#84/#40/#186) escaped the machine channel by re-classification (status BLOCKED→PARTIAL, severity P3), not by listing. [V claim-to-proof-matrix.json (C+1 tree), claim rows]
- Mitigation (keeps this P2, not P1): the holds ARE dispositioned by operator decisions D3/D6/D9/D10 [V docs/v6/operator-decision-record-2026-08-18.md:27–64 (C+1 tree)] and named in the acceptance procedure's item-3 hold ledger [V docs/v6/OPERATOR-ACCEPTANCE-PROCEDURE.md:42–50 (C+1 tree)] — the human channel carries what the machine channel drops.

**Falsifier:** Method: load matrix + packet at the freeze tree; apply the criterion's literal rule (BLOCKED ∨ owner-contains-operator ∨ release_consequence-starts-P1 ⇒ in blocking_claims ∨ named in a known_limits entry). Threshold: zero unlisted non-PROVED claims discharges this finding; equivalently, a committed amendment to the criterion text (or a packet-recorded note) documenting the status/severity qualifiers closes the trace gap. Timeframe: at re-submission.

**Validation_kernel:** the single-home derivation (validator-owned `derive_blocking`, generator delegates to it) is the right architecture and verifies consistent today; the PROVED-exclusion is plainly the criterion's intent. Preserve it — the finding is that the requirement text and the certified mechanism diverge with no record, so the next auditor re-derives the discrepancy from scratch.

**Suggested fix:** in the RTA-1 regeneration, add the qualifiers to the criterion-citing comment/doc (or a `known_limits` owner-index entry naming the operator-owned non-PROVED claims), so rule text, mechanism, and record coincide.

### RTA-4 (P3) — Cluster of relocated/partial criterion limbs the discharge table flattens to "discharged"

- **R3, condition conjunct 3 relocated.** Criterion requires "a known_limit disclosing that the candidate's base was produced by BUILD-window merges." [V promotion-packet.json (C+1 tree)] no known_limit names #190/#156/#192 or the base-merge fact (recomputed: `#190`/`#156`/`#192` absent from all nine KL entries). The substance lives in matrix row CLM-MERGE-192's statement ("…this candidate lineage's base…") [V claim-to-proof-matrix.json (C+1 tree)]. The falsifier (rows name each + D1 ratification [V operator-decision-record:21–25]) is met; the condition's artifact-type requirement is not. Falsifier for this note: a KL entry (or operator ruling) naming the base-merge fact appears, or the criterion is amended to accept the matrix-row locus; method: grep the packet's known_limits; threshold: present; timeframe: at next freeze.
- **R5(a) PINS limb (FC-5) confirmed open.** [V `git ls-remote`] both rc2 pin tags exist and peel to C / C+1. [V plugins/…/check_pin_tags.py registry + README.md:64–65 (C+1 tree)] the rc2 pins are NOT in PINS; the deferral is README-disclosed with a digest-guard rationale, but the falsifier's alternative requires "a recorded operator ruling" — D4 [V operator-decision-record:31–35] classifies pin-tag CREATION as BUILD-permitted; no decision addresses PINS registration. Note the structural tension this lens flags: PINS lives in the inventoried code tree, so registration can never be INSIDE the frozen tree it guards — the criterion's "appears in PINS" is only evaluable at a later ref, which the criterion does not specify. The criterion is under-specified, not merely unmet. Falsifier: PINS entry (at any ref, with the ref named) or a recorded operator ruling; method: grep PINS + the ODR; threshold: present; timeframe: before PROMOTION_RUN per the criterion's own re-check clause.
- **R5(c) partial confirmed by direct read.** [V promotion-packet.json (C+1 tree), KL-RESTAMP] discloses the restamp class generically; omits the two specifically-required elements (clean-baseline.json's post-freeze addition; the deleted disclaimer's substance). Falsifier: KL-RESTAMP text contains both elements; method: read the entry; threshold: both present; timeframe: at next freeze.
- **R5(d) stricter-than-spec, divergence undocumented.** Criterion: refusal "absent an explicit --restamp flag." [V v6_generate_candidate_packet.py:1229–1237 (C tree)] the generator refuses `--sha != HEAD` with NO override flag ("No override flag exists on purpose"). Stricter is acceptable; undocumented divergence from the requirement text is the trace defect. Falsifier: criterion text amended or divergence recorded; timeframe: next freeze.
- **Packet self-description drift (FC-4 substance).** [V promotion-packet.json:41 (C+1 tree)] KL-DRAFT-CI states the clean-room "replicates 52 of the 53 workflow python steps"; the seat's measured run printed "51 of 54" [I <- V oracle-crib-2026-08-18.md]. Different count bases (dossier D-4), but the KL's number does not reproduce on the panel's host — a stated measurement that its own harness contradicts. Falsifier: KL states the count base (N of M steps of workflow W on host class H) and the number reproduces; timeframe: next freeze.

**Validation_kernel for RTA-4:** every one of these items has its SUBSTANCE present somewhere in the tree (base-merge disclosure in CLM-MERGE-192, pin tags on origin, restamp class in KL-RESTAMP, refusal mechanism in the generator, numerator/denominator in the harness output) — the defects are locus/record mismatches, not missing substance. Any fix must preserve the disclosed substances.

## Per-criterion notes (R1–R15)

- **R1 — DISCHARGED (verified).** Schema @2 `independent_gauntlet_ref` {gauntlet_run_id, verdict_path, subject_sha} [V promotion-packet.schema.json (C+1)]; validator: any non-NOT_RUN enum requires ref + subject_sha == candidate_sha + on-disk verdict artifact naming the SHA; TERMINAL requires GO + `blocking_claims == []` + recorded operator_acceptance [V validate_v6_assurance.py:229–265 region (C+1)]; self-test planted bare-enum-GO / verdict-not-on-disk / wrong-SHA fail closed [V own run at C: self-test PASS].
- **R2 — DISCHARGED.** CLM-SECRET-SCAN row (oracle = full-history scan green at candidate; falsifier names planted-secret control) with evidence_paths → requalification.json [V matrix row (C+1)]; run 32190035556 at C with positive-control step green [I <- V live-verification-2026-08-18.md].
- **R3 — discharged per falsifier; condition conjunct relocated (RTA-4).**
- **R4 — PARTIAL (RTA-2).** All limbs verified except README-literal.
- **R5 — PARTIAL, contains the run's P1 (RTA-1) plus three lesser limbs (RTA-4).**
- **R6 — DISCHARGED (path a).** CLM-DISPOSITION-CENSUS statement matches its oracle ("a census claim"); generator `require_dispositions` fails closed on undispositioned items [V v6_generate_candidate_packet.py:791–802 (C tree)].
- **R7 — DISCHARGED (path a).** Whole-tree readers carry no `paths:` filters [V grep at C: epistemic-flexibility, release-security, commission-watch filter-free; openai-bundles/mission-custody keep scoped filters]; oracle audit classifies whole-tree readers with planted fail-closed self-test [I <- V oracle-crib]; draft-gating + fail-fast risk now honest in KL-DRAFT-CI [V promotion-packet.json:41 (C+1)].
- **R8 — DISCHARGED.** `ready_for_review` on all five gating workflows [V grep at C]; drill transcript in-tree and live-verified [I <- V dossier-challenge D-1].
- **R9 — DISCHARGED (substance).** Completeness assertion FATAL on extraction divergence + numerator/denominator print + step accounting [V cleanroom_ci.sh:124,131,185 (C tree)]; KL names 5/5 skipped jobs + DCO. Count-base drift noted (RTA-4).
- **R10 — DISCHARGED (retired by live state).** KL-MAIN-RED carries all three required elements plus its retirement clause [V packet (C+1)]; main green at 03b7724 [I <- V live-verification-2026-08-18.md].
- **R11 — DISCHARGED.** Digest-bound exact-file allowlist, fail-closed on byte change [V check_public_content.py:60–72 comment + live green run at C, own execution: "37 allowlisted exact files digest-verified (1 dormant…)"]; owner+cadence recorded; four inert entries retired; closure_path names the exemption granularity (by reference — "ES6-ZI-001 coordinates" — adequate).
- **R12 — mechanism consistent, letter divergent (RTA-3).**
- **R13 — artifact DISCHARGED, chain broken downstream.** Procedure names acceptor, personal-verification list, recording artifact, and the "authorizes nothing" scope limit [V OPERATOR-ACCEPTANCE-PROCEDURE.md (C+1)]; schema fields exist [V]. But its item 4 routes through the dead validator (RTA-1): the requirement→verification chain dead-ends.
- **R14 — DISCHARGED (verified).** Register: 8 claim classes + 16 evidence classes + 9 RELEASING gates, zero unmapped (this lens recomputed) [V requirement-register.json (C+1)]; validator fails closed on unmapped/missing-claim mappings [V own self-test run at C]; CLM-COMPATIBILITY claim present (PROVED).
- **R15 — DISCHARGED.** KL-GUARD-LEXICAL + CLM-MC-GUARD-LEXICAL (LIMITED) [V packet/matrix (C+1)]; safe-direction reasoning reinstated as comment at `_collapse_parent_segments` [V custody_gate.py:85–99 (C tree)]. FC-2's privileged-NT FAIL-not-SKIP behavior does not touch the disclosure limbs.

**Orphan scan (all three directions):** orphan REQUIREMENTS — R4-README limb, R5(a) PINS limb, R5(c) two elements, R12 letter rule (above). Orphan ARTIFACTS — none found: every packet artifact maps to at least one criterion (receipt→R4, reconciliation→R6/R12, inventory→R5, register→R14, requalification→R2/R4). Orphan VERIFICATIONS — the 17 `.pyc` digest entries (verify volatile noise no requirement justifies; mechanism of RTA-1) and the clean-room validator step (exercises only the legacy @1 path; the @2 seal has no green witness anywhere).

## Rival hypotheses

- **Killed:** "the packet's honesty structure is intact enough that CONDITIONAL-on-candidate suffices" — RTA-1's repair requires editing an inventoried generator + regeneration → new SHA; a verdict against THIS SHA cannot carry that condition (predecessor valid kernel B).
- **Killed:** "FC-1 is environment noise" — reproduced by this lens on a pristine worktree with bytecode-writing disabled; root cause read in the generator source; 0 of 17 `.pyc` paths tracked.
- **Supported:** the dossier's FC-1 (strongly), FC-5 (confirmed open), and the named partials R5(c)/R11(d) (R11(d) this lens rates fully discharged — owner+cadence recorded, dormant entry digest-bound by design; the criterion's "retire the three inert entries" was done, four actually).
- **Qualified:** the dossier discharge table's "R4 discharged" and "R12 discharged (mechanism)" — both survive only under a charitable re-predication of the criterion; against the falsifiers as written, R4 fires (RTA-2) and R12's recurrence clause is arguable (RTA-3).

## Known unknowns

- Requalification run conclusions (R2/R4 live limbs) and the ready-mark drill transcripts were NOT re-fetched by this lens (triple-verified by seat + challenger already); anchored [I <- V run evidence]. If the panel wants a fourth fetch, `gh api` read calls settle it in one command.
- Whether the generator's regeneration at a fixed HEAD is byte-stable modulo `generated_at` timestamps (R5 falsifier third limb) — not probed; running the generator mutates, out of bounds for this seat. The criterion's "byte-stable or fails loudly" may itself be unsatisfiable as written (timestamps) — a further criterion-specification gap the panel may want to name.
- R11(b) closure_path "names both files" — the packet names them by reference ("ES6-ZI-001 coordinates"), not by literal path; this lens judged it adequate, a stricter reader could fire it.
- Single-model-family caveat (all seats Kimi/Moonshot) applies to this report; D8 Step-7b is the designated cross-family mitigation at GO posture.

## The one question the operator most needs to answer

The digest seal failed because the generator's inventory and its clean-tree check use two different models of "the tree" — and no executed surface anywhere ever ran the @2 seal green before freeze. **Does the operator want the freeze process amended so that every NEW verification mechanism must produce one green witness on a clean checkout before the packet that depends on it may be sealed** — i.e., treat "no green witness" as a generator-level refusal, the same fail-closed philosophy the rest of the packet already embodies?
