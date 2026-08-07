#!/usr/bin/env python3
"""Apply the exact PR #110 truth and handoff hardening, then remove this helper."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def replace_once(path: str, old: str, new: str) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected one marker, found {count}: {old[:100]!r}")
    target.write_text(text.replace(old, new), encoding="utf-8")


# Close the semantic post-crossing classification. Mission custody is not a
# value in this field and order does not carry meaning.
replace_once(
    "plugins/epistemic-skills/contracts/watch-commission/verify_watch_commission.py",
    '''BLOCK_REASONS = {
    "NO_EXECUTION_SUBSTRATE",
    "NO_REACHABLE_DESTINATION",
    "NO_AUTHORITY_TO_ENABLE",
    "NO_KILL_SWITCH",
    "KILL_SWITCH_UNPROVEN",
    "NO_SAFE_PROOF_CROSSING",
    "PROBE_UNAVAILABLE",
}
FORBIDDEN_EVIDENCE_PREFIXES = (
''',
    '''BLOCK_REASONS = {
    "NO_EXECUTION_SUBSTRATE",
    "NO_REACHABLE_DESTINATION",
    "NO_AUTHORITY_TO_ENABLE",
    "NO_KILL_SWITCH",
    "KILL_SWITCH_UNPROVEN",
    "NO_SAFE_PROOF_CROSSING",
    "PROBE_UNAVAILABLE",
}
POST_CROSSING_HANDOFF = frozenset({"triage", "decision-ledger"})
FORBIDDEN_EVIDENCE_PREFIXES = (
''',
)
replace_once(
    "plugins/epistemic-skills/contracts/watch-commission/verify_watch_commission.py",
    '''    on_crossing = _require_string_list(handoff, "on_crossing", "handoff", errors)
    if on_crossing is not None and any(not item.strip() for item in on_crossing):
        _error(errors, "INVALID_VALUE", "handoff.on_crossing entries must be non-empty")
''',
    '''    on_crossing = _require_string_list(handoff, "on_crossing", "handoff", errors)
    if on_crossing is not None and any(not item.strip() for item in on_crossing):
        _error(errors, "INVALID_VALUE", "handoff.on_crossing entries must be non-empty")
    if on_crossing is not None and set(on_crossing) != POST_CROSSING_HANDOFF:
        _error(
            errors,
            "INVALID_POST_CROSSING_HANDOFF",
            "handoff.on_crossing must classify exactly triage and decision-ledger; mission custody is separate",
        )
''',
)

replace_once(
    "plugins/epistemic-skills/contracts/watch-commission/watch-commission.schema.json",
    '''    "handoff": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "on_crossing"
      ],
      "properties": {
        "on_crossing": {
          "type": "array",
          "items": {
            "type": "string",
            "minLength": 1
          },
          "uniqueItems": true
        }
      }
    },
''',
    '''    "handoff": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "on_crossing"
      ],
      "properties": {
        "on_crossing": {
          "type": "array",
          "minItems": 2,
          "maxItems": 2,
          "items": {
            "type": "string",
            "enum": [
              "triage",
              "decision-ledger"
            ]
          },
          "uniqueItems": true
        }
      }
    },
''',
)

replace_once(
    "plugins/epistemic-skills/contracts/watch-commission/README.md",
    '''`handoff.on_crossing` is intentionally narrow: it names the disciplines that may
consume a **real crossing** after the external observer reports one. It does not
name the system that stores or operates the commission. Optional mission-control
custody is a separate outward transport concern and remains explicit/generic
until an external package publishes and verifies a `watch-commission@1` intake
contract. The carrier therefore implies no automatic routing to Practical Agency
or any other package.
''',
    '''`handoff.on_crossing` is a closed post-crossing classification containing
exactly `triage` and `decision-ledger`; array order has no meaning. It identifies
the two epistemic disciplines that may consume a **real crossing** after the
external observer reports one. It does not compel either discipline to fire —
each still owns its positive trigger — and it does not name the system that
stores or operates the commission.

Optional mission-control custody is a separate outward transport concern and
remains explicit/generic until a consumer publishes, verifies, and admits a
versioned `watch-commission@1` intake contract. The carrier therefore rejects
`manifest` or any other custody target in `handoff.on_crossing` and implies no
automatic routing to Practical Agency or any other package.
''',
)

replace_once(
    "plugins/epistemic-skills/skills/watch/SKILL.md",
    '''When a mission-control layer is available, hand the validated commission record
outward so it can select an authorized adapter, retain the external mechanism
reference, checkpoint the evidence receipts, and route later crossings or
failures back into the mission. This package does not assume that layer is
installed.


`handoff.on_crossing` and `metadata.hands-to` name post-crossing epistemic
consumers: `triage` for cause and `decision-ledger` for durable consequential
state. They do **not** declare commission custody by another package. A
cross-package mission-control handoff becomes machine-routable only after that
package publishes and verifies an intake contract.
''',
    '''When an admitted mission-control intake is available, hand the validated
commission record outward through that versioned intake so the consumer can
select an authorized adapter, retain the external mechanism reference,
checkpoint evidence receipts, and route later events back into the mission.
Repository or package existence alone is not routability; no automatic
Practical Agency intake is claimed here.

`handoff.on_crossing` and `metadata.hands-to` are the same closed post-crossing
classification: exactly `triage` for cause and `decision-ledger` for durable
consequential state. Array order is not semantic, and the classification does not
compel either discipline to fire — each still owns its trigger. It does **not**
declare commission custody, and `manifest` is not a valid value in this field.
A cross-package mission-control handoff becomes machine-routable only after its
versioned intake contract is implemented, verified, and admitted.
''',
)

DESIGN = "docs/superpowers/specs/2026-08-07-practical-agency-and-commission-watch-design.md"
replace_once(
    DESIGN,
    '''revision is `e244d534a6e26bc9a352846a25ffce18b8d93a53` and contains one initial root
`skills/manifest/SKILL.md`, root/Cursor plugin metadata, a README, and a v0
Markdown mission-manifest field guide.

That seed establishes the project identity and sole public entry skill. It is an
''',
    '''revision is `e244d534a6e26bc9a352846a25ffce18b8d93a53` and contains one initial root
`skills/manifest/SKILL.md`, root/Cursor plugin metadata, a README, and a v0
Markdown mission-manifest field guide. Cursor metadata declares `0.1.0`, but no
tag or GitHub release exists; that value is an unreleased seed version, not
evidence that the deterministic mission kernel has shipped.

That seed establishes the project identity and sole public entry skill. It is an
''',
)
replace_once(
    DESIGN,
    '''PR #110 does not modify or verify the external repository and creates no
automatic `watch`→`manifest` route. `watch`'s generic outward handoff remains the
truthful boundary until Practical Agency publishes and verifies an intake
contract.
''',
    '''PR #110 does not modify the external repository or verify its target kernel,
checkpoint, adapter, or intake behavior. It does record the inspected seed
baseline above so this design does not reason from a nonexistent repository.
The PR creates no automatic `watch`→`manifest` route; generic outward transport
remains the truthful boundary until a versioned Practical Agency intake contract
is implemented, verified, and admitted.
''',
)
replace_once(
    DESIGN,
    '''The existing root skill remains canonical. Harness metadata points at `./skills`;
no second independently editable skill tree is introduced.
''',
    '''The existing root skill remains canonical. Each harness metadata surface uses
its native schema; surfaces that support an explicit skill-path field point at
`./skills`. No second independently editable skill tree or copied skill inventory
is introduced.
''',
)
replace_once(
    DESIGN,
    '''handoff:
  on_crossing: [triage, decision-ledger]
coverage_limits: []
```

### State semantics
''',
    '''handoff:
  on_crossing: [triage, decision-ledger]
coverage_limits: []
```

`handoff.on_crossing` is closed to exactly `triage` and `decision-ledger`;
ordering is not semantic. It classifies possible epistemic consumers after a
real crossing, does not compel either to fire, and never denotes mission custody.

### State semantics
''',
)
replace_once(
    DESIGN,
    '''manifest / mission steward
    selects an authorized adapter, retains the commission, routes later events
''',
    '''future admitted mission-control intake (for example `manifest`)
    selects an authorized adapter, retains the commission, routes later events
''',
)
replace_once(
    DESIGN,
    '''Where Practical Agency is unavailable, commission-watch may still produce `DECLARED`, `BLOCKED`, or a provider-specific commission if the current harness can directly configure and prove an external observer. It must never pretend the missing mission layer exists.
''',
    '''Where an admitted, intake-capable Practical Agency mission-control layer is unavailable, commission-watch may still produce `DECLARED`, `BLOCKED`, or a provider-specific commission if the current harness can directly configure and prove an external observer. It must never infer intake capability from repository or package existence.
''',
)

BOOTSTRAP = "docs/superpowers/plans/2026-08-07-practical-agency-bootstrap.md"
replace_once(
    BOOTSTRAP,
    '''Every task below modifies this seed in place. The root
`skills/manifest/SKILL.md` remains the sole canonical skill body and all harness
metadata must point at `./skills`.
''',
    '''Every task below modifies this seed in place. The root
`skills/manifest/SKILL.md` remains the sole canonical skill body. Each harness
metadata surface uses its native schema; only schemas with an explicit skill-path
field point at `./skills`. No surface may introduce a copied skill body or
hand-maintained inventory.
''',
)
replace_once(
    BOOTSTRAP,
    '''│   ├── test_manifest_skill.py
│   └── test_state_machine.py
├── AGENTS.md
''',
    '''│   ├── test_manifest_skill.py
│   └── test_state_machine.py
├── tests/__init__.py
├── AGENTS.md
''',
)
replace_once(
    BOOTSTRAP,
    '''- Create: `.github/workflows/ci.yml`
- Create: `practical_agency/__init__.py`
''',
    '''- Create: `.github/workflows/ci.yml`
- Create: `practical_agency/__init__.py`
- Create: `tests/__init__.py`
''',
)
replace_once(
    BOOTSTRAP,
    '''Add a status section stating that v0.1 is a deterministic mission kernel and portable skill, not a daemon, hosted service, or autonomous background actor.
''',
    '''Add a status section stating that the existing `0.1.0` metadata describes an
unreleased seed with a portable authorization-and-recording skill. Do not call it
a deterministic mission kernel until Tasks 2–9 and independent acceptance pass;
at every stage it remains neither a daemon, hosted service, nor autonomous
background actor.
''',
)
replace_once(
    BOOTSTRAP,
    '''Use distribution name `zms-practical-agency` to avoid claiming an unscoped package name. The repository and project remain `practical-agency`.

- [ ] **Step 4: Add the minimal test command**
''',
    '''Use distribution name `zms-practical-agency` to avoid claiming an unscoped package name. The repository and project remain `practical-agency`.

The inspected Cursor metadata already declares `0.1.0`, but no tag or GitHub
release exists. Treat it as the unreleased seed version, keep all version surfaces
synchronized, and do not tag `0.1.0` until the release boundary in Task 10 is met.

- [ ] **Step 4: Add the minimal test command**
''',
)
replace_once(
    BOOTSTRAP,
    '''Create `practical_agency/__init__.py`:

```python
"""Practical Agency deterministic mission-control kernel."""

__version__ = "0.1.0"
```

Run:
''',
    '''Create `practical_agency/__init__.py`:

```python
"""Practical Agency deterministic mission-control kernel."""

__version__ = "0.1.0"
```

Also create an empty `tests/__init__.py` so `unittest` discovery has a real
start directory before the first behavior test exists.

Run:
''',
)
replace_once(
    BOOTSTRAP,
    '''Root, Cursor, and any Claude harness metadata point directly at the same `./skills` directory and describe one explicit-entry mission-control skill. No copied skill inventory or duplicate skill body is permitted.
''',
    '''Root, Cursor, Claude, and later harness metadata each use their native schema
and describe the same one explicit-entry mission-control skill. Only metadata
schemas with a path field point at `./skills`; no copied skill inventory or
duplicate skill body is permitted.
''',
)

COMMISSION_PLAN = "docs/superpowers/plans/2026-08-07-commission-watch-clarification.md"
replace_once(
    COMMISSION_PLAN,
    '''When a mission-control layer is available, hand the validated commission record
outward so it can select an authorized adapter, retain the external mechanism
reference, checkpoint the proof receipt, and route later crossings back into the
mission. This package does not assume that layer is installed.
```

Do not add `manifest` to `metadata.hands-to` until a package containing that capability exists and the cross-package routing contract has been admitted.
''',
    '''When an admitted mission-control intake is available, hand the validated
commission record outward through that versioned intake so the consumer can
select an authorized adapter, retain the external mechanism reference,
checkpoint evidence receipts, and route later events back into the mission.
Repository or package existence alone is not routability.
```

Practical Agency and an initial `manifest` package now exist. That fact alone does
not establish a `watch-commission@1` intake or cross-package route. Do not add
`manifest` to `metadata.hands-to`; add no custody target there unless a versioned
intake/routing contract is implemented, verified, and admitted. Post-crossing
classification remains exactly `triage` and `decision-ledger`.
''',
)
replace_once(
    COMMISSION_PLAN,
    '''- Practical Agency is specified separately and not falsely claimed implemented by this PR; and
''',
    '''- the existing Practical Agency seed is acknowledged while its target kernel and commission intake are not falsely claimed implemented by this PR; and
''',
)

POST_FREEZE = "docs/gauntlet-runs/commission-watch-pr110-2026-08-07/POST-FREEZE-RECONCILIATION.md"
replace_once(
    POST_FREEZE,
    '''| `handoff.on_crossing` denotes mission custody | It denotes post-crossing `triage`/`decision-ledger`; custody is separate outward transport. |
| The raw-SHA clean-room checkout defect is still open | Closed: reconciliation run `31196648201` passed focused checks and exact-commit clean-room checkout before pushing the verified commit. |
''',
    '''| `handoff.on_crossing` denotes mission custody | It is a closed classification containing exactly `triage` and `decision-ledger`; order is non-semantic, each discipline still owns its trigger, and custody is separate outward transport. |
| Schema/verifier parity was already enforced | The frozen evidence report named a parity test that did not exist. PR #110 now contains the actual exact field/enum parity test. |
| Prose alone prevented a custody target in `handoff.on_crossing` | The schema and verifier accepted arbitrary strings, including `manifest`. PR #110 now rejects that and machine-enforces the documented boundary. |
| The raw-SHA clean-room checkout defect is still open | Closed: reconciliation run `31196648201` passed focused checks and exact-commit clean-room checkout before pushing the verified commit. |
''',
)
replace_once(
    POST_FREEZE,
    '''- `handoff.on_crossing` and `watch.metadata.hands-to` remain
  `[triage, decision-ledger]` because they describe response after a real crossing.
''',
    '''- `handoff.on_crossing` and `watch.metadata.hands-to` are machine-closed to
  exactly `[triage, decision-ledger]` because they classify possible response
  after a real crossing. Ordering is not semantic, neither is compelled to fire,
  and neither field denotes custody.
''',
)
replace_once(
    POST_FREEZE,
    '''5. Post-crossing response is explicitly separated from commission custody.
6. The PR body and current-status review records distinguish proved
   commission-watch behavior from unimplemented Practical Agency behavior.
''',
    '''5. Post-crossing response is explicitly separated from commission custody,
   and the schema/verifier reject `manifest` or arbitrary custody targets.
6. The schema/verifier field and closed-enum parity claim is backed by the actual
   executable test named in the review record.
7. The PR body and current-status review records distinguish proved
   commission-watch behavior from unimplemented Practical Agency behavior.
''',
)
replace_once(
    POST_FREEZE,
    '''- **B1 — ordinary final-head gates:** the dedicated reconciliation workflow is
  green, but the ordinary PR-triggered workflows for the current head are
  `action_required`. Approve them and require successful conclusions before
  merge.
''',
    '''- **B1 — ordinary final-head gates:** branch-push verification is necessary
  evidence but does not substitute for required PR checks. The exact final-head
  branch run is recorded in the PR body; approve the ordinary PR-triggered
  workflows and require successful conclusions before merge.
''',
)

GAUNTLET = "docs/gauntlet-runs/commission-watch-pr110-2026-08-07/GAUNTLET-SUMMARY.md"
replace_once(
    GAUNTLET,
    '''> and one initial `manifest` skill now exist; its deterministic kernel and
> commission intake do not. The dedicated reconciliation workflow passed the
> exact-commit clean-room and focused repository gates. The ordinary PR-triggered
> workflows for the current head are `action_required` and still need approval
> and a green conclusion. The historical frozen verdict remains `CONDITIONAL`;
''',
    '''> and one initial `manifest` skill now exist; its deterministic kernel and
> commission intake do not. The reconciliation also corrects the frozen report's
> nonexistent parity-test claim and machine-closes `handoff.on_crossing` to the
> post-crossing epistemic classification. The exact final-head branch run is
> recorded in the PR body. Ordinary PR-triggered workflows still need approval
> and a green conclusion. The historical frozen verdict remains `CONDITIONAL`;
''',
)
replace_once(
    GAUNTLET,
    '''- Schema and semantic verifier fields/enums are parity-tested.
''',
    '''- Schema and semantic verifier fields/enums are parity-tested by the actual
  executable test named in the review record.
- `handoff.on_crossing` is closed to exactly `triage` and `decision-ledger` and
  cannot be repurposed as `manifest` custody.
''',
)

print("PR #110 truth hardening applied")
