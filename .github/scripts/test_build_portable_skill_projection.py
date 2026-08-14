#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("build_portable_skill_projection.py")


def load_builder():
    spec = importlib.util.spec_from_file_location("build_portable_skill_projection", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def skill_text(name: str, marker: str = "") -> str:
    return (
        "---\n"
        f"name: {name}\n"
        f"description: Use when {name} applies.\n"
        "---\n\n"
        f"# {name}\n\n"
        f"PRIVATE_PROCEDURE_{marker or name}\n"
    )


class PortableProjectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.builder = load_builder()
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.package = self.root / "plugins" / "epistemic-skills"
        self.metadata_path = self.root / "packaging" / "portability" / "dependencies.json"
        for name in ("alpha", "beta", "manifest"):
            target = self.package / "skills" / name
            target.mkdir(parents=True)
            (target / "SKILL.md").write_text(skill_text(name), encoding="utf-8")
            (target / "reference.md").write_text(f"reference {name}\n", encoding="utf-8")
        custody = self.package / "contracts" / "mission-custody"
        custody.mkdir(parents=True)
        (custody / "schema.json").write_text('{"type":"object"}\n', encoding="utf-8")
        self.metadata_path.parent.mkdir(parents=True)
        self.write_metadata({
            "schema": "zms-skill-dependencies@1",
            "defaults": {"standalone": {"state": "unverified"}},
            "skills": {
                "manifest": {
                    "dependency_roots": [
                        "plugins/epistemic-skills/contracts/mission-custody"
                    ],
                    "standalone": {
                        "state": "suite_only",
                        "refusal_code": "PACKAGE_BOUND_NO_APPROVED_SKILL_LOCAL_LAUNCHER",
                    },
                }
            },
        })
        self.source = {
            "kind": "working-tree",
            "revision": "working-tree+0123456789abcdef0123456789abcdef01234567",
            "dirty": True,
        }
        self.profile = {
            "product": "zms-local",
            "surface": "non-host-projection",
            "release_or_channel": "working-tree",
            "profile_revision": "phase1-v1",
            "transform": "preserve-canonical-package-layout@1",
        }

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_metadata(self, payload: dict) -> None:
        self.metadata_path.write_text(
            json.dumps(payload, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def derive_ir(self) -> dict:
        return self.builder.derive_ir(self.root, self.source, self.profile)

    def test_ir_is_filesystem_derived_and_procedure_free(self) -> None:
        ir = self.derive_ir()
        by_name = {entry["name"]: entry for entry in ir["skills"]}

        self.assertEqual("zms-skill-ir@1", ir["schema"])
        self.assertEqual(["alpha", "beta", "manifest"], [s["name"] for s in ir["skills"]])
        self.assertEqual("unverified", by_name["alpha"]["standalone"]["state"])
        self.assertEqual("suite_only", by_name["manifest"]["standalone"]["state"])
        self.assertEqual(
            "PACKAGE_BOUND_NO_APPROVED_SKILL_LOCAL_LAUNCHER",
            by_name["manifest"]["standalone"]["refusal_code"],
        )
        encoded = json.dumps(ir, sort_keys=True)
        self.assertNotIn("PRIVATE_PROCEDURE_alpha", encoded)
        self.assertNotIn("PRIVATE_PROCEDURE_manifest", encoded)
        self.assertTrue(ir["structural_only"])
        self.assertTrue(ir["non_release"])

    def test_ir_tracks_skill_addition_without_metadata_inventory_edit(self) -> None:
        before = self.derive_ir()
        gamma = self.package / "skills" / "gamma"
        gamma.mkdir()
        (gamma / "SKILL.md").write_text(skill_text("gamma"), encoding="utf-8")

        after = self.derive_ir()

        self.assertEqual(3, before["skill_count"])
        self.assertEqual(4, after["skill_count"])
        self.assertEqual("gamma", after["skills"][2]["name"])

    def test_metadata_rejects_stale_skill_override(self) -> None:
        payload = json.loads(self.metadata_path.read_text(encoding="utf-8"))
        payload["skills"]["phantom"] = {"standalone": {"state": "unverified"}}
        self.write_metadata(payload)

        with self.assertRaisesRegex(self.builder.ProjectionError, "STALE_SKILL_OVERRIDE"):
            self.derive_ir()

    def test_metadata_rejects_unknown_keys_that_could_duplicate_procedure(self) -> None:
        payload = json.loads(self.metadata_path.read_text(encoding="utf-8"))
        payload["skills"]["manifest"]["procedure"] = "PRIVATE_PROCEDURE_COPY"
        self.write_metadata(payload)

        with self.assertRaisesRegex(self.builder.ProjectionError, "UNKNOWN_METADATA_KEY"):
            self.derive_ir()

    def test_metadata_rejects_invalid_dependency_roots(self) -> None:
        invalid = {
            "absolute": "/tmp/not-portable",
            "escape": "../outside",
            "missing": "plugins/epistemic-skills/contracts/not-there",
        }
        for label, root in invalid.items():
            with self.subTest(label=label):
                payload = json.loads(self.metadata_path.read_text(encoding="utf-8"))
                payload["skills"]["manifest"]["dependency_roots"] = [root]
                self.write_metadata(payload)
                with self.assertRaisesRegex(
                    self.builder.ProjectionError,
                    "INVALID_DEPENDENCY_ROOT|MISSING_DEPENDENCY_ROOT",
                ):
                    self.derive_ir()
                self.setUp_metadata_only()

    def setUp_metadata_only(self) -> None:
        self.write_metadata({
            "schema": "zms-skill-dependencies@1",
            "defaults": {"standalone": {"state": "unverified"}},
            "skills": {
                "manifest": {
                    "dependency_roots": [
                        "plugins/epistemic-skills/contracts/mission-custody"
                    ],
                    "standalone": {
                        "state": "suite_only",
                        "refusal_code": "PACKAGE_BOUND_NO_APPROVED_SKILL_LOCAL_LAUNCHER",
                    },
                }
            },
        })

    def test_metadata_rejects_symlinked_dependency_root(self) -> None:
        link = self.package / "contracts" / "linked-custody"
        try:
            os.symlink(self.package / "contracts" / "mission-custody", link)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks unavailable on this platform")
        payload = json.loads(self.metadata_path.read_text(encoding="utf-8"))
        payload["skills"]["manifest"]["dependency_roots"] = [
            "plugins/epistemic-skills/contracts/linked-custody"
        ]
        self.write_metadata(payload)

        with self.assertRaisesRegex(self.builder.ProjectionError, "SYMLINK_NOT_PORTABLE"):
            self.derive_ir()

    def test_metadata_rejects_wrong_schema(self) -> None:
        payload = json.loads(self.metadata_path.read_text(encoding="utf-8"))
        payload["schema"] = "zms-skill-dependencies@999"
        self.write_metadata(payload)

        with self.assertRaisesRegex(self.builder.ProjectionError, "UNSUPPORTED_METADATA_SCHEMA"):
            self.derive_ir()

    def test_projection_preserves_package_and_binds_structural_digests(self) -> None:
        result = self.builder.build_projection(
            self.root,
            self.root / "out",
            self.source,
            self.profile,
        )

        projected = self.root / "out" / "projection" / "plugins" / "epistemic-skills"
        self.assertEqual(
            (self.package / "skills" / "alpha" / "SKILL.md").read_bytes(),
            (projected / "skills" / "alpha" / "SKILL.md").read_bytes(),
        )
        ir = json.loads(result.ir_path.read_text(encoding="utf-8"))
        evidence = json.loads(result.result_path.read_text(encoding="utf-8"))
        self.assertEqual("zms-projection-result@1", evidence["schema"])
        self.assertTrue(evidence["structural_only"])
        self.assertTrue(evidence["non_release"])
        self.assertNotIn("tier", evidence)
        self.assertNotIn("achieved_tier", evidence)
        self.assertEqual(ir["profile_sha256"], evidence["profile_sha256"])
        self.assertEqual(self.builder.sha256_bytes(result.ir_path.read_bytes()), evidence["ir_sha256"])
        self.assertEqual(
            self.builder.portable_tree_sha256(projected),
            evidence["served_tree_sha256"],
        )

    def test_projection_is_byte_deterministic_for_same_inputs(self) -> None:
        first = self.builder.build_projection(
            self.root,
            self.root / "first",
            self.source,
            self.profile,
        )
        second = self.builder.build_projection(
            self.root,
            self.root / "second",
            self.source,
            self.profile,
        )

        self.assertEqual(first.ir_path.read_bytes(), second.ir_path.read_bytes())
        self.assertEqual(first.result_path.read_bytes(), second.result_path.read_bytes())
        self.assertEqual(
            self.builder.portable_tree_sha256(first.projection_root),
            self.builder.portable_tree_sha256(second.projection_root),
        )

    def test_manifest_standalone_request_refuses_without_output(self) -> None:
        destination = self.root / "standalone"

        with self.assertRaisesRegex(
            self.builder.ProjectionError,
            "PACKAGE_BOUND_NO_APPROVED_SKILL_LOCAL_LAUNCHER",
        ):
            self.builder.build_projection(
                self.root,
                destination,
                self.source,
                self.profile,
                standalone_skill="manifest",
            )

        self.assertFalse(destination.exists())

    def test_unverified_standalone_request_refuses_without_output(self) -> None:
        destination = self.root / "standalone"

        with self.assertRaisesRegex(self.builder.ProjectionError, "STANDALONE_UNVERIFIED"):
            self.builder.build_projection(
                self.root,
                destination,
                self.source,
                self.profile,
                standalone_skill="alpha",
            )

        self.assertFalse(destination.exists())

    def test_foreign_output_directory_is_preserved(self) -> None:
        destination = self.root / "occupied"
        destination.mkdir()
        marker = destination / "foreign.txt"
        marker.write_text("keep me\n", encoding="utf-8")

        with self.assertRaisesRegex(self.builder.ProjectionError, "OUTPUT_ALREADY_EXISTS"):
            self.builder.build_projection(
                self.root,
                destination,
                self.source,
                self.profile,
            )

        self.assertEqual("keep me\n", marker.read_text(encoding="utf-8"))
        self.assertEqual([marker], list(destination.iterdir()))

    def test_output_inside_canonical_package_is_refused(self) -> None:
        destination = self.package / "generated-output"

        with self.assertRaisesRegex(self.builder.ProjectionError, "OUTPUT_INSIDE_SOURCE_PACKAGE"):
            self.builder.build_projection(
                self.root,
                destination,
                self.source,
                self.profile,
            )

        self.assertFalse(destination.exists())

    def initialize_git_fixture(self) -> str:
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        subprocess.run(
            ["git", "config", "user.email", "fixture@example.invalid"],
            cwd=self.root,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Fixture"],
            cwd=self.root,
            check=True,
        )
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "fixture"], cwd=self.root, check=True)
        return subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=self.root,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        ).stdout.strip()

    def test_working_tree_source_is_explicitly_mutable_and_dirty(self) -> None:
        head = self.initialize_git_fixture()
        target = self.package / "skills" / "alpha" / "reference.md"
        target.write_text("dirty working tree\n", encoding="utf-8")

        with self.builder.prepared_source(
            self.root,
            working_tree=True,
            source_revision=None,
        ) as prepared:
            source_root, record = prepared

        self.assertEqual(self.root.resolve(), source_root)
        self.assertEqual("working-tree", record["kind"])
        self.assertEqual(f"working-tree+{head}", record["revision"])
        self.assertTrue(record["dirty"])
        self.assertTrue(record["mutable"])

    def test_committed_source_uses_git_object_bytes_not_dirty_worktree(self) -> None:
        revision = self.initialize_git_fixture()
        committed = self.builder.derive_ir(self.root, {
            "kind": "git-commit",
            "revision": revision,
            "dirty": False,
            "mutable": False,
        }, self.profile)
        target = self.package / "skills" / "alpha" / "SKILL.md"
        target.write_text(skill_text("alpha", marker="DIRTY_ONLY"), encoding="utf-8")

        with self.builder.prepared_source(
            self.root,
            working_tree=False,
            source_revision=revision,
        ) as prepared:
            source_root, record = prepared
            extracted = self.builder.derive_ir(source_root, record, self.profile)
            extracted_text = (
                source_root
                / "plugins"
                / "epistemic-skills"
                / "skills"
                / "alpha"
                / "SKILL.md"
            ).read_text(encoding="utf-8")

        self.assertEqual(committed["canonical_package_tree_sha256"], extracted["canonical_package_tree_sha256"])
        self.assertNotIn("DIRTY_ONLY", extracted_text)
        self.assertEqual("git-commit", record["kind"])
        self.assertEqual(revision, record["revision"])
        self.assertFalse(record["dirty"])
        self.assertFalse(record["mutable"])

    def test_committed_source_rejects_short_revision(self) -> None:
        self.initialize_git_fixture()

        with self.assertRaisesRegex(self.builder.ProjectionError, "FULL_COMMIT_REQUIRED"):
            with self.builder.prepared_source(
                self.root,
                working_tree=False,
                source_revision="HEAD",
            ):
                self.fail("short revision unexpectedly prepared")

    def test_committed_source_ignores_irrelevant_repository_symlink(self) -> None:
        claude = self.root / ".claude"
        claude.mkdir()
        try:
            os.symlink(self.package / "skills", claude / "skills")
        except (OSError, NotImplementedError):
            self.skipTest("symlinks unavailable on this platform")
        revision = self.initialize_git_fixture()

        with self.builder.prepared_source(
            self.root,
            working_tree=False,
            source_revision=revision,
        ) as prepared:
            source_root, _ = prepared
            self.assertTrue(
                (source_root / "plugins" / "epistemic-skills" / "skills" / "alpha" / "SKILL.md").is_file()
            )
            self.assertFalse((source_root / ".claude").exists())

    def test_cli_builds_explicit_working_tree_projection(self) -> None:
        self.initialize_git_fixture()
        destination = self.root / "cli-output"

        status = self.builder.main([
            "--repo-root", str(self.root),
            "--working-tree",
            "--out-dir", str(destination),
        ])

        self.assertEqual(0, status)
        evidence = json.loads(
            (destination / "PROJECTION-RESULT.json").read_text(encoding="utf-8")
        )
        self.assertTrue(evidence["non_release"])
        self.assertTrue(evidence["structural_only"])

    def test_cli_refuses_manifest_standalone_without_output(self) -> None:
        self.initialize_git_fixture()
        destination = self.root / "cli-output"

        with self.assertRaisesRegex(
            self.builder.ProjectionError,
            "PACKAGE_BOUND_NO_APPROVED_SKILL_LOCAL_LAUNCHER",
        ):
            self.builder.main([
                "--repo-root", str(self.root),
                "--working-tree",
                "--out-dir", str(destination),
                "--standalone-skill", "manifest",
            ])

        self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
