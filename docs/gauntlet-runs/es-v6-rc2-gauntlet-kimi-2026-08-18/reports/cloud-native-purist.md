# Lens report — cloud-native-purist (constructive)

Run: es-v6-rc2-gauntlet-kimi-2026-08-18. Subject: candidate C = `6db8c50420b194aebbd09a2ea5f81c6a276897dc`
with freeze packet C+1 = `9aecd467236dfb927e9c13784d77a16d62f28f67` (`docs/v6/ES6-V6-CANDIDATE/`).
Citations: `[V path:line @C]` = verified by this lens against the pristine C worktree (code tree);
`[V path:line @C+1]` = verified against the pristine C+1 worktree (packet); run-local evidence is cited
as `evidence/…` and treated as re-verified only where this lens re-executed it.

## Verdict recommendation: NO-GO (single-defect, narrowest re-freeze class)

One open P1 (CNP-1 = confirmed FC-1) defeats R5's acceptance criterion on its own falsifier and makes
the operator-acceptance procedure's item 4 unsatisfiable by construction. The defect cannot be repaired
on C — the fix edits an inventoried generator and regenerates the packet, producing a new SHA — so
CONDITIONAL-on-C is unattainable. Everything else this lens re-verified discharges. This is the
strongest version of the candidate failing on one tree-model bug, not an architecture error: the
minimal re-freeze recipe below is a one-file generator change plus re-execution of an already-built,
already-drilled pipeline. If the ambition were wrong I would say so; it is right and nearly landed.

**The strongest version of the subject (constructive read):** C/C+1 layering closes the predecessor's
R4 identity gap by construction; the digest seal over the 141 real sources verifies byte-exact; the
validator fails *closed* on every planted defect (18/18 self-test PASS, re-run by this lens
`[V plugins/epistemic-skills/contracts/v6-assurance/test_v6_assurance_validator.py @C — self-test rc=0]`);
ready-mark takeover is real and drilled; the packet's own honesty scaffolding (NOT_READY,
`blocking_claims == ['CLM-INDEPENDENT-GAUNTLET']`, `self_certification: refused` —
`[V docs/v6/ES6-V6-CANDIDATE/promotion-packet.json @C+1]`) is intact. Keep every one of those
mechanisms; cut only the filesystem-walk tree model and the hand-run regeneration toil.

## Findings

### CNP-1 — The @2 digest seal binds volatile host-local disk state; the packet cannot validate anywhere, including where it was made (P1; confirms FC-1)

