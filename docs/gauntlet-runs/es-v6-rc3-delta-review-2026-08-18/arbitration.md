# Arbitration — ES6-V6-CANDIDATE rc3 delta review (run `es-v6-rc3-delta-review-2026-08-18`)

**Computed verdict: NO-GO against candidate SHA `16b80ac6ada24a663e39b38ab06e8f2614d247f4`** (freeze packet commit C+1 = `7ce03b905309d304e70524f1e9144cd9e3cb1259`) for issue #191's terminal state `V6_CANDIDATE_READY_FOR_OPERATOR_ACCEPTANCE`.

All ten rulings of the rc2 verdict of record CLOSE on this SHA — the repair is real, was executed, and survived adversarial verification seat by seat. The NO-GO rests on one NEW P1 found in the delta's blast radius: the candidate commit itself byte-rewrote the published durable-ledger lines, so the required stdlib-checks job fails closed the moment freeze PR #197 is marked ready — the same red-on-arrival consequence class that anchored rc2's P1, reproduced by a new mechanism on a surface no pre-freeze check exercises.

**Verdict binding (anti-counterfeit, per the red-lines gate):** the verdict of record is THIS artifact — run `es-v6-rc3-delta-review-2026-08-18`, subject SHA `16b80ac6ada24a663e39b38ab06e8f2614d247f4`, ruling-set below. A bare `independent_gauntlet` enum value written into `promotion-packet.json` does not constitute this panel's verdict; the packet's enum is bound to a verdict only via `independent_gauntlet_ref` naming this run id, this artifact path, and this subject SHA. No verdict of this run places the program in the terminal state by itself — terminal state requires recorded operator acceptance per `docs/v6/OPERATOR-ACCEPTANCE-PROCEDURE.md`, exactly — and even a GO would confer no promotion authority (publication is an explicit owner act under `RELEASING.md`; CONDITIONAL is not GO). **No verdict transfer across SHAs:** this verdict speaks only to the C/C+1 pair above; the repair it demands forces new coordinates, and this verdict does not travel to them.

**Lineage cap: EXHAUSTED.** This is panel THREE of the three-panel cap on this subject lineage (freeze panel `es-v6-candidate-freeze-2026-08-18`; rc2 gauntlet `es-v6-rc2-gauntlet-kimi-2026-08-18`; this delta review). With this verdict the cap is spent: no further independent panel may be seated on this lineage without an explicit, recorded operator ruling extending it.

## Seat independence (of record)

This run is an **author-dispatched fresh-seat panel**: the dispatcher AUTHORED the repair under review and assembled the seats. That structure is operator-authorized — the operator's words: *"you can run the delta review with fresh context free workflows"* — and was disclosed to every seat, each instructed to weigh dispatcher framing as potentially self-serving and to re-execute any load-bearing claim it doubted. Compensations of record:

1. The acceptance criteria applied here are the rc2 adjudicator's, and that adjudicator was **cross-family (Kimi/Moonshot)** — the author's repair was graded against another family's rulings, applied at their letter, not against criteria of its own drafting.
2. Every load-bearing repair claim was re-executed from primary sources (fresh `--no-local` clones, live GitHub reads) by isolated verifier seats, and this judge independently re-executed the pivotal ones (register below) rather than adopting any seat's word.
3. The challenger's surviving attacks received full independent evaluation — and the P1 that decides this verdict was surfaced by this panel **against the dispatcher's own delta**, which is the behavior an author-framed panel must demonstrate to be credited at all.

Caveat, binding: dispatcher, verifiers, challenger, and this judge share a **single model family**. **D8's Step-7b cross-family consult is OWED BEFORE OPERATOR ACCEPTANCE at any GO posture and is NOT discharged by this panel** — moot for a NO-GO, carried forward as an open obligation.

