#!/usr/bin/env python3
"""Build deterministic OpenAI/ChatGPT bundles from the canonical skill package.

No skill inventory is stored in this script. Every build discovers direct
``skills/<name>/SKILL.md`` children from ``plugins/epistemic-skills`` and fails
closed when their frontmatter disagrees with the filesystem. The same source
therefore feeds both the marketplace/plugin bundle and the single-skill
ChatGPT upload bridge.
"""
from __future__ import annotations

import argparse
import json
import os
import tempfile
import zipfile
from pathlib import Path
from typing import Iterable, NamedTuple

from skill_artifact_lib import (
    ArtifactError,
    SkillRecord,
    discover_skills,
    parse_skill_frontmatter,
    regular_files,
    sha256_bytes,
)

CANONICAL_PACKAGE = Path("plugins/epistemic-skills")
MARKETPLACE_PATH = Path(".agents/plugins/marketplace.json")
CHATGPT_TEMPLATE = Path("packaging/openai/chatgpt-skill/SKILL.md")
PLUGIN_ARCHIVE_ROOT = Path("epistemic-skills-openai")
CHATGPT_ARCHIVE_ROOT = Path("epistemic-skills")
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)
BundleError = ArtifactError


class BuildResult(NamedTuple):
    chatgpt_skill: Path
    openai_plugin: Path
    checksums: Path
    skill_count: int


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise BundleError(f"MISSING_REQUIRED_FILE: {path}") from error
    except (OSError, json.JSONDecodeError) as error:
        raise BundleError(f"MALFORMED_JSON: {path}: {error}") from error


def validate_marketplace(repo_root: Path) -> None:
    marketplace = load_json(repo_root / MARKETPLACE_PATH)
    if not isinstance(marketplace, dict) or not isinstance(marketplace.get("plugins"), list):
        raise BundleError(f"MALFORMED_MARKETPLACE: {repo_root / MARKETPLACE_PATH}")
    matches = [
        entry for entry in marketplace["plugins"]
        if isinstance(entry, dict) and entry.get("name") == "epistemic-skills"
    ]
    if len(matches) != 1:
        raise BundleError("MARKETPLACE_PLUGIN_COUNT: expected exactly one epistemic-skills entry")
    source = matches[0].get("source")
    expected_source = {"source": "local", "path": "./plugins/epistemic-skills"}
    if source != expected_source:
        raise BundleError(
            f"MARKETPLACE_SOURCE_DRIFT: expected {expected_source!r}, got {source!r}"
        )

    manifest_path = repo_root / CANONICAL_PACKAGE / ".codex-plugin" / "plugin.json"
    manifest = load_json(manifest_path)
    if not isinstance(manifest, dict):
        raise BundleError(f"MALFORMED_PLUGIN_MANIFEST: {manifest_path}")
    if manifest.get("name") != "epistemic-skills":
        raise BundleError(
            f"PLUGIN_NAME_DRIFT: {manifest_path} has {manifest.get('name')!r}"
        )
    if manifest.get("skills") != "./skills/":
        raise BundleError(
            "PLUGIN_SKILLS_SOURCE_DRIFT: expected './skills/' so the canonical glob "
            f"remains authoritative, got {manifest.get('skills')!r}"
        )

    template = repo_root / CHATGPT_TEMPLATE
    template_name, _ = parse_skill_frontmatter(template)
    if template_name != "epistemic-skills":
        raise BundleError(
            f"CHATGPT_TEMPLATE_NAME_DRIFT: {template} declares {template_name!r}"
        )


def render_index(records: list[SkillRecord], source_revision: str) -> bytes:
    payload = {
        "schema": "openai-epistemic-bundle-index@1",
        "source": {
            "repository": "https://github.com/ZMS-Labs/epistemic-skills",
            "revision": source_revision,
            "canonical_package": CANONICAL_PACKAGE.as_posix(),
            "inventory_rule": "direct skills/<name>/SKILL.md children",
        },
        "skill_count": len(records),
        "skills": [record._asdict() for record in records],
    }
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")


def zip_entries(path: Path, archive_prefix: Path) -> Iterable[tuple[str, bytes]]:
    for file_path in regular_files(path):
        relative = file_path.relative_to(path)
        yield (archive_prefix / relative).as_posix(), file_path.read_bytes()


