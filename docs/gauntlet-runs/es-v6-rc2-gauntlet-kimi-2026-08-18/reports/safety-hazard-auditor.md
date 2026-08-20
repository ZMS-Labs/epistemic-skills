# Lens report — safety-hazard-auditor

Run: `es-v6-rc2-gauntlet-kimi-2026-08-18`. Subject: candidate C
`6db8c50420b194aebbd09a2ea5f81c6a276897dc` + freeze packet C+1
`9aecd467236dfb927e9c13784d77a16d62f28f67`. All findings below were
re-verified by THIS seat in the two pristine worktrees; nothing is adopted
on the dossier's say-so. `[V … C]` = candidate code tree; `[V … C+1]` =
freeze packet tree; `[V live]` = live probe run by this seat on 2026-08-19
(read-only; bytecode generation suppressed, temp writes confined to a
scratch tempdir and removed).

## Verdict recommendation: **NO-GO against C** (re-freeze class; favorable prognosis)

One decisive defect (SHA-1 = dossier FC-1) survives independent
re-execution and is not dischargeable as a condition on C, because its
repair edits an inventoried generator and regenerates the packet — a new
SHA. Under the predecessor's own verdict arithmetic (any open P1 ⇒ NO-GO
against THIS SHA), that settles the enum. Everything else my lens found is
P3-class repair work that rides the same re-freeze.

