#!/usr/bin/env python3
"""Render Cursor CLI hooks with an installed, absolute custody-hook command.

Cursor CLI does not load marketplace-plugin hooks.  Project and user hook
files also do not run from the plugin root, so the plugin-relative IDE
template cannot be copied there unchanged.  This renderer binds both the
Python interpreter and custody hook to their absolute installed paths.

That binding is MACHINE-LOCAL.  Committed to a shared repository, the
rendered config points every collaborator's Cursor at files that exist
only on the authoring machine -- a shared interpreter exits 2 (cannot
open the hook script), which Cursor reads as a custody BLOCK on every
matching tool call with a refusal custody never issued, and a missing
interpreter exits 1, which fails open.  `_version_control_gate` keeps the
generated file out of version control; see README.md, "Cursor CLI".
"""
from __future__ import annotations

import argparse
import io
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path


RELATIVE_COMMAND = (
    "python ./contracts/mission-custody/custody_hook.py --harness cursor"
)

# Every Cursor event the custody gate must be wired into.  Rendering
# REFUSES if the canonical template stops carrying a command for any of
# them, so a template that silently drops a guarded event cannot install
# as a config that looks armed but leaves that actuator class open.
# An event ADDED to the template is carried through, not rejected --
# over-refusal here would be its own outage.
REQUIRED_EVENTS = ("beforeShellExecution", "preToolUse", "beforeMCPExecution")

# The tool coverage a preToolUse matcher must preserve.  The gate can only
# evaluate what the config delivers: Shell carries the command the command
# guards match, Write and Delete carry the file_path the path guards
# match.  A matcher narrowed to "Shell" still passes a command-string
# check while Write/Delete calls never reach the gate (Codex es#216 thread
# r3858530080) -- a config that looks armed with the file-mutating
# actuator class open.  No matcher at all is FULL coverage and passes.
REQUIRED_TOOL_COVERAGE = {"preToolUse": ("Shell", "Write", "Delete")}

# Events whose payloads the gate must see in FULL.  Their matcher field
# filters by payload TEXT (the shell command string, the MCP tool name) --
# narrowing there pre-empts the mission's own guard regexes, which are the
# only place that decision may live.
MATCHERLESS_EVENTS = ("beforeShellExecution", "beforeMCPExecution")

# cmd.exe expands %NAME% even INSIDE double quotes, and no command-line
# escape suppresses it (measured: `"a%USERNAME%b"` -> `aRESOLVEDb`).  Every
# other cmd metacharacter a Windows path may legally hold -- & ^ ( ) $ !,
# and whitespace -- IS neutralised by double quotes (measured).  So: encode
# what quoting can hold, refuse what it cannot.
#
# '%' is refused OUTRIGHT, not just as a `%...%` pair.  Two earlier, weaker
# rules both failed, and for the same reason -- each was measured in one
# execution context and generalised to "Windows":
#
#   1. per-argument `%...%` only.  Two arguments each holding ONE '%' pass
#      individually and then JOIN into a pair (Codex es#216):
#      `"C:\100%done\python.exe" "C:\100%done\hook.py"`.
#   2. "a LONE % is safe".  True under `cmd /c`, FALSE in a batch file:
#          cmd /c  echo "C:\100%done\x"  ->  "C:\100%done\x"
#          a .bat  echo "C:\100%done\x"  ->  "C:\100done\x"     (EATEN)
#
# Cursor does not document which shell runs a hook command on Windows, so
# the renderer cannot know which rule applies.  Measured end-to-end: a
# plugin installed under `100%done` rendered exit 0, and the emitted
# command run from a batch file exited 2 WITHOUT naming a rule -- python
# could not open `...100done\custody_hook.py`.  Cursor reads that as a
# custody BLOCK on every tool call carrying a refusal custody never
# issued: the same fabricated-refusal class as the resolved-symlink bug.
# Refusing every '%' makes a pair unconstructible and is context-free.
#
# The cost is deliberate: a legitimate '%' install path cannot be rendered
# on Windows.  That fails CLOSED at install time, loudly, with nothing
# written -- the alternative fails open (or fabricates a block) at runtime.
_CMD_UNSAFE = "%"

# Characters an argument may hold and still be emitted BARE to cmd.exe.
# Kept deliberately narrow -- exactly what an ordinary Windows path needs.
# Everything else (space, & | < > ( ) ^ " ' ` , ; = ! ~ + @ # $ [ ] { } and
# any character not listed) is quoted.  Narrowing is always safe here; the
# only cost of a redundant quote is that the line may start with one.
# WIDENING is not safe: admit a cmd metacharacter and that argument goes
# out bare, cmd splits the command at it, and the armed guard exits 1 --
# the original fail-open.  Pinned by the test-suite constant
# CMD_METACHARACTERS, which asserts every one of them still forces quotes.
_CMD_SAFE_CHARS = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
    "0123456789"
    "\\/:._-"
)


