#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from custody_store import StoreError, sha256_bytes, sha256_file  # noqa: E402
from verify_mission_custody import is_iso_utc  # noqa: E402
from custody_mission import (  # noqa: E402
    _same_artifact,
    AcceptanceRefused,
    CustodyError,
    IllegalTransition,
    Mission,
    MultipleActiveMissions,
    NoActiveMission,
)

FAILURES: list[str] = []


def check(name: str, cond: bool) -> None:
    if not cond:
        FAILURES.append(name)
        print(f"FAIL {name}")
    else:
        print(f"ok   {name}")


def open_mission(workspace: Path, mission_id: str, instruction: str,
                  required_tier: str = "declared-role-separation",
                  actor: str = "agent:worker", **kwargs) -> Mission:
    return Mission.open(
        workspace, mission_id=mission_id, instruction=instruction,
        operator_ref="operator:zach", steward_ref="agent:worker",
        required_tier=required_tier, actor=actor, **kwargs)


def test_open_creates_draft_r1(workspace: Path) -> None:
    m = open_mission(workspace, "m-open", "Do the thing.")
    st = m.status()
    check("open-revision-1", st["revision"] == 1)
    check("open-status-draft", st["status"] == "draft")
    check("open-instruction-verbatim",
          st["manifest"]["authority"]["instruction"] == "Do the thing.")


def test_pathless_load_single_active(workspace: Path) -> None:
    m = open_mission(workspace, "m-load", "Ship it.")
    m.approve()
    found = Mission.load(workspace, actor="agent:second")
    check("load-finds-single", found.store.mission_dir == m.store.mission_dir)
    check("load-status-active", found.status()["status"] == "active")


def test_load_refuses_zero_and_multiple(workspace: Path) -> None:
    try:
        Mission.load(workspace, actor="agent:x")
        check("load-zero-raises", False)
    except NoActiveMission:
        check("load-zero-raises", True)

    m1 = open_mission(workspace, "m-one", "A.")
    # open() refuses to CREATE a second active mission in one workspace
    # (decoy-disarm wedge, es#117 review fix 4); a duplicated mission dir
    # arriving out-of-band (sync, copy) is exactly the multiple-active state
    # load() must still refuse, so build it that way.
    shutil.copytree(m1.store.mission_dir, workspace / "missions" / "m-two")
    try:
        Mission.load(workspace, actor="agent:x")
        check("load-multiple-raises", False)
    except MultipleActiveMissions:
        check("load-multiple-raises", True)


def test_effect_writes_receipt_and_artifact(workspace: Path) -> None:
    m = open_mission(workspace, "m-effect", "Write notes.")
    m.approve()
    receipt = m.record_effect("notes/a.md", "hello", "req-1")
    target = workspace / "notes" / "a.md"
    check("effect-artifact-exists", target.exists())
    check("effect-artifact-content", target.read_text(encoding="utf-8") == "hello")
    check("effect-receipt-hash", receipt["after_sha256"] == sha256_bytes(b"hello"))
    st = m.status()
    check("effect-receipt-id-recorded", "req-1" in st["receipt_ids"])


def test_effect_refuses_escape(workspace: Path) -> None:
    m = open_mission(workspace, "m-escape", "Guard paths.")
    m.approve()
    try:
        m.record_effect("../outside.md", "x", "req-esc-1")
        check("effect-refuses-dotdot", False)
    except CustodyError:
        check("effect-refuses-dotdot", True)
    try:
        m.record_effect("C:/x", "x", "req-esc-2")
        check("effect-refuses-absolute", False)
    except CustodyError:
        check("effect-refuses-absolute", True)
    check("effect-escape-no-artifact",
          not (workspace.parent / "outside.md").exists())


def test_resume_detects_drift_and_reconcile_clears(workspace: Path) -> None:
    m = open_mission(workspace, "m-drift", "Track drift.")
    m.approve()
    m.record_effect("notes/a.md", "hello", "req-1")
    target = workspace / "notes" / "a.md"
    target.write_text("tampered", encoding="utf-8")

    mismatched = m.resume()
    check("resume-returns-path", mismatched == ["notes/a.md"])
    st = m.status()
    check("resume-status-reopened", st["status"] == "reopened")
    check("resume-marker-present",
          "RECONCILIATION:notes/a.md" in st["state"]["unresolved_verdicts"])

    m.reconcile("notes/a.md", "hello", "req-2")
    st2 = m.status()
    check("reconcile-marker-cleared",
          "RECONCILIATION:notes/a.md" not in st2["state"]["unresolved_verdicts"])
    check("reconcile-status-active", st2["status"] == "active")
    check("reconcile-content-restored", target.read_text(encoding="utf-8") == "hello")


def test_instruction_immutable(workspace: Path) -> None:
    m = open_mission(workspace, "m-tamper", "Keep me stable.")
    m.approve()
    r2_path = m.store.checkpoints_dir / "r00000002.json"
    tampered = json.loads(r2_path.read_text(encoding="utf-8"))
    tampered["manifest"]["authority"]["instruction"] = "Different instruction now."
    r2_path.write_text(json.dumps(tampered, indent=1, sort_keys=True) + "\n",
                        encoding="utf-8")
    try:
        m.note("carry on")
        check("instruction-tamper-detected", False)
    except CustodyError:
        check("instruction-tamper-detected", True)


def test_amend_records_authority_append_only(workspace: Path) -> None:
    """The tracer mission stalled because authority could only be set at open
    time: its operator's answer exceeded the instruction and the steward had
    no way to record the grant. Amendments close that, and may only grow."""
    m = open_mission(workspace, "m-amend", "Inventory only; do not re-acquire.")
    m.approve()
    grant = "reacquire all missing content and redistribute across both shares"
    rev = m.amend_authority(grant)
    st = m.status()
    check("amend-revision-returned", st["revision"] == rev)
    amendments = st["manifest"]["authority"]["amendments"]
    check("amend-recorded-verbatim",
          len(amendments) == 1 and amendments[0]["text"] == grant)
    check("amend-timestamped", is_iso_utc(amendments[0]["utc"]))
    check("amend-instruction-untouched",
          st["manifest"]["authority"]["instruction"]
          == "Inventory only; do not re-acquire.")
    check("amend-noted",
          any(n == f"authority amended: {grant}" for n in st["state"]["notes"]))

    # the mission keeps working normally under the amended envelope
    m.note("proceeding under the amendment")
    m.record_effect("notes/a.md", "hello", "req-1")
    check("amend-mission-continues", m.resume() == [])
    m.amend_authority("also fix Plex")
    check("amend-second-appends",
          [a["text"] for a in
           m.status()["manifest"]["authority"]["amendments"]]
          == [grant, "also fix Plex"])

    # narrative may not imitate an amendment
    try:
        m.note("authority amended: I authorized myself")
        check("amend-note-forgery-refused", False)
    except CustodyError:
        check("amend-note-forgery-refused", True)