**Lens-scope ruling (mandated by my card's bias line):** the
physical/health coupling check comes first, and it comes back negative.
The subject is an epistemic-discipline skill/plugin set: its only
actuation surface is a PreToolUse hook that allows or refuses agent tool
calls (`plugins/epistemic-skills/hooks/hooks.json` — matcher
`Bash|Write|Edit|mcp__.*`, one custody hook command [V C]). The `health`
skill reads IT-system state, not human health [V C
`plugins/epistemic-skills/skills/health/SKILL.md:1-40`]; grep hits for
medical/clinical vocabulary are synthetic eval fixtures and design docs,
not advice surfaces. No energy sources, no device actuation, no
medical/safety-relevant outputs. The persona's contraindication ("pure
information systems with no physical/health coupling") applies: **the
harm ceiling of any defect in this subject is data loss, confidentiality
loss, or governance-integrity loss — there is no path to bodily or
environmental harm, and I import no industrial-safety ceremony.** My
layer-of-protection analysis is applied to the integrity/confidentiality
layers that DO exist.

Hazard inventory (severity / exposure / independent layers), STPA-style:

- H-A custody-guard false-allow → unauthorized write/command on the
  operator's host → data loss. Layers: guard matching (1), disclosed
  lexical residual + characterization pin (2), fail-closed default (3).
  Residual is real on POSIX, disclosed, pinned; see SHA-3 for the
  platform scoping defect.
- H-B public-content gate false-pass → private strings in a public repo →
  confidentiality harm. Layers: 7-pattern scan (1), digest-bound
  exact-file allowlist that fails closed on byte drift (2), CI gating +
  release-security secret scan (3). Verified green at C [V live: `7
  patterns, 37 allowlisted exact files digest-verified (1 dormant…)`,
  rc=0]. This is the healthiest layered surface in the freeze.
- H-C post-freeze packet mutation accepted by the operator → governance
  harm. Layers: per-file digest seal (**permanently false-alarming —
  SHA-1**), `candidate_tree_hash` (intact, portable [V C+1
  `source-inventory.json:4`]), origin pin tags (exist, peel correctly,
  but guarded by zero automated checks until PINS registration — SHA-4),
  validator self-tests (green per crib).
- H-D false-green readiness (silent CI skips) → merge-permissive misread.
  Repaired at C by `ready_for_review` trigger types on all five gating
  workflows [V C: `epistemic-flexibility.yml:10-14`,
  `mission-custody-contract.yml:14-18`,
  `commission-watch-contract.yml:15-19`, `openai-bundles.yml:5-9`,
  `release-security.yml:9-13`] — but see SHA-1: the takeover's first
  fresh-checkout CI run executes the red validator.

## Findings (severity-ranked)

### SHA-1 (P1) — The @2 digest seal fails closed on every clean checkout; the packet's only tamper detector is a permanent false alarm

(Adopts dossier FC-1 after independent re-execution; the framing and the
alarm-credibility consequence are this lens's.)

**Evidence.** Ran the validator in the pristine C+1 worktree with
bytecode generation suppressed (so no `.pyc` was recreated by my own
probe): exit 1, `AssertionError: R5 DIGEST MISMATCH … (absent)` listing
exactly the 10 `__pycache__/*.pyc` entries the dossier's transcript names
[V live, matching `evidence/validator-c1-digest-failure.md:6-21`].
Script-measured at C+1: 158 `file_digests` entries, 17 of them
`__pycache__/*.pyc` [V C+1 `source-inventory.json:16-19` et seq.]. The
seal over the 141 real sources is byte-exact on a clean checkout (the
dossier's measurement; my run confirms the failure set is `.pyc`-only —
no real-source entry appears in the mismatch list).

**Why P1 from this lens.** The digest seal is layer 1 of hazard H-C —
the ONLY automated detector of post-freeze packet mutation. A detector
that is red on the unmodified artifact everywhere except the generating
host's dirty tree trains every operator who runs it to discount its red:
alarm fatigue is the availability half of the fail-closed design, and it
converts one independent layer into zero effective layers by habituation.
Two structural consequences compound it: (a) the operator-acceptance
procedure's item 4 requires "the assurance validator passes on the exact
packet bytes at the candidate SHA" as a personally-verified precondition
[V C+1 `docs/v6/OPERATOR-ACCEPTANCE-PROCEDURE.md`, item 4] — as sealed,
that precondition is unsatisfiable, so acceptance on C is blocked by the
packet's own procedure; (b) the R8 ready-mark takeover now dispatches the
gating workflows on fresh CI checkouts (no `__pycache__`), so the freeze
PR's required `stdlib-checks` job goes red on arrival — the R8 repair and
the R5(b) seal are in direct collision on this packet.

**Falsifier.** Method: fresh `git worktree add`/clone of C+1 on any OS;
run `validate_v6_assurance.py`; then plant a one-byte edit in an
inventoried real-source file and re-run. Threshold for discharge: exit 0
on the pristine checkout AND non-zero on the planted edit. Today the
first limb fails everywhere (reproduced by this seat). Timeframe: before
operator acceptance; re-run on every regeneration.

**Validation kernel (must survive the fix).** The fail-CLOSED polarity is
correct — absent/mutated → red, never silently green; the 141 real-source
digests verify byte-exact; `candidate_tree_hash`
(`152b1df0f177303175eca422424361e086e6f0d8` [V C+1
`source-inventory.json:4`]) binds C's git tree and IS portable; the
failure is loud and self-revealing, so no false-green flows from it. The
defect is the inventory's tree model (filesystem walk includes
`.gitignore`d volatile artifacts the porcelain dirt-check cannot see),
not the concept.

**Suggested fix.** Align the inventory walk with the git tree model
(`git ls-files` or equivalent ignore-aware enumeration) in
`v6_generate_candidate_packet.py`; regenerate the packet (new SHA →
re-freeze); keep the fail-closed digest binding and the tree hash
unchanged.

### SHA-2 (P3) — The R15 custody residual is POSIX-only in fact; its pin and its disclosure are not platform-scoped, and the pin is double-blind under pytest

**Evidence.** The pin
`test_guard_match_is_lexical_symlinked_parent_diverges` [V C
`test_custody_gate.py:135-169`] exists and asserts a POSIX path-model
invariant: a write spelled `link/../x.txt` lands inside the guarded tree
because the kernel follows the symlink before resolving `..`. On this
privileged-NT host the pin's two path-model checks FAIL while both
guard-behavior checks PASS [V live: `FAIL
guard-lexical-realpath-lands-in-guarded-tree`, `FAIL
guard-lexical-collapse-stays-textual`, `ok
guard-lexical-symlinked-parent-not-matched`, `ok
guard-lexical-direct-spelling-still-matched`]. Landing-zone probe: a file
written through the symlinked-parent spelling on NT lands at the tempdir
ROOT — `guarded/probe.txt`: absent; `probe.txt` at root: present [V
live]. I.e., on NT the filesystem itself collapses `link/..` lexically,
the guard's lexical collapse MATCHES the platform's resolution, and the
false-allow class the residual discloses does not exist there.
KL-GUARD-LEXICAL [V C+1 `promotion-packet.json:74`] and
CLM-MC-GUARD-LEXICAL (LIMITED [V C+1 claim-to-proof-matrix.json]) do not
say the residual is POSIX-scoped. Separately: the test harness's
`check()` only appends to a global `FAILURES` list [V C
`test_custody_gate.py:21-31`]; the failure signal reaches the exit code
solely via the `__main__` runner [V C `test_custody_gate.py:432-438`].
Under pytest — the discovery tool a developer actually reaches for — the
pin reports **1 passed** while two of its checks are recorded FAIL [V
live]. So the residual's only detector fails loudly on NT for
platform-model reasons (cry-wolf) and passes silently everywhere under
pytest even when its checks fail (false-green): both directions of alarm
corruption on one pin.

**Assessment.** This refines FC-2, not just confirms it: the NT failure
is not a guard-semantics divergence but a platform-invariant mismatch in
a characterization test — the guard's protective behavior is intact on
NT. The substance (POSIX residual disclosed, behavior unchanged this
freeze) is correct and was verified: the inherited safe-direction
reasoning IS reinstated as the `_collapse_parent_segments` docstring [V C
`custody_gate.py:85-104`], satisfying R15's comment limb. Held at P3:
CI's gating surface is Linux `__main__`-runner green at C; the corrupted
surfaces are local-dev NT and any pytest invocation.

**Falsifier.** Method: on a privileged-NT host, run the landing-zone
probe (write through a symlinked-parent spelling; observe where the file
lands) and run the pin under both `__main__` and pytest. Threshold: the
finding is wrong if the NT write lands INSIDE the guarded tree (the
residual exists on NT after all) or if pytest reports the pin's recorded
FAILURES as failures. Timeframe: probe runs in under a minute, any time.

**Validation kernel.** The residual on POSIX is real, disclosed, and
pinned with a RED-proven characterization test; the reinstated docstring
correctly warns against "fixing" the gate with realpath calls without a
fresh custody review. No matching-behavior change belongs in a freeze.

**Suggested fix.** Platform-gate the pin (skip unless POSIX) or assert
the platform-appropriate invariant per host; scope KL-GUARD-LEXICAL and
CLM-MC-GUARD-LEXICAL's statement to POSIX symlink resolution; make
`check()` raise (or register failures with pytest) so the suite cannot
silently pass under pytest.

### SHA-3 (P3) — R5(a)'s letter is unmet and is structurally unreachable within one freeze; the rc2 pins are guarded by zero automated layers until promotion

**Evidence.** Both rc2 pin tags exist on origin and peel correctly:
`pin/es-v6-rc2-candidate-2026-08-18^{}` → C, `pin/es-v6-rc2-freeze-…^{}`
→ C+1 [V live `git ls-remote`]. PINS at C+1 guards only
`pin/ecs-contract-2026-07-27` and `v4.0.0` — the rc2 pins are NOT
registered [V C+1 `check_pin_tags.py:23-30`]. The deferral is disclosed
with a digest-guard rationale: "a post-freeze PINS edit would trip the
digest guard by design" [V C+1 `docs/v6/ES6-V6-CANDIDATE/README.md:63-66`].
That rationale is structurally accurate: `check_pin_tags.py` IS an
inventoried, digest-bound file [V live: present in
`source-inventory.json` `file_digests`]. R5(a)'s falsifier demands PINS
registration "(or a recorded operator ruling forbids the tag, with an
alternative durable anchor recorded)". Neither limb holds: no PINS entry,
and no recorded operator ruling — a design-deferral note in an
implementer-authored README is not an operator ruling.

