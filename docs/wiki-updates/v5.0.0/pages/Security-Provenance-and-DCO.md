> **Maintainer handbook:** current development
>
> **Released baseline:** [v3.0.0 release-security workflow](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/.github/workflows/release-security.yml)
>
> Historical review records are dated evidence about their frozen subjects. They are not standing certification of later commits.

# Security, Provenance, and DCO

The repository's publication trust is layered: contribution rights, source provenance, secret scanning, static analysis, exact-head review, and immutable release identity answer different questions. No one green check substitutes for the rest.

## License and contribution rights

epistemic-skills is distributed under [GPL-3.0-or-later](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/LICENSE). Contributions use Developer Certificate of Origin 1.1 sign-off.

Every commit in a pull request must contain a `Signed-off-by` trailer matching the commit author identity:

```text
git commit --signoff
```

DCO is a contributor declaration of the right to submit the work. It is not a correctness review, malware scan, cryptographic signature, or copyright investigation by the workflow.

## DCO workflow design

The released [`dco.yml`](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/.github/workflows/dco.yml) runs on `pull_request_target` with read-only content and pull-request permissions. It checks out the trusted base revision—not the untrusted pull-request head—and executes the base branch's checker.

The policy test suite covers:

- fully signed history;
- unsigned history;
- mixed signed and unsigned history; and
- a sign-off identity that does not match the commit author.

The dated [DCO live proof from 2026-07-17](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/docs/release/DCO-LIVE-PROOF-2026-07-17.md) records a negative control that failed and a signed positive path. It demonstrates that historical workflow exercise; it does not certify future commits. Every new pull request must pass its own DCO check.

## Full-history secret scanning

The released [`release-security` workflow](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/.github/workflows/release-security.yml):

1. checks out complete Git history with `fetch-depth: 0`;
2. installs gitleaks v8.30.1;
3. writes a disposable planted private-key-shaped fixture;
4. requires gitleaks to detect that positive control with the expected finding status; and
5. scans the complete repository history with redaction enabled.

The positive control matters: a clean scanner exit is not useful evidence if the scanner was incapable of detecting the target class. Redaction prevents findings from being copied into public logs.

Do not print suspected secret values while diagnosing a failure. Report detector class, file/history coordinate as safely redacted, and remediation state.

## CodeQL

CodeQL success on the exact release-PR head is a non-waivable release gate. The v3.0.0 release record states that CodeQL passed at the frozen feature head and requires it again for the exact release head.

CodeQL configuration may be owned by GitHub or organization settings rather than a checked-in workflow in this repository. Do not infer absence or success from `.github/workflows` alone. Verify the check suite for the exact commit and retain the run coordinate required by the release packet.

Static analysis is not a provenance review and cannot detect every secret, malicious intent, licensing issue, or behavioral error.

## Public-content and provenance review

Before release, independently review the public diff and history for:

- secrets, credentials, and confidential material;
- private infrastructure names, paths, topology, and operational telemetry;
- vendored or copied third-party content and assets;
- licenses, attribution, and research citations;
- generated or model-assisted content provenance where material;
- executable install or supply-chain changes;
- retained run artifacts that were intended to remain local; and
- links to missing, private, or mutable evidence.

The [2026-07-17 public release review](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/docs/release/PUBLIC-RELEASE-REVIEW-2026-07-17.md) and [2026-07-21 addendum](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/docs/release/PUBLIC-RELEASE-REVIEW-ADDENDUM-2026-07-21.md) are useful examples. Their scope ended at named historical revisions. The addendum found and removed or scrubbed private-topology material without rewriting history. Neither document is a standing claim that later commits are clean.

## Provenance of evaluation evidence

Behavioral and diagnostic records should retain:

- exact source revision and content hash;
- protocol and fixture version;
- provider, model, judge, and runtime identity;
- prompt or reconstructable prompt hash;
- call/seat accounting, including zero-token failures;
- normalization and missingness;
- independent-review boundary; and
- release-credit status.

A local tree hash identifies retained local evidence but does not make it committed release evidence. A handoff receipt is a producer self-issued declaration: its verifier establishes schema/hash binding and envelope well-formedness only, not origin/authenticity, the truth of self-reported provenance, verdict truth, or independence.

## Supply-chain discipline

- Pin stable user installs to an immutable version tag.
- Keep GitHub Actions dependencies pinned according to repository policy; do not casually replace immutable action coordinates.
- Treat install scripts and role renderers as executable supply-chain surfaces.
- Keep one canonical skills tree and one installed copy per harness.
- Review any new network fetch, package installer, or executable dependency.
- Preserve full history and failed epochs unless a separately authorized security response requires a different action.

## Exact-head release checklist

For the final release candidate, verify all of the following on the same commit:

- DCO passes every release-PR commit;
- deterministic repository checks pass;
- CodeQL passes;
- full-history gitleaks scan passes after its positive control proves detection;
- public-content and provenance review covers the complete diff;
- no unredacted finding appears in logs or documentation;
- version and immutable install coordinates agree;
- independent publication review and Gauntlet complete; and
- annotated tag, Release target, `main`, and committed notes agree.

Operator risk acceptance applies only to its named behavioral-confidence gaps. It has no publication authority over this checklist.

## Sources

- [Released DCO workflow](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/.github/workflows/dco.yml)
- [Released security workflow](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/.github/workflows/release-security.yml)
- [Released public-review record](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/docs/release/PUBLIC-RELEASE-REVIEW-2026-07-17.md)
- [Released public-review addendum](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/docs/release/PUBLIC-RELEASE-REVIEW-ADDENDUM-2026-07-21.md)
- [Released risk record and non-waivable gates](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/docs/release/RELEASE-3.0.0-RISK-ACCEPTANCE.json)
- **Current development:** [workflows on `main`](https://github.com/ZMS-Labs/epistemic-skills/tree/main/.github/workflows)
