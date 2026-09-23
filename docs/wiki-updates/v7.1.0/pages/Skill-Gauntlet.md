> **Applies to:** epistemic-skills v7.1.0.

# Gauntlet

**Put a consequential proposal through plural scrutiny and adjudication.**

Gauntlet examines a common, versioned subject through distinct evaluative questions, checks the findings against evidence, and reconciles the material tensions. Constructive improvements matter alongside objections. For an open decision, option generation precedes evaluation and includes the strongest case for doing nothing.

**Use it when:** An architecture, governance choice, or other consequential decision benefits from multiple examinations and a reasoned judgment; or you explicitly request that review.

**Use something simpler when:** The task is routine code review, a reversible edit, one focused concern, or diagnosis of a reproducible failure.

### Illustrative request

> Review this storage migration before we commit to it. Consider rollback, operating cost, and the assumptions behind the availability claim.

**What a useful result looks like:** A scoped GO, CONDITIONAL, or NO-GO, supported findings, preserved dissent, coverage limits, and the conditions that could change the judgment. Unresolved evidence must remain visible.

**Boundary:** Shared models or context constrain independence. Another model family is optional; an applicable external gate still retains its own authority. A verdict does not authorize an otherwise unauthorized action.

[Perspective](Skill-Perspective.md) handles focused examination; [Resolve](Skill-Resolve.md) can supply missing decision evidence.

[Read the canonical v7.1.0 method](https://github.com/ZMS-Labs/epistemic-skills/blob/v7.1.0/plugins/epistemic-skills/skills/gauntlet/SKILL.md) · [All methods](Skill-Catalog.md)
