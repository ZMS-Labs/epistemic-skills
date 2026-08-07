#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

SCRIPT = Path(__file__).with_name("build_openai_bundles.py")


def load_builder():
    spec = importlib.util.spec_from_file_location("build_openai_bundles", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def skill_text(name: str, description: str = "Use when this fixture applies.") -> str:
    return f"---\nname: {name}\ndescription: {description}\n---\n\n# {name}\n"


def write_fixture(root: Path) -> None:
    package = root / "plugins" / "epistemic-skills"
    (root / ".agents" / "plugins").mkdir(parents=True)
    (package / ".codex-plugin").mkdir(parents=True)
    (root / "packaging" / "openai" / "chatgpt-skill").mkdir(parents=True)
    (package / "contracts").mkdir(parents=True)
    for name in ("alpha", "beta"):
        target = package / "skills" / name
        target.mkdir(parents=True)
        (target / "SKILL.md").write_text(skill_text(name), encoding="utf-8")
        (target / "reference.md").write_text(f"reference for {name}\n", encoding="utf-8")
    (package / "contracts" / "schema.json").write_text('{"type":"object"}\n', encoding="utf-8")
    (package / ".codex-plugin" / "plugin.json").write_text(
        json.dumps({"name": "epistemic-skills", "version": "0.0.0", "skills": "./skills/"}) + "\n",
        encoding="utf-8",
    )
    (root / ".agents" / "plugins" / "marketplace.json").write_text(
        json.dumps({
            "name": "epistemic-skills",
            "plugins": [{
                "name": "epistemic-skills",
                "source": {"source": "local", "path": "./plugins/epistemic-skills"},
            }],
        }) + "\n",
        encoding="utf-8",
    )
    (root / "packaging" / "openai" / "chatgpt-skill" / "SKILL.md").write_text(
        "---\nname: epistemic-skills\ndescription: Dynamic fixture bridge.\n---\n\n# Bridge\n",
        encoding="utf-8",
    )
    (root / "LICENSE").write_text("fixture license\n", encoding="utf-8")


class OpenAIBundleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        write_fixture(self.root)
        self.builder = load_builder()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def build(self, destination: str = "dist"):
        return self.builder.build_bundles(
            repo_root=self.root,
            out_dir=self.root / destination,
            source_revision="fixture-sha",
        )

    def read_json_from_zip(self, archive: Path, member: str) -> dict:
        with zipfile.ZipFile(archive) as bundle:
            return json.loads(bundle.read(member).decode("utf-8"))

    def test_discovers_added_skill_without_inventory_edit(self) -> None:
        first = self.build("first")
        first_index = self.read_json_from_zip(
            first.chatgpt_skill,
            "epistemic-skills/skill-index.json",
        )
        self.assertEqual(["alpha", "beta"], [item["name"] for item in first_index["skills"]])

        gamma = self.root / "plugins" / "epistemic-skills" / "skills" / "gamma"
        gamma.mkdir()
        (gamma / "SKILL.md").write_text(skill_text("gamma"), encoding="utf-8")

        second = self.build("second")
        second_index = self.read_json_from_zip(
            second.chatgpt_skill,
            "epistemic-skills/skill-index.json",
        )
        self.assertEqual(
            ["alpha", "beta", "gamma"],
            [item["name"] for item in second_index["skills"]],
        )
        self.assertEqual(3, second_index["skill_count"])

    def test_build_is_byte_deterministic_for_same_inputs(self) -> None:
        first = self.build("first")
        second = self.build("second")
        self.assertEqual(first.chatgpt_skill.read_bytes(), second.chatgpt_skill.read_bytes())
        self.assertEqual(first.openai_plugin.read_bytes(), second.openai_plugin.read_bytes())
        self.assertEqual(first.checksums.read_text(), second.checksums.read_text())

    def test_chatgpt_skill_wraps_the_complete_canonical_package(self) -> None:
        result = self.build()
        with zipfile.ZipFile(result.chatgpt_skill) as bundle:
            names = set(bundle.namelist())
        self.assertIn("epistemic-skills/SKILL.md", names)
        self.assertIn("epistemic-skills/skill-index.json", names)
        self.assertIn("epistemic-skills/package/skills/alpha/SKILL.md", names)
        self.assertIn("epistemic-skills/package/skills/beta/reference.md", names)
        self.assertIn("epistemic-skills/package/contracts/schema.json", names)

    def test_plugin_bundle_preserves_marketplace_and_package_layout(self) -> None:
        result = self.build()
        with zipfile.ZipFile(result.openai_plugin) as bundle:
            names = set(bundle.namelist())
        self.assertIn("epistemic-skills-openai/.agents/plugins/marketplace.json", names)
        self.assertIn(
            "epistemic-skills-openai/plugins/epistemic-skills/.codex-plugin/plugin.json",
            names,
        )
        self.assertIn(
            "epistemic-skills-openai/plugins/epistemic-skills/skills/alpha/SKILL.md",
            names,
        )
        self.assertIn("epistemic-skills-openai/BUNDLE-INDEX.json", names)

    def test_preserves_yaml_single_quoted_apostrophe_in_description(self) -> None:
        target = self.root / "plugins" / "epistemic-skills" / "skills" / "alpha" / "SKILL.md"
        target.write_text(
            "---\nname: alpha\ndescription: 'Gauntlet''s ledger.'\n---\n\n# alpha\n",
            encoding="utf-8",
        )
        result = self.build()
        index = self.read_json_from_zip(result.chatgpt_skill, "epistemic-skills/skill-index.json")
        self.assertEqual("Gauntlet's ledger.", index["skills"][0]["description"])

    def test_rejects_skill_name_that_disagrees_with_directory(self) -> None:
        target = self.root / "plugins" / "epistemic-skills" / "skills" / "alpha" / "SKILL.md"
        target.write_text(skill_text("not-alpha"), encoding="utf-8")
        with self.assertRaisesRegex(self.builder.BundleError, "FRONTMATTER_NAME_MISMATCH"):
            self.build()

    def test_rejects_marketplace_source_that_bypasses_canonical_package(self) -> None:
        marketplace = self.root / ".agents" / "plugins" / "marketplace.json"
        payload = json.loads(marketplace.read_text(encoding="utf-8"))
        payload["plugins"][0]["source"]["path"] = "./copied-snapshot"
        marketplace.write_text(json.dumps(payload) + "\n", encoding="utf-8")
        with self.assertRaisesRegex(self.builder.BundleError, "MARKETPLACE_SOURCE_DRIFT"):
            self.build()


if __name__ == "__main__":
    unittest.main(verbosity=2)
