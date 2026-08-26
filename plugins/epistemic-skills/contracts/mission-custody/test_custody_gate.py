#!/usr/bin/env python3
"""Unit + integration tests for custody_gate.py."""
from __future__ import annotations

import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from custody_gate import _guard_norm_path, evaluate, run_gate  # noqa: E402
from custody_mission import Mission  # noqa: E402
from custody_store import sha256_file  # noqa: E402

FAILURES: list[str] = []


def check(name: str, cond: bool) -> None:
    if not cond:
        FAILURES.append(name)
        print(f"FAIL {name}")
        # Under pytest the script-style exit-code discipline never runs, so a
        # recorded failure would pass silently (kimi ruling S7): surface it as
        # a real assertion there. Script execution keeps collect-then-exit.
        if "PYTEST_CURRENT_TEST" in os.environ:
            raise AssertionError(f"custody gate check failed: {name}")
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


def test_glob_parent_segment_resolves_for_guard_match() -> None:
    """es#137: a guard on ``M:/Media/**`` must match a write whose lexical
    path carries a parent segment that resolves under Media."""
    guards = [{"name": "g", "tool_names": ["Write"], "command_regexes": [],
               "path_globs": ["M:/Media/**"]}]
    call = {"tool_name": "Write", "command": None, "file_path": "M:/Mediaevil/x"}
    check("glob-mediaevil-rejected",
          not evaluate(auth("enforce", guards), call)["matched"])
    call = {"tool_name": "Write", "command": None, "file_path": "M:/Media/a/b/c.mkv"}
    check("glob-deep-still-matches",
          evaluate(auth("enforce", guards), call)["matched"])
    call = {"tool_name": "Write", "command": None,
            "file_path": "M:/Other/../Media/x.mkv"}
    check("glob-dotdot-resolves-into-guarded-tree",
          evaluate(auth("enforce", guards), call)["matched"])
    call = {"tool_name": "Write", "command": None,
            "file_path": "M:/Media/../etc/passwd"}
    check("glob-dotdot-outside-guarded-tree-not-matched",
          not evaluate(auth("enforce", guards), call)["matched"])


