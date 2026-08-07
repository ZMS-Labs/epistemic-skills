# Practical Agency Bootstrap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create `ZMS-Labs/practical-agency`, a portable mission-control project whose sole public skill `manifest` carries operator-authorized intent through durable, coordinated, resumable action without self-certifying completion.

**Architecture:** A stdlib-first deterministic mission kernel owns authority, state transitions, capability discovery, invocation records, and atomic checkpoints. The `manifest` skill is a concise explicit-entry instruction surface over that kernel. External execution, schedulers, monitoring, and model-specific behavior are adapters; epistemic judgments remain in their originating packages.

**Tech Stack:** Python 3.12 standard library, JSON/JSONL, Markdown Agent Skill, JSON Schema draft 2020-12, GitHub Actions, `unittest`.

## Global Constraints

### Existing-seed amendment — normative over absence assumptions below

`ZMS-Labs/practical-agency` already exists at inspected `main` revision
`e244d534a6e26bc9a352846a25ffce18b8d93a53` with `README.md`, `LICENSE`, `plugin.json`,
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
  mission-kernel, checkpoint, independent-acceptance, `"helix it"`, and
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

- Project/repository: **Practical Agency** / `practical-agency`.
- Sole v1 public skill: **`manifest`**.
- Do not create public skills for resume, checkpoint, reconcile, dispatch, commission, or close; those are internal mission operations.
- Preserve operator-authored instructions and amendments verbatim and append-only.
- The operator owns ends, permissions, protected state, acceptable costs, and revocation.
- `manifest` may coordinate capabilities but may not copy a hand-maintained inventory or static stage-to-skill table.
- Material completion requires an independent acceptor declared by the mission contract.
- No runtime, scheduler, or persistence claim without an external durable receipt.
- No production execution adapter in v1 may run arbitrary shell commands by default.
- Stdlib-only deterministic core; adapter dependencies remain optional and isolated.
- All state mutations are atomic, revisioned, and crash-recoverable.
- Every production behavior change follows RED → GREEN → REFACTOR.
- Every commit carries `Signed-off-by: SternOne <89846440+SternOne@users.noreply.github.com>`.
- Public content must not expose private repository names, local absolute paths, credentials, hostnames, or estate topology.

---

## Initial repository structure

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

---

### Task 1: Create the repository and fail-closed CI shell

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

- [ ] **Step 2: Add the first-screen README**

Use this opening exactly:

```markdown
# Practical Agency

Practical Agency is human-authorized mission control for carrying intent through
durable, coordinated, resumable action.

Its sole public entry skill is `manifest`.

Practical Agency does not give an artificial agent independent ends. It extends
the operator's agency through bounded delegation: the operator owns the purpose,
authority, protected state, acceptable costs, and right to interrupt; the system
preserves those constraints while coordinating workflow, epistemic discipline,
execution substrates, continuity, and independent proof.
```

Add a status section stating that v0.1 is a deterministic mission kernel and portable skill, not a daemon, hosted service, or autonomous background actor.

- [ ] **Step 3: Add project metadata**

`pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=75"]
build-backend = "setuptools.build_meta"

[project]
name = "zms-practical-agency"
version = "0.1.0"
description = "Human-authorized mission control for durable agentic work"
readme = "README.md"
requires-python = ">=3.12"
license = { text = "GPL-3.0-or-later" }
authors = [{ name = "ZMS Labs" }]
dependencies = []

[tool.setuptools.packages.find]
include = ["practical_agency*"]
```

Use distribution name `zms-practical-agency` to avoid claiming an unscoped package name. The repository and project remain `practical-agency`.

- [ ] **Step 4: Add the minimal test command**

Create `practical_agency/__init__.py`:

```python
"""Practical Agency deterministic mission-control kernel."""

__version__ = "0.1.0"
```

Run:

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
python -m compileall -q practical_agency tests
```

Expected: zero tests discovered, compile succeeds.

- [ ] **Step 5: Add fail-closed CI**

`.github/workflows/ci.yml` runs on pull requests, pushes to `main`, and manual dispatch. It must:

1. check out without persisted credentials;
2. install Python 3.12;
3. run `python -m unittest discover -s tests -p 'test_*.py' -v`;
4. run `python -m compileall -q practical_agency tests`;
5. parse every committed `.json` file with stdlib;
6. ensure exactly one `plugins/practical-agency/skills/*/SKILL.md` exists once Task 6 lands;
7. run the DCO checker on pull requests.

Copy the author-matching DCO semantics from `epistemic-skills`; do not weaken them.

- [ ] **Step 6: Commit**

```bash
git add .
git commit -m "chore: bootstrap practical-agency repository

Signed-off-by: SternOne <89846440+SternOne@users.noreply.github.com>"
```

---

### Task 2: Define `mission-manifest@1` with tests first

**Files:**
- Create: `tests/test_manifest_model.py`
- Create: `practical_agency/manifest_model.py`
- Create: `practical_agency/validation.py`
- Create: `contracts/mission-manifest.schema.json`
- Create: `examples/minimal-mission.json`

**Interfaces:**
- Consumes: operator-authorized mission fields.
- Produces: `MissionManifest`, `MissionStatus`, `validate_manifest_dict()`, `load_manifest()`, and canonical JSON serialization.

- [ ] **Step 1: Write the failing model tests**

Create `tests/test_manifest_model.py`:

```python
from __future__ import annotations

import json
import unittest
from pathlib import Path

from practical_agency.manifest_model import MissionManifest, MissionStatus
from practical_agency.validation import validate_manifest_dict


class MissionManifestTests(unittest.TestCase):
    def minimal_payload(self) -> dict[str, object]:
        return {
            "schema": "mission-manifest@1",
            "mission_id": "mission-001",
            "revision": 1,
            "authority": {
                "operator_ref": "operator:test",
                "instruction": "Create and verify the example artifact.",
                "amendments": [],
                "permissions": ["repository:write"],
                "protected_state": ["unrelated files"],
                "acceptable_costs": ["one feature branch"],
                "escalation_required_for": ["destructive action"],
                "revoked": False,
                "revocation_reason": None,
            },
            "outcome": {
                "desired_state": "The example artifact exists and validates.",
                "completion_proof": ["validator passes"],
                "integrity_guards": ["runtime reads the canonical artifact"],
                "scope_proof": ["diff contains only intended files"],
                "stop_conditions": ["operator revokes authority"],
            },
            "truth": {
                "subject_refs": ["repo:example@rev-1"],
                "verified_facts": [],
                "assumptions": [],
                "contradictions": [],
                "unknowns": [],
            },
            "state": {
                "status": "draft",
                "completed_actions": [],
                "current_frontier": ["obtain approval"],
                "blockers": [],
                "next_action": "obtain approval",
            },
            "capabilities": {
                "discovered_at": None,
                "available": [],
                "invoked": [],
                "unavailable": [],
                "degraded": [],
            },
            "continuity": {
                "prior_checkpoint": None,
                "durable_artifacts": [],
                "decisions": [],
                "external_handoffs": [],
                "watch_commissions": [],
            },
            "integrity": {
                "actor_may_self_accept": False,
                "required_gates": [],
                "unresolved_verdicts": [],
                "completion_acceptor": None,
            },
        }

    def test_minimal_manifest_is_valid(self) -> None:
        self.assertEqual(validate_manifest_dict(self.minimal_payload()), [])

    def test_operator_instruction_round_trips_verbatim(self) -> None:
        payload = self.minimal_payload()
        payload["authority"]["instruction"] = "Keep  two spaces\nand this newline."
        manifest = MissionManifest.from_dict(payload)
        encoded = manifest.to_canonical_json()
        decoded = json.loads(encoded)
        self.assertEqual(decoded["authority"]["instruction"], payload["authority"]["instruction"])

    def test_self_acceptance_is_rejected(self) -> None:
        payload = self.minimal_payload()
        payload["integrity"]["actor_may_self_accept"] = True
        errors = validate_manifest_dict(payload)
        self.assertTrue(any(error.startswith("SELF_ACCEPTANCE_FORBIDDEN:") for error in errors))

    def test_revision_must_be_positive(self) -> None:
        payload = self.minimal_payload()
        payload["revision"] = 0
        errors = validate_manifest_dict(payload)
        self.assertTrue(any(error.startswith("INVALID_REVISION:") for error in errors))

    def test_status_enum_is_closed(self) -> None:
        payload = self.minimal_payload()
        payload["state"]["status"] = "mostly-done"
        errors = validate_manifest_dict(payload)
        self.assertTrue(any(error.startswith("INVALID_STATUS:") for error in errors))

    def test_example_file_is_valid(self) -> None:
        path = Path(__file__).parents[1] / "examples" / "minimal-mission.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(validate_manifest_dict(payload), [])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run RED**

```bash
python -m unittest tests.test_manifest_model -v
```

Expected: import failure because `manifest_model` and `validation` do not exist.

- [ ] **Step 3: Implement the dataclasses and enums**

In `manifest_model.py`, define:

```python
class MissionStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    BLOCKED = "blocked"
    VERIFYING = "verifying"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

@dataclass(frozen=True, slots=True)
class MissionManifest:
    schema: str
    mission_id: str
    revision: int
    authority: dict[str, Any]
    outcome: dict[str, Any]
    truth: dict[str, Any]
    state: dict[str, Any]
    capabilities: dict[str, Any]
    continuity: dict[str, Any]
    integrity: dict[str, Any]

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "MissionManifest": ...
    def to_dict(self) -> dict[str, Any]: ...
    def to_canonical_json(self) -> str: ...
```

Canonical JSON uses:

```python
json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
```

Deep-copy nested mappings/lists on ingress and egress so callers cannot mutate frozen state through an alias.

- [ ] **Step 4: Implement semantic validation**

`validate_manifest_dict(payload) -> list[str]` checks:

- exact schema;
- stable non-empty mission id;
- positive integer revision, excluding booleans;
- exact top-level objects;
- closed status enum;
- non-empty operator ref, instruction, desired state, and proof arrays;
- `actor_may_self_accept` is exactly false;
- completed requires a completion acceptor and no unresolved verdicts;
- revoked authority permits only cancelled or blocked state;
- active/verifying/completed require a non-null prior checkpoint after revision 1; and
- unknown keys are rejected at every governed object level.

Use named error prefixes; never return booleans alone.

- [ ] **Step 5: Add the JSON Schema and example**

The schema structurally mirrors the validator and uses `additionalProperties: false`. The Python validator remains the semantic oracle for cross-field rules.

Write `examples/minimal-mission.json` from the test fixture.

- [ ] **Step 6: Run GREEN**

```bash
python -m unittest tests.test_manifest_model -v
python -m compileall -q practical_agency tests
```

Expected: all pass.

- [ ] **Step 7: Commit**

```bash
git add contracts/mission-manifest.schema.json examples/minimal-mission.json \
        practical_agency/manifest_model.py practical_agency/validation.py \
        tests/test_manifest_model.py
git commit -m "feat: define the mission manifest contract

Signed-off-by: SternOne <89846440+SternOne@users.noreply.github.com>"
```

---

### Task 3: Implement authority-preserving state transitions

**Files:**
- Create: `tests/test_state_machine.py`
- Create: `tests/test_authority.py`
- Create: `practical_agency/state_machine.py`
- Create: `practical_agency/authority.py`
- Create: `contracts/mission-event.schema.json`

**Interfaces:**
- Consumes: `MissionManifest` plus an authorized `MissionEvent`.
- Produces: `apply_event(manifest, event) -> MissionManifest` with revision +1 or a named `TransitionError`.

- [ ] **Step 1: Write failing transition tests**

Test all legal transitions from the design and these refusals:

```python
with self.assertRaisesRegex(TransitionError, "INDEPENDENT_ACCEPTANCE_REQUIRED"):
    apply_event(active_manifest, MissionEvent(kind="complete", actor_ref="mission-steward", ...))

with self.assertRaisesRegex(TransitionError, "AUTHORITY_REVOKED"):
    apply_event(revoked_manifest, MissionEvent(kind="dispatch", ...))

with self.assertRaisesRegex(TransitionError, "PROTECTED_STATE_VIOLATION"):
    authorize_action(manifest, requested_effects=["unrelated files"])
```

Also assert that operator instruction is byte-for-byte identical after every transition and amendments append rather than replace.

- [ ] **Step 2: Run RED**

```bash
python -m unittest tests.test_state_machine tests.test_authority -v
```

Expected: import failures.

- [ ] **Step 3: Implement `MissionEvent` and closed transition table**

Define events:

```text
approve
pause
resume
block
unblock
begin_verification
accept
reject
revoke
cancel
record_action
record_observation
amend_authority
```

Do not expose arbitrary status assignment. `accept` requires:

- current status `verifying`;
- actor ref equals `integrity.completion_acceptor`;
- actor ref is not the mission steward that recorded the material work;
- verdict `PASS`;
- unresolved verdicts empty; and
- all completion-proof item refs present in continuity artifacts or observation events.

- [ ] **Step 4: Implement action authorization**

`authorize_action(manifest, capability_id, requested_permissions, requested_effects, estimated_costs) -> list[str]` returns named refusal codes for:

```text
AUTHORITY_REVOKED
PERMISSION_NOT_GRANTED
PROTECTED_STATE_VIOLATION
COST_NOT_AUTHORIZED
ESCALATION_REQUIRED
```

An empty list means the action is inside authority; it does not execute it.

- [ ] **Step 5: Run GREEN and commit**

```bash
python -m unittest tests.test_state_machine tests.test_authority -v
python -m unittest discover -s tests -p 'test_*.py' -v
```

```bash
git add contracts/mission-event.schema.json practical_agency/authority.py \
        practical_agency/state_machine.py tests/test_authority.py \
        tests/test_state_machine.py
git commit -m "feat: enforce bounded mission authority and transitions

Signed-off-by: SternOne <89846440+SternOne@users.noreply.github.com>"
```

---

### Task 4: Add atomic checkpoints and honest resumption

**Files:**
- Create: `tests/test_checkpoint_store.py`
- Create: `practical_agency/checkpoint_store.py`
- Create: `contracts/checkpoint.schema.json`
- Create: `contracts/execution-receipt.schema.json`

**Interfaces:**
- Consumes: a validated `MissionManifest` and append-only mission events.
- Produces: atomic checkpoint files, SHA-256 receipts, and `load_latest(mission_id)`.

- [ ] **Step 1: Write failing checkpoint tests**

Cover:

- atomic write uses temp file + `os.replace`;
- checkpoint filename includes zero-padded revision;
- receipt hash matches exact bytes;
- loading rejects a hash mismatch;
- loading rejects a lower revision as latest when a higher valid revision exists;
- a stray partial temp file is ignored;
- a summary cannot substitute for a checkpoint; and
- a live-subject contradiction is returned as a first-class reconciliation item.

- [ ] **Step 2: Run RED**

```bash
python -m unittest tests.test_checkpoint_store -v
```

- [ ] **Step 3: Implement the store**

Public interface:

```python
@dataclass(frozen=True, slots=True)
class CheckpointReceipt:
    mission_id: str
    revision: int
    path: str
    sha256: str
    created_at: str

class FileCheckpointStore:
    def __init__(self, root: Path) -> None: ...
    def save(self, manifest: MissionManifest) -> CheckpointReceipt: ...
    def load(self, receipt: CheckpointReceipt) -> MissionManifest: ...
    def load_latest(self, mission_id: str) -> tuple[MissionManifest, CheckpointReceipt] | None: ...
```

Use `tempfile.NamedTemporaryFile(delete=False, dir=target.parent)`, flush, `os.fsync`, then `os.replace`. Hash the exact canonical bytes before replace. Never overwrite an existing revision file with different bytes.

- [ ] **Step 4: Implement reconciliation hook**

Define:

```python
@dataclass(frozen=True, slots=True)
class ReconciliationFinding:
    subject_ref: str
    checkpoint_value: object
    live_value: object
    classification: str  # CONTRADICTED | MOVED | UNVERIFIED
```

The checkpoint store does not fetch live state. It accepts observations from an adapter and compares them to stored claims.

- [ ] **Step 5: Run GREEN and commit**

```bash
python -m unittest tests.test_checkpoint_store -v
python -m unittest discover -s tests -p 'test_*.py' -v
```

```bash
git add contracts/checkpoint.schema.json contracts/execution-receipt.schema.json \
        practical_agency/checkpoint_store.py tests/test_checkpoint_store.py
git commit -m "feat: add atomic mission checkpoints

Signed-off-by: SternOne <89846440+SternOne@users.noreply.github.com>"
```

---

### Task 5: Discover capabilities without an inventory

**Files:**
- Create: `tests/test_capability_discovery.py`
- Create: `practical_agency/capability_discovery.py`
- Create: `contracts/capability-request.schema.json`
- Create: `contracts/capability-result.schema.json`

**Interfaces:**
- Consumes: one or more explicit capability roots and optional harness-provided descriptors.
- Produces: sorted `CapabilityDescriptor` records with source hashes and availability.

- [ ] **Step 1: Write failing discovery tests**

Use temporary directories to prove:

- a `SKILL.md` child is discovered from frontmatter;
- adding a new skill requires no source-code list edit;
- removing a skill removes it from discovery;
- malformed frontmatter becomes `degraded`, not silently absent;
- empty/blank descriptions become `unavailable`;
- duplicate ids at different sources become a named conflict;
- source SHA-256 changes when the skill body changes; and
- no file in `practical_agency/` contains a literal list of known epistemic or workflow skill names.

- [ ] **Step 2: Run RED**

```bash
python -m unittest tests.test_capability_discovery -v
```

- [ ] **Step 3: Implement descriptors and provider protocol**

```python
class Persistence(str, Enum):
    PROMPT = "prompt"
    SESSION = "session"
    EXTERNAL = "external"

@dataclass(frozen=True, slots=True)
class CapabilityDescriptor:
    capability_id: str
    kind: str
    source_ref: str
    source_sha256: str
    description: str
    input_contract: str | None
    output_contract: str | None
    authority_required: tuple[str, ...]
    persistence: Persistence
    independence: str
    availability: str
    degradation_reason: str | None

class CapabilityProvider(Protocol):
    def discover(self) -> list[CapabilityDescriptor]: ...
```

`FileSystemSkillProvider` scans only immediate child directories containing `SKILL.md`. Parse the leading YAML frontmatter with a deliberately small parser supporting top-level `name`, `description`, and `metadata`; fail closed on unsupported syntax rather than pretending to understand it.

- [ ] **Step 4: Add capability request/result carriers**

`capability-request@1` contains mission id/revision, capability id/source hash, bounded question/action, authority receipt, expected output contract, return point, and timeout/stop condition.

`capability-result@1` contains request id, status (`completed|declined|blocked|failed`), artifact refs, observed effects, returned control point, and coverage limits. It never carries an implicit completion verdict for the whole mission.

- [ ] **Step 5: Run GREEN and commit**

```bash
python -m unittest tests.test_capability_discovery -v
python -m unittest discover -s tests -p 'test_*.py' -v
```

```bash
git add contracts/capability-request.schema.json contracts/capability-result.schema.json \
        practical_agency/capability_discovery.py tests/test_capability_discovery.py
git commit -m "feat: discover mission capabilities dynamically

Signed-off-by: SternOne <89846440+SternOne@users.noreply.github.com>"
```

---

### Task 6: Implement the bounded mission coordinator

**Files:**
- Create: `tests/test_coordinator.py`
- Create: `practical_agency/coordinator.py`
- Create: `roles/mission-steward.md`
- Create: `roles/independent-acceptor.md`

**Interfaces:**
- Consumes: manifest, capabilities, checkpoint store, observations, and an execution adapter.
- Produces: one bounded `CoordinationDecision`, one capability request or execution request, and a checkpointed mission revision.

- [ ] **Step 1: Write failing coordinator tests**

Cover:

- routine directly checkable action can proceed without manufacturing epistemic ceremony;
- an unresolved load-bearing claim produces a bounded capability request and preserves the exact return point;
- capability result returns to that point rather than taking over the mission;
- unavailable capability becomes visible degraded/blocker state;
- one call dispatches at most one consequential execution step;
- no authority means no dispatch;
- no checkpoint store means a visible session-bounded degradation;
- a completion proposal enters verifying, never completed;
- a returned `NO-GO` or `FAIL` verdict cannot be rewritten; and
- `helix it` and `manifest this` normalize to the same invocation intent.

- [ ] **Step 2: Run RED**

```bash
python -m unittest tests.test_coordinator -v
```

- [ ] **Step 3: Implement coordinator types**

```python
@dataclass(frozen=True, slots=True)
class ReturnPoint:
    mission_id: str
    revision: int
    frontier_index: int
    label: str

@dataclass(frozen=True, slots=True)
class CoordinationDecision:
    kind: str  # NOOP | REQUEST_CAPABILITY | DISPATCH | BLOCK | VERIFY
    reason: str
    request: dict[str, Any] | None
    return_point: ReturnPoint | None

class ExecutionAdapter(Protocol):
    def dispatch(self, request: dict[str, Any]) -> dict[str, Any]: ...
```

The coordinator does not contain a stage-to-skill table. It accepts either:

- a condition already named by the current workflow/epistemic layer;
- a capability id explicitly invoked by the operator; or
- a descriptor whose own trigger/role text matches a harness-provided invocation decision.

The deterministic kernel records the decision but does not attempt natural-language trigger matching itself.

- [ ] **Step 4: Write role contracts**

`mission-steward.md` states:

- preserve authority;
- re-anchor before resumption;
- choose one bounded next action;
- invoke rather than reimplement member capabilities;
- checkpoint every material transition;
- never self-accept.

`independent-acceptor.md` states:

- receives frozen mission revision and proof bundle;
- did not perform the material work under review;
- returns `PASS|FAIL|INCONCLUSIVE` with evidence refs;
- cannot alter operator intent or dispatch fixes.

- [ ] **Step 5: Run GREEN and commit**

```bash
python -m unittest tests.test_coordinator -v
python -m unittest discover -s tests -p 'test_*.py' -v
```

```bash
git add practical_agency/coordinator.py roles tests/test_coordinator.py
git commit -m "feat: add bounded mission coordination

Signed-off-by: SternOne <89846440+SternOne@users.noreply.github.com>"
```

---

### Task 7: Add the sole public `manifest` skill

**Files:**
- Create: `tests/test_manifest_skill.py`
- Create: `plugins/practical-agency/skills/manifest/SKILL.md`
- Create: `plugins/practical-agency/.claude-plugin/plugin.json`
- Modify: `.github/workflows/ci.yml`
- Modify: `README.md`

**Interfaces:**
- Consumes: explicit operator intent to create, resume, reconcile, advance, verify, or close a mission.
- Produces: a validated mission manifest, bounded next action, and honest execution/checkpoint receipts.

- [ ] **Step 1: Write failing skill-surface tests**

Test:

```python
SKILLS = ROOT / "plugins" / "practical-agency" / "skills"
skill_files = sorted(SKILLS.glob("*/SKILL.md"))
self.assertEqual([path.parent.name for path in skill_files], ["manifest"])

