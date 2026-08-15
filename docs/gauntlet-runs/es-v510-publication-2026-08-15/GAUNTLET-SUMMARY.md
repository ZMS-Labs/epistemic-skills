# Gauntlet summary — v5.1.0 publication (panel 1 + panel-2 charter)

Run: `es-v510-publication-2026-08-15` · depth **standard** (5 evaluators +
judge) · docket mode `manual-docket` · independence `concurrent-isolated-subagents`
· role binding `materialized-role` · registry 3.0.0 @ `a71b7f30` · all
artifacts in this directory; ledger entry in the operator's private gauntlet
home (not committed).

## Subject

- **Decision:** create annotated tag `v5.1.0` and a non-draft GitHub Release
  (body = `docs/release/RELEASE-5.1.0.md` verbatim) for the candidate chain
  `7ba1f19` (release content, PR #179) → `8180554` (gate evidence, PR #180) →
  discharge commit (PR #181) → this record commit. Panel 1 froze
  `8180554` (git tree `0b275d98e2ea24982f63b1e3a3fd6d160e3b7ee9`).
- **Question:** conforming release under `RELEASING.md` — recorded GO, no
  unresolved P1/P2 — rather than another exception?

## Independence limits (mandatory disclosure)

Lenses, arbitrator, and the release-evidence author are **one model family**
(GLM-5.3) in isolated sub-agent contexts — concurrent, context-partitioned,
barrier-held, but same-family; no cross-family or human adjudication ran.
Mitigation: every load-bearing mechanical row (CI run/step conclusions,
scan controls, workflow triggers) was re-verified independently via the
live GitHub API by three lens contexts plus the dispatcher. The same-family
ceiling bounds the judgment rows; it is recorded, not waived.

## Panel 1 (against `8180554`)

| Seat | Stance | Report |
|---|---|---|
| script-kiddie | adversarial / security | `reports/script-kiddie.md` |
| angry-customer | adversarial / human-factors | `reports/angry-customer.md` |
| adjacent-possible-explorer | constructive / strategy | `reports/adjacent-possible-explorer.md` |
| causal-identification-auditor | metatextual / data-validity | `reports/causal-identification-auditor.md` |
| polymath-inquisitor (wildcard) | metatextual / framing | `reports/polymath-inquisitor.md` |
| pragmatic-judge (arbitrator; red-lines gate folded in) | arbitral | `arbitration.md` |

Verdict (full reasoning in `arbitration.md`; docket in `deepreason-docket.md`
of this directory):

- **Publishing `8180554` as specified: NO-GO.** P1 ×2 (immutable body would
  ship item-8 frozen at "pending"; live repo description + public wiki
  falsified item-4's "met") + P2 ×5 (item-6 review scope; exact-SHA suite
  evidence; phantom tier pointer; junction referent timing; silent
  budget-drop warning gap).
- **Fix-forward pathway: GO, binding on execution of the discharge set.**

## Discharge set and its execution

| Finding | Discharge | State at this record |
|---|---|---|
| P1-A pending item-8 row | terminal GO row + this record's coordinate + independence limits | done in PR #181; this commit lands the record |
| P1-B live surfaces | repo description (router phrase) + wiki install page | done zero-commit 2026-08-15, re-probed live (wiki `e6c6ba7..710dd2b`) |
| P2-C item-6 scope | full-window review with dispositions | done in PR #181 (notes §full release-window review) |
| P2-D exact-SHA suites | dispatch both path-filtered workflows at the final SHA | executed at the discharge commit `2890ae6`: `openai-bundles` run 31897020113 **success**; `mission-custody-contract` run 31897018984 — required `contract` job **success**; dispatch-only `contract-macos` probe **2 failures → es#162 settled**, see below |
| P2-E phantom tiers | re-point to successor matrix; README bridge row | done in PR #181 |
| P2-F junction referent | honest pin; post-tag `-Verify` receipt | done in PR #181; receipt lands post-tag |
| P2-G budget warning | README boundary note | done in PR #181 |
| AP-2 (P3 rider) | budget-script comment 14→15 | done in PR #181 |

### es#162 settlement (new evidence produced by the P2-D dispatch)

The first-ever `contract-macos` run failed 2 lifecycle tests
(`distinct-real-file-untouched`, `distinct-both-files-tracked-separately`) —
case-distinct pathnames collapse to one object on default (case-insensitive)
APFS. Evidence comment on es#162 (2026-08-15). Ruling D was written as
"any red → P1, revert to iterate" without anticipating that the dispatch
also fires the optional es#162 probe job. The bounded-reinstatement attack —
*the red came from the optional probe job, whose failure is the es#162
settlement, not the required suite* — goes to **panel 2**; the release notes
disclose the limitation either way. Fix direction stays as filed on es#162.

## Panel-2 charter (delta-scoped re-affirmation against this record commit)

Scope: the delta `8180554..this-commit` (PR #181 + this record) and the new
P2-D/es#162 evidence. Panel 1's rulings on unchanged content stand. Panel 2
must rule at minimum:

1. Does the discharge set satisfy each P1/P2 acceptance criterion as
   written in `arbitration.md`?
2. The D/es#162 bounded-reinstatement attack above — does the probe-job red
   block the tag, or is disclosed-limitation + green required job
   conforming?
3. Any regression introduced by the delta itself.

Verdict form: GO / CONDITIONAL / NO-GO with reversion triggers. The verdict
and the final-SHA suite run IDs are recorded in the **annotated tag
message** at publication and mirrored to this directory in the post-tag
record commit (main is rolling; `RELEASING.md` blesses post-tag corrective
documentation — the tag never moves).

## Non-claims

- Not behavioral superiority of the package (UNCHANGED posture).
- Not a retrospective GO for `v5.0.0` (item 8 remains WAIVED/NOT MET
  historically; the unexecuted v5.0.0 release-body amendment is a post-tag
  docket item).
- Not a macOS fix for es#162 — this run *settled* it and the release
  discloses it.
- Not satisfaction of any externally-enforced infra safety gate.

## Post-tag docket (tracked, not waived)

check_public_content RFC1918/UNC/email patterns with RED seeds · narrow
`ALLOWLIST_PREFIXES` to line-scoped regexes · POSIX install guard mirroring
the Windows one · mission custody in Kimi/plugin.json enumerations ·
path-filter ⊇ input-space coverage guard · full v5.1.0 wiki packet ·
v5.0.0 release-body amendment execution · es#162 filesystem-probe fix.
