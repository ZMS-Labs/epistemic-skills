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