def _link_preserving(path: str | os.PathLike[str]) -> Path:
    """Make `path` absolute WITHOUT resolving symlinks or junctions.

    The install this renderer serves is a *retargetable* link (README.md,
    "Cursor"): `ln -sfn .../plugins/epistemic-skills ~/.cursor/plugins/
    local/epistemic-skills` on POSIX, `mklink /J` on Windows, pointed at a
    versioned checkout.  `Path.resolve()` collapses that link and bakes the
    checkout path into hooks.json, so the ordinary upgrade -- re-point the
    link at the new tag, delete the old checkout -- leaves the armed gate
    naming a path that no longer exists.  It then stops being a gate: the
    interpreter exits 2 because it cannot open the script, which Cursor
    reads as a custody BLOCK on every tool call, with a refusal message
    custody never issued.  Binding to the link instead keeps the gate live
    across upgrades, and an actual uninstall still fails closed.
    """
    return Path(path).absolute()


def _quote_cmd(arg: str) -> str:
    """Quote one argument for cmd.exe *and* the CreateProcess argv parser."""
    if _CMD_UNSAFE in arg:
        raise RuntimeError(
            f"cannot safely quote {arg!r} for a Windows shell: it contains "
            "'%'.  cmd.exe expands a %-delimited name even inside double "
            "quotes, a batch file strips a lone '%' outright, and two "
            "arguments holding one '%' each join into a pair -- and Cursor "
            "does not document which shell runs the hook.  Install to a "
            "path with no '%' in it."
        )
    if any(ch in arg for ch in "\n\r\x00"):
        raise RuntimeError(f"argument is not a single shell word: {arg!r}")
    out = ['"']
    backslashes = 0
    for char in arg:
        if char == "\\":
            backslashes += 1
            continue
        if char == '"':
            out.append("\\" * (backslashes * 2 + 1))
            out.append('"')
        else:
            out.append("\\" * backslashes)
            out.append(char)
        backslashes = 0
    out.append("\\" * (backslashes * 2))
    out.append('"')
    return "".join(out)


def _needs_cmd_quoting(arg: str) -> bool:
    """True unless EVERY character of `arg` is known safe bare to cmd.exe.

    Deliberately a WHITELIST.  A blacklist of metacharacters fails open on
    the character nobody enumerated -- it emits that argument bare and cmd
    splits the command there.  This fails closed on it: an unrecognised
    character means quote, and the worst case is a redundant quote.
    """
    return not arg or not all(ch in _CMD_SAFE_CHARS for ch in arg)


def _shell_command(argv: list[str], style: str | None = None) -> str:
    """Quote for the SHELL that will execute the config.

    `subprocess.list2cmdline` is deliberately NOT used here.  It rebuilds an
    argv for CreateProcess and quotes only on whitespace, so an install path
    holding a cmd metacharacter (`C:\\Tools\\R&D\\...`) came out bare: cmd
    split the command at the `&`, handed the interpreter a truncated path,
    and the armed guard exited 1 -- fail OPEN -- while the tail after `&`
    ran as a second command.

    `style` is explicit so both quoters are testable on either platform;
    it defaults to the host.

    The Windows branch quotes MINIMALLY, and that is load-bearing rather
    than cosmetic.  `cmd /?` documents that for `cmd /c <command>`, when
    the line begins with a quote and holds more than two, cmd strips the
    FIRST quote and the LAST quote on the line.  Quoting every argument
    therefore destroyed the command under a bare `cmd /c` -- for EVERY
    install path, including one with no space and no metacharacter in it
    (measured: rc 1, "The filename, directory name, or volume label
    syntax is incorrect"; the guard never ran, and exit 1 is fail OPEN).
    `subprocess(shell=True)` emits `cmd /d /s /c "<command>"` and a batch
    file re-parses per line, so both supply or absorb the outer pair and
    mask the defect entirely -- which is why proving the command through
    only those two contexts licensed nothing about a bare `cmd /c`.

    Quoting only what needs it keeps the metacharacter fix (`R&D` is not
    in `_CMD_SAFE_CHARS`, so it is still quoted) and leaves the line
    starting bare whenever the interpreter path needs no quoting, which
    is the case cmd's rule can be got past at all.

    What stays shell-dependent is narrower but real, and is recorded in
    README.md as UNADDRESSED rather than assumed away: an interpreter
    path that itself needs quoting is unrescuable under a bare `cmd /c`
    (no quoting survives the rule); `!` is literal under a plain
    `cmd /c` but expands under `cmd /v:on`; and under PowerShell a quoted
    leading token is a string expression, not a command.  `%` is refused
    outright (see `_CMD_UNSAFE`) because its meaning is what differs
    between `cmd /c` and a batch file.
    """
    if style is None:
        style = "cmd" if os.name == "nt" else "posix"
    if style == "cmd":
        # Refuse '%' for EVERY argument, independently of the quoting
        # decision: a bare argument never reaches `_quote_cmd`, so the
        # refusal cannot be allowed to ride on the whitelist.
        for arg in argv:
            if _CMD_UNSAFE in arg:
                _quote_cmd(arg)
        return " ".join(
            _quote_cmd(arg) if _needs_cmd_quoting(arg) else arg
            for arg in argv
        )
    if style == "posix":
        return shlex.join(argv)
    raise RuntimeError(f"unknown shell style: {style!r}")


