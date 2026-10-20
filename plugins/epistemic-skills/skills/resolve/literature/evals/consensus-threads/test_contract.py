"""Source-contract checks, not evidence of model behavior or provider execution."""
from pathlib import Path
import unittest

LITERATURE = Path(__file__).resolve().parents[2]


class ThreadsContract(unittest.TestCase):
    def test_incomplete_runs_do_not_claim_convergence(self):
        text = (LITERATURE / 'METHOD.md').read_text()
        for marker in ('`pending`', '`failed`', '`ambiguous`', 'not convergence labels'):
            self.assertIn(marker, text)

    def test_release_records_bind_current_authority_and_evidence_fields(self):
        repo = Path(__file__).resolve().parents[7]
        handbook = (repo / 'docs/handbook/pages/Release-Process-and-Versioning.md').read_text()
        self.assertIn('/docs/release/evidence/7.3-preauthorization.md', handbook)
        self.assertNotIn('PREAUTH-7.2.0.md', handbook)
        self.assertNotIn('explains v7.2.0 behavior', handbook)
        notes = (repo / 'docs/release/RELEASE-7.3.0.md').read_text()
        self.assertIn('| Gate | Status | Exact subject | Evidence | Limits |', notes)

    def test_hosted_suite_executes_this_contract(self):
        repo = Path(__file__).resolve().parents[7]
        workflow = (repo / '.github/workflows/epistemic-flexibility.yml').read_text()
        self.assertIn('run: python plugins/epistemic-skills/skills/resolve/literature/evals/consensus-threads/test_contract.py', workflow)

    def test_ambiguous_dispatch_and_failed_outcome_are_explicit(self):
        text = (LITERATURE / 'reference/consensus-threads.md').read_text()
        for marker in ('AMBIGUOUS', 'before IDs', 'reported terminal failure', 'either dispatch tool'):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_contract_is_reachable_from_method(self):
        self.assertIn('reference/consensus-threads.md', (LITERATURE / 'METHOD.md').read_text())

    def test_operational_boundaries_have_an_authoritative_home(self):
        path = LITERATURE / 'reference/consensus-threads.md'
        self.assertTrue(path.is_file(), 'Threads operational contract is missing')
        text = path.read_text()
        for marker in ('create_thread', 'add_to_thread', '30 seconds', '`pro`', '`deep`',
                       'included capacity', 'overages', 'capped-by-budget', 'fetch',
                       '[N.M]', 'document', 'primary', 'UNAVAILABLE', '2026-10-20'):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)


if __name__ == '__main__':
    unittest.main()
