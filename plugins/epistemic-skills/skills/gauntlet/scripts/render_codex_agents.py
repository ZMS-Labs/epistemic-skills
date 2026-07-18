#!/usr/bin/env python3
"""Render canonical gauntlet Markdown roles into Codex user-agent TOML files."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
AGENTS_ROOT = SKILL_ROOT.parent.parent / "agents"


def parse_role(path: Path) -> tuple[str, str, str]:
    source = path.read_text(encoding="utf-8")
    if not source.startswith("---\n"):
        raise ValueError(f"missing YAML frontmatter: {path}")
    _, frontmatter, body = source.split("---", 2)
    fields: dict[str, str] = {}
    for line in frontmatter.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    name = fields.get("name", "")
    description = fields.get("description", "")
    if not name or not description or not body.strip():
        raise ValueError(f"incomplete role definition: {path}")
    return name, description, body.strip() + "\n"


def render(name: str, description: str, instructions: str) -> str:
    return (
        "# Generated from the canonical epistemic-skills Markdown role.\n"
        "# Re-run render_codex_agents.py after upgrading the plugin.\n"
        f"name = {json.dumps(name, ensure_ascii=False)}\n"
        f"description = {json.dumps(description, ensure_ascii=False)}\n"
        f"developer_instructions = {json.dumps(instructions, ensure_ascii=False)}\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    try:
        role_files = sorted(AGENTS_ROOT.glob("gauntlet-*.md"))
        if len(role_files) != 5:
            raise ValueError(f"expected five canonical roles, found {len(role_files)}")
        args.out.mkdir(parents=True, exist_ok=True)
        for role_file in role_files:
            name, description, instructions = parse_role(role_file)
            destination = args.out / f"{name}.toml"
            destination.write_text(
                render(name, description, instructions), encoding="utf-8"
            )
            print(f"render-codex-agents: wrote {destination}")
    except (OSError, ValueError) as exc:
        print(f"render-codex-agents: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