**Priority:** P1 (blocks acceptance-procedure item 4; turns the required `stdlib-checks` job red on the
freeze PR the moment R8's ready-mark fires).

**Evidence:**
- `source-inventory.json@2` carries 158 `file_digests` entries; 17 are `__pycache__/*.cpython-31{1,2}.pyc`
  `[V docs/v6/ES6-V6-CANDIDATE/source-inventory.json:16-19,67 @C+1; count computed by script: 158 total,
  17 pycache]`.
- This lens re-ran the validator on the pristine C+1 worktree (bytecode generation suppressed, tree
  untouched): `AssertionError: R5 DIGEST MISMATCH … (absent)` naming 10 `.pyc` entries, exit code 1.
  `[V — re-execution at C+1, 2026-08-19]`.
- Root cause, read at C: `build_source_inventory` walks the *filesystem*
  (`(REPO_ROOT / "plugins/epistemic-skills/contracts").rglob("*")`, `p.is_file()`)
  `[V .github/scripts/v6_generate_candidate_packet.py:856-860 @C]`, while `dirty_tree()` asks git
  (`git status --porcelain`) `[V .github/scripts/v6_generate_candidate_packet.py:1202-1206 @C]`.
  The two tree models disagree exactly on the `.gitignore`d, host-generated, content-volatile class:
  `.pyc` files embed source mtime/size and regenerate on every import — a digest over a `.pyc` is a
  digest over noise.
- `OPERATOR-ACCEPTANCE-PROCEDURE.md` item 4 requires that "the assurance validator passes on the exact
  packet bytes at the candidate SHA" as something the acceptor *personally* verifies
  `[V docs/v6/OPERATOR-ACCEPTANCE-PROCEDURE.md:55-59 @C+1]`. As sealed, no checkout of C+1 can satisfy
  it — the packet fails its own acceptance gate on arrival.
- Lens frame: this is the archetypal "state on disks" defect. A declarative, content-addressed manifest
  was allowed to absorb mutable, machine-local build residue. Git already maintains the correct,
  portable inventory of the tree (`candidate_tree_hash` binds it —
  `[V docs/v6/ES6-V6-CANDIDATE/source-inventory.json:4 @C+1]`); the per-file layer re-derived it from
  the wrong substrate (a developer host's disk instead of the index).

**Falsifier:** statement — "the seal is portable: the packet validates on any clean checkout." Method:
fresh `git worktree add`/clone of C+1 on any OS, run `validate_v6_assurance.py`, then plant a one-byte
edit in an inventoried real source and re-run. Threshold for discharge: exit 0 on the clean checkout
AND non-zero on the planted edit. Today the first limb fails everywhere (measured by this lens).
Timeframe: before any replacement packet is submitted; re-run on every regeneration.

**Validation kernel (must survive the fix):** the fail-closed direction is correct and proven (absent/
mutated → red; planted post-freeze-mutation self-test case PASSes); the 141 non-`.pyc` digests verify
byte-exact on a clean checkout; the failure is loud and self-revealing — no false-green risk flows from
it. Do not "fix" this by making the digest check advisory, by allowlisting `.pyc` misses in the
validator, or by dropping the per-file layer.

**Suggested fix (minimal):** source the inventory from git, not the disk —
`git ls-files` over the three roots (or filter the walk through the index) in
`build_source_inventory` — so the inventoried set is exactly the tracked set the porcelain dirt-check
already sees. One tree model, git's. Then regenerate at the new C, re-run the five dispatched requal
workflows at the new SHA, re-freeze. (Structural improvement folded into CNP-2.)

### CNP-2 — Packet regeneration is a hand-run, host-bound recipe; the managed equivalent is already built and half-used (P2)

**Priority:** P2 (toil + drift generator; the producing cause of CNP-1 and of the packet's
prose-vs-reality gaps).

**Evidence:**
- The README's "Regenerate (C/C+1 discipline)" section is a six-step manual recipe run on a developer
  host, including a hand-executed "dispatch the five gating workflows at C; record run URLs + job
  conclusions in evidence/requalification.json"
  `[V docs/v6/ES6-V6-CANDIDATE/README.md:68-86 @C+1]`.
- The managed/declarative substrate already exists and is already trusted for the gating verdict: all
  five gating workflows accept `workflow_dispatch`, and the requalification evidence consists of
  dispatch runs at C `[V — this lens fetched run 32190035556: event=workflow_dispatch,
  head_sha=6db8c50…, conclusion=success, planted-secret step green]`. GitHub-hosted runners are
  ephemeral cattle: a fresh runner has no `__pycache__`, no symlink-privilege quirks, no user-profile
  tempdir — the entire KL-WINDOWS/FC-2/FC-3 host class and the CNP-1 contamination class both
  structurally absent.
- Manual capture has already produced drift: the R8 drill transcript transposes two run IDs (challenger
  D-1, `evidence/dossier-challenge-2026-08-18.md`), and KL-DRAFT-CI's hand-maintained "52 of the 53"
  clean-room fraction does not match the seat's measured 51-of-54 (challenger D-4) — copies rot;
  hand-transcribed run metadata rots fastest.

**Falsifier:** statement — "host-local manual regeneration has lower total cost than a dispatch-driven
regeneration workflow." Method: compare (a) counted manual steps + measured defect classes traceable to
host state (this run: CNP-1 re-freeze, two transcript/count discrepancies) against (b) the one-time
cost of a `workflow_dispatch` regeneration workflow writing the packet to a branch. Threshold: the
finding is falsified if the manual path shows fewer defects/toil across the next two freezes.
Timeframe: evaluate at the next freeze cycle.

**Validation kernel:** the C/C+1 commit discipline, the dirty-tree/restamp refusals
(`RESTAMP_REFUSED`, `DIRTY_TREE_REFUSED`, no override flag —
`[V .github/scripts/v6_generate_candidate_packet.py:1231-1252 @C]`), and human recording of the freeze
commit all survive; only the *execution environment* and the *hand transcription* move into CI. The
packet remains reviewed and committed by a human — GitOps for the mechanics, not for the decision.

**Suggested fix:** after the minimal CNP-1 repair unblocks this freeze, add a dispatch workflow that
runs the README recipe on a clean runner and opens the packet as a PR; generator keeps refusing dirty
trees and `--sha != HEAD`. Do not block this candidate on it — block the *next* freeze on it.

### CNP-3 — The durable-anchor registry (PINS) lags the anchors it exists to guard; deferral is disclosed but the rationale is now self-defeating (P3; adjudicates FC-5)

**Priority:** P3 (does not independently block; couples with CNP-1).

**Evidence:**
- Both rc2 pin tags exist on origin and peel correctly — `pin/es-v6-rc2-candidate-2026-08-18^{}` → C,
  `pin/es-v6-rc2-freeze-2026-08-18^{}` → C+1 `[V — this lens's \`git ls-remote origin "refs/tags/pin/*"\`]`.
- `check_pin_tags.py` PINS at C+1 registers only `pin/ecs-contract-2026-07-27` and `v4.0.0`
  `[V .github/scripts/check_pin_tags.py:23-28 @C+1]`; the rc2 pins are NOT registered.
- The deferral is disclosed with a digest-guard rationale: "a post-freeze PINS edit would trip the
  digest guard by design" `[V docs/v6/ES6-V6-CANDIDATE/README.md:63-65 @C+1]`.

**Adjudication of FC-5:** R5(a)'s falsifier admits the alternative — "a recorded operator ruling
forbids the tag, with an alternative durable anchor recorded." The tags exist (not forbidden), the
deferral is recorded, and `candidate_tree_hash` is a durable in-git anchor. On the letter, the limb
passes. But through this lens: the PINS guard exists so that pin drift/deletion is a red build instead
of a silent break for the counterpart repository that fetches by SHA; an unregistered pin is a pet —
hand-known, unmonitored. And the deferral rationale is now circular: the digest guard that supposedly
justifies delaying PINS registration is the same digest guard CNP-1 shows red on every clean checkout.
When the packet is regenerated for CNP-1, the PINS edit rides the same re-freeze at zero marginal
cost — the deferral's reason evaporates with the defect.

**Falsifier:** statement — "unregistered rc2 pins carry no drift risk before promotion." Method:
at the next re-freeze, check whether the rc2 pins appear in PINS with peeled hashes and whether
`check_pin_tags.py` runs green guarding them. Threshold: finding stands if a re-frozen packet still
ships pins absent from PINS without a recorded operator ruling; falsified if the re-freeze registers
them (or an operator ruling forbidding registration is recorded). Timeframe: at the re-freeze; re-run
before any PROMOTION_RUN (R5's own timeframe).

**Validation kernel:** the tags themselves are correct, annotated, and peel to the right commits; the
deferral is disclosed in the packet rather than silent. Do not delete and re-push tags to "fix" this —
register, never move.

**Suggested fix:** fold `pin/es-v6-rc2-*` (or their rc3 successors) into PINS in the same commit series
as the CNP-1 regeneration.

### CNP-4 — Hand-maintained prose duplicates machine-checkable state and has already drifted (P3; confirms FC-4's mechanism, narrows its blast radius)

**Priority:** P3 (metatextual; erodes trust in an otherwise honest packet).

**Evidence:**
- KL-RESTAMP's statement claims the discipline "binds per-file sha256 digests plus the candidate tree
  hash, and the validator recomputes those digests" with consequence "Any post-freeze edit to an
  inventoried file turns the validator red" `[V docs/v6/ES6-V6-CANDIDATE/promotion-packet.json:66-72
  @C+1]` — true only on the generating host's dirty tree; everywhere else the validator is red on the
  *unmodified* packet (CNP-1). The disclosure describes the intended posture, not the observed one.
- KL-RESTAMP also omits the two elements R5(c) specifically required (the post-freeze addition of
  `clean-baseline.json`; the deleted disclaimer's substance) `[I <- V promotion-packet.json:66-72 @C+1
  + pred ruling-set R5 acceptance criterion]` — the dossier's PARTIAL on R5(c) is confirmed by this
  lens's read.
- KL-DRAFT-CI's "52 of the 53" clean-room fraction vs measured 51-of-54 (D-4) — different count bases,
  unreconciled in the prose.

**Falsifier:** statement — "packet prose tracks machine-verifiable reality." Method: at the re-frozen
packet, for each known_limit/consequence sentence that asserts validator/gate behavior, execute the
assertion on a clean checkout. Threshold: zero prose claims contradicted by execution. Timeframe: at
re-submission.

**Validation kernel:** the packet's structural honesty — NOT_READY, empty requested-acts, blocking
claims naming this very gauntlet, UNPROVED on `CLM-INDEPENDENT-GAUNTLET`
`[V docs/v6/ES6-V6-CANDIDATE/claim-to-proof-matrix.json @C+1]` — is real and must not be "repaired" by
softening it. The defect is stale descriptive prose, not concealed substance.

**Suggested fix:** in the re-freeze, regenerate known-limit prose from the same measured runs the
evidence JSONs capture (or scope the sentences to what was executed: "verified on the generating host;
clean-checkout behavior gated by <test>"), and add a validator self-test case that runs the digest
stage against a synthetic inventory containing a `.pyc` entry so the CNP-1 class fails closed in CI
forever.

## Per-acceptance-criterion notes (where this lens has something to say)

- **R1 (terminal-gate-forgeable): discharged.** Schema @2 adds `independent_gauntlet_ref` with
  `gauntlet_run_id`/`gauntlet_verdict_path`/`gauntlet_subject_sha`
  `[V plugins/epistemic-skills/contracts/v6-assurance/promotion-packet.schema.json:22,131-146 @C+1]`;
  packet carries it `null` pending this run `[V promotion-packet.json:10 @C+1]`; self-test's planted
  bare-enum-GO / hand-edited-blocking / post-freeze-mutation cases all fail closed (re-run by this
  lens, rc=0). The honest-defaults kernel is preserved.
- **R2 (secret-scan): discharged.** `CLM-SECRET-SCAN` PROVED in the matrix
  `[V docs/v6/ES6-V6-CANDIDATE/claim-to-proof-matrix.json @C+1]`; this lens independently fetched run
  32190035556: `workflow_dispatch`, head_sha == C, `full-history-secret-scan` success, "Prove the
  scanner detects a planted secret" step success. The criterion's exact-SHA + positive-control
  threshold is met on live evidence.
- **R3 (merges): discharged on its operator limb** per the echo-certified ODR (D1); this lens adds
  nothing beyond the dossier's verification and the challenger's spot-check of the CLM-MERGE rows.
- **R4 (SHA-binding): discharged.** C/C+1 layering verified by this lens's own worktree reads (both
  worktrees clean at the pinned SHAs); pin tags peel correctly (CNP-3 evidence); the packet stamps C
  throughout. The self-describing-artifact identity lag that decided the predecessor is closed by the
  two-commit discipline.
- **R5 (immutability): OPEN — the deciding criterion.** (a) tags exist, PINS deferred — letter-met via
  the alternative-anchor clause, see CNP-3; (b) per-file digests exist and are verified by the
  validator — **fails on its own falsifier**: "validator exits non-zero on tampering" holds, but the
  AC requires the digest layer to verify the packet, and it cannot on any clean checkout (CNP-1,
  re-executed by this lens); (c) KL-RESTAMP disclosure PARTIAL (CNP-4); (d) restamp refusal present
  and stronger than specified — no override flag at all
  `[V .github/scripts/v6_generate_candidate_packet.py:1231-1252 @C]` — with the irony that the dirty
  check's packet-dir exclusion `[V same file:1240-1246 @C]` plus the porcelain tree model is exactly
  the blind spot that let the `.pyc` digests through. One open P1 limb ⇒ R5 open ⇒ NO-GO.
- **R6 (tracker reconciliation): discharged (path a).** `CLM-DISPOSITION-CENSUS` present with a
  census-scoped statement `[V claim-to-proof-matrix.json @C+1]`; generator calls
  `require_dispositions` `[V v6_generate_candidate_packet.py:1259 @C]` (fail-closed behavior per
  challenger, :792-802).
- **R7 (wf path coverage): discharged (path a).** `epistemic-flexibility.yml` pull_request block
  carries `types: [opened, synchronize, reopened, ready_for_review]` and no `paths:` filter, with an
  in-tree comment citing R7/R8 `[V .github/workflows/epistemic-flexibility.yml:10-14 @C]`;
  `CLM-WF-PATH-COVERAGE` PROVED with the narrowed statement `[V claim-to-proof-matrix.json @C+1]`.
- **R8 (ready-mark takeover): discharged.** All five gating workflows declare `ready_for_review`
  `[V .github/workflows/{epistemic-flexibility,release-security,commission-watch-contract,
  mission-custody-contract,openai-bundles}.yml @C]`; drill run 32184104218 re-fetched by this lens:
  event=pull_request, head `564a1e53…`, conclusion `failure` ≠ skipped — the takeover *mechanism* is
  proven. Note well: when this takeover fires on the freeze PR, CNP-1 turns the required job red —
  the drill's green mechanism and the packet's red validator arrive together.
- **R9 (cleanroom coverage): discharged (substance).** Completeness print with numerator/denominator
  and named exclusions `[V .github/scripts/cleanroom_ci.sh:131,156-163,182 @C]`; KL-DRAFT-CI names all
  five skipped jobs + DCO `[V promotion-packet.json @C+1]`. Count-base discrepancy (52/53 vs 51/54)
  carried under CNP-4.
- **R10 (main-red): discharged by live state** per the dossier's verified retirement (PR #195 merged,
  main push runs green); not re-fetched by this lens — accepted as `[I <- evidence/live-verification
  -2026-08-18.md]`, and the criterion's own falsifier welcomes the retirement.
- **R11 (public-content gate): discharged; (d) PARTIAL-minor confirmed.** This lens re-ran the gate at
  C: rc=0, "7 patterns, 37 allowlisted exact files digest-verified (1 dormant entries name files
  absent from this branch)" `[V — re-execution at C]`. Owner + cadence recorded
  `[V .github/scripts/check_public_content.py:67-69 @C]`. The residual dormant entry is digest-bound
  and exempts nothing on this branch — acceptable as designed, provided the cadence is real. This is
  the good pattern: exemptions as explicit, digest-pinned, reviewable acts rather than prefix-based
  drift-amnesty.
- **R12 (operator-alert channel): discharged.** `blocking_claims == ['CLM-INDEPENDENT-GAUNTLET']`
  `[V promotion-packet.json @C+1]`; planted hand-edited-blocking self-test case fails closed (this
  lens's self-test re-run).
- **R13 (acceptance procedure): discharged — and it is the tripwire.** The procedure exists, names the
  acceptor's personal verifications and the recording artifact
  `[V docs/v6/OPERATOR-ACCEPTANCE-PROCEDURE.md:31-70 @C+1]`. Its item 4 is precisely what CNP-1 makes
  unsatisfiable; the procedure did its job by being specific enough to fail against.
- **R14 (taxonomy/register): discharged (mechanism)** — planted register-cites-missing-claim and
  register-requirement-unmapped self-test cases fail closed (this lens's re-run).
- **R15 (custody residual): discharged (disclosure limbs).** `KL-GUARD-LEXICAL` present with the
  LIMITED row `[V promotion-packet.json:73-79 @C+1]`. FC-2's privileged-NT FAIL-instead-of-SKIP
  behavior is a real characterization-pin wrinkle on an unusual host class; gating Linux surface is
  green at C `[I <- evidence/live-verification-2026-08-18.md run 32190028540 job contract: success]`.
  Noted, not blocking; same for FC-3's one-line `target_is_directory` omission
  `[V .github/scripts/sync_skill_surfaces.py:524 @C]` — worth folding into the re-freeze since the
  tree is being regenerated anyway.

## Known unknowns

- FC-2's privileged-NT realpath/case-fold divergence was not re-executed by this lens (host behavior;
  cited from `evidence/oracle-crib-2026-08-18.md`); its mechanism is plausible and consistent with the
  FC-3 code read, but remains second-hand.
- The clean-room 51/54 vs 52/53 count-base discrepancy (D-4) is unreconciled — this lens did not re-run
  the clean-room harness; either count could be the stale one.
- Whether R5(a)'s "recorded operator ruling" alternative formally covers *deferral-by-README* (as
  opposed to an operator-authored ruling) is a judge call; CNP-3 argues the re-freeze moots it.
- The whole-tree-reader oracle strengthening (R7) guards today's workflows; whether it classifies
  *future* whole-tree readers correctly is unprobed by this lens.
- Single-model-family caveat (all seats Kimi/Moonshot) stands over this report; D8 Step-7b remains the
  designated cross-family check at GO posture.

## The single "do this next" move

Re-freeze with exactly one behavioral change: make `build_source_inventory` enumerate git (`git
ls-files`) instead of walking the filesystem, fold in the PINS registration and the FC-3 one-liner,
regenerate, re-dispatch the five requal workflows at the new C, re-freeze as the new C+1. The pipeline,
the drills, the disclosures, and the acceptance procedure for that re-freeze already exist and have
already been executed once — this candidate's remaining defect is one tree model, not a program.
