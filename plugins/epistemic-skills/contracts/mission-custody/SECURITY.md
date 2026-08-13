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
on NTFS, `find -samefile` on POSIX) before acknowledging. An acknowledgement
here records that a human looked, which is the only thing that is true.

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
