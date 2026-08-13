#!/usr/bin/env python3
"""Mission lifecycle: draft -> active -> verifying -> completed, with drift
reanchoring on resume and a clearable FAIL path (no PA reject dead-end)."""
from __future__ import annotations

import json
import os
import re
import sys
import unicodedata
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
# Notes are the mission's append-only, hash-chained narrative AND the carrier
# for retirement (checkpoint state is exact-field-closed in @1, so a
# retired_ids field would break the schema). Machine-written notes therefore
# own these prefixes exclusively: a caller-supplied note that could imitate
# one would let ordinary narrative forge machine state.
_RESERVED_NOTE_PREFIXES = (
    "effect: ", "reconciled: ", "drift detected: ", "receipt restored: ",
    "authority amended: ", _RETIRED_NOTE, "scope-ack by ",
)


def _refuse_reserved_note(text: str) -> None:
    """Refuse caller text that imitates a machine-written note ON ANY LINE.

    The first version checked `text.startswith(prefix)` on the whole string,
    case-sensitively. Four ways past it, each verified: a leading space, a
    capital, a leading newline, and -- the load-bearing one -- an ordinary
    multi-line note whose SECOND line is a byte-identical machine note. The
    guard only inspected the start of the string, so a note reading
    "session note
scope-ack by agent:acceptor: secrets.env" passed.

    That never bypassed a gate (the acceptance gate reads `scope_ack`, never
    notes). What it defeated is the AUDIT property those prefixes exist for: an
    auditor grepping the chain for who took responsibility could not tell a
    genuine acknowledgement from steward narrative.

    Applied to every surface that embeds caller text into a note -- `note`,
    `amend`, `cancel` and verdict reasons -- because the composed note is
    machine-written but the text inside it is not."""
    for line in (text or "").splitlines() or [text or ""]:
        # Invisible characters are neither whitespace nor line separators, so
        # strip()/splitlines() do not see them while a reader sees nothing:
        # ZWSP, BOM, LRM, WORD JOINER and SOFT HYPHEN each walked past the
        # guard, producing a stored note that renders IDENTICALLY to a genuine
        # acknowledgement. NFKC + dropping category Cf closes that class in one
        # place, and only for the COMPARISON -- the text is stored verbatim.
        #
        # Homoglyphs (Cyrillic 'a' in "scope-ack") are deliberately NOT chased
        # here. Confusables are unbounded, and enumerating them would be the
        # denial-marker mistake in a new location. The structural fix is
        # `scope_ack` as a validated field on the acceptance-verdict record
        # (es#150 / contract@2 Task 9), which retires string matching entirely.
        flat = "".join(c for c in unicodedata.normalize("NFKC", line)
                       if unicodedata.category(c) != "Cf")
        candidate = flat.strip().casefold()
        for prefix in _RESERVED_NOTE_PREFIXES:
            if candidate.startswith(prefix.casefold()):
                raise CustodyError(
                    f"text may not contain a line beginning with {prefix!r}: "
                    "machine-written notes carry mission state and narrative "
                    "must not be able to imitate them, on any line")


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