**Review mode:** DELTA + blast radius per the recorded operator ruling (ledger id `v6-successor-review-delta-mode-20260818-19`). Rulings on unchanged content stand. This panel reviewed the S1–S10 repairs at the new subject, the full repair delta (rc2 C+1 `9aecd46…` → `7ce03b9…`, 29 files), and live GitHub state (main head, PR #197, requalification runs, pin tags, tracker census).

## Rulings digest — the rc2 verdict's S1–S10 on this SHA

| id | kimi priority | disposition | basis (one line) |
|---|---|---|---|
| S1-pyc-sealed-inventory-unverifiable | P1 | **CLOSED** (qualified) | tracked-only inventory (141 files, 0 volatile); validator exit 0 on pristine C+1 and fails closed on 1-byte tamper naming the file (judge-reproduced); five requal dispatch runs live at C, green at gating-job level |
| S2-operator-channel-recurrence-r12 | P2 | **CLOSED** | criterion path (b): recorded operator ruling (ledger 18) + register law matching the derivation; CLM-DESCRIPTION-BUDGET machine-channeled; fail-closed enforcement, planted controls PASS |
| S3-readme-literal-sha-r4-letter | P3 | **CLOSED** | README literally names C (judge-read); validator S3 check enforces it, mutation-verified |
| S4-restamp-disclosure-partial-r5c | P3 | **CLOSED** | KL-RESTAMP names both required elements; SHA-is-an-observation invariant re-erected and enforced |
| S5-pins-deferral-r5a | P3 | **CLOSED** (qualified) | rc2 pins in PINS, live-verified peeling to rc2 C/C+1; lag discipline recorded; rc3 pins pending operator one-liner; prose contradiction → R3-NF5 |
| S6-prose-layer-drift | P3 | **CLOSED** (class recurs) | all three named limbs repaired and verified; class recurrence in the NEW delta counted as R3-NF2/NF3/NF4/NF5 |
| S7-r15-pin-portability | P3 | **CLOSED** | NT early-skip before any filesystem act; check() raises under pytest (planted-failure proven); POSIX suite green |
| S8-sync-selftest-windows-crash | P3 | **CLOSED** | `target_is_directory=True` at the cited site; repo-wide sweep clean; self-test/--check green |
| S9-drill-predates-seal | P3 | **CLOSED** (consequence recurs elsewhere) | its CL-4-counted consequence (ready-mark red via the validator) discharged; the red-on-arrival class recurs via a NEW mechanism, counted once as R3-NF1 |
| S10-cleanroom-sensitive-path-collision | P4 | **CLOSED** | CLEANROOM_TMPDIR override = the ruling's first sanctioned option; honest comment; POSIX-proven; NT residual → R3-NF8 |

New findings from this panel: **one P1 (open)**, one P3 with a P2 dissent, two further P3, four P4 — adjudicated below.

## Per-ruling dispositions (evidence)

**S1 — CLOSED with one qualification.** The generator enumerates sources exclusively via `git ls-files` (one tree model, `v6_generate_candidate_packet.py:857-885`); `source-inventory@2` seals 141 tracked files (6 workflows + 112 contracts + 23 ci_scripts), zero `__pycache__`/`.pyc`, `candidate_tree_hash` equal to `git rev-parse C^{tree}`; all 141 digests independently recomputed with zero mismatches. The falsifier was executed by three seats AND this judge: `validate_v6_assurance.py` exits 0 on a pristine clone of C+1; a one-byte tamper of an inventoried file fails closed with `R5 DIGEST MISMATCH` naming the file; restore returns green. The validator adds a fail-closed `S1 INVENTORY_UNTRACKED` guard with planted controls in both directions (self-test 21/21 PASS, including the literal rc2 defect class rebuilt in a real git repo). All five requalification dispatch runs were live-fetched at `head_sha` = C: four success; mission-custody run 32216975199 aggregate failure caused solely by the dispatch-only, non-gating `contract-macos` job (`if: github.event_name == 'workflow_dispatch'`, so it cannot gate a PR), gating job success. **Qualification:** the criterion phrase "all five gating workflow_dispatch runs green" holds at gating-JOB level, not run-aggregate level, for that one run. Closed on the verdict of record's own precedent — its re-verification register (item 7) recorded the identical per-job custody split while writing this criterion — with the aggregate red loudly disclosed in `requalification.json` (`non_flip_records`: "so the aggregate red is never silently dropped").

**S2 — CLOSED.** The criterion's threshold offers two disjuncts; the second is met: the recorded operator ruling exists at C (`.ledger/entries.jsonl` line 18, `v6-s2-operator-channel-law-20260818-18` — judge-verified present) and the amended criterion letter (`requirement-register.json → operator_channel_law`) matches the derivation limb-for-limb: LIMITED P1/P2 operator claims get generator-DERIVED `known_limits` entries naming the claim (`operator_limited_limits`); non-PROVED non-LIMITED P1/P2 go to `blocking_claims` via `derive_blocking` (one home, imported by the generator); PROVED are row-only; P3 census rows channel via the reconciliation artifact and acceptance item 3. Enforcement fails closed (`validate_operator_channel` raises `S2 CHANNEL DROP`; `validate_blocking_derivation` pins `blocking_claims` exactly); planted controls PASS, including the literal rc2 defect shape. At C+1 all 7 operator-owned claims are lawfully channeled; `CLM-DESCRIPTION-BUDGET` is named by the derived `KL-OPERATOR-DESCRIPTION-BUDGET` (claim field, owner present); `blocking_claims == ['CLM-INDEPENDENT-GAUNTLET']` matches the independent recomputation. The verifier's honest note is adopted: neither (a) nor (b) alone literally describes the hybrid, but the falsifier's governing threshold is satisfied on its letter — no unlisted operator-owned claim lacks a ruling — and the ruling mandates a machine channel rather than exempting one, which is stronger than (b) contemplated. S2 retires by ruling-plus-code exactly as CL-2's dissent clause anticipated. Content staleness of the exemplar claim is a separate finding (R3-NF4), not a channel drop.

**S3 — CLOSED.** README at C+1 line 30 literally names `C = 16b80ac6ada24a663e39b38ab06e8f2614d247f4` with an honest precedence clause (JSON governs on disagreement) — judge-read. The validator now enforces R4's letter structurally (`S3 README_SHA`, `validate_v6_assurance.py:457-464`): a one-hex-char flip turns it red naming the check, restore returns green (seat-executed). Enforcement exceeds the ruling's ask. The check's substring-anywhere laxity is noted for future criterion tightening; non-blocking.

**S4 — CLOSED.** `KL-RESTAMP` at C+1 names both specifically-required R5(c) elements verbatim — the post-freeze addition of `clean-baseline.json` to the predecessor packet while it claimed immutability, and the deleted disclaimer whose SHA-is-an-observation substance "is hereby re-erected as the governing invariant of this packet" — with the invariant carried into `release_consequence` and enforced by the mechanisms the statement names (dirty-tree/`--sha` refusals; digest recomputation, executed green and red this run).

**S5 — CLOSED with qualifications** (its acceptance-criteria array was empty; CL-3's structural holding governs). Both rc2 pins are registered in PINS (`check_pin_tags.py`) with values live-verified peeling to rc2's C (`6db8c50…`) and C+1 (`9aecd46…`); the one-freeze-lag discipline is recorded in the inventoried file citing S5/CL-3; the check runs green. Qualifications, recorded not waived: (1) CL-3's literal recommendation was register-at-freeze-with-deliberate-restamp; the repair chose a lag discipline instead — a coherent reading of CL-3's substance under its own "unreachable inside one freeze by design" concession, but adopted on the repair's authority, not a recorded operator ruling; (2) rc3's own pins do not yet exist on origin — the anchors are correct operator one-liners in PR #197's body (live-verified naming `16b80ac…`/`7ce03b9…`), and the falsifier's "before operator acceptance" timeframe is not yet violated; (3) the README pins prose contradicting the shipped discipline is R3-NF5.

**S6 — CLOSED on every limb the ruling named; the class recurs and is counted as new findings.** (a) `KL-DRAFT-CI` carries no hand-written fraction — counts live in `evidence/clean-baseline.json` (54/54 completeness, 53/54 replicated, pass=53 fail=0, one named ci-context skip, exit 0 at C); no other step fraction in the packet. (b) The drill READY-table transposition is fixed in the live-API-verified correct direction (32184104186 = mission-custody-contract with contract-macos skipped; 32184104140 = commission-watch-contract; custody equals the contract-macos row as required). (c) The handoff's NT-skip prose matches the S7-fixed code, and the rc2 limb "the validator's digest recomputation proves it" now survives execution (pristine exit 0). The basin's class — prose promising what the bytes don't deliver — recurs in fresh instances inside the delta itself; those are adjudicated once, as R3-NF2/NF3/NF4/NF5, not by reopening this ruling.

**S7 — CLOSED.** Both prescribed fixes are present at C and proven: `check()` raises `AssertionError` when `PYTEST_CURRENT_TEST` is set — dynamically proven against the shipped module and end-to-end under real pytest with a planted failing check (pytest exit 1; the silent-pass hole named in the basin is closed), while script-mode collect-then-exit discipline is preserved; the R15 guard-lexical pin early-skips on `os.name == "nt"` with a printed reason BEFORE any filesystem act, matching the ruling's measured POSIX-scoped basis, with the OSError skip retained. Full suite green in script mode on POSIX (63 ok, all four pin checks exercised). NT limb code-verified (no NT host at any seat); the packet makes no NT overclaim (`KL-WINDOWS` intact).

**S8 — CLOSED.** The exact prescribed one-line fix sits at the cited (moved) call site: `symlink_to("plugins/epistemic-skills/skills", target_is_directory=True)` with a comment citing the ruling and an OSError alias-file fallback. Repo-wide sweep: all 7 `symlink_to` call sites carry the flag — the defect class, not just the instance, is closed. `--self-test` 8/8 PASS and gating `--check` green on POSIX; NT limb code-verified.

**S9 — CLOSED; its letter-pattern's recurrence is counted once, elsewhere.** S9 carried no acceptance criteria; per CL-4 its only counted consequence was S1's (ready-mark turns required stdlib-checks red via the validator). That consequence is discharged at this head: the validator is green on pristine C+1 (judge-executed) and the workflow retains the `ready_for_review` trigger and validator step. R8 itself was already DISCHARGED as written by the verdict of record, and no workflow file changes in this delta. The pattern — the takeover has never RUN live against the sealed head, and would land red if fired — is structurally true again at rc3 via a NEW mechanism (the ledger append-only step). Exactly as CL-4 refused to double-count the rc2 instance, this panel counts the rc3 instance once: as R3-NF1.

**S10 — CLOSED.** `CLEANROOM_TMPDIR` implements the first of the ruling's two sanctioned options (relocate clean-room scratch outside the profile), opt-in, default-preserving, with a comment that honestly frames the guard refusal as "the guard working, not a defect" and cites S10; `bash -n` clean; the exact idiom probed on POSIX (unset/space/invalid). Mechanism fit code-verified against the cwd-derived guard leg it cures. Residuals (misattributed FATAL on an invalid override; the NT `C:/tmp` test dependency meaning the override alone may not green the original NT host) are P4, fail-closed, pre-existing or diagnostic-only: R3-NF8.

## New findings (adjudicated)

| id | severity | status | one line |
|---|---|---|---|
| R3-NF1-ledger-reserialization-red-on-arrival | **P1** | **OPEN** | commit C byte-rewrote published ledger lines; required append-only check fails closed at ready-mark of PR #197; no pre-freeze surface runs the oracle |
| R3-NF2-successor-handoff-locks-spent-rc2-subject | P3 (P2 dissent) | open | sealed successor-seat brief hardcodes the NO-GO'd rc2 coordinates in every operational instruction |
| R3-NF3-packet-stale-prose-cluster | P3 | open | KL-MAIN-RED false at generation time; packet self-labels rc2; rc2 NO-GO undiscoverable from the README |
| R3-NF4-budget-fork-claimed-open-but-resolved-in-tree | P3 | open | packet asserts the description-budget fork open; the same tree's ledger entry 17 + spec amendment record it resolved |
| R3-NF5-readme-pins-prose-contradicts-lag-discipline | P4 (P3 dissent) | open | two contradictory pin-registration doctrines ship in one sealed packet |
| R3-NF6-channel-law-latent-gaps | P4 | open | operator-owned P3 non-census and joint-owned LIMITED classes silently uncovered; owner substring-vs-set seam; zero live instances |
| R3-NF7-validator-hardening-notes | P4 | open | full-deletion PRE-FREEZE green; new main() paths untested by planted controls; `_tracked_set` foreign-repo false alarm |
| R3-NF8-portability-and-completeness-residuals | P4 | open | cleanroom FATAL misattribution; NT `C:/tmp` residual; `evidence_paths` omissions; CLM-PR-197 pre-retitle title |

**R3-NF1 (P1, OPEN — the verdict-deciding finding).** Commit C (`16b80ac`, "Fix ledger-entry schema conformance on the three new decision entries") collaterally re-serialized 13 pre-existing, published `.ledger/entries.jsonl` lines from compact to spaced JSON separators — parse-identical, byte-different — while the committed contract is BYTE-exact prefix survival of the merge base (`check_ledger_append_only.py`: "requiring the base revision's bytes to survive as an exact prefix"; self-test 6/6 PASS). Consequence: the required stdlib-checks job's "Durable ledger append-only against merge base" step (`epistemic-flexibility.yml:236-251`, gated `if: github.event_name == 'pull_request'`, `BASE_SHA` = the PR base) fails closed the moment freeze PR #197 (base = main@`03b7724`, head = C+1, currently draft) is marked ready. The R8 ready-mark takeover — drilled at rc2 precisely because it must work — lands RED on arrival at the sealed head, and merging #197 (promotion) is mechanically blocked at this SHA. The blind spot is structural and is the same oracle-gap pattern that made rc2's S1 a P1: no surface that runs before ready-mark exercises this oracle — the step is skipped on `workflow_dispatch` (all five green requalification runs at C show it `skipped`, live step-level API), and the local clean-room SKIPs it (`ci-context` in `clean-baseline.json`). Compounding: commit C's own message asserts the opposite of the checker's contract ("Lines above the merge-base are editable under the append-only contract").

*Judge reproduction:* `check_ledger_append_only.py --base <main@03b7724 ledger> --current <C+1 ledger>` → exit 1, `LEDGER-REWRITTEN: byte 9 (line 1)`; base head verified live via `ls-remote` (`03b7724d0b1d9fb02c7d92c4dd9e783c2b7ea635`); the byte divergence is visible in the first 80 bytes of each file. Two seats independently pinned the rewrite to commit C (the ledger at `72aa6a6` is byte-identical to main's prefix) and field-level-diffed all entries: parsed-content changes are confined to the three new entries exactly as the commit message describes — a serialization defect, not tampering, zero false-green risk.

*Severity ruling (SPLIT ruled, dissent preserved).* The blast-radius seat graded P1; the challenger graded P2, arguing acceptance-procedure items 1–5 remain letter-satisfiable (item 4's validator passes on the exact packet bytes; item 5's "required jobs green on the candidate SHA" is arguably met by the five dispatch runs at C under the packet's own draft-CI clause). **Ruled P1.** Grounds: (1) the verdict of record's own severity idiom — its S1 P1 expressly counted "ready-marking the freeze PR turns required stdlib-checks red on arrival" among the P1 consequences, and its gate capped every acceptance-supporting path while "the freeze's own gate cannot pass"; (2) the acceptance walk's letter survives here only because every pre-acceptance surface structurally skips the failing oracle — a green that is real but unexercised is precisely the credibility erosion the rc2 P1 named, now on the freeze discipline itself; (3) the drilled R8 mechanism, the one takeover surface the program summons a panel to trust, is red at the sealed head. The challenger's kernel is preserved as the dissent of record: fail-CLOSED polarity, intact content integrity on all 19 entries, and a repair that is a byte-revert outside the digest inventory. The dissent does not change the enum: even at P2, the repair requires new commits and is therefore not dischargeable on this SHA — NO-GO on either grading (CL-1 precedent of the freeze run: "a verdict against THAT SHA cannot be CONDITIONAL when the conditions require a new SHA").

**R3-NF2 (P3, P2 dissent preserved).** The sealed successor-seat brief (`KIMI-SEAT-HANDOFF.md` at C+1) was rewritten FOR the delta-review seat yet hardcodes the spent rc2 coordinates in every operational instruction — subject lock `9aecd46…`/`6db8c50…` (lines 60–61), "Candidate C = `6db8c50…`" (:64), freeze C+1 (:68), cleanroom crib (:91), and the verdict-recording instruction naming subject SHA `6db8c50…` (:136); zero occurrences of `16b80ac` (judge-executed grep). Its crib is red on arrival at the instructed checkout (validator `R5 DIGEST MISMATCH` at `9aecd46`, reproduced). Ruled P3 rather than the blast-radius seat's P2: the governing document by both files' own hierarchy (`gauntlet-request.md` — "this handoff … never overrides it") derives the subject correctly by indirection (`promotion-packet.json → candidate_sha`); the packet's own artifacts loudly contradict the stale SHAs; and with the lineage cap exhausted at this verdict, no further seat exists to misdirect absent a fresh operator dispatch, which would carry fresh coordinates. The P2 dissent is preserved verbatim: the misdirection sits in the delta itself, on the highest-stakes step of the very instrument the freeze exists to summon.

**R3-NF3 (P3).** Stale-prose cluster in the freshly sealed packet, three limbs, all conservative in direction: (a) `KL-MAIN-RED` (packet and README) asserts origin/main RED with PR #195 in flight, and the rollback field timestamps that assertion to generation — false at generation: #195 merged as `03b7724` ~6.7 hours before the 04:48:46Z regeneration, main head green on both push runs (live-verified by two seats and the challenger; main head re-confirmed by this judge), while the same freeze's handoff states the truth; (b) the README title and `gauntlet-request.md` still self-identify as "rc2" against the commit message, PR #197 title, and `check_pin_tags.py`, all naming rc3 — treat "the packet at C+1 = `7ce03b9`" as the only reliable identity; (c) the README's predecessor paragraph names only the rc1 NO-GO — the rc2 NO-GO and S1–S10 are undiscoverable from the packet front page (the gauntlet request does list both). P3 not P2: overstated risk, self-retiring clause on KL-MAIN-RED, JSON-governs staleness clause on the README.

**R3-NF4 (P3).** The candidate tree at C carries the operator's resolution of the description-budget fork (ledger entry 17, hybrid Path 2; v5-design AMENDMENT 2026-08-18; RELEASING.md row), yet the packet generated at the same C asserts the fork "remains an open operator fork" (CLM-DESCRIPTION-BUDGET LIMITED/P2) and derives a hold telling the operator to choose a path their recorded ruling already chose. By the row's own oracle the Path-2 owner amendment exists on disk. The S2 channel machinery is sound, but its only live instance contradicts the freeze's own decision record — the exact class S2 exists to kill — and `test_v6_candidate_packet.py` hard-pins this claim as the S2 exemplar, coupling the self-test to the stale row. Conservative direction (an extra hold, never a hidden one): P3.

**R3-NF5 (P4, P3 dissent noted).** The README "Honest gaps" pins bullet still carries the rc2 deferral doctrine ("PINS registration follows at promotion — a post-freeze PINS edit would trip the digest guard by design"), the tripwire-as-prohibition framing CL-3 explicitly overruled, while the same tree's `check_pin_tags.py` codifies the opposite lag discipline. Two contradictory pin doctrines in one sealed packet. P4: S5's substance is code-delivered, the operator-one-liner half of the bullet is accurate (PR #197 body carries correct rc3 tag commands, live-verified), and the README self-flags staleness.

**R3-NF6 (P4).** Latent channel-law gaps, mutation-verified with ZERO live instances: an operator-owned LIMITED/PARTIAL P3 non-census claim would occupy no machine channel silently (the validator skips all P3; the law's limb 3 covers only census rows — ledger entry 18's `revisit_when` anticipates this class); `derive_blocking`'s owner SET vs the enforcers' `'operator'` SUBSTRING is asymmetric (a joint-owned LIMITED P1/P2 claim would silently drop from every channel; a hypothetical owner string containing "operator" outside the set would make the generator emit a packet its own validator rejects — fail-closed seam); a wholly severity-less matrix degrades both enforcements to notices (effectively unreachable for a committed candidate); the register's `enforced_by` over-attributes the P3 limb's enforcement. Live census at C+1 by two seats: every operator-substring P3 claim is a census row with a reconciliation row; the only joint claim is P3.

**R3-NF7 (P4).** Validator hardening notes, all loud: deleting ALL FIVE packet artifacts from a sealed tree (README/evidence remaining) yields the PRE-FREEZE exit 0 — TORN covers only partial deletion; terminal state stays unreachable (the readiness enum lives in the deleted packet; acceptance items 1/4 need packet bytes), so CI-cosmetic; the new `main()` paths (PRE-FREEZE, TORN, S3 README_SHA) have no planted controls — verified only by hand-probes this run; `_tracked_set` trusts `is-inside-work-tree` without confirming toplevel==root, so a byte-exact non-git copy nested in an unrelated repo false-alarms `S1 INVENTORY_UNTRACKED` with a misleading "volatile host state" message (seat-probed; zero false-green risk; one-line fix identified).

**R3-NF8 (P4).** Residuals: `cleanroom_ci.sh` with an invalid `CLEANROOM_TMPDIR` dies later with a misattributing FATAL (mktemp's own stderr precedes it); `test_live_runner.py` hardcodes `Path("C:/tmp")` on NT, so the S10 override alone may not green the original NT host (loud, pre-existing, non-gating); packet `evidence_paths` omits `evidence/requalification.json` (present only per-claim) and `evidence/tracker-capture.json`; the sealed CLM-PR-197 row carries the freeze PR's capture-time rc2 title (retitled to rc3/`16b80ac` after the 04:48:32Z capture — snapshot honest, compounds R3-NF2 for a packet-only reader).

## Challenger attacks ruled (dissent preserved)

- **ADV-1 (ledger red-on-arrival, challenger P2):** ADOPTED as R3-NF1; severity ruled UP to P1 with the challenger's calibration preserved as the dissent of record (see the split ruling above). The challenger's execution, provenance pinning, and "no pre-freeze surface runs this check" analysis are credited in full.
- **ADV-2 (KL-MAIN-RED false at generation, P3):** ADOPTED into R3-NF3 at P3, including the aggravator that the regeneration postdated public knowledge of the merge and the same freeze's handoff states the truth.
- **ADV-3 (handoff subject lock, P3):** ADOPTED as R3-NF2 at the challenger's P3, with the blast-radius seat's P2 preserved as dissent.
- **ADV-4 (README stale, four limbs, P3):** ADOPTED — limbs (1)–(3) into R3-NF3, limb (4) into R3-NF5. The byte-identity proof (rc2 README == rc3 README except the SHA block) is credited.
- **ADV-5 (budget fork vs ledger 17, P3):** ADOPTED as R3-NF4, including the steelman (a residual publication-time obligation could justify SOME hold, but not this statement text).
- **ADV-6 (channel-law latent gaps, P4):** ADOPTED into R3-NF6, merged with the two verifier seats' convergent findings; the challenger's mutation executions against the real artifacts are the controlling evidence.
- **ADV-7 (evidence_paths omissions, P4):** ADOPTED into R3-NF8.
- **Refuted-attack register:** the challenger's fourteen refuted attacks (S1 letter-dodge, five-green-runs letter, derive_blocking undercount, S2 drop/vacuity, requalification forgery, S3 gaming, PRE-FREEZE counterfeit, tracker forgery, inventory-count sleight, S5 dodge, S6–S10 dodges, ledger content-tampering, test self-sabotage, commit-message stamping) are accepted as corroborating evidence for the closures above; each refutation rests on the challenger's own execution or live fetch, not on dispatcher assertions. Its dispatcher-bias notes are recorded and two are elevated: the P1 hid inside the candidate commit under a routine title whose message misstates the contract it violates; and the delta's green surfaces were emphasized while the one surface that cannot pass was never mentioned — the same silence pattern S9 flagged at rc2. Both weigh in R3-NF1's severity ruling. The challenger's environment caveat (the checkout's local `origin/main` ref is stale; live refs must be fetched) is confirmed by this judge and recorded for any future seat.

## Judge re-verification register (independent spot-checks; no seat's word adopted for a load-bearing fact)

1. Verdict of record read in full from `origin/kimi/es-v6-rc2-gauntlet-2026-08-18` before any other input; S1–S10 criteria, CL-1–CL-5, and the register used as governing text.
2. Subject lock: checkout HEAD = `7ce03b9…` (C+1), parent `16b80ac…` (C), status clean; re-verified untouched after all work.
3. S1 limb 1: fresh `git clone --no-local` at C+1 → `validate_v6_assurance.py` exit 0 ("schema + rule checks passed (ZI-001 + candidate)"; the LEGACY note traced to the predecessor ZI-001 inventory, not the candidate).
4. S1 limb 2: appended-byte tamper of inventoried `.github/scripts/check_dco.py` → `AssertionError: R5 DIGEST MISMATCH … ['.github/scripts/check_dco.py']`; restore → exit 0.
5. R3-NF1: live `ls-remote` main = `03b7724d0b1d9fb02c7d92c4dd9e783c2b7ea635`; `check_ledger_append_only.py` with CI's exact inputs → exit 1 `LEDGER-REWRITTEN: byte 9 (line 1)`; byte divergence inspected; workflow step and its `pull_request`-only gate read at C+1 (`epistemic-flexibility.yml:236-251`).
6. `OPERATOR-ACCEPTANCE-PROCEDURE.md` read in full (items 4 and 5 letters, scope limit, recording artifact) — the basis for the R3-NF1 severity ruling.
7. R3-NF2: grep census of the handoff — stale anchors at lines 16/60/61/64/68/91/136, zero `16b80ac`.
8. S3/R3-NF3: README line 1 ("…, rc2") and lines 29–32 (literal C SHA + JSON-governs clause) read; packet fields read (`candidate_sha` = C, `readiness` = NOT_READY, `blocking_claims` = `['CLM-INDEPENDENT-GAUNTLET']`, KL-MAIN-RED / KL-RESTAMP / KL-OPERATOR-DESCRIPTION-BUDGET statements).
9. S2/R3-NF4: ledger has 19 lines; entries 17/18/19 present with ids `v6-description-budget-hybrid-path2-20260818-17`, `v6-s2-operator-channel-law-20260818-18`, `v6-successor-review-delta-mode-20260818-19`.
10. Hygiene: all mutating work in a scratch clone (deleted); the subject checkout finished clean at C+1; no GitHub writes by this judge (network use: two read-only `ls-remote`/fetch operations).

## Verdict gate trace (mechanical)

Open P1 at subject SHA `16b80ac6ada24a663e39b38ab06e8f2614d247f4`: **R3-NF1** (required stdlib-checks red at ready-mark of the freeze PR; promotion mechanically blocked; oracle unexercised by any pre-freeze surface; repair requires new commits). Any open P1 ⇒ NO-GO. Belt: under the dissent's P2 grading, the sole open P2's condition (byte-prefix restore + re-append) is not dischargeable on this SHA — new commits by construction — so the CONDITIONAL branch is closed and the result is NO-GO on either grading (CL-1 precedent). All ten predecessor rulings CLOSE and do not offset a new open P1. Open P3/P4 findings (R3-NF2..NF8) do not move the enum. `computed_verdict == NO-GO`.

**Prognosis (recorded, not laundered):** narrower than rc2's. The entire kimi ruling set is repaired and verified; the sealed inventory, channel law, and portability fixes are sound and carry planted regression controls. The new defect is a serialization byte-revert plus a prose/coordinates sweep — mechanical, small, and outside the digest seal. But it forces new coordinates, and this lineage's panel cap is now spent.

## Next action

1. **Repair (agent-executable):** restore origin/main's ledger bytes as the exact prefix and re-append entries 17–19 in the base serialization (compact separators, schema-conformant); in the same change, fix the successor-brief coordinates (R3-NF2) or replace its hardcoded SHAs with the request's derivation rule, update the rc2-labeled titles and KL-MAIN-RED/predecessor paragraph (R3-NF3), and re-derive CLM-DESCRIPTION-BUDGET against ledger entry 17 (R3-NF4). This produces new coordinates; the operator should rule explicitly whether that is rc4 (full C/C+1 re-freeze) or a sanctioned repair commit — and record the ruling either way, noting that `.ledger` and the packet dir sit outside the digest inventory so the seal itself is not tripped.
2. **Close the oracle gap that hid R3-NF1:** give the ledger append-only check a pre-freeze surface — a dispatch-safe or locally-runnable invocation against live origin/main — so the freeze discipline exercises it before sealing, not first at ready-mark.
3. **Panel cap:** EXHAUSTED with this verdict (three of three). Any further independent review of this lineage — including the review of the repair above — requires an explicit, recorded operator ruling extending the cap or opening a new lineage.
4. **D8 stands:** Step-7b cross-family consult at GO posture, BEFORE operator acceptance; this single-family panel did not and could not discharge it.
5. Fold the remaining P4s (R3-NF5..NF8) into the next freeze's sweep; none blocks independently.

## Bounded reinstatement

One round per protocol: any party may attack a ruling's validity; a surviving attack recomputes that ruling only. The severity split on R3-NF1 was raised and ruled inside this run (dissent preserved above); it does not alter the enum on either branch. No other reinstatement attack was raised.

## The ruling-set@1 block (writable home of the verdict)

```json
{
 "ruling_set": "ruling-set@1",
 "run": "es-v6-rc3-delta-review-2026-08-18",
 "subject_sha": "16b80ac6ada24a663e39b38ab06e8f2614d247f4",
 "freeze_commit": "7ce03b905309d304e70524f1e9144cd9e3cb1259",
 "review_mode": "delta-plus-blast-radius per operator ruling v6-successor-review-delta-mode-20260818-19; rulings on unchanged content stand",
 "lineage_panel_cap": {
  "cap": 3,
  "used": 3,
  "state": "EXHAUSTED",
  "note": "freeze panel + rc2 gauntlet (kimi) + this delta review; any further panel on this lineage requires an explicit recorded operator ruling"
 },
 "seat": {
  "structure": "author-dispatched fresh-seat delta panel; dispatcher authored the repair under review",
  "authorization": "operator-authorized and disclosed: 'you can run the delta review with fresh context free workflows'",
  "family": "single model family across dispatcher, verifiers, challenger, judge (claude)",
  "criteria_provenance": "acceptance criteria are the rc2 adjudicator's (cross-family, kimi/moonshot), applied at their letter",
  "d8": "Step-7b cross-family consult OWED before operator acceptance at GO posture; NOT discharged by this panel"
 },
 "predecessor_ruling_dispositions": {
  "S1-pyc-sealed-inventory-unverifiable": {
   "disposition": "CLOSED",
   "qualification": "five-green-runs limb holds at gating-job level (custody aggregate red = disclosed non-gating macos diagnostic; verdict-of-record register item 7 precedent)"
  },
  "S2-operator-channel-recurrence-r12": {
   "disposition": "CLOSED",
   "qualification": "hybrid of paths (a)/(b); threshold's second disjunct met on its letter; exemplar content staleness = R3-NF4"
  },
  "S3-readme-literal-sha-r4-letter": {
   "disposition": "CLOSED",
   "qualification": null
  },
  "S4-restamp-disclosure-partial-r5c": {
   "disposition": "CLOSED",
   "qualification": null
  },
  "S5-pins-deferral-r5a": {
   "disposition": "CLOSED",
   "qualification": "lag discipline is repair-authored, not operator-ruled; rc3 pins pending operator one-liner; prose contradiction = R3-NF5"
  },
  "S6-prose-layer-drift": {
   "disposition": "CLOSED",
   "qualification": "named limbs repaired; class recurrence counted as R3-NF2/NF3/NF4/NF5"
  },
  "S7-r15-pin-portability": {
   "disposition": "CLOSED",
   "qualification": "NT limb code-verified only"
  },
  "S8-sync-selftest-windows-crash": {
   "disposition": "CLOSED",
   "qualification": "NT limb code-verified only"
  },
  "S9-drill-predates-seal": {
   "disposition": "CLOSED",
   "qualification": "CL-4-counted consequence discharged; letter-pattern recurrence via new mechanism counted once as R3-NF1"
  },
  "S10-cleanroom-sensitive-path-collision": {
   "disposition": "CLOSED",
   "qualification": "NT residuals = R3-NF8"
  }
 },
 "new_findings": [
  {
   "id": "R3-NF1-ledger-reserialization-red-on-arrival",
   "priority": "P1",
   "status": "open",
   "severity_split": "blast-radius seat P1 vs challenger P2; ruled P1, dissent preserved; NO-GO on either grading (repair not dischargeable on this SHA)"
  },
  {
   "id": "R3-NF2-successor-handoff-locks-spent-rc2-subject",
   "priority": "P3",
   "status": "open",
   "severity_split": "blast-radius seat P2 vs challenger P3; ruled P3, dissent preserved"
  },
  {
   "id": "R3-NF3-packet-stale-prose-cluster",
   "priority": "P3",
   "status": "open"
  },
  {
   "id": "R3-NF4-budget-fork-claimed-open-but-resolved-in-tree",
   "priority": "P3",
   "status": "open"
  },
  {
   "id": "R3-NF5-readme-pins-prose-contradicts-lag-discipline",
   "priority": "P4",
   "status": "open"
  },
  {
   "id": "R3-NF6-channel-law-latent-gaps",
   "priority": "P4",
   "status": "open"
  },
  {
   "id": "R3-NF7-validator-hardening-notes",
   "priority": "P4",
   "status": "open"
  },
  {
   "id": "R3-NF8-portability-and-completeness-residuals",
   "priority": "P4",
   "status": "open"
  }
 ],
 "computed_verdict": "NO-GO",
 "verdict_binding": {
  "run_id": "es-v6-rc3-delta-review-2026-08-18",
  "subject_sha": "16b80ac6ada24a663e39b38ab06e8f2614d247f4",
  "verdict_path": "docs/gauntlet-runs/es-v6-rc3-delta-review-2026-08-18/arbitration.md",
  "statements": [
   "This artifact is the verdict of record; a bare independent_gauntlet enum flip in promotion-packet.json is not this panel's verdict.",
   "No verdict of this run places the program in the terminal state by itself; terminal state requires recorded operator acceptance per docs/v6/OPERATOR-ACCEPTANCE-PROCEDURE.md exactly.",
   "Even a GO would confer no promotion authority; CONDITIONAL is not GO; publication is an explicit owner act under RELEASING.md.",
   "No verdict transfer across SHAs: the R3-NF1 repair forces new coordinates; rulings on unchanged content stand for any operator-authorized successor review.",
   "The three-panel lineage cap is EXHAUSTED with this verdict; further panels require an explicit recorded operator ruling.",
   "D8 Step-7b cross-family consult is owed before operator acceptance at GO posture and was not discharged by this single-family panel.",
   "This run satisfies no externally-enforced safety gate."
  ]
 },
 "rulings": [
  {
   "id": "S1-pyc-sealed-inventory-unverifiable",
   "ruling": "CRITERION-ADJUDICATED",
   "status": "closed"
  },
  {
   "id": "S2-operator-channel-recurrence-r12",
   "ruling": "CRITERION-ADJUDICATED",
   "status": "closed"
  },
  {
   "id": "S3-readme-literal-sha-r4-letter",
   "ruling": "CRITERION-ADJUDICATED",
   "status": "closed"
  },
  {
   "id": "S4-restamp-disclosure-partial-r5c",
   "ruling": "CRITERION-ADJUDICATED",
   "status": "closed"
  },
  {
   "id": "S5-pins-deferral-r5a",
   "ruling": "CRITERION-ADJUDICATED",
   "status": "closed"
  },
  {
   "id": "S6-prose-layer-drift",
   "ruling": "CRITERION-ADJUDICATED",
   "status": "closed"
  },
  {
   "id": "S7-r15-pin-portability",
   "ruling": "CRITERION-ADJUDICATED",
   "status": "closed"
  },
  {
   "id": "S8-sync-selftest-windows-crash",
   "ruling": "CRITERION-ADJUDICATED",
   "status": "closed"
  },
  {
   "id": "S9-drill-predates-seal",
   "ruling": "CRITERION-ADJUDICATED",
   "status": "closed"
  },
  {
   "id": "S10-cleanroom-sensitive-path-collision",
   "ruling": "CRITERION-ADJUDICATED",
   "status": "closed"
  },
  {
   "id": "R3-NF1-ledger-reserialization-red-on-arrival",
   "priority": "P1",
   "status": "open",
   "severity_split": "blast-radius seat P1 vs challenger P2; ruled P1, dissent preserved; NO-GO on either grading (repair not dischargeable on this SHA)",
   "ruling": "UPHELD"
  },
  {
   "id": "R3-NF2-successor-handoff-locks-spent-rc2-subject",
   "priority": "P3",
   "status": "open",
   "severity_split": "blast-radius seat P2 vs challenger P3; ruled P3, dissent preserved",
   "ruling": "UPHELD"
  },
  {
   "id": "R3-NF3-packet-stale-prose-cluster",
   "priority": "P3",
   "status": "open",
   "ruling": "UPHELD"
  },
  {
   "id": "R3-NF4-budget-fork-claimed-open-but-resolved-in-tree",
   "priority": "P3",
   "status": "open",
   "ruling": "UPHELD"
  },
  {
   "id": "R3-NF5-readme-pins-prose-contradicts-lag-discipline",
   "priority": "P4",
   "status": "open",
   "ruling": "UPHELD"
  },
  {
   "id": "R3-NF6-channel-law-latent-gaps",
   "priority": "P4",
   "status": "open",
   "ruling": "UPHELD"
  },
  {
   "id": "R3-NF7-validator-hardening-notes",
   "priority": "P4",
   "status": "open",
   "ruling": "UPHELD"
  },
  {
   "id": "R3-NF8-portability-and-completeness-residuals",
   "priority": "P4",
   "status": "open",
   "ruling": "UPHELD"
  }
 ],
 "dispatcher_format_note": "The judge's machine block carried its content under predecessor_ruling_dispositions/new_findings; the dispatcher added this conforming rulings array 1:1 from that same content (no substantive change) to satisfy validate_ruling_set.py's ruling-set@1 contract. Original keys preserved above."
}
```