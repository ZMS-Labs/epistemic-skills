#!/usr/bin/env python3
"""Validate mission-custody@1 records without third-party dependencies.

Record kinds: mission-manifest@1, checkpoint@1, receipt@1, acceptance-verdict@1.
validate_record() dispatches on the required "record" field and returns a list
of "FIELD: reason" strings; empty list means valid.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

STATES = {"draft", "active", "reopened", "verifying", "completed", "cancelled"}
TIERS = {"operator-accepted", "declared-role-separation"}
VERDICTS = {"PASS", "FAIL", "INCONCLUSIVE"}
RECORD_KINDS = {
    "mission-manifest@1",
    "checkpoint@1",
    "receipt@1",
    "acceptance-verdict@1",
    # `audit` EMITS this kind. A `record:` label is a claim of membership in
    # this contract family, and the claim was false: `validate_record` answered
    # `unknown kind 'continuity-report@1'`, so the command's own JSON could not
    # be read by the repository's own validator. Either the label goes or the
    # validator does; the label is the useful half.
    #
    # It is a REPORT, not a stored record: nothing writes it into a mission
    # store, so it never reaches the chain, the receipts directory, or
    # `atomic_write_json`'s pre-write validation of things that do.
    "continuity-report@1",
}

# The epoch this reader implements, per record family. RECORD_KINDS above is a
# CLOSED set, so a record from a newer epoch is not "degraded" by this reader --
# it is refused, exactly like corruption. That refusal is correct and stays.
# What was missing is the ability to TELL THE TWO APART downstream.
#
# Measured on an armed enforce-mode mission: rewriting its tail `record` to
# `checkpoint@2` flips the live gate from `block` to `allow`, because the store
# fails validation, `Mission.load` skips it, and the workspace then reports
# NoActiveMission. The stderr line names the cause, but the verdict handed back
# to the harness says `gate inert: NoActiveMission` -- which is false. The
# mission is there and active; the READER is old. On an allow path that stderr
# is also the channel least likely to reach anyone.
#
# This matters most at exactly one moment: the first contract@2 write on a fleet
# whose readers have not been updated (es#118, and the es#150 ruling's
# "version-aware degraded reader fleet-wide" precondition). The upgrade itself
# would silently retire every guard in every stale workspace.
SUPPORTED_EPOCHS = {
    "mission-manifest": 1,
    "checkpoint": 1,
    "receipt": 1,
    "acceptance-verdict": 1,
    "continuity-report": 1,
}


def _canonical_epoch(epoch: str) -> str | None:
    """`epoch` when it is a canonical decimal epoch string; None otherwise.

    NOT `int(epoch)`. `str.isdigit()` and `int()` do not agree on what a digit
    is, in two directions, and BOTH raise from inside an error-handling path
    that has no except clause for them:

      * `'2'.isdigit()` is True and `int('2')` raises -- superscripts and
        other Unicode digit forms pass the test and fail the conversion;
      * on Python 3.11+ `int()` refuses strings over `sys.get_int_max_str_digits()`
        (4300 by default), so `receipt@` followed by 4301 digits passes
        `isdigit()` and raises `ValueError` on conversion.

    Measured before this function existed: a receipt with the long-digit kind
    crashed `resume()` outright with an uncaught ValueError -- the recovery
    flow was not degraded, it was unreachable, from a filename an attacker
    controls. Comparing canonical decimal strings answers the same question
    with no conversion and no bound.

    Canonical means ASCII digits with no leading zeros, so `@01` is malformed
    rather than a claim about epoch 1 -- consistent with the rest of this
    predicate, which returns None for anything it cannot read as a
    well-formed claim and leaves `validate_record` to report it.
    """
    if not (epoch.isascii() and epoch.isdigit()):
        return None
    if len(epoch) > 1 and epoch.startswith("0"):
        return None
    return epoch


def epoch_skew(record, expected_family: str) -> str | None:
    """A human-readable reason when `record` CLAIMS the family EXPECTED IN
    THIS SLOT from a NEWER epoch than this reader implements; None otherwise.

    CLAIMS, not is. This reader has no @2 validator, and `validate_record`
    short-circuits on the unknown kind, so NOTHING about the rest of the
    record has been checked when this fires: `{"record": "checkpoint@2"}`
    with every required field absent reaches here identically to a genuine
    future record. The first version of this function told the operator the
    store was "readable by an updated consumer, not corrupt -- update this
    consumer rather than repairing the mission", which is an assertion this
    reader cannot make and an attacker can exploit: relabel a corrupt or
    tampered tail as a newer epoch and the corruption diagnosis is replaced
    by advice to leave it alone.

    EXPECTED_FAMILY IS REQUIRED, and a mismatch is None. Every record sits in
    a slot some schema fixes: a checkpoint file holds a checkpoint, a receipt
    file holds a receipt. A `checkpoint@2` in a receipt slot is therefore not
    a store this reader is too old for -- no epoch of that family can ever be
    valid there -- it is corruption wearing a newer label, and honouring the
    claim replaces the accurate diagnosis with advice to upgrade. Measured
    with the family unchecked: such a receipt was reported
    `RECEIPT-NEWER-EPOCH`, `acknowledge_receipt_loss` refused it as too new,
    and the mission was left `reopened` with NO EXIT -- the stranding this
    contract's own tests forbid, reached through the one door still open.

    That is the fourth appearance of one defect: the nested walk (round 5),
    the unsupported outer kind (round 6) and the embedded family (round 11)
    each narrowed WHERE a claim is honoured and left WHAT may claim it
    unchecked one level out. Round 11 fixed exactly this for embedded
    positions and not for the top-level one it was standing on.

    None covers every other case deliberately -- an unknown or unexpected
    family, a malformed kind, an older epoch, or a non-record -- because this
    function answers one question ("is this too new for me?") and must not
    become a second opinion about validity. `validate_record` remains the
    only authority on whether a record is acceptable.
    """
    if expected_family not in SUPPORTED_EPOCHS:
        # A caller-side literal, never data: a typo here would silence the
        # skew signal everywhere it is consulted rather than fail visibly.
        raise ValueError(f"unknown expected family {expected_family!r}")
    if not isinstance(record, dict):
        return None
    kind = record.get("record")
    if not isinstance(kind, str) or kind in RECORD_KINDS or "@" not in kind:
        return None
    family, _, epoch = kind.rpartition("@")
    if family != expected_family:
        return None
    supported = SUPPORTED_EPOCHS.get(family)
    canonical = _canonical_epoch(epoch)
    if supported is None or canonical is None:
        return None
    # Numeric order over canonical decimal strings: longer is larger, equal
    # lengths compare lexicographically. No int(), so no conversion limit.
    if (len(canonical), canonical) <= (len(str(supported)), str(supported)):
        return None
    return (f"record {kind!r} CLAIMS an epoch newer than this reader "
            f"implements ({family}@{supported}). This reader cannot tell a "
            "genuine newer record from a corrupt or relabelled one -- it has "
            "no validator for that epoch. Read it with an updated consumer "
            "before concluding the store is healthy; do not treat this as "
            "proof the mission is intact")


# Records EMBED records: a checkpoint@1 carries a mission-manifest, and the
# schema requires that manifest to be @1. So a store can be too new for this
# reader with a perfectly familiar OUTER kind -- validate_record returns
# "manifest: embedded mission-manifest@1 required" while epoch_skew(outer)
# returns None, and the mission is reported ChainBroken. Measured on an armed
# mission: `run_gate` allowed with `gate inert: NoActiveMission`, which is
# exactly the silent stale-reader diagnosis this signal exists to replace.
#
# ONLY AT SCHEMA-DECLARED POSITIONS. The first fix for the above walked every
# nested dict, on the reasoning that a hand-written list would go stale. That
# widened the round-2 attack surface instead of closing it: planting
# `{"record": "checkpoint@2"}` in `state` -- a plain object under the schema,
# which cannot hold a record -- made a tampered checkpoint report as a stale
# reader and told the operator to upgrade rather than to look at the damage
# (measured, with `written_by` corrupted alongside). Suppressing a corruption
# diagnosis is the exact failure epoch_skew's docstring was rewritten to
# prevent, and a permissive walk hands the attacker every key in the file
# instead of just the top-level one.
#
# The staleness objection is answered by pinning rather than by permissiveness:
# `test_embedded_record_paths_match_the_schemas` reads the .schema.json files
# and fails if a `$ref` position appears that is not listed here.
# POSITION -> EXPECTED FAMILY, not just position. The schema fixes a
# checkpoint's `manifest` slot to the mission-manifest family, so a record
# claiming `receipt@2` there cannot be a genuine newer store at any epoch --
# it is corruption wearing a newer label. Listing the key alone honoured that
# claim and replaced the definitive embedded-manifest error with EpochSkew
# (measured), sending the operator to upgrade a reader instead of looking at
# the damage. That is the SAME decoy suppression as the nested walk (round 5)
# and the unsupported outer kind (round 6), one level further in: each fix
# narrowed WHERE a claim is honoured and left WHAT may claim it unchecked.
EMBEDDED_RECORD_PATHS = {
    "checkpoint": {"manifest": "mission-manifest"},
}


def epoch_skew_anywhere(record, expected_family: str) -> str | None:
    """`epoch_skew` for the record, then for each record the SCHEMA says it
    embeds -- and nowhere else.

    Returns the outermost skew first, so the message names the biggest thing
    known to be too new. `epoch_skew` stays the single-record predicate; this
    is the one callers deciding "can I read this file at all?" should use.
    `expected_family` is the family the CALLER'S slot fixes -- "checkpoint"
    for a file from the chain, "receipt" for one from the receipts dir.

    An unknown, malformed or unexpected outer kind yields None: this reader
    cannot know what such a record embeds, and guessing would be the
    permissive walk again. `validate_record` reports it, which is the
    accurate diagnosis.
    """
    if not isinstance(record, dict):
        return None
    skew = epoch_skew(record, expected_family)
    if skew:
        return skew
    kind = record.get("record")
    # THE OUTER KIND MUST BE ONE THIS READER IMPLEMENTS, not merely one whose
    # family name is familiar. `checkpoint@0` has no schema here, so nothing
    # establishes that it embeds a manifest at all -- traversing it on the
    # strength of the family string let an unknown-kind record (ordinary
    # corruption, per validate_record) be reported as EpochSkew, which is the
    # decoy suppression again one level up. A newer outer kind never reaches
    # this line: epoch_skew(record) above already returned for it.
    if not _in_vocab(kind, RECORD_KINDS):
        return None
    family, _, _ = kind.rpartition("@")
    # ... AND IT MUST BE THE FAMILY THIS SLOT HOLDS. A whole checkpoint@1
    # dropped into a receipt file is corruption, and traversing it would
    # report the skew of ITS embedded manifest -- so a manifest@2 planted
    # inside a misfiled record would send the operator to upgrade a reader
    # while a foreign record sat in the receipts dir. The outer epoch_skew
    # above cannot catch this one: the misfiled record's own kind is current.
    if family != expected_family:
        return None
    for key, nested_family in EMBEDDED_RECORD_PATHS.get(family, {}).items():
        nested = record.get(key)
        if not isinstance(nested, dict):
            continue
        skew = epoch_skew(nested, nested_family)
        if skew:
            return skew
    return None


# \Z, never $: re's $ also matches just before a trailing newline, so
# "m-x\n" passed as a kebab-case id (fix-refuter F-D, measured). No legal
# value of any of these carries a newline; the same one-character mechanism
# is closed for all three rather than only the instance it was caught on.
_ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z\Z")
_SHA_RE = re.compile(r"^[0-9a-f]{64}\Z")
_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*\Z")

MANIFEST_FIELDS = {
    "record", "mission_id", "created_utc", "authority", "scope",
    "acceptance", "stop_rules", "steward_ref",
}
AUTHORITY_FIELDS = {
    "operator_ref", "instruction", "amendments", "permissions",
    "protected_state", "acceptable_costs",
}
AUTHORITY_OPTIONAL_FIELDS = {"guard_mode", "actuator_guards"}
GUARD_MODES = {"audit", "enforce"}
GUARD_RULE_FIELDS = {"name", "tool_names", "command_regexes", "path_globs"}
GUARD_RULE_REQUIRED = {"name", "tool_names", "command_regexes", "path_globs"}
# Tool-name classes for inert-shape detection: a rule whose pattern lists can
# never fire for its tools arms nothing while reading as armed.
GUARD_SHELL_TOOLS = {
    "Bash", "bash", "shell", "Shell",
    "run_command", "local_shell", "run_shell_command",
}
GUARD_FS_WRITE_TOOLS = {
    "Write", "Edit", "MultiEdit", "write_file", "replace",
    "apply_patch", "str_replace_editor",
}
CHECKPOINT_FIELDS = {
    "record", "mission_id", "revision", "status", "prev_checkpoint_sha256",
    "manifest", "state", "receipt_ids", "written_utc", "written_by",
}
RECEIPT_FIELDS = {
    "record", "mission_id", "request_id", "actor", "utc",
    "artifact_path", "before_sha256", "after_sha256",
}
VERDICT_FIELDS = {
    "record", "mission_id", "revision", "verdict", "acceptor_id", "worker_id",
    "operator_ref", "assurance_tier", "receipt_refs", "reason", "utc",
}


def is_iso_utc(value: Any) -> bool:
    return isinstance(value, str) and bool(_ISO_RE.match(value))


def is_sha256(value: Any) -> bool:
    return isinstance(value, str) and bool(_SHA_RE.match(value))


def _in_vocab(value: Any, vocabulary: set) -> bool:
    """Closed-vocabulary membership that ANSWERS instead of raising.

    `value in SET` is a TypeError the moment `value` is unhashable, and every
    one of these vocabularies is read straight out of an untrusted JSON file.
    es#137 P2 fixed exactly one instance (`guard_mode`) with an inline
    `isinstance` and left the mechanism scoped to it; `status`, `verdict`,
    `assurance_tier`, `required_tier` and the top-level `record` kind all kept
    the raising shape, and a sibling checkpoint carrying `"status": []` took
    every pathless custody command in the workspace down with a TypeError.
    `validate_record` promises a LIST OF ERRORS: a promise that turns into a
    traceback on hostile input is a denial of service through the recovery
    path -- exactly what drift detection exists to survive. One predicate, so
    the next vocabulary added cannot be forgotten.

    Non-strings are never members: every one of these vocabularies is a set of
    strings, so "not a string" and "not in the set" are the same verdict, and
    the caller's existing error message already says the right thing."""
    return isinstance(value, str) and value in vocabulary


