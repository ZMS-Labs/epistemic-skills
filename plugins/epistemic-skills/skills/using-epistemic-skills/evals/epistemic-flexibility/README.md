# epistemic-flexibility conformance battery

A deterministic, stdlib-only **protocol conformance smoke check** for the cross-cutting controls in `reference/epistemic-flexibility.md`.

It is not a behavioral effectiveness measurement and does not estimate how often a model will apply the controls in real work. It validates structured synthetic traces and rejects planted protocol defects.

## Defect classes

- fused observation without a source;
- proxy metric without a named proxy-failure mode;
- post-hoc experiment interpretation;
- forced action on a load-bearing unverified claim;
- recurrent correction without a failure chain.

Two controls must also pass:

- a complete high-information trace;
- a minimal low-stakes trace, proving the protocol remains a floor rather than mandatory ceremony.

## Usage

```bash
python run_tests.py
python validate_trace.py fixtures/valid-complete.json
python validate_trace.py --json fixtures/invalid-forced-closure.json
```

The validator returns 0 for a conforming trace, 1 for a non-conforming trace, and 2 for malformed input or CLI errors.