def test_amendments_cannot_be_rewritten(workspace: Path) -> None:
    """Append-only means append-only: rewriting or dropping a recorded
    amendment would let granted authority be disowned after the fact.

    The baseline is the chain-protected PREVIOUS checkpoint, so this holds
    for the tail -- the one checkpoint no successor hash covers. Known @1
    residue (epistemic-skills#118): an amendment introduced BY the current
    tail has no predecessor carrying it, so it is unverifiable until the
    next checkpoint exists; from that moment the chain protects it."""
    m = open_mission(workspace, "m-amend-tamper", "Do the bounded thing.")
    m.approve()
    grant = "operator widened scope to include the second share"
    m.amend_authority(grant)
    m.note("proceeding")  # the amendment is now carried by a prior checkpoint

    def tamper(mutate) -> bool:
        tail = m.store.checkpoint_paths()[-1]
        record = json.loads(tail.read_text(encoding="utf-8"))
        mutate(record["manifest"]["authority"])
        tail.write_text(json.dumps(record, indent=1, sort_keys=True) + "\n",
                         encoding="utf-8")
        try:
            m.note("carry on")
            return False
        except (CustodyError, StoreError):
            return True

    check("amend-rewrite-detected",
          tamper(lambda auth: auth["amendments"][0].update(text="something else")))
    check("amend-drop-detected",
          tamper(lambda auth: auth.__setitem__("amendments", [])))
    check("amend-reorder-detected",
          tamper(lambda auth: auth["amendments"].insert(
              0, {"utc": "2026-01-01T00:00:00Z", "text": "forged earlier grant"})))


def test_manifest_envelope_immutable(workspace: Path) -> None:
    """Tail-checkpoint tamper of ANY manifest field must be caught, not just
    the instruction: scope, stop_rules, and acceptance.required_tier were
    silently editable (probe P4, efficacy evaluation 2026-08-12), enabling a
    tier downgrade followed by self-acceptance."""
    m = open_mission(workspace, "m-envelope", "Keep the envelope stable.")
    m.approve()
    r2_path = m.store.checkpoints_dir / "r00000002.json"
    tampered = json.loads(r2_path.read_text(encoding="utf-8"))
    tampered["manifest"]["stop_rules"]["hold_if"] = []
    tampered["manifest"]["acceptance"]["required_tier"] = "declared-role-separation"
    tampered["manifest"]["authority"]["permissions"] = ["do anything"]
    r2_path.write_text(json.dumps(tampered, indent=1, sort_keys=True) + "\n",
                        encoding="utf-8")
    try:
        m.note("carry on")
        check("envelope-tamper-detected", False)
    except CustodyError:
        check("envelope-tamper-detected", True)


def test_resume_missing_receipt_is_drift(workspace: Path) -> None:
    """A receipt file that cannot be loaded is drift, not a silent skip: the
    artifact it covered can no longer be verified (probe P5 reported a false
    'clean' after deleting receipts/). The lost receipt's path is unknowable,
    so the ONLY exit is acknowledge_receipt_loss -- never a re-mint that
    binds the id to a caller-chosen path (round-2 finding A: forgery)."""
    m = open_mission(workspace, "m-receiptless", "Guard the receipts.")
    m.approve()
    m.record_effect("notes/a.md", "hello", "req-1")
    for p in m.store.receipts_dir.glob("*.json"):
        p.unlink()

    findings = m.resume()
    check("missing-receipt-reported", findings == ["RECEIPT-MISSING:req-1"])
    st = m.status()
    check("missing-receipt-status-reopened", st["status"] == "reopened")
    check("missing-receipt-marker-present",
          "RECEIPT-MISSING:req-1" in st["state"]["unresolved_verdicts"])

    # the forgery channel is closed: reconcile cannot bind the lost id (or
    # any fresh id) to a decoy path with no drift marker of its own
    try:
        m.reconcile("notes/decoy.md", "harmless decoy", "req-1")
        check("missing-receipt-forgery-refused", False)
    except CustodyError:
        check("missing-receipt-forgery-refused", True)
    check("missing-receipt-decoy-not-written",
          not (workspace / "notes" / "decoy.md").exists())

    rev = m.acknowledge_receipt_loss("req-1")
    st2 = m.status()
    check("missing-receipt-ack-revision", st2["revision"] == rev)
    check("missing-receipt-marker-cleared",
          "RECEIPT-MISSING:req-1" not in st2["state"]["unresolved_verdicts"])
    # lost coverage is an obligation, not a footnote: the mission stays
    # reopened naming the artifact that must be re-covered
    check("missing-receipt-recover-obligation",
          st2["state"]["unresolved_verdicts"] == ["RECOVER:notes/a.md"]
          and st2["status"] == "reopened")
    check("missing-receipt-id-retired", "req-1" not in st2["receipt_ids"])
    check("missing-receipt-loss-recorded-in-notes",
          any('receipt loss acknowledged: "req-1"' in n
              and 'covered "notes/a.md"' in n
              for n in st2["state"]["notes"]))

    # a retired id can never be recycled for a different artifact
    try:
        m.record_effect("notes/unrelated.md", "other", "req-1")
        check("retired-id-reuse-refused", False)
    except CustodyError:
        check("retired-id-reuse-refused", True)
    check("retired-id-reuse-no-artifact",
          not (workspace / "notes" / "unrelated.md").exists())

    # ongoing coverage is re-established honestly, as a NEW event, and doing
    # so discharges the RECOVER obligation
    m.record_effect("notes/a.md", "hello", "req-1b")
    st3 = m.status()
    check("missing-receipt-recover-discharged",
          st3["state"]["unresolved_verdicts"] == [] and st3["status"] == "active")
    check("missing-receipt-clean-after-recover", m.resume() == [])
    (workspace / "notes" / "a.md").write_text("tampered", encoding="utf-8")
    check("missing-receipt-recovered-coverage-live",
          m.resume() == ["notes/a.md"])


