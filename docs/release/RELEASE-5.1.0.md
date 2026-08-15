# Release 5.1.0 — manifest ships, corrections land, custody's verify verb stops lying

**Date:** 2026-08-15 (candidate). **Minor.** Fifteen skills — the fourteen of
5.0.0 plus `manifest`, the mission-custody seat, published as a canonical
junction-reachable skill.

> **What this releases:** (1) the `manifest` skill reaches every host that
> consumes the packaged `skills/` tree, not just plugin-marketplace harnesses;
> (2) all of the never-published 5.0.1 correction work lands; (3) the custody
> CLI's `verify` becomes what its name promised — read-only — closing es#138,
> the defect that stranded a live mission.

## Why 5.1.0, and where 5.0.1 went

`release/5.0.1` was cut as a fourteen-skill correction patch but never
tagged. While it sat, `main` advanced thirty commits — including the entire
mission-custody contract family (#114) — past the branch point. Every
candidate whose commit could live in `main`'s history therefore carried the
fifteenth skill, making RELEASE-5.0.1's "fourteen skills, unchanged" claim
untrue for any mergeable tree, and `RELEASING.md` step 9 requires the release
commit to be contained in `main`. An honest v5.0.1 had become impossible.

**The 5.0.1 number is retired, unpublished.** No tag ever existed, so no tag
moved. Its corrections — install-metadata honesty, the hardened
phantom-skill guard, the 5.0.0 errata and record corrections, the UTF-8
description-budget measurement — are carried here in full; see
`RELEASE-5.0.0.md`, `RELEASE-5.0.0-ERRATA-2026-08-06.md`, and the design
conformance records of 2026-08-06 for the underlying history.

## What ships

### 1. `manifest` as a canonical skill (es#178)

The mission-custody seat already lived on `main` under
`plugins/epistemic-skills/skills/manifest/` (added by #114, after the 5.0.1
branch point). This release makes it loadable by every host that consumes the
canonical `skills/` tree — junction-projected harnesses included — instead of
plugin-marketplace harnesses only.

- **Operator decision (2026-08-15, es#178):** publish as canonical; junction
  hosts stay **tag-pinned** (they gain the seat at this tag); the generic-host
  caveat applies — the host must supply the custody CLI/hook runtime.
- **ADR-184's four-layer precedence** now holds on every install surface:
  wherever the epistemic seat ships, the agency seat ships with it.
- Description budget re-measured for fifteen: **8,636 bytes at ceiling**
  (`check_description_budget.py` green; was 8,159 across fourteen).
- README gains the manifest catalog row and the entry-point carve-out
  (manifest may also be invoked directly — `manifest this` / `/manifest`).

### 2. The 5.0.1 corrections, landed

Install metadata no longer advertises deleted skills (the 5.0.0
`using-epistemic-skills`/`helix` overclaim), the member lists are generated
from the packaged set, `check_no_phantom_skills.py` carries the 5.0.0
deletions in its RETIRED map and scans `marketplace.json` + root instruction
prose, and the 5.0.0 release-record corrections (items 6/7/8) stand as
recorded in the errata. All version-bearing surfaces read 5.1.0; skill-count
claims read fifteen everywhere the surface-sync contract checks.

### 3. Custody `verify` is now read-only (es#138)

`verify` was `begin_verification` wearing a read verb's name; a read-only
auditor moved the live `media-library-rebuild` mission `active → verifying`
through it, with no clean path back. Now:

- `verify` runs `Mission.verify_chain()` — walks every checkpoint, checks
  `prev_checkpoint_sha256` linkage, **mutates nothing** (`read_only: true`
  in the report; exit 0 intact / 4 walk-break; schema-broken chains still
  fail loudly at load, exit 2).
- The transition is `begin-verification`, matching the API.
- **No mutating alias** — old muscle memory gets a hard error, not a silent
  state change. That asymmetry is the fix.
- Oracles added: no-checkpoint-appended + status-unchanged on a healthy
  chain; tampered checkpoint → nonzero exit naming the file, zero writes.

## Release gate status for 5.1.0

| Item | Status | Evidence |
|---|---|---|
| 4 — version/link alignment | met | all ten version-bearing surfaces at 5.1.0; surface-sync `--check` green (15 skills / 14 disciplines); no stale tag URLs |
| 5 — deterministic suite, DCO, parity, JSON, CodeQL | pending exact-commit CI | local: all custody suites 0 failures; inventory/phantom/budget checks green |
| 6 — secret scan **and** public-content/provenance review | pending | scan via CI; the public-content half **will be performed on the release diff this time** and recorded here, not waived |
| 7 — harness surfaces exercised or assigned an honest tier | junction projection verified on one fleet device (zms-pc-2025) post-tag; plugin surfaces inherit 5.0.0 tiers | README install table carries the honest boundaries |
| 8 — independent Gauntlet publication review reaching GO | **required, scheduled** | v5.0.0 shipped as a documented exception; this release runs the gate |

## Known limitations, carried honestly

- **es#148: role separation is syntactic.** `--actor` strings are
  unauthenticated; the worker can self-accept. Documented known-limit; the
  authenticated-actor fix is future work.
- **es#173: one active mission per workspace stands.** Multi-mission
  (session-binding + union fallback) is operator-adjudicated for a future
  release under full gauntlet — not this one.
- **Behavioural superiority remains UNESTABLISHED** (unchanged since 5.0.0's
  four-arm campaign).
- Description budget: 8,636 bytes across fifteen skills — the rivalrous
  constraint grows with the package.

## Provenance notes

- The `custody-instrument` steward mission's records (untracked in a fleet
  checkout) are deliberately untouched; es#178's decision is recorded on the
  issue and here.
- Decision trail: es#178 (publish canonical; single 5.1.0 after the
  impossibility finding; tag-pinned junctions; #138 gates, #148 documented)
  and its same-session amendment, both 2026-08-15.
