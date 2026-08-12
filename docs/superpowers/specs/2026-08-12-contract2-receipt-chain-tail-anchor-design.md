# mission-custody contract@2 — receipt-hash chaining + tail anchor (es#118)

**Date:** 2026-08-12 · **Author:** claude-code steward session (operator grant: "proceed on
all of the open queue items") · **Issue:** es#118 · **Subsumes:** the reachable half of
es#124's second residue; the #117 forged-amendment-on-tail residue class (SECURITY.md)

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
   to `state` (notes / frontier / receipt_ids) and forged tail amendments (the #117
   guard-tamper residue) are invisible. es#124's remaining residue (phantom
   `RECONCILIATION` from an unattributable receipt id) is reachable **only** through
   tail-note corruption — same hole.

Constraint (verified in `verify_mission_custody.py`): @1 validation is exact-field
closure — unknown AND missing fields both rejected — so any new checkpoint field is a
breaking change. Existing live records: `media-library-rebuild` (r78+, zms-homelab),
the tracer record (vanta branch `mission/tracer-media-missing-record`), the enforce-armed
livefire scratch mission, plus any future mission.

## 2. Threat model (explicit, because the fix is partial by construction)

In scope (the attacker the design must beat): **a workspace-scoped writer** — an agent
session, subagent, or tool whose filesystem writes are confined to the workspace tree
(the common harness sandbox), tampering with mission records using ordinary file tools
instead of custody verbs. This includes the honest-confusion case (a session "fixing"
a checkpoint by hand).

Explicitly out of scope, disclosed rather than defended:
- A **user-account-scoped** attacker (can write both the workspace and the user home)
  defeats the tail anchor by deleting it before rewriting the tail (TOFU re-adopts).
- **Principal identity** — actor strings remain unverified (SECURITY.md already says so).
- **Receipt deletion asymmetry** for superseded receipts (SECURITY.md; unchanged).
- Signing / third-party-verifiable claims (future work; "hashed, not signed" stands).

## 3. Approaches considered

### Gap 1 — receipt integrity

- **(A) `receipt_ids` entries become `{request_id, receipt_sha256}` objects.**
  The sha of the receipt file's bytes is recorded by the same checkpoint that admits the
  id, so receipt content is covered by the chain the moment the admitting revision is
  sealed. One list, one truth. **Chosen.**
- (B) Parallel field (`receipt_shas` map). Same breaking cost (exact-field closure), two
  fields to keep consistent, one more invariant to defend. Rejected.
- (C) Receipts embedded whole in checkpoints. Kills the receipt-file model, bloats every
  checkpoint, worsens the known O(n²) growth. Rejected.

### Gap 2 — tail anchor

- **(A) User-level anchor file outside the workspace** at
  `~/.mission-custody/anchors/<sha256(resolved mission_dir)>.json`, holding
  `{mission_id, revision, checkpoint_sha256, updated_utc, adopted_utc}`. Updated after
  every checkpoint write; verified inside `load_latest`. Beats the in-scope attacker:
  a workspace-confined writer cannot touch the anchor, so any tail rewrite is detected
  at the next load. **Chosen.**
- (B) Sidecar HEAD file inside the mission dir. Forgeable by exactly the attacker that
  matters (same directory, same write access); raises the bar one file. Rejected as
  primary (subsumed by A).
- (C) Git commit as the off-box anchor (SAFETY-5 alignment). Right instinct, wrong
  layer: scratch missions aren't in git, live mission tails are routinely uncommitted,
  and custody must not take a dependency on repo state or push access. Kept as
  **operator practice** (commit mission dirs regularly; the git DAG then anchors every
  committed prefix), documented in README, not enforced in code.
- (D) Signed checkpoints. Key management and principal binding are their own project;
  out of @2 scope, listed in SECURITY.md as future work.

### Migration shape

- **(A) Epoch boundary inside one chain: append-only migration.** The chain keeps its
  @1 prefix byte-identical (SAFETY-7: the state being superseded is preserved); the
  first `checkpoint@2` record links to the last @1 checkpoint by the same
  `prev_checkpoint_sha256` rule. Chain rule: `1→1`, `1→2` (exactly once), `2→2` legal;
  `2→1` refused. **Chosen.**