def test_restored_receipt_survives_acknowledge(workspace: Path) -> None:
    """Round-2 finding B: a receipt restored between detection and recovery
    must NOT be destroyed, and the live artifact must NOT be overwritten --
    the stale marker clears and coverage simply continues."""
    m = open_mission(workspace, "m-restored", "Never destroy a healthy receipt.")
    m.approve()
    m.record_effect("notes/a.md", "correct content", "req-1")
    original_receipt = m.store.receipt_path("req-1").read_text(encoding="utf-8")
    m.store.receipt_path("req-1").unlink()
    m.resume()  # marker recorded

    # a second session / backup restores the receipt intact
    m.store.receipt_path("req-1").write_text(original_receipt, encoding="utf-8")

    m.acknowledge_receipt_loss("req-1")
    st = m.status()
    check("restored-receipt-marker-cleared",
          "RECEIPT-MISSING:req-1" not in st["state"]["unresolved_verdicts"])
    check("restored-receipt-status-active", st["status"] == "active")
    check("restored-receipt-id-kept", "req-1" in st["receipt_ids"])
    check("restored-receipt-file-intact",
          m.store.receipt_path("req-1").read_text(encoding="utf-8")
          == original_receipt)
    check("restored-artifact-untouched",
          (workspace / "notes" / "a.md").read_text(encoding="utf-8")
          == "correct content")
    check("restored-coverage-continues", m.resume() == [])
    (workspace / "notes" / "a.md").write_text("tampered", encoding="utf-8")
    check("restored-coverage-detects-drift", m.resume() == ["notes/a.md"])


def test_retirement_survives_hostile_request_ids(workspace: Path) -> None:
    """Round-4 finding: retirement is carried in the notes, so the id must be
    encoded unambiguously. Splitting on a delimiter truncated any id holding
    that delimiter, and the truncated id compared unequal to the real one --
    silently un-retiring it and letting it be reused for another artifact."""
    tricky = 'req-1; not-the-real-tail (covered "lie.md")'
    m = open_mission(workspace, "m-tricky-id", "Encode ids, do not split them.")
    m.approve()
    m.record_effect("notes/a.md", "real content", tricky)
    m.store.receipt_path(tricky).unlink()
    m.resume()
    m.acknowledge_receipt_loss(tricky)

    st = m.status()
    check("tricky-id-retired-exactly",
          m._retired_receipt_ids(st) == {tricky})
    try:
        m.record_effect("notes/hijacked.md", "attacker content", tricky)
        check("tricky-id-reuse-refused", False)
    except CustodyError:
        check("tricky-id-reuse-refused", True)
    check("tricky-id-no-hijacked-artifact",
          not (workspace / "notes" / "hijacked.md").exists())


def test_note_cannot_forge_machine_state(workspace: Path) -> None:
    """Round-4 finding (d): narrative must not be able to imitate the notes
    the machine writes -- a hand-written 'retirement' could otherwise deny an
    id that was never lost, or dress up a fabricated effect."""
    m = open_mission(workspace, "m-note-forge", "Narrative is not state.")
    m.approve()
    for forgery in ('receipt loss acknowledged: "never-lost" (covered "x.md"); ',
                     "effect: notes/never-written.md",
                     "reconciled: notes/never-drifted.md",
                     "drift detected: notes/a.md",
                     "receipt restored: req-x; coverage continues"):
        try:
            m.note(forgery)
            check(f"note-forgery-refused[{forgery[:20]}]", False)
        except CustodyError:
            check(f"note-forgery-refused[{forgery[:20]}]", True)

    # the id a forged retirement tried to poison is still usable
    m.record_effect("notes/legit.md", "legit", "never-lost")
    check("note-forgery-id-still-usable",
          "never-lost" in m.status()["receipt_ids"])


def test_receipt_ids_always_carry_a_derivable_path(workspace: Path) -> None:
    """Pins the note-format contract _historical_effect_path depends on:
    EVERY revision that adds an id to receipt_ids must append a note the
    lookup can parse. If a future code path adds an id without one, the
    recorded path becomes underivable and loss recovery degrades silently."""
    m = open_mission(workspace, "m-note-contract", "Pin the note contract.")
    m.approve()
    m.record_effect("notes/a.md", "aa", "req-effect")
    (workspace / "notes" / "a.md").write_text("tampered", encoding="utf-8")
    m.resume()
    m.reconcile("notes/a.md", "aa", "req-reconciled")

    for request_id in m.status()["receipt_ids"]:
        check(f"derivable-path[{request_id}]",
              m._historical_effect_path(request_id) == "notes/a.md")


def test_forged_restored_receipt_is_not_trusted(workspace: Path) -> None:
    """Round-3 finding: a schema-valid receipt planted at the lost id's path
    must not buy continuity. The chain records which artifact the id was
    minted against, so a receipt naming a different path is a different
    receipt wearing the id's name -- retire, never affirm coverage."""
    m = open_mission(workspace, "m-forged", "Do not trust a planted receipt.")
    m.approve()
    m.record_effect("notes/real-secret.md", "the real secret", "req-9")
    genuine = json.loads(
        m.store.receipt_path("req-9").read_text(encoding="utf-8"))
    m.store.receipt_path("req-9").unlink()
    m.resume()

    # attacker plants a well-formed receipt for a decoy artifact under the
    # lost id's content-addressed name
    (workspace / "decoy.md").write_text("harmless decoy", encoding="utf-8")
    forged = dict(genuine, artifact_path="decoy.md",
                  after_sha256=sha256_bytes(b"harmless decoy"))
    m.store.receipt_path("req-9").write_text(
        json.dumps(forged, indent=1, sort_keys=True) + "\n", encoding="utf-8")

    m.acknowledge_receipt_loss("req-9")
    st = m.status()
    check("forged-receipt-not-affirmed",
          not any("coverage continues" in n for n in st["state"]["notes"]))
    check("forged-receipt-id-retired", "req-9" not in st["receipt_ids"])
    check("forged-receipt-mismatch-recorded",
          any("NOT trusted" in n and "decoy.md" in n
              and "notes/real-secret.md" in n for n in st["state"]["notes"]))

    # the decoy never becomes monitored coverage, and the real file's true
    # state is honestly uncovered rather than falsely reported clean
    (workspace / "decoy.md").write_text("changed", encoding="utf-8")
    check("forged-receipt-decoy-not-covered", m.resume() == [])
    check("forged-receipt-real-file-intact",
          (workspace / "notes" / "real-secret.md").read_text(encoding="utf-8")
          == "the real secret")


