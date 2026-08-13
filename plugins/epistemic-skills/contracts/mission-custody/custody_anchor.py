#!/usr/bin/env python3
"""Tail-anchor identity, file, and state machine (mission-custody@2).

The anchor pins the newest checkpoint's sha OUTSIDE the workspace. A
workspace-scoped attacker can append a well-formed checkpoint as easily as
edit one -- `prev_checkpoint_sha256` is computable from a pure read of the
tail -- so the only thing that distinguishes the real tail from a forged one
is a record the attacker cannot reach.

Three properties this module is built around. Each is a laundering hazard,
and each was measured rather than assumed:

1. `read_anchor` is THREE-VALUED and keys its middle state on FILE
   EXISTENCE, never on parse success. `absent` is the only state that
   triggers trust-on-first-use adoption, so anything reaching `absent` by
   mistake adopts a fresh anchor pinning whatever tail is present -- a
   forged tail becomes `verified` on the next check. `null` is valid JSON
   that parses to `None`, and a directory named `<key>.json` raises
   PermissionError on Windows: both are files that exist, so neither is
   `absent`.

2. `classify` is TOTAL over the anchor value. The anchor file is the
   adversary-controlled artifact this state machine exists to judge, so a
   one-byte file must not disable the control by crashing it. Same doctrine
   as `_load_receipt`: crashing the recovery path on a mangled artifact is a
   denial of service by exactly the tampering the detection exists to catch.
   (Totality is claimed over `anchor` only. `tail_sha` and `chain_shas` come
   from the store, not from disk-as-JSON, and are trusted to be a str and a
   sequence of str.)

3. `mission_key` must yield ONE key per directory and DIFFERENT keys per
   directory. Over-matching makes two missions fight over one anchor;
   under-matching mints parallel anchors, each adopting independently, which
   is quiet erosion of the whole control.

Dependency note: this module imports `custody_store` (for `StoreError`) and
deliberately does NOT import `custody_mission`. `_ascii_case_fold` is
COPIED below rather than imported because a later task wires the anchor into
`resume`, at which point `custody_mission` imports this module; importing it
back would close a cycle that only import order is holding open today.
`test_custody_anchor.py` pins the copy against the original so it cannot
drift.

Two directories, not one: `anchor_root()` returns the ROOT (whose path is
recorded as `resolved_root` and printed when overridden), while
`read_anchor`/`write_anchor` take the directory that holds the anchor FILES.
`anchors_dir(root)` is the bridge between them, and is the only correct way
to get from one to the other.
"""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path

from custody_store import StoreError

_HEX = frozenset("0123456789abcdef")

# The 4-character extended-length prefix, as 4 characters: \ \ ? \
_EXT_PREFIX = "\\\\?\\"
_EXT_UNC_PREFIX = _EXT_PREFIX + "UNC\\"

_DEFAULT_ROOT_NAME = ".mission-custody"
_ANCHORS_SUBDIR = "anchors"

ANCHOR_UNREADABLE = object()  # a distinct sentinel: NOT None, NOT a dict


class AnchorMismatch(StoreError):
    """The anchor does not agree with the chain; refuse loudly."""


class AnchorWriteFailed(StoreError):
    """The anchor was NOT persisted.

    Raised rather than returned because the natural call site discards a
    return value, and a discarded write failure is indistinguishable from a
    mission that never had an anchor: the next check finds no file, reports
    `absent`, and adopts. A caller that genuinely wants best-effort
    behaviour (the read-path TOFU write) must catch this explicitly and
    surface it -- `unpersisted` is a state to report, not a silence.
    """


class AnchorKeyUnresolvable(StoreError):
    """The mission directory could not be canonicalised into a key.

    Measured on this fleet: `os.path.realpath` raises OSError
    (WinError 1326) on a UNC path whose share will not authenticate, which
    is the very spelling this fleet's mission dirs can take. Left uncaught
    it kills the anchor with a bare stdlib traceback. Refusing is the safe
    direction and substituting a different canonicalisation is not: a key
    that changes when a share hiccups mints a second anchor, and a second
    anchor adopts.
    """


class AnchorState:
    """The four states, as constants. `classify` returns one of these."""

    VERIFIED = "verified"
    LAGGING = "lagging"
    ABSENT = "absent"
    MISMATCH = "mismatch"
    ALL = frozenset({VERIFIED, LAGGING, ABSENT, MISMATCH})


