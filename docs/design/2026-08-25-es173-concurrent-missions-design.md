# es#173 — Concurrent missions: session→mission binding with union guards

**Status:** DESIGN FOR GAUNTLET — the 2026-08-15 operator adjudication requires
a full gauntlet on this document before any implementation. Nothing here is
built. **Subject freeze:** this file at its commit sha is the gauntlet subject.

**Adjudicated model (verbatim constraint):** *"explicit session→mission binding
with union fallback. A session declares which mission it acts under; calls
without a binding are checked against the UNION of all active missions' guards
— any mission may block, and the block names its mission and rule. Fail-safe by
construction: no silent disarm."*

**The four questions the adjudication ordered answered:** binding mechanics ·
coexistence without false drift · fairness/coordination on shared artifacts ·
migration of the scratch-workspace missions. Each has a section; the case table
covers the product space.

---

## 0. Grounding — what the shipped core does today (read at `488f252`)

- `Mission.open` refuses at the door if `load()` finds ANY active mission
  (`custody_mission.py:911-941`). Refusal happens before any write.
- `Mission.load` resolves exactly one active mission; two or more raises
  `MultipleActiveMissions` (`custody_mission.py:1031-1034`).
- `custody_gate.run_gate` catches `MultipleActiveMissions` and returns
  `{"decision": "allow", "mode": "inert"}` — loud on stderr, but ALLOW
  (`custody_gate.py:305-314`). This is the fail-open surface: the state the
  contract forbids is also the state that disarms its own enforcement.
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

`MultipleActiveMissions` as a load-failure class is retired from these paths;
it survives only as an internal distinction inside `load` for the gate.

## 2. Guard evaluation — union ALWAYS; binding routes authority, not exposure

The adjudication's floor: unbound calls are checked against the union. This
design goes one step stricter, and the gauntlet should attack exactly this
choice: **guard evaluation is union over all active missions' armed guards for
EVERY call, bound or not.**

Rationale: binding routes *authority* — where effects/receipts/notes land,
whose amendments can discharge a block, whose frontier moves. It must not
route *exposure*: if binding to mission A exempted a call from mission B's
guards, then the moment two missions coexist, every guard becomes voluntary —
choose the mission whose guards don't cover your actuator and act. That is the
A1 undifferentiated-override failure in session clothing.

Semantics:
- A block names `(mission_id, rule)` of every matching guard (all matches, not
  first — the operator discharging the block needs the full bill).
- Discharge stays per-mission: an amend recorded in mission B discharges B's
  rule only. A call blocked by A and B needs both. THIS is the coordination
  mechanism (§4) — cross-mission conflict surfaces as two named rules, not as
  a race.
- Guard-log append goes to EVERY matching mission's `guard-log.jsonl`
  (each mission's audit trail must be complete from its own dir).
- `guard_mode` is per-mission and applies to that mission's own rules.
- Unguarded missions contribute nothing to the union (unchanged semantics).
- Gate discovery failures keep today's honest-inert behaviour for corrupt or
  epoch-skewed stores — but `MultipleActiveMissions` disappears as an inert
  cause, because plurality is no longer a failure. **The fail-open decoy is
  removed not by handling the error better but by making the state legal.**

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

Mechanism — **sibling attribution at effect time**:
- `effect` (in B, bound) checks whether the path is receipted by any OTHER
  active mission. If yes, the receipt B mints gains
  `sibling_touch: [{mission: A, last_receipt: <id>}]`, and a paired note is
  appended to A's state (`sibling-touched: <path> by <B> receipt <id>`), so
  BOTH chains carry the crossing. A's note append is a state write, not a
  checkpoint rewrite — the same channel `note` already uses.
- `resume` (in A) on a drifted artifact consults active siblings' receipts for
  the path: content-hash match against a sibling's receipt reports
  `DRIFT-SIBLING(mission=B, receipt=<id>)` — reconciled by acknowledging the
  sibling receipt (recorded), not by `acknowledge-loss` (nothing was lost).
  No sibling receipt matches → plain drift, exactly today's severity.
- **Fairness:** no locks. Single-operator estate; the cost of a lock manager
  exceeds the cost it prevents. The union guard + sibling attribution makes
  simultaneous writes VISIBLE and attributable; the operator remains the
  scheduler. The gauntlet should test whether visible-but-unserialised is
  sufficient at this estate's concurrency level (measured: 2–4 concurrent
  sessions, one operator).

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

