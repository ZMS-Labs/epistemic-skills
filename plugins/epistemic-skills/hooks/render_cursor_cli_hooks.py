#!/usr/bin/env python3
"""Render Cursor CLI hooks with an installed, absolute custody-hook command.

Cursor CLI does not load marketplace-plugin hooks.  Project and user hook
files also do not run from the plugin root, so the plugin-relative IDE
template cannot be copied there unchanged.  This renderer binds both the
Python interpreter and custody hook to their absolute installed paths.
"""
from __future__ import annotations

import argparse
import io
import json
import os
import re
import shlex
import sys
from pathlib import Path


RELATIVE_COMMAND = (
    "python ./contracts/mission-custody/custody_hook.py --harness cursor"
)

# cmd.exe expands %NAME% even INSIDE double quotes, and no command-line
# escape suppresses it (measured: `"a%USERNAME%b"` -> `aRESOLVEDb`).  Every
# other cmd metacharacter a Windows path may legally hold -- & ^ ( ) $ !,
# whitespace, and a LONE % -- is neutralised by double quotes (measured).
# So: encode what quoting can hold, refuse only what it cannot.
_CMD_EXPANDS = re.compile(r"%[^%]*%")


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
    if _CMD_EXPANDS.search(arg):
        raise RuntimeError(
            f"cannot safely quote {arg!r} for cmd.exe: it contains a "
            "%-delimited name that cmd.exe expands even inside double "
            "quotes, and no command-line escape suppresses it; install to "
            "a path with no '%' pair"
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


def _shell_command(argv: list[str], style: str | None = None) -> str:
    """Quote for the SHELL that will execute the config.

    `subprocess.list2cmdline` is deliberately NOT used here.  It rebuilds an
    argv for CreateProcess and quotes only on whitespace, so an install path
    holding a cmd metacharacter (`C:\\Tools\\R&D\\...`) came out bare: cmd
    split the command at the `&`, handed the interpreter a truncated path,
    and the armed guard exited 1 -- fail OPEN -- while the tail after `&`
    ran as a second command.

    `style` is explicit so both quoters are testable on either platform;
    it defaults to the host.  The Windows branch assumes cmd.exe, which is
    what Cursor's undocumented shell is on Windows in practice.  Delayed
    expansion is off under a plain `cmd /c`, so a `!` in the path is
    literal; under `cmd /v:on` it would still expand.
    """
    if style is None:
        style = "cmd" if os.name == "nt" else "posix"
    if style == "cmd":
        return " ".join(_quote_cmd(arg) for arg in argv)
    if style == "posix":
        return shlex.join(argv)
    raise RuntimeError(f"unknown shell style: {style!r}")


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

    rows_seen = 0
    for event, rows in template.get("hooks", {}).items():
        if not isinstance(rows, list):
            raise RuntimeError(f"Cursor hook event {event!r} is not a list")
        for row in rows:
            if not isinstance(row, dict) or row.get("command") != RELATIVE_COMMAND:
                raise RuntimeError(
                    f"Cursor hook event {event!r} has an unexpected command"
                )
            row["command"] = command
            rows_seen += 1
    if rows_seen == 0:
        raise RuntimeError("Cursor hook template contains no commands")
    return template


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
        destination.parent.mkdir(parents=True, exist_ok=True)
        _write_new_config(destination, rendered)
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"cursor-cli-hook install refused: {exc}", file=sys.stderr)
        return 2

    # The install is COMPLETE from here.  Nothing below may report a refusal.
    _report_installed(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