def _str_list(value: Any) -> bool:
    return isinstance(value, list) and all(
        isinstance(item, str) and item for item in value)


# One explicit predicate is mirrored byte-for-byte in the JSON Schema.  Do not
# spell this as `\S`: ECMA-262 and Python disagree about several whitespace
# characters (notably U+001C..U+001F and U+0085).  This class is Python's
# current `str.isspace()` set, written out so every schema engine receives the
# same rule instead of substituting its host regex's idea of whitespace.
DECLARATION_CONTENT_PATTERN = (
    r"[^\u0009-\u000d\u001c-\u0020\u0085\u00a0\u1680"
    r"\u2000-\u200a\u2028-\u2029\u202f\u205f\u3000]"
)
_DECLARATION_CONTENT_RE = re.compile(DECLARATION_CONTENT_PATTERN)


def _nonblank_str_list(value: Any) -> bool:
    """A declaration list whose entries say something a reader can see.

    Keep this narrower than `_str_list`: receipt ids, notes, and artifact paths
    have their own contracts. This predicate is only for manifest declaration
    fields, where truthy whitespace would present an empty boundary as set.
    """
    return _str_list(value) and all(
        _DECLARATION_CONTENT_RE.search(item) for item in value)


# The eight envelope-declaration positions this rule governs -- the same eight
# `status --brief` and `resume` present as set.  Named once, so the store's
# carry-forward comparison and the JSON Schema parity oracle cannot drift from
# the validator that decides.
DECLARATION_FIELDS = (
    ("authority", "permissions"),
    ("authority", "protected_state"),
    ("authority", "acceptable_costs"),
    ("scope", "in"),
    ("scope", "out"),
    ("stop_rules", "hold_if"),
    ("stop_rules", "stop_if"),
    ("stop_rules", "escalate_if"),
)


