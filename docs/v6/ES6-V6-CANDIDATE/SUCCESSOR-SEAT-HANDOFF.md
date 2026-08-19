# Independent Gauntlet seat handoff — fresh seat, rc4 delta review

You are a **context-fresh independent Gauntlet seat** for the epistemic-skills
v6 rc4 BUILD freeze. You did not author the candidate, and you are not any
prior adjudicating seat of this lineage (the original adjudicator took the
repair role under D2; the kimi rc2 seat and the rc3 delta panel are prior
adjudicators). If you are a different model family from the candidate's
authors, state it in your run record; it strengthens seat independence but
does NOT by itself discharge the D8 Step-7b instruction ("At GO posture"
below).

## Subject lock — DERIVE it, never copy it (R3-NF2)

The rc3 edition of this brief hardcoded its predecessor's spent
coordinates and misdirected the very seat it was written for. This
edition binds by DERIVATION; the packet's JSON artifacts govern over any
prose, including this file:

- **Candidate C** = `promotion-packet.json → candidate_sha` in THIS
  directory. Every packet artifact must name exactly that SHA.
- **Freeze C+1** = the commit whose diff introduced this packet:
  `git log -1 --format=%H -- docs/v6/ES6-V6-CANDIDATE/promotion-packet.json`
  on `origin/claude/v6-candidate-rc2`. Verify C+1's parent is C and its
  diff touches ONLY `docs/v6/ES6-V6-CANDIDATE/`.
- **C's tree carries NO packet directory** (R3-NF7 discipline): run
  subject-tree oracles on a worktree of C; read packet artifacts at C+1.
- Convenience copy, verify before use (stale here = the JSON governs):
  at writing, C = `7408a462b413d0ab41a08de1d37a10b9cdf2a6ea`.

```bash
git fetch origin claude/v6-candidate-rc2
git checkout <C+1>                       # derived above
git worktree add ../es-v6-subject <C>    # derived above
```

- Later commits on the branch (if any) must leave every inventoried file
  byte-identical to C — the validator's digest recomputation proves it;
  run it yourself, trust nothing stamped.

## Review mode: DELTA + BLAST RADIUS (operator rulings of record)

This lineage's three-panel cap was EXHAUSTED at the rc3 verdict. The
operator's recorded ruling `v6-lineage-panel-cap-extension-20260819-21`
(`.ledger/entries.jsonl`) seats EXACTLY ONE more panel — this one —
scoped to the rc4 repair delta plus its blast radius, under the same mode
as ruling `v6-successor-review-delta-mode-20260818-19`:

- Rulings on unchanged content STAND as evidence. Do not re-litigate the
  kimi rulings S1–S10 (all CLOSED at the rc3 review on their own
  acceptance criteria); verify instead that the rc4 delta did not break
  their repairs where its blast radius reaches them.
- The rc4 delta closes the rc3 verdict's findings. Verify each against
  the arbitration's own letter
  (`docs/gauntlet-runs/es-v6-rc3-delta-review-2026-08-18/arbitration.md`
  on `origin/claude/es-v6-rc3-delta-review`):
  - **R3-NF1 (P1)**: `.ledger/entries.jsonl` at C must carry live
    `origin/main`'s bytes as an EXACT PREFIX (run
    `check_ledger_append_only.py --base-git-ref` yourself against a fresh
    fetch); the oracle must have pre-freeze surfaces — the dispatch runs
    at C execute the ledger step, and the clean-room replicates it.
  - **R3-NF2**: this brief derives its subject (you are reading the fix).
  - **R3-NF3**: no KL-MAIN-RED; rollback states dated facts + a live
    re-check obligation; the README self-identifies as rc4 and lists all
    three NO-GOs.
  - **R3-NF4**: CLM-DESCRIPTION-BUDGET is PROVED against ledger entry 17
    with the amendment + RELEASING.md row on disk.
  - **R3-NF5..NF8**: pins prose matches the lag discipline; one owner
    predicate both sides plus severity hard-gate; PRE-FREEZE/TORN and
    `_tracked_set` hardening with main()-path planted controls; clean-room
    override validation, NT temp-root override, `evidence_paths`
    completeness, capture-time PR title.
- Anything OUTSIDE the delta you touch only where the delta's blast
  radius reaches it, or where live state changed (main, tracker, tags).

Your verdict optimizes assurance and truthfulness — never speed, closure
counts, or a wish to be agreeable. NO-GO is a legitimate, useful outcome;
this lineage has three of them and improved through each.

## Authoritative documents (read in this order, from the checkout)

