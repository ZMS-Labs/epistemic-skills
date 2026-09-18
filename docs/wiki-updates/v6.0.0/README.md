# Handbook source and publication

`pages/` is the complete committed handbook snapshot for v6.0.0. The published
GitHub Wiki is a separate repository; changing this directory alone does not
publish it. The `wiki-contract` workflow checks the snapshot on pull requests
and the live wiki on its daily schedule.

Validate the snapshot before publishing:

```bash
python docs/wiki-updates/v6.0.0/check_wiki.py --self-test
python docs/wiki-updates/v6.0.0/check_wiki.py docs/wiki-updates/v6.0.0/pages --links
```

Copy the reviewed pages to a clean wiki checkout, inspect the diff, and run the
same checker against that checkout before committing and pushing. Check the
published wiki again after the push. `apply_v6_updates.py` is a limited migration
helper; it does not replace the complete snapshot or verify publication.

The sections below retain the original migration measurements. They describe
the historical v5-to-v6 migration, not the current publication state.

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
