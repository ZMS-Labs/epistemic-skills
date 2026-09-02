#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from custody_store import (  # noqa: E402
    ChainBroken, MissionStore, StoreError, atomic_write_json, sha256_file,
)

FAILURES: list[str] = []


def check(name: str, cond: bool) -> None:
    if not cond:
        FAILURES.append(name)
        print(f"FAIL {name}")
    else:
        print(f"ok   {name}")


def manifest() -> dict:
    return json.loads(
        (ROOT / "examples" / "valid-manifest-minimal.json").read_text(
            encoding="utf-8"))


def checkpoint(rev: int, prev: str | None, status: str = "draft") -> dict:
    return {
        "record": "checkpoint@1",
        "mission_id": "tracer-media-missing",
        "revision": rev,
        "status": status,
        "prev_checkpoint_sha256": prev,
        "manifest": manifest(),
        "state": {"frontier": "f", "notes": [], "unresolved_verdicts": []},
        "receipt_ids": [],
        "written_utc": "2026-08-11T00:00:01Z",
        "written_by": "agent:worker",
    }


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        mdir = Path(td) / "missions" / "tracer-media-missing"
        store = MissionStore(mdir)

        # invalid record refused before touching disk
        try:
            store.write_checkpoint({"record": "checkpoint@1"})
            check("store-refuses-invalid", False)
        except StoreError:
            check("store-refuses-invalid", True)

        sha1 = store.write_checkpoint(checkpoint(1, None))
        check("r1-written", (mdir / "checkpoints" / "r00000001.json").exists())

        # r2 with wrong prev refused
        try:
            store.write_checkpoint(checkpoint(2, "b" * 64, "active"))
            check("store-refuses-bad-chain", False)
        except StoreError:
            check("store-refuses-bad-chain", True)

        store.write_checkpoint(checkpoint(2, sha1, "active"))
        latest, path = store.load_latest()
        check("latest-is-r2", latest["revision"] == 2)

        # tamper with r1 on disk -> chain verification must fail.
        # Replace a string that provably exists in the store-written record and
        # keep newline handling platform-stable, so the byte change is the
        # tamper itself (CI caught the prior version passing on Windows only
        # via LF->CRLF rewriting while the target string never matched).
        p1 = mdir / "checkpoints" / "r00000001.json"
        tampered = p1.read_text(encoding="utf-8").replace(
            "agent:worker", "agent:tamper")
        assert tampered != p1.read_text(encoding="utf-8")
        p1.write_text(tampered, encoding="utf-8", newline="\n")
        try:
            store.load_latest()
            check("chain-tamper-detected", False)
        except ChainBroken:
            check("chain-tamper-detected", True)

        # receipts round-trip
        receipt = json.loads((ROOT / "examples" / "valid-receipt.json").read_text(
            encoding="utf-8"))
        rp = store.write_receipt(receipt)
        check("receipt-written", rp.exists())
        check("receipt-loaded", store.load_receipts() == [receipt])

        # writing a second receipt with the same request_id must be refused
        try:
            store.write_receipt(receipt)
            check("store-refuses-duplicate-receipt", False)
        except StoreError:
            check("store-refuses-duplicate-receipt", True)

    # two writers racing to the same checkpoint name: exclusive publication
    # makes the loser fail loudly instead of silently clobbering the winner
    # (probe P8: last-writer-wins lost a session's checkpoint with no trace)
    with tempfile.TemporaryDirectory() as td:
        target = Path(td) / "r00000001.json"
        atomic_write_json(target, checkpoint(1, None), exclusive=True)
        first_sha = sha256_file(target)
        try:
            atomic_write_json(target, checkpoint(1, None, "active"),
                              exclusive=True)
            check("store-refuses-checkpoint-clobber", False)
        except StoreError:
            check("store-refuses-checkpoint-clobber", True)
        check("store-clobber-loser-left-no-tmp",
              list(Path(td).glob("*.tmp")) == [])
        check("store-clobber-winner-intact", sha256_file(target) == first_sha)

    # the no-hardlink fallback must not strand a partial record at the
    # canonical name on failure, and a retry must then succeed (merge-gate
    # blocker 3: partial JSON bricked loading AND blocked every retry with a
    # misleading concurrent-writer refusal)
    import custody_store as cs
    with tempfile.TemporaryDirectory() as td:
        target = Path(td) / "r00000001.json"
        real_link, real_fsync = cs.os.link, cs.os.fsync

        def no_link(*a, **k):
            raise OSError("hard links unsupported")

        calls = {"n": 0}

        def flaky_fsync(fd):
            calls["n"] += 1
            if calls["n"] == 2:  # 1st = tmp write; 2nd = fallback target
                raise OSError(28, "No space left on device")
            return real_fsync(fd)

        cs.os.link, cs.os.fsync = no_link, flaky_fsync
        try:
            try:
                atomic_write_json(target, checkpoint(1, None), exclusive=True)
                check("fallback-failure-propagates", False)
            except OSError:
                check("fallback-failure-propagates", True)
            check("fallback-no-partial-left", not target.exists())
            check("fallback-no-tmp-left", list(Path(td).glob("*.tmp")) == [])

            cs.os.fsync = real_fsync  # link still unsupported: retry via fallback
            atomic_write_json(target, checkpoint(1, None), exclusive=True)
            check("fallback-retry-succeeds", target.exists())
        finally:
            cs.os.link, cs.os.fsync = real_link, real_fsync

    # ---- filename must agree with the revision it claims ----------------
    # `write_checkpoint` derives the destination from the RECORD's revision
    # and refuses out-of-order writes, but `load_latest` never checked that
    # `rNNNNNNNN.json` actually CONTAINS revision NNNNNNNN, nor that the
    # revisions are contiguous. Renaming r2 to the r3 filename therefore
    # loaded as a healthy chain (the hash link still verifies), and the next
    # mutation refused with "already exists; concurrent writer detected" --
    # a diagnosis that names a race that never happened and sends the
    # operator looking for another process. The chain is fine; the FILENAMES
    # are not, and only this loader can say so.
    with tempfile.TemporaryDirectory() as td:
        store = MissionStore(Path(td) / "m")
        store.write_checkpoint(checkpoint(1, None))
        r1 = store.checkpoint_paths()[0]
        store.write_checkpoint(checkpoint(2, sha256_file(r1)))
        r2 = store.checkpoint_paths()[1]
        r2.rename(r2.parent / "r00000003.json")
        try:
            store.load_latest()
            check("renamed-revision-detected", False)
        except ChainBroken as exc:
            check("renamed-revision-detected", True)
            check("renamed-revision-names-the-file",
                  "r00000003.json" in str(exc))
            # The old failure mode was "already exists; concurrent writer
            # detected" from the NEXT write. The new message may SAY the words
            # in order to deny them, so the assertion is on the claim, not the
            # substring.
            check("renamed-revision-does-not-blame-a-race",
                  "concurrent writer detected" not in str(exc)
                  and "FILENAME break" in str(exc))
        except Exception:  # noqa: BLE001
            check("renamed-revision-detected", False)

    # Positive control: an ORDINARY chain must still load. A contiguity check
    # that refuses everything would pass the test above and break the product.
    with tempfile.TemporaryDirectory() as td:
        store = MissionStore(Path(td) / "m")
        store.write_checkpoint(checkpoint(1, None))
        r1 = store.checkpoint_paths()[0]
        store.write_checkpoint(checkpoint(2, sha256_file(r1)))
        record, path = store.load_latest()
        check("contiguity-positive-control",
              record["revision"] == 2 and path.name == "r00000002.json")

    print(f"\n{len(FAILURES)} failures")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    raise SystemExit(main())
