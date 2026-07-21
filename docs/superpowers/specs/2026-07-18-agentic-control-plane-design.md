# Agentic control-plane design

**Status:** approved 2026-07-18; implementation not started.
**Scope:** reconcile the two ChatGPT Pro portfolio audits with the existing
agentic-skills packaging decision and define the first safe implementation
tranche.

## Decision

Keep `ZMS-Labs/epistemic-skills` public and focused. Create one private
`ZMS-Labs/agentic-control-plane` only after Phase 0 restores and inventories the
current public-core/private-overlay relationship.

The control plane initially includes a bounded `conformance/` module. Do not
create a separate `agentic-skill-lab`, `agent-continuity-skills`, or
`agent-runtime-skills` repository yet. Extract or create those only after their
independent lifecycle and family resemblance are demonstrated by real runs.

This refines, rather than reverses, the earlier Option B verdict: distinct public
method packs plus private bindings and operations remain correct. The refinement
removes editable private copies as an accepted steady state and makes installed
skill trees generated materializations.

## Why this option wins

Three repository shapes were considered:

1. **One private control plane with internal conformance** — selected.
2. **Separate private control-plane and skill-lab repositories immediately.**
3. **Private `zms-agent-ops` plus a continuity pack immediately.**

### Formal derivation

**SSOT and normalization-for-code.** A capability's identity determines its
source pin, license, installation scope, adapter set, and current compatibility
evidence. Storing compatibility status independently in a catalog repository and
an evaluation repository introduces an update dependency between two editable
records. Until independent lifecycles exist, that is an avoidable update anomaly.
The normalized base record belongs in the control plane; detailed run artifacts
are evidence referenced by stable IDs.

**Cohesion and coupling.** Pins, overlays, adapter generation, admission policy,
installation auditing, and conformance decisions initially change together.
Keeping their modules in one repository gives high functional cohesion without
coupling public method bodies to private policy. Evaluation runners may remain
upstream dependencies rather than becoming a new ZMS product.

**Failure domains.** Evaluation can execute untrusted skills and produce large
artifacts. Initially isolate it with dedicated directories, credentials, CI jobs,
retention rules, and output boundaries. A repository split becomes justified
when it needs independent secrets, retention, runner infrastructure, access
control, or release cadence.

**Reversibility.** Extracting a well-bounded `conformance/` module later is a
low-risk history-preserving operation. Merging two prematurely separated control
repositories after their schemas and claims diverge is harder. Start with the
more reversible topology.

**Type boundary.** Artifact kinds are not interchangeable:

| Kind | Source of truth | Invocation / treatment |
|---|---|---|
| Skill | Public or private method repository | Model-selectable when triggers match |
| Flow | Private control plane unless generically reusable | Explicit/manual; may contain human gates |
| Command | Harness adapter | Explicit user interface for a skill or flow |
| Agent role | Method repository | Orchestrator-invoked participant |
| Adapter | Control plane or public pack packaging | Never a method source |
| Overlay/policy | Private organization or project repository | Binding only; cannot override protocol |
| Tool/script | Owning method or control repository | Deterministic machinery invoked by a method |
| Run record | Private evidence store | Data, never protocol |
| Installation | Generated materialization | Disposable; never a source of truth |

**Synthesis.** The selected option concedes the immediate isolation of a separate
skill lab. It recovers that benefit with a strict `conformance/` boundary and
explicit extraction gates, without paying a second-repository coordination cost
before it is earned.

## Target portfolio boundary

