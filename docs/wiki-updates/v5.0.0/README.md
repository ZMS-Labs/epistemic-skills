# Wiki update for v5.0.0 — published

**Status: published to live wiki** at commit `e6c6ba7` on
`ZMS-Labs/epistemic-skills.wiki` (2026-08-07). This directory remains the
in-repo mirror and regeneration source.

Prior live wiki HEAD was `cd8ea69` (v3.x-era inventory). The earlier v4.0.0
package under `docs/wiki-updates/v4.0.0/` was never published and is superseded.

## What this is

The full v5.0.0 update to the `ZMS-Labs/epistemic-skills.wiki` repository:

- **5 new pages** — `Skill-Metacognate`, `Skill-Health`, `Skill-Triage`,
  `Skill-Did-It-Land`, `Skill-Watch`.
- **Navigation rewrite** — Home, Start-Here, Sidebar, Catalog, Choosing a Skill,
  Epistemic Arc, Installation, Version History aligned to fourteen skills and
  `metacognate` as the sole named entry point.
- **Historical banners** — deleted router/Helix pages and pre-4.0 consolidated
  names kept readable with explicit “not a live skill” banners.
- **Honesty pointers** — Evidence and Version History surface item-6 / item-8
  gate status and successor corrective work on `main`.

Regenerate authored pages with:

```bash
python docs/wiki-updates/v5.0.0/_generate_pages.py
```

(Idempotent for files the generator owns; re-seed from live wiki + v4 overlay
first if you need a clean base.)

## How to apply

**Copy into a wiki clone:**

```bash
git clone https://github.com/ZMS-Labs/epistemic-skills.wiki.git
cd epistemic-skills.wiki
# Review if HEAD moved past cd8ea69
cp -a /path/to/epistemic-skills/docs/wiki-updates/v5.0.0/pages/*.md .
git add -A
git commit -m "docs(wiki): v5.0.0 handbook — metacognate + fourteen skills"
git push origin master
```

**Via the wiki web UI:** paste each file in `pages/` over the corresponding page;
create the five new Skill-* pages listed above.

If the wiki has moved since this package was authored, prefer page-by-page review
— do not force-push over newer edits.

## Inventory check (expected)

Current skills linked from Sidebar/Catalog: metacognate, health, triage,
did-it-land, watch, recon, resolve, decision-ledger, write-goal, outsource,
open-questions, context-audit, gauntlet, evidence-locked-uat (14).

Historical: using-epistemic-skills, helix, blindspot-pass, wayfinding,
applying-formal-rigor, evidence-research, throwaway-prototyping,
continuity-verify, intent-traced-merge, agent-interface-design.
