#!/usr/bin/env python3
"""Apply the bounded factual reconciliation for epistemic-skills PR #110.

The script is branch-scoped and fail-closed. It preserves frozen review reports,
adds an authoritative post-freeze correction, fixes exact-SHA clean-room checkout,
and removes temporary self-mutating workflows before committing.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GAUNTLET = ROOT / "docs/gauntlet-runs/commission-watch-pr110-2026-08-07"
SEED_SHA = "e244d534a6e26bc9a352846a25ffce18b8d93a53"


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected one match, found {count}: {old[:90]!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def insert_after_once(path: Path, marker: str, addition: str) -> None:
    replace_once(path, marker, marker + addition)


def prepend_once(path: Path, marker: str, block: str) -> None:
    text = path.read_text(encoding="utf-8")
    if block in text:
        raise SystemExit(f"{path}: correction already present")
    if text.count(marker) != 1:
        raise SystemExit(f"{path}: expected one heading marker, found {text.count(marker)}")
    path.write_text(text.replace(marker, marker + block, 1), encoding="utf-8")


def fix_cleanroom() -> None:
    path = ROOT / ".github/scripts/cleanroom_ci.sh"
    replace_once(
        path,
        """# This script removes all three: a fresh clone of a named ref, on Linux, in a
# scratch directory, running exactly the `run: python ...` steps the workflow
# declares. It is not a replacement for CI's independence — it runs on the same
""",
        """# This script removes all three: a fresh detached checkout of the exact
# locally available commit named by REF, or a fresh clone of a remote branch/tag
# when that commit is not local, running exactly the workflow-declared Python
# steps. It is not a replacement for CI's independence — it runs on the same
""",
    )
    replace_once(
        path,
        """git clone --quiet --depth 50 --branch "$REF" "$REMOTE" "$WORK/repo" || {
  echo "FATAL: clone failed for ref '$REF'"; exit 2; }
cd "$WORK/repo" || exit 2
""",
        """SOURCE_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
RESOLVED_REF=""
if [ -n "$SOURCE_ROOT" ]; then
  RESOLVED_REF="$(git -C "$SOURCE_ROOT" rev-parse --verify "${REF}^{commit}" 2>/dev/null || true)"
fi

if [ -n "$RESOLVED_REF" ]; then
  # Clone committed objects only. --no-local avoids shared-object shortcuts while
  # preserving otherwise hidden PR merge commits available in the tested checkout.
  git clone --quiet --no-local --no-checkout "$SOURCE_ROOT" "$WORK/repo" || {
    echo "FATAL: clean clone failed for local commit '$RESOLVED_REF'"; exit 2; }
  cd "$WORK/repo" || exit 2
  git checkout --quiet --detach "$RESOLVED_REF" || {
    echo "FATAL: checkout failed for local commit '$RESOLVED_REF'"; exit 2; }
else
  git clone --quiet --depth 50 --branch "$REF" "$REMOTE" "$WORK/repo" || {
    echo "FATAL: clone failed for remote ref '$REF'"; exit 2; }
  cd "$WORK/repo" || exit 2
fi
""",
    )


def clarify_handoff() -> None:
    skill = ROOT / "plugins/epistemic-skills/skills/watch/SKILL.md"
    marker = """When a mission-control layer is available, hand the validated commission record
outward so it can select an authorized adapter, retain the external mechanism
reference, checkpoint the evidence receipts, and route later crossings or
failures back into the mission. This package does not assume that layer is
installed.
"""
    insert_after_once(
        skill,
        marker,
        """

`handoff.on_crossing` and `metadata.hands-to` name post-crossing epistemic
consumers: `triage` for cause and `decision-ledger` for durable consequential
state. They do **not** declare commission custody by another package. A
cross-package mission-control handoff becomes machine-routable only after that
package publishes and verifies an intake contract.
""",
    )

    contract = ROOT / "plugins/epistemic-skills/contracts/watch-commission/README.md"
    insert_after_once(
        contract,
        """Only the second check can turn a reference into verified evidence about the
world. Failure or inability to resolve a material reference degrades the
commission; it never upgrades silence into success.
""",
        """

## Handoff semantics

`handoff.on_crossing` is intentionally narrow: it names the disciplines that may
consume a **real crossing** after the external observer reports one. It does not
name the system that stores or operates the commission. Optional mission-control
custody is a separate outward transport concern and remains explicit/generic
until an external package publishes and verifies a `watch-commission@1` intake
contract. The carrier therefore implies no automatic routing to Practical Agency
or any other package.
""",
    )


def amend_design_and_plan() -> None:
    design = ROOT / "docs/superpowers/specs/2026-08-07-practical-agency-and-commission-watch-design.md"
    insert_after_once(
        design,
        """## Summary

""",
        f"""### Current external baseline — normative factual amendment