```text
PUBLIC, ZMS-OWNED
  epistemic-skills
    Epistemic methods, portable roles, generic references, tests, and adapters.

PRIVATE, ZMS-OWNED
  agentic-control-plane
    Catalog, source locks, policy, private flows, adapters, materialization,
    installation auditing, and bounded conformance evidence.

  <private-fleet-repo> and product repositories
    Domain/project LOCAL overlays, acceptance contracts, and real run records.

UPSTREAM, PINNED
  obra/superpowers
    In-session software-development methodology.

  pro-vi/loopgen
    Long-running prompt/contract compiler.

  selected Ralph implementation(s)
    Experimental execution-loop references.

  gastownhall/beads
    Long-horizon task graph and persistent memory.

  trailofbits/skills
    Security, review, verification, and second-opinion specialists.

  vercel-labs/agent-skills
    Web/product implementation guidance.

  prime-radiant-inc/superpowers-evals
    Cross-harness behavioral-evaluation substrate.

  prime-radiant-inc/gauntlet
    UI/CLI/TUI QA actor candidate.

FUTURE, ONLY IF EARNED
  agentic-skill-lab
    Extract when evaluation has an independent security or operational lifecycle.

  agent-continuity-skills or agent-runtime-skills
    Create only after repeated runs reveal at least two coherent ZMS-owned methods
    not already supplied upstream.
```

## Control-plane responsibilities

The eventual private control plane owns:

- a canonical capability catalog and reviewed source lock;
- visibility, license, provenance, maturity, and installation-scope policy;
- overlay locations and validation rules;
- harness compatibility records tied to evidence IDs;
- adapter and installation materialization;
- duplicate-install and trigger-collision checks;
- private operator flows such as installation audit, session bank/resume, and
  release preparation;
- conformance scenarios and references to their run artifacts.

It does not own copied upstream/public method bodies, homelab-specific facts,
product acceptance criteria, or unrestricted run telemetry.

## Upstream dependency set

The following upstreams must be represented explicitly in the initial capability
inventory and eventual source lock. Inclusion here is a target-state requirement,
not a claim that every source is already admitted, installed, or pinned:

| Upstream | Intended role | Initial disposition |
|---|---|---|
| `obra/superpowers` | In-session software-development methodology | Daily-core dependency; verify installed source and pin |
| `pro-vi/loopgen` | Long-running prompt/contract compiler | Explicit pilot candidate; verify license and provenance before adoption |
| selected Ralph implementation(s) | Experimental execution-loop references | Reference/canary only until a runner decision is earned |
| `gastownhall/beads` | Long-horizon task graph and persistent memory | Project-scoped pilot candidate |
| `trailofbits/skills` | Security, review, verification, and second-opinion specialists | Admit selected plugins individually; preserve upstream licensing |
| `vercel-labs/agent-skills` | Web/product implementation guidance | Project-scoped selections; do not install globally as a blob |
| `prime-radiant-inc/superpowers-evals` | Cross-harness behavioral-evaluation substrate | Primary evaluation-runner candidate |
| `prime-radiant-inc/gauntlet` | UI/CLI/TUI QA actor | Actor/evidence-collector pilot; never self-certifies ZMS UAT |

For every upstream, the control plane must eventually record the immutable ref,
source URL, license/provenance status, admitted capabilities, installation scope,
harness support, conflicts, update policy, and rollback path. Method bodies remain
upstream; the control plane stores only catalog facts, locks, adapters, policy, and
evidence references.

## Phase 0 — restore truth before expansion

Phase 0 is the only approved implementation tranche from this design.

### 1. Preserve concurrent work

Do not modify, delete, stage, or absorb the current unrelated worktree changes:

- `plugins/epistemic-skills/skills/evidence-research/SKILL.md`;
- `plugins/epistemic-skills/skills/gauntlet/runs/ledger.jsonl`;
- `.cursor/`;
- `outputs/`.

Re-check repository state immediately before every commit.

### 2. Correct stale Gauntlet overlay state

In the authoritative `<local-checkout>/<private-fleet-repo>` checkout:

- replace the claim that issue `#164` is open with its resolved state;
- remove the temporary "until #164 lands" instruction;
- retain the fail-closed operational rule as current protocol, not a workaround;
- add a machine-checkable assertion that the installed public core contains both
  the binary-aware guard and its positive/negative regression coverage.

Do not conflate this overlay-narrative defect with the separate
`evidence-research` core drift.

### 3. Inventory public-core/private-copy drift

Produce a machine-readable inventory for every private `skills/*/SKILL.md` copy:

- public source path and commit/release;
- private path;
- byte hash after newline normalization;
- equality state;
- associated `LOCAL.md` path;
- installed harness copies and revisions when observable.