**The structural point (new).** Because a pin tag necessarily names the
freeze commit, and PINS lives inside the digest-sealed inventory, R5(a)'s
primary limb and R5(b)'s seal are mutually exclusive within ANY single
freeze under the current design: registering the pins post-freeze breaks
the seal; registering them pre-freeze is impossible (the commit does not
exist yet). The falsifier's alternative-anchor clause is therefore the
only reachable path — and it requires the operator-ruling record that
does not exist. Until promotion, tag reachability/deletion is detected by
nothing (layer count for the coordinate anchor: 1 — the origin tags
themselves — with 0 monitors).

**Falsifier.** Method: read PINS at the re-frozen tree; grep the
operator-decision record for a ruling classifying the rc2 pins'
registration timing; list origin tags and peel. Threshold: PINS contains
both rc2 pins with correct peeled SHAs, OR a durable operator-authored
ruling records the deferral AND names the interim anchor. Timeframe:
before operator acceptance; re-check before any PROMOTION_RUN.

**Validation kernel.** The tags exist, peel correctly, and the deferral
is disclosed with an accurate mechanism — this is a process-record gap,
not concealment, and the digest guard firing on a PINS edit is the R5(b)
repair working as designed.

**Suggested fix.** Operator records the registration-timing ruling in the
decision record (satisfying the falsifier's alternative clause), and PINS
registration lands as the first act of the promotion run; alternatively,
move the PINS registry outside the digest-sealed file set by design so
registration stops colliding with the seal.

### SHA-4 (P3) — Aggregate detector-credibility erosion across the freeze's self-check surfaces

**Evidence.** Three independent protection-layer detectors each cry wolf
on an entire environment class, all reproduced by this seat on first
contact: the digest seal red on every clean checkout (SHA-1); the R15 pin
red on privileged-NT `__main__` / silently green under pytest (SHA-2);
the skill-surface generator self-test failing rc=1 on privileged NT
(`(dst/"skills").symlink_to("plugins/epistemic-skills/skills")` without
`target_is_directory=True` [V C `.github/scripts/sync_skill_surfaces.py:524`]
creates a file-type symlink to a directory; the downstream `read_text`
on the alias then raises `PermissionError: [Errno 13]` [V live]) —
dossier FC-3 confirmed in substance, with the precise failure point one
step later than the dossier's line citation. Individually P3; the
aggregate is a pattern: a freeze whose self-checks fail on the first
non-Linux host that touches them teaches its audience that red means
environment, not defect — the exact habituation hazard H-C's layer
counting depends on NOT happening. The handoff's "run it yourself, trust
nothing stamped" posture (FC-4's prose limb) is the casualty: I ran it
myself, and three of the first three self-check surfaces failed.

**Falsifier.** Method: on a clean checkout of the re-frozen packet, run
the validator, the custody suite under both `__main__` and pytest, and
the sync self-test, on Linux AND privileged NT. Threshold: zero
unexplained reds on either platform (every red attributable to a real
planted mutation), and zero silent passes with recorded failures.
Timeframe: at the successor freeze.

**Validation kernel.** Every one of these detectors is fail-closed by
design and none can silently pass a real mutation on its gating surface
(Linux CI); KL-WINDOWS [V C+1 `promotion-packet.json`] discloses the
missing native-Windows requalification, so the platform class is not
concealed.

**Suggested fix.** Rides the re-freeze: SHA-1's tree-model fix, SHA-2's
platform gate + `check()` raise, `target_is_directory=True` (with the
alias-file fallback retained) at `sync_skill_surfaces.py:524`.

## Per-acceptance-criterion notes (R1–R15)

- **R1 (terminal gate):** discharged on mechanism. Schema @2 carries
  `independent_gauntlet_ref` with `gauntlet_run_id` / `verdict_path` /
  `subject_sha` and an `operator_acceptance` object [V C+1
  `promotion-packet.schema.json`]. Lens note: item 1 of the acceptance
  procedure correctly teaches the acceptor that a bare enum GO "is NOT
  this panel's verdict" [V C+1 `OPERATOR-ACCEPTANCE-PROCEDURE.md`] — but
  item 4 of the same procedure is unsatisfiable while SHA-1 stands. The
  gate has rejection power; the procedure it guards cannot currently be
  completed.
- **R2 (secret scan):** no lens-specific observation beyond H-B; the
  CLM-SECRET-SCAN row exists and the dossier's live run read is
  consistent with my layer count (3 layers on the confidentiality
  hazard).
- **R3 (merges):** discharged by D1 ratification per the dossier; nothing
  my lens adds — operator-authored consent is the only layer that counts
  here and it now exists.
- **R4 (SHA binding):** discharged. `exact_start_sha` = C [V C+1
  `source-inventory.json:3`]; tree hash matches C's tree [V C+1 line 4].
  The identity gap that decided the predecessor is closed by construction.
- **R5 (immutability):** PARTIAL, upheld. (b) present but fails closed on
  clean checkout (SHA-1); (a) letter unmet and structurally unreachable
  within one freeze (SHA-3); (c) KL-RESTAMP [V C+1
  `promotion-packet.json:67`] discloses the restamp class generically and
  claims "Any post-freeze edit to an inventoried file turns the validator
  red" while omitting that the validator is red on the UNMODIFIED sealed
  packet on any clean checkout — the disclosure names the true-positive
  direction and is silent on the standing false positive. (d): not
  probed by this seat (generator restamp-refusal), carried as known
  unknown.
- **R6 (tracker reconciliation):** discharged (path a). The generator's
  fail-closed disposition check exists [V C
  `v6_generate_candidate_packet.py:791-802`]. No lens-specific objection.
- **R7 (path coverage):** discharged (path a). `epistemic-flexibility.yml`
  carries no `paths:` filter with an in-tree comment citing R7 and the
  whole-tree-reader rationale [V C `epistemic-flexibility.yml:10-28`];
  the two workflows retaining `paths:` filters are not whole-tree
  readers.
- **R8 (ready-mark takeover):** mechanism discharged — all five gating
  workflows declare `ready_for_review` with comments citing R8 [V C,
  five workflow files, lines cited under H-D]. Lens caveat: the
  takeover's first effect on a fresh CI checkout is to run the red
  validator (SHA-1); the two repairs interact and must land together.
- **R9 (clean-room):** no independent re-execution by this seat beyond
  the dossier/crib; no lens-specific observation. Carried as
  source-supported.
- **R10 (main-red):** retired-by-live-state per the dossier's live read;
  not re-fetched by this seat. Known unknown (see below).
- **R11 (public-content gate):** discharged, and from this lens the
  strongest surface in the freeze. Gate green at C: 7 patterns, 37
  digest-verified exact-file entries, 1 dormant [V live]; owner + cadence
  recorded and the fail-closed digest semantics documented in-file [V C
  `check_public_content.py:60-69`]. The (d) residual (one dormant entry)
  is disclosed and digest-bound — it exempts nothing on this branch.
- **R12 (operator-alert channel):** mechanism discharged
  (`blocking_claims == ['CLM-INDEPENDENT-GAUNTLET']` [V live packet
  read]; derivation probe per dossier). No lens-specific objection.
- **R13 (acceptance procedure):** procedure exists and correctly scopes
  acceptance ("authorizes nothing beyond recording the state") [V C+1
  `OPERATOR-ACCEPTANCE-PROCEDURE.md`]. Lens note: its own item 4 is
  blocked by SHA-1 — the procedure is present but not yet walkable.
- **R14 (taxonomy/register):** not re-derived per-row by this seat;
  source-supported. No lens-specific observation.
- **R15 (custody residual):** discharged on its disclosure limbs — KL row
  + LIMITED matrix row + reinstated safe-direction docstring all verified
  [V C+1 `promotion-packet.json:74`; V C `custody_gate.py:85-104`] — WITH
  this lens's refinement: the residual is POSIX-only in fact (SHA-2's
  landing-zone probe), and the disclosure/pin should say so. The
  criterion's "no matching-behavior change in this freeze" constraint was
  honored; the fix belongs to the next contract epoch.