def declaration_view(manifest: Any) -> dict:
    """The eight declaration lists of `manifest`, for carry-forward comparison.

    Total by construction: a missing or malformed section yields None for that
    position rather than raising, because this is called on records that have
    not been validated yet and must never turn a shape question into a crash.
    """
    out: dict = {}
    for section, field in DECLARATION_FIELDS:
        block = manifest.get(section) if isinstance(manifest, dict) else None
        out[f"{section}.{field}"] = (
            block.get(field) if isinstance(block, dict) else None)
    return out


def _require(errors: list[str], cond: bool, field: str, reason: str) -> None:
    if not cond:
        errors.append(f"{field}: {reason}")


def _check_exact_fields(errors: list[str], rec: dict, allowed: set[str],
                        where: str) -> None:
    for key in rec:
        if key not in allowed:
            errors.append(f"{where}.{key}: unknown field")
    for key in allowed:
        if key not in rec:
            errors.append(f"{where}.{key}: missing")


def validate_manifest(rec: dict, *,
                      declaration_content: bool = True) -> list[str]:
    """Validate a mission-manifest@1.

    `declaration_content` gates ONE rule: whether the eight envelope
    declaration lists must carry visible content (es#160).  It defaults to
    True -- the contract this repository publishes -- and is turned OFF only
    where applying it to an ALREADY-PERSISTED record would change an
    enforcement answer.  See `custody_store.MissionStore.load_latest` and
    `write_checkpoint` for the two exemptions and why each exists.
    """
    errors: list[str] = []
    entries_ok = _nonblank_str_list if declaration_content else _str_list
    wanted = ("list of nonblank strings required" if declaration_content
              else "list of strings required")
    _check_exact_fields(errors, rec, MANIFEST_FIELDS, "manifest")
    if errors:
        return errors
    _require(errors, isinstance(rec["mission_id"], str)
             and bool(_ID_RE.match(rec["mission_id"])),
             "mission_id", "kebab-case identifier required")
    _require(errors, is_iso_utc(rec["created_utc"]),
             "created_utc", "ISO-8601 Z timestamp required")
    _require(errors, isinstance(rec["steward_ref"], str) and rec["steward_ref"],
             "steward_ref", "non-empty string required")

    auth = rec["authority"]
    if not isinstance(auth, dict):
        errors.append("authority: object required")
        return errors
    for key in auth:
        if key not in AUTHORITY_FIELDS | AUTHORITY_OPTIONAL_FIELDS:
            errors.append(f"authority.{key}: unknown field")
    for key in AUTHORITY_FIELDS:
        if key not in auth:
            errors.append(f"authority.{key}: missing")
    if not errors:
        _require(errors, isinstance(auth["operator_ref"], str)
                 and auth["operator_ref"],
                 "authority.operator_ref", "non-empty string required")
        _require(errors, isinstance(auth["instruction"], str)
                 and auth["instruction"],
                 "authority.instruction", "non-empty verbatim string required")
        amendments = auth["amendments"]
        ok = isinstance(amendments, list) and all(
            isinstance(a, dict) and set(a) == {"utc", "text"}
            and is_iso_utc(a["utc"]) and isinstance(a["text"], str) and a["text"]
            for a in amendments)
        _require(errors, ok, "authority.amendments",
                 "append-only list of {utc, text} objects required")
        for name in ("permissions", "protected_state", "acceptable_costs"):
            _require(errors, entries_ok(auth[name]),
                     f"authority.{name}", wanted)
        mode = auth.get("guard_mode")
        guards = auth.get("actuator_guards")
        if mode is not None:
            _require(errors, _in_vocab(mode, GUARD_MODES),
                     "authority.guard_mode", "must be 'audit' or 'enforce'")
            _require(errors, isinstance(guards, list) and bool(guards),
                     "authority.guard_mode",
                     "guard_mode requires a non-empty actuator_guards list")
        if guards is not None:
            if not isinstance(guards, list) or not guards:
                errors.append(
                    "authority.actuator_guards: non-empty list of guard rules "
                    "required (to disarm, amend with actuator_guards=None)")
            else:
                for i, rule in enumerate(guards):
                    where = f"authority.actuator_guards[{i}]"
                    if not isinstance(rule, dict) or set(rule) != GUARD_RULE_FIELDS:
                        errors.append(
                            f"{where}: rule must carry exactly "
                            "{name, tool_names, command_regexes, path_globs}")
                        continue
                    if not (isinstance(rule["name"], str) and rule["name"]):
                        errors.append(f"{where}.name: non-empty string required")
                        continue
                    if not rule["tool_names"] or not _str_list(rule["tool_names"]):
                        errors.append(
                            f"{where}.tool_names: non-empty list of non-empty "
                            "strings required")
                        continue
                    patterns = []
                    shape_bad = False
                    for field in ("command_regexes", "path_globs"):
                        value = rule[field]
                        if not isinstance(value, list) or not all(
                                isinstance(p, str) for p in value):
                            errors.append(
                                f"{where}.{field}: list of strings required")
                            shape_bad = True
                            break
                        patterns.extend(value)
                    if shape_bad:
                        continue
                    for pattern in rule["path_globs"]:
                        if pattern == "":
                            errors.append(
                                f"{where}.path_globs: empty string pattern is "
                                "inert and not permitted")
                            shape_bad = True
                            break
                    if shape_bad:
                        continue
                    if not patterns:
                        # a patternless rule matches nothing -> inert by accident
                        errors.append(
                            f"{where}: >=1 pattern across command_regexes and "
                            "path_globs required (patternless rule is inert)")
                        continue
                    regex_bad = False
                    for pattern in rule["command_regexes"]:
                        try:
                            re.compile(pattern)
                        except re.error:
                            errors.append(
                                f"{where}.command_regexes: does not compile: "
                                f"{pattern!r}")
                            regex_bad = True
                            break
                    if regex_bad:
                        continue
                    # Inert-shape refusal: the pattern lists a rule carries
                    # must be ones its tools can actually fire. Mixed or
                    # unknown tool names pass -- unknown tools are the
                    # operator's responsibility.
                    names = rule["tool_names"]
                    if all(n in GUARD_SHELL_TOOLS for n in names) \
                            and not rule["command_regexes"]:
                        errors.append(
                            f"{where}: shell tools carry no file_path, so "
                            "path_globs never fire; command_regexes required")
                    elif all(n in GUARD_FS_WRITE_TOOLS for n in names) \
                            and not rule["path_globs"]:
                        errors.append(
                            f"{where}: fs-write tools carry no command "
                            "string, so command_regexes never fire; "
                            "path_globs required")
                    elif all(n.startswith("mcp__") for n in names) \
                            and not rule["command_regexes"]:
                        errors.append(
                            f"{where}: MCP arguments match command_regexes "
                            "(serialized tool_input) only, so path_globs "
                            "never fire; command_regexes required")

    scope = rec["scope"]
    ok = isinstance(scope, dict) and set(scope) == {"in", "out"} \
        and entries_ok(scope.get("in")) and entries_ok(scope.get("out"))
    _require(errors, ok, "scope", '{"in": [...], "out": [...]} required')

    acc = rec["acceptance"]
    ok = isinstance(acc, dict) and set(acc) == {"required_tier", "acceptor_ref"} \
        and _in_vocab(acc.get("required_tier"), TIERS) \
        and (acc.get("acceptor_ref") is None
             or (isinstance(acc.get("acceptor_ref"), str) and acc["acceptor_ref"]))
    _require(errors, ok, "acceptance",
             "required_tier in TIERS and acceptor_ref string-or-null required")

    stop = rec["stop_rules"]
    ok = isinstance(stop, dict) \
        and set(stop) == {"hold_if", "stop_if", "escalate_if"} \
        and all(entries_ok(stop[k])
                for k in ("hold_if", "stop_if", "escalate_if"))
    _require(errors, ok, "stop_rules",
             "hold_if/stop_if/escalate_if "
             + ("nonblank " if declaration_content else "")
             + "string lists required")
    return errors


