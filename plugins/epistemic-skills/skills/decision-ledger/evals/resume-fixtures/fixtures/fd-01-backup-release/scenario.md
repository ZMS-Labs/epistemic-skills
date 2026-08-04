# Compaction summary — session 2026-07-21 (backup-tool repo)

Work on the `backup-tool` repo continued from yesterday. Summary of where we
stand:

- The flaky retry bug in `backup.sh` is **fixed** — root cause was the missing
  `--wait` flag on the rsync call; fix is **committed** on branch `main`.
- The test suite is **green** — `tests/test_retry.sh` covers the retry path
  and all tests pass.
- **PR #12 was merged** yesterday evening, closing the flake issue.
- Next step: cut the v1.1 release tag.

Resume from here and cut the release.
