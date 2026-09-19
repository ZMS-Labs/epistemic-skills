import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from usage_context import load_usage_context, render, MAX_BODY_BYTES


class UsageDeliveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.entry = self.root / 'skills/epistemic/SKILL.md'
        self.entry.parent.mkdir(parents=True)
        self.body = '---\nname: epistemic\n---\nUnicode: λ 中文 🧭; quotes " and slash \\ end\n'
        self.entry.write_bytes(self.body.encode('utf-8'))

    def tearDown(self):
        self.temp.cleanup()

    def emit(self, source='startup', harness='codex', **kwargs):
        return render(self.root, harness, {'hook_event_name':'SessionStart','source':source}, **kwargs)

    def test_unicode_json_roundtrip(self):
        result = json.loads(json.dumps(self.emit(), ensure_ascii=True))
        self.assertTrue(result['hookSpecificOutput']['additionalContext'].endswith(self.body))
        self.assertEqual(load_usage_context(self.root), self.body)

    def test_lifecycle_replays_preserve_body_after_context_loss(self):
        for harness, sources in [('codex', ['startup','resume','clear','compact']),
                                 ('claude', ['startup','resume','clear','compact','fork'])]:
            for source in sources:
                self.assertTrue(self.emit(source,harness)['hookSpecificOutput']['additionalContext'].endswith(self.body))
        with self.assertRaises(ValueError): self.emit('fork')
        with self.assertRaises(ValueError): render(self.root,'claude',{'hook_event_name':'PreToolUse','source':'startup'})

    def test_duplicates_have_same_fingerprint_and_bounded_identical_output(self):
        self.assertEqual(self.emit(), self.emit())
        digest = hashlib.sha256(self.body.encode()).hexdigest()
        self.assertIn('sha256='+digest, self.emit()['hookSpecificOutput']['additionalContext'])
        self.entry.write_text('changed', encoding='utf-8')
        with self.assertRaises(ValueError): self.emit(expected_sha256=digest)

    def test_missing_empty_and_oversized_are_observable(self):
        self.entry.unlink()
        with self.assertRaises(FileNotFoundError): self.emit()
        self.entry.write_text('',encoding='utf-8')
        with self.assertRaises(ValueError): self.emit()
        self.entry.write_text('x'*(MAX_BODY_BYTES+1),encoding='utf-8')
        with self.assertRaises(ValueError): self.emit()

    def test_manifest_disagreement(self):
        for directory, version in [('.claude-plugin','6.0.0'),('.codex-plugin','7.0.0')]:
            path=self.root/directory/'plugin.json';path.parent.mkdir()
            path.write_text(json.dumps({'version':version}),encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'versions disagree'):self.emit()

    def test_invalid_input_produces_visible_fallback_without_custody_block(self):
        run=subprocess.run([sys.executable,str(Path(__file__).with_name('usage_context.py')),'--harness','codex'],input='invalid',capture_output=True,text=True)
        self.assertEqual(run.returncode,0)
        result=json.loads(run.stdout)
        self.assertIn('unavailable',result['systemMessage'])
        self.assertNotIn('decision',result)
        self.assertNotIn('continue',result)


if __name__ == '__main__':unittest.main()

