# Contributing

Contributions are accepted under the repository's
`GPL-3.0-or-later` license and the Developer Certificate of Origin 1.1.

## Ordinary contributions do not require the whole arc

A contributor fixing a typo, changing local copy or styling, renaming a private
helper, or making another reversible/local/directly-checkable/non-precedential
change is not expected to create a Gauntlet dossier, formal-rigor record,
decision-ledger entry, UAT manifest, entry-point skip inventory, or similar process
artifact.

For unfamiliar routine-looking work, inspect the file being changed and its
nearest test/example, make the smallest change, and report the bounded check.
Escalate only when those reads expose a real positive trigger: hidden coupling,
a material design fork, a scholarly premise, external delegation, a persistent
goal, material UI acceptance uncertainty, or a high-stakes/irreversible
boundary.

The normative gate is
[`routine-fast-path.md`](plugins/epistemic-skills/skills/metacognate/reference/routine-fast-path.md).
Maintainers may ask for a discipline when its trigger is present; invocation
count and artifact volume are never contribution-quality metrics.

## DCO

Every commit in a pull request must include a `Signed-off-by` line matching the
commit author. Create one automatically with:

```text
git commit --signoff
```

By signing off, you certify that you have the right to submit the contribution
under this repository's license. The full DCO text is available at
<https://developercertificate.org/>.

### What the check actually enforces

The rule above is the rule for contributors. `.github/scripts/check_dco.py`
applies it with exactly two exceptions, both deliberate and both narrow:

1. **Merge commits that author nothing are exempt.** A merge whose tree is
   exactly what a clean three-way merge of its parents produces contains no
   authored content, and its author is whoever ran `git merge`; the DCO
   certifies authored contributions.

   **A merge that resolves a conflict is not exempt.** Its tree differs from the
   clean result, and that difference is hand-written content like any other, so
   it requires an author-matching sign-off. Use `git merge --signoff`, or amend
   the resolution with one.

   This was a recorded *limit* until 2026-08-21 — the exemption applied to every
   merge unconditionally, so content could ship uncertified by routing it
   through a conflict. It is now enforced: the checker recomputes the clean
   merge with `git merge-tree` and compares trees. A merge it cannot classify,
   because the objects are missing, fails closed rather than being waved
   through — an exemption that cannot be verified is not an exemption.
2. **A closed list of five commits** is certified by the repository owner by
   exact 40-hex SHA. They predate this workflow's coverage of the branch they
   live on. The list is closed and content-bound: any amend or rebase produces a
   different SHA and fails. A new unsigned commit is a defect to fix with
   `git commit --amend --signoff`, never a new entry.

**Release candidates are merged with a merge commit, not a squash.** A squash
attributes the resulting commit to whoever merged it, so a `Signed-off-by`
trailer naming any other identity is an author mismatch — and asserting a
sign-off for an identity that did not author the commit is a false attestation,
worse than an absent trailer. A merge commit keeps the individually signed
commits in history and is exempt under the rule above.

Two limits worth knowing. The check runs against a pull request's commits, so it
does not run against the commit a squash-merge actually creates — sign those off
too. And GitHub's pull-request commits endpoint returns at most 250 commits; past
that the check fails closed rather than certifying a range it cannot read.
