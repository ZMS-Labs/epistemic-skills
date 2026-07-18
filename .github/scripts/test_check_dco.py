#!/usr/bin/env python3
"""Synthetic signed-pass / unsigned-fail tests for the DCO gate."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("check_dco.py")
SPEC = importlib.util.spec_from_file_location("check_dco", SCRIPT)
CHECK_DCO = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(CHECK_DCO)


def commit(sha: str, message: str, name: str = "Ada Lovelace", email: str = "ada@example.com"):
    return {"sha": sha, "commit": {"message": message, "author": {"name": name, "email": email}}}


class DcoTests(unittest.TestCase):
    def test_signed_commit_passes(self):
        commits = [commit("a" * 40, "feat: x\n\nSigned-off-by: Ada Lovelace <ada@example.com>")]
        self.assertEqual(CHECK_DCO.unsigned_commits(commits), [])

    def test_unsigned_commit_fails(self):
        self.assertEqual(CHECK_DCO.unsigned_commits([commit("b" * 40, "feat: x")]), ["bbbbbbbbbbbb"])

    def test_one_unsigned_commit_blocks_multi_commit_pr(self):
        commits = [
            commit("c" * 40, "feat: signed\n\nSigned-off-by: Ada Lovelace <ada@example.com>"),
            commit("d" * 40, "fix: unsigned"),
        ]
        self.assertEqual(CHECK_DCO.unsigned_commits(commits), ["dddddddddddd"])

    def test_mismatched_signoff_does_not_pass(self):
        commits = [commit("e" * 40, "feat: x\n\nSigned-off-by: Someone Else <else@example.com>")]
        self.assertEqual(CHECK_DCO.unsigned_commits(commits), ["eeeeeeeeeeee"])


if __name__ == "__main__":
    unittest.main()