def test_guard_match_is_lexical_symlinked_parent_diverges() -> None:
    """R15 / es#137 residual pin: guard matching collapses ``..`` LEXICALLY,
    while the kernel resolves it only AFTER following symlinks, so a write
    whose real landing site is inside a guarded tree can fail to match an
    armed guard (false-allow direction). This CHARACTERIZATION test pins the
    current invariant (KL-GUARD-LEXICAL / CLM-MC-GUARD-LEXICAL) so a future
    resolution-aware change flips it loudly; it does not assert the
    divergence is desirable."""
    # POSIX-scoped by measurement (kimi ruling S7): on NT, os.path.realpath
    # collapses `..` lexically too, so the write lands OUTSIDE the guarded
    # tree — guard and filesystem AGREE and the pinned divergence does not
    # exist. Running the pin there fails it for the wrong reason (it did,
    # on a symlink-privileged NT host); the disclosure in KL-GUARD-LEXICAL
    # remains POSIX-accurate.
    if os.name == "nt":
        print("  skip guard-lexical pin (POSIX-scoped: NT realpath collapses lexically; the divergence does not exist there)")
        return
    root = Path(tempfile.mkdtemp(prefix="custody-r15-"))
    try:
        (root / "guarded" / "sub").mkdir(parents=True)
        link = root / "link"
        try:
            link.symlink_to(root / "guarded" / "sub", target_is_directory=True)
        except OSError:
            print("  skip guard-lexical pin (symlinks unavailable on this host)")
            return
        base = str(root).replace("\\", "/")
        guards = [{"name": "g", "tool_names": ["Write"], "command_regexes": [],
                   "path_globs": [f"{base}/guarded/**"]}]
        lexical_path = f"{base}/link/../x.txt"
        check("guard-lexical-realpath-lands-in-guarded-tree",
              Path(os.path.realpath(lexical_path)) == root / "guarded" / "x.txt")
        check("guard-lexical-symlinked-parent-not-matched",
              not evaluate(auth("enforce", guards),
                           {"tool_name": "Write", "command": None,
                            "file_path": lexical_path})["matched"])
        check("guard-lexical-collapse-stays-textual",
              _guard_norm_path(lexical_path) == f"{base}/x.txt")
        check("guard-lexical-direct-spelling-still-matched",
              evaluate(auth("enforce", guards),
                       {"tool_name": "Write", "command": None,
                        "file_path": f"{base}/guarded/x.txt"})["matched"])
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_block_reason_names_only_exits_that_work() -> None:
    """The refusal used to say "record an operator grant via `amend`" --
    but `evaluate` reads ONLY guard_mode and actuator_guards, never
    `amendments`, so amendment TEXT discharges nothing however clearly it
    grants the work. That is the dead-end-recipe class this contract has
    now paid for four times: a refusal whose printed exit does not work.
    The message must name only exits that change what the gate reads."""
    guards = [{"name": "no-secrets", "tool_names": ["Write"],
               "command_regexes": [], "path_globs": ["secrets/**"]}]
    call = {"tool_name": "Write", "command": None,
            "file_path": "secrets/x.env"}
    v = evaluate(auth("enforce", guards), call)
    check("block-reason-blocks", v["decision"] == "block")
    reason = v["reason"]
    check("block-reason-names-the-rule", "no-secrets" in reason)
    check("block-reason-says-text-does-not-discharge",
          "does not discharge" in reason)
    check("block-reason-names-the-guards-file-exit",
          "--guards-file" in reason)
    check("block-reason-names-the-audit-exit", "--guard-mode audit" in reason)
    # the negative: it must not advertise bare `amend` as sufficient
    check("block-reason-does-not-advertise-bare-amend",
          "via `amend` or stop" not in reason)


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


def test_workspace_and_suffixed_directory_markers() -> None:
    """The marker's other two edges, found on its second review round.

    './' (and '.\\', and bare '.') normalize to the EMPTY path, which
    compiled to a match-nothing regex: an armed workspace guard covering
    nothing, silently. It now covers everything -- the over-match
    direction, and the one that also catches absolute respellings.

    'foo/**/' already carries subtree semantics including the BASE;
    appending another '/**' required a separator after 'foo', so a write
    to the base itself was silently allowed where plain 'foo/**' matches
    it."""
    for label, globs in (("dot-slash", ["./"]), ("dot-backslash", [".\\"]),
                         ("bare-dot", ["."])):
        g = [{"name": "ws", "tool_names": ["Write"], "command_regexes": [],
              "path_globs": globs}]
        call = {"tool_name": "Write", "command": None,
                "file_path": "docs/x.txt"}
        check(f"guard-workspace-marker-{label}-covers-relative-writes",
              evaluate(auth("enforce", g), call)["matched"])
    g = [{"name": "ws", "tool_names": ["Write"], "command_regexes": [],
          "path_globs": ["./"]}]
    call = {"tool_name": "Write", "command": None, "file_path": "/etc/passwd"}
    check("guard-workspace-marker-catches-absolute-respellings",
          evaluate(auth("enforce", g), call)["matched"])
    # The literal EMPTY STRING is NOT a workspace marker: it expresses no
    # directory intent, passes the validator, and has always been inert --
    # flipping it to block-everything would be an undisclosed enforcement
    # change on armed fleets. It keeps its historical nothing-matches
    # behavior, deliberately.
    empty = [{"name": "ph", "tool_names": ["Write"], "command_regexes": [],
              "path_globs": [""]}]
    call = {"tool_name": "Write", "command": None, "file_path": "docs/x.txt"}
    check("guard-empty-string-placeholder-stays-inert",
          not evaluate(auth("enforce", empty), call)["matched"])
    suffixed = [{"name": "sub", "tool_names": ["Write"],
                 "command_regexes": [], "path_globs": ["foo/**/"]}]
    for label, path, expect in (
            ("base-still-matched", "foo", True),
            ("descendant-matched", "foo/a/b.txt", True),
            ("sibling-not-matched", "foobar", False)):
        call = {"tool_name": "Write", "command": None, "file_path": path}
        check(f"guard-doublestar-slash-{label}",
              evaluate(auth("enforce", suffixed), call)["matched"] is expect)
    # 'foo/*/' keeps its narrower meaning: subtrees one level down, not foo
    starred = [{"name": "star", "tool_names": ["Write"],
                "command_regexes": [], "path_globs": ["foo/*/"]}]
    for label, path, expect in (
            ("child-subtree-matched", "foo/x/y.txt", True),
            ("base-not-matched", "foo", False)):
        call = {"tool_name": "Write", "command": None, "file_path": path}
        check(f"guard-single-star-slash-{label}",
              evaluate(auth("enforce", starred), call)["matched"] is expect)


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
            "tool_input": {"url": "http://203.0.113.10:7878/api/v3/series",
                           "method": "POST"}}
    v = evaluate(auth("enforce", guards), call)
    check("eval-mcp-serialized-args-block",
          v["decision"] == "block" and v["rule"] == "arr-mcp")
    safe = {"tool_name": "mcp__sonarr__post", "command": None,
            "file_path": None,
            "tool_input": {"url": "http://203.0.113.10:8989/api/v3/series"}}
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


