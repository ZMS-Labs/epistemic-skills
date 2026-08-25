#!/usr/bin/env python3
"""Durable mission store: atomic JSON writes, checkpoint hash chain, receipts."""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path

from verify_mission_custody import epoch_skew_anywhere, validate_record


class StoreError(Exception):
    pass


class ChainBroken(StoreError):
    pass


class EpochSkew(ChainBroken):
    """This store is from a NEWER contract epoch than this reader implements.

    Deliberately a ChainBroken SUBCLASS, so every existing handler keeps its
    current behavior byte for byte: `Mission.load` still skips the store, the
    gate still degrades to inert rather than bricking the tool loop, and no
    caller has to learn a new exception to stay correct. The only thing that
    changes is that a caller who WANTS to distinguish "too new" from "corrupt"
    now can -- and the message says which.

    Not fail-closed, on purpose. Flipping an unreadable store to a hard refusal
    would strand every workspace it applies to with no verb to resolve it,
    which is the same objection es#173's kernel 3 raises against shipping the
    fail-open inversion without a duplicate-resolution verb in the same change.
    Disclose the skew; do not invert the posture underneath it.
    """


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def _publish_exclusive(tmp: str, path: Path) -> None:
    """Publish tmp at path, refusing to overwrite: two writers racing to the
    same checkpoint name must produce one winner and one LOUD failure, never a
    silent last-writer-wins clobber of a chained record."""
    try:
        os.link(tmp, path)
        return
    except FileExistsError:
        raise StoreError(
            f"{path.name} already exists; concurrent writer detected") from None
    except OSError:
        pass  # hard links unsupported on this filesystem
    try:
        with open(path, "xb") as out, open(tmp, "rb") as src:
            out.write(src.read())
            out.flush()
            os.fsync(out.fileno())
    except FileExistsError:
        raise StoreError(
            f"{path.name} already exists; concurrent writer detected") from None
    except BaseException:
        # Never leave a partial record at the canonical name: it would brick
        # chain loading AND block every retry with a misleading concurrent-
        # writer refusal. Residual window: a hard kill between write and this
        # unlink still strands a partial file -- load_latest fails loudly on
        # it (never silently), and the os.link path above has no such window.
        try:
            os.unlink(path)
        except OSError:
            pass
        raise


def atomic_write_json(path: Path, record: dict, *, exclusive: bool = False) -> str:
    errors = validate_record(record)
    if errors:
        raise StoreError(f"invalid record for {path.name}: {errors[:3]}")
    path.parent.mkdir(parents=True, exist_ok=True)
    data = (json.dumps(record, indent=1, sort_keys=True) + "\n").encode("utf-8")
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        if exclusive:
            _publish_exclusive(tmp, path)
            os.unlink(tmp)
        else:
            os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise
    return sha256_bytes(data)