text = skill_files[0].read_text(encoding="utf-8")
for required in (
    "name: manifest",
    "operator",
    "mission manifest",
    "never self-certify",
    "capability",
    "checkpoint",
    "helix it",
):
    self.assertIn(required, text)
```

Also parse the frontmatter description and enforce a recorded UTF-8 byte ceiling of **420 bytes** for v0.1. Raising the ceiling requires an explicit same-commit justification.

- [ ] **Step 2: Run RED**

```bash
python -m unittest tests.test_manifest_skill -v
```

Expected: no skill exists.

- [ ] **Step 3: Write the `manifest` skill**

Frontmatter:

```yaml
---
name: manifest
description: Use when the operator asks to make an intended outcome real through durable, coordinated, resumable work, including "manifest this", "carry this through", or "helix it". Preserve operator authority and mission state, invoke available workflow and epistemic capabilities, act only through authorized substrates, checkpoint observed effects, and never self-certify material completion. Do NOT use for a routine one-step task already directly checkable in the current session.
---
```

If this exceeds 420 UTF-8 bytes, shorten without removing explicit invocation, authority, checkpoint, independence, and routine-decline semantics.

The body must define:

1. what Practical Agency is and is not;
2. create-versus-resume behavior;
3. authority capture and amendment;
4. live-state re-anchoring;
5. capability discovery and member ownership;
6. bounded invocation and return points;
7. one-action dispatch;
8. observation and checkpointing;
9. commission-watch integration;
10. independent verification and completion;
11. degraded operation; and
12. output format.

Do not enumerate installed skill names. Mention external packages only as examples of capability classes, not as a routing list.

- [ ] **Step 4: Add package metadata**

`plugin.json` points directly at `./skills` and describes the package as one explicit-entry mission-control skill. No copied skill inventory.

- [ ] **Step 5: Extend CI**

Add a script or inline check that fails unless the canonical skills directory contains exactly one `SKILL.md` child named `manifest`. Add the byte-budget test to the normal suite.

- [ ] **Step 6: Run GREEN and commit**

```bash
python -m unittest tests.test_manifest_skill -v
python -m unittest discover -s tests -p 'test_*.py' -v
```

```bash
git add plugins README.md .github/workflows/ci.yml tests/test_manifest_skill.py
git commit -m "feat: add the manifest mission-control skill

