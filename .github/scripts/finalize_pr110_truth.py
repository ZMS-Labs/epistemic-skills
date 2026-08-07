#!/usr/bin/env python3
"""Remove the remaining stale Practical Agency assumptions from PR #110.

This helper is branch-scoped, exact-match, and self-removing. It changes only
current normative documentation and current-status review summaries. Frozen lens
reports remain preserved behind their existing reconciliation notices.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DESIGN = ROOT / "docs/superpowers/specs/2026-08-07-practical-agency-and-commission-watch-design.md"
PLAN = ROOT / "docs/superpowers/plans/2026-08-07-practical-agency-bootstrap.md"
GAUNTLET = ROOT / "docs/gauntlet-runs/commission-watch-pr110-2026-08-07"
SUMMARY = GAUNTLET / "GAUNTLET-SUMMARY.md"
RECONCILIATION = GAUNTLET / "POST-FREEZE-RECONCILIATION.md"
SCRIPT = ROOT / ".github/scripts/finalize_pr110_truth.py"
WORKFLOW = ROOT / ".github/workflows/finalize-pr110-truth.yml"
SEED_SHA = "e244d534a6e26bc9a352846a25ffce18b8d93a53"


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected one match, found {count}: {old[:100]!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def reconcile_design() -> None:
    replace_once(
        DESIGN,
        "**Scope:** successor design for `epistemic-skills/watch` plus the boundary and bootstrap contract for a separate `practical-agency` project",
        "**Scope:** successor design for `epistemic-skills/watch` plus the boundary and seed-adoption contract for the existing `practical-agency` project",
    )

    replace_once(
        DESIGN,
        """That seed establishes the project identity and sole public entry skill. It does
**not** yet implement the deterministic `mission-manifest@1` kernel, authority
state machine, atomic checkpoints, dynamic capability discovery, independent
acceptance, `\"helix it\"` compatibility, or `watch-commission@1` intake described
later in this document. All later repository shapes, lifecycle rules, invocation
aliases, and handoff diagrams are approved **target architecture**, not claims
about the inspected external repository. Implementation must adopt the seed and
preserve one canonical `manifest` skill body rather than create competing copies.
""",
        """That seed establishes the project identity and sole public entry skill. It is an
authorization-and-recording steward, not yet the approved mission driver: its
current trigger explicitly declines use when a current mission manifest already
governs the task, and its completion flow does not require an independent
acceptor. It also lacks the deterministic `mission-manifest@1` kernel, target
lifecycle, create/resume/reconcile/advance/verify/close modes, atomic checkpoints,
dynamic capability discovery, bounded return points, `\"helix it\"` compatibility,
and `watch-commission@1` intake described later in this document. The v0 guide's
`draft|active|hold|complete|cancelled` vocabulary is an input to migrate, not the
`mission-manifest@1` state machine.

All later repository shapes, lifecycle rules, invocation aliases, and handoff
diagrams are approved **target architecture**, not claims about the inspected
external repository. Implementation must adopt the seed and preserve the root
`skills/manifest/SKILL.md` as the one canonical skill body rather than create a
competing copy.
""",
    )

    replace_once(
        DESIGN,
        """### Recommended repository shape

```text
practical-agency/
├── plugins/practical-agency/skills/manifest/SKILL.md
├── contracts/
│   ├── mission-manifest.schema.json
│   ├── mission-event.schema.json
│   ├── checkpoint.schema.json
│   ├── capability-request.schema.json
│   ├── capability-result.schema.json
│   └── execution-receipt.schema.json
├── practical_agency/
│   ├── manifest_model.py
│   ├── state_machine.py
│   ├── authority.py
│   ├── capability_discovery.py
│   ├── coordinator.py
│   └── checkpoint_store.py
├── roles/
│   ├── mission-steward.md
│   └── independent-acceptor.md
├── adapters/
│   ├── generic-agent-skills/
│   ├── repository/
│   ├── scheduler/
│   └── execution-orchestrator/
├── evals/
├── examples/
└── docs/
```
""",
        """### Recommended repository shape