def _is_path_pattern(entry: str) -> bool:
    """Is this scope entry a PATH pattern, or prose?

    `scope` has always been free text, and real manifests declare boundaries in
    English -- the bundled examples carry entries like
    "monitored-missing reconciliation" and "indexer changes". Treating those as
    globs would classify every ordinary receipt as out-of-scope and refuse a
    legitimate PASS on every mission with a populated prose scope: a silent
    compatibility break dressed as a security check.

    So only entries that LOOK like path patterns take part in the comparison; a
    prose declaration remains exactly what it always was -- advisory text a
    human reads.

    Whitespace and commas are the first discriminator, because real
    declarations read like sentences -- "media acquisition, arr/Plex/NAS
    operations" contains slashes and is unmistakably prose, and it appeared in
    a real manifest written during this very change.

    The first version of this predicate stopped there, and required a slash or
    a wildcard. That silently discarded `scope.out=["secrets.env"]` -- a bare
    filename, the most natural exclusion an operator can write -- so the
    comparison ran with an empty exclude list and PASS succeeded after writing
    the one file the mission was told not to touch.

    The asymmetry argument that justified "anything ambiguous is prose" was
    reasoned about scope.IN only, where an over-eager pattern matches nothing
    and wedges an honest close. It does not carry to scope.OUT, where dropping
    an entry is the FALSE-CLEAN direction: the boundary reads as enforced and
    compares nothing. Same predicate, opposite error costs.

    The case table this is written against -- the enumeration is the spec:

      docs/**, src/*.py, *.env        pattern (glob)
      secrets.env, README.md          pattern (bare filename + extension)
      .env, .gitignore                pattern (dotfile)
      reconciliation                  prose  (single bare word, no extension)
      monitored-missing reconc...     prose  (whitespace)
      media acquisition, arr/Plex     prose  (comma + whitespace)
      "" (empty)                      prose

    A single bare word with no extension stays prose: `notes` could be a
    directory or a noun, and nothing in the string decides which. That residue
    is real and is not silently absorbed -- `uncompared_scope_entries` reports
    every entry this predicate declines, so an operator sees which of their
    declarations no machine is checking instead of assuming all of them are."""
    if not entry or "," in entry:
        return False
    if any(c.isspace() for c in entry):
        # A SPACE ALONE NO LONGER MEANS PROSE. Testing whitespace before the
        # slash test made every path containing a space invisible:
        # "My Documents/secrets.env" and "docs/release notes/**" were dropped
        # from the comparison entirely, so PASS succeeded after writing them.
        #
        # A spaced entry is a path only when it both contains a separator and
        # ENDS like a path -- a wildcard, a trailing slash, or a final segment
        # with an extension. That keeps real prose out: "TCP/IP tuning" and
        # "arr/Plex/NAS operations" carry slashes but end in a bare word, and
        # "What now?" has no separator at all.
        if "/" not in entry:
            return False
        last = entry.rstrip("/").rpartition("/")[2]
        if entry.endswith("/") or "*" in entry or "?" in entry:
            return True
        stem, dot, ext = last.rpartition(".")
        return bool(stem) and bool(dot) and ext.isalnum()
    if "/" in entry or "*" in entry or "?" in entry or entry.endswith("\\"):
        return True
    name = entry[1:] if entry.startswith(".") else entry
    stem, dot, ext = name.rpartition(".")
    if entry.startswith(".") and not dot:
        return bool(name) and name.isalnum()      # .env, .gitignore
    return bool(stem) and bool(dot) and ext.isalnum()


def _names_a_specific_path(token: str) -> bool:
    """Does this token name SOMETHING, rather than everything?

    `_is_path_pattern` accepts `*` and `**`, which is right for a scope
    declaration (an operator may legitimately exclude everything) and
    catastrophic for a discharge token: `_glob_regex("*")` is `[^/]*$` and
    `_glob_regex("**")` is `.*$`, so a bare wildcard in an amendment matches
    every drifted artifact.

    That is not a hypothetical shape. `amend` carries the operator's words
    VERBATIM, and a multi-part grant is most naturally written as a markdown
    bullet list -- whose bullets are bare `*` tokens. A genuine, unrelated
    two-line grant was demonstrated discharging an out-of-scope write to
    `secrets.env`, with no surface anywhere reporting that the key was `*`.

    So a discharge token must retain at least one literal character after its
    wildcards and separators are removed."""
    return bool(token.strip("*?/\\"))


