# Independent Gauntlet seat handoff — fresh seat, rc5 narrow review

You are a **context-fresh independent Gauntlet seat** for the epistemic-skills
v6 rc5 BUILD freeze. You did not author the candidate, and you are not any
prior adjudicating seat of this lineage (the original adjudicator took the
repair role under D2; the kimi rc2 seat, the rc3 delta panel, and the rc4
panel are prior adjudicators). If you are a different model family from the
candidate's authors, state it in your run record; it strengthens seat
independence but does NOT by itself discharge the D8 Step-7b instruction
("At GO posture" below).

## Subject lock — DERIVE it, never copy it (R3-NF2)

An earlier edition of this brief hardcoded spent coordinates and misdirected
the seat it was written for. This edition binds by DERIVATION; the packet's
JSON artifacts govern over any prose, including this file:

- **Candidate C** = `promotion-packet.json → candidate_sha` in THIS
  directory. Every packet artifact that carries a candidate SHA names
  exactly that one. (Two evidence artifacts — `tracker-capture.json` and
  `workflow-oracle-audit.json` — carry no SHA stamp at all by design;
  R4-NF7 corrected an earlier over-broad phrasing of this rule.)
- **Freeze C+1** = the commit whose diff introduced this packet:
  `git log -1 --format=%H -- docs/v6/ES6-V6-CANDIDATE/promotion-packet.json`
  on `origin/claude/v6-candidate-rc2`. Verify C+1's parent is C and its
  diff touches ONLY `docs/v6/ES6-V6-CANDIDATE/`.
- **C's tree carries NO packet directory** (R3-NF7): run subject-tree
  oracles on a worktree of C; read packet artifacts at C+1.
- Convenience copy, verify before use (stale here = the JSON governs):
  at writing, C = `03e972c5d427238033cb90d66846adabaf11928d`.

```bash
git fetch origin claude/v6-candidate-rc2 main
git checkout <C+1>                       # derived above
git worktree add ../es-v6-subject <C>    # derived above
```

## Review mode: NARROW (operator ruling D19)

The lineage cap was exhausted at rc3, extended once (spent by the fourth
panel), and extended once more by ruling `D19`
(ledger `v6-lineage-panel-cap-extension-two-20260819-23`). Your verdict
spends that second extension. Scope, per the ruling:

