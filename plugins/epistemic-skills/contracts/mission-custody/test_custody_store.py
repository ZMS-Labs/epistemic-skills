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

        # tamper with r1 on disk -> chain verification must fail
        p1 = mdir / "checkpoints" / "r00000001.json"
        p1.write_text(p1.read_text(encoding="utf-8").replace(
            "await operator approval", "tampered"), encoding="utf-8")
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

    print(f"\n{len(FAILURES)} failures")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    raise SystemExit(main())