def test_run_gate_multiple_active_evaluates_the_union() -> None:
    # es#173: plurality is legal and the old inert-on-plurality fail-open is
    # DELETED -- a duplicated mission dir arriving out-of-band (sync, copy)
    # now contributes its guards to the union like any approved mission, and
    # a block names every matching (mission, rule) pair.
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp)
        m = Mission.open(ws, "gate-multi", "i", "operator:test", "agent:test",
                         actor="agent:test", guard_mode="enforce",
                         actuator_guards=GUARDS)
        m.approve()
        shutil.copytree(m.store.mission_dir, ws / "missions" / "gate-multi-2")
        v = run_gate(ws, {"tool_name": "Bash", "command": "curl :7878/api",
                          "file_path": None}, actor="hook:custody-gate")
        check("run-gate-multi-active-blocks", v["decision"] == "block")
        check("run-gate-multi-active-names-both-missions",
              "gate-multi" in v["reason"] and "gate-multi-2" in v["reason"])
        for name in ("gate-multi", "gate-multi-2"):
            check(f"run-gate-multi-active-logs-{name}",
                  (ws / "missions" / name / "guard-log.jsonl").exists())


# --- Codex MODERATE/MINOR triage, 2026-08-25 ------------------------------


def test_union_excludes_unaddressable_mission_dirs() -> None:
    """A store copied to a name no binding can ever name (`missions/.backup`)
    used to ARM enforce guards nobody could discharge: `Mission.load` refuses
    the id before it opens the store, so the documented per-mission exits are
    unreachable. It must degrade, not arm."""
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp)
        m = Mission.open(ws, "gate-legal", "i", "operator:test", "agent:test",
                         actor="agent:test", guard_mode="enforce",
                         actuator_guards=GUARDS)
        m.approve()
        shutil.copytree(m.store.mission_dir, ws / "missions" / ".backup")
        buf = io.StringIO()
        with contextlib.redirect_stderr(buf):
            v = run_gate(ws, {"tool_name": "Bash", "command": "curl :7878/api",
                              "file_path": None}, actor="hook:custody-gate")
        check("union-illegal-dir-still-blocks-on-the-legal-mission",
              v["decision"] == "block")
        check("union-illegal-dir-not-armed",
              all(row["mission"] == "gate-legal"
                  for row in v.get("matches", [])))
        check("union-illegal-dir-disclosed",
              "UNION DEGRADED" in v["reason"] and ".backup" in v["reason"])
        check("union-illegal-dir-logged-no-guard-log",
              not (ws / "missions" / ".backup" / "guard-log.jsonl").exists())


