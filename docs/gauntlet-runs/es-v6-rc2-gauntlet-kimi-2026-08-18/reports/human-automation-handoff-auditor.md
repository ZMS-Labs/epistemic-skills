# Lens report — human-automation-handoff-auditor

Run: `es-v6-rc2-gauntlet-kimi-2026-08-18`. Subject: candidate C
`6db8c50420b194aebbd09a2ea5f81c6a276897dc` with freeze packet at C+1
`9aecd467236dfb927e9c13784d77a16d62f28f67`. `[V ...]` citations resolve
against the C tree (code) or the C+1 tree (packet), each naming which; "tip"
means branch tip `36b40a6` (handoff document). Live probes were re-executed
by this lens seat, not adopted from the dispatcher.

**Lens question:** when the automation (validators, packet generators, CI
gates) gives up or goes red, what does the human see, and can they still do
the job? Who has authority mid-handoff?

## Verdict recommendation: NO-GO (against this SHA)

One P1 finding, re-freeze class. The terminal state this candidate exists to
reach is a HUMAN act — operator acceptance — and the acceptance procedure's
own verification list cannot be walked at the sealed packet: its step 4
requires the assurance validator to pass on the exact packet bytes, and the
validator fails closed on every clean checkout of C+1 (independently
reproduced by this seat). The automation hands the human a permanent red
alarm whose message describes a tampering event that did not happen. That is
the textbook handoff failure this lens exists to catch: the takeover is
unpracticed-in-fact (the drill cannot complete) and the alert carries false
context at the exact moment of transfer. Repair requires editing an
inventoried generator and regenerating the packet — a new SHA — so it is not
dischargeable as a condition on C.

Everything else in this lens's scope is discharged or minor: the acceptance
procedure itself (R13) is real and well-formed, the ready-mark drill
transcript (R8) exists and was live-verified, authority mid-handoff (R3/D1,
D4, D8) is recorded and echo-certified, and the blocking-claim derivation
(R12) recomputes clean.

## Findings (priority-placed)

### HAHA-1 (P1) — The operator-acceptance drill is unexecutable at the sealed packet; the seal fires a permanent false-positive alarm with misleading context

Confirms FC-1, independently reproduced, and reframes it as the handoff
failure it is.

**Evidence:**

- This seat ran `validate_v6_assurance.py` in the pristine C+1 worktree
  (bytecode writes disabled): exit 1, `AssertionError: R5 DIGEST MISMATCH:
  inventoried files changed after the packet was generated (restamp class)`
  naming 10+ absent `__pycache__/*.pyc` entries. [V C+1
  `plugins/epistemic-skills/contracts/v6-assurance/validate_v6_assurance.py:183`
  raising; run transcript this seat 2026-08-18; corroborates
  `evidence/validator-c1-digest-failure.md`]
- Script-computed on C+1: `source-inventory.json` `file_digests` has 158
  entries; 17 are `__pycache__/*.pyc`; of the 141 real sources, zero absent,
  zero content-mismatched. The substrate seal is intact; the tree model is
  not. [V C+1 `docs/v6/ES6-V6-CANDIDATE/source-inventory.json`, recomputed by
  this seat]
- Root cause read at C: `build_source_inventory` walks the filesystem
  (`rglob("*")`, .gitignore-blind) while `dirty_tree()` uses
  `git status --porcelain` (.gitignore-respecting; `__pycache__/` is ignored
  at `.gitignore:1`). The clean-tree refusal cannot see the volatile class
  the inventory seals. [V C
  `.github/scripts/v6_generate_candidate_packet.py:851-858,1202-1204`]
- The handoff consequence chain: `OPERATOR-ACCEPTANCE-PROCEDURE.md` item 4
  requires the operator to personally confirm "the assurance validator
  passes on the exact packet bytes at the candidate SHA" [V C+1
  `docs/v6/OPERATOR-ACCEPTANCE-PROCEDURE.md:56-59`]. As sealed, no acceptor
  can ever check that box. And when the freeze PR is marked ready (the R8
  takeover), `stdlib-checks` runs the validator on a fresh CI checkout
  [V C `.github/workflows/epistemic-flexibility.yml:268`] — guaranteed red.
