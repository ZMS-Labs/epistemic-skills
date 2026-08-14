#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import os
import stat
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("skill_artifact_lib.py")


def load_library():
    spec = importlib.util.spec_from_file_location("skill_artifact_lib", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def skill_text(name: str) -> str:
    return (
        "---\n"
        f"name: {name}\n"
        f"description: Use when {name} applies.\n"
        "---\n\n"
        f"# {name}\n"
    )


class SkillArtifactLibraryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.library = load_library()
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_skill(self, name: str) -> Path:
        target = self.root / "package" / "skills" / name
        target.mkdir(parents=True)
        (target / "SKILL.md").write_text(skill_text(name), encoding="utf-8")
        return target

    def test_discovery_is_sorted_and_filesystem_derived(self) -> None:
        self.write_skill("zeta")
        self.write_skill("alpha")

        records = self.library.discover_skills(self.root / "package")

        self.assertEqual(["alpha", "zeta"], [record.name for record in records])
        self.assertEqual("skills/alpha/SKILL.md", records[0].canonical_path)

    def test_tree_hash_does_not_depend_on_file_creation_order(self) -> None:
        first = self.root / "first"
        second = self.root / "second"
        first.mkdir()
        second.mkdir()
        (first / "b.txt").write_bytes(b"b\n")
        (first / "a.txt").write_bytes(b"a\n")
        (second / "a.txt").write_bytes(b"a\n")
        (second / "b.txt").write_bytes(b"b\n")

        self.assertEqual(
            self.library.tree_sha256(first),
            self.library.tree_sha256(second),
        )

    def test_regular_files_rejects_symlink(self) -> None:
        source = self.root / "source"
        source.mkdir()
        (source / "real.txt").write_text("real\n", encoding="utf-8")
        try:
            os.symlink(source / "real.txt", source / "link.txt")
        except (OSError, NotImplementedError):
            self.skipTest("symlinks unavailable on this platform")

        with self.assertRaisesRegex(self.library.ArtifactError, "SYMLINK_NOT_PORTABLE"):
            self.library.regular_files(source)

    def test_canonical_json_is_compact_sorted_and_newline_terminated(self) -> None:
        encoded = self.library.canonical_json_bytes({"z": 1, "a": [2]})

        self.assertEqual(b'{"a":[2],"z":1}\n', encoded)
        self.assertEqual({"a": [2], "z": 1}, json.loads(encoded))

    def test_copy_regular_tree_preserves_relative_bytes(self) -> None:
        source = self.root / "source"
        destination = self.root / "destination"
        (source / "nested").mkdir(parents=True)
        (source / "nested" / "payload.bin").write_bytes(b"\x00payload\xff")
        (source / "nested" / "payload.bin").chmod(0o755)

        self.library.copy_regular_tree(source, destination)

        self.assertEqual(
            b"\x00payload\xff",
            (destination / "nested" / "payload.bin").read_bytes(),
        )
        self.assertEqual(
            self.library.tree_sha256(source),
            self.library.tree_sha256(destination),
        )
        self.assertEqual(
            0o755,
            stat.S_IMODE((destination / "nested" / "payload.bin").stat().st_mode),
        )

    def test_portable_tree_hash_binds_normalized_file_mode(self) -> None:
        first = self.root / "first"
        second = self.root / "second"
        first.mkdir()
        second.mkdir()
        (first / "tool.py").write_bytes(b"print('same bytes')\n")
        (second / "tool.py").write_bytes(b"print('same bytes')\n")
        (first / "tool.py").chmod(0o644)
        (second / "tool.py").chmod(0o755)

        self.assertNotEqual(
            self.library.portable_tree_sha256(first),
            self.library.portable_tree_sha256(second),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
