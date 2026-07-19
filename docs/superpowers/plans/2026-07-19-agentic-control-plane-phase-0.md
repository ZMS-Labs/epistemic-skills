# Agentic Control Plane Phase 0 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restore truthful public-core/private-overlay state, produce reproducible drift and capability inventories, and bank the forward-only audit evidence required before creating `ZMS-Labs/agentic-control-plane`.

**Architecture:** Phase 0 adds a small, stdlib-first `scripts/governance/agentic_skills/` verification module and committed evidence artifacts to the private `zms-homelab` repository. It separately adds only historical/classification documentation to the public `epistemic-skills` repository. Public method bodies, installed caches, and the concurrently edited files remain untouched; no new package, repository, materializer, or installation mechanism is created.

**Tech Stack:** Python 3.11+ standard library, pytest, JSON, Markdown, Git worktrees, PowerShell.

## Global Constraints

- Implement only Phase 0 from `docs/superpowers/specs/2026-07-18-agentic-control-plane-design.md`.
- Treat `Y:\dev` checkouts and upstream Git as authoritative. Do not use `H:` or UNC mirrors as sources of truth.
- Create isolated worktrees from committed bases before editing either repository:
  - `Y:\dev\zms-homelab-wt-agentic-phase0` on `codex/agentic-phase0-private`, based on `origin/main`;
  - `Y:\dev\epistemic-skills-wt-agentic-phase0` on `codex/agentic-phase0-public`, based on the commit containing this plan.
- Do not modify, stage, or absorb these existing `epistemic-skills` paths:
  - `plugins/epistemic-skills/skills/evidence-research/SKILL.md`;
  - `plugins/epistemic-skills/skills/gauntlet/runs/ledger.jsonl`;
  - `.cursor/`;
  - `outputs/`.
- Do not modify the existing dirty `Y:\dev\zms-homelab` checkout or the existing `Y:\dev\zms-homelab-wt-skill-overlay` worktree.
- Do not overwrite or delete any divergent private `SKILL.md`. The drift inventory is evidence only.
- Use newline-normalized SHA-256 (`CRLF` and lone `CR` converted to `LF`; no whitespace trimming) for cross-platform comparisons.
- Record unavailable facts as `null`, `unverified`, `not-installed`, `license-pending`, or `pilot-candidate`. Never infer an immutable pin or verified state from a directory name alone.
- Re-check branch, status, remote, and the protected-path fingerprints before every commit.
- Make exactly scoped commits. Do not push unless the operator separately asks.

---

## Task 1: Create isolated worktrees and freeze protected-path evidence

**Required sub-skill:** `superpowers:using-git-worktrees`.

**Files:**