def validate_record(record: Any, *,
                    declaration_content: bool = True) -> list[str]:
    if not isinstance(record, dict):
        return ["record: JSON object required"]
    kind = record.get("record")
    if not _in_vocab(kind, RECORD_KINDS):
        return [f"record: unknown kind {kind!r}"]
    if kind == "mission-manifest@1":
        return validate_manifest(record,
                                 declaration_content=declaration_content)
    if kind == "checkpoint@1":
        return validate_checkpoint(          # Task 2
            record, declaration_content=declaration_content)
    if kind == "receipt@1":
        return validate_receipt(record)         # Task 3
    if kind == "continuity-report@1":
        return validate_continuity_report(record)
    return validate_acceptance_verdict(record)  # Task 3


CONTINUITY_REPORT_FIELDS = {
    "record", "continuity_breaks", "orphaned_retired_receipts",
}

# Every field `Mission.continuity_breaks` emits, enumerated here so the
# validator and continuity-report.schema.json state one shape in two places
# and the parity test can compare them.
CONTINUITY_BREAK_FIELDS = frozenset({
    "artifact_path", "prior_request_id", "request_id",
    "expected_before_sha256", "observed_before_sha256",
    "no_op_write", "already_reconciled",
})

# Likewise for the orphan objects.
ORPHANED_RECEIPT_FIELDS = frozenset({"request_id", "receipt_path", "note"})


