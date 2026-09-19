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

``--require-capture`` is release-gate mode (v5 design AMENDMENT 2026-08-07, D8
Path 1: "show estate headroom via a capture receipt"): there, a missing capture
is a hard FAILURE, not a note — the mode a release pipeline must use if the
operator elects Path 1 rather than publishing the Path-2 owner amendment. CI's
default informational tier is unchanged without the flag.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SKILLS = REPO / "plugins" / "epistemic-skills" / "skills"
FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---", re.S)
DESCRIPTION = re.compile(
    r"^description:\s*(.*?)(?=^[A-Za-z_][A-Za-z0-9_-]*:|\Z)", re.S | re.M
)


def normalize_description(value: str) -> str:
    """Ignore ASCII layout whitespace only; preserve words and punctuation."""
    return re.sub(r"[ \t\r\n]+", " ", value).strip(" ")


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
        quote = value[0]
        body = value[1:-1]
        if quote == "'":
            return body.replace("''", "'")
        # JSON-compatible YAML double quotes preserve literal Unicode. Unsupported
        # escapes fail explicitly instead of corrupting the captured instruction.
        return json.loads(re.sub(r"\r?\n[ \t]*", " ", value))
    return normalize_description(value)


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


def add_capture_entry(loaded: dict[str, str], name: object, description: object) -> None:
    if not isinstance(name, str) or not name.strip():
        raise ValueError("capture entry requires a nonempty string name")
    name = name.strip()
    if description is None:
        description = ""
    if not isinstance(description, str):
        raise ValueError(f"capture description for {name!r} must be a string or null")
    if name in loaded and normalize_description(loaded[name]) != normalize_description(description):
        raise ValueError(f"conflicting duplicate capture identity: {name!r}")
    loaded[name] = description


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
            if not isinstance(row, dict):
                raise ValueError("each JSON capture entry must be an object")
            add_capture_entry(loaded, row.get("name"), row.get("description"))
        return loaded
    loaded = {}
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if "\t" in line:
            name, desc = line.split("\t", 1)
        elif "|" in line:
            name, desc = line.split("|", 1)
        else:
            raise ValueError(f"unrecognized capture line: {line!r}")
        add_capture_entry(loaded, name, desc)
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
        elif normalize_description(got) != normalize_description(desc):
            failures.append(
                f"DESCRIPTION_MISMATCH: {name!r} loaded text differs from packaged description"
            )
    return failures


def regression_checks() -> list[str]:
    errors: list[str] = []
    description = "Use when investigating a reproducible failure. Do not run for a lookup."
    expected = {"sample": description}
    cases = [
        ("prefix truncation", "Use", True),
        ("interior fragment", "reproducible failure", True),
        ("missing exclusion", description.split(" Do not")[0], True),
        ("changed condition", description.replace("failure", "success"), True),
        ("intact description", description, False),
        ("line wrapping", description.replace("reproducible ", "reproducible\n  "), False),
    ]
    for label, captured, reject in cases:
        failed = bool(compare(expected, {"sample": captured}))
        if failed != reject:
            errors.append(f"{label}: expected {'rejection' if reject else 'acceptance'}")
    unicode_text = "Use when checking caf\u00e9 output \u2014 preserve Unicode."
    if unquote(json.dumps(unicode_text, ensure_ascii=False)) != unicode_text:
        errors.append("quoted Unicode description was corrupted")
    with tempfile.TemporaryDirectory() as directory:
        capture = Path(directory) / "capture.json"
        cases = [
            ("conflicting duplicate", [{"name": "sample", "description": "Use"},
                                       {"name": "sample", "description": description}], True),
            ("identical duplicate", [{"name": "sample", "description": description},
                                     {"name": "sample", "description": description}], False),
            ("non-object row", ["sample"], True),
            ("missing name", [{"description": description}], True),
            ("non-string description", [{"name": "sample", "description": [description]}], True),
        ]
        for label, rows, reject in cases:
            capture.write_text(json.dumps(rows), encoding="utf-8")
            try:
                load_capture(capture)
                failed = False
            except ValueError:
                failed = True
            except (KeyError, TypeError, AttributeError) as error:
                errors.append(f"{label}: malformed capture escaped as {type(error).__name__}")
                continue
            if failed != reject:
                errors.append(f"{label}: expected {'rejection' if reject else 'acceptance'}")
        capture = Path(directory) / "capture.tsv"
        capture.write_text("sample\tUse\nsample\t" + description + "\n", encoding="utf-8")
        try:
            load_capture(capture)
            errors.append("conflicting text duplicate was silently overwritten")
        except ValueError:
            pass
    return errors


def run_self_test() -> int:
    regressions = regression_checks()
    if regressions:
        for failure in regressions:
            print(f"SELF-TEST FAILURE: {failure}", file=sys.stderr)
        return 1
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
    # Release-gate mode: a missing capture must fail closed, and the default
    # informational tier must keep exiting 0 (LIVE_BLOCKED note).
    if main(["--require-capture"]) != 1:
        print(
            "SELF-TEST FAILURE: --require-capture without a capture must fail",
            file=sys.stderr,
        )
        return 1
    if main([]) != 0:
        print(
            "SELF-TEST FAILURE: default tier without a capture must stay exit 0",
            file=sys.stderr,
        )
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
    parser.add_argument(
        "--require-capture",
        action="store_true",
        help="release-gate mode (v5 D8 Path 1): a missing capture is a hard "
        "failure instead of a LIVE_BLOCKED note.",
    )
    args = parser.parse_args(argv)
    if args.self_test:
        return run_self_test()
    packaged = packaged_descriptions()
    if args.capture is None:
        if args.require_capture:
            print(
                "CAPTURE_REQUIRED: release-gate mode (v5 design AMENDMENT "
                "2026-08-07, D8 Path 1) demands a live harness capture receipt "
                "and none was provided. Estate headroom cannot be claimed "
                "without one; the alternative is the Path-2 owner amendment.",
                file=sys.stderr,
            )
            return 1
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
