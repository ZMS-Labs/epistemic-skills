# epistemic-skills

Epistemic-discipline skills for [Claude Code](https://claude.com/claude-code) — how an agent **knows** things before, during, and after work.

Most public skill collections cover the *workflow* layer: test-driven development, systematic debugging, plan writing (see [superpowers](https://github.com/obra/superpowers), which these skills are designed to compose with). This collection covers the layer underneath: the disciplines that keep an agent's claims tethered to evidence and its effort aimed at the real target.

**Start with `using-epistemic-skills`** — the router. It answers *which* of these applies to a given task, in *what order*, and how each one's output feeds the next. The five below are the disciplines it routes to; install the router plus whichever ones you want.

## The arc

The skills are one system — *how an agent knows things* before, during, and after work — with each ending at a defined boundary and handing off to the next:

```
 recon              decide                     gate               prove
 blindspot-pass  →  applying-formal-rigor   →  gauntlet        →  evidence-locked-uat
 (rewrites the      (derives the design;       (computed          (blinded verdict on
  request)           evidence-research          GO/NO-GO on         a finished UI change)
                     grounds any premise)       a frozen subject)
```

Most tasks fire zero or one. The router's value is the case where more than one applies.

## Skills

| Skill | What it disciplines |
|---|---|
| **using-epistemic-skills** | The entry point. Routes a task to the right discipline(s), sequences them (recon → design → evidence → gate → verify), and defines the handoff contracts so the skills compose without overreaching. Read it first; it never does the work itself. |
| **applying-formal-rigor** | Design *and complexity* decisions. Sets a graduate-level formal-theory floor: name the *precise* construct (the exact normal form, the named isolation anomaly, the Master-Theorem case, the Ω lower bound), **derive** the conclusion instead of asserting it, and sweep every relevant lens. Ships a 7-lens theory battery; lens 4 is a full standalone Big-O / complexity analysis (recurrences, lower bounds, optimization convergence). |
| **blindspot-pass** | The moment *before* work begins. A cheap read-only reconnaissance pass that surfaces landmines, hidden context, exemplars, and the questions an expert would ask — then **rewrites the request** so downstream work aims at the territory, not the map. Technique from Thariq Shihipar (Anthropic), *"A Field Guide to Claude Fable 5: Finding Your Unknowns"* (2026). |
| **evidence-research** | Claims about *the literature*. Two engines answering different questions: **Consensus** discovers what the literature says; **Scite** interrogates how each paper was *received* — supporting vs contrasting citation statements, retractions and editorial notices. Consensus finds the witnesses; Scite runs the cross-examination. Prevents the worst failure: citing a refuted or retracted paper as support. Requires the Consensus and/or Scite MCP connectors; degrades explicitly and visibly when one is absent rather than quietly narrowing its claims. |
| **evidence-locked-uat** | Claims that UI-facing work is *done*. No agent certifies its own work: the actor drives, a **blinded verifier** judges from evidence alone, and the judge is deterministic script code. Per-case evidence packets, triage tiers, and a strict verdict vocabulary where `INCONCLUSIVE` is reported as `INCONCLUSIVE` — never rounded up to PASS. Ships the full standard and agent directive it operationalizes. |
| **gauntlet** | High-stakes decision points. A multi-lens adversarial panel reviews a *frozen* subject: a truth-gated dossier, rival failure modes each naming their own falsifier, independent lens passes from a 102-persona registry (deterministic, constraint-checked selection), mechanical evidence verification (`[V path:line]` anchoring, oracle-adequacy checks), a dissent-preserving Conflict Ledger, and a **computed** GO/CONDITIONAL/NO-GO — the reviewer cannot simply assert a verdict. Ships with the full roster, role agents, orchestration template, and a tested deterministic selector. |

## Install

```
/plugin marketplace add ZMS-Labs/epistemic-skills
/plugin install using-epistemic-skills@epistemic-skills
/plugin install applying-formal-rigor@epistemic-skills
/plugin install blindspot-pass@epistemic-skills
/plugin install gauntlet@epistemic-skills
/plugin install evidence-research@epistemic-skills
/plugin install evidence-locked-uat@epistemic-skills
```

Each skill is a separate plugin — install only what you want.

## Design principles

- **Floors, not ceilings.** Each skill states the minimum acceptable rigor for its moment, not a maximal process.
- **Derive, don't assert.** A conclusion is earned by a chain from named theory or read evidence; "it's better" is an opinion.
- **End at the boundary.** blindspot-pass ends at understanding (it never implements); applying-formal-rigor ends at a derived verdict. Skills that know where they stop compose cleanly.
- **Anti-rationalization tables.** Each skill enumerates the exact excuses an agent under pressure uses to skip it, with counters.

These skills are extracted from a private fleet where they run as standing discipline, hardened by daily use and adversarial review.

The gauntlet's honest status is stated in its own roadmap section: the staple, falsifiability contract, mechanical evidence checks, and the validated deterministic selector are shipped; the certified-arbitrator battery and behavioral regression battery are designed but not yet built or run.

## License

MIT — see [LICENSE](LICENSE).