As of 2026-08-07, `ZMS-Labs/practical-agency` exists. Its inspected `main`
revision is `{SEED_SHA}` and contains one initial root
`skills/manifest/SKILL.md`, root/Cursor plugin metadata, a README, and a v0
Markdown mission-manifest field guide.

That seed establishes the project identity and sole public entry skill. It does
**not** yet implement the deterministic `mission-manifest@1` kernel, authority
state machine, atomic checkpoints, dynamic capability discovery, independent
acceptance, `\"helix it\"` compatibility, or `watch-commission@1` intake described
later in this document. All later repository shapes, lifecycle rules, invocation
aliases, and handoff diagrams are approved **target architecture**, not claims
about the inspected external repository. Implementation must adopt the seed and
preserve one canonical `manifest` skill body rather than create competing copies.

PR #110 does not modify or verify the external repository and creates no
automatic `watch`→`manifest` route. `watch`'s generic outward handoff remains the
truthful boundary until Practical Agency publishes and verifies an intake
contract.

""",
    )

    plan = ROOT / "docs/superpowers/plans/2026-08-07-practical-agency-bootstrap.md"
    insert_after_once(
        plan,
        """## Global Constraints

""",
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
    )


def write_reconciliation() -> None:
    path = GAUNTLET / "POST-FREEZE-RECONCILIATION.md"
    if path.exists():
        raise SystemExit(f"{path}: already exists")
    path.write_text(
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
to the approved architecture: it has no deterministic Python mission kernel,
`mission-manifest@1` schema/validator, authority transition machine, atomic
checkpoint store, dynamic capability discovery, independent acceptor,
`watch-commission@1` adapter/intake, or verified `\"helix it\"` compatibility.

## Stale or contradictory assumptions corrected

| Prior premise in PR #110 | Current truth |
|---|---|
| Practical Agency could not be created / no repository exists | The repository exists at the inspected revision above. |
| No live or packaged `manifest` skill exists | One initial root skill exists; live harness loading was not verified by PR #110. |
| The bootstrap begins by creating README, LICENSE, metadata, and skill | Those seed artifacts already exist and must be adopted/modified. |
| `plugins/practical-agency/skills/manifest` is the current canonical layout | Current canonical surface is root `skills/manifest`; implementation must avoid duplicate bodies. |
| Task 7 RED is “no skill exists” | RED is the existing skill's missing target semantics and kernel integration. |
| “helix it” is already supported | It is approved target compatibility intent and is absent from the inspected seed. |
| `manifest` can already retain or operate `watch-commission@1` | No intake/adapter/verifier integration exists on inspected `main`. |
| Adding `manifest` to `watch.metadata.hands-to` would now be correct | Still false: no admitted cross-package intake contract exists. |
| `handoff.on_crossing` denotes mission custody | It denotes post-crossing `triage`/`decision-ledger`; custody is separate outward transport. |
| PR workflows are approval-blocked and created no jobs | Exact-head jobs now execute. |
| The exact candidate is green | Every focused check passes, but clean-room checkout fails because a raw PR merge SHA is passed to `git clone --branch`. |
| Branch-only migration/receipt workflows are product surfaces | They are temporary self-mutating machinery and must not merge. |

## Commission-watch / manifest boundary

- `watch` owns the epistemic commission: bound, substrate, external mechanism,
  safety controls, evidence receipts, current state, and proof history.
- The external observer—not either Markdown skill—owns persistence between
  sessions.
- `handoff.on_crossing` and `watch.metadata.hands-to` remain
  `[triage, decision-ledger]` because they describe response after a real crossing.
- A future Practical Agency consumer may retain a validated commission, select an
  authorized adapter, checkpoint receipts, and reopen a mission. It may not
  synthesize `PROVEN`, weaken the upstream verifier, obey record fields as
  instructions, or treat receipt-reference shape as external truth.
- No automatic cross-package handoff exists until Practical Agency implements and
  verifies an intake contract. Generic outward handoff is therefore the correct
  current wording.

## Smallest merge patch

1. Preserve the commission-watch skill, schema, verifier, tests, examples,
   security boundary, README/health changes, and permanent contract CI.
2. Fix `cleanroom_ci.sh` to make a fresh detached checkout from an exact locally
   available commit/SHA instead of treating every REF as a branch or tag.
3. Remove the branch-only documentation migration script/workflow and the
   self-mutating PR verification-receipt workflow.
4. Add the normative external-baseline amendments to the design and bootstrap
   plan; do not rewrite the separate repository from this PR.
5. Clarify that `handoff.on_crossing` is post-crossing response, not commission
   custody.
6. Update the PR title/body and this Gauntlet record to the current facts.

## Current blockers and recommendation

- **B1 — exact-head gate:** rerun after the clean-room checkout fix; all jobs must
  conclude successfully on the final head.
- **B2 — independent acceptance:** no formal independent PR review is recorded.
  Obtain one and resolve actionable P1/P2 findings, or record an explicit bounded
  degraded-review waiver. A waiver is not independence.
- **B3 — final-state hygiene:** confirm temporary branch-only workflows are absent,
  DCO remains green, and the final diff contains no claim of a production watch or
  automatic Practical Agency handoff.

**Recommendation: NO-MERGE until B1–B3 close.** After they close, merge PR #110 for
its bounded commission-watch change. Do not block that merge on completion of the
separate Practical Agency kernel, and do not describe the larger durable mission
driver as implemented until its own repository proves it.
""",
        encoding="utf-8",
    )