- `checkpoint@1` unchanged: no stored binding, no new required fields. The
  additive receipt field `sibling_touch` and state notes are within the
  existing tolerant-reader rules (verify: older reader must skip unknown
  receipt fields — if it refuses instead, this design forces contract@2 and
  says so honestly; the gauntlet must check the shipped reader's behaviour).
- New error classes: `BindingRequired`, `BindingInvalid`. `MultipleActiveMissions`
  retired from CLI paths; the gate's inert-on-plurality branch deleted.
- CLI: `--mission` on all verbs; `ZMS_MISSION_ID`; `missions list` verb
  (id, status, steward, frontier — plurality needs an enumeration verb;
  `census_missions.py` already prototypes this read).

## 7. Case table — the product space

Axes: active missions in workspace (0 / 1 / N) × binding (none / valid /
stale-or-bad) × operation (open / lifecycle verb / gate call). Every cell has
a defined outcome; blank cells do not exist.

| # | active | binding | operation | outcome |
|---|---|---|---|---|
| 1 | 0 | none | open | opens; prints binding line |
| 2 | 0 | none | lifecycle | NoActiveMission (unchanged) |
| 3 | 0 | none | gate | allow, mode per no-mission today (unchanged) |
| 4 | 0 | valid-id | any | BindingInvalid — nothing to bind to; never silently unbound |
| 5 | 1 | none | open | opens SECOND mission; overlap disclosure; prints binding line |
| 6 | 1 | none | lifecycle | resolves to the one active (today's flow preserved) |
| 7 | 1 | none | gate | union of 1 = today's behaviour |
| 8 | 1 | valid | lifecycle | bound mission (same as 6 when ids coincide) |
| 9 | 1 | stale/bad | lifecycle | BindingInvalid, names found state; NO fallback to the one active |
| 10 | N | none | open | opens N+1th; disclosure vs every active sibling |
| 11 | N | none | lifecycle | BindingRequired, lists ids + channels |
| 12 | N | none | gate | UNION; all matching (mission, rule) pairs named; log to each |
| 13 | N | valid | lifecycle | bound mission; effect gains sibling_touch on cross-receipted paths |
| 14 | N | valid | gate | UNION still (binding routes authority, not exposure) |
| 15 | N | stale/bad | lifecycle | BindingInvalid; NO fallback to union or to any mission |
| 16 | N | stale/bad | gate | UNION (gate never trusts binding for exposure; bad binding logged) |
| 17 | any | any | open w/ unreadable sibling dir | refuse unless --acknowledge-unreadable |
| 18 | any | any | open w/ EpochSkew sibling | refuse (unchanged) |
| 19 | N | valid | resume | drift vs own receipts; sibling-receipt match → DRIFT-SIBLING |
| 20 | N | valid | accept | bound mission only; scope-ack semantics unchanged; sibling receipts on a crossed path surface as findings, ack'd per existing kinds |

Mirror rows the table forces (per the fixes-open-holes discipline): 4 vs 9
(bad binding with nothing active vs one active — both refuse, different
messages); 12 vs 14 (unbound vs bound gate — SAME exposure, different
audit routing); 6 vs 11 (the convenience of one active must not survive into
N, or binding is optional forever).

## 8. What this deliberately does not do

- No scheduler, no locks, no queueing (§4 fairness rationale).
- No cross-WORKSPACE missions (out of es#173's scope; the scratch migration
  §5 is the bridge back, not a feature).
- No stored session registry: binding lives in the session's environment; the
  store never records who is bound (a stored binding goes stale the moment a
  terminal closes, and stale authority records are worse than none).
- No change to acceptance separation, amendment append-only, chain hashing.

## 9. Test obligations (implementation gate, post-gauntlet)

Every case-table row becomes at least one test; additionally: byte-identity of
gate runs (existing invariant) under N missions; older-reader tolerance of
`sibling_touch` (or the honest contract@2 escalation); the §2 exposure
property as an adversarial test (bound session attempts an actuator guarded
only by the sibling — MUST block); scope-overlap disclosure determinism.
Self-authored tests are not the merge gate; the v6 assurance program's
release process and operator sign-off govern the merge (repo convention:
main has no branch protection — the only gate is the one we build).
