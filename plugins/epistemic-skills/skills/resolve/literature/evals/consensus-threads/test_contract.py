"""Source-contract checks, not evidence of model behavior or provider execution."""
from pathlib import Path
import unittest

LITERATURE = Path(__file__).resolve().parents[2]


class ThreadsContract(unittest.TestCase):
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
