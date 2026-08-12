# mission-custody contract@2 — receipt-hash chaining + tail anchor (es#118)

**Date:** 2026-08-12 · **Author:** claude-code steward session (operator grant: "proceed on
all of the open queue items") · **Issue:** es#118 · **Subsumes:** the reachable half of
es#124's second residue; the #117 forged-amendment-on-tail residue class (SECURITY.md)
· **Rev 2** after a three-lens pre-implementation design review (adversarial / correctness /
framing) — see §10 for what the review changed and why the shape survived.

## 1. Problem

Two integrity gaps in mission-custody@1 are schema-shaped (probe-verified in the
2026-08-12 manifest-efficacy evaluation, receipted into `media-library-rebuild`):

1. **Receipts are unchained.** Checkpoints carry receipt `request_id`s only. The drift
   oracle (`resume`) compares live artifacts against `after_sha256` read from receipt
   files whose integrity nothing attests. Editing one receipt file makes `resume` bless
   a tampered artifact (probe P6). The one runtime teeth custody has is defeatable by a
   single-file edit.
2. **The tail checkpoint is anchored by nothing.** `load_latest` re-verifies every
   interior link, but no successor references the newest checkpoint's hash. Tail edits
   to `state` and forged tail amendments (the #117 guard-tamper residue) are invisible.
   es#124's remaining residue (phantom `RECONCILIATION` from an unattributable receipt
   id) is reachable **only** through tail corruption — same hole.

Constraint (verified in `verify_mission_custody.py`): @1 validation is exact-field
closure — unknown AND missing fields both rejected — so any new checkpoint field is a
breaking change. Existing live records: `media-library-rebuild` (r80+, zms-homelab),
the enforce-armed `livefire` scratch mission, the archived tracer record (vanta branch,
will NOT be migrated), plus any future mission.

## 2. Threat model (explicit, because the fix is partial by construction)

In scope (the attacker the design must beat): **a workspace-scoped writer** — an agent
session, subagent, or tool whose filesystem writes are confined to the workspace tree,
tampering with mission records using ordinary file tools instead of custody verbs. This
is the historically observed class: probe P6 and the 11 predecessor defects were all
workspace-scoped probes or honest-confusion sessions. The attacker can **append** a
well-formed checkpoint as readily as edit one in place — `prev_checkpoint_sha256` is
computable from the readable tail — and this design must beat the append vector, which
is the one the first review draft missed.

Explicitly out of scope, disclosed rather than defended:
- A **user-account-scoped** attacker (can write both the workspace and the user home)
  defeats the anchor by deleting it before rewriting the tail (TOFU re-adopts). **On this
  fleet the primary interactive session is typically in this class** — its scratchpad and
  config live under the user home — so the anchor's teeth concentrate on subagents,
  probes, and honest confusion, and against a malicious primary session the only defense
  is the *loudness* of TOFU adoption (recorded `adopted_utc` + adoption revision, surfaced
  in `status` and to the acceptor), not the anchor's placement.
- **Principal identity** — actor strings remain unverified (SECURITY.md already says so).
- **Receipt deletion asymmetry** for superseded receipts (SECURITY.md; unchanged).
- Signing / third-party-verifiable claims (future work; "hashed, not signed" stands).

## 3. Approaches considered

### Gap 1 — receipt integrity

- **(A) `receipt_ids` entries become `{request_id, receipt_sha256}` objects.** The sha of
  the receipt file's bytes is recorded by the same checkpoint that admits the id, so
  receipt content is covered by the chain the moment the admitting revision is sealed by
  a successor. One list, one truth. **Chosen.**
- (B) Parallel field. Same breaking cost, two fields to keep consistent. Rejected.
- (C) Receipts embedded whole in checkpoints. Kills the receipt-file model, worsens the
  known O(n²) growth. Rejected.

### Gap 2 — tail anchor

- **(A) User-level anchor file outside the workspace**, verified on load, but with **no
  automatic advance** (see §4.2 — the review-driven change). A workspace-confined writer
  cannot touch it, so any tail rewrite OR append leaves the anchor not matching the tail,
  and the mismatch is surfaced (reads) or refused (writes) until an explicit human
  `anchor-repair` inspects the delta. **Chosen.**
- (B) Sidecar HEAD file inside the mission dir. Forgeable by exactly the in-scope attacker
  (same dir, same write access), and it rides the sync/commit flows it attests. Rejected.
- (C) Git commit as the off-box anchor (SAFETY-5). Right instinct, wrong layer: scratch
  missions aren't in git, live tails are routinely uncommitted, and custody must not
  depend on repo/push state. Kept as **operator practice** (commit mission dirs; the git
  DAG then anchors every committed prefix), documented, not enforced in code.
- (D) Signed checkpoints. Key management + principal binding are their own project; out of
  @2 scope, listed as future work in SECURITY.md.

### Null option (framing-lens steelman, rejected on evidence)

Ship **only** receipt-hash chaining, defer the anchor. Rejected: receipt shas admitted on
the tail are editable without the anchor, so a two-file edit (tail entry's `receipt_sha256`
+ the receipt's `after_sha256`) restores the full P6 defeat for exactly the receipts under
active work — the ones `resume` consults most. The two halves are load-bearing together.

### Migration shape

- **(A) Append-only epoch boundary inside one chain.** The @1 prefix stays byte-identical
  (SAFETY-7: the superseded state is preserved; external references to checkpoint hashes
  stay valid); the first `checkpoint@2` links to the last @1 checkpoint by the same
  `prev_checkpoint_sha256` rule. **Chosen.**
- (B) Rewrite history to @2. Destroys byte-identity of the past and contradicts
  append-only custody. Rejected outright.

## 4. Design

### 4.1 Records

- New record kind **`checkpoint@2`**: identical to @1 except
  `receipt_ids: [{request_id: string, receipt_sha256: 64-hex}]` (each `request_id` unique
  within the list). `mission-manifest@1`, `receipt@1`, `acceptance-verdict@1` unchanged;
  `acceptance-verdict@1.receipt_refs` stays a **string list of request ids**.
- JSON schema `checkpoint2.schema.json` + hand validator `validate_checkpoint2`.
- **Forward-compat, bought now (@2 is the last cheap moment):** the validator recognizes
  the shape `^checkpoint@(\d+)$`. A kind whose epoch is **greater than the highest this
  build knows** returns a distinct `EPOCH-TOO-NEW` error, NOT generic "unknown kind".
  Invalid corpus (≥8 examples): string entry in a @2 list, object entry in a @1 list,
  missing/malformed `receipt_sha256`, duplicate `request_id` in one list, epoch downgrade
  in a chain, second 1→2 boundary, a `checkpoint@3` (must classify as EPOCH-TOO-NEW, not
  unknown), unknown field in a @2 record.

### 4.2 Store (custody_store) — chain + anchor

**Epoch monotonicity is enforced on the READ path** (`load_latest`), not only on write,
because the in-scope attacker writes raw files and never calls `write_checkpoint`:

- A record whose epoch is **lower** than any earlier record in the chain → `ChainBroken`.
- **More than one** 1→2 transition in a chain → `ChainBroken`.
- The transition is judged by **record kind only**, never by a note string (mutable,
  attacker-writable). The migration note (§4.5) is belt-and-suspenders at the write path.
- A record classifying as `EPOCH-TOO-NEW` → surfaced as a distinct `EpochTooNew`
  (a `StoreError` subclass) so discovery can treat it as **present-but-unreadable**, not
  as a corrupt sibling to skip (see §4.8).

**Anchor** lives at `<anchor-root>/anchors/<mission-key>.json` holding
`{mission_id, revision, checkpoint_sha256, adopted_utc, adoption_revision, updated_utc}`.
Default anchor-root is `~/.mission-custody/`.

- **Anchor engages only for @2 tails.** A mission whose tail is `checkpoint@1` has no
  anchor and needs none — @1 missions load exactly as today, un-migrated and unbricked.
- **`mission-key`** = `sha256(canonical_mission_identity)`. Canonicalization (§4.2a) makes
  the key stable across the honest path-spellings this fleet produces.
- **Verification outcomes on load of a @2 tail (NO auto-advance):**
  - anchor present, `(revision, sha)` == tail → **verified**.
  - anchor present, pins an **ancestor** of the current fully-verified chain (revision <
    tail, pinned file's on-disk sha still matches the anchor, chain links pinned→tail) →
    **lagging** (the legitimate-crash shape OR a forged append — indistinguishable at the
    byte level, so not auto-trusted): reads SUCCEED but flag loudly
    (`anchor_state="lagging-unrepaired"`), writes REFUSE (see below). The anchor is **not**
    advanced by any read.
  - anchor present, pins a revision whose on-disk sha ≠ the anchor's recorded sha, or
    ahead of the tail, or not an ancestor → **`AnchorMismatch`** (refuse loudly).
  - anchor present but unparseable / shape-invalid → **`AnchorMismatch`** (refuse loudly).
    Corruption must NEVER alias to "absent"; absence is the one state a workspace attacker
    cannot fabricate, and corruption must not imitate it.
  - anchor absent → **TOFU-adopt** the current fully-verified tail, LOUDLY: record
    `adopted_utc` + `adoption_revision`, stderr notice, `anchor_state="adopted-at-rN"`.
    Before adopting, run the **mission_id secondary scan**: if another anchor file carries
    the same `mission_id`, this is path-aliasing / relocation, NOT a fresh device →
    refuse (`AnchorMismatch`, "split anchor: run anchor-repair"), never mint a parallel
    anchor. Legitimate first-contact on a new device has no same-id anchor and adopts.
- **Write path:** a write verb requires **`verified`**. Any other state (`lagging`,
  mismatch, absent-multi-revision) → the verb REFUSES with a pointer to `anchor-repair` /
  `anchor-adopt`. This is the invariant that closes the append attack: **no new work ever
  builds on an unverified tail.** (A legitimate crash therefore costs one `anchor-repair`
  before the next write — rare, since the crash window is milliseconds in-process, and
  high-signal.)
- **Anchor advance happens only** in `write_checkpoint` after a successful publish, as an
  **advance-only CAS** (read current anchor; write only if `(revision, sha)` strictly
  advances; exclusive-publish like `_publish_exclusive`). A lost/failed anchor update
  after a successful checkpoint publish is **stderr-warned and the verb still succeeds**
  (`anchor_state="anchor-writes-failing"` surfaces it) — a mission never fails a real
  write because the anchor couldn't be persisted, and it is never silently unprotected
  either.
- **Anchor writes on the READ path** (TOFU-adopt) are best-effort: failure is stderr-loud,
  the read succeeds, `anchor_state="unpersisted"`. Read-only surfaces stay read-only for
  the *mission* dir; only the user-home anchor may be touched, and never fatally.
- `anchor_state()` returns the state string for `status`/CLI:
  `verified | adopted-at-rN | lagging-unrepaired | anchor-writes-failing | unpersisted |
  root-overridden:<path>`.

#### 4.2a Anchor identity (Windows-stable)

`canonical_mission_identity` = `normcase(realpath(mission_dir))` with: `\\?\` prefix
stripped; ASCII-only casefold (reusing `_ascii_case_fold` — NOT `str.casefold`, same NTFS
reasoning as the drift keys); best-effort drive-letter→UNC canonicalization with a **fixed
fallback order** (try `GetFinalPathNameByHandle`; on failure keep the normalized
drive-letter spelling deterministically). The mission_id secondary scan above is the
safety net for any residual split.

#### 4.2b Anchor root (no ambient-env provenance seam)

The trust root is configurable **only** via an explicit `--anchor-root` CLI flag (for
tests and documented multi-user setups). There is **no** `MISSION_CUSTODY_ANCHOR_ROOT`
environment variable — ambient environment must never set the trust boundary that
authorizes "verified" (CONFIDENTIALITY-2). The flag:
- refuses any root that resolves **inside the workspace tree** (containment check
  mirroring `_resolve_artifact_path`);
- is **not exposed** by the hook/gate entry points — enforcement surfaces always use the
  default user-home root;
- when non-default, every surface prints the effective root
  (`anchor_state="root-overridden:<path>"`).

### 4.3 Receipt verification (custody_mission)

- **Single chokepoint** `_receipt_entries(checkpoint) -> list[(request_id, sha|None)]`
  normalizes @1 (sha `None`) and @2 entries. **Every** consumer routes through it; the
  test suite includes a **grep-guard** forbidding raw `["receipt_ids"]` indexing or
  membership outside the chokepoint and the two writers. Enumerated consumers (all must
  change): `resume`, `continuity_breaks`, `_all_receipt_ids_ever`,
  `_historical_effect_path`, `_retired_receipt_ids` callers, `reconcile`'s membership test,
  `acknowledge_receipt_loss`'s retirement filter, `record_effect`'s reuse checks, verdict
  `receipt_refs` extraction, the CLI clean-resume `len(set(...))`, and `_write_next`'s
  copy-forward/append.
- **sha resolution is latest-attestation-wins:** admission ORDER is first-occurrence (for
  chain ordering), but the effective `expected_sha` for an id is the sha from the **latest
  checkpoint that lists it** (chain-protected when interior). A silent `None` fallback when
  a sha exists elsewhere in the chain is forbidden — that is a false-clean. A pre-migration
  id whose only admitting entry lacked a sha resolves to `None` and is verified at
  **@1-strength**, surfaced explicitly, never marketed as covered.
- `_load_receipt(request_id, expected_sha)`: when `expected_sha` is present and the file
  loads but hashes differently → **`RECEIPT-TAMPERED:<id>`**, a drift finding distinct from
  unloadable, same weight (reopens). Exit: `acknowledge-loss` handles both marker kinds;
  with a chained sha, "restored" is **byte-provable** (a file at the id's path hashing to
  the chained sha IS the original) — strictly stronger than @1's path-match heuristic,
  which remains the fallback for `None`-sha ids.
- Regression test: reproduce P6 (edit `after_sha256` to match a tampered artifact) on a
  @2 mission and assert `RECEIPT-TAMPERED`; and tamper a **superseded** pre-migration
  receipt after migration and assert `audit` reports it (latest-attestation-wins in
  action), rather than consuming the forged hashes.

### 4.4 Writers

- `write_receipt` returns `(path, sha256_of_bytes)` (today it returns only the Path and
  discards the sha `atomic_write_json` computed).
- `_write_next` receipt plumbing carries `(request_id, receipt_sha256)`.
- `record_effect` / `reconcile` append @2 entries; retirement removes entries **by id**
  (the filter must compare against `request_id`, not against the whole dict).
- On a **pre-migration (@1) mission**, all writers keep producing @1 records unchanged.

### 4.5 Migration (`migrate` verb) — does NOT bless

Preconditions, all hard (migration attests receipt **bytes as of migration time**; it
cannot upgrade minting-time integrity, and it must not launder a P6 edit that `resume`
alone cannot see):

1. **Operator consent recorded** — a prior amendment authorizing the epoch migration
   (`amend --text "<operator grant>"`), since the epoch change is consequential and
   irreversible (2→1 is refused). CONSENT-1.
2. `resume()` returns `[]` (no drift) **AND** `continuity_breaks()` has no *unreconciled*
   entries — a P6 edit with a successor receipt on the same path is audit-visible today,
   and migrating over it would launder that evidence into chain-attested state.
3. Every id in the current `receipt_ids` loads, **and** each receipt's `artifact_path`
   agrees with the chain's recorded effect path where derivable (the check
   `acknowledge_receipt_loss` already performs) — a path-forged receipt passes `resume`
   but must not get its forgery chain-blessed.
4. Not already @2.

The drift check in precondition 2 uses a **non-mutating** probe (it must not side-effect a
`reopened` checkpoint on a refused migrate). Then:

- Write the first `checkpoint@2`: same state/manifest, `receipt_ids` backfilled to
  `{id, sha256(current receipt file bytes)}`, notes extended by exactly one new machine
  note with reserved prefix `contract migrated: ` recording `checkpoint@1->checkpoint@2;
  receipts backfilled: <n>`. `write_checkpoint`'s 1→2 rule requires: prev kind == @1, new
  kind == @2, and `notes == prev_notes + [migration note]`.
- Establish/refresh the anchor at the new @2 tail.
- Honesty line in the note and README: backfilled shas attest receipts **as of migration
  time only** and inherit **every** @1 blind spot (P6 included); they do not prove
  minting-time integrity. "receipts now chained" ≠ "backfilled receipts now trustworthy".

### 4.6 CLI

- `migrate`, `anchor-repair`, `anchor-adopt` subcommands (workspace+actor; each prints the
  landed revision / adopted revision like every mutator). `--anchor-root` is a global flag
  on the CLI only (§4.2b).
- **`anchor-repair`**: for a `lagging` anchor, prove the pinned `(revision, sha)` is an
  ancestor of the current fully-verified chain, **print the full appended-revision delta**
  (per revision: amendments added, guard changes, receipt admissions, status transitions,
  frontier change), then advance the anchor. A legitimate crash prints the steward's own
  last checkpoint; a forged append prints the attacker's forged amendment/guard change —
  the human sees exactly what they are being asked to adopt before it is trusted.
- **`anchor-adopt`**: the explicit exit for `AnchorMismatch` / split-anchor states — prints
  the current verified tail and adopts it deliberately (never silent).
- `status --brief` gains `record` (epoch) and `anchor` (state string incl. `adopted_utc` +
  `adoption_revision`, so an acceptor sees whether continuous anchoring spans the mission).
- `resume`/`audit` stderr surfaces anchor lagging/adoption/failure events.

### 4.7 Hook/gate — real teeth on enforce, honest about audit

`custody_gate` and `custody_hook` read through `load_latest` and inherit anchor
verification. Behavior on a discovered mission:

- **Hook-internal errors** (crash, timeout, unreadable payload) → fail open LOUD (unchanged;
  a broken hook must not brick the harness).
- **Detected `AnchorMismatch` / `lagging` on an ENFORCE-armed mission** → **BLOCK** (exit 2,
  "custody tail integrity failed; refusing to authorize the actuator"). This is the whole
  point of enforce: a tampered/uncertain tail on an armed mission is exactly when the guard
  must fire pre-execution. Blocking on uncertainty is the safe direction (SAFETY).
- **Detected `AnchorMismatch` / `lagging` on an AUDIT mission** → append a distinguishable
  `degraded-anchor` guard-log entry and ALLOW (audit observes, never blocks).
- Either way, the next `status`/`resume`/`audit` REFUSES (via `load_latest`), so tamper
  cannot stay quiet past the next custody verb.

SECURITY.md states plainly: on an audit mission the anchor is detection-only; on an enforce
mission it blocks. "Inherits anchor verification" does not silently read as "the gate now
blocks tamper on every mission".

### 4.8 Discovery (`Mission.load`)

- `EpochTooNew` from a sibling is treated as **present-but-unreadable**, distinct from a
  skipped corrupt sibling: `open` REFUSES ("a mission exists here this build is too old to
  read"), and the gate returns its degraded-loud path (+ guard-log entry), never plain
  inert — so a future-epoch checkpoint can never silently disarm an armed mission or admit
  a duplicate `open`.
- A false `AnchorMismatch` must not silently reroute discovery: `AnchorMismatch` on the
  single active mission propagates as a loud refusal from the invoked verb, it does not
  get swallowed into `NoActiveMission` (which would permit a duplicate `open`). The
  discovery loop only skips genuinely unreadable-corrupt siblings.

## 5. What @2 deliberately does not do

- No notes compaction / O(n²) fix (separate concern, harmless at current scale).
- No signing, no principal binding, no receipt-deletion symmetry change.
- No forced migration; `Mission.open` keeps emitting **checkpoint@1 for one release
  window** so `migrate` is the sole @1→@2 entry (one boundary shape, existing suites keep
  their meaning). Flipping `open` to @2 is a later, separately-recorded decision gated on a
  verified fleet deploy.
- No anchor sync across devices (per-device TOFU; the chain is the cross-device truth, and
  adoption is loud + recorded).

## 6. Consumers and rollout (mixed-fleet hazard)

Pre-@2 validators reject `checkpoint@2` → `ChainBroken` → mission skipped → could permit a
duplicate `open`. Deploy @2 code to every custody consumer BEFORE migrating any shared
mission. Order: merge → deploy cache (**re-verify at migrate time** that both harnesses
load the same custody file bytes — hash them, do not inherit the stage-c handoff's claim,
per committed≠deployed) → migrate `livefire` scratch (pilot) → UAT tamper probes
(append-forge, in-place-edit, receipt P6, split-path, corrupt-anchor, enforce-block) →
migrate `media-library-rebuild` (operator-consented) → re-run resume/audit/status →
receipts into the mission. The vanta tracer record stays @1 (archived).

## 7. Test plan

Existing suites stay green with **two sanctioned modifications**, not "unmodified":
(i) a conftest-level `--anchor-root` injection into every subprocess so tests never write
into the real `~/.mission-custody` (on this device, the sacred C:); (ii) tamper-assertion
tests whose error KIND legitimately changes (e.g. a tail-tamper that now surfaces as
`AnchorMismatch` before the @1 `CustodyError`) are updated **deliberately**, enumerated in
the plan, not reactively during fix rounds. New coverage:

- validator: @2 field/shape matrix; invalid corpus (≥8); `checkpoint@3` → EPOCH-TOO-NEW.
- store: epoch read-path monotonicity (reject 2→1 append, reject double 1→2); anchor state
  machine (verified / lagging→read-flag+write-refuse / mismatch→refuse / ahead→refuse /
  corrupt→refuse / absent→loud-TOFU / same-id-scan→refuse); advance-only CAS; two-session
  ping-pong with a suspended writer (no false mismatch after next write); anchor-write
  failure warns-and-succeeds; `--anchor-root` inside workspace refused; hook ignores root.
- mission: P6 regression; RECEIPT-TAMPERED lifecycle through acknowledge-loss
  (restore-by-hash + retire); latest-attestation-wins on a superseded pre-migration
  receipt; mixed-chain readers across the 1→2 boundary; verdict receipt_refs on @2;
  migration preconditions (refuse on drift, on unreconciled break, on path-mismatch, on
  missing operator consent, on already-@2; non-mutating drift probe) and success shape;
  the CLI clean-resume path on a migrated mission (no `TypeError`).
- gate/hook: enforce-mission AnchorMismatch BLOCKS (exit 2); audit-mission logs+allows;
  hook-internal error fails open loud; EpochTooNew degraded path.
- discovery: EpochTooNew sibling refuses `open`; AnchorMismatch on active mission does not
  become NoActiveMission.
- process-proof: byte-identical @1 prefix under @2 reads.
- Windows path aliasing: load one mission via two spellings; assert stable mission-key.

## 8. Path-spelling & Windows hazards (this fleet)

`Y:\dev` is mapped to `\\10.10.10.127`; NTFS is case-insensitive; claude runs MSYS2 and
kimi does not. The anchor identity function (§4.2a) + mission_id secondary scan exist
specifically for this. `os.replace` onto a file another process holds open can raise
`PermissionError` on Windows — anchor CAS uses exclusive-publish and never fails the verb.

## 9. Review plan

Independent design review ran **before** implementation (this rev incorporates it — §10).
Post-implementation: fresh-agent code review + adversarial PoC review with live repros
(the append-forge, epoch-downgrade, migration-launder, split-anchor, and enforce-block
attacks specifically re-run against the built code), fix rounds re-reviewed (a fix is a
change and needs the same gate), mechanical merge gate, then the §6 rollout.

## 10. What the pre-implementation review changed (rev 1 → rev 2)

A three-lens panel (adversarial / correctness / framing) reviewed rev 1. All three
returned **proceed-with-changes** and all three **independently** found the same CRITICAL:
the rev-1 crash-window **auto-repair** blessed a forged tail **append** (not just an
in-place edit) and advanced the anchor onto it — unbounded forgery, carrying the exact
forged-amendment+guard-change #118 exists to close. The shape (receipt-sha inline +
off-box anchor + append-only epoch) survived unanimously; these decisions did not, and are
now changed above:

1. **Auto-advance deleted.** Anchor verification is verified / loud-TOFU-at-absent /
   else-refuse, with explicit `anchor-repair`/`anchor-adopt` verbs; reads flag a lagging
   anchor, writes refuse it (§4.2, §4.6). Closes the append attack and makes the #117
   forged-amendment subsumption actually true.
2. **Epoch monotonicity on the READ path** (§4.2), keyed on record kind, plus forward-compat
   `EpochTooNew` so @2 does not reproduce the flaw for @3 (§4.1, §4.8).
3. **Migration does not bless** (§4.5): operator-consent gate + continuity-clean +
   path-agreement preconditions, non-mutating drift probe, explicit "as-of-migration only"
   disclosure.
4. **Windows-stable anchor identity** + mission_id secondary scan (§4.2a) — the rev-1
   path-only key split on this fleet's Y:/UNC/case spellings, causing both false alarms and
   silent TOFU resets.
5. **Ambient-env provenance seam removed** (§4.2b): `--anchor-root` flag only, refused
   inside the workspace, hidden from enforcement entry points.
6. **_receipt_entries as an enforced chokepoint** with a grep-guard test and
   latest-attestation-wins sha (§4.3) — four rev-1-latent code landmines (CLI `set()`
   TypeError, acknowledge-loss filter no-op, `_all_receipt_ids_ever` dict-hash,
   `reconcile` membership) are exactly the predecessor's probe-found defect class.
7. **Anchor teeth on enforce, honesty on audit** (§4.7); anchor-write failure fails
   loud-not-silent (§4.2); corrupt anchor → refuse, never absent (§4.2).

The most valuable review outcome, per this project's own history, was the **argument that
the rev-1 residue disclosure was factually wrong** — "the @1 status quo narrowed to one
revision for the duration of a crash" was disproven three times over, because the attacker
constructs the crash-window state on demand and repair chained it unbounded. That single
correction is why this is a design revision, not an implementation note.
