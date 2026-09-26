# v7.2.0 handbook snapshot

The 29-page source snapshot records the handbook for v7.2.0. It lands on
`main` after the immutable release tag, then is published to the separate Wiki
from a committed public documentation ref. The editorial stager
(`docs/handbook/stage_wiki.py`) verifies the published tag and Release before
staging those committed pages.

Version banners identify the release described by each page. Canonical skill
links are pinned to v7.2.0. The v7.1.0, v7.0.0, and v6.0.0 snapshots remain
unchanged at their historical refs.

## Check offline

```text
python docs/wiki-updates/v6.0.0/check_wiki.py docs/wiki-updates/v7.2.0/pages --source-ref v7.2.0
python docs/handbook/stage_wiki.py --self-test
python docs/handbook/stage_wiki.py --check
```

## Publish the Wiki for v7.2.0

```text
python docs/handbook/stage_wiki.py --wiki <clean-wiki-clone> \
  --docs-ref <committed public main SHA carrying this snapshot> \
  --expected-release-sha ce5d2ce616990385975ef1835cb6005bb939e9ea --apply
```

The helper stages pages only; review the diff, commit with a sign-off, and push
as separate maintainer actions.
