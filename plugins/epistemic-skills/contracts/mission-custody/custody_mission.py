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
_UNSET = object()  # amend sentinel: distinguishes "leave alone" from "clear"
_GUARD_AUTHORITY_KEYS = ("actuator_guards", "guard_mode")
assert set(_TIER_RANK) == TIERS, "tier rank table out of sync with verify_mission_custody.TIERS"

_ABS_DRIVE_RE = re.compile(r"^[A-Za-z]:")
_RETIRED_NOTE = "receipt loss acknowledged: "
# Tamper-retirement gets its OWN prefix, distinct from an honest loss's
# (T3-1, es#118 fix round 1): the two are already distinguished live (a
# tampered id's "why" is re-derived from evidence, never from which marker
# won priority -- see acknowledge_receipt_loss), but that distinction lived
# only in free text, unreadable to any consumer that wants to treat
# "tampering" and "honest loss" differently (e.g. paging a human on the
# former, not the latter). _retired_receipt_ids still unions both --
# permanent non-reusability is correct either way.
_RETIRED_TAMPERED_NOTE = "receipt tamper acknowledged: "
# Notes are the mission's append-only, hash-chained narrative AND the carrier
# for retirement (checkpoint state is exact-field-closed in @1, so a
# retired_ids field would break the schema). Machine-written notes therefore
# own these prefixes exclusively: a caller-supplied note that could imitate
# one would let ordinary narrative forge machine state.
_RESERVED_NOTE_PREFIXES = (
    "effect: ", "reconciled: ", "drift detected: ", "receipt restored: ",
    "authority amended: ", _RETIRED_NOTE, _RETIRED_TAMPERED_NOTE,
)


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _tier_meets(actual: str, required: str) -> bool:
    return _TIER_RANK[actual] >= _TIER_RANK[required]


def _ascii_case_fold(text: str) -> str:
    """Fold A-Z only, leaving every other codepoint byte-exact.

    NOT str.casefold(): full Unicode folding performs 1-to-many expansions
    that NTFS's per-codepoint upcase table does not -- 'strasse.txt' and
    'strasse.txt' with an eszett casefold equal while coexisting on disk as
    two independent files (verified on NTFS), and U+212A KELVIN SIGN folds
    onto 'k'. Under a marker comparison those false positives let a write to
    one artifact discharge another artifact's obligation, dropping a real
    file from custody while the mission reads clean.

    The two error directions are not symmetric, so the tie-break is not a
    close call. Under-matching leaves an obligation outstanding, and the
    marker names the exact path that discharges it -- visible, recoverable.
    Over-matching silently retires custody of a file nobody is watching."""
    return "".join(c.lower() if "A" <= c <= "Z" else c for c in text)


def _normalize_relpath(path: str) -> str:
    """Spelling differences that cannot denote two different files:
    separator flavor, repeated separators, a leading './', a trailing '/'.
    ('..' never appears -- _resolve_artifact_path rejects it at the door.)"""
    norm = path.replace("\\", "/")
    while "//" in norm:
        norm = norm.replace("//", "/")
    while "/./" in norm:
        norm = norm.replace("/./", "/")
    while norm.startswith("./"):
        norm = norm[2:]
    return norm.rstrip("/") or norm


def _same_artifact(left: str, right: str) -> bool:
    """Do two workspace-relative paths name the same artifact on THIS
    platform? Obligation markers must answer this the same way resume()
    answers it for drift keys, or an obligation raised under one spelling
    can never be discharged under another -- and since both name one
    physical file, that is a mission that can never legitimately close."""
    left = _normalize_relpath(left)
    right = _normalize_relpath(right)
    if os.name == "nt":
        return _ascii_case_fold(left) == _ascii_case_fold(right)
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