def _validate_matcher_coverage(event: str, row: dict) -> None:
    """Refuse a matcher that narrows a guarded event below what custody
    needs -- the drift check's command-string comparison cannot see it.

    The matcher is a JavaScript regex; it is evaluated here as a Python
    regex.  The two dialects agree on the alternations this template
    carries, and a pattern Python cannot compile is REFUSED rather than
    waved through: an unverifiable matcher cannot be proven to cover the
    required tools, so failing closed is the only sound reading.
    """
    matcher = row.get("matcher")
    if event in MATCHERLESS_EVENTS:
        if matcher:
            raise RuntimeError(
                f"Cursor hook event {event!r} carries a matcher "
                f"({matcher!r}).  That narrows delivery by payload text, "
                "pre-empting the mission's own guard regexes: the gate "
                "must see every payload for this event."
            )
        return
    required = REQUIRED_TOOL_COVERAGE.get(event)
    if not required or not matcher:
        # no matcher: the row fires for every tool call -- full coverage
        return
    if not isinstance(matcher, str):
        raise RuntimeError(
            f"Cursor hook event {event!r} has a non-string matcher: "
            f"{matcher!r}"
        )
    try:
        pattern = re.compile(matcher)
    except re.error as exc:
        raise RuntimeError(
            f"Cursor hook event {event!r} matcher {matcher!r} does not "
            f"compile ({exc}); coverage cannot be proven"
        ) from exc
    uncovered = [tool for tool in required if not pattern.search(tool)]
    if uncovered:
        raise RuntimeError(
            f"Cursor hook event {event!r} matcher {matcher!r} no longer "
            f"covers {', '.join(uncovered)}.  Those tool calls would "
            "never reach the custody gate, installing a config that "
            "looks armed while that actuator class is open."
        )


def render() -> dict:
    plugin_root = _link_preserving(__file__).parent.parent
    template_path = plugin_root / "hooks" / "cursor-hooks.json"
    hook_path = (
        plugin_root / "contracts" / "mission-custody" / "custody_hook.py"
    )
    if not sys.executable:
        raise RuntimeError(
            "no interpreter to bind: sys.executable is empty"
        )
    python_path = _link_preserving(sys.executable)

    if not hook_path.is_file():
        raise RuntimeError(f"installed custody hook not found: {hook_path}")
    template = json.loads(template_path.read_text(encoding="utf-8"))
    command = _shell_command(
        [str(python_path), str(hook_path), "--harness", "cursor"]
    )

    rendered_per_event: dict[str, int] = {}
    for event, rows in template.get("hooks", {}).items():
        if not isinstance(rows, list):
            raise RuntimeError(f"Cursor hook event {event!r} is not a list")
        for row in rows:
            if not isinstance(row, dict) or row.get("command") != RELATIVE_COMMAND:
                raise RuntimeError(
                    f"Cursor hook event {event!r} has an unexpected command"
                )
            _validate_matcher_coverage(event, row)
            row["command"] = command
            rendered_per_event[event] = rendered_per_event.get(event, 0) + 1

    # Counting rows across the WHOLE template only ever required ONE row
    # anywhere, so dropping or emptying a guarded event still rendered a
    # config that installed cleanly with that actuator class unguarded --
    # a fail-open inside the fail-closed drift policy (Codex es#216).
    # Measured before this fix: deleting `beforeMCPExecution`, emptying it,
    # deleting `preToolUse`, and deleting all but one event each left
    # render SUCCEEDING.  Every guarded event must now carry a command.
    missing = [event for event in REQUIRED_EVENTS
               if not rendered_per_event.get(event)]
    if missing:
        raise RuntimeError(
            "Cursor hook template is missing a command for required "
            f"event(s): {', '.join(missing)}.  Rendering would install a "
            "config leaving that actuator class unguarded."
        )
    return template


