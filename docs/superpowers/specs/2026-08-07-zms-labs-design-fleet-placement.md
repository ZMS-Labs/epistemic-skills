# ZMS Labs design — fleet placement & skill decision

**Date:** 2026-08-07  
**Status:** draft — **blocked on reading** [`ZMS-Labs/zms-labs-design`](https://github.com/ZMS-Labs/zms-labs-design)  
**Extends:** PR [#100](https://github.com/ZMS-Labs/epistemic-skills/pull/100), [`2026-08-07-visual-design-stack-alignment.md`](2026-08-07-visual-design-stack-alignment.md)

## Access note (this session)

From the Cloud Agent environment (`cursor` GitHub integration):

- `gh repo view ZMS-Labs/zms-labs-design` → **404**
- Anonymous `git ls-remote` → **repository not found**
- Public HTTP fetch of the repo URL → **404**

So either the repository is **private** and the agent app lacks org/repo access, or it is **not created yet** under that exact name. This document coheres PR #100 with the **intended** role of `zms-labs-design` as the org design home. **Reconcile against the real README/philosophy** once the repo is cloned (add it to the [Cloud environment](https://cursor.com/dashboard/cloud-agents) repos + grant the Cursor GitHub App access to `zms-labs-design`).

---

## Intended philosophy (coherence with PR #100)

PR #100 argues: human-facing visual work needs a **pinned direction** before pixels;
acceptance stays with `evidence-locked-uat`; machine contracts stay with
`agent-interface-design`. That is **epistemic choreography**, not a design system.

**`zms-labs-design` (intended seat)** should own what PR #100 deliberately refuses
to put in `epistemic-skills`:

| Concern | Owner | Rationale |
|---|---|---|
| Brand, tokens, components, typography, motion rules | **`zms-labs-design`** | Durable product/org artifact; versioned; human + agent consumable |
| When to pin direction / hand off to UAT | **`epistemic-skills` craft** (`visual-design-md`) | Portable method; link, don’t vendor |
| Canvas exploration + org DS in Anthropic cloud | **Claude Design** + `/design-sync` | Harness product; sync **from** `zms-labs-design` when React DS exists |
| Terminal polish / anti-slop passes | **Impeccable** (optional per harness) | Third-party; reads repo `DESIGN.md` |
| Greenfield character before ZMS DS exists | **Fudge** (link only) | External reference seed |
| “It works on screen” / material UI claims | **`evidence-locked-uat`** | Epistemic acceptance |

**One sentence:** `zms-labs-design` is the **organization’s visual source of truth**;
`epistemic-skills` teaches **when and how agents must bind to that truth** (or an
explicit interim pin) before building and before claiming done.

### What should live in `zms-labs-design` (target shape)

Pending repo content, expect at least:

1. **Canonical `DESIGN.md`** (and/or Stitch-style packet) — what every ZMS human UI repo should cite or submodule.
2. **`PRODUCT.md` template or org default** — strategy layer Impeccable/Claude Design expect.
3. **Implementable design system** — tokens, components; if React, the **sync source** for Claude Design `/design-sync`.
4. **Consumption contract** — how product repos pin a version (git submodule, npm package, copied hash-pinned excerpt).
5. **Explicit non-goals** — not epistemic disciplines, not fleet health, not calibration science (`epistemic-calibration` stays no-UI).

### What should *not* move into `epistemic-skills`

- Full Fudge tree, Impeccable bundle, or Claude Design
- ZMS brand tokens (duplicates `zms-labs-design` and breaks portability thesis)
- A second copy of org `DESIGN.md` that can drift

---

## (a) Does a skill deserve to exist — and in which repo?

Use the **subject test** (v5 design): `epistemic-skills` owns **claims that must bear
load** about work, reasoning, or running systems. Visual taste and token compliance
are **workflow substrate**, not an epistemic moment — same reason
`agent-interface-design` was demoted to **craft**.

### Decision table

| Candidate | Verdict | Where |
|---|---|---|
| New **routed** `visual-design` / `design-system` skill in **`epistemic-skills`** | **No** | Description-byte budget (D8); duplicates craft + UAT; wrong subject |
| **`visual-design-md` craft** in `epistemic-skills` | **Yes** (thin) | Points to org DS + stack; no ZMS tokens inside portable core |
| **ZMS-specific “apply our DS” skill** (normalize, token lint, component names) | **Yes, if needed** | **`zms-labs-design`** (or a tiny plugin *published from* that repo) — not copied into every app repo |
| **Impeccable** | **No new org skill** | Install per harness/project; already ~1.2k description bytes in estate |
| **`evidence-locked-uat`** in product repos | **Already in `epistemic-skills`** | Same package everywhere; do not fork |
| **Per-repo design skill** in each ZMS-Labs app | **No** | Drift, budget burn, inconsistent triggers |

### Recommended rule for “any repo within ZMS-Labs”

- **Every repo** that ships human UI: **depends on** `zms-labs-design` (pin) + loads **`epistemic-skills`** (unchanged).
- **At most one** org-owned design-application skill/package: lives with **`zms-labs-design`**, not N copies.
- **Zero** new routed visual skills in `epistemic-skills` unless the subject test changes (e.g. you need *epistemic* gates on design *claims* — that is still `evidence-locked-uat` / `gauntlet`, not a design skill).

### If `zms-labs-design` already ships agent skills

Map each skill to:

- **Application** (use tokens) → keep in `zms-labs-design`
- **Acceptance** (prove UI) → invoke `evidence-locked-uat` from `epistemic-skills`
- **Exploration** (canvas) → Claude Design + handoff, not a repo skill

---

## (b) Leveraging design across repos, fleets, services, clusters

Think in **layers**, not “install design everywhere.”

```text
                    ┌─────────────────────────────┐
                    │   zms-labs-design (Git)      │
                    │   DESIGN.md · tokens · DS    │
                    └──────────────┬──────────────┘
           pin / submodule / package │
     ┌─────────────┬───────────────┼───────────────┬─────────────┐
     ▼             ▼               ▼               ▼             ▼
 product repos  Claude Design   Claude Code    Cursor fleet   (future)
 (UI apps)      org DS          /design-sync   Impeccable     surfaces
     │             │               │               │
     └─────────────┴─────── build in repo ────────┘
                           │
                           ▼
              epistemic-skills: evidence-locked-uat
                           │
     ┌─────────────────────┴─────────────────────┐
     ▼                                           ▼
 headless services / jobs                   K8s clusters
 (no visual-design-md)                      health · triage · watch
```

### By surface type

| Surface | Design leverage | Epistemic package |
|---|---|---|
| **Human UI repos** (wiki, canvas chrome, operator tools) | Pin `zms-labs-design`; optional Fudge only pre-DS; Impeccable or Claude path per harness | `visual-design-md` craft + `evidence-locked-uat` |
| **Libraries / APIs / agents** | `agent-interface-design` only | No visual craft |
| **Homelab / fleet ops** | `LOCAL.md` overrides; site-specific diagnostics stay out of portable DS | `health` · `triage` · `watch` (v5) |
| **Clusters (K8s)** | Dashboards only if product-owned; DS from `zms-labs-design` | Runtime truth ≠ pixel polish |
| **Claude Code fleet** | `/design-login`; `/design-sync` from DS rooted in `zms-labs-design`; handoff bundles land in product repos | Same `epistemic-skills` install |
| **Cursor / cloud agents** | Environment lists repos; add `zms-labs-design` to agent environment; craft points to pinned DS path | No `/design-sync` unless API path |

### Distribution patterns (pick one primary)

1. **Git submodule** `vendor/zms-labs-design` + CI check that `DESIGN.md` hash matches tag.
2. **Published package** (`@zms-labs/design-tokens`) consumed by apps; `DESIGN.md` generated or copied at release.
3. **Claude Design org default** fed by periodic `/design-sync` from the package’s React layer.

Avoid: pasting tokens into each repo’s `DESIGN.md` without a single upstream.

### Fleet-wide agent instructions

| Layer | What to configure once |
|---|---|
| **Org** | Claude Design enabled; design system sourced from `zms-labs-design`; admin role for publish |
| **`epistemic-skills`** | Approve craft; one line in README/wiki: “ZMS UI pins `zms-labs-design` @ ref” |
| **`zms-labs-design`** | Version tags; consumption doc; optional ZMS design skill/plugin |
| **Each UI repo** | `PRODUCT.md` local; `DESIGN.md` = pointer or re-export; UAT in CI for material UI |
| **Harness** | Impeccable in `.cursor/skills` where Cursor; Claude MCP where Code |

---

## Operator decisions (unblocks implementation)

1. **Confirm `zms-labs-design` exists and grant** Cursor GitHub App + Cloud Environment repo access.
2. **Approve:** no routed visual skill in `epistemic-skills`; org design skill only in `zms-labs-design` if needed.
3. **Choose distribution:** submodule vs npm vs sync-only Claude Design.
4. **Merge PR #100 craft** after aligning README in `zms-labs-design` with this split (no contradiction).

## Next step after repo is readable

1. Diff this doc against `zms-labs-design` README, ADRs, and any existing skills.
2. Update [`visual-design-md.md`](../../../plugins/epistemic-skills/reference/craft/visual-design-md.md) with the **canonical pin URL/path** for ZMS.
3. Optionally add `zms-labs-design` to the [Cloud Agent environment](https://cursor.com/dashboard/cloud-agents/environments/e/688d12dd-9109-11f1-ba66-0e7d0216e441) repos (see `epistemic-calibration/.cursor/environment.json` `repositoryDependencies`).