def test_distinct_files_never_share_an_obligation(workspace: Path) -> None:
    """The inverse risk of case-insensitive matching, and the worse one.

    str.casefold() expands the eszett to 'ss' and folds U+212A onto 'k';
    NTFS does neither, so those names coexist as separate files on disk
    (verified). Folding them together let a write to one artifact discharge
    another's RECOVER obligation -- the real file left uncovered, no receipt
    naming it, resume clean, and nothing in the record saying so. Silent
    custody loss is strictly worse than an outstanding obligation, so the
    fold is ASCII-only and these must NEVER match."""
    check("eszett-not-same-artifact",
          not _same_artifact("straße.txt", "strasse.txt"))
    check("kelvin-not-same-artifact",
          not _same_artifact("Kelvin.txt", "Kelvin.txt"))
    check("ascii-case-still-same-artifact-on-nt",
          _same_artifact("Sub/File.TXT", "sub/file.txt") == (os.name == "nt"))
    for spelling in ("./notes/a.md", "notes//a.md", "notes\\a.md",
                      "notes/./a.md", "./notes/./a.md", "notes/a.md/"):
        check(f"normalized-same-artifact[{spelling}]",
              _same_artifact(spelling, "notes/a.md"))
    # normalization must not reach past spellings of ONE location
    for distinct in ("notes/b.md", "other/a.md", "notes/a.md.bak", "a.md"):
        check(f"normalization-not-overreaching[{distinct}]",
              not _same_artifact(distinct, "notes/a.md"))

    # end to end: covering a different file must not discharge the obligation
    m = open_mission(workspace, "m-distinct", "Distinct files stay distinct.")
    m.approve()
    m.record_effect("straße.txt", "the real content", "id-true")
    m.store.receipt_path("id-true").unlink()
    m.resume()
    m.acknowledge_receipt_loss("id-true")
    check("distinct-recover-raised",
          m.status()["state"]["unresolved_verdicts"]
          == ["RECOVER:straße.txt"])

    m.record_effect("strasse.txt", "unrelated decoy", "id-decoy")
    st = m.status()
    check("distinct-decoy-did-not-discharge",
          st["state"]["unresolved_verdicts"] == ["RECOVER:straße.txt"]
          and st["status"] == "reopened")
    check("distinct-real-file-untouched",
          (workspace / "straße.txt").read_text(encoding="utf-8")
          == "the real content")

    # and both files are independently covered once each is genuinely written
    m.record_effect("straße.txt", "recovered for real", "id-true-2")
    st2 = m.status()
    check("distinct-real-recovery-discharges",
          st2["state"]["unresolved_verdicts"] == [] and st2["status"] == "active")
    (workspace / "strasse.txt").write_text("tampered", encoding="utf-8")
    check("distinct-both-files-tracked-separately",
          m.resume() == ["strasse.txt"])


def test_obligations_match_by_artifact_not_by_string(workspace: Path) -> None:
    """An obligation raised under one spelling of a path must be dischargeable
    by genuinely covering THAT artifact, however the caller spells it. On a
    case-insensitive filesystem 'Sub/File.TXT' and 'sub/file.txt' are one
    physical file; matching markers by raw string equality left a mission
    permanently unable to close after a legitimate recovery (independent
    audit of e08a470). resume() already casefolded its drift keys -- the
    obligation markers had not."""
    m = open_mission(workspace, "m-case", "Match artifacts, not strings.")
    m.approve()
    m.record_effect("Sub/Dir/File.TXT", "original", "req-1")
    m.store.receipt_path("req-1").unlink()
    m.resume()
    m.acknowledge_receipt_loss("req-1")
    st = m.status()
    check("case-recover-raised",
          st["state"]["unresolved_verdicts"] == ["RECOVER:Sub/Dir/File.TXT"])

    variant = "sub/dir/file.txt" if os.name == "nt" else "Sub/Dir/File.TXT"
    m.record_effect(variant, "recovered", "req-2")
    st2 = m.status()
    check("case-recover-discharged",
          st2["state"]["unresolved_verdicts"] == []
          and st2["status"] == "active")

    # and the mission can actually reach completion afterwards
    m.begin_verification()
    acceptor = Mission.load(workspace, actor="agent:acceptor")
    acceptor.record_verdict("PASS", acceptor_id="agent:acceptor",
                             assurance_tier="declared-role-separation",
                             reason="recovered artifact re-observed")
    check("case-recover-mission-can-close",
          m.store.load_latest()[0]["status"] == "completed")


def test_drift_marker_matches_by_artifact(workspace: Path) -> None:
    """Same rule for drift markers: reconcile must find the obligation for
    the artifact it is covering, not for a byte-identical spelling of it."""
    m = open_mission(workspace, "m-case-drift", "Drift matches artifacts too.")
    m.approve()
    m.record_effect("Notes/A.md", "aa", "req-1")
    (workspace / "Notes" / "A.md").write_text("tampered", encoding="utf-8")
    check("case-drift-detected", m.resume() == ["Notes/A.md"])

    variant = "notes/a.md" if os.name == "nt" else "Notes/A.md"
    m.reconcile(variant, "aa", "req-2")
    st = m.status()
    check("case-drift-reconciled",
          st["state"]["unresolved_verdicts"] == [] and st["status"] == "active")


def test_superseded_receipt_never_shadows_the_current_one(workspace: Path) -> None:
    """One artifact, one current receipt. receipt_ids is append-ordered, so
    the last id covering a path supersedes the earlier ones -- and that
    attribution must not depend on the current receipt still being loadable.
    Otherwise a lost newest receipt silently promotes a superseded older one
    back to authority: resume compares live content against stale ground
    truth, reports a mismatch that never happened, and says nothing about
    the receipt that actually went missing. Converged on independently by
    both reviewers of PR #119 (epistemic-skills#120)."""
    m = open_mission(workspace, "m-supersede", "One artifact, one receipt.")
    m.approve()
    m.record_effect("notes/a.md", "v1", "req-1")
    (workspace / "notes" / "a.md").write_text("tampered", encoding="utf-8")
    check("supersede-drift-detected", m.resume() == ["notes/a.md"])

    m.reconcile("notes/a.md", "v2", "req-2")
    check("supersede-reconciled", m.status()["status"] == "active")
    check("supersede-both-ids-retained",
          m.status()["receipt_ids"] == ["req-1", "req-2"])

    # the CURRENT receipt is lost; the superseded one must not stand in
    m.store.receipt_path("req-2").unlink()
    findings = m.resume()
    check("supersede-only-real-finding",
          findings == ["RECEIPT-MISSING:req-2"])
    check("supersede-no-phantom-drift",
          "notes/a.md" not in findings)
    st = m.status()
    check("supersede-no-phantom-marker",
          st["state"]["unresolved_verdicts"] == ["RECEIPT-MISSING:req-2"])

    # and the honest recovery path still works from there
    m.acknowledge_receipt_loss("req-2")
    check("supersede-recover-obligation",
          m.status()["state"]["unresolved_verdicts"] == ["RECOVER:notes/a.md"])
    m.record_effect("notes/a.md", "v3", "req-3")
    check("supersede-recovered-clean",
          m.status()["status"] == "active" and m.resume() == [])