Signed-off-by: SternOne <89846440+SternOne@users.noreply.github.com>"
```

---

### Task 8: Integrate commission-watch through an adapter contract

**Files:**
- Create: `tests/test_watch_commission_adapter.py`
- Create: `practical_agency/watch_commission.py`
- Create: `examples/watch-commission-mission.json`
- Create: `adapters/README.md`

**Interfaces:**
- Consumes: a validated `watch-commission@1` record from `epistemic-skills` and a `WatchExecutionAdapter`.
- Produces: retained mechanism/proof refs and a mission event; never performs epistemic promotion itself.

#### Hardened commission carrier requirements

The adapter must preserve the distinction among current state, historical proof,
block evidence, and later observed failure. It never synthesizes, strips, or
reinterprets evidence fields:

- every adapter claim returns a durable external receipt reference;
- a missing or unproven dependency returns dated `block_evidence` as well as the
  closed `block_reason`;
- preparing a disabled external mechanism yields
  `BLOCKED: KILL_SWITCH_UNPROVEN` until `exercise_kill_switch` returns a verified
  receipt; only then may the adapter request `INERT`;
- `INERT` can retain a complete prior proof after deliberate disablement;
- `PROVEN` is accepted only from the upstream semantic verifier and only while
  the external mechanism remains enabled;
- `SUSPECT` carries a later observed failure kind, detail, time, and receipt;
- prompt/chat/session artifacts and self-asserted receipt references are refused;
- fixture adapters explicitly identify isolated scope and unestablished
  production coverage;
- a missing verifier leaves the external contract unverified; and
- revocation/disablement changes current state without rewriting prior proof or
  block evidence.

Tests must round-trip the dedicated upstream fixtures: valid proven, valid
inert-with-proof-history, valid suspect-observed-failure, valid
blocked-no-substrate, and valid blocked-kill-switch-unproven. Also prove rejection
of self-asserted skill persistence, missing block evidence, undeclared fixture
scope, and partial proof history.

- [ ] **Step 1: Write failing integration tests**

Define a fake adapter and prove:

- `BLOCKED/NO_EXECUTION_SUBSTRATE` is retained without dispatch;
- a prepared external mechanism remains `BLOCKED: KILL_SWITCH_UNPROVEN` until the adapter returns a verified kill-switch receipt, then becomes `INERT`;
- `PROVEN` is accepted only after the external verifier accepts the returned record;
- the mission steward cannot synthesize `PROVEN` from adapter success alone;
- an incoming crossing event references the retained commission id and reopens the mission frontier; and
- kill/revocation invokes the adapter's disable operation when required by authority.

- [ ] **Step 2: Run RED**

```bash
python -m unittest tests.test_watch_commission_adapter -v
```

- [ ] **Step 3: Implement the adapter protocol**

```python
class WatchExecutionAdapter(Protocol):
    def prepare_disabled(self, commission: Mapping[str, Any]) -> Mapping[str, Any]: ...
    def exercise_kill_switch(self, mechanism_ref: str) -> Mapping[str, Any]: ...
    def enable_for_proof(self, mechanism_ref: str, authority_ref: str) -> Mapping[str, Any]: ...
    def perform_safe_crossing(self, mechanism_ref: str, proof_spec: Mapping[str, Any]) -> Mapping[str, Any]: ...
    def disable(self, mechanism_ref: str) -> Mapping[str, Any]: ...
