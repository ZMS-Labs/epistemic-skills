<!-- craft doctrine: visual-design-md — EXPLORATORY DRAFT (2026-08-06).
     Not approved craft. Proposal lives in
     docs/superpowers/specs/2026-08-06-fudge-design-md-leverage.md.
     Pattern mirrors agent-interface-design: workflow/craft method, not a
     routed epistemic skill; no description-byte budget claim. -->

# visual-design-md — pin a visual contract before painting pixels

When work produces a **human-facing** visual surface (landing page, product
chrome, docs site, operator UI), the failure mode is not only wrong acceptance —
it is an ungrounded visual invention: purple-on-white SaaS defaults, card soup,
or a first viewport that could belong to any brand.

`agent-interface-design` owns machine contracts and **declines** human UI.
`evidence-locked-uat` owns acceptance of material UI and **does not** choose
the look. This craft fills the gap: **encode visual direction as a pinned
DESIGN.md before implementing layout and chrome.**

## Evidence posture

This craft is **methodological**, not literature-graded. Upstream Fudge guides
are capture-derived briefs with explicit known gaps; treat missing tokens as
unknown, not as permission to invent a full system. Do not overclaim that a
DESIGN.md improves acceptance rates — UAT still owns acceptance.

## Where this sits

| Slot | Skill / craft | Relation |
|---|---|---|
| Machine contract to another agent | `reference/craft/agent-interface-design.md` | Twin for agent-consumed schemas; not for human pixels |
| Visual direction before build | **this craft** | Pins character, hierarchy, and measured relationships |
| Acceptance of the built surface | `evidence-locked-uat` | Judges the rendered surface; does not pick the reference |
| High-blast-radius product claims | `gauntlet` | Adversarial review when stakes require it |

## Stack alignment (Fudge + Claude Design + frontend-design + Impeccable)

These layers are complementary when **ordered** and **harness-aware**; they are
not competing authorities for the same `DESIGN.md` slot. Full spec:
[`docs/superpowers/specs/2026-08-07-visual-design-stack-alignment.md`](../../../../docs/superpowers/specs/2026-08-07-visual-design-stack-alignment.md).

| Layer | Role |
|---|---|
| **Claude Design** (product) | Optional explore/handoff on Claude harness — canvas, org design system, export; [Help Center](https://support.claude.com/en/articles/14604416-get-started-with-claude-design) |
| **`/design-login` + `/design-sync`** | Claude Code only (Anthropic API): sync **React** design system with Claude Design — [commands](https://code.claude.com/docs/en/commands); **not** on Bedrock/Foundry |
| **Fudge guide** (link or thin cite) | Reference *seed* — character, hierarchy, known gaps |
| **Project `DESIGN.md` + `PRODUCT.md`** | Build-time truth when [Impeccable](https://impeccable.style) (or equivalent) is installed |
| **Claude `frontend-design`** | Implementation craft — not the Claude Design canvas; usually via Impeccable |
| **Impeccable commands** | Optional passes (`audit`, `normalize`, `polish`, …) before acceptance |
| **This craft** | Gate: direction pinned before pixels; handoff bundle ≠ PASS |
| **`evidence-locked-uat`** | Acceptance after build |

**Cursor / non-Claude-Design harnesses:** Fudge pin → repo `DESIGN.md` →
Impeccable/`frontend-design` → UAT. Do not assume `/design-sync` or Claude
Design MCP.

Do not add Impeccable, Claude Design, or the full Fudge tree to
`epistemic-skills`; estate description bytes are rivalrous (v5 D8).

## Core moves

1. **Pin one guide.** Before implementing human-facing layout, place or link a
   `DESIGN.md` at the project root or `docs/design/DESIGN.md`. Prefer a single
   primary reference over a collage of five.
2. **Match character, not celebrity.** Choose a Fudge guide (or a
   project-authored DESIGN.md in the same shape) for the *mood and hierarchy*
   you need — editorial calm, dense workspace, austere empty canvas, dark
   workstation — not because the brand is fashionable.
3. **Adapt; do not clone.** Preserve relationships (scale ratios, accent
   scarcity, separator-over-shadow, open field vs dense chrome). Do not copy
   proprietary marks, licensed typefaces you do not have, or trademarked
   illustration systems.
4. **Respect known gaps.** If the guide omits color tokens, interaction
   states, or responsive rules, invent the minimum needed for the task and
   record that invention in the PR — do not pretend the capture specified it.
5. **Hand off to acceptance.** Routine presentation check or
   `evidence-locked-uat` still gates material UI claims. A pinned DESIGN.md is
   direction, not a PASS.

## Upstream source (link, do not vendor by default)

Collection: [scroobius-pip/fudge-design-md](https://github.com/scroobius-pip/fudge-design-md) (MIT).  
Product: [design.withfudge.com](https://design.withfudge.com/).

Pin by linking the specific `design-md/<domain>.md` file (and optionally
quoting the Design character / Practical guidance sections into the PR or a
thin local `DESIGN.md` that cites upstream). Vendor a copy only when offline
durability is required; if you vendor, keep MIT attribution and a fetch date.

### Character shortlist (pointers only)

| Need | Guide |
|---|---|
| Calm editorial tech narrative | [`anthropic.com.md`](https://github.com/scroobius-pip/fudge-design-md/blob/main/design-md/anthropic.com.md) |
| Dense product workspace | [`linear.app.md`](https://github.com/scroobius-pip/fudge-design-md/blob/main/design-md/linear.app.md) |
| Quiet infrastructure landing | [`stripe.com.md`](https://github.com/scroobius-pip/fudge-design-md/blob/main/design-md/stripe.com.md) |
| Austere brand-first empty canvas | [`abc.xyz.md`](https://github.com/scroobius-pip/fudge-design-md/blob/main/design-md/abc.xyz.md) |
| Dark developer workstation shell | [`cursor.com.md`](https://github.com/scroobius-pip/fudge-design-md/blob/main/design-md/cursor.com.md) |

## Use it when

- Starting or substantially redesigning a human-facing visual surface.
- An agent is about to invent a look without a project design system.
- Operator frontend constraints exist but no project-local visual packet does.

## Do not use it when

- The surface is agent-consumed only (schemas, MCP, CLI contracts) — use
  `agent-interface-design`.
- The change is a routine, reversible presentation tweak with an existing
  design system already in-tree.
- You need acceptance evidence — that is `evidence-locked-uat`, not this file.
- The target is `epistemic-calibration`'s learning loop (no UI required).

## Anti-patterns

| Failure | Fix |
|---|---|
| "I'll vibe a purple gradient landing page." | Pin a guide; start from its character and practical guidance. |
| "I'll merge Linear + Stripe + A24 into one moodboard." | One primary guide; secondary references only for a named subsystem. |
| "The guide had no hex values, so I invented a 40-token palette." | Invent the minimum; document the gap; keep accent budget small. |
| "DESIGN.md exists, so UAT is optional." | Direction ≠ acceptance. Run the routine check or UAT as usual. |
| Vendoring the entire Fudge tree into the plugin. | Link. Curate at most a shortlist of pointers in craft. |

## Falsifiable gate (lightweight)

Before claiming the visual direction is set: a cold reader of the pinned
DESIGN.md can state (1) the intended character in one sentence, (2) what must
be preserved, and (3) at least one known gap. If they cannot, the pin is too
thin or the wrong guide was chosen.