def _ascii_case_fold(text: str) -> str:
    """Fold A-Z only, leaving every other codepoint byte-exact.

    COPIED from `custody_mission._ascii_case_fold`, deliberately, to keep
    `custody_anchor` free of a `custody_mission` import (see the module
    docstring). `test_custody_anchor.py` asserts the two agree, so the copy
    cannot drift silently.

    NOT str.casefold(): full Unicode folding performs 1-to-many expansions
    that NTFS's per-codepoint upcase table does not -- 'strasse.txt' and the
    eszett spelling casefold equal while coexisting on disk as two
    independent files, and U+212A KELVIN SIGN folds onto 'k'. Here that
    would collapse two genuinely distinct mission directories onto one
    anchor key.
    """
    return "".join(c.lower() if "A" <= c <= "Z" else c for c in text)


def _is_sha256(value: object) -> bool:
    """A lowercase 64-char hex digest -- the only shape `sha256_file` emits.

    An anchor pinning anything else cannot name a checkpoint on disk, so
    treating it as shape-invalid is not pedantry: without this check, the
    equality test `pinned == tail_sha` decides the state, and a caller that
    passes a non-sha `tail_sha` (the empty-chain call shape) makes
    `{"checkpoint_sha256": ""}` classify as `verified`. Measured.

    An uppercase spelling is shape-invalid, hence `mismatch`, and that is
    the safe direction: under-matching refuses loudly and names the anchor,
    over-matching silently blesses a tail nothing verified.
    """
    return (isinstance(value, str) and len(value) == 64
            and all(c in _HEX for c in value))


def _strip_extended_length(text: str) -> str:
    r"""Remove a `\\?\` extended-length prefix, preserving absoluteness.

    The naive 4-character slice is wrong for the UNC form: `\\?\UNC\srv\sh`
    becomes `UNC\srv\sh`, which is RELATIVE, so `realpath` resolves it
    against the current working directory and one mission directory mints a
    different key per CWD. Measured: two CWDs, two keys, for one path.

    The isabs fallback is the net for any other prefixed form this
    enumeration has not reached. It looks redundant beside the UNC branch
    and is kept BECAUSE it looks redundant: the failure it catches is the
    spelling nobody listed.

    Ordering note: on this platform `realpath` PRESERVES a genuine 4-char
    prefix, so strip-before and strip-after produce identical keys and this
    ordering is not load-bearing here. It is kept ahead of `realpath`
    because a stripped path is the one that can equal the plain spelling on
    a filesystem where `realpath` does less.
    """
    if text.startswith(_EXT_UNC_PREFIX):
        return "\\\\" + text[len(_EXT_UNC_PREFIX):]
    if not text.startswith(_EXT_PREFIX):
        return text
    stripped = text[len(_EXT_PREFIX):]
    if os.path.isabs(text) and not os.path.isabs(stripped):
        return text  # stripping would have made an absolute path relative
    return stripped


def _resolve_path(target: Path | str) -> str:
    """Strip the extended-length prefix, then `realpath`. Case preserved.

    Separate from `_canonical_identity` because the two results are for
    different jobs: this one is a path to USE (returned by `anchor_root`,
    recorded as `resolved_root`, printed in messages), so folding its case
    here would hand the operator a lowercased path that is not how anything
    else spells it.
    """
    text = _strip_extended_length(str(target))
    try:
        return os.path.realpath(text)
    except OSError as exc:
        raise AnchorKeyUnresolvable(
            f"cannot canonicalise path {text!r}: {exc}") from exc


def _canonical_identity(target: Path | str) -> str:
    """One spelling per directory: strip -> realpath -> case-fold on NT.

    For KEYS and for path-containment comparisons only, never for a path
    that will be shown or stored.
    """
    text = _resolve_path(target)
    if os.name == "nt":
        # Gated exactly as `custody_mission._same_artifact` gates it, and for
        # the same reason: answer the way THIS platform answers. Folding
        # unconditionally would make `/x/A` and `/x/a` -- two different
        # directories on a case-sensitive filesystem -- share one anchor,
        # and two missions fighting over one anchor is not stability.
        text = _ascii_case_fold(text)
    return text


def mission_key(mission_dir: Path) -> str:
    """The anchor key for a mission directory.

    Keyed on the PATH, not on the mission id, so deleting a mission dir and
    reopening the same id at the same path keeps the key -- which is why the
    case fold matters: `realpath` case-normalises an EXISTING path on NTFS
    but leaves a non-existent one exactly as spelled (measured), and the
    delete-then-reopen case is precisely the non-existent one.
    """
    return hashlib.sha256(
        _canonical_identity(mission_dir).encode("utf-8")).hexdigest()


