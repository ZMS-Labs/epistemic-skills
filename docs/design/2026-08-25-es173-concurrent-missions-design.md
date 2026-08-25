# es#173 — Concurrent missions: session→mission binding with union guards

**Status:** REVISED POST-GAUNTLET. The frozen subject (`c439118`) went through
the full gauntlet (record: `docs/design/2026-08-25-es173-gauntlet-record.txt`
@ `cc2cf27`, judged against core @ `488f252`); verdict **CONDITIONAL** — four
CONFIRMED fatals with named repairs, four operator decisions. The operator
adjudicated all four OD questions on 2026-08-24 (es#173, "Operator
adjudication — the four OD questions"). This revision applies every
adjudicated decision and every binding condition; each corrected claim cites
the adjudication line and the gauntlet finding that settled it. Nothing here
is built. Core citations re-verified against the shipped files at `488f252`
(byte-identical in this worktree, checked at revision time).

**Adjudicated model (verbatim constraint, quote restored in full per
gauntlet major mF6):** *"explicit session→mission binding with union
fallback. A session declares which mission it acts under; calls without a
binding are checked against the UNION of all active missions' guards — any
mission may block, and the block names its mission and rule. Fail-safe by
construction: no silent disarm (the decoy failure in this issue's reason 1),
binding answers authority routing."*

**The 2026-08-24 adjudication lines this revision implements:**

- **OD-1 UNION-ALWAYS** — every gate-routed call is checked against the
  union of all active missions' guards, bound or not; *"binding answers
  authority routing (where effects/notes land), never guard exposure."*
- **OD-2 GATE `effect` ONLY** — `effect` (the world-mutating verb — effect
  IS the file write) goes through union guard evaluation before
  `_write_effect`; `note` and `amend` remain ungated **by design** as
  unblockable audit channels, documented as such, not as a residual hole.
- **OD-3 DROP the structured `sibling_touch` field** — sibling attribution
  survives via resume-time scan of sibling receipt stores plus the FATAL-3
  authorization discriminator; zero schema change; contract@2 is off the
  table; the tolerant-reader claim is deleted.
- **OD-4 GATE ON APPROVE** — guards join the union only once the mission is
  operator-approved; a never-approved draft cannot block the fleet;
  `evaluate()` gains a status check; the case table gains the rows.

**The four questions the 2026-08-15 adjudication ordered answered:** binding
mechanics · coexistence without false drift · fairness/coordination on shared
artifacts · migration of the scratch-workspace missions. Each has a section;
the case tables (§7) enumerate the product space.

---

## 0. Grounding — what the shipped core does today (read at `488f252`)

Discovery and the door:

- `Mission.open` refuses at the door if `load()` finds ANY active mission
  (`custody_mission.py:912-942` — door-check comment through the refusal;
  the message is at `:941`). Refusal happens before any write. The
  `operator_ref`/`steward_ref` it takes are unverified strings
  (`custody_mission.py:887-897`) — mission existence proves no authority.
- `Mission.load` resolves exactly one active mission; two or more raises
  `MultipleActiveMissions` (`custody_mission.py:1031-1033`). "Active" means
  latest checkpoint status not in `("completed", "cancelled")`
  (`custody_mission.py:1018-1019`) — a **draft counts as active**.
- `load` **skips** a mission dir whose latest checkpoint fails to load
  (`StoreError`/`ValueError`), loudly on stderr, and continues
  (`custody_mission.py:1003-1017`). Under the singleton model that skip
  protects discovery of the healthy mission; under plurality it silently
  shrinks the union (§2, case rows B22–B23).
- `custody_gate.run_gate` catches `MultipleActiveMissions` and returns
  `{"decision": "allow", "mode": "inert"}` — loud on stderr, but ALLOW
  (`custody_gate.py:305-314`). This is the fail-open surface: the state the
  contract forbids is also the state that disarms its own enforcement.

What consults the gate — and what does not (the FATAL-2 facts):

- Lifecycle verbs **never** consult `run_gate`: `custody_cli.py`'s
  `dispatch()` (`custody_cli.py:376-404`) imports `run_gate` only for the
  explicit `gate` command (`:397-402`); every other verb resolves
  `Mission.load` (`:404`) and calls Mission methods directly.
- `record_effect` (`custody_mission.py:1498-1528`) status-checks against
  `_EFFECT_STATES` (`:1502`) and goes straight to `_write_effect`
  (`:1521`); `_write_effect` (`custody_mission.py:1160-1200`) writes the
  target bytes (`:1188`) and mints the receipt with zero guard evaluation.
- `evaluate()` (`custody_gate.py:222-258`) reads ONLY `guard_mode` and
  `actuator_guards` from the authority dict (`:223-224`); it has **no
  status input** — approval is invisible to it today (the OD-4 change
  lands here and in the union assembler, §2).
- The gate's only write is an append to `missions/<id>/guard-log.jsonl`
  (`custody_gate.py:2-9` docstring, `GUARD_LOG_NAME` at `:33`,
  `_append_guard_log` at `:260-263`, best-effort append at `:352-360`) —
  the checkpoint chain is never touched. This is the side-channel precedent
  §4 reuses for the sibling crossing record (FATAL-4 repair).

Record closure (the FATAL-1 facts):

- `RECEIPT_FIELDS` is a closed 8-key set (`verify_mission_custody.py:263-266`)
  enforced field-exactly — unknown keys AND missing keys are both errors
  (`_check_exact_fields`, `verify_mission_custody.py:291-298`; applied by
  `validate_receipt` at `:511-513`) — at **write time**: `atomic_write_json`
  and `write_receipt` raise `StoreError` on any validation error
  (`custody_store.py:81-84`, `:209-212`). `receipt.schema.json` declares
  `additionalProperties: false` (`:8`). There is no tolerant-reader rule for
  receipts in either direction; a same-version writer cannot mint a receipt
  carrying a new field at all.
- Checkpoint status is a closed six-member enum:
  `STATES = {"draft", "active", "reopened", "verifying", "completed",
  "cancelled"}` (`verify_mission_custody.py:16`, asserted at `:477-478`).
  `_OPEN_STATES = {"draft", "active", "reopened", "verifying"}` and
  `_EFFECT_STATES = {"draft", "active", "reopened"}`
  (`custody_mission.py:22-23`).
- **Approval is a chain property, not a latest-status property**:
  `approve()` transitions draft→active (`custody_mission.py:1489-1495`),
  but a never-approved mission can sit in `reopened` (drift on a draft
  reopens it), so the core's own approval test is "the chain holds a
  checkpoint whose status is outside `{draft, reopened}`"
  (`_resumption_status`, `custody_mission.py:1420-1445`; the
  damaged-file-crossing-the-approval-gate incident is documented at
  `:1427-1434`). OD-4 and the FATAL-3 discriminator both use THIS test.
- Machine-note integrity: `_RESERVED_NOTE_PREFIXES`
  (`custody_mission.py:41-44`) is guarded by `_refuse_reserved_note`
  (`:47-101`): per-line, NFKC-normalized, format-character-stripped,
  case-folded, whitespace-stripped — the docstring documents the four
  historically-exploited bypass shapes (leading space, capital, leading
  newline, machine note on the second line) plus the invisible-character
  class. §4's new prefix registers here and inherits this guard and its
  test obligations.
- Receipts, drift-checks (`resume`), amendments, and acceptance all resolve
  through the single active mission. None carries a mission address today.

## 1. Binding mechanics

A session declares the mission it acts under through exactly two channels:

1. **`--mission <mission-id>`** on every CLI verb (explicit, per-call, wins).
2. **`ZMS_MISSION_ID` environment variable** (session-scoped default).

Precedence: flag > env > unbound. `open` prints the binding line for the shell
(`export ZMS_MISSION_ID=<id>`) but does NOT set it — a child process cannot set
its parent's environment, and pretending otherwise would manufacture the
"bound, actually unbound" decoy. There is no open-time inheritance state on
disk: binding is a property of the SESSION, not of the store, so nothing about
it can go stale inside a checkpoint.

**Validation is strict.** A binding must name a mission directory in THIS
workspace whose latest checkpoint status is an open state. Bound-to-completed,
bound-to-cancelled, bound-to-nonexistent, and bound-to-unreadable are four
spellings of the same refusal (`BindingInvalid`, naming the state found).
A stale binding NEVER falls through to union or to "the only active mission" —
silent fallback is how a session acts under the wrong authority politely.

**Lifecycle verbs bind hard.** `effect`, `amend`, `note`, `frontier`,
`begin-verification`, `accept`, `acknowledge-loss`, `resume`, `audit`:
- 0 active missions → `NoActiveMission` (unchanged).
- 1 active mission, unbound → resolves to it (today's behaviour, preserved —
  the single-mission workflow must not grow ceremony).
- N>1 active, unbound → **`BindingRequired`**: the refusal lists every active
  mission id and the two binding channels. It never guesses.
- Bound → the bound mission, after validation.

Binding answers WHERE a verb's writes land and WHOSE amendments discharge a
block. It answers nothing about guard exposure — that is §2, and the split is
the adjudication's own: *"binding answers authority routing (where
effects/notes land), never guard exposure"* (OD-1).

`MultipleActiveMissions` as a load-failure class is retired from these paths;
it survives only as an internal distinction inside `load` for the gate.

## 2. Guard evaluation — union ALWAYS on the mediated surface; approval arms

**OD-1 (UNION-ALWAYS, adjudicated 2026-08-24):** every gate-routed call is
checked against the union of all approved missions' armed guards, **bound or
not**. Binding routes authority (§1), never exposure. This ratifies the
frozen design's reading as the ruling's meaning — no longer an open question.
The rationale stands: if binding to mission A exempted a call from mission
B's guards, the moment two missions coexist every guard becomes voluntary —
choose the mission whose guards don't cover your actuator and act. That is
the A1 undifferentiated-override failure in session clothing.

**Corrected claim — the mediated surface (FATAL-2, settled by OD-2).** The
frozen design claimed union evaluation "for EVERY call". That claim was
false against the core: lifecycle verbs never consult `run_gate`, and
`_write_effect` writes bytes and mints the receipt with zero guard
evaluation (evidence in §0; `custody_cli.py:376-404`,
`custody_mission.py:1160-1200`, `:1498-1528`). The corrected claim, per
OD-2 ("GATE `effect` ONLY"):

- **Union guard evaluation covers exactly two surfaces:** (a) gate-routed
  harness calls (`run_gate`, as today), and (b) the **`effect` verb** —
  effect IS the file write, so `record_effect` runs union evaluation
  **before** `_write_effect`. A blocked effect refuses side-effect-free
  (nothing written, no receipt minted — the same refuse-before-mutate
  posture `_write_effect` already takes for idempotency,
  `custody_mission.py:1162-1165`), naming every matching
  `(mission_id, rule)` pair.
- **`note`, `amend`, and `frontier` remain ungated BY DESIGN** — they are
  unblockable audit channels, not a residual hole. A guard must never be
  able to block the recording of an escalation, a grant, or narrative: the
  discharge channel for a block (`amend`) cannot itself be blockable, and
  an audit trail that a guard can silence is not an audit trail. This is
  the adjudication's third arm verbatim: *"complete mediation for
  actuation, guaranteed availability for audit"* (OD-2). What keeps these
  channels honest is not a gate: the append-only hash chain, per-mission
  authority routing (§1), and the reserved-prefix forgery guard
  (`custody_mission.py:41-101`, extended in §4).

**OD-4 (GATE ON APPROVE, adjudicated 2026-08-24): approval arms the union.**
A mission's guards join the union only once the mission is
operator-approved. "Approved" is the chain test the core already ships —
the chain holds a checkpoint whose status is outside `{draft, reopened}`
(`custody_mission.py:1420-1445`) — deliberately stronger than
"latest status ≠ draft": a never-approved mission can sit in `reopened` via
drift on a draft (`:1427-1434`), and the adjudication's intent ("a
never-approved draft cannot block the fleet") must not invert into "damage
a draft's store to arm its guards". Mechanically: the union assembler
gathers `(authority, approved?)` per active mission and `evaluate()` gains
the status check — today it reads only `guard_mode` and `actuator_guards`
(`custody_gate.py:222-227`) and cannot see approval at all. The asymmetry
is deliberate and one-directional in the safe direction: a draft mission is
**subject to** the union (its effects are checked against approved
siblings' guards) but **contributes nothing** to it until `approve()`
(`custody_mission.py:1489-1495`) lands. Case rows B24–B25.

Union semantics:

- A block names `(mission_id, rule)` of every matching guard (all matches,
  not first — the operator discharging the block needs the full bill).
- Discharge stays per-mission: an amend recorded in mission B discharges B's
  rule only. A call blocked by A and B needs both. THIS is the coordination
  mechanism (§4) — cross-mission conflict surfaces as two named rules, not
  as a race.
- Guard-log append goes to EVERY matching mission's `guard-log.jsonl`
  (each mission's audit trail must be complete from its own dir).
- `guard_mode` is per-mission and applies to that mission's own rules.
- Unguarded missions contribute nothing to the union (unchanged semantics).
- Gate discovery failures keep today's honest-inert behaviour for corrupt or
  epoch-skewed stores — but `MultipleActiveMissions` disappears as an inert
  cause, because plurality is no longer a failure. **The fail-open decoy is
  removed not by handling the error better but by making the state legal.**

**Mid-session union degradation (gauntlet major, case rows B22–B23).**
`Mission.load` skips a mission dir that fails to load — loudly, but it
skips (`custody_mission.py:1003-1017`). §3's open-time refusal covers only
the open-time snapshot: a sibling that becomes unreadable BETWEEN two gate
calls drops its guards from the union with nothing but a stderr line. The
design closes this per surface, by what each surface can afford:

- The **hook path** stays fail-open — a hook must never brick the tool loop
  (the shipped posture, `custody_gate.py:305-314` rationale) — but the
  verdict's `reason` and stderr must both name the skipped sibling and say
  its guards are NOT enforced (`union degraded: <dir> unreadable`). An
  allow that silently dropped a mission's guards would be the §0 decoy
  rebuilt one layer down.
- The **`effect` verb** CAN refuse without bricking anything, so it does:
  effect under a skipped active sibling refuses (`UnionDegraded`, naming
  the dir) until the sibling is repaired, completed/cancelled by an
  updated reader, or explicitly acknowledged with the same
  `--acknowledge-unreadable` act §3 defines at open time (recorded in the
  acting mission's chain).

## 3. Open — plurality becomes legal; the door checks change target

`open` no longer refuses on an existing active mission. It refuses on:
- duplicate `mission_id` (dir exists), unchanged;
- EpochSkew anywhere in the store (unchanged — a store this reader cannot read
  may hold anything; opening beside it is still blind);
- unreadable mission dirs (StoreError/ValueError skips) — NEW refusal: today's
  open-door treats a corrupt sibling as ignorable; under plurality a corrupt
  sibling's guards are silently absent from the union, so open in a workspace
  with unreadable mission dirs refuses until they are repaired or explicitly
  quarantined (`--acknowledge-unreadable <dir>` records the acknowledgement in
  the new mission's opening checkpoint).

A freshly opened mission is a **draft**: it is active for discovery and
binding (`custody_mission.py:1018-1019`), its steward may work it
(`_EFFECT_STATES` includes draft, `custody_mission.py:23`), and it is
subject to the union — but its guards arm nothing until `approve()` (OD-4,
§2). `open` printing the binding line therefore hands the session authority
routing, not blocking power.

**Scope-overlap disclosure:** when a new mission's `scope.in` path patterns
intersect an active sibling's (pattern-vs-pattern intersection is decidable for
the glob dialect in `_glob_regex`; prose entries are reported as incomparable),
`open` prints the overlap and records it in the opening checkpoint. Disclosure,
not refusal — coexistence on shared paths is the feature being built (§4).

## 4. Coexistence without false drift; fairness on shared artifacts

The drift model today: `resume` hash-checks the BOUND mission's receipted
artifacts. Under plurality, mission B may legitimately `effect` a file mission
A receipted. Without new machinery A's next resume reports drift — true
(bytes changed) but mis-attributed (it reads as unsanctioned).

**Corrected mechanism (OD-3, adjudicated 2026-08-24: "DROP THE STRUCTURED
FIELD"; FATAL-1 CONFIRMED incl. live falsifier).** The frozen design put a
`sibling_touch` field on B's receipt. That field cannot be written under
receipt@1 at all — the closed 8-key exact-match validation refuses it at
write time (evidence in §0: `verify_mission_custody.py:263-266`, `:291-298`,
`:511-513`; `custody_store.py:81-84`, `:209-212`;
`receipt.schema.json:8`) — and contract@2 is off the table per OD-3. The
function survives with **zero schema change**, in three parts:

**(a) Detection — resume-time scan of sibling receipt stores.** `resume`
(in A) on a drifted receipted artifact scans the receipt stores of the
other active missions in the workspace for receipt@1 records whose
`artifact_path` matches and whose `after_sha256` equals the current content
hash. Every field this needs — `mission_id`, `artifact_path`,
`after_sha256` — already exists on receipt@1
(`verify_mission_custody.py:263-266`). No new field, no new record type,
nothing minted at effect time that the schema must carry.

**(b) Classification — the FATAL-3 authorization discriminator.**
Hash-match alone is a self-serve audit-downgrade: `open()` takes unverified
refs (`custody_mission.py:887-897`), so anyone who caused unauthorized
drift could open a throwaway sibling, effect the tampered bytes, and
self-mint the receipt that launders the drift into an ack-only lane.
Reclassification to `DRIFT-SIBLING(mission=B, receipt=<id>)` therefore
requires ALL of:

1. **hash match** — a sibling receipt@1 record with matching
   `artifact_path` and `after_sha256` (part (a));
2. **the sibling is operator-approved** — by the chain test
   (`custody_mission.py:1420-1445`), not latest-status ≠ draft: a
   never-approved mission wedged in `reopened` must not launder any more
   than a draft can (same reasoning as OD-4 in §2);
3. **an explicit cross-mission authorization record in A's own chain** — an
   authority amendment recorded through the existing `amend` channel
   (`amend_authority`, `custody_mission.py:1531`; appended, chained,
   comparable) naming the sibling mission id authorized on the path or
   pattern, recorded before the reclassification is offered.

Any leg missing → **plain drift at today's severity**, with the sibling
receipt reported as evidence alongside it. The discriminator gates the
severity downgrade, never the information: resume always says what it
found.

DRIFT-SIBLING is reconciled by acknowledging the sibling receipt — recorded
in A's chain by A's own bound session as the machine note
`sibling-touched: <path> by <mission-B> receipt <id>` — not by
`acknowledge-loss` (nothing was lost). That note is written under A's
authority by A's steward, consistent with §1.

**(c) The crossing record — side-channel, never the sibling's chain
(FATAL-4).** The frozen design had B's effect append a note into A's chain.
That contradicts this design's own authority model (§1: binding routes
where notes land) and would land a hash-linked revision in A's chain via
`_write_next` (`custody_mission.py:1109`) with no actor authorization.
Instead, when B's effect touches a path receipted by an active sibling A,
B appends one JSON line to **`missions/<A>/sibling-touch.jsonl`** — the
`guard-log.jsonl` analog (`custody_gate.py:2-9`, `:33`, `:260-263`):
append-only, outside the chain, chain byte-identity preserved. The entry
carries `{utc, actor, session_id, from_mission, receipt_id, artifact_path,
after_sha256}`. The append is best-effort exactly like the guard-log append
(`custody_gate.py:352-360`): a failed append never blocks B's effect but is
loud on stderr. It is **advisory**: ground truth for detection is the
receipt scan in (a), so a lost or suppressed side-channel entry cannot hide
a crossing — it only costs A's next resume the early hint.

**Forgery closure (gauntlet major).** `"sibling-touched: "` is registered
in `_RESERVED_NOTE_PREFIXES` (`custody_mission.py:41-44`) so caller
narrative cannot imitate the machine acknowledgement, with a forgery test
covering the four documented bypass shapes and the invisible-character
class the guard already folds away (`custody_mission.py:47-101`): leading
space, capital, leading newline, machine note on a second line, and
Cf-character smuggling. The prefix guard applies on every surface that
embeds caller text into a note (`note`, `amend`, `cancel`, verdict
reasons — `custody_mission.py:62-64`).

**Fairness:** no locks. Single-operator estate; the cost of a lock manager
exceeds the cost it prevents. The union guard + sibling attribution makes
simultaneous writes VISIBLE and attributable; the operator remains the
scheduler. The implementation gate should test whether
visible-but-unserialised is sufficient at this estate's concurrency level
(measured: 2–4 concurrent sessions, one operator).

## 5. Migration of the scratch-workspace missions

The workaround population (`scratch/custody-hook-livefire`, `scratch/es133-*`,
and kin): each is a mission whose store is detached from the repo it governs.
Migration is an OPERATOR act per mission, not a bulk script:

1. `git mv <scratch-ws>/missions/<id> <real-ws>/missions/<id>` (history moves
   with the chain — receipts reference workspace-relative paths, which now
   resolve against the governed repo).
2. `resume` in the real workspace: every receipt whose path did not exist in
   the scratch workspace reports RECEIPT-MISSING/drift; reconcile per the
   existing contract (`acknowledge-loss` for unreceiptable history, fresh
   effects to re-cover). Nothing is re-minted.
3. Missions that cannot be made to resolve (paths meaningless in the real
   repo) stay where they are, completed or cancelled in place, and the scratch
   convention is retired for NEW missions by this design (open no longer
   refuses, so the pressure that created it is gone).

## 6. Record and epoch impact

- **receipt@1 unchanged — because the new field is DROPPED, not because a
  reader would tolerate it.** The frozen design claimed `sibling_touch` was
  "within the existing tolerant-reader rules"; that claim was false and is
  deleted (FATAL-1, CONFIRMED including a live falsifier; settled by OD-3).
  No tolerant-reader rule exists for receipts in either direction:
  `RECEIPT_FIELDS` is closed and exact (unknown AND missing keys both fail,
  `verify_mission_custody.py:263-266`, `:291-298`, `:511-513`), enforcement
  is at write time (`custody_store.py:81-84`, `:209-212`), and the schema
  declares `additionalProperties: false` (`receipt.schema.json:8`). A
  same-version writer cannot mint the record at all — the question of an
  older reader never arises. contract@2 is off the table per OD-3.
- **checkpoint@1 unchanged:** no stored binding, no new fields, no new
  statuses — the status enum stays the six of
  `verify_mission_custody.py:16`. The new reserved note prefix
  `"sibling-touched: "` is a writer-side code change
  (`_RESERVED_NOTE_PREFIXES`, `custody_mission.py:41-44`), not a record
  format change: notes are free strings in checkpoint state, and the
  reservation constrains what callers may write, not what readers accept.
- **New side-channel file:** `missions/<id>/sibling-touch.jsonl` — the
  `guard-log.jsonl` analog (§4c): append-only JSONL, outside the checkpoint
  chain, not validated by `verify_mission_custody`, best-effort writes.
- New error classes: `BindingRequired`, `BindingInvalid`, `UnionDegraded`.
  `MultipleActiveMissions` retired from CLI paths; the gate's
  inert-on-plurality branch (`custody_gate.py:305-314`) deleted.
- CLI: `--mission` on all verbs; `ZMS_MISSION_ID`; `missions list` verb
  (id, status, approved?, steward, frontier — plurality needs an enumeration
  verb; `census_missions.py` already prototypes this read). `effect` gains
  union guard evaluation before the write (OD-2, §2).

## 7. Case tables — the product space

Two tables. Table A enumerates the **guard-source axis** — per-mission
status (all six of `verify_mission_custody.py:16`, with `reopened` split by
the approval-lineage chain test, plus the two degraded store states) against
discovery, binding, and union membership. The frozen design collapsed this
axis into one "active" bucket; a gauntlet major (spot-verified F8) refuted
that. Table B enumerates **operation × active-count × binding**. Every cell
has a defined outcome; blank cells do not exist.

### Table A — mission status × discovery × binding × union (guard-source)

| # | latest status (lineage) | active for load? | bindable? | guards in union? | subject to union? |
|---|---|---|---|---|---|
| A1 | draft (never approved) | yes (`custody_mission.py:1018-1019`) | yes — own steward works it (`_EFFECT_STATES`, `:23`) | **NO** (OD-4) | yes |
| A2 | reopened (never approved — drift on a draft, `:1427-1434`) | yes | yes | **NO** — chain test (`:1420-1445`), not latest-status | yes |
| A3 | active | yes | yes | yes | yes |
| A4 | reopened (approved lineage) | yes | yes | yes | yes |
| A5 | verifying | yes | yes — but `effect` is status-illegal (`_EFFECT_STATES` excludes verifying, `:23`) | yes — guards keep binding the fleet while it verifies | yes (for its remaining legal verbs) |
| A6 | completed | no | no — `BindingInvalid` | no | n/a |
| A7 | cancelled | no | no — `BindingInvalid` | no | n/a |
| A8 | unreadable dir (StoreError/ValueError skip, `:1003-1017`) | skipped | no — `BindingInvalid` | **absent** — handled per B17/B22/B23, never silently | n/a |
| A9 | EpochSkew store | unreadable to this reader | no | unknown to this reader — gate inert-loud (unchanged), open refuses (B18) | n/a |

### Table B — operation × active missions × binding

"lifecycle" rows resolve per-verb through the status gates Table A and §0
name (`_OPEN_STATES`/`_EFFECT_STATES`/exact-status transitions,
`custody_mission.py:22-23`, `:1492`, `:1502`, `:1586`, `:2002`, `:2265`);
no row below claims a verb succeeds in a status where the core refuses it.

| # | active | binding | operation | outcome |
|---|---|---|---|---|
| 1 | 0 | none | open | opens (draft); prints binding line |
| 2 | 0 | none | lifecycle | NoActiveMission (unchanged) |
| 3 | 0 | none | gate | allow, mode per no-mission today (unchanged) |
| 4 | 0 | valid-id | any | BindingInvalid — nothing to bind to; never silently unbound |
| 5 | 1 | none | open | opens SECOND mission (draft — union-inert until approve, OD-4); overlap disclosure; prints binding line |
| 6 | 1 | none | lifecycle | resolves to the one active (today's flow preserved) |
| 7 | 1 | none | gate | union of that mission if approved; a lone unapproved draft contributes nothing (OD-4) — allow, disclosed as "no approved mission guards" |
| 8 | 1 | valid | lifecycle | bound mission (same as 6 when ids coincide) |
| 9 | 1 | stale/bad | lifecycle | BindingInvalid, names found state; NO fallback to the one active |
| 10 | N | none | open | opens N+1th (draft); disclosure vs every active sibling |
| 11 | N | none | lifecycle | BindingRequired, lists ids + channels |
| 12 | N | none | gate | UNION over approved missions; all matching (mission, rule) pairs named; log to each |
| 13 | N | valid | effect (status legal per A-row) | union-evaluated BEFORE `_write_effect` (OD-2); block refuses side-effect-free naming all (mission, rule) pairs; allowed → write + receipt + B21 |
| 14 | N | valid | gate | UNION still (binding routes authority, not exposure — OD-1) |
| 15 | N | stale/bad | lifecycle | BindingInvalid; NO fallback to union or to any mission |
| 16 | N | stale/bad | gate | UNION (gate never trusts binding for exposure; bad binding logged) |
| 17 | any | any | open w/ unreadable sibling dir | refuse unless --acknowledge-unreadable |
| 18 | any | any | open w/ EpochSkew sibling | refuse (unchanged) |
| 19 | N | valid | resume | drift vs own receipts; sibling-receipt handling per B26–B28 |
| 20 | N | valid | accept | bound mission only; scope-ack semantics unchanged; sibling receipts on a crossed path surface as findings, ack'd per existing kinds |
| 21 | N | valid | effect crossing an active sibling's receipted path | after 13 allows: write + receipt in B; append advisory line to sibling's `sibling-touch.jsonl` (best-effort, loud on failure, never blocks — §4c); sibling's chain untouched |
| 22 | N | any | gate, sibling dir became unreadable mid-session | allow (hook fail-open stands) with union-degraded disclosure in reason + stderr naming the dir and that its guards are NOT enforced (§2) |
| 23 | N | valid | effect, sibling dir became unreadable mid-session | refuse `UnionDegraded` naming the dir, until repair or recorded acknowledgement (§2) |
| 24 | N incl. armed never-approved draft/reopened | any | gate or effect matching ONLY that mission's guards | allow — never-approved guards are not in the union (OD-4, chain test); nothing evaluated, nothing logged for it |
| 25 | same as 24, after `approve()` lands | any | same call | the guard now blocks/audits per its mission's guard_mode — approval is the arming event (OD-4 mirror of 24) |
| 26 | N | valid | resume in A: drifted artifact hash-matches a NEVER-APPROVED sibling's receipt | plain drift at today's severity + sibling receipt reported as evidence; NO DRIFT-SIBLING downgrade (FATAL-3 leg 2) |
| 27 | N | valid | resume in A: hash-matches APPROVED sibling's receipt, no cross-mission authorization amendment in A | plain drift + evidence; NO downgrade (FATAL-3 leg 3) |
| 28 | N | valid | resume in A: hash-match + approved sibling + authorization amendment in A | `DRIFT-SIBLING(mission, receipt)`; reconciled by acknowledgement; machine note `sibling-touched: …` in A's chain by A's session |
| 29 | any | any | caller note/amend/cancel text imitating `sibling-touched: ` in any bypass shape | refused by `_refuse_reserved_note` (`custody_mission.py:47-101`) |
| 30 | N | valid | note / amend / frontier under a union guard that would block effect on the same surface | recorded, never blocked — unblockable audit channels BY DESIGN (OD-2); reserved-prefix and append-only-chain guards still apply |

Mirror rows the tables force (per the fixes-open-holes discipline): 4 vs 9
(bad binding with nothing active vs one active — both refuse, different
messages); 12 vs 14 (unbound vs bound gate — SAME exposure, different audit
routing); 6 vs 11 (the convenience of one active must not survive into N, or
binding is optional forever); 24 vs 25 (the SAME guard inert then armed —
approval is the only edge, OD-4); 26/27 vs 28 (each discriminator leg has a
row where it alone withholds the downgrade — the false-CLEAN twin is
enumerated, not assumed); 21 vs 23 (readable vs unreadable sibling on the
same crossing); 13 vs 30 (actuation gated, audit unblockable — the OD-2
boundary drawn as adjacent rows); A1/A2 vs A3/A4 (never-approved vs approved
lineage — latest status alone cannot tell them apart, the chain test can).

## 8. What this deliberately does not do

- No scheduler, no locks, no queueing (§4 fairness rationale).
- No gating of `note`, `amend`, or `frontier` — BY DESIGN, per OD-2: they
  are unblockable audit channels (§2); a design that let a guard silence
  the discharge-and-escalation record would fail its own audit floor.
- No cross-WORKSPACE missions (out of es#173's scope; the scratch migration
  §5 is the bridge back, not a feature).
- No stored session registry: binding lives in the session's environment; the
  store never records who is bound (a stored binding goes stale the moment a
  terminal closes, and stale authority records are worse than none).
- No new receipt or checkpoint fields, no new statuses, no epoch bump
  (OD-3; §6).
- No change to acceptance separation, amendment append-only, chain hashing.

## 9. Test obligations (implementation gate)

Every row of BOTH case tables becomes at least one test; additionally:

- byte-identity of gate runs (existing invariant) under N missions, AND
  byte-identity of every sibling's checkpoint chain across
  `sibling-touch.jsonl` appends (§4c — the side channel must be provably
  outside the chain);
- the §2 exposure property as an adversarial test: a bound session attempts
  an actuator guarded only by an approved sibling — MUST block (OD-1);
- the OD-2 boundary as a paired test: the same union guard blocks `effect`
  side-effect-free (no bytes written, no receipt minted) while `note` and
  `amend` on the same surface succeed and are recorded;
- the OD-4 arming pair: an armed never-approved draft blocks nothing; the
  identical call blocks the moment `approve()` lands; and the
  never-approved-`reopened` variant (drift a draft first) also blocks
  nothing — the chain test, not latest status, must be what the
  implementation reads;
- the FATAL-3 laundering test: adversary opens a throwaway sibling
  (unverified refs, `custody_mission.py:887-897`), effects the tampered
  bytes, and A's resume must report plain drift — no DRIFT-SIBLING offer —
  on both the never-approved leg and the missing-authorization leg;
- the `sibling-touched: ` forgery test across every documented bypass
  shape: leading space, capital, leading newline, machine note on the
  second line, and Cf-character smuggling (`custody_mission.py:47-101`), on
  every caller-text surface (`note`, `amend`, `cancel`, verdict reasons);
- receipt@1 closure regression: the implementation never attempts a receipt
  field outside `RECEIPT_FIELDS` (a fixture receipt from a pre-change store
  round-trips byte-identically);
- mid-session unreadable-sibling behaviour: gate discloses union
  degradation in reason + stderr; `effect` refuses `UnionDegraded` (B22/B23);
- scope-overlap disclosure determinism.

Self-authored tests are not the merge gate; the v6 assurance program's
release process and operator sign-off govern the merge (repo convention:
main has no branch protection — the only gate is the one we build).
