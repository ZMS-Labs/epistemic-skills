# ES6-V6-CANDIDATE — BUILD freeze (issue #191), rc5

This packet is the v6 **BUILD** freeze against an exact candidate SHA. It is
not PROMOTION. It does not merge, tag, close tracker items, or record
Gauntlet GO. This is the **fifth candidate** of a lineage with four NO-GO
verdicts of record, each implemented here:

1. NO-GO against `00e5146e…` — the freeze panel
   (`docs/gauntlet-runs/es-v6-candidate-freeze-2026-08-18/` on
   `claude/epistemic-skills-v6-completion-nwptmc`; 18 rulings, 15
   acceptance criteria), plus operator decisions D1–D15
   (`docs/v6/operator-decision-record-2026-08-18.md`, echo-certified).
2. NO-GO against `6db8c50…` (rc2) — the cross-family kimi gauntlet
   (`docs/gauntlet-runs/es-v6-rc2-gauntlet-kimi-2026-08-18/` on
   `kimi/es-v6-rc2-gauntlet-2026-08-18`; rulings S1–S10, all closed).
3. NO-GO against `16b80ac…` (rc3) — the delta-review panel
   (`docs/gauntlet-runs/es-v6-rc3-delta-review-2026-08-18/` on
   `claude/es-v6-rc3-delta-review`); one P1 (R3-NF1, ledger bytes) plus
   R3-NF2..NF8, all closed at rc4.