def _git_probe(args: list[str], cwd: Path) -> subprocess.CompletedProcess | None:
    """Run a read-only git query; None when git itself cannot run."""
    try:
        return subprocess.run(["git", *args], cwd=str(cwd),
                              capture_output=True, text=True)
    except OSError:
        return None


def _version_control_gate(destination: Path) -> tuple[str | None, str | None]:
    """Keep the machine-local config out of version control.

    Returns (refusal, notice).  The rendered command binds THIS machine's
    interpreter and plugin paths.  Committed to a shared repository it
    points every collaborator's Cursor at files that exist only on the
    authoring machine: a shared interpreter exits 2 -- cannot open the
    hook script -- which Cursor reads as a custody BLOCK on every matching
    tool call, with a refusal custody never issued (measured end-to-end:
    rendered as the author, committed, cloned, the author's plugin tree
    deleted, the committed command run -> exit 2 naming no rule), and a
    missing interpreter exits 1, which fails OPEN (Codex es#216 thread
    r3858335200).

    A portable committed form was considered and rejected: the command
    still has to name an interpreter and a script, and no cross-platform
    spelling exists -- Cursor's own guidance is that shebang scripts do
    not run on Windows (use .cmd or an explicit interpreter), git does not
    restore the execute bit on Windows clones, and Cursor documents no
    variable expansion inside command strings.  The machine binding is
    exactly what this renderer exists to compute, so the generated file
    is machine-local and this gate refuses the two shapes that would put
    it into version control silently:

      * a destination git already TRACKS, and
      * ANY .cursor/hooks.json inside the worktree that git does not
        IGNORE -- Cursor opened on the directory above it (including a
        NESTED directory, e.g. a monorepo package) auto-loads it as the
        project hooks file.

    Anything else inside a worktree that git does not ignore renders, with
    a notice: the hazard there needs a manual commit AND a manual copy
    into place, which no install-time gate can reach.
    """
    probe_dir = destination.parent
    while not probe_dir.is_dir():
        # the destination's parent chain need not exist yet; the nearest
        # existing ancestor answers the worktree question just as well
        if probe_dir.parent == probe_dir:
            return None, None
        probe_dir = probe_dir.parent
    probe = _git_probe(["rev-parse", "--show-toplevel"], probe_dir)
    if probe is None or probe.returncode != 0:
        # no git, or outside any worktree: nothing to prove with, and no
        # version-control path for the file to leak through
        return None, None
    root = probe.stdout.strip()

    def norm(p: str) -> str:
        # realpath, not normpath alone: git reports the worktree root in
        # resolved terms, so on macOS an unresolved destination under
        # /var/folders would compare against a /private/var/folders root
        # and silently escape the gate.  This resolution only feeds the
        # gate's path MATH; the rendered command still binds the
        # link-preserving spelling (see `_link_preserving`).
        return os.path.normcase(os.path.normpath(os.path.realpath(p)))

    root_norm = norm(root)
    try:
        rel = os.path.relpath(norm(str(destination)), root_norm)
    except ValueError:
        return None, None  # different drive on Windows
    if rel == ".." or rel.startswith(".." + os.sep):
        return None, None
    rel_posix = rel.replace(os.sep, "/")

    tracked = _git_probe(["ls-files", "--error-unmatch", "--", rel_posix],
                         Path(root))
    if tracked is not None and tracked.returncode == 0:
        return (
            f"{destination} is tracked by git at {root}.  The rendered "
            "config binds this machine's interpreter and plugin paths and "
            "is machine-local: committed, it fabricates a custody block "
            "(or fails open) on every collaborator's machine.  Remove it "
            "from the index (`git rm --cached`) and ignore it, or render "
            "to stdout (the default) and merge by hand.",
            None,
        )

    ignored = _git_probe(["check-ignore", "-q", "--", rel_posix],
                         Path(root))
    if ignored is not None and ignored.returncode == 0:
        return None, None  # git ignores it: it cannot be committed by accident

    # The shape Cursor auto-loads as project hooks is ANY
    # `.cursor/hooks.json` inside the worktree, not only the root one:
    # Cursor opened on a NESTED directory (a monorepo package, say
    # repo/packages/app) loads packages/app/.cursor/hooks.json as the
    # project hooks file.  The destination is already known to sit inside
    # this worktree, so the final two segments decide.
    destination_parts = Path(norm(str(destination))).parts
    if len(destination_parts) >= 2 and \
            destination_parts[-2] == os.path.normcase(".cursor") and \
            destination_parts[-1] == os.path.normcase("hooks.json"):
        return (
            f"{destination} is a project-hooks file Cursor auto-loads "
            f"(.cursor/hooks.json at {rel_posix} in the worktree at "
            f"{root}), and git does not ignore it.  "
            "The rendered config binds this machine's interpreter and "
            "plugin paths and is machine-local: committed, it fabricates "
            "a custody block (or fails open) on every collaborator's "
            "machine.  Add '.cursor/hooks.json' to the .gitignore beside "
            f"the project root (or '{rel_posix}' to the worktree root's) "
            "FIRST, then re-render; or render to stdout (the "
            "default) and merge by hand.",
            None,
        )

    return None, (
        f"cursor-cli-hook note: {destination} sits inside the git "
        f"worktree at {root} and is not ignored.  The rendered config is "
        "machine-local (it binds this machine's interpreter and plugin "
        "paths) -- do not commit it."
    )


