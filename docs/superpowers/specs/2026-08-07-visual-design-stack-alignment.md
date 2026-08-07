# Visual design stack alignment — Fudge, Claude Design, frontend-design, Impeccable

**Date:** 2026-08-07 (Claude Design harness section added same day)  
**Status:** design draft (extends PR [#100](https://github.com/ZMS-Labs/epistemic-skills/pull/100); not operator-approved)  
**Related:** [`2026-08-06-fudge-design-md-leverage.md`](2026-08-06-fudge-design-md-leverage.md) · [`2026-08-06-epistemic-skills-v5-design.md`](2026-08-06-epistemic-skills-v5-design.md) (D8 estate budget)

**Primary external docs (Claude Design ↔ harness):**

- [Get started with Claude Design](https://support.claude.com/en/articles/14604416-get-started-with-claude-design) — canvas flow, `/design-sync`, MCP setup, handoff to Claude Code  
- [Claude Code commands — `/design-login`, `/design-sync`](https://code.claude.com/docs/en/commands) — bundled skill behavior and API-only availability  
- [Claude Design admin guide](https://support.claude.com/en/articles/14604406-claude-design-admin-guide-for-team-and-enterprise-plans) — org design systems, rollout, Enterprise admin role  

## Naming (do not conflate)

| Name | What it is | Where it lives |
|---|---|---|
| **Claude Design** | Anthropic Labs **product**: chat + canvas for prototypes, decks, microsites; org **design systems**; export and **handoff to Claude Code** | [claude.ai/design](https://claude.ai/design), Claude Desktop sidebar; beta on paid plans |
| **`frontend-design` skill** | Anthropic **implementation craft** (bold direction, eight domains, anti–AI-slop) — text skill, not the canvas product | Bundled in Impeccable; Apache 2.0 |
| **Impeccable** | Third-party **harness toolkit** (commands + `frontend-design` + anti-patterns + repo `PRODUCT.md` / `DESIGN.md`) | Per-project `.cursor/skills/` etc. |
| **Fudge DESIGN.md** | Third-party **capture briefs** (~287 sites) for agent-consumable visual character | Link to [fudge-design-md](https://github.com/scroobius-pip/fudge-design-md) |
| **`/design-sync`** | Claude Code **bundled skill**: upload/sync a **React** design system with Claude Design | Terminal; requires Anthropic API path to claude.ai |
| **Claude Design MCP** | HTTP MCP so Claude Code can create/edit design projects without leaving the terminal | `claude mcp add --scope user --transport http claude-design https://api.anthropic.com/v1/design/mcp` + `/design-login` per Help Center |

“Claude design” in operator conversation often means **Claude Design the product**, not the **`frontend-design` skill**. This document treats both and states how they compose.

## Problem

Five layers can all speak “design” to agents, with overlapping goals but different
shapes, install surfaces, and authority:

| Layer | Primary artifact | Typical harness |
|---|---|---|
| Fudge guide | Upstream `design-md/<domain>.md` | Any |
| Claude Design | Org design system + canvas project + handoff bundle | Web/Desktop; Claude Code via MCP/handoff |
| Repo `DESIGN.md` / `PRODUCT.md` | Stitch-style / Impeccable context | Cursor, Claude Code, Codex, … |
| `frontend-design` | Skill doctrine | Impeccable or host-shipped skill |
| Impeccable commands | Audit, polish, normalize, … | Cursor nightly / other harnesses |

Without alignment, agents pin a Fudge file, skip org design systems, ignore a
Claude Design handoff, or treat canvas output as shipped software — while
`DESIGN.md` means three different things.

## Design goal

One **ordered stack** with clear seats, **harness-aware branches**, and
`epistemic-skills` staying package-portable (craft pointers only — no vendoring
Fudge, Impeccable, or Claude Design).

## Recommended stack (harness-aware)

### A — Claude Code on Anthropic API (full loop available)

```text
Human-facing UI work starts
        │
        ├─ Optional exploration: Claude Design (canvas) OR Fudge character seed
        │
        ▼
[1] epistemic-skills craft: visual-design-md
        │  Direction pinned? If React DS exists: note /design-sync expectation
        ▼
[2] Claude Design integration (when used)
        │  /design-login → org design system attached to project
        │  /design-sync [hint]  — repo React DS → Claude Design (re-run after DS changes; not a watcher)
        │  Optional MCP: claude-design server for terminal create/edit
        │  Handoff bundle → Claude Code (continues from design work, not a screenshot-only prompt)
        ▼
[3] Repo ground truth
        │  PRODUCT.md + DESIGN.md (Impeccable when installed)
        │  Fudge link only in Reference section if it seeded character
        ▼
[4] Build / refine in code
        │  frontend-design principles; Impeccable audit · normalize · polish
        ▼
[5] evidence-locked-uat
        ▼
Acceptance claim
```

**Constraints from Anthropic docs:**

- `/design-sync` is **unavailable** on Amazon Bedrock, Google Cloud Agent
  Platform, Microsoft Foundry, and Claude Platform on AWS — the tool cannot reach
  claude.ai ([commands reference](https://code.claude.com/docs/en/commands)).
  On those deployments, use branch **B** only.
- First `/design-sync` on a large React repo can take hours (per-component verify).
- Claude Design without an org design system still produces **functional but
  generic** output ([admin guide](https://support.claude.com/en/articles/14604406-claude-design-admin-guide-for-team-and-enterprise-plans)) — same failure class as unpinned Fudge.

### B — Cursor and other harnesses (no Claude Design product API)

```text
visual-design-md craft → Fudge seed (link) → repo DESIGN.md/PRODUCT.md (Impeccable)
        → frontend-design / Impeccable during build → evidence-locked-uat
```

Do not instruct Cursor agents to run `/design-sync` or depend on Claude Design
MCP. Treat Claude Design handoff artifacts as **inputs** when the operator
drops them into the repo or task, not as an assumed integration.

### C — Machine-only surfaces

`agent-interface-design` only; this stack does not apply.

## Role of each layer

### Claude Design (product) — *explore, systematize, hand off*

- **Owns:** Canvas iteration, org-scoped design systems (from codebase, GitHub,
  uploads, web capture), exports (HTML, PDF, PPTX, partners), **handoff bundle**
  into Claude Code.
- **Does not own:** Production merge authority, CI acceptance, or epistemic
  claims about “done.”
- **epistemic-skills stance:** Document as **optional Claude-harness path** in
  craft; never bundle or proxy Claude Design inside the plugin. Handoff bundle +
  implemented code still require **evidence-locked-uat** for material UI claims.

### `/design-sync` + `/design-login` — *bridge code ↔ Claude Design*

- **Owns:** Keeping Claude Design’s generated UI aligned with **real React
  components** in the repo (push/upload semantics per Anthropic; re-sync after
  token/component changes).
- **Does not own:** Non-React stacks, offline harnesses, or automatic bidirectional
  merge without operator review (community reports: design→code may need explicit
  steps beyond a single command).
- **epistemic-skills stance:** Mention in craft under “when on Claude Code (API)”;
  point to official commands doc; flag Bedrock/Foundry gap.

### Fudge DESIGN.md — *reference seed*

(Unchanged from PR #100.) Capture-derived character; link-by-default; cite in
project `DESIGN.md` when Impeccable or Claude Design org system is primary.

### Claude `frontend-design` — *implementation craft*

(Unchanged.) Distinct from Claude Design product; execution quality during coding.

### Impeccable — *repo-local design ops*

(Unchanged.) Out of `epistemic-skills` package; complements both Cursor and
Claude Code terminal work **after** direction exists.

## Resolving `DESIGN.md` and “design system” collisions

| Artifact | Authority |
|---|---|
| Claude Design **org design system** (cloud) | Source for **canvas** and synced React components after `/design-sync` |
| Repo **`DESIGN.md`** (Impeccable / Stitch) | **Build-time truth** for coding agents in that repo |
| Fudge **`design-md/*.md`** | **Reference seed** only — mood, hierarchy, gaps |
| Claude Design **handoff bundle** | **Contract input** for implementation session — not a PASS |

**Rule:** One primary repo `DESIGN.md` per surface. After `/design-sync`, prefer
**real components** over re-inventing markup. If Fudge seeded the project, keep a
short Reference section; do not let Fudge override synced org tokens.

## Composability matrix (extended)

| Situation | Claude Design | /design-sync | Fudge | Impeccable | Craft |
|---|---|---|---|---|---|
| Greenfield UI, Claude Code API, React DS | Explore on canvas → handoff | Before/after DS changes | Optional character seed | `init` / `document` | Pin + harness note |
| Greenfield UI, Cursor only | N/A (operator may explore manually) | N/A | Pin link | `init` / `document` | Pin mandatory |
| Brownfield React, DS in repo | Optional polish on canvas | Re-sync when components change | Skip | `normalize` / `audit` | Light gate |
| Bedrock / Foundry Claude Code | Not available | **Unavailable** | Pin + repo files | If installed | Full B path |
| Deck / PPTX only | Claude Design primary | Optional | Rare | N/A | UAT if “product UI” claim |
| Agent API only | — | — | — | — | `agent-interface-design` |

## Conflicts and how to decide

| Tension | Resolution |
|---|---|
| Claude Design canvas vs repo `DESIGN.md` | Canvas explores; repo file + synced components win at implementation unless operator explicitly adopts export-only HTML without code integration. |
| Handoff bundle vs UAT | Handoff = starting point for code; **evidence-locked-uat** gates material UI acceptance. |
| Claude Design generic output vs Fudge pin | Set up org design system or pin Fudge **before** broad rollout; admin guide recommends DS-first rollout. |
| `frontend-design` “BOLD” vs Fudge restraint | Bold within pinned character (unchanged). |
| Impeccable vs Claude Design | Complementary: Claude Design for visual exploration/system sync on Claude harness; Impeccable for terminal command passes on repo files. |
| Purple SaaS / AI slop | All layers agree it is a failure mode. |
| Skill estate budget (D8) | Do not add Claude Design or Impeccable into `epistemic-skills`; craft links only. |

## What changes in PR #100 (if accepted)

1. **`visual-design-md.md`** — Stack section includes Claude Design branch,
   `/design-sync` prerequisites, MCP pointer, Bedrock caveat, handoff ≠ UAT.
2. **This spec** — Canonical alignment doc for all four names plus harness table.
3. **Handoff** — Operator: approve harness branches; whether wiki documents
   Claude Design for ZMS fleet Claude Code users.
4. **Still out of scope:** Vendoring any third-party design tree; new routed
   skill; `epistemic-calibration` UI.

## Operator decisions needed

1. Approve stack **A vs B** defaults per fleet (Claude Code API vs Cursor-primary).
2. Whether ZMS standardizes **org design system in Claude Design** before agent UI work.
3. Impeccable naming in package docs (unchanged recommendation: yes, optional).
4. Require **handoff bundle + UAT** for any UI merged from Claude Design canvas.

## Open follow-ups

- Fudge section → Stitch `DESIGN.md` mapping table (one page).
- Fleet runbook: `/design-login` once per user, when to re-run `/design-sync`,
  MCP scope (`user` vs `project`).
- Project PR template when a surface uses Claude Design handoff (paths, anchors).
