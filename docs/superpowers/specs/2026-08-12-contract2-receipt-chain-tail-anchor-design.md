# mission-custody contract@2 — receipt-hash chaining + tail anchor (es#118)

**Date:** 2026-08-12 · **Author:** claude-code steward session (operator grant: "proceed on
all of the open queue items") · **Issue:** es#118 · **Subsumes:** the reachable half of
es#124's second residue; the #117 forged-amendment-on-tail residue class (SECURITY.md)
· **Rev 4** — three independent review rounds before any implementation: a three-lens panel
(§10.1), a focused adversarial re-check (§10.2), and a fresh convergence check by a
different reviewer (§10.3). Every round found real defects, and **three of them were holes
created by the previous round's own fixes** — which is why each round is gated by a fresh
adversary rather than a re-read. Every claim in §10.2 and §10.3 was independently
re-verified against the source before being acted on (citations inline). The architecture
— receipt-sha inline, off-box anchor, append-only epoch, gate inside `write_checkpoint` —
has now held unchanged across two fresh adversaries; §10.3's verdict is **converged**.

## 1. Problem

Two integrity gaps in mission-custody@1 are schema-shaped (probe-verified in the
2026-08-12 manifest-efficacy evaluation, receipted into `media-library-rebuild`):

1. **Receipts are unchained.** Checkpoints carry receipt `request_id`s only. `resume`
   compares live artifacts against `after_sha256` read from receipt files whose integrity
   nothing attests, so editing one receipt file makes `resume` bless a tampered artifact
   (probe P6). The one runtime teeth custody has is defeatable by a single-file edit.
2. **The tail checkpoint is anchored by nothing.** `load_latest` re-verifies every
   interior link, but no successor references the newest checkpoint's hash. Tail edits and
   forged tail amendments (the #117 guard-tamper residue) are invisible; es#124's residue
   is reachable only through the same hole.

A third gap, found during review and folded in because the fix is nearly free (§4.9):
**acceptance verdicts are entirely unchained** — `_store_verdict` writes
`verdicts/<rev>-<verdict>.json` with a plain `atomic_write_json`
(`custody_mission.py:502-504`) and the completing checkpoint's note is only
`f"PASS: {reason}"` (`custody_mission.py:903`), so **`acceptor_id` and `assurance_tier`
appear nowhere in the chain**. Under the Four-Layer Precedence, acceptance authority is
the rung that makes "done" defensible; today a workspace writer can edit a completed
mission's recorded acceptor and nothing detects it.

Constraint (verified in `verify_mission_custody.py`): @1 validation is exact-field
closure, so any new checkpoint field is a breaking change. Live records:
`media-library-rebuild` (r81+), the enforce-armed `livefire` scratch mission, the archived
tracer record (not migrated).

## 2. Threat model

In scope: **a workspace-scoped agent session, subagent, or tool** — it can write anywhere
in the workspace tree with ordinary file tools (so it can **append** a well-formed
checkpoint as easily as edit one: `prev_checkpoint_sha256` is computable from the readable
tail), it can **invoke processes** (including custody verbs) and **control their
environment**, and it cannot write the user home directly.

⚠ **That last clause is an ASSUMPTION with a named external dependency, not a property this
contract enforces.** Nothing in custody code prevents a user-home write; it rests entirely
on the harness permission control (this fleet's `safety_gate` hook) covering *every* write
path — including a spawned shell doing `echo x > ~/.mission-custody/anchors/...`. This fleet
found and fixed exactly that class of Bash bypass in its own safety gate within the last two
weeks, so the dependency is live, not hypothetical. Stating it as a flat attacker property
would be the same "writing a control is not installing one" error named below. If that
control does not cover shell writes, the anchor's off-box property degrades to the
user-account-scoped case already disclosed.

That last pair is load-bearing and rev 2 got it wrong. Process invocation means:
- the attacker can run `anchor-repair` and have the process write the anchor **on its
  behalf** (confused deputy) — so any control that says "a human inspects the delta" must
  be a *mechanism*, not an intention (this fleet's own recorded failure pattern: writing a
  control is not installing one);
- the attacker can set `USERPROFILE`/`HOME`, and `Path.home()` resolves through them.
  **Empirically verified on this device:** overriding `USERPROFILE` made `Path.home()`
  return the attacker-chosen path. Rev 2's claim that the ambient-env seam was "removed"
  was therefore false; §4.2b now mitigates instead of denying (see §10.2 D5).

Out of scope, disclosed rather than defended:
- A **user-account-scoped** attacker deletes the anchor and TOFU re-adopts. **On this
  fleet the primary interactive session is typically in this class**, so the anchor's
  teeth concentrate on subagents, probes, and honest confusion; against a malicious
  primary session the defense is the *loudness and recorded-ness* of adoption, not
  placement.
- **Principal identity** — actor strings are unverified (SECURITY.md).
- **Superseded-receipt deletion asymmetry** (SECURITY.md; unchanged).
- Signing / third-party-verifiable claims (future work).

## 3. Approaches considered

**Gap 1 — receipt integrity. (A) `receipt_ids` entries become
`{request_id, receipt_sha256}`** — the sha is recorded by the checkpoint that admits the
id, so receipt content is chain-covered once that revision is sealed. One list, one truth.
**Chosen.** Rejected: a parallel field (same breaking cost, two things to keep consistent);
embedding receipts whole (kills the receipt-file model, worsens O(n²) growth).

**Gap 2 — tail anchor. (A) A user-level anchor outside the workspace**, gated inside the
store's write path, with **no automatic advance**. **Chosen.** Rejected: a sidecar HEAD
file in the mission dir (forgeable by exactly the in-scope attacker, and it rides the sync
flows it attests); git-commit-as-anchor (right instinct, wrong layer — scratch missions
aren't in git and tails are routinely uncommitted; kept as **operator practice**);
signed checkpoints (key management + principal binding are their own project).

**Null option** (receipt chaining only, defer the anchor) — steelmanned and rejected on
evidence: receipt shas admitted on the tail are editable without the anchor, so a two-file
edit restores the full P6 defeat for exactly the receipts under active work.

**Migration — (A) append-only epoch boundary inside one chain.** The @1 prefix stays
byte-identical (SAFETY-7; external hash references stay valid). Rejected: rewriting
history to @2 (destroys byte-identity of the past, contradicts append-only custody).

## 4. Design

### 4.1 Records

- **`checkpoint@2`**: identical to @1 except
  `receipt_ids: [{request_id, receipt_sha256}]`, `request_id` unique within the list.
  `mission-manifest@1`, `receipt@1`, `acceptance-verdict@1` unchanged.
- **`acceptance-verdict@1.receipt_refs` stays a string list.** This is deliberate, not an
  oversight: `record_verdict` copies `latest["receipt_ids"]` (`custody_mission.py:888`)
  and `_str_list` rejects dicts (`verify_mission_custody.py:331`); the writer extracts ids
  via the §4.3 chokepoint. **Do not "fix" this into an object list.**
- JSON schema `checkpoint2.schema.json` + `validate_checkpoint2`.
- **Forward-compat bought now** (@2 is the last cheap moment): the validator recognizes
  `^checkpoint@(\d+)$`; an epoch above the highest this build knows returns a distinct
  `EPOCH-TOO-NEW`, never generic "unknown kind".
- Invalid corpus (≥8): string entry in a @2 list, object entry in a @1 list,
  missing/malformed sha, duplicate `request_id`, epoch downgrade, second 1→2 boundary,
  `checkpoint@3` (must classify EPOCH-TOO-NEW), unknown field in @2.

### 4.2 Store — the anchor gate lives HERE, not at the verb layer

This placement is the single most important decision in the design, and it is a rev-3
correction. Rev 2 put the rule at the verb layer ("write verbs require verified"), which
forced a judgment call about which verbs are writes — and **`resume` is a writer**
(`custody_mission.py:740` calls `_write_next` on drift; `custody_cli.py:246` exposes it as
the standard post-interruption verb). Classified as a read, it laundered the whole attack:
attacker appends forged rN+1 → anchor lags → steward runs `resume` after an interruption
(the ritual the skill prescribes) → resume writes rN+2 **chained onto the forgery** → CAS
advances the anchor onto it → `anchor-repair`'s delta print never runs and the human never
sees the forged amendment.

**Therefore: `MissionStore.write_checkpoint` evaluates the anchor gate itself, against the
same bytes it uses to compute `prior_sha`** (`custody_store.py:115`). This closes three
holes: no verb can be miscategorized; the verify-then-write race (§10.2 E1) cannot open,
because the write is justified by the same read that approved it; and a *forged* tail
cannot declare its own guard mode (an *unforged* one still can via the sanctioned `amend`
path — §4.7 residue). It does **not** by itself make the enforce gate evaluate correctly
after an honest crash — rev 3 claimed that and it was false; §4.7's strictest-of rule is
what delivers it.

**Revision 1 is exempt.** At `Mission.open` no chain exists, so there is no tail to verify
and no anchor to check; the anchor is minted by the post-publish advance. (The @1 code
already structures this correctly — the `prior_sha` comparison lives inside the
`else:` of `if revision == 1`, `custody_store.py:111` — but a literal reading of the state
list below would call `load_latest()` on an empty chain and make opening a mission
impossible, so the exemption is stated rather than left to be rediscovered.)

**An anchor present over an EMPTY chain refuses at open**, naming `anchor-adopt`. Reachable
without an attacker: delete a mission dir and reopen the same mission-id at the same path
(§4.2a keys on path, so the key is unchanged); discovery skips checkpoint-less dirs
(`custody_mission.py:211-212`) so `open` would succeed at r1, and then the advance-only CAS
refuses to regress the anchor — wedging the mission permanently at its first r2 write.

**Anchor file** `<anchor-root>/anchors/<mission-key>.json`:
`{mission_id, revision, checkpoint_sha256, resolved_root, adopted_utc, adoption_revision,
updated_utc}`.

**Engagement is keyed on anchor PRESENCE, never on the tail's epoch.** Rev 2 said "the
anchor engages only for @2 tails", which handed the attacker a whole-chain rewrite: rewrite
r1..rN as valid @1 records with recomputed links (nothing is signed), and the chain has *no
epoch transition at all*, so read-path monotonicity has nothing to fire on and the anchor
is never consulted — receipt-sha coverage stripped wholesale, no alarm. Under rev 3, an
anchor that exists is verified whatever the tail's epoch (a @1 tail matching nothing the
anchor pins → `AnchorMismatch`). A genuinely un-migrated @1 mission has no anchor, mints
none, and stays exactly as unbricked as before.

**States** (evaluated on load AND inside `write_checkpoint`):
- `(revision, sha)` == tail → **verified**.
- anchor pins an **ancestor** of the fully-verified chain → **lagging**: reads succeed
  with a loud flag; **all writes refuse** (including `resume`'s drift write). Nothing
  advances the anchor.
- pinned sha not found on disk, pinned file's sha differs, anchor ahead, not an ancestor,
  or **unparseable/shape-invalid** → **`AnchorMismatch`** (refuse loudly). Corruption and
  a missing pinned file MUST NOT alias to "absent" — absence is the one state the in-scope
  attacker cannot fabricate **at a given root**. Under §4.2b's env-redirect absence is
  trivially fabricable at the *attacker's* root, and absence→TOFU is the most permissive
  state; the two clauses are in tension by construction and must be read together. What
  redirection buys the attacker is a *private* anchor, not control of the steward's — the
  honest steward's next run still reads `lagging` and refuses.
- absent → **TOFU-adopt** the fully-verified tail, loudly, recording `adopted_utc`,
  `adoption_revision`, and `resolved_root`. First run the **mission_id secondary scan**:
  another anchor carrying the same `mission_id` means path-aliasing, relocation, or a
  second worktree — refuse with a message **naming the other anchor's path**, never mint a
  parallel anchor.

**Ancestry is resolved by hashing, never by trusting a `revision` field.** `load_latest`
chains on sha only and never checks `revision` against the filename or for contiguity
(`custody_store.py:120-133`), so an appended file carries an attacker-chosen `revision`.
The pinned checkpoint is located by hashing candidate files to find
`anchor.checkpoint_sha256`, then walking the sha chain forward. A filename↔revision
contiguity assertion is added to `load_latest` (cheap; @2 is the right moment).

**Advance** happens only in `write_checkpoint` after a successful publish, as an
**advance-only CAS** (exclusive-publish, mirroring `_publish_exclusive`). A failed anchor
*advance* after a successful publish is stderr-warned and the verb still succeeds
(`anchor-writes-failing` surfaces it) — a real write never fails because the anchor could
not be persisted, and the mission is never silently unprotected. Anchor writes on the read
path (TOFU) are best-effort: loud on failure, read succeeds, state `unpersisted`.

**Epoch monotonicity on the read path**: a lower epoch after a higher one → `ChainBroken`;
more than one 1→2 transition → `ChainBroken`; judged by **record kind only**, never by a
note string (mutable, attacker-writable).

#### 4.2a Anchor identity (Windows-stable)

`mission-key = sha256(canonical_mission_identity)` where canonicalization =
`realpath` → strip `\\?\` → ASCII-only casefold (reusing `_ascii_case_fold`, **not**
`str.casefold` — same NTFS reasoning as the drift keys) → best-effort drive-letter→UNC
canonicalization with a **fixed fallback order**. This fleet maps `Y:\dev` to
`\\10.10.10.127`, NTFS is case-insensitive, and one harness runs MSYS2, so path spellings
of one directory genuinely vary. The mission_id secondary scan is the net for the residual
case; **two worktrees of one repo are two directories, not two spellings**, and refusing
there is correct — a mission dir present twice IS a fork — provided the message names the
other path and `anchor-adopt` records the fork as a deliberate act.

#### 4.2b Anchor root — mitigated, not "removed" (honest correction)

There is **no `MISSION_CUSTODY_ANCHOR_ROOT` variable**; the root is settable only by an
explicit `--anchor-root` CLI flag, which is refused if it resolves inside the workspace
tree and is **not exposed on the hook/gate entry points**.

**But the default root is not env-free**, and rev 2 was wrong to claim the seam was
removed: `~` resolves through `USERPROFILE`/`HOMEDRIVE`+`HOMEPATH` on Windows and `HOME`
on POSIX, all of which an in-scope attacker that can invoke a process controls (verified
empirically). Mitigations, since denial is not available:
- the anchor records its `resolved_root`, and **first contact at a previously-unseen root
  is a loud event, not routine TOFU** — the adoption message states the root explicitly;
- every surface prints the effective root when non-default (`root-overridden:<path>`);
- SECURITY.md names this as a live seam under the in-scope actor, not a closed one.

### 4.3 Receipt verification

- **Single chokepoint** `_receipt_entries(checkpoint) -> [(request_id, sha|None)]`
  normalizes @1 (sha `None`) and @2 entries. A **grep-guard test** forbids raw
  `["receipt_ids"]` indexing/membership outside the chokepoint and the two writers.
  Consumers that must all route through it: `resume`, `continuity_breaks`,
  `_all_receipt_ids_ever`, `_historical_effect_path`, retirement, `reconcile`'s membership
  test, `acknowledge_receipt_loss`'s filter, `record_effect`'s reuse checks, verdict
  `receipt_refs` extraction, the CLI clean-resume `len(set(...))`, and `_write_next`.
- **Latest-attestation-wins**: admission order is first-occurrence; the effective
  `expected_sha` is the sha from the **latest checkpoint listing the id**. A silent `None`
  fallback when a sha exists elsewhere is forbidden (false-clean). An id whose only
  admitting entry lacked a sha is verified at **@1-strength and surfaced as such**.
- `_load_receipt(request_id, expected_sha)`: file loads but hashes differently →
  **`RECEIPT-TAMPERED:<id>`**, a drift finding distinct from unloadable, same weight.
  With a chained sha, "restored" is **byte-provable**; the @1 path-match heuristic remains
  the fallback for `None`-sha ids.

### 4.4 Writers

`write_receipt` returns `(path, sha)` (today it discards the sha `atomic_write_json`
already computed). `_write_next` carries `(request_id, receipt_sha256)`. `record_effect`
and `reconcile` append @2 entries; retirement removes entries **by id** (comparing
`request_id`, not the whole dict). On a pre-migration mission, writers still emit @1.

### 4.5 Migration — does not bless

Preconditions: (1) a prior **operator-consent amendment** authorizing the epoch migration
(consequential and irreversible — 2→1 is refused); (2) `resume()` clean **and** no
unreconciled continuity breaks, via a **non-mutating** drift probe (a refused migrate must
not side-effect a `reopened` checkpoint); (3) every current receipt loads **and** its
`artifact_path` agrees with the chain's recorded effect path where derivable; (4) not
already @2.

Then write the first `checkpoint@2` with `receipt_ids` backfilled to
`{id, sha256(receipt bytes)}` and notes extended by exactly one machine note, reserved
prefix `contract migrated: `. The 1→2 rule requires prev kind @1, new kind @2, and
`notes == prev_notes + [migration note]`.

**A P6 variant survives this and always will**: a single-receipt path has no continuity
neighbour (`zip(ids, ids[1:])` is empty for one id — `custody_mission.py:648-649`,
verified), so a co-tampered artifact+receipt passes every precondition and gets backfilled.
**No further precondition is added** — no runtime check can see it, and adding gates would
buy nothing. Instead the distinction is made **structural and surfaced**: ids present in
both the last @1 checkpoint and the migration @2 checkpoint are **backfilled**
(as-of-migration attestation only, inheriting every @1 blind spot including P6); ids
admitted afterwards are **minted-chained**. Both counts are computable from the chain with
no schema change and are printed by `status --brief`, so an acceptor cannot read
"receipts chained" as "backfilled receipts trustworthy".

### 4.6 CLI

- `migrate`, `anchor-repair`, `anchor-adopt`, `quarantine` (each prints the landed
  revision). `--anchor-root` is CLI-only (§4.2b).
- **`anchor-repair`** proves the pinned checkpoint is an ancestor by hash, prints the full
  per-revision delta — amendments, guard changes, receipt admissions, status transitions,
  frontier change, **plus `written_by` and `written_utc`** (a forged amendment can copy the
  operator's words verbatim; a foreign actor string or timestamp gap is the discriminator
  a human actually has) — then advances. It **refuses on non-interactive stdin and offers
  no `--yes` flag**: the in-scope attacker can invoke the process, so consent must be a
  mechanism, not an intention.
- **`quarantine`** is the missing repudiation path. Without it the honest steward facing a
  forged append chooses between adopting the forgery and leaving the mission permanently
  unwritable — pressure to click through, which retires the control. `quarantine` MOVES
  the offending revisions to `missions/<id>/quarantine/` (never deletes); the tail then
  equals the pinned revision, the state returns to `verified`, and it immediately writes a
  machine note recording the quarantined shas, so recovery is auditable and append-only in
  spirit.
- If the anchor root is unwritable, `anchor-repair` cannot persist and writes refuse
  forever. Documented break-glass: `--anchor-root` to a writable location, which is
  recorded in the chain as a note.
- `status --brief` gains `record` (epoch), `anchor` (state, `adopted_utc`,
  `adoption_revision`, effective root), and the backfilled/minted-chained receipt counts.

### 4.7 Hook/gate — STRICTEST-OF pinned and tail (rev-4 correction)

- **Hook-internal errors** (crash, timeout, unreadable payload) → fail open LOUD.
- **When the anchor is not `verified`, guards are the STRICTEST-OF the pinned and tail
  records**: the UNION of their guard rules, and `enforce` if EITHER says enforce.

  Rev 3 said *pinned-only*, and that was asymmetric in the wrong direction — verified
  reachable **with no attacker at all**. §4.2 makes a failed anchor advance warn-and-succeed
  (correctly — the alternative bricks a mission whenever the anchor root blinks), so the
  chain legitimately sits one revision ahead whenever the root is briefly unwritable. If
  *that* revision is the `amend` that armed `guard_mode: enforce`, the pinned record is the
  pre-arming one, and `evaluate()` returns `{"decision": "allow", "mode": "inert",
  "reason": "no guards armed"}` (`custody_gate.py:106-110`, verified) — **the operator's
  just-armed enforce guard is silently disarmed.** Silently, because the guard-log is only
  written `if verdict["matched"]` (`custody_gate.py:154`), and nothing matches when nothing
  is armed, so §4.7's promised `degraded-anchor` entry never appears either. One revision of
  lag is exactly enough when it is the arming revision, and custody *writes* freezing does
  not help: the agent's tool calls keep flowing through a gate that now allows everything.

  Strictest-of keeps rev 3's genuine win — a forged tail can only ever **add** restrictions,
  i.e. produce a false block, which this module's own doctrine calls the safe direction
  (`custody_gate.py:11-13`: a false block names its rule and is discharged by an `amend`;
  a false allow silently retires custody) — while making a lagging anchor incapable of
  disarming anything.
- **A tail claiming `completed`/`cancelled` over an OPEN pinned record is a loud refusal,
  never `NoActiveMission`.** Second, distinct hole, verified: activeness is decided from the
  TAIL's status (`custody_mission.py:228`) before the gate ever reads authority, and
  `run_gate` converts `NoActiveMission` into `{"decision": "allow", "mode": "inert"}`
  (`custody_gate.py:139-141`). So appending a forged checkpoint with `status: "completed"`
  disarms every guard on a live mission — the same "attacker-controlled record decides how
  seriously its own tamper is taken" shape, moved one layer out. The anchor is the first
  artifact that ever recorded *"this mission was open at rN"* outside the workspace, so @2
  is the first release that **can** close this.
- **True `AnchorMismatch`** (pinned record unresolvable): block on enforce, loud-allow on
  audit.
- Audit missions log a distinguishable `degraded-anchor` guard-log entry and allow. That
  entry must be written on the degraded path itself, not only on a rule match.
- The next `status`/`resume`/`audit` refuses regardless, so tamper cannot stay quiet.
- **Known residue, disclosed (pre-existing @1, not a @2 regression):** the guard-change
  sanction is **length-only** — `len(latest_amendments) <= len(baseline_amendments)`
  (`custody_mission.py:298-302`), never reading amendment text — and `amend` accepts
  `--guard-mode` with no `--guards-file` (`custody_cli.py:230-236`). Since §2 grants the
  attacker process invocation *including custody verbs*, `amend --text "anything"
  --guard-mode audit` is a **chain-legal enforce→audit downgrade through the sanctioned
  path**, which `write_checkpoint` then blesses and the anchor advances onto. §4.2's "a
  forged tail cannot declare its own guard mode" is true but incomplete: an *unforged* tail
  can. Recorded in SECURITY.md; a guard-**weakening** amend deserves the same
  interactive-consent treatment §4.6 gives `anchor-repair`, tracked separately rather than
  smuggled into @2.

### 4.8 Discovery

`EpochTooNew` from a sibling is **present-but-unreadable**, distinct from corrupt-skip:
`open` refuses; the gate takes the degraded-loud path — **allow-with-loud-log, unless the
discovered mission is enforce-armed, in which case block** (matching §4.7's principle).
This grants the attacker no new denial power: a workspace writer can already wedge every
verb with one decoy mission dir (`custody_mission.py:233-235`) and push the gate inert
(`custody_gate.py:144-151`); refusing `open` beats silently disarming.
`AnchorMismatch` on the single active mission propagates as a loud refusal from the invoked
verb — it must not be swallowed into `NoActiveMission`, which would permit a duplicate
`open`.

### 4.9 Acceptance verdicts enter the chain

Today `_store_verdict` writes `verdicts/<rev>-<verdict>.json` outside the chain
(`custody_mission.py:502-504`) and the completing note is only `f"PASS: {reason}"` (`:903`),
so `acceptor_id` and `assurance_tier` are nowhere in the chain. The verdict file's hash
therefore rides the hash-chained notes.

**Format: machine fields FIRST, behind a reserved prefix** — `verdict PASS <sha256hex>:
<reason>` — and `verdict ` joins `_RESERVED_NOTE_PREFIXES`. Rev 3 proposed
`PASS: <reason>; verdict_sha256=<hex>`, which had two defects: `"PASS: "` is **not** a
reserved prefix (`custody_mission.py:32-35`), so ordinary `note()` can forge it — and rev 3
made it the first note-parsing surface whose prefix is unreserved, while every existing
note-parser reads a reserved one (`_historical_effect_path` at `:443`,
`_retired_receipt_ids` at `:474`). Worse, `reason` is free operator text
(`custody_cli.py:138`), so a reason *ending* in `; verdict_sha256=<attacker-hex>` is
byte-indistinguishable from the machine suffix, and whether the attacker wins depends on
whether the reader takes the first or last match. Machine-fields-first kills both.
(`"cleared: "` at `:939` is likewise unreserved — folded in.)

**A terminal PASS needs a reader, or "tamper-evident" is unsupported.** The record is pinned
at write time, but two gaps: its final anchor advance can fail warn-and-succeed like any
other and — because no verb may write after `completed` — there is no future write to retry
it; and **no CLI surface can load a completed mission at all** (`Mission.load` excludes
completed/cancelled at `:228`, every verb but `open`/`gate` routes through it, and discovery
is pathless by contract). `verify_mission_custody.py` validates record *shape* only — not
the chain, not the anchor, not the verdict hash. So @2 adds **`verify --mission-id`**, a
mission-addressable surface that checks chain + anchor + `verdict_sha256` on a completed
mission. Without it the tamper would be *recorded*, not *evident*.

## 5. What @2 deliberately does not do

No notes compaction / O(n²) work; no signing or principal binding; no change to the
superseded-receipt deletion asymmetry; no forced migration. `Mission.open` keeps emitting
**@1 for one release window** so `migrate` is the sole @1→@2 entry (one boundary shape;
existing suites keep their meaning). No cross-device anchor sync.

## 6. Consumers and rollout

Pre-@2 validators reject @2 records → `ChainBroken` → mission skipped → could permit a
duplicate `open`. Deploy @2 to every custody consumer BEFORE migrating any shared mission.
Order: merge → deploy cache and **re-verify at migrate time that every harness loads the
same custody bytes** (hash them; do not inherit a prior session's claim — committed ≠
deployed, and this fleet currently has concurrent agents landing changes) → migrate
`livefire` (pilot) → UAT probes → operator-consented migration of `media-library-rebuild`
→ re-run resume/audit/status → receipts into the mission. The tracer record stays @1.

## 7. Test plan

Existing suites stay green with **two sanctioned modifications**: a conftest-level
`--anchor-root` injection so tests never write into the real `~/.mission-custody` (on this
device, the sacred C:), and deliberate, enumerated updates to tamper assertions whose error
KIND legitimately changes.

⚠ **The dangerous direction is not a test that goes red — it is one that stays GREEN while
testing nothing.** `test_amendments_cannot_be_rewritten`
(`test_custody_mission.py:202-217`) forges by rewriting the tail **in place** and asserts
`except (CustodyError, StoreError)`. Under @2 the rewritten tail's sha no longer matches the
anchor, so `AnchorMismatch` (a `StoreError`) fires *before* `_verify_manifest` ever runs —
the broad except swallows the substitution and the test silently stops covering the
append-only amendment check. Contrast `test_tail_guard_tamper_without_amendment_detected`
(`:910-927`), which forges via `store.write_checkpoint`, so the anchor advances onto the
forgery and `_verify_manifest` still runs: **in-place edits erode, appends do not.**
Therefore every manifest-tamper test MUST assert the **specific** error kind (or arrange the
anchor onto the forged tail first). Auditing the existing suite for this pattern is a
required implementation step, not a nicety.

New coverage:

- **validator**: @2 matrix; invalid corpus (≥8); `checkpoint@3` → EPOCH-TOO-NEW.
- **store**: read-path epoch monotonicity (reject @1-after-@2 append; reject double 1→2);
  **whole-chain rewrite to pure @1 detected via anchor presence**; anchor state machine
  (verified / lagging→read-flag+write-refuse / mismatch / ahead / corrupt / pinned-file-
  absent / absent→loud-TOFU / same-id-scan→refuse-naming-other-path); ancestry resolved by
  hash with an attacker-chosen `revision` field; filename↔revision contiguity;
  advance-only CAS; **the E1 race: anchor verified, tail swapped, write must refuse**;
  anchor-advance failure warns-and-succeeds; `--anchor-root` inside workspace refused.
- **the laundering regression**: forged append + `resume` → resume must REFUSE, not write
  rN+2 onto the forgery.
- **mission**: P6 → RECEIPT-TAMPERED; acknowledge-loss restore-by-hash and retire;
  latest-attestation-wins on a superseded pre-migration receipt; mixed-chain readers;
  verdict `receipt_refs` stays strings on @2; migration preconditions (each refusal path,
  non-mutating probe) and success shape incl. backfilled/minted counts; CLI clean-resume on
  a migrated mission (no `TypeError`); **verdict_sha256 in the note detects an edited
  verdict file**.
- **gate/hook**: guards read from the PINNED checkpoint when not verified — specifically
  the forged-tail `guard_mode: audit` inversion must still BLOCK; enforce vs audit on
  mismatch; hook-internal error fails open loud; EpochTooNew path.
- **CLI consent**: `anchor-repair` refuses non-interactive stdin; `quarantine` restores
  `verified` and records shas.
- **discovery**: EpochTooNew refuses `open`; AnchorMismatch does not become
  `NoActiveMission`.
- **process-proof**: byte-identical @1 prefix under @2 reads.
- **Windows**: one mission via two path spellings → one stable mission-key.

## 8. Windows / fleet hazards

`Y:\dev` maps to `\\10.10.10.127`; NTFS is case-insensitive; claude runs MSYS2 and kimi
does not; many worktrees exist; several agents run concurrently. §4.2a exists for the
spelling problem, the mission_id scan for relocation/fork, and the in-`write_checkpoint`
gate for the concurrency race. `os.replace` onto a file another process holds open can
raise `PermissionError` on Windows — anchor CAS uses exclusive-publish and never fails the
verb.

## 9. Review plan

Two design-review rounds have run **before implementation** (§10). Post-implementation:
fresh-agent code review + adversarial PoC review re-running *these specific attacks* live
(append-forge-then-resume, whole-chain @1 rewrite, verify-then-write race, forged-tail
guard-mode inversion, migration single-receipt P6, env-redirected root, verdict-file edit),
fix rounds re-reviewed (**a fix is a change and needs the same gate** — two of round 2's
findings were holes round 1's fixes created), mechanical merge gate, then §6.

## 10. Review history

### 10.1 Rev 1 → rev 2 (three-lens panel: adversarial / correctness / framing)

All three returned proceed-with-changes; all three **independently** found the same
CRITICAL — rev 1's crash-window auto-repair blessed a forged tail **append** and advanced
the anchor onto it, chaining unbounded forgeries, because `prev_checkpoint_sha256` is
computable from the readable tail. Rev 1's disclosure ("the @1 status quo narrowed to one
revision for the duration of a crash") was factually wrong: the window is
attacker-constructible on demand. Also found: epoch enforcement was write-path only;
migration blessed P6-tampered state; and the anchor key was unstable on this fleet's
Y:/UNC/case spellings. Rev 2 deleted auto-advance, moved epoch checks to the read path,
hardened migration, stabilized the key, and added the `_receipt_entries` chokepoint.

### 10.3 Rev 3 → rev 4 (fresh convergence check; every claim re-verified in source)

A **different** reviewer (not the one who proposed the `write_checkpoint` placement — no
actor certifies its own recommendation) scoped to four questions. It **proved the E1 race
closed** and validated quarantine, migration, and anchor-repair mechanically. It found two
CRITICALs, both at leaf level, and one of them was again mine:

- **§4.7 pinned-only was asymmetric in the wrong direction** — and reachable with **no
  attacker**. §4.2's warn-and-succeed makes a one-revision lag a permanent architectural
  possibility; if that revision is the `amend` that armed enforce, pinned-only evaluates the
  pre-arming record and `evaluate()` returns inert-allow, **silently** (the guard-log writes
  only on match). → strictest-of.
- **A forged `completed` tail disarms every guard** via `NoActiveMission` → inert gate;
  §4.8's protection was scoped to `AnchorMismatch` and never fired for `lagging`.
- **Rev 3 repeated rev 2's error class in one sentence**: "the enforce gate keeps evaluating
  correctly after an honest crash" was falsified by the finding above. Corrected in §4.2.
- **§4.9's note format was unreserved and injectable**; **a completed mission has no reader
  at all**, so "tamper-evident" was unsupported → `verify --mission-id`.
- **§7 silent test erosion**: an in-place tamper test would stay GREEN while testing nothing.
- **§2 stated an external control as an attacker property** — the same
  writing-≠-installing error the section itself invokes.
- Confirmed and **argued against changing**: the single-receipt P6 residue, migration
  preconditions, `receipt_refs` as a string list, the `write_checkpoint` placement, and
  warn-and-succeed. Also confirmed `manifest['scope']` is consumed nowhere and rev 3 leans
  on it nowhere — with the nuance that it *is* tamper-checked by `_verify_manifest`'s byte
  comparison while being enforced by nothing, which is precisely the shape a reader mistakes
  for a control (→ SECURITY.md).

Verdict: **CONVERGED** — the architecture held under a second fresh adversary, and every
remaining defect sits at a leaf (which record supplies authority, how a note is formatted,
which surface reads it), the defect profile of a design settling rather than moving.

### 10.2 Rev 2 → rev 3 (focused adversarial re-check; every claim re-verified in source)

The shape survived again — no reshape asked for — but five clauses were under- or
mis-specified, **two of them holes rev 2's own fixes created**:

- **A — `resume` is a writer** (`custody_mission.py:740`, verified). Rev 2's verb-layer
  rule let the attack complete through the one verb whose purpose is to run after an
  interruption. → §4.2 moves the gate into `write_checkpoint`.
- **B — whole-chain rewrite to pure @1** evades everything, because rev 2 engaged the
  anchor only for @2 tails. → engagement now keys on anchor **presence**. Also:
  `load_latest` never validates `revision` (`custody_store.py:120-133`), so ancestry must
  be resolved by hashing.
- **C — a single-receipt P6 survives migration** (`custody_mission.py:648-649`, verified:
  `zip` on one id is empty). Judged RESIDUAL-DISCLOSED-OK; the reviewer **argued against**
  adding preconditions and for making the backfilled/minted distinction structural
  instead. Adopted as argued.
- **D — new holes from the fixes**: no repudiation path (adopt-the-forgery or freeze the
  mission) → `quarantine`; `anchor-repair` self-serviceable by a process-invoking attacker
  → interactive-only, no `--yes`; **§4.7 never said which record determines "enforce-armed"**
  → the forged tail could declare `guard_mode: audit` and downgrade the response to its own
  tamper → authority now reads from the **pinned** checkpoint.
- **E — the ambient-env seam was renamed, not removed** (`Path.home()` follows
  `USERPROFILE`/`HOME`; **empirically proven on this device**). Rev 2's §10 celebrated
  catching exactly this error class in rev 1 and then committed it. → §4.2b mitigates and
  discloses. Plus **E1** the verify-then-write race (an anchor-created hole: a durable
  "verified" conclusion outliving the read that justified it) and **E2** unchained
  acceptance verdicts → §4.9.

The most valuable outcomes of round 2 were, again, not defect counts: the reviewer's
**argument against** further migration gates, and its protection of a rev-2 decision a
future reviewer's reflex would "fix" (`receipt_refs` must stay a string list — §4.1).