```

Practical Agency stores adapter receipts and calls the `epistemic-skills` verifier when available. If the verifier is unavailable, state remains `UNVERIFIED_EXTERNAL_CONTRACT`; do not duplicate its promotion logic as a second authority.

- [ ] **Step 4: Add the example mission**

The example contains a mission whose desired state is a proven external disk-space alert. It begins with `watch_commissions` containing `BLOCKED/NO_EXECUTION_SUBSTRATE` plus dated discovery evidence, demonstrating honest degradation rather than fabricated persistence. A second transition fixture prepares a mechanism as `BLOCKED/KILL_SWITCH_UNPROVEN` and reaches `INERT` only after a verified kill-switch receipt.

- [ ] **Step 5: Run GREEN and commit**

```bash
python -m unittest tests.test_watch_commission_adapter -v
python -m unittest discover -s tests -p 'test_*.py' -v
```

```bash
git add adapters examples/watch-commission-mission.json \
        practical_agency/watch_commission.py tests/test_watch_commission_adapter.py
git commit -m "feat: integrate external watch commissions

Signed-off-by: SternOne <89846440+SternOne@users.noreply.github.com>"
```

---

### Task 9: Prove crash recovery and independent completion end to end

**Files:**
- Create: `tests/test_end_to_end_mission.py`
- Modify: `README.md`

**Interfaces:**
- Consumes: all prior kernel components.
- Produces: one deterministic end-to-end proof fixture.

- [ ] **Step 1: Write the end-to-end test**

The test must:

1. create a draft mission from verbatim operator intent;
2. approve it;
3. discover a fixture capability dynamically;
4. dispatch one authorized action through an in-memory adapter;
5. record the observed artifact hash;
6. checkpoint revision N;
7. discard all in-memory objects;
8. load revision N from the store;
9. inject a live-state contradiction and verify the mission reopens;
10. dispatch a corrective action;
11. enter verifying;
12. attempt and reject steward self-acceptance;
13. accept through an independent actor; and
14. load the final completed checkpoint with the original operator instruction unchanged.

- [ ] **Step 2: Run RED**

Run the test before any missing glue is implemented. Expected: fail at the first absent integration behavior, not on fixture syntax.

- [ ] **Step 3: Add only the minimal glue needed**

Do not add a service, daemon, network API, arbitrary shell adapter, or UI. Keep the entire end-to-end path in-process and deterministic.

- [ ] **Step 4: Run the full suite**

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
python -m compileall -q practical_agency tests
```

