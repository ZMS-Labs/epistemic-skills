# Leveraging Fudge DESIGN.md for agent visual work

**Date:** 2026-08-06  
**Status:** exploratory draft (Approach A recommended; not approved)  
**Upstream:** [scroobius-pip/fudge-design-md](https://github.com/scroobius-pip/fudge-design-md) (MIT) · [design.withfudge.com](https://design.withfudge.com/)  
**Future-agent pick-up:** [`docs/handoffs/2026-08-06-fudge-design-md-leverage.md`](../../handoffs/2026-08-06-fudge-design-md-leverage.md)  
**Sibling note:** `epistemic-calibration` remains no-UI by design; this proposal does not add a surface there.

## What Fudge DESIGN.md is

[fudge-design-md](https://github.com/scroobius-pip/fudge-design-md) is a curated collection (~287 guides as of this draft) of **agent-consumable visual briefs** generated from real websites captured in Fudge. Each `design-md/<domain>.md` guide typically:

- states a **design character** (mood, hierarchy, what to preserve);
- separates **captured measurements** from **interpretation**;
- lists typography / color / spacing / radius observations when retained;
- shows representative page captures;
- ends with **practical guidance** and **known gaps** (what the capture did *not* establish).

The intended use, from the upstream README: drop one guide into a project so a coding agent gets a specific visual direction grounded in a real reference, instead of inventing a generic SaaS look.

## Why this package should care

`epistemic-skills` already owns two adjacent seats and leaves a hole between them:

| Seat | Owns | Explicitly declines |
|---|---|---|
| `reference/craft/agent-interface-design.md` | Machine contracts another agent consumes | Human-facing UI/UX and docs for people |
| `evidence-locked-uat` | Acceptance of material UI-facing change | Choosing the visual language before build |

There is **no craft doctrine for grounding visual direction** before an agent paints pixels. Operator Cursor rules already constrain frontend taste (one composition, brand-first, no default purple SaaS, etc.), but those rules are session-global and not project-scoped reference packets. Fudge guides are exactly that missing packet class: portable, citeable, measurement-honest visual contracts.

This is craft, not a new routed skill. Description-byte budget (v5 D8) forbids adding a trigger row for "when doing UI." The pattern matches the v4 demotion of `agent-interface-design` and `intent-traced-merge` into `reference/craft/`.

## Non-goals

- Do **not** vendor the full ~287-guide tree into this repo.
- Do **not** mint a routed skill or expand the metacognate roster for visual design.
- Do **not** treat a Fudge guide as a license to clone a brand; adapt character, not trademarked marks or proprietary fonts.
- Do **not** invent UI for `epistemic-calibration` under this proposal.
- Do **not** weaken `evidence-locked-uat`: DESIGN.md is pre-build direction, not acceptance evidence.

## Approaches

### A — Craft doctrine + pin-by-link (recommended)

Add thin craft under `plugins/epistemic-skills/reference/craft/visual-design-md.md` that teaches agents:

1. When human-facing visual work starts, **pin one DESIGN.md** (project root or `docs/design/DESIGN.md`) before implementing layout/chrome.
2. Prefer a Fudge guide matched to the intended character; link upstream rather than copying unless a durable offline pin is required.
3. Adapt character and token *relationships*; do not treat missing measurements as license to invent a full design system.
4. Hand off to `evidence-locked-uat` (or the routine presentation check) for acceptance.

**Pros:** Matches package thesis and craft slot; zero description-byte cost; MIT-compatible via link/attribution; reversible.  
**Cons:** Agents must discover the craft file (same as other craft doctrine).

### B — Curated shortlist vendored under `reference/visual-references/`

Copy a small set of guides (e.g. anthropic, linear, stripe, abc.xyz) into-tree with MIT attribution and a README that maps each to a use case (editorial product, dense workspace, calm infra landing, austere investor page).

**Pros:** Offline, reviewable diffs when upstream changes.  
**Cons:** Stale copies; license attribution surface; still need craft doctrine for *when/how* to use them; duplicates upstream.

### C — Operator-only convention (no package change)

Document "put a DESIGN.md in the target repo" in fleet notes / Cursor rules only; leave `epistemic-skills` untouched.

**Pros:** Fastest.  
**Cons:** Invisible to anyone loading the plugin; does not close the craft hole next to `agent-interface-design`.

## Recommended decision

**Ship Approach A** as craft doctrine. Optionally keep a **shortlist pointer table** (links only, no file copies) inside that craft file for common characters. Revisit Approach B only if offline pins become load-bearing for a specific product surface.

## Suggested shortlist (links only)

| Character | Guide | When to prefer |
|---|---|---|
| Calm editorial tech | [anthropic.com](https://github.com/scroobius-pip/fudge-design-md/blob/main/design-md/anthropic.com.md) | Docs, research, long-form product narrative |
| Dense product workspace | [linear.app](https://github.com/scroobius-pip/fudge-design-md/blob/main/design-md/linear.app.md) | Operator tools, issue/project chrome |
| Quiet infra / payments landing | [stripe.com](https://github.com/scroobius-pip/fudge-design-md/blob/main/design-md/stripe.com.md) | Marketing surfaces that must feel precise, not loud |
| Austere empty canvas | [abc.xyz](https://github.com/scroobius-pip/fudge-design-md/blob/main/design-md/abc.xyz.md) | Brand-first pages that win by restraint |
| Dark developer workstation | [cursor.com](https://github.com/scroobius-pip/fudge-design-md/blob/main/design-md/cursor.com.md) | Devtool account/settings/marketplace shells |

Full catalog: [scroobius-pip/fudge-design-md](https://github.com/scroobius-pip/fudge-design-md).

## Relation to existing disciplines

```text
visual need appears
        │
        ▼
  craft: visual-design-md   ← pin DESIGN.md / Fudge guide (this proposal)
        │
        ▼
  build the surface
        │
        ▼
  evidence-locked-uat       ← routine check or full UAT packet
        │
        ▼
  acceptance claim
```

`agent-interface-design` remains the twin for **machine** interfaces. A surface that is both human UI and agent-consumed API needs both crafts, applied to their respective layers.

## Open questions for review

1. Approve Approach A (craft + pin-by-link), or prefer B/C?
2. Should the craft file mention operator frontend Cursor rules as complementary constraints, or stay package-portable and silent about host rules?
3. Is a one-line pointer from `evidence-locked-uat` ("visual direction should already be pinned; see craft/visual-design-md") worth the coupling, or keep discovery via craft only?
4. Any ZMS Labs product surface that should get a *project-local* DESIGN.md in a follow-up PR (wiki, future operator UI, etc.)?

## Draft artifact in this PR

See [`plugins/epistemic-skills/reference/craft/visual-design-md.md`](../../../plugins/epistemic-skills/reference/craft/visual-design-md.md) — a concrete Approach A sketch, marked exploratory until this design is approved.