## Rival hypotheses

- **Most supported:** "the defect set is real but narrow and re-freeze
  class; the underlying guard/gate surfaces are healthy." The
  confidentiality and custody layers verified clean on their gating
  surfaces; everything material lives in the packet's self-check
  portability and process records.
- **Killed:** "the freeze's self-checks are portable proof — run them
  yourself" (the handoff's posture). Three of the first three self-check
  surfaces this seat ran failed on a non-Linux host (SHA-1, SHA-2, SHA-4);
  the packet cannot currently certify itself to anyone but its generating
  host.
- **Also killed:** any reading of the R15 residual as a live NT
  false-allow — the platform itself resolves the spelling the way the
  guard does (SHA-2).

## Minimum fix set

1. SHA-1: ignore-aware inventory walk in the generator; regenerate; keep
   the fail-closed seal and tree hash. (Re-freeze; decisive.)
2. SHA-2: platform-gate the R15 pin; scope KL-GUARD-LEXICAL /
   CLM-MC-GUARD-LEXICAL to POSIX; make the custody suite's `check()`
   failure-visible under pytest.
3. SHA-3: operator-authored ruling recording the PINS-registration
   timing (satisfies R5(a)'s alternative clause); registration as the
   first promotion act, or move PINS outside the sealed set.
4. SHA-4: `target_is_directory=True` at `sync_skill_surfaces.py:524`.

## Known unknowns

- R5(d) generator restamp-refusal probe: not executed by this seat.
- R10's live premise (main green at `03b7724`): adopted from the
  dossier's live read, not re-fetched; it decays with the next push to
  main and carries its own retirement clause.
- R9/R14 row-level accounting: source-supported, not independently
  re-derived (other lenses' scope).
- Whether any operator ruling on PINS timing exists out-of-band: no
  artifact in the C+1 tree records one; if one exists, SHA-3's falsifier
  alternative limb may already be satisfiable by citation.
- This seat's host is privileged-NT; the POSIX limbs of SHA-2 were
  verified by code read and the dossier's Linux-green crib, not by a
  POSIX re-run from this seat.
