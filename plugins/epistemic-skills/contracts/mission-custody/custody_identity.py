"""Bounded filesystem/comparator witnesses, with a crash-visible refusal latch.

Not filesystem certification or an atomic defense against hostile replacement.
The sidecar is advisory evidence, never authority to delete/adopt an orphan.
Only descriptor-relative POSIX probing is implemented; other contexts refuse.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import stat
import uuid

_PENDING = 'identity-probe.pending.json'
_PAIRS = (('Case', 'case'), ('straße', 'strasse'), ('é', 'e\u0301'))


class IdentityRefused(Exception):
    pass


def pending_path(store: Path) -> Path:
    return store / _PENDING


def pending_reason(store: Path) -> str | None:
    try:
        pending_path(store).lstat()
    except FileNotFoundError:
        return None
    except OSError as exc:
        return f'UNKNOWN: pending probe state unreadable ({type(exc).__name__}); investigation required'
    return 'UNKNOWN: pending probe record exists; investigation required; preserve uncertain entries'


def _key(st):
    return st.st_dev, st.st_ino


def _directory(path: Path) -> int:
    if (not hasattr(os, 'O_DIRECTORY') or not hasattr(os, 'O_NOFOLLOW')
            or not all(fn in os.supports_dir_fd for fn in (os.open, os.stat, os.unlink))):
        raise IdentityRefused('UNKNOWN: descriptor-relative identity probing unavailable')
    return os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)


def _same_entry(fd: int, name: str, owned_fd: int) -> bool:
    observed = os.stat(name, dir_fd=fd, follow_symlinks=False)
    held = os.fstat(owned_fd)
    return (stat.S_ISREG(observed.st_mode) and observed.st_nlink == 1
            and observed.st_ino != 0 and _key(observed) == _key(held))


def _measure_pairs(fd: int, prefix: str, owned: list, comparator) -> str:
    result = 'NO_MISMATCH_OBSERVED'
    for index, (left, right) in enumerate(_PAIRS):
        left, right = f'{prefix}{index}-{left}', f'{prefix}{index}-{right}'
        a = os.open(left, os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_NOFOLLOW,
                    0o600, dir_fd=fd)
        owned.append((left, a))
        if not _same_entry(fd, left, a):
            raise IdentityRefused('UNKNOWN: probe entry identity unavailable')
        try:
            b = os.open(right, os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_NOFOLLOW,
                        0o600, dir_fd=fd)
        except FileExistsError:
            other = os.stat(right, dir_fd=fd, follow_symlinks=False)
            if not stat.S_ISREG(other.st_mode) or _key(other) != _key(os.fstat(a)):
                raise IdentityRefused('UNKNOWN: unexpected probe collision')
            aliases = True
        else:
            owned.append((right, b))
            if not _same_entry(fd, right, b):
                raise IdentityRefused('UNKNOWN: probe entry identity unavailable')
            aliases = _key(os.fstat(a)) == _key(os.fstat(b))
            if aliases:
                raise IdentityRefused('UNKNOWN: exclusive probe identities not distinct')
        if aliases != comparator(left, right):
            result = 'KNOWN_MISMATCH'
    return result


def check_context(store: Path, parent: Path, comparator) -> str:
    """Measure this existing directory only. Any incomplete lifecycle latches.

    Persistence ordering: exclusive sidecar + file/dir fsync, scratch effects,
    ownership-checked cleanup + directory fsync, then sidecar removal + fsync.
    Failures/interruption preserve the sidecar. No automatic recovery is offered.
    Filesystems that cannot supply these primitives remain UNKNOWN.
    """
    reason = pending_reason(store)
    if reason:
        raise IdentityRefused(reason)
    parent_fd = store_fd = pending_fd = None
    owned: list[tuple[str, int]] = []
    prefix = '.custody-probe-' + uuid.uuid4().hex + '-'
    try:
        parent_fd = _directory(parent)
        store_fd = _directory(store)
        parent_key = _key(os.fstat(parent_fd))
        if _key(os.stat(parent, follow_symlinks=False)) != parent_key:
            raise IdentityRefused('UNKNOWN: target context changed')
        pending_fd = os.open(_PENDING, os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_NOFOLLOW,
                             0o600, dir_fd=store_fd)
        record = json.dumps({'record': 'identity-probe-pending@1', 'state': 'pending',
                             'parent': str(parent), 'prefix': prefix}, ensure_ascii=True).encode()
        with os.fdopen(os.dup(pending_fd), 'wb') as out:
            out.write(record)
            out.flush()
            os.fsync(out.fileno())
        os.fsync(store_fd)  # Must complete before any scratch entry is created.
        result = _measure_pairs(parent_fd, prefix, owned, comparator)
        # Only a normal completed measurement attempts cleanup. An uncertain
        # entry/exception leaves ALL remaining entries for investigation.
        for name, f in owned:
            if not _same_entry(parent_fd, name, f):
                raise IdentityRefused('UNKNOWN: probe entry replaced; preserve uncertain entries')
        for name, f in owned:
            if not _same_entry(parent_fd, name, f):
                raise IdentityRefused('UNKNOWN: probe entry changed during cleanup')
            os.unlink(name, dir_fd=parent_fd)
        os.fsync(parent_fd)
        if (_key(os.stat(parent, follow_symlinks=False)) != parent_key
                or _key(os.stat(store, follow_symlinks=False)) != _key(os.fstat(store_fd))):
            raise IdentityRefused('UNKNOWN: context changed during probe')
        if not _same_entry(store_fd, _PENDING, pending_fd):
            raise IdentityRefused('UNKNOWN: pending record replaced; preserve it')
        os.unlink(_PENDING, dir_fd=store_fd)
        try:
            os.fsync(store_fd)
        except OSError:
            # Restore the refusal latch if the final directory sync fails.
            # Storage failure can prevent restoration too: no claim of
            # durability on a filesystem that cannot honor fsync is made.
            try:
                restore = os.open(_PENDING, os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_NOFOLLOW,
                                  0o600, dir_fd=store_fd)
                with os.fdopen(restore, 'wb') as out:
                    out.write(record)
                    out.flush()
                    os.fsync(out.fileno())
                os.fsync(store_fd)
            finally:
                raise IdentityRefused('UNKNOWN: pending record removal could not be synced; investigation required')
        return result
    except (OSError, ValueError) as exc:
        raise IdentityRefused(f'UNKNOWN: identity probe failed ({type(exc).__name__}); '
                              f'preserve uncertain entries; pending record: {pending_path(store)}') from exc
    finally:
        for _, f in owned:
            os.close(f)
        for f in (pending_fd, parent_fd, store_fd):
            if f is not None:
                os.close(f)
