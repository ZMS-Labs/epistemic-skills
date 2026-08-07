# `watch-commission@1`

`watch-commission@1` is the durable carrier emitted by the `watch`
commissioning discipline. It keeps current operating state, historical proof,
blocking evidence, observed failure, and external evidence references separate.

## What the two validators prove

- `watch-commission.schema.json` defines the closed structural carrier.
- `verify_watch_commission.py` enforces the cross-field state machine, required
  evidence-reference presence, closed state/direction/substrate/failure/reason
  vocabularies, block-reason consistency, proof completeness, fixture scope,
  re-proof boundaries, and refusal of obvious prompt/session/self-asserted
  evidence references.
- `test_watch_commission.py` requires the published schema and semantic verifier
  to expose the same fields and closed enums, then exercises accepted and rejected
  controls.

## What they do not prove

The schema and semantic verifier **do not dereference, authenticate, or
independently establish the truth of an external receipt**. A syntactically
acceptable `receipt_ref` remains a claim about evidence until the consumer
resolves it against the named source of truth and verifies that it supports the
field carrying it.

They also do not prove that:

- a production scheduler, monitoring provider, listener, or human cadence is
  actually installed;
- an external mechanism is currently running merely because its identifier is
  well formed;
- a timestamp or condition string is fresh in the consumer's present context;
- a fixture result transfers to an untested production environment; or
- an alert recipient will act correctly after delivery.

A load-bearing consumer therefore performs two distinct checks:

1. validate the record structurally and semantically; and
2. resolve each material evidence reference against the real external system,
   authority source, probe output, destination receipt, or incident record.

Only the second check can turn a reference into verified evidence about the
world. Failure or inability to resolve a material reference degrades the
commission; it never upgrades silence into success.


## Handoff semantics

`handoff.on_crossing` is a closed post-crossing classification containing
exactly `triage` and `decision-ledger`; array order has no meaning. It identifies
the two epistemic disciplines that may consume a **real crossing** after the
external observer reports one. It does not compel either discipline to fire —
each still owns its positive trigger — and it does not name the system that
stores or operates the commission.

Optional mission-control custody is a separate outward transport concern and
remains explicit/generic until a consumer publishes, verifies, and admits a
versioned `watch-commission@1` intake contract. The carrier therefore rejects
`manifest` or any other custody target in `handoff.on_crossing` and implies no
automatic routing to Practical Agency or any other package.
