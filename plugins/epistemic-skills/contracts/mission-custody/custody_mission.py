#!/usr/bin/env python3
"""Mission lifecycle: draft -> active -> verifying -> completed, with drift
reanchoring on resume and a clearable FAIL path (no PA reject dead-end)."""
from __future__ import annotations

import json
import os
import re
import stat
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

from custody_store import (
    MissionStore, StoreError, atomic_write_json, sha256_bytes, sha256_file,
)
from verify_mission_custody import (
    TIERS, VERDICTS, _ID_RE, epoch_skew_anywhere, validate_record,
)

_OPEN_STATES = {"draft", "active", "reopened", "verifying"}
_EFFECT_STATES = {"draft", "active", "reopened"}
_TIER_RANK = {"declared-role-separation": 1, "operator-accepted": 2}
_UNSET = object()  # amend sentinel: distinguishes "leave alone" from "clear"
_GUARD_AUTHORITY_KEYS = ("actuator_guards", "guard_mode")
assert set(_TIER_RANK) == TIERS, "tier rank table out of sync with verify_mission_custody.TIERS"

_ABS_DRIVE_RE = re.compile(r"^[A-Za-z]:")
# The scope comparison can prove a receipted artifact has ANOTHER NAME, and it
# cannot prove where that name is. Both halves live in the reason string,
# because a finding naming only the half it proved reads as a boundary it
# checked.
_MULTIPLY_LINKED = "multiply linked -- other names are not compared"
_RETIRED_NOTE = "receipt loss acknowledged: "
# Notes are the mission's append-only, hash-chained narrative AND the carrier
# for retirement (checkpoint state is exact-field-closed in @1, so a
# retired_ids field would break the schema). Machine-written notes therefore
# own these prefixes exclusively: a caller-supplied note that could imitate
# one would let ordinary narrative forge machine state.
_RESERVED_NOTE_PREFIXES = (
    "effect: ", "reconciled: ", "drift detected: ", "receipt restored: ",
    "authority amended: ", _RETIRED_NOTE, "scope-ack by ",
    # es#173: the quarantine acknowledgement discharges the UnionDegraded
    # refusal, so narrative able to imitate it would forge the discharge.
    "unreadable-acknowledged: ",
    # es#173 section 4: the machine acknowledgement that reconciles
    # DRIFT-SIBLING -- caller narrative must not be able to imitate the
    # record that downgrades a drift finding (gauntlet major).
    "sibling-touched: ",
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
                # A refusal with no stated discharge is a dead end, and this
                # one refuses text the operator was INSTRUCTED to supply:
                # SKILL.md says record the grant verbatim, and a grant may
                # legitimately begin 'effect: ...'. The guard stays; the exit
                # must be printed here, because it is printed nowhere else.
                # The repr of the line is load-bearing for the invisible-
                # character class: the caller who typed what LOOKS benign can
                # only see the refused byte in an escaped rendering.
                raise CustodyError(
                    f"text may not contain a line beginning with {prefix!r}: "
                    "machine-written notes carry mission state and narrative "
                    "must not be able to imitate them, on any line. To record "
                    "this text anyway (a verbatim operator grant, a "
                    "quotation), prefix the offending line with '> ' -- the "
                    "quote marker keeps the words exact while making the line "
                    "unmistakably narrative. Indentation does NOT work: "
                    "leading whitespace is stripped before this comparison. "
                    f"Offending line: {line!r}")


def _refuse_unprintable_identity(value, field: str) -> None:
    """An identity is ONE VISIBLE LINE; refuse the character class at ingestion.

    `acceptor_id` was schema'd as any nonempty string, and the scope-ack note
    interpolates it -- so an actor named
    'agent:acceptor\\nscope-ack by operator: forged.env' wrote a chained note
    whose second line reads as an acknowledgement by the operator (reproduced
    live). `_refuse_reserved_note` exists precisely so an auditor can trust
    those lines, and the identity field walked around it.

    The first guard enumerated categories -- Cc and Cf -- and enumeration is
    the defect's own shape: a full-range census found the `splitlines`
    boundary set is {0A,0B,0C,0D,1C,1D,1E,85,2028,2029}, and 8 of the 10 are
    Cc, which is why the enumerated rule caught most of them and missed
    exactly the two Z ones (U+2028, U+2029 -- line structure the category
    list never named). Extending the list by the two categories the last
    reviewer happened to find would be the same failure again. So the rule is
    now a PREDICATE that fails closed on the unenumerated class:

        len(value.splitlines()) > 1  or  not value.isprintable()

    on the RAW value -- never NFKC first, which maps NBSP to a plain space
    and launders the confusable before the check. `isprintable()` refuses
    Cc, Cf, the Z line/paragraph separators, every non-ASCII space, lone
    surrogates (which persist to disk via ensure_ascii and then crash any
    utf-8-strict reader), private-use and unassigned -- with zero false
    refusals across the realistic battery: ASCII, composed AND decomposed
    accents, CJK, emoji, spaced human names.

    The splitlines clause is REDUNDANT TODAY, on purpose, and an earlier
    revision of this docstring falsely called both clauses load-bearing
    (round-3 refutation, executed): the full-range census shows every
    splitlines boundary character is itself unprintable, so isprintable
    subsumes it -- 'a\\n', 'a\\tb' and an ANSI escape are all caught by
    isprintable alone, and no codepoint exists that splits a line while
    printing. The clause stays because it restates the PROPERTY this guard
    exists for (one line) directly, so if printability and line-splitting
    ever diverge in a future Unicode database the guard widens its refusal
    instead of silently admitting the new line boundary. It can only ever
    refuse more, never less.

    EDGE WHITESPACE is refused separately, and the row that forces it is
    pure ASCII: 'agent:worker-1 ' (trailing space) versus 'agent:worker-1'
    is a display-identical, byte-distinct pair that defeats the casefolded
    acceptor != worker self-certification check, and both clauses above
    accept it. Interior spaces stay legal -- 'John Smith' is an identity;
    an identity that starts or ends with one is either a paste error or
    that pair.

    What this guard now CLAIMS: no line structure, no control effects, no
    Cf-class invisibles, no invisible edge whitespace. It does NOT claim
    display-uniqueness: invisible-but-printable characters -- CGJ (U+034F),
    variation selectors, Hangul fillers -- pass every candidate rule at this
    granularity, because the same category holds the combining acute in
    'José'. That residual is real, disclosed, and filed (es#167, riding
    es#150's structured-record direction), exactly as the reserved-note
    guard already defers homoglyphs. Non-strings and empties are left to
    their existing failure modes; this guard owns exactly the character
    class."""
    if not isinstance(value, str):
        return
    bad = sorted({c for c in value if not c.isprintable()})
    if bad or len(value.splitlines()) > 1:
        raise CustodyError(
            f"{field} may not contain control, separator, or invisible "
            "format characters: an identity is one visible line, "
            "interpolated into machine-written notes and display surfaces, "
            "where an embedded newline forges a machine-note line and an "
            "escape sequence rewrites the terminal. Supply the identity "
            "without them. "
            "Offending: " + ", ".join(repr(c) for c in bad)
            + f" in {value!r}")
    if value != value.strip():
        raise CustodyError(
            f"{field} may not begin or end with whitespace: "
            f"{value!r} and {value.strip()!r} are display-identical but "
            "byte-distinct, so an edge space forges a second identity that "
            "reads as the first -- including past the acceptor/worker "
            "separation check. Supply the identity without edge whitespace.")


def _refuse_unrecordable_artifact_path(relpath) -> None:
    """Refuse line structure and control effects in NEW artifact paths, at
    the one verb that mints them.

    es#153, in exactly the narrow form the gauntlet adjudication ruled
    (es#150 adjudication, 2026-08-13): the `effect:` note carries the path
    verbatim because `_historical_effect_path` reads it back out -- the note
    IS the tamper-evident record of the path -- so a newline in a filename
    wrote a chained note whose second line read as a machine acknowledgement
    (executed on the issue). Quoting the note is a contract change; refusing
    the class at ingestion is not.

    NARROW means narrow: the refusal set is Cc (controls: newline, CR, tab,
    ESC, DEL), Zl and Zp (the Unicode line/paragraph separators
    `splitlines` honors) -- the characters that can forge note structure or
    rewrite a terminal. Spaces, quotes, NBSP, and every printable Unicode
    name stay LEGAL: the discharge machinery for awkward-but-printable
    names survives intact, and the adjudication's freeze forbids widening
    it. Cf (printable-invisible format characters, including BiDi
    overrides) is deliberately NOT refused here -- it breaks no line
    structure and rewrites no terminal; that display-spoofing residue is
    the same class es#167 already tracks for identities.

    INGESTION ONLY, at `record_effect`: `reconcile` re-covers artifacts
    that already exist in the record, and refusing there would wedge the
    recovery of exactly the historical missions this guard cannot reach --
    records written before it shipped remain readable, comparable, and
    dischargeable forever. Non-strings are left to their existing failure
    modes; this guard owns exactly the character class."""
    if not isinstance(relpath, str):
        return
    bad = sorted({c for c in relpath
                  if unicodedata.category(c) in ("Cc", "Zl", "Zp")})
    if bad:
        raise CustodyError(
            "artifact path may not contain control characters or line "
            "separators: the chained effect note carries the path verbatim "
            "(the note is the record), so an embedded line boundary forges "
            "a machine-note line and a control character rewrites the "
            "terminal that displays it. Record the artifact under a name "
            "without them. "
            "Offending: " + ", ".join(repr(c) for c in bad)
            + f" in {relpath!r}")


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
    separator flavor, repeated separators, '.' SEGMENTS (leading './',
    interior '/./', terminal '/.', and iterated mixes of them), a trailing
    '/'. ('..' never appears in receipted paths -- _resolve_artifact_path
    rejects it at the door; on the pattern side a '..' segment is demoted to
    uncompared by `_is_matchable_pattern`.)

    '.' segments ONLY: a trailing dot inside a final segment NAME ('weird.')
    is a legal filename character everywhere this runs, and NT-only
    filesystem semantics must not leak into a cross-platform lexical
    normaliser. The collapse runs to a fixed point because each rule can
    expose another's pattern ('docs/.//' needs the doubled-separator rule
    again after the terminal-dot rule fires).

    The terminal '/.' rule earns its place twice over. On the receipt side
    the resolver treats 'docs/x.txt/.' and 'docs/x.txt' as one path while
    the lexical normaliser kept them distinct -- a false FLAG, dischargeable,
    the safe direction. The row that flips the priority is its MIRROR on the
    pattern side: a scope.out entry carrying one '/.' spelling compiled to a
    regex no normalized receipt path can ever match, silently disabling a
    boundary the operator wrote, with `uncompared_scope_entries` not listing
    it -- silent-inert, the exact class that surface exists to end. A bare
    '.' (or './', or './.') normalizes to the EMPTY path, which names the
    workspace itself, not any receiptable artifact -- `_is_matchable_pattern`
    demotes those to disclosed."""
    norm = path.replace("\\", "/")
    prev = None
    while norm != prev:
        prev = norm
        while "//" in norm:
            norm = norm.replace("//", "/")
        while "/./" in norm:
            norm = norm.replace("/./", "/")
        while norm.startswith("./"):
            norm = norm[2:]
        if norm.endswith("/."):
            norm = norm[:-1]
    if norm == ".":
        return ""
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


def _first_effect_note(notes: list[str], kind: bool = False) -> str | None:
    """The path (or with kind=True, the mint kind) recorded by the first
    'effect: ' / 'reconciled: ' note in this slice of newly-appended notes.

    The ONE place that rule is written. `_historical_effect_path` and
    `_effect_path_index` both call it, so the single-id answer and the
    whole-chain index cannot disagree -- a differential test pins that
    (test_effect_path_index_matches_per_id).

    SEPARATORS ARE NORMALIZED HERE, exactly as `_write_effect` normalizes
    them when it writes the receipt (`.replace("\\\\", "/")`). The note keeps
    whatever spelling the caller passed, so `dir\\file.txt` -- the native
    spelling on Windows -- was recorded as a receipt saying `dir/file.txt`
    and a note saying `dir\\file.txt`. Any comparison of the two rejected
    the contract's OWN valid receipt: `resume()` then reported
    RECEIPT-MISSING for honest work, and `acknowledge_receipt_loss` would
    retire a perfectly good id and demand re-coverage. Comparing spellings
    that one writer deliberately produces in two forms is a defect in the
    comparison, not in the record."""
    for note in notes:
        for prefix in ("effect: ", "reconciled: "):
            if note.startswith(prefix):
                if kind:
                    return prefix.rstrip(": ")
                return note[len(prefix):].replace("\\", "/")
    return None


def _find_marker(unresolved: list[str], prefix: str, artifact_relpath: str) -> str | None:
    """The marker in `unresolved` naming this artifact, or None. Matching is
    by artifact identity, never by string equality of the whole marker."""
    for marker in unresolved:
        if marker.startswith(prefix) and _same_artifact(
                marker[len(prefix):], artifact_relpath):
            return marker
    return None


def _approved_by_chain(store: MissionStore) -> bool:
    """Has this mission EVER been operator-approved? The chain test, not
    latest status: a never-approved mission can sit in `reopened` (drift on
    a draft reopens it), so "latest status != draft" would let store damage
    arm a draft's guards (OD-4) and let a never-approved sibling launder
    drift (FATAL-3 leg 2). The core's own `_resumption_status` doctrine,
    shared here so the union assembler and the resume discriminator cannot
    disagree with it. Unreadable checkpoints answer False -- damage must
    never widen authority."""
    for cp_path in store.checkpoint_paths():
        try:
            record = json.loads(cp_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return False
        if record.get("status") not in ("draft", "reopened"):
            return True
    return False


class CustodyError(Exception):
    pass


class NoActiveMission(CustodyError):
    pass


class MultipleActiveMissions(CustodyError):
    """RETIRED as a load-failure class (es#173): plurality is legal, so no
    verb raises this any more. The class survives for import compatibility
    and for readers of historical stores/logs that name it."""


class BindingRequired(CustodyError):
    """N>1 active missions and no session binding: the verb refuses rather
    than guess which mission's authority the work lands under (es#173 §1)."""


class BindingInvalid(CustodyError):
    """The session's binding names a mission this workspace cannot act
    under -- nonexistent, unreadable, completed, or cancelled. A stale
    binding NEVER falls through to discovery or to the union: silent
    fallback is how a session acts under the wrong authority politely
    (es#173 §1)."""


class UnionDegraded(CustodyError):
    """An active sibling's store is unreadable, so its guards are silently
    absent from the union. `effect` refuses under this state until the
    sibling is repaired or the degradation is explicitly acknowledged
    (es#173 §2, case row B23)."""


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
    if any(c in norm for c in "{}[]"):
        return False
    # A `..` SEGMENT survives normalization -- `_normalize_relpath` collapses
    # `.` segments and `//` but not `..` -- while every receipted artifact
    # path is normalized before comparison. So `docs/../secrets/**` compiles
    # to a regex that can only match the literal spelling
    # `docs/../secrets/...`, which no normalized path ever produces: it is a
    # boundary an operator wrote as a traversal, and it binds nothing.
    #
    # SEGMENT, not substring: `a..b/**` and `docs/.../x` are legal names whose
    # dots are inside a segment, and they match normally. A substring test
    # demotes both -- checked against the case table, where it is the only
    # difference between the two candidates.
    segments = _norm_scope_segments(norm)
    if segments == [""]:
        # './' (and '.', './.') normalize to the EMPTY path: the workspace
        # itself, which no receipt path ever spells. 'the whole workspace is
        # in scope' is a natural thing to DECLARE and an impossible thing to
        # match against per-artifact paths, so the entry is disclosed as
        # uncompared -- for scope.in this disables the absence inference
        # entirely (everything is inside a declared-universal include), which
        # is both the declared meaning and the safe direction.
        return False
    return ".." not in segments


def _seg_intersect(a: str, b: str) -> bool:
    """Can two single-segment globs ('*'/'?' in-segment, no '/') both match
    at least one string? Standard two-pattern recursion; memoized."""
    memo: dict[tuple[int, int], bool] = {}

    def rec(i: int, j: int) -> bool:
        key = (i, j)
        if key in memo:
            return memo[key]
        out = False
        if i == len(a) and j == len(b):
            out = True
        else:
            if not out and i < len(a) and a[i] == "*":
                out = rec(i + 1, j) or (j < len(b) and rec(i, j + 1))
            if not out and j < len(b) and b[j] == "*":
                out = rec(i, j + 1) or (i < len(a) and rec(i + 1, j))
            if not out and i < len(a) and j < len(b) \
                    and a[i] != "*" and b[j] != "*" \
                    and (a[i] == "?" or b[j] == "?" or a[i] == b[j]):
                out = rec(i + 1, j + 1)
        memo[key] = out
        return out

    return rec(0, 0)


def _globs_intersect(left: str, right: str) -> bool:
    """Do two scope path patterns admit a common path? (es#173 §3.)

    Decidable for the dialect `_glob_regex` compiles: segments split on '/',
    a segment containing '**' matches ZERO or more whole segments (which
    also covers the trailing-'/**' base-path rule: ['x','**'] with '**'
    consuming zero segments matches the base 'x'), '*'/'?' stay in-segment.
    Both sides are normalized exactly as the receipt comparison normalizes,
    including the NT-only A-Z fold, so the disclosure agrees with the
    machinery it discloses about. Disclosure-only: an over- or under-report
    here blocks nothing (coexistence on shared paths is the feature)."""
    def prep(pattern: str) -> list[str]:
        norm = _normalize_relpath(pattern)
        if os.name == "nt":
            norm = _ascii_case_fold(norm)
        return ["**" if "**" in seg else seg for seg in norm.split("/")]

    pa, pb = prep(left), prep(right)
    memo: dict[tuple[int, int], bool] = {}

    def rec(i: int, j: int) -> bool:
        key = (i, j)
        if key in memo:
            return memo[key]
        out = False
        if i == len(pa) and j == len(pb):
            out = True
        else:
            if not out and i < len(pa) and pa[i] == "**":
                out = rec(i + 1, j) or (j < len(pb) and rec(i, j + 1))
            if not out and j < len(pb) and pb[j] == "**":
                out = rec(i, j + 1) or (i < len(pa) and rec(i + 1, j))
            if not out and i < len(pa) and j < len(pb) \
                    and pa[i] != "**" and pb[j] != "**" \
                    and _seg_intersect(pa[i], pb[j]):
                out = rec(i + 1, j + 1)
        memo[key] = out
        return out

    return rec(0, 0)


def _norm_scope_segments(norm: str) -> list[str]:
    """Segments of an entry as the comparison will see them, so the matchability
    question is asked against the same normalization the matcher uses."""
    from custody_gate import _norm_path
    return _norm_path(norm).split("/")


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


def _amendment_names_mission(text: str, mission_id: str) -> bool:
    """Does this amendment NAME `mission_id` as a whole token?

    The id leg of the FATAL-3 discriminator, held to the standard
    `_amendment_names` sets for the path leg: never a raw substring. A
    substring test let mission `m-al` ride on an amendment authorizing
    `m-alpine`, and a mission named `test` ride on the word `latest` --
    the false-ALLOW direction, an audit-severity downgrade self-served by
    choosing a convenient id (PR #220 refuter, finding 1). Tokenized
    exactly like `_amendment_names` so the two legs cannot drift apart."""
    for segment in text.replace("\\", "/").splitlines():
        for raw in segment.split():
            if raw.strip(_TOKEN_TRIM).rstrip(".") == mission_id:
                return True
    return False


def _display_path(path: str) -> str:
    """A path the acceptor can SEE, in a spelling that survives being typed.

    `', '.join(outstanding)` renders `secret.env ` and `secret.env`
    identically, so matching the ack exactly would be unusable even once it is
    correct: an acceptor cannot type a spelling the message never shows them.
    Quoting is applied ONLY to paths carrying whitespace or a literal
    double-quote, so ordinary paths -- and the `--scope-ack <path>` line the
    CLI surface is asserted on -- still render bare.

    The double-quote row is the fix's own residue, found on its second
    round: a filename literally containing quotes (`linked:"foo.txt"`, legal
    POSIX) printed bare, and bash ate exactly those quotes on the way back,
    so the token that arrived named a different string and the obligation
    was unreachable through the printed recipe. JSON-escaping the quote
    (`"linked:\\"foo.txt\\""`) is the one spelling bash's double-quote
    context AND CommandLineToArgvW both deliver back byte-exact -- and a
    verbatim (API) arrival decodes through the parser's JSON candidate, so
    both channels land on the same path.

    The quoting is JSON, because it is unambiguous about spaces, tabs and
    quotes; it is deliberately NOT offered as a shell recipe, since cmd,
    PowerShell and sh disagree and a wrong recipe is worse than none. Paths
    carrying OTHER shell-special characters ($, backtick, !) still print
    bare and are still not paste-safe in every shell -- that residue is
    es#163's, unchanged by this rule."""
    if any(c.isspace() for c in path) or '"' in path:
        return json.dumps(path)
    return path


def _acknowledged_paths(scope_ack, violating: set[str]) -> set[str]:
    """Which violating paths the acceptor's `--scope-ack` values actually name.

    The ack was normalised `_np(p.strip())` while the finding was normalised
    `_np(p)` -- two different functions on the two sides of one comparison. A
    path whose real name carries leading or trailing whitespace could therefore
    not be named by any spelling an acceptor could reach. (Not literally none:
    the strip runs BEFORE `_normalize_relpath`, so `'secret.env /'` and
    `'./ secret.env'` survive it and do discharge. Those are incantations
    produced by an implementation detail, printed in no message, in no receipt
    and in no document -- an exit nobody can find is not an exit.)

    The naive repair -- strip the finding too -- is refused, and this is the
    case that refuses it: a name ending in a space is a legal POSIX filename,
    so equating it with the stripped name creates a NEW collision class, in
    which acknowledging the ordinary `secret.env` silently retires custody of a
    different file named `secret.env `. This module has already settled that
    tie-break (see `_ascii_case_fold`): under-matching leaves an obligation
    outstanding with the exact path named -- visible, recoverable -- while
    over-matching silently retires custody of a file nobody is watching.

    So: EXACT FIRST, PER ACK. `_np(raw)` is tried against the violating set,
    and `_np(raw.strip())` only when the exact form named nothing. A union of
    the two normalisations is NOT this rule and is wrong on one row: with both
    `secret.env` and `secret.env ` outstanding, an ack of `'secret.env '`
    matches exactly here and discharges BOTH under a union. That row looks
    redundant beside the ack of `'secret.env'`, and it is the only row that
    separates the two rules.

    Paste tolerance survives for the case it was written for -- an acceptor
    copying `secrets.env` out of a handoff note with a stray trailing space is
    still matched -- because the stripped form is tried when the exact one
    misses. An ack naming nothing at all matches nothing and is inert.

    THE PRINTED RECIPE MUST WORK, so the displayed spelling is also an ack.
    `_display_path` shows a whitespace-bearing path JSON-quoted --
    `"safe.txt\\n"` -- and every shell delivers that argument with the outer
    quotes eaten and the backslash-n as two literal characters. The mangled
    arrival therefore has TWO READINGS: `_norm_path` folds the backslash to
    `safe.txt/n` (the Windows-separator tolerance), and the JSON decode
    restores `safe.txt` + newline. Neither reading is 'exact' -- both are
    interpretations of keystrokes the shell already rewrote -- and the first
    shipped rule called the folded reading exact and took it first, so when
    a genuinely different path `safe.txt/n` was ALSO outstanding, the
    newline file's own printed recipe silently discharged the slash-twin
    the acceptor never named (round-3 refutation, executed: a PASS closed
    with the twin unjudged and the note attributing it to the acceptor).
    Over-matching silently retires custody of a path nobody is watching --
    the direction this module's tie-breaks always refuse.

    So: per ack, ALL readings are computed, and the ack discharges only
    when they agree on ONE unmatched violating path. Two readings naming
    two distinct outstanding paths is AMBIGUOUS and discharges NOTHING --
    under-matched, visible, recoverable. The stripped reading stays a
    fallback tried only when the unstripped readings named nothing (the
    exact-vs-stripped tie-break already settled below stands: for an
    unstripped raw the folded and JSON readings agree, so `'secret.env '`
    still names the spaced twin exactly). Matching runs to a FIXPOINT over
    the whole ack list: discharging the slash-twin by its own unambiguous
    spelling removes it from the outstanding set, after which the mangled
    spelling names only the newline file -- so the full printed recipe
    discharges both in one accept, in either order. An ack that is not
    valid JSON when so read simply contributes no reading from that tier."""
    from custody_gate import _norm_path as _np
    matched: set[str] = set()
    consumed: set[int] = set()
    acks = [raw for raw in (scope_ack or ()) if raw]
    progress = True
    while progress:
        progress = False
        for i, raw in enumerate(acks):
            # ONE DISCHARGE PER TYPED ACK, ever: without the consumed set,
            # an ack of 'secret.env ' would name the spaced twin on one
            # pass and then its STRIPPED reading would name the bare twin
            # on the next -- the union rule the exact-vs-stripped tie-break
            # already refused, resurrected through the fixpoint.
            if i in consumed:
                continue
            outstanding = violating - matched
            readings = {r for r in (_np(raw), _json_decoded_ack(raw))
                        if r is not None and r in outstanding}
            if not readings:
                stripped = raw.strip()
                # A whitespace-ONLY ack is not dropped: `"   "` is a legal
                # filename, and dropping it would recreate this very dead
                # end for exactly the path least likely to be noticed.
                if stripped:
                    readings = {r for r in (_np(stripped),
                                            _json_decoded_ack(stripped))
                                if r is not None and r in outstanding}
            if len(readings) == 1:
                matched.add(readings.pop())
                consumed.add(i)
                progress = True
            # len > 1: ambiguous -- this raw discharges nothing on this
            # pass; a later pass retries it once other acks have thinned
            # the outstanding set
    return matched


def _json_decoded_ack(raw: str) -> str | None:
    """The JSON reading of an ack normalised like every other candidate, or
    None when it has none."""
    from custody_gate import _norm_path as _np
    decoded = _json_decoded_ack_text(raw)
    return _np(decoded) if decoded is not None else None


def _json_decoded_ack_text(raw: str) -> str | None:
    """The JSON reading of an ack as TEXT, or None when it has none.

    Quoted verbatim ('"safe.txt\\n"') decodes directly; the bare form
    ('safe.txt\\n', outer quotes eaten by the shell) decodes after the quotes
    are restored -- refused when the raw text contains an unescaped '"',
    because restoring quotes around it would silently truncate at the
    embedded one."""
    text = raw
    if not (len(text) >= 2 and text.startswith('"') and text.endswith('"')):
        if '"' in text:
            return None
        text = f'"{text}"'
    try:
        decoded = json.loads(text)
    except ValueError:
        return None
    return decoded if isinstance(decoded, str) else None


# Obligation kinds: what an acknowledgement is FOR. A boundary crossing and a
# multiply-linked disclosure are different judgements -- "I checked the
# operator authorised this path" versus "I found the other name and checked
# where it points" -- and one ack used to discharge both at once, so the
# cheaper judgement silently absorbed the dearer one.
_KIND_BOUNDARY = "boundary"
_KIND_LINKED = "linked"
_LINKED_ACK_PREFIX = "linked:"


def _obligation_kind(reason: str) -> str:
    """Map a finding's reason to the obligation kind an ack must name.

    Unknown reasons map to THEMSELVES, and no token form ever discharges
    them: a new finding kind added without its ack shape fails CLOSED (the
    PASS stays refused) instead of failing open through the bare path key --
    which is also why a per-kind bespoke flag (--link-ack) was rejected: a
    noun list of flags cannot terminate, and each new kind would ship
    without its flag and discharge through the path."""
    if reason in ("matches scope.out", "outside scope.in"):
        return _KIND_BOUNDARY
    if reason == _MULTIPLY_LINKED:
        return _KIND_LINKED
    return reason


def _ack_token(path: str, kind: str) -> str | None:
    """The --scope-ack spelling that discharges this obligation, display-
    quoted, or None for a kind no token form can discharge."""
    if kind == _KIND_BOUNDARY:
        return _display_path(path)
    if kind == _KIND_LINKED:
        return _display_path(_LINKED_ACK_PREFIX + path)
    return None


def _acknowledged_obligations(scope_ack,
                              obligations: set[tuple[str, str]]
                              ) -> set[tuple[str, str]]:
    """Which (path, kind) obligations the acceptor's acks actually discharge.

    A bare ack discharges only BOUNDARY obligations; a link obligation needs
    the qualified 'linked:PATH' spelling. The qualifier is read only after
    the raw text failed as a literal boundary path, because 'linked:name' is
    a creatable filename (NTFS alternate-data-stream syntax) and
    exact-path-first is the tie-break `_acknowledged_paths` already settled.
    That same collision makes the RECORD half ('scope-ack by X: linked:p')
    permanently ambiguous between a qualifier and a literal path -- the
    record cannot be made unambiguous by token syntax at all; that is
    es#150's structured {path, kind} field, deliberately not invented here.

    The link ack is CATEGORICAL: it acknowledges that another name exists
    and the acceptor went and looked, not a particular st_nlink value -- a
    count change between the finding and the ack creates no new obligation,
    because the judgement acknowledged ('I found the other names and checked
    where they point') is about the condition, not the number."""
    boundary = {p for p, k in obligations if k == _KIND_BOUNDARY}
    linked = {p for p, k in obligations if k == _KIND_LINKED}
    matched: set[tuple[str, str]] = set()
    consumed: set[int] = set()
    acks = [raw for raw in (scope_ack or ()) if raw]
    progress = True
    while progress:
        progress = False
        for i, raw in enumerate(acks):
            if i in consumed:
                continue
            # Each typed ack discharges at most ONE obligation EVER (the
            # consumed set), and the boundary reading wins only while it
            # still names something new. Without the fallthrough the shadow
            # case is a dead end no spelling can exit through a shell: the
            # quoted qualifier ('linked:"foo.txt"') loses its interior
            # quotes to bash, PowerShell AND CommandLineToArgvW alike, so
            # every pasted token arrives as the bare 'linked:foo.txt' and
            # the boundary reading consumed all of them as the same literal
            # path -- the printed recipe discharged one obligation no matter
            # how many flags were pasted (measured against real shell argv,
            # not a preconstructed argument). The SECOND arrival of the same
            # token therefore means the qualifier. A duplicated BARE path
            # still widens nothing: the fallthrough only reaches tokens
            # that parse as qualifiers. The outer FIXPOINT exists for the
            # ambiguity rule in _acknowledged_paths: an ack whose readings
            # named two outstanding paths discharges nothing on that pass,
            # and is retried once other acks have thinned the set -- so the
            # printed recipe converges in one accept, in either order.
            b_out = {p for p in boundary
                     if (p, _KIND_BOUNDARY) not in matched}
            hit = _acknowledged_paths([raw], b_out)
            if hit:
                matched |= {(p, _KIND_BOUNDARY) for p in hit}
                consumed.add(i)
                progress = True
                continue
            qualified = None
            if raw.startswith(_LINKED_ACK_PREFIX):
                qualified = raw[len(_LINKED_ACK_PREFIX):]
            else:
                # the displayed token for a whitespace-bearing linked path
                # is JSON-quoted WHOLE ('"linked:a b.txt"'), so the
                # qualifier can arrive inside the quoting
                decoded = _json_decoded_ack_text(raw)
                if decoded is not None \
                        and decoded.startswith(_LINKED_ACK_PREFIX):
                    qualified = decoded[len(_LINKED_ACK_PREFIX):]
            if qualified is not None:
                l_out = {p for p in linked
                         if (p, _KIND_LINKED) not in matched}
                hit = _acknowledged_paths([qualified], l_out)
                if hit:
                    matched |= {(p, _KIND_LINKED) for p in hit}
                    consumed.add(i)
                    progress = True
    return matched


class Mission:
    def __init__(self, store: MissionStore, workspace: Path, actor: str) -> None:
        # Every construction path funnels here (open's load-probe, load, the
        # CLI's --actor), so this is the single ingestion point for the
        # acting identity. record_verdict later requires acceptor_id ==
        # self.actor, so a clean actor also bounds the acceptor.
        _refuse_unprintable_identity(actor, "actor")
        self.store = store
        self.workspace = Path(workspace)
        self.actor = actor
        # Filled lazily by _own_mission_id() from the chain-protected origin;
        # immutable for the mission's life, so reading it once is sound and
        # keeps receipt loading off a per-call chain read.
        self._mission_id: str | None = None
        self._effect_index_cache: tuple[int, dict[str, str]] | None = None

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
              actuator_guards: list | None = None,
              acknowledge_unreadable: list[str] | None = None) -> "Mission":
        workspace = Path(workspace)
        # ALL THREE identities validate BEFORE the load-probe, so a refused
        # open touches nothing on disk. The actor was missing from this
        # list, and the constructor's guard sat on the wrong side of the
        # first write: on an empty workspace the load-probe raises
        # NoActiveMission before any Mission is constructed, so revision 1
        # was written carrying the rejected `written_by` -- and only THEN
        # did `cls(...)` refuse, leaving an active draft that wedged every
        # subsequent open (reproduced live). The constructor still guards
        # every other construction path; this line guards the one path that
        # writes first.
        _refuse_unprintable_identity(actor, "actor")
        _refuse_unprintable_identity(steward_ref, "steward_ref")
        _refuse_unprintable_identity(operator_ref, "operator_ref")
        # PLURALITY IS LEGAL (es#173 §3): open no longer refuses on an
        # existing active mission -- the fail-open decoy is removed not by
        # handling MultipleActiveMissions better but by making the state
        # legal. What open still refuses, checked BEFORE anything is written
        # so a refused open leaves no partial mission dir:
        #
        # 1. a duplicate mission_id (the dir already holds checkpoints);
        # 2. EpochSkew anywhere in the store -- a store this reader cannot
        #    read may hold anything, and opening beside it is still blind;
        # 3. unreadable mission dirs, unless each is explicitly quarantined:
        #    under concurrent missions a corrupt sibling's guards are
        #    silently absent from the union, so ignorable-corruption is no
        #    longer a safe posture (case row B17).
        if MissionStore(workspace / "missions" / mission_id).checkpoint_paths():
            raise CustodyError(
                f"mission {mission_id!r} already exists under this "
                "workspace; mission ids are permanent -- choose a fresh id")
        siblings, skipped = cls._discover(workspace)
        if any(s["kind"] == "EpochSkew" for s in skipped):
            raise CustodyError(
                "a mission store here CLAIMS a newer contract epoch, so "
                "this reader cannot tell whether it holds an active "
                "mission or what guards it arms. Opening beside it is "
                "blind. Read this workspace with an updated custody "
                "plugin/CLI first.")
        acked = {str(name) for name in (acknowledge_unreadable or [])}
        unknown = sorted(acked - {s["name"] for s in skipped})
        if unknown:
            raise CustodyError(
                "acknowledge_unreadable names dir(s) that are not "
                f"unreadable mission dirs here: {', '.join(unknown)} -- an "
                "acknowledgement that matches nothing is a typo, not a "
                "quarantine")
        unacked = sorted(s["name"] for s in skipped if s["name"] not in acked)
        if unacked:
            raise CustodyError(
                "unreadable mission dir(s) under this workspace: "
                + ", ".join(unacked) +
                ". Under concurrent missions an unreadable sibling's guards "
                "are silently absent from the union, so open refuses until "
                "they are repaired or explicitly quarantined "
                "(--acknowledge-unreadable <dir>, recorded in the opening "
                "checkpoint).")
        opening_notes = [f"unreadable sibling acknowledged: {s['name']}"
                         for s in sorted(skipped, key=lambda s: s["name"])]
        # Scope-overlap disclosure (§3): pattern-vs-pattern intersection is
        # decidable for this glob dialect; prose entries are reported as
        # incomparable. Disclosure, not refusal -- coexistence on shared
        # paths is the feature being built. Deterministic: sorted walk over
        # sorted siblings, so identical inputs disclose identically.
        new_patterns = sorted(e for e in (scope_in or [])
                              if _is_matchable_pattern(e))
        new_prose = sorted(e for e in (scope_in or [])
                           if not _is_matchable_pattern(e))
        for entry in sorted(siblings, key=lambda e: e["name"]):
            sib_in = entry["latest"]["manifest"]["scope"]["in"]
            sib_patterns = sorted(e for e in sib_in
                                  if _is_matchable_pattern(e))
            sib_prose = sorted(e for e in sib_in
                               if not _is_matchable_pattern(e))
            for a in new_patterns:
                for b in sib_patterns:
                    if _globs_intersect(a, b):
                        opening_notes.append(
                            f"scope overlap with {entry['name']}: "
                            f"{a} ~ {b}")
            if (scope_in or []) and sib_in:
                for e in new_prose:
                    opening_notes.append(
                        f"scope entry vs {entry['name']} incomparable "
                        f"(prose): {e}")
                for e in sib_prose:
                    opening_notes.append(
                        f"scope entry of {entry['name']} incomparable "
                        f"(prose): {e}")
        for note in opening_notes:
            # The composed disclosure embeds caller text (scope entries, dir
            # names); a multi-line entry could smuggle a machine-note line
            # into the opening checkpoint. Refusing the open is the fail-safe
            # direction, and the guard's own message names the offending line.
            _refuse_reserved_note(note)
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
                "notes": opening_notes,
                "unresolved_verdicts": [],
            },
            "receipt_ids": [],
            "written_utc": created,
            "written_by": actor,
        }
        store.write_checkpoint(checkpoint)
        return cls(store, workspace, actor)

    @classmethod
    def _discover(cls, workspace: Path) -> tuple[list[dict], list[dict]]:
        """Walk missions/ once: every ACTIVE mission and every skip.

        Returns (active, skipped). Each active entry is
        {"name", "dir", "store", "latest"} -- latest is the chain-verified
        latest checkpoint. Each skipped entry is {"name", "kind", "reason"}
        for a dir whose latest checkpoint fails to load. The ONE discovery
        walk, shared by load, open, the union assembler, and the effect
        gate, so no two surfaces can disagree about what is active."""
        workspace = Path(workspace)
        missions_root = workspace / "missions"
        active: list[dict] = []
        skipped: list[dict] = []
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
                    skipped.append({"name": mission_dir.name,
                                    "kind": type(exc).__name__,
                                    "reason": reason})
                    print(("custody: skipping unreadable mission dir " + reason)
                          .encode("ascii", "backslashreplace").decode("ascii"),
                          file=sys.stderr)
                    continue
                if latest["status"] not in ("completed", "cancelled"):
                    active.append({"name": mission_dir.name,
                                   "dir": mission_dir, "store": store,
                                   "latest": latest})
        return active, skipped

    @classmethod
    def load(cls, workspace: Path, actor: str,
             mission_id: str | None = None) -> "Mission":
        """Resolve the mission this session acts under (es#173 §1).

        Bound (mission_id given): the binding must name a mission directory
        in THIS workspace whose latest checkpoint status is an open state.
        Bound-to-nonexistent, bound-to-unreadable, bound-to-completed and
        bound-to-cancelled are four spellings of the same BindingInvalid
        refusal -- a stale binding NEVER falls through to discovery or to
        "the only active mission": silent fallback is how a session acts
        under the wrong authority politely.

        Unbound: 0 active -> NoActiveMission (unchanged); 1 active ->
        resolves to it (the single-mission workflow must not grow
        ceremony); N>1 active -> BindingRequired naming every id and both
        binding channels. It never guesses."""
        workspace = Path(workspace)
        if mission_id is not None:
            # The binding channels (--mission / ZMS_MISSION_ID) are
            # lower-provenance input: env-derived text must never steer
            # which store this session acts under beyond naming ONE id in
            # THIS workspace. Without this check a traversal id
            # (`../../ws2/missions/m-remote`) bound across workspaces --
            # the effect wrote its artifact here while the receipt landed
            # in the foreign store, a split brain neither workspace's
            # resume could explain (PR #220 refuter, finding 3). Same
            # _ID_RE the schema enforces on every manifest at open: an id
            # is a single kebab-case segment, never a path.
            if not _ID_RE.match(mission_id):
                raise BindingInvalid(
                    f"binding names {mission_id!r}, which is not a legal "
                    "mission id (single kebab-case segment, the rule "
                    "open's schema enforces) -- a binding is an "
                    "identifier, never a path. Fix or unset it "
                    "(--mission / ZMS_MISSION_ID)")
            mission_dir = workspace / "missions" / mission_id
            store = MissionStore(mission_dir)
            if not store.checkpoint_paths():
                raise BindingInvalid(
                    f"binding names mission {mission_id!r}: no such mission "
                    f"under {workspace / 'missions'}. A binding never falls "
                    "through to discovery -- fix or unset it (--mission / "
                    "ZMS_MISSION_ID)")
            try:
                latest, _ = store.load_latest()
            except (StoreError, ValueError) as exc:
                raise BindingInvalid(
                    f"binding names mission {mission_id!r}, whose store "
                    f"cannot be read ({type(exc).__name__}: {exc}). A "
                    "binding never falls through -- repair the store or "
                    "unset the binding (--mission / ZMS_MISSION_ID)"
                ) from exc
            if latest["status"] not in _OPEN_STATES:
                raise BindingInvalid(
                    f"binding names mission {mission_id!r}, whose status is "
                    f"{latest['status']!r} -- not an open state. Unset the "
                    "binding (--mission / ZMS_MISSION_ID)")
            return cls(store, workspace, actor)
        active, skipped = cls._discover(workspace)
        if not active:
            reasons = [s["reason"] for s in skipped]
            detail = (f"; skipped unreadable: {'; '.join(reasons)}"
                      if skipped else "")
            exc = NoActiveMission(
                f"no active mission under {workspace / 'missions'}{detail}")
            # STRUCTURED, not prose. A caller that needs to know WHY discovery
            # came up empty must not have to grep the message: the message
            # contains the workspace path, so a directory literally named
            # `/work/NEWER epoch migration` made a substring test report a
            # newer-epoch store in a workspace holding no stores at all
            # (measured). Callers read this attribute instead.
            exc.skipped_kinds = tuple(s["kind"] for s in skipped)
            raise exc
        if len(active) > 1:
            names = ", ".join(e["name"] for e in active)
            raise BindingRequired(
                f"{len(active)} active missions under this workspace: "
                f"{names}. Bind the session to one -- pass --mission <id> "
                "on the verb, or export ZMS_MISSION_ID=<id> for the "
                "session. Binding routes authority (where effects and "
                "notes land), never guard exposure.")
        return cls(active[0]["store"], workspace, actor)

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

    def _own_mission_id(self) -> str | None:
        """This mission's id, from the ORIGIN checkpoint, read once.

        The origin is the right source: it is chain-protected (every later
        checkpoint hashes back to it) and mission_id is immutable from open
        to close, so a forged tail cannot move it. None when underivable,
        which downgrades the check rather than inventing an answer."""
        if self._mission_id is None:
            try:
                paths = self.store.checkpoint_paths()
                origin = json.loads(paths[0].read_text(encoding="utf-8"))
                value = origin.get("mission_id")
                self._mission_id = value if isinstance(value, str) else None
            except (OSError, ValueError, IndexError, AttributeError):
                self._mission_id = None
        return self._mission_id

    def _load_receipt(self, request_id: str) -> dict | None:
        """None means UNLOADABLE -- absent, corrupt, schema-invalid, or
        BELONGING TO ANOTHER MISSION alike. A corrupt receipt must degrade to
        drift (RECEIPT-MISSING), never crash resume: crashing the recovery
        path on a mangled receipt is a denial of service by exactly the
        tampering drift detection exists to catch."""
        return self._load_receipt_checked(request_id)[0]

    def _load_receipt_checked(
            self, request_id: str
    ) -> tuple[dict | None, str | None, tuple[str, str] | None]:
        """(record, refusal reason, OPAQUE). ONE implementation of the trust rule,
        two callers: `_load_receipt` wants only the verdict, while
        `acknowledge_receipt_loss` must also tell the operator WHY -- and
        "a receipt claiming decoy.md where the chain records the real path"
        is a different incident from "no receipt at all". Splitting these
        into two readers would be a fifth paraphrase of this rule; splitting
        the RETURN VALUE is not.

        THE THIRD SLOT IS "OPAQUE", not "skewed": `(KIND, message)` for a
        receipt that is PRESENT and that this reader cannot verify. Two kinds
        share that state exactly -- `NEWER-EPOCH` (no validator for it) and
        `UNREADABLE` (I/O refused it) -- and both must stay out of the loss
        bucket, whose only exit destroys the id. The kind is carried rather
        than inferred so the marker and the operator message can name the real
        condition; routing an I/O failure through the epoch wording would be
        mis-stated enforcement, which this contract has had to correct five
        times already."""
        path = self.store.receipt_path(request_id)
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            return None, "no receipt file at the id's content-addressed path", None
        except ValueError as exc:
            return None, f"receipt is not parseable JSON ({type(exc).__name__})", None
        except OSError as exc:
            # PRESENT BUT UNREADABLE IS NOT LOST. Only FileNotFoundError was
            # caught, so a receipt that exists and cannot be read -- wrong
            # permissions, a directory planted at its path, a failing disk --
            # escaped as an uncaught OSError and crashed `resume()` and
            # `continuity_breaks()` outright (measured: IsADirectoryError).
            # That is the denial of service this method's own docstring
            # forbids: the recovery path must not be killable by the tampering
            # drift detection exists to catch.
            #
            # It is reported OPAQUE, never as loss. The loss marker's only
            # exit permanently retires the id, and an I/O failure is not
            # evidence the receipt is gone -- retiring on a transient
            # permission error would destroy live coverage exactly as the
            # newer-epoch case would (round 10).
            return None, None, (
                "UNREADABLE",
                f"receipt file is present but could not be read "
                f"({type(exc).__name__}: {exc.strerror or exc}). This reader "
                f"cannot verify the artifact and cannot conclude the receipt "
                f"is lost -- repair access and re-run resume")
        errors = validate_record(record)
        if errors:
            # A NEWER-EPOCH RECEIPT IS NOT A LOST ONE. During a rollout a
            # `receipt@2` can sit under a `checkpoint@1` chain this reader
            # still handles, so the checkpoint path never consults the epoch
            # table and the receipt fails validation as an unknown kind.
            # Reported as loss, that receipt reaches `acknowledge_receipt_loss`
            # -- which PERMANENTLY RETIRES the id. Measured before this check:
            # `resume()` emitted `RECEIPT-MISSING:req-1` for a receipt that was
            # present, intact and merely newer. Destroying live coverage
            # because this reader is old is the worst outcome available here.
            skew = epoch_skew_anywhere(record, "receipt")
            if skew:
                return None, None, ("NEWER-EPOCH", skew)
            return None, f"receipt fails receipt@1 validation: {errors[:2]}", None
        # A receipt whose own request_id disagrees with the content-addressed
        # name it is stored under is malformed by construction -- never a
        # trustworthy source for a claim about that id.
        if record.get("request_id") != request_id:
            return None, (
                f"receipt names request_id {record.get('request_id')!r}, but it "
                f"is stored under the content-addressed name for {request_id!r}"), None
        # ... and neither is a receipt that says it belongs to a DIFFERENT
        # mission. request_id uniqueness is per-mission, so two missions can
        # legitimately mint the same id; the receipt path is content-addressed
        # on the id alone, so a foreign receipt dropped in this mission's
        # receipts dir sits exactly where this mission looks. Schema validity
        # and id agreement were both satisfied by such a copy, and
        # `acknowledge_receipt_loss` would then read it as RESTORED coverage
        # -- affirming continuity from a record that documents someone else's
        # write. The record names its own mission; believe it.
        own = self._own_mission_id()
        if own is not None and record.get("mission_id") != own:
            return None, (
                f"receipt belongs to mission {record.get('mission_id')!r}, not "
                f"{own!r} -- NOT trusted"), None
        # ... and mission_id is unique only WITHIN a workspace, so that check
        # alone still admits a receipt copied between two workspaces that
        # both happen to run a mission of the same name -- an ordinary
        # collision (`deploy`, `main`), not an exotic one. Measured: with the
        # donor's receipt naming a decoy path whose bytes also exist in the
        # victim workspace, `resume()` returned CLEAN while the victim's real
        # artifact sat on disk reading "TAMPERED". Drift detection silenced
        # by a file copy is the worst outcome this contract has.
        #
        # The chain is the authority on WHICH PATH (the same doctrine
        # scope_consistency and the census already apply), so a receipt that
        # disagrees with the chained effect note is not this id's receipt,
        # whoever wrote it. When the chain cannot derive a path the check is
        # skipped rather than guessed -- underivable is not disagreement.
        #
        # HOW FAR THIS ACTUALLY REACHES, measured both ways: an INTERIOR note
        # cannot be rewritten (the hash chain breaks and the store is skipped
        # entirely), but the TAIL checkpoint is unsealed, so for an id
        # introduced by the LATEST revision a writer who can replace the
        # receipt can also rewrite that note to match the decoy. The binding
        # raises the bar without closing that case; it is the es#118 residue,
        # and the tail anchor closes it. Disclosed in SECURITY.md rather than
        # papered over here.
        chained = self._effect_path_index().get(request_id)
        if chained is not None and record.get("artifact_path") != chained:
            return None, (
                f"present receipt claims {record.get('artifact_path')!r}, "
                f"chain records {chained!r} -- NOT trusted"), None
        return record, None, None

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
                return _first_effect_note(notes[len(prev_notes):], kind)
            prev_ids, prev_notes = ids, notes
        return None

    def _effect_path_index(self) -> dict[str, str]:
        """Every chain-bound request id -> the path its admitting revision
        recorded, built in ONE pass over the chain.

        Same rule as `_historical_effect_path`, and deliberately sharing
        `_first_effect_note` with it so the two cannot drift: a reader that
        paraphrases this rule is a reader that will eventually disagree with
        it, and every disagreement is a defect (sixteen of them on the
        census, merge-gate rounds 1-2).

        Why it exists: the per-id method rescans from checkpoint 1 each time,
        so asking it about every id in a mission is quadratic -- an estate
        walk over long-running missions with thousands of revisions becomes
        millions of JSON parses. Callers that want ALL the paths ask once.
        Ids with no derivable path are ABSENT (never mapped to a guess), so
        `.get(rid)` returns None exactly where the per-id method does."""
        # CACHED against the checkpoint COUNT, not time: the chain is
        # append-only, so a count that has not moved cannot have new ids in
        # it, and a count that has moved rebuilds. Without this, binding
        # `_load_receipt` to the chain (round 7) would have reintroduced the
        # quadratic walk round 3 removed -- resume() loads every receipt.
        paths = self.store.checkpoint_paths()
        if self._effect_index_cache is not None \
                and self._effect_index_cache[0] == len(paths):
            return self._effect_index_cache[1]
        index: dict[str, str] = {}
        prev_ids: list[str] = []
        prev_notes: list[str] = []
        for cp_path in paths:
            record = json.loads(cp_path.read_text(encoding="utf-8"))
            ids = record["receipt_ids"]
            notes = record["state"]["notes"]
            fresh = [rid for rid in ids if rid not in prev_ids]
            if fresh:
                path = _first_effect_note(notes[len(prev_notes):])
                if path is not None:
                    for rid in fresh:
                        index.setdefault(rid, path)
            prev_ids, prev_notes = ids, notes
        self._effect_index_cache = (len(paths), index)
        return index

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

    def _resumption_status(self) -> str:
        """The lifecycle state a mission returns to once nothing is left
        unresolved -- `draft` if it has never been approved, else `active`.

        NOT the constant "active". Every path back from `reopened` used that
        constant, which silently assumes the mission was active before it
        reopened. A DRAFT mission can reopen -- `record_effect` is legal in
        draft, so a tampered artifact, a lost receipt or a receipt relabelled
        to a newer epoch all reach `resume()` before approval -- and each exit
        then promoted it to `active` WITHOUT THE APPROVAL TRANSITION. Measured
        on all four exits: afterwards `approve()` refuses ("status is
        'active', expected 'draft'") while `begin_verification()` proceeds, so
        the draft-to-active gate is not merely skipped but rendered
        unreachable. An authority transition that can be crossed by damaging a
        file is not a gate.

        The chain is the authority, as everywhere else here: a mission that
        has never been approved has no checkpoint whose status is anything but
        `draft` or `reopened`. Nothing is read from a caller-supplied string.
        ONE implementation (`_approved_by_chain`), shared with the union
        assembler and the sibling-drift discriminator (es#173), so the three
        readers of "was this ever approved" cannot drift apart."""
        return "active" if _approved_by_chain(self.store) else "draft"

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

    def _acknowledged_unreadable(self, latest: dict) -> set[str]:
        """Dir names whose union degradation this mission's chain has
        acknowledged (machine note, reserved prefix -- so narrative cannot
        forge the discharge). Permanent for the mission's life, like every
        note: the quarantine judgement was recorded once and holds."""
        prefix = "unreadable-acknowledged: "
        return {note[len(prefix):] for note in latest["state"]["notes"]
                if note.startswith(prefix)}

    def _effect_union_entries(
            self, latest: dict,
            acknowledge_unreadable: tuple | list = (),
    ) -> tuple[list[dict], list[str]]:
        """Assemble the union for an `effect` (es#173, OD-2) and enforce the
        B23 degradation rule. Returns (entries, fresh_acknowledgements).

        Every ACTIVE mission joins as {"name", "store", "authority",
        "approved"} -- including this one: complete mediation has no
        self-exemption. A sibling whose store cannot be read or whose
        manifest fails verification is a DEGRADED union: unlike the hook
        (which must never brick the tool loop), effect CAN refuse without
        bricking anything, so it does -- UnionDegraded, until the sibling
        is repaired, completed/cancelled by an updated reader, or
        explicitly acknowledged (recorded in this mission's chain via the
        reserved 'unreadable-acknowledged: ' machine note, so the
        acknowledgement persists and cannot be forged by narrative)."""
        own_name = self.store.mission_dir.name
        active, skipped = Mission._discover(self.workspace)
        degraded = [{"name": s["name"], "reason": s["reason"]}
                    for s in skipped]
        entries: list[dict] = []
        for e in active:
            if e["name"] == own_name:
                entries.append({"name": own_name, "store": self.store,
                                "authority":
                                    latest["manifest"]["authority"],
                                "approved":
                                    _approved_by_chain(self.store)})
                continue
            sibling = Mission(e["store"], self.workspace, self.actor)
            try:
                sib_latest = sibling.status()
            except (StoreError, ValueError, CustodyError) as exc:
                degraded.append({
                    "name": e["name"],
                    "reason": f"{type(exc).__name__}: {exc}"})
                continue
            entries.append({"name": e["name"], "store": e["store"],
                            "authority":
                                sib_latest["manifest"]["authority"],
                            "approved": _approved_by_chain(e["store"])})
        acked_chain = self._acknowledged_unreadable(latest)
        acked_now = {str(name) for name in (acknowledge_unreadable or ())}
        degraded_names = {d["name"] for d in degraded}
        unknown = sorted(acked_now - degraded_names - acked_chain)
        if unknown:
            raise CustodyError(
                "acknowledge_unreadable names dir(s) that are not degraded "
                f"here: {', '.join(unknown)} -- an acknowledgement that "
                "matches nothing is a typo, not a quarantine")
        unacked = sorted(d["name"] for d in degraded
                         if d["name"] not in acked_chain
                         and d["name"] not in acked_now)
        if unacked:
            detail = "; ".join(d["reason"] for d in degraded
                               if d["name"] in unacked)
            raise UnionDegraded(
                "effect refused: sibling mission dir(s) "
                + ", ".join(unacked) +
                " cannot be read, so their guards are silently absent from "
                "the union (case row B23). Repair them, resolve them with "
                "an updated reader, or acknowledge explicitly "
                "(--acknowledge-unreadable <dir>; recorded in this "
                f"mission's chain). Detail: {detail}")
        fresh = sorted((acked_now & degraded_names) - acked_chain)
        return entries, fresh

    def _append_sibling_touches(self, entries: list[dict],
                                artifact_relpath: str, request_id: str,
                                after_sha256: str) -> None:
        """The crossing record (es#173 section 4c, FATAL-4): when this
        effect touches a path an ACTIVE sibling has receipted, append one
        advisory JSON line to that sibling's sibling-touch.jsonl -- the
        guard-log analog: append-only, OUTSIDE the chain, chain
        byte-identity preserved, never a write into the sibling's chain
        (binding routes where notes land; this mission's actor holds no
        authority there). Best-effort exactly like the guard-log append: a
        failed append never blocks the effect but is loud on stderr. It is
        ADVISORY: ground truth for detection is the resume-time receipt
        scan, so a lost or suppressed entry cannot hide a crossing -- it
        only costs the sibling's next resume the early hint."""
        own_name = self.store.mission_dir.name
        rel = artifact_relpath.replace("\\", "/")
        for entry in entries:
            if entry["name"] == own_name:
                continue
            try:
                touched = any(
                    isinstance(r, dict)
                    and isinstance(r.get("artifact_path"), str)
                    and _same_artifact(r["artifact_path"], rel)
                    for r in entry["store"].load_receipts())
                if not touched:
                    continue
                line = json.dumps({
                    "utc": now_utc(),
                    "actor": self.actor,
                    "session_id": "",
                    "from_mission": own_name,
                    "receipt_id": request_id,
                    "artifact_path": rel,
                    "after_sha256": after_sha256,
                }, sort_keys=True)
                with open(entry["store"].mission_dir
                          / "sibling-touch.jsonl", "a",
                          encoding="utf-8") as handle:
                    handle.write(line + "\n")
            except Exception as exc:  # noqa: BLE001
                print(("custody: sibling-touch append failed for "
                       f"{entry['name']} ({type(exc).__name__}: {exc}); "
                       "the effect stands -- detection falls back to the "
                       "sibling's resume-time receipt scan")
                      .encode("ascii", "backslashreplace").decode("ascii"),
                      file=sys.stderr)

    def _log_effect_matches(self, matches: list[dict],
                            artifact_relpath: str) -> None:
        """Guard-log the effect verb's matches into each matching mission's
        dir, mirroring the gate's audit trail (tool_name 'effect').
        Best-effort: the audit append is not verdict-bearing."""
        for row in matches:
            entry = {
                "utc": now_utc(),
                "actor": self.actor,
                "session_id": "",
                "harness": "effect",
                "mode": row["mode"],
                "decision": row["decision"],
                "rule": row["rule"],
                "tool_name": "effect",
                "command_preview": "",
                "file_path": artifact_relpath,
            }
            target = (self.workspace / "missions" / row["mission"]
                      / "guard-log.jsonl")
            try:
                with open(target, "a", encoding="utf-8") as handle:
                    handle.write(json.dumps(entry, sort_keys=True) + "\n")
            except Exception as exc:  # noqa: BLE001
                print(f"custody: guard-log append failed for "
                      f"{row['mission']} ({type(exc).__name__}: {exc}); "
                      f"verdict {row['decision']} stands but was not "
                      "logged", file=sys.stderr)

    def record_effect(self, artifact_relpath: str, content: str,
                       request_id: str, *,
                       acknowledge_unreadable: tuple | list = ()) -> dict:
        latest, path = self.store.load_latest()
        self._verify_manifest(latest)
        if latest["status"] not in _EFFECT_STATES:
            raise IllegalTransition(f"cannot record_effect: status is {latest['status']!r}")
        # A fresh effect on an artifact awaiting re-coverage discharges that
        # obligation -- that is exactly what RECOVER asks for.
        unresolved = latest["state"]["unresolved_verdicts"]
        status = latest["status"]
        remaining = None
        recover = _find_marker(unresolved, "RECOVER:", artifact_relpath)
        # BEFORE any write, a refused mint must be side-effect free (the
        # opening-actor lesson -- reads are fine, writes are not). And the
        # guard yields to an outstanding RECOVER obligation: a historical
        # control-char record whose receipt was lost leaves a RECOVER
        # marker whose ONLY exit is a fresh effect on that same artifact --
        # refusing it here would strand the mission 'reopened' forever, a
        # block with no legal discharge, the RECOVER-UNKNOWN wedge this
        # contract already rejected once. Recovery re-covers an artifact
        # the record ALREADY carries; only genuinely NEW paths are refused.
        if recover is None:
            _refuse_unrecordable_artifact_path(artifact_relpath)
        # es#173 OD-2: effect IS the file write, so it runs union guard
        # evaluation BEFORE _write_effect. A block refuses side-effect-free
        # (nothing written, no receipt minted -- the same
        # refuse-before-mutate posture as the idempotency guard), naming
        # every matching (mission_id, rule) pair; audit-mode matches are
        # allowed and logged. A RECOVER discharge is deliberately NOT
        # exempt: a blocked recovery discharges through the (unblockable)
        # amend channel of each matching mission, not through a hole in the
        # mediation -- amend being unblockable is what keeps this legal.
        entries, fresh_acks = self._effect_union_entries(
            latest, acknowledge_unreadable)
        from custody_gate import evaluate_effect_union
        matches = evaluate_effect_union(entries, artifact_relpath)
        if matches:
            self._log_effect_matches(matches, artifact_relpath)
        blocking = [m for m in matches if m["decision"] == "block"]
        if blocking:
            pairs = "; ".join(f"mission={m['mission']} rule={m['rule']}"
                              for m in blocking)
            raise CustodyError(
                f"effect blocked by custody guard(s): {pairs}. Nothing was "
                "written and no receipt was minted. Discharge is "
                "PER-MISSION: an amend recorded in one mission discharges "
                "that mission's rule only -- bind to each matching mission "
                "(--mission <id>) and change the rule via `amend "
                "--guards-file`, or `amend --guard-mode audit` to retire "
                "that mission's guard set, or stop. `note` and `amend` "
                "remain unblockable by design (OD-2): record the "
                "escalation there.")
        # Only now -- with the union verdict in hand -- does anything touch
        # the chain. The fresh-quarantine checkpoints used to land BEFORE
        # evaluation, so a blocked effect mutated the chain while its
        # refusal claimed "Nothing was written" (PR #220 refuter, finding
        # 4: checkpoint count 2 -> 3 on a block, measured). Evaluation is a
        # pure read over `entries`, so ordering it first costs nothing; the
        # quarantine judgement still becomes chain state BEFORE the write
        # it licenses, one machine-note checkpoint per dir.
        for name in fresh_acks:
            self._write_next(latest, path, status=latest["status"],
                              note=f"unreadable-acknowledged: {name}")
            latest, path = self.store.load_latest()
        receipt = self._write_effect(latest, artifact_relpath, content, request_id)
        if recover is not None:
            remaining = [m for m in unresolved if m != recover]
            if status == "reopened" and not remaining:
                status = self._resumption_status()
        self._write_next(latest, path, status=status, add_receipt_id=request_id,
                          unresolved_verdicts=remaining,
                          note=f"effect: {artifact_relpath}")
        self._append_sibling_touches(entries, artifact_relpath, request_id,
                                     receipt["after_sha256"])
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
                # Documented disarm is actuator_guards=None alone
                # (README / validator). Leaving guard_mode behind made
                # _write_next reject the result (es#137).
                if guard_mode is _UNSET:
                    manifest["authority"].pop("guard_mode", None)
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

    def orphaned_retired_receipts(self) -> list[dict]:
        """Ids whose loss was acknowledged but whose receipt file is present.

        Retirement is permanent and `_write_effect` refuses to reuse a retired
        id, so a receipt sitting at a retired id's path is coverage nothing
        will ever read: the chain says the id is gone, the filesystem says the
        receipt is there. Until this existed the condition was ENTIRELY
        SILENT -- `resume()` returned `[]` and `status` said nothing, measured.

        That silence is what made the retirement race destructive rather than
        merely racy. The window itself cannot be closed without cross-process
        locking this contract does not have (see SECURITY.md); what CAN be
        guaranteed is that landing in it leaves a mark somebody can find.

        Read-only, and it raises NOTHING, for the same reason
        `continuity_breaks` does not: a retirement cannot be undone, so an
        obligation here would be a marker with no exit. Surfaced, not
        enforced.
        """
        latest, _ = self.store.load_latest()
        found = []
        for request_id in sorted(self._retired_receipt_ids(latest)):
            path = self.store.receipt_path(request_id)
            if path.exists():
                found.append({"request_id": request_id,
                              "receipt_path": str(path),
                              "note": ("receipt present for an id the chain "
                                       "retired; it covers nothing and the "
                                       "id can never be reused")})
        return found

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

    def _scan_sibling_receipts(self, rel: str, current_sha: str) -> list[dict]:
        """receipt@1 records in OTHER mission stores whose artifact_path
        names this artifact and whose after_sha256 equals the CURRENT
        content hash -- the es#173 section 4(a) detection scan. Every field
        it needs already exists on receipt@1; nothing is minted at effect
        time that the schema must carry (OD-3: zero schema change).

        ANY status, not only active -- the verification-report correction
        to the design's section 4(a) wording: the adjudication's
        "resume-time scan of sibling receipt stores" carries no active-only
        narrowing, and a sibling that completed or was cancelled between
        its write and this resume must still explain the drift. Best-effort
        per store: an unreadable sibling contributes no evidence, never a
        crash -- the recovery path must not be killable (the
        _load_receipt doctrine, applied to foreign stores)."""
        own_name = self.store.mission_dir.name
        missions_root = self.workspace / "missions"
        found: list[dict] = []
        if not missions_root.is_dir():
            return found
        for mission_dir in sorted(missions_root.iterdir()):
            if not mission_dir.is_dir() or mission_dir.name == own_name:
                continue
            store = MissionStore(mission_dir)
            try:
                receipts = store.load_receipts()
            except Exception as exc:  # noqa: BLE001
                print(("custody: sibling receipt scan skipped "
                       f"{mission_dir.name} ({type(exc).__name__}: {exc})")
                      .encode("ascii", "backslashreplace").decode("ascii"),
                      file=sys.stderr)
                continue
            for record in receipts:
                if not isinstance(record, dict) or validate_record(record):
                    continue  # only well-formed receipt@1 counts
                if _same_artifact(str(record.get("artifact_path")), rel)                         and record.get("after_sha256") == current_sha:
                    found.append({"mission": mission_dir.name,
                                  "receipt_id": record.get("request_id"),
                                  "record": record})
        return found

    def _classify_sibling_drift(
            self, latest: dict, rel: str, current_sha: str,
    ) -> tuple[dict | None, list[str]]:
        """The FATAL-3 authorization discriminator (es#173 section 4b).

        Hash-match alone is a self-serve audit-downgrade: open() takes
        unverified refs, so whoever caused unauthorized drift could open a
        throwaway sibling, effect the tampered bytes, and self-mint the
        laundering receipt. DRIFT-SIBLING therefore requires ALL of:
        (1) a sibling receipt@1 hash match (the scan);
        (2) the sibling operator-approved BY THE CHAIN TEST
            (_approved_by_chain) -- never latest-status, so a
            never-approved mission wedged in `reopened` launders nothing;
        (3) an explicit cross-mission authorization amendment in THIS
            mission's own chain, naming the sibling mission id as a
            whole token (_amendment_names_mission -- never a raw
            substring) and the path or a pattern covering it
            (_amendment_names).

        Any leg missing -> (None, evidence): plain drift at today's
        severity with the sibling receipt reported as evidence. The
        discriminator gates the severity downgrade, never the information
        -- resume always says what it found."""
        candidates = self._scan_sibling_receipts(rel, current_sha)
        evidence: list[str] = []
        amendments = latest["manifest"]["authority"]["amendments"]
        for candidate in candidates:
            mission_name = candidate["mission"]
            approved = _approved_by_chain(
                MissionStore(self.workspace / "missions" / mission_name))
            authorized = any(
                isinstance(a, dict) and isinstance(a.get("text"), str)
                and _amendment_names_mission(a["text"], mission_name)
                and _amendment_names(a["text"], rel)
                for a in amendments)
            if approved and authorized:
                return candidate, []
            legs = []
            if not approved:
                legs.append("sibling not operator-approved (chain test)")
            if not authorized:
                legs.append("no cross-mission authorization amendment "
                            "in this mission's chain")
            evidence.append(
                f"{rel} matches sibling {mission_name} receipt "
                f"{candidate['receipt_id']} -- NOT reclassified: "
                + "; ".join(legs))
        return None, evidence

    def acknowledge_sibling(self, artifact_relpath: str) -> int:
        """The only exit for a DRIFT-SIBLING marker (es#173 section 4):
        acknowledge a sanctioned sibling write, recorded in THIS mission's
        chain by this mission's own bound session as the reserved machine
        note `sibling-touched: <path> by <mission> receipt <id>`. Not
        `acknowledge_loss` -- nothing was lost -- and not `reconcile` --
        nothing needs rewriting.

        The three discriminator legs are RE-VERIFIED here, at the moment
        the downgrade is consummated: a marker raised by an earlier resume
        must not discharge against a store that has since changed."""
        latest, path = self.store.load_latest()
        self._verify_manifest(latest)
        if latest["status"] != "reopened":
            raise IllegalTransition(
                f"cannot acknowledge_sibling: status is "
                f"{latest['status']!r}, expected 'reopened'")
        norm = artifact_relpath.replace("\\", "/")
        unresolved = latest["state"]["unresolved_verdicts"]
        marker = _find_marker(unresolved, "DRIFT-SIBLING:", norm)
        if marker is None:
            raise CustodyError(
                f"no DRIFT-SIBLING marker for {artifact_relpath!r}")
        rel = marker[len("DRIFT-SIBLING:"):]
        target = self.workspace / rel
        current_sha = sha256_file(target) if target.exists() else None
        hit = None
        if current_sha is not None:
            hit, _evidence = self._classify_sibling_drift(
                latest, rel, current_sha)
        if hit is None:
            raise CustodyError(
                "sibling attribution no longer verifies for "
                f"{rel!r} (content moved on, the sibling receipt vanished, "
                "or a discriminator leg no longer holds) -- re-run resume: "
                "it re-classifies the path at its current severity, "
                "replacing this stale DRIFT-SIBLING marker (a "
                "no-longer-attributable path becomes a plain "
                "RECONCILIATION finding for `reconcile`; content that now "
                "verifies drops the marker)")
        remaining = [m for m in unresolved if m != marker]
        status = "reopened" if remaining else self._resumption_status()
        new = self._write_next(
            latest, path, status=status, unresolved_verdicts=remaining,
            note=(f"sibling-touched: {rel} by {hit['mission']} receipt "
                  f"{hit['receipt_id']}"))
        return new["revision"]

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
        current_by_key: dict[str, tuple[str, dict | None, str | None]] = {}
        missing: list[str] = []
        unplaceable_opaque: list[tuple[str, str]] = []
        for request_id in latest["receipt_ids"]:
            receipt, _refusal, opaque = self._load_receipt_checked(request_id)
            # KIND, not a boolean. Both opaque kinds behave identically here
            # (present, unverifiable, never "lost"), and differ only in the
            # marker and message the operator is handed.
            kind = opaque[0] if opaque else None
            # NOT missing, and NOT clean: this reader cannot read the receipt,
            # so it cannot verify the artifact -- but the receipt is present
            # and may be perfectly good. Which skewed ids get a MARKER is
            # decided AFTER the per-artifact winners are known (see below).
            #
            # A SKEWED RECEIPT STILL TAKES ITS SLOT. Skipping it here left the
            # SUPERSEDED older receipt authoritative for the same artifact, so
            # resume compared live content against an obsolete hash and
            # reported RECONCILIATION -- a false drift diagnosis whose remedy,
            # `reconcile`, would OVERWRITE content the newer receipt governs
            # (measured: artifact reading "NEW", resume reporting drift).
            # Claiming the slot as an OPAQUE entry supersedes the stale
            # receipt without asserting anything this reader cannot check.
            rel = (receipt["artifact_path"] if receipt is not None
                   else self._historical_effect_path(request_id))
            if rel is None:
                if kind:
                    # Unattributable but NOT lost: a receipt that is merely
                    # too new must never fall into the loss bucket, whose
                    # only exit destroys the id.
                    if request_id not in [r for r, _k in unplaceable_opaque]:
                        unplaceable_opaque.append((request_id, kind))
                    continue
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
            current_by_key[key] = (request_id, receipt, kind)
        # ONLY THE AUTHORITATIVE RECEIPT FOR AN ARTIFACT GETS A MARKER. Marking
        # every skewed id in receipt_ids meant a SUPERSEDED historical receipt
        # -- one the chain has already replaced with a readable successor --
        # reopened the mission and wedged it there: the current receipt
        # verifies the artifact, nothing is wrong, and the marker can never
        # clear because the old file is still relabelled (measured: `old@2`
        # followed by a readable `new@1` left the mission reopened with
        # RECEIPT-NEWER-EPOCH:req-old). Historical skew stays visible in the
        # census, which reports every id in receipt_ids; `resume` speaks only
        # about what currently governs an artifact.
        opaque_ids = [(rid, k) for rid, _r, k in current_by_key.values()
                      if k] + unplaceable_opaque
        mismatched: list[str] = []
        current_sha_by_rel: dict[str, str] = {}
        for request_id, receipt, kind in current_by_key.values():
            if kind:
                # Unverifiable, and honestly so: without the receipt's hash
                # this reader cannot say the artifact drifted OR that it is
                # clean. RECEIPT-NEWER-EPOCH already carries that, and NOT
                # emitting RECONCILIATION here is what keeps `reconcile`
                # unavailable for this path -- it refuses without a marker.
                continue
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
                if actual is not None:
                    current_sha_by_rel[rel] = actual
        mismatched.sort()
        missing.sort()
        opaque_ids.sort()
        # es#173 section 4: a drifted artifact whose CURRENT bytes match a
        # sibling receipt@1 is either a sanctioned crossing (all three
        # discriminator legs -> DRIFT-SIBLING, reconciled by
        # acknowledge_sibling) or plain drift WITH the sibling receipt
        # reported as evidence (any leg missing). The discriminator gates
        # the severity downgrade, never the information.
        sibling_class: dict[str, dict] = {}
        sibling_evidence: list[str] = []
        for rel in mismatched:
            current_sha = current_sha_by_rel.get(rel)
            if current_sha is None:
                continue
            hit, evidence = self._classify_sibling_drift(
                latest, rel, current_sha)
            if hit is not None:
                sibling_class[rel] = hit
            else:
                sibling_evidence.extend(evidence)
        findings = ([f"DRIFT-SIBLING:{rel}" if rel in sibling_class else rel
                     for rel in mismatched]
                    + [f"RECEIPT-MISSING:{rid}" for rid in missing]
                    + [f"RECEIPT-{k}:{rid}" for rid, k in opaque_ids])
        # THE SKEW MARKER'S EXIT LIVES HERE. Its remedy is "update the reader
        # (or repair a false relabel) and re-run resume" -- no new verb, since
        # `reconcile` clears drift and `acknowledge_receipt_loss` retires an
        # id, and neither is right for a receipt that was never lost. Without
        # this, the marker persisted forever and the mission stayed `reopened`
        # with nothing able to clear it (measured) -- a workspace stranded
        # with no verb to resolve it, which is the exact objection this
        # contract raises against inverting the gate's fail-open posture.
        live_opaque = {f"RECEIPT-{k}:{rid}" for rid, k in opaque_ids}
        stale_skew = [m for m in latest["state"]["unresolved_verdicts"]
                      if (m.startswith("RECEIPT-NEWER-EPOCH:")
                          or m.startswith("RECEIPT-UNREADABLE:"))
                      and m not in live_opaque]
        # THE STALE SIBLING MARKER'S EXIT LIVES HERE (PR #220 refuter,
        # finding 2). acknowledge_sibling re-verifies attribution against
        # CURRENT bytes, so a DRIFT-SIBLING marker whose path had since
        # moved on (operator edit, reconcile) could never discharge: ack
        # refused forever, reconcile cleared only RECONCILIATION, and the
        # mission wedged in `reopened` with begin_verification refusing
        # (measured). Resume therefore re-classifies the path at its
        # CURRENT severity: a still-attributable path keeps its marker, a
        # no-longer-attributable one becomes a plain RECONCILIATION
        # finding (the mismatched loop below raises it), and a path whose
        # content now verifies drops the marker entirely.
        live_sibling = {f"DRIFT-SIBLING:{rel}" for rel in sibling_class}
        stale_sibling = [m for m in latest["state"]["unresolved_verdicts"]
                         if m.startswith("DRIFT-SIBLING:")
                         and m not in live_sibling]
        if not findings and not stale_skew and not stale_sibling:
            return []
        unresolved = [m for m in latest["state"]["unresolved_verdicts"]
                      if m not in stale_skew and m not in stale_sibling]
        for rel in mismatched:
            marker = (f"DRIFT-SIBLING:{rel}" if rel in sibling_class
                      else f"RECONCILIATION:{rel}")
            if marker not in unresolved:
                unresolved.append(marker)
        for rid in missing:
            marker = f"RECEIPT-MISSING:{rid}"
            if marker not in unresolved:
                unresolved.append(marker)
        for rid, kind in opaque_ids:
            # Deliberately NOT a RECEIPT-MISSING marker: that marker's only
            # exit is acknowledge_receipt_loss, which retires the id forever.
            # The exit for these is repairing what made the receipt opaque --
            # update the reader, or restore access to the file.
            marker = f"RECEIPT-{kind}:{rid}"
            if marker not in unresolved:
                unresolved.append(marker)
        # A run that ONLY cleared stale skew markers is not drift: if nothing
        # is left unresolved the mission returns to `active`, or the reader
        # update that fixed the receipt would leave it reopened forever.
        if findings:
            status, note = "reopened", f"drift detected: {', '.join(findings)}"
            for rel, hit in sorted(sibling_class.items()):
                note += (f"; sibling receipt: {rel} matches "
                         f"{hit['mission']} receipt {hit['receipt_id']}")
            for line in sibling_evidence:
                note += f"; sibling receipt evidence: {line}"
            for m in stale_sibling:
                note += (f"; stale sibling marker superseded: {m} "
                         "re-classified at current severity")
        else:
            status = ("reopened" if unresolved
                      else self._resumption_status())
            cleared = []
            if stale_skew:
                cleared.append(
                    "previously unverifiable receipt(s) now readable: "
                    + ", ".join(m.split(":", 1)[1] for m in stale_skew))
            if stale_sibling:
                cleared.append(
                    "stale sibling marker(s) discharged, content verifies: "
                    + ", ".join(m.split(":", 1)[1] for m in stale_sibling))
            note = "; ".join(cleared)
        self._write_next(latest, path, status=status,
                          unresolved_verdicts=unresolved, note=note)
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
        next_status = (self._resumption_status() if not remaining
                       else "reopened")
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
        # ONE SNAPSHOT, read once and used for every decision below. The
        # first version of this guard read the receipt here and AGAIN for the
        # restoration check, discarding the second read's skew -- so a
        # future-format receipt published between the two reads passed the
        # guard and was then retired anyway. A destructive verb must not
        # decide from two different observations of the same file.
        #
        # REFUSE THE DESTRUCTIVE VERB ON A SKEWED RECEIPT, and refuse it
        # BEFORE the marker check so the operator gets the real reason rather
        # than "no receipt-loss marker". Retiring the id would discard
        # coverage an updated reader can still verify, and this verb has no
        # inverse.
        receipt, refusal, opaque = self._load_receipt_checked(request_id)
        if opaque:
            # PRESENT BUT UNVERIFIABLE IS NOT LOST, whichever kind. Retiring
            # discards coverage that a newer reader -- or a repaired
            # permission -- can still verify, and this verb has no inverse.
            kind, detail = opaque
            raise CustodyError(
                f"refusing to retire {request_id!r}: its receipt is present "
                f"and this reader cannot verify it ({kind}), so it cannot be "
                f"concluded lost. Resolve that first, then re-run `resume`. "
                f"Detail: {detail}")
        marker = f"RECEIPT-MISSING:{request_id}"
        unresolved = latest["state"]["unresolved_verdicts"]
        if marker not in unresolved:
            raise CustodyError(f"no receipt-loss marker for {request_id!r}")
        remaining = [m for m in unresolved if m != marker]
        next_status = (self._resumption_status() if not remaining
                       else "reopened")

        recorded_path = self._historical_effect_path(request_id)
        # Deliberately raw equality, NOT _same_artifact: everywhere else the
        # question is "does this write satisfy that obligation", where two
        # spellings of one file must match. Here the question is "is this the
        # receipt the chain recorded", and a receipt that reappears respelled
        # is not provably the original -- the safe answer is to retire the id
        # and let a fresh effect re-establish coverage honestly. Strictness
        # here is intentional, not an oversight.
        # COMPARE AND SWAP, IMMEDIATELY BEFORE THE DESTRUCTIVE WRITE. One
        # snapshot fixed an earlier defect -- deciding the guard from one read
        # and the restoration from another -- but it does not close the window
        # between the snapshot and the commit, and this method spends that
        # window walking the whole chain TWICE (`_historical_effect_path` and
        # `_resumption_status`, the latter added while fixing the draft
        # promotion, which measurably widened it). A receipt published in
        # there was retired anyway.
        #
        # This is NOT a return to deciding from two reads: nothing below reads
        # the recheck. Any difference at all REFUSES, so the observation can
        # only cost this verb its write, never redirect it. Retirement is
        # permanent and has no inverse; declining a racy one costs a re-run.
        recheck, _, recheck_opaque = self._load_receipt_checked(request_id)
        if recheck_opaque is not None or recheck != receipt:
            raise CustodyError(
                f"refusing to retire {request_id!r}: its receipt changed "
                f"between the check and the write, so this retirement would "
                f"decide from an observation that is already stale. Nothing "
                f"was retired; re-run `resume` and try again."
                + (f" Detail: {recheck_opaque[1]}" if recheck_opaque else ""))
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
            # The loader already decided WHY, and it is the only place that
            # rule lives -- recomputing the explanation here is how the two
            # would eventually disagree. "Receipt unloadable" alone would
            # also flatten a planted decoy into a missing file, losing the
            # one sentence that tells an operator this was an ATTACK and not
            # a crash.
            why = refusal or "receipt unloadable"
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

    def _link_count(self, rel: str) -> int | None:
        """How many names this artifact has on disk, or None if unknowable.

        A hard link is not a link to a path -- it is a second name for one
        inode -- so `_resolved_relpath`, which follows symlinks, is blind to it.
        Measured against the shipped code: `docs/alias.txt` hard-linked to
        `secrets/data.txt`, an effect on the alias, `scope.out=["secrets/**"]`
        -> `scope_consistency()` returned [] while `secrets/data.txt` read
        'changed'. Silent, which is the one outcome that is not allowed.

        `st_nlink` is the whole signal, and it is deliberately half an answer:
        it proves ANOTHER NAME EXISTS and cannot say where. Locating the other
        names means walking the workspace and grouping by (st_dev, st_ino),
        because a file does not know its own aliases.

        That walk is NOT taken here, and the reason is a measurement rather
        than a preference. On this box, per call:

            receipts  ws files   st_nlink probe   full walk   scope_consistency()
               100      2,302          1.9 ms        63 ms          699 ms
               400      9,202          9.2 ms       294 ms       10,783 ms
               800     22,402         24.8 ms       817 ms       41,487 ms

        The probe is 0.06% of the call it lives in, so nothing argues against
        detecting the condition. The walk's cost scales with the WORKSPACE,
        which is unrelated to the mission's size: at ~100k files and 20
        receipts it would be seconds against a `scope_consistency()` of
        milliseconds. So the cheap half is taken and the expensive half is
        disclosed (SECURITY.md), not silently skipped.

        `os.stat` follows symlinks deliberately: the question is how many names
        the BYTES have, and a symlinked spelling of a hard-linked file is the
        same exposure. A vanished or unreadable artifact answers None -- unknown
        is never reported as one.

        The probe stats the target of the SAME `_resolve_artifact_path` the
        writer used -- not the raw spelling, and not `_norm_path`, which
        case-folds on NT and would name a nonexistent spelling on a
        case-sensitive directory. The raw stat had two holes, both measured: a
        forged receipt carrying an absolute `artifact_path` made
        `self.workspace / rel` IGNORE the workspace entirely (Path join with
        an absolute right side replaces the base), so acceptance stat-probed
        arbitrary paths outside the workspace -- an information-probe surface
        -- and could report a multiply-linked claim about bytes that were
        never the receipted artifact. `_resolve_artifact_path` refuses both
        the absolute and the escaping spelling at the door.

        `RuntimeError` is in the caught set because `Path.resolve` raises it
        on a symlink loop (verified on CPython 3.11: 'RuntimeError: Symlink
        loop'), and a loop is attacker-influenceable filesystem state -- an
        uncaught raise here is a crash on the acceptance path, the
        denial-of-service class `_load_receipt`'s doctrine already forbids.
        The `S_ISREG` gate exists for the forged `artifact_path` of '.': it
        resolves to the workspace root, whose `st_nlink >= 2` on POSIX by
        construction, and reporting the workspace root as MULTIPLY LINKED is
        a false claim about a directory, not a disclosure about an artifact.
        Every legitimately receipted artifact is a regular file (the writer
        only ever `write_bytes`), so None for anything else is 'unknowable',
        never a suppressed finding."""
        try:
            st = os.stat(self._resolve_artifact_path(rel))
        except (CustodyError, OSError, ValueError, RuntimeError):
            return None
        if not stat.S_ISREG(st.st_mode):
            return None
        return st.st_nlink

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
        # A TRAILING SLASH is a directory marker, and _norm_path erases it
        # before compilation -- so scope.out=["secrets/"] compiled to an
        # exact `secrets` regex and an effect on secrets/a.txt yielded no
        # finding, undisclosed: the silent false-CLEAN class again (es#155,
        # found a third time by review on this PR). The semantics are not
        # invented here: `_amendment_names` already settled that a
        # trailing-slash token names the directory AND what is under it,
        # so a scope entry gets the identical reading via the same
        # compiler's trailing-base form. The base itself stays matched on
        # purpose -- a FILE named `secrets` under scope.out=["secrets/"]
        # flags, which is the dischargeable over-match direction, not the
        # silent one. (The gate's operator-authored `path_globs` keep
        # their own surface; that half stays with es#155.)
        def _scope_regex(entry: str):
            norm = _norm_path(entry)
            if entry.replace("\\", "/").endswith("/") and norm:
                return _glob_regex(norm + "/**")
            return _glob_regex(norm)

        includes = [_scope_regex(g) for g in scope["in"]
                    if _is_compared_entry(g)]
        excludes = [_scope_regex(g) for g in scope["out"]
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
            # `if`, NOT `elif`. An exclusion match on ONE representation used to
            # skip the inclusion test for ALL of them, so with
            # scope.in=["docs/**"], scope.out=["alias/**"] and alias -> src, the
            # finding named only `alias/x.py` -- the resolved target `src/x.py`
            # was outside scope.in and was reported NOWHERE. An acceptor acking
            # the one path the finding named permitted a write whose real
            # destination the record never mentioned.
            #
            # The invariant this restores: EVERY candidate representation that
            # crosses ANY boundary appears in exactly one finding's
            # violating_paths. Hence `c not in violating` -- a representation
            # already reported as forbidden is not reported a second time as
            # merely unpermitted. Dropping that clause is the rejected
            # alternative, and it is not equivalent: it emits a second finding
            # for a path that both matches scope.out and sits outside scope.in
            # (secrets/c.env under scope.in=["docs/**"]), which the callers that
            # key findings by artifact_path silently collapse -- turning the
            # specific reason into the vaguer one. The two rules agree on the
            # UNION of violating paths in every row, so the acceptance gate
            # cannot distinguish them; only the disclosure can.
            if includes:
                # INCLUSION is tested against every representation too. The
                # exclusion side checked both while this one stayed lexical, so
                # `scope.in=["docs/**"]` with `docs/alias -> src/` accepted a
                # write to `src/a.py`. "Where it was not permitted to go" is
                # the same defect as "where it was forbidden to go".
                outside = [c for c in candidates
                           if c not in violating
                           and not any(rx.match(c) for rx in includes)]
                if outside:
                    findings.append({"artifact_path": rel,
                                     "request_id": request_id,
                                     "violating_paths": outside,
                                     "reason": "outside scope.in"})
            # Independent of BOTH checks above, and that is the point: the
            # dangerous hard-link case is the one where the receipted path is
            # squarely inside scope.in and matches no exclusion, so neither
            # comparison has anything to say while the bytes it wrote also
            # answer to a name in scope.out. `violating_paths` carries the
            # receipted spelling, which is the name an acceptor can actually
            # acknowledge; the other names are exactly what this cannot supply.
            links = self._link_count(rel)
            if links is not None and links > 1:
                findings.append({"artifact_path": rel, "request_id": request_id,
                                 "violating_paths": [target],
                                 "reason": _MULTIPLY_LINKED,
                                 "link_count": links})
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
                #
                # The repair for that stripped the ack and not the finding, so
                # the two sides ran through DIFFERENT functions and a path whose
                # real name carries whitespace became unnameable. `_acknowledged_
                # paths` restores one function on both sides -- exact first, per
                # ack, with the strip as a named fallback rather than a blanket
                # rule (see its docstring for the row that refutes both the
                # strip-everything and the strip-nothing repairs).
                # Obligations are keyed by (path, KIND), not by path alone. A
                # boundary crossing and a multiply-linked disclosure demand
                # different judgements from the acceptor, and under a bare
                # path key one ack discharged both at once -- acknowledging
                # the lexical crossing silently absorbed 'I found the other
                # name and checked where it points', the dearer of the two.
                obligations: set[tuple[str, str]] = set()
                for f in drifted:
                    kind = _obligation_kind(f["reason"])
                    obligations |= {(p, kind) for p in f["violating_paths"]}
                acknowledged = _acknowledged_obligations(scope_ack, obligations)
                outstanding_obl = sorted(obligations - acknowledged)
                if outstanding_obl:
                    outstanding = sorted({p for p, _ in outstanding_obl})
                    mentioned = sorted(
                        p for p in outstanding
                        if any(_amendment_names(a.get("text", ""), p)
                               for a in manifest["authority"]["amendments"]))
                    hint = (" Amendments MENTION "
                            + ", ".join(_display_path(p) for p in mentioned)
                            + " -- read them and decide; a mention is not a "
                              "grant." if mentioned else "")
                    # A multiply-linked artifact reaches this message under the
                    # same "crossed the declared scope" lead as a genuine
                    # boundary crossing, and it is not the same claim: the
                    # comparison found ANOTHER NAME, not a violation. Saying so
                    # here is the whole disclosure -- the finding is otherwise
                    # indistinguishable from an exclusion match, and an acceptor
                    # would acknowledge it without ever learning what to look
                    # at. Its ack is the QUALIFIED spelling, so the cheaper
                    # boundary judgement can never stand in for it.
                    linked = sorted({p for p, k in outstanding_obl
                                     if k == _KIND_LINKED})
                    link_note = (
                        " " + ", ".join(_display_path(p) for p in linked) + " "
                        + ("is" if len(linked) == 1 else "are")
                        + " MULTIPLY LINKED: the same bytes answer to another "
                        "name in the filesystem. Resolution follows symlinks, "
                        "and a hard link is not a link to a path, so this "
                        "comparison CANNOT see the other name or tell you "
                        "whether it is inside scope.out -- find it before "
                        "acknowledging, and acknowledge it as linked:PATH."
                        if linked else "")
                    # An ack must be typed to match EXACTLY, so a path whose
                    # whitespace the message hides is a path the acceptor
                    # cannot supply. Quoting is per path and only where it
                    # carries information, so the ordinary case -- and the
                    # `--scope-ack secrets.env` line callers assert on -- is
                    # unchanged.
                    # TOKEN COLLISION: a receipted file literally named
                    # 'linked:<p>' (legal everywhere, NTFS ADS syntax aside)
                    # that crossed the boundary shares its ack spelling with
                    # the link obligation on <p> -- and exact-path-first
                    # consumes every bare 'linked:<p>' as the literal path,
                    # so the printed recipe would name the same token twice
                    # and discharge only one obligation no matter how often
                    # it is repeated: a refusal whose printed exit does not
                    # work, the dead-end class this PR has now paid for three
                    # times. The parser already reads 'linked:"<p>"' as a
                    # qualifier (the JSON spelling misses the boundary set,
                    # then decodes inside the qualifier branch), so the
                    # message prints THAT spelling exactly when the bare one
                    # is shadowed. Collision is tested against ALL boundary
                    # obligations, not just outstanding ones: a same-call ack
                    # of the literal path leaves it in the parse set, still
                    # shadowing.
                    boundary_all = {p for p, k in obligations
                                    if k == _KIND_BOUNDARY}

                    def _shown_token(p: str, k: str) -> str | None:
                        if (k == _KIND_LINKED
                                and _LINKED_ACK_PREFIX + p in boundary_all):
                            return _LINKED_ACK_PREFIX + json.dumps(p)
                        return _ack_token(p, k)

                    rows = [(p, k, _shown_token(p, k))
                            for p, k in outstanding_obl]
                    tokens = [t for _, _, t in rows if t is not None]
                    unackable = [(p, k) for p, k, t in rows if t is None]
                    unackable_note = (
                        " No acknowledgement form exists for: "
                        + ", ".join(f"{_display_path(p)} ({k})"
                                    for p, k in unackable)
                        + " -- this finding kind fails closed; record FAIL or "
                        "INCONCLUSIVE." if unackable else "")
                    # the quoting note fires only when quoting actually
                    # changed a token's spelling -- the linked: qualifier
                    # alone is not quoting
                    quoted = any(
                        t is not None and t != (
                            p if k == _KIND_BOUNDARY
                            else _LINKED_ACK_PREFIX + p)
                        for p, k, t in rows)
                    # the note must not claim a REASON for the quoting it
                    # cannot know: shadow disambiguation quotes a path that
                    # carries no whitespace at all, and telling the acceptor
                    # to look for whitespace there is a false instruction
                    # (round-3 refutation, executed)
                    ws_note = (
                        " Quoted spellings are JSON, shown to make the "
                        "exact bytes unambiguous: the quoting marks "
                        "whitespace or quote characters that are part of "
                        "the NAME, or separates a linked: acknowledgement "
                        "from a file literally named with that prefix. "
                        "Supply quoted tokens to --scope-ack exactly as "
                        "shown -- the quoted spelling is itself accepted, "
                        "with or without its outer quotes."
                        if quoted else "")
                    raise AcceptanceRefused(
                        f"{len(outstanding_obl)} finding(s) crossed the "
                        f"declared scope and are not acknowledged: "
                        f"{', '.join(tokens)}.{hint}{link_note}{ws_note}"
                        f"{unackable_note} "
                        "Re-record the "
                        "verdict acknowledging each finding you have judged "
                        "covered -- CLI: `accept ... "
                        + " ".join(f"--scope-ack {t}" for t in tokens)
                        + "` -- or accept with FAIL/INCONCLUSIVE. A PASS would "
                        "assert a boundary the record contradicts.")
                # The acknowledgement is a first-class chain fact, not a
                # side effect: it names who judged what, so an auditor can see
                # that the boundary was crossed AND that a distinct acceptor
                # took responsibility for it.
                # Only obligations that were ACTUALLY outstanding are
                # recorded. An ack naming something that was never a finding
                # used to be written verbatim into the permanent note -- inert
                # for the gate, but it pollutes the one record that says what
                # the acceptor judged, which is the record's entire purpose.
                # `_acknowledged_obligations` only ever returns obligations
                # that WERE found, so the intersection that used to filter
                # this list now lives at the point of matching instead of
                # here. A linked discharge is recorded in its qualified
                # spelling -- which a file named 'linked:...' makes
                # permanently ambiguous as a RECORD; that ambiguity cannot be
                # cured by token syntax and belongs to es#150's structured
                # {path, kind} field.
                covered = sorted(_ack_token(p, k) or p
                                 for p, k in acknowledged)
                scope_note = (f"scope-ack by {acceptor_id}: "
                              f"{', '.join(covered)}")
                acked = self._write_next(latest, path,
                                          status=latest["status"],
                                          note=scope_note)
                latest, path = self.store.load_latest()
                # A write is a window. This one was inserted ahead of a
                # `_write_next(status="completed")` that predates it and
                # validates nothing, so the status checked at entry is stale by
                # the time it is used. Measured against the shipped code, both
                # shapes ended the same way:
                #   racer cancel() -> FINAL status 'completed', notes reading
                #     'cancelled: operator pulled the plug', 'PASS: looks fine'
                #   racer FAIL     -> FINAL status 'completed' while
                #     unresolved_verdicts still held 'FAIL:no good'
                # A cancelled mission and a failed mission both closed PASSED.
                #
                # Re-validating `status` covers the DRIFT set completely:
                # every verb that can change it (record_effect, reconcile,
                # acknowledge_receipt_loss, resume, FAIL, cancel) also moves
                # status off 'verifying' -- scope is immutable under
                # _verify_manifest, and receipt_ids cannot grow outside
                # _EFFECT_STATES or 'reopened'. But an earlier revision of
                # this comment called status the COMPLETE discriminator, and
                # that was refuted by a reproduced chain: `amend_authority`
                # leaves status 'verifying' while changing the AUTHORITY the
                # PASS asserts against -- scope-ack, then 'authority amended:
                # operator now also requires B', then a completed PASS the
                # acceptor recorded against the old manifest. Unchanged drift
                # does not make an authority change benign, so the reloaded
                # manifest must BE the manifest that was evaluated. A benign
                # concurrent `note` still passes (notes live in state, not
                # the manifest) -- that row stays pinned, so tightening this
                # to exact-checkpoint identity still has to argue with a red
                # suite.
                #
                # BEFORE _store_verdict: refusing after it would strand an
                # orphan verdicts/<rev>-PASS.json describing a PASS the chain
                # never recorded.
                if latest["status"] != "verifying":
                    raise IllegalTransition(
                        f"cannot record PASS: the mission moved to "
                        f"{latest['status']!r} while this verdict was being "
                        f"recorded (the scope acknowledgement landed at "
                        f"revision {acked['revision']} and stands); re-read the "
                        "mission and record the verdict against its current "
                        "state")
                if latest["manifest"] != manifest:
                    raise IllegalTransition(
                        "cannot record PASS: the mission's manifest changed "
                        "while this verdict was being recorded -- the "
                        "acceptance was evaluated against authority the "
                        "record no longer carries (the scope acknowledgement "
                        f"landed at revision {acked['revision']} and stands); "
                        "re-read the mission, evaluate the amended "
                        "authority, and record the verdict against its "
                        "current state")
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
        next_status = (self._resumption_status() if not remaining
                       else "reopened")
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

    def verify_chain(self) -> dict:
        """READ-ONLY checkpoint-chain integrity audit (es#138).

        Walks every checkpoint and checks the hash chain -- each record's
        ``prev_checkpoint_sha256`` must equal the SHA-256 of the preceding
        checkpoint file, and r1's must be null. Writes nothing, appends no
        checkpoint, and never changes mission state. This is what the CLI's
        ``verify`` verb runs; the lifecycle transition that used to wear that
        name is ``begin-verification``. An auditor with read-only intent
        cannot move the mission by calling this.
        """
        paths = self.store.checkpoint_paths()
        breaks: list[dict] = []
        prev_sha: str | None = None
        revision: int | None = None
        for path in paths:
            try:
                record = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                breaks.append({"checkpoint": path.name, "error": f"unreadable/invalid JSON: {exc}"})
                break
            observed_prev = record.get("prev_checkpoint_sha256", "")
            if observed_prev != prev_sha:
                breaks.append({
                    "checkpoint": path.name,
                    "expected_prev": prev_sha,
                    "observed_prev": observed_prev,
                })
            prev_sha = sha256_file(path)
            revision = record.get("revision", revision)
        return {
            "record": "chain-audit@1",
            "read_only": True,
            "checkpoints": len(paths),
            "chain_ok": not breaks,
            "breaks": breaks,
            "latest_revision": revision,
        }
