# Mission Custody Contracts ("custodian") Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Land the `mission-custody@1` contract family (Stage A) and the stdlib custody core + Claude Code `manifest` skill (Stage B) per the approved design `docs/superpowers/specs/2026-08-11-mission-custody-contracts-design.md`, ending with the tracer-mission handoff.

**Architecture:** Contracts-first, mirroring `plugins/epistemic-skills/contracts/watch-commission/` file-for-file in kind: four schema JSONs + ONE hand-rolled stdlib verifier + flat valid/invalid examples corpus + stdlib test script + path-filtered CI. The custody core is three focused stdlib modules beside the contracts (store / mission / CLI), proven by a three-subprocess kill-resume-repair test. The skill is one SKILL.md with three trigger doors and a hard decline clause.

**Tech Stack:** Python stdlib only (no jsonschema, no pip deps — house rule). Tests are plain scripts run with `python <file>` (exit code is the oracle), matching `test_watch_commission.py`. CI mirrors `.github/workflows/commission-watch-contract.yml` (pinned actions, Python 3.12).

## Global Constraints

- **Stdlib-only**: no third-party imports anywhere in contracts or core (spec: "stdlib verifier", "stdlib-only ... custody core").
- **Core size cap**: custody core total **~500–800 lines** across its three modules (spec cap). If a change pushes past ~800, stop and flag — do not gold-plate.
- **Schema evolution rule**: additive optional fields only within `@1`; anything else is a new epoch (spec, locked from gauntlet P1-DEFER-SCHEMA-RULE).
- **No routing**: no skill names, member inventories, or stage-to-skill tables anywhere in custodian output or SKILL.md (spec: P2-NO-PA-ROUTING preserved).
- **Closed state list**: `draft / active / reopened / verifying / completed / cancelled` — exactly these six.
- **Acceptance tiers**: `operator-accepted` > `declared-role-separation`; self-certification refused; **no `externally-proven` tier exists**.
- **FAIL is clearable**: a `FAIL` verdict must have a tested remediate → re-verify → accept path (designed out of PA's reject dead-end).
- **Line endings**: repo files are LF. Write files as shown; commit with `git -c core.autocrlf=input commit`. (Estate CRLF landmine.)
- **Every commit**: DCO sign-off `Signed-off-by: Zach Stern <zachstern@gmail.com>` plus the session trailers used in commit 979e0fd.
- **Working directory**: the worktree `Y:/dev/es-wt-mission-custody`, branch `spec/mission-custody-contracts-design`. Never touch `Y:/dev/epistemic-skills` (main checkout) or its stashes.
- **Timestamps**: all `*_utc` fields are ISO-8601 `YYYY-MM-DDTHH:MM:SSZ` strings; validators check shape (regex), not clock truth.
- **Hashes**: all `*_sha256` fields are 64 lowercase hex chars.

**Contract directory (all Stage A files):** `plugins/epistemic-skills/contracts/mission-custody/`
**Record kinds:** `mission-manifest@1`, `checkpoint@1`, `receipt@1`, `acceptance-verdict@1` — one verifier validates all four, dispatching on the required `"record"` field.

---

### Task 1: Verifier scaffold + `mission-manifest@1`

**Files:**
- Create: `plugins/epistemic-skills/contracts/mission-custody/verify_mission_custody.py`
- Create: `plugins/epistemic-skills/contracts/mission-custody/test_mission_custody.py`
- Create: `plugins/epistemic-skills/contracts/mission-custody/mission-manifest.schema.json`
- Create: `plugins/epistemic-skills/contracts/mission-custody/examples/valid-manifest-minimal.json`
- Create: `plugins/epistemic-skills/contracts/mission-custody/examples/invalid-manifest-amended-instruction.json`

**Interfaces:**
- Produces: `validate_record(record: dict) -> list[str]` (empty list = valid; each entry `"FIELD_PATH: reason"`), constants `STATES`, `TIERS`, `VERDICTS`, `RECORD_KINDS`, helpers `is_iso_utc(s) -> bool`, `is_sha256(s) -> bool`, `validate_manifest(rec) -> list[str]`. CLI: `python verify_mission_custody.py <file.json>...` exits 0 iff all valid, prints errors per file.
- Consumes: nothing (first task).

- [ ] **Step 1: Write the failing test**

`test_mission_custody.py` (complete file; later tasks append functions and extend `main()`):

```python
#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from verify_mission_custody import (  # noqa: E402
    RECORD_KINDS,
    STATES,
    TIERS,
    VERDICTS,
    validate_record,
)

FAILURES: list[str] = []


def check(name: str, cond: bool) -> None:
    if not cond:
        FAILURES.append(name)
        print(f"FAIL {name}")
    else:
        print(f"ok   {name}")


def load(name: str) -> dict:
    return json.loads((ROOT / "examples" / name).read_text(encoding="utf-8"))


def valid_manifest() -> dict:
    return load("valid-manifest-minimal.json")


def test_constants() -> None:
    check("states-closed-list", STATES == {
        "draft", "active", "reopened", "verifying", "completed", "cancelled"})
    check("tiers", TIERS == {"operator-accepted", "declared-role-separation"})
    check("verdicts", VERDICTS == {"PASS", "FAIL", "INCONCLUSIVE"})
    check("record-kinds", RECORD_KINDS == {
        "mission-manifest@1", "checkpoint@1", "receipt@1", "acceptance-verdict@1"})


def test_manifest_valid_example() -> None:
    check("manifest-valid-example", validate_record(valid_manifest()) == [])


def test_manifest_missing_instruction() -> None:
    rec = copy.deepcopy(valid_manifest())
    del rec["authority"]["instruction"]
    check("manifest-missing-instruction", validate_record(rec) != [])


def test_manifest_unknown_top_level_field() -> None:
    rec = copy.deepcopy(valid_manifest())
    rec["surprise"] = 1
    check("manifest-unknown-field", validate_record(rec) != [])


def test_manifest_bad_tier() -> None:
    rec = copy.deepcopy(valid_manifest())
    rec["acceptance"]["required_tier"] = "externally-proven"
    check("manifest-no-externally-proven-tier", validate_record(rec) != [])


def test_manifest_amendments_must_be_list_of_dated_text() -> None:
    rec = copy.deepcopy(valid_manifest())
    rec["authority"]["amendments"] = ["bare string"]
    check("manifest-amendment-shape", validate_record(rec) != [])


def test_unknown_record_kind_rejected() -> None:
    check("unknown-record-kind", validate_record({"record": "mystery@1"}) != [])


def test_examples_corpus() -> None:
    ex = ROOT / "examples"
    for path in sorted(ex.glob("valid-*.json")):
        rec = json.loads(path.read_text(encoding="utf-8"))
        check(f"corpus-{path.name}", validate_record(rec) == [])
    for path in sorted(ex.glob("invalid-*.json")):
        rec = json.loads(path.read_text(encoding="utf-8"))
        check(f"corpus-{path.name}", validate_record(rec) != [])


def main() -> int:
    test_constants()
    test_manifest_valid_example()
    test_manifest_missing_instruction()
    test_manifest_unknown_top_level_field()
    test_manifest_bad_tier()
    test_manifest_amendments_must_be_list_of_dated_text()
    test_unknown_record_kind_rejected()
    test_examples_corpus()
    print(f"\n{len(FAILURES)} failures")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd Y:/dev/es-wt-mission-custody && python plugins/epistemic-skills/contracts/mission-custody/test_mission_custody.py`
Expected: FAIL — `ModuleNotFoundError: No module named 'verify_mission_custody'`

- [ ] **Step 3: Write the examples**

`examples/valid-manifest-minimal.json`:

```json
{
  "record": "mission-manifest@1",
  "mission_id": "tracer-media-missing",
  "created_utc": "2026-08-11T00:00:00Z",
  "authority": {
    "operator_ref": "operator:zach-stern",
    "instruction": "Reconcile the monitored-missing media backlog without re-grabbing over VPN.",
    "amendments": [],
    "permissions": ["repo:vanta:read", "repo:vanta:write-config"],
    "protected_state": ["download-clients:enabled-state"],
    "acceptable_costs": ["one working session per stage"]
  },
  "scope": {
    "in": ["monitored-missing reconciliation"],
    "out": ["indexer changes", "VPN configuration"]
  },
  "acceptance": {
    "required_tier": "declared-role-separation",
    "acceptor_ref": null
  },
  "stop_rules": {
    "hold_if": ["any download client starts re-grabbing"],
    "stop_if": ["operator revokes"],
    "escalate_if": ["protected state would be touched"]
  },
  "steward_ref": "agent:claude-code-session"
}
```

`examples/invalid-manifest-amended-instruction.json` (amendment tries to carry a replacement instruction — append-only text is allowed, a non-object amendment is not):

```json
{
  "record": "mission-manifest@1",
  "mission_id": "bad-amend",
  "created_utc": "2026-08-11T00:00:00Z",
  "authority": {
    "operator_ref": "operator:zach-stern",
    "instruction": "Original instruction.",
    "amendments": ["replace the instruction with: do something else"],
    "permissions": [],
    "protected_state": [],
    "acceptable_costs": []
  },
  "scope": {"in": [], "out": []},
  "acceptance": {"required_tier": "declared-role-separation", "acceptor_ref": null},
  "stop_rules": {"hold_if": [], "stop_if": [], "escalate_if": []},
  "steward_ref": "agent:x"
}
```

- [ ] **Step 4: Write the verifier**

`verify_mission_custody.py` (complete file for this task; Tasks 2–3 add the dispatch branches marked below):

```python
#!/usr/bin/env python3
"""Validate mission-custody@1 records without third-party dependencies.

Record kinds: mission-manifest@1, checkpoint@1, receipt@1, acceptance-verdict@1.
validate_record() dispatches on the required "record" field and returns a list
of "FIELD: reason" strings; empty list means valid.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

STATES = {"draft", "active", "reopened", "verifying", "completed", "cancelled"}
TIERS = {"operator-accepted", "declared-role-separation"}
VERDICTS = {"PASS", "FAIL", "INCONCLUSIVE"}
RECORD_KINDS = {
    "mission-manifest@1",
    "checkpoint@1",
    "receipt@1",
    "acceptance-verdict@1",
}

_ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
_SHA_RE = re.compile(r"^[0-9a-f]{64}$")
_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")

MANIFEST_FIELDS = {
    "record", "mission_id", "created_utc", "authority", "scope",
    "acceptance", "stop_rules", "steward_ref",
}
AUTHORITY_FIELDS = {
    "operator_ref", "instruction", "amendments", "permissions",
    "protected_state", "acceptable_costs",
}


def is_iso_utc(value: Any) -> bool:
    return isinstance(value, str) and bool(_ISO_RE.match(value))


def is_sha256(value: Any) -> bool:
    return isinstance(value, str) and bool(_SHA_RE.match(value))


def _str_list(value: Any) -> bool:
    return isinstance(value, list) and all(
        isinstance(item, str) and item for item in value)


def _require(errors: list[str], cond: bool, field: str, reason: str) -> None:
    if not cond:
        errors.append(f"{field}: {reason}")


def _check_exact_fields(errors: list[str], rec: dict, allowed: set[str],
                        where: str) -> None:
    for key in rec:
        if key not in allowed:
            errors.append(f"{where}.{key}: unknown field")
    for key in allowed:
        if key not in rec:
            errors.append(f"{where}.{key}: missing")


def validate_manifest(rec: dict) -> list[str]:
    errors: list[str] = []
    _check_exact_fields(errors, rec, MANIFEST_FIELDS, "manifest")
    if errors:
        return errors
    _require(errors, isinstance(rec["mission_id"], str)
             and bool(_ID_RE.match(rec["mission_id"])),
             "mission_id", "kebab-case identifier required")
    _require(errors, is_iso_utc(rec["created_utc"]),
             "created_utc", "ISO-8601 Z timestamp required")
    _require(errors, isinstance(rec["steward_ref"], str) and rec["steward_ref"],
             "steward_ref", "non-empty string required")

    auth = rec["authority"]
    if not isinstance(auth, dict):
        errors.append("authority: object required")
        return errors
    _check_exact_fields(errors, auth, AUTHORITY_FIELDS, "authority")
    if not errors:
        _require(errors, isinstance(auth["operator_ref"], str)
                 and auth["operator_ref"],
                 "authority.operator_ref", "non-empty string required")
        _require(errors, isinstance(auth["instruction"], str)
                 and auth["instruction"],
                 "authority.instruction", "non-empty verbatim string required")
        amendments = auth["amendments"]
        ok = isinstance(amendments, list) and all(
            isinstance(a, dict) and set(a) == {"utc", "text"}
            and is_iso_utc(a["utc"]) and isinstance(a["text"], str) and a["text"]
            for a in amendments)
        _require(errors, ok, "authority.amendments",
                 "append-only list of {utc, text} objects required")
        for name in ("permissions", "protected_state", "acceptable_costs"):
            _require(errors, _str_list(auth[name]),
                     f"authority.{name}", "list of strings required")

    scope = rec["scope"]
    ok = isinstance(scope, dict) and set(scope) == {"in", "out"} \
        and _str_list(scope.get("in")) and _str_list(scope.get("out"))
    _require(errors, ok, "scope", '{"in": [...], "out": [...]} required')

    acc = rec["acceptance"]
    ok = isinstance(acc, dict) and set(acc) == {"required_tier", "acceptor_ref"} \
        and acc.get("required_tier") in TIERS \
        and (acc.get("acceptor_ref") is None
             or (isinstance(acc.get("acceptor_ref"), str) and acc["acceptor_ref"]))
    _require(errors, ok, "acceptance",
             "required_tier in TIERS and acceptor_ref string-or-null required")

    stop = rec["stop_rules"]
    ok = isinstance(stop, dict) \
        and set(stop) == {"hold_if", "stop_if", "escalate_if"} \
        and all(_str_list(stop[k]) for k in ("hold_if", "stop_if", "escalate_if"))
    _require(errors, ok, "stop_rules",
             "hold_if/stop_if/escalate_if string lists required")
    return errors


def validate_record(record: Any) -> list[str]:
    if not isinstance(record, dict):
        return ["record: JSON object required"]
    kind = record.get("record")
    if kind not in RECORD_KINDS:
        return [f"record: unknown kind {kind!r}"]
    if kind == "mission-manifest@1":
        return validate_manifest(record)
    if kind == "checkpoint@1":
        return validate_checkpoint(record)      # Task 2
    if kind == "receipt@1":
        return validate_receipt(record)         # Task 3
    return validate_acceptance_verdict(record)  # Task 3


def validate_checkpoint(rec: dict) -> list[str]:  # replaced in Task 2
    return ["record: checkpoint@1 validation not implemented"]


def validate_receipt(rec: dict) -> list[str]:  # replaced in Task 3
    return ["record: receipt@1 validation not implemented"]


def validate_acceptance_verdict(rec: dict) -> list[str]:  # replaced in Task 3
    return ["record: acceptance-verdict@1 validation not implemented"]


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: verify_mission_custody.py <file.json>...", file=sys.stderr)
        return 2
    failed = False
    for arg in argv:
        rec = json.loads(Path(arg).read_text(encoding="utf-8"))
        errors = validate_record(rec)
        if errors:
            failed = True
            for err in errors:
                print(f"{arg}: {err}")
        else:
            print(f"{arg}: valid")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

- [ ] **Step 5: Write the schema doc**

`mission-manifest.schema.json` — documentation contract (validation authority is the verifier, matching the watch-commission pattern):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "mission-manifest@1",
  "title": "mission-manifest@1",
  "description": "Durable mission authority record. Verbatim operator instruction is immutable; amendments append. Validation authority: verify_mission_custody.py (stdlib).",
  "type": "object",
  "required": ["record", "mission_id", "created_utc", "authority", "scope", "acceptance", "stop_rules", "steward_ref"],
  "additionalProperties": false,
  "properties": {
    "record": {"const": "mission-manifest@1"},
    "mission_id": {"type": "string", "pattern": "^[a-z0-9][a-z0-9-]*$"},
    "created_utc": {"type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}Z$"},
    "authority": {
      "type": "object",
      "required": ["operator_ref", "instruction", "amendments", "permissions", "protected_state", "acceptable_costs"],
      "additionalProperties": false,
      "properties": {
        "operator_ref": {"type": "string", "minLength": 1},
        "instruction": {"type": "string", "minLength": 1},
        "amendments": {"type": "array", "items": {"type": "object", "required": ["utc", "text"], "additionalProperties": false, "properties": {"utc": {"type": "string"}, "text": {"type": "string", "minLength": 1}}}},
        "permissions": {"type": "array", "items": {"type": "string"}},
        "protected_state": {"type": "array", "items": {"type": "string"}},
        "acceptable_costs": {"type": "array", "items": {"type": "string"}}
      }
    },
    "scope": {"type": "object", "required": ["in", "out"], "additionalProperties": false, "properties": {"in": {"type": "array", "items": {"type": "string"}}, "out": {"type": "array", "items": {"type": "string"}}}},
    "acceptance": {"type": "object", "required": ["required_tier", "acceptor_ref"], "additionalProperties": false, "properties": {"required_tier": {"enum": ["operator-accepted", "declared-role-separation"]}, "acceptor_ref": {"type": ["string", "null"]}}},
    "stop_rules": {"type": "object", "required": ["hold_if", "stop_if", "escalate_if"], "additionalProperties": false, "properties": {"hold_if": {"type": "array", "items": {"type": "string"}}, "stop_if": {"type": "array", "items": {"type": "string"}}, "escalate_if": {"type": "array", "items": {"type": "string"}}}},
    "steward_ref": {"type": "string", "minLength": 1}
  }
}
```

- [ ] **Step 6: Run test to verify it passes**

Run: `python plugins/epistemic-skills/contracts/mission-custody/test_mission_custody.py`
Expected: `0 failures`, exit 0. Also run `python -m py_compile plugins/epistemic-skills/contracts/mission-custody/verify_mission_custody.py` — exit 0.

- [ ] **Step 7: Commit**

```bash
git add plugins/epistemic-skills/contracts/mission-custody
git -c core.autocrlf=input commit -m "feat: mission-custody@1 verifier scaffold + mission-manifest" \
  -m "Signed-off-by: Zach Stern <zachstern@gmail.com>"
```

---

### Task 2: `checkpoint@1`

**Files:**
- Modify: `plugins/epistemic-skills/contracts/mission-custody/verify_mission_custody.py` (replace the `validate_checkpoint` stub)
- Modify: `plugins/epistemic-skills/contracts/mission-custody/test_mission_custody.py` (append tests; extend `main()`)
- Create: `plugins/epistemic-skills/contracts/mission-custody/checkpoint.schema.json`
- Create: `examples/valid-checkpoint-r1.json`, `examples/valid-checkpoint-r2-chained.json`, `examples/invalid-checkpoint-r2-unchained.json`, `examples/invalid-checkpoint-bad-status.json` (in the contract's `examples/` dir)

**Interfaces:**
- Consumes: `validate_manifest`, `is_iso_utc`, `is_sha256`, `STATES`, `_require`, `_check_exact_fields` from Task 1.
- Produces: `validate_checkpoint(rec) -> list[str]`; constant `CHECKPOINT_FIELDS`.

- [ ] **Step 1: Append failing tests**

```python
def valid_checkpoint_r1() -> dict:
    return load("valid-checkpoint-r1.json")


def test_checkpoint_valid_examples() -> None:
    check("checkpoint-r1", validate_record(valid_checkpoint_r1()) == [])
    check("checkpoint-r2", validate_record(load("valid-checkpoint-r2-chained.json")) == [])


def test_checkpoint_r1_must_have_null_prev() -> None:
    rec = copy.deepcopy(valid_checkpoint_r1())
    rec["prev_checkpoint_sha256"] = "a" * 64
    check("checkpoint-r1-null-prev", validate_record(rec) != [])


def test_checkpoint_r2_requires_prev_sha() -> None:
    rec = load("valid-checkpoint-r2-chained.json")
    rec["prev_checkpoint_sha256"] = None
    check("checkpoint-r2-needs-prev", validate_record(rec) != [])


def test_checkpoint_embedded_manifest_is_validated() -> None:
    rec = copy.deepcopy(valid_checkpoint_r1())
    del rec["manifest"]["authority"]
    check("checkpoint-embedded-manifest", validate_record(rec) != [])


def test_checkpoint_status_closed_list() -> None:
    rec = copy.deepcopy(valid_checkpoint_r1())
    rec["status"] = "paused"
    check("checkpoint-closed-status", validate_record(rec) != [])
```

Add the five calls to `main()` before the corpus test. Run the test file — expected: FAIL (`checkpoint@1 validation not implemented`).

- [ ] **Step 2: Write the examples**

`examples/valid-checkpoint-r1.json`:

```json
{
  "record": "checkpoint@1",
  "mission_id": "tracer-media-missing",
  "revision": 1,
  "status": "draft",
  "prev_checkpoint_sha256": null,
  "manifest": { "record": "mission-manifest@1", "mission_id": "tracer-media-missing", "created_utc": "2026-08-11T00:00:00Z", "authority": { "operator_ref": "operator:zach-stern", "instruction": "Reconcile the monitored-missing media backlog without re-grabbing over VPN.", "amendments": [], "permissions": ["repo:vanta:read", "repo:vanta:write-config"], "protected_state": ["download-clients:enabled-state"], "acceptable_costs": ["one working session per stage"] }, "scope": {"in": ["monitored-missing reconciliation"], "out": ["indexer changes", "VPN configuration"]}, "acceptance": {"required_tier": "declared-role-separation", "acceptor_ref": null}, "stop_rules": {"hold_if": ["any download client starts re-grabbing"], "stop_if": ["operator revokes"], "escalate_if": ["protected state would be touched"]}, "steward_ref": "agent:claude-code-session" },
  "state": {
    "frontier": "await operator approval",
    "notes": [],
    "unresolved_verdicts": []
  },
  "receipt_ids": [],
  "written_utc": "2026-08-11T00:00:01Z",
  "written_by": "agent:claude-code-session"
}
```

`valid-checkpoint-r2-chained.json`: copy r1, set `"revision": 2`, `"status": "active"`, `"prev_checkpoint_sha256": "4f2a09c1d8e7b6a5493827160f5e4d3c2b1a09f8e7d6c5b4a392817065f4e3d2"`, `"state": {"frontier": "stage 1: inventory", "notes": ["approved by operator"], "unresolved_verdicts": []}`, `"written_utc": "2026-08-11T00:10:00Z"`.
`invalid-checkpoint-r2-unchained.json`: same as r2 but `"prev_checkpoint_sha256": null`.
`invalid-checkpoint-bad-status.json`: r1 with `"status": "paused"`.

- [ ] **Step 3: Implement `validate_checkpoint`**

Replace the stub:

```python
CHECKPOINT_FIELDS = {
    "record", "mission_id", "revision", "status", "prev_checkpoint_sha256",
    "manifest", "state", "receipt_ids", "written_utc", "written_by",
}


def validate_checkpoint(rec: dict) -> list[str]:
    errors: list[str] = []
    _check_exact_fields(errors, rec, CHECKPOINT_FIELDS, "checkpoint")
    if errors:
        return errors
    _require(errors, isinstance(rec["revision"], int) and rec["revision"] >= 1,
             "revision", "integer >= 1 required")
    _require(errors, rec["status"] in STATES, "status",
             f"one of {sorted(STATES)} required")
    prev = rec["prev_checkpoint_sha256"]
    if rec.get("revision") == 1:
        _require(errors, prev is None, "prev_checkpoint_sha256",
                 "null required at revision 1")
    else:
        _require(errors, is_sha256(prev), "prev_checkpoint_sha256",
                 "64-hex sha256 of prior checkpoint file required")
    if isinstance(rec["manifest"], dict) \
            and rec["manifest"].get("record") == "mission-manifest@1":
        for err in validate_manifest(rec["manifest"]):
            errors.append(f"manifest.{err}")
        if rec["manifest"].get("mission_id") != rec["mission_id"]:
            errors.append("manifest.mission_id: must equal checkpoint mission_id")
    else:
        errors.append("manifest: embedded mission-manifest@1 required")
    state = rec["state"]
    ok = isinstance(state, dict) \
        and set(state) == {"frontier", "notes", "unresolved_verdicts"} \
        and isinstance(state.get("frontier"), str) and state["frontier"] \
        and _str_list(state.get("notes")) \
        and _str_list(state.get("unresolved_verdicts"))
    _require(errors, ok, "state",
             "frontier (non-empty str), notes[], unresolved_verdicts[] required")
    _require(errors, _str_list(rec["receipt_ids"]), "receipt_ids",
             "list of receipt id strings required")
    _require(errors, is_iso_utc(rec["written_utc"]), "written_utc",
             "ISO-8601 Z timestamp required")
    _require(errors, isinstance(rec["written_by"], str) and rec["written_by"],
             "written_by", "non-empty actor id required")
    return errors
```

- [ ] **Step 4: Schema doc**

`checkpoint.schema.json` — same documentation-contract style as Task 1 Step 5: `additionalProperties: false`, required = `CHECKPOINT_FIELDS`, `revision` integer minimum 1, `status` enum of the six states, `prev_checkpoint_sha256` type `["string","null"]` with the sha pattern, `manifest` `$ref`-described as `mission-manifest@1`, `state` object with `frontier`/`notes`/`unresolved_verdicts`, plus a `description` noting the r1-null / r≥2-sha chain rule lives in the verifier.

- [ ] **Step 5: Run tests, then commit**

Run: `python plugins/epistemic-skills/contracts/mission-custody/test_mission_custody.py` — expected `0 failures`.

```bash
git add plugins/epistemic-skills/contracts/mission-custody
git -c core.autocrlf=input commit -m "feat: mission-custody@1 checkpoint record" \
  -m "Signed-off-by: Zach Stern <zachstern@gmail.com>"
```

---

### Task 3: `receipt@1` + `acceptance-verdict@1`

**Files:**
- Modify: `verify_mission_custody.py` (replace both remaining stubs), `test_mission_custody.py` (append tests) — in the contract dir
- Create: `receipt.schema.json`, `acceptance-verdict.schema.json`
- Create: `examples/valid-receipt.json`, `examples/valid-verdict-pass-separated.json`, `examples/valid-verdict-fail.json`, `examples/invalid-verdict-self-certified.json`, `examples/invalid-verdict-operator-tier-wrong-acceptor.json`

**Interfaces:**
- Consumes: helpers + constants from Tasks 1–2.
- Produces: `validate_receipt(rec) -> list[str]`, `validate_acceptance_verdict(rec) -> list[str]`; constants `RECEIPT_FIELDS`, `VERDICT_FIELDS`.
- Semantic rules later tasks rely on: **`acceptor_id != worker_id` always**; tier `operator-accepted` additionally requires `operator_ref` non-empty and `acceptor_id == operator_ref`.

- [ ] **Step 1: Append failing tests**

```python
def test_receipt_valid() -> None:
    check("receipt-valid", validate_record(load("valid-receipt.json")) == [])


def test_receipt_after_hash_required() -> None:
    rec = load("valid-receipt.json")
    rec["after_sha256"] = "not-a-hash"
    check("receipt-after-hash", validate_record(rec) != [])


def test_verdict_valid_pass() -> None:
    check("verdict-pass", validate_record(load("valid-verdict-pass-separated.json")) == [])
    check("verdict-fail", validate_record(load("valid-verdict-fail.json")) == [])


def test_verdict_self_certification_refused() -> None:
    rec = load("valid-verdict-pass-separated.json")
    rec["acceptor_id"] = rec["worker_id"]
    check("verdict-no-self-cert", validate_record(rec) != [])


def test_verdict_operator_tier_binds_acceptor() -> None:
    rec = load("valid-verdict-pass-separated.json")
    rec["assurance_tier"] = "operator-accepted"
    check("verdict-operator-tier-acceptor", validate_record(rec) != [])
```

Add calls to `main()`. Run — expected FAIL (`receipt@1 validation not implemented`).

- [ ] **Step 2: Write the examples**

`examples/valid-receipt.json`:

```json
{
  "record": "receipt@1",
  "mission_id": "tracer-media-missing",
  "request_id": "req-0001",
  "actor": "agent:claude-code-session",
  "utc": "2026-08-11T00:20:00Z",
  "artifact_path": "notes/stage-1-inventory.md",
  "before_sha256": null,
  "after_sha256": "9e2b7c1a4d5f60897a6b5c4d3e2f10987b6a5c4d3e2f109876b5a4c3d2e1f098"
}
```

`examples/valid-verdict-pass-separated.json`:

```json
{
  "record": "acceptance-verdict@1",
  "mission_id": "tracer-media-missing",
  "revision": 6,
  "verdict": "PASS",
  "acceptor_id": "agent:acceptor-session",
  "worker_id": "agent:claude-code-session",
  "operator_ref": "operator:zach-stern",
  "assurance_tier": "declared-role-separation",
  "receipt_refs": ["req-0001"],
  "reason": "Artifact re-observed; hashes match the receipt chain.",
  "utc": "2026-08-11T01:00:00Z"
}
```

`valid-verdict-fail.json`: same shape, `"verdict": "FAIL"`, `"reason": "Inventory omits season packs."`
`invalid-verdict-self-certified.json`: valid-pass copy with `"acceptor_id": "agent:claude-code-session"`.
`invalid-verdict-operator-tier-wrong-acceptor.json`: valid-pass copy with `"assurance_tier": "operator-accepted"` (acceptor is not the operator_ref).

- [ ] **Step 3: Implement both validators**

```python
RECEIPT_FIELDS = {
    "record", "mission_id", "request_id", "actor", "utc",
    "artifact_path", "before_sha256", "after_sha256",
}
VERDICT_FIELDS = {
    "record", "mission_id", "revision", "verdict", "acceptor_id", "worker_id",
    "operator_ref", "assurance_tier", "receipt_refs", "reason", "utc",
}


def validate_receipt(rec: dict) -> list[str]:
    errors: list[str] = []
    _check_exact_fields(errors, rec, RECEIPT_FIELDS, "receipt")
    if errors:
        return errors
    for name in ("mission_id", "request_id", "actor", "artifact_path"):
        _require(errors, isinstance(rec[name], str) and rec[name],
                 name, "non-empty string required")
    _require(errors, is_iso_utc(rec["utc"]), "utc", "ISO-8601 Z required")
    _require(errors, rec["before_sha256"] is None or is_sha256(rec["before_sha256"]),
             "before_sha256", "null (new artifact) or 64-hex sha256 required")
    _require(errors, is_sha256(rec["after_sha256"]),
             "after_sha256", "64-hex sha256 required")
    return errors


def validate_acceptance_verdict(rec: dict) -> list[str]:
    errors: list[str] = []
    _check_exact_fields(errors, rec, VERDICT_FIELDS, "verdict")
    if errors:
        return errors
    _require(errors, isinstance(rec["revision"], int) and rec["revision"] >= 1,
             "revision", "integer >= 1 required")
    _require(errors, rec["verdict"] in VERDICTS, "verdict",
             f"one of {sorted(VERDICTS)} required")
    _require(errors, rec["assurance_tier"] in TIERS, "assurance_tier",
             f"one of {sorted(TIERS)} required")
    for name in ("acceptor_id", "worker_id", "operator_ref", "reason",
                 "mission_id"):
        _require(errors, isinstance(rec[name], str) and rec[name],
                 name, "non-empty string required")
    _require(errors, _str_list(rec["receipt_refs"]), "receipt_refs",
             "list of receipt id strings required")
    _require(errors, is_iso_utc(rec["utc"]), "utc", "ISO-8601 Z required")
    if not errors:
        _require(errors, rec["acceptor_id"] != rec["worker_id"],
                 "acceptor_id", "self-certification refused (== worker_id)")
        if rec["assurance_tier"] == "operator-accepted":
            _require(errors, rec["acceptor_id"] == rec["operator_ref"],
                     "acceptor_id",
                     "operator-accepted tier requires acceptor_id == operator_ref")
    return errors
```

- [ ] **Step 4: Schema docs**

`receipt.schema.json` and `acceptance-verdict.schema.json` in the Task 1 Step 5 style (`additionalProperties: false`, required = the field sets, enums for `verdict`/`assurance_tier`, sha patterns; `description` on acceptance-verdict states the two semantic rules verbatim: self-certification refused; operator tier binds acceptor to operator_ref).

- [ ] **Step 5: Run tests, then commit**

Run the test file — expected `0 failures` (corpus loop now covers 9 examples).

```bash
git add plugins/epistemic-skills/contracts/mission-custody
git -c core.autocrlf=input commit -m "feat: mission-custody@1 receipt + acceptance-verdict records" \
  -m "Signed-off-by: Zach Stern <zachstern@gmail.com>"
```

---

### Task 4: Contract README + SECURITY + CI workflow

**Files:**
- Create: `plugins/epistemic-skills/contracts/mission-custody/README.md`
- Create: `plugins/epistemic-skills/contracts/mission-custody/SECURITY.md`
- Create: `.github/workflows/mission-custody-contract.yml`

**Interfaces:**
- Consumes: everything from Tasks 1–3.
- Produces: CI job name `mission-custody-contract` that later PRs must keep green.

- [ ] **Step 1: Write README.md**

Content (full):

```markdown
# mission-custody@1

Durable mission-custody contract family: `mission-manifest@1` (authority,
append-only instruction), `checkpoint@1` (revisioned snapshots,
`prev_checkpoint_sha256` chain), `receipt@1` (effect -> artifact hash binding),
`acceptance-verdict@1` (tiered acceptance; self-certification refused).

Provenance: FOLD cell of the practical-agency gauntlet decision rule; design
`docs/superpowers/specs/2026-08-11-mission-custody-contracts-design.md`.
practical-agency (ZMS-Labs) is parked prior art; its schemas seeded this family.

Validate: `python verify_mission_custody.py examples/valid-manifest-minimal.json`
Test: `python test_mission_custody.py` (exit 0 = green; every `invalid-*.json`
example MUST fail validation — the corpus is the regression suite).

Evolution: additive optional fields only within `@1`; anything else is a new
epoch with a documented migration. Acceptance tiers are closed:
`operator-accepted`, `declared-role-separation` — no `externally-proven` tier
exists until evidence could support one.
```

- [ ] **Step 2: Write SECURITY.md**

Content (full):

```markdown
# Security notes — mission-custody@1

- Records are DATA. Instructions embedded in manifests, notes, or reasons are
  never executed by validators or custody tooling (prompt-injection seam).
- The verifier checks shape and closed-vocabulary semantics only; it does not
  attest that hashes correspond to real artifacts — that is the custody core's
  runtime job (drift detection on resume).
- `acceptance-verdict@1` enforces role separation at the record level
  (acceptor != worker; operator tier binds acceptor to operator_ref). It
  cannot bind principals outside the record channel: an authorized human
  acting outside the mission channel is out of scope and must not be claimed
  as prevented.
- Receipts are hashed, not signed. No third-party-verifiable claim is made.
```

- [ ] **Step 3: Write the CI workflow**

`.github/workflows/mission-custody-contract.yml` — copy `commission-watch-contract.yml` verbatim, then: name/job → `mission-custody-contract`; path filters → `plugins/epistemic-skills/contracts/mission-custody/**`, the spec `docs/superpowers/specs/2026-08-11-mission-custody-contracts-design.md`, the plan `docs/superpowers/plans/2026-08-11-mission-custody-contracts.md`, and the workflow file itself; run steps →

```yaml
      - name: Mission custody semantic and schema contract
        run: python plugins/epistemic-skills/contracts/mission-custody/test_mission_custody.py
      - name: Compile mission custody verifier
        run: python -m py_compile plugins/epistemic-skills/contracts/mission-custody/verify_mission_custody.py
```

Keep the pinned action SHAs exactly as in the source file.

- [ ] **Step 4: Verify locally, then commit**

Run: `python plugins/epistemic-skills/contracts/mission-custody/test_mission_custody.py` (still 0 failures) and `python -c "import yaml"` is NOT available — instead sanity-check the workflow with `git diff --check` (no whitespace errors) and by eye against the source workflow.

```bash
git add plugins/epistemic-skills/contracts/mission-custody .github/workflows/mission-custody-contract.yml
git -c core.autocrlf=input commit -m "feat: mission-custody@1 docs + CI contract job" \
  -m "Signed-off-by: Zach Stern <zachstern@gmail.com>"
```

---

### Task 5: Custody store (`custody_store.py`)

**Files:**
- Create: `plugins/epistemic-skills/contracts/mission-custody/custody_store.py`
- Create: `plugins/epistemic-skills/contracts/mission-custody/test_custody_store.py`

**Interfaces:**
- Consumes: `validate_record` from `verify_mission_custody` (every write validates first).
- Produces (exact signatures later tasks use):
  - `sha256_file(path: Path) -> str`
  - `sha256_bytes(data: bytes) -> str`
  - `atomic_write_json(path: Path, record: dict) -> str` — mkstemp + fsync + `os.replace`; returns sha256 of written bytes; raises `StoreError` on invalid record.
  - `class MissionStore(mission_dir: Path)` with: `write_checkpoint(record: dict) -> str` (enforces revision monotonicity + `prev_checkpoint_sha256` == sha of prior checkpoint file; r1 requires prev null), `load_latest() -> tuple[dict, Path]` (verifies the whole chain from r1; raises `ChainBroken`), `write_receipt(record: dict) -> Path` (filename `sha256(request_id.encode()) + ".json"`), `load_receipts() -> list[dict]`, `checkpoint_paths() -> list[Path]`.
  - Exceptions: `StoreError(Exception)`, `ChainBroken(StoreError)`.
- Layout produced: `missions/<mission_id>/checkpoints/r%08d.json`, `missions/<mission_id>/receipts/<sha>.json`.

- [ ] **Step 1: Write the failing tests** — full file `test_custody_store.py`:

```python
#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from custody_store import (  # noqa: E402
    ChainBroken, MissionStore, StoreError, atomic_write_json, sha256_file,
)

FAILURES: list[str] = []


def check(name: str, cond: bool) -> None:
    if not cond:
        FAILURES.append(name)
        print(f"FAIL {name}")
    else:
        print(f"ok   {name}")


def manifest() -> dict:
    return json.loads(
        (ROOT / "examples" / "valid-manifest-minimal.json").read_text(
            encoding="utf-8"))


def checkpoint(rev: int, prev: str | None, status: str = "draft") -> dict:
    return {
        "record": "checkpoint@1",
        "mission_id": "tracer-media-missing",
        "revision": rev,
        "status": status,
        "prev_checkpoint_sha256": prev,
        "manifest": manifest(),
        "state": {"frontier": "f", "notes": [], "unresolved_verdicts": []},
        "receipt_ids": [],
        "written_utc": "2026-08-11T00:00:01Z",
        "written_by": "agent:worker",
    }


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        mdir = Path(td) / "missions" / "tracer-media-missing"
        store = MissionStore(mdir)

        # invalid record refused before touching disk
        try:
            store.write_checkpoint({"record": "checkpoint@1"})
            check("store-refuses-invalid", False)
        except StoreError:
            check("store-refuses-invalid", True)

        sha1 = store.write_checkpoint(checkpoint(1, None))
        check("r1-written", (mdir / "checkpoints" / "r00000001.json").exists())

        # r2 with wrong prev refused
        try:
            store.write_checkpoint(checkpoint(2, "b" * 64, "active"))
            check("store-refuses-bad-chain", False)
        except StoreError:
            check("store-refuses-bad-chain", True)

        store.write_checkpoint(checkpoint(2, sha1, "active"))
        latest, path = store.load_latest()
        check("latest-is-r2", latest["revision"] == 2)

        # tamper with r1 on disk -> chain verification must fail
        p1 = mdir / "checkpoints" / "r00000001.json"
        p1.write_text(p1.read_text(encoding="utf-8").replace(
            "await operator approval", "tampered"), encoding="utf-8")
        try:
            store.load_latest()
            check("chain-tamper-detected", False)
        except ChainBroken:
            check("chain-tamper-detected", True)

        # receipts round-trip
        receipt = json.loads((ROOT / "examples" / "valid-receipt.json").read_text(
            encoding="utf-8"))
        rp = store.write_receipt(receipt)
        check("receipt-written", rp.exists())
        check("receipt-loaded", store.load_receipts() == [receipt])

    print(f"\n{len(FAILURES)} failures")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Run to verify failure** — `python .../test_custody_store.py` → `ModuleNotFoundError: custody_store`.

- [ ] **Step 3: Implement `custody_store.py`** — full module:

```python
#!/usr/bin/env python3
"""Durable mission store: atomic JSON writes, checkpoint hash chain, receipts."""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path

from verify_mission_custody import validate_record


class StoreError(Exception):
    pass


class ChainBroken(StoreError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def atomic_write_json(path: Path, record: dict) -> str:
    errors = validate_record(record)
    if errors:
        raise StoreError(f"invalid record for {path.name}: {errors[:3]}")
    path.parent.mkdir(parents=True, exist_ok=True)
    data = (json.dumps(record, indent=1, sort_keys=True) + "\n").encode("utf-8")
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise
    return sha256_bytes(data)


class MissionStore:
    def __init__(self, mission_dir: Path) -> None:
        self.mission_dir = Path(mission_dir)
        self.checkpoints_dir = self.mission_dir / "checkpoints"
        self.receipts_dir = self.mission_dir / "receipts"

    def checkpoint_paths(self) -> list[Path]:
        if not self.checkpoints_dir.is_dir():
            return []
        return sorted(self.checkpoints_dir.glob("r????????.json"))

    def _path_for(self, revision: int) -> Path:
        return self.checkpoints_dir / f"r{revision:08d}.json"

    def write_checkpoint(self, record: dict) -> str:
        errors = validate_record(record)
        if errors:
            raise StoreError(f"invalid checkpoint: {errors[:3]}")
        revision = record["revision"]
        existing = self.checkpoint_paths()
        expected_rev = len(existing) + 1
        if revision != expected_rev:
            raise StoreError(
                f"revision {revision} out of order; expected {expected_rev}")
        if revision == 1:
            if record["prev_checkpoint_sha256"] is not None:
                raise StoreError("revision 1 must have null prev sha")
        else:
            prior_sha = sha256_file(existing[-1])
            if record["prev_checkpoint_sha256"] != prior_sha:
                raise StoreError("prev_checkpoint_sha256 does not match prior file")
        return atomic_write_json(self._path_for(revision), record)

    def load_latest(self) -> tuple[dict, Path]:
        paths = self.checkpoint_paths()
        if not paths:
            raise StoreError(f"no checkpoints under {self.checkpoints_dir}")
        prev_sha: str | None = None
        for path in paths:
            record = json.loads(path.read_text(encoding="utf-8"))
            errors = validate_record(record)
            if errors:
                raise ChainBroken(f"{path.name}: invalid: {errors[:3]}")
            if record["prev_checkpoint_sha256"] != prev_sha:
                raise ChainBroken(f"{path.name}: chain mismatch")
            prev_sha = sha256_file(path)
        return record, paths[-1]

    def write_receipt(self, record: dict) -> Path:
        errors = validate_record(record)
        if errors:
            raise StoreError(f"invalid receipt: {errors[:3]}")
        name = sha256_bytes(record["request_id"].encode("utf-8")) + ".json"
        path = self.receipts_dir / name
        atomic_write_json(path, record)
        return path

    def load_receipts(self) -> list[dict]:
        if not self.receipts_dir.is_dir():
            return []
        return [json.loads(p.read_text(encoding="utf-8"))
                for p in sorted(self.receipts_dir.glob("*.json"))]
```

- [ ] **Step 4: Run tests** — both `test_custody_store.py` and `test_mission_custody.py` → 0 failures.
- [ ] **Step 5: Commit** — `feat: custody store with atomic chained checkpoints` (same DCO trailer pattern).

---

### Task 6: Mission lifecycle (`custody_mission.py`)

**Files:**
- Create: `plugins/epistemic-skills/contracts/mission-custody/custody_mission.py`
- Create: `plugins/epistemic-skills/contracts/mission-custody/test_custody_mission.py`

**Interfaces:**
- Consumes: `MissionStore`, `StoreError`, `sha256_bytes`, `sha256_file` (Task 5); `TIERS`, `VERDICTS` (Task 1).
- Produces (exact API the CLI binds):
  - `class Mission` — constructor `Mission(store: MissionStore, workspace: Path, actor: str)`; classmethods `Mission.open(workspace, mission_id, instruction, operator_ref, steward_ref, required_tier, actor, scope_in, scope_out, permissions, protected_state) -> Mission` (writes manifest + checkpoint r1 `draft`) and `Mission.load(workspace, actor) -> Mission` (**pathless**: scans `workspace/missions/*/checkpoints/`, requires exactly one mission whose latest status is not in `{"completed","cancelled"}`; zero → `NoActiveMission`, several → `MultipleActiveMissions`).
  - Methods, each writing the next checkpoint: `approve() -> int` (draft→active; records note "approved"), `record_effect(artifact_relpath: str, content: str, request_id: str) -> dict` (broker write inside workspace: refuses `..` and absolute paths, captures before/after sha, writes artifact + receipt, appends receipt id; returns the receipt), `note(text: str) -> int`, `set_frontier(text: str) -> int`, `resume() -> list[str]` (chain-verify + **drift detection**: for every receipt, live file hash vs `after_sha256`; mismatches → status `reopened`, marker `"RECONCILIATION:<artifact_path>"` appended to `unresolved_verdicts`; returns mismatched paths), `reconcile(artifact_relpath, content, request_id) -> dict` (repair effect; clears that `RECONCILIATION:` marker; if none left and status `reopened` → `active`), `begin_verification() -> int` (active→verifying; refuses if `unresolved_verdicts`), `record_verdict(verdict: str, acceptor_id: str, assurance_tier: str, reason: str) -> int` (validates an `acceptance-verdict@1`; **PASS**: refuses unless status `verifying`, tier meets manifest `required_tier`, acceptor ≠ steward; → `completed`. **FAIL**: appends `"FAIL:<reason>"` marker, → `reopened`. **INCONCLUSIVE**: note only), `clear_fail(reason_fragment: str, receipt_request_id: str) -> int` (**the FAIL-clear path**: requires a receipt written after the FAIL, removes the matching `FAIL:` marker), `cancel(reason) -> int`, `status() -> dict` (latest checkpoint).
  - Exceptions: `CustodyError(Exception)`, `NoActiveMission(CustodyError)`, `MultipleActiveMissions(CustodyError)`, `IllegalTransition(CustodyError)`, `AcceptanceRefused(CustodyError)`.
  - Authority invariant enforced everywhere: `manifest.authority.instruction` byte-identical across all checkpoints (amendments append; a changed instruction raises `CustodyError`).
- Timestamps: module-level `def now_utc() -> str` using `datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")`.

- [ ] **Step 1: Write the failing tests** — `test_custody_mission.py`, same harness pattern (check/FAILURES/main). Required test functions, each with real asserts:

```python
# All operate in a tempfile.TemporaryDirectory() workspace.
def test_open_creates_draft_r1(): ...
    # Mission.open(...) -> status()["revision"] == 1, status "draft",
    # manifest instruction verbatim.
def test_pathless_load_single_active(): ...
    # open + approve, then Mission.load(workspace, actor="agent:second")
    # finds it WITHOUT being given the mission id.
def test_load_refuses_zero_and_multiple(): ...
    # empty workspace -> NoActiveMission; open two missions -> MultipleActiveMissions.
def test_effect_writes_receipt_and_artifact(): ...
    # record_effect("notes/a.md", "hello", "req-1"): file exists, receipt
    # after_sha256 == sha of file bytes, checkpoint receipt_ids contains id.
def test_effect_refuses_escape(): ...
    # record_effect("../outside.md", ...) and ("C:/x", ...) raise CustodyError.
def test_resume_detects_drift_and_reconcile_clears(): ...
    # effect; overwrite artifact directly on disk; resume() returns the path,
    # status "reopened", marker "RECONCILIATION:notes/a.md" present;
    # reconcile("notes/a.md", "hello", "req-2") -> marker gone, status "active".
def test_instruction_immutable(): ...
    # tamper latest checkpoint manifest instruction via store internals ->
    # next operation raises CustodyError.
def test_accept_requires_verifying_and_separation(): ...
    # record_verdict PASS while "active" -> IllegalTransition;
    # begin_verification; PASS with acceptor == steward -> AcceptanceRefused;
    # PASS with distinct acceptor at required tier -> status "completed".
def test_fail_is_clearable(): ...          # THE PA-dead-end regression test
    # begin_verification; record_verdict FAIL -> "reopened" + FAIL marker;
    # record_effect remediation; clear_fail(...) -> marker gone;
    # begin_verification; record_verdict PASS (distinct acceptor) -> "completed".
def test_operator_tier(): ...
    # manifest required_tier "operator-accepted": PASS at
    # declared-role-separation -> AcceptanceRefused; PASS with
    # acceptor_id == operator_ref, tier operator-accepted -> completed.
```

Write each `...` body out in full in the file (the assertions described in the comments are the required content — an implementer writes them as real code against the Produces API above).

- [ ] **Step 2: Run to verify failure** — `ModuleNotFoundError: custody_mission`.
- [ ] **Step 3: Implement `custody_mission.py`** against the exact Produces API. Implementation notes an engineer needs: every mutating method (a) loads latest via `store.load_latest()`, (b) verifies the instruction invariant against checkpoint r1, (c) builds the next checkpoint dict (revision+1, `prev_checkpoint_sha256` = sha of latest file via `sha256_file`), (d) `store.write_checkpoint`. `record_verdict` builds and validates a full `acceptance-verdict@1` record with `worker_id = manifest["steward_ref"]` and validates via `validate_record` before applying transition rules; store the verdict record at `missions/<id>/verdicts/<revision>-<verdict>.json` via `atomic_write_json`. Status transitions allowed: draft→active (approve), draft/active/reopened/verifying→cancelled (cancel), active→verifying (begin_verification), verifying→completed (PASS), verifying→reopened (FAIL), reopened→active (last marker cleared via reconcile/clear_fail). Everything else raises `IllegalTransition`.
- [ ] **Step 4: Run all three test files** — 0 failures; check total line count: `wc -l custody_store.py custody_mission.py` — flag if the two already exceed ~600 (budget for the CLI).
- [ ] **Step 5: Commit** — `feat: mission lifecycle with drift reanchoring and clearable FAIL`.

---### Task 7: CLI (`custody_cli.py`)

**Files:**
- Create: `plugins/epistemic-skills/contracts/mission-custody/custody_cli.py`
- Create: `plugins/epistemic-skills/contracts/mission-custody/test_custody_cli.py`

**Interfaces:**
- Consumes: the full `Mission` API (Task 6).
- Produces: `python custody_cli.py <command> --workspace W --actor A [...]` with commands and exact flags:
  - `open --mission-id ID --instruction TEXT --operator REF --steward REF [--tier TIER] [--scope-in X ...] [--scope-out X ...] [--permission X ...] [--protected X ...]`
  - `approve` · `status` (prints latest checkpoint JSON to stdout) · `note --text T` · `frontier --text T`
  - `effect --path REL --content TEXT --request-id ID`
  - `resume` (prints drift list; exit 3 when drift found — a *visible*, non-zero signal)
  - `reconcile --path REL --content TEXT --request-id ID`
  - `verify` · `accept --verdict V --acceptor REF --tier TIER --reason TEXT`
  - `clear-fail --match FRAGMENT --request-id ID` · `cancel --reason TEXT`
  - Exit codes: 0 success · 2 usage/refusal (`CustodyError` subclasses print the exception class name + message to stderr) · 3 drift detected on resume.
  - **No `--mission-path` or `--mission-id` on any command except `open`** — discovery is pathless by contract (the argparse test asserts their absence).
- [ ] **Step 1: Failing tests** — `test_custody_cli.py` drives the CLI via `subprocess.run([sys.executable, "custody_cli.py", ...])` in a temp workspace: open→approve→effect→status round-trip (parse stdout JSON, assert revision/status); drift scenario asserting exit code 3; `accept` self-cert asserting exit 2 + `AcceptanceRefused` on stderr; an AST test (`ast.parse`) walking `custody_cli.py` asserting no argparse argument named `--mission-path` or `--mission-id` outside the `open` subparser.
- [ ] **Step 2: Run to verify failure.**
- [ ] **Step 3: Implement** — thin argparse dispatch onto `Mission`; no logic beyond translation; `PYTHONIOENCODING`-safe (ASCII-only output).
- [ ] **Step 4: Run all four test files** — 0 failures; `wc -l custody_*.py` total must be ≤ ~800.
- [ ] **Step 5: Commit** — `feat: custody CLI with pathless resume and visible drift exit`.

---

### Task 8: Three-subprocess kill/resume/repair proof

**Files:**
- Create: `plugins/epistemic-skills/contracts/mission-custody/test_custody_process_proof.py`

**Interfaces:**
- Consumes: `custody_cli.py` only (black-box through subprocesses — that is the point).
- Produces: the executable continuity proof CI runs.

- [ ] **Step 1: Write the proof test** (this task is test-only; it must pass against Task 7's code — if it fails, the defect is in Tasks 5–7 and is fixed there). Full scenario, mirroring the fold-spike runner:
  1. **Process A** (`subprocess.Popen`): `open` + `approve` + `effect notes/proof.md "state-1" req-a1` + a `frontier` write, then **`proc.kill()`** immediately after the CLI process for `frontier` returns (each CLI call is its own process; "kill" here = kill a still-running `effect` invocation launched with a `--content` large enough to observe, OR simpler and deterministic: run `effect` to completion, then kill a deliberately-hung fourth invocation started with an interposed `python -c` wrapper that sleeps after import — assert the wrapper died pre-checkpoint and the store shows no partial file: `checkpoints/` contains no `*.tmp`).
  2. **Drift plant**: overwrite `notes/proof.md` directly with different bytes.
  3. **Process B**: `resume` with NO mission id → asserts exit 3 and stderr/stdout names `notes/proof.md`; `status` shows `reopened` + `RECONCILIATION:notes/proof.md`; `reconcile` repairs; `status` shows `active`.
  4. **Process C**: `verify`, then `accept --verdict PASS --acceptor agent:worker ...` (same as steward) → exit 2 `AcceptanceRefused`; `accept --verdict FAIL --acceptor agent:acceptor-2 --tier declared-role-separation --reason "missing section"` → `reopened`; `effect` remediation + `clear-fail` + `verify` + `accept --verdict PASS --acceptor agent:acceptor-2 ...` → final `status` `completed`, revision ≥ 10, instruction byte-identical to r1's.
  5. Independent re-verification from disk: recompute the full checkpoint sha chain in the test process; assert no `.tmp` files anywhere under `missions/`.
- [ ] **Step 2: Run it** — `python .../test_custody_process_proof.py` → 0 failures. Fix any defect in the module that owns it (with its own unit test first), never by weakening the proof.
- [ ] **Step 3: Add the proof + the three unit test files to the CI workflow** (four new `run:` lines in `mission-custody-contract.yml`).
- [ ] **Step 4: Commit** — `test: three-subprocess kill/resume/repair continuity proof`.

---

### Task 9: The `manifest` skill (Claude Code binding)

**Files:**
- Create: `plugins/epistemic-skills/skills/manifest/SKILL.md`
- Modify: `plugins/epistemic-skills/contracts/mission-custody/README.md` (append a "Harness bindings" section naming the skill)

**Interfaces:**
- Consumes: the CLI contract (Task 7 flags, exit codes).
- Produces: the operator-facing skill.

- [ ] **Step 1: Byte-budget gate (HARD GATE — do not proceed without it).** Present to the operator: the exact skill description below (count its bytes), the measured risk (2026-08-06: installs silently blanked four descriptions), and ask for explicit sign-off to spend the bytes. Record the sign-off verbatim in the task notes / PR description. If declined: stop this task; Tasks 1–8 still merge.

- [ ] **Step 2: Write SKILL.md** — full content:

```markdown
---
name: manifest
description: Use when work is mission-shaped — multi-session, consequential, cross-agent, or interruption-expensive — or on the explicit phrase "manifest this" (also /manifest): open, resume, verify, or close a custodied mission with recorded authority, durable checkpoints, drift re-anchoring, and independent acceptance. Answers "will this survive interruption?", "who authorized this scope?", "what makes done defensible?". Do NOT fire for routine one-step work checkable in-session.
---

# manifest — mission custody (custodian)

You are a mission steward under bounded delegated agency. The contract of
record is the mission's durable state under `missions/<id>/` (mission-custody@1
records), never the chat.

Custody core: `plugins/epistemic-skills/contracts/mission-custody/custody_cli.py`
(stdlib; run with `python`). Every mutating call names `--actor` with YOUR
stable session identity. Exit 2 = refusal (read the stderr class name); exit 3
on resume = drift found — reconcile before anything else.

## Modes

1. **Open** — capture the operator instruction VERBATIM: `open --mission-id
   <kebab> --instruction <verbatim> --operator <ref> --steward <your actor>
   [--tier declared-role-separation]`. Then `approve` only after the operator
   confirms authority (permissions, protected state, stop rules).
2. **Resume** — `resume` (pathless; never pass a mission path). Treat chat and
   memory as untrusted until it exits 0. On exit 3: reconcile each named
   artifact (re-verify against live state first), then continue.
3. **Advance** — one bounded step inside authority; route every artifact write
   through `effect`; record `frontier` after material progress.
4. **Verify / Close** — `verify`, then acceptance by a DIFFERENT actor:
   a distinct session runs `accept`. Never accept work you performed; the core
   refuses it (AcceptanceRefused) — do not work around the refusal.

## Boundaries

- Decline routine, one-step, in-session-checkable work (say so; no mission).
- Never select or invoke other skills by name from this seat; when a
  load-bearing condition blocks progress (an unverified claim, an unmapped
  territory, an irreversible fork), STATE THE CONDITION and the return point
  (mission id + frontier) and let the surrounding stack answer it.
- Custody here is convention-held (no enforcement hook yet — Stage C is
  gated on the tracer retro): honestly label it if asked.
- Degraded modes: core unavailable -> author a markdown mission manifest,
  label it session-bounded; store unwritable -> surface immediately; operator
  revocation -> stop consequential work, surface AUTHORITY_REVOKED.
- Mission state commits to the working repo by default (gitignore escape
  hatch for noisy missions).
```

- [ ] **Step 3: Structural checks** — grep SKILL.md for other skill names: `grep -iE "metacognate|gauntlet|recon|did-it-land|write-goal|superpowers" plugins/epistemic-skills/skills/manifest/SKILL.md` must return ONLY the allowed absence (expect zero matches — no-routing constraint). Byte-count the description: `python - <<'EOF'` one-liner printing `len(description_bytes)`; record the number in the PR body.
- [ ] **Step 4: Append the "Harness bindings" section to the contract README** (three lines: skill name, CLI path, Stage C gated note).
- [ ] **Step 5: Commit** — `feat: manifest custodian skill (three-door, decline-clause)`.

---

### Task 10: Live UAT, PR, and tracer handoff

**Files:**
- Create: `docs/superpowers/plans/2026-08-11-mission-custody-tracer-retro-template.md`
- No other repo files — this task is verification + handoff.

**Interfaces:**
- Consumes: everything.
- Produces: a pushed branch, an open PR, and the armed tracer.

- [ ] **Step 1: Full local suite** — run all five test files + `python -m compileall -q plugins/epistemic-skills/contracts/mission-custody` → all green, verbatim output captured for the PR body.
- [ ] **Step 2: Live UAT (evidence-locked-uat skill governs)** — in a scratch workspace, drive one real mission through the skill text's exact commands from a live session: open→approve→effect→kill session→fresh session resume (pathless)→plant drift→reconcile→verify→accept from a second session identity. Save the transcript + exit codes as the UAT packet under the scratch workspace; reference it (path + sha) in the PR body. This is Stage B's oracle-adequate check: the skill's documented commands, not the test suite, are what the UAT exercises.
- [ ] **Step 3: Write the tracer retro template** — headings: Mission id · Sessions (count, dates) · Interruptions survived (what died, what resumed) · Drift events (detected? honest?) · Acceptance (tier, actor separation real?) · **Did custody change the outcome?** (the adoption falsifier, answered plainly) · Stage C decision input (build teeth / stay convention-held / park).
- [ ] **Step 4: Push + PR (operator-gated)** — `git push -u origin spec/mission-custody-contracts-design`; open a PR titled `feat: mission-custody@1 contracts + custody core + manifest skill` whose body carries: spec+plan links, test output, UAT packet ref, byte-budget sign-off quote, the Stage C gate statement, and the practical-agency provenance paragraph from the spec. **Ask the operator before pushing** if this session hasn't already been told to.
- [ ] **Step 5: Arm the tracer** — with the operator, pin the exact tracer mission id (default candidate: the monitored-missing reconciliation arc), open it via `/manifest` in the target repo, and schedule the retro against the template. Stage C is decided by that retro, not by this plan.

---

## Self-review (performed at write time)

- **Spec coverage:** contracts §→Tasks 1–4 · core §→Tasks 5–7 (incl. FAIL-clearable, pathless discovery, drift, acceptance tiers) · proof→Task 8 · skill three-doors/decline/no-routing→Task 9 · degraded modes→SKILL.md Boundaries + store/CLI refusals · testing & success criterion→Tasks 8/10 · non-goals: no ECS wiring, no Codex port, no signing, no second skill — absent everywhere by construction. Stage C: explicitly out of scope (Tasks 9 Step 2 label + Task 10 retro gate).
- **Placeholders:** Task 6 Step 1 lists test bodies as specified assertions with a written instruction to expand — intentional (the Produces API fully determines them); no TBD/TODO remains.
- **Type consistency:** `validate_record`/`MissionStore`/`Mission`/CLI flag names cross-checked across tasks; state list and tier vocabulary identical in Tasks 1, 6, 9.
