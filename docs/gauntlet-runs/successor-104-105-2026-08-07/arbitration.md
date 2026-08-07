# Arbitration — successor #104/#105

## Inputs

Three evaluate reports; mechanical CI green on local gate subset; independence
degraded (same-family / manual-docket).

## Ruling set

| Finding | Disposition | Kernel |
|---|---|---|
| Watch P1 | **UPHELD historically; FIXED on branch** | Corrective SKILL + sentinel RED |
| Inventory generation gap | **UPHELD historically; FIXED on branch** | `sync_skill_surfaces.py --check` |
| Live harness absence | **UPHELD as P2 release condition C1** | Matrix + loaded-description tool |
| Estate net-negative unproven | **UPHELD as P2 release condition C2** | D8 amendment + matrix |
| Degraded independence | **UPHELD as P2 release condition C3** | This document's disclosure |
| Public-content current tree | **SATISFIED on branch** | `check_public_content.py` |
| Allowlist residual | **OVERRULED as release-blocking; retained P3** | Narrow prefixes; do not expand casually |
| Repo description stale | **UPHELD as P2 ops task** | Amend text prepared |

## Computed verdict

```json
{
  "merge_to_main": "GO",
  "conforming_successor_release": "CONDITIONAL",
  "open_p1": 0,
  "open_p2_for_release": ["C1", "C2", "C3", "repo-description"],
  "independence_mode": "degraded-same-family-manual-docket",
  "v5.0.0_retrospective": "NO-GO (unchanged)"
}
```

## Next actions

1. Merge the corrective PR once GitHub checks are green.
2. Apply `docs/release/RELEASE-BODY-AMEND-v5.0.0.md` to the mutable Release.
3. Update GitHub repository description to the prepared string.
4. Before tagging a conforming successor: discharge C1–C3 with live captures and
   an isolated Gauntlet on the exact tag candidate.

## Machine-readable ruling set

```json
{
  "ruling_set": "ruling-set@1",
  "subject": "successor-104-105-corrective-branch",
  "verdict": {
    "merge_to_main": "GO",
    "conforming_successor_release": "CONDITIONAL"
  },
  "rulings": [
    {
      "id": "R1-watch-p1-fixed",
      "lens": "disgruntled-maintainer F1",
      "priority": "P1",
      "ruling": "UPHELD",
      "status": "resolved-on-branch",
      "validation_kernel": "watch SKILL state machine includes explicit enable before PROVEN; sentinel watch-silence-read-as-healthy.json rejects inert-without-enable."
    },
    {
      "id": "R2-inventory-generated",
      "lens": "disgruntled-maintainer F2",
      "priority": "P2",
      "ruling": "UPHELD",
      "status": "resolved-on-branch",
      "validation_kernel": "sync_skill_surfaces.py --check regenerates schema enum, SKILL_NAMES, SKILL_EVENT_MAP, EXPECTED_SKILLS, ROUTING.md."
    },
    {
      "id": "R3-live-harness-c1",
      "lens": "disgruntled-maintainer F3",
      "priority": "P2",
      "ruling": "UPHELD",
      "status": "open",
      "validation_kernel": "HARNESS-VERIFICATION-MATRIX records LIVE_BLOCKED_EXTERNAL; conforming release requires capture receipts or owner-acknowledged tiers."
    },
    {
      "id": "R4-estate-budget-c2",
      "lens": "chaos-monkey F3",
      "priority": "P2",
      "ruling": "UPHELD",
      "status": "open",
      "validation_kernel": "D8 amendment separates package ceiling from estate cap; estate net-negative unproven without capture."
    },
    {
      "id": "R5-independence-c3",
      "lens": "disgruntled-maintainer F4",
      "priority": "P2",
      "ruling": "UPHELD",
      "status": "open",
      "validation_kernel": "This panel is same-family manual-docket; isolated multi-family Gauntlet required for conforming release GO."
    },
    {
      "id": "R6-allowlist-residual",
      "lens": "chaos-monkey F2",
      "priority": "P3",
      "ruling": "OVERRULED",
      "status": "accepted-residual",
      "validation_kernel": "Allowlist is limited to release-review receipt prefixes; broadening without review is forbidden. Residual P3 is monitoring, not release-blocking for the corrective merge."
    },
    {
      "id": "R7-repo-description",
      "lens": "release-integrity F4",
      "priority": "P2",
      "ruling": "UPHELD",
      "status": "open",
      "validation_kernel": "Prepared replacement string in RELEASE-BODY-AMEND-v5.0.0.md; GitHub API update returned 403 from this agent."
    }
  ]
}
```
