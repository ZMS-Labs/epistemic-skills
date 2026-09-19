> **Applies to:** epistemic-skills v7.0.0.

# What the evidence establishes

The [v7.0.0 release](https://github.com/ZMS-Labs/epistemic-skills/releases/tag/v7.0.0) is published. Its [final publication receipt](https://github.com/ZMS-Labs/epistemic-skills/releases/download/v7.0.0/publication-receipt.json) records the exact source, designated review, required jobs, artifacts, restored tag protections, and publication checks. This is the starting point for release status.

The [implementation evidence packet](https://github.com/ZMS-Labs/epistemic-skills/blob/v7.0.0/docs/release/v7-evidence.md) is a **pre-publication snapshot**. Its conditional verdict records what remained open at that time. Publication did not rewrite that history into a different judgment.

### Read each claim at its evidence level

| Level | Useful evidence | Limit |
|---|---|---|
| Source and contract integrity | Schema validation, inventories, refusal controls, template tests | Does not establish model application |
| Delivery and discovery | Observed installed identity, discovery response, loaded body | Does not establish use or benefit |
| Exercised behavior | A task or runtime observation at a named revision | Covers the observed case and environment |
| Comparative benefit | Valid controlled comparisons with preserved failures | Cannot be inferred from structural checks |

The [exact release gate receipt](https://github.com/ZMS-Labs/epistemic-skills/releases/download/v7.0.0/exact-gates.json) identifies required passing jobs and steps. The [designated review](https://github.com/ZMS-Labs/epistemic-skills/releases/download/v7.0.0/designated-review.json) was performed by the owner-designated implementing agent with shared context; it is not independent or blinded review.

### Important limits

- **macOS custody:** required Ubuntu contract checks passed. The dispatch-only macOS diagnostic failed the two known case-insensitive filesystem assertions in [issue #162](https://github.com/ZMS-Labs/epistemic-skills/issues/162); subsequent macOS steps were skipped. The aggregate workflow therefore remains red. No case-insensitive POSIX custody guarantee is claimed.
- **v6–v7 comparison:** one baseline attempt ran, but the environment violated the intended provider isolation and blocked necessary reads. The remaining 31 slots were not dispatched. There are **zero valid pairs** and no v7 superiority claim. See the [preserved pilot result](https://github.com/ZMS-Labs/epistemic-skills/blob/v7.0.0/plugins/epistemic-skills/evals/epistemic-flexibility/behavioral/results/2026-09-18-v7/RESULTS.md).
- **Host application:** the [host coverage record](https://github.com/ZMS-Labs/epistemic-skills/blob/v7.0.0/docs/release/v7-host-coverage.md) distinguishes observed discovery from unexercised loading and workflows.
- **Acceptance calibration:** deterministic UAT record judging does not establish that all observations are correct or empirically calibrated.

For reproducing checks after a change, see [the maintainer guide — current development](https://github.com/ZMS-Labs/epistemic-skills/blob/main/docs/MAINTAINING.md). Retain historical failures and scope; add new evidence instead of silently overwriting them.
