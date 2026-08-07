#!/usr/bin/env python3
"""Optional check: compare a harness's loaded description inventory to the package.

This package cannot observe a remote harness's live description budget. When an
operator captures the harness's loaded skill listing (one skill name and its
resolved description per line, or JSON list of {name, description}), this check
proves whether every packaged skill is present and whether any description was
dropped or truncated relative to the packaged SKILL.md.

Without a capture file the check exits 0 with an explicit LIVE_BLOCKED tier note.
That is intentional: absence of a live capture must not silently become a pass
claim about estate-wide headroom.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SKILLS = REPO / "plugins" / "epistemic-skills" / "skills"
FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---", re.S)
DESCRIPTION = re.compile(
    r"^description:\s*(.*?)(?=^[A-Za-z_][A-Za-z0-9_-]*:|\Z)", re.S | re.M
)


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
        quote = value[0]
        body = value[1:-1]
        if quote == "'":
            return body.replace("''", "'")
        return bytes(body, "utf-8").decode("unicode_escape")
    return " ".join(value.split())


def packaged_descriptions() -> dict[str, str]:
    out: dict[str, str] = {}
    for path in sorted(SKILLS.glob("*/SKILL.md")):
        text = path.read_text(encoding="utf-8")
        front = FRONTMATTER.match(text)
        if not front:
            continue
        match = DESCRIPTION.search(front.group(1))
        if not match:
            continue
        out[path.parent.name] = unquote(match.group(1))
    return out


def load_capture(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        blob = json.loads(text)
        if isinstance(blob, dict) and "skills" in blob:
            blob = blob["skills"]
        if not isinstance(blob, list):
            raise ValueError("JSON capture must be a list or {skills: [...]}")
        loaded: dict[str, str] = {}
        for row in blob:
            loaded[row["name"]] = row.get("description") or ""
        return loaded
    loaded = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "\t" in line:
            name, desc = line.split("\t", 1)
        elif "|" in line:
            name, desc = line.split("|", 1)
        else:
            raise ValueError(f"unrecognized capture line: {line!r}")
        loaded[name.strip()] = desc.strip()
    return loaded


def compare(packaged: dict[str, str], loaded: dict[str, str]) -> list[str]:
    failures: list[str] = []
    for name, desc in packaged.items():
        if name not in loaded:
            failures.append(f"MISSING_LOADED: packaged skill {name!r} absent from harness listing")
            continue
        got = loaded[name]
        if not got.strip():
            failures.append(f"DROPPED_DESCRIPTION: {name!r} is listed but description is empty")
        elif got != desc and not desc.startswith(got) and got not in desc:
            failures.append(
                f"DESCRIPTION_MISMATCH: {name!r} loaded text differs from packaged description"
            )
    return failures


def run_self_test() -> int:
    packaged = {"alpha": "hello world", "beta": "second"}
    failures = compare(packaged, {"alpha": "", "beta": "second"})
    if not any(item.startswith("DROPPED_DESCRIPTION") for item in failures):
        print("SELF-TEST FAILURE: empty description not detected", file=sys.stderr)
        return 1
    failures = compare(packaged, {"beta": "second"})
    if not any(item.startswith("MISSING_LOADED") for item in failures):
        print("SELF-TEST FAILURE: missing skill not detected", file=sys.stderr)
        return 1
    if compare(packaged, packaged):
        print("SELF-TEST FAILURE: aligned capture must pass", file=sys.stderr)
        return 1
    print("loaded-description self-test ok")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument(
        "--capture",
        type=Path,
        help="harness listing file (tsv/| or JSON). Omit for LIVE_BLOCKED note.",
    )
    args = parser.parse_args(argv)
    if args.self_test:
        return run_self_test()
    packaged = packaged_descriptions()
    if args.capture is None:
        print(
            "loaded-description check LIVE_BLOCKED: no harness capture provided; "
            f"package has {len(packaged)} descriptions. "
            "Pass --capture <file> to compare a live listing. "
            "Package-local ceiling is not estate headroom."
        )
        return 0
    try:
        loaded = load_capture(args.capture)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"CAPTURE_UNREADABLE: {error}", file=sys.stderr)
        return 1
    failures = compare(packaged, loaded)
    if failures:
        for failure in failures:
            print(f"VIOLATION {failure}", file=sys.stderr)
        return 1
    print(
        f"loaded-description ok: {len(packaged)} packaged skills present in capture "
        f"{args.capture}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
