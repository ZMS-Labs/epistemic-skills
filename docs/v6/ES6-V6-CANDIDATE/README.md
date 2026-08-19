# ES6-V6-CANDIDATE — BUILD freeze (issue #191), rc2

This packet is the v6 **BUILD** freeze against an exact candidate SHA. It is
not PROMOTION. It does not merge, tag, close tracker items, or record
Gauntlet GO. This is the **successor freeze** to the NO-GO'd predecessor
(subject `00e5146e…`, run `docs/gauntlet-runs/es-v6-candidate-freeze-2026-08-18/`
on the gauntlet-record branch): every acceptance criterion in that run's
ruling-set, plus operator decisions D1–D15
(`docs/v6/operator-decision-record-2026-08-18.md`, echo-certified), is
implemented in this lineage.

Parent: [epistemic-skills#191](https://github.com/ZMS-Labs/epistemic-skills/issues/191)

## The C/C+1 layering (R4/R5)

A packet cannot name the commit that contains it. This freeze therefore has
two commits:

- **C — the candidate**: the last code commit. Every artifact in this
  directory names C as `candidate_sha`/`exact_start_sha`, carries per-file
  sha256 digests of C's inventoried sources, and was generated AT C from a
  clean tree (the generator refuses `--sha != HEAD` and any dirt outside
  this directory).
- **C+1 — the freeze commit**: adds/updates ONLY this directory. The
  validator, running on C+1 or any descendant, recomputes every inventory
  digest — a post-freeze edit to an inventoried file turns CI red
  (`allowlist-stale`-style, see KL-RESTAMP).

**Subject SHA (this freeze, R4's letter):** candidate
**C = `16b80ac6ada24a663e39b38ab06e8f2614d247f4`** — cross-check it against
`promotion-packet.json → candidate_sha` and the artifact stamps; on any
disagreement the JSON artifacts govern and this README is stale. C+1 is
the commit whose diff introduced these artifacts (`git log -1
--format=%H -- docs/v6/ES6-V6-CANDIDATE/promotion-packet.json`).

## What this packet completes of the BUILD contract

- claim-to-proof matrix: 26 class claims (verdict-bound gauntlet row;
  per-commitment v5 rows; secret-scan, compatibility, guard-lexical,
  description-budget, and the three D1-ratified merge rows) + one census
  row per open tracker item, each with structured `consequence_severity`
- `blocking_claims` DERIVED from the matrix (`derive_blocking`, one home in
  the validator) — never a hand list
- issue/PR reconciliation with explicit human-read dispositions (an
  unlisted open item fails generation closed)
- source inventory with per-file digests + candidate tree hash
- requalification evidence: GitHub `workflow_dispatch` runs of all five
  gating workflows at C (`evidence/requalification.json` — the only
  mechanism that flips a claim PARTIAL→PROVED), plus local clean-room,
  workflow-oracle audit, public-content, and custody evidence at C
- an immutable promotion packet (schema @2) naming known limits with
  owners, a qualified rollback, and **zero** requested irreversible acts

## Honest gaps (do not read as GO)

- `CLM-INDEPENDENT-GAUNTLET` is UNPROVED by construction; a FRESH seat must
  run it (the prior adjudicating seat took the repair role under D2).
- Live-environment LIMITED: #77, #39, #136, #129, #142.
- Platform LIMITED: #162 (now with the MEASURED APFS Unicode-fold
  collision — see KL-MACOS-162) and CLM-WINDOWS-FS.
- Integrity: es#137 closed in THIS tree, open on `main` (KL-MAIN-137);
  `main` red at the Public-content step pending PR #195 (KL-MAIN-RED);
  draft CI skips all five gating workflows until ready-mark (KL-DRAFT-CI).
- The description-budget estate fork (Path 1 capture / Path 2 owner
  amendment) is the operator's open decision (CLM-DESCRIPTION-BUDGET).
- Pin tags: the session's git proxy refuses `refs/tags` pushes, so the
  freeze pins are an operator one-liner (see the freeze PR body); PINS
  registration follows at promotion (a post-freeze PINS edit would trip
  the digest guard by design).

## Regenerate (C/C+1 discipline)

```bash
# at C, clean tree; the generator refuses anything else
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
