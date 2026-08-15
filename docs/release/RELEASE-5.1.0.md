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

Per `RELEASING.md` §Release gate. Candidate chain: release content
`7ba1f19` (PR #179 squash) → gate-evidence commit `8180554` (PR #180 squash,
against which the Gauntlet panel 1 ran and returned **NO-GO as-specified,
GO binding on a named discharge set**) → this discharge commit, which
executes that set. The final tag candidate is the commit carrying this
table together with the committed Gauntlet record at
`docs/gauntlet-runs/es-v510-publication-2026-08-15/`. Verification is at
job and step level, not by run label.

| Item | Status | Evidence |
|---|---|---|
| 4 — version/link alignment | **met, after four in-tree stalenesses and two live out-of-tree stalenesses were found and fixed** | all ten version-bearing surfaces at 5.1.0; surface-sync `--check` green (15 skills / 14 disciplines). In-tree (found by the release-diff review, fixed in `8180554`): two Cursor install guards and the Kimi `/plugins install` URL still pinned to `v5.0.0`, and the README support-point paragraph still describing v5.0.0's gate history as 5.1.0's. Out-of-tree (found by Gauntlet panel 1, fixed before this commit, re-probed live 2026-08-15): the GitHub repo description still advertised the router seat deleted in v5.0.0 (executing the unchecked order in `RELEASE-BODY-AMEND-v5.0.0.md`), and the README-linked public wiki Installation page installed v5.0.0/fourteen with `tree/v5.0.0` URLs — now v5.1.0/fifteen (`epistemic-skills.wiki` e6c6ba7..710dd2b); the full v5.1.0 handbook pass is a recorded post-tag follow-up. |
| 5 — deterministic suite, DCO, parity, JSON, CodeQL | **met** | six workflows green at `7ba1f19`, step-verified: `epistemic-flexibility` run 31894206384; `release-security` run 31894206380; `openai-bundles` run 31894206377; `mission-custody-contract` run 31894206404 (`contract-macos` correctly skipped — dispatch-only probe job); `commission-watch-contract` run 31894206405; CodeQL run 31894206293, all three `Analyze` matrices success. Four workflows green at `8180554` (31895143032/030/022/005) and at the discharge commit `2890ae6`. The two path-filtered suites were **dispatched via `workflow_dispatch` at `2890ae6`** per panel-1 ruling: `openai-bundles` run 31897020113 **success**; `mission-custody-contract` run 31897018984 — the required `contract` job **success**, while the dispatch-only `contract-macos` probe job (built to settle es#162) failed 2 case-distinctness lifecycle tests at `2890ae6` and again at the final candidate: **es#162 is settled negative** — macOS-default (case-insensitive) filesystems do not support the custody CLI's case-distinct multi-file tracking; a prior dispatch at `8aa4ffe` on 2026-08-13 (run 31723939498) had already failed the same step, so the settlement predates this release cycle and the dispatch runs triple-confirm it (31723939498, 31897018984, 31898055755); disclosed as a known limitation below and adjudicated by the panel-2 re-affirmation (the "red blocks the tag" clause is ruled there against the probe-job attack). Both suites are re-dispatched at the final tag SHA; their run IDs and conclusions are recorded in the annotated tag message. |
| 6 — secret scan **and** public-content/provenance review | **met, both halves, at both scopes** | scan: `release-security` runs 31894206380 and 31895143030, every step success — including the planted-secret positive control and the digest-allowlist narrowness control — before the full-history gitleaks pass. Public content: `check_public_content.py --self-test` + live run both exit 0 in `stdlib-checks` (runs 31894206384, 31895143032), plus the manual release-diff review below — **extended at panel-1 direction from the 19-file PR diff to the full 266-file `v5.0.0..candidate` window**, whose findings and dispositions are recorded in the second subsection. |
| 7 — harness surfaces exercised or assigned an honest tier | **met via explicit tiers; one live junction verification lands post-tag** | the README install table carries per-harness honest boundaries, now including the generated ChatGPT/OpenAI bridge (snapshot artifact, no live execution). Cursor's recorded behavioral epoch stays `BLOCKED_EXTERNAL`. ZCode: the junction **mechanism** was verified at v5.0.0 content on one fleet device (zms-pc-2025) with no recorded procedure — the v5.1.0-specific junction count (fifteen) is verified by the same-session post-tag installer `-Verify` receipt; plugin install remains untested. Other plugin surfaces carry the per-harness tiers recorded in `HARNESS-VERIFICATION-MATRIX-SUCCESSOR-2026-08-07.md` (recorded at fourteen-skill content; the fifteenth seat adds no new runtime primitive on those surfaces — its caveat, the host-supplied custody runtime, is the README row's). No new live plugin-harness executions in this release. |
| 8 — independent Gauntlet publication review reaching GO | **GO — recorded, binding on the discharge set this commit executes** | panel record at `docs/gauntlet-runs/es-v510-publication-2026-08-15/GAUNTLET-SUMMARY.md`: panel 1 (standard, five isolated lenses + judge) ruled **NO-GO** on publishing `8180554` as-specified (P1 ×2, P2 ×5) and **GO binding on execution of the named discharge set**; this commit executes every pre-tag item (the two zero-commit live-surface fixes verified above; the row amendments and full-window review in this file; both suite dispatches at the final SHA), and a delta-scoped panel-2 re-affirmation runs on this candidate before tag creation — a regression there reverts to iterate, no tag. **Independence limits (per `RELEASING.md`):** lenses, arbitrator, and the release-evidence author share one model family (GLM-5.3) in isolated sub-agent contexts; every load-bearing mechanical row was re-verified independently via the live GitHub API; no cross-family or human adjudication ran — that ceiling is recorded, not waived. |

