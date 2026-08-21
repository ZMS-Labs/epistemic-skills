# Epistemic Skills v6.0.0 publication-gate dossier

- **Run ID:** `es-v6-publication-openai-2026-08-20`
- **Frozen subject:** `d0165bd0cf1e79b94140d4493cc11bf7ba31a2a3`
- **Subject tree:** `dea62d357da2b3d617aa3c23809094772c7bc39e`
- **Subject archive SHA-256:** `cfb219c6ae11b13fff607186e6fd337a2540aa9616a2f9078e88decf4099b42b`
- **Review date:** 2026-08-20
- **Requested seat:** OpenAI GPT-5.6, operator-dispatched publication gate
- **Repository:** `ZMS-Labs/epistemic-skills`

This dossier freezes the evidence used for the ruling in `arbitration.md`. The
review was performed from a clean checkout of the exact subject and from live
GitHub metadata. It did not treat an implementer-authored verdict, release-note
assertion, merge message, or green self-test as independent publication
authorization.

## Independence and authority

The adjudicating seat had not authored the candidate and did not participate in
the prior v6 implementation or verdict lineage. The candidate commit is authored
by `SternOne` and carries an Anthropic/Claude sign-off; this review is authored by
an OpenAI model family. The internal adversarial, constructive, governance, and
judge passes used to challenge the dossier were all OpenAI-family passes, so they
provide role isolation but not additional model-family diversity. The binding
publication result is this independent seat's ruling, not a vote count.

The operator request authorized only a review branch and verdict artifact. This
run did **not** merge, tag, create a Release, change the tag ruleset, mutate the
promotion packet, record operator acceptance, or grant publication authorization.

## Frozen observations

### Repository identity and delta

- `origin/main`, the local subject, and `git ls-remote origin refs/heads/main`
  resolved to the exact subject at review time.
- `92b3ca6cf7009cb668146b526e3b35012f7454a6` is an ancestor of the subject.
- The only file changed from that parent to the subject is
  `docs/release/RELEASE-6.0.0.md` (`+25/-10`). This is a post-freeze
  release-note correction, and therefore a new candidate under
  `RELEASING.md` procedure step 4.
- No `v6.0.0` tag or GitHub Release existed at review time.
- Live ruleset `protect-version-tags` (ID `20090781`) was active for
  `refs/tags/v*`, with creation, update, and deletion restrictions and no listed
  bypass actor.

### Exact-SHA checks

GitHub showed these successful checks on the exact subject:

| Run | Workflow | Conclusion |
|---|---|---|
| `32415190757` | epistemic-flexibility | success |
| `32415190700` | release-security | success |
| `32415190928` | commission-watch-contract | success |
| `32415189193` | CodeQL (Python, Actions, JavaScript/TypeScript) | success |

GitHub showed **no** exact-subject run for `openai-bundles` or
`mission-custody-contract`. The release note instead cites the five manual runs
at parent SHA `92b3ca6cf7009cb668146b526e3b35012f7454a6`. That parent set includes a
successful required Linux custody job and a failed dispatch-only macOS job. The
macOS log's two failures were
`distinct-real-file-untouched` and
`distinct-both-files-tracked-separately`; the documented es#162 probe passed.
This review does not convert that diagnostic job failure into a separate
release blocker, but parent evidence cannot satisfy an exact-candidate rule.

### Exact-SHA DCO result

The subject is a one-parent commit authored by the `SternOne` GitHub noreply
identity. Its only sign-off trailer names the separate `Claude` Anthropic
noreply identity. The addresses themselves are omitted to comply with the
repository's public-content policy.

```text
author identity: SternOne
sign-off identity: Claude
```

Running the repository's own `.github/scripts/check_dco.py` logic against the
exact commit returned `d0165bd0cf1e` in `unsigned_commits`. The commit is neither
a merge commit nor one of the five SHA-attested exceptions. This matches
`CONTRIBUTING.md`, which requires an author-matching sign-off and specifically
warns that squash commits must also be signed off. The DCO workflow is
`pull_request_target`-scoped and did not validate this landed squash commit.

### Deterministic local verification

All fourteen commands in the requested deterministic crib exited zero, including
the v6 assurance validator and its 38-control test, public-content self-tests and
live scan, phantom-file checks, DCO self-test, surface synchronization, JSON
validation, ledger checks, outsource tests, gauntlet tests, custody tests, and
wiki self-test. A fresh `cleanroom_ci.sh` run against the exact subject reported
`54/55` steps (`54` pass, `1` CI-context skip, `0` fail). The clean-room script
does not reproduce DCO, `openai-bundles`, `mission-custody-contract`,
`commission-watch-contract`, or `release-security`, so these green local results
do not close the missing exact-SHA workflow evidence or the exact-commit DCO
failure.

### Packet and prior verdict lineage

- `docs/v6/ES6-V6-CANDIDATE/promotion-packet.json` is a historical BUILD-freeze
  record for `03e972c5...`, says `NOT_READY`, has no `operator_acceptance`, and
  leaves `CLM-INDEPENDENT-GAUNTLET` as its only blocking claim. Recomputing its
  blocking claims produced the same list. Its validator success is therefore an
  honest nonterminal result, not publication evidence for the subject.
- Seven prior in-tree gauntlet run directories were compared with their named
  remote branches. Their private-coordinate edits are mechanical public-surface
  redactions. Six are `NO-GO`; the sole `GO` is for the historical BUILD freeze
  `03e972c5...`. None adjudicates or transfers to the subject.
- The cited v5.1 precedent does not support parent-only workflow evidence:
  `docs/release/RELEASE-5.1.0.md` records that path-filtered workflows were
  manually re-dispatched at its final tagged SHA.
- Issue `#191` reserves promotion actions to a separate current operator
  approval. Its D8 ratification requires the Step 7b consult at the next GO
  posture before acceptance. No later acceptance was found.

### Governing-text conflict

`RELEASING.md` requires the complete deterministic suite, DCO, parity, JSON, and
all CodeQL jobs on the exact candidate; step 4 says every exact-commit integrity
workflow is rerun and any correction creates a new candidate that invalidates
earlier evidence; step 5 requires the independent Gauntlet on that exact
candidate; step 7 requires committed release-note authorization naming the
verdict, exact candidate SHA, and owner before disarm.

As written, adding the post-GO packet/acceptance/authorization records changes
the commit and invalidates the exact-SHA evidence and verdict that those records
must cite. The text defines no narrow transfer rule or out-of-tree control record
that closes this fixed point. This is a governance defect, not permission to
silently substitute parent evidence.

### Release-record accuracy

The subject's release note says its own correction is "pending merge" although it
is already on `main`, says the public-content self-test has seven seeds although
the current test reports eight, and reports 229 changed files while
`git diff --name-only v5.1.0..HEAD` reports 232. The live public-content scan
passed; these are record-accuracy defects, not evidence of a current secret leak.

## Evidence limits

- Native Windows behavior was not re-executed.
- The ruleset's practical bypass behavior was not tested because changing or
  attempting to bypass it was outside this seat's authority.
- The review did not publish packages or run live harness installs because no
  release tag exists and publication was explicitly forbidden.
- Same-family internal lenses are disclosed above; cross-family independence is
  between this seat and the candidate-authoring lineage.