def _report_notice(notice: str) -> None:
    """Best-effort stderr notice; never raises, never changes exit status."""
    try:
        sys.stderr.write(notice + "\n")
        sys.stderr.flush()
    except (OSError, ValueError):
        pass


def _write_new_config(destination: Path, rendered: str) -> None:
    """Create a config without leaving a partial file after I/O failure."""
    created = False
    try:
        with destination.open("x", encoding="utf-8", newline="\n") as handle:
            created = True
            handle.write(rendered)
    except OSError:
        if created:
            try:
                destination.unlink()
            except FileNotFoundError:
                pass
        raise


def _neutralise_stdout() -> None:
    """Stop a dead stdout from re-raising during interpreter shutdown.

    CPython flushes sys.stdout while finalising and exits 120 if that fails,
    whatever main() returned (measured with a real broken pipe).  Catching
    the write alone would therefore NOT have closed this: the descriptor has
    to be repointed at the null device as well.
    """
    try:
        fileno = sys.stdout.fileno()
    except (AttributeError, OSError, ValueError):
        fileno = None
    if fileno is not None:
        try:
            null_fd = os.open(os.devnull, os.O_WRONLY)
        except OSError:
            null_fd = None
        if null_fd is not None:
            try:
                os.dup2(null_fd, fileno)
            except OSError:
                pass
            finally:
                try:
                    os.close(null_fd)
                except OSError:
                    pass
    try:
        sys.stdout = io.TextIOWrapper(io.BytesIO(), encoding="utf-8")
    except Exception:  # pragma: no cover - last resort sink
        sys.stdout = io.StringIO()


def _report_installed(destination: Path) -> None:
    """Announce a COMPLETED install.

    Never raises, and never changes the exit status.  By the time this runs
    the config is on disk and complete; reporting "install refused" would be
    a false statement that no retry can reconcile, because the retry can
    only fail with "File exists".  If stdout is dead the destination still
    goes to stderr, so the path is not lost silently.
    """
    line = f"{destination}\n"
    try:
        sys.stdout.write(line)
        sys.stdout.flush()
        return
    except (OSError, ValueError):
        pass
    _neutralise_stdout()
    try:
        sys.stderr.write(
            f"cursor-cli-hook installed (stdout unavailable): {line}"
        )
        sys.stderr.flush()
    except (OSError, ValueError):
        pass


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="-",
        help="destination hooks.json, or - for stdout (existing files refuse)",
    )
    args = parser.parse_args(argv)

    try:
        rendered = json.dumps(render(), indent=2, ensure_ascii=True) + "\n"
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"cursor-cli-hook install refused: {exc}", file=sys.stderr)
        return 2

    if args.output == "-":
        # stdout IS the product on this path, so a write failure is a real
        # failure and must still refuse.
        try:
            sys.stdout.write(rendered)
            sys.stdout.flush()
        except (OSError, ValueError) as exc:
            _neutralise_stdout()
            print(f"cursor-cli-hook install refused: {exc}", file=sys.stderr)
            return 2
        return 0

    try:
        destination = _link_preserving(Path(args.output).expanduser())
        refusal, notice = _version_control_gate(destination)
        if refusal is not None:
            print(f"cursor-cli-hook install refused: {refusal}",
                  file=sys.stderr)
            return 2
        destination.parent.mkdir(parents=True, exist_ok=True)
        _write_new_config(destination, rendered)
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"cursor-cli-hook install refused: {exc}", file=sys.stderr)
        return 2

    # The install is COMPLETE from here.  Nothing below may report a refusal.
    if notice is not None:
        _report_notice(notice)
    _report_installed(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
