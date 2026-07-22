# Lens report — compliance-litigator (SYNTHETIC EXAMPLE — not a real run)

**Finding F2 (P2):** a receipt schema that persists session material is a privacy
liability if the identifier is raw. The draft's `session` field is described as a
keyed-hash equality token, never a raw session id [V handoff-receipt.schema.json:12] —
so as drafted the exposure is closed. Recorded so arbitration can rule it OVERRULED
on the evidence rather than silently dropped. (An example of a finding that *should*
be overruled: the mechanism is real, the draft already mitigates it.)
- Falsifier: {statement: "no raw session identifier persists in a shipped receipt",
  method: "grep shipped example receipts for raw session ids", threshold: "0 occurrences",
  timeframe: "every PR touching the schema"}

**Finding F3 (P3):** the draft states no retention rule for stale receipts
[H]. One-line falsifier: a retention paragraph appearing in the contract doc would
change this assessment.
