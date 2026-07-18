# DCO live proof — 2026-07-17

The repository's DCO workflow was exercised against GitHub pull requests after the workflow reached the default branch.

- Negative control: pull request #10 used commit `88ac20e07a3598209a3a43f5ed2eb4dcdc87e480` without a `Signed-off-by` trailer. The `DCO` job failed in 5 seconds. The pull request was closed without merge and its disposable branch was removed.
- Positive control: the signed commit that adds this receipt is the positive control. It must receive a successful live `DCO` check before merge.

The local checker also has synthetic coverage for fully signed history, unsigned history, mixed signed/unsigned history, and a sign-off whose identity does not match the commit author.
