#!/usr/bin/env python3
"""Build a local, non-release portable skill IR and suite projection.

Phase 1 is structural only. It does not publish, install, execute skill code,
contact a network, or emit a host/runtime capability tier.
"""
from __future__ import annotations

import argparse
import io
import json
import re
import shutil
import subprocess
import tarfile
import tempfile
from contextlib import contextmanager
from pathlib import Path, PurePosixPath
from typing import Iterator, NamedTuple

from skill_artifact_lib import (
    ArtifactError,
    canonical_json_bytes,
    copy_regular_tree,
    discover_skills,
    normalized_file_mode,
    portable_tree_sha256,
    regular_files,
    sha256_bytes,
)

CANONICAL_PACKAGE = Path("plugins/epistemic-skills")
DEPENDENCY_CONTRACT = Path("packaging/portability/dependencies.json")
METADATA_SCHEMA = "zms-skill-dependencies@1"
IR_SCHEMA = "zms-skill-ir@1"
GENERATOR_REVISION = "phase1-v1"
TOP_LEVEL_KEYS = {"schema", "defaults", "skills"}
DEFAULT_KEYS = {"standalone"}
SKILL_KEYS = {"dependency_roots", "standalone"}
STANDALONE_KEYS = {"state", "refusal_code"}
STANDALONE_STATES = {"unverified", "suite_only"}
FULL_COMMIT = re.compile(r"\A[0-9a-f]{40}\Z")
LOCAL_PHASE1_PROFILE = {
    "product": "zms-local",
    "surface": "non-host-projection",
    "release_or_channel": "working-tree",
    "profile_revision": "phase1-v1",
    "transform": "preserve-canonical-package-layout@1",
}


class ProjectionError(ArtifactError):
    """A named fail-closed Phase-1 projection error."""


class BuildResult(NamedTuple):
    ir_path: Path
    result_path: Path
    projection_root: Path
    skill_count: int


