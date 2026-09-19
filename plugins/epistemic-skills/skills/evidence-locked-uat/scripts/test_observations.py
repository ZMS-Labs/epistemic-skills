"""Synthetic contract regressions; no rendered UAT or calibration claims."""
import json
import subprocess
import unittest
from pathlib import Path
import judge

ROOT = Path(__file__).resolve().parents[1]


def fixture():
    c = judge._contract('REQ-SAVE', 'critical', 1)
    c['schema_version'] = 'uat-contract@2'
    cc = c['criteria'][0]
    cc.update(expected_observation='New name remains after reload',
              disconfirming_observation='Old name returns after reload',
              required_oracles=['rendered-ui', 'persistence'])
    row = judge._vrow(cc['id'], 'PASS')
    row.update(expected_observation={'result': 'observed', 'evidence': ['after.png: new name']},
               disconfirming_observation={'result': 'not-observed', 'evidence': ['reload.png: new name']},
               oracle_observations=[{'oracle': o, 'result': 'satisfied', 'evidence': ['reload.png: new name']} for o in cc['required_oracles']])
    return c, row


class ObservationTests(unittest.TestCase):
    def gate(self, c, row):
        cid = c['id'] + '--returning-desktop'
        gate = judge.judge([c], 'smoke', 'synthetic', 'http://localhost', 'synthetic',
                           {cid: judge._actor(cid)}, {cid: {'criteria': [row]}})
        # Execute the actual Workflow template with deterministic mocked role returns.
        # No model/browser call occurs; this proves embedded judge parity, not UAT.
        js = r"""
const fs = require('fs');
const f = JSON.parse(fs.readFileSync(0, 'utf8'));
const source = fs.readFileSync(f.path, 'utf8').replace('export const meta', 'const meta');
const AsyncFunction = Object.getPrototypeOf(async function(){}).constructor;
const run = new AsyncFunction('args', 'phase', 'log', 'agent', 'pipeline', source);
const agent = async (prompt, opts) => {
  if (opts.label === 'compile') {
    const contract = opts.schema.properties.contracts.items;
    if (!contract.required.includes('schema_version')) throw Error('compiler must require version');
    const cc = contract.properties.criteria.items;
    for (const field of ['expected_observation', 'disconfirming_observation']) {
      if (!cc.required.includes(field) || !cc.properties[field]) throw Error('compiler missing ' + field);
    }
    return {contracts: [f.contract]};
  }
  if (opts.label.startsWith('act:')) return {completed: true};
  return {criteria: [f.row]};
};
const pipeline = async (cases, act, verify) => Promise.all(cases.map(async cs => verify(await act(cs))));
run({tier:'smoke',run_id:'synthetic',target_url:'http://localhost',commit_sha:'synthetic',evidence_dir:'synthetic',target_repo_dir:'synthetic',requirement_sources:[]}, ()=>{}, ()=>{}, agent, pipeline).then(g=>process.stdout.write(JSON.stringify(g))).catch(e=>{console.error(e);process.exit(1)});
"""
        result = subprocess.run(['node', '-e', js], input=json.dumps({
            'path': str(ROOT / 'references/workflow-template.mjs'), 'contract': c, 'row': row}),
            capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0, result.stderr)
        embedded = json.loads(result.stdout)
        expected = judge.judge([c], 'smoke', 'synthetic', 'http://localhost', 'synthetic',
                               {cid: judge._actor(cid)}, {cid: {'criteria': [row]}}, verification_mode='blinded')
        self.assertEqual(embedded, expected)
        return gate

    def test_clean_observations_pass(self):
        c, row = fixture()
        self.assertEqual(self.gate(c, row)['release_decision'], 'PASS')

    def test_success_display_failed_persistence(self):
        c, row = fixture()
        row['oracle_observations'][1].update(result='violated', evidence=['reload.png: old name returned'])
        self.assertEqual(self.gate(c, row)['release_decision'], 'FAIL')

    def test_missing_disconfirmation_observation(self):
        c, row = fixture()
        del row['disconfirming_observation']
        self.assertEqual(self.gate(c, row)['release_decision'], 'INCONCLUSIVE')

    def test_missing_compiler_disconfirmation(self):
        c, row = fixture()
        del c['criteria'][0]['disconfirming_observation']
        self.assertEqual(self.gate(c, row)['release_decision'], 'INCONCLUSIVE')

    def test_observed_disconfirmation_fails(self):
        c, row = fixture()
        row['disconfirming_observation']['result'] = 'observed'
        self.assertEqual(self.gate(c, row)['release_decision'], 'FAIL')

    def test_missing_oracle_and_uncited_observation(self):
        for field in ['oracle_observations', 'expected_observation']:
            c, row = fixture()
            if field == 'oracle_observations':
                row[field].pop()
            else:
                row[field]['evidence'] = []
            self.assertEqual(self.gate(c, row)['release_decision'], 'INCONCLUSIVE')

    def test_unknown_version_does_not_use_legacy_pass(self):
        c, row = fixture()
        c['schema_version'] = 'uat-contract@999'
        self.assertEqual(self.gate(c, row)['release_decision'], 'INCONCLUSIVE')

    def test_legacy_recompute_is_explicit(self):
        c, row = fixture()
        del c['schema_version']
        gate = self.gate(c, judge._vrow(row['criterion_id'], 'PASS'))
        self.assertEqual(gate['release_decision'], 'PASS')
        self.assertEqual(gate['contract_versions'], ['legacy-unversioned'])
        self.assertTrue(any('historical' in s for s in gate['known_limitations']))

    def test_direct_is_not_blinded(self):
        c, row = fixture()
        self.assertEqual(self.gate(c, row)['verification_mode'], 'direct')

    def test_routine_copy_only_remains_bounded(self):
        result = subprocess.run(['python', str(ROOT / 'evals/triage/tests/run_tests.py')], capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        skill = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
        self.assertIn('This path creates no `run_id`', skill)
        self.assertIn('bounded preview/test', skill)


if __name__ == '__main__':
    unittest.main()
