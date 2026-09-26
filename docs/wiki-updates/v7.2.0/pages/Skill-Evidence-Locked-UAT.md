> **Applies to:** epistemic-skills v7.2.0.

# Evidence Locked UAT

**Judge acceptance against observations specified before the test.**

Evidence-Locked UAT ties material user-facing criteria to expected and disconfirming observations. It keeps the target revision, evidence coverage, verification mode, and result together, then uses the supplied deterministic judge to evaluate the evidence record.

**Use it when:** Acceptance depends on material interactions, persistence, focus, identity, responsive behavior, or explicit user-acceptance testing.

**Use something simpler when:** A reversible local presentation edit can be established with a bounded preview check. That check should remain ordinary verification.

### Illustrative request

> Check whether a keyboard-only user can change and save this setting, return later, and recover the saved value. Record what would disprove each criterion.

**What a useful result looks like:** A scoped acceptance result with observed evidence, omitted coverage, and limitations. Direct checks are labeled direct. Only actually isolated actor/verifier contexts with the actor verdict withheld can claim blinding.

**Boundary:** A deterministic judge does not make its observational inputs infallible. The shipped evaluation remains uncalibrated; source checks and screenshots alone cannot establish every interaction criterion.

[Did It Land](Skill-Did-It-Land.md) checks the consumer effect; [Write Goal](Skill-Write-Goal.md) defines the intended completion proof.

[Read the canonical v7.2.0 method](https://github.com/ZMS-Labs/epistemic-skills/blob/v7.2.0/plugins/epistemic-skills/skills/evidence-locked-uat/SKILL.md) · [All methods](Skill-Catalog.md)
