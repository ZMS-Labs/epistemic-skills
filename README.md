# epistemic-skills

<!-- ZMS-ESTATE:BEGIN -->

> **Estate status:** `maintenance` · **Purpose:** `governance_method` · **Portfolio role:** `none`
> **Canonical for:** epistemic-agent-skill-package
> Lifecycle authority: `ZMS-Labs/zms-homelab/governance/estate.yaml`.

<!-- ZMS-ESTATE:END -->

Epistemic-discipline skills for agentic coding — how an agent **knows** things before, during, and after work.

**Version 2.9.1.** **License: [GPL-3.0-or-later](LICENSE).**

**Harness-agnostic.** The skills are plain [Agent Skills](https://agentskills.io/specification) (`SKILL.md` + supporting files) describing *methods*, not any one tool's mechanics. They run in any harness that can load a skill or a context file — Claude Code, Codex, Cursor, Gemini CLI, Antigravity, Kimi Code, or your own agent loop. Where a step needs a runtime primitive (concurrent sub-agents, a structured-output schema, an MCP tool), the skill states the **contract** and points at a labeled *reference implementation* for one harness; other harnesses meet the same contract with their own primitives. See [Using these in any harness](#using-these-in-any-harness).

Most skill collections cover the *workflow* layer: test-driven development, systematic debugging, plan writing (see [superpowers](https://github.com/obra/superpowers), which these compose with). This collection covers the layer underneath: the disciplines that keep an agent's claims tethered to evidence and its effort aimed at the real target. The `helix` skill is the pairing map for running the two layers in tandem.

Across the arc, five **epistemic-flexibility controls** separate claims from sources,
operator-authorized priorities from success proxies, predictions from post-hoc stories,
recurrent failures from their earliest interruptible links, and unresolved uncertainty from
forced closure. They are cross-cutting controls inside the existing skills — **not another
skill or trigger**. Functional definition, evidence limits, and the deterministic conformance
battery: [`using-epistemic-skills/reference/epistemic-flexibility.md`](plugins/epistemic-skills/skills/using-epistemic-skills/reference/epistemic-flexibility.md).

**Start with `using-epistemic-skills`** — the router. It answers whether the task should leave through the routine path or enter one or more disciplines, in what order, and how each output feeds the next. The package ships **eleven** skills: the router, the **nine** disciplines it routes to, and **helix** — the tandem entry point that pairs those disciplines with a workflow-skill layer such as superpowers. Install once; each skill self-triggers only when its own `description` matches.

## Routine work first

The collection is not a requirement to convene a review process for every edit.
A task stays on the **routine path** when it is all four of:

1. reversible by an ordinary revert;
2. local — no security, privacy, authorization, tenancy, billing, legal,
   infrastructure, network, public-contract, migration, or cross-service boundary;
3. directly checkable by a targeted test, local preview, deterministic reproduction,
   or comparably bounded observation; and
4. non-precedential — no unresolved decision, scholarly premise, authorization, or
   cross-session judgment must be preserved.

For unfamiliar routine-looking territory, open the target artifact and its nearest
test/example. If they agree with the request and the four conditions still hold, make
the change and run the bounded check. **Do not emit router or Helix skip inventories,
a blindspot report, a formal record, a ledger entry, a UAT packet, or another process-
only artifact.** Escalate only when the first reads expose a positive trigger.

Normative details and examples:
[`routine-fast-path.md`](plugins/epistemic-skills/skills/using-epistemic-skills/reference/routine-fast-path.md).
The structural proportionality battery lives at
[`evals/proportionality/`](plugins/epistemic-skills/skills/using-epistemic-skills/evals/proportionality/).

## The arc

The nine disciplines are one system — *how an agent knows things* before, during, and after work — with each ending at a defined boundary and handing off to the next:

```
routine: reversible + local + directly checkable + non-precedential
         → change + bounded check; no process-only artifact

resume (pre-arc):  continuity-verify  (the summary is a claim, not a state — re-anchor or stamp)
        │
 recon              decide                  contract          gate             prove
 blindspot-pass  →  applying-formal-rigor → write-goal     → gauntlet       → evidence-locked-uat
 (rewrites the      (derives the design;     (binds intent    (computed         (blinded verdict on
  request)           evidence-research        to proof and     GO/NO-GO on        a material finished
                     grounds any premise)     stop rules)      a frozen subject)  UI change)

persist (cross-cutting): decision-ledger records a consequential moment only when an
   existing durable plan/ADR/issue/PR/goal/derivation does not already satisfy the consumer

delegate (cross-cutting): outsource commits a context-complete repo packet + short prompt,
   then records every external response in the repo before the next turn
```

Most tasks clear the routine gate or fire zero or one discipline. The router's value is the case where more than one applies.

## Skills

| Skill | Role |
|---|---|
| **using-epistemic-skills** | **Router** (not a discipline). Applies the routine gate, then routes positive triggers to the right discipline(s), sequences them (recon → decide → [evidence] → contract → gate → prove), and defines handoff contracts. Read it first; it never does the work itself. |
| **helix** | **Tandem entry point** (not a discipline). When a workflow-skill layer (such as superpowers) runs alongside this collection, helix pairs workflow stages with positively triggered epistemic disciplines. Routine and absent pairs are silent. |
| **applying-formal-rigor** | Software-and-systems property analysis and decision synthesis. Focused questions stay within six bullets/250 words; material forks use an open-world P1-P9 inventory, specialist modules, applicability proofs, and revision-bound `formal-rigor-record@2` output. |
| **blindspot-pass** | Full read-only reconnaissance after micro-recon exposes a material map/territory mismatch, hidden coupling, unresolved scope, or fan-out risk. It surfaces landmines, context, examples, and expert questions, then rewrites the request. Unfamiliarity alone is not the full-pass trigger. |
| **evidence-research** | Claims about *the literature*. **Consensus** discovers; **Scite** interrogates *reception* (supporting/contrasting citations, retractions); **Zotero** (durable library) does holdings-check + deposit so the org keeps a curated shelf. Prevents citing a refuted/retracted paper as support **and** rediscovering what the library already holds. Requires the triad in tandem; degrades explicitly when a layer is absent. |
| **write-goal** | Explicit requests to author or start a persistent goal. Converts intent into an approved completion contract with goal-type selection, direct proof plus anti-proxy and provenance guards, scope and blocker policy, interruptibility, and opt-in budgets. Adapted from Kimi Code's built-in `write-goal` and strengthened with a documented research basis. |
| **outsource** | External model/agent/process handoff. Writes the complete workload context and completion contract to `docs/outsource/<work-id>/HANDOFF.md`, commits it at an exact GitHub ref, emits a short copy/paste pointer, and records every return relay in-repo before it bears load. |
| **evidence-locked-uat** | Claims that material UI-facing work is *done*. Actor drives; a **blinded verifier** judges from evidence alone; the judge is deterministic script code. Strict verdict vocabulary: `INCONCLUSIVE` is never rounded up to PASS. Routine directly checkable presentation changes use their bounded preview/test instead of constructing a full packet. |
| **gauntlet** | High-stakes decision points. Multi-lens adversarial panel on a *frozen* subject: truth-gated dossier, falsifiers, deterministic selection, mechanical `[V path:line]` evidence checks, Conflict Ledger, and computed GO/CONDITIONAL/NO-GO. It is not ordinary code review. |
| **decision-ledger** | The arc's **persistence** moment. Reuses an adequate durable ADR/plan/issue/PR/goal/derivation when one exists; otherwise appends `ledger-entry@1` for a consequential decision, load-bearing assumption, or recurrent correction. Never a verdict; readers re-anchor, never trust. |
| **continuity-verify** | The **resumption** moment — fires first when a session resumes from a compaction summary, handoff note, or prior-session task whose next action depends on remembered state. It re-anchors load-bearing claims and emits a state digest. Its quick mode keeps trivial resumptions small. |

## Layout

```
epistemic-skills/                         # repo root
├── plugins/epistemic-skills/
│   ├── skills/<name>/SKILL.md            # canonical skill cores (eleven)
│   ├── contracts/                        # handoff-receipt contract: schema, stdlib verifier, synthetic examples
│   ├── agents/                           # gauntlet role-agents (five)
│   ├── .claude-plugin/plugin.json
│   ├── .codex-plugin/plugin.json
│   └── .cursor-plugin/plugin.json
├── skills/  → plugins/epistemic-skills/skills/    # symlink (Gemini / root scanners)
├── agents/  → plugins/epistemic-skills/agents/    # symlink
├── .claude-plugin/marketplace.json
├── .agents/plugins/marketplace.json      # Codex marketplace index
├── .cursor-plugin/plugin.json            # Cursor whole-repo plugin
├── .cursor-plugin/marketplace.json       # Cursor team-marketplace index
├── gemini-extension.json + GEMINI.md     # Gemini CLI extension
├── .kimi-plugin/plugin.json              # Kimi Code plugin (points at the same skills tree)
└── plugin.json                           # Antigravity native plugin
```

One tree of method files; harness-specific manifests only. Do not fork the skills per harness.

## Install

Install with **exactly one** mechanism per harness. A second copy of the same skills (for example `npx skills add` on top of a plugin install) produces duplicate triggers.

### Claude Code

```
/plugin marketplace add ZMS-Labs/epistemic-skills
/plugin install epistemic-skills@epistemic-skills
```

### Codex

```powershell
codex plugin marketplace add ZMS-Labs/epistemic-skills --ref main
codex plugin add epistemic-skills@epistemic-skills
# Register the five gauntlet roles in Codex's user-agent registry:
python "$HOME/.codex/plugins/cache/epistemic-skills/epistemic-skills/2.9.1/skills/gauntlet/scripts/render_codex_agents.py" --out "$HOME/.codex/agents"
```

Start a new Codex task after rendering the roles. Codex plugin manifests do not
currently register custom collaboration-agent types themselves; the renderer
bridges the canonical packaged Markdown roles into Codex's native user-agent
TOML registry. The gauntlet also retains a hashed exact-role materialization
fallback for a task started before registration.

### Cursor

**Status:** packaging is ready (`.cursor-plugin/` manifests, version 2.9.1). The plugin is **not yet listed** on the public [Cursor Marketplace](https://cursor.com/marketplace); `/add-plugin epistemic-skills` works only after Cursor lists it or you import the repo as a [team marketplace](https://cursor.com/docs/plugins). Publisher application: [cursor.com/marketplace/publish](https://cursor.com/marketplace/publish).

| Path | When to use |
|---|---|
| Local install (below) | Personal / fleet / until marketplace listing |
| Team marketplace import of this GitHub repo | Cursor Teams/Enterprise private distribution |
| Public marketplace `/add-plugin` | After Cursor accepts the publisher listing |

**Local install:**

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

Then **Developer: Reload Window**. Success check: all eleven skills under Customize → Skills, and auto-trigger on matching prompts (for example an irreversible / stress-test ask should surface the router or `gauntlet`).

Do **not** also install these skills into `~/.cursor/skills/` while the plugin is loaded.

### Gemini CLI

```bash
gemini extensions install https://github.com/ZMS-Labs/epistemic-skills --consent
# local dev:
gemini extensions link /path/to/epistemic-skills
```

Restart the Gemini session after install/link. Entrypoints: `gemini-extension.json`, `GEMINI.md`, root `skills/` symlink. Validated with `gemini extensions validate`.

### Antigravity (`agy`)

Native plugin marker is root [`plugin.json`](plugin.json) (Antigravity schema: `name` + `description`). Same `skills/` / `agents/` tree:

```bash
agy plugin install https://github.com/ZMS-Labs/epistemic-skills
# or:
agy plugin install /path/to/epistemic-skills
agy plugin validate /path/to/epistemic-skills
```

Prefer **one** of: native `agy plugin install`, Gemini extension link, or `agy plugin import gemini` — not several copies.

### Kimi Code

```text
/plugins install https://github.com/ZMS-Labs/epistemic-skills
# local dev, from a clone:
/plugins install /path/to/epistemic-skills
```

Run `/reload` or start a new session after install. Entrypoint: root `.kimi-plugin/plugin.json`, which points at the same canonical `plugins/epistemic-skills/skills/` tree; its `skillInstructions` carries the Kimi tool mapping (gauntlet role agents and the UAT actor/verifier/judge dispatch through the `Agent` tool in isolated contexts). If the plugin manager is unavailable, junction the skills into the user skills directory instead — pick exactly one mechanism:

```powershell
Get-ChildItem .\plugins\epistemic-skills\skills -Directory | ForEach-Object {
  New-Item -ItemType Junction -Path "$env:USERPROFILE\.kimi-code\skills\$($_.Name)" -Target $_.FullName
}
```

### Using these in any harness

The skills follow the [Agent Skills spec](https://agentskills.io/specification). Point your agent at `plugins/epistemic-skills/skills/` (or the root `skills/` symlink) or a single `SKILL.md`:

```bash
npx skills add https://github.com/ZMS-Labs/epistemic-skills/tree/main/plugins/epistemic-skills/skills
```

Use this **only** when the harness has no native plugin/extension install.

- **Frontmatter `description`** is the trigger; the body is the method.
- **Apply the routine gate before loading a process container.** A missing optional skill does not block reversible, local, directly-checkable work; a missing discipline at a positive high-stakes boundary does.
- **Meet the contract, not the tool.** Runtime needs:
  - **gauntlet** Step 5: concurrent, context-isolated exact-role agents behind a barrier (degrade: sequential isolated calls). Definitions in `agents/`; runtimes without plugin-defined custom-agent registration use the replayable materialized-role adapter documented in `skills/gauntlet/reference/runtime-role-binding.md`.
  - **evidence-locked-uat**: actor / blinded-verifier / deterministic-judge in separate contexts for material acceptance runs.
  - **evidence-research**: Consensus + Scite MCP + durable library (Zotero or equivalent — identify by server / Web API / LOCAL.md host); degrade explicitly when a layer is absent.
  - **write-goal**: persistent-goal inspection/creation plus a user-question primitive when the harness provides them; otherwise it returns the approved contract without pretending to start it.
  - **outsource**: repository read/write plus Git/GitHub publication and verification when available; without a pushed, target-readable packet it returns `BLOCKED`, never a ready-looking prompt.
  - **applying-formal-rigor** and **blindspot-pass**: pure method — no runtime dependency.
- **`using-epistemic-skills`** is the router; read it first.

Gauntlet scripts (`skills/gauntlet/scripts/*.py`) are stdlib-only Python.

## Design principles

- **Floors, not ceilings; proportional cost.** Routine work leaves before the arc. Extra process earns no credit unless it can expose an action-changing error.
- **Derive, don't assert.** Conclusions are earned from named theory or read evidence.
- **Language carries claims, not automatic truth or authority.** Separate observation,
  interpretation, prediction, value, and authorization before a claim bears load.
- **End at the boundary.** Each skill stops where the next begins.
- **Absent triggers are silent.** Audit consequential actions and overrides, not non-events.
- **Fail closed; degrade explicitly.** Missing load-bearing tools yield visible limits — never a silent pass; preserve uncertainty with hold, escalation, or a bounded reversible probe.

## Gauntlet status (honest)

Full map: [`skills/gauntlet/reference/roadmap.md`](plugins/epistemic-skills/skills/gauntlet/reference/roadmap.md).

**Shipped and validated:** staple, falsifiability contract, mechanical evidence checks, deterministic selector, and — as of 2026-07-17 — the **certified-arbitrator battery** (arbitrator blind against 10 planted defect classes; **10/10 catch, certified at standard rigor**). Battery, scorer, and results: [`evals/arbitrator-certification/`](plugins/epistemic-skills/skills/gauntlet/evals/arbitrator-certification/).

**Still partial:** behavioral regression battery has only a smoke-subset run (non-inferiority, not superiority); the full 24×4 sweep and later measurement bundles remain designs — stated as such, never claimed done. (Smoke-run notes are not published as a standalone file in this repo.)

## License

[GPL-3.0-or-later](LICENSE) — GNU General Public License, version 3 or (at your option) any later version.