The inventory is evidence, not a reconciliation mechanism. Phase 0 must not
blindly overwrite a divergent private file or delete copied cores before the
materializer and lock format are approved.

### 4. Review pushed commit `5f8a190` by forward fixes only

The published commit mixed the packaging decision with `evidence-research`,
Zotero reference, router, and README changes. Do not rewrite history. Classify
each change as:

- retained generic protocol;
- public integration reference;
- private overlay/policy;
- harness adapter detail;
- accidental or unsupported behavior requiring a focused follow-up.

Do not edit the concurrently modified `evidence-research/SKILL.md` until its
owner's work is reconciled.

### 5. Correct the historical handoff

The pre-reboot session-handoff note (git state pause/resume record) has since
been relocated to the private fleet repo as internal working material with no
public value; commits `5f8a190`, `95c4881`, and `395ab0b` from that session
were subsequently pushed to `origin/main`.

### 6. Produce the first capability inventory

Record the currently observed owned, upstream, private, and installed
capabilities without installing new packages. Each entry must distinguish:

- method ownership;
- source and revision;
- visibility and license;
- global, explicit, project, or fleet-only scope;
- harness installation mechanism;
- overlay source;
- verified, pending, degraded, or conflicting state;
- evidence reference and observation timestamp.

The inventory must include all eight upstream entries in **Upstream dependency
set**, even when their initial state is `not-installed`, `license-pending`,
`pilot-candidate`, or `unverified`. Omission is not an allowed way to represent a
pending decision.

## Phase 0 acceptance criteria

Phase 0 is complete only when:

1. issue `#164` is represented as resolved and the overlay no longer describes
   the shipped guard as pending;
2. the binary-aware guard is checked mechanically against the installed/public
   core, with a regression assertion that can fail;
3. every discovered copied core has an inventory row and an equality state;
4. `evidence-research` drift is visible and not silently overwritten;
5. the accidental scope of `5f8a190` is classified in a durable report;
6. the reboot handoff clearly identifies itself as historical;
7. the initial capability inventory exists without introducing a new package or
   installation mechanism;
8. all eight named upstream entries are present with an honest current state and
   no unsupported `pinned` or `verified` claim;
9. unrelated worktree changes remain byte-for-byte untouched;
10. verification commands and their results are recorded.

## Extraction and creation gates

### Separate `agentic-skill-lab`

Extract only when at least one condition is demonstrated:

- independent credentials or access control;
- independent artifact-retention/security policy;
- dedicated runner infrastructure with a distinct failure domain;
- independent release cadence or maintainership;
- repository size or CI cost materially impairs control-plane operation.

Compatibility verdicts remain catalog facts in the control plane; the lab, if
extracted, supplies referenced evidence rather than a competing status source.

### Runtime or continuity method pack

Create only when all are true:

- at least two coherent ZMS-owned methods recur in real runs;
- upstream loop, task-graph, and workflow packages do not already own them;
- each method has a distinct trigger and stopping boundary;
- positive and negative trigger scenarios pass on the sentinel harness set;
- interruption/resume fixtures show lower false-DONE and stale-state rates than
  the unskilled baseline;
- the frozen repository proposal passes the required Gauntlet gate.

## Non-goals

- Creating a new public repository during Phase 0.
- Installing every repository named by either audit.
- Forking Superpowers, loopgen, Ralph, Beads, or specialist skill packs.
- Rewriting pushed history.
- Treating manifests or file equality as behavioral portability proof.
- Generalizing `evidence-locked-uat` before an equivalent verified protocol
  exists.
- Adding a third always-loaded global router.

## Provenance

- Existing packaging verdict:
  `2026-07-18-agentic-skills-packaging-architecture.md`.
- Historical pause record: relocated to the private fleet repo (fleet-internal working material; see the public-repo hygiene sweep addendum in `docs/release/`).
- ChatGPT Pro portfolio audits supplied by the operator on 2026-07-18.
- Live verification before approval confirmed the `evidence-research` public /
  private mismatch, stale issue-`#164` overlay language, current pushed Git
  state, missing Kimi adapter, and manually repeated package version metadata.
