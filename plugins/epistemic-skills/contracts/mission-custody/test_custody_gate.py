#!/usr/bin/env python3
"""Unit + integration tests for custody_gate.py."""
from __future__ import annotations

import contextlib
import io
import json
import shutil
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


def test_glob_doublestar_zero_segments() -> None:
    guards = [{"name": "g", "tool_names": ["Write"], "command_regexes": [],
               "path_globs": ["src/**/secret*"]}]
    # '**/' must match ZERO or more segments, not one-or-more
    call = {"tool_name": "Write", "command": None, "file_path": "src/secret.txt"}
    check("glob-doublestar-zero-segments",
          evaluate(auth("enforce", guards), call)["matched"])
    call = {"tool_name": "Write", "command": None,
            "file_path": "src/a/b/secret.txt"}
    check("glob-doublestar-many-segments",
          evaluate(auth("enforce", guards), call)["matched"])
    # trailing '/**' must match the base path itself
    guards[0]["path_globs"] = ["M:/Media/**"]
    call = {"tool_name": "Write", "command": None, "file_path": "M:/Media"}
    check("glob-trailing-doublestar-base",
          evaluate(auth("enforce", guards), call)["matched"])


def test_glob_overmatch_still_held() -> None:
    guards = [{"name": "g", "tool_names": ["Write"], "command_regexes": [],
               "path_globs": ["M:/Media/**"]}]
    call = {"tool_name": "Write", "command": None, "file_path": "M:/Mediaevil/x"}
    check("glob-mediaevil-rejected",
          not evaluate(auth("enforce", guards), call)["matched"])
    call = {"tool_name": "Write", "command": None, "file_path": "M:/Media/a/b/c.mkv"}
    check("glob-deep-still-matches",
          evaluate(auth("enforce", guards), call)["matched"])
    # '..' is not collapsed by normalization, so it over-matches -- the safe
    # direction (a false block names its rule; a false allow retires custody)
    call = {"tool_name": "Write", "command": None,
            "file_path": "M:/Media/../etc/passwd"}
    check("glob-dotdot-overmatches",
          evaluate(auth("enforce", guards), call)["matched"])


def test_trailing_slash_guard_glob_binds_the_subtree() -> None:
    """es#155's gate half: 'M:/Media/' compiled to an exact 'M:/Media' and
    an armed guard silently allowed every write UNDER the directory the
    operator evidently declared. The trailing separator now reads as the
    directory marker scope entries and amendment tokens already use. This
    makes an armed guard MORE restrictive -- the disclosed, over-match-safe
    direction (a false block names its rule)."""
    guards = [{"name": "dir", "tool_names": ["Write"], "command_regexes": [],
               "path_globs": ["M:/Media/"]}]
    for label, path, expect in (
            ("subtree-write-blocked", "M:/Media/a/b.mkv", True),
            ("base-itself-matched", "M:/Media", True),
            ("prefix-sibling-not-matched", "M:/Mediaevil/x", False)):
        call = {"tool_name": "Write", "command": None, "file_path": path}
        check(f"guard-dir-marker-{label}",
              evaluate(auth("enforce", guards), call)["matched"] is expect)
    win = [{"name": "dirwin", "tool_names": ["Write"], "command_regexes": [],
            "path_globs": ["M:\\Media\\"]}]
    call = {"tool_name": "Write", "command": None,
            "file_path": "M:/Media/deep/file.mkv"}
    check("guard-dir-marker-windows-spelling",
          evaluate(auth("enforce", win), call)["matched"])
    # THE ROOT is the one spelling normalization leaves with its separator
    # attached, so the naive marker append built '//**' -- matching the
    # root and nothing under it. A guard of '/' means 'block all absolute
    # writes' and must cover every descendant; drive roots ('C:/') were
    # never affected.
    root = [{"name": "abs", "tool_names": ["Write"], "command_regexes": [],
             "path_globs": ["/"]}]
    for label, path, expect in (
            ("descendant-blocked", "/etc/passwd", True),
            ("deep-descendant-blocked", "/var/lib/x/y.db", True),
            ("relative-path-not-matched", "docs/x.md", False)):
        call = {"tool_name": "Write", "command": None, "file_path": path}
        check(f"guard-root-marker-{label}",
              evaluate(auth("enforce", root), call)["matched"] is expect)
    drive = [{"name": "drv", "tool_names": ["Write"], "command_regexes": [],
              "path_globs": ["C:/"]}]
    call = {"tool_name": "Write", "command": None,
            "file_path": "C:/Windows/System32/cfg.sys"}
    check("guard-drive-root-marker-covers-subtree",
          evaluate(auth("enforce", drive), call)["matched"])