### Release-diff public-content review (item 6 record)

Scope: `git diff 1e36da9..7ba1f19` — 19 files, +303/−48 (version surfaces,
README, release notes, CI config, gitleaks config, custody CLI + mission
code, custody tests, two SKILL.md touch-ups), plus the current-tree
`check_public_content.py` pass cited above. Findings and dispositions:

- **No credentials, private paths, internal topology, or telemetry** in
  the 19-file release-PR diff (the window-wide topology findings are
  recorded in the extended subsection below). The one hostname-shaped
  token, `zms-pc-2025` in the item-7 row and
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

### Full release-window review — `v5.0.0..candidate` (item 6 record, extended at panel-1 direction)

Panel 1 ruled the 19-file scope above insufficient: the release diff a
consumer actually receives is `v5.0.0..<this candidate>` — **266 files,
+35,354/−466**. The window was enumerated for the disclosure classes by
three isolated lens contexts and re-verified by the dispatcher (reports in
the panel record); findings and dispositions:

- **RFC1918 topology literals, 8 files** (all new since v5.0.0, none in
  the 19-file PR diff): the mission-custody guard fixtures
  (`examples/invalid-manifest-guard-*.json`, `valid-manifest-guards.json`),
  `test_custody_gate.py`, and two `docs/superpowers/` custody-hook
  documents. Content: `10.10.10.x` host literals with `*arr`-service ports
  (7878/8989/8686/9696), the UNC path `//10.10.10.107/Media` paired with
  its drive mapping `M:/Media`, and `10.10.10.50` test endpoints.
  Disposition: **accepted as test/fixture data, operator-informed.** These
  are private-range literals with no credential, no hostname-to-service
  mapping beyond port conventions, and they have been public on `main`
  since the 2026-08-12/14 pushes — the tag adds no new exposure. Scrubbing
  was considered and rejected: the fixtures legitimately exercise
  path-scoping rules, git history is immutable, and rewrites would break
  the suite for zero exposure delta. The durable guard — extending
  `check_public_content.py` with RFC1918/UNC/email patterns, each with a
  RED seed — is a recorded post-tag work item.
- **Personal name + email, 11 tree files** (10 predate v5.0.0 and ship in
  its tree; one — the 2026-08-11 mission-custody-contracts plan document —
  is new in this window). Disposition: git-history DCO trailers are the
  accepted floor (unavoidable and already public); the new-in-window tree
  occurrences are **flagged to the operator** — the designated public
  callsign `SternOne` is the required form going forward, and historical
  plan documents are not rewritten. No credential accompanies any
  occurrence.
- **No credentials, tokens, telemetry, or public-range endpoints** were
  found anywhere in the window; the gitleaks full-history scan with its
  positive control (item 6, first half) covers the credential class
  mechanically.
- **Out-of-tree live surfaces** (repo description, public wiki) were
  stale for v5.0.0-era content and were fixed before this commit —
  recorded under item 4 above. The v5.0.0 release-body amendment ordered
  by `RELEASE-BODY-AMEND-v5.0.0.md` remains unexecuted and is carried as a
  post-tag work item.

## Known limitations, carried honestly

- **es#162: case-insensitive filesystems (macOS default APFS) are not
  supported for case-distinct multi-file tracking in the custody CLI.**
  Settled by dispatch runs — first at `8aa4ffe` on 2026-08-13 (run
  31723939498), re-confirmed at `2890ae6` and at the final tagged candidate
  (runs 31897018984, 31898055755, and 31899154663 at `5906464` — the
  true final-SHA dispatch, recorded in the annotated tag message; each time
  the required `contract` job green, the probe job failing the same 2
  lifecycle tests,
  `distinct-real-file-untouched` and `distinct-both-files-tracked-separately`);
  every other custody suite is green on the same tree, Linux included. The
  fix direction — probe the workspace filesystem's case behavior instead of
  keying on `os.name` — is filed on the issue.
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
