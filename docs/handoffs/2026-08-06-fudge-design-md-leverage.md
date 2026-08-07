# Handoff — Fudge DESIGN.md leverage recommendations

**Date:** 2026-08-06  
**Branch:** `cursor/fudge-design-md-leverage-b285`  
**Draft PR:** [#100](https://github.com/ZMS-Labs/epistemic-skills/pull/100)  
**Design spec:** [`docs/superpowers/specs/2026-08-06-fudge-design-md-leverage.md`](../superpowers/specs/2026-08-06-fudge-design-md-leverage.md)  
**Stack alignment (Fudge + Claude Design + frontend-design + Impeccable):** [`docs/superpowers/specs/2026-08-07-visual-design-stack-alignment.md`](../superpowers/specs/2026-08-07-visual-design-stack-alignment.md)  
**ZMS org design repo placement (skill decision + fleet):** [`docs/superpowers/specs/2026-08-07-zms-labs-design-fleet-placement.md`](../superpowers/specs/2026-08-07-zms-labs-design-fleet-placement.md) — *blocked until `zms-labs-design` is readable by agents*  
**Draft craft stub:** [`plugins/epistemic-skills/reference/craft/visual-design-md.md`](../../plugins/epistemic-skills/reference/craft/visual-design-md.md)  
**Upstream:** [scroobius-pip/fudge-design-md](https://github.com/scroobius-pip/fudge-design-md) (MIT)  
**Status:** recommendations recorded; **not operator-approved**; no implementation beyond this exploratory PR

This file is the durable pick-up brief for a future agent. Prefer it over chat
history. Do not treat the draft craft stub as live doctrine until an operator
approves the design and the exploratory markers are removed.

## Verdict (recommended)

**Ship Approach A only:** thin craft doctrine under
`plugins/epistemic-skills/reference/craft/visual-design-md.md`, pin Fudge
guides **by link**, do not vendor the collection, do not add a routed skill.

**Stack (2026-08-07):** Treat Fudge as the *reference seed*; **Claude Design**
(canvas + org design system + Claude Code handoff/`/design-sync` on API) as
*optional Claude-harness exploration* — distinct from the **`frontend-design`**
skill; Impeccable as *optional per-project* `PRODUCT.md` / `DESIGN.md` + commands.
See the alignment spec. Do **not** bundle Impeccable or Claude Design into
`epistemic-skills` (D8 budget).

### Why

1. **Hole is real.** `agent-interface-design` declines human UI;
   `evidence-locked-uat` accepts UI but does not choose visual direction.
   Fudge `DESIGN.md` is the missing pre-build visual packet.
2. **Craft slot matches package law.** v4 already demoted workflow methods to
   `reference/craft/`. v5 D8 forbids burning description bytes on a new
   "when doing UI" skill trigger.
3. **Link > vendor.** Upstream is MIT and churns (~287 guides). Vendoring
   copies (Approach B) adds stale trees and attribution surface for little
   gain. Operator-only notes (Approach C) leave the hole invisible to plugin
   consumers.
4. **Calibration stays out.** `epistemic-calibration` is no-UI by design;
   do not invent a surface there under this workstream.

## Do / don't for the next agent

| Do | Don't |
|---|---|
| Get operator approval of Approach A (or an explicit override to B/C) before merging as doctrine | Merge the exploratory stub as if it were approved craft |
| On approval: strip "EXPLORATORY DRAFT" markers; optionally add a one-line craft pointer from wiki/catalog pages the way other craft is listed | Add `visual-design-md` to metacognate roster or any skill description |
| Keep shortlist as **pointers** to upstream `design-md/<domain>.md` | Copy the full Fudge tree into this repo |
| If a product needs offline durability, vendor **one** guide with MIT attribution + fetch date | Invent hex/type tokens the capture marked as unknown |
| Leave `evidence-locked-uat` as acceptance authority | Treat a pinned DESIGN.md as a UAT PASS |

## Defaults on open questions (unless operator overrides)

1. **Approach:** A (craft + pin-by-link).  
2. **Host Cursor frontend rules:** mention as complementary in craft only if
   the package stays honest that they are host-local, not portable doctrine;
   default = stay package-portable and silent about host rules.  
3. **Pointer from `evidence-locked-uat`:** skip for v1; discovery via craft
   only. Add a one-liner later only if agents keep skipping the pin.  
4. **First project-local DESIGN.md:** none required by this PR; spawn a
   follow-up only when a concrete human-facing surface is in scope.

## Artifacts already on this branch

- Design with A/B/C and recommendation:
  `docs/superpowers/specs/2026-08-06-fudge-design-md-leverage.md`
- Exploratory craft sketch (same recommendation, operational form):
  `plugins/epistemic-skills/reference/craft/visual-design-md.md`
- This handoff

## Stop condition for *this* session

Recommendations are committed on the PR branch for future consideration.
No further implementation in the originating session.
