# Wiki update for v4.0.0 — ready to apply

**Status: authored, adversarially verified, NOT yet published.** The
session environment's git proxy allows wiki reads but returns 403 on wiki
pushes, so the verified commit could not be published from here. This
directory is the complete hand-off.

## What this is

The full v4.0.0 update to the `ZMS-Labs/epistemic-skills.wiki` repository,
built against wiki HEAD `cd8ea69` (v3.4.0 state) on 2026-08-04:

- **2 new pages** — `Skill-Recon.md`, `Skill-Resolve.md` (house-shape
  guides with mode/instrument selection tables and v4.0.0-tag source
  links; candidate mode gets its first wiki coverage).
- **31 updated pages** — eleven-skill catalog and sidebar (with a
  "Historical (pre-4.0)" group), consolidation banners on the eight
  retired-name pages (bodies untouched), decision-ledger resume-mode
  amendment, Home/Version-History/FAQ/Installation inventory truth-sync,
  and `v4.0.0 note` banners wherever a retired name was presented as a
  current skill.

Verification (six checks, all PASS): inventory truth on all 41 pages,
mapping correctness against `docs/release/RELEASE-4.0.0.md`, link
integrity (75 v4.0.0 source links resolved against the repo), honest
claims (no superiority language; does-not-claim boundaries carried),
sidebar/catalog coherence, and no collateral damage to retired-page
bodies.

## How to apply (either way works)

**As a git patch (preserves the verified commit):**

```bash
git clone https://github.com/ZMS-Labs/epistemic-skills.wiki.git
cd epistemic-skills.wiki   # HEAD should be cd8ea69; if the wiki moved, review before applying
git am ../v4.0.0-wiki-update.patch
git push origin master
```

**Via the wiki web UI:** every changed page is in `pages/` under its wiki
filename — paste each file's content over the corresponding page (create
`Skill-Recon` and `Skill-Resolve` as new pages).

If the wiki has moved past `cd8ea69` since 2026-08-04, prefer the web-UI
route page-by-page, or rebase the patch — do not force-push over newer
edits.
