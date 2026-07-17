# epistemic-skills

Epistemic-discipline skills for [Claude Code](https://claude.com/claude-code) — how an agent **knows** things before, during, and after work.

Most public skill collections cover the *workflow* layer: test-driven development, systematic debugging, plan writing (see [superpowers](https://github.com/obra/superpowers), which these skills are designed to compose with). This collection covers the layer underneath: the disciplines that keep an agent's claims tethered to evidence and its effort aimed at the real target.

## Skills

| Skill | What it disciplines |
|---|---|
| **applying-formal-rigor** | Design decisions. Sets a graduate-level formal-theory floor: name the *precise* construct (the exact normal form, the named isolation anomaly, the consistency guarantee in the lattice), **derive** the conclusion instead of asserting it, and sweep every relevant lens instead of stopping at the first one. Ships with a 7-lens theory battery (relational, concurrency, distributed consistency, complexity, type theory, information theory, architecture formalisms). |
| **blindspot-pass** | The moment *before* work begins. A cheap read-only reconnaissance pass that surfaces landmines, hidden context, exemplars, and the questions an expert would ask — then **rewrites the request** so downstream work aims at the territory, not the map. Technique from Thariq Shihipar (Anthropic), *"A Field Guide to Claude Fable 5: Finding Your Unknowns"* (2026). |
| **gauntlet** | High-stakes decision points. A multi-lens adversarial panel reviews a *frozen* subject: a truth-gated dossier, rival failure modes each naming their own falsifier, independent lens passes from a 102-persona registry (deterministic, constraint-checked selection), mechanical evidence verification (`[V path:line]` anchoring, oracle-adequacy checks), a dissent-preserving Conflict Ledger, and a **computed** GO/CONDITIONAL/NO-GO — the reviewer cannot simply assert a verdict. Ships with the full roster, role agents, orchestration template, and a tested deterministic selector. |

## Install

```
/plugin marketplace add ZMS-Labs/epistemic-skills
/plugin install applying-formal-rigor@epistemic-skills
/plugin install blindspot-pass@epistemic-skills
/plugin install gauntlet@epistemic-skills
```

Each skill is a separate plugin — install only what you want.

## Design principles

- **Floors, not ceilings.** Each skill states the minimum acceptable rigor for its moment, not a maximal process.
- **Derive, don't assert.** A conclusion is earned by a chain from named theory or read evidence; "it's better" is an opinion.
- **End at the boundary.** blindspot-pass ends at understanding (it never implements); applying-formal-rigor ends at a derived verdict. Skills that know where they stop compose cleanly.
- **Anti-rationalization tables.** Each skill enumerates the exact excuses an agent under pressure uses to skip it, with counters.

These skills are extracted from a private fleet where they run as standing discipline, hardened by daily use and adversarial review. More are planned (scholarly evidence-research, evidence-locked UAT) as their extraction completes.

The gauntlet's honest status is stated in its own roadmap section: the staple, falsifiability contract, mechanical evidence checks, and the validated deterministic selector are shipped; the certified-arbitrator battery and behavioral regression battery are designed but not yet built or run.

## License

MIT — see [LICENSE](LICENSE).