class MissionStore:
    def __init__(self, mission_dir: Path) -> None:
        self.mission_dir = Path(mission_dir)
        self.checkpoints_dir = self.mission_dir / "checkpoints"
        self.receipts_dir = self.mission_dir / "receipts"

    def checkpoint_paths(self) -> list[Path]:
        if not self.checkpoints_dir.is_dir():
            return []
        return sorted(self.checkpoints_dir.glob("r????????.json"))

    def _path_for(self, revision: int) -> Path:
        return self.checkpoints_dir / f"r{revision:08d}.json"

    def write_checkpoint(self, record: dict) -> str:
        errors = validate_record(record)
        if errors:
            raise StoreError(f"invalid checkpoint: {errors[:3]}")
        revision = record["revision"]
        existing = self.checkpoint_paths()
        expected_rev = len(existing) + 1
        if revision != expected_rev:
            raise StoreError(
                f"revision {revision} out of order; expected {expected_rev}")
        if revision == 1:
            if record["prev_checkpoint_sha256"] is not None:
                raise StoreError("revision 1 must have null prev sha")
        else:
            prior_sha = sha256_file(existing[-1])
            if record["prev_checkpoint_sha256"] != prior_sha:
                raise StoreError("prev_checkpoint_sha256 does not match prior file")
        return atomic_write_json(self._path_for(revision), record, exclusive=True)

    def _successor_proves_alteration(self, paths: list[Path],
                                     index: int) -> bool:
        """True when the NEXT checkpoint's recorded predecessor hash no longer
        matches `paths[index]`'s current bytes.

        That link is independently understandable: it was written before these
        bytes were touched, so a mismatch is proof of alteration and not an
        opinion about epochs. Read defensively -- an unreadable or malformed
        successor proves nothing, and must not be turned into an accusation.
        """
        if index + 1 >= len(paths):
            return False
        try:
            successor = json.loads(paths[index + 1].read_text(encoding="utf-8"))
            recorded = successor.get("prev_checkpoint_sha256")
            if not isinstance(recorded, str):
                return False
            return recorded != sha256_file(paths[index])
        except (OSError, ValueError):
            return False

    def load_latest(self) -> tuple[dict, Path]:
        paths = self.checkpoint_paths()
        if not paths:
            raise StoreError(f"no checkpoints under {self.checkpoints_dir}")
        prev_sha: str | None = None
        for index, path in enumerate(paths):
            # THE FILENAME IS PART OF THE RECORD. `write_checkpoint` derives
            # the destination from the record's revision and refuses
            # out-of-order writes, but nothing checked that `rNNNNNNNN.json`
            # CONTAINS revision NNNNNNNN, or that revisions are contiguous.
            # Renaming r2 to the r3 filename therefore loaded as a healthy
            # chain -- the hash link still verifies, because the bytes did not
            # change -- and the NEXT mutation refused with "already exists;
            # concurrent writer detected", a diagnosis naming a race that
            # never happened. The exclusive publish keeps the store safe; only
            # this loader can make the DIAGNOSIS honest.
            expected_revision = index + 1
            if path.name != f"r{expected_revision:08d}.json":
                raise ChainBroken(
                    f"{path.name}: checkpoint filenames must be contiguous "
                    f"from r00000001.json; expected "
                    f"r{expected_revision:08d}.json at this position. The "
                    "hash chain may still verify -- a renamed or removed "
                    "checkpoint file does not alter any bytes -- so this is "
                    "a FILENAME break, not a concurrent writer")
            record = json.loads(path.read_text(encoding="utf-8"))
            errors = validate_record(record)
            if errors:
                # ANYWHERE: an embedded mission-manifest@2 inside a
                # checkpoint@1 fails validation with a familiar outer
                # kind, and reporting that as ChainBroken sends the
                # operator to repair a store that is merely too new.
                skew = epoch_skew_anywhere(record, "checkpoint")
                # ... BUT A PROVABLE BREAK OUTRANKS A CLAIM. EpochSkew says
                # "this reader cannot tell a genuine newer record from a
                # relabelled corrupt one" -- true only while nothing else
                # settles it. The SUCCESSOR settles it: its
                # prev_checkpoint_sha256 was computed over this file's
                # ORIGINAL bytes, so a mismatch proves these bytes changed
                # after the successor was written, whatever epoch they now
                # claim. Returning the weaker diagnosis let a relabel conceal
                # a demonstrated alteration and send the operator to upgrade a
                # reader instead of to the damage (measured on a
                # three-revision chain with the INTERIOR checkpoint edited).
                #
                # The tail has no successor, so nothing settles it there and
                # EpochSkew remains the honest answer -- the same unsealed-tail
                # boundary this contract already documents.
                if skew and not self._successor_proves_alteration(paths,
                                                                  index):
                    raise EpochSkew(f"{path.name}: {skew}")
                if skew:
                    raise ChainBroken(
                        f"{path.name}: CHAIN BREAK PROVEN, and the record also "
                        f"CLAIMS a newer epoch -- the next checkpoint's "
                        f"prev_checkpoint_sha256 was computed over this file's "
                        f"original bytes and no longer matches them, so these "
                        f"bytes were altered after it was written. Do not read "
                        f"this as a stale reader: {skew}")
                raise ChainBroken(f"{path.name}: invalid: {errors[:3]}")
            if record.get("revision") != expected_revision:
                raise ChainBroken(
                    f"{path.name}: contains revision "
                    f"{record.get('revision')!r}, not {expected_revision} -- "
                    "the filename and the record disagree about which "
                    "checkpoint this is")
            if record["prev_checkpoint_sha256"] != prev_sha:
                raise ChainBroken(f"{path.name}: chain mismatch")
            prev_sha = sha256_file(path)
        return record, paths[-1]

    def receipt_path(self, request_id: str) -> Path:
        name = sha256_bytes(request_id.encode("utf-8")) + ".json"
        return self.receipts_dir / name

    def write_receipt(self, record: dict) -> Path:
        errors = validate_record(record)
        if errors:
            raise StoreError(f"invalid receipt: {errors[:3]}")
        path = self.receipt_path(record["request_id"])
        if path.exists():
            raise StoreError(
                f"receipt already exists for request_id {record['request_id']!r}")
        atomic_write_json(path, record)
        return path

    def load_receipts(self) -> list[dict]:
        if not self.receipts_dir.is_dir():
            return []
        return [json.loads(p.read_text(encoding="utf-8"))
                for p in sorted(self.receipts_dir.glob("*.json"))]
