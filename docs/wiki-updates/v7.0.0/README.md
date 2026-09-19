# v7.0.0 candidate handbook

Status: prepared, not published to the live Wiki. Pages are source-tree-relative
and link to canonical methods; publish only after candidate and link identity are
verified. Preserve the v6 snapshot unchanged.

```text
python docs/wiki-updates/v6.0.0/check_wiki.py --self-test
python docs/wiki-updates/v6.0.0/check_wiki.py docs/wiki-updates/v7.0.0/pages
python docs/wiki-updates/v6.0.0/check_wiki.py docs/wiki-updates/v6.0.0/pages --source-ref v6.0.0
```

The existing handbook checker now accepts `--source-ref` to derive historical
inventory and version from an actual Git revision. The default still checks the
current canonical source. Source-root and live URL checks remain available.
