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

**One package, many manifests, same files.** Cores live once under
`plugins/epistemic-skills/skills/` (and role-agents under
`plugins/epistemic-skills/agents/`). Root `skills/` and `agents/` are symlinks to
those paths so harnesses that only scan the repo root (Gemini CLI) still find
them. Install with **exactly one** mechanism per harness — do not also copy the
same skills into that harness's user-skills directory, or you will get duplicate
triggers.

Each skill **self-triggers** from its frontmatter `description`, so one install
gives à-la-carte behavior: you only pay attention-cost when a skill matches.

### Claude Code

```
/plugin marketplace add ZMS-Labs/epistemic-skills
/plugin install epistemic-skills@epistemic-skills
```

### Codex

```powershell
codex plugin marketplace add ZMS-Labs/epistemic-skills --ref main
codex plugin add epistemic-skills@epistemic-skills
```

### Cursor

**Recommended for personal / public use:** submit or install via the
[Cursor Marketplace](https://cursor.com/marketplace/publish) (GitHub repo
`ZMS-Labs/epistemic-skills`). Root `.cursor-plugin/plugin.json` is the
single-plugin entry point. After it is listed:

```text
/add-plugin epistemic-skills
```

Or: Customize → Plugins → browse/install **epistemic-skills**.

**Team marketplace** (Cursor Teams/Enterprise): only needed if you want
*private* org distribution. Import this same GitHub repo; `.cursor-plugin/marketplace.json`
indexes the nested plugin at `plugins/epistemic-skills/`. Public MIT users can
skip team marketplaces entirely.

**Local install (dev / before marketplace listing):**

```powershell
# Windows — from a clone of this repo
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.cursor\plugins\local" | Out-Null
$src  = (Resolve-Path .\plugins\epistemic-skills).Path
$dest = Join-Path $env:USERPROFILE '.cursor\plugins\local\epistemic-skills'
if (Test-Path $dest) { Remove-Item $dest -Force -Recurse }
cmd /c mklink /J "$dest" "$src"
```

```bash
# macOS / Linux
mkdir -p ~/.cursor/plugins/local
ln -sfn "$(pwd)/plugins/epistemic-skills" ~/.cursor/plugins/local/epistemic-skills
```

Then **Developer: Reload Window**. Success check: all six skills visible under
Customize → Skills, and they auto-trigger on matching prompts.

Do **not** also run `npx skills add` into `~/.cursor/skills/` for this package
while the plugin is installed — that is a second copy of the same triggers.

### Gemini CLI / Antigravity

```bash
gemini extensions install https://github.com/ZMS-Labs/epistemic-skills --consent
# local dev against a clone:
gemini extensions link /path/to/epistemic-skills
```

Requires a restart of the Gemini session after install/link. Root `skills/`
(symlink) is what the extension loader discovers; `gemini-extension.json` +
`GEMINI.md` are the extension entrypoints.

Antigravity can install from the same GitHub URL (`agy plugin install …`) or
import an already-linked Gemini extension (`agy plugin import gemini`). Prefer
one of those paths — not both plus a manual skills copy.

### Universal / any other harness

The skills follow the [Agent Skills spec](https://agentskills.io/specification).
Point your agent at `plugins/epistemic-skills/skills/` (or the root `skills/`
symlink) or a single `SKILL.md`:

```bash
npx skills add https://github.com/ZMS-Labs/epistemic-skills/tree/main/plugins/epistemic-skills/skills
```

Use this path **only** when the harness has no native plugin/extension install.
If you already installed via Claude, Codex, Cursor, or Gemini above, skip
`npx skills add` for those same skills.

- **Point your agent at the `SKILL.md`.** Frontmatter `description` is the trigger;
  the body is the method.
- **Meet the contract, not the tool.** A few skills need a runtime primitive. Each
  states a harness-agnostic contract and labels one reference implementation:
  - **gauntlet** Step 5: *concurrent, context-isolated role-agents behind a barrier*
    (degrade: sequential isolated calls). Role-agent definitions are in `agents/`.
  - **evidence-locked-uat**: keep *actor / blinded-verifier / deterministic-judge*
    in separate contexts.
  - **evidence-research**: Consensus and/or Scite MCP (identify by server); degrade
    explicitly when absent.
  - **applying-formal-rigor** and **blindspot-pass**: pure method — no runtime dependency.
- **`using-epistemic-skills`** is the router; read it first.

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