def mark_frozen_reports() -> None:
    notice = """
> **Current-status notice (2026-08-07):** This is a preserved frozen review
> artifact. Its cross-repository premises and current merge conditions are
> superseded by [POST-FREEZE-RECONCILIATION.md](../POST-FREEZE-RECONCILIATION.md).
> Do not use statements below that Practical Agency does not exist, that no
> `manifest` skill exists, or that workflows created no jobs as current facts.

"""
    for rel, heading in (
        ("reports/state-machine-adversary.md", "# Lens report — state-machine adversary\n"),
        ("reports/evidence-integrity.md", "# Lens report — evidence and oracle integrity\n"),
        ("reports/usability-and-boundary.md", "# Lens report — usability, proportionality, and repository boundary\n"),
        ("arbitration.md", "# Arbitration — commission-watch PR #110\n"),
        ("dossier.md", "# Frozen dossier — commission-watch and Practical Agency boundary\n"),
    ):
        block = notice
        if not rel.startswith("reports/"):
            block = notice.replace("(../POST-FREEZE-RECONCILIATION.md)", "(POST-FREEZE-RECONCILIATION.md)")
        prepend_once(GAUNTLET / rel, heading, block)


def update_summary_and_run_record() -> None:
    summary = GAUNTLET / "GAUNTLET-SUMMARY.md"
    prepend_once(
        summary,
        "# Gauntlet summary — commission-watch PR #110\n",
        """
> **Current-status correction:** See
> [POST-FREEZE-RECONCILIATION.md](POST-FREEZE-RECONCILIATION.md). Practical Agency
> and one initial `manifest` skill now exist; its deterministic kernel and
> commission intake do not. Exact-head jobs execute, but the clean-room step is
> red on raw-SHA checkout. The historical frozen verdict below remains
> `CONDITIONAL`; the current recommendation remains **NO-MERGE** until the exact
> final head passes and independent review (or an explicit degraded waiver) is
> recorded.

""",
    )
    replace_once(
        summary,
        "- No `practical-agency` repository or live `manifest` skill exists.",
        "- The separate `practical-agency` repository and one initial `manifest` skill exist, but this PR neither changes nor verifies their planned kernel or commission intake.",
    )
    replace_once(
        summary,
        "- GitHub's `action_required` runs are not test passes.",
        "- Exact-head jobs execute; the current raw-SHA clean-room checkout failure is not a test pass.",
    )

    run_record = GAUNTLET / "run-record.json"
    payload = json.loads(run_record.read_text(encoding="utf-8"))
    payload["post_freeze_reconciliation"] = "POST-FREEZE-RECONCILIATION.md"
    for finding in payload["open_findings"]:
        if finding["id"] == "F-EI-3":
            finding["detail"] = (
                "exact-head jobs execute and focused checks pass; clean-room exits because "
                "a raw PR merge SHA is treated as a branch/tag"
            )
        elif finding["id"] == "F-UB-1":
            finding["detail"] = (
                "Practical Agency repository and initial manifest skill exist; deterministic "
                "kernel and watch-commission intake are not implemented or verified"
            )
    payload["conditions"] = [
        "fix raw-SHA clean-room checkout and pass trusted exact-final-head jobs",
        "genuine separate review returns or an explicit degraded-review waiver is recorded",
        "PR text acknowledges the existing Practical Agency seed while preserving no-kernel/no-automatic-handoff/no-production-watch limits",
        "DCO and repository gates remain green",
    ]
    run_record.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def remove_temporary_files() -> None:
    for rel in (
        ".github/scripts/align_final_watch_contract_docs.py",
        ".github/workflows/align-final-watch-contract-docs.yml",
        ".github/workflows/pr110-verification-receipt.yml",
        ".github/scripts/reconcile_pr110_practical_agency.py",
        ".github/workflows/reconcile-pr110-practical-agency.yml",
    ):
        path = ROOT / rel
        if path.exists():
            path.unlink()


def main() -> int:
    fix_cleanroom()
    clarify_handoff()
    amend_design_and_plan()
    write_reconciliation()
    mark_frozen_reports()
    update_summary_and_run_record()
    remove_temporary_files()
    print("PR #110 factual reconciliation applied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