4. NO-GO against `7408a46…` (rc4) — the fourth panel
   (`docs/gauntlet-runs/es-v6-rc4-delta-review-2026-08-19/` on
   `claude/es-v6-rc4-delta-review`); all eight rc3 findings CLOSED, one
   new P1 (R4-NF1, six unsigned commits in the freeze PR's range) plus
   eight P4 — the subject of this candidate's delta.

Parent: [epistemic-skills#191](https://github.com/ZMS-Labs/epistemic-skills/issues/191)

## Why rc5 exists at all (read this before the layering)

The rc4 freeze was sound in its own tree and was superseded anyway. Its
R4-NF1 repair had to land on `main` (the DCO checker runs from the PR's
BASE revision), and CI validates a pull request against its **merge
ref** — so three inventoried files diverged between `main` and the sealed
candidate, and the validator failed `R5 DIGEST MISMATCH` on a candidate
branch nobody had touched. Measured before acting: the merge ref was
built locally and the validator run against it.

That coupling is now a disclosed limit, **KL-SEAL-MAIN-COUPLING**, with a
rule attached: while a freeze is open, `main` must not change inventoried
files, or the freeze must be re-cut to absorb them. Land main-side policy
repairs BEFORE cutting a candidate, and keep the freeze→ready-mark window
short. rc5 absorbs `main` and closes the fourth panel's P4 sweep.

## The C/C+1 layering (R4/R5)

A packet cannot name the commit that contains it. This freeze therefore has
two commits:

- **C — the candidate**: the last code commit. Its tree carries NO packet
  directory at all — a superseded packet is deleted WHOLE with its repair
  (R3-NF7: core artifacts gone but prose remaining is TORN, not
  pre-freeze), immutable in history at its own freeze commit. Every
  artifact in this directory that carries a SHA names C, carries per-file
  sha256 digests of C's inventoried sources, and was generated AT C from a
  tree whose only dirt was this directory (the generator refuses
  `--sha != HEAD` and any dirt outside it).
- **C+1 — the freeze commit**: adds ONLY this directory. The validator,
  running on C+1 or any descendant, recomputes every inventory digest — a
  post-freeze edit to an inventoried file turns CI red (see KL-RESTAMP),
  and so does a main-side edit reaching the merge ref (KL-SEAL-MAIN-COUPLING).

**Subject SHA (this freeze, R4's letter):** candidate
**C = `03e972c5d427238033cb90d66846adabaf11928d`** — cross-check it against
`promotion-packet.json → candidate_sha` and the artifact stamps; on any
disagreement the JSON artifacts govern and this README is stale. C+1 is
the commit whose diff introduced these artifacts (`git log -1
--format=%H -- docs/v6/ES6-V6-CANDIDATE/promotion-packet.json`).

## What this packet completes of the BUILD contract

- claim-to-proof matrix: 26 class claims + one census row per open tracker
  item, each with structured `consequence_severity` and an owner drawn
  from a CLOSED, validated vocabulary (R4-NF4 — the check found a real
  unclassified owner on its first run)
- `blocking_claims` DERIVED from the matrix (`derive_blocking`, one home
  in the validator) — never a hand list; the S2 operator-channel law uses
  ONE owner predicate on both sides (R3-NF6)
- issue/PR reconciliation with explicit human-read dispositions (an
  unlisted open item fails generation closed)
- source inventory with per-file digests + candidate tree hash (S1:
  git-tracked paths only, fail-closed both directions)
- the durable ledger extends `origin/main`'s bytes as an EXACT PREFIX,
  with PRE-FREEZE oracle surfaces: the `workflow_dispatch` requalification
  runs the append-only check against live origin/main, and the clean-room
  replicates it (R3-NF1)
- the record-path secret-scan exemption is ANCHORED and proven narrow in
  CI on every run — the control asserts a look-alike path still fires
  (R4-NF2)
- requalification evidence: `workflow_dispatch` runs of all five gating
  workflows at C, with step-level proof that both added oracles executed;
  superseded rounds are itemized, not laundered (R4-NF9)
- an immutable promotion packet (schema @2) naming known limits with
  owners, a rollback stated as dated facts plus a live re-check
  obligation (R3-NF3), and **zero** requested irreversible acts

## Honest gaps (do not read as GO)

- `CLM-INDEPENDENT-GAUNTLET` is UNPROVED by construction; a FRESH seat
  must run it. The three-panel lineage cap was exhausted at rc3 and
  extended once (spent by the fourth panel); ruling D19
  (`v6-lineage-panel-cap-extension-two-20260819-23`) seats ONE further
  narrow panel, whose verdict spends that extension too.
- **KL-SEAL-MAIN-COUPLING** — the seal binds inventoried sources at C, and
  CI validates the freeze PR against its merge ref; a main-side change to
  any inventoried file breaks it. This candidate is only as fresh as
  `main` is quiet.
- Live-environment LIMITED: #77, #39, #136, #129, #142.
- Platform LIMITED: #162 (MEASURED APFS Unicode-fold collision — see
  KL-MACOS-162) and CLM-WINDOWS-FS.
- Integrity: es#137 is closed in THIS tree, still open on `main`
  (KL-MAIN-137; the custody fixes merge only at PROMOTION). Draft CI skips
  all five gating workflows until ready-mark (KL-DRAFT-CI).
- The description-budget estate fork is RESOLVED, not open (ledger entry
  `v6-description-budget-hybrid-path2-20260818-17`, hybrid Path 2).
- Pin tags — the one-freeze-lag discipline (S5/CL-3): `PINS` registers the
  newest pins that EXIST on origin at freeze time, which is not the same
  as the previous candidate's pins — a NO-GO'd candidate's pins are never
  pushed (R4-NF3). Currently the rc2 pair. This freeze's own pins are
  operator one-liners in the freeze PR body.
- Record-only from the fourth panel: R4-NF6 (a commit message overcounts
  rewritten ledger lines as 15 where the measured count is 13;
  conservative direction, immutable text) and R4-NF5 (ruling provenance —
  discharged by the operator's confirmation at acceptance, and by ledger
  entries 22/23 plus `operator-decision-record-2026-08-19.md`).

## Regenerate (C/C+1 discipline)

```bash
# at C the packet directory does not exist; recreate it as the ONLY dirt
git fetch origin main   # ledger append-only pre-freeze oracle (R3-NF1)
python .github/scripts/check_ledger_append_only.py --base-git-ref FETCH_HEAD --current .ledger/entries.jsonl
python .github/scripts/v6_audit_workflow_oracles.py --write docs/v6/ES6-V6-CANDIDATE/evidence/workflow-oracle-audit.json
python .github/scripts/v6_collect_candidate_evidence.py \
  --public-content docs/v6/ES6-V6-CANDIDATE/evidence/public-content.json \
  --custody docs/v6/ES6-V6-CANDIDATE/evidence/custody-suite.json
python .github/scripts/v6_run_clean_baseline.py --ref HEAD \
  --program ES6-V6-CANDIDATE --packet ES6-V6-CANDIDATE-REQUAL \
  --write docs/v6/ES6-V6-CANDIDATE/evidence/clean-baseline.json
# dispatch the five gating workflows at C; record run URLs + job
# conclusions in evidence/requalification.json (candidate_sha must be C)
python .github/scripts/v6_generate_candidate_packet.py \
  --tracker-json docs/v6/ES6-V6-CANDIDATE/evidence/tracker-capture.json
python plugins/epistemic-skills/contracts/v6-assurance/validate_v6_assurance.py
# BEFORE committing: build the PR merge ref (candidate + current main) and
# run the validator against it — KL-SEAL-MAIN-COUPLING, the check whose
# absence cost rc4.
# commit ONLY docs/v6/ES6-V6-CANDIDATE/** as C+1
```
