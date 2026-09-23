> **Applies to:** epistemic-skills v7.1.0.

# What the evidence establishes

The [v7.1.0 release](https://github.com/ZMS-Labs/epistemic-skills/releases/tag/v7.1.0) is published. Its [final publication receipt](https://github.com/ZMS-Labs/epistemic-skills/releases/download/v7.1.0/publication-receipt.json) records the exact source, designated review, required jobs, artifacts, restored tag protections, and publication checks. This is the starting point for release status. The [v7.0.0 release](https://github.com/ZMS-Labs/epistemic-skills/releases/tag/v7.0.0) remains published with its own unchanged records.

The [v7 implementation evidence packet](https://github.com/ZMS-Labs/epistemic-skills/blob/v7.0.0/docs/release/v7-evidence.md) is a pre-publication snapshot. Its conditional verdict records what remained open at that time. Publication did not rewrite that history into a different judgment.

### Read each claim at its evidence level

| Level | Useful evidence | Limit |
|---|---|---|
| Source and contract integrity | Schema validation, inventories, refusal controls, template tests | Does not establish model application |
| Delivery and discovery | Observed installed identity, discovery response, loaded body | Does not establish use or benefit |
| Exercised behavior | A task or runtime observation at a named revision | Covers the observed case and environment |
| Comparative benefit | Valid controlled comparisons with preserved failures | Cannot be inferred from structural checks |

### What passed at release

The [exact release gate receipt](https://github.com/ZMS-Labs/epistemic-skills/releases/download/v7.1.0/exact-gates.json) lists the dispatched runs on the exact v7.1.0 merge commit. Every required job passed: the five dispatchable gate workflows, the required Ubuntu custody contract job, and CodeQL; the macOS custody diagnostic failed the same two known case-insensitive filesystem assertions as at v7.0.0 and is disclosed, not gating. After tagging, the version-tag protection was restored and both seeded probes (git push and the REST ref API) were refused. At v7.0.0, all 10 required hosted jobs had passed (155 required steps, none skipped) and a live check of Codex CLI in an isolated workspace listed all 17 skills; that live host check was not repeated for v7.1.0, which adds no new host support claim.

The [designated review](https://github.com/ZMS-Labs/epistemic-skills/releases/download/v7.1.0/designated-review.json) was done by the ZCode agent that implemented the transfer mode, which the project owner designated as reviewer. It worked in the same context as the implementation, so it is not an independent or blinded review. The v7.0.0 [designated review](https://github.com/ZMS-Labs/epistemic-skills/releases/download/v7.0.0/designated-review.json) by the implementing Codex agent carried the same disclosed limitation.

### Important limits

- macOS custody: required Ubuntu contract checks passed. The dispatch-only macOS diagnostic failed the two known case-insensitive filesystem assertions in [issue #162](https://github.com/ZMS-Labs/epistemic-skills/issues/162); subsequent macOS steps were skipped. The aggregate workflow therefore remains red. No case-insensitive POSIX custody guarantee is claimed.
- v6 to v7 comparison: one baseline attempt ran, but the environment violated the intended provider isolation and blocked necessary reads. The remaining 31 slots were not dispatched. There are zero valid pairs and no v7 superiority claim. See the [preserved pilot result](https://github.com/ZMS-Labs/epistemic-skills/blob/v7.1.0/plugins/epistemic-skills/evals/epistemic-flexibility/behavioral/results/2026-09-18-v7/RESULTS.md).
- Earlier four-arm experiment (August 2026): a preregistered, blinded run of 72 trials compared four versions of the instructions, one of them an empty baseline, on an earlier version of the methods. It found no separation between the four (p = 0.875 on the preregistered main test). Its size and a scoring adapter added after the run make it exploratory, and it supports no superiority claim in any direction. See the [preserved four-arm result](https://github.com/ZMS-Labs/epistemic-skills/blob/v7.1.0/plugins/epistemic-skills/evals/epistemic-flexibility/behavioral/results/2026-08-04-four-arm/RESULTS.md).
- Host application: the [host coverage record](https://github.com/ZMS-Labs/epistemic-skills/blob/v7.0.0/docs/release/v7-host-coverage.md) distinguishes observed discovery from unexercised loading and workflows.
- Acceptance calibration: deterministic UAT record judging does not establish that all observations are correct or empirically calibrated.

For reproducing checks after a change, see [the maintainer guide](https://github.com/ZMS-Labs/epistemic-skills/blob/main/docs/MAINTAINING.md). Retain historical failures and scope; add new evidence instead of silently overwriting them.
