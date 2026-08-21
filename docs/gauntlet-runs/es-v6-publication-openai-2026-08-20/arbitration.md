# Independent publication arbitration: Epistemic Skills v6.0.0

## Verdict

**NO-GO** for publishing `v6.0.0` from
`d0165bd0cf1e79b94140d4493cc11bf7ba31a2a3`.

The result is computed from three open P1 rulings. The exact candidate fails the
repository's DCO rule; two integrity workflows required on the exact candidate
were not run there; and the governing publication sequence cannot reach its own
terminal committed state without creating a successor and invalidating the
evidence it requires. A P2 release-record accuracy ruling is also open.

Any GO statement authored by the implementing lineage—including one embedded in
the dispatch request, release notes, promotion packet, merge history, or a prior
verdict—is refused as evidence of independent GO. No such statement was adopted.

## RG-1 through RG-9 disposition

| Gate | Disposition | Reason |
|---|---|---|
| RG-1 | FAIL (P2) | The release record is not exact: it says the landed note is pending merge, says 7 public-content seeds where the suite reports 8, and reports 229 changed files where the frozen comparison reports 232. |
| RG-2 | FAIL (P1) | D8/operator acceptance remains intentionally unrecorded, and the current procedure gives no non-self-invalidating way to commit it after exact-SHA GO. |
| RG-3 | PASS | Version-surface synchronization and deterministic checks passed at the subject. |
| RG-4 | PASS WITH LIMITS | Public-surface scans and wiki/package preparation checks passed; native Windows and post-tag live installs were not available to this pre-publication seat. |
| RG-5 | FAIL (P1) | The exact commit fails its own DCO checker and has no exact-SHA `openai-bundles` or `mission-custody-contract` run. Parent-SHA runs do not meet the rule. |
| RG-6 | FAIL (P2) | Public-content controls pass, but the immutable release record contains material verification-count and scope inaccuracies. |
| RG-7 | PASS WITH LIMITS | The release-note table discloses harness verification tiers; no live-fire publication was performed. |
| RG-8 | FAIL (P1) | This independent seat returns NO-GO on the exact subject; no prior lineage verdict transfers. |
| RG-9 | FAIL (P1) | The required committed SHA-bound owner authorization is absent, and adding it under the present sequence creates a new candidate that needs a new gate. |

## Rulings

### OAI-P1-01 — exact-candidate DCO failure

**UPHELD, P1, open.** The exact one-parent subject is authored by `SternOne` but
only signed off by `Claude`. The repository's own checker classifies it as
unsigned. Green DCO self-tests establish checker behavior; they do not sign the
subject commit.

### OAI-P1-02 — exact-SHA integrity evidence incomplete

**UPHELD, P1, open.** `RELEASING.md` requires every exact-commit integrity
workflow on the exact candidate after any correction. `openai-bundles` and
`mission-custody-contract` were not run on the subject. The cited runs are on its
parent. The v5.1 precedent actually re-dispatched path-filtered workflows at the
final SHA, so it does not authorize this substitution.

### OAI-P1-03 — publication authorization fixed point

**UPHELD, P1, open.** Procedure steps 4, 5, and 7 require exact-SHA workflow
evidence and gate judgment, followed by committed packet/acceptance/authorization
records naming that SHA. Committing the latter records creates a different SHA
and invalidates the former. The release note may not self-waive the governing
text. A prospective procedure correction and a fresh successor candidate are
required.

### OAI-P2-01 — immutable release record is inaccurate

**UPHELD, P2, open.** The subject's release note contains three reproducible
accuracy errors: landed work called pending, 7 seeds instead of 8, and 229 files
instead of 232. These do not establish secret exposure, but the release record is
not sufficiently exact for publication.

### OAI-Q-01 — historical packet is honest but nonterminal

**UPHELD WITH QUALIFICATIONS, resolved.** The BUILD-freeze packet's `NOT_READY`
state and surviving independent-gate claim are internally honest. They neither
create a new blocker beyond the current gate nor prove readiness for the subject.
The packet should not be regenerated merely to make this review look green; its
role in the publication sequence must first be defined without circularity.

## Minimum safe path to a new gate

1. Do not tag or publish the subject.
2. Correct the publication procedure prospectively so the terminal independent
   verdict and owner authorization can bind one immutable release subject without
   changing it afterward. Define the authoritative out-of-tree control record or
   a narrow, explicit transfer/freeze rule; do not infer one.
3. Create a successor commit with an author-matching DCO sign-off and correct the
   three release-note inaccuracies. The procedure correction, if committed, is
   part of that successor's reviewed content.
4. Freeze the successor and rerun the complete exact-commit suite, explicitly
   including DCO against the landed commit, `openai-bundles`,
   `mission-custody-contract`, `commission-watch-contract`, release security,
   parity/JSON checks, and every CodeQL language job.
5. Obtain a fresh operator-dispatched independent publication gate for that exact
   successor. Only after a conforming GO may D8 consultation, operator acceptance,
   owner authorization, ruleset disarm, tag creation, and Release publication
   proceed in the amended order.

## Machine-readable ruling set

