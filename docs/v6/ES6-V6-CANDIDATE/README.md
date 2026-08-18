# ES6-V6-CANDIDATE — BUILD freeze (issue #191)

This packet is the v6 **BUILD** freeze against an exact candidate SHA. It is
not PROMOTION. It does not merge, tag, close tracker items, or record
Gauntlet GO.

Parent: [epistemic-skills#191](https://github.com/ZMS-Labs/epistemic-skills/issues/191)

## Terminal contract vs this packet

`#191` reaches `V6_CANDIDATE_READY_FOR_OPERATOR_ACCEPTANCE` only when an
**independent** Gauntlet computes GO with no unresolved P1/P2 blockers.
This actor produced the candidate, so `self_certification: refused` and
`readiness: NOT_READY`.

What this packet *does* complete of the BUILD contract:

- a machine-readable claim-to-proof matrix covering every **class** claim
  and every **open tracker item** at generation time
- current issue/PR reconciliation with explicit dispositions
- source inventory
- requalification evidence that can run from this checkout (clean-room
  stdlib steps, workflow oracle audit, public-content gate, custody suite)
- an immutable promotion packet naming known limits, rollback, and
  **zero** requested irreversible acts

## SHAs for this freeze

| Role | SHA |
|---|---|
| Packet `candidate_sha` / `exact_start_sha` | freeze commit that first contained this packet |
| es#137 P1+P2 code (not on `main`) | `e8a476c730750a9b3e51ac1001b96825996187cc` |
| Clean-room evidence subject | `evidence/clean-baseline.json` `exact_start_sha` |

Committing JSON artifacts creates a child SHA. The follow-up evidence commit
records clean-room of the freeze commit and is not itself a second candidate.

## Honest gaps (do not read as GO)

Operator holds: `#104`, `#186` tag-ruleset remainder, `#84` field-pair, `#40`.
Live-environment LIMITED: `#77`, `#39`, `#136`, `#129`, `#142`.
Platform LIMITED: `#162` (macOS) and `CLM-WINDOWS-FS`.
Integrity: es#137 is closed in **this tree** and still open on `main`.
Draft PRs skip required CI jobs; local clean-room is the BUILD oracle.

## Regenerate

```bash
python .github/scripts/v6_generate_candidate_packet.py
python .github/scripts/v6_audit_workflow_oracles.py --write docs/v6/ES6-V6-CANDIDATE/evidence/workflow-oracle-audit.json
python .github/scripts/v6_collect_candidate_evidence.py \
  --public-content docs/v6/ES6-V6-CANDIDATE/evidence/public-content.json \
  --custody docs/v6/ES6-V6-CANDIDATE/evidence/custody-suite.json
# After committing the freeze files, requalify that SHA:
python .github/scripts/v6_run_clean_baseline.py \
  --program ES6-V6-CANDIDATE \
  --packet ES6-V6-CANDIDATE-REQUAL \
  --write docs/v6/ES6-V6-CANDIDATE/evidence/clean-baseline.json
python plugins/epistemic-skills/contracts/v6-assurance/validate_v6_assurance.py
```
