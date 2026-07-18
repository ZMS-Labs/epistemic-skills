# Public release review — 2026-07-17

Repository: `ZMS-Labs/epistemic-skills`

Decision: approved by the ZMS-Labs owner for `GPL-3.0-or-later` publication.

## Ownership and provenance

- Full Git history at baseline `d28a672` contained 33 commits and 75 tracked
  files.
- All commit authors resolve to the same organization owner through the two
  identities `Zachary Stern <zachstern@gmail.com>` and
  `SternOne <89846440+SternOne@users.noreply.github.com>`.
- Some commits disclose model assistance with `Co-Authored-By` trailers. The
  organization owner is the submitting author and rights holder for the
  resulting repository content.
- The original `evidence-locked-uat` publication commit (`36e111b`) records
  `references/standard.md` as the owner's original research synthesis; its
  outbound links are citations rather than reproduced source text.
- `blindspot-pass` credits the external essay that inspired its method and
  expressly states that it does not repackage a third-party skill.
- No vendored dependency source, external asset bundle, or unresolved
  third-party copyright-bearing material was identified. The unmodified GPLv3
  license text remains in the root `LICENSE` file.

## Secret and confidential-material review

Scanner: official `gitleaks` v8.30.1 Windows x64 release, verified against the
publisher's SHA-256 checksum file.

The oracle was proven capable of failing before its clean results were trusted:
the official gitleaks AWS-token test value was planted in a disposable Git
repository and produced the configured finding exit code `42`.

- Full history (`--all`): 33 commits, approximately 1.84 MB scanned, no leaks.
- Current release worktree: approximately 1.00 MB scanned, no leaks.
- GitHub secret-scanning alerts: zero.

No secret value or unredacted finding was copied into this record.

## Actions logs and artifacts

- All 23 retained GitHub Actions run logs were downloaded and scanned.
- Approximately 13.05 MB of logs were scanned; no leaks were found.
- GitHub reported zero Actions artifacts, so there was no artifact payload to
  download or inspect.
- All 23 recorded runs were completed successfully at review time.

## License consistency

- Root `LICENSE`: unmodified GNU GPL version 3 text.
- README and runtime manifests: `GPL-3.0-or-later`.
- Contribution policy: Developer Certificate of Origin sign-off required.
- DCO workflow: base-revision checkout only, read-only permissions, no pull
  request head checkout or execution; signed, unsigned, mixed, and mismatched
  synthetic cases pass/fail as intended.

The repository therefore satisfies the ZMS-Labs public-release gate for the
license change recorded in this release.
