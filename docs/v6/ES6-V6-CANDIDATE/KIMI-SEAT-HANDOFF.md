# Independent Gauntlet seat handoff — Kimi Code CLI, local Windows checkout

You are a **context-fresh independent Gauntlet seat** for the epistemic-skills
v6 rc2 BUILD freeze. You did not author the candidate, and you are not the
seat that adjudicated the predecessor (that seat took the repair role under
operator decision D2 and is disqualified). You are additionally a different
model family from the candidate's authors — state this in your run record;
it strengthens seat independence but does NOT by itself discharge the D8
Step-7b instruction (see "At GO posture" below).

Your verdict optimizes assurance and truthfulness — never speed, closure
counts, or a wish to be agreeable. NO-GO is a legitimate, useful outcome;
the predecessor freeze received one and the program improved because of it.

## Authoritative documents (read in this order, from the checkout)

1. `docs/v6/ES6-V6-CANDIDATE/gauntlet-request.md` — THE request. Its
   Step-0 truth gate and required outputs govern; this handoff only adds
   environment tuning and never overrides it.
2. `docs/v6/ES6-V6-CANDIDATE/README.md` — the C/C+1 layering.
3. `plugins/epistemic-skills/skills/gauntlet/SKILL.md` — the
   Sovereign-Gauntlet protocol you execute (subject lock, triage, panel,
   mechanical criticism, arbitration, finalize/verify).
4. `docs/v6/operator-decision-record-2026-08-18.md` — ratified D1–D15.
5. `docs/v6/OPERATOR-ACCEPTANCE-PROCEDURE.md` — what happens after you.
6. Predecessor verdict of record (fetch the branch):
   `docs/gauntlet-runs/es-v6-candidate-freeze-2026-08-18/` on
   `origin/claude/epistemic-skills-v6-completion-nwptmc` — the ruling-set
   whose 15 acceptance criteria this candidate claims to discharge.
   Verify each claim against that ruling-set's own falsifiers.

## Subject lock (do this before anything else)

```powershell
git fetch origin claude/v6-candidate-rc2 claude/epistemic-skills-v6-completion-nwptmc
git checkout 9aecd467236dfb927e9c13784d77a16d62f28f67   # C+1, the freeze packet commit
git worktree add ..\es-v6-subject 6db8c50420b194aebbd09a2ea5f81c6a276897dc   # C, the candidate
```

- **Candidate C** = `6db8c50420b194aebbd09a2ea5f81c6a276897dc` — every packet
  artifact must name exactly this SHA. Run subject-tree oracles in the
  `..\es-v6-subject` worktree (C's own tree; note its packet directory is
  the stale predecessor's by design — the fresh packet lives at C+1).
- **Freeze C+1** = `9aecd46…` — read packet artifacts here; verify C+1's
  diff against C touches ONLY `docs/v6/ES6-V6-CANDIDATE/`.
- Later commits on the branch (a history-only merge of main after PR #195)
  must leave every inventoried file byte-identical to C — the validator's
  digest recomputation proves it; run it yourself, trust nothing stamped.

## Windows / Kimi CLI environment notes

- Use `python` (not `python3`) in every command below.
- **es#140 (known, disclosed):** the mission-custody suite has intermittent
  Windows-only flakes (subprocess/tempdir timing). A custody test failure
  on your machine is a FINDING CANDIDATE, not a finding: re-run the exact
  file once; a repeat failure is real, a one-off matching the es#140
  signature is recorded as environment noise with the issue cited.
- **Expected loud skips (not defects):** symlink-dependent tests — the R15
  guard-lexical characterization pin and custody symlink probes — skip
  loudly on NT without symlink privilege (`KL-WINDOWS` discloses that no
  native-Windows requalification is claimed). A SKIP printed with its
  reason is correct behavior; a silent pass of a symlink test on
  unprivileged NT would itself be suspicious.
- `cleanroom_ci.sh` is bash: run it from Git Bash / MSYS2
  (`bash .github/scripts/cleanroom_ci.sh 6db8c50420b194aebbd09a2ea5f81c6a276897dc`).
  The repo's clean-room header documents this exact host class.
- Do NOT re-run macOS evidence: the APFS results (including the disclosed
  Unicode-fold collision, es#162) are in the requalification capture and
  in GitHub run 32189655677 / 32190028540 — verify by reading, not
  re-execution.
- PowerShell quoting mangles inline text; prefer running the repo's own
  scripts over ad-hoc one-liners, and `--*-file` variants where offered.

## Verification crib (run all, in the C worktree unless noted)

```powershell
python plugins\epistemic-skills\contracts\v6-assurance\test_v6_assurance_validator.py
python plugins\epistemic-skills\contracts\v6-assurance\validate_v6_assurance.py   # run at C+1 checkout too
python .github\scripts\check_public_content.py --self-test
python .github\scripts\check_public_content.py
python .github\scripts\sync_skill_surfaces.py --self-test
python .github\scripts\sync_skill_surfaces.py --check
python .github\scripts\check_no_phantom_skills.py --self-test
python .github\scripts\check_no_phantom_skills.py
python .github\scripts\score_sentinels.py --self-test
python .github\scripts\score_sentinels.py
python .github\scripts\check_skill_run_ledger.py --self-test
python .github\scripts\check_skill_run_ledger.py
python .github\scripts\test_v6_candidate_packet.py
python .github\scripts\test_v6_audit_workflow_oracles.py    # needs: pip install pyyaml
python .github\scripts\v6_audit_workflow_oracles.py
python plugins\epistemic-skills\contracts\mission-custody\test_custody_gate.py
python plugins\epistemic-skills\contracts\mission-custody\test_custody_hook.py
python plugins\epistemic-skills\contracts\mission-custody\test_custody_cli.py
```

Also verify LIVE (never from packet prose): the five requalification run
URLs in `evidence/requalification.json` resolve to real completed
`workflow_dispatch` runs at C with the stated per-JOB conclusions; the
`blocking_claims` list equals `derive_blocking` recomputed from the matrix;
`origin/main`'s current state for KL-MAIN-137 / KL-MAIN-RED (PR #195 merged
2026-08-18 as `03b7724`; both limits decay — read today's truth).

## Recording your run

- Create a NEW branch for your run record (e.g.
  `kimi/es-v6-rc2-gauntlet-<date>`); commit under
  `docs/gauntlet-runs/<your-run-id>/` following the predecessor run's
  artifact shape (`arbitration.md` with a computed verdict naming subject
  SHA `6db8c50…`, docket, reports, run-record). Push only your own branch.
- Sign off commits (`Signed-off-by:` line, DCO). Never write the private
  fleet repository name or any user path into committed files —
  `check_public_content.py` fails closed and its vocabulary is exactly
  what you must not add to.
- You may not: close issues or PRs, merge anything, tag, edit settings,
  push to any branch you did not create, or flip any field in the freeze
  packet. Your verdict binds via your on-disk arbitration artifact; the
  packet's `independent_gauntlet_ref` is updated only by the acceptance
  flow afterward.

## At GO posture

STOP before recording GO: surface operator decision **D8** (standing
Step-7b cross-family consult instruction) to the operator and let them
either run the consult or explicitly waive it in writing, noting your own
cross-family position. Then record the verdict artifact. Acceptance and
everything after it belongs to the operator per
`OPERATOR-ACCEPTANCE-PROCEDURE.md` — a GO from you authorizes nothing
beyond its own record.
