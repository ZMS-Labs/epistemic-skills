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


    def test_signed_octopus_merge_is_not_a_permanent_red(self):
        """`merge_authored_content` cannot AUTO-EXEMPT an octopus merge, which
        is not the same as being unable to VERIFY one. Returning None routed it
        to `unverifiable`, which raises unconditionally and names a remedy
        ("fetch them before running this check") that no fetch can satisfy: no
        fetch turns three parents into two. A correctly signed octopus merge
        was a permanently red gate."""
        octopus = {
            "sha": "f" * 40,
            "parents": [{"sha": "1" * 40}, {"sha": "2" * 40}, {"sha": "3" * 40}],
            "commit": {
                "message": "merge: three heads\n\n"
                           "Signed-off-by: Ada Lovelace <ada@example.com>",
                "author": {"name": "Ada Lovelace", "email": "ada@example.com"},
            },
        }
        self.assertEqual(CHECK_DCO.unsigned_commits([octopus]), [])

    def test_unsigned_octopus_merge_still_fails(self):
        """The positive control: falling through to the ordinary sign-off
        requirement must still REQUIRE the sign-off, not wave the merge past."""
        octopus = {
            "sha": "e" * 40,
            "parents": [{"sha": "1" * 40}, {"sha": "2" * 40}, {"sha": "3" * 40}],
            "commit": {"message": "merge: three heads",
                       "author": {"name": "Ada Lovelace",
                                  "email": "ada@example.com"}},
        }
        self.assertEqual(CHECK_DCO.unsigned_commits([octopus]),
                         ["eeeeeeeeeeee"])

    def test_two_parent_merge_with_absent_objects_is_still_unverifiable(self):
        """The other None cause must keep failing closed: a two-parent merge
        whose objects are not in this clone cannot be classified, and an
        exemption that cannot be verified is not an exemption."""
        merge = {
            "sha": "d" * 40,
            "parents": [{"sha": "a" * 40}, {"sha": "b" * 40}],
            "commit": {"message": "merge: two heads",
                       "author": {"name": "Ada Lovelace",
                                  "email": "ada@example.com"}},
        }
        with self.assertRaises(SystemExit):
            CHECK_DCO.unsigned_commits([merge])


if __name__ == "__main__":
    unittest.main()