def test_all_degraded_union_discloses_on_stderr_too() -> None:
    """The `if not entries:` branch composed the degradation into `reason` and
    printed nothing, so a workspace whose ONLY missions are unreadable
    produced an allow whose sole stderr line never says guards are not
    enforced."""
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp)
        broken = ws / "missions" / "m-broken" / "checkpoints"
        broken.mkdir(parents=True)
        (broken / "r00000001.json").write_text("{not json", encoding="utf-8")
        buf = io.StringIO()
        with contextlib.redirect_stderr(buf):
            v = run_gate(ws, {"tool_name": "Bash", "command": "curl :7878/api",
                              "file_path": None}, actor="hook:custody-gate")
        check("all-degraded-allows", v["decision"] == "allow")
        check("all-degraded-reason-discloses",
              "UNION DEGRADED" in v["reason"])
        check("all-degraded-stderr-discloses",
              "UNION DEGRADED" in buf.getvalue())


def test_unmatched_mixed_union_reports_the_strongest_posture() -> None:
    """The unmatched-call `mode` was read from the alphabetically first armed
    mission, so `a-audit` + `z-enforce` reported "audit" over an enforcing
    workspace."""
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp)
        for name, mode in (("a-audit", "audit"), ("z-enforce", "enforce")):
            m = Mission.open(ws, name, "i", "operator:test", "agent:test",
                             actor="agent:test", guard_mode=mode,
                             actuator_guards=GUARDS)
            m.approve()
        v = run_gate(ws, {"tool_name": "Bash", "command": "echo nothing",
                          "file_path": None}, actor="hook:custody-gate")
        check("mixed-union-unmatched-allows",
              v["decision"] == "allow" and not v["matched"])
        check("mixed-union-reports-enforce", v["mode"] == "enforce")
        check("mixed-union-says-it-is-mixed", "MIXED" in v["reason"])


def test_environmental_read_failure_degrades_the_union_it_does_not_abort() -> None:
    """One unreadable mission dir must not silence every OTHER mission's
    guards.

    `Mission._discover` deliberately propagates environmental OSErrors so that
    `open` does not reroute around a mission that is merely busy and invite a
    duplicate open. For the gate that reasoning inverts: the exception escaped
    `_union_entries`, the hook caught it at the workspace boundary, and an
    approved enforce-mode mission's BLOCK became a silent allow. Measured
    before the fix by injecting PermissionError for one mission's checkpoint
    read: `run_gate` raised instead of blocking, so the healthy sibling never
    voted.

    The failure is injected at the read the discovery walk performs, which is
    where a locked or permission-denied store actually fails."""
    import custody_mission
    import custody_store

    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp)
        blocked = Mission.open(ws, "a-blocked", "i", "operator:test",
                               "agent:test", actor="agent:test")
        blocked.approve()
        healthy = Mission.open(ws, "z-healthy", "i", "operator:test",
                               "agent:test", actor="agent:test",
                               guard_mode="enforce", actuator_guards=GUARDS)
        healthy.approve()

        real_load = custody_store.MissionStore.load_latest
        target = (ws / "missions" / "a-blocked").resolve()

        def refusing_load(self):
            if Path(self.mission_dir).resolve() == target:
                raise PermissionError(13, "Permission denied")
            return real_load(self)

        custody_store.MissionStore.load_latest = refusing_load
        try:
            verdict = run_gate(
                ws, {"tool_name": "Bash", "command": "curl :7878/api/v3",
                     "file_path": None}, actor="hook:custody-gate")
        finally:
            custody_store.MissionStore.load_latest = real_load

        check("unreadable-sibling-does-not-suppress-a-real-block",
              verdict["decision"] == "block")
        check("unreadable-sibling-block-names-the-healthy-mission",
              "z-healthy" in verdict["reason"])
        check("unreadable-sibling-loss-is-disclosed",
              "DEGRADED" in verdict["reason"].upper()
              or "a-blocked" in verdict["reason"])

    # CONTROL: with nothing unreadable, the same call must still block and the
    # verdict must NOT claim degradation -- a gate that always says "degraded"
    # has stopped distinguishing.
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp)
        healthy = Mission.open(ws, "z-healthy", "i", "operator:test",
                               "agent:test", actor="agent:test",
                               guard_mode="enforce", actuator_guards=GUARDS)
        healthy.approve()
        verdict = run_gate(
            ws, {"tool_name": "Bash", "command": "curl :7878/api/v3",
                 "file_path": None}, actor="hook:custody-gate")
        check("clean-union-still-blocks", verdict["decision"] == "block")
        check("clean-union-claims-no-degradation",
              "DEGRADED" not in verdict["reason"].upper())