1. **Is R4-NF1 discharged?** Six commits in freeze PR #197's range had no
   `Signed-off-by` line. The repair landed on `main` (PR #198, merged):
   merge commits are exempt, and five inherited Cursor Agent commits are
   attested by exact 40-hex SHA in a closed list. Verify by running the
   shipped `check_dco.py` logic over PR #197's live commit list yourself —
   it must return zero unsigned — and by reading `--self-test`'s seven
   planted controls, including that a commit sharing an attested PREFIX is
   still caught.
2. **Are the fourth panel's eight P4 findings correctly dispositioned?**
   R4-NF2 (anchored exemption + CI narrowness control), R4-NF3 (pin
   comment), R4-NF4 (closed owner vocabulary), R4-NF5 (ruling provenance),
   R4-NF6 (record-only), R4-NF7 (this brief's SHA rule), R4-NF8 (test
   harness root), R4-NF9 (superseded rounds itemized). Their letters are in
   `docs/gauntlet-runs/es-v6-rc4-delta-review-2026-08-19/arbitration.md`
   on `origin/claude/es-v6-rc4-delta-review`.
3. **The rc5 delta itself** — the ruling named "the same rc4 coordinates",
   and the subject moved because a main-side change to inventoried files
   broke the rc4 seal on the freeze PR's merge ref. Ledger entry 23 records
   that reading. The delta is: the `main` merge, the P4 sweep, and the
   regenerated packet. Everything the fourth panel closed on unchanged
   content STANDS — do not re-litigate it.
4. **KL-SEAL-MAIN-COUPLING is the load-bearing new disclosure.** Verify it
   yourself the way it was found: build the PR merge ref (candidate merged
   with current `origin/main`) and run
   `validate_v6_assurance.py` against that tree. It must exit 0. If `main`
   has moved onto an inventoried file since this freeze, it will not — and
   that is the limit doing its job, not a defect in the packet.

Your verdict optimizes assurance and truthfulness — never speed, closure
counts, or a wish to be agreeable. NO-GO is a legitimate, useful outcome;
this lineage has four of them and improved through each.

## Authoritative documents (read in this order, from the checkout)

1. `docs/v6/ES6-V6-CANDIDATE/gauntlet-request.md` — THE request. Its
   Step-0 truth gate and required outputs govern; this handoff only adds
   environment tuning and never overrides it.
2. `docs/v6/ES6-V6-CANDIDATE/README.md` — the C/C+1 layering and why rc5
   exists.
3. `plugins/epistemic-skills/skills/gauntlet/SKILL.md` — the protocol.
4. `docs/v6/operator-decision-record-2026-08-18.md` (D1–D15, echo-certified)
   and `docs/v6/operator-decision-record-2026-08-19.md` (D16–D19).
5. `docs/v6/OPERATOR-ACCEPTANCE-PROCEDURE.md` — what happens after you.
6. The four verdicts of record (branches named in the README's lineage).

## Verification crib (run all, in the C worktree unless noted)

```bash
python plugins/epistemic-skills/contracts/v6-assurance/test_v6_assurance_validator.py
python plugins/epistemic-skills/contracts/v6-assurance/validate_v6_assurance.py   # PRE-FREEZE at C; full at C+1
git fetch origin main
python .github/scripts/check_ledger_append_only.py --self-test
python .github/scripts/check_ledger_append_only.py --base-git-ref FETCH_HEAD --current .ledger/entries.jsonl
python .github/scripts/check_dco.py --self-test
python .github/scripts/check_public_content.py --self-test
python .github/scripts/check_public_content.py
python .github/scripts/sync_skill_surfaces.py --self-test
python .github/scripts/sync_skill_surfaces.py --check
python .github/scripts/check_no_phantom_skills.py --self-test
python .github/scripts/check_no_phantom_skills.py
python .github/scripts/score_sentinels.py --self-test
python .github/scripts/score_sentinels.py
python .github/scripts/check_skill_run_ledger.py --self-test
python .github/scripts/check_skill_run_ledger.py
python .github/scripts/check_pin_tags.py
python .github/scripts/test_v6_candidate_packet.py
python .github/scripts/test_v6_audit_workflow_oracles.py    # needs: pip install pyyaml
python .github/scripts/v6_audit_workflow_oracles.py
python plugins/epistemic-skills/contracts/mission-custody/test_custody_gate.py
python plugins/epistemic-skills/contracts/mission-custody/test_custody_hook.py
python plugins/epistemic-skills/contracts/mission-custody/test_custody_cli.py
```

Also verify LIVE (never from packet prose): the five requalification runs
resolve to real completed `workflow_dispatch` runs at C with the stated
per-JOB conclusions, including the ledger append-only step and the
record-path narrowness control EXECUTED, not skipped; `blocking_claims`
equals `derive_blocking` recomputed from the matrix; `origin/main`'s
current head and CI state; which pin tags exist on origin; and PR #197's
live commit list against the shipped DCO logic.

## Environment notes

- Suites are stdlib-only except the workflow-oracle audit (PyYAML).
- On Windows: use `python`; es#140 custody flakes — re-run the exact file
  once, a repeat failure is real; the R15 guard-lexical pin and symlink
  probes print loud SKIPs where they do not apply (S7, measured);
  `cleanroom_ci.sh` is bash (Git Bash / MSYS2), and `CLEANROOM_TMPDIR`
  relocates its scratch outside the profile (S10), validated early.
- Do NOT re-run macOS evidence: the es#162 APFS results are in the
  requalification capture and its cited runs — verify by reading.
- The record-path scan exemption is ANCHORED. If you scan a directory by
  absolute path, gitleaks reports absolute paths and no repo-anchored
  pattern matches — scan from the repository root with a relative target,
  the way CI does.

## Recording your run

- Create a NEW branch (e.g. `<seat>/es-v6-rc5-review-<date>`); commit under
  `docs/gauntlet-runs/<your-run-id>/` following the predecessor runs'
  shape (`arbitration.md` naming the C you derived, reports, run-record,
  and a conforming `ruling-set@1` block — `validate_ruling_set.py` requires
  a `rulings` array). Push only your own branch.
- Sign off commits (`Signed-off-by:`, DCO). Never write the private fleet
  repository name, user paths, or email addresses into committed files —
  `check_public_content.py` fails closed and its vocabulary is exactly what
  you must not add to. Note that record prose quoting a run id beside the
  word "API" trips the secret scanner's entropy heuristic; the exemption
  covers `^docs/gauntlet-runs/` only.
- You may not: close issues or PRs, merge anything, tag, edit settings,
  push to any branch you did not create, or flip any field in the freeze
  packet.

## At GO posture

STOP before recording GO: surface operator decision **D8** (standing
Step-7b cross-family consult instruction) to the operator and let them
either run the consult or explicitly waive it in writing, noting your own
cross-family position. Then record the verdict artifact. Acceptance and
everything after it belongs to the operator per
`OPERATOR-ACCEPTANCE-PROCEDURE.md` — a GO from you authorizes nothing
beyond its own record.
