# Forward classification of commit 5f8a190

**Reviewed:** 2026-07-19
**Commit:** `5f8a190a81601e76406764bde5ecead0ba9a5295`
**Policy:** forward fixes only; do not rewrite pushed history.

## Scope

Commit `5f8a190` changed six paths. Its intended packaging decision was bundled
with an already-staged change to the `evidence-research` protocol, its Zotero
reference, the collection router, and the public README. This report classifies
the pushed surface without changing the concurrently edited
`plugins/epistemic-skills/skills/evidence-research/SKILL.md`.

The classifications below describe artifact ownership, not whether the prose is
good or bad. A useful change may still require a focused follow-up because it
entered an unrelated commit without an isolated protocol review.

## Classification ledger

| Path / coherent hunk | Classification | Evidence | Forward disposition |
|---|---|---|---|
| `README.md`: evidence-research summary row | `public integration reference` | `5f8a190:README.md` hunk `@@ -30,9 +30,9` | Defer final wording until the protocol-owner reconciliation below; keep current pushed text meanwhile. |
| `README.md`: runtime dependency changes from Consensus/Scite to Consensus/Scite/library | `public integration reference` | `5f8a190:README.md` hunk `@@ -150,9 +150,9` | Same dependency as the core protocol; update only in the focused follow-up. |
| `docs/superpowers/specs/2026-07-17-epistemic-skills-plugin-design.md`: packaging-spec cross-link | `public integration reference` | `5f8a190:...plugin-design.md` hunk `@@ -32,4 +32,8` | Retain. It links two public design records and changes no runtime behavior. |
| `docs/superpowers/specs/2026-07-18-agentic-skills-packaging-architecture.md`: layer map, type boundary, options, and Option B verdict | `public integration reference` | `5f8a190:...packaging-architecture.md` lines 1-78 | Retain as the historical packaging decision, now refined by `2026-07-18-agentic-control-plane-design.md`. |
| Same file: named private fleet layout, `zms-homelab` paths, overlay/deploy rules, and private index proposal | `private overlay/policy` | `5f8a190:...packaging-architecture.md` lines 35-50 and 79-115 | Keep as already-published historical context; future operational detail belongs in the private control-plane/homelab layer. Do not add new private facts here. |
| Same file: loopgen, `/release`, pickup checklist, non-goals, and provenance | `public integration reference` | `5f8a190:...packaging-architecture.md` lines 90-137 | Retain. Later actions are governed by the approved control-plane design, not this older pickup checklist alone. |
| `plugins/epistemic-skills/skills/evidence-research/SKILL.md`: frontmatter and two-engine → mandatory three-layer contract | `accidental or unsupported behavior requiring focused follow-up` | `5f8a190:...evidence-research/SKILL.md` hunks `@@ -1,26 +1,36` and `@@ -32,79 +42,104` | Defer pending owner reconciliation. The durability goal is coherent, but mandatory Zotero activation and tandem-use semantics changed the public trigger/protocol outside the packaging commit's intended scope. |
| Same file: holdings-first workflow and Consensus discovery changes | `accidental or unsupported behavior requiring focused follow-up` | hunks beginning `### 3. Holdings check` through `### 4. Discover` | Evaluate as public protocol in a focused change with positive/negative trigger tests; do not silently revert or broaden in Phase 0. |
| Same file: cross-validation, selection, mandatory deposit, and matrix `holdings` column | `accidental or unsupported behavior requiring focused follow-up` | hunks `### 7. Cross-validate` through `### 9. Claim-evidence matrix` | Defer pending owner reconciliation. Confirm that unavailable/operator-mediated Zotero degrades without blocking valid scholarly research. |
| Same file: synthesis, artifact emission, adversarial handoff, references, and LOCAL binding | `accidental or unsupported behavior requiring focused follow-up` | hunks `### 10. Synthesize` through `## Local overlay` | Reconcile with the same focused protocol change so README, router, references, and method remain one reviewed unit. |
| `plugins/epistemic-skills/skills/evidence-research/reference/zotero-first-contact.md`: role, access modes, holdings/deposit contract, degradation labels | `public integration reference` | `5f8a190:.../reference/zotero-first-contact.md` lines 1-84 | Retain as a documented-but-live-schema-subordinate reference. Verify mutable external claims during the focused protocol review. |
| `plugins/epistemic-skills/skills/using-epistemic-skills/SKILL.md`: output contract gains holdings | `public integration reference` | hunk `@@ -21,9 +21,9` | Defer final wording until `evidence-research` ownership reconciliation; router must describe, not independently redefine, the child skill. |
| Same router: trigger rationale gains durable holdings | `public integration reference` | hunk `@@ -62,9 +62,9` | Same disposition; keep router and child protocol synchronized in the focused follow-up. |
| Same router: missing Zotero becomes an explicit degradation example | `retained generic protocol` | hunk `@@ -83,10 +83,10` | Retain. Explicit degradation is an existing collection invariant and does not by itself require Zotero to be installed. |

## Forward conclusions

1. Do not rewrite or split `5f8a190`; it is already on `origin/main`.
2. Retain the packaging verdict and generic Zotero first-contact reference as
   public historical/integration documentation.
3. Treat the mandatory triad and deposit semantics as an accidentally bundled
   public protocol change that still needs one focused owner reconciliation.
4. In that follow-up, review the public core, README, router, trigger tests, and
   degradation behavior together. Do not edit only one projection.
5. Phase 0 does not perform that reconciliation because the public
   `evidence-research/SKILL.md` has concurrent owner work in progress.

## Verification commands

```text
git show --format=fuller --name-status 5f8a190
git show --format= --unified=4 5f8a190 -- README.md docs/superpowers/specs/2026-07-17-epistemic-skills-plugin-design.md docs/superpowers/specs/2026-07-18-agentic-skills-packaging-architecture.md plugins/epistemic-skills/skills/evidence-research/SKILL.md plugins/epistemic-skills/skills/evidence-research/reference/zotero-first-contact.md plugins/epistemic-skills/skills/using-epistemic-skills/SKILL.md
```

The first command returns exactly six changed paths. This report is the durable
forward classification; it is not authorization to modify the protected method
body during Phase 0.
