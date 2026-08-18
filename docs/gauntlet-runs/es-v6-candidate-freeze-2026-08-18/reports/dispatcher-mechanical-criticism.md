# Dispatcher mechanical criticism — Step 6 (pre-arbitration)

Inputs: the five structured lens reports (barrier-isolated; rendered to
`reports/*.md`, canonical JSON in the workflow journal), the frozen
dossier, and the run evidence. This memo records the mechanical
evidence truth-check, the dispatcher's independent re-verifications of
load-bearing lens claims, corrections, and the tensions the arbitrator
must rule. It contains no verdict.

## Evidence truth-check (verify_evidence.py)

Sovereign Fingerprint (`reports/fingerprint.json`): **222 V-tags total,
222 verified, 0 hallucinated — 100.0% for every lens**; 64 `[I]`
inference tags (anchors named inline, spot-checks below); **0 `[H]`
tags**. Composite evidence root: pristine packet-head worktree (git tree
`26d0e9c5…`) + this run's pinned `evidence/`.

## Structural checks (workflow Verify phase, mechanical)

40 findings entered; **0 struck** for malformed falsifiers (all carry
statement+method+threshold+timeframe); **0 struck** for missing
validation kernels on P1/P2; **0 flagged** H-only/zero-weight. Schema
enforcement did this work at the tool layer.

## Dispatcher re-verifications of load-bearing lens claims

Each item: the lens claim → the dispatcher's independent command → result.

1. **ready_for_review takeover cannot dispatch the gating suites**
   (human-automation-handoff-auditor P1). Grep of all six workflows:
   only `dco.yml` declares
   `types: [opened, synchronize, reopened, ready_for_review]` (with the
   in-tree rationale comment); `epistemic-flexibility.yml`,
   `mission-custody-contract.yml`, `release-security.yml`, and
   `commission-watch-contract.yml` declare bare `pull_request:` (default
   activity types exclude `ready_for_review`). **CONFIRMED.**
2. **Terminal readiness gate accepts a self-written GO literal**
   (human-automation-handoff-auditor P1; entropy-demon P1 limb;
   requirements-traceability-auditor P2). Independent reproduction: in a
   scratch copy of the packet-head tree, set
   `readiness=V6_CANDIDATE_READY_FOR_OPERATOR_ACCEPTANCE` and
   `independent_gauntlet="GO"` with all nine `blocking_claims` intact →
   `validate_v6_assurance.py` printed "schema checks passed" and exited
   0. **CONFIRMED.**
3. **origin/main's head is red on its own required gate**
   (chesterton-gate P1). Fresh worktree at `a2b9c0d` →
   `check_public_content.py` exits 1 with exactly two
   `private-fleet-repo-name` defects
   (`.github/scripts/v6_generate_baseline_claims.py`,
   `docs/v6/ES6-ZI-001/exact-start-receipt.json`) — the two files the
   CANDIDATE's allowlist edit exempts. **CONFIRMED** (matches the lens's
   live job-record read: run 32107889882, stdlib-checks failure at the
   Public-content step, 11 downstream steps skipped).
