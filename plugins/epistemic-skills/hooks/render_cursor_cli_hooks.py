#!/usr/bin/env python3
"""Render Cursor CLI hooks with an installed, absolute custody-hook command.

Cursor CLI does not load marketplace-plugin hooks.  Project and user hook
files also do not run from the plugin root, so the plugin-relative IDE
template cannot be copied there unchanged.  This renderer binds both the
Python interpreter and custody hook to their absolute installed paths.
"""
from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path


RELATIVE_COMMAND = (
    "python ./contracts/mission-custody/custody_hook.py --harness cursor"
)


def _shell_command(argv: list[str]) -> str:
    """Quote for the platform on which Cursor will execute the config."""
    if os.name == "nt":
        return subprocess.list2cmdline(argv)
    return shlex.join(argv)


def render() -> dict:
    plugin_root = Path(__file__).resolve().parent.parent
    template_path = plugin_root / "hooks" / "cursor-hooks.json"
    hook_path = (
        plugin_root / "contracts" / "mission-custody" / "custody_hook.py"
    ).resolve()
    python_path = Path(sys.executable).resolve()

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
        if args.output == "-":
            sys.stdout.write(rendered)
            return 0
        destination = Path(args.output).expanduser()
        destination.parent.mkdir(parents=True, exist_ok=True)
        _write_new_config(destination, rendered)
        print(destination.resolve())
        return 0
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"cursor-cli-hook install refused: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
