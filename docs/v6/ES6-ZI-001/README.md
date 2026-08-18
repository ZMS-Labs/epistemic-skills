# ES6-ZI-001 — first bounded BUILD run (issue #191)

Parent: [epistemic-skills#191](https://github.com/ZMS-Labs/epistemic-skills/issues/191)

This directory holds artifacts for the **first** authorized v6.0 BUILD packet.
It does **not** implement mission-custody fixes, merge release PRs, or close
tracker items. Those belong to later packets or PROMOTION.

## Three ordered packets

| Packet | Artifact | Status |
|---|---|---|
| **ES6-BASELINE-CLAIMS** | `exact-start-receipt.json`, `claim-to-proof-matrix.json`, `issue-pr-reconciliation.json`, `source-inventory.json` | complete |
| **ES6-ORACLE-AUDIT** | `.github/scripts/v6_audit_workflow_oracles.py` + `evidence/workflow-oracle-audit.json` | complete (0 findings) |
| **ES6-CLEAN-BASELINE** | `evidence/clean-baseline.json` | complete (32/32 pass) |

## Sequencing rule

Working through “every open item” means **reconciling** each item to evidence or
an explicit disposition in the matrix — not closing all 41 issues in one pass.
Implementation order follows the decision map:

1. Frontier operator decisions (#186 tag governance, #104 implement-vs-retire, #190)
2. Parent decisions (#173, #118, #150, #166, #149, #148)
3. Later BUILD custody/behavioral/harness packets (explicitly deferred by #191)

## Regenerate

```bash
python .github/scripts/v6_generate_baseline_claims.py
python .github/scripts/v6_audit_workflow_oracles.py --write docs/v6/ES6-ZI-001/evidence/workflow-oracle-audit.json
python .github/scripts/v6_run_clean_baseline.py --write docs/v6/ES6-ZI-001/evidence/clean-baseline.json
python plugins/epistemic-skills/contracts/v6-assurance/validate_v6_assurance.py
```