def validate_continuity_report(rec: dict) -> list[str]:
    """The shape `custody_cli audit` emits. Structural only, deliberately:
    the report is a READING of a mission, not an authority record, so this
    validates that a consumer can traverse it -- not that its findings are
    true. Saying which of the two a check establishes is the whole point of
    this file."""
    errors: list[str] = []
    _check_exact_fields(errors, rec, CONTINUITY_REPORT_FIELDS,
                        "continuity-report")
    if errors:
        return errors
    breaks = rec["continuity_breaks"]
    if not isinstance(breaks, list) or not all(
            isinstance(item, dict) for item in breaks):
        errors.append("continuity_breaks: list of objects required")
    else:
        for index, item in enumerate(breaks):
            # The WHOLE shape `Mission.continuity_breaks` guarantees, not the
            # two fields the first version happened to check. Checking a
            # subset of a guaranteed shape is not a weaker validator, it is a
            # validator that RETURNS SUCCESS on a record a consumer cannot
            # traverse: the missing five could be absent, or hold lists and
            # integers, and `validate_record` still answered [].
            #
            # expected_before_sha256 comes from the prior receipt's
            # `after_sha256`, which the receipt contract types as a plain
            # string. observed_before_sha256 comes from the next receipt's
            # `before_sha256`, typed `["string", "null"]` -- null is how a
            # first write records "nothing was there". Collapsing the two into
            # one rule would either reject honest reports or accept a null
            # where a hash is guaranteed.
            for name in CONTINUITY_BREAK_FIELDS:
                if name not in item:
                    errors.append(
                        f"continuity_breaks[{index}].{name}: missing")
            extra = sorted(set(item) - CONTINUITY_BREAK_FIELDS)
            if extra:
                errors.append(
                    f"continuity_breaks[{index}]: unexpected field(s) "
                    f"{extra}")
            for name in ("artifact_path", "prior_request_id", "request_id"):
                if name in item and not (
                        isinstance(item[name], str) and item[name]):
                    errors.append(
                        f"continuity_breaks[{index}].{name}: "
                        "non-empty string required")
            if "expected_before_sha256" in item and not is_sha256(
                    item["expected_before_sha256"]):
                errors.append(
                    f"continuity_breaks[{index}].expected_before_sha256: "
                    "sha256 hex string required")
            if "observed_before_sha256" in item and not (
                    item["observed_before_sha256"] is None
                    or is_sha256(item["observed_before_sha256"])):
                errors.append(
                    f"continuity_breaks[{index}].observed_before_sha256: "
                    "sha256 hex string or null required")
            for name in ("no_op_write", "already_reconciled"):
                if name in item and not isinstance(item[name], bool):
                    errors.append(
                        f"continuity_breaks[{index}].{name}: "
                        "boolean required")
    orphans = rec["orphaned_retired_receipts"]
    if not isinstance(orphans, list) or not all(
            isinstance(item, dict) for item in orphans):
        # The emitter (`Mission.orphaned_retired_receipts`) supplies OBJECTS
        # -- request_id, receipt_path, note -- and the first version of this
        # check required STRINGS, so a continuity report validated only
        # while the orphan list was empty and was rejected precisely when an
        # orphan was reported: the validator refused the command's real
        # output at the exact moment the output carried its finding.
        errors.append("orphaned_retired_receipts: list of objects required")
    else:
        for index, item in enumerate(orphans):
            extra = sorted(set(item) - ORPHANED_RECEIPT_FIELDS)
            if extra:
                errors.append(
                    f"orphaned_retired_receipts[{index}]: unexpected "
                    f"field(s) {extra}")
            for name in sorted(ORPHANED_RECEIPT_FIELDS):
                if name not in item:
                    errors.append(
                        f"orphaned_retired_receipts[{index}].{name}: missing")
                elif not isinstance(item[name], str) or not item[name]:
                    errors.append(
                        f"orphaned_retired_receipts[{index}].{name}: "
                        "non-empty string required")
    return errors