class _ReceiptTampered(Exception):
    """Module-private signal, not a CustodyError: raised by _load_receipt,
    caught only by its two @2-aware callers (resume, acknowledge_receipt_loss)
    and never meant to escape either. Distinct from None (UNLOADABLE) on
    purpose -- a receipt whose bytes disagree with the chain-attested sha for
    its id is not absent or corrupt, it is a different receipt wearing the
    id's name. Collapsing the two into one None-shaped signal let a tampered
    receipt read as an honest loss and be silently retired by
    acknowledge_receipt_loss's old path-match heuristic -- discharging
    tampering as if nothing had happened."""

    def __init__(self, request_id: str) -> None:
        super().__init__(request_id)
        self.request_id = request_id


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
              acceptable_costs: list[str] | None = None,
              guard_mode: str | None = None,
              actuator_guards: list | None = None) -> "Mission":
        workspace = Path(workspace)
        # One ACTIVE mission per workspace, enforced at the door: every other
        # command refuses multiple-active discovery, so open creating that
        # state would be a decoy-disarm wedge (a second armed-or-unarmed
        # mission bricks the gate's discovery). Checked BEFORE anything is
        # written, so a refused open leaves no partial mission dir.
        try:
            cls.load(workspace, actor=actor)
        except NoActiveMission:
            pass  # the expected state: nothing active to conflict with
        else:
            raise CustodyError(
                "an active mission already exists under this workspace; "
                "complete or cancel it before opening another")
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
                **({"actuator_guards": actuator_guards}
                   if actuator_guards is not None else {}),
                **({"guard_mode": guard_mode} if guard_mode is not None else {}),
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
        """The manifest is immutable from open to close EXCEPT for
        authority.amendments, which is append-only. Verifying only the
        instruction left every other authority field -- scope, permissions,
        stop_rules, and critically acceptance.required_tier -- silently
        editable on the tail checkpoint, which no successor hash references.
        Amendments are the one sanctioned way authority changes, and they
        may only GROW: rewriting or dropping a recorded amendment would let
        granted authority be quietly disowned after the fact."""
        paths = self.store.checkpoint_paths()
        origin = json.loads(paths[0].read_text(encoding="utf-8"))
        origin_manifest = origin["manifest"]
        latest_manifest = latest["manifest"]
        # No equality fast path: dropping an amendment makes the manifest
        # equal to the origin again, so "same as origin" is not proof of
        # integrity once amendments exist.
        #
        # The append-only baseline is the PREVIOUS checkpoint, not the origin:
        # the origin's amendment list is empty by construction, so comparing
        # against it would let any already-recorded amendment be rewritten on
        # the tail -- the one checkpoint no successor hash protects. Interior
        # checkpoints cannot be edited without breaking the chain, so the
        # chain-protected predecessor is the trustworthy baseline.
        baseline = origin_manifest
        if len(paths) >= 2:
            baseline = json.loads(
                paths[-2].read_text(encoding="utf-8"))["manifest"]
        baseline_amendments = baseline["authority"]["amendments"]
        latest_amendments = latest_manifest["authority"]["amendments"]
        if latest_amendments[:len(baseline_amendments)] != baseline_amendments:
            raise CustodyError(
                "authority.amendments is append-only; recorded amendments "
                "were rewritten or dropped (tampered)")

        # Everything except the amendments list must be byte-identical.
        origin_rest = json.loads(json.dumps(origin_manifest))
        latest_rest = json.loads(json.dumps(latest_manifest))
        origin_rest["authority"]["amendments"] = []
        latest_rest["authority"]["amendments"] = []
        # Guard fields are authority too: they may change only via amend, and
        # amend always appends the operator's verbatim grant. The trustworthy
        # baseline is the chain-protected PREVIOUS checkpoint (the same
        # baseline the append-only check above uses), NOT the origin: an
        # amended mission legitimately diverges from its origin, so a forged
        # tail that reverts guards to the origin spelling -- or rides on an
        # earlier unrelated amendment -- must still read as tampering. A
        # guard difference from the baseline is sanctioned only when the
        # amendments list GREW between baseline and latest. (A forged
        # amendment stays possible on the unsealed tail; that is the es#118
        # residue, disclosed in SECURITY.md, not something this check invents
        # coverage for.)
        baseline_rest = json.loads(json.dumps(baseline))
        baseline_guards = {k: baseline_rest["authority"].pop(k, None)
                           for k in _GUARD_AUTHORITY_KEYS}
        latest_guards = {k: latest_rest["authority"].pop(k, None)
                         for k in _GUARD_AUTHORITY_KEYS}
        for k in _GUARD_AUTHORITY_KEYS:
            origin_rest["authority"].pop(k, None)
        if baseline_guards != latest_guards \
                and len(latest_amendments) <= len(baseline_amendments):
            raise CustodyError(
                "actuator guards changed with no new authority amendment "
                "recorded (tampered)")
        if origin_rest != latest_rest:
            differing = sorted(
                key for key in set(origin_rest) | set(latest_rest)
                if origin_rest.get(key) != latest_rest.get(key))
            raise CustodyError(
                "manifest changed since mission open (tampered): "
                + ", ".join(differing))

    def _write_next(self, latest: dict, latest_path: Path, *, status: str,
                     note: str | None = None, frontier: str | None = None,
                     add_receipt_id: str | dict | None = None,
                     receipt_ids: list[str | dict] | None = None,
                     manifest: dict | None = None,
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
        # Copy-forward must preserve each entry's existing @1/@2 shape exactly
        # -- never normalise it through _receipt_entries, which collapses both
        # shapes into uniform tuples and would silently upgrade an @1 chain to
        # @2 on every write, a migration this refactor must not perform.
        receipt_ids = (list(receipt_ids) if receipt_ids is not None
                       else list(latest["receipt_ids"]))  # ALLOW-RAW-RECEIPT-IDS
        if add_receipt_id is not None:
            receipt_ids.append(add_receipt_id)
        checkpoint = {
            "record": "checkpoint@1",
            "mission_id": latest["mission_id"],
            "revision": latest["revision"] + 1,
            "status": status,
            "prev_checkpoint_sha256": sha256_file(latest_path),
            "manifest": manifest if manifest is not None else latest["manifest"],
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
        retired_kind = self._retired_receipt_ids(latest).get(request_id)
        if retired_kind is not None:
            # Reuse would make one id mean two different artifacts across the
            # record, forcing an auditor to walk revisions to disambiguate.
            # T3-4b: name WHICH kind was retired -- calling a
            # tamper-retirement a 'loss' misdescribes the distinction T3-1
            # made real.
            raise CustodyError(
                f"request_id {request_id!r} was retired by an acknowledged "
                f"receipt {retired_kind} and can never be reused -- use a "
                "fresh id")
        if request_id in set(self._all_receipt_ids_ever()):
            # An id whose receipt file merely vanished is NOT free for reuse
            # either: the chain still remembers what it was minted against,
            # and rebinding it silently backdates the new write to the old
            # event -- which made a legitimate reconciliation read as
            # unreconciled (merge-gate review of #125).
            raise CustodyError(
                f"request_id {request_id!r} is already recorded in this "
                "mission's history and can never be reused -- use a fresh id")
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

    def _load_receipt(self, request_id: str,
                       expected_sha: str | None = None) -> dict | None:
        """None means UNLOADABLE -- absent, corrupt, schema-invalid, or
        id-mismatched. A hash mismatch against a chain-attested sha is a
        DIFFERENT state and is never folded into None: it raises
        _ReceiptTampered instead (caught by resume, which reports
        RECEIPT-TAMPERED, and by acknowledge_receipt_loss's byte-provable
        restoration check -- see both). None already means "unloadable,
        treat as an honest loss", and acknowledge_receipt_loss retires a None
        id on that basis; a tampered receipt returning None would be retired
        the same way, discharging tampering as if nothing had happened. A
        corrupt receipt must still degrade to drift (RECEIPT-MISSING), never
        crash resume: crashing the recovery path on a mangled receipt is a
        denial of service by exactly the tampering drift detection exists to
        catch.

        expected_sha is the LATEST chain attestation for this id (see
        _expected_sha) -- the receipt file's own bytes, hashed, as the chain
        last recorded them. No @1 entry ever carries one, so for a
        pre-attestation id expected_sha is always None and the tamper check
        below never fires; the schema/id-match checks are the fallback for
        those ids, same as before @2 existed."""
        path = self.store.receipt_path(request_id)
        try:
            raw = path.read_bytes()
        except FileNotFoundError:
            return None
        if expected_sha is not None and sha256_bytes(raw) != expected_sha:
            # TAMPERED is distinct from unloadable: the chain attests
            # specific bytes for this id and these are not them -- whether or
            # not they still happen to parse as a well-formed receipt.
            raise _ReceiptTampered(request_id)
        try:
            record = json.loads(raw.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            return None
        if validate_record(record):
            return None
        # A receipt whose own request_id disagrees with the content-addressed
        # name it is stored under is malformed by construction -- never a
        # trustworthy source for a claim about that id.
        if record.get("request_id") != request_id:
            return None
        return record

    def _covered_by_other_id(self, recorded_path: str, excluding: str,
                              entries: list[tuple[str, str | None]],
                              expected_shas: dict[str, str]) -> bool:
        """True iff recorded_path is CURRENTLY covered by a loadable receipt
        belonging to an id OTHER than `excluding`, using resume()'s own
        last-id-wins-by-append-order rule over the FULL `entries` list --
        `excluding` INCLUDED, in its own chronological position (T3-3, fix
        round 1: acknowledge_receipt_loss must not raise a spurious RECOVER
        for a path a surviving id already, genuinely covers).

        Must walk the id's ORIGINAL append order, not merely "does any
        surviving id's receipt happen to load and claim this path": an id
        being retired because it IS the current one for this path (the last
        id covering it) must not be treated as covered just because an
        EARLIER, already-superseded id for the same path still loads. That
        earlier id was already stale ground truth before this retirement --
        crediting it as 'coverage' reintroduces exactly the silent-promotion
        bug test_superseded_receipt_never_shadows_the_current_one guards (a
        lost newest receipt letting a superseded older one stand in for it,
        so resume compares live content against stale ground truth). Only
        an id that comes AFTER `excluding` in append order -- one that had
        ALREADY superseded it before this retirement -- can count; an id
        that comes before, or `excluding` itself, cannot.

        expected_shas MUST be the chain-wide latest attestation per id (see
        _expected_sha_map), NOT each entry's own embedded sha (T3-4a, fix
        round 2): on the @1-tail chain shape -- the only shape _write_next
        can produce today -- every entry in `entries` carries sha=None
        regardless of whether an EARLIER checkpoint attested one. Passing
        that embedded None through to _load_receipt silently skips the
        tamper check inside this walk entirely, and can credit a TAMPERED
        id as 'coverage' -- the exact suppression direction T3-3 exists to
        get right, not merely to exist."""
        current_id: str | None = None
        current_receipt: dict | None = None
        for other_id, _entry_sha in entries:
            try:
                other_receipt = self._load_receipt(
                    other_id, expected_shas.get(other_id))
            except _ReceiptTampered:
                other_receipt = None
            other_rel = (other_receipt["artifact_path"] if other_receipt is not None
                         else self._historical_effect_path(other_id))
            if other_rel is not None and _same_artifact(other_rel, recorded_path):
                current_id, current_receipt = other_id, other_receipt
        return (current_id is not None and current_id != excluding
                and current_receipt is not None)

    def _historical_effect_path(self, request_id: str, kind: bool = False) -> str | None:
        """The artifact path this request id was minted against, read from the
        hash-chained checkpoint history: the effect note appended by the very
        revision that put the id into receipt_ids. A lost receipt's path is
        NOT unknowable -- the chain remembers it, and interior checkpoints are
        tamper-evident, so this is a sounder authority than a receipt file
        anyone able to write the receipts dir could have replaced.
        None when underivable (treated as unprovable, never as agreement).

        With kind=True, returns HOW it was minted instead ('effect' or
        'reconciled') -- the same note that records the path records whether
        the write was an ordinary effect or a reconciliation."""
        prev_ids: list[str] = []
        prev_notes: list[str] = []
        for cp_path in self.store.checkpoint_paths():
            record = json.loads(cp_path.read_text(encoding="utf-8"))
            ids = [rid for rid, _ in self._receipt_entries(record)]
            notes = record["state"]["notes"]
            if request_id in ids and request_id not in prev_ids:
                for note in notes[len(prev_notes):]:
                    for prefix in ("effect: ", "reconciled: "):
                        if note.startswith(prefix):
                            return note[len(prefix):] if not kind \
                                else prefix.rstrip(": ")
                return None
            prev_ids, prev_notes = ids, notes
        return None

    def _all_receipt_ids_ever(self) -> list[str]:
        """Every request id ever admitted to receipt_ids, in the order the
        chain admitted it -- including ids since retired, which the current
        list no longer carries. The chain is the only place the full order
        survives."""
        seen: list[str] = []
        known: set[str] = set()
        for cp_path in self.store.checkpoint_paths():
            record = json.loads(cp_path.read_text(encoding="utf-8"))
            for request_id, _ in self._receipt_entries(record):
                if request_id not in known:
                    known.add(request_id)
                    seen.append(request_id)
        return seen

    def _retired_receipt_ids(self, latest: dict) -> dict[str, str]:
        """Ids whose loss OR tamper was acknowledged, mapped to WHICH
        ('loss' or 'tamper') -- unioning both note prefixes into one
        lookup. Retirement is permanent and lives in the append-only notes
        (checkpoint state is exact-field-closed in @1, so a retired_ids
        field would break the schema), so a retired id can never be
        silently recycled for a different artifact once the file that once
        occupied its path is gone. Permanent non-reusability is correct
        either way: a tampered id that could not be byte-provably restored
        is exactly as untrustworthy to recycle as a lost one (T3-1).

        A dict, not a set: every existing `in` check against this method's
        result still answers identically (membership tests a dict's keys),
        but the reuse-refusal message can now name WHICH kind was retired
        (T3-4b, fix round 2) -- a message that calls a tamper-retirement a
        'loss' misdescribes exactly the distinction T3-1 made real."""
        retired: dict[str, str] = {}
        decoder = json.JSONDecoder()
        for note in latest["state"]["notes"]:
            for prefix, kind in ((_RETIRED_NOTE, "loss"),
                                  (_RETIRED_TAMPERED_NOTE, "tamper")):
                if not note.startswith(prefix):
                    continue
                # The id is JSON-encoded, so it is read back exactly
                # regardless of what it contains. Splitting on a delimiter
                # truncated any id holding that delimiter, and a truncated id
                # compared unequal to the real one -- silently un-retiring it
                # (merge-gate round 4).
                try:
                    value, _ = decoder.raw_decode(note[len(prefix):])
                except ValueError:
                    continue
                if isinstance(value, str):
                    retired[value] = kind
                break
        return retired

    def _receipt_entries(self, checkpoint: dict) -> list[tuple[str, str | None]]:
        """(request_id, receipt_sha256|None) for one checkpoint, @1 or @2.

        THE single reader of receipt_ids. @1 entries are bare strings and carry
        no sha; @2 entries are objects. Every consumer goes through here,
        because a string-vs-dict comparison never matches and never raises --
        it silently reports nothing, which is the false-clean direction."""
        entries: list[tuple[str, str | None]] = []
        for entry in checkpoint["receipt_ids"]:  # ALLOW-RAW-RECEIPT-IDS
            if isinstance(entry, str):
                entries.append((entry, None))
            else:
                entries.append((entry["request_id"], entry.get("receipt_sha256")))
        return entries

    def _expected_sha_map(self) -> dict[str, str]:
        """The LATEST chain attestation for EVERY id, in a single chain pass.

        The data _expected_sha(id) answers per id, computed once for the
        whole chain instead of once per id: a caller resolving many ids (e.g.
        resume() over every receipt) must not re-read and re-parse every
        checkpoint file per id -- that is O(ids x checkpoints), and it grows
        unusably on a long-lived mission (measured: read_text calls 124 ->
        3844 going from 30 to 60 receipts). Same latest-wins rule as
        _expected_sha; the two must stay in sync, which is why _expected_sha
        delegates to this rather than duplicating the walk."""
        latest: dict[str, str] = {}
        for cp_path in self.store.checkpoint_paths():
            record = json.loads(cp_path.read_text(encoding="utf-8"))
            for rid, sha in self._receipt_entries(record):
                if sha is not None:
                    latest[rid] = sha
        return latest

    def _expected_sha(self, request_id: str) -> str | None:
        """The LATEST chain attestation for this id, not the first.

        A pre-migration id appears with sha None in @1 records and with a
        backfilled sha from the migration checkpoint onward. Taking the first
        occurrence would discard the backfill and verify at @1 strength while
        the record claims otherwise -- a silent downgrade.

        Single-id convenience wrapper over _expected_sha_map; a caller
        resolving many ids in one call (resume()) should use the map
        directly instead of calling this in a loop -- see its docstring."""
        return self._expected_sha_map().get(request_id)

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

    def amend_authority(self, text: str, *, guard_mode=_UNSET,
                        actuator_guards=_UNSET) -> int:
        """Record a VERBATIM operator grant that changes the mission's
        authority, appended to authority.amendments.

        The tracer mission stalled at exactly this point -- its operator's
        answer exceeded the recorded instruction, and the steward could only
        escalate and stop, because the schema had an amendments list that no
        method or CLI surface could ever write. Authority that can only be
        set at open time forces a false choice between acting outside the
        envelope and abandoning the mission.

        This records authority; it does not grant it. Like the opening
        instruction, the text is the operator's words carried verbatim, and
        the contract cannot verify the operator said them -- that is the
        runtime boundary's job. What it does guarantee is that the grant is
        durable, timestamped, hash-chained, and append-only: once recorded,
        an amendment can never be rewritten or quietly dropped."""
        latest, path = self.store.load_latest()
        self._verify_manifest(latest)
        if latest["status"] not in _OPEN_STATES:
            raise IllegalTransition(
                f"cannot amend_authority: status is {latest['status']!r}")
        if not isinstance(text, str) or not text.strip():
            raise CustodyError("amendment text required (verbatim operator grant)")
        manifest = json.loads(json.dumps(latest["manifest"]))
        manifest["authority"]["amendments"].append(
            {"utc": now_utc(), "text": text})
        if actuator_guards is not _UNSET:
            # None clears the field (the key is removed, not nulled -- the
            # schema has no nullable guard fields); a [] "clear" is refused
            # by validation (minItems: 1), so clearing MUST go through None.
            if actuator_guards is None:
                manifest["authority"].pop("actuator_guards", None)
            else:
                manifest["authority"]["actuator_guards"] = actuator_guards
        if guard_mode is not _UNSET:
            if guard_mode is None:
                manifest["authority"].pop("guard_mode", None)
            else:
                manifest["authority"]["guard_mode"] = guard_mode
        new = self._write_next(latest, path, status=latest["status"],
                                manifest=manifest,
                                note=f"authority amended: {text}")
        return new["revision"]

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

    def continuity_breaks(self) -> list[dict]:
        """Where an artifact changed between two receipted events without a
        receipted event of its own.

        Each receipt records the artifact's hash BEFORE its write and AFTER.
        Chained per path those must meet: receipt[n].before_sha256 ==
        receipt[n-1].after_sha256. A gap is positive evidence of unreceipted
        mutation -- including the one case drift detection structurally
        cannot see, where a steward re-effects over a file it never resumed
        against, so the current receipt truthfully describes content nobody
        ever sanctioned. The evidence was always in the receipts; nothing
        read it.

        Read-only, and it raises NOTHING. A break is history: it cannot be
        discharged, so making it an obligation would create a marker with no
        exit -- the wedge RECOVER-UNKNOWN was rejected for. Surfaced, not
        enforced.

        Visibility is asymmetric and SECURITY.md names it: a break whose far
        receipt was superseded AND then deleted is invisible here, because
        nothing may be asserted across a receipt that cannot be loaded.
        Bridging the gap instead would fabricate breaks on honest histories
        where an intervening write legitimately changed the content."""
        # Order comes from the CHAIN, not from the current receipt_ids list.
        # Retirement removes a lost id from that list, so zipping survivors
        # would compare two receipts that were never adjacent -- inventing a
        # break across the gap where the retired one honestly sat. That fires
        # on the ordinary sanctioned recovery flow, which would train stewards
        # to ignore the signal on day one.
        by_path: dict[str, list[str]] = {}
        for request_id in self._all_receipt_ids_ever():
            receipt = self._load_receipt(request_id)
            rel = (receipt["artifact_path"] if receipt is not None
                   else self._historical_effect_path(request_id))
            if rel is None:
                continue
            key = _normalize_relpath(rel)
            if os.name == "nt":
                key = _ascii_case_fold(key)
            by_path.setdefault(key, []).append(request_id)
        breaks: list[dict] = []
        for ids in by_path.values():
            for prior_id, next_id in zip(ids, ids[1:]):
                prior = self._load_receipt(prior_id)
                nxt = self._load_receipt(next_id)
                if prior is None or nxt is None:
                    # A gap we cannot read is not evidence of a break. The
                    # missing receipt is already reported by resume as its own
                    # finding; claiming a mismatch across it would be asserting
                    # something this data cannot support.
                    continue
                if nxt["before_sha256"] == prior["after_sha256"]:
                    continue
                # A reconciliation FOLLOWS a mutation that drift detection
                # already caught and the steward already answered for. The
                # break is real either way, but only an unreconciled one is
                # news -- that is the case nothing else in the contract sees.
                reconciled = self._historical_effect_path(
                    nxt["request_id"], kind=True) == "reconciled"
                breaks.append({
                    "artifact_path": nxt["artifact_path"],
                    "prior_request_id": prior["request_id"],
                    "request_id": nxt["request_id"],
                    "expected_before_sha256": prior["after_sha256"],
                    "observed_before_sha256": nxt["before_sha256"],
                    "no_op_write": nxt["before_sha256"] == nxt["after_sha256"],
                    "already_reconciled": reconciled,
                })
        breaks.sort(key=lambda b: (b["artifact_path"], b["request_id"]))
        return breaks

    def resume(self) -> list[str]:
        latest, path = self.store.load_latest()
        self._verify_manifest(latest)
        if latest["status"] in ("completed", "cancelled"):
            raise IllegalTransition(f"cannot resume: status is {latest['status']!r}")
        # One artifact, one current receipt: receipt_ids is append-ordered, so
        # the LAST id covering a path supersedes the earlier ones. Attribution
        # must not depend on the receipt being loadable, or a lost newest
        # receipt would let a superseded older one silently become the
        # authority again -- comparing live content against stale ground truth
        # and reporting a mismatch that never happened, while the real loss of
        # the current receipt went unreported.
        current_by_key: dict[str, tuple[str, dict | None]] = {}
        missing: list[str] = []
        tampered: list[str] = []
        # One chain pass for every id's attestation, not one pass per id
        # (_expected_sha_map's docstring has the measured blow-up).
        expected_shas = self._expected_sha_map()
        for request_id, _ in self._receipt_entries(latest):
            try:
                receipt = self._load_receipt(request_id, expected_shas.get(request_id))
            except _ReceiptTampered:
                # Reported unconditionally, per id -- deliberately NOT routed
                # through the "one artifact, one current receipt" supersession
                # logic below. A later id superseding this one's path does
                # not un-happen a proven tamper on this one; silence here
                # would be the exact false-clean this check exists to catch.
                if request_id not in tampered:
                    tampered.append(request_id)
                continue
            rel = (receipt["artifact_path"] if receipt is not None
                   else self._historical_effect_path(request_id))
            if rel is None:
                # Unloadable AND unattributable: it can only be reported as
                # the lost receipt it is (see _historical_effect_path).
                if request_id not in missing:
                    missing.append(request_id)
                continue
            # Case-insensitive filesystems: Doc.md and doc.md are one
            # artifact; keying case-sensitively splits them and reports
            # spurious drift on the superseded casing. Folded ASCII-only --
            # str.casefold() would map two genuinely distinct files onto one
            # key here, and the loser would vanish from the drift check
            # entirely (see _ascii_case_fold).
            key = _normalize_relpath(rel)
            if os.name == "nt":
                key = _ascii_case_fold(key)
            current_by_key[key] = (request_id, receipt)
        mismatched: list[str] = []
        for request_id, receipt in current_by_key.values():
            if receipt is None:
                # An unloadable receipt is drift, not a skip: the artifact it
                # covered can no longer be verified, and silence here is a
                # false "clean" for exactly the file most likely tampered.
                if request_id not in missing:
                    missing.append(request_id)
                continue
            rel = receipt["artifact_path"]
            target = self.workspace / rel
            actual = sha256_file(target) if target.exists() else None
            if actual != receipt["after_sha256"]:
                mismatched.append(rel)
        mismatched.sort()
        missing.sort()
        tampered.sort()
        findings = (mismatched + [f"RECEIPT-MISSING:{rid}" for rid in missing]
                    + [f"RECEIPT-TAMPERED:{rid}" for rid in tampered])
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
        for rid in tampered:
            marker = f"RECEIPT-TAMPERED:{rid}"
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
        existing_ids = {rid for rid, _ in self._receipt_entries(latest)}
        add_id = request_id if request_id not in existing_ids else None
        self._write_next(latest, path, status=next_status, add_receipt_id=add_id,
                          unresolved_verdicts=remaining,
                          note=f"reconciled: {artifact_relpath}")
        return receipt

    def acknowledge_receipt_loss(self, request_id: str) -> int:
        """The only exit for a RECEIPT-MISSING or RECEIPT-TAMPERED marker. It
        never writes an artifact and never deletes a file, and it never
        asserts continuity it has not proven: a receipt found at the id's
        path counts as RESTORED only if it is proven to be the original.

        When the chain attests a receipt_sha256 for this id, that proof is
        byte-provable: the file at the id's path hashing to EXACTLY the
        chained sha IS the original, no further check needed -- strictly
        stronger than comparing paths, which only proves two claims agree
        with each other, never that either is genuine. For a pre-attestation
        id (expected_sha is None), the only available proof is @1's path-match
        heuristic: the receipt loads, and agrees with the chained history (its
        own request_id, and the artifact path the id was originally minted
        against) -- kept as the fallback, not the primary check, now that a
        stronger one exists. A receipt that disagrees is a different receipt
        wearing the id's name -- trusting its schema-validity alone let a
        forged path silently replace real coverage while the mission read
        clean (merge-gate round 3). Anything unproven retires the id with the
        loss (or tamper) recorded permanently; ongoing coverage then requires
        a FRESH effect, minted as a new event."""
        latest, path = self.store.load_latest()
        self._verify_manifest(latest)
        if latest["status"] != "reopened":
            raise IllegalTransition(
                f"cannot acknowledge_receipt_loss: status is "
                f"{latest['status']!r}, expected 'reopened'")
        missing_marker = f"RECEIPT-MISSING:{request_id}"
        tampered_marker = f"RECEIPT-TAMPERED:{request_id}"
        unresolved = latest["state"]["unresolved_verdicts"]
        if missing_marker in unresolved:
            marker = missing_marker
        elif tampered_marker in unresolved:
            marker = tampered_marker
        else:
            raise CustodyError(
                f"no receipt-loss or receipt-tamper marker for {request_id!r}")
        remaining = [m for m in unresolved if m != marker]
        next_status = "active" if not remaining else "reopened"

        expected_sha = self._expected_sha(request_id)
        still_tampered = False
        try:
            receipt = self._load_receipt(request_id, expected_sha)
        except _ReceiptTampered:
            # Still not the chain-attested bytes -- not restored, whatever
            # marker brought us here.
            receipt = None
            still_tampered = True
        recorded_path = self._historical_effect_path(request_id)
        if expected_sha is not None:
            # A chained sha makes RESTORED byte-provable: _load_receipt only
            # returns non-None here when the file's bytes hashed to EXACTLY
            # what the chain last attested. That already IS the original --
            # a path comparison on top would only weaken the claim.
            restored = receipt is not None
        else:
            # Deliberately raw equality, NOT _same_artifact: everywhere else
            # the question is "does this write satisfy that obligation",
            # where two spellings of one file must match. Here the question
            # is "is this the receipt the chain recorded", and a receipt that
            # reappears respelled is not provably the original -- the safe
            # answer is to retire the id and let a fresh effect re-establish
            # coverage honestly. Strictness here is intentional, not an
            # oversight.
            restored = (receipt is not None and recorded_path is not None
                        and receipt["artifact_path"] == recorded_path)
        if restored:
            effect_path = recorded_path if recorded_path is not None \
                else receipt["artifact_path"]
            new = self._write_next(
                latest, path, status=next_status, unresolved_verdicts=remaining,
                note=(f"receipt restored: {request_id}; matches the recorded "
                      f"effect on {effect_path}; coverage continues"))
            return new["revision"]

        covered = (f" (covered {json.dumps(recorded_path)})"
                   if recorded_path else "")
        if still_tampered:
            why = "receipt present but its bytes do not match the chain-attested hash"
        elif receipt is None:
            why = "receipt unloadable"
        elif recorded_path is None:
            why = "no recorded effect in the chain to check the receipt against"
        else:
            why = (f"present receipt claims {receipt['artifact_path']!r}, "
                   f"chain records {recorded_path!r} -- NOT trusted")
        # Filter by NORMALISED id (rid) while keeping the RAW entry (entry) in
        # the output -- shape must survive the filter unchanged, same reason
        # _write_next's copy-forward does not route through _receipt_entries.
        receipt_ids = [
            entry for entry, (rid, _)
            in zip(latest["receipt_ids"], self._receipt_entries(latest))  # ALLOW-RAW-RECEIPT-IDS
            if rid != request_id
        ]
        # T3-3: recorded_path may already be covered by a DIFFERENT id that
        # had ALREADY superseded request_id before this retirement (e.g. a
        # fresh effect re-covered it after request_id was tampered) --
        # retiring request_id then does not leave the artifact uncovered.
        # Walks the FULL pre-retirement entries (latest, not the filtered
        # receipt_ids local) so append order -- and request_id's own
        # chronological position in it -- is preserved; see
        # _covered_by_other_id for why that ordering is load-bearing, and
        # for why it needs the chain-wide _expected_sha_map (T3-4a), not
        # each entry's own embedded sha.
        if recorded_path is not None and not self._covered_by_other_id(
                recorded_path, request_id, self._receipt_entries(latest),
                self._expected_sha_map()):
            # Losing coverage is an OBLIGATION, not a footnote: the mission
            # stays reopened, naming the artifact that must be re-covered, so
            # an uncovered artifact can never sit quietly in an active
            # mission just because its receipt was destroyed.
            if _find_marker(remaining, "RECOVER:", recorded_path) is None:
                remaining = remaining + [f"RECOVER:{recorded_path}"]
            next_status = "reopened"
        # T3-4e (fix round 4): tamper-taint is monotone ALONG THE FILE AXIS --
        # a recorded tamper for this id is never downgraded by the later
        # ABSENCE or UNPARSEABILITY of the file. Those are the two ways the
        # live re-check can go quiet without anything having been cleared,
        # and both arrive here with the marker still open, so both are a
        # tamper.
        #
        # Read that scope literally; it is not shorthand for a general
        # guarantee, and widening it would assert a property this system does
        # NOT have. Monotonicity does not hold along the ATTESTATION axis:
        # with a RECEIPT-TAMPERED marker open, appending an @2 checkpoint
        # that attests the FORGED bytes retires the id as "receipt restored
        # ... coverage continues" -- no prefix at all, id kept, unresolved
        # empty, status active. No rule written HERE can reach that; it
        # returns from the `restored` branch before a prefix is ever chosen.
        # That is the unsealed-tail residue, owned by the tail-anchor task,
        # and it is left KNOWN-UNCOVERED here rather than papered over. What
        # this line guarantees is narrow and worth stating exactly: nobody
        # launders a recorded tamper by deleting or mangling the receipt.
        # Someone who can append to the chain still can.
        #
        # (Round 3's comment asserted the unqualified version -- "everything
        # else ... is loss-shaped" -- and that sentence is what produced the
        # defect this round fixes. An over-wide guarantee in a comment is a
        # false one handed to the next reader.)
        #
        # Both limbs are load-bearing; each was confirmed necessary by
        # deleting it and re-running the discharge case table:
        #
        #   still_tampered -- the file is present RIGHT NOW and its bytes
        #     fail the chain-attested hash. The only limb that fires when
        #     live evidence proves a tamper the chain never recorded a
        #     marker for: a forged receipt placed back under an already-open
        #     RECEIPT-MISSING, with no intervening resume to raise
        #     RECEIPT-TAMPERED. Membership alone reports that as a loss.
        #     Note this limb also covers UNPARSEABLE-but-attested bytes,
        #     because _load_receipt hashes the RAW bytes BEFORE parsing --
        #     corrupt bytes raise _ReceiptTampered rather than returning the
        #     unloadable None. That ordering is load-bearing and pinned by a
        #     test; membership holds the row at 'tamper' even if it changes.
        #
        #   tampered_marker in unresolved -- the chain DID record a tamper
        #     for this id and it is still undischarged. The only limb that
        #     fires once the file is gone: deleting the forged receipt after
        #     being caught makes still_tampered False, so keying the prefix
        #     on live evidence alone let one extra step (get caught, delete
        #     the receipt) retire a proven tamper under the honest-'loss'
        #     prefix -- fix round 3's defect, and the reason this is not
        #     `still_tampered` alone.
        #
        # MEMBERSHIP, not `marker == tampered_marker`: in the double-marker
        # window (both RECEIPT-MISSING and RECEIPT-TAMPERED open for one id)
        # MISSING wins the priority selection above, so the marker being
        # discharged is not the tampered one even though the chain holds an
        # undischarged RECEIPT-TAMPERED for that id. Equality reports which
        # marker the discharge order happened to pick; membership reports
        # what the chain recorded, which is what the prefix is FOR.
        #
        # `unresolved` is the pre-filter list of WHOLE markers, so `in` is
        # exact element equality -- an id that is a substring of another id
        # cannot bleed a tamper across ids. It must stay a list, not be
        # joined into a string, for that to hold.
        retired_note = (_RETIRED_TAMPERED_NOTE
                        if still_tampered or tampered_marker in unresolved
                        else _RETIRED_NOTE)
        new = self._write_next(
            latest, path, status=next_status, unresolved_verdicts=remaining,
            receipt_ids=receipt_ids,
            note=(f"{retired_note}{json.dumps(request_id)}{covered}; {why}; "
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
            "receipt_refs": [rid for rid, _ in self._receipt_entries(latest)],
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
