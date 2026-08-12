# Stage-C Custody Enforcement Hook Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship es#117 — a PreToolUse custody-enforcement hook that gates a mission's real actuators (arr API mutations, filesystem moves) on operator-approved, manifest-resident guard rules, shipped inert.

**Architecture:** Two additive optional fields on `mission-manifest@1` authority (`guard_mode`, `actuator_guards`); a new pure evaluator module `custody_gate.py`; a `gate` CLI verb; a stdlib hook script `custody_hook.py` with per-harness payload adapters (claude/kimi/codex/cursor/gemini(+agy)/generic); per-harness wiring files. Hook never mutates chain state; matches append to `missions/<id>/guard-log.jsonl`.

**Tech Stack:** Python 3.11 stdlib only (repo constraint — validation is hand-rolled, no jsonschema). No new dependencies.

**Spec:** `docs/superpowers/specs/2026-08-12-stage-c-custody-hook-design.md` (same worktree).

## Global Constraints

- All work in worktree `Y:/dev/es-wt-stage-c-hook`, branch `agent/stage-c-custody-hook` (cut from ES main `2931d386`). Never touch the main checkout (RULE-028) or auditor worktrees.
- Contract dir referred to below as `MC/` = `plugins/epistemic-skills/contracts/mission-custody/`.
- Stdlib only. Validation lives in `verify_mission_custody.py` (hand-rolled); `atomic_write_json` validates every write — a manifest carrying guard fields cannot be written until Task 1 lands.
- **Case folding: NEVER `str.casefold()`** (ß→ss expansion retires custody of the wrong file — PR #122). Reuse `_ascii_case_fold` / `_normalize_relpath` from `custody_mission.py`.
- Over-matching bias: a false block names its rule and is recoverable via amend; a false allow silently retires custody. Regexes err broad.
- Tests are plain scripts (`python test_x.py`, exit 0 = green), using the module-level `FAILURES` list + `check(name, cond)` pattern from existing test files. No pytest.
- Black-box CLI tests drive `custody_cli.py` via `subprocess` exactly as `test_custody_cli.py` does.
- **Every `git commit` step requires an explicit operator GO before execution** (fleet consent guard, per-session). Commits are DCO-signed (`git commit --signoff`). Batches of commits per GO are fine if the operator says so.
- Exit-code contract (existing, do not regress): 0 success; 2 usage/refusal; 3 drift on `resume` / breaks on `audit`. `gate` adds: 2 = block.
- The hook must fail open: any exception, malformed payload, missing mission, or timeout → exit 0. Denial travels ONLY via the deliberate exit-2/decision-JSON path.
- MSYS2 on this machine: `export MSYS_NO_PATHCONV=1 MSYS2_ARG_CONV_EXCL='*'` for path/revspec args.

---

### Task 1: Validator + schema support for guard fields

**Files:**
- Modify: `MC/verify_mission_custody.py` (AUTHORITY_FIELDS at lines 34-37; `validate_manifest` at lines 80-135)
- Modify: `MC/mission-manifest.schema.json`
- Create: `MC/examples/valid-manifest-guards.json`
- Create: `MC/examples/invalid-manifest-guard-bad-mode.json`
- Create: `MC/examples/invalid-manifest-guard-empty-rule.json`
- Create: `MC/examples/invalid-manifest-guard-bad-regex.json`
- Create: `MC/examples/invalid-manifest-guard-mode-without-guards.json`
- Create: `MC/examples/invalid-manifest-guard-unknown-field.json`
- Test: `MC/test_mission_custody.py` (add tests at end; it already walks `examples/`)

**Interfaces:**
- Consumes: nothing new.
- Produces: `validate_manifest` accepts authority objects optionally carrying `guard_mode` (`"audit"|"enforce"`) and `actuator_guards` (list of guard rules); every other authority object validates exactly as before. Guard rule shape: `{"name": str, "tool_names": [str...], "command_regexes": [str...], "path_globs": [str...]}` — `name`/`tool_names` required, both pattern lists required (either may be `[]`, but at least one pattern total across the two), no unknown keys. Later tasks rely on this exact rule shape.

- [ ] **Step 1: Write the failing tests**

Append to `MC/test_mission_custody.py`:

```python
def test_manifest_guards_valid_example() -> None:
    check("manifest-guards-valid-example",
          validate_record(load("valid-manifest-guards.json")) == [])


def test_manifest_guard_examples_invalid() -> None:
    for name in (
        "invalid-manifest-guard-bad-mode.json",
        "invalid-manifest-guard-empty-rule.json",
        "invalid-manifest-guard-bad-regex.json",
        "invalid-manifest-guard-mode-without-guards.json",
        "invalid-manifest-guard-unknown-field.json",
    ):
        check(f"manifest-{name}", validate_record(load(name)) != [])


def test_manifest_guards_optional_absent() -> None:
    # The pre-change minimal manifest must still validate: fields are additive.
    check("manifest-guards-optional-absent",
          validate_record(valid_manifest()) == [])


def test_manifest_guard_rules_shape() -> None:
    rec = copy.deepcopy(valid_manifest())
    rec["authority"]["guard_mode"] = "audit"
    rec["authority"]["actuator_guards"] = [{
        "name": "arr", "tool_names": ["Bash"],
        "command_regexes": ["7878"], "path_globs": []}]
    check("manifest-guard-rules-inline-valid", validate_record(rec) == [])
    bad = copy.deepcopy(rec)
    bad["authority"]["actuator_guards"][0]["tool_names"] = []
    check("manifest-guard-empty-tool-names", validate_record(bad) != [])
```

- [ ] **Step 2: Create the example files**

`valid-manifest-guards.json` = `valid-manifest-minimal.json` plus, inside `authority`:

```json
"guard_mode": "audit",
"actuator_guards": [
  {"name": "arr-api-mutations", "tool_names": ["Bash"],
   "command_regexes": ["https?://[^\\s]*:(7878|8989|8686|9696)/api/"],
   "path_globs": []},
  {"name": "media-fs-moves", "tool_names": ["Bash", "Write", "Edit"],
   "command_regexes": ["\\b(mv|robocopy|rsync|Move-Item)\\b[^\\n]*[Mm]edia"],
   "path_globs": ["M:/Media/**", "//10.10.10.107/Media/**"]}
]
```

`invalid-manifest-guard-bad-mode.json`: same but `"guard_mode": "block"`.
`invalid-manifest-guard-empty-rule.json`: rule with `"command_regexes": []` and `"path_globs": []`.
`invalid-manifest-guard-bad-regex.json`: `"command_regexes": ["([unclosed"]`.
`invalid-manifest-guard-mode-without-guards.json`: `"guard_mode": "audit"` with no `actuator_guards` key.
`invalid-manifest-guard-unknown-field.json`: rule carrying `"action": "block"`.

- [ ] **Step 3: Run tests to verify they fail**

Run: `python MC/test_mission_custody.py`
Expected: FAIL on all five new `manifest-guard*`/`manifest-invalid*` checks (unknown-field errors).

- [ ] **Step 4: Implement validator support**

In `MC/verify_mission_custody.py`:

```python
# after AUTHORITY_FIELDS (line 37)
AUTHORITY_OPTIONAL_FIELDS = {"guard_mode", "actuator_guards"}
GUARD_MODES = {"audit", "enforce"}
GUARD_RULE_FIELDS = {"name", "tool_names", "command_regexes", "path_globs"}
GUARD_RULE_REQUIRED = {"name", "tool_names", "command_regexes", "path_globs"}
```

In `validate_manifest`, replace the exact-fields call on authority with required+allowed handling, then add guard validation:

```python
    # was: _check_exact_fields(errors, auth, AUTHORITY_FIELDS, "authority")
    for key in auth:
        if key not in AUTHORITY_FIELDS | AUTHORITY_OPTIONAL_FIELDS:
            errors.append(f"authority.{key}: unknown field")
    for key in AUTHORITY_FIELDS:
        if key not in auth:
            errors.append(f"authority.{key}: missing")
    if not errors:
        # ... existing operator_ref/instruction/amendments/list checks unchanged ...
        mode = auth.get("guard_mode")
        guards = auth.get("actuator_guards")
        if mode is not None:
            _require(errors, mode in GUARD_MODES,
                     "authority.guard_mode", "must be 'audit' or 'enforce'")
            _require(errors, isinstance(guards, list) and bool(guards),
                     "authority.guard_mode",
                     "guard_mode requires a non-empty actuator_guards list")
        if guards is not None:
            ok = isinstance(guards, list)
            if ok:
                for rule in guards:
                    if not isinstance(rule, dict) or set(rule) != GUARD_RULE_FIELDS:
                        ok = False
                        break
                    if not (isinstance(rule["name"], str) and rule["name"]):
                        ok = False
                        break
                    if not _str_list(rule["tool_names"]):
                        ok = False
                        break
                    patterns = []
                    for field in ("command_regexes", "path_globs"):
                        value = rule[field]
                        if not isinstance(value, list) or not all(
                                isinstance(p, str) for p in value):
                            ok = False
                            break
                        patterns.extend(value)
                    if not ok:
                        break
                    if not patterns:
                        ok = False  # a patternless rule matches nothing -> inert by accident
                        break
                    for pattern in rule["command_regexes"]:
                        try:
                            re.compile(pattern)
                        except re.error:
                            ok = False
                            break
                    if not ok:
                        break
            _require(errors, ok, "authority.actuator_guards",
                     "list of {name, tool_names, command_regexes, path_globs} "
                     "rules; tool_names non-empty; >=1 pattern; regexes must compile")
```

Also update `MC/mission-manifest.schema.json`: add to `authority.required`… nothing (fields are optional); add to `authority.properties`:

```json
"guard_mode": {"enum": ["audit", "enforce"]},
"actuator_guards": {"type": "array", "minItems": 1, "items": {
  "type": "object", "additionalProperties": false,
  "required": ["name", "tool_names", "command_regexes", "path_globs"],
  "properties": {
    "name": {"type": "string", "minLength": 1},
    "tool_names": {"type": "array", "items": {"type": "string", "minLength": 1}, "minItems": 1},
    "command_regexes": {"type": "array", "items": {"type": "string"}},
    "path_globs": {"type": "array", "items": {"type": "string"}}
  }}}
```

(`additionalProperties: false` on authority stays — the schema json now names the two new keys.)

- [ ] **Step 5: Run tests to verify they pass**

Run: `python MC/test_mission_custody.py`
Expected: PASS all (exit 0), including every pre-existing invalid-* example still failing validation.

- [ ] **Step 6: Commit (operator GO required)**

```bash
git add plugins/epistemic-skills/contracts/mission-custody/
git commit --signoff -m "feat(mission-custody): validate optional actuator_guards + guard_mode on mission-manifest@1 (refs #117)"
```

---

### Task 2: Mission lifecycle support (open / amend / tamper rule)

**Files:**
- Modify: `MC/custody_mission.py` (`Mission.open` lines 128-178; `_verify_manifest` lines 220-265; `amend_authority` lines 495-525)
- Test: `MC/test_custody_mission.py` (append)

**Interfaces:**
- Consumes: Task 1's validator (writes with guard fields now pass `atomic_write_json`).
- Produces:
  - `Mission.open(..., guard_mode: str | None = None, actuator_guards: list | None = None)` — both keyword-only, appended after `acceptable_costs`. Fields are written into `authority` only when `actuator_guards is not None` (`guard_mode` written only when not None).
  - `Mission.amend_authority(text, *, guard_mode=_UNSET, actuator_guards=_UNSET)` — sentinel `_UNSET = object()` at module level; a non-sentinel value REPLACES the field in the amended manifest (empty list clears guards).
  - `_verify_manifest` new rule: guard fields may differ from the origin manifest ONLY when `authority.amendments` is non-empty on the latest checkpoint; otherwise `CustodyError("tampered")`.

- [ ] **Step 1: Write the failing tests**

Append to `MC/test_custody_mission.py` (follow its existing fixture style for creating a workspace + mission; reuse its helpers):

```python
def test_open_with_guards_roundtrip() -> None:
    # open a mission with guards + mode; checkpoint r1 must validate and carry them
    ws = _tmp_workspace()  # use the file's existing workspace helper
    guards = [{"name": "g", "tool_names": ["Bash"],
               "command_regexes": ["rm"], "path_globs": []}]
    m = Mission.open(ws, "guard-open", "do the thing", "operator:test",
                     "agent:test", actor="agent:test",
                     guard_mode="audit", actuator_guards=guards)
    latest, _ = m.store.load_latest()
    auth = latest["manifest"]["authority"]
    check("open-guards-roundtrip",
          auth["guard_mode"] == "audit" and auth["actuator_guards"] == guards)


def test_open_without_guards_omits_fields() -> None:
    ws = _tmp_workspace()
    m = Mission.open(ws, "guard-less", "do the thing", "operator:test",
                     "agent:test", actor="agent:test")
    latest, _ = m.store.load_latest()
    auth = latest["manifest"]["authority"]
    check("open-guardless-omits-fields",
          "guard_mode" not in auth and "actuator_guards" not in auth)


def test_amend_changes_guards() -> None:
    ws = _tmp_workspace()
    m = Mission.open(ws, "guard-amend", "i", "operator:test", "agent:test",
                     actor="agent:test")
    m.approve()
    rev = m.amend_authority(
        "operator: arm the hook in audit mode",
        guard_mode="audit",
        actuator_guards=[{"name": "g", "tool_names": ["Bash"],
                          "command_regexes": ["rm"], "path_globs": []}])
    latest, _ = m.store.load_latest()
    check("amend-guards-landed",
          latest["manifest"]["authority"]["guard_mode"] == "audit"
          and latest["revision"] == rev)


def test_tail_guard_tamper_without_amendment_detected() -> None:
    ws = _tmp_workspace()
    m = Mission.open(ws, "guard-tamper", "i", "operator:test", "agent:test",
                     actor="agent:test")
    m.approve()
    # Forge a tail checkpoint: same chain, guards added by hand, no amendment.
    latest, path = m.store.load_latest()
    forged = json.loads(json.dumps(latest))
    forged["revision"] = latest["revision"] + 1
    forged["prev_checkpoint_sha256"] = sha256_file(path)
    forged["manifest"]["authority"]["actuator_guards"] = [
        {"name": "x", "tool_names": ["Bash"], "command_regexes": ["a"],
         "path_globs": []}]
    forged["manifest"]["authority"]["guard_mode"] = "audit"
    m.store.write_checkpoint(forged)
    try:
        m.note("probe")
        check("tail-guard-tamper-detected", False)
    except CustodyError:
        check("tail-guard-tamper-detected", True)
```

(Imports `sha256_file` from `custody_store` — add to the test file's import block.)

- [ ] **Step 2: Run tests to verify they fail**

Run: `python MC/test_custody_mission.py`
Expected: FAIL — `TypeError: unexpected keyword argument 'guard_mode'` on open/amend tests.

- [ ] **Step 3: Implement**

In `MC/custody_mission.py`:

Module level, near `_OPEN_STATES`:

```python
_UNSET = object()  # amend sentinel: distinguishes "leave alone" from "clear"
_GUARD_AUTHORITY_KEYS = ("actuator_guards", "guard_mode")
```

`Mission.open` — extend signature and manifest build:

```python
        acceptable_costs: list[str] | None = None,
        guard_mode: str | None = None,
        actuator_guards: list | None = None) -> "Mission":
```

```python
            "authority": {
                ...existing keys...,
                **({"actuator_guards": actuator_guards} if actuator_guards is not None else {}),
                **({"guard_mode": guard_mode} if guard_mode is not None else {}),
            },
```

`_verify_manifest` — after zeroing amendments on both deep copies (current lines 257-258), add:

```python
        # Guard fields are authority too: they may change only via amend, and
        # amend always appends the operator's verbatim grant -- so a guard
        # difference without any recorded amendment is tampering. (A forged
        # amendment stays possible on the unsealed tail; that is the es#118
        # residue, disclosed in SECURITY.md, not something this check invents
        # coverage for.)
        origin_guards = {k: origin_rest["authority"].pop(k, None)
                         for k in _GUARD_AUTHORITY_KEYS}
        latest_guards = {k: latest_rest["authority"].pop(k, None)
                         for k in _GUARD_AUTHORITY_KEYS}
        if origin_guards != latest_guards and not latest_amendments:
            raise CustodyError(
                "actuator guards changed with no authority amendment "
                "recorded (tampered)")
```

(This must sit BEFORE the `origin_rest != latest_rest` comparison, which then runs unchanged on the stripped copies.)

`amend_authority` — new signature and application:

```python
    def amend_authority(self, text: str, *, guard_mode=_UNSET,
                        actuator_guards=_UNSET) -> int:
```

after the amendments append:

```python
        if actuator_guards is not _UNSET:
            manifest["authority"]["actuator_guards"] = actuator_guards
        if guard_mode is not _UNSET:
            manifest["authority"]["guard_mode"] = guard_mode
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python MC/test_custody_mission.py`
Expected: PASS all (exit 0), including all pre-existing tamper tests.

- [ ] **Step 5: Commit (operator GO required)**

```bash
git add plugins/epistemic-skills/contracts/mission-custody/
git commit --signoff -m "feat(mission-custody): open/amend carry actuator guards; guard change without amendment reads as tamper (refs #117)"
```

---

### Task 3: The gate evaluator (`custody_gate.py`)

**Files:**
- Create: `MC/custody_gate.py`
- Test: `MC/test_custody_gate.py` (create)

**Interfaces:**
- Consumes: `Mission.load` / `mission.status()` from `custody_mission`; `_ascii_case_fold`, `_normalize_relpath` from `custody_mission`; `MissionStore.mission_dir`.
- Produces (Task 4's CLI and Task 5's hook rely on exactly these):
  - `evaluate(authority: dict, tool_call: dict) -> dict` — pure. `tool_call` = `{"tool_name": str, "command": str|None, "file_path": str|None}`. Returns `{"decision": "allow"|"block", "matched": bool, "rule": str|None, "mode": str, "reason": str}`.
  - `run_gate(workspace: Path, tool_call: dict, *, actor: str, session_id: str = "", harness: str = "") -> dict` — loads the active mission, evaluates, appends to `guard-log.jsonl` on match, returns the verdict dict. Raises nothing for no-mission (returns allow with reason).

- [ ] **Step 1: Write the failing tests**

Create `MC/test_custody_gate.py` (script style, `check()` pattern, tempfile workspaces; build missions via `Mission.open` directly):

```python
#!/usr/bin/env python3
"""Unit + integration tests for custody_gate.py."""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from custody_gate import evaluate, run_gate  # noqa: E402
from custody_mission import Mission  # noqa: E402
from custody_store import sha256_file  # noqa: E402

FAILURES: list[str] = []


def check(name: str, cond: bool) -> None:
    if not cond:
        FAILURES.append(name)
        print(f"FAIL {name}")
    else:
        print(f"ok   {name}")


GUARDS = [
    {"name": "arr-api", "tool_names": ["Bash"],
     "command_regexes": [r":7878/api"], "path_globs": []},
    {"name": "media-moves", "tool_names": ["Bash", "Write", "Edit"],
     "command_regexes": [r"\b(mv|robocopy)\b[^\n]*[Mm]edia"],
     "path_globs": ["M:/Media/**"]},
]


def auth(mode: str | None, guards=None) -> dict:
    out: dict = {}
    if mode is not None:
        out["guard_mode"] = mode
    if guards is not None:
        out["actuator_guards"] = guards
    return out


def test_evaluate_inert() -> None:
    call = {"tool_name": "Bash", "command": "curl :7878/api", "file_path": None}
    check("eval-inert-no-fields", evaluate(auth(None), call)["decision"] == "allow")
    check("eval-inert-guards-no-mode",
          evaluate(auth(None, GUARDS), call)["decision"] == "allow")


def test_evaluate_modes() -> None:
    call = {"tool_name": "Bash", "command": "curl :7878/api", "file_path": None}
    v = evaluate(auth("audit", GUARDS), call)
    check("eval-audit-allows-matched",
          v["decision"] == "allow" and v["matched"] and v["rule"] == "arr-api")
    v = evaluate(auth("enforce", GUARDS), call)
    check("eval-enforce-blocks",
          v["decision"] == "block" and v["rule"] == "arr-api")


def test_evaluate_tool_gate() -> None:
    call = {"tool_name": "Read", "command": None, "file_path": "M:/Media/x.mkv"}
    v = evaluate(auth("enforce", GUARDS), call)
    check("eval-tool-not-in-rule", not v["matched"] and v["decision"] == "allow")
    call = {"tool_name": "Write", "command": None, "file_path": "M:/Media/x.mkv"}
    v = evaluate(auth("enforce", GUARDS), call)
    check("eval-glob-match", v["matched"] and v["rule"] == "media-moves")
    call = {"tool_name": "Write", "command": None, "file_path": "M:/Other/x.mkv"}
    check("eval-glob-no-match", not evaluate(auth("enforce", GUARDS), call)["matched"])


def test_evaluate_case_fold_is_ascii_only() -> None:
    guards = [{"name": "g", "tool_names": ["Write"], "command_regexes": [],
               "path_globs": ["M:/Media/STRASSE/**"]}]
    call = {"tool_name": "Write", "command": None,
            "file_path": "M:/Media/strasse/x"}  # ß-folded spelling
    # NTFS folds A-Z only: 'strasse' (with eszett in the glob) must NOT match
    # a different codepoint sequence. Build both spellings explicitly:
    glob_eszett = ["M:/Media/stra\u00dfe/**"]
    guards[0]["path_globs"] = glob_eszett
    check("eval-no-eszett-fold",
          not evaluate(auth("enforce", guards), call)["matched"])
    call_ascii = {"tool_name": "Write", "command": None,
                  "file_path": "m:/media/stra\u00dfe/x"}
    if sys.platform.startswith("win"):
        check("eval-ascii-fold-nt",
              evaluate(auth("enforce", guards), call_ascii)["matched"])


def test_run_gate_chain_untouched_and_log() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp)
        m = Mission.open(ws, "gate-it", "i", "operator:test", "agent:test",
                         actor="agent:test", guard_mode="audit",
                         actuator_guards=GUARDS)
        m.approve()
        before = {p.name: sha256_file(p)
                  for p in sorted((ws / "missions" / "gate-it").rglob("*.json"))}
        call = {"tool_name": "Bash", "command": "curl :7878/api", "file_path": None}
        v = run_gate(ws, call, actor="hook:custody-gate", session_id="s1",
                     harness="test")
        after = {p.name: sha256_file(p)
                 for p in sorted((ws / "missions" / "gate-it").rglob("*.json"))}
        check("run-gate-allows-audit", v["decision"] == "allow" and v["matched"])
        check("run-gate-chain-byte-identical", before == after)
        log = ws / "missions" / "gate-it" / "guard-log.jsonl"
        check("run-gate-log-written", log.is_file())
        entry = json.loads(log.read_text(encoding="utf-8").splitlines()[-1])
        check("run-gate-log-fields",
              entry["rule"] == "arr-api" and entry["session_id"] == "s1"
              and entry["mode"] == "audit")
        # No match -> no log line
        n_lines = len(log.read_text(encoding="utf-8").splitlines())
        run_gate(ws, {"tool_name": "Read", "command": None, "file_path": "x"},
                 actor="hook:custody-gate")
        check("run-gate-no-match-no-log",
              len(log.read_text(encoding="utf-8").splitlines()) == n_lines)


def test_run_gate_no_mission_allows() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        v = run_gate(Path(tmp), {"tool_name": "Bash", "command": "rm -rf /",
                                 "file_path": None}, actor="hook:custody-gate")
        check("run-gate-no-mission-allow",
              v["decision"] == "allow" and not v["matched"])


if __name__ == "__main__":
    for fn in list(globals().values()):
        if callable(fn) and getattr(fn, "__name__", "").startswith("test_"):
            fn()
    if FAILURES:
        print(f"{len(FAILURES)} FAILURES")
        sys.exit(1)
    print("all green")
```

(Note: `test_open` helpers in existing files use their own conventions; this file is self-contained on purpose.)

- [ ] **Step 2: Run to verify it fails**

Run: `python MC/test_custody_gate.py`
Expected: ImportError — `custody_gate` does not exist.

- [ ] **Step 3: Implement `MC/custody_gate.py`**

```python
#!/usr/bin/env python3
"""Stage-C gate: evaluate a harness tool call against the active mission's
operator-approved actuator guards (mission-manifest@1 optional fields).

Read-only by contract: the only write anywhere in this module is an append to
missions/<id>/guard-log.jsonl on a MATCH -- the checkpoint chain is never
touched (verified by test: run-gate-chain-byte-identical). The checkpoint read
goes through MissionStore.load_latest, so the manifest evaluated is the
chain-verified latest.

Matching is deliberately over-broad (handoff error-direction lesson): a false
block names its rule and is discharged by an amend; a false allow silently
retires custody of the actuator class the tracer retro named.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

from custody_mission import (
    Mission,
    MultipleActiveMissions,
    NoActiveMission,
    _ascii_case_fold,
    _normalize_relpath,
)

GUARD_LOG_NAME = "guard-log.jsonl"
_PREVIEW = 120


def _glob_regex(glob: str) -> "re.Pattern[str]":
    """Translate a path glob: '**' crosses separators, '*'/'?' stay in-segment.
    Paths are normalized ('\\' -> '/', no './', no trailing '/') before match;
    on NT both sides fold A-Z only (_ascii_case_fold -- never str.casefold)."""
    out: list[str] = []
    i = 0
    while i < len(glob):
        if glob[i] == "*":
            if glob[i:i + 2] == "**":
                out.append(".*")
                i += 2
            else:
                out.append("[^/]*")
                i += 1
        elif glob[i] == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(glob[i]))
            i += 1
    return re.compile("".join(out) + "$", re.DOTALL)


def _fold(text: str) -> str:
    return _ascii_case_fold(text) if os.name == "nt" else text


def _norm_path(path: str) -> str:
    return _fold(_normalize_relpath(path.replace("\\", "/")))


def _tool_in(rule: dict, tool_name: str) -> bool:
    return tool_name in rule["tool_names"]


def _patterns_match(rule: dict, tool_call: dict) -> bool:
    command = tool_call.get("command")
    if command:
        for pattern in rule["command_regexes"]:
            if re.search(pattern, command):
                return True
    file_path = tool_call.get("file_path")
    if file_path:
        target = _norm_path(file_path)
        for glob in rule["path_globs"]:
            if _glob_regex(_fold(_normalize_relpath(glob))).match(target):
                return True
    return False


def evaluate(authority: dict, tool_call: dict) -> dict:
    mode = authority.get("guard_mode")
    guards = authority.get("actuator_guards")
    if not mode or not guards:
        return {"decision": "allow", "matched": False, "rule": None,
                "mode": mode or "inert", "reason": "no guards armed"}
    for rule in guards:
        if _tool_in(rule, tool_call.get("tool_name", "")) \
                and _patterns_match(rule, tool_call):
            if mode == "enforce":
                return {"decision": "block", "matched": True,
                        "rule": rule["name"], "mode": mode,
                        "reason": (
                            f"custody guard '{rule['name']}' matched this call; "
                            "the mission envelope does not discharge it -- record "
                            "an operator grant via `amend` or stop")}
            return {"decision": "allow", "matched": True, "rule": rule["name"],
                    "mode": mode,
                    "reason": f"custody guard '{rule['name']}' matched (audit mode)"}
    return {"decision": "allow", "matched": False, "rule": None,
            "mode": mode, "reason": "no guard matched"}


def _append_guard_log(mission_dir: Path, entry: dict) -> None:
    path = mission_dir / GUARD_LOG_NAME
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, sort_keys=True) + "\n")


def run_gate(workspace: Path, tool_call: dict, *, actor: str,
             session_id: str = "", harness: str = "") -> dict:
    workspace = Path(workspace)
    try:
        mission = Mission.load(workspace, actor=actor)
    except (NoActiveMission, MultipleActiveMissions) as exc:
        return {"decision": "allow", "matched": False, "rule": None,
                "mode": "inert", "reason": f"gate inert: {type(exc).__name__}"}
    latest = mission.status()
    verdict = evaluate(latest["manifest"]["authority"], tool_call)
    if verdict["matched"]:
        command = tool_call.get("command") or ""
        entry = {
            "utc": latest["written_utc"],  # see note below
            "actor": actor,
            "session_id": session_id,
            "harness": harness,
            "mode": verdict["mode"],
            "decision": verdict["decision"],
            "rule": verdict["rule"],
            "tool_name": tool_call.get("tool_name", ""),
            "command_preview": command[:_PREVIEW],
            "file_path": tool_call.get("file_path"),
        }
        _append_guard_log(mission.store.mission_dir, entry)
    return verdict
```

Implementation note for the executor: use `custody_mission.now_utc()` for the log entry's `utc`, not the checkpoint's `written_utc` (import it; the sketch above marks the spot).

- [ ] **Step 4: Run tests to verify they pass**

Run: `python MC/test_custody_gate.py`
Expected: PASS all (exit 0).

- [ ] **Step 5: Commit (operator GO required)**

```bash
git add plugins/epistemic-skills/contracts/mission-custody/
git commit --signoff -m "feat(mission-custody): custody_gate evaluator -- read-only, log-on-match, ascii-only case fold (refs #117)"
```

---

### Task 4: CLI — `gate` verb + `open`/`amend` flags

**Files:**
- Modify: `MC/custody_cli.py` (`build_parser` lines 68-134; `dispatch` lines 153-228; module docstring lines 1-17)
- Test: `MC/test_custody_cli.py` (append)

**Interfaces:**
- Consumes: `custody_gate.run_gate` (Task 3); `Mission.open`/`amend_authority` new kwargs (Task 2).
- Produces:
  - `custody_cli.py gate --workspace W --actor A [--input-file F]` — tool-call JSON on stdin or from file; prints verdict JSON on stdout; exit 0 allow / 2 block.
  - `open --guards-file F --guard-mode audit|enforce` (both optional; `--guard-mode` without `--guards-file` → usage error exit 2).
  - `amend --text T [--guards-file F] [--guard-mode MODE]` (flags optional; `--guards-file` with `[]` clears guards).

- [ ] **Step 1: Write the failing tests**

Append to `MC/test_custody_cli.py` (uses its existing `run()` subprocess helper + workspace fixture style):

```python
def test_gate_verb(tmp: Path) -> None:
    # open an enforced mission guarding 'rm -rf'
    guards = [{"name": "no-rm", "tool_names": ["Bash"],
               "command_regexes": ["rm -rf"], "path_globs": []}]
    gfile = tmp / "guards.json"
    gfile.write_text(json.dumps(guards), encoding="utf-8")
    run("open", "--workspace", str(tmp), "--actor", "agent:t",
        "--mission-id", "gate-cli", "--instruction", "i",
        "--operator", "operator:t", "--steward", "agent:t",
        "--guards-file", str(gfile), "--guard-mode", "enforce")
    run("approve", "--workspace", str(tmp), "--actor", "agent:t")
    blocked = subprocess.run(
        [sys.executable, str(CLI), "gate", "--workspace", str(tmp),
         "--actor", "hook:custody-gate"],
        input=json.dumps({"tool_name": "Bash", "command": "rm -rf x",
                          "file_path": None}),
        capture_output=True, text=True)
    check("gate-blocks-enforced", blocked.returncode == 2)
    verdict = json.loads(blocked.stdout)
    check("gate-verdict-fields",
          verdict["decision"] == "block" and verdict["rule"] == "no-rm")
    allowed = subprocess.run(
        [sys.executable, str(CLI), "gate", "--workspace", str(tmp),
         "--actor", "hook:custody-gate"],
        input=json.dumps({"tool_name": "Bash", "command": "ls",
                          "file_path": None}),
        capture_output=True, text=True)
    check("gate-allows-unmatched", allowed.returncode == 0)


def test_gate_no_mission_allows(tmp: Path) -> None:
    res = subprocess.run(
        [sys.executable, str(CLI), "gate", "--workspace", str(tmp),
         "--actor", "hook:custody-gate"],
        input=json.dumps({"tool_name": "Bash", "command": "rm -rf /"}),
        capture_output=True, text=True)
    check("gate-no-mission-exit-0", res.returncode == 0)


def test_open_guard_mode_without_guards_refused(tmp: Path) -> None:
    res = run("open", "--workspace", str(tmp), "--actor", "agent:t",
              "--mission-id", "bad-open", "--instruction", "i",
              "--operator", "operator:t", "--steward", "agent:t",
              "--guard-mode", "audit")
    check("open-mode-without-guards-refused", res.returncode == 2)


def test_amend_guard_mode_flag(tmp: Path) -> None:
    run("open", "--workspace", str(tmp), "--actor", "agent:t",
        "--mission-id", "amend-cli", "--instruction", "i",
        "--operator", "operator:t", "--steward", "agent:t")
    run("approve", "--workspace", str(tmp), "--actor", "agent:t")
    guards = [{"name": "g", "tool_names": ["Bash"],
               "command_regexes": ["x"], "path_globs": []}]
    gfile = tmp / "g.json"
    gfile.write_text(json.dumps(guards), encoding="utf-8")
    res = run("amend", "--workspace", str(tmp), "--actor", "agent:t",
              "--text", "operator: arm audit mode",
              "--guards-file", str(gfile), "--guard-mode", "audit")
    check("amend-guards-accepted", res.returncode == 0)
```

(Adapt `tmp` to the file's actual fixture convention — `test_custody_cli.py` uses `tempfile` contexts; match what is there.)

- [ ] **Step 2: Run to verify they fail**

Run: `python MC/test_custody_cli.py`
Expected: FAIL — `invalid choice: 'gate'` / unrecognized arguments.

- [ ] **Step 3: Implement**

In `build_parser`:

```python
    p_open.add_argument("--guards-file", dest="guards_file")
    p_open.add_argument("--guard-mode", dest="guard_mode",
                        choices=["audit", "enforce"])
```

```python
    p_amend.add_argument("--guards-file", dest="guards_file")
    p_amend.add_argument("--guard-mode", dest="guard_mode",
                         choices=["audit", "enforce"])
```

```python
    p_gate = sub.add_parser("gate", parents=[common])
    p_gate.add_argument("--input-file", dest="input_file")
```

Helpers (module level):

```python
def _read_guards_file(path: str) -> list:
    with open(path, encoding="utf-8") as handle:
        guards = json.load(handle)
    if not isinstance(guards, list):
        raise CustodyError("guards file must contain a JSON list of rules")
    return guards


def _read_tool_call(args: argparse.Namespace) -> dict:
    # stdin carries the tool-call JSON by default -- argv has a ~32KB ceiling
    # on Windows and every shell metachar must survive, same reason
    # --content-file exists. --input-file is the explicit-file escape hatch.
    raw = (Path(args.input_file).read_text(encoding="utf-8")
           if args.input_file else sys.stdin.read())
    try:
        call = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise CustodyError(f"gate: tool-call JSON unreadable: {exc}") from None
    if not isinstance(call, dict) or not isinstance(call.get("tool_name"), str):
        raise CustodyError("gate: tool-call JSON needs a string 'tool_name'")
    call.setdefault("command", None)
    call.setdefault("file_path", None)
    return call
```

In `dispatch`, `open` branch — before `Mission.open`:

```python
        if args.guard_mode and not args.guards_file:
            raise CustodyError("--guard-mode requires --guards-file")
        guards = (_read_guards_file(args.guards_file)
                  if args.guards_file else None)
```
and pass `guard_mode=args.guard_mode, actuator_guards=guards` to `Mission.open`.

`amend` branch:

```python
    elif args.command == "amend":
        kwargs: dict = {}
        if args.guards_file:
            kwargs["actuator_guards"] = _read_guards_file(args.guards_file)
        if args.guard_mode:
            kwargs["guard_mode"] = args.guard_mode
        print(mission.amend_authority(args.text, **kwargs))
```

`gate` branch (before the `mission = Mission.load(...)` line — gate does its own load inside `run_gate`, so place it with `open` above that line):

```python
    if args.command == "gate":
        from custody_gate import run_gate
        verdict = run_gate(workspace, _read_tool_call(args), actor=args.actor,
                           session_id="", harness="cli")
        _print_status(verdict)
        return 2 if verdict["decision"] == "block" else 0
```

Update the module docstring's exit-code line: `gate` exit 2 = block (a guarded actuator fired outside the armed envelope).

- [ ] **Step 4: Run tests to verify they pass**

Run: `python MC/test_custody_cli.py`
Expected: PASS all (exit 0).

- [ ] **Step 5: Commit (operator GO required)**

```bash
git add plugins/epistemic-skills/contracts/mission-custody/
git commit --signoff -m "feat(mission-custody): gate verb + open/amend guard flags (refs #117)"
```

---

### Task 5: The hook script (`custody_hook.py`)

**Files:**
- Create: `MC/custody_hook.py`
- Test: `MC/test_custody_hook.py` (create)

**Interfaces:**
- Consumes: `custody_gate.run_gate`.
- Produces: `python custody_hook.py --harness <name>` reads a harness payload on stdin, exits 0 (allow) or 2 (block, reason on stderr; cursor/gemini may instead emit decision JSON per their docs — see Task 6 verification step). Adapter contract: `ADAPTERS[name](payload: dict) -> dict | None` returning `{"tool_name", "command", "file_path", "session_id", "cwd"}`; `None` = nothing to evaluate → exit 0.

- [ ] **Step 1: Write the failing tests**

Create `MC/test_custody_hook.py` — subprocess-driven, one workspace fixture with an enforced guard on `rm -rf`, feeding canonical payloads:

```python
#!/usr/bin/env python3
"""End-to-end tests for custody_hook.py: stdin payload -> exit code."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HOOK = ROOT / "custody_hook.py"
sys.path.insert(0, str(ROOT))
from custody_mission import Mission  # noqa: E402

FAILURES: list[str] = []


def check(name: str, cond: bool) -> None:
    if not cond:
        FAILURES.append(name)
        print(f"FAIL {name}")
    else:
        print(f"ok   {name}")


GUARDS = [{"name": "no-rm", "tool_names": ["Bash", "shell", "Shell"],
           "command_regexes": ["rm -rf"], "path_globs": []}]


def run_hook(harness: str, payload: dict | str) -> subprocess.CompletedProcess:
    raw = payload if isinstance(payload, str) else json.dumps(payload)
    return subprocess.run(
        [sys.executable, str(HOOK), "--harness", harness],
        input=raw, capture_output=True, text=True)


def payloads(cwd: str) -> dict:
    return {
        "claude": {"hook_event_name": "PreToolUse", "session_id": "s1",
                   "cwd": cwd,
                   "tool_name": "Bash", "tool_input": {"command": "rm -rf x"}},
        "kimi": {"hook_event_name": "PreToolUse", "session_id": "s2",
                 "cwd": cwd,
                 "tool_name": "Bash", "tool_input": {"command": "rm -rf x"}},
        "codex": {"session_id": "s3", "cwd": cwd,
                  "tool_name": "Bash", "tool_input": {"command": "rm -rf x"}},
        "cursor": {"command": "rm -rf x", "cwd": cwd},  # beforeShellExecution
        "gemini": {"tool_name": "Bash",
                   "tool_input": {"command": "rm -rf x"}, "cwd": cwd},
        "generic": {"tool_name": "Bash",
                    "tool_input": {"command": "rm -rf x"}, "cwd": cwd},
    }


def test_block_per_harness() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp)
        m = Mission.open(ws, "hook-e2e", "i", "operator:t", "agent:t",
                         actor="agent:t", guard_mode="enforce",
                         actuator_guards=GUARDS)
        m.approve()
        for harness, payload in payloads(tmp).items():
            res = run_hook(harness, payload)
            check(f"hook-{harness}-blocks", res.returncode == 2)
            check(f"hook-{harness}-reason-names-rule",
                  "no-rm" in (res.stderr + res.stdout))


def test_allow_paths() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp)
        m = Mission.open(ws, "hook-allow", "i", "operator:t", "agent:t",
                         actor="agent:t", guard_mode="enforce",
                         actuator_guards=GUARDS)
        m.approve()
        ok = payloads(tmp)["claude"]
        ok["tool_input"] = {"command": "ls"}
        check("hook-unmatched-allows", run_hook("claude", ok).returncode == 0)
    with tempfile.TemporaryDirectory() as tmp:
        # no missions dir at all -> inert fast path
        p = payloads(tmp)["claude"]
        check("hook-no-missions-dir-allows",
              run_hook("claude", p).returncode == 0)


def test_fail_open() -> None:
    check("hook-garbage-stdin-allows", run_hook("claude", "not json{{").returncode == 0)
    check("hook-empty-stdin-allows", run_hook("claude", "").returncode == 0)
    check("hook-unknown-harness-allows",
          subprocess.run([sys.executable, str(HOOK), "--harness", "nope"],
                         input="{}", capture_output=True,
                         text=True).returncode == 0)


if __name__ == "__main__":
    for fn in list(globals().values()):
        if callable(fn) and getattr(fn, "__name__", "").startswith("test_"):
            fn()
    if FAILURES:
        print(f"{len(FAILURES)} FAILURES")
        sys.exit(1)
    print("all green")
```

Note for executor: the cursor/gemini payload shapes above are placeholders pending the docs-verification in Task 6 — if the official payloads differ, update the adapter AND this fixture to match, and note the source URL in the commit message.

- [ ] **Step 2: Run to verify it fails**

Run: `python MC/test_custody_hook.py`
Expected: failures — `custody_hook.py` does not exist.

- [ ] **Step 3: Implement `MC/custody_hook.py`**

```python
#!/usr/bin/env python3
"""Stage-C PreToolUse hook: harness payload -> custody gate -> exit 0/2.

Fail-open by contract: ANY error (bad JSON, unknown harness, missing cwd,
no mission, evaluator exception) exits 0. Denial travels only via the
deliberate block path. Timeout is the harness's (configure <=10s); the inert
fast path is one directory stat.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _claude_kimi(payload: dict) -> dict | None:
    tool_input = payload.get("tool_input") or {}
    return {
        "tool_name": payload.get("tool_name", ""),
        "command": tool_input.get("command"),
        "file_path": tool_input.get("file_path"),
        "session_id": payload.get("session_id", ""),
        "cwd": payload.get("cwd", ""),
    }


def _cursor(payload: dict) -> dict | None:
    # beforeShellExecution: {"command", "cwd"}; preToolUse carries tool fields.
    return {
        "tool_name": payload.get("tool_name", "Shell"),
        "command": payload.get("command")
        or (payload.get("tool_input") or {}).get("command"),
        "file_path": (payload.get("tool_input") or {}).get("file_path"),
        "session_id": payload.get("session_id", ""),
        "cwd": payload.get("cwd", ""),
    }


ADAPTERS = {
    "claude": _claude_kimi,
    "kimi": _claude_kimi,
    "codex": _claude_kimi,   # same PreToolUse shape; Task 6 docs-verify
    "cursor": _cursor,
    "gemini": _claude_kimi,  # BeforeTool shape; Task 6 docs-verify (agy shares it)
    "generic": _claude_kimi,
}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="custody_hook.py")
    parser.add_argument("--harness", default="generic")
    args = parser.parse_args(argv)
    try:
        adapter = ADAPTERS[args.harness]
        raw = sys.stdin.read()
        payload = json.loads(raw)
        if not isinstance(payload, dict):
            return 0
        call = adapter(payload)
        if not call or not call.get("tool_name") and not call.get("command"):
            return 0
        cwd = call.get("cwd") or "."
        workspace = Path(cwd)
        if not (workspace / "missions").is_dir():
            return 0  # inert fast path: no custody state here at all
        from custody_gate import run_gate
        verdict = run_gate(
            workspace,
            {"tool_name": call["tool_name"], "command": call.get("command"),
             "file_path": call.get("file_path")},
            actor="hook:custody-gate",
            session_id=call.get("session_id", ""), harness=args.harness)
        if verdict["decision"] == "block":
            print(f"custody gate: BLOCKED -- {verdict['reason']}",
                  file=sys.stderr)
            return 2
        return 0
    except Exception:
        return 0  # fail open, always


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python MC/test_custody_hook.py`
Expected: PASS all (exit 0).

- [ ] **Step 5: Commit (operator GO required)**

```bash
git add plugins/epistemic-skills/contracts/mission-custody/
git commit --signoff -m "feat(mission-custody): custody_hook PreToolUse script with per-harness adapters, fail-open (refs #117)"
```

---

### Task 6: Harness wiring (docs-verified per harness)

**Files:**
- Create: `plugins/epistemic-skills/hooks/hooks.json` (Claude Code plugin hooks)
- Modify: `plugins/epistemic-skills/.kimi-plugin/plugin.json` (add `hooks` array)
- Create: `plugins/epistemic-skills/hooks/codex-hooks.json` + `plugins/epistemic-skills/hooks/cursor-hooks.json` + `plugins/epistemic-skills/hooks/gemini-settings-snippet.json`
- Modify: `plugins/epistemic-skills/.cursor-plugin/plugin.json` (add `hooks` key if the docs support plugin-shipped hooks)
- Modify: root-level manifests (`/.kimi-plugin/plugin.json`, `/.claude-plugin/...`, `/.cursor-plugin/plugin.json`, `/gemini-extension.json`) ONLY IF `packaging/` shows they are hand-maintained siblings rather than generated — inspect `packaging/` first and follow the repo's sync mechanism.
- Test: manual wiring validation step below (no unit tests for JSON wiring; verification is structural + docs citations)

**Interfaces:**
- Consumes: `custody_hook.py --harness <name>` (Task 5).
- Produces: each harness's canonical hook registration pointing at the hook script with the right `--harness` value.

- [ ] **Step 1: Inspect packaging/sync**

Run: `ls packaging/` in the worktree; read the sync/packaging script. Determine whether root-level `.kimi-plugin/`, `.claude-plugin/`, `.cursor-plugin/`, `gemini-extension.json` are generated from `plugins/epistemic-skills/` or hand-maintained. Record the answer in the commit message; wire whichever level(s) are canonical.

- [ ] **Step 2: Claude Code wiring**

Create `plugins/epistemic-skills/hooks/hooks.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|Write|Edit|mcp__.*",
        "hooks": [
          {
            "type": "command",
            "command": "python \"${CLAUDE_PLUGIN_ROOT}/contracts/mission-custody/custody_hook.py\" --harness claude",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

- [ ] **Step 3: Kimi wiring (docs-verified 2026-08-12: plugin `hooks` array, `event`/`matcher`/`command`/`timeout`, cwd = plugin root, `./` paths allowed)**

Add to `plugins/epistemic-skills/.kimi-plugin/plugin.json`:

```json
"hooks": [
  {
    "event": "PreToolUse",
    "matcher": "Bash|Write|Edit",
    "command": "python ./contracts/mission-custody/custody_hook.py --harness kimi",
    "timeout": 10
  }
]
```

- [ ] **Step 4: Codex / Cursor / Gemini — docs-verify, then wire**

For EACH of the three: fetch the harness's official hook documentation (Codex: docs.openai.com codex hooks; Cursor: cursor.com docs hooks; Gemini CLI: github.com/google-gemini/gemini-cli hooks doc). Confirm: event name, matcher semantics, payload shape, blocking contract (exit 2 vs decision JSON), whether plugin/extension manifests can ship hooks natively. Then:

- If the payload/blocking shape matches the Task 5 adapter: wire it (config JSON in `hooks/` + manifest key where supported + a README install note where only user-level config exists).
- If it differs: fix the adapter and the Task 5 fixture to match the official schema, rerun `test_custody_hook.py`, and cite the doc URL in the commit.
- If official docs cannot confirm: ship the wiring file marked unverified and say so in the README table (design's docs-verification gate). Do NOT assert support.

Codex wiring (expected shape — verify): `hooks/codex-hooks.json` with a `PreToolUse` entry matching `Bash|apply_patch|mcp__.*` running `python <plugin>/contracts/mission-custody/custody_hook.py --harness codex`; README note that Codex reads `~/.codex/hooks.json` / project `.codex/hooks.json`.

Cursor wiring (expected shape — verify): `.cursor-plugin/plugin.json` gains `"hooks": "./hooks/cursor-hooks.json"`; that file registers `beforeShellExecution`, `beforeMCPExecution`, `preToolUse` running the hook with `--harness cursor`.

Gemini wiring (expected shape — verify): `hooks/gemini-settings-snippet.json` documenting the `BeforeTool` entry for `~/.gemini/settings.json` (covers Gemini CLI and agy, which share that surface), or `gemini-extension.json` hooks key if officially supported.

- [ ] **Step 5: Structural validation**

Run: `python -c "import json,glob; [json.load(open(f, encoding='utf-8')) for f in glob.glob('plugins/epistemic-skills/hooks/*.json') + ['plugins/epistemic-skills/.kimi-plugin/plugin.json']]; print('json ok')"` from the worktree root.
Expected: `json ok`.

- [ ] **Step 6: Commit (operator GO required)**

```bash
git add plugins/epistemic-skills/
git commit --signoff -m "feat(mission-custody): PreToolUse wiring for claude/kimi/codex/cursor/gemini(+agy) (refs #117)"
```

---

### Task 7: Retro-consumption docs

**Files:**
- Modify: `MC/README.md` (the "Harness bindings" section, currently: `Stage C (enforcement) is gated on the tracer retro.`)
- Modify: `MC/SECURITY.md` (append fail-open + guard-tamper-residue sections)
- Modify: `plugins/epistemic-skills/skills/manifest/SKILL.md` (the boundary bullet naming es#117)

**Interfaces:**
- Consumes: Tasks 1-6 landed.
- Produces: no code interfaces; the retro ruling is recorded as consumed.

- [ ] **Step 1: README edit**

Replace the line `- Stage C (enforcement) is gated on the tracer retro.` with:

```markdown
- Stage C (enforcement): the tracer retro (2026-08-11, vanta
  `mission/tracer-media-missing-record` @ `4540ddb`) ruled teeth IN, scoped to
  the successor mission's real actuators. Shipped as `custody_hook.py` +
  `gate` (design: `docs/superpowers/specs/2026-08-12-stage-c-custody-hook-design.md`).
  Inert by default: a mission arms it by adding operator-approved
  `actuator_guards` + `guard_mode` to its manifest (`open --guards-file` /
  `amend --guard-mode`). Harness wiring:
  | harness | mechanism | verified |
  |---|---|---|
  | Claude Code | plugin `hooks/hooks.json` PreToolUse | yes |
  | Kimi Code | plugin.json `hooks` array | yes (official docs 2026-08-12) |
  | Codex | `hooks/codex-hooks.json` install note | <yes/no + doc URL> |
  | Cursor | plugin.json `hooks` key | <yes/no + doc URL> |
  | Gemini CLI + agy | `~/.gemini/settings.json` BeforeTool snippet | <yes/no + doc URL> |
  | others | `generic` adapter recipe (below) | by construction |
```

(Fill the `<yes/no + doc URL>` cells from Task 6 Step 4 outcomes.)

- [ ] **Step 2: SECURITY.md append**

Append a new section:

```markdown
## Stage-C hook: fail-open and guard-tamper residue

The PreToolUse custody hook is an enforcement layer over convention, not a
sole barrier. Every supported harness fails open on hook error, timeout, or
crash (Kimi documents this explicitly; Claude's contract is the same), so a
broken hook silently reverts enforcement to convention-held. Denial travels
only via the deliberate exit-2 / decision-JSON path.

Guard matching is deliberately over-broad: a false block names its rule and
is discharged by an `amend`; a false allow silently retires custody of the
actuator class.

A guard change without a recorded authority amendment is detected as manifest
tampering. A guard change accompanied by a FORGED amendment on the unsealed
tail checkpoint is the same residue class as amendment fabrication today;
the structural fix (tail anchor) is tracked as es#118.
```

- [ ] **Step 3: SKILL.md boundary bullet edit**

Replace the bullet beginning `- Custody here is convention-held, not mechanically enforced` with:

```markdown
- Custody enforcement is opt-in per mission: if the operator armed
  `actuator_guards` + `guard_mode` (the es#117 Stage-C hook), guarded
  actuators are mechanically gated -- a block names the rule and is
  discharged only by an operator-granted `amend`. If the mission carries no
  guards, custody remains convention-held; say so honestly if asked.
```

- [ ] **Step 4: Commit (operator GO required)**

```bash
git add plugins/epistemic-skills/
git commit --signoff -m "docs(mission-custody): record Stage-C ruling consumed; fail-open + guard-tamper disclosure (refs #117)"
```

---

### Task 8: Full-suite green + self-review gate

**Files:** none modified.

- [ ] **Step 1: Run every custody test**

```bash
cd plugins/epistemic-skills/contracts/mission-custody
for t in test_mission_custody.py test_custody_store.py test_custody_mission.py test_custody_cli.py test_custody_process_proof.py test_custody_gate.py test_custody_hook.py; do python "$t" || echo "FAILED: $t"; done
python verify_mission_custody.py examples/valid-manifest-minimal.json
```

Expected: every suite prints all-green / exit 0; every `invalid-*.json` example still fails validation (the valid-manifest check exits 0).

- [ ] **Step 2: Plugin-level checks**

Run the repo's existing plugin validation (check `packaging/` or CI config for the command — e.g. manifest validation that shipped with v5.0.0's "advertised skills" guard) from the worktree root. Expected: green.

- [ ] **Step 3: Diff review**

`git diff 2931d386...HEAD --stat` — expected files only: mission-custody contract files, hooks/ wiring, manifest JSONs, skill/README/SECURITY docs, spec + plan under docs/superpowers/. Anything else is scope creep; drop it.

- [ ] **Step 4: Final commit if anything changed (operator GO required)**

---

## Post-plan (operator-gated, from the goal contract — not plan tasks)

1. requesting-code-review + independent adversarial review of the PR.
2. PR (`Closes #117`) on operator GO; merge gated mechanically on green checks at the reviewed head SHA.
3. Deploy to plugin cache; did-it-land hash-verify against the merge SHA.
4. Evidence-locked live UAT on a scratch mission (audit logs a guarded call → amend to enforce → named-rule block) on Claude Code and Kimi.
5. Receipt the outcome into `media-library-rebuild` (effect/note + frontier); close es#117.
