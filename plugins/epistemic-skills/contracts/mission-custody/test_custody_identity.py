#!/usr/bin/env python3
"""Issue #162 safeguard regressions. Injected measurements are simulations."""
import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import custody_mission as cm
import test_custody_mission as fixtures

try:
    import custody_identity as identity
except ModuleNotFoundError:
    identity = None


class IdentitySafeguardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='custody-identity-')
        self.addCleanup(self.temp.cleanup)
        self.ws = Path(self.temp.name).resolve()
        self.m = fixtures.open_mission(self.ws, 'identity', 'Synthetic identity regression')

    def guard(self):
        self.assertIsNotNone(identity, 'durable identity safeguard is missing')
        return identity

    def checkpoints(self):
        return len(self.m.store.checkpoint_paths())

    def simulated_compatible(self):
        return patch.object(self.guard(), '_measure_pairs', return_value='NO_MISMATCH_OBSERVED')

    def test_native_alias_refuses_before_approval(self):
        a, b = self.ws / 'Case-witness', self.ws / 'case-witness'
        a.write_text('sentinel')
        if not b.exists() or not os.path.samefile(a, b):
            self.skipTest('native filesystem does not alias this witness')
        before = self.checkpoints()
        with self.assertRaisesRegex(cm.CustodyError, 'KNOWN_MISMATCH'):
            self.m.approve()
        self.assertEqual(before, self.checkpoints())
        self.assertEqual('sentinel', a.read_text())

    def test_pending_and_corrupt_sidecars_block_legacy_draft_effect_and_pass(self):
        g = self.guard()
        for payload in ('{bad', json.dumps({'state': 'pending'})):
            g.pending_path(self.m.store.mission_dir).write_text(payload)
            before = self.checkpoints()
            for operation in (self.m.approve,
                              lambda: self.m.record_effect('artifact.txt', 'payload', 'r'),
                              lambda: self.m._require_identity_contexts([self.ws])):
                with self.assertRaisesRegex(cm.CustodyError, 'UNKNOWN.*pending'):
                    operation()
            self.assertEqual(before, self.checkpoints())
            self.assertFalse((self.ws / 'artifact.txt').exists())
            self.assertEqual('draft', self.m.status()['status'])
            self.assertTrue(self.m.verify_chain()['chain_ok'])
            g.pending_path(self.m.store.mission_dir).unlink()

    def test_simulated_compatible_measurement_cleans_record_and_writes(self):
        g = self.guard()
        with self.simulated_compatible():
            self.m.approve()
            self.m.record_effect('artifact.txt', 'payload', 'r')
        self.assertEqual('payload', (self.ws / 'artifact.txt').read_text())
        self.assertFalse(g.pending_path(self.m.store.mission_dir).exists())

    def test_missing_parent_refuses_without_hierarchy_or_chain_change(self):
        with self.simulated_compatible():
            before = self.checkpoints()
            with self.assertRaisesRegex(cm.CustodyError, 'UNKNOWN'):
                self.m.record_effect('missing/child.txt', 'payload', 'r')
        self.assertEqual(before, self.checkpoints())
        self.assertFalse((self.ws / 'missing').exists())

    def test_pending_is_durable_before_scratch_and_permission_failure_retains_it(self):
        g = self.guard()
        def denied(fd, prefix, owned, comparator):
            p = g.pending_path(self.m.store.mission_dir)
            self.assertEqual('pending', json.loads(p.read_text())['state'])
            raise PermissionError('simulated read-only context')
        before = self.checkpoints()
        with patch.object(g, '_measure_pairs', side_effect=denied):
            with self.assertRaisesRegex(cm.CustodyError, 'UNKNOWN'):
                self.m.approve()
        self.assertEqual(before, self.checkpoints())
        self.assertTrue(g.pending_path(self.m.store.mission_dir).exists())
        with self.simulated_compatible(), self.assertRaisesRegex(cm.CustodyError, 'pending'):
            self.m.approve()

    def test_interrupted_process_leaves_blocking_record_and_scratch(self):
        g = self.guard()
        script = '''import os,sys
from pathlib import Path
import custody_identity as g
from custody_mission import _same_artifact
def crash(fd,prefix,owned,comparator):
    os.open(prefix+'orphan',os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600,dir_fd=fd)
    os._exit(73)
g._measure_pairs=crash
g.check_context(Path(sys.argv[1]),Path(sys.argv[2]),_same_artifact)
'''
        p = subprocess.run([sys.executable, '-c', script,
                            str(self.m.store.mission_dir), str(self.ws)],
                           cwd=Path(__file__).parent, capture_output=True, text=True)
        self.assertEqual(73, p.returncode, p.stderr)
        leftovers = list(self.ws.glob('.custody-probe-*'))
        self.assertEqual(1, len(leftovers))
        with self.simulated_compatible(), self.assertRaisesRegex(cm.CustodyError, 'pending'):
            self.m.approve()
        self.assertTrue(leftovers[0].exists())
        self.assertTrue(g.pending_path(self.m.store.mission_dir).exists())

    def test_replacement_is_preserved_and_unknown(self):
        g = self.guard()
        replacement = self.ws / 'replacement'
        replacement.write_text('other-owner')
        def replaced(fd, prefix, owned, comparator):
            name = prefix + 'owned'
            f = os.open(name, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600, dir_fd=fd)
            owned.append((name, f))
            os.replace(replacement, self.ws / name)
            return 'NO_MISMATCH_OBSERVED'
        with patch.object(g, '_measure_pairs', side_effect=replaced):
            with self.assertRaisesRegex(cm.CustodyError, 'UNKNOWN'):
                self.m.approve()
        leftovers = list(self.ws.glob('.custody-probe-*'))
        self.assertEqual(1, len(leftovers))
        self.assertEqual('other-owner', leftovers[0].read_text())
        self.assertTrue(g.pending_path(self.m.store.mission_dir).exists())

    def test_early_refusal_precedes_ack_but_late_refusal_retains_ack(self):
        g = self.guard()
        junk = self.ws / 'missions/.junk/checkpoints'
        junk.mkdir(parents=True)
        (junk / 'r00000001.json').write_text('{invalid')
        before = self.checkpoints()
        with patch.object(g, '_measure_pairs', return_value='KNOWN_MISMATCH'), contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaisesRegex(cm.CustodyError, 'KNOWN_MISMATCH'):
                self.m.record_effect('artifact.txt', 'payload', 'r', acknowledge_unreadable=['.junk'])
        self.assertEqual(before, self.checkpoints())
        calls = 0
        def context_changed(*args):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise cm.CustodyError('UNKNOWN: simulated late context change')
        with patch.object(self.m, '_require_identity_contexts', side_effect=context_changed), contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaisesRegex(cm.CustodyError, 'late context change'):
                self.m.record_effect('artifact.txt', 'payload', 'r', acknowledge_unreadable=['.junk'])
        self.assertEqual(before + 1, self.checkpoints())
        self.assertTrue(any('unreadable-acknowledged: .junk' in n for n in self.m.status()['state']['notes']))
        self.assertFalse((self.ws / 'artifact.txt').exists())
        self.assertEqual([], self.m.store.load_receipts())

    def test_native_excluded_alias_draft_effect_preserves_bytes_and_receipts(self):
        self.m = fixtures.open_mission(self.ws, 'excluded', 'Synthetic excluded alias regression',
                                       scope_out=['secrets.env'])
        sentinel = self.ws / 'secrets.env'
        sentinel.write_text('sentinel')
        attempted = self.ws / 'SECRETS.env'
        if not attempted.exists() or not os.path.samefile(sentinel, attempted):
            self.skipTest('native alias witness absent')
        self.assertEqual(['secrets.env'], self.m.status()['manifest']['scope']['out'])
        before = self.checkpoints()
        with self.assertRaisesRegex(cm.CustodyError, 'KNOWN_MISMATCH'):
            self.m.record_effect('SECRETS.env', 'overwritten', 'r')
        self.assertEqual('sentinel', sentinel.read_text())
        self.assertEqual(before, self.checkpoints())
        self.assertEqual([], self.m.store.load_receipts())
        self.assertFalse(list(self.ws.glob('.custody-probe-*')))

    def test_pending_blocks_real_pass_and_reconcile_without_state_mutation(self):
        g = self.guard()
        with self.simulated_compatible():
            self.m.approve()
            self.m.record_effect('artifact.txt', 'original', 'r')
        (self.ws / 'artifact.txt').write_text('outside-edit')
        self.assertEqual(['artifact.txt'], self.m.resume())
        g.pending_path(self.m.store.mission_dir).write_text('{bad')
        before = self.checkpoints()
        with self.assertRaisesRegex(cm.CustodyError, 'pending'):
            self.m.reconcile('artifact.txt', 'repair', 'r2')
        self.assertEqual('outside-edit', (self.ws / 'artifact.txt').read_text())
        self.assertEqual(before, self.checkpoints())
        g.pending_path(self.m.store.mission_dir).unlink()
        with self.simulated_compatible():
            self.m.reconcile('artifact.txt', 'repair', 'r2')
        self.m.begin_verification()
        g.pending_path(self.m.store.mission_dir).write_text('{bad')
        before = self.checkpoints()
        self.m.actor = 'agent:acceptor'
        with self.assertRaisesRegex(cm.CustodyError, 'pending'):
            self.m.record_verdict('PASS', self.m.actor, 'declared-role-separation', 'Synthetic test acceptance')
        self.assertEqual(before, self.checkpoints())
        self.assertEqual('verifying', self.m.status()['status'])
        self.assertFalse(list((self.m.store.mission_dir / 'verdicts').glob('*PASS*')))
        self.assertTrue(any('IDENTITY-UNKNOWN' in item for item in self.m.resume()))

    def test_each_directory_is_measured_not_inherited_from_root(self):
        g = self.guard()
        child = self.ws / 'child'
        child.mkdir()
        parents = []
        def measurement(fd, prefix, owned, comparator):
            parents.append((os.fstat(fd).st_dev, os.fstat(fd).st_ino))
            return 'NO_MISMATCH_OBSERVED' if len(parents) == 1 else 'KNOWN_MISMATCH'
        before = self.checkpoints()
        with patch.object(g, '_measure_pairs', side_effect=measurement):
            with self.assertRaisesRegex(cm.CustodyError, 'KNOWN_MISMATCH'):
                self.m.record_effect('child/artifact.txt', 'payload', 'r')
        self.assertEqual(2, len(set(parents)))
        self.assertEqual(before, self.checkpoints())
        self.assertFalse((child / 'artifact.txt').exists())

    def test_sidecar_sync_failure_precedes_scratch(self):
        g = self.guard()
        before = self.checkpoints()
        with patch.object(g.os, 'fsync', side_effect=OSError('simulated fsync failure')), patch.object(g, '_measure_pairs') as measure:
            with self.assertRaisesRegex(cm.CustodyError, 'UNKNOWN'):
                self.m.approve()
            measure.assert_not_called()
        self.assertTrue(g.pending_path(self.m.store.mission_dir).exists())
        self.assertEqual(before, self.checkpoints())
        self.assertFalse(list(self.ws.glob('.custody-probe-*')))

    def test_cleanup_failure_preserves_pending_and_scratch(self):
        g = self.guard()
        unlink = os.unlink
        def deny(name, *args, **kwargs):
            if str(name).startswith('.custody-probe-'):
                raise PermissionError('simulated cleanup failure')
            return unlink(name, *args, **kwargs)
        with patch.object(g.os, 'unlink', deny), patch.object(g.os, 'supports_dir_fd', os.supports_dir_fd | {deny}):
            with self.assertRaisesRegex(cm.CustodyError, 'UNKNOWN'):
                self.m.approve()
        self.assertTrue(g.pending_path(self.m.store.mission_dir).exists())
        self.assertTrue(list(self.ws.glob('.custody-probe-*')))

    def test_process_interruptions_at_persistence_and_cleanup_boundaries(self):
        g = self.guard()
        for boundary in ('before-scratch', 'after-cleanup', 'before-latch-removal'):
            with self.subTest(boundary=boundary):
                script = r"""import os,sys
from pathlib import Path
import custody_identity as g
from custody_mission import _same_artifact
boundary=sys.argv[3]
original_sync=os.fsync
original_unlink=os.unlink
calls=0
def sync(fd):
    global calls
    calls+=1
    original_sync(fd)
    if (boundary=='before-scratch' and calls==2) or (boundary=='after-cleanup' and calls==3):
        os._exit(74)
def unlink(name,*a,**kw):
    if boundary=='before-latch-removal' and name=='identity-probe.pending.json':
        os._exit(74)
    return original_unlink(name,*a,**kw)
g.os.fsync=sync
g.os.unlink=unlink
g.os.supports_dir_fd=set(g.os.supports_dir_fd)|{unlink}
g.check_context(Path(sys.argv[1]),Path(sys.argv[2]),_same_artifact)
"""
                p = subprocess.run([sys.executable, '-c', script, str(self.m.store.mission_dir), str(self.ws), boundary],
                                   cwd=Path(__file__).parent, capture_output=True, text=True)
                self.assertEqual(74, p.returncode, p.stderr)
                self.assertTrue(g.pending_path(self.m.store.mission_dir).exists())
                with self.simulated_compatible(), self.assertRaisesRegex(cm.CustodyError, 'pending'):
                    self.m.approve()
                self.assertFalse(list(self.ws.glob('.custody-probe-*')))
                # Test-only reset after proving the latch. No recovery API is added.
                g.pending_path(self.m.store.mission_dir).unlink()

    def test_root_mismatch_quarantines_without_descendant_override(self):
        g = self.guard()
        child = self.ws / 'child'
        child.mkdir()
        with patch.object(g, '_measure_pairs', side_effect=['KNOWN_MISMATCH', 'NO_MISMATCH_OBSERVED']) as measure:
            with self.assertRaisesRegex(cm.CustodyError, 'KNOWN_MISMATCH'):
                self.m.record_effect('child/artifact.txt', 'payload', 'r')
        self.assertEqual(1, measure.call_count)
        self.assertFalse((child / 'artifact.txt').exists())

    def test_pending_record_replacement_is_not_removed(self):
        g = self.guard()
        replacement = self.ws / 'replacement'
        replacement.write_text('other-owner')
        def replace(fd, prefix, owned, comparator):
            os.replace(replacement, g.pending_path(self.m.store.mission_dir))
            return 'NO_MISMATCH_OBSERVED'
        with patch.object(g, '_measure_pairs', side_effect=replace):
            with self.assertRaisesRegex(cm.CustodyError, 'UNKNOWN.*replaced'):
                self.m.approve()
        self.assertEqual('other-owner', g.pending_path(self.m.store.mission_dir).read_text())

    def test_sync_failure_after_cleanup_preserves_latch(self):
        g = self.guard()
        original = os.fsync
        for failure in (3, 4):  # parent cleanup sync; final store removal sync
            calls = 0
            def fail_once(fd):
                nonlocal calls
                calls += 1
                if calls == failure:
                    raise OSError('simulated persistence failure')
                return original(fd)
            with self.subTest(failure=failure), patch.object(g.os, 'fsync', side_effect=fail_once):
                with self.assertRaisesRegex(cm.CustodyError, 'UNKNOWN'):
                    self.m.approve()
            self.assertTrue(g.pending_path(self.m.store.mission_dir).exists())
            self.assertFalse(list(self.ws.glob('.custody-probe-*')))
            with self.simulated_compatible(), self.assertRaisesRegex(cm.CustodyError, 'pending'):
                self.m.approve()
            g.pending_path(self.m.store.mission_dir).unlink()  # test-only reset

    def test_unavailable_primitives_refuse_without_scratch(self):
        g = self.guard()
        before = self.checkpoints()
        with patch.object(g.os, 'supports_dir_fd', set()):
            with self.assertRaisesRegex(cm.CustodyError, 'UNKNOWN.*unavailable'):
                self.m.approve()
        self.assertEqual(before, self.checkpoints())
        self.assertFalse(list(self.ws.glob('.custody-probe-*')))
        self.assertFalse(g.pending_path(self.m.store.mission_dir).exists())

    def test_concurrent_record_is_not_overwritten(self):
        g = self.guard()
        g.pending_path(self.m.store.mission_dir).symlink_to(self.ws / 'absent-record')
        with self.simulated_compatible(), self.assertRaisesRegex(cm.CustodyError, 'pending'):
            self.m.approve()
        self.assertTrue(g.pending_path(self.m.store.mission_dir).is_symlink())
        self.assertFalse((self.ws / 'absent-record').exists())

    def test_native_legacy_active_effect_and_pass_refuse(self):
        a, b = self.ws / 'Case-witness', self.ws / 'case-witness'
        a.write_text('sentinel')
        if not b.exists() or not os.path.samefile(a, b):
            self.skipTest('native alias witness absent')
        with self.simulated_compatible():
            self.m.approve()
        before = self.checkpoints()
        with self.assertRaisesRegex(cm.CustodyError, 'KNOWN_MISMATCH'):
            self.m.record_effect('artifact.txt', 'payload', 'r')
        self.assertEqual(before, self.checkpoints())
        self.assertFalse((self.ws / 'artifact.txt').exists())
        self.m.begin_verification()
        self.m.actor = 'agent:acceptor'
        before = self.checkpoints()
        with self.assertRaisesRegex(cm.CustodyError, 'KNOWN_MISMATCH'):
            self.m.record_verdict('PASS', self.m.actor, 'declared-role-separation', 'Synthetic legacy acceptance')
        self.assertEqual(before, self.checkpoints())
        self.assertEqual('verifying', self.m.status()['status'])

    def test_sibling_pending_blocks_other_mission_effect_and_pass(self):
        g = self.guard()
        sibling = fixtures.open_mission(self.ws, 'sibling', 'Synthetic sibling custody')
        with self.simulated_compatible():
            self.m.approve()
            self.m.record_effect('artifact.txt', 'original', 'r')
        g.pending_path(sibling.store.mission_dir).write_text('{invalid')
        before = self.checkpoints()
        with self.simulated_compatible():
            with self.assertRaisesRegex(cm.CustodyError, 'UNKNOWN.*pending'):
                self.m.record_effect('artifact.txt', 'changed', 'r2')
        self.assertEqual(before, self.checkpoints())
        self.assertEqual('original', (self.ws / 'artifact.txt').read_text())
        self.m.begin_verification()
        self.m.actor = 'agent:acceptor'
        before = self.checkpoints()
        with self.simulated_compatible():
            with self.assertRaisesRegex(cm.CustodyError, 'UNKNOWN.*pending'):
                self.m.record_verdict('PASS', self.m.actor, 'declared-role-separation', 'Synthetic sibling acceptance')
        self.assertEqual(before, self.checkpoints())
        self.assertTrue(g.pending_path(sibling.store.mission_dir).exists())

    def test_unreadable_pending_discovery_is_not_acknowledgeable(self):
        self.guard()
        sibling = self.ws / 'missions/unreadable'
        sibling.mkdir()
        original = Path.stat
        def deny(path, *args, **kwargs):
            if path == sibling:
                raise PermissionError('simulated pending discovery denial')
            return original(path, *args, **kwargs)
        with self.simulated_compatible(), patch.object(Path, 'stat', deny):
            with self.assertRaisesRegex(cm.CustodyError, 'UNKNOWN.*discovery'):
                self.m.approve()
        self.assertEqual('draft', self.m.status()['status'])

    def test_native_diagnostic_probe_reports_refusal_without_crashing(self):
        a, b = self.ws / 'Case-witness', self.ws / 'case-witness'
        a.write_text('sentinel')
        if not b.exists() or not os.path.samefile(a, b):
            self.skipTest('native alias witness absent')
        result = subprocess.run([sys.executable, str(Path(__file__).with_name('probe_case_insensitivity.py'))],
                                capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn('SAFEGUARD REFUSED', result.stdout)
        self.assertIn('identity safeguard', result.stdout)

    def test_cli_pending_refusal_and_diagnostics_keep_exit_contract(self):
        g = self.guard()
        g.pending_path(self.m.store.mission_dir).write_text('{corrupt')
        common = ['--workspace', str(self.ws), '--actor', self.m.actor, '--mission', 'identity']
        cli = Path(__file__).with_name('custody_cli.py')
        before = self.checkpoints()
        refused = subprocess.run([sys.executable, str(cli), 'effect', *common,
                                  '--path', 'artifact.txt', '--content', 'payload', '--request-id', 'r'],
                                 capture_output=True, text=True)
        self.assertEqual(2, refused.returncode, refused.stderr)
        self.assertIn('identity safeguard', refused.stderr)
        self.assertNotIn('Traceback', refused.stderr)
        self.assertFalse((self.ws / 'artifact.txt').exists())
        self.assertEqual(before, self.checkpoints())
        status = subprocess.run([sys.executable, str(cli), 'status', *common], capture_output=True, text=True)
        self.assertEqual(0, status.returncode, status.stderr)
        self.assertEqual('checkpoint@1', json.loads(status.stdout)['record'])
        self.assertIn('UNKNOWN', status.stderr)
        resume = subprocess.run([sys.executable, str(cli), 'resume', *common], capture_output=True, text=True)
        self.assertEqual(3, resume.returncode, resume.stderr)
        self.assertIn('IDENTITY-UNKNOWN', resume.stdout)
        self.assertEqual(before, self.checkpoints())

    def test_root_resolution_error_is_blocking_unknown(self):
        self.guard()
        with patch.object(Path, 'resolve', side_effect=PermissionError('simulated root denial')):
            try:
                self.m._require_identity_contexts([])
            except Exception as exc:
                self.assertIsInstance(exc, cm.CustodyError)
                self.assertIn('UNKNOWN', str(exc))
            else:
                self.fail('resolution failure allowed')

    def test_pass_loop_is_explicit_acceptance_refusal_and_preserves_state(self):
        self.guard()
        folder = self.ws / 'folder'
        folder.mkdir()
        with self.simulated_compatible():
            self.m.approve()
            self.m.record_effect('folder/artifact.txt', 'original', 'r')
        (folder / 'artifact.txt').unlink()
        folder.rmdir()
        folder.symlink_to('folder')
        self.m.begin_verification()
        self.m.actor = 'agent:acceptor'
        before = self.checkpoints()
        try:
            with self.simulated_compatible():
                self.m.record_verdict('PASS', self.m.actor, 'declared-role-separation', 'Synthetic loop acceptance')
        except Exception as exc:
            self.assertIsInstance(exc, cm.AcceptanceRefused)
            self.assertIn('identity safeguard', str(exc))
        else:
            self.fail('PASS accepted an unmeasurable loop context')
        self.assertEqual(before, self.checkpoints())
        self.assertEqual('verifying', self.m.status()['status'])
        self.assertFalse(list((self.m.store.mission_dir / 'verdicts').glob('*PASS*')))


if __name__ == '__main__':
    unittest.main(verbosity=2)
