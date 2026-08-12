#!/usr/bin/env python3
"""Mission lifecycle: draft -> active -> verifying -> completed, with drift
reanchoring on resume and a clearable FAIL path (no PA reject dead-end)."""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from custody_store import (
    MissionStore, StoreError, atomic_write_json, sha256_bytes, sha256_file,
)
from verify_mission_custody import TIERS, VERDICTS, validate_record

_OPEN_STATES = {"draft", "active", "reopened", "verifying"}
_EFFECT_STATES = {"draft", "active", "reopened"}
_TIER_RANK = {"declared-role-separation": 1, "operator-accepted": 2}
assert set(_TIER_RANK) == TIERS, "tier rank table out of sync with verify_mission_custody.TIERS"

_ABS_DRIVE_RE = re.compile(r"^[A-Za-z]:")
_RETIRED_NOTE = "receipt loss acknowledged: "
# Notes are the mission's append-only, hash-chained narrative AND the carrier
# for retirement (checkpoint state is exact-field-closed in @1, so a
# retired_ids field would break the schema). Machine-written notes therefore
# own these prefixes exclusively: a caller-supplied note that could imitate
# one would let ordinary narrative forge machine state.
_RESERVED_NOTE_PREFIXES = (
    "effect: ", "reconciled: ", "drift detected: ", "receipt restored: ",
    _RETIRED_NOTE,
)


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _tier_meets(actual: str, required: str) -> bool:
    return _TIER_RANK[actual] >= _TIER_RANK[required]


def _same_artifact(left: str, right: str) -> bool:
    """Do two workspace-relative paths name the same artifact on THIS
    platform? resume() already casefolds its drift keys on Windows; the
    obligation markers must use the identical rule or an obligation raised
    under one casing can never be discharged under another -- and since
    both name one physical file, that is a mission that can never close."""
    left = left.replace("\\", "/")
    right = right.replace("\\", "/")
    if os.name == "nt":
        return left.casefold() == right.casefold()
    return left == right


def _find_marker(unresolved: list[str], prefix: str, artifact_relpath: str) -> str | None:
    """The marker in `unresolved` naming this artifact, or None. Matching is
    by artifact identity, never by string equality of the whole marker."""
    for marker in unresolved:
        if marker.startswith(prefix) and _same_artifact(
                marker[len(prefix):], artifact_relpath):
            return marker
    return None


class CustodyError(Exception):
    pass


class NoActiveMission(CustodyError):
    pass


class MultipleActiveMissions(CustodyError):
    pass


class IllegalTransition(CustodyError):
    pass


class AcceptanceRefused(CustodyError):
    pass