def write_deterministic_zip(destination: Path, entries: Iterable[tuple[str, bytes]]) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    ordered = sorted(entries, key=lambda item: item[0])
    names = [name for name, _ in ordered]
    if len(names) != len(set(names)):
        raise BundleError("DUPLICATE_ARCHIVE_PATH: bundle construction produced duplicate members")
    with zipfile.ZipFile(destination, "w") as archive:
        for name, content in ordered:
            info = zipfile.ZipInfo(name, FIXED_ZIP_TIME)
            info.create_system = 3
            info.external_attr = (0o100644 & 0xFFFF) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, content, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def build_bundles(repo_root: Path, out_dir: Path, source_revision: str) -> BuildResult:
    repo_root = repo_root.resolve()
    out_dir = out_dir.resolve()
    if not source_revision.strip():
        raise BundleError("EMPTY_SOURCE_REVISION")
    validate_marketplace(repo_root)
    package_root = repo_root / CANONICAL_PACKAGE
    records = discover_skills(package_root)
    index = render_index(records, source_revision.strip())

    chatgpt_skill = out_dir / "epistemic-skills-chatgpt-skill.zip"
    chatgpt_entries: list[tuple[str, bytes]] = [
        ((CHATGPT_ARCHIVE_ROOT / "SKILL.md").as_posix(),
         (repo_root / CHATGPT_TEMPLATE).read_bytes()),
        ((CHATGPT_ARCHIVE_ROOT / "skill-index.json").as_posix(), index),
    ]
    chatgpt_entries.extend(zip_entries(package_root, CHATGPT_ARCHIVE_ROOT / "package"))
    if (repo_root / "LICENSE").is_file():
        chatgpt_entries.append(
            ((CHATGPT_ARCHIVE_ROOT / "LICENSE").as_posix(), (repo_root / "LICENSE").read_bytes())
        )
    write_deterministic_zip(chatgpt_skill, chatgpt_entries)

    openai_plugin = out_dir / "epistemic-skills-openai-plugin.zip"
    plugin_entries: list[tuple[str, bytes]] = [
        ((PLUGIN_ARCHIVE_ROOT / MARKETPLACE_PATH).as_posix(),
         (repo_root / MARKETPLACE_PATH).read_bytes()),
        ((PLUGIN_ARCHIVE_ROOT / "BUNDLE-INDEX.json").as_posix(), index),
    ]
    plugin_entries.extend(
        zip_entries(package_root, PLUGIN_ARCHIVE_ROOT / CANONICAL_PACKAGE)
    )
    if (repo_root / "LICENSE").is_file():
        plugin_entries.append(
            ((PLUGIN_ARCHIVE_ROOT / "LICENSE").as_posix(), (repo_root / "LICENSE").read_bytes())
        )
    write_deterministic_zip(openai_plugin, plugin_entries)

    checksums = out_dir / "SHA256SUMS"
    checksum_lines = [
        f"{sha256_bytes(chatgpt_skill.read_bytes())}  {chatgpt_skill.name}",
        f"{sha256_bytes(openai_plugin.read_bytes())}  {openai_plugin.name}",
    ]
    checksums.write_text("\n".join(checksum_lines) + "\n", encoding="utf-8", newline="\n")
    return BuildResult(chatgpt_skill, openai_plugin, checksums, len(records))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("dist/openai"),
        help="output directory (default: dist/openai)",
    )
    parser.add_argument(
        "--source-revision",
        default=os.environ.get("GITHUB_SHA", "working-tree"),
        help="revision recorded in the generated index",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate and build in a temporary directory without retaining artifacts",
    )
    arguments = parser.parse_args(argv)
    repo_root = Path(__file__).resolve().parents[2]
    if arguments.check:
        with tempfile.TemporaryDirectory() as temporary:
            result = build_bundles(repo_root, Path(temporary), arguments.source_revision)
            print(
                f"OpenAI bundle check ok: {result.skill_count} dynamically discovered skills; "
                "both deterministic archives built"
            )
        return 0
    result = build_bundles(repo_root, arguments.out_dir, arguments.source_revision)
    print(f"built: {result.chatgpt_skill}")
    print(f"built: {result.openai_plugin}")
    print(f"wrote: {result.checksums}")
    print(f"inventory: {result.skill_count} dynamically discovered skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