- The alarm's message ("restamp class: inventoried files changed") asserts a
  post-freeze mutation on an untouched tree. A cold operator cannot
  distinguish "17 volatile bytecode artifacts" from real tampering without
  out-of-band knowledge the packet does not supply. Alert-to-context gap,
  alarm-fatigue class.

**Falsifier:** Method: fresh `git worktree add`/clone of C+1 on any OS; run
the validator; then plant a one-byte edit in an inventoried source and
re-run. Threshold: exit 0 on the clean checkout AND non-zero on the planted
edit discharges the finding; today the first limb fails everywhere (this
seat: exit 1). Timeframe: before operator acceptance; re-run on every packet
regeneration.

**validation_kernel:** The fail-closed digest binding over the 141 real
sources verifies byte-exact on a clean checkout; the validator self-test at
C proves planted post-freeze mutations fail closed (18/18 PASS, re-run by
this seat); `candidate_tree_hash` (`152b1df0…`) is portable and correct. The
defect is ONLY the inventory's tree model (filesystem walk sealing
`.gitignore`d volatile artifacts the porcelain dirt-check cannot see). Any
fix MUST preserve the fail-closed semantics and the digest layer.

**Fix:** Exclude non-git-tracked (or volatile-class) paths from
`build_source_inventory`'s walk — e.g. intersect with `git ls-files` — in
`v6_generate_candidate_packet.py`; regenerate the packet (new SHA);
disclose in KL-RESTAMP that the rc2 seal false-positived on clean checkouts.

### HAHA-2 (P2) — The context the human inherits misstates the alarm they will meet

Confirms the substance of FC-4 (two of its three limbs).

**Evidence:**

- The handoff tells the incoming human: branch-tip commits "must leave every
  inventoried file byte-identical to C — the validator's digest
  recomputation proves it; run it yourself, trust nothing stamped"
  [V tip `docs/v6/ES6-V6-CANDIDATE/KIMI-SEAT-HANDOFF.md:46-48`]. Run, it
  proves nothing — it fails (HAHA-1). The designated trust instrument is
  broken and the handoff asserts it works.
- KL-RESTAMP's consequence text: "Any post-freeze edit to an inventoried
  file turns the validator red instead of shipping silently" [V C+1
  `docs/v6/ES6-V6-CANDIDATE/promotion-packet.json`, known_limits]. True and
  incomplete: the validator is red with NO post-freeze edit, everywhere
  except the generating host's dirty tree. The known_limit describes an
  alarm that fires on attack and is silent about the alarm that fires
  permanently.
- Counterweight (honesty structure otherwise intact, verified by this seat):
  `readiness: NOT_READY`, `independent_gauntlet: NOT_RUN`,
  `self_certification: refused`, `blocking_claims: ['CLM-INDEPENDENT-GAUNTLET']`
  [V C+1 `promotion-packet.json`]. The packet is not inflating itself; the
  gap is specific to the seal's posture.
- Third FC-4 limb ("expected loud skips mischaracterizes FC-2/FC-3"):
  ATTACKED, partially killed. The handoff's skip note is correctly scoped —
  "skip loudly on NT WITHOUT symlink privilege" [V tip handoff:58-63]. It
  does not claim what privileged NT does. The residual defect is HAHA-3's
  host-class gap, not a false statement.

**Falsifier:** Method: execute the handoff's own crib validator command at a
pristine C+1 checkout and read KL-RESTAMP against the result. Threshold:
validator green at C+1, OR a KL-RESTAMP sentence disclosing the clean-
checkout false positive, falsifies this finding. Today: red, and no such
sentence. Timeframe: at the next packet regeneration; the KL text travels
with the packet.

**validation_kernel:** The handoff's "trust nothing stamped, run it
yourself" posture is exactly right and must survive; the packet's
NOT_READY/NOT_RUN/refused/empty-acts honesty structure must survive. Fix the
claims, not the posture.