def _is_matchable_pattern(entry: str) -> bool:
    """Can this pattern EVER match a workspace-relative receipt path?

    `_is_path_pattern` decides whether an entry looks like a path. It does not
    ask whether the compiler can do anything with it, and `custody_gate.
    _glob_regex` implements only `*`, `**` and `?` -- everything else is
    `re.escape`d into a literal. So entries that classify as patterns can
    compile to regexes that match NOTHING, verified against the live compiler:

        !secrets/**     negation is not a syntax this compiler has
        /etc/passwd     absolute; receipts are workspace-relative
        ~/.ssh/id_rsa   home-relative, same reason
        C:/Windows      drive-absolute
        docs/[abc].md   character classes are escaped literals

    That is WORSE than being called prose, and the difference is disclosure. A
    prose entry is reported by `uncompared_scope_entries`, so an operator can
    see their boundary is not machine-checked. An unmatchable PATTERN is
    reported nowhere: the declaration reads as enforced, compares nothing, and
    says nothing. Silent-inert instead of disclosed-inert.

    Demoting these to uncompared does not weaken any comparison -- they were
    already matching nothing -- it only makes the nothing visible. Where a real
    file could plausibly bear such a name (`[Mm]akefile` is a legal filename),
    disclosure is still the safe direction: the operator is told, rather than
    believing in an exclusion that never fires."""
    norm = (entry or "").replace("\\", "/")
    if norm.startswith(("/", "~", "!")):
        return False
    if re.match(r"^[A-Za-z]:", norm):
        return False
    return not any(c in norm for c in "{}[]")


def _is_compared_entry(entry: str) -> bool:
    """The single question both the comparison and the disclosure must ask, so
    they cannot drift apart and report different sets."""
    return _is_path_pattern(entry) and _is_matchable_pattern(entry)


def uncompared_scope_entries(manifest: dict) -> dict:
    """Scope entries that `_is_path_pattern` declines, per direction.

    An unenforced boundary the reader believes is enforced is this estate's
    keystone failure. The comparison silently ignoring half a declaration is
    that failure in miniature, so the ignored half gets a surface."""
    scope = manifest["scope"]
    uncompared = {direction: [e for e in scope[direction]
                              if not _is_compared_entry(e)]
                  for direction in ("in", "out")}
    # One prose entry disables the scope.in comparison ENTIRELY -- "outside
    # scope.in" is an absence inference and is unsound on a partial include
    # set. Listing only the prose entry let a reader conclude the OTHER entries
    # were compared. They were not; nothing was.
    uncompared["in_comparison_disabled"] = bool(uncompared["in"])
    return uncompared


_TOKEN_TRIM = "\"'`,;:()[]{}<>"