4. **The es#137 P1 fix deleted the safe-direction fence test**
   (chesterton-gate P2). `git log -S test_glob_overmatch_still_held`:
   added by `c561213` (PR #128), removed by `dc33de2` (the P1 fix);
   present at `a2b9c0d` (1 hit), absent at `00e5146`. **CONFIRMED.**
5. **blocking_claims is a hardcoded nine-id whitelist filtered by
   `!PROVED`** (human-automation-handoff-auditor P2).
   `v6_generate_candidate_packet.py` `blocking_from_matrix` source
   read: fixed `required` list of 9 ids; operator-owned BLOCKED claims
   (CLM-ISSUE-104/84/40/186) structurally cannot enter. **CONFIRMED.**
6. **Secret-scan surface has no matrix claim and no run on the chain**
   (four lenses, one basin). Already dossier-verified pre-panel: no
   class claim covers release-security; `full-history-secret-scan`
   skipped on both PR heads; no runs at `00e5146`. **CONFIRMED.**
7. **`check_public_content.py` reads the whole tracked tree while its
   only executing workflow is path-filtered**
   (cloud-native-purist P1 anchors). `tracked_files()` runs
   `git ls-files` over the repo root; `epistemic-flexibility.yml`
   `pull_request.paths` is a finite list. Anchor-level **CONFIRMED**
   (the lens's 1467/1395/72 enumeration and PR-dispatch probe are its
   own recorded [I] work).
8. **Public-content gate transfer-invalidity and self-falsifying
   recorded evidence** — pre-panel dossier facts (allowlist 39/39/41/41
   across `a2b9c0d`/`e8a476c`/`00e5146`/`7de88fa`; recorded stdout "41"
   under an `e8a476c` stamp). **CONFIRMED** (dossier, challenger, and
   chesterton-gate's independent probe all agree).

## Corrections the arbitrator must apply

- **requirements-traceability-auditor:build-window-merges (P1) is
  partially overstated.** Its "no claim" limb is wrong for two of the
  three merges: PR #190 appears in CLM-RELEASE-AUTH/CLM-REQUIRED-JOB
  (linked_prs, authority) and CLM-MC-MACOS-CASE (independence note);
  PR #156 appears in CLM-RELEASE-AUTH's authority. The limbs that
  stand, dispatcher-verified: no reconciliation ROW or disposition
  exists for any of the three window merges, and **PR #192 — the
  candidate's own base commit — appears nowhere in any packet
  artifact**. Weigh the finding on the standing limbs.

## Tension the arbitrator must rule explicitly

- **CLM-WF-PATH-COVERAGE truth**: cloud-native-purist P1
  (`proved-path-filter-claim-false` — statement false because the
  public-content step's input set is the whole tracked tree, 72 files
  outside the filter; probe satisfied the claim's own falsifier) versus
  chesterton-gate P3 (`proved-claim-labels-a-risk-its-oracle-cannot-see`
  — "its narrow statement is true"). Direct factual conflict on whether
  a PROVED row is false. The dispatcher verified cnp's anchors (whole
  tree read; finite path filter); the divergence is over the
  construction of "files its steps read or execute". Rule it; preserve
  the dissent.

## Correlated basins (merge as ONE claim each; weigh chains, not votes)

- Secret-scan unclaimed+unrun: entropy-demon P1, cloud-native-purist
  P1, requirements-traceability-auditor P1, chesterton-gate P1.
- Clean-room under-coverage / "BUILD oracle" overstatement:
  human-automation-handoff-auditor P2, entropy-demon P2,
  cloud-native-purist P2, requirements-traceability-auditor P2
  (kl-draft-ci), chesterton-gate P1-reasoning limb (fail-fast
  blindness).
- Packet non-reproducibility / regeneration: human-automation-
  handoff-auditor P2, cloud-native-purist P2, entropy-demon P1 limb.
- Tracker reconciliation boilerplate:
  requirements-traceability-auditor P1, chesterton-gate P2,
  entropy-demon P2, cloud-native-purist P3.
- Restamp/immutability (README disclaimer deletion, --sha literal, no
  integrity anchor): entropy-demon P1, chesterton-gate P2,
  requirements-traceability-auditor P2, human-automation-handoff-
  auditor P2.
- ready_for_review / draft-CI handoff: human-automation-handoff-auditor
  P1 (unique chain; corroborated at anchor level by the dispatcher).
- Operator-channel omissions (blocking_claims whitelist, known_limits
  gaps): human-automation-handoff-auditor P2 + P1-limb of the terminal
  gate; entropy-demon P1 limb.

## Oracle-adequacy review of lens claims

No lens claim of the form "verified/tested/passes" rests on an
inadequate oracle requiring downgrade: every probe names its method and
observable inline; live GitHub reads record tool+parameters+observed
values; all four "PROVED-claim-false" attacks satisfied (or failed to
satisfy) the claims' OWN falsifiers, which is the correct oracle for a
matrix row. The lens verdict tally (4 NO-GO, 1 CONDITIONAL) is
dissent-bearing input, NOT a vote — chesterton-gate's CONDITIONAL and
its reasoning must be preserved in the Conflict Ledger.
