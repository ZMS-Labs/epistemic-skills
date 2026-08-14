# Security notes — mission-custody@1

- Records are DATA. Instructions embedded in manifests, notes, or reasons are
  never executed by validators or custody tooling (prompt-injection seam).
- The verifier checks shape and closed-vocabulary semantics only; it does not
  attest that hashes correspond to real artifacts — that is the custody core's
  runtime job (drift detection on resume).
- `acceptance-verdict@1` enforces role separation at the record level
  (acceptor != worker; operator tier binds acceptor to operator_ref). It
  cannot bind principals outside the record channel: an authorized human
  acting outside the mission channel is out of scope and must not be claimed
  as prevented.
- Receipts are hashed, not signed. No third-party-verifiable claim is made.
- Receipt visibility is ASYMMETRIC by design, and deleting a receipt file is
  not equally visible in both cases. Deleting the CURRENT receipt for a path
  is caught: `resume` reports `RECEIPT-MISSING`. Deleting a SUPERSEDED one is
  not, and if that superseded receipt was the far side of a continuity break,
  the break becomes invisible to every reporting surface -- `resume` only
  consults the current receipt per path, and `continuity_breaks()` will not
  assert a mismatch across a receipt it cannot load. The alternative
  (bridging the gap and comparing the surviving neighbours) was rejected on
  evidence: against an honest history where an intervening write legitimately
  changed the content and its receipt was later lost, the neighbour-to-
  neighbour hash comparison such an implementation would perform was computed
  by hand from the real receipts, and it does not match -- it would report a
  break that never happened. No bridging code was written and run; that
  comparison is arithmetic over recorded hashes, which is the whole of what
  the implementation would do. Deleting receipt files requires filesystem access
  outside the mission channel, which this document already places out of
  scope; this entry names the asymmetry so it is a known property rather than
  a rediscovery.

## Scope comparison: hard links are DETECTED, never RESOLVED

`scope_consistency()` compares two spellings of each receipted artifact: the
path recorded in the chain, and where that path resolves. Resolution follows
symlinks. **A hard link is not a link to a path — it is a second name for one
inode — and `realpath` cannot see it.** Measured: `docs/alias.txt` hard-linked
to `secrets/data.txt`, an effect on the alias, `scope.out=["secrets/**"]` — the
comparison returned clean while `secrets/data.txt` held the new bytes.

What the contract now does is prove the *condition*: a receipted artifact whose
`st_nlink > 1` is reported as `multiply linked -- other names are not compared`,
and a PASS is refused until an acceptor acknowledges it. What it does **not**
do is find the other name, so it cannot tell you whether that name sits inside
`scope.out`. A file does not know its own aliases; locating them means walking
the workspace and grouping by `(st_dev, st_ino)`.

That walk is deliberately not taken, on a measurement rather than a preference.
Per call on the reference box:

| receipts | workspace files | `st_nlink` probe | full walk | `scope_consistency()` |
|---|---|---|---|---|
| 100 | 2,302 | 1.9 ms | 63 ms | 699 ms |
| 400 | 9,202 | 9.2 ms | 294 ms | 10,783 ms |
| 800 | 22,402 | 24.8 ms | 817 ms | 41,487 ms |

The probe costs 0.06 % of the call it lives in, so nothing argues against
detection. The walk's cost scales with the **workspace**, which is unrelated to
the mission's size: at ~100k files and 20 receipts it is seconds against a
`scope_consistency()` of milliseconds. Precise resolution is therefore a
contract change with its own cost profile, not something to smuggle into the
acceptance path — the same call es#147 made for recording the resolved path at
write time.

**Operator consequence:** when acceptance reports MULTIPLY LINKED, the other
name has not been checked against any boundary. Find it (`fsutil hardlink list`
on NTFS, `find -samefile` on POSIX) before acknowledging, and acknowledge it
in the QUALIFIED spelling — `accept … --scope-ack linked:<path>` — never the
bare path: a boundary crossing and a link disclosure are different
judgements, and the bare spelling discharges only the former. An
acknowledgement here records that a human looked, which is the only thing
that is true.

## Glob anchoring: `\Z` in the compiler, `$` residue in operator regexes

Every glob this contract compiles (`scope.in`/`scope.out` comparison, guard
`path_globs`, amendment discharge tokens) is anchored with `\Z`, never `$`:
`$` also matches just before a trailing newline, so the glob `safe.txt`
matched the distinct file `safe.txt\n` — a path one byte outside a
declaration reading as inside it.

`command_regexes` are the residue: they are **operator-authored Python
regexes**, applied verbatim with `re.search`. A rule author who writes a
trailing `$` gets Python's semantics, including the one-newline tolerance —
rewriting an author's pattern would trade a documented seam for a silent
divergence between what the author wrote and what runs. If a single trailing
newline matters to a command guard, write `\Z` in the rule. This tolerance is
disclosed here rather than patched because the pattern language belongs to
the author; the globs are this contract's own language, so their compiler is
where the guarantee lives.