def _git(repo_root: Path, *args: str) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(
            ["git", *args],
            cwd=repo_root,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        detail = getattr(error, "stderr", b"")
        if isinstance(detail, bytes):
            detail = detail.decode("utf-8", errors="replace").strip()
        raise ProjectionError(f"LOCAL_GIT_FAILURE: git {' '.join(args)}: {detail}") from error


def _extract_git_archive(archive_bytes: bytes, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:") as archive:
        for member in archive.getmembers():
            pure = PurePosixPath(member.name)
            if pure.is_absolute() or ".." in pure.parts or "\\" in member.name:
                raise ProjectionError(f"GIT_ARCHIVE_PATH_ESCAPE: {member.name}")
            target = destination / Path(*pure.parts)
            if member.isdir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            if not member.isfile():
                raise ProjectionError(f"GIT_ARCHIVE_NON_REGULAR: {member.name}")
            extracted = archive.extractfile(member)
            if extracted is None:
                raise ProjectionError(f"GIT_ARCHIVE_UNREADABLE: {member.name}")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(extracted.read())


@contextmanager
def prepared_source(
    repo_root: Path,
    *,
    working_tree: bool,
    source_revision: str | None,
) -> Iterator[tuple[Path, dict]]:
    repo_root = repo_root.resolve()
    head = _git(repo_root, "rev-parse", "HEAD").stdout.decode("ascii").strip()
    if not FULL_COMMIT.fullmatch(head):
        raise ProjectionError(f"INVALID_HEAD_REVISION: {head!r}")
    if working_tree:
        if source_revision is not None:
            raise ProjectionError("SOURCE_MODE_CONFLICT: working tree and source revision")
        dirty = bool(_git(repo_root, "status", "--porcelain", "--untracked-files=normal").stdout)
        yield repo_root, {
            "kind": "working-tree",
            "revision": f"working-tree+{head}",
            "dirty": dirty,
            "mutable": True,
        }
        return
    if source_revision is None or not FULL_COMMIT.fullmatch(source_revision):
        raise ProjectionError("FULL_COMMIT_REQUIRED: provide a full 40-hex --source-revision")
    _git(repo_root, "cat-file", "-e", f"{source_revision}^{{commit}}")
    archive = _git(
        repo_root,
        "archive",
        "--format=tar",
        source_revision,
        "--",
        CANONICAL_PACKAGE.as_posix(),
        DEPENDENCY_CONTRACT.as_posix(),
    ).stdout
    with tempfile.TemporaryDirectory(prefix="zms-portable-source-") as temporary:
        extracted_root = Path(temporary)
        _extract_git_archive(archive, extracted_root)
        yield extracted_root, {
            "kind": "git-commit",
            "revision": source_revision,
            "dirty": False,
            "mutable": False,
        }


def _load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ProjectionError(f"MISSING_DEPENDENCY_CONTRACT: {path}") from error
    except (OSError, json.JSONDecodeError) as error:
        raise ProjectionError(f"MALFORMED_DEPENDENCY_CONTRACT: {path}: {error}") from error


def _require_object(value: object, label: str) -> dict:
    if not isinstance(value, dict):
        raise ProjectionError(f"MALFORMED_METADATA: {label} must be an object")
    return value


def _reject_unknown_keys(value: dict, allowed: set[str], label: str) -> None:
    unknown = sorted(set(value) - allowed)
    if unknown:
        raise ProjectionError(f"UNKNOWN_METADATA_KEY: {label}: {unknown}")


def _validate_standalone(value: object, label: str) -> dict[str, str]:
    standalone = _require_object(value, label)
    _reject_unknown_keys(standalone, STANDALONE_KEYS, label)
    state = standalone.get("state")
    if state not in STANDALONE_STATES:
        raise ProjectionError(f"INVALID_STANDALONE_STATE: {label}: {state!r}")
    refusal = standalone.get("refusal_code")
    if refusal is not None and (not isinstance(refusal, str) or not refusal.strip()):
        raise ProjectionError(f"INVALID_REFUSAL_CODE: {label}")
    if state == "suite_only" and refusal is None:
        raise ProjectionError(f"MISSING_REFUSAL_CODE: {label}")
    if state != "suite_only" and refusal is not None:
        raise ProjectionError(f"UNEXPECTED_REFUSAL_CODE: {label}")
    result = {"state": state}
    if isinstance(refusal, str):
        result["refusal_code"] = refusal
    return result


def load_dependency_contract(repo_root: Path, discovered_names: set[str] | None = None) -> dict:
    contract = _require_object(_load_json(repo_root / DEPENDENCY_CONTRACT), "contract")
    _reject_unknown_keys(contract, TOP_LEVEL_KEYS, "contract")
    if contract.get("schema") != METADATA_SCHEMA:
        raise ProjectionError(
            f"UNSUPPORTED_METADATA_SCHEMA: expected {METADATA_SCHEMA!r}, "
            f"got {contract.get('schema')!r}"
        )
    defaults = _require_object(contract.get("defaults"), "defaults")
    _reject_unknown_keys(defaults, DEFAULT_KEYS, "defaults")
    default_standalone = _validate_standalone(defaults.get("standalone"), "defaults.standalone")
    skills = _require_object(contract.get("skills"), "skills")
    if discovered_names is not None:
        stale = sorted(set(skills) - discovered_names)
        if stale:
            raise ProjectionError(f"STALE_SKILL_OVERRIDE: {stale}")
    normalized_skills: dict[str, dict] = {}
    for name, raw_override in sorted(skills.items()):
        if not isinstance(name, str) or not name:
            raise ProjectionError("MALFORMED_METADATA: skill override name must be non-empty")
        override = _require_object(raw_override, f"skills.{name}")
        _reject_unknown_keys(override, SKILL_KEYS, f"skills.{name}")
        roots = override.get("dependency_roots", [])
        if not isinstance(roots, list) or not all(isinstance(root, str) for root in roots):
            raise ProjectionError(f"MALFORMED_METADATA: skills.{name}.dependency_roots")
        if len(roots) != len(set(roots)):
            raise ProjectionError(f"DUPLICATE_DEPENDENCY_ROOT: skills.{name}")
        normalized_skills[name] = {
            "dependency_roots": roots,
            "standalone": _validate_standalone(
                override.get("standalone", default_standalone),
                f"skills.{name}.standalone",
            ),
        }
    return {
        "schema": METADATA_SCHEMA,
        "defaults": {"standalone": default_standalone},
        "skills": normalized_skills,
    }


def _validated_dependency(repo_root: Path, raw: str) -> dict[str, str]:
    pure = PurePosixPath(raw)
    if (
        not raw
        or pure.is_absolute()
        or ".." in pure.parts
        or "." in pure.parts
        or "\\" in raw
        or any(marker in raw for marker in ("*", "?", "[", "]"))
    ):
        raise ProjectionError(f"INVALID_DEPENDENCY_ROOT: {raw!r}")
    normalized = pure.as_posix()
    target = repo_root / Path(*pure.parts)
    if target.is_symlink():
        raise ProjectionError(f"SYMLINK_NOT_PORTABLE: {target}")
    if not target.exists():
        raise ProjectionError(f"MISSING_DEPENDENCY_ROOT: {normalized}")
    if target.is_file():
        digest = sha256_bytes(target.read_bytes())
        kind = "file"
    elif target.is_dir():
        digest = portable_tree_sha256(target)
        kind = "directory"
    else:
        raise ProjectionError(f"INVALID_DEPENDENCY_ROOT: {normalized}")
    return {"path": normalized, "kind": kind, "sha256": digest}


def _skill_members(repo_root: Path, skill_root: Path) -> list[dict[str, str]]:
    return [
        {
            "path": path.relative_to(repo_root).as_posix(),
            "mode": f"{normalized_file_mode(path):04o}",
            "sha256": sha256_bytes(path.read_bytes()),
        }
        for path in regular_files(skill_root)
    ]


def derive_ir(repo_root: Path, source_record: dict, profile: dict) -> dict:
    repo_root = repo_root.resolve()
    package_root = repo_root / CANONICAL_PACKAGE
    records = discover_skills(package_root)
    names = {record.name for record in records}
    contract = load_dependency_contract(repo_root, names)
    skills: list[dict] = []
    for record in records:
        skill_root = package_root / "skills" / record.name
        override = contract["skills"].get(record.name, {})
        roots = override.get("dependency_roots", [])
        standalone = override.get("standalone", contract["defaults"]["standalone"])
        skills.append({
            "name": record.name,
            "canonical_path": record.canonical_path,
            "description_sha256": sha256_bytes(record.description.encode("utf-8")),
            "skill_md_sha256": record.skill_md_sha256,
            "source_tree_sha256": portable_tree_sha256(skill_root),
            "members": _skill_members(repo_root, skill_root),
            "dependencies": [_validated_dependency(repo_root, root) for root in roots],
            "standalone": dict(standalone),
        })
    return {
        "schema": IR_SCHEMA,
        "generator_revision": GENERATOR_REVISION,
        "source": dict(source_record),
        "canonical_package": CANONICAL_PACKAGE.as_posix(),
        "canonical_package_tree_sha256": portable_tree_sha256(package_root),
        "inventory_rule": "direct skills/<name>/SKILL.md children",
        "profile": dict(profile),
        "profile_sha256": sha256_bytes(canonical_json_bytes(profile)),
        "skill_count": len(skills),
        "skills": skills,
        "structural_only": True,
        "non_release": True,
        "never_attests": [
            "host-discovery",
            "skill-callability",
            "custody-capability",
            "guard-enforcement",
        ],
    }


def _refuse_standalone(ir: dict, skill_name: str) -> None:
    matches = [entry for entry in ir["skills"] if entry["name"] == skill_name]
    if not matches:
        raise ProjectionError(f"UNKNOWN_SKILL: {skill_name}")
    standalone = matches[0]["standalone"]
    if standalone["state"] == "suite_only":
        raise ProjectionError(standalone["refusal_code"])
    raise ProjectionError(f"STANDALONE_UNVERIFIED: {skill_name}")


def build_projection(
    repo_root: Path,
    out_dir: Path,
    source_record: dict,
    profile: dict,
    *,
    standalone_skill: str | None = None,
) -> BuildResult:
    repo_root = repo_root.resolve()
    package_root = (repo_root / CANONICAL_PACKAGE).resolve()
    out_dir = out_dir.resolve()
    if out_dir == package_root or package_root in out_dir.parents:
        raise ProjectionError(f"OUTPUT_INSIDE_SOURCE_PACKAGE: {out_dir}")
    if out_dir.exists():
        raise ProjectionError(f"OUTPUT_ALREADY_EXISTS: {out_dir}")

    ir = derive_ir(repo_root, source_record, profile)
    if standalone_skill is not None:
        _refuse_standalone(ir, standalone_skill)

    out_dir.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".zms-portable-stage-", dir=out_dir.parent))
    try:
        projected_package = stage / "projection" / CANONICAL_PACKAGE
        copy_regular_tree(package_root, projected_package)
        ir_path = stage / "PORTABILITY-IR.json"
        ir_bytes = canonical_json_bytes(ir)
        ir_path.write_bytes(ir_bytes)
        result = {
            "schema": "zms-projection-result@1",
            "source_sha256": sha256_bytes(canonical_json_bytes(source_record)),
            "profile_sha256": ir["profile_sha256"],
            "ir_sha256": sha256_bytes(ir_bytes),
            "served_tree_sha256": portable_tree_sha256(projected_package),
            "structural_only": True,
            "non_release": True,
            "never_attests": list(ir["never_attests"]),
        }
        result_path = stage / "PROJECTION-RESULT.json"
        result_path.write_bytes(canonical_json_bytes(result))
        stage.replace(out_dir)
    except BaseException:
        if stage.exists():
            shutil.rmtree(stage)
        raise
    return BuildResult(
        ir_path=out_dir / "PORTABILITY-IR.json",
        result_path=out_dir / "PROJECTION-RESULT.json",
        projection_root=out_dir / "projection" / CANONICAL_PACKAGE,
        skill_count=ir["skill_count"],
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--out-dir", type=Path, required=True)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--working-tree", action="store_true")
    source.add_argument("--source-revision")
    parser.add_argument("--standalone-skill")
    args = parser.parse_args(argv)
    with prepared_source(
        args.repo_root,
        working_tree=args.working_tree,
        source_revision=args.source_revision,
    ) as (source_root, source_record):
        result = build_projection(
            source_root,
            args.out_dir,
            source_record,
            LOCAL_PHASE1_PROFILE,
            standalone_skill=args.standalone_skill,
        )
    print(
        f"portable Phase-1 projection: {result.skill_count} skills; "
        f"structural-only, non-release; output={args.out_dir.resolve()}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ProjectionError as error:
        print(f"REFUSED {error}")
        raise SystemExit(2) from error