**Fix:** One disclosure sentence in KL-RESTAMP (the seal false-positives on
clean checkouts; substrate intact) and a corrected handoff line; lands
naturally with the HAHA-1 regeneration.

### HAHA-3 (P3) — Privileged-NT host class: the handoff's triage rule misclassifies deterministic platform artifacts as real findings

Confirms FC-2 and FC-3, reproduced by this seat, merged as one handoff-gap
finding.

**Evidence:**

- `test_custody_gate.py` at C on this host (Windows with symlink
  privilege): 2 FAILURES, repeat-deterministic — the R15 characterization-pin
  tests. The skip guard keys on `OSError` from `symlink_to`; this host
  creates symlinks, then NT `realpath`/case-fold semantics diverge. [V this
  seat's run 2026-08-18; corroborates `evidence/oracle-crib-2026-08-18.md`
  cluster A]
- `sync_skill_surfaces.py --self-test` at C: FAIL, `PermissionError` —
  `symlink_to(...)` without `target_is_directory=True` [V C
  `.github/scripts/sync_skill_surfaces.py:524`; this seat's run].
- The handoff arms the human with a triage rule: "re-run the exact file
  once; a repeat failure is real" [V tip handoff:54-57]. On this host class
  both failures repeat deterministically, so the handoff's own procedure
  directs the human to record platform artifacts as REAL findings. The
  "expected loud skips" note covers only unprivileged NT [V tip
  handoff:58-63]; the privileged-NT class is nowhere anticipated.
- Containment: gating Linux surfaces green at C (requalification runs at
  head_sha == C live-verified; KL-WINDOWS discloses no native-Windows
  requalification). Non-gating, platform-class, one-line-fix class.

**Falsifier:** Method: on a Windows host WITH symlink privilege, run the two
R15 pin tests and the sync self-test at C. Threshold: skips-with-reason or
passes falsify the finding; today: deterministic FAIL/FAIL. Timeframe:
single run, minutes; re-check after any skip-guard edit.

**validation_kernel:** The R15 lexical-matching characterization pins and
the `--check` gating operation are green where they gate (Linux CI at C);
the fail-closed sensitive-path guards are correct behavior. Do not weaken
the pins to silence the platform noise — fix the skip guard (capability
probe, not `OSError`) and add `target_is_directory=True`.

**Fix:** Capability-based skip guard in the R15 tests;
`target_is_directory=True` at `sync_skill_surfaces.py:524`; one handoff
sentence naming the privileged-NT failure signature as environment noise.

### HAHA-4 (P3) — R5(a) PINS deferral: the durable anchor exists but the guarding registry does not know it

FC-5, resolved as far as the record allows; left as a judge call with a
recommendation.

**Evidence:**

- Origin pin tags exist and peel correctly, verified live by this seat:
  `pin/es-v6-rc2-candidate-2026-08-18^{}` → C;
  `pin/es-v6-rc2-freeze-2026-08-18^{}` → C+1 (`git ls-remote`).
- The rc2 pins are NOT in `check_pin_tags.py`'s PINS registry at C [V C
  `.github/scripts/check_pin_tags.py:23-29` — only `pin/ecs-contract-2026-07-27`
  and `v4.0.0`].
- The deferral is disclosed with a mechanism rationale: "PINS registration
  follows at promotion (a post-freeze PINS edit would trip the digest guard
  by design)" [V C+1 `docs/v6/ES6-V6-CANDIDATE/README.md:63-65`]. Operator
  decision D4 classifies non-`v*` pin tags as BUILD-permitted
  agent-executable acts [V C+1 `docs/v6/operator-decision-record-2026-08-18.md`
  D4].
- The criterion's falsifier asks for the tag in PINS "or a recorded operator
  ruling forbids the tag, with an alternative durable anchor recorded".
  Neither limb is cleanly met: the tag is not forbidden (it exists,
  operator-classified), and the "alternative durable anchor" is the
  digest-guard rationale rather than a named substitute anchor. From this
  lens: a future human auditing the pin registry will not find the rc2
  anchors — the inventory the human consults and the anchors that exist have
  diverged, with only prose bridging them.

