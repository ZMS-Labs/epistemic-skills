# v7.0.0 handbook publication

The 24-page source snapshot describes the v7.0.0 contract. Neutral version
banners do not claim that a tag, GitHub Release, or live Wiki publication already
exists. Canonical repository links are pinned to v7.0.0; local source targets can
be checked before the tag exists, and HTTP links must be checked after publication.
The v6 snapshot remains unchanged.

## Check before publication

```text
python docs/wiki-updates/v7.0.0/stage_wiki.py --self-test
python docs/wiki-updates/v7.0.0/stage_wiki.py --check
python docs/wiki-updates/v6.0.0/check_wiki.py docs/wiki-updates/v7.0.0/pages
python docs/wiki-updates/v6.0.0/check_wiki.py docs/wiki-updates/v6.0.0/pages --source-ref v6.0.0
```

Use a new clone if an existing wiki checkout has local changes. The staging helper
refuses dirty or unrelated repositories and unrecognized legacy pages. It
replaces known legacy addresses with useful navigation to current guidance and
links to the retained historical v6 snapshot. The existing wiki Git history and
non-page files remain untouched. Internal source `.md` links become wiki page
slugs during staging; canonical repository links remain version-pinned URLs.

For a complete read-only preview against the actual clean wiki inventory:

```text
python docs/wiki-updates/v7.0.0/stage_wiki.py --check --wiki <clean-wiki-clone>
```

## Stage only after the real release exists

The local annotated `v7.0.0` tag, public remote tag, approved source commit, tagged
package version, and published non-draft GitHub Release must agree. The helper
reads snapshot content from that tag, not from mutable working files. It validates
source targets and the complete resulting wiki with the existing checker before
writing any page. It does not commit or push.

```text
python docs/wiki-updates/v7.0.0/stage_wiki.py --wiki <clean-wiki-clone> --expected-sha <approved-release-commit>
python docs/wiki-updates/v7.0.0/stage_wiki.py --wiki <clean-wiki-clone> --expected-sha <approved-release-commit> --apply
python docs/wiki-updates/v6.0.0/check_wiki.py <clean-wiki-clone> --source-ref v7.0.0 --links
git -C <clean-wiki-clone> diff --check
git -C <clean-wiki-clone> diff --stat
```

After review, the publication owner commits and pushes the staged wiki pages.
Verify the remote wiki commit, read back published pages, and rerun the live wiki
workflow. That workflow derives its expected source from the latest actually
published GitHub Release. A source snapshot, staged clone, or local wiki commit
alone is not live publication evidence. Do not run the historical v6 rewrite
helper to publish v7.
