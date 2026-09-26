> **Applies to:** epistemic-skills v7.2.0.

# Health

**Report what is working, what is degraded, and what could not be observed.**

Health compares a declared set of running subjects against explicit bounds. It returns OK, WARN, CRITICAL, or UNKNOWN with the observations behind each result. An unreachable probe is an observation gap, not a healthy service.

**Use it when:** You need a current operational picture, including before a consequential change or after a restart.

**Use something simpler when:** A specific failure is already known and you need its cause, or reading one directly available metric would answer the question.

### Illustrative request

> Check the services involved in this rollout against their declared readiness and latency bounds. Include anything you cannot observe.

**What a useful result looks like:** A time-scoped readout with subject coverage, measured values, applicable bounds, and unknowns. A roll-up cannot silently remove failed probes or imply unexamined services were healthy.

**Boundary:** A healthy service may still be using stale configuration. Health assesses current state and does not diagnose a fault or authorize repairs.

[Triage](Skill-Triage.md) investigates a known failure; [Did It Land](Skill-Did-It-Land.md) checks a change; [Watch](Skill-Watch.md) commissions observation between sessions.

[Read the canonical v7.2.0 method](https://github.com/ZMS-Labs/epistemic-skills/blob/v7.2.0/plugins/epistemic-skills/skills/health/SKILL.md) · [All methods](Skill-Catalog.md)
