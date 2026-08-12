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
for `amend`. They read the bytes directly (`newline=''`, trailing newline
stripped), so the recorded text is the supplied text.