The existing root skill remains canonical. Harness metadata points at `./skills`;
no second independently editable skill tree is introduced.

```text
practical-agency/
├── skills/manifest/SKILL.md
├── plugin.json
├── .cursor-plugin/plugin.json
├── .claude-plugin/plugin.json        # optional harness metadata; points at ./skills
├── contracts/
│   ├── mission-manifest.schema.json
│   ├── mission-event.schema.json
│   ├── checkpoint.schema.json
│   ├── capability-request.schema.json
│   ├── capability-result.schema.json
│   └── execution-receipt.schema.json
├── practical_agency/
│   ├── manifest_model.py
│   ├── state_machine.py
│   ├── authority.py
│   ├── capability_discovery.py
│   ├── coordinator.py
│   └── checkpoint_store.py
├── roles/
│   ├── mission-steward.md
│   └── independent-acceptor.md
├── adapters/
│   ├── generic-agent-skills/
│   ├── repository/
│   ├── scheduler/
│   └── execution-orchestrator/
├── evals/
├── examples/
└── docs/
```
""",
    )


def reconcile_plan() -> None:
    replace_once(
        PLAN,
        "# Practical Agency Bootstrap Implementation Plan",
        "# Practical Agency Seed-Adoption Implementation Plan",
    )
    replace_once(
        PLAN,
        "**Goal:** Create `ZMS-Labs/practical-agency`, a portable mission-control project whose sole public skill `manifest` carries operator-authorized intent through durable, coordinated, resumable action without self-certifying completion.",
        "**Goal:** Evolve the existing `ZMS-Labs/practical-agency` seed into a portable mission-control project whose sole public skill `manifest` carries operator-authorized intent through durable, coordinated, resumable action without self-certifying completion.",
    )

    replace_once(
        PLAN,
        f"""### Existing-seed amendment — normative over absence assumptions below

`ZMS-Labs/practical-agency` already exists at inspected `main` revision
`{SEED_SHA}` with `README.md`, `LICENSE`, `plugin.json`,
`.cursor-plugin/plugin.json`, `docs/mission-manifest.md`, and the canonical root
`skills/manifest/SKILL.md`.

Interpret the original task sketches as follows:

- **Task 1 adopts and normalizes the existing repository; it does not create it.**
  Existing history, README, license, metadata, and skill are inputs to inspect and
  modify. Repository settings still need normalization: projects/wiki are
  enabled, merge/rebase commits are allowed, and head branches are not deleted
  automatically.
- **The root `skills/manifest/SKILL.md` is the canonical v0.1 skill surface.** Do
  not add a second independently editable copy under `plugins/`; point harness
  metadata at the one canonical directory.
- **Task 7 upgrades an existing seed skill.** Its RED condition is missing
  mission-kernel, checkpoint, independent-acceptance, `\"helix it\"`, and
  commission-intake semantics—not absence of a skill file.
- The current v0 Markdown manifest guide is not `mission-manifest@1`; the planned
  schema, deterministic Python kernel, tests, checkpoints, capability discovery,
  coordinator, and watch adapter remain unimplemented.
- The current seed does not accept `watch-commission@1`. Task 8 remains the first
  machine-verified cross-package handoff; until then no automatic route may be
  claimed.

These amendments supersede every later instruction to create the repository,
create a first `manifest` skill from nothing, or treat the target layout and
compatibility phrases as already implemented. All other safety, TDD, authority,
state, and verification requirements remain in force.
""",
        f"""### Verified starting point

This plan starts from inspected `main` revision `{SEED_SHA}`. The repository
already contains `README.md`, `LICENSE`, root and Cursor plugin metadata,
`docs/mission-manifest.md`, and the canonical root `skills/manifest/SKILL.md`.
Do not recreate, fork, or replace that history with a second package tree.

The seed is useful but materially short of the approved driver:

