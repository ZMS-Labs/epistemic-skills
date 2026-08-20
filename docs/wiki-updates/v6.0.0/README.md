# Wiki update for v6.0.0 — NOT PUBLISHED

**Status: prepared, not applied.** The live `ZMS-Labs/epistemic-skills.wiki`
still serves v5.0.0-era content. This package exists so that gap is a
*reproducible correction* rather than a promise.

It is deliberately a **delta package**, not a 40-page rewrite: the v5.0.0
package under `docs/wiki-updates/v5.0.0/` remains the base, and this applies the
drift measured on top of it.

## Why this exists

Publication-gate finding **PG-08**. The v5.1.0 release recorded a post-tag
handbook pass as a follow-up and it was never performed — "we will fix the wiki
after the tag" is 0-for-1 in this project. So the correction ships as runnable
code with a self-test, and the gap is recorded in the release note with an owner
and an exit criterion.

## Measured drift (2026-08-20, by cloning the wiki)

| Rule | Occurrences | Pages |
|---|---|---|
| `applies-to-banner` | 26 | 26 |
| `discipline-count` | 5 | 4 |
| `retired-seat-present-tense (MANUAL)` | 9 | 9 |
| `skill-count-lower` | 6 | 5 |
| `skill-count-title` | 1 | 1 |
| `tagged-tree-url` | 219 | 40 |

Plus one page that does not exist at all: **`Skill-Manifest`** — the seat
carrying this release's headline security fix. It is authored here under
`pages/`.

## How to use it

The wiki is a separate repository, so no CI job can run this against the thing
it edits. It is written to be checkable instead:

```bash
# Prove the rules on fixtures — no wiki needed.
python docs/wiki-updates/v6.0.0/apply_v6_updates.py --self-test

# See exactly what would change. Default is dry-run; writes nothing.
git clone https://github.com/ZMS-Labs/epistemic-skills.wiki.git /tmp/es-wiki
python docs/wiki-updates/v6.0.0/apply_v6_updates.py /tmp/es-wiki

# Write, then review the diff before pushing.
python docs/wiki-updates/v6.0.0/apply_v6_updates.py /tmp/es-wiki --apply
git -C /tmp/es-wiki diff
```

## What it will NOT do for you

The retired-seat rule is **advisory and reported only**. Nine pages describe
seats deleted in v4.0.0/v5.0.0 in the present tense, and rewriting a sentence's
tense mechanically produces confident nonsense. The script names the pages; a
human edits them.

The tagged-URL and banner rules bump to `v6.0.0`. **Do not apply them until the
tag exists** — the README learned this the expensive way (PG-18): pointing at an
unpublished tag ships dead links.

## Exit criterion

Installation and catalog pages read fifteen skills with v6.0.0 install guidance,
a `Skill-Manifest` page exists, and retired seats are described in the past
tense. Until all four hold, the gap recorded in `docs/release/RELEASE-6.0.0.md`
stays open.
