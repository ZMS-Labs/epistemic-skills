# Agentic skills packaging architecture (org-wide)

**Status: decided, not implemented** (banked 2026-07-18).  
**Method:** `/using-epistemic-skills` → blindspot-pass → applying-formal-rigor.  
**Gauntlet:** deferred until a frozen subject exists (new public package, license/visibility cut, or overlay-convention change).  
**Evidence-research / UAT:** skipped (no scholarly premise; no UI).

This note banks the analysis so a later session can implement without re-deriving. It is **not** a change to the epistemic-skills plugin family resemblance; it constrains how *other* agentic skill kinds relate to this repo and to the fleet.

## Context (what prompted this)

Evaluated two external artifacts relative to this collection:

1. [pro-vi/loopgen](https://github.com/pro-vi/loopgen) — prompt compiler for `/goal` / ralph-style overnight loops.
2. Custom `/release` slash-command pattern (r/ClaudeCode / [difit `release.md`](https://raw.githubusercontent.com/yoshiko-pg/difit/main/.claude/commands/release.md)).

Neither belongs *inside* `epistemic-skills`. That raised: what *are* they, and should there be a new GitHub basis (open monorepo vs distinct public/private repos) so skills port to Claude, Codex, Cursor, Gemini, Kimi, etc.?

## Layer map (what things are)

| Kind | Job | Examples | Packaging fit |
|---|---|---|---|
| **Epistemic discipline** | How the agent *knows* | gauntlet, UAT, evidence-research, formal-rigor, blindspot-pass | **This repo** (`epistemic-skills`) |
| **Workflow method** | How a *session* does work | TDD, plans, debug (superpowers) | Depend on [obra/superpowers](https://github.com/obra/superpowers); don’t fork a twin |
| **Loop / runtime** | How work *persists over time* | loopgen, ralph, halt/state contracts | Upstream or future **public** `agent-runtime-skills` — **not** this repo |
| **Ops ritual / slash command** | Recurring operator procedures | `/release`, ship/tag/changelog | **Private** fleet commands pack — often not a `SKILL.md` at all |

Portable unit across harnesses: [Agent Skills](https://agentskills.io/specification) (`SKILL.md` + optional `scripts/` / `references/`). Harness manifests are adapters around the same tree.

Composition with the epistemic router (unchanged):

```text
recon → decide → build (workflow / optional overnight loop) → gate → prove
blindspot   formal-rigor     superpowers / loopgen→/goal      gauntlet   UAT
            + evidence-research
```

Natural loopgen placement: **after** recon/decide, **before** gate/prove. Un-gated overnight runs can skip epistemic floors — compose deliberately.

## Territory already shipped (hidden context)

A private fleet tracking item (private `<private-fleet-repo>` `skills/README.md`) already defines:

| Layer | Where | Rule |
|---|---|---|
| **Core** | Public `ZMS-Labs/epistemic-skills` | Generic protocol; kept **byte-identical** to fleet copies |
| **Overlay** | Private `<private-fleet-repo>` `skills/*/LOCAL.md` (+ fleet-only assets) | Bindings only; **never overrides** the protocol |
| **Deploy** | Device cache = core + overlay | Cache reset must not lose skills |

Org pattern: few **public** method repos vs many **private** fleet products. Overlay lives in the private fleet repo (via a local worktree checkout), not in a public kitchen-sink monorepo.

Public plugin family resemblance (router invariants) — a skill belongs in *this* collection only if it enforces all of: floors not ceilings; derive/verify don’t assert; know where you stop; fail closed / degrade explicitly; provenance and independence.

## Blindspot landmines (do not forget)

1. “One GitHub basis” ≠ “one open monorepo.” Portability needs addressable trees + install paths.
2. Duplicating cores without sync → **update anomaly** (drift already called a bug in fleet overlay docs).
3. Publishing `LOCAL.md` / ledgers / evals by accident → disclosure of NAS paths, SAFETY-2 gates, Zotero IDs, etc.
4. Stuffing `/release` or loopgen into `epistemic-skills` → breaks family resemblance and trigger quality.
5. Private ≠ non-portable — authenticated harnesses can install private remotes.

## Options considered

| ID | Shape |
|---|---|
| **A** | One **open** monorepo: epistemics + runtime + ops |
| **B** | **Distinct** public package(s) + **private** fleet overlay (**extend status quo**) |
| **C** | Everything private |
| **D** | Public **methods-only** monorepo (`plugins/epistemic`, later `runtime`) + private overlay elsewhere |

## Formal derivation (summary)

Precise constructs used (applying-formal-rigor):

- **FD:** GitHub `repo → visibility` — one repo, one visibility; mixed public/private rows unrepresentable.
- **SSOT / normalization-for-code:** `skill_core` vs `skill_binding` must not share a relation that forces one visibility.
- **Type theory:** make illegal states unrepresentable (no public LOCAL secrets; no epistemic package containing ops/runtime).
- **Blast radius / failure domains:** accidental disclosure vs install ergonomics.
- **Materialized-view pattern:** recover “one place to look” via indexes + deploy scripts without denormalizing base tables.

**Verdict: B** (extend status quo). **A rejected.** **C** loses the open plugin story already shipped. **D** is a later optimization only if several public method plugins share packaging CI — still never an open kitchen-sink; still no private bindings in-tree.

### What B concedes (and how to recover)

Concedes: no single public clone that contains “everything.”

Recover via **materialized views**:

1. **Private** fleet skills index / marketplace manifest (in the private fleet repo or private org `.github`) listing public remotes + private overlay/command paths.
2. Optional **public** README index linking *only* public packages (derived view; no private rows).
3. Existing deploy scripts remain the device-cache materialization of (public core ⋈ private overlay).

### External artifacts under B

| Artifact | Disposition |
|---|---|
| **loopgen** | Consume upstream for now. Open a public `agent-runtime-skills` only when ZMS owns general loop/halt/state methods worth maintaining. Never merge into `epistemic-skills`. |
| **`/release`** | Private fleet ops command (procedure + harness adapters). Human holds publish; does not certify “done” (UAT/gauntlet still apply when triggers match). |

## Target end-state (when implementing)

```text
Public (ZMS-Labs)
  epistemic-skills              ← keep pure (knowing) — THIS repo
  agent-runtime-skills          ← only if/when owning general loop floors
                                  (else document upstream loopgen in fleet index)

Private (fleet)
  <private-fleet-repo>/skills/  ← LOCAL.md overlays + fleet-only assets (already)
  fleet ops commands            ← /release-class rituals (add when needed)
  private marketplace / index   ← lists public remotes + private paths

Optional public
  thin README “skills index”    ← links public packages only
```

## Pickup checklist (next session)

- [ ] Document layer map (epistemic / workflow / runtime / ops) in fleet `skills/README.md` without new repos yet.
- [ ] Add private fleet marketplace/index stub that points at `ZMS-Labs/epistemic-skills` + local overlays.
- [ ] Only scaffold `agent-runtime-skills` when there is ≥1 general loop method to maintain.
- [ ] Add `/release` (or equivalent) under private fleet commands when shipping pain justifies it.
- [ ] **Gauntlet** any proposal that: publishes a new public skills repo; changes license/visibility; or merges private overlay history into a public tree.
- [ ] Do **not** expand `epistemic-skills` family resemblance to include runtime or ops rituals.

## Non-goals

- Replacing superpowers with a ZMS workflow twin.
- Reimplementing loopgen inside this org before ownership is justified.
- An open monorepo that mixes public methods with fleet bindings.
- Treating slash commands as interchangeable with epistemic disciplines.

## Provenance

- Session analysis 2026-07-18 (Cursor): loopgen + `/release` evaluation → packaging fork → epistemic arc.
- Fleet core/overlay convention: private fleet repo skills README (2026-07-17).
- Related shipped design: [`2026-07-17-epistemic-skills-plugin-design.md`](./2026-07-17-epistemic-skills-plugin-design.md).
- Pre-reboot pause note: relocated to the private fleet repo (fleet-internal working material; see the public-repo hygiene sweep addendum in `docs/release/`).
