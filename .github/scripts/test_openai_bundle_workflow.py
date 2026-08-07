#!/usr/bin/env python3
from __future__ import annotations

import unittest
from pathlib import Path

WORKFLOW = Path(__file__).resolve().parents[1] / "workflows" / "openai-bundles.yml"
SOURCE_EXPRESSION = "${{ github.event.pull_request.head.sha || github.sha }}"


class OpenAIBundleWorkflowTests(unittest.TestCase):
    def test_artifacts_bind_to_durable_source_revision(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn(f"SOURCE_REVISION: {SOURCE_EXPRESSION}", text)
        self.assertIn("ref: ${{ env.SOURCE_REVISION }}", text)
        self.assertEqual(2, text.count('--source-revision "$SOURCE_REVISION"'))
        self.assertIn("name: epistemic-skills-openai-${{ env.SOURCE_REVISION }}", text)
        self.assertIn("python .github/scripts/test_openai_bundle_workflow.py", text)
        self.assertEqual(3, text.count(".github/scripts/test_openai_bundle_workflow.py"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