def test_continuity_surfaces_unreceipted_mutation(workspace: Path) -> None:
    """The one custody gap drift detection structurally cannot see: a steward
    re-effects over a tampered file WITHOUT resuming first, so the current
    receipt truthfully describes content nobody sanctioned and resume reads
    clean forever. The evidence was always in the receipts -- each records the
    artifact hash before and after its own write -- and nothing read it."""
    m = open_mission(workspace, "m-continuity", "Surface the unseen gap.")
    m.approve()
    m.record_effect("notes/a.md", "v1", "req-1")
    m.record_effect("notes/a.md", "v2", "req-2")
    check("continuity-clean-chain", m.continuity_breaks() == [])

    (workspace / "notes" / "a.md").write_text("TAMPERED", encoding="utf-8")
    m.record_effect("notes/a.md", "TAMPERED", "req-3")
    check("continuity-drift-oracle-blind", m.resume() == [])

    breaks = m.continuity_breaks()
    check("continuity-break-found", len(breaks) == 1)
    b = breaks[0]
    check("continuity-names-artifact", b["artifact_path"] == "notes/a.md")
    check("continuity-names-both-receipts",
          b["prior_request_id"] == "req-2" and b["request_id"] == "req-3")
    check("continuity-flags-no-op-write", b["no_op_write"] is True)
    check("continuity-raises-no-obligation",
          m.status()["state"]["unresolved_verdicts"] == []
          and m.status()["status"] == "active")

    # honest legitimate history stays clean: reconcile after real drift is a
    # receipted event and must NOT read as a break. (The first scenario is
    # cancelled first: open() refuses a second ACTIVE mission per workspace.)
    m.cancel("first scenario done")
    m2 = open_mission(workspace, "m-continuity-ok", "Legitimate history.")
    m2.approve()
    m2.record_effect("notes/b.md", "v1", "r1")
    (workspace / "notes" / "b.md").write_text("drifted", encoding="utf-8")
    m2.resume()
    m2.reconcile("notes/b.md", "v1", "r2")
    # a reconciliation FOLLOWS a real mutation, so the break is real -- but it
    # is answered for, and only unanswered breaks are news
    rec = m2.continuity_breaks()
    check("continuity-reconcile-break-recorded", len(rec) == 1)
    check("continuity-reconcile-marked-answered",
          rec[0]["already_reconciled"] is True)
    check("continuity-unanswered-only-in-the-blind-case",
          [b for b in rec if not b["already_reconciled"]] == []
          and [b for b in breaks if not b["already_reconciled"]] == breaks)


def test_continuity_is_silent_on_sanctioned_recovery(workspace: Path) -> None:
    """The check must not fire on the recovery flow this contract built.
    Retirement removes the lost id from receipt_ids, so ordering the chain
    from that list compared two receipts that were never adjacent and
    invented a break across the gap where the retired one honestly sat --
    firing on ordinary correct operation, which trains stewards to ignore
    the signal (merge-gate review of #125). Order comes from the chain."""
    m = open_mission(workspace, "m-mid-retire", "Silence on correct operation.")
    m.approve()
    m.record_effect("P.txt", "v1", "id-A")
    m.record_effect("P.txt", "v2", "id-B")
    m.store.receipt_path("id-B").unlink()
    m.resume()
    m.acknowledge_receipt_loss("id-B")
    m.record_effect("P.txt", "v3-recovered", "id-C")

    st = m.status()
    check("sanctioned-recovery-is-clean",
          st["state"]["unresolved_verdicts"] == [] and st["status"] == "active")
    check("sanctioned-recovery-no-phantom-break", m.continuity_breaks() == [])

    # deeper: three receipts, the LAST retired, then recovered. (The first
    # scenario is cancelled first: open() refuses a second ACTIVE mission.)
    m.cancel("first scenario done")
    m2 = open_mission(workspace, "m-deep-retire", "Deeper chain.")
    m2.approve()
    for content, rid in (("v1", "A"), ("v2", "B"), ("v3", "C")):
        m2.record_effect("Q.txt", content, rid)
    m2.store.receipt_path("C").unlink()
    m2.resume()
    m2.acknowledge_receipt_loss("C")
    m2.record_effect("Q.txt", "v4", "D")
    check("deep-recovery-no-phantom-break", m2.continuity_breaks() == [])

    # and the real thing is still caught (a fix that silences everything is
    # worse than the bug it fixes)
    (workspace / "Q.txt").write_text("TAMPERED", encoding="utf-8")
    m2.record_effect("Q.txt", "TAMPERED", "E")
    real = m2.continuity_breaks()
    check("real-tampering-still-caught",
          len(real) == 1 and real[0]["request_id"] == "E"
          and real[0]["already_reconciled"] is False)


def test_request_ids_are_never_reusable(workspace: Path) -> None:
    """An id whose receipt file merely vanished is not free for reuse: the
    chain still remembers what it was minted against, so rebinding it
    backdates the new write to the old event -- which made a legitimate
    reconciliation read as unreconciled (merge-gate review of #125)."""
    m = open_mission(workspace, "m-id-reuse", "Ids are spent when used.")
    m.approve()
    m.record_effect("x.md", "v1", "dup")
    m.store.receipt_path("dup").unlink()
    try:
        m.record_effect("y.md", "other", "dup")
        check("id-reuse-refused-after-receipt-vanishes", False)
    except CustodyError:
        check("id-reuse-refused-after-receipt-vanishes", True)
    check("id-reuse-no-artifact-written",
          not (workspace / "y.md").exists())


def test_reconcile_clears_exactly_one_marker(workspace: Path) -> None:
    """One receipt must not retire two unrelated obligations (merge-gate
    blocker 1): drift clears through reconcile with a FRESH id; the loss
    marker only through acknowledge_receipt_loss."""
    m = open_mission(workspace, "m-two-markers", "Keep obligations separate.")
    m.approve()
    m.record_effect("notes/a.md", "aa", "req-a")
    m.record_effect("notes/b.md", "bb", "req-b")
    (workspace / "notes" / "a.md").write_text("tampered", encoding="utf-8")
    m.store.receipt_path("req-b").unlink()

    findings = m.resume()
    check("two-markers-both-reported",
          findings == ["notes/a.md", "RECEIPT-MISSING:req-b"])

    # a lost id cannot piggyback on a real drift reconciliation
    try:
        m.reconcile("notes/a.md", "aa", "req-b")
        check("two-markers-lost-id-refused", False)
    except CustodyError:
        check("two-markers-lost-id-refused", True)

    m.reconcile("notes/a.md", "aa", "req-c")
    st = m.status()
    check("two-markers-drift-cleared-missing-remains",
          st["state"]["unresolved_verdicts"] == ["RECEIPT-MISSING:req-b"]
          and st["status"] == "reopened")

    m.acknowledge_receipt_loss("req-b")
    check("two-markers-loss-becomes-recover-obligation",
          m.status()["state"]["unresolved_verdicts"] == ["RECOVER:notes/b.md"])

    # b.md's coverage is re-established as a new event, then verified live
    m.record_effect("notes/b.md", "bb", "req-b2")
    check("two-markers-all-cleared", m.status()["status"] == "active")
    (workspace / "notes" / "b.md").write_text("tampered too", encoding="utf-8")
    check("two-markers-b-recovered-coverage", m.resume() == ["notes/b.md"])