- (B) Rewrite history to @2 (re-chain all revisions). Destroys byte-identity of the
  recorded past, invalidates every external reference to checkpoint hashes, and
  contradicts append-only custody. Rejected outright.

## 4. Design

### 4.1 Records

- New record kind **`checkpoint@2`**: identical to @1 except
  `receipt_ids: [{request_id: string, receipt_sha256: 64-hex}]`.
  `mission-manifest@1`, `receipt@1`, `acceptance-verdict@1` are unchanged.
  `acceptance-verdict@1.receipt_refs` stays a **string list of request ids** — writers
  extract ids from @2 entries.
- JSON schema file `checkpoint2.schema.json` + hand validator `validate_checkpoint2`
  (dispatch on `record`). Invalid-corpus examples for: string entries in a @2 list,
  object entries in a @1 list, missing/malformed sha, duplicate request_id in one list,
  epoch downgrade, unknown fields.

### 4.2 Store (custody_store)

- `write_checkpoint`: epoch rule enforced against the prior file's `record` kind
  (`2→1` refused; `1→2` allowed only when the new record carries the migration note —
  see 4.5 — so an ordinary write can never silently jump epochs).
- `load_latest`: after the existing per-link verification, **anchor verification**:
  - anchor file present and `(revision, sha)` == tail → verified.
  - anchor pins tail−1 and the pinned file's on-disk sha matches AND the tail links to
    it → **crash-window repair**: accept, advance the anchor, log to stderr. (The
    checkpoint-then-anchor write order makes a one-revision stale anchor the only
    legitimate crash state; the residual exposure — an attacker replacing the single
    newest checkpoint inside that window — is exactly the @1 status quo narrowed to
    one revision for the duration of a crash, and is disclosed.)
  - anchor behind by >1, ahead, or mismatched at its pinned revision → **refuse loudly**
    (`AnchorMismatch`, a `StoreError`): tamper or corruption; reconciling is an explicit
    operator/steward act (delete or re-adopt the anchor deliberately, never silently).
  - anchor absent → **TOFU-adopt** the current verified tail; record `adopted_utc` +
    adoption revision in the anchor file; stderr notice. Absence is visible in `status`.
  - root override `MISSION_CUSTODY_ANCHOR_ROOT` (tests; multi-user setups).
- Anchor updates happen in `write_checkpoint` after a successful publish; anchor repair
  happens on read. Anchor state never enters checkpoint records (it must not travel
  with the files it attests).
- Store exposes `anchor_state()` for `status`/CLI surfacing:
  `verified | adopted-now | repaired | absent-adopted-at:<utc> …`.

### 4.3 Receipt verification (custody_mission)

- Internal helper `_receipt_entries(checkpoint) -> list[tuple[request_id, sha|None]]`
  normalizes @1 (sha None) and @2 entries; every reader
  (`resume`, `continuity_breaks`, `_all_receipt_ids_ever`, `_historical_effect_path`,
  retirement, verdict `receipt_refs`) goes through it.
- `_load_receipt(request_id, expected_sha)`: when `expected_sha` is present and the file
  loads but its bytes hash differently → the receipt is **TAMPERED**, a new finding
  distinct from unloadable:
  - `resume` raises marker `RECEIPT-TAMPERED:<id>` (drift, reopens — same weight as
    RECEIPT-MISSING; the artifact it covered can no longer be trusted-verified).
  - Exit: `acknowledge-loss` handles both marker kinds. With a chained sha, "restored"
    becomes **byte-provable**: a file at the id's path hashing to the chained sha IS the
    original receipt (strictly stronger than @1's path-match heuristic, which remains
    the @1-era fallback for pre-migration ids whose sha is unknown).
- Regression test reproduces probe P6 (edit `after_sha256` in a receipt to match a
  tampered artifact) and asserts @2 catches it as RECEIPT-TAMPERED.

### 4.4 Writers

- `_write_next` receipt plumbing carries `(request_id, receipt_sha256)` (the sha is
  what `atomic_write_json` already returns from `write_receipt`).
- `record_effect` / `reconcile` append @2 entries; retirement removes entries by id.
- On a **pre-migration (@1) mission**, all writers keep producing @1 records — @2 code
  reads and writes @1 chains unchanged. Nothing forces migration.