def _amendment_names(text: str, rel_path: str) -> bool:
    """Does this amendment MENTION `rel_path`? A hint for the acceptor.

    This was a gate and is now a hint, which is the honest reading of what a
    substring test can establish. It says the operator's text mentions a path.
    It cannot say the operator granted it -- "secrets.env remains forbidden"
    mentions secrets.env and authorises nothing. Discharge now requires an
    explicit acceptor acknowledgement (`scope_ack`); this only tells the
    acceptor WHERE TO LOOK.

    Token-wise, never as a raw substring: a substring test would let an
    amendment mentioning `data.py` discharge drift on `a.py`, which is the
    false-ALLOW direction. Operator prose is data here, never a pattern
    language -- only tokens that already pass `_is_path_pattern` are compiled,
    and they go through the same `_glob_regex` the scope entries use."""
    from custody_gate import _glob_regex, _norm_path
    target = _norm_path(rel_path)
    for segment in text.replace("\\", "/").splitlines():
        for raw in segment.split():
            token = raw.strip(_TOKEN_TRIM).rstrip(".")
            if not token or not _is_path_pattern(token):
                continue
            if not _names_a_specific_path(token):
                continue      # a bare wildcard names everything: not a name
            if token.endswith("/"):
                # "the src/ work was authorized" grants a DIRECTORY, and
                # operators write it that way. A trailing slash covers what is
                # under it -- still a scoped grant naming a specific subtree,
                # not a universal key, which is the property that matters here.
                prefix = _norm_path(token.rstrip("/"))
                if prefix and (target == prefix
                               or target.startswith(prefix + "/")):
                    return True
                continue
            if _glob_regex(_norm_path(token)).match(target):
                return True
    return False


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
                     add_receipt_id: str | None = None,
                     receipt_ids: list[str] | None = None,
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
        if request_id in self._retired_receipt_ids(latest):
            # Reuse would make one id mean two different artifacts across the
            # record, forcing an auditor to walk revisions to disambiguate.
            raise CustodyError(
                f"request_id {request_id!r} was retired by an acknowledged "
                "receipt loss and can never be reused -- use a fresh id")
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
            ids = record["receipt_ids"]
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
            for request_id in record["receipt_ids"]:
                if request_id not in known:
                    known.add(request_id)
                    seen.append(request_id)
        return seen

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
        _refuse_reserved_note(text)
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
        _refuse_reserved_note(text)
        new = self._write_next(latest, path, status=latest["status"], note=text)
        return new["revision"]

    def set_frontier(self, text: str) -> int:
        latest, path = self.store.load_latest()
        self._verify_manifest(latest)
        if latest["status"] not in _OPEN_STATES:
            raise IllegalTransition(f"cannot set_frontier: status is {latest['status']!r}")
        # A frontier is not a note, so it forges no note -- but it is displayed
        # by `status`/`resume` and lives in the same checkpoint JSON, so an
        # auditor grepping the chain for a machine-note prefix hits it just the
        # same. Same guard, same reason.
        _refuse_reserved_note(text)
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
        for request_id in latest["receipt_ids"]:
            receipt = self._load_receipt(request_id)
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
        # Deliberately raw equality, NOT _same_artifact: everywhere else the
        # question is "does this write satisfy that obligation", where two
        # spellings of one file must match. Here the question is "is this the
        # receipt the chain recorded", and a receipt that reappears respelled
        # is not provably the original -- the safe answer is to retire the id
        # and let a fresh effect re-establish coverage honestly. Strictness
        # here is intentional, not an oversight.
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

    def _resolved_relpath(self, rel: str) -> str | None:
        """Where `rel` actually lands inside the workspace, or None.

        None covers every case where the question has no answer right now: the
        artifact is gone, the link dangles, the target escapes the workspace,
        or the filesystem refuses. None never weakens the comparison -- the
        lexical path is still tested -- so an unresolvable path is simply not
        an extra chance to catch an escape."""
        from custody_gate import _norm_path
        try:
            target = (self.workspace / rel).resolve()
            return _norm_path(str(target.relative_to(self.workspace.resolve())))
        except (OSError, ValueError, RuntimeError):
            return None

    def scope_consistency(self) -> list[dict]:
        """Receipted artifacts falling OUTSIDE declared scope.in, or INSIDE
        scope.out. Read-only; raises nothing.

        This is the one machine job `scope` earns, and the placement is the
        whole point. Teeth on the ACTION would be prevention, and prevention
        was never available: the measured contamination was mostly `note` text
        (which no path predicate ranges over) plus work whose cwd sat in a
        different repo, where the gate is structurally inert. A mint-time
        refusal would also have fired during a stretch when the work was
        operator-AUTHORIZED but the `amend` verb did not yet exist -- a block
        with no legal discharge, the RECOVER-UNKNOWN wedge already rejected.

        Teeth on the CLAIM is different. It refuses only the assertion that the
        chain is clean, never the work: every artifact already exists when this
        runs, so it cannot wedge. And unlike a guard, the actor it constrains
        cannot disarm it -- `scope` sits inside the manifest tamper-compare and
        is NOT one of _GUARD_AUTHORITY_KEYS, so it cannot be amended away the
        way `amend --guard-mode audit` retires a guard.

        An empty scope declares nothing and flags nothing: unbounded, exactly
        as an empty envelope field means everywhere else."""
        from custody_gate import _glob_regex, _norm_path
        latest, _ = self.store.load_latest()
        scope = latest["manifest"]["scope"]
        includes = [_glob_regex(_norm_path(g)) for g in scope["in"]
                    if _is_compared_entry(g)]
        excludes = [_glob_regex(_norm_path(g)) for g in scope["out"]
                    if _is_compared_entry(g)]
        # "outside scope.in" is an ABSENCE inference: it concludes from a
        # receipt matching NO include that it is out of bounds. That is only
        # sound when the whole include set is comparable. With a mixed
        # declaration -- one path pattern plus a prose entry -- the prose is
        # dropped, `includes` is non-empty, and every artifact the prose
        # covered is reported outside a boundary that in fact permits it,
        # wedging an honest close.
        #
        # "matches scope.out" is a PRESENCE inference: one pattern matching is
        # positive evidence on its own, so a partially-prose exclusion list
        # still contributes everything it can. Same data, opposite soundness
        # conditions -- which is why only one side is gated here.
        if any(not _is_compared_entry(g) for g in scope["in"]):
            includes = []
        if not includes and not excludes:
            return []
        findings: list[dict] = []
        for request_id in self._all_receipt_ids_ever():
            # The CHAINED effect note, not the receipt file, decides which
            # artifact an id covers. A receipt is a mutable file: a schema-valid
            # replacement keeping the same request_id but claiming a different
            # artifact_path would move an out-of-scope write into scope and let
            # PASS through. The chain is tamper-evident and is already treated
            # as the sounder authority everywhere else in this module.
            rel = self._historical_effect_path(request_id)
            if rel is None:
                receipt = self._load_receipt(request_id)
                rel = receipt["artifact_path"] if receipt is not None else None
            if rel is None:
                continue
            target = _norm_path(rel)
            # An EXCLUSION is also tested against where the path actually
            # lands. With scope.out=["secrets/**"], a receipt for `docs/alias`
            # -- a symlink into `secrets/` -- passes a lexical test while the
            # write went exactly where it was forbidden to go.
            #
            # Both representations are checked rather than one replacing the
            # other, because neither is sound alone: the chained declared path
            # is tamper-evident but lexical, and a link resolved at acceptance
            # time is the true target but re-pointable after the fact. Either
            # matching scope.out is a finding, so defeating the comparison
            # requires defeating both. Recording the resolved path in the
            # effect note at WRITE time is the real fix and is a contract
            # change -- filed as es#147, not smuggled in here.
            candidates = [target]
            resolved = self._resolved_relpath(rel)
            if resolved is not None and resolved != target:
                candidates.append(resolved)
            # WHICH representation violated is recorded, not just that one did.
            # The finding used to carry only the lexical path, so an amendment
            # naming `docs/**` discharged a write that -- through a link --
            # landed in `secrets/`. The operator authorised `docs/`; nothing
            # authorised `secrets/x`; the PASS was accepted anyway.
            # ALL violating representations, not the first. `next()` recorded
            # only one, so when two exclusions both fired -- secrets/alias ->
            # keys/, with scope.out=["secrets/**","keys/**"] -- discharging the
            # lexical one was enough, and a private key landed in keys/ under
            # an amendment that named only secrets/alias/. Every path that
            # crossed a boundary has to be covered.
            violating = [c for c in candidates
                         if any(rx.match(c) for rx in excludes)]
            if violating:
                findings.append({"artifact_path": rel, "request_id": request_id,
                                 "violating_paths": violating,
                                 "reason": "matches scope.out"})
            elif includes:
                # INCLUSION is tested against every representation too. The
                # exclusion side checked both while this one stayed lexical, so
                # `scope.in=["docs/**"]` with `docs/alias -> src/` accepted a
                # write to `src/a.py`. "Where it was not permitted to go" is
                # the same defect as "where it was forbidden to go".
                outside = [c for c in candidates
                           if not any(rx.match(c) for rx in includes)]
                if outside:
                    findings.append({"artifact_path": rel,
                                     "request_id": request_id,
                                     "violating_paths": outside,
                                     "reason": "outside scope.in"})
        findings.sort(key=lambda f: (f["artifact_path"], f["request_id"]))
        return findings

    def record_verdict(self, verdict: str, acceptor_id: str, assurance_tier: str,
                        reason: str,
                        scope_ack: list[str] | None = None) -> int:
        latest, path = self.store.load_latest()
        self._verify_manifest(latest)
        if verdict not in VERDICTS:
            raise CustodyError(f"unknown verdict {verdict!r}")
        _refuse_reserved_note(reason)
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
            # A PASS asserts the chain is clean. If receipted work fell outside
            # the declared boundary, that assertion needs an answer.
            #
            # PROSE IS NO LONGER THE ANSWER. Three rounds tried to read the
            # operator's verbatim amendment and decide whether it AUTHORISED a
            # path: first any-amendment, then name-the-path, then
            # name-it-without-a-denial-marker. Each closed a real hole and each
            # opened the next, because the decision procedure was "pattern-match
            # English" and the input space is unbounded. Measured at the end of
            # that line: the denial-marker list caught 1 of 14 denial shapes,
            # and two of the misses -- a denial header with paths listed
            # beneath it, and a grant and a prohibition in one clause -- cannot
            # be fixed by adding vocabulary. A substring test establishes that
            # an amendment MENTIONS a path. It cannot establish that the
            # operator granted it, and "secrets.env remains forbidden"
            # discharging a write to secrets.env is what that difference costs.
            #
            # So the parse is demoted to a HINT and the judgement moves to a
            # party who can actually make it: the ACCEPTOR, who is already
            # required to be distinct from the steward. `scope_ack` is an
            # explicit, per-path acknowledgement. The record then asserts "an
            # acceptor judged these covered", which is true and attributable,
            # instead of "an amendment covers these", which the parser
            # demonstrably cannot establish.
            #
            # es#150 replaces this with a structured `--grants-path` populated
            # by an affirmative act; a denial never populates it, and all 14
            # shapes collapse to one case.
            drifted = self.scope_consistency()
            if drifted:
                # NORMALISE the ack the same way the findings were normalised.
                # `violating_paths` hold `_norm_path` output, and exact string
                # equality meant the acceptor had to supply a spelling that
                # appears nowhere except the refusal message: not the path the
                # operator wrote, not the path in the receipt. "Secrets.ENV",
                # "./secrets.env" and a trailing space all refused. Worse,
                # `_norm_path` folds case only on NT, so an ack captured in a
                # runbook was platform-specific.
                # Surrounding whitespace is stripped before normalising: an
                # acceptor pastes these out of the refusal message or a handoff
                # note, and refusing over a trailing space is a false block
                # with no diagnostic value.
                from custody_gate import _norm_path as _np
                acknowledged = {_np(p.strip()) for p in (scope_ack or ())
                                if p and p.strip()}
                outstanding = sorted({p for f in drifted
                                      for p in f["violating_paths"]
                                      if p not in acknowledged})
                if outstanding:
                    mentioned = sorted(
                        p for p in outstanding
                        if any(_amendment_names(a.get("text", ""), p)
                               for a in manifest["authority"]["amendments"]))
                    hint = (f" Amendments MENTION {', '.join(mentioned)} -- "
                            "read them and decide; a mention is not a grant."
                            if mentioned else "")
                    raise AcceptanceRefused(
                        f"{len(outstanding)} path(s) crossed the declared "
                        f"scope and are not acknowledged: "
                        f"{', '.join(outstanding)}.{hint} Re-record the "
                        "verdict acknowledging each path you have judged "
                        "covered -- CLI: `accept ... "
                        + " ".join(f"--scope-ack {p}" for p in outstanding)
                        + "` -- or accept with FAIL/INCONCLUSIVE. A PASS would "
                        "assert a boundary the record contradicts.")
                # The acknowledgement is a first-class chain fact, not a
                # side effect: it names who judged what, so an auditor can see
                # that the boundary was crossed AND that a distinct acceptor
                # took responsibility for it.
                # Only paths that were ACTUALLY outstanding are recorded. An
                # ack naming something that was never a finding used to be
                # written verbatim into the permanent note -- inert for the
                # gate, but it pollutes the one record that says what the
                # acceptor judged, which is the record's entire purpose.
                covered = sorted({p for f in drifted
                                  for p in f["violating_paths"]}
                                 & acknowledged)
                scope_note = (f"scope-ack by {acceptor_id}: "
                              f"{', '.join(covered)}")
                self._write_next(latest, path, status=latest["status"],
                                 note=scope_note)
                latest, path = self.store.load_latest()
                new_revision = latest["revision"] + 1
                verdict_record["revision"] = new_revision
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
        _refuse_reserved_note(reason)
        new = self._write_next(latest, path, status="cancelled", note=f"cancelled: {reason}")
        return new["revision"]

    def status(self) -> dict:
        latest, _ = self.store.load_latest()
        self._verify_manifest(latest)
        return latest