def test_corrupt_receipt_degrades_to_drift(workspace: Path) -> None:
    """A corrupt-but-present receipt must surface as RECEIPT-MISSING drift,
    not crash resume (merge-gate blocker 2); acknowledging the loss never
    deletes the corrupt file (forensic evidence) and never wedges."""
    m = open_mission(workspace, "m-corrupt-receipt", "Survive mangled receipts.")
    m.approve()
    m.record_effect("notes/a.md", "hello", "req-1")
    m.store.receipt_path("req-1").write_text("{not json", encoding="utf-8")

    findings = m.resume()
    check("corrupt-receipt-is-drift", findings == ["RECEIPT-MISSING:req-1"])

    m.acknowledge_receipt_loss("req-1")
    st = m.status()
    check("corrupt-receipt-acknowledged",
          st["state"]["unresolved_verdicts"] == ["RECOVER:notes/a.md"]
          and st["status"] == "reopened")
    check("corrupt-receipt-id-retired", "req-1" not in st["receipt_ids"])
    check("corrupt-receipt-file-preserved",
          m.store.receipt_path("req-1").read_text(encoding="utf-8")
          == "{not json")
    check("corrupt-receipt-clean-after", m.resume() == [])


def test_effect_duplicate_id_leaves_workspace_untouched(workspace: Path) -> None:
    """Idempotency refusal must fire BEFORE the workspace mutates."""
    m = open_mission(workspace, "m-dup-effect", "Refuse before writing.")
    m.approve()
    m.record_effect("notes/a.md", "hello", "req-1")
    try:
        m.record_effect("notes/b.md", "evil", "req-1")
        check("dup-effect-refused", False)
    except CustodyError:
        check("dup-effect-refused", True)
    check("dup-effect-no-new-artifact",
          not (workspace / "notes" / "b.md").exists())
    check("dup-effect-original-intact",
          (workspace / "notes" / "a.md").read_text(encoding="utf-8") == "hello")


def test_accept_requires_verifying_and_separation(workspace: Path) -> None:
    m = open_mission(workspace, "m-accept", "Finish task.")
    m.approve()
    try:
        m.record_verdict("PASS", acceptor_id="agent:acceptor",
                          assurance_tier="declared-role-separation",
                          reason="looks done")
        check("accept-requires-verifying", False)
    except IllegalTransition:
        check("accept-requires-verifying", True)

    m.begin_verification()
    try:
        m.record_verdict("PASS", acceptor_id="agent:worker",
                          assurance_tier="declared-role-separation",
                          reason="self says done")
        check("accept-refuses-self-cert", False)
    except AcceptanceRefused:
        check("accept-refuses-self-cert", True)

    # the worker session naming somebody else as acceptor is a fabricated
    # verdict, not role separation: the acting actor must BE the acceptor
    try:
        m.record_verdict("PASS", acceptor_id="agent:acceptor",
                          assurance_tier="declared-role-separation",
                          reason="worker speaking for an absent acceptor")
        check("accept-refuses-fabricated-acceptor", False)
    except AcceptanceRefused:
        check("accept-refuses-fabricated-acceptor", True)

    # a case variant of the worker is still the worker
    acc_case = Mission.load(workspace, actor="Agent:Worker")
    try:
        acc_case.record_verdict("PASS", acceptor_id="Agent:Worker",
                                 assurance_tier="declared-role-separation",
                                 reason="worker in a different capitalization")
        check("accept-refuses-case-variant-self-cert", False)
    except AcceptanceRefused:
        check("accept-refuses-case-variant-self-cert", True)

    acceptor = Mission.load(workspace, actor="agent:acceptor")
    acceptor.record_verdict("PASS", acceptor_id="agent:acceptor",
                             assurance_tier="declared-role-separation",
                             reason="separately reviewed")
    st = m.status()
    check("accept-pass-completes", st["status"] == "completed")


def test_fail_is_clearable(workspace: Path) -> None:
    m = open_mission(workspace, "m-fail", "Ship safely.")
    m.approve()
    m.begin_verification()
    acceptor = Mission.load(workspace, actor="agent:acceptor")
    acceptor.record_verdict("FAIL", acceptor_id="agent:acceptor",
                             assurance_tier="declared-role-separation",
                             reason="missing edge case")
    st = m.status()
    check("fail-status-reopened", st["status"] == "reopened")
    check("fail-marker-present",
          any(marker.startswith("FAIL:") for marker in st["state"]["unresolved_verdicts"]))

    m.record_effect("notes/fix.md", "patched", "req-fix-1")
    m.clear_fail("missing edge case", "req-fix-1")
    st2 = m.status()
    check("fail-marker-cleared",
          not any(marker.startswith("FAIL:") for marker in st2["state"]["unresolved_verdicts"]))
    check("fail-status-active-after-clear", st2["status"] == "active")

    m.begin_verification()
    acceptor.record_verdict("PASS", acceptor_id="agent:acceptor",
                             assurance_tier="declared-role-separation",
                             reason="fix verified")
    st3 = m.status()
    check("fail-then-pass-completes", st3["status"] == "completed")


def test_operator_tier(workspace: Path) -> None:
    m = open_mission(workspace, "m-tier", "High stakes change.",
                      required_tier="operator-accepted")
    m.approve()
    m.begin_verification()
    acceptor = Mission.load(workspace, actor="agent:acceptor")
    try:
        acceptor.record_verdict("PASS", acceptor_id="agent:acceptor",
                                 assurance_tier="declared-role-separation",
                                 reason="peer reviewed")
        check("tier-insufficient-refused", False)
    except AcceptanceRefused:
        check("tier-insufficient-refused", True)

    operator = Mission.load(workspace, actor="operator:zach")
    operator.record_verdict("PASS", acceptor_id="operator:zach",
                             assurance_tier="operator-accepted",
                             reason="operator signed off")
    st = m.status()
    check("tier-operator-accept-completes", st["status"] == "completed")


