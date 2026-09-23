# v7.1.0 handbook snapshot

The 29-page source snapshot records the handbook as published for v7.1.0.
Unlike the v7.0.0 snapshot (which shipped inside that release's candidate),
this snapshot landed on `main` after the v7.1.0 tag, following the same
sequencing the current editorial handbook itself used for v7.0.0. The wiki
publication for v7.1.0 uses the editorial stager
(`docs/handbook/stage_wiki.py`), which reads pages from a committed public
docs ref and validates the published v7.1.0 tag and Release separately.

Neutral version banners do not claim that a tag, GitHub Release, or live Wiki
publication already exists for any future release. Canonical repository links
are pinned to v7.1.0; local source targets can be checked offline, and HTTP
links require the published tag. The v7.0.0 and v6.0.0 snapshots remain
unchanged and pinned to their own refs.

## Check offline

```text
python docs/wiki-updates/v6.0.0/check_wiki.py docs/wiki-updates/v7.1.0/pages
python docs/wiki-updates/v6.0.0/check_wiki.py docs/wiki-updates/v7.0.0/pages --source-ref v7.0.0
python docs/wiki-updates/v6.0.0/check_wiki.py docs/wiki-updates/v6.0.0/pages --source-ref v6.0.0
python docs/handbook/stage_wiki.py --self-test
python docs/handbook/stage_wiki.py --check
```

## Publish the wiki for v7.1.0

```text
python docs/handbook/stage_wiki.py --wiki <clean-wiki-clone> \
  --docs-ref <committed public main SHA carrying this snapshot> \
  --expected-release-sha 11f21acf14e2331858c960c0f43f681e79dbfb3d --apply
```

The helper stages pages only; review the diff, commit with a sign-off, and
push as separate maintainer actions.