- `manifest` currently declines invocation when a current mission manifest already
  governs the task; the target must create **and** resume, reconcile, advance,
  verify, or close an existing mission;
- its completion block does not yet require an independent acceptor;
- the v0 guide uses `draft|active|hold|complete|cancelled`, not the closed
  `mission-manifest@1` lifecycle;
- no deterministic kernel, atomic checkpoint store, dynamic capability discovery,
  bounded return-point coordinator, `\"helix it\"` compatibility, or
  `watch-commission@1` intake exists; and
- repository settings still need normalization: projects/wiki are enabled,
  merge/rebase commits are allowed, and merged head branches are retained.

Every task below modifies this seed in place. The root
`skills/manifest/SKILL.md` remains the sole canonical skill body and all harness
metadata must point at `./skills`.
""",
    )

    replace_once(
        PLAN,
        """## Initial repository structure

```text
practical-agency/
├── .github/
│   ├── scripts/check_dco.py
│   └── workflows/ci.yml
├── plugins/practical-agency/
│   ├── .claude-plugin/plugin.json
│   └── skills/manifest/SKILL.md
├── practical_agency/
│   ├── __init__.py
│   ├── authority.py
│   ├── capability_discovery.py
│   ├── checkpoint_store.py
│   ├── coordinator.py
│   ├── manifest_model.py
│   ├── state_machine.py
│   └── validation.py
├── contracts/
│   ├── capability-request.schema.json
│   ├── capability-result.schema.json
│   ├── checkpoint.schema.json
│   ├── execution-receipt.schema.json
│   ├── mission-event.schema.json
│   └── mission-manifest.schema.json
├── roles/
│   ├── independent-acceptor.md
│   └── mission-steward.md
├── adapters/
│   └── README.md
├── examples/
│   ├── minimal-mission.json
│   └── watch-commission-mission.json
├── tests/
│   ├── test_authority.py
│   ├── test_capability_discovery.py
│   ├── test_checkpoint_store.py
│   ├── test_coordinator.py
│   ├── test_manifest_model.py
│   ├── test_manifest_skill.py
│   └── test_state_machine.py
├── AGENTS.md
├── LICENSE
├── README.md
└── pyproject.toml
```
""",
        """## Target repository structure

```text
practical-agency/
├── .github/
│   ├── scripts/check_dco.py
│   └── workflows/ci.yml
├── skills/manifest/SKILL.md
├── plugin.json
├── .cursor-plugin/plugin.json
├── .claude-plugin/plugin.json
├── practical_agency/
│   ├── __init__.py
│   ├── authority.py
│   ├── capability_discovery.py
│   ├── checkpoint_store.py
│   ├── coordinator.py
│   ├── manifest_model.py
│   ├── state_machine.py
│   └── validation.py
├── contracts/
│   ├── capability-request.schema.json
│   ├── capability-result.schema.json
│   ├── checkpoint.schema.json
│   ├── execution-receipt.schema.json
│   ├── mission-event.schema.json
│   └── mission-manifest.schema.json
├── roles/
│   ├── independent-acceptor.md
│   └── mission-steward.md
├── adapters/
│   └── README.md
├── examples/
│   ├── minimal-mission.json
│   └── watch-commission-mission.json
├── tests/
│   ├── test_authority.py
│   ├── test_capability_discovery.py
│   ├── test_checkpoint_store.py
│   ├── test_coordinator.py
│   ├── test_manifest_model.py
│   ├── test_manifest_skill.py
│   └── test_state_machine.py
├── AGENTS.md
├── LICENSE
├── README.md
└── pyproject.toml
```
""",
    )

    replace_once(
        PLAN,
        """### Task 1: Create the repository and fail-closed CI shell

**Files:**
- Create repository: `ZMS-Labs/practical-agency`
- Create: `README.md`
- Create: `LICENSE`
- Create: `pyproject.toml`
- Create: `AGENTS.md`
- Create: `.github/scripts/check_dco.py`
- Create: `.github/workflows/ci.yml`
- Create: `practical_agency/__init__.py`

