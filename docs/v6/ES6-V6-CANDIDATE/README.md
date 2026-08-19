# ES6-V6-CANDIDATE — BUILD freeze (issue #191), rc4

This packet is the v6 **BUILD** freeze against an exact candidate SHA. It is
not PROMOTION. It does not merge, tag, close tracker items, or record
Gauntlet GO. This is the **fourth candidate** of a lineage with three
NO-GO verdicts of record, each implemented here:

1. NO-GO against `00e5146e…` — the freeze panel
   (`docs/gauntlet-runs/es-v6-candidate-freeze-2026-08-18/` on
   `claude/epistemic-skills-v6-completion-nwptmc`; 18 rulings, 15
   acceptance criteria), plus operator decisions D1–D15
   (`docs/v6/operator-decision-record-2026-08-18.md`, echo-certified).
2. NO-GO against `6db8c50…` (rc2) — the cross-family kimi gauntlet
   (`docs/gauntlet-runs/es-v6-rc2-gauntlet-kimi-2026-08-18/` on
   `kimi/es-v6-rc2-gauntlet-2026-08-18`; rulings S1–S10).
3. NO-GO against `16b80ac…` (rc3) — the delta-review panel
   (`docs/gauntlet-runs/es-v6-rc3-delta-review-2026-08-18/` on
   `claude/es-v6-rc3-delta-review`; all ten S-rulings CLOSED, one new P1
   R3-NF1 — the candidate commit byte-rewrote published ledger lines —
   plus findings R3-NF2..NF8, all repaired in this candidate).

Parent: [epistemic-skills#191](https://github.com/ZMS-Labs/epistemic-skills/issues/191)

## The C/C+1 layering (R4/R5)

A packet cannot name the commit that contains it. This freeze therefore has
two commits:

- **C — the candidate**: the last code commit. Its tree carries NO packet
  directory at all — the superseded rc3 packet is deleted WHOLE with the
  repair (R3-NF7: core artifacts gone but prose remaining is TORN, not
  pre-freeze), immutable in history at its own freeze commit `7ce03b9…`.
  Every artifact in this directory names C as
  `candidate_sha`/`exact_start_sha`, carries per-file sha256 digests of
  C's inventoried sources, and was generated AT C from a tree whose only
  dirt was this directory (the generator refuses `--sha != HEAD` and any
  dirt outside it).
- **C+1 — the freeze commit**: adds ONLY this directory. The validator,
  running on C+1 or any descendant, recomputes every inventory digest — a
  post-freeze edit to an inventoried file turns CI red
  (`allowlist-stale`-style, see KL-RESTAMP).

**Subject SHA (this freeze, R4's letter):** candidate
**C = `7408a462b413d0ab41a08de1d37a10b9cdf2a6ea`** — cross-check it against
`promotion-packet.json → candidate_sha` and the artifact stamps; on any
disagreement the JSON artifacts govern and this README is stale. C+1 is
the commit whose diff introduced these artifacts (`git log -1
--format=%H -- docs/v6/ES6-V6-CANDIDATE/promotion-packet.json`).

## What this packet completes of the BUILD contract

- claim-to-proof matrix: 26 class claims (verdict-bound gauntlet row;
  per-commitment v5 rows; secret-scan, compatibility, guard-lexical,
  description-budget, and the three D1-ratified merge rows) + one census
  row per open tracker item, each with structured `consequence_severity`
- `blocking_claims` DERIVED from the matrix (`derive_blocking`, one home
  in the validator) — never a hand list; the S2 operator-channel law is
  enforced with ONE owner predicate (`is_operator_class`) on both sides
  (R3-NF6)
- issue/PR reconciliation with explicit human-read dispositions (an
  unlisted open item fails generation closed)
- source inventory with per-file digests + candidate tree hash (S1:
  git-tracked paths only, fail-closed both directions)
- the durable ledger extends `origin/main`'s bytes as an EXACT PREFIX,
  and the append-only oracle now has PRE-FREEZE surfaces: the
  `workflow_dispatch` requalification runs it against live origin/main,
  and the clean-room replicates the same comparison (R3-NF1)
- requalification evidence: GitHub `workflow_dispatch` runs of all five
  gating workflows at C (`evidence/requalification.json` — the only
  mechanism that flips a claim PARTIAL→PROVED), plus local clean-room,
  workflow-oracle audit, public-content, and custody evidence at C
- an immutable promotion packet (schema @2) naming known limits with
  owners, a rollback stated as dated facts plus a live re-check
  obligation (R3-NF3), and **zero** requested irreversible acts

## Honest gaps (do not read as GO)

- `CLM-INDEPENDENT-GAUNTLET` is UNPROVED by construction; a FRESH seat
  must run it. The three-panel lineage cap was EXHAUSTED at the rc3
  verdict; the operator's recorded ruling
  (`v6-lineage-panel-cap-extension-20260819-21`, `.ledger/entries.jsonl`)
  extends it by EXACTLY ONE delta-plus-blast-radius panel for this
  repair. That panel's verdict spends the extension.
- Live-environment LIMITED: #77, #39, #136, #129, #142.
- Platform LIMITED: #162 (MEASURED APFS Unicode-fold collision — see
  KL-MACOS-162) and CLM-WINDOWS-FS.
- Integrity: es#137 is closed in THIS tree, still open on `main`
  (KL-MAIN-137; the custody fixes merge only at PROMOTION). `main` itself
  is no longer asserted red — PR #195 merged 2026-08-18 as `03b7724` and
  its push runs were green; live main state is re-checked at operator
  acceptance, never assumed from this packet (R3-NF3). Draft CI skips
  all five gating workflows until ready-mark (KL-DRAFT-CI).
- The description-budget estate fork is RESOLVED, not open: recorded
  operator ruling `v6-description-budget-hybrid-path2-20260818-17`
  (hybrid Path 2 — package ceiling stays a hard gate; release notes
  report the byte delta; `--require-capture` stays available). The rc3
  packet's contrary claim was R3-NF4.
- Pin tags — the one-freeze-lag discipline (S5/CL-3, R3-NF5): `PINS` in
  `check_pin_tags.py` registers the newest pins that EXIST on origin at
  freeze time (currently the rc2 pair, the only pins the operator has
  pushed). This freeze's own pins (`pin/es-v6-rc4-*`) are operator
  one-liners in the freeze PR body; the NEXT freeze registers whatever
  pins then exist. A post-freeze PINS edit would trip the digest guard —
  that is the tripwire working, not a prohibition on registration.

## Regenerate (C/C+1 discipline)

```bash
# at C the packet directory does not exist; recreate it as the ONLY dirt
# (the generator refuses --sha != HEAD and any dirt outside it)
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
# commit ONLY docs/v6/ES6-V6-CANDIDATE/** as C+1
```