```json
{
  "ruling_set": "ruling-set@1",
  "subject_sha": "d0165bd0cf1e79b94140d4493cc11bf7ba31a2a3",
  "run_id": "es-v6-publication-openai-2026-08-20",
  "seat": {
    "model_family": "OpenAI",
    "model": "GPT-5.6",
    "independence_mode": "operator-dispatched-cross-family-publication-seat",
    "implementer_authored_go_accepted": false
  },
  "rulings": [
    {
      "id": "OAI-P1-01",
      "lens": "pragmatic-judge",
      "priority": "P1",
      "basin": "exact-candidate-dco",
      "gate_items": ["RG-5"],
      "ruling": "UPHELD",
      "status": "open",
      "evidence": [
        "subject author identity is SternOne",
        "only sign-off identity is Claude",
        "check_dco.py unsigned_commits returned d0165bd0cf1e"
      ],
      "acceptance_criteria": [
        {
          "condition": "A new immutable candidate has an author-matching Signed-off-by trailer or an exact-SHA attestation authorized by the repository policy, and the repository checker accepts that landed commit.",
          "falsifier": {
            "method": "Run .github/scripts/check_dco.py logic against the exact landed candidate and inspect author/trailers.",
            "threshold": "candidate absent from unsigned_commits and evidence matches the exact 40-hex SHA",
            "timeframe": "before the next independent publication gate"
          },
          "owner": "release-author"
        }
      ]
    },
    {
      "id": "OAI-P1-02",
      "lens": "adjacent-possible-explorer",
      "priority": "P1",
      "basin": "exact-sha-workflow-evidence",
      "gate_items": ["RG-5"],
      "ruling": "UPHELD",
      "status": "open",
      "evidence": [
        "no openai-bundles run at d0165bd0cf1e79b94140d4493cc11bf7ba31a2a3",
        "no mission-custody-contract run at d0165bd0cf1e79b94140d4493cc11bf7ba31a2a3",
        "RELEASING.md step 4 invalidates parent evidence after a correction"
      ],
      "acceptance_criteria": [
        {
          "condition": "Every integrity workflow required by RELEASING.md is rerun against the exact successor candidate, with required jobs green and diagnostic exceptions explicitly recorded.",
          "falsifier": {
            "method": "Query GitHub runs by head_sha and compare workflow/job names and conclusions to RELEASING.md.",
            "threshold": "complete exact-SHA set; zero missing required workflows or failed required jobs",
            "timeframe": "after the last candidate-content correction and before the next independent gate"
          },
          "owner": "release-engineer"
        }
      ]
    },
    {
      "id": "OAI-P1-03",
      "lens": "decision-rights-auditor",
      "priority": "P1",
      "basin": "self-invalidating-publication-sequence",
      "gate_items": ["RG-2", "RG-8", "RG-9"],
      "ruling": "UPHELD",
      "status": "open",
      "evidence": [
        "RELEASING.md steps 4 and 5 bind checks and gate to the exact candidate",
        "RELEASING.md step 7 requires a committed authorization line naming that exact SHA before disarm",
        "the governing text defines no out-of-tree authority record or verdict-transfer rule"
      ],
      "acceptance_criteria": [
        {
          "condition": "A prospectively reviewed procedure defines a non-self-invalidating authority sequence, and one successor satisfies that sequence without treating an implementer-authored GO as independent evidence.",
          "falsifier": {
            "method": "Simulate the amended steps from frozen candidate through tag; recompute the SHA after every required write and verify all exact-SHA predicates still refer to the tagged commit.",
            "threshold": "one immutable 40-hex subject remains identical across required checks, independent verdict, authorization, and annotated tag target",
            "timeframe": "before D8 acceptance or tag-ruleset disarm"
          },
          "owner": "repository-owner"
        }
      ]
    },
    {
      "id": "OAI-P2-01",
      "lens": "pragmatic-judge",
      "priority": "P2",
      "basin": "release-record-accuracy",
      "gate_items": ["RG-1", "RG-6"],
      "ruling": "UPHELD",
      "status": "open",
      "evidence": [
        "release note says pending merge although the correction is on main",
        "release note says seven public-content seeds while the suite reports eight",
        "release note says 229 changed files while v5.1.0..subject contains 232"
      ],
      "acceptance_criteria": [
        {
          "condition": "The successor's release record accurately describes its landed state, current public-content seed count, and reproducible release-window file count.",
          "falsifier": {
            "method": "Compare note text to git ancestry, public-content test output, and git diff --name-only v5.1.0..<candidate>.",
            "threshold": "zero mismatches in the three cited fields",
            "timeframe": "on the successor submitted to the next independent gate"
          },
          "owner": "release-author"
        }
      ]
    },
    {
      "id": "OAI-Q-01",
      "lens": "decision-rights-auditor",
      "priority": "P2",
      "basin": "historical-packet-status",
      "gate_items": ["RG-2"],
      "ruling": "UPHELD-WITH-QUALIFICATIONS",
      "status": "resolved",
      "validation_kernel": "The packet honestly remains NOT_READY for its historical BUILD-freeze subject and correctly preserves the independent-gate blocking claim; validator success proves consistency, not publication readiness for d0165bd0.",
      "qualification": "Do not treat the historical packet as a separate current blocker or regenerate it merely for cosmetic readiness before the authority sequence is repaired."
    }
  ],
  "open_priorities": {
    "P1": 3,
    "P2": 1,
    "P3": 0,
    "P4": 0
  },
  "verdict_rule": "any open P1 implies NO-GO",
  "computed_verdict": "NO-GO",
  "forbidden_actions_performed": []
}
```