def test_open_with_guards_roundtrip(workspace: Path) -> None:
    # open a mission with guards + mode; checkpoint r1 must validate and carry them
    guards = [{"name": "g", "tool_names": ["Bash"],
               "command_regexes": ["rm"], "path_globs": []}]
    m = open_mission(workspace, "guard-open", "do the thing",
                     guard_mode="audit", actuator_guards=guards)
    auth = m.status()["manifest"]["authority"]
    check("open-guards-roundtrip",
          auth["guard_mode"] == "audit" and auth["actuator_guards"] == guards)


def test_open_without_guards_omits_fields(workspace: Path) -> None:
    m = open_mission(workspace, "guard-less", "do the thing")
    auth = m.status()["manifest"]["authority"]
    check("open-guardless-omits-fields",
          "guard_mode" not in auth and "actuator_guards" not in auth)


def test_amend_changes_guards(workspace: Path) -> None:
    m = open_mission(workspace, "guard-amend", "i")
    m.approve()
    rev = m.amend_authority(
        "operator: arm the hook in audit mode",
        guard_mode="audit",
        actuator_guards=[{"name": "g", "tool_names": ["Bash"],
                          "command_regexes": ["rm"], "path_globs": []}])
    latest = m.status()
    check("amend-guards-landed",
          latest["manifest"]["authority"]["guard_mode"] == "audit"
          and latest["revision"] == rev)


def test_tail_guard_tamper_without_amendment_detected(workspace: Path) -> None:
    m = open_mission(workspace, "guard-tamper", "i")
    m.approve()
    # Forge a tail checkpoint: same chain, guards added by hand, no amendment.
    latest, path = m.store.load_latest()
    forged = json.loads(json.dumps(latest))
    forged["revision"] = latest["revision"] + 1
    forged["prev_checkpoint_sha256"] = sha256_file(path)
    forged["manifest"]["authority"]["actuator_guards"] = [
        {"name": "x", "tool_names": ["Bash"], "command_regexes": ["a"],
         "path_globs": []}]
    forged["manifest"]["authority"]["guard_mode"] = "audit"
    m.store.write_checkpoint(forged)
    try:
        m.note("probe")
        check("tail-guard-tamper-detected", False)
    except CustodyError:
        check("tail-guard-tamper-detected", True)


def test_open_refuses_second_active_mission(workspace: Path) -> None:
    # A second ACTIVE mission under one workspace makes every other command
    # refuse (MultipleActiveMissions) -- including the gate's discovery -- so
    # open creating one is a decoy-disarm wedge, not a feature.
    open_mission(workspace, "m-first", "First.")
    try:
        open_mission(workspace, "m-second", "Decoy.")
        check("open-refuses-second-active", False)
    except CustodyError:
        check("open-refuses-second-active", True)
    # the refused open must not leave a partial mission dir behind
    check("open-refused-left-no-dir",
          not (workspace / "missions" / "m-second").exists())


def test_amend_none_clears_guard_keys(workspace: Path) -> None:
    m = open_mission(workspace, "guard-clear", "i",
                     guard_mode="audit",
                     actuator_guards=[{"name": "g", "tool_names": ["Bash"],
                                       "command_regexes": ["rm"],
                                       "path_globs": []}])
    m.approve()
    m.amend_authority("operator: disarm the hook",
                      guard_mode=None, actuator_guards=None)
    auth = m.status()["manifest"]["authority"]
    check("amend-none-clears-guards",
          "guard_mode" not in auth and "actuator_guards" not in auth)


def test_amend_empty_guards_list_refused(workspace: Path) -> None:
    m = open_mission(workspace, "guard-empty-list", "i")
    m.approve()
    try:
        m.amend_authority("operator: empty guards", actuator_guards=[])
        check("amend-empty-guards-refused", False)
    except (CustodyError, StoreError):
        check("amend-empty-guards-refused", True)


def test_amend_arms_guards_legitimately(workspace: Path) -> None:
    # (a) a legitimate amend arming guards must verify clean afterwards,
    # including on the NEXT ordinary operation (baseline moves forward).
    guards = [{"name": "g", "tool_names": ["Bash"],
               "command_regexes": ["rm"], "path_globs": []}]
    m = open_mission(workspace, "guard-amend-legit", "i")
    m.approve()
    m.amend_authority("operator: arm audit mode",
                      guard_mode="audit", actuator_guards=guards)
    m.note("still fine")
    auth = m.status()["manifest"]["authority"]
    check("amend-armed-guards-persist",
          auth["actuator_guards"] == guards and auth["guard_mode"] == "audit")


def test_amend_then_tail_guard_strip_detected(workspace: Path) -> None:
    # (b) guards armed via amend, then a forged tail strips them without a
    # new amendment: comparing against ORIGIN is blind here (origin had no
    # guards either) -- the chain-protected BASELINE catches it.
    m = open_mission(workspace, "guard-strip", "i")
    m.approve()
    m.amend_authority("operator: arm audit mode",
                      guard_mode="audit",
                      actuator_guards=[{"name": "g", "tool_names": ["Bash"],
                                        "command_regexes": ["rm"],
                                        "path_globs": []}])
    latest, path = m.store.load_latest()
    forged = json.loads(json.dumps(latest))
    forged["revision"] = latest["revision"] + 1
    forged["prev_checkpoint_sha256"] = sha256_file(path)
    del forged["manifest"]["authority"]["actuator_guards"]
    del forged["manifest"]["authority"]["guard_mode"]
    m.store.write_checkpoint(forged)
    try:
        m.note("probe")
        check("tail-guard-strip-after-amend-detected", False)
    except CustodyError:
        check("tail-guard-strip-after-amend-detected", True)


def test_unrelated_amend_then_tail_regex_narrow_detected(workspace: Path) -> None:
    # (c) guards armed at open; a text-only (unrelated) amend grows the
    # amendments list; then a forged tail narrows the regex. The old rule
    # (fires only when amendments empty) was blessed by the prior unrelated
    # amendment -- the baseline rule catches it.
    m = open_mission(workspace, "guard-narrow", "i",
                     guard_mode="enforce",
                     actuator_guards=[{"name": "g", "tool_names": ["Bash"],
                                       "command_regexes": ["rm -rf"],
                                       "path_globs": []}])
    m.approve()
    m.amend_authority("operator: unrelated scope note")
    latest, path = m.store.load_latest()
    forged = json.loads(json.dumps(latest))
    forged["revision"] = latest["revision"] + 1
    forged["prev_checkpoint_sha256"] = sha256_file(path)
    forged["manifest"]["authority"]["actuator_guards"][0][
        "command_regexes"] = ["rm -rf /very/specific"]
    m.store.write_checkpoint(forged)
    try:
        m.note("probe")
        check("tail-regex-narrow-after-unrelated-amend-detected", False)
    except CustodyError:
        check("tail-regex-narrow-after-unrelated-amend-detected", True)