def anchors_dir(root: Path) -> Path:
    """The directory holding anchor files, given an anchor ROOT.

    `read_anchor`/`write_anchor` take THIS, not the root. Passing a root
    where an anchors dir belongs writes real anchors one directory too high,
    where the next check will not find them -- and not-found is `absent`,
    which adopts.
    """
    return Path(root) / _ANCHORS_SUBDIR


def anchor_root(override: str | None = None, *,
                workspace: Path | str | None = None) -> Path:
    """Resolve the anchor root. Creates nothing; touches no file.

    `override` is honoured only when given explicitly (there is no
    environment variable for it, by design). The default is
    `~/.mission-custody`.

    ⚠ The default is NOT env-free and this is disclosed, not denied:
    `Path.home()` resolves through `USERPROFILE`/`HOMEDRIVE`+`HOMEPATH` on
    Windows and `HOME` on POSIX, all of which an actor that can invoke a
    process controls. What that buys such an actor is a PRIVATE anchor, not
    control of the steward's: the honest steward's next run still reads the
    real root and refuses.

    `workspace`, when given, is the tree the anchor must stay out of -- an
    anchor inside the workspace is reachable by exactly the attacker the
    anchor exists to detect, so a root resolving inside it is refused rather
    than quietly accepted.
    """
    chosen = (Path(override) if override is not None
              else Path.home() / _DEFAULT_ROOT_NAME)
    resolved = _resolve_path(chosen)
    if workspace is not None:
        # Compare on the CANONICAL spellings (case-folded on NT), not on the
        # returned ones: `C:\WS` and `c:\ws\anchors` are the same tree, and a
        # containment check that misses that is a check that passes.
        here = _canonical_identity(resolved)
        ws = _canonical_identity(workspace).rstrip(os.sep)
        if here == ws or here.startswith(ws + os.sep):
            raise AnchorMismatch(
                f"anchor root {resolved!r} resolves inside the workspace "
                f"{ws!r}; an anchor the workspace can write anchors nothing")
    return Path(resolved)


def _is_safe_key(key: object) -> bool:
    """Is `key` exactly one path component?

    The key comes from `mission_key` (64 hex chars) in every shipped call
    path, so this guard is for the call path that does not exist yet: a key
    carrying a separator or `..` would let `write_anchor` land a file
    OUTSIDE the root it was handed, which is the one thing this module's
    mutation surface says it never does.

    Both separators are rejected on BOTH platforms, not just the local one.
    A backslash is a legal filename character on POSIX, so `os.sep`-only
    checking accepts `..\\..\\x` there -- and anchor roots travel (a synced
    home directory, a repo checked out on two platforms). Rejecting a
    spelling the other platform would have escaped through costs a refusal;
    accepting it costs a write outside the root.
    """
    if not isinstance(key, str) or not key or key in (".", ".."):
        return False
    return not any(c in key for c in ("/", "\\", ":"))


def read_anchor(key: str, root: Path):
    """THREE-VALUED, and that is the whole point:

         None                -> no anchor file exists            -> `absent`
         ANCHOR_UNREADABLE   -> a file exists but is not usable   -> `mismatch`
         dict                -> parsed (contents still untrusted)

    Collapsing the middle case into None is the defect this signature exists
    to prevent: `absent` is the only state that triggers trust-on-first-use
    adoption, so an unusable file would be adopted as a fresh anchor pinning
    whatever tail is present. Once both return None, `classify` CANNOT tell
    them apart -- the distinction has to be preserved HERE.

    The middle state is keyed on the file being THERE, not on the parse
    succeeding, because three routes reach "there but unusable" and only one
    of them is a parse failure:

      - `null` is valid JSON that parses to None -- the same value that
        means "no file at all";
      - a DIRECTORY at `<key>.json` raises PermissionError on Windows
        (measured, errno 13), not FileNotFoundError, so catching only
        FileNotFoundError lets a `mkdir` crash the control outright;
      - the anchors directory itself being a FILE raises FileNotFoundError
        on Windows (measured, errno 2) -- indistinguishable from a missing
        anchor unless the parent is checked, and a broken store is
        corruption, not absence.

    Never raises, including on a malformed key: an unsafe key would read
    some file that is not this mission's anchor, and "cannot read a valid
    anchor" is `ANCHOR_UNREADABLE`, not `absent`.
    """
    if not _is_safe_key(key):
        return ANCHOR_UNREADABLE
    path = Path(root) / f"{key}.json"
    try:
        raw = path.read_bytes()
    except FileNotFoundError:
        # A missing ancestry is a fresh install: genuinely absent. An
        # ancestor that EXISTS and is NOT a directory is a broken store, and
        # corruption must never alias to absence.
        #
        # The walk is not decoration: POSIX reports ENOTDIR for a path
        # through a file (caught by the OSError branch below), but Windows
        # reports plain FileNotFoundError (errno 2, measured) for the same
        # tree, at any depth. Checking only the immediate parent agrees with
        # POSIX one level down and disagrees two levels down, which is a
        # state machine that answers differently by platform.
        probe = path.parent
        while True:
            if probe.exists():
                return None if probe.is_dir() else ANCHOR_UNREADABLE
            if probe.parent == probe:
                return None
            probe = probe.parent
    except OSError:
        # PermissionError, IsADirectoryError, a locked file, an I/O error:
        # the file is there and we cannot use it. Never `absent`.
        return ANCHOR_UNREADABLE
    try:
        value = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return ANCHOR_UNREADABLE
    return ANCHOR_UNREADABLE if value is None else value