def test_glob_anchor_is_Z_not_dollar() -> None:
    """'$' matches just before a trailing newline, so the glob 'safe.txt'
    matched the distinct file 'safe.txt\\n' -- one byte outside the
    declaration reading as inside it. The seven suites were provably blind
    to the anchor (they passed byte-identically either way), so this change
    brings its own pins. DOTALL stays: wildcards must still span a newline
    INSIDE a name; only the terminal one-character tolerance dies."""
    from custody_gate import _glob_regex
    check("glob-anchor-literal-refuses-trailing-newline",
          _glob_regex("safe.txt").match("safe.txt\n") is None)
    check("glob-anchor-star-refuses-trailing-newline",
          _glob_regex("docs/*.txt").match("docs/a.txt\n") is None)
    check("glob-anchor-doublestar-base-refuses-trailing-newline",
          _glob_regex("secrets/**").match("secrets\n") is None)
    check("glob-anchor-exact-still-matches",
          _glob_regex("safe.txt").match("safe.txt") is not None)
    check("glob-star-still-spans-interior-newline",
          _glob_regex("docs/*.txt").match("docs/a\nb.txt") is not None)
    check("glob-doublestar-still-spans-interior-newline",
          _glob_regex("secrets/**").match("secrets/a\nb/c") is not None)


def test_mcp_tool_input_serialized_match() -> None:
    guards = [{"name": "arr-mcp", "tool_names": ["mcp__sonarr__post"],
               "command_regexes": ["7878"], "path_globs": []}]
    call = {"tool_name": "mcp__sonarr__post", "command": None,
            "file_path": None,
            "tool_input": {"url": "http://10.10.10.50:7878/api/v3/series",
                           "method": "POST"}}
    v = evaluate(auth("enforce", guards), call)
    check("eval-mcp-serialized-args-block",
          v["decision"] == "block" and v["rule"] == "arr-mcp")
    safe = {"tool_name": "mcp__sonarr__post", "command": None,
            "file_path": None,
            "tool_input": {"url": "http://10.10.10.50:8989/api/v3/series"}}
    check("eval-mcp-no-match-allows",
          not evaluate(auth("enforce", guards), safe)["matched"])


def test_run_gate_mcp_end_to_end() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp)
        m = Mission.open(ws, "gate-mcp", "i", "operator:test", "agent:test",
                         actor="agent:test", guard_mode="enforce",
                         actuator_guards=[{
                             "name": "arr-mcp",
                             "tool_names": ["mcp__sonarr__post"],
                             "command_regexes": ["7878"], "path_globs": []}])
        m.approve()
        v = run_gate(ws, {"tool_name": "mcp__sonarr__post", "command": None,
                          "file_path": None,
                          "tool_input": {"url": "http://h:7878/api"}},
                     actor="hook:custody-gate")
        check("run-gate-mcp-blocks", v["decision"] == "block")
        entry = json.loads(
            (ws / "missions" / "gate-mcp" / "guard-log.jsonl")
            .read_text(encoding="utf-8").splitlines()[-1])
        check("run-gate-mcp-logged", entry["rule"] == "arr-mcp")


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


def test_run_gate_log_failure_keeps_verdict() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp)
        m = Mission.open(ws, "gate-logfail", "i", "operator:test", "agent:test",
                         actor="agent:test", guard_mode="enforce",
                         actuator_guards=GUARDS)
        m.approve()
        # guard-log.jsonl occupied by a directory: the append must fail
        (ws / "missions" / "gate-logfail" / "guard-log.jsonl").mkdir()
        buf = io.StringIO()
        with contextlib.redirect_stderr(buf):
            v = run_gate(ws, {"tool_name": "Bash", "command": "curl :7878/api",
                              "file_path": None}, actor="hook:custody-gate")
        check("run-gate-log-failure-keeps-block",
              v["decision"] == "block" and v["matched"])
        check("run-gate-log-failure-notes-loss",
              "guard-log" in buf.getvalue())


def test_run_gate_multiple_active_allows_loudly() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp)
        m = Mission.open(ws, "gate-multi", "i", "operator:test", "agent:test",
                         actor="agent:test", guard_mode="enforce",
                         actuator_guards=GUARDS)
        m.approve()
        # a duplicated mission dir arriving out-of-band (sync, copy) -- the
        # decoy shape open() now refuses to create itself
        shutil.copytree(m.store.mission_dir, ws / "missions" / "gate-multi-2")
        buf = io.StringIO()
        with contextlib.redirect_stderr(buf):
            v = run_gate(ws, {"tool_name": "Bash", "command": "curl :7878/api",
                              "file_path": None}, actor="hook:custody-gate")
        check("run-gate-multi-active-allows", v["decision"] == "allow")
        check("run-gate-multi-active-warns",
              "multiple active" in buf.getvalue().lower())


if __name__ == "__main__":
    for fn in list(globals().values()):
        if callable(fn) and getattr(fn, "__name__", "").startswith("test_"):
            fn()
    if FAILURES:
        print(f"{len(FAILURES)} FAILURES")
        sys.exit(1)
    print("all green")
