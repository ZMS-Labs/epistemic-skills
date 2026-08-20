# Live verification transcript — 2026-08-18 (seat: Kimi Code CLI, independent)

All commands run by the independent seat on 2026-08-18 ~21:20–22:35 UTC from a
fresh fetch of `origin`. Paths are repo-relative; local checkout paths are
elided per the public-content gate.

## Subject pins

```
C   = 6db8c50420b194aebbd09a2ea5f81c6a276897dc  tree 152b1df0f177303175eca422424361e086e6f0d8
C+1 = 9aecd467236dfb927e9c13784d77a16d62f28f67  tree 3a6c51aa23f9d755f66cc5dce5a64a0012645507
tip = 36b40a6 (branch claude/v6-candidate-rc2)  tree c84cfc2f2410d7dbe13d0cef5160ff41fdb12bd1
```

- `git cat-file -t` both SHAs → `commit` (exist).
- `git diff --name-only C C+1` → 13 files, ALL under `docs/v6/ES6-V6-CANDIDATE/`
  (grep for non-packet paths: NONE). C+1 diff confined to the packet dir: TRUE.
- `git diff --name-only C 36b40a6` → full output is 17 files: the 13
  packet-dir files (C+1's content) PLUS `.ledger/entries.jsonl`,
  `RELEASING.md`, `docs/superpowers/specs/2026-08-06-epistemic-skills-v5-design.md`,
  `docs/v6/ES6-V6-CANDIDATE/KIMI-SEAT-HANDOFF.md` (packet-dir files elided in
  an earlier draft of this line; challenger D-3). Intersection with the 158
  inventoried paths in `source-inventory.json@2`: **ZERO** (computed by
  script, not eyeball; independently recomputed by the dossier challenger).

## Pin tags (origin)

```
git ls-remote origin "refs/tags/pin/*"
pin/es-v6-rc2-candidate-2026-08-18^{}  -> 6db8c50420b194aebbd09a2ea5f81c6a276897dc  (peels to C)
pin/es-v6-rc2-freeze-2026-08-18^{}     -> 9aecd467236dfb927e9c13784d77a16d62f28f67  (peels to C+1)
```
`check_pin_tags.py` PINS registry at C+1 guards two entries
(`pin/ecs-contract-2026-07-27` and `v4.0.0` — footnote per challenger D-5);
the rc2 pins are NOT registered in PINS (README discloses deferral to
promotion: "a post-freeze PINS edit would trip the digest guard by design").

## Requalification runs (evidence/requalification.json names C; verified live)

`gh api repos/ZMS-Labs/epistemic-skills/actions/runs/<id>` per URL:

| run | workflow | event | head_sha | status/conclusion |
|---|---|---|---|---|
| 32190026236 | epistemic-flexibility | workflow_dispatch | 6db8c50420b194aebbd09a2ea5f81c6a276897dc | completed/success |
| 32190035556 | release-security | workflow_dispatch | 6db8c50420b194aebbd09a2ea5f81c6a276897dc | completed/success |
| 32190028540 | mission-custody-contract | workflow_dispatch | 6db8c50420b194aebbd09a2ea5f81c6a276897dc | completed/failure |
| 32190030973 | commission-watch-contract | workflow_dispatch | 6db8c50420b194aebbd09a2ea5f81c6a276897dc | completed/success |
| 32190033179 | openai-bundles | workflow_dispatch | 6db8c50420b194aebbd09a2ea5f81c6a276897dc | completed/success |

- Custody run 32190028540 job-level: `contract: success`, `contract-macos:
  failure` — matches the packet's disclosed es#162 instance (non-gating,
  dispatch-only diagnostic).
- Secret-scan run 32190035556 steps include `Prove the scanner detects a
  planted secret: success` and `Scan the complete repository history: success`
  (R2 positive control present and green at C).
- The handoff's "GitHub run 32189655677" (APFS capture) is cited inside
  KL-MACOS-162; not one of the five requal URLs. Not re-executed per handoff.

## origin/main live state (KL-MAIN-137 / KL-MAIN-RED)

- `git log --oneline -3 origin/main`: head `03b7724` = PR #195 merge
  ("fix(public-content): allowlist ES6-ZI-001 parent-tracker files and the
  gauntlet challenge record"). `gh pr view 195`: MERGED 2026-08-18T22:03:42Z,
  mergeCommit 03b7724d0b1d9fb02c7d92c4dd9e783c2b7ea635.
- Latest push runs on main at 03b7724: `epistemic-flexibility` SUCCESS,
  `release-security` SUCCESS (runs 32190904730 / 32190904577). Main is GREEN
  at head → KL-MAIN-RED's own retirement clause ("a green push to main retires
  this limit") has fired; R10's falsifier ("a subsequent green push to main
  retires the disclosure need") satisfied by live state.
- es#137: `gh issue view 137` → OPEN. The fix commits `dc33de2` / `e8a476c`
  are NOT ancestors of origin/main (`git merge-base --is-ancestor` → false).
  KL-MAIN-137 substance holds (exposure open on main, disclosed, owner
  operator, merge = PROMOTION).

## Operator decision record hash chain (D14 echo certification)

```
git show d7c4178f28014431a86c3a5bfdff3ad0633e6c9f:docs/v6/operator-decision-record-2026-08-18.md | sha256sum
= 5298827ea96d4d7b6ade1a863741ceced6bd4166456500f1fa129bc7a1a9a971
```
Matches the sha256 named in the certification section of the ODR at HEAD.
The ratified object at d7c4178 is intact in history.

## Workflow trigger repairs (R7 path A / R8) — read at C's tree

- `epistemic-flexibility.yml` pull_request: `types: [opened, synchronize,
  reopened, ready_for_review]`, NO paths filter (comment cites rulings R7/R8).
- `release-security.yml`, `commission-watch-contract.yml`,
  `mission-custody-contract.yml`, `openai-bundles.yml`: same
  `ready_for_review` type added (custody keeps its paths filter — its checks
  read only the custody tree). `dco.yml` already had the type.
- KL-DRAFT-CI text names all five skipped gating jobs + DCO, states the
  clean-room scope (52 of 53 python steps of ONE workflow), and references a
  "2026-08-18 ready-mark drill".