Expected: all pass with no warnings.

- [ ] **Step 5: Document the proof and limitations**

README must state:

- deterministic mission custody is proven by the fixture;
- no production external execution adapter is included yet;
- no background service is claimed;
- live harness loading is unverified until tested in each packaged harness; and
- end-to-end mission benefit over an ordinary skilled agent remains unestablished until comparative evaluation exists.

- [ ] **Step 6: Commit**

```bash
git add README.md tests/test_end_to_end_mission.py practical_agency
git commit -m "test: prove resumable independently accepted missions

Signed-off-by: SternOne <89846440+SternOne@users.noreply.github.com>"
```

---

### Task 10: Final verification, packaging, and first release boundary

**Files:**
- Verify entire repository.
- Create: `docs/release/RELEASE-0.1.0.md`

**Interfaces:**
- Consumes: Tasks 1–9.
- Produces: a reviewable v0.1 candidate without unverified runtime claims.

- [ ] **Step 1: Run all deterministic checks**

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
python -m compileall -q practical_agency tests
python - <<'PY'
import json
from pathlib import Path
for path in sorted(Path('.').rglob('*.json')):
    json.loads(path.read_text(encoding='utf-8'))
print('json ok')
PY
git diff --check main...HEAD
```

- [ ] **Step 2: Verify public-content boundaries**

Search the exact candidate for:

```text
absolute Windows/POSIX home paths
private repository coordinates
hostnames and IP addresses
credential/token/secret assignments
user email addresses other than DCO trailers
```

Review each hit in context and retain a release receipt. Do not treat a secret scanner as a substitute for public-content review.

- [ ] **Step 3: Verify live package loading**

For every supported harness, record:

```text
source revision
installed path
loaded skill count = 1
loaded skill name = manifest
loaded description present and exact
"manifest this" invocation accepted
"helix it" compatibility intent accepted
cache/reload behavior
verification tier
```

A structural archive test is not a live harness test.

- [ ] **Step 4: Run independent adversarial review**

Freeze the exact candidate. Review at minimum:

- authority confusion;
- mission-state corruption;
- hidden self-certification;
- prompt-injection through capability descriptors;
- stale checkpoint continuation;
- adapter privilege escalation;
- description-budget displacement; and
- semantic overlap with workflow and epistemic packages.

Retain findings, dissent, arbitration, and computed verdict. Do not tag on an unresolved high-severity condition.

- [ ] **Step 5: Write honest release notes**

`RELEASE-0.1.0.md` must distinguish:

```text
PROVEN: deterministic contracts/state/checkpoint tests
VERIFIED PER HARNESS: only harnesses actually exercised
UNVERIFIED: production adapters not exercised
NOT CLAIMED: autonomous background operation, universal efficacy, independent ends
```

- [ ] **Step 6: Open the release PR**

Keep it draft until deterministic CI, DCO, public-content review, live harness evidence, and independent judgment are all recorded against the exact head commit.
