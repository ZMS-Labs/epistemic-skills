# Release 5.1.0 — manifest ships, corrections land, custody's verify verb stops lying

**Date:** 2026-08-15. **Minor.** Fifteen skills — the fourteen of
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

Per `RELEASING.md` §Release gate. Rows 4–7 are recorded against the release
content commit `7ba1f19` (PR #179 squash) together with this gate-evidence
commit — the commit that carries this table is the final tag candidate, and
item 8 must reach GO against it before the annotated tag is created.
Verification is at job and step level, not by run label.

| Item | Status | Evidence |
|---|---|---|
| 4 — version/link alignment | **met, after four live-surface stalenesses found and fixed by the release-diff review** | all ten version-bearing surfaces at 5.1.0; surface-sync `--check` green (15 skills / 14 disciplines). The review caught four prose-level stalenesses that no automated surface check covers, fixed in this commit: two Cursor install guards and the Kimi `/plugins install` URL still pinned to `v5.0.0`, and the README support-point paragraph still describing v5.0.0's gate history (fourteen skills, item 6 PARTIALLY MET, item 8 WAIVED) as 5.1.0's. |
| 5 — deterministic suite, DCO, parity, JSON, CodeQL | **met on `7ba1f19`** | six workflows green at `7ba1f19`, step-verified: `epistemic-flexibility` run 31894206384 (`stdlib-checks` green incl. skill inventory, surface synchronization, no-phantom, description budget, public-content gate steps); `release-security` run 31894206380; `openai-bundles` run 31894206377; `mission-custody-contract` run 31894206404 (its `contract-macos` job correctly skipped — inapplicable platform); `commission-watch-contract` run 31894206405; CodeQL run 31894206293 with all three `Analyze` matrices (`actions`, `javascript-typescript`, `python`) success. This gate-evidence commit's own push-CI is verified green before the tag; its run IDs are recorded in the annotated tag message. |
| 6 — secret scan **and** public-content/provenance review | **met, both halves, on `7ba1f19`** | scan: `release-security` run 31894206380, every step success — including the planted-secret positive control and the digest-allowlist narrowness control — before the full-history gitleaks pass. Public content: `check_public_content.py --self-test` + live run both exit 0 in the `stdlib-checks` Public-content gate step (run 31894206384), **plus** a manual release-diff review of all 19 changed files (+303/−48) against private paths, internal topology, credentials, personal data, and accidental telemetry — findings and dispositions recorded below. |
| 7 — harness surfaces exercised or assigned an honest tier | **met via explicit tiers; one live junction verification lands post-tag** | the README install table carries per-harness honest boundaries: Cursor's recorded behavioral epoch stays `BLOCKED_EXTERNAL`; ZCode's junction surface is verified on one fleet device (zms-pc-2025) with plugin install untested; the generic host carries the runtime-primitive caveat. Plugin surfaces inherit their 5.0.0 tiers — no new live plugin-harness executions in this release. |
| 8 — independent Gauntlet publication review reaching GO | **required — pending, pre-tag** | the panel runs against the frozen final candidate before tag creation; its record lands at an immutable path identifying this candidate's SHA. v5.0.0 shipped as a documented exception — this release does not repeat that. |

### Release-diff public-content review (item 6 record)

Scope: `git diff 1e36da9..7ba1f19` — 19 files, +303/−48 (version surfaces,
README, release notes, CI config, gitleaks config, custody CLI + mission
code, custody tests, two SKILL.md touch-ups), plus the current-tree
`check_public_content.py` pass cited above. Findings and dispositions:

- **No credentials, private paths, internal topology, or telemetry** in the
  diff. The one hostname-shaped token, `zms-pc-2025` in the item-7 row and
  tests, names a device with no address, role, or network detail, and
  device-name mentions of this class are already public in
  `docs/release/PUBLIC-RELEASE-REVIEW-ADDENDUM-2026-07-21.md`.
- `operator:SternOne` appears as an `--actor` string in the new custody
  tests. Disposition: accepted — `SternOne` is the operator's designated
  public callsign, deliberately not a personal name.
- `.gitleaks.toml` and the new "digest allowlist is narrow" CI step embed a
  synthetic SHA-256 fixture. Disposition: accepted — synthetic test data,
  admitted only by line-anchored allowlist regexes whose narrowness the new
  control step proves (a neighboring `credential` field is rejected).
- The release notes name the `media-library-rebuild` mission and the
  `custody-instrument` steward mission. Disposition: accepted — incident
  names only, no workspace paths, checkpoint contents, or fleet state.
- The review's four README staleness findings are recorded under item 4
  above and fixed in this commit; they are content-truth defects, not
  disclosure defects, and are listed here because the same review produced
  them.

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