- Create: `Y:\dev\epistemic-skills-wt-agentic-phase0\docs\superpowers\plans\2026-07-19-agentic-control-plane-phase-0.md` (inherited through the worktree base)
- Create: `Y:\dev\zms-homelab-wt-agentic-phase0\` (Git worktree only; no repository file yet)
- Verify only: the four protected `epistemic-skills` paths listed in Global Constraints

- [ ] **Step 1: Verify both authoritative repositories before creating worktrees**

Run:

```powershell
git -C Y:\dev\epistemic-skills status --short
git -C Y:\dev\epistemic-skills branch --show-current
git -C Y:\dev\epistemic-skills remote -v
git -C Y:\dev\epistemic-skills rev-parse HEAD
git -C Y:\dev\zms-homelab status --short
git -C Y:\dev\zms-homelab branch --show-current
git -C Y:\dev\zms-homelab remote -v
git -C Y:\dev\zms-homelab rev-parse origin/main
```

Expected: the public checkout still reports the protected dirty paths; the private checkout may contain unrelated work; both origins point to their ZMS-Labs GitHub repositories.

- [ ] **Step 2: Capture protected-path hashes without staging anything**

Run from `Y:\dev\epistemic-skills`:

```powershell
git diff -- plugins/epistemic-skills/skills/evidence-research/SKILL.md plugins/epistemic-skills/skills/gauntlet/runs/ledger.jsonl | git hash-object --stdin
git ls-files --others --exclude-standard .cursor outputs | Sort-Object | ForEach-Object { $p = Join-Path (Get-Location) $_; "$_ $(Get-FileHash -Algorithm SHA256 -LiteralPath $p | Select-Object -ExpandProperty Hash)" } | git hash-object --stdin
```

Record the two resulting hashes in the execution notes. Expected: two 40-character Git object IDs. These are comparison evidence, not files to commit.

- [ ] **Step 3: Create clean worktrees**

Run:

```powershell
git -C Y:\dev\zms-homelab fetch origin
git -C Y:\dev\zms-homelab worktree add -b codex/agentic-phase0-private Y:\dev\zms-homelab-wt-agentic-phase0 origin/main
git -C Y:\dev\epistemic-skills worktree add -b codex/agentic-phase0-public Y:\dev\epistemic-skills-wt-agentic-phase0 HEAD
```

Expected: both new worktrees are clean; the original dirty checkouts are unchanged.

- [ ] **Step 4: Verify worktree isolation**

Run:

```powershell
git -C Y:\dev\zms-homelab-wt-agentic-phase0 status --short
git -C Y:\dev\epistemic-skills-wt-agentic-phase0 status --short
git -C Y:\dev\zms-homelab worktree list
git -C Y:\dev\epistemic-skills worktree list
```

Expected: both new worktrees have empty short status and appear on the named `codex/` branches.

## Task 2: Build the copied-core inventory with tests first

**Files:**

- Create: `Y:\dev\zms-homelab-wt-agentic-phase0\scripts\governance\agentic_skills\__init__.py`
- Create: `Y:\dev\zms-homelab-wt-agentic-phase0\scripts\governance\agentic_skills\inventory.py`
- Create: `Y:\dev\zms-homelab-wt-agentic-phase0\scripts\governance\agentic_skills\tests\__init__.py`
- Create: `Y:\dev\zms-homelab-wt-agentic-phase0\scripts\governance\agentic_skills\tests\conftest.py`
- Create: `Y:\dev\zms-homelab-wt-agentic-phase0\scripts\governance\agentic_skills\tests\test_inventory.py`
- Create: `Y:\dev\zms-homelab-wt-agentic-phase0\docs\governance\agentic-skills\skill-core-inventory.json`

- [ ] **Step 1: Write failing normalization and discovery tests**

`test_inventory.py` must cover:

```python
def test_normalized_sha256_treats_crlf_and_lf_as_equal(): ...
def test_normalized_sha256_does_not_trim_other_whitespace(): ...
def test_discovery_emits_one_row_per_private_skill_core(): ...
def test_divergence_is_reported_without_modifying_either_file(): ...
def test_missing_public_counterpart_is_explicit(): ...
def test_local_overlay_and_installed_copy_are_recorded_when_present(): ...
def test_check_mode_fails_when_committed_inventory_is_stale(): ...
```

Fixtures must create temporary public/private/installed roots, including one equal core, one CRLF-only variant, one genuinely divergent core, one missing public counterpart, and one `LOCAL.md`.

- [ ] **Step 2: Run the focused test and confirm RED**

Run:

```powershell
python -m pytest scripts/governance/agentic_skills/tests/test_inventory.py -q
```

Expected: collection or import failure because `inventory.py` does not exist yet.

- [ ] **Step 3: Implement the smallest inventory module**

`inventory.py` must expose:

```python
def normalize_newlines(data: bytes) -> bytes: ...
def normalized_sha256(path: Path) -> str: ...
def discover_private_cores(private_root: Path) -> list[Path]: ...
def build_inventory(
    public_root: Path,
    private_root: Path,
    public_ref: str,
    private_ref: str,
    observed_at: str,
    installed_roots: dict[str, Path],
) -> dict: ...
def validate_inventory(payload: dict) -> list[str]: ...
def main(argv: list[str] | None = None) -> int: ...
```

The CLI must support:

```text
--public-root PATH
--private-root PATH
--public-ref REF
--private-ref REF
--observed-at ISO8601
--installed-root HARNESS=PATH   (repeatable)
--out PATH
--check PATH
```

The JSON schema shape must be:

```json
{
  "schema_version": "1.0",
  "observed_at": "ISO-8601 UTC",
  "normalization": "CRLF and CR to LF; no other trimming",
  "public_repo": {"url": "https://github.com/ZMS-Labs/epistemic-skills.git", "ref": "immutable commit"},
  "private_repo": {"url": "https://github.com/ZMS-Labs/zms-homelab.git", "ref": "immutable commit"},
  "skills": [
    {
      "skill_id": "gauntlet",
      "public_source": "plugins/epistemic-skills/skills/gauntlet/SKILL.md",
      "public_ref": "immutable commit",
      "public_normalized_sha256": "64 lowercase hex",
      "private_path": "skills/gauntlet/SKILL.md",
      "private_normalized_sha256": "64 lowercase hex",
      "equality": "equal | different | missing-public",
      "overlay_path": "skills/gauntlet/LOCAL.md | null",
      "installed_copies": []
    }
  ]
}
```

Installed-copy rows must record `harness`, `path`, `revision` when observable, normalized hash, and equality to the public core. Directory names may be recorded as observations but must not be promoted to immutable revisions.

- [ ] **Step 4: Run the focused tests and confirm GREEN**

Run:

```powershell
python -m pytest scripts/governance/agentic_skills/tests/test_inventory.py -q
```

Expected: all inventory tests pass.

- [ ] **Step 5: Generate the real inventory from clean committed sources**

Use the clean public worktree as the public source and the clean private worktree as the private source. Capture immutable refs first:

```powershell
$publicRef = git -C Y:\dev\epistemic-skills-wt-agentic-phase0 rev-parse HEAD
$privateRef = git -C Y:\dev\zms-homelab-wt-agentic-phase0 rev-parse HEAD
$observedAt = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
python scripts/governance/agentic_skills/inventory.py --public-root Y:\dev\epistemic-skills-wt-agentic-phase0 --private-root . --public-ref $publicRef --private-ref $privateRef --observed-at $observedAt --installed-root codex=C:\Users\zachs\.codex\plugins\cache\epistemic-skills\epistemic-skills\2.3.1\skills --out docs/governance/agentic-skills/skill-core-inventory.json
```

Expected: every `skills/*/SKILL.md` in the private worktree has exactly one row; `evidence-research` is visibly `different`; no source file changes.

- [ ] **Step 6: Prove deterministic check mode**

Run the same command with the same captured variables and replace `--out ...` with:

```powershell
--check docs/governance/agentic-skills/skill-core-inventory.json
```

Expected: exit 0 and `inventory current`.

- [ ] **Step 7: Commit only the inventory module, tests, and generated inventory**

Run:

```powershell
git status --short
git add scripts/governance/agentic_skills/__init__.py scripts/governance/agentic_skills/inventory.py scripts/governance/agentic_skills/tests/__init__.py scripts/governance/agentic_skills/tests/conftest.py scripts/governance/agentic_skills/tests/test_inventory.py docs/governance/agentic-skills/skill-core-inventory.json
git diff --cached --check
git commit -m "governance: inventory agentic skill core drift"
```

Expected: one private-repository commit containing no `skills/*/SKILL.md` changes.

## Task 3: Make the issue-164 guard executable and correct the stale overlay

**Files:**

- Create: `Y:\dev\zms-homelab-wt-agentic-phase0\scripts\governance\agentic_skills\gauntlet_guard.py`
- Create: `Y:\dev\zms-homelab-wt-agentic-phase0\scripts\governance\agentic_skills\tests\test_gauntlet_guard.py`
- Modify: `Y:\dev\zms-homelab-wt-agentic-phase0\skills\gauntlet\LOCAL.md`

- [ ] **Step 1: Write failing behavioral guard tests**

First capture the authoritative issue state:

```powershell
gh issue view 164 --repo ZMS-Labs/zms-homelab --json state,closedAt,url,title
```

Expected: `state` is `CLOSED` and `closedAt` is non-null. Record this output as
the source for the overlay correction and final verification report.

`test_gauntlet_guard.py` must create a temporary installed Gauntlet tree and cover:

```python
def test_binary_tag_downgrades_to_h(): ...
def test_text_tag_remains_v(): ...
def test_missing_path_downgrades_to_h(): ...
def test_regression_function_is_present_in_installed_test_runner(): ...
def test_guard_fails_when_binary_control_is_removed(): ...
```

The tests must exercise the installed tree's `scripts/verify_evidence.py` via `importlib`, not merely grep for prose. The coverage assertion must also confirm `tests/run_tests.py` contains and invokes `test_verify_evidence_fails_closed_on_binary`.

- [ ] **Step 2: Run the focused test and confirm RED**

Run:

```powershell
python -m pytest scripts/governance/agentic_skills/tests/test_gauntlet_guard.py -q
```

Expected: import failure because `gauntlet_guard.py` is absent.

- [ ] **Step 3: Implement the guard checker**

`gauntlet_guard.py` must expose:

```python
def verify_binary_guard(skill_root: Path) -> dict: ...
def main(argv: list[str] | None = None) -> int: ...
```

The checker must:

1. load `scripts/verify_evidence.py` from the supplied skill root;
2. create a compiled `.pyc`, a two-line UTF-8 text file, and a missing path in a temporary directory;
3. require binary → `H` with a binary reason, text → `V`, missing → `H`;
4. require the installed `tests/run_tests.py` to define and call the named F13 regression;
5. emit JSON with individual controls and return non-zero if any control fails.

CLI:

```text
python scripts/governance/agentic_skills/gauntlet_guard.py --skill-root PATH --json
```

- [ ] **Step 4: Run tests and the checker against the private installed copy**

Run:

```powershell
python -m pytest scripts/governance/agentic_skills/tests/test_gauntlet_guard.py -q
python scripts/governance/agentic_skills/gauntlet_guard.py --skill-root skills/gauntlet --json
python skills/gauntlet/tests/run_tests.py
```

Expected: all controls pass; the full Gauntlet test runner ends with `ALL PASS`.

- [ ] **Step 5: Replace stale issue-164 overlay language**

In `skills/gauntlet/LOCAL.md`, replace the `Known protocol defect (open — issue #164)` section with a resolved-state section that states:

- issue `#164` is closed and the F13 regression shipped;
- binary evidence must use a binary-aware oracle;
- unreadable, missing, or text-inappropriate evidence fails closed;
- the rule is current protocol, not a temporary workaround;
- the executable check command is `python scripts/governance/agentic_skills/gauntlet_guard.py --skill-root skills/gauntlet --json`.

Do not edit `skills/gauntlet/SKILL.md`, its scripts, or its test runner.

- [ ] **Step 6: Prove the stale claim is gone and commit**

Run:

```powershell
rg -n "Known protocol defect|open — issue #164|Until #164 lands" skills/gauntlet/LOCAL.md
python -m pytest scripts/governance/agentic_skills/tests/test_gauntlet_guard.py -q
python scripts/governance/agentic_skills/gauntlet_guard.py --skill-root skills/gauntlet --json
git status --short
git add scripts/governance/agentic_skills/gauntlet_guard.py scripts/governance/agentic_skills/tests/test_gauntlet_guard.py skills/gauntlet/LOCAL.md
git diff --cached --check
git commit -m "fix: mark gauntlet binary guard resolved"
```

Expected: `rg` returns no matches; tests and checker pass; commit contains exactly the three named files.

## Task 4: Create and validate the first capability inventory

**Files:**

- Create: `Y:\dev\zms-homelab-wt-agentic-phase0\scripts\governance\agentic_skills\capabilities.py`
- Create: `Y:\dev\zms-homelab-wt-agentic-phase0\scripts\governance\agentic_skills\tests\test_capabilities.py`
- Create: `Y:\dev\zms-homelab-wt-agentic-phase0\docs\governance\agentic-skills\capability-inventory.json`

- [ ] **Step 1: Write failing schema and honesty tests**

`test_capabilities.py` must cover:

```python
def test_all_eight_required_upstreams_are_required(): ...
def test_missing_required_upstream_fails(): ...
def test_pending_upstream_with_null_ref_is_valid(): ...
def test_pinned_requires_immutable_ref_and_evidence(): ...
def test_verified_requires_evidence_and_observed_timestamp(): ...
def test_scope_and_state_enums_reject_unknown_values(): ...
def test_every_entry_has_ownership_visibility_license_and_installation(): ...
```

The required upstream IDs are:

```python
{
    "obra/superpowers",
    "pro-vi/loopgen",
    "ralph/selected-implementations",
    "gastownhall/beads",
    "trailofbits/skills",
    "vercel-labs/agent-skills",
    "prime-radiant-inc/superpowers-evals",
    "prime-radiant-inc/gauntlet",
}
```

- [ ] **Step 2: Run the focused test and confirm RED**

Run:

```powershell
python -m pytest scripts/governance/agentic_skills/tests/test_capabilities.py -q
```

Expected: import failure because `capabilities.py` is absent.

- [ ] **Step 3: Implement the validator**

`capabilities.py` must expose:

```python
REQUIRED_UPSTREAMS: frozenset[str]
def validate_capability_inventory(payload: dict) -> list[str]: ...
def main(argv: list[str] | None = None) -> int: ...
```

Allowed values:

- ownership: `zms-owned`, `upstream`, `private-project`;
- visibility: `public`, `private`;
- scope: `global`, `explicit`, `project`, `fleet-only`;
- state: `verified`, `pending`, `degraded`, `conflicting`, `not-installed`, `license-pending`, `pilot-candidate`, `unverified`;
- installation mechanism: `codex-plugin`, `claude-plugin`, `cursor-rule`, `project-copy`, `manual`, `none`, `unknown`.

The validator must reject `pinned` or `verified` claims unless an immutable commit/tag and at least one evidence reference are present. A Ralph family entry may list candidate repositories while keeping `source.ref` null and state `unverified`.

- [ ] **Step 4: Populate the inventory from observed state only**

Create `docs/governance/agentic-skills/capability-inventory.json` with:

- all six ZMS-owned public epistemic skills;
- the private homelab overlay layer;
- every currently observable harness materialization;
- all eight required upstream entries;
- source URL/ref, ownership, visibility, license status, scope, installation mechanism, overlay source, current state, evidence references, and one UTC observation timestamp per row.

For sources not inspected during execution, use honest pending states. Specifically, the Ralph family record must not select an implementation by implication, and neither `superpowers-evals` nor upstream `gauntlet` may be called admitted merely because they are named in the design.

- [ ] **Step 5: Validate and commit**

Run:

```powershell
python -m pytest scripts/governance/agentic_skills/tests/test_capabilities.py -q
python scripts/governance/agentic_skills/capabilities.py docs/governance/agentic-skills/capability-inventory.json
git status --short
git add scripts/governance/agentic_skills/capabilities.py scripts/governance/agentic_skills/tests/test_capabilities.py docs/governance/agentic-skills/capability-inventory.json
git diff --cached --check
git commit -m "governance: record initial agentic capability inventory"
```

Expected: validator prints `capability inventory valid`; commit contains exactly the three named files.

## Task 5: Classify commit 5f8a190 and mark the handoff historical

**Files:**

- Create: `Y:\dev\epistemic-skills-wt-agentic-phase0\docs\superpowers\specs\2026-07-19-5f8a190-forward-classification.md`
- Modify: `Y:\dev\epistemic-skills-wt-agentic-phase0\docs\superpowers\specs\2026-07-18-SESSION-HANDOFF.md`
- Verify only: `Y:\dev\epistemic-skills-wt-agentic-phase0\plugins\epistemic-skills\skills\evidence-research\SKILL.md`

- [ ] **Step 1: Capture the exact commit surface**

Run:

```powershell
git show --format=fuller --name-status 5f8a190
git diff 5f8a190^ 5f8a190 -- README.md docs/superpowers/specs/2026-07-17-epistemic-skills-plugin-design.md docs/superpowers/specs/2026-07-18-agentic-skills-packaging-architecture.md plugins/epistemic-skills/skills/evidence-research/SKILL.md plugins/epistemic-skills/skills/evidence-research/reference/zotero-first-contact.md plugins/epistemic-skills/skills/using-epistemic-skills/SKILL.md
```

Expected: exactly six changed paths: three modified/added docs, `evidence-research/SKILL.md`, its Zotero reference, and the router.

- [ ] **Step 2: Write the forward-only classification report**

The report must include:

- immutable commit ID and review date;
- one row for every changed path and, where a file contains mixed concerns, one row per coherent change hunk;
- exactly one classification per row:
  - `retained generic protocol`;
  - `public integration reference`;
  - `private overlay/policy`;
  - `harness adapter detail`;
  - `accidental or unsupported behavior requiring focused follow-up`;
- evidence line/range or commit-diff reference;
- disposition: retain, relocate later, defer pending owner reconciliation, or focused follow-up;
- an explicit statement that history is not rewritten and the concurrently edited `evidence-research/SKILL.md` is not changed in Phase 0.

Do not turn the report into a new architecture proposal.

- [ ] **Step 3: Mark the pre-reboot handoff historical without rewriting it**

Add a short note immediately after the handoff title stating:

- it is a historical pre-reboot snapshot;
- its pause/unpushed statements describe the state at capture time;
- commits `5f8a190`, `95c4881`, and `395ab0b` were subsequently pushed to `origin/main`;
- the original record below is intentionally preserved.

Do not revise the original narrative line by line.

- [ ] **Step 4: Prove the protected method body is untouched and commit**

Run:

```powershell
git diff -- plugins/epistemic-skills/skills/evidence-research/SKILL.md
git status --short
git add docs/superpowers/specs/2026-07-19-5f8a190-forward-classification.md docs/superpowers/specs/2026-07-18-SESSION-HANDOFF.md
git diff --cached --check
git commit -m "docs: classify phase-zero packaging drift"
```

Expected: the first command is empty; commit contains exactly the two documentation files.

## Task 6: Bank the Phase 0 verification record

**Files:**

- Create: `Y:\dev\zms-homelab-wt-agentic-phase0\docs\reports\2026-07-19-agentic-control-plane-phase-0.md`
- Modify only if generated content changed: `Y:\dev\zms-homelab-wt-agentic-phase0\docs\governance\agentic-skills\skill-core-inventory.json`

- [ ] **Step 1: Run the complete private verification suite**

Run from the private worktree:

```powershell
python -m pytest scripts/governance/agentic_skills/tests -q
python scripts/governance/agentic_skills/gauntlet_guard.py --skill-root skills/gauntlet --json
python skills/gauntlet/tests/run_tests.py
python scripts/governance/agentic_skills/capabilities.py docs/governance/agentic-skills/capability-inventory.json
```

Expected: pytest passes; guard JSON reports all controls true; Gauntlet ends `ALL PASS`; capability validator passes.

- [ ] **Step 2: Re-run copied-core inventory check**

Use the exact `publicRef`, `privateRef`, `observedAt`, and installed-root values recorded when the inventory was generated:

```powershell
python scripts/governance/agentic_skills/inventory.py --public-root Y:\dev\epistemic-skills-wt-agentic-phase0 --private-root . --public-ref $publicRef --private-ref $privateRef --observed-at $observedAt --installed-root codex=C:\Users\zachs\.codex\plugins\cache\epistemic-skills\epistemic-skills\2.3.1\skills --check docs/governance/agentic-skills/skill-core-inventory.json
```

Expected: exit 0 and `inventory current`. If private commits changed only non-core files, `private_ref` is observation metadata and must remain the originally captured core-source ref rather than forcing a meaningless inventory rewrite.

- [ ] **Step 3: Write the durable verification report**

The report must record:

- both repository branches, HEADs, and origins;
- issue `#164` closed-state evidence and the behavioral guard result;
- copied-core inventory row count and equality-state counts;
- the explicit `evidence-research` divergence result;
- all eight upstream capability IDs and current honest states;
- the public classification-report path and historical-handoff path;
- every verification command, exit code, and concise result;
- the protected-path before/after hashes from Task 1;
- explicit non-goals: no new repository, no install, no copied core reconciliation, no pushed-history rewrite.

- [ ] **Step 4: Recompute protected-path hashes in the original public checkout**

Run from `Y:\dev\epistemic-skills` using the exact Task 1 commands.

Expected: both hashes match Task 1. If they do not, stop; do not stage or commit anything until the concurrent owner change is understood.

- [ ] **Step 5: Run final diff and placeholder checks**

Run:

```powershell
rg -n "TODO|TBD|PLACEHOLDER|<fill|CHANGEME" scripts/governance/agentic_skills docs/governance/agentic-skills docs/reports/2026-07-19-agentic-control-plane-phase-0.md
git diff --check
git status --short
```

Expected: placeholder search returns no matches; diff check passes; only the verification report is uncommitted.

- [ ] **Step 6: Commit the verification record**

Run:

```powershell
git add docs/reports/2026-07-19-agentic-control-plane-phase-0.md
git diff --cached --check
git commit -m "docs: record agentic phase-zero verification"
```

Expected: one documentation-only commit.

## Task 7: Final acceptance audit and handoff

**Required sub-skill:** `superpowers:verification-before-completion`.

**Files:**

- Verify: all files created or modified in Tasks 2–6
- Verify only: original dirty checkouts and protected paths

- [ ] **Step 1: Verify clean implementation worktrees and scoped commit history**

Run:

```powershell
git -C Y:\dev\zms-homelab-wt-agentic-phase0 status --short
git -C Y:\dev\zms-homelab-wt-agentic-phase0 log --oneline origin/main..HEAD
git -C Y:\dev\epistemic-skills-wt-agentic-phase0 status --short
git -C Y:\dev\epistemic-skills-wt-agentic-phase0 log --oneline main..HEAD
```

Expected: both worktrees are clean; private history contains the inventory, guard, capability, and verification commits; public history contains the classification/handoff commit only.

- [ ] **Step 2: Verify all ten design acceptance criteria explicitly**

Check:

1. overlay calls issue `#164` resolved;
2. behavioral binary guard can fail and passes on the installed copy;
3. every discovered private core has one inventory row;
4. `evidence-research` divergence remains visible and untouched;
5. every path/hunk from `5f8a190` is durably classified;
6. handoff is marked historical;
7. capability inventory adds no installation mechanism;
8. all eight upstream entries exist without unsupported pin/verification claims;
9. protected path hashes match;
10. commands and results appear in the private verification report.

- [ ] **Step 3: Report repository state without pushing**

Report separately:

- private worktree branch and local commits;
- public worktree branch and local commit;
- original dirty checkout state;
- pushed state (`not pushed`, unless separately authorized later).

Do not create `agentic-control-plane`, install upstream packages, reconcile divergent cores, merge branches, or remove worktrees in this task.