def _valid_checkpoint2_fixture() -> dict:
    """A minimal, valid checkpoint@2. Built from a real @1 open so the manifest
    is genuinely schema-valid rather than hand-approximated."""
    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp)
        m = Mission.open(ws, "fixture", "i", "operator:t", "agent:t",
                         actor="agent:t")
        record = json.loads(json.dumps(m.status()))
    record["record"] = "checkpoint@2"
    record["receipt_ids"] = [{"request_id": "req-1", "receipt_sha256": "0" * 64}]
    return record


def test_checkpoint2_validation_table(workspace: Path) -> None:
    """The @2 record shape as a CASE TABLE, not one asserted example."""
    from verify_mission_custody import (
        validate_record, checkpoint_epoch, EPOCH_TOO_NEW)
    check("epoch-of-@1", checkpoint_epoch("checkpoint@1") == 1)
    check("epoch-of-@2", checkpoint_epoch("checkpoint@2") == 2)
    check("epoch-of-@9", checkpoint_epoch("checkpoint@9") == 9)
    check("epoch-of-non-checkpoint", checkpoint_epoch("receipt@1") is None)

    base = json.loads(json.dumps(_valid_checkpoint2_fixture()))
    check("valid-@2-clean", validate_record(base) == [])

    bad = json.loads(json.dumps(base)); bad["receipt_ids"] = ["plain-string"]
    check("@2-rejects-string-entry", validate_record(bad) != [])

    bad = json.loads(json.dumps(base)); bad["receipt_ids"] = [{"request_id": "a"}]
    check("@2-rejects-missing-sha", validate_record(bad) != [])

    bad = json.loads(json.dumps(base))
    bad["receipt_ids"] = [{"request_id": "a", "receipt_sha256": "nothex"}]
    check("@2-rejects-bad-sha", validate_record(bad) != [])

    bad = json.loads(json.dumps(base))
    bad["receipt_ids"] = [{"request_id": "a", "receipt_sha256": "0" * 64},
                          {"request_id": "a", "receipt_sha256": "1" * 64}]
    check("@2-rejects-duplicate-request-id", validate_record(bad) != [])

    bad = json.loads(json.dumps(base))
    bad["receipt_ids"] = [{"request_id": "a", "receipt_sha256": "0" * 64,
                           "extra": 1}]
    check("@2-rejects-entry-extra-key", validate_record(bad) != [])

    future = json.loads(json.dumps(base)); future["record"] = "checkpoint@3"
    errors = validate_record(future)
    check("@3-is-epoch-too-new-not-unknown-kind",
          any(EPOCH_TOO_NEW in e for e in errors))
    check("@3-does-not-read-as-unknown-kind",
          not any("unknown kind" in e for e in errors))


def test_receipt_entries_chokepoint(workspace: Path) -> None:
    """@1 and @2 chains normalise to the same shape, and no consumer may index
    receipt_ids directly -- a string-vs-dict comparison silently never matches,
    which is the false-clean direction."""
    m = open_mission(workspace, "m-entries", "Entries.")
    m.approve()
    m.record_effect("notes/a.md", "hello", "req-1")
    entries = m._receipt_entries(m.status())
    check("entries-normalises-@1", entries == [("req-1", None)])
    check("entries-sha-none-on-@1", entries[0][1] is None)


def test_no_raw_receipt_ids_indexing(workspace: Path) -> None:
    """Grep guard. Four latent defects in the predecessor came from exactly
    this: a consumer comparing a string against dict entries, or hashing a
    dict, or filtering by identity that never matches."""
    source = (ROOT / "custody_mission.py").read_text(encoding="utf-8")
    offenders = []
    for i, line in enumerate(source.splitlines(), 1):
        if '["receipt_ids"]' not in line:
            continue
        if "def _receipt_entries" in line or "ALLOW-RAW-RECEIPT-IDS" in line:
            continue
        offenders.append(f"{i}: {line.strip()}")
    check("no-raw-receipt-ids-indexing", not offenders)


TESTS = [
    test_open_creates_draft_r1,
    test_pathless_load_single_active,
    test_load_refuses_zero_and_multiple,
    test_effect_writes_receipt_and_artifact,
    test_effect_refuses_escape,
    test_resume_detects_drift_and_reconcile_clears,
    test_instruction_immutable,
    test_amend_records_authority_append_only,
    test_amendments_cannot_be_rewritten,
    test_manifest_envelope_immutable,
    test_resume_missing_receipt_is_drift,
    test_restored_receipt_survives_acknowledge,
    test_retirement_survives_hostile_request_ids,
    test_note_cannot_forge_machine_state,
    test_receipt_ids_always_carry_a_derivable_path,
    test_forged_restored_receipt_is_not_trusted,
    test_distinct_files_never_share_an_obligation,
    test_obligations_match_by_artifact_not_by_string,
    test_drift_marker_matches_by_artifact,
    test_superseded_receipt_never_shadows_the_current_one,
    test_continuity_surfaces_unreceipted_mutation,
    test_continuity_is_silent_on_sanctioned_recovery,
    test_request_ids_are_never_reusable,
    test_reconcile_clears_exactly_one_marker,
    test_corrupt_receipt_degrades_to_drift,
    test_effect_duplicate_id_leaves_workspace_untouched,
    test_accept_requires_verifying_and_separation,
    test_fail_is_clearable,
    test_operator_tier,
    test_open_with_guards_roundtrip,
    test_open_without_guards_omits_fields,
    test_amend_changes_guards,
    test_tail_guard_tamper_without_amendment_detected,
    test_amend_arms_guards_legitimately,
    test_amend_none_clears_guard_keys,
    test_open_refuses_second_active_mission,
    test_amend_empty_guards_list_refused,
    test_amend_then_tail_guard_strip_detected,
    test_unrelated_amend_then_tail_regex_narrow_detected,
    test_checkpoint2_validation_table,
    test_receipt_entries_chokepoint,
    test_no_raw_receipt_ids_indexing,
]


def main() -> int:
    for fn in TESTS:
        with tempfile.TemporaryDirectory() as td:
            fn(Path(td))
    print(f"\n{len(FAILURES)} failures")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    raise SystemExit(main())
