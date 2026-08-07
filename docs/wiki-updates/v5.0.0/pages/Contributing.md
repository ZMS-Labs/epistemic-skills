> **Maintainer handbook:** current development
>
> **Released policy baseline:** [v5.0.0 `CONTRIBUTING.md`](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/CONTRIBUTING.md)
>
> **Current development:** [`CONTRIBUTING.md` on `main`](https://github.com/ZMS-Labs/epistemic-skills/blob/main/CONTRIBUTING.md) is mutable and controls new pull requests when it differs from this page.
>
> **v5.0.0 note:** invoke [`metacognate`](Skill-Metacognate) when the approach is uncertain; do not look for deleted `using-epistemic-skills` / `helix` seats. Inventory is fourteen skills — see the [Skill Catalog](Skill-Catalog).

# Contributing

Contributions are accepted under GPL-3.0-or-later and Developer Certificate of Origin 1.1 sign-off. The maintainer objective is proportionate, reviewable change—not artifact volume.

## Ordinary contributions use the routine path

A typo fix, local copy adjustment, private-helper rename, or similarly bounded change does not require the whole epistemic arc when it is all four of:

1. reversible by ordinary revert;
2. local to the artifact, with no security, privacy, authorization, tenancy, billing, legal, infrastructure, network, public-contract, migration, or cross-service boundary;
3. directly checkable by a targeted test, preview, reproduction, or comparable bounded observation; and
4. non-precedential, with no unresolved decision, scholarly premise, authorization, or cross-session judgment to preserve.

For unfamiliar but routine-looking work, inspect the target file and its nearest test or example. If both agree with the requested change and the four conditions still hold, make the smallest coherent edit and run the bounded check.

Do not manufacture a router skip inventory, Blindspot report, formal-rigor record, ledger entry, Gauntlet dossier, UAT packet, or other process-only artifact for a routine no-op. [Routine Work and Proportionality](Routine-Work-and-Proportionality) explains the released rule.

## Escalate from evidence, not size

Use a discipline when the first reads expose a positive trigger:

| Observed boundary | Likely discipline |
|---|---|
| Map/territory mismatch, hidden coupling, unresolved scope, or fan-out risk | [Blindspot Pass](Skill-Blindspot-Pass) |
| Consequential design fork or software/system property question | [Applying Formal Rigor](Skill-Applying-Formal-Rigor) |
| Load-bearing scholarly premise | [Evidence Research](Skill-Evidence-Research) |
| Explicit request for a persistent goal | [Write Goal](Skill-Write-Goal) |
| Consequential decision not already adequately persisted | [Decision Ledger](Skill-Decision-Ledger) |
| External model/process handoff that must bear load | [Outsource](Skill-Outsource) |
| High-stakes or irreversible frozen decision | [Gauntlet](Skill-Gauntlet) |
| Material user-visible completion claim | [Evidence-Locked UAT](Skill-Evidence-Locked-UAT) |

If a workflow-skill layer is active, [Helix](Helix-Central-Passage) is the central passage that pairs the workflow stage with the positively triggered discipline. It does not require every skill or replace the routine exit.

## Repository invariants

Before editing, preserve these structural properties:

- `plugins/epistemic-skills/skills/` is the only canonical skill implementation tree.
- `plugins/epistemic-skills/agents/` is the only canonical Gauntlet role tree.
- root `skills` and `agents` are symlinks, not copied implementations.
- harness manifests are thin adapters and must not acquire divergent method text.
- the collection contains fourteen skills: router, Helix, and nine disciplines.
- `using-epistemic-skills` remains the epistemic router; Helix remains the central passage between layers.
- routine exits and absent triggers remain silent.
- focused formal rigor stays inline and record-free; standard/high-assurance work uses `formal-rigor-record@2`.
- schema and closed-vocabulary additions change the verifier and tests in the same pull request.

See [Architecture and Contracts](Architecture-and-Contracts) and [Cross-Harness Packaging](Cross-Harness-Packaging).

## Make the smallest contract-complete change

1. Reproduce or identify the exact contract mismatch.
2. Locate the canonical source and nearest discriminating test.
3. When behavior is changing, establish a RED case before the production edit.
4. Patch only the files needed to close the mismatch.
5. Run the targeted test, then the relevant integration surface.
6. Update stable documentation only when the released contract changes; label current-development links.
7. Preserve historical evaluations and failed epochs. Add corrected evidence at new coordinates rather than overwriting the original.
8. Review the diff for scope creep, duplicate implementations, silent degradation, and unsupported claims.

Invocation count, token spend, panel size, and artifact count are not contribution-quality metrics.

## Tests by change type

| Change | Required focus |
|---|---|
| Skill trigger or router rule | Positive and negative trigger fixtures, routine/proportionality polarity, package integration |
| Skill method or handoff | Targeted fixtures plus producer/consumer contract tests |
| Schema, receipt, or record vocabulary | Verifier and schema in the same PR, valid/invalid examples, downstream checks |
| Scorer or evaluator | Passing and parody/negative controls; retain prior results unchanged |
| Harness manifest or path | JSON parsing, path resolution, eleven-skill inventory, version parity, targeted harness validation if claimed |
| Python script | Targeted test and compilation |
| Documentation only | Local-link, immutable-coordinate, version/claim, and whitespace checks |
| Release surface | The complete release gate, not a targeted subset |

The executable map lives in [Testing and Evaluations](Testing-and-Evaluations). The exact current workflow on `main` is mutable; inspect it before opening a pull request.

## DCO sign-off

Every commit in a pull request must contain an author-matching `Signed-off-by` trailer:

```text
git commit --signoff
```

The trailer certifies that the contributor has the right to submit the work under the repository license. It is not a cryptographic signature and does not itself prove correctness. See [Security, Provenance, and DCO](Security-Provenance-and-DCO).

Before pushing, inspect the authored range:

```powershell
git log --format=fuller origin/main..HEAD
git log --format='%H%n%an <%ae>%n%B%n---' origin/main..HEAD
```

Every commit—not merely the latest—must pass the repository's identity-matching DCO rule.

## Pull-request content

A reviewable pull request states:

- the user-visible or contract-level problem;
- the smallest coherent change;
- exact verification commands and results;
- affected release/harness surfaces;
- known limitations or intentionally untested claims;
- migration impact, if any; and
- evidence coordinates for behavioral work.

For a routine change, that can be a short description and one bounded check. For a contract or release change, it should be correspondingly richer. Do not inflate routine work to resemble a release packet.

## Documentation discipline

The repository contract controls the Wiki. When documentation describes stable behavior:

- anchor it to `v3.0.0` or a later immutable release;
- label `main` as current development;
- describe historical audits with their date, subject, and original status;
- separate deterministic tests from behavioral evidence and release credit;
- retain the exact known limitations; and
- avoid copying low-level schema or method text when a canonical link is safer.

## Sources

- [Released contribution policy](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/CONTRIBUTING.md)
- [Released routine fast path](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/plugins/epistemic-skills/skills/using-epistemic-skills/reference/routine-fast-path.md)
- [Released DCO workflow](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/.github/workflows/dco.yml)
- **Current development:** [contribution policy on `main`](https://github.com/ZMS-Labs/epistemic-skills/blob/main/CONTRIBUTING.md)
- **Current development:** [test workflow on `main`](https://github.com/ZMS-Labs/epistemic-skills/blob/main/.github/workflows/epistemic-flexibility.yml)