**Interfaces:**
- Consumes: the approved design in `epistemic-skills/docs/superpowers/specs/2026-08-07-practical-agency-and-commission-watch-design.md`.
- Produces: a public repository with a deterministic test command and DCO enforcement.

- [ ] **Step 1: Create the GitHub repository**

Create `ZMS-Labs/practical-agency` with:

```text
visibility: public
default branch: main
initial README: disabled (the committed tree supplies it)
license template: disabled (the committed tree supplies GPL-3.0-or-later)
issues: enabled
projects: disabled initially
wiki: disabled initially
squash merge: enabled
merge commits: disabled
rebase merge: disabled
auto-merge: disabled initially
delete head branches: enabled
```

Do not create a repository named `manifest`, `praxis`, or `practical-agency-skills`.
""",
        """### Task 1: Adopt the seed and add a fail-closed CI shell

**Files:**
- Inspect/modify: `README.md`
- Inspect/preserve: `LICENSE`
- Modify: `plugin.json`
- Modify: `.cursor-plugin/plugin.json`
- Create: `.claude-plugin/plugin.json`
- Create: `pyproject.toml`
- Create: `AGENTS.md`
- Create: `.github/scripts/check_dco.py`
- Create: `.github/workflows/ci.yml`
- Create: `practical_agency/__init__.py`

**Interfaces:**
- Consumes: the existing seed plus the approved design in
  `epistemic-skills/docs/superpowers/specs/2026-08-07-practical-agency-and-commission-watch-design.md`.
- Produces: the same public repository and canonical skill history with a
  deterministic test command, normalized settings, and DCO enforcement.

- [ ] **Step 1: Verify the seed and normalize repository settings**

Before editing, assert the inspected files and commit are present and that exactly
one root `skills/*/SKILL.md` exists, named `manifest`. Then normalize settings to:

```text
visibility: public
default branch: main
issues: enabled
projects: disabled
wiki: disabled
squash merge: enabled
merge commits: disabled
rebase merge: disabled
auto-merge: disabled initially
delete head branches: enabled
```

Do not recreate the repository, rewrite its initial commits, or add a second skill
body under `plugins/`.
""",
    )

    replace_once(
        PLAN,
        "- [ ] **Step 2: Add the first-screen README**\n\nUse this opening exactly:",
        "- [ ] **Step 2: Reconcile the existing first-screen README**\n\nPreserve useful seed material, but make the current-versus-target status explicit and use this opening:",
    )
    replace_once(
        PLAN,
        "6. ensure exactly one `plugins/practical-agency/skills/*/SKILL.md` exists once Task 6 lands;",
        "6. ensure exactly one root `skills/*/SKILL.md` exists and it is `skills/manifest/SKILL.md`;",
    )
    replace_once(
        PLAN,
        "git commit -m \"chore: bootstrap practical-agency repository",
        "git commit -m \"chore: adopt practical-agency seed",
    )

    replace_once(
        PLAN,
        """### Task 7: Add the sole public `manifest` skill

**Files:**
- Create: `tests/test_manifest_skill.py`
- Create: `plugins/practical-agency/skills/manifest/SKILL.md`
- Create: `plugins/practical-agency/.claude-plugin/plugin.json`
- Modify: `.github/workflows/ci.yml`
- Modify: `README.md`
""",
        """### Task 7: Upgrade the sole public `manifest` skill

**Files:**
- Create: `tests/test_manifest_skill.py`
- Modify: `skills/manifest/SKILL.md`
- Modify: `plugin.json`
- Modify: `.cursor-plugin/plugin.json`
- Create/modify: `.claude-plugin/plugin.json`
- Modify: `.github/workflows/ci.yml`
- Modify: `README.md`
""",
    )
    replace_once(
        PLAN,
        """SKILLS = ROOT / \"plugins\" / \"practical-agency\" / \"skills\"
