# Superseded — a live epoch has run

The original justification here ("no live behavioral epoch has been run
against these fixtures") was retired on 2026-08-04: the first live epoch is
committed at [`2026-08-04/`](2026-08-04/RESULTS.md) — outcome **FAIL, 8/10**
(two reporting-contract failures over behaviorally-correct conduct, diagnosed
in the record). Committing the failing epoch rather than re-running until it
passes is the house norm, same as committing BLOCKED was. Follow-up contract
clarifications and the second epoch are tracked in issue #77.
