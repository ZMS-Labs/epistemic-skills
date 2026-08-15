#!/usr/bin/env python3
"""Shared deterministic primitives for generated skill artifacts.

This module owns filesystem-derived discovery and byte/tree operations only.
It contains no skill inventory, host profile, release policy, installer, or
runtime capability logic.
"""
from __future__ import annotations

import ast
import hashlib
import json
import re
from pathlib import Path
from typing import NamedTuple

FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", re.S)
IGNORED_PARTS = {"__pycache__", ".DS_Store"}


class ArtifactError(ValueError):
    """A named fail-closed portable artifact validation error."""


class DuplicateJsonMember(ArtifactError):
    """Raised when a JSON object contains a repeated member name."""


def _reject_duplicate_json_members(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJsonMember(f"DUPLICATE_JSON_MEMBER: {key}")
        result[key] = value
    return result


def load_json_strict(path: Path) -> object:
    """Load JSON while refusing duplicate members and unreadable input."""
    try:
        return json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_reject_duplicate_json_members,
        )
    except DuplicateJsonMember:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ArtifactError(f"JSON_UNREADABLE: {path}: {error}") from error


class SkillRecord(NamedTuple):
    name: str
    description: str
    canonical_path: str
    skill_md_sha256: str
    tree_sha256: str


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_bytes(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def yaml_scalar(raw: str, path: Path, key: str) -> str:
    value = raw.strip()
    if not value:
        raise ArtifactError(f"EMPTY_FRONTMATTER_VALUE: {path}: {key}")
    if value[0] == "'":
        if len(value) < 2 or value[-1] != "'":
            raise ArtifactError(f"MALFORMED_FRONTMATTER_VALUE: {path}: {key}")
        parsed = value[1:-1].replace("''", "'").strip()
        if not parsed:
            raise ArtifactError(f"MALFORMED_FRONTMATTER_VALUE: {path}: {key}")
        return parsed
    if value[0] == '"':
        try:
            parsed = ast.literal_eval(value)
        except (SyntaxError, ValueError) as error:
            raise ArtifactError(f"MALFORMED_FRONTMATTER_VALUE: {path}: {key}") from error
        if not isinstance(parsed, str) or not parsed.strip():
            raise ArtifactError(f"MALFORMED_FRONTMATTER_VALUE: {path}: {key}")
        return parsed.strip()
    if value in {">", "|", ">-", "|-", ">+", "|+"}:
        raise ArtifactError(f"UNSUPPORTED_MULTILINE_FRONTMATTER: {path}: {key}")
    return value


def parse_skill_frontmatter(path: Path) -> tuple[str, str]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise ArtifactError(f"UNREADABLE_SKILL: {path}: {error}") from error
    match = FRONTMATTER.match(text)
    if not match:
        raise ArtifactError(f"MISSING_FRONTMATTER: {path}")
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, separator, raw = line.partition(":")
        if separator and key.strip() in {"name", "description"}:
            values[key.strip()] = yaml_scalar(raw, path, key.strip())
    missing = {"name", "description"} - values.keys()
    if missing:
        raise ArtifactError(f"MISSING_FRONTMATTER_KEYS: {path}: {sorted(missing)}")
    return values["name"], values["description"]


def regular_files(root: Path) -> list[Path]:
    if not root.is_dir():
        raise ArtifactError(f"MISSING_DIRECTORY: {root}")
    files: list[Path] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root)
        if any(part in IGNORED_PARTS for part in relative.parts) or path.suffix == ".pyc":
            continue
        if path.is_symlink():
            raise ArtifactError(f"SYMLINK_NOT_PORTABLE: {path}")
        if path.is_file():
            files.append(path)
    return files


def tree_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    for path in regular_files(root):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        content = path.read_bytes()
        digest.update(relative)
        digest.update(b"\0")
        digest.update(hashlib.sha256(content).digest())
        digest.update(b"\n")
    return digest.hexdigest()


def normalized_file_mode(path: Path) -> int:
    return 0o755 if path.stat().st_mode & 0o111 else 0o644


def portable_tree_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    digest.update(b"zms-portable-tree-v1\0")
    for path in regular_files(root):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        content_digest = hashlib.sha256(path.read_bytes()).digest()
        mode = f"{normalized_file_mode(path):04o}".encode("ascii")
        digest.update(relative)
        digest.update(b"\0")
        digest.update(mode)
        digest.update(b"\0")
        digest.update(content_digest)
        digest.update(b"\n")
    return digest.hexdigest()


def discover_skills(package_root: Path) -> list[SkillRecord]:
    skills_root = package_root / "skills"
    if not skills_root.is_dir():
        raise ArtifactError(f"MISSING_SKILLS_DIRECTORY: {skills_root}")
    records: list[SkillRecord] = []
    for directory in sorted(skills_root.iterdir(), key=lambda item: item.name):
        skill_md = directory / "SKILL.md"
        if not directory.is_dir() or not skill_md.is_file():
            continue
        name, description = parse_skill_frontmatter(skill_md)
        if name != directory.name:
            raise ArtifactError(
                "FRONTMATTER_NAME_MISMATCH: "
                f"{skill_md} declares {name!r}, directory is {directory.name!r}"
            )
        records.append(SkillRecord(
            name=name,
            description=description,
            canonical_path=(Path("skills") / name / "SKILL.md").as_posix(),
            skill_md_sha256=sha256_bytes(skill_md.read_bytes()),
            tree_sha256=tree_sha256(directory),
        ))
    if not records:
        raise ArtifactError(f"EMPTY_SKILL_GLOB: {skills_root}")
    names = [record.name for record in records]
    if len(names) != len(set(names)):
        raise ArtifactError(f"DUPLICATE_SKILL_NAME: {names}")
    return records


def copy_regular_tree(source: Path, destination: Path) -> None:
    if destination.exists() and destination.is_symlink():
        raise ArtifactError(f"SYMLINK_NOT_PORTABLE: {destination}")
    for source_file in regular_files(source):
        relative = source_file.relative_to(source)
        destination_file = destination / relative
        if destination_file.exists() and destination_file.is_symlink():
            raise ArtifactError(f"SYMLINK_NOT_PORTABLE: {destination_file}")
        destination_file.parent.mkdir(parents=True, exist_ok=True)
        destination_file.write_bytes(source_file.read_bytes())
        destination_file.chmod(normalized_file_mode(source_file))