**Falsifier:** Method: read PINS at the next freeze/promotion and peel the
origin tags. Threshold: rc2 pins present in PINS with matching peeled SHAs,
or an operator-authored ruling naming the deferral and its substitute
anchor, falsifies the finding. Timeframe: at promotion, per the README's own
deferral — this is a scheduled check, not a block.

**validation_kernel:** The digest-guard tripwire that motivates the deferral
is the same fail-closed seal HAHA-1 depends on; the tags themselves exist
and are correct. Do not "fix" by weakening the guard to allow mid-freeze
PINS edits.

**Fix:** Register both rc2 pins in PINS in the same commit that regenerates
the packet (or record the operator's explicit deferral ruling); re-verify at
promotion per the criterion's own timeframe.

## Findings table

| id | title | priority | AC/criterion engaged | status vs dossier hypothesis |
|---|---|---|---|---|
| HAHA-1 | Acceptance drill unexecutable; seal false-positives with misleading alarm text | P1 | R5(b), R13 (procedure item 4), R8 takeover path | FC-1 CONFIRMED (independently reproduced) |
| HAHA-2 | Handoff/KL-RESTAMP misstate the alarm posture | P2 | R5(c) | FC-4 CONFIRMED in substance (1 of 3 limbs killed) |
| HAHA-3 | Privileged-NT host class unanticipated; triage rule misclassifies | P3 | R15 (pin behavior), handoff accuracy | FC-2/FC-3 CONFIRMED (reproduced) |
| HAHA-4 | rc2 pins absent from PINS registry; deferral prose-only | P3 | R5(a) | FC-5 CONFIRMED as stated; discharge question referred to judge |

## Per-acceptance-criterion notes (lens scope)

Verified against the predecessor ruling-set's own falsifiers; "discharged"
means the falsifier's threshold is met on evidence this seat re-ran or read
in the frozen trees.

- **R1 (terminal-gate forgeable) — discharged at mechanism level.** The
  validator at C+1 requires an on-disk verdict artifact naming the candidate
  SHA for any recorded verdict, and empty `blocking_claims` plus a recorded
  `operator_acceptance` for terminal readiness [V C+1
  `validate_v6_assurance.py:236-258,264-282`]. Self-test at C: 18 planted-
  defect cases fail closed, including bare-enum-GO (re-run by this seat,
  PASS). Caveat: this mechanism only gets to speak once HAHA-1 stops it from
  screaming about `.pyc` files first — alarm ordering matters to the human.
- **R2 (secret scan) — discharged.** Matrix row `CLM-SECRET-SCAN` PROVED
  [V C+1 `claim-to-proof-matrix.json`]; run 32190035556 live-verified by
  this seat: `workflow_dispatch` at head_sha == C, `full-history-secret-scan`
  success, planted-secret positive-control step success.
- **R3 (merge consent) — discharged.** D1 ratifies #190/#156/#192 in the
  echo-certified operator record [V C+1 ODR "D1"]; matrix reconciliation
  rows for all three merges cite D1 [V C+1 `claim-to-proof-matrix.json:491-538`].
  Authority mid-handoff is now defined: the operator ruled, durably.
- **R5 (immutability mechanism) — NOT discharged.** Limb (b) is present but
  broken on arrival (HAHA-1); limb (c) present with a posture gap (HAHA-2);
  limb (a) partial (HAHA-4); limb (d) generator-refusal not independently
  re-probed by this lens (other lenses' basin).
- **R8 (ready-mark takeover) — discharged, and the dossier's known-unknown
  is resolved.** The drill transcript EXISTS at
  `docs/v6/evidence/r8-ready-mark-drill-2026-08-18.md` [V C+1]; this seat
  live-verified three ready-state runs (32184104218 executed-failure,
  32184104140 success, 32184104164 success) created at 20:46:05Z at the
  unchanged drill head `564a1e5…` with event `pull_request` — the criterion's
  "new run per gating workflow at identical head, conclusion != skipped"
  threshold is met. The takeover has been practiced once, on a throwaway
  PR — exactly the drill the falsifier template asks for. Note the drill's
  stdlib-checks leg executed-and-FAILED (latent PyYAML defect, fixed at C);
  the freeze PR's own takeover will additionally hit HAHA-1's validator red.
- **R10 (main-red premise) — retired by live state.** This seat re-read
  main: head `03b7724`, push runs `epistemic-flexibility` and
  `release-security` both SUCCESS (2026-08-18T22:03:45Z). The disclosure's
  own retirement clause has fired.
- **R12 (blocking derivation) — discharged.** This seat recomputed
  `derive_blocking` over the C+1 matrix in-memory:
  `['CLM-INDEPENDENT-GAUNTLET']` == packet `blocking_claims`. Zero unlisted
  BLOCKED/operator-owned/P1-consequence claims.
- **R13 (no acceptance procedure) — discharged.** The procedure exists, is
  repo-authored, names the sole acceptor (the repository operator; agents
  must refuse), lists five personal-verification items including the four
  operator holds and the R3 ratification, defines the recording artifact
  (`operator_acceptance` with `accepted_by`/`accepted_at`/`verdict_ref`),
  and states the scope limit first [V C+1
  `docs/v6/OPERATOR-ACCEPTANCE-PROCEDURE.md`]. Schema holds the fields
  [V C+1 `promotion-packet.schema.json`, `operator_acceptance` object];
  validator enforces presence + `verdict_ref` match + GO precondition [V C+1
  `validate_v6_assurance.py:264-282`]. This is the human-in-the-loop done
  right — which is precisely why HAHA-1 (its step 4 unmeetable) is P1 and
  not noise.
- **R4, R6, R7, R9, R11, R14, R15 — outside this lens's basin.** Dossier
  Step-0 items (identity closure, requalification, trigger repairs,
  allowlist digest semantics) are consistent with what this seat read in
  passing; per-row re-execution left to the owning lenses.

## Rival hypotheses

- **Most supported:** "the candidate discharges the fix ticket except for
  one re-freeze-class seal defect" — HAHA-1 is decisive alone; R1/R2/R3/R8/
  R10/R12/R13 all independently verified discharged.
- **Killed:** "the ready-mark drill transcript does not exist" (dossier
  known-unknown) — it exists and live-verifies. Also killed: FC-4's third
  limb (the handoff's skip note is correctly scoped; the real gap is the
  unanticipated host class, HAHA-3).
- **Killed:** "the digest seal is conceptually unsound" — 141/141 real
  sources verify byte-exact; planted mutations fail closed; the defect is
  the tree model, not the mechanism.

## Minimum fix set (from this lens)

1. `v6_generate_candidate_packet.py`: intersect the inventory walk with
   tracked files (or exclude volatile/`__pycache__` class); regenerate
   packet → new SHA → re-freeze. Preserve fail-closed semantics and all 141
   real-source digests.
2. With that regeneration: KL-RESTAMP gains the clean-checkout false-
   positive disclosure; handoff crib line corrected; rc2 pins registered in
   PINS (or operator deferral ruling recorded).
3. Independent of the freeze: capability-based skip guard for the R15 pin
   tests; `target_is_directory=True` in the sync self-test; one handoff
   sentence on the privileged-NT signature.

## Known unknowns / not verified by this lens

- Generator `--restamp` refusal (R5 limb d) — not re-probed.
- Per-row matrix falsifier re-execution beyond R2/R12 spot checks — panel
  scope, other lenses.
- macOS surface (es#162) — read-only per handoff; not re-executed.
- Whether a GAUNTLET seat on a non-Windows host would have caught HAHA-1
  earlier — the defect is host-independent (any clean checkout fails), so
  seat platform is not load-bearing for the finding.
- Single-model-family caveat (all seats this run share one family): carried;
  D8 Step-7b cross-family consult is the designated mitigation at GO
  posture, and this run's handoff document surfaces it correctly [V tip
  handoff:121-129].
