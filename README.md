# epistemic-skills

Epistemic-discipline skills for agentic coding — how an agent **knows** things before, during, and after work.

**Harness-agnostic.** The skills are plain [Agent Skills](https://agentskills.io/specification) (`SKILL.md` + supporting files) describing *methods*, not any one tool's mechanics. They run in any harness that can load a skill or a context file — Claude Code, Codex, Cursor, Gemini, or your own agent loop. Where a step needs a runtime primitive (concurrent sub-agents, a structured-output schema, an MCP tool), the skill states the **contract** and points at a labeled *reference implementation* for one harness; other harnesses meet the same contract with their own primitives. See [Using these in any harness](#using-these-in-any-harness).

Most skill collections cover the *workflow* layer: test-driven development, systematic debugging, plan writing (see [superpowers](https://github.com/obra/superpowers), which these compose with). This collection covers the layer underneath: the disciplines that keep an agent's claims tethered to evidence and its effort aimed at the real target.

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

### Claude Code (plugin marketplace) — one command

```
/plugin marketplace add ZMS-Labs/epistemic-skills
/plugin install epistemic-skills@epistemic-skills
```

That installs all six skills as a single package. Each one **self-triggers** — it
activates only when its own `description` matches the task, so you get à-la-carte
behavior from a one-command install; you're never paying attention-cost for a skill a
task doesn't need.

### Codex (plugin marketplace)

```powershell
codex plugin marketplace add ZMS-Labs/epistemic-skills --ref main
codex plugin add epistemic-skills@epistemic-skills
```

The repository includes native Claude and Codex manifests backed by the same skill
files. Harness-specific packaging does not fork the methods or their supporting
resources.

### Using these in any harness

The skills are just files. They live under `plugins/epistemic-skills/skills/<name>/` — a
`SKILL.md` plus any references, scripts, and role-agent definitions — following the
[Agent Skills spec](https://agentskills.io/specification), so any harness that reads
skills or context files can use them. Point your agent at the whole `skills/` directory
(the trivial integration) or a single `SKILL.md`:

```bash
npx skills add https://github.com/ZMS-Labs/epistemic-skills/tree/main/plugins/epistemic-skills/skills
```

- **Point your agent at the `SKILL.md`.** Its frontmatter `description` is the trigger
  ("use when…"); the body is the method. Load it as a skill, an `AGENTS.md`/`GEMINI.md`
  include, a Cursor rule, or plain context.
- **Meet the contract, not the tool.** A few skills need a runtime primitive. Each states
  the harness-agnostic contract and labels its Claude Code implementation as a *reference*:
  - **gauntlet** Step 5 wants *concurrent, context-isolated role-agents behind a barrier*.
    Any parallel-subagent primitive works; with none, use the documented degrade fallback
    (sequential isolated calls). Role-agent definitions are in each plugin's `agents/`
    directory — register them however your harness registers agents, or inline the persona
    text if it has no agent concept.
  - **evidence-locked-uat** wants the *actor / blinded-verifier / deterministic-judge*
    roles kept in separate contexts — same subagent story.
  - **evidence-research** needs the Consensus and/or Scite tools (MCP); identify them by
    server, not by any harness's tool-naming. It degrades explicitly when one is absent.
  - **applying-formal-rigor** and **blindspot-pass** are pure method — no runtime
    dependency at all.
- **`using-epistemic-skills`** is the router; read it first to see which skill a task needs
  and how their outputs chain.

The scripts (`gauntlet/scripts/*.py`) are stdlib-only Python and run anywhere Python does.

## Design principles

- **Floors, not ceilings.** Each skill states the minimum acceptable rigor for its moment, not a maximal process.
- **Derive, don't assert.** A conclusion is earned by a chain from named theory or read evidence; "it's better" is an opinion.
- **End at the boundary.** blindspot-pass ends at understanding (it never implements); applying-formal-rigor ends at a derived verdict. Skills that know where they stop compose cleanly.
- **Anti-rationalization tables.** Each skill enumerates the exact excuses an agent under pressure uses to skip it, with counters.

These skills are extracted from a private fleet where they run as standing discipline, hardened by daily use and adversarial review.

The gauntlet's honest status is stated in its own roadmap section. Shipped and validated: the staple, the falsifiability contract, mechanical evidence checks, the deterministic selector, and — as of 2026-07-17 — the **certified-arbitrator battery**, which runs the arbitrator blind against 10 planted defect classes it must catch and scored **10/10 (certified at standard rigor)**; the battery, scorer, and results are in [`evals/arbitrator-certification/`](plugins/epistemic-skills/skills/gauntlet/evals/arbitrator-certification/) so the claim is reproducible. Still partial: the behavioral battery has only a smoke subset run (non-inferiority, not superiority); the full sweep and the later measurement bundle remain designs — stated as such, never claimed done.

## License

MIT — see [LICENSE](LICENSE).