### 4.5 Migration (`migrate` verb)

Preconditions, all hard: mission loads with verified manifest; `resume()` returns `[]`
(no drift — migration BLESSES current state, so current state must first be proven);
every id in current `receipt_ids` loads; not already @2. Then:

- Write the first `checkpoint@2`: same state/manifest, `receipt_ids` backfilled to
  `{id, sha256(current receipt file bytes)}`, machine note (new reserved prefix)
  `contract migrated: checkpoint@1->checkpoint@2; receipts backfilled: <n>` — the note
  makes the epoch boundary a recorded, chain-protected event, and `write_checkpoint`'s
  `1→2` rule requires it.
- Establish/refresh the anchor at the new tail.
- Honesty line in the note and README: backfilled shas attest receipts **as of
  migration time**; they cannot retroactively prove minting-time integrity. (Hence the
  clean-resume precondition: the record migrated is one that just passed every check
  @1 can perform.)

### 4.6 CLI

- `migrate` subcommand (workspace+actor only; prints the landed revision like every
  mutator).
- `status --brief` gains `record` (epoch) and `anchor` (state string).
- `resume`/`audit` stderr surfaces anchor repair/adoption events.
- Everything else unchanged.

### 4.7 Hook/gate

`custody_gate` and `custody_hook` read through `load_latest` and inherit anchor
verification automatically. Hook stays **fail-open LOUD** on `AnchorMismatch` (it is a
custody error like any tamper finding — enforcement must not brick the harness; the
block channel remains the deliberate exit-2 path). Gate CLI surfaces the anchor error
on stderr before failing open.

## 5. What @2 deliberately does not do

- No notes compaction / O(n²) fix (separate concern, harmless at current scale — the
  handoff's ~100 MB projection is an extrapolation ~7× beyond observed range).
- No signing, no principal binding, no receipt-deletion symmetry change.
- No forced migration of any existing mission; the tracer record stays @1 and readable.
- No anchor sync across devices (per-device TOFU; the chain itself is the cross-device
  truth, and adopting is loud).

## 6. Consumers and rollout (mixed-fleet hazard, same class as #117 guards)

Pre-@2 validators reject `checkpoint@2` records → `ChainBroken` → mission skipped as
unreadable → **discovery could then permit a duplicate `open`**. Therefore: deploy @2
code to every custody consumer BEFORE migrating any shared mission. On this device both
harnesses read the Claude plugin cache path (verified in the stage-c handoff). Order:
merge → deploy cache (hash-verified) → migrate `livefire` scratch (pilot) → UAT tamper
probes → migrate `media-library-rebuild` → re-run resume/audit/status → receipts into
the mission. The vanta tracer record is not migrated (closed record, branch-archived).

## 7. Test plan

Existing 7 suites stay green unmodified (@1 behavior preserved) except where they
assert exhaustive record-kind sets. New coverage:

- validator: @2 field/shape matrix + invalid corpus (≥7 new examples).
- store: epoch transition rules (1→1, 1→2-with-note, 2→2, refuse 2→1, refuse 1→2
  without migration note); anchor lifecycle (adopt, verify, crash-window repair,
  behind->refuse, ahead->refuse, mismatch->refuse, absent->adopt-loudly); anchor root
  override.
- mission: P6 regression (receipt edit caught); RECEIPT-TAMPERED lifecycle through
  acknowledge-loss (restore-by-hash + retire paths); mixed-chain readers
  (continuity_breaks / _historical_effect_path across the 1→2 boundary); verdict
  receipt_refs extraction on @2; migration preconditions (refuse on drift, on
  unloadable receipt, on already-@2) and success shape.
- gate/hook: unchanged behavior on @2 missions; fail-open-loud on AnchorMismatch.
- process-proof suite: byte-identical chain guarantee holds for @2 reads.

## 8. Review plan

Independent design review BEFORE implementation (adversarial + correctness/compat +
framing lenses — the #117 Critical was a plan-level flaw both reviewers found in
design, not code). Post-implementation: fresh-agent code review + adversarial PoC
review with live repros, fix rounds re-reviewed, mechanical merge gate, then the
rollout order in §6.