def test_verification_reread_oserror_degrades_the_union() -> None:
    """The discovery walk's OSError arm covers the FIRST read; the union
    then re-reads every discovered mission through `mission.status()`,
    whose handler caught only (StoreError, ValueError, CustodyError). A
    mission that becomes unreadable BETWEEN the two reads (a lock or
    permission change) raised OSError out of `_union_entries`, `run_gate`
    propagated, and the hook caught it at the workspace boundary and failed
    OPEN -- the silent-allow class the discovery fix closed, one read
    later."""
    import custody_store

    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp)
        flaky = Mission.open(ws, "a-flaky", "i", "operator:test",
                             "agent:test", actor="agent:test")
        flaky.approve()
        healthy = Mission.open(ws, "z-healthy", "i", "operator:test",
                               "agent:test", actor="agent:test",
                               guard_mode="enforce", actuator_guards=GUARDS)
        healthy.approve()

        real_load = custody_store.MissionStore.load_latest
        target = (ws / "missions" / "a-flaky").resolve()
        reads = {"n": 0}

        def failing_second_read(self):
            if Path(self.mission_dir).resolve() == target:
                reads["n"] += 1
                if reads["n"] > 1:
                    raise PermissionError(13, "Permission denied")
            return real_load(self)

        custody_store.MissionStore.load_latest = failing_second_read
        verdict = None
        try:
            try:
                verdict = run_gate(
                    ws, {"tool_name": "Bash", "command": "curl :7878/api/v3",
                         "file_path": None}, actor="hook:custody-gate")
            except PermissionError:
                pass
        finally:
            custody_store.MissionStore.load_latest = real_load

        check("reread-oserror-run-gate-does-not-raise",
              verdict is not None)
        check("reread-oserror-does-not-suppress-a-real-block",
              verdict is not None and verdict["decision"] == "block")
        check("reread-oserror-block-names-the-healthy-mission",
              verdict is not None and "z-healthy" in verdict["reason"])
        check("reread-oserror-loss-is-disclosed",
              verdict is not None
              and ("DEGRADED" in verdict["reason"].upper()
                   or "a-flaky" in verdict["reason"]))

    # CONTROL: with nothing failing, the same call blocks and the verdict
    # claims no degradation.
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp)
        healthy = Mission.open(ws, "z-healthy", "i", "operator:test",
                               "agent:test", actor="agent:test",
                               guard_mode="enforce", actuator_guards=GUARDS)
        healthy.approve()
        verdict = run_gate(
            ws, {"tool_name": "Bash", "command": "curl :7878/api/v3",
                 "file_path": None}, actor="hook:custody-gate")
        check("reread-control-still-blocks", verdict["decision"] == "block")
        check("reread-control-claims-no-degradation",
              "DEGRADED" not in verdict["reason"].upper())


if __name__ == "__main__":
    for fn in list(globals().values()):
        if callable(fn) and getattr(fn, "__name__", "").startswith("test_"):
            fn()
    if FAILURES:
        print(f"{len(FAILURES)} FAILURES")
        sys.exit(1)
    print("all green")
