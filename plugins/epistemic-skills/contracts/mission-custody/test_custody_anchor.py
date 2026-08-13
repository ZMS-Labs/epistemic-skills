#!/usr/bin/env python3
"""Unit tests for `custody_anchor`.

Runner convention is `test_custody_mission.py`'s: an explicit `TESTS`
registry, every test takes `(tmp: Path)` even when it ignores it, and the
runner prints `N failures`. The other convention in this package
(`test_custody_gate.py`: auto-discovery, `fn()`, `all green`) is
incompatible -- mixing them raises TypeError.

One addition to that convention: the per-test temp directory honours
`CUSTODY_TEST_TMPDIR` via `dir=`. Unset, this is exactly the upstream
behaviour. Set, it FAILS CLOSED -- a bad path raises rather than silently
falling back to the system temp dir, which is what the env-var route does.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from custody_anchor import (  # noqa: E402
    ANCHOR_UNREADABLE,
    AnchorKeyUnresolvable,
    AnchorMismatch,
    AnchorState,
    AnchorWriteFailed,
    _ascii_case_fold,
    _is_safe_key,
    _strip_extended_length,
    anchor_root,
    anchors_dir,
    classify,
    mission_key,
    read_anchor,
    write_anchor,
)

FAILURES: list[str] = []

CHAIN = ["aa" * 32, "bb" * 32, "cc" * 32]   # r1, r2, r3
TAIL = CHAIN[-1]


def check(name: str, cond: bool) -> None:
    if not cond:
        FAILURES.append(name)
        print(f"FAIL {name}")
    else:
        print(f"ok   {name}")


def test_anchor_state_table(tmp: Path) -> None:
    """The state machine as a case table.

    The shape rows exist because the anchor file is ADVERSARY-CONTROLLED:
    every one of them must RETURN, never raise. A one-byte file must not
    disable the control by crashing it.

    Rows are explicit 5-tuples rather than the brief's name-keyed
    `tail`/`chain` override, because three of the added rows need their own
    pair and extending a name-keyed switch is how a table stops enumerating
    a product space and starts accumulating special cases.
    """
    cases = [
        # (name, anchor, tail, chain, want)
        ("verified", {"checkpoint_sha256": TAIL, "revision": 3},
         TAIL, CHAIN, "verified"),
        ("lagging-1", {"checkpoint_sha256": CHAIN[1], "revision": 2},
         TAIL, CHAIN, "lagging"),
        ("lagging-2", {"checkpoint_sha256": CHAIN[0], "revision": 1},
         TAIL, CHAIN, "lagging"),
        ("ahead", {"checkpoint_sha256": "dd" * 32, "revision": 9},
         TAIL, CHAIN, "mismatch"),
        ("forked", {"checkpoint_sha256": "ee" * 32, "revision": 2},
         TAIL, CHAIN, "mismatch"),
        ("absent", None, TAIL, CHAIN, "absent"),
        # --- non-dict JSON. isinstance(True, int) is True in Python, so the
        # dict guard has to precede anything numeric; bool is listed
        # separately from int for exactly that reason.
        ("non-dict-list", [], TAIL, CHAIN, "mismatch"),
        ("non-dict-str", "x", TAIL, CHAIN, "mismatch"),
        ("non-dict-int", 5, TAIL, CHAIN, "mismatch"),
        ("non-dict-bool", True, TAIL, CHAIN, "mismatch"),
        ("non-dict-float", 1.5, TAIL, CHAIN, "mismatch"),
        # --- the sentinel is the value MOST likely to reach classify in
        # production, and the only one this module itself produces.
        ("sentinel", ANCHOR_UNREADABLE, TAIL, CHAIN, "mismatch"),
        # --- dict, bad pin
        ("no-key", {"revision": 3}, TAIL, CHAIN, "mismatch"),
        ("pinned-none", {"checkpoint_sha256": None}, TAIL, CHAIN, "mismatch"),
        ("pinned-int", {"checkpoint_sha256": 5}, TAIL, CHAIN, "mismatch"),
        ("pinned-bool", {"checkpoint_sha256": True}, TAIL, CHAIN, "mismatch"),
        ("pinned-list", {"checkpoint_sha256": []}, TAIL, CHAIN, "mismatch"),
        ("pinned-dict", {"checkpoint_sha256": {}}, TAIL, CHAIN, "mismatch"),
        ("pinned-not-sha", {"checkpoint_sha256": "zz"}, TAIL, CHAIN, "mismatch"),
        ("pinned-63-hex", {"checkpoint_sha256": "a" * 63},
         TAIL, CHAIN, "mismatch"),
        ("pinned-65-hex", {"checkpoint_sha256": "a" * 65},
         TAIL, CHAIN, "mismatch"),
        ("pinned-64-nonhex", {"checkpoint_sha256": "gg" * 32},
         TAIL, CHAIN, "mismatch"),
        # An uppercase spelling of the tail is `mismatch`, not `verified`.
        # sha256_file only ever emits lowercase, so this is the safe
        # direction: refuse loudly rather than bless a spelling nothing
        # produced.
        ("pinned-uppercase-tail", {"checkpoint_sha256": TAIL.upper()},
         TAIL, CHAIN, "mismatch"),
        ("empty-chain", {"checkpoint_sha256": TAIL}, "", [], "mismatch"),
        # --- THE DISCRIMINATING ROWS. Every row above answers `mismatch`
        # for a non-sha pin only because that pin happens not to equal
        # `tail_sha` and happens not to be in `chain_shas`. These three
        # remove the coincidence: they pass a non-sha pin that DOES match.
        # Measured against the un-guarded state machine: `verified`,
        # `verified`, `lagging`. `tail_sha=""` is not hypothetical -- the
        # `empty-chain` row above is that call shape.
        ("pinned-empty-equals-empty-tail", {"checkpoint_sha256": ""},
         "", [], "mismatch"),
        ("pinned-nonsha-equals-tail", {"checkpoint_sha256": "zz"},
         "zz", [], "mismatch"),
        ("pinned-nonsha-in-chain", {"checkpoint_sha256": "zz"},
         TAIL, ["zz"], "mismatch"),
    ]
    for name, anchor, tail, chain, want in cases:
        check(f"anchor-state-{name}", classify(anchor, tail, chain) == want)


def test_classify_is_total_over_json_values(tmp: Path) -> None:
    """Totality is the property, so sweep the value space, not a sample.

    Scoped claim: total over `anchor`. `tail_sha` and `chain_shas` come from
    the store rather than from disk-as-JSON and are trusted to be a str and
    a sequence of str; nothing here tests that axis.
    """
    literals = [
        "null", "true", "false", "0", "-1", "1.5", '""', '"x"', "[]",
        "[1,2]", "{}", '{"checkpoint_sha256": null}',
        '{"checkpoint_sha256": {"nested": 1}}',
        '{"checkpoint_sha256": "' + TAIL + '"}',
    ]
    corpus = [(t, json.loads(t)) for t in literals]
    # Labelled, not repr'd: `repr(ANCHOR_UNREADABLE)` embeds a memory
    # address, and a check name that changes every run cannot be diffed
    # between two runs of the same suite.
    corpus.append(("<ANCHOR_UNREADABLE>", ANCHOR_UNREADABLE))
    for label, value in corpus:
        try:
            got = classify(value, TAIL, CHAIN)
        except Exception as exc:                            # noqa: BLE001
            check(f"classify-total-{label}-raised-{type(exc).__name__}", False)
            continue
        check(f"classify-returns-declared-state-{label}",
              got in AnchorState.ALL)


def test_a_file_that_exists_is_never_absent(tmp: Path) -> None:
    """`absent` is the ONLY state that triggers trust-on-first-use adoption,
    so ANY existing file reaching it launders a forged tail into `verified`
    on the next check. The distinction must survive the READ -- classify
    cannot reconstruct it, because None-from-no-file and None-from-bad-file
    are the same value.

    ROW `null` IS THE ONE THAT MATTERS and it is why this test is keyed on
    EXISTENCE, not on parse failure: `null` is VALID JSON that parses to
    None, so a parse-failure-keyed read hands classify the same None that
    means 'no file'. A test that only writes `{not json` takes the
    parse-failure branch and CANNOT catch it.

    ROW `dir` is the second one, and it is not a parse question at all:
    measured on this platform, `read_bytes` on a DIRECTORY named
    `<key>.json` raises PermissionError (errno 13), NOT FileNotFoundError.
    A read that catches only FileNotFoundError lets a `mkdir` crash the
    whole control -- the `_load_receipt` denial-of-service doctrine, one
    function upstream of where it was applied.
    """
    root = tmp / "anchors"
    root.mkdir()
    for name, payload in [("corrupt", b"{not json"), ("empty", b""),
                          ("null", b"null"), ("num", b"5"),
                          ("str", b'"x"'), ("list", b"[]"), ("bool", b"true"),
                          ("badutf8", b"\xff\xfe\x00")]:
        (root / f"{name}.json").write_bytes(payload)
        got = read_anchor(name, root)
        check(f"exists-not-none-{name}", got is not None)
        # THE SEAM: read and classify are each tested above and below; this
        # is the JOIN, which is where the laundering would actually happen.
        check(f"exists-not-absent-{name}",
              classify(got, TAIL, [TAIL]) != "absent")

    (root / "dir.json").mkdir()
    got = read_anchor("dir", root)
    check("dir-not-none", got is not None)
    check("dir-does-not-raise-and-is-not-absent",
          classify(got, TAIL, [TAIL]) == "mismatch")

    check("missing-file-is-absent", read_anchor("nope", root) is None)
    check("sentinel-classifies-mismatch",
          classify(ANCHOR_UNREADABLE, TAIL, [TAIL]) == "mismatch")

    # A broken store is corruption, not absence. On this platform reading
    # through a FILE where the anchors dir belongs raises FileNotFoundError
    # (errno 2, measured), which is indistinguishable from a missing anchor
    # unless the parent is checked.
    broken = tmp / "not-a-dir"
    broken.write_bytes(b"x")
    check("anchors-dir-is-a-file-is-not-absent",
          read_anchor("k", broken) is ANCHOR_UNREADABLE)

    # A fresh install has no anchors directory at all, and THAT is absent.
    check("missing-anchors-dir-is-absent",
          read_anchor("k", tmp / "never-created") is None)

    # An unsafe key cannot read this mission's anchor, so it is unusable --
    # never `absent`, and never an exception on the recovery path.
    check("unsafe-key-reads-unreadable-not-absent",
          read_anchor("../escape", root) is ANCHOR_UNREADABLE)


def test_anchor_roundtrip_and_write_refusals(tmp: Path) -> None:
    root = anchors_dir(tmp / "anchor-root")
    key = mission_key(tmp / "missions" / "m")
    record = {"mission_id": "m", "revision": 3, "checkpoint_sha256": TAIL,
              "resolved_root": str(tmp / "anchor-root")}
    path = write_anchor(key, root, record)
    check("write-returns-a-path-under-the-given-root", path.parent == root)
    check("roundtrip-reads-back", read_anchor(key, root) == record)
    check("roundtrip-classifies-verified",
          classify(read_anchor(key, root), TAIL, CHAIN) == "verified")

    # Overwrite, not compare-and-swap: the advance-only CAS belongs to the
    # caller that knows what the anchor currently pins.
    write_anchor(key, root, {**record, "revision": 4})
    check("write-overwrites-in-place",
          read_anchor(key, root)["revision"] == 4)

    for name, bad in [("not-a-dict", ["x"]), ("no-sha", {"revision": 1}),
                      ("sha-none", {"checkpoint_sha256": None}),
                      ("sha-not-hex", {"checkpoint_sha256": "zz"}),
                      ("sha-uppercase", {"checkpoint_sha256": TAIL.upper()})]:
        raised = False
        try:
            write_anchor("k2", root, bad)
        except AnchorWriteFailed:
            raised = True
        check(f"write-refuses-{name}", raised)
    check("refused-record-wrote-nothing", not (root / "k2.json").exists())

    # A key that is not one path component would land a file outside the
    # root it was handed. The probe target stays inside tmp on purpose.
    escaped = tmp / "anchor-root" / "escape.json"
    raised = False
    try:
        write_anchor(os.path.join("..", "escape"), root, record)
    except AnchorWriteFailed:
        raised = True
    check("write-refuses-a-traversal-key", raised)
    check("traversal-key-wrote-nothing-outside-root", not escaped.exists())


def test_write_failure_is_observable_to_the_caller(tmp: Path) -> None:
    """A failed write must reach the caller, and a return value does not.

    The natural call site discards a bool, and a discarded write failure is
    indistinguishable from a mission that never had an anchor: the next
    check finds no file, reports `absent`, and adopts -- the same laundering
    as a forged file, reached by a failed write.

    The `refused-root` case below is the one the brief names, and it is the
    load-bearing one: `anchor_root` refusing a root inside the workspace is
    precisely a condition that makes the write fail, and when the write
    never happens the store it would have written to is INTACT, so the next
    read is a truthful `absent` and there is nothing at all for the read
    path to notice. The exception is the entire signal.
    """
    key = mission_key(tmp / "missions" / "m")
    record = {"mission_id": "m", "revision": 1, "checkpoint_sha256": TAIL}

    # 1. Refused root -> the caller never gets a root to write to.
    ws = tmp / "workspace"
    ws.mkdir()
    healthy = anchors_dir(tmp / "healthy-root")
    healthy.mkdir(parents=True)
    raised = False
    try:
        anchor_root(str(ws / "anchors"), workspace=ws)
    except AnchorMismatch:
        raised = True
    check("refused-root-raises", raised)
    # THE DISCRIMINATOR: had that refusal been a return value the caller
    # dropped, this is everything the next check would have to go on.
    check("a-swallowed-refusal-would-read-as-absent",
          classify(read_anchor(key, healthy), TAIL, CHAIN) == "absent")

    # 2. A root that cannot be created: a file where the root belongs.
    blocked = tmp / "blocked"
    blocked.write_bytes(b"a file where the anchor root belongs")
    raised = False
    try:
        write_anchor(key, anchors_dir(blocked), record)
    except AnchorWriteFailed:
        raised = True
    check("blocked-write-raises", raised)
    check("blocked-store-is-not-absent",
          classify(read_anchor(key, anchors_dir(blocked)), TAIL, CHAIN)
          == "mismatch")

    # 3. A directory occupying the anchor's own name.
    good_root = anchors_dir(tmp / "root2")
    good_root.mkdir(parents=True)
    (good_root / f"{key}.json").mkdir()
    raised = False
    try:
        write_anchor(key, good_root, record)
    except AnchorWriteFailed:
        raised = True
    check("write-onto-a-directory-raises", raised)
    check("write-onto-a-directory-is-mismatch-not-absent",
          classify(read_anchor(key, good_root), TAIL, CHAIN) == "mismatch")
    leftovers = [p.name for p in good_root.iterdir() if p.suffix == ".tmp"]
    check("failed-write-leaves-no-tmp-file", leftovers == [])


def test_anchor_root_refuses_a_root_inside_the_workspace(tmp: Path) -> None:
    """An anchor the workspace can write anchors nothing.

    Both halves of the fixture are built under `tmp`: the failure mode of
    this specific test is "writes where it should not", so the real worktree
    is never passed as the workspace.
    """
    ws = tmp / "workspace"
    ws.mkdir()
    for name, candidate in [("inside", ws / "anchors"),
                            ("equal", ws),
                            ("deep", ws / "a" / "b" / "c")]:
        raised = False
        try:
            anchor_root(str(candidate), workspace=ws)
        except AnchorMismatch:
            raised = True
        check(f"anchor-root-refuses-{name}", raised)

    # Looks redundant beside `inside`, and is the row that matters: a
    # containment test written as a bare string prefix accepts `inside` and
    # WRONGLY refuses this, because "…/ws-anchors".startswith("…/ws").
    sibling = tmp / "workspace-anchors"
    check("anchor-root-allows-a-sibling-whose-name-shares-the-prefix",
          anchor_root(str(sibling), workspace=ws) == Path(os.path.realpath(sibling)))

    outside = tmp / "outside"
    got = anchor_root(str(outside), workspace=ws)
    check("anchor-root-honours-an-override-outside-the-workspace",
          got == Path(os.path.realpath(outside)))
    check("anchor-root-creates-nothing", not outside.exists())

    # The DEFAULT root. This asserts on the returned Path and creates
    # nothing at it -- `anchor_root` performs no filesystem mutation, which
    # is what makes this assertion safe to make at all.
    default = anchor_root()
    check("default-root-is-named-.mission-custody",
          default.name == ".mission-custody")
    check("default-root-is-under-home",
          default.parent == Path(os.path.realpath(Path.home())))
    check("default-root-is-outside-this-worktree",
          not str(default).lower().startswith(str(ROOT).lower()))
    check("default-root-is-stable", anchor_root() == default)

    check("anchors-dir-is-the-bridge-from-root-to-files",
          anchors_dir(default) == default / "anchors")


def test_mission_key_is_stable_across_path_spellings(tmp: Path) -> None:
    """One directory has several honest spellings; a key that varies by
    spelling mints parallel anchors, each TOFU-adopting independently --
    quiet erosion.

    ⚠ READ THIS BEFORE TRUSTING THE TWO `UNPINNED` ASSERTIONS. On THIS
    platform `os.path.realpath` already collapses case AND 8.3 short names
    for an EXISTING path, and it PRESERVES a genuine 4-character
    extended-length prefix. Re-measured for this task:

        realpath('\\\\?\\Y:\\dev')  -> '\\\\?\\Y:\\dev'   (preserved)
        realpath('\\?\\Y:\\dev')    -> 'Y:dev'      (3-char: shell-mangled)

    So both keep passing with their corresponding code deleted, and NEITHER
    pins anything here. They are kept as portability regression guards,
    labelled, so no later round reads a green as proof the fold or the strip
    is exercised.

    The PINNED assertions below are the answer to "find a spelling realpath
    does NOT normalise on this platform": a NON-EXISTENT directory. Measured
    -- realpath case-normalises an existing path and leaves a non-existent
    one exactly as spelled, so the fold is load-bearing there and only
    there. That case is not exotic: the design keys the anchor on the PATH
    precisely so that deleting a mission dir and reopening the same id at
    the same path keeps the key, and a deleted directory is a non-existent
    one.
    """
    a = mission_key(tmp / "missions" / "m")
    b = mission_key(Path("\\\\?\\" + str(tmp)) / "missions" / "m")
    check("mission-key-extended-length-stable-UNPINNED-ON-NTFS", a == b)
    c = mission_key(Path(str(tmp).upper()) / "missions" / "m")

    ghost_lo = tmp / "ghost-mission" / "m"
    ghost_hi = tmp / "GHOST-MISSION" / "M"
    if os.name == "nt":
        check("mission-key-case-stable-UNPINNED-ON-NTFS", a == c)
        check("mission-key-folds-case-on-a-NONEXISTENT-dir-PINNED",
              mission_key(ghost_lo) == mission_key(ghost_hi))
    else:
        # On a case-sensitive filesystem these are two DIFFERENT directories
        # and one key for both would be a collision, not stability. The fold
        # is gated on os.name for the same reason `_same_artifact` is.
        check("mission-key-case-distinct-on-a-case-sensitive-fs-PINNED",
              a != c)
        check("mission-key-does-not-fold-case-on-posix-PINNED",
              mission_key(ghost_lo) != mission_key(ghost_hi))

    check("mission-key-is-a-sha256", len(a) == 64
          and all(ch in "0123456789abcdef" for ch in a))
    check("mission-key-distinguishes-two-directories",
          a != mission_key(tmp / "missions" / "other"))


def test_stripping_a_prefix_never_makes_an_absolute_path_relative(
        tmp: Path) -> None:
    r"""The naive 4-character slice is wrong for the UNC form.

    `\\?\UNC\srv\sh` sliced becomes `UNC\srv\sh`, which is RELATIVE, so
    `realpath` resolves it against the CURRENT WORKING DIRECTORY and one
    mission directory mints a different key per CWD. Measured: two CWDs, two
    keys, for one path -- unbounded parallel anchors, each adopting
    independently.

    The isabs invariant is asserted over the corpus rather than only for the
    UNC branch, because the spelling that breaks this next is the one this
    enumeration did not reach.
    """
    for text, want in [
        ("\\\\?\\C:\\ws\\missions\\m", "C:\\ws\\missions\\m"),
        ("\\\\?\\UNC\\srv\\share\\missions\\m", "\\\\srv\\share\\missions\\m"),
    ]:
        check(f"strip-handles-{text}", _strip_extended_length(text) == want)
    check("naive-4-char-slice-would-have-produced-a-relative-path",
          not os.path.isabs("\\\\?\\UNC\\srv\\share\\missions\\m"[4:]))

    for text in ["\\\\srv\\share\\missions\\m", "C:\\ws\\missions\\m",
                 "/ws/missions/m", "relative\\missions\\m"]:
        check(f"strip-leaves-alone-{text}",
              _strip_extended_length(text) == text)

    if os.name == "nt":
        # The positive control for the isabs fallback, and the reason that
        # fallback is not dead weight: a volume-GUID path is absolute,
        # extended-length, and NOT the UNC form, so the branch above does
        # not see it and the naive slice would turn it relative. Refusing to
        # strip what it cannot strip safely is the fallback's whole job.
        # (Judged with the LOCAL isabs, so this is an NT-only spelling
        # question -- no posix mission directory is named like this.)
        vol = "\\\\?\\Volume{4c1b2a3d-0000-0000-0000-000000000000}\\m"
        check("strip-refuses-to-relativise-an-unknown-prefixed-form",
              _strip_extended_length(vol) == vol)
        check("the-volume-form-is-absolute-and-its-naive-slice-is-not",
              os.path.isabs(vol) and not os.path.isabs(vol[4:]))


def test_an_unresolvable_path_refuses_instead_of_crashing(tmp: Path) -> None:
    """`os.path.realpath` is not total.

    Measured on this fleet: it raises OSError (WinError 1326, 'the user name
    or password is incorrect') for a UNC path whose share will not
    authenticate -- which is the spelling this fleet's own mission
    directories can take. Uncaught, that kills the anchor with a bare stdlib
    traceback from inside ntpath.

    Substituting a different canonicalisation (`abspath`) instead of
    refusing would be worse than the crash: the key would change whenever a
    share hiccups, and a changed key is a fresh anchor, and a fresh anchor
    ADOPTS. Refusing is the safe direction.

    Patched rather than provoked because no portable input reproduces it.
    """
    import custody_anchor

    real = custody_anchor.os.path.realpath

    def boom(_path):
        raise OSError(22, "the user name or password is incorrect")

    custody_anchor.os.path.realpath = boom
    try:
        raised = False
        try:
            mission_key(tmp / "missions" / "m")
        except AnchorKeyUnresolvable:
            raised = True
        check("unresolvable-mission-dir-raises-a-typed-refusal", raised)
        raised = False
        try:
            anchor_root(str(tmp / "root"))
        except AnchorKeyUnresolvable:
            raised = True
        check("unresolvable-anchor-root-raises-a-typed-refusal", raised)
    finally:
        custody_anchor.os.path.realpath = real
    check("realpath-restored", custody_anchor.os.path.realpath is real)


def test_the_case_fold_copy_has_not_drifted(tmp: Path) -> None:
    """`custody_anchor` copies `_ascii_case_fold` rather than importing it,
    to keep `custody_anchor` -> `custody_mission` from existing at all: a
    later task wires the anchor into `resume`, and `custody_mission` will
    import this module. A copy with no guard is a copy that drifts, so this
    is the guard. The TEST may import both; only the module may not.
    """
    from custody_mission import _ascii_case_fold as original

    # Labelled by index, not by content: two of these are non-ASCII, and a
    # check NAME carrying them raises UnicodeEncodeError on a Windows
    # console under the default code page -- a suite that cannot print its
    # own result is a suite nobody runs.
    corpus = ["ABC", "abc", "Y:\\Dev\\Missions", "/tmp/A/b",
              "stra\u00dfe.txt", "\u212a", "\u0130stanbul", "\u00c4\u00e4",
              "", "0123456789", "MiXeD_CaSe-123"]
    for index, text in enumerate(corpus):
        check(f"case-fold-copy-matches-corpus-{index}",
              _ascii_case_fold(text) == original(text))
    check("case-fold-does-not-do-unicode-expansion",
          _ascii_case_fold("stra\u00dfe") == "stra\u00dfe")
    check("case-fold-leaves-kelvin-alone", _ascii_case_fold("\u212a") != "k")


def test_safe_key_rejects_everything_that_is_not_one_component(
        tmp: Path) -> None:
    for good in ["a", "a" * 64, "mission-1", "0123abcd", ".hidden"]:
        check(f"safe-key-accepts-{good}", _is_safe_key(good))
    bad = ["", ".", "..", "a/b", "a\\b", "..\\..\\x", "C:x", None, 5,
           os.path.join("..", "escape")]
    for value in bad:
        check(f"safe-key-rejects-{value!r}", not _is_safe_key(value))


TESTS = [
    test_anchor_state_table,
    test_classify_is_total_over_json_values,
    test_a_file_that_exists_is_never_absent,
    test_anchor_roundtrip_and_write_refusals,
    test_write_failure_is_observable_to_the_caller,
    test_anchor_root_refuses_a_root_inside_the_workspace,
    test_mission_key_is_stable_across_path_spellings,
    test_stripping_a_prefix_never_makes_an_absolute_path_relative,
    test_an_unresolvable_path_refuses_instead_of_crashing,
    test_the_case_fold_copy_has_not_drifted,
    test_safe_key_rejects_everything_that_is_not_one_component,
]


def main() -> int:
    # An unregistered test is a control that was written and never
    # installed, which is this estate's standing failure mode.
    registered = {fn.__name__ for fn in TESTS}
    orphans = sorted(
        name for name, obj in list(globals().items())
        if name.startswith("test_") and callable(obj)
        and name not in registered)
    for name in orphans:
        check(f"test-registered-{name}", False)

    tmp_root = os.environ.get("CUSTODY_TEST_TMPDIR") or None
    for fn in TESTS:
        with tempfile.TemporaryDirectory(dir=tmp_root) as td:
            # Recorded as a failure rather than allowed to abort the run: an
            # uncaught exception in test 3 leaves tests 4..N unrun, and a
            # suite-level exit code cannot then distinguish CAUGHT from
            # CRASHED-EARLY -- which is the one distinction every mutation
            # round on this contract depends on.
            try:
                fn(Path(td))
            except Exception as exc:                        # noqa: BLE001
                check(f"{fn.__name__}-RAISED-{type(exc).__name__}", False)
    print(f"\n{len(FAILURES)} failures")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    raise SystemExit(main())