skill_files = sorted(SKILLS.glob(\"*/SKILL.md\"))
self.assertEqual([path.parent.name for path in skill_files], [\"manifest\"])

text = skill_files[0].read_text(encoding=\"utf-8\")
for required in (
    \"name: manifest\",
    \"operator\",
    \"mission manifest\",
    \"never self-certify\",
    \"capability\",
    \"checkpoint\",
    \"helix it\",
):
    self.assertIn(required, text)
""",
        """SKILLS = ROOT / \"skills\"
skill_files = sorted(SKILLS.glob(\"*/SKILL.md\"))
self.assertEqual([path.parent.name for path in skill_files], [\"manifest\"])

text = skill_files[0].read_text(encoding=\"utf-8\")
for required in (
    \"name: manifest\",
    \"operator\",
    \"mission manifest\",
    \"never self-certify\",
    \"capability\",
    \"checkpoint\",
    \"helix it\",
    \"resume\",
    \"reconcile\",
):
    self.assertIn(required, text)
self.assertNotIn(\"when a mission manifest already governs the task and is current\", text)
""",
    )
    replace_once(
        PLAN,
        "Expected: no skill exists.",
        "Expected: the existing seed skill fails the target semantic assertions (driver modes, independent completion, checkpointing, or compatibility intent).",
    )
    replace_once(
        PLAN,
        "- [ ] **Step 3: Write the `manifest` skill**",
        "- [ ] **Step 3: Upgrade the canonical `manifest` skill in place**",
    )
    replace_once(
        PLAN,
        """The body must define:

1. what Practical Agency is and is not;
""",
        """Remove the seed's decline rule for an already-current manifest: the same
public entry must be able to create, resume, reconcile, advance, verify, or close
a mission. Preserve proportional decline only for genuinely routine one-step work.

The body must define:

1. what Practical Agency is and is not;
""",
    )
    replace_once(
        PLAN,
        "`plugin.json` points directly at `./skills` and describes the package as one explicit-entry mission-control skill. No copied skill inventory.",
        "Root, Cursor, and any Claude harness metadata point directly at the same `./skills` directory and describe one explicit-entry mission-control skill. No copied skill inventory or duplicate skill body is permitted.",
    )
    replace_once(
        PLAN,
        "git add plugins README.md .github/workflows/ci.yml tests/test_manifest_skill.py\ngit commit -m \"feat: add the manifest mission-control skill",
        "git add skills/manifest/SKILL.md plugin.json .cursor-plugin .claude-plugin README.md .github/workflows/ci.yml tests/test_manifest_skill.py\ngit commit -m \"feat: upgrade the manifest mission-control skill",
    )


def reconcile_gauntlet() -> None:
    replace_once(
        SUMMARY,
        """> **Current-status correction:** See
> [POST-FREEZE-RECONCILIATION.md](POST-FREEZE-RECONCILIATION.md). Practical Agency
> and one initial `manifest` skill now exist; its deterministic kernel and
> commission intake do not. Exact-head jobs execute, but the clean-room step is
> red on raw-SHA checkout. The historical frozen verdict below remains
> `CONDITIONAL`; the current recommendation remains **NO-MERGE** until the exact
> final head passes and independent review (or an explicit degraded waiver) is
> recorded.
""",
        """> **Current-status correction:** See
> [POST-FREEZE-RECONCILIATION.md](POST-FREEZE-RECONCILIATION.md). Practical Agency
> and one initial `manifest` skill now exist; its deterministic kernel and
> commission intake do not. The dedicated reconciliation workflow passed the
> exact-commit clean-room and focused repository gates. The ordinary PR-triggered
> workflows for the current head are `action_required` and still need approval
> and a green conclusion. The historical frozen verdict remains `CONDITIONAL`;
> the current recommendation remains **NO-MERGE** until those ordinary gates and
> independent review (or an explicit degraded waiver) close.
""",
    )
    replace_once(
        SUMMARY,
        "- Practical Agency is correctly separated as future mission control with one\n  public `manifest` skill.",
        "- Practical Agency is correctly separated as an existing seed with one public\n  `manifest` skill and an explicitly unimplemented target mission-control kernel.",
    )
    replace_once(
        SUMMARY,
        "- Exact-head jobs execute; the current raw-SHA clean-room checkout failure is not a test pass.",
        "- The dedicated exact-commit reconciliation gate passed; ordinary PR-triggered workflows for the current head remain approval-blocked and are not yet green.",
    )

    RECONCILIATION.write_text(
        f"""# Post-freeze reconciliation — PR #110 and Practical Agency

**Date:** 2026-08-07  
**Epistemic-skills subject:** PR #110  
**External baseline inspected:** `ZMS-Labs/practical-agency@{SEED_SHA}`

This document is the authoritative current-status correction for the frozen
Gauntlet artifacts in this directory. Those reports remain preserved as review
history; statements below supersede their stale cross-repository premises and
merge conditions.

## Actual Practical Agency baseline

The separate public repository exists and its inspected `main` contains:

```text
.cursor-plugin/plugin.json
.gitignore
LICENSE
README.md
docs/mission-manifest.md
plugin.json
skills/manifest/SKILL.md
```

It publishes one initial public skill, `manifest`. The seed is prose-only relative
to the approved architecture. It has no deterministic Python mission kernel,
`mission-manifest@1` schema/validator, authority transition machine, atomic
checkpoint store, dynamic capability discovery, independent acceptor,
`watch-commission@1` adapter/intake, or verified `\"helix it\"` compatibility.
The current skill also declines invocation when a current manifest already
governs the task and permits closure through a steward-written completion block;
those behaviors are seed limitations, not the approved driver contract.

## Stale or contradictory assumptions corrected

| Prior premise in PR #110 | Current truth |
|---|---|
| Practical Agency could not be created / no repository exists | The repository exists at the inspected revision above. |
| No live or packaged `manifest` skill exists | One initial root skill exists; live harness loading was not verified by PR #110. |
| The implementation plan begins by creating README, LICENSE, metadata, and skill | Those artifacts already exist and must be adopted and modified in place. |
| `plugins/practical-agency/skills/manifest` is canonical | Root `skills/manifest/SKILL.md` is canonical; every harness metadata surface must point at it. |
| Task 7 RED is “no skill exists” | RED is the existing skill's missing driver modes, independent acceptance, checkpointing, compatibility intent, and kernel integration. |
| A current mission manifest means `manifest` should decline | The approved public entry must also resume, reconcile, advance, verify, and close existing missions. |
| `\"helix it\"` is already supported | It is approved target compatibility intent and is absent from the inspected seed. |
| `manifest` can retain or operate `watch-commission@1` | No intake, adapter, or verifier integration exists on inspected `main`. |
| Adding `manifest` to `watch.metadata.hands-to` is now correct | Still false: no admitted cross-package intake contract exists. |
| `handoff.on_crossing` denotes mission custody | It denotes post-crossing `triage`/`decision-ledger`; custody is separate outward transport. |
| The raw-SHA clean-room checkout defect is still open | Closed: reconciliation run `31196648201` passed focused checks and exact-commit clean-room checkout before pushing the verified commit. |
| Temporary self-mutating workflows are product surfaces | They are absent from the reconciled PR tree and must remain absent. |

## Commission-watch / manifest boundary

- `watch` owns the epistemic commission: bound, substrate, external mechanism,
  safety controls, evidence receipts, current state, block evidence, and proof
  history.
- The external observer—not either Markdown skill—owns persistence between
  sessions.
- `handoff.on_crossing` and `watch.metadata.hands-to` remain
  `[triage, decision-ledger]` because they describe response after a real crossing.
- Optional mission-control custody is a separate outward transport concern. A
  future Practical Agency consumer may retain a validated commission, select an
  authorized adapter, checkpoint receipts, and reopen a mission. It may not
  synthesize `PROVEN`, weaken the upstream verifier, obey record fields as
  instructions, or treat receipt-reference shape as external truth.
- No automatic cross-package handoff exists until Practical Agency implements and
  verifies an intake contract. Generic outward handoff is therefore the correct
  current wording.

## Reconciliation completed in the PR

1. The commission-watch skill, schema, verifier, tests, examples, security
   boundary, README/health changes, and permanent contract CI remain intact.
2. `cleanroom_ci.sh` now supports a fresh detached checkout of an exact locally
   available commit instead of treating every ref as a branch or tag.
3. Temporary migration and verification workflows are absent from the final tree.
4. The design and implementation plan now start directly from the actual
   Practical Agency seed and preserve the root canonical skill.
5. Post-crossing response is explicitly separated from commission custody.
6. The PR body and current-status review records distinguish proved
   commission-watch behavior from unimplemented Practical Agency behavior.

## Current blockers and recommendation

- **B1 — ordinary final-head gates:** the dedicated reconciliation workflow is
  green, but the ordinary PR-triggered workflows for the current head are
  `action_required`. Approve them and require successful conclusions before
  merge.
- **B2 — independent acceptance:** no formal independent PR review is recorded.
  Obtain one and resolve actionable P1/P2 findings, or record an explicit bounded
  degraded-review waiver. A waiver is not independence.
- **B3 — hygiene guard:** temporary workflows are absent and the boundary text is
  truthful at the reconciled head; re-check after any later commit.

**Recommendation: NO-MERGE until B1 and B2 close and B3 remains true.** Once they
close, merge PR #110 for its bounded commission-watch change. Completion of the
separate Practical Agency kernel is not a prerequisite for this merge and must
not be implied by it.
""",
        encoding="utf-8",
    )


def verify_truth() -> None:
    design = DESIGN.read_text(encoding="utf-8")
    plan = PLAN.read_text(encoding="utf-8")
    summary = SUMMARY.read_text(encoding="utf-8")
    reconciliation = RECONCILIATION.read_text(encoding="utf-8")

    forbidden = {
        PLAN: (
            "Create repository: `ZMS-Labs/practical-agency`",
            "### Task 1: Create the repository",
            "Expected: no skill exists.",
            "plugins/practical-agency/skills/manifest/SKILL.md",
            'ROOT / "plugins" / "practical-agency" / "skills"',
        ),
        DESIGN: ("├── plugins/practical-agency/skills/manifest/SKILL.md",),
        SUMMARY: ("clean-room step is\n> red on raw-SHA checkout",),
        RECONCILIATION: ("clean-room checkout fails because",),
    }
    texts = {PLAN: plan, DESIGN: design, SUMMARY: summary, RECONCILIATION: reconciliation}
    for path, needles in forbidden.items():
        for needle in needles:
            if needle in texts[path]:
                raise SystemExit(f"{path}: stale assumption remains: {needle!r}")

    required = {
        DESIGN: (
            "skills/manifest/SKILL.md",
            "current trigger explicitly declines use",
            "no second independently editable skill tree",
        ),
        PLAN: (
            "Seed-Adoption Implementation Plan",
            "resume, reconcile, advance",
            "ROOT / \"skills\"",
            "prepare_disabled",
        ),
        SUMMARY: ("dedicated reconciliation workflow passed", "action_required"),
        RECONCILIATION: (
            "Current blockers and recommendation",
            "No automatic cross-package handoff exists",
            "NO-MERGE until B1 and B2 close",
        ),
    }
    for path, needles in required.items():
        for needle in needles:
            if needle not in texts[path]:
                raise SystemExit(f"{path}: required truth marker missing: {needle!r}")


def remove_temporary_machinery() -> None:
    for path in (SCRIPT, WORKFLOW):
        if not path.exists():
            raise SystemExit(f"temporary path missing before cleanup: {path}")
        path.unlink()


def main() -> int:
    reconcile_design()
    reconcile_plan()
    reconcile_gauntlet()
    verify_truth()
    remove_temporary_machinery()
    print("PR #110 current truth reconciled")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