## OPERATOR NOTICE — trailing-slash guard globs now bind the subtree

A `path_globs` entry ending in `/` (or `\`) is a **directory marker**: it now
matches the directory and everything under it. It previously normalized to an
exact name and matched almost nothing — an armed guard declaring `M:/Media/`
silently allowed every write under `M:/Media/`. The same reading covers the
**workspace and root spellings**: `.`, `./`, `.\` and `./.` (previously inert
— they normalized to the empty path and matched nothing) now match every
target, and `/` (previously root-only) now matches every absolute target. A
literal empty-string entry is a placeholder, not a marker, and stays inert as
before. **On upgrade, an armed guard with any of these spellings becomes MORE
restrictive.** If a guard starts blocking calls it previously allowed, that
is this change working; the block names its rule, and the discharge is an
ordinary `amend`. This is the same
directory-marker reading `scope.in`/`scope.out` entries and amendment
discharge tokens already use. (es#155, landed per the es#150 adjudication —
which mandated this distinct notice rather than a silent landing.)

## Stage-C hook: fail-open and guard-tamper residue

The PreToolUse custody hook is an enforcement layer over convention, not a
sole barrier. Every supported harness fails open on hook error, timeout, or
crash (Kimi documents this explicitly; Claude's contract is the same), so a
broken hook silently reverts enforcement to convention-held. Denial travels
only via the deliberate exit-2 / decision-JSON path.

Guard matching is deliberately over-broad: a false block names its rule and
is discharged by an `amend`; a false allow silently retires custody of the
actuator class.

A guard change relative to the chain-protected previous checkpoint without a
NEW recorded authority amendment since that checkpoint is detected as
manifest tampering (reverting guards to the origin spelling, or riding on an
earlier unrelated amendment, does not evade this). A guard change accompanied
by a FORGED amendment on the unsealed tail checkpoint is the same residue
class as amendment fabrication today; the structural fix (tail anchor) is
tracked as es#118.

**The unsealed tail also bounds receipt binding.** `_load_receipt` refuses a
receipt whose `artifact_path` disagrees with the `effect:` note the chain
recorded for that request id, which is what stops a receipt copied from
another workspace from silencing drift detection. That binding is only as
trustworthy as the note. Both facts are measured, not assumed:

- An **interior** note cannot be rewritten. Editing one breaks the hash
  chain, `load_latest()` raises `ChainBroken`, and discovery skips the store
  entirely — verified.
- A **tail** note can. For an id introduced by the LATEST checkpoint, a
  writer who can replace the receipt can also rewrite that note to match the
  decoy, and `resume()` returns clean over a drifted artifact — verified.

So the binding raises the bar (the attacker must now write the checkpoint
too, not just drop a file in `receipts/`) without closing the hole for
tail-introduced ids. It is the same es#118 residue as forged amendments, and
the same tail anchor closes both. Ids introduced by any earlier revision are
fully protected — **for the PATH. Not for the BYTES.**

### RECEIPT FILES ARE UNAUTHENTICATED DATA

The chain records which artifact an id was minted against. It records
nothing about the artifact's CONTENT, so nothing binds `after_sha256` to
history. Measured, with no second workspace involved and no checkpoint
touched: an attacker who can write `receipts/` edits `after_sha256` in place
to the hash of the tampered bytes, and `resume()` returns clean over the
tampered artifact.

That is worth stating plainly because the narrower framings understate it —
this needs no donor mission, no matching mission_id, no copied file. **Write
access to `receipts/` is write access to what drift detection believes.**
Everything `_load_receipt` checks (schema, content-addressed id, mission id,
chained path) constrains WHICH RECORD may speak for an id; none of it
constrains what that record says about bytes, because the record is
unsigned and the chain never hashed it.

The fix is structural and belongs to es#118: bind receipt digests into the
checkpoint chain, so the hash an auditor checks against is one the attacker
cannot rewrite without breaking the chain. It is deliberately NOT attempted
as another `_load_receipt` refinement — no check inside that function can
authenticate data the chain never covered, and four consecutive rounds of
tightening it produced one regression that falsely reported drift on honest
work (see the round-8 backslash defect). **Consumers should treat receipt
hashes as trustworthy exactly as far as they trust write access to the
mission directory** — which is the same boundary the guard-log and the
unsealed tail already sit behind.

## A NEWER EPOCH DISARMS A STALE READER — the migration's own first write

`RECORD_KINDS` is a **closed** set: a record from a newer contract epoch is not
degraded by this reader, it is refused, exactly like corruption. That refusal is
correct and stays. The consequence downstream is not.

**Measured.** An armed `enforce` mission blocks a guarded call. Rewrite its tail
`record` to `checkpoint@2`, leave everything else byte-identical, and the same
call returns `allow` — the store fails validation, `Mission.load` skips it, and
the workspace reports `NoActiveMission`. Before this was named, the verdict
handed back to the harness said `gate inert: NoActiveMission`, which is false:
the mission is present and active, and the READER is old. On an allow path, the
stderr line carrying the real cause is also the channel least likely to reach
anyone.

**Why it matters more than an ordinary skip.** This is not an exotic corruption
case; it is the expected steady state during a contract@2 rollout (es#118). At
the first `@2` write, every workspace whose consumer is stale silently retires
every guard it holds — the upgrade itself is the disarm. That is why the es#150
ruling makes a **version-aware degraded reader, fleet-wide** an engineering
precondition of the first `@2` write, not a nicety to follow it.

**What now happens.** `MissionStore.load_latest` raises `EpochSkew` (a
`ChainBroken` subclass, so every existing handler keeps its behavior byte for
byte); `run_gate` names the skew on the verdict and on stderr instead of
reporting an empty workspace; the census discloses every skewed store and marks
the run partial. It reports the **ROOT** as fail-open with cause
`STALE READER (newer contract epoch)` **only when no other active mission
resolves there** — a skewed store beside a readable active mission does not
disarm the root, since `Mission.load` skips the skewed store and the gate still
blocks (measured). The skewed mission's own guards are unenforced either way;
see "Scope is per MISSION, not per root" below, which is the authority on what
the census prints for a given root.

**What deliberately does NOT happen.** The posture is not inverted. Refusing to
run on skew would strand every workspace it applies to with no verb to resolve
it — the same objection es#173's kernel 3 raises against shipping the fail-open
inversion without a duplicate-resolution verb in the same change. The skew is
disclosed; the fail-open underneath it is unchanged and still owed a fix.

**What the skew signal does NOT establish.** This reader has no validator for
a newer epoch, and `validate_record` short-circuits on the unknown kind — so
when the skew fires, *nothing else about the record has been checked*. A
`{"record": "checkpoint@2"}` with every required field absent is
indistinguishable here from a genuine future record. An earlier version of this
disclosure told the operator the store was "not corrupt … repair nothing",
which is an assertion this reader cannot make and an attacker can exploit:
relabel a corrupt or tampered tail as a newer epoch and the corruption
diagnosis is replaced by advice to leave it alone. The signal means the record
**claims** a newer epoch. Read it with an updated consumer to learn whether that
claim is true.

**Where the claim is honoured, and why the position matters.** Records embed
records: a `checkpoint@1` carries a `mission-manifest` the schema requires to
be `@1`, so a store can be too new while its outer kind looks familiar — an
armed mission whose embedded manifest says `@2` was reported `ChainBroken` and
went inert as `NoActiveMission`, the silent diagnosis this signal exists to
replace. The fix for that first walked **every** nested dictionary, which
widened the attack above rather than closing it: planting
`{"record": "checkpoint@2"}` in `state` — a plain object that cannot hold a
record — made a tampered checkpoint report as a stale reader and sent the
operator to upgrade instead of to look at the damage (measured, with
`written_by` corrupted alongside). The epoch claim is therefore honoured
**only at schema-declared record positions** (`EMBEDDED_RECORD_PATHS`), and a
test reads the `.schema.json` files and fails if a `$ref` position is not
listed — staleness is caught in CI rather than by an operator acting on a
wrong verdict. A `record` key anywhere else is data, and data does not get to
say what this reader may skip.

**Scope is per MISSION, not per root.** A skewed store beside a readable active
mission does not disarm the root — `Mission.load` skips the skewed store and the
gate still blocks (measured). The skewed mission's own guards are unenforced
either way; the census now says which of the two situations a given root is in.

## Discovery ambiguity DISARMS the gate — an unarmed decoy is enough

**Verified live (es#173 adjudication, 2026-08-13):** an armed mission with
`guard_mode: enforce` and a `secrets/**` rule blocks a matching call. Add a
**second, entirely unarmed** mission directory under the same workspace root
and the identical call returns `allow` / `mode: inert`. `run_gate` catches
`MultipleActiveMissions` and fails open by design — a hook must never brick
the tool loop on discovery ambiguity — but the consequence is that **any
second active mission, carrying no guards at all, silently retires every
guard in that workspace.**

`Mission.open` refuses to create the second one **sequentially** — but that
refusal is a check-then-write with no lock between the two steps, so it does
NOT hold under concurrency. Verified live: two `Mission.open` calls racing on
an empty workspace (each completing the `Mission.load` preflight before
either wrote revision 1) both returned successfully, leaving `m-1` and `m-2`
active, after which `Mission.load` raises `MultipleActiveMissions` and every
guard in that workspace is retired. **Concurrent opens are therefore a
reachable ambiguity path through the supported surface**, alongside the
out-of-band routes (a filesystem write, a sync, a restored backup, a copied
mission dir, or a symlinked duplicate of one store).

Serializing open is not attempted here: the obvious lock file introduces a
stale-lock wedge that bricks every future open in the workspace after a
crash — a new dead-end recipe of exactly the class this document already
tracks — and the es#173 adjudication ruled NO-GO on adopting any concurrency
design this cycle. It is named, not fixed, and the census reports the
resulting state (`Q1 FAIL-OPEN REACHABILITY`) wherever it has already
happened. Three further properties make this worth naming rather than
assuming:

- **"Active" is broad.** A mission counts as active unless its status is
  `completed` or `cancelled` — so a mission parked in `verifying`
  indefinitely both holds the workspace's only slot and, if duplicated,
  disarms it.
- **There is no supported repair.** Every CLI verb except `open` and `gate`
  sits below a single `Mission.load` call, which raises on ambiguity. Once a
  workspace holds two active missions, no verb can resolve it; the fix is a
  filesystem action outside the contract.

**Operator consequence:** treat "how many active missions are under this
root?" as a security question, not housekeeping. A guard set that reads as
armed is only armed while that answer is exactly one.

## An acceptance PASS certifies the mission's receipts, not the workspace

`scope_consistency()` compares the artifacts THIS mission receipted against
THIS mission's declared scope. It says nothing about writes made by another
mission, by a session acting outside custody, or by a human — and with
concurrent missions under nested roots (which the contract permits today,
one per root) each mission's PASS is silent about every artifact the other
one touched. "This mission declared its scope and nothing crossed it" is the
claim; "nothing crossed this boundary in this workspace" is not.

## Effect-phrased boundaries are UNENFORCED

Only `authority.actuator_guards` (with `guard_mode`) reaches the runtime
chokepoint. `stop_rules` (`hold_if` / `stop_if` / `escalate_if`),
`protected_state`, and `permissions` are **declarations a human reads**:
nothing evaluates them, at any point, ever. This matters most for the
missions whose real boundaries are conditions on effects — "do not expose
secret material", "do not merge pull requests", "do not improvise platform
privileges" — because those cannot be expressed as the path/tool/command
patterns `evaluate()` matches on. A mission whose genuine constraints live in
`stop_rules` has a record that makes a violation **attributable**, not one
that makes it **impossible**. Closing that gap is tracked as es#166 and is
explicitly NOT what concurrent-mission work (es#173) addresses.

## Stage-C hook: discovery scope, log sensitivity, mixed-fleet hazard

Mission discovery walks up from the payload's cwd to the nearest ancestor
holding `missions/`. A payload cwd OUTSIDE the workspace tree (or a harness
that reports no cwd) finds nothing and the gate stays inert: the hook covers
work reported from inside the mission's tree, not work reported from
elsewhere.

Guard-log command previews (`command_preview`, up to 120 chars of the matched
command) may carry secrets embedded in command lines, and mission dirs ride
sync/commit flows -- treat `guard-log.jsonl` as sensitive at the same level
as shell history.

Arming guards on a mission writes `actuator_guards` / `guard_mode` into that
mission's checkpoints, and pre-#117 plugin caches cannot validate those
fields: their stores will read the armed mission's checkpoints as
ChainBroken (or skip the mission as unreadable). On a mixed fleet, update
ALL custody consumers to the #117-or-later plugin before arming guards on
any shared mission.

## Verbatim text and the argv channel

`amend` records the operator's VERBATIM grant, and `open --instruction` records
the mission's founding instruction. Both, plus `note`/`frontier`/`--reason`,
accept text inline on the command line -- where a shell can rewrite the string
BEFORE the contract ever sees it. Backticks and `$(...)` are command
substitution, `$VAR` expands, and argv caps near 32K chars on Windows.

That corruption is invisible to every guarantee this contract provides: the
mangled string is validated, hashed, chained, and (under contract@2) anchored,
all faithfully -- the record is intact and wrong. Observed live: backticks in a
double-quoted shell string silently rewrote a recorded note while the CLI
exited 0.

Use the `--*-file` variants for anything whose exactness matters, and always
for `amend`. They remove exactly two editor artifacts and nothing else: a
leading UTF-8 BOM (PowerShell writes one by default, and U+FEFF is not
whitespace, so it otherwise lands as the first character of a "verbatim"
grant) and ONE trailing line terminator. Interior bytes -- including CRLF and
deliberate blank lines -- are preserved exactly. A file that is not valid
UTF-8 is refused with exit 2 rather than crashing, since PowerShell's bare
`Out-File` writes UTF-16LE.
