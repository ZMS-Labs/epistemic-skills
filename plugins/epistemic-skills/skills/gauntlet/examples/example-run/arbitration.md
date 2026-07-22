# Arbitration — adopt a handoff-receipt schema (SYNTHETIC EXAMPLE — not a real run)

Two lens reports entered arbitration; the other three seated lenses
(century-horizon-architect, tech-debt-curator, explainability-steward) reported no
P1–P4 findings. The exploration seat (concurrency-interleaving-auditor) ran as
SHADOW: its report was withheld from arbitration and its findings are excluded from
the verdict.

## Conflict ledger

- **F1 vs ship-as-is** — integration-weaver's closed-vocabulary finding has a named
  mechanism and a mechanically runnable falsifier; the draft's evidence supports it.
  Ruled UPHELD, open → blocking P2.
- **F2** — compliance-litigator's session-identity concern is answered by the draft
  itself (keyed-hash token). Ruled OVERRULED on the cited evidence, resolved.
- **F3** — retention rule for stale receipts: real but minor, and partially covered
  by the validity-window semantics. Ruled UPHELD-WITH-QUALIFICATIONS, resolved.

The ruling-set@1 block below is the writable home of the verdict; the run record
and the ledger line derive from it (finalize_run.py), they never restate it.

```json
{
  "ruling_set": "ruling-set@1",
  "synthetic": true,
  "rulings": [
    {
      "id": "F1",
      "lens": "integration-weaver",
      "priority": "P2",
      "basin": "closed-vocabulary-extension",
      "ruling": "UPHELD",
      "status": "open",
      "acceptance_criteria": [
        {
          "condition": "An extension procedure for the closed valid_while vocabulary is documented in the contract README: predicates are added only by schema-version bump plus verifier release in the same PR.",
          "falsifier": {
            "method": "grep the contract README for an extension-procedure section",
            "threshold": "section present, naming schema-version bump + same-PR verifier release",
            "timeframe": "before the schema merges"
          },
          "owner": "schema-author"
        }
      ]
    },
    {
      "id": "F2",
      "lens": "compliance-litigator",
      "priority": "P2",
      "basin": "session-identity",
      "ruling": "OVERRULED",
      "status": "resolved",
      "acceptance_criteria": []
    },
    {
      "id": "F3",
      "lens": "compliance-litigator",
      "priority": "P3",
      "basin": "stale-receipt-retention",
      "ruling": "UPHELD-WITH-QUALIFICATIONS",
      "status": "resolved",
      "acceptance_criteria": []
    }
  ],
  "computed_verdict": "CONDITIONAL",
  "next_action": "Land the F1 extension-procedure condition, then the schema merges; F3 rides as a one-line doc note."
}
```