class Mission:
    def __init__(self, store: MissionStore, workspace: Path, actor: str) -> None:
        self.store = store
        self.workspace = Path(workspace)
        self.actor = actor

    # -- construction -----------------------------------------------------

    @classmethod
    def open(cls, workspace: Path, mission_id: str, instruction: str,
              operator_ref: str, steward_ref: str,
              required_tier: str = "declared-role-separation", *, actor: str,
              scope_in: list[str] | None = None, scope_out: list[str] | None = None,
              permissions: list[str] | None = None,
              protected_state: list[str] | None = None,
              hold_if: list[str] | None = None, stop_if: list[str] | None = None,
              escalate_if: list[str] | None = None,
              acceptable_costs: list[str] | None = None) -> "Mission":
        workspace = Path(workspace)
        store = MissionStore(workspace / "missions" / mission_id)
        created = now_utc()
        manifest = {
            "record": "mission-manifest@1",
            "mission_id": mission_id,
            "created_utc": created,
            "authority": {
                "operator_ref": operator_ref,
                "instruction": instruction,
                "amendments": [],
                "permissions": list(permissions or []),
                "protected_state": list(protected_state or []),
                "acceptable_costs": list(acceptable_costs or []),
            },
            "scope": {"in": list(scope_in or []), "out": list(scope_out or [])},
            "acceptance": {"required_tier": required_tier, "acceptor_ref": None},
            "stop_rules": {
                "hold_if": list(hold_if or []),
                "stop_if": list(stop_if or []),
                "escalate_if": list(escalate_if or []),
            },
            "steward_ref": steward_ref,
        }
        checkpoint = {
            "record": "checkpoint@1",
            "mission_id": mission_id,
            "revision": 1,
            "status": "draft",
            "prev_checkpoint_sha256": None,
            "manifest": manifest,
            "state": {
                "frontier": "await operator approval",
                "notes": [],
                "unresolved_verdicts": [],
            },
            "receipt_ids": [],
            "written_utc": created,
            "written_by": actor,
        }
        store.write_checkpoint(checkpoint)
        return cls(store, workspace, actor)

    @classmethod
    def load(cls, workspace: Path, actor: str) -> "Mission":
        workspace = Path(workspace)
        missions_root = workspace / "missions"
        active: list[Path] = []
        skipped: list[str] = []
        if missions_root.is_dir():
            for mission_dir in sorted(missions_root.iterdir()):
                if not mission_dir.is_dir():
                    continue
                store = MissionStore(mission_dir)
                if not store.checkpoint_paths():
                    continue
                try:
                    latest, _ = store.load_latest()
                except (StoreError, ValueError) as exc:
                    # A CORRUPT sibling must not brick discovery of a healthy
                    # mission -- but the skip is loud, and if nothing loads the
                    # skip reasons ride the NoActiveMission error. Environmental
                    # OSErrors (transient locks, permissions) propagate instead:
                    # skipping those would reroute discovery around a mission
                    # that is merely busy, inviting a duplicate open.
                    reason = f"{mission_dir.name}: {type(exc).__name__}: {exc}"
                    skipped.append(reason)
                    print(("custody: skipping unreadable mission dir " + reason)
                          .encode("ascii", "backslashreplace").decode("ascii"),
                          file=sys.stderr)
                    continue
                if latest["status"] not in ("completed", "cancelled"):
                    active.append(mission_dir)
        if not active:
            detail = f"; skipped unreadable: {'; '.join(skipped)}" if skipped else ""
            raise NoActiveMission(f"no active mission under {missions_root}{detail}")
        if len(active) > 1:
            names = ", ".join(p.name for p in active)
            raise MultipleActiveMissions(f"multiple active missions: {names}")
        return cls(MissionStore(active[0]), workspace, actor)

    # -- internal helpers ---------------------------------------------------

    def _verify_manifest(self, latest: dict) -> None:
        """The whole manifest is immutable from open to close (no code path
        amends it in @1). Verifying only the instruction left every other
        authority field -- scope, permissions, stop_rules, and critically
        acceptance.required_tier -- silently editable on the tail checkpoint,
        which no successor hash references."""
        origin_path = self.store.checkpoint_paths()[0]
        origin = json.loads(origin_path.read_text(encoding="utf-8"))
        origin_manifest = origin["manifest"]
        latest_manifest = latest["manifest"]
        if origin_manifest != latest_manifest:
            differing = sorted(
                key for key in set(origin_manifest) | set(latest_manifest)
                if origin_manifest.get(key) != latest_manifest.get(key))
            raise CustodyError(
                "manifest changed since mission open (tampered): "
                + ", ".join(differing))

    def _write_next(self, latest: dict, latest_path: Path, *, status: str,
                     note: str | None = None, frontier: str | None = None,
                     add_receipt_id: str | None = None,
                     receipt_ids: list[str] | None = None,
                     unresolved_verdicts: list[str] | None = None) -> dict:
        notes = list(latest["state"]["notes"])
        if note is not None:
            notes.append(note)
        state = {
            "frontier": frontier if frontier is not None else latest["state"]["frontier"],
            "notes": notes,
            "unresolved_verdicts": (
                list(unresolved_verdicts) if unresolved_verdicts is not None
                else list(latest["state"]["unresolved_verdicts"])),
        }
        receipt_ids = (list(receipt_ids) if receipt_ids is not None
                       else list(latest["receipt_ids"]))
        if add_receipt_id is not None:
            receipt_ids.append(add_receipt_id)
        checkpoint = {
            "record": "checkpoint@1",
            "mission_id": latest["mission_id"],
            "revision": latest["revision"] + 1,
            "status": status,
            "prev_checkpoint_sha256": sha256_file(latest_path),
            "manifest": latest["manifest"],
            "state": state,
            "receipt_ids": receipt_ids,
            "written_utc": now_utc(),
            "written_by": self.actor,
        }
        self.store.write_checkpoint(checkpoint)
        return checkpoint

    def _resolve_artifact_path(self, relpath: str) -> Path:
        if not isinstance(relpath, str) or not relpath:
            raise CustodyError(f"invalid artifact path: {relpath!r}")
        norm = relpath.replace("\\", "/")
        if norm.startswith("/") or _ABS_DRIVE_RE.match(norm):
            raise CustodyError(f"artifact path must be workspace-relative: {relpath!r}")
        if any(part == ".." for part in norm.split("/")):
            raise CustodyError(f"artifact path escapes workspace: {relpath!r}")
        workspace_resolved = self.workspace.resolve()
        target = (self.workspace / norm).resolve()
        try:
            target.relative_to(workspace_resolved)
        except ValueError:
            raise CustodyError(f"artifact path escapes workspace: {relpath!r}") from None
        return target

    def _write_effect(self, latest: dict, artifact_relpath: str, content: str,
                       request_id: str) -> dict:
        # Idempotency is checked BEFORE the workspace mutates: previously the
        # target file was rewritten and only then did write_receipt refuse the
        # duplicate, leaving an unreceipted mutation behind.
        if self.store.receipt_path(request_id).exists():
            raise CustodyError(
                f"receipt already exists for request_id {request_id!r}; "
                "effects are idempotent by request id -- use a fresh id")
        if request_id in self._retired_receipt_ids(latest):
            # Reuse would make one id mean two different artifacts across the
            # record, forcing an auditor to walk revisions to disambiguate.
            raise CustodyError(
                f"request_id {request_id!r} was retired by an acknowledged "
                "receipt loss and can never be reused -- use a fresh id")
        target = self._resolve_artifact_path(artifact_relpath)
        before_sha = sha256_file(target) if target.exists() else None
        data = content.encode("utf-8")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        receipt = {
            "record": "receipt@1",
            "mission_id": latest["mission_id"],
            "request_id": request_id,
            "actor": self.actor,
            "utc": now_utc(),
            "artifact_path": artifact_relpath.replace("\\", "/"),
            "before_sha256": before_sha,
            "after_sha256": sha256_bytes(data),
        }
        self.store.write_receipt(receipt)
        return receipt

    def _load_receipt(self, request_id: str) -> dict | None:
        """None means UNLOADABLE -- absent, corrupt, or schema-invalid alike.
        A corrupt receipt must degrade to drift (RECEIPT-MISSING), never crash
        resume: crashing the recovery path on a mangled receipt is a denial of
        service by exactly the tampering drift detection exists to catch."""
        path = self.store.receipt_path(request_id)
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            return None
        except ValueError:
            return None
        if validate_record(record):
            return None
        # A receipt whose own request_id disagrees with the content-addressed
        # name it is stored under is malformed by construction -- never a
        # trustworthy source for a claim about that id.
        return record if record.get("request_id") == request_id else None

    def _historical_effect_path(self, request_id: str) -> str | None:
        """The artifact path this request id was minted against, read from the
        hash-chained checkpoint history: the effect note appended by the very
        revision that put the id into receipt_ids. A lost receipt's path is
        NOT unknowable -- the chain remembers it, and interior checkpoints are
        tamper-evident, so this is a sounder authority than a receipt file
        anyone able to write the receipts dir could have replaced.
        None when underivable (treated as unprovable, never as agreement)."""
        prev_ids: list[str] = []
        prev_notes: list[str] = []
        for cp_path in self.store.checkpoint_paths():
            record = json.loads(cp_path.read_text(encoding="utf-8"))
            ids = record["receipt_ids"]
            notes = record["state"]["notes"]
            if request_id in ids and request_id not in prev_ids:
                for note in notes[len(prev_notes):]:
                    for prefix in ("effect: ", "reconciled: "):
                        if note.startswith(prefix):
                            return note[len(prefix):]
                return None
            prev_ids, prev_notes = ids, notes
        return None

    def _retired_receipt_ids(self, latest: dict) -> set[str]:
        """Ids whose loss was acknowledged. Retirement is permanent and lives
        in the append-only notes (checkpoint state is exact-field-closed in
        @1), so a retired id can never be silently recycled for a different
        artifact once the file that once occupied its path is gone."""
        retired: set[str] = set()
        decoder = json.JSONDecoder()
        for note in latest["state"]["notes"]:
            if not note.startswith(_RETIRED_NOTE):
                continue
            # The id is JSON-encoded, so it is read back exactly regardless of
            # what it contains. Splitting on a delimiter truncated any id
            # holding that delimiter, and a truncated id compared unequal to
            # the real one -- silently un-retiring it (merge-gate round 4).
            try:
                value, _ = decoder.raw_decode(note[len(_RETIRED_NOTE):])
            except ValueError:
                continue
            if isinstance(value, str):
                retired.add(value)
        return retired

    def _find_verdict_record(self, verdict: str, reason: str) -> dict | None:
        verdicts_dir = self.store.mission_dir / "verdicts"
        if not verdicts_dir.is_dir():
            return None
        matches = []
        for p in verdicts_dir.glob(f"*-{verdict}.json"):
            rec = json.loads(p.read_text(encoding="utf-8"))
            if rec.get("reason") == reason:
                matches.append(rec)
        if not matches:
            return None
        matches.sort(key=lambda r: r["revision"])
        return matches[-1]

    def _store_verdict(self, revision: int, verdict: str, record: dict) -> None:
        path = self.store.mission_dir / "verdicts" / f"{revision}-{verdict}.json"
        atomic_write_json(path, record)

    # -- mutating lifecycle operations ---------------------------------------

    def approve(self) -> int:
        latest, path = self.store.load_latest()
        self._verify_manifest(latest)
        if latest["status"] != "draft":
            raise IllegalTransition(
                f"cannot approve: status is {latest['status']!r}, expected 'draft'")
        new = self._write_next(latest, path, status="active", note="approved")
        return new["revision"]

    def record_effect(self, artifact_relpath: str, content: str,
                       request_id: str) -> dict:
        latest, path = self.store.load_latest()
        self._verify_manifest(latest)
        if latest["status"] not in _EFFECT_STATES:
            raise IllegalTransition(f"cannot record_effect: status is {latest['status']!r}")
        receipt = self._write_effect(latest, artifact_relpath, content, request_id)
        # A fresh effect on an artifact awaiting re-coverage discharges that
        # obligation -- that is exactly what RECOVER asks for.
        unresolved = latest["state"]["unresolved_verdicts"]
        status = latest["status"]
        remaining = None
        recover = _find_marker(unresolved, "RECOVER:", artifact_relpath)
        if recover is not None:
            remaining = [m for m in unresolved if m != recover]
            if status == "reopened" and not remaining:
                status = "active"
        self._write_next(latest, path, status=status, add_receipt_id=request_id,
                          unresolved_verdicts=remaining,
                          note=f"effect: {artifact_relpath}")
        return receipt

    def note(self, text: str) -> int:
        latest, path = self.store.load_latest()
        self._verify_manifest(latest)
        if latest["status"] not in _OPEN_STATES:
            raise IllegalTransition(f"cannot note: status is {latest['status']!r}")
        for prefix in _RESERVED_NOTE_PREFIXES:
            if text.startswith(prefix):
                raise CustodyError(
                    f"note text may not begin with {prefix!r}: machine-written "
                    "notes carry mission state and narrative must not be able "
                    "to imitate them")
        new = self._write_next(latest, path, status=latest["status"], note=text)
        return new["revision"]

    def set_frontier(self, text: str) -> int:
        latest, path = self.store.load_latest()
        self._verify_manifest(latest)
        if latest["status"] not in _OPEN_STATES:
            raise IllegalTransition(f"cannot set_frontier: status is {latest['status']!r}")
        new = self._write_next(latest, path, status=latest["status"], frontier=text)
        return new["revision"]

    def resume(self) -> list[str]:
        latest, path = self.store.load_latest()
        self._verify_manifest(latest)
        if latest["status"] in ("completed", "cancelled"):
            raise IllegalTransition(f"cannot resume: status is {latest['status']!r}")
        latest_by_key: dict[str, dict] = {}
        missing: list[str] = []
        for request_id in latest["receipt_ids"]:
            receipt = self._load_receipt(request_id)
            if receipt is None:
                # An unloadable receipt is drift, not a skip: the artifact it
                # covered can no longer be verified, and silence here is a
                # false "clean" for exactly the file most likely tampered.
                if request_id not in missing:
                    missing.append(request_id)
                continue
            key = receipt["artifact_path"]
            if os.name == "nt":
                # Case-insensitive filesystems: Doc.md and doc.md are one
                # artifact; keying case-sensitively splits them and reports
                # spurious drift on the superseded casing.
                key = key.casefold()
            latest_by_key[key] = receipt
        mismatched: list[str] = []
        for receipt in latest_by_key.values():
            rel = receipt["artifact_path"]
            target = self.workspace / rel
            actual = sha256_file(target) if target.exists() else None
            if actual != receipt["after_sha256"]:
                mismatched.append(rel)
        mismatched.sort()
        missing.sort()
        findings = mismatched + [f"RECEIPT-MISSING:{rid}" for rid in missing]
        if not findings:
            return []
        unresolved = list(latest["state"]["unresolved_verdicts"])
        for rel in mismatched:
            marker = f"RECONCILIATION:{rel}"
            if marker not in unresolved:
                unresolved.append(marker)
        for rid in missing:
            marker = f"RECEIPT-MISSING:{rid}"
            if marker not in unresolved:
                unresolved.append(marker)
        self._write_next(latest, path, status="reopened", unresolved_verdicts=unresolved,
                          note=f"drift detected: {', '.join(findings)}")
        return findings

    def reconcile(self, artifact_relpath: str, content: str, request_id: str) -> dict:
        latest, path = self.store.load_latest()
        self._verify_manifest(latest)
        if latest["status"] != "reopened":
            raise IllegalTransition(
                f"cannot reconcile: status is {latest['status']!r}, expected 'reopened'")
        norm = artifact_relpath.replace("\\", "/")
        unresolved = latest["state"]["unresolved_verdicts"]
        # reconcile clears DRIFT only. A lost receipt's path is unknowable
        # once the receipt is gone, so any flow that re-binds its request id
        # to a caller-chosen path is a forgery channel (merge-gate round 2,
        # finding A): acknowledge_receipt_loss is the only exit for
        # RECEIPT-MISSING markers, and it destroys nothing.
        marker = _find_marker(unresolved, "RECONCILIATION:", norm)
        if marker is None:
            raise CustodyError(f"no reconciliation marker for {artifact_relpath!r}")
        if f"RECEIPT-MISSING:{request_id}" in unresolved:
            raise CustodyError(
                f"request_id {request_id!r} has a pending receipt-loss marker; "
                "acknowledge the loss and reconcile under a fresh id")
        receipt = self._write_effect(latest, artifact_relpath, content, request_id)
        remaining = [m for m in unresolved if m != marker]
        next_status = "active" if not remaining else "reopened"
        add_id = request_id if request_id not in latest["receipt_ids"] else None
        self._write_next(latest, path, status=next_status, add_receipt_id=add_id,
                          unresolved_verdicts=remaining,
                          note=f"reconciled: {artifact_relpath}")
        return receipt

    def acknowledge_receipt_loss(self, request_id: str) -> int:
        """The only exit for a RECEIPT-MISSING marker. It never writes an
        artifact and never deletes a file, and it never asserts continuity it
        has not proven: a receipt found at the id's path counts as RESTORED
        only if it agrees with the chained history (its own request_id, and
        the artifact path the id was originally minted against). A receipt
        that disagrees is a different receipt wearing the id's name -- trusting
        its schema-validity alone let a forged path silently replace real
        coverage while the mission read clean (merge-gate round 3). Anything
        unproven retires the id with the loss recorded permanently; ongoing
        coverage then requires a FRESH effect, minted as a new event."""
        latest, path = self.store.load_latest()
        self._verify_manifest(latest)
        if latest["status"] != "reopened":
            raise IllegalTransition(
                f"cannot acknowledge_receipt_loss: status is "
                f"{latest['status']!r}, expected 'reopened'")
        marker = f"RECEIPT-MISSING:{request_id}"
        unresolved = latest["state"]["unresolved_verdicts"]
        if marker not in unresolved:
            raise CustodyError(f"no receipt-loss marker for {request_id!r}")
        remaining = [m for m in unresolved if m != marker]
        next_status = "active" if not remaining else "reopened"

        receipt = self._load_receipt(request_id)  # already request_id-checked
        recorded_path = self._historical_effect_path(request_id)
        if receipt is not None and recorded_path is not None \
                and receipt["artifact_path"] == recorded_path:
            new = self._write_next(
                latest, path, status=next_status, unresolved_verdicts=remaining,
                note=(f"receipt restored: {request_id}; matches the recorded "
                      f"effect on {recorded_path}; coverage continues"))
            return new["revision"]

        covered = (f" (covered {json.dumps(recorded_path)})"
                   if recorded_path else "")
        if receipt is None:
            why = "receipt unloadable"
        elif recorded_path is None:
            why = "no recorded effect in the chain to check the receipt against"
        else:
            why = (f"present receipt claims {receipt['artifact_path']!r}, "
                   f"chain records {recorded_path!r} -- NOT trusted")
        receipt_ids = [rid for rid in latest["receipt_ids"] if rid != request_id]
        if recorded_path is not None:
            # Losing coverage is an OBLIGATION, not a footnote: the mission
            # stays reopened, naming the artifact that must be re-covered, so
            # an uncovered artifact can never sit quietly in an active
            # mission just because its receipt was destroyed.
            if _find_marker(remaining, "RECOVER:", recorded_path) is None:
                remaining = remaining + [f"RECOVER:{recorded_path}"]
            next_status = "reopened"
        new = self._write_next(
            latest, path, status=next_status, unresolved_verdicts=remaining,
            receipt_ids=receipt_ids,
            note=(f"{_RETIRED_NOTE}{json.dumps(request_id)}{covered}; {why}; "
                  "id retired permanently -- re-cover the artifact with a "
                  "fresh effect"))
        return new["revision"]

    def begin_verification(self) -> int:
        latest, path = self.store.load_latest()
        self._verify_manifest(latest)
        if latest["status"] != "active":
            raise IllegalTransition(
                f"cannot begin_verification: status is {latest['status']!r}, expected 'active'")
        if latest["state"]["unresolved_verdicts"]:
            raise IllegalTransition(
                "cannot begin_verification: unresolved_verdicts present")
        new = self._write_next(latest, path, status="verifying", note="verification started")
        return new["revision"]

    def record_verdict(self, verdict: str, acceptor_id: str, assurance_tier: str,
                        reason: str) -> int:
        latest, path = self.store.load_latest()
        self._verify_manifest(latest)
        if verdict not in VERDICTS:
            raise CustodyError(f"unknown verdict {verdict!r}")
        if verdict in ("PASS", "FAIL"):
            if latest["status"] != "verifying":
                raise IllegalTransition(
                    f"cannot record {verdict}: status is {latest['status']!r}, "
                    "expected 'verifying'")
        elif latest["status"] not in _OPEN_STATES:
            raise IllegalTransition(f"cannot record verdict: status is {latest['status']!r}")
        if acceptor_id != self.actor:
            # A verdict is recorded by its acceptor: the acting session must
            # BE the named acceptor, so a worker session cannot fabricate a
            # verdict under someone else's name (it can still lie about who it
            # is -- principal binding is the enforcement hook's job -- but the
            # record can no longer be incoherent about it).
            raise AcceptanceRefused(
                f"acceptor_id {acceptor_id!r} must equal the acting actor "
                f"{self.actor!r}: a verdict is recorded by its acceptor")

        manifest = latest["manifest"]
        worker_id = manifest["steward_ref"]
        operator_ref = manifest["authority"]["operator_ref"]
        new_revision = latest["revision"] + 1
        verdict_record = {
            "record": "acceptance-verdict@1",
            "mission_id": latest["mission_id"],
            "revision": new_revision,
            "verdict": verdict,
            "acceptor_id": acceptor_id,
            "worker_id": worker_id,
            "operator_ref": operator_ref,
            "assurance_tier": assurance_tier,
            "receipt_refs": list(latest["receipt_ids"]),
            "reason": reason,
            "utc": now_utc(),
        }
        errors = validate_record(verdict_record)
        if errors:
            raise AcceptanceRefused(f"invalid acceptance-verdict: {errors[:3]}")

        if verdict == "PASS":
            required_tier = manifest["acceptance"]["required_tier"]
            if not _tier_meets(assurance_tier, required_tier):
                raise AcceptanceRefused(
                    f"assurance_tier {assurance_tier!r} does not meet "
                    f"required {required_tier!r}")
            self._store_verdict(new_revision, verdict, verdict_record)
            self._write_next(latest, path, status="completed", note=f"PASS: {reason}")
        elif verdict == "FAIL":
            self._store_verdict(new_revision, verdict, verdict_record)
            unresolved = list(latest["state"]["unresolved_verdicts"]) + [f"FAIL:{reason}"]
            self._write_next(latest, path, status="reopened", unresolved_verdicts=unresolved,
                              note=f"FAIL: {reason}")
        else:  # INCONCLUSIVE
            self._store_verdict(new_revision, verdict, verdict_record)
            self._write_next(latest, path, status=latest["status"],
                              note=f"INCONCLUSIVE: {reason}")
        return new_revision

    def clear_fail(self, reason_fragment: str, receipt_request_id: str) -> int:
        latest, path = self.store.load_latest()
        self._verify_manifest(latest)
        if latest["status"] != "reopened":
            raise IllegalTransition(
                f"cannot clear_fail: status is {latest['status']!r}, expected 'reopened'")
        unresolved = latest["state"]["unresolved_verdicts"]
        matches = [m for m in unresolved if m.startswith("FAIL:") and reason_fragment in m]
        if not matches:
            raise CustodyError(f"no FAIL marker matching {reason_fragment!r}")
        marker = matches[0]
        reason = marker[len("FAIL:"):]
        verdict_rec = self._find_verdict_record("FAIL", reason)
        if verdict_rec is None:
            raise CustodyError("originating FAIL verdict record not found")
        receipt = self._load_receipt(receipt_request_id)
        if receipt is None:
            raise CustodyError(f"no receipt found for request_id {receipt_request_id!r}")
        if receipt["utc"] < verdict_rec["utc"]:
            raise CustodyError(
                f"receipt {receipt_request_id!r} predates the FAIL verdict; remediate first")
        remaining = [m for m in unresolved if m != marker]
        next_status = "active" if not remaining else "reopened"
        new = self._write_next(latest, path, status=next_status, unresolved_verdicts=remaining,
                                note=f"cleared: {marker}")
        return new["revision"]

    def cancel(self, reason: str) -> int:
        latest, path = self.store.load_latest()
        self._verify_manifest(latest)
        if latest["status"] not in ("draft", "active", "reopened", "verifying"):
            raise IllegalTransition(f"cannot cancel: status is {latest['status']!r}")
        new = self._write_next(latest, path, status="cancelled", note=f"cancelled: {reason}")
        return new["revision"]

    def status(self) -> dict:
        latest, _ = self.store.load_latest()
        self._verify_manifest(latest)
        return latest
