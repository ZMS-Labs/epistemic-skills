# Live proportionality arms: BLOCKED

Status recorded: 2026-07-23

The runnable protocol, five pinned arms, isolated fixture inputs, invocation
profile, hashing, raw-response retention, and deterministic scorer are present.
No live result is claimed.

| Arm | Status | Required runs |
|---|---|---:|
| `main-80eb0827` | `NOT_RUN` | 1 |
| `pr46-candidate-a4f2210f` | `NOT_RUN` | 3 |
| `candidate-final-4e1945e` | `NOT_RUN` | 3 |
| `full-ceremony` | `NOT_RUN` | 1 |
| `always-routine` | `NOT_RUN` | 1 |

## Missing capability

This execution context does not expose a primitive that can launch the pinned
model/provider/harness combination in a fresh, isolated repository-aware
context once per fixture while withholding the scorer, ground truth, other
fixtures, and other arms. The available collaboration mechanism shares task
context and does not prove the required isolation; it is therefore not a valid
substitute. Repository tests can validate packet construction and scorer
polarity, but cannot manufacture model behavior.

## Closure

Run `runner.py prepare` from the final protocol checkout with `--source-root`
pointing at each exact arm commit, invoke every packet through the pinned
isolated harness, retain the unedited response files, and run `runner.py score`.
Candidate repetitions must remain separate. Failures and dissent must be kept,
not retried away. Until then, OUT-011 behavioral execution is blocked and no
population-effect claim is supported.
