# DeepReason Integration For Sovereign-Gauntlet

## Role Boundary

DeepReason is a pre-panel exploration engine. Sovereign-Gauntlet remains the governance verdict engine.

DeepReason may propose:

- rival explanations,
- failure theories,
- falsifiers,
- discriminating tests,
- red-team cases,
- unresolved conflicts.

DeepReason must not:

- set GO / NO-GO,
- bypass evidence verification,
- satisfy a separate red-team gate,
- override P1/P2 semantics,
- convert hypotheses into verified facts.

## When To Run The Docket

Run a docket when the subject is open-ended and the panel would benefit from a richer attack surface:

- architecture choices,
- incident root-cause explanations,
- irreversible infra changes,
- legal/governance charters,
- security posture changes,
- product readiness questions with multiple plausible blockers.

Skip a docket when:

- the task is a direct factual lookup,
- the failure is already deterministic and reproducible,
- the operator requested a quick narrow review,
- no falsifiable structure can be stated.

## How To Feed The Panel

Do not paste a huge docket into every prompt. Extract:

- top 3-7 survivor theories,
- killed theories that prevent wasted panel time,
- the strongest falsifier for each survivor,
- discriminating tests likely to become P1/P2,
- red-team cases that need concrete validation.

Add a short "DeepReason Docket Excerpt" section to each lens prompt. Tell each lens it may attack the docket itself.

## Arbitration Treatment

The arbitrator should treat docket items as:

- replay-backed evidence only when a real run root/log exists and is cited,
- structured hypotheses when the docket is manual,
- prompts for verification, not verdicts.

Any surviving theory that would change the decision should appear in the Conflict Ledger or P1/P2 matrix.

