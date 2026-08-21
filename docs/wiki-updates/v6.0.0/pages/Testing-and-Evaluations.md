> **Maintainer handbook:** current development
>
> **Released baseline:** [v5.0.0 workflows and evaluations](https://github.com/ZMS-Labs/epistemic-skills/tree/v5.0.0/.github/workflows)
>
> **Interpretation rule:** a green structural test, a behavioral observation, a diagnostic result, and release credit are different evidence classes. Prefer `main` command maps when validating post-tag corrective work.
>
> **Relocation note:** proportionality and epistemic-flexibility evals live under `plugins/epistemic-skills/evals/` (relocated from the deleted router seat). Routine-fast-path reference lives under `metacognate/reference/`.

# Testing and Evaluations

This page is a maintainer map of how to verify claims. It is not a substitute for the released workflows or for reading what a result actually proves.

## Evidence classes

| Class | What it can establish | What it cannot establish |
|---|---|---|
| Deterministic / structural | Invariants, schemas, inventory, path integrity, receipt mechanics | Behavioral correctness of a live agent run |
| Behavioral epoch | Observed candidate behavior under a committed design | Universal superiority or cross-provider generality |
| Diagnostic / post-hoc | Named failure modes and risk information | Retroactive release credit (`release_credit: none` stays none) |
| Publication gate | Whether RELEASING.md items were met, waived, or unmet | That a waiver becomes a pass |

## Local entry points (stdlib)

Run from the repository root. These mirror common CI steps; the [epistemic-flexibility workflow](https://github.com/ZMS-Labs/epistemic-skills/blob/main/.github/workflows/epistemic-flexibility.yml) is authoritative for the full gate.

```bash
# Routing / proportionality (package-level evals)
python plugins/epistemic-skills/evals/epistemic-flexibility/run_tests.py
python plugins/epistemic-skills/evals/proportionality/run_tests.py

# Formal-rigor / outsource
python plugins/epistemic-skills/skills/resolve/derivation/evals/formal-rigor-v2-fixtures/tests/run_tests.py
python plugins/epistemic-skills/skills/outsource/tests/run_tests.py

# Shared mechanics
python .github/scripts/check_json_artifacts.py
python plugins/epistemic-skills/contracts/verify_receipt.py --self-test
python plugins/epistemic-skills/skills/evidence-locked-uat/scripts/judge.py --self-test
python plugins/epistemic-skills/skills/gauntlet/tests/run_tests.py

# Inventory / public-content / phantom / surfaces
python .github/scripts/check_no_phantom_skills.py
python .github/scripts/check_public_content.py
python plugins/epistemic-skills/scripts/sync_skill_surfaces.py --check
```

## v5.0.0 honesty for evidence consumers

- Publication item 6 was only PARTIALLY MET; item 8 was WAIVED.
- Post-release independent review: **NO-GO** for retrospective certification.
- Successor corrective work on `main` (issues #104/#105) adds public-content gate, generated routing, intrinsic run ledgers, sentinels, and watch state-machine fixes — not present in the immutable annotated tag unless re-tagged under a new version.

See [Evidence, Status, and Known Limitations](Evidence-Status-and-Known-Limitations) and [Version History](Version-History).

## Canonical references

- [epistemic-flexibility.yml on main](https://github.com/ZMS-Labs/epistemic-skills/blob/main/.github/workflows/epistemic-flexibility.yml)
- [RELEASING.md](https://github.com/ZMS-Labs/epistemic-skills/blob/main/RELEASING.md)
- [EVIDENCE-POLICY.md](https://github.com/ZMS-Labs/epistemic-skills/blob/main/docs/policy/EVIDENCE-POLICY.md)
