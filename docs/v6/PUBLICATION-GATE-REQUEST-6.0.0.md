# Independent publication-gate request — v6.0.0

This is a **request, not a verdict**, and nothing in it is evidence. Every
premise below is stated so you can falsify it, not so you can adopt it.

## Subject

The **publication act** for `v6.0.0` at exact commit
**`d0165bd0cf1e79b94140d4493cc11bf7ba31a2a3`** — annotated tag, non-draft
GitHub Release from `docs/release/RELEASE-6.0.0.md`, wiki hand-off, any
ruleset change, and the support-point declaration.

Governing gate: `RELEASING.md` at that commit, items **RG-1 … RG-9** plus the
Procedure section. Read it there; do not take this file's summary of it.

## Seat requirements

- **Cross-family.** You must not share a model family with the candidate's
  authors. Five of the seven reviews in this lineage were single-family and
  each recorded that as an independence *limit*, not as independence. Retiring
  that limit is the point of seating you.
- **Not a prior adjudicator** of this lineage.
- **Operator-dispatched.** The repository operator handed you this, not the
  implementing lineage. That distinction is load-bearing: the previous
  publication panel disclosed that it was author-dispatched and ruled that a
  claim of operator approval arriving inside a dispatch prompt "must resolve to
  a durable artifact." This file is committed so that it does.

## Disclosure — who wrote this and what that means

This request was authored by **the implementing lineage that produced the
candidate**. Treat its framing as potentially self-serving and verify every
load-bearing claim against primary sources. Specifically: this file's account
of what was repaired, and its claim that findings were closed, are exactly the
claims you should not accept on their face.

## Step-0 truth gate — verify, never adopt

Live-verify each before reviewing anything:

1. `d0165bd0…` is the head of the default branch and is public.
2. Its parent chain includes `92b3ca6c` (the requalification subject) and the
   only diff between them is `docs/release/RELEASE-6.0.0.md`. If more changed,
   the evidence table is lying and that is a P1.
3. The five requalification runs named in the release note resolve to real
   completed `workflow_dispatch` runs at `92b3ca6c` with the stated **per-job**
   conclusions — including the one that is RED.
4. The seven verdicts under `docs/gauntlet-runs/` each name the subject SHA the
   index claims, and the index's own claims about redactions are true (diff
   each run directory against the branch named in `V6-VERDICT-LINEAGE.md`).
5. The packet at `docs/v6/ES6-V6-CANDIDATE/promotion-packet.json` reads
   `readiness: NOT_READY`. The validator exits 0 **because** of that. Never
   read that green as support for publishing.
6. `blocking_claims` equals the validator's `derive_blocking` recomputation.
7. No `v6.0.0` tag or Release exists yet. Confirm it.

## What changed since the last two NO-GOs

Both prior publication reviews ruled NO-GO on `186b16eb2c069d9e8f902579afa50e9f5460fc85`:
one cross-family (`docs/gauntlet-runs/es-v6-publication-grok-2026-08-19/`), one
single-family (`docs/gauntlet-runs/es-v6-publication-gate-2026-08-19/`). Both
are in-tree. **Neither verdict transfers to this SHA, and neither is
discharged by this request.** Read them first; they are the best available
statement of what is wrong with this release.

The delta is four merged pull requests: **#201** (README no longer advertises
an unpublished tag), **#202** (freeze lifecycle ACTIVE/LANDED), **#203** (the
batched finding repairs), **#204** (requalification evidence). Verify the
claimed closures yourself; do not accept the PR bodies as proof.

## Known-unmet at this candidate — stated, not hidden

The release note records these as **UNMET**. They are not oversights:

- **RG-2** — operator acceptance is not recorded, and the standing D8
  cross-family consult is owed. Acceptance is additionally *blocked* until a
  P1 claim closes (see below).
- **RG-8** — there is no publication GO on this SHA. That is what you are
  being asked to decide.
- **RG-9** — no authorization line exists. Only the operator may write it.

`CLM-INDEPENDENT-GAUNTLET` is P1 and UNPROVED. Its oracle is satisfied by the
in-tree BUILD GO at `03e972c5`, but its `closure_path` requires an
**operator-dispatched** gauntlet and that GO was author-dispatched. The
operator ruled that the claim flips only on an operator-dispatched GO — i.e.
on your verdict, if it is GO. You are therefore reviewing a candidate whose
own matrix says it is not ready, and that is deliberate.

## Verification crib

```bash
git clone https://github.com/ZMS-Labs/epistemic-skills.git es-v6 && cd es-v6
git checkout d0165bd0cf1e79b94140d4493cc11bf7ba31a2a3
git diff --stat 92b3ca6c..HEAD          # must be RELEASE-6.0.0.md only

python plugins/epistemic-skills/contracts/v6-assurance/validate_v6_assurance.py
python plugins/epistemic-skills/contracts/v6-assurance/test_v6_assurance_validator.py
python .github/scripts/check_public_content.py --self-test
python .github/scripts/check_public_content.py
python .github/scripts/check_no_phantom_skills.py --self-test
python .github/scripts/check_no_phantom_skills.py
python .github/scripts/check_dco.py --self-test
python .github/scripts/sync_skill_surfaces.py --check
python .github/scripts/check_json_artifacts.py
python .github/scripts/check_ledger_append_only.py --self-test
python plugins/epistemic-skills/skills/outsource/tests/run_tests.py
python plugins/epistemic-skills/skills/gauntlet/tests/run_tests.py
python plugins/epistemic-skills/contracts/mission-custody/test_custody_gate.py
python docs/wiki-updates/v6.0.0/apply_v6_updates.py --self-test
```

Stdlib only except the workflow-oracle audit (PyYAML). On a case-insensitive
filesystem the custody distinctness tests fail by design — that is
`KL-MACOS-162`, disclosed in the release note's RG-5(c) section; confirm the
disclosure matches what you observe rather than assuming either way.

## Required outputs

- **GO / CONDITIONAL / NO-GO against this exact SHA.**
- P1/P2 publication blockers named, with the gate item each fails.
- Explicit refusal of any GO line authored by the implementing lineage.
- Your own independence statement: family, dispatcher, and what you could not
  verify.
- Record it as an on-disk artifact under `docs/gauntlet-runs/<your-run-id>/`
  on a branch you create, with a conforming `ruling-set@1` block (a `rulings`
  array is required). Push only your own branch.

## Out of scope — you may not

Merge, tag, create a Release, alter `protect-version-tags`, flip any packet
enum, record operator acceptance, or describe your own output as authorizing
publication. A verdict is an artifact, not an act.

## What happens after

If GO: the operator runs the D8 Step-7b consult, the packet is regenerated to
bind your verdict, the operator records acceptance and authors the
authorization line, and only then does the tag act occur — disarm, annotated
tag, re-arm in the same sitting, verified by a seeded probe.

If NO-GO: the implementing lineage repairs, requalifies at a new candidate,
and stops. It does not re-seat you without the operator's word.