def classify(anchor, tail_sha: str, chain_shas: list[str]) -> str:
    """verified | lagging | absent | mismatch.

    NO auto-advance. A lagging anchor is the legitimate-crash shape AND the
    forged-append shape, and they are byte-identical: `prev_checkpoint_
    sha256` is computable from the readable tail, so an attacker constructs
    the lag on demand.

    TOTAL over every JSON value the anchor file can hold, by construction --
    it must RETURN for any input, never raise.

    Ancestry is resolved by HASH, never by comparing `revision`:
    `load_latest` never validates `revision` against the filename, so an
    appended file carries an attacker-chosen revision number.
    """
    if anchor is None:
        return AnchorState.ABSENT
    if not isinstance(anchor, dict):
        # list/str/int/float/bool, and ANCHOR_UNREADABLE. Note
        # `isinstance(True, int)` is True in Python, so this check must stay
        # ahead of anything numeric added later.
        return AnchorState.MISMATCH
    pinned = anchor.get("checkpoint_sha256")
    if not _is_sha256(pinned):
        return AnchorState.MISMATCH  # shape-invalid NEVER means absent
    if pinned == tail_sha:
        return AnchorState.VERIFIED
    if pinned in chain_shas:
        return AnchorState.LAGGING  # an ANCESTOR, resolved by hash
    return AnchorState.MISMATCH


def write_anchor(key: str, root: Path, record: dict) -> Path:
    """Persist an anchor atomically. Returns the path; RAISES on failure.

    There is no boolean here on purpose. A `False` the caller can drop
    produces the same laundering as a forged file by a different route: the
    anchor is believed written, is not on disk, and the next check finds no
    file, reports `absent`, and adopts. `anchor_root` refusing a root inside
    the workspace is precisely a condition that makes this write fail, so
    the refusal path and the silent-no-anchor path are one edit apart.

    A caller that wants the design's best-effort read-path (TOFU) behaviour
    catches `AnchorWriteFailed` explicitly and reports `unpersisted`. A
    caller that drops it gets a traceback, which is the correct outcome:
    loud beats silently unprotected.

    Overwrite, not compare-and-swap. The advance-only CAS belongs to the
    caller that knows what the anchor currently pins; this is the file
    layer.
    """
    if not isinstance(record, dict):
        raise AnchorWriteFailed(f"anchor record must be a dict, got {type(record)}")
    if not _is_sha256(record.get("checkpoint_sha256")):
        # An anchor pinning a non-sha can never verify against any chain, so
        # writing one wedges the mission at `mismatch` forever. Refuse at the
        # writer rather than discover it at the next read.
        raise AnchorWriteFailed(
            "anchor record needs a lowercase 64-hex checkpoint_sha256, got "
            f"{record.get('checkpoint_sha256')!r}")
    if not _is_safe_key(key):
        raise AnchorWriteFailed(f"anchor key is not one path component: {key!r}")
    path = Path(root) / f"{key}.json"
    data = (json.dumps(record, indent=1, sort_keys=True) + "\n").encode("utf-8")
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    except OSError as exc:
        raise AnchorWriteFailed(f"cannot write anchor at {path}: {exc}") from exc
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    except BaseException as exc:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        if isinstance(exc, OSError):
            raise AnchorWriteFailed(
                f"cannot write anchor at {path}: {exc}") from exc
        raise
    return path
