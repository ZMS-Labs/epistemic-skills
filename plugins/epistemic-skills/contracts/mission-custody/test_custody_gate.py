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