def validate_checkpoint(rec: dict, *,
                        declaration_content: bool = True) -> list[str]:
    errors: list[str] = []
    _check_exact_fields(errors, rec, CHECKPOINT_FIELDS, "checkpoint")
    if errors:
        return errors
    _require(errors, isinstance(rec["revision"], int) and rec["revision"] >= 1,
             "revision", "integer >= 1 required")
    _require(errors, _in_vocab(rec["status"], STATES), "status",
             f"one of {sorted(STATES)} required")
    prev = rec["prev_checkpoint_sha256"]
    if rec.get("revision") == 1:
        _require(errors, prev is None, "prev_checkpoint_sha256",
                 "null required at revision 1")
    else:
        _require(errors, is_sha256(prev), "prev_checkpoint_sha256",
                 "64-hex sha256 of prior checkpoint file required")
    if isinstance(rec["manifest"], dict) \
            and rec["manifest"].get("record") == "mission-manifest@1":
        for err in validate_manifest(
                rec["manifest"], declaration_content=declaration_content):
            errors.append(f"manifest.{err}")
        if rec["manifest"].get("mission_id") != rec["mission_id"]:
            errors.append("manifest.mission_id: must equal checkpoint mission_id")
    else:
        errors.append("manifest: embedded mission-manifest@1 required")
    state = rec["state"]
    ok = isinstance(state, dict) \
        and set(state) == {"frontier", "notes", "unresolved_verdicts"} \
        and isinstance(state.get("frontier"), str) and state["frontier"] \
        and _str_list(state.get("notes")) \
        and _str_list(state.get("unresolved_verdicts"))
    _require(errors, ok, "state",
             "frontier (non-empty str), notes[], unresolved_verdicts[] required")
    _require(errors, _str_list(rec["receipt_ids"]), "receipt_ids",
             "list of receipt id strings required")
    _require(errors, is_iso_utc(rec["written_utc"]), "written_utc",
             "ISO-8601 Z timestamp required")
    _require(errors, isinstance(rec["written_by"], str) and rec["written_by"],
             "written_by", "non-empty actor id required")
    return errors


