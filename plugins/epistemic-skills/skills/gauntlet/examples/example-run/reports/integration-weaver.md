# Lens report — integration-weaver (SYNTHETIC EXAMPLE — not a real run)

**Finding F1 (P2):** the draft closes the `valid_while` predicate vocabulary
[V handoff-receipt.schema.json:11] but the contract names no extension procedure —
a predicate that does not fit has no path in, so consumers will fork the vocabulary
silently and receipts will diverge per repo.
- Mechanism: closed vocabularies without a documented extension path accumulate
  out-of-band additions; interop fails at the seam the schema was meant to protect.
- Evidence: the enum is exhaustive at [V handoff-receipt.schema.json:11]; no
  extension rule appears anywhere in the frozen dossier's evidence root.
- Falsifier: {statement: "an extension procedure is documented for `valid_while`",
  method: "grep the contract README for an extension-procedure section",
  threshold: "section present, naming schema-version bump + same-PR verifier release",
  timeframe: "before the schema merges"}
- Proposed action: add the extension procedure to the contract doc. The repo's own
  convention that a schema change and its verifier release land in the same PR
  [V skills-repo-conventions.md:5] is the natural rule to adopt [I <- V1, V2].
