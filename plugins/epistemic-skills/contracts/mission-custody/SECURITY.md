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
  (bridging the gap and comparing the surviving neighbours) was constructed
  and rejected: it reintroduces false positives on the far more common honest
  history where an intervening write legitimately changed the content and its
  receipt was later lost. Deleting receipt files requires filesystem access
  outside the mission channel, which this document already places out of
  scope; this entry names the asymmetry so it is a known property rather than
  a rediscovery.