def validate_receipt(rec: dict) -> list[str]:
    errors: list[str] = []
    _check_exact_fields(errors, rec, RECEIPT_FIELDS, "receipt")
    if errors:
        return errors
    _require(errors, isinstance(rec["mission_id"], str)
             and bool(_ID_RE.match(rec["mission_id"])),
             "mission_id", "kebab-case identifier required")
    for name in ("request_id", "actor", "artifact_path"):
        _require(errors, isinstance(rec[name], str) and rec[name],
                 name, "non-empty string required")
    _require(errors, is_iso_utc(rec["utc"]), "utc", "ISO-8601 Z required")
    _require(errors, rec["before_sha256"] is None or is_sha256(rec["before_sha256"]),
             "before_sha256", "null (new artifact) or 64-hex sha256 required")
    _require(errors, is_sha256(rec["after_sha256"]),
             "after_sha256", "64-hex sha256 required")
    return errors


def validate_acceptance_verdict(rec: dict) -> list[str]:
    errors: list[str] = []
    _check_exact_fields(errors, rec, VERDICT_FIELDS, "verdict")
    if errors:
        return errors
    _require(errors, isinstance(rec["revision"], int) and rec["revision"] >= 1,
             "revision", "integer >= 1 required")
    _require(errors, _in_vocab(rec["verdict"], VERDICTS), "verdict",
             f"one of {sorted(VERDICTS)} required")
    _require(errors, _in_vocab(rec["assurance_tier"], TIERS), "assurance_tier",
             f"one of {sorted(TIERS)} required")
    _require(errors, isinstance(rec["mission_id"], str)
             and bool(_ID_RE.match(rec["mission_id"])),
             "mission_id", "kebab-case identifier required")
    for name in ("acceptor_id", "worker_id", "operator_ref", "reason"):
        _require(errors, isinstance(rec[name], str) and rec[name],
                 name, "non-empty string required")
    _require(errors, _str_list(rec["receipt_refs"]), "receipt_refs",
             "list of receipt id strings required")
    _require(errors, is_iso_utc(rec["utc"]), "utc", "ISO-8601 Z required")
    if not errors:
        # Casefolded: "Steward-A" accepting "steward-a" is the same principal
        # wearing different capitalization, not role separation.
        _require(errors,
                 rec["acceptor_id"].casefold() != rec["worker_id"].casefold(),
                 "acceptor_id", "self-certification refused (== worker_id, casefolded)")
        if rec["assurance_tier"] == "operator-accepted":
            _require(errors, rec["acceptor_id"] == rec["operator_ref"],
                     "acceptor_id",
                     "operator-accepted tier requires acceptor_id == operator_ref")
    return errors


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: verify_mission_custody.py <file.json>...", file=sys.stderr)
        return 2
    failed = False
    for arg in argv:
        rec = json.loads(Path(arg).read_text(encoding="utf-8"))
        errors = validate_record(rec)
        if errors:
            failed = True
            for err in errors:
                print(f"{arg}: {err}")
        else:
            print(f"{arg}: valid")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