1. `docs/v6/ES6-V6-CANDIDATE/gauntlet-request.md` — THE request. Its
   Step-0 truth gate and required outputs govern; this handoff only adds
   environment tuning and never overrides it.
2. `docs/v6/ES6-V6-CANDIDATE/README.md` — the C/C+1 layering.
3. `plugins/epistemic-skills/skills/gauntlet/SKILL.md` — the
   Sovereign-Gauntlet protocol (subject lock, triage, panel, mechanical
   criticism, arbitration, finalize/verify).
4. `docs/v6/operator-decision-record-2026-08-18.md` — ratified D1–D15.
5. `docs/v6/OPERATOR-ACCEPTANCE-PROCEDURE.md` — what happens after you.
6. The three verdicts of record (fetch their branches; paths in the
   README's lineage list). The rc3 arbitration's acceptance letters are
   your primary criteria for the delta.

## Verification crib (run all, in the C worktree unless noted)

```bash
python plugins/epistemic-skills/contracts/v6-assurance/test_v6_assurance_validator.py
python plugins/epistemic-skills/contracts/v6-assurance/validate_v6_assurance.py   # PRE-FREEZE at C; full at C+1
git fetch origin main
python .github/scripts/check_ledger_append_only.py --self-test
python .github/scripts/check_ledger_append_only.py --base-git-ref FETCH_HEAD --current .ledger/entries.jsonl
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
python .github/scripts/test_v6_candidate_packet.py
python .github/scripts/test_v6_audit_workflow_oracles.py    # needs: pip install pyyaml
python .github/scripts/v6_audit_workflow_oracles.py
python plugins/epistemic-skills/contracts/mission-custody/test_custody_gate.py
python plugins/epistemic-skills/contracts/mission-custody/test_custody_hook.py
python plugins/epistemic-skills/contracts/mission-custody/test_custody_cli.py
```

Also verify LIVE (never from packet prose): the five requalification run
URLs in `evidence/requalification.json` resolve to real completed
`workflow_dispatch` runs at C with the stated per-JOB conclusions,
including the ledger append-only step EXECUTED (not skipped) in the
stdlib-checks run; `blocking_claims` equals `derive_blocking` recomputed
from the matrix; `origin/main`'s current head and CI state (dated facts
in the packet: #195 merged 2026-08-18 as `03b7724`; re-read today's
truth); which pin tags exist on origin.

## Environment notes

- The candidate's suites are stdlib-only except the workflow-oracle audit
  (PyYAML; its own error text names the remedy).
- On Windows hosts: use `python` (not `python3`); es#140 custody flakes —
  re-run the exact file once, a repeat failure is real; the R15
  guard-lexical pin and symlink probes print loud SKIPs where they do not
  apply (S7, measured); `cleanroom_ci.sh` is bash (Git Bash / MSYS2), and
  `CLEANROOM_TMPDIR` relocates its scratch outside the profile (S10) —
  it is validated early and `test_live_runner` honors it on NT (R3-NF8).
- Do NOT re-run macOS evidence: the APFS results (es#162 Unicode-fold
  collision) are in the requalification capture and its cited runs —
  verify by reading, not re-execution.

## Recording your run

- Create a NEW branch for your run record (e.g.
  `<seat>/es-v6-rc4-review-<date>`); commit under
  `docs/gauntlet-runs/<your-run-id>/` following the predecessor runs'
  artifact shape (`arbitration.md` with a computed verdict naming the C
  you derived, docket, reports, run-record, and a conforming
  `ruling-set@1` block — `validate_ruling_set.py` requires a `rulings`
  array). Push only your own branch.
- Sign off commits (`Signed-off-by:` line, DCO). Never write the private
  fleet repository name, user paths, or email addresses into committed
  files — `check_public_content.py` fails closed and its vocabulary is
  exactly what you must not add to.
- You may not: close issues or PRs, merge anything, tag, edit settings,
  push to any branch you did not create, or flip any field in the freeze
  packet. Your verdict binds via your on-disk arbitration artifact; the
  packet's `independent_gauntlet_ref` is updated only by the acceptance
  flow afterward.
- Your verdict SPENDS the cap extension: after it, any further panel on
  this lineage requires a fresh explicit recorded operator ruling.

## At GO posture

STOP before recording GO: surface operator decision **D8** (standing
Step-7b cross-family consult instruction) to the operator and let them
either run the consult or explicitly waive it in writing, noting your own
cross-family position. Then record the verdict artifact. Acceptance and
everything after it belongs to the operator per
`OPERATOR-ACCEPTANCE-PROCEDURE.md` — a GO from you authorizes nothing
beyond its own record.
