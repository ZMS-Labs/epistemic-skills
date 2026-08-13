#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
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
    _ReceiptTampered,
    now_utc,
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
    except CustodyError as exc:
        check("retired-id-reuse-refused", True)
        # T3-4b: an honest-loss retirement still says 'loss', not 'tamper'
        # -- the message differentiates in both directions, not just one.
        check("retired-id-reuse-names-loss-not-tamper",
              "retired by an acknowledged receipt loss" in str(exc))
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
    # _retired_receipt_ids returns {id: kind} since T3-4b (fix round 2) --
    # an honest loss (this scenario), so kind == "loss".
    check("tricky-id-retired-exactly",
          m._retired_receipt_ids(st) == {tricky: "loss"})
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
                     'receipt tamper acknowledged: "never-tampered" '
                     '(covered "x.md"); ',
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


def test_receipt_entries_normalises_at2_and_mixed(workspace: Path) -> None:
    """_receipt_entries's @2 branch: an object entry normalises to
    (request_id, receipt_sha256); a mixed @1/@2 list normalises per-entry,
    not uniformly; an entry missing receipt_sha256 normalises its sha to
    None rather than raising -- _receipt_entries reads raw-parsed records
    that have not necessarily been schema-validated yet."""
    m = open_mission(workspace, "m-entries2", "Entries2.")
    checkpoint = {"receipt_ids": [
        "bare-1",
        {"request_id": "obj-1", "receipt_sha256": "a" * 64},
        {"request_id": "obj-2"},
    ]}
    entries = m._receipt_entries(checkpoint)
    check("entries-@2-object-normalises",
          entries[1] == ("obj-1", "a" * 64))
    check("entries-mixed-@1-then-@2",
          entries[0] == ("bare-1", None))
    check("entries-@2-missing-sha-is-none",
          entries[2] == ("obj-2", None))


def _write_reattestation(m: Mission, request_id: str, sha: str) -> None:
    """Append one checkpoint@2 to m's chain attesting request_id -> sha,
    whatever the chain currently ends with. Nothing in the Mission API
    writes checkpoint@2 yet (a later task's job), so tests that need one
    build it directly via the store, the same way
    _valid_checkpoint2_fixture does."""
    latest, path = m.store.load_latest()
    record = json.loads(json.dumps(latest))
    record["record"] = "checkpoint@2"
    record["revision"] = latest["revision"] + 1
    record["prev_checkpoint_sha256"] = sha256_file(path)
    record["receipt_ids"] = [{"request_id": request_id, "receipt_sha256": sha}]
    record["written_utc"] = now_utc()
    m.store.write_checkpoint(record)


def test_expected_sha_latest_wins(workspace: Path) -> None:
    """The LATEST chain attestation wins, not the first -- not merely "an
    attestation beats no attestation". A single re-attestation with a
    DIFFERENT sha is required to discriminate the two: with only one
    attestation on the chain, first-non-None-wins and latest-wins agree, so
    a fixture that stops there cannot detect a regression to the former
    (proven by mutation below). A pre-migration id appears unattested in @1
    records, attested from a migration checkpoint onward, and then
    RE-attested (e.g. a receipt legitimately rewritten and re-chained) --
    _expected_sha must return the newest sha, not the first non-None one."""
    m = open_mission(workspace, "m-sha", "Sha.")
    m.approve()
    m.record_effect("notes/a.md", "hello", "req-1")
    check("unattested-before-migration", m._expected_sha("req-1") is None)

    _write_reattestation(m, "req-1", "a" * 64)
    check("attested-after-migration", m._expected_sha("req-1") == "a" * 64)
    check("map-agrees-with-single-id-lookup",
          m._expected_sha_map() == {"req-1": "a" * 64})

    _write_reattestation(m, "req-1", "b" * 64)
    check("latest-wins-not-first-attestation", m._expected_sha("req-1") == "b" * 64)
    check("map-latest-wins-not-first-attestation",
          m._expected_sha_map() == {"req-1": "b" * 64})


def test_load_receipt_expected_sha_check(workspace: Path) -> None:
    """_load_receipt's expected_sha parameter: loads when the receipt
    file's own bytes match the chain-attested hash, is unaffected when no
    attestation exists (expected_sha=None -- the pre-attestation fallback),
    and raises _ReceiptTampered -- NOT the UNLOADABLE None a corrupt or
    id-mismatched receipt gets -- on a mismatch. A tampered receipt is a
    DIFFERENT state from unloadable: folding it into None would let
    acknowledge_receipt_loss retire it as an honest loss (Task 2's original
    behaviour here, corrected by the CONTROLLER NOTE -- that return value was
    a judgment call pending exactly this reconciliation, not settled
    precedent)."""
    m = open_mission(workspace, "m-loadsha", "LoadSha.")
    m.approve()
    m.record_effect("notes/a.md", "hello", "req-1")
    actual_sha = sha256_file(m.store.receipt_path("req-1"))
    check("load-receipt-no-expected-sha-loads",
          m._load_receipt("req-1") is not None)
    check("load-receipt-matching-expected-sha-loads",
          m._load_receipt("req-1", actual_sha) is not None)
    try:
        m._load_receipt("req-1", "0" * 64)
        check("load-receipt-mismatched-expected-sha-raises-tampered", False)
    except _ReceiptTampered as exc:
        check("load-receipt-mismatched-expected-sha-raises-tampered",
              exc.request_id == "req-1")


def _setup_p6_tampered(workspace: Path) -> tuple[Mission, bytes]:
    """Shared P6 scaffold: opens a mission, chains 'p6-1's receipt sha
    WITHOUT depending on Task 7's migrate verb, then tampers the artifact AND
    the receipt's after_sha256 to match. Returns (mission, the receipt
    file's ORIGINAL bytes pre-tamper) so a caller can restore it
    byte-for-byte to exercise the byte-provable RESTORED path -- BYTES, not
    str: Path.write_text on Windows translates '\\n' to '\\r\\n', so a
    round-tripped str would silently stop being byte-identical to what
    sha256_file hashed, defeating the very restore this scaffold exists to
    let a caller perform (caught by mutation: the first draft of this helper
    used str and test_tampered_receipt_byte_restored_survives_acknowledge
    failed on real Windows I/O, not a code defect).

    Chaining the sha takes TWO manual writes, not one: first a checkpoint@2
    attesting it (via _write_reattestation), then ONE MORE checkpoint
    continuing the chain in checkpoint@1 (bare-string) shape before ever
    calling resume(). The second write is deliberate, not incidental:
    nothing in the Mission API emits checkpoint@2 yet -- _write_next
    hardcodes "record": "checkpoint@1" on every state change,
    unconditionally, regardless of what shape the latest checkpoint it is
    copying forward from was. Calling resume() (or acknowledge_receipt_loss)
    with checkpoint@2 still the LATEST checkpoint hits that head-on:
    _write_next would copy the @2, dict-shaped receipt_ids forward into a
    record it still labels checkpoint@1, which fails checkpoint@1's own
    schema (receipt_ids must be a list of strings) before any assertion here
    is ever reached -- a known, separately-tracked gap in the write path
    (the record-kind switch and the copy-forward have to land together, in a
    later task, or the chain bricks), not something Task 3 owns or should
    paper over. Continuing the constructed chain back to @1 shape -- exactly
    what _write_next can actually produce today -- keeps every test built on
    this scaffold exercising the real write path end-to-end instead of
    stopping short of it. The attestation survives the shape reversion
    regardless: _expected_sha_map reads every checkpoint in the chain, not
    just the latest, and latest-wins is about attestations, not about which
    checkpoint happens to be newest (see test_expected_sha_latest_wins)."""
    m = open_mission(workspace, "m-p6t", "P6.")
    m.approve()
    m.record_effect("notes/a.md", "original", "p6-1")
    receipt_path = m.store.receipt_path("p6-1")
    original_receipt = receipt_path.read_bytes()
    sha = sha256_file(receipt_path)
    _write_reattestation(m, "p6-1", sha)
    attested, attested_path = m.store.load_latest()
    continued = json.loads(json.dumps(attested))
    continued["record"] = "checkpoint@1"
    continued["revision"] = attested["revision"] + 1
    continued["prev_checkpoint_sha256"] = sha256_file(attested_path)
    continued["receipt_ids"] = ["p6-1"]
    continued["written_utc"] = now_utc()
    m.store.write_checkpoint(continued)
    (workspace / "notes" / "a.md").write_text("tampered", encoding="utf-8")
    record = json.loads(original_receipt.decode("utf-8"))
    record["after_sha256"] = sha256_bytes(b"tampered")
    receipt_path.write_bytes(
        (json.dumps(record, indent=1, sort_keys=True) + "\n").encode("utf-8"))
    return m, original_receipt


def test_probe_p6_receipt_tamper_is_caught(workspace: Path) -> None:
    """P6: edit an artifact AND its receipt's after_sha256 to match. Under @1
    resume reports clean -- the drift oracle trusts a receipt whose integrity
    nothing attests. Under @2 the chained sha catches it."""
    m, _original_receipt = _setup_p6_tampered(workspace)
    findings = m.resume()
    check("p6-caught-as-tampered",
          any(f == "RECEIPT-TAMPERED:p6-1" for f in findings))
    check("p6-not-misreported-as-missing",
          "RECEIPT-MISSING:p6-1" not in findings)
    st = m.status()
    check("p6-mission-reopened", st["status"] == "reopened")
    check("p6-marker-persisted-in-unresolved",
          "RECEIPT-TAMPERED:p6-1" in st["state"]["unresolved_verdicts"])


def test_tampered_receipt_byte_restored_survives_acknowledge(workspace: Path) -> None:
    """A RECEIPT-TAMPERED marker discharges cleanly when the receipt file is
    restored to EXACTLY the chain-attested bytes -- byte-provable, not
    path-heuristic (see acknowledge_receipt_loss). The id is KEPT, not
    retired: this is proven restoration, not an honest loss. The artifact
    itself is left tampered by this scaffold, so once the receipt is honest
    again, drift correctly moves from RECEIPT-TAMPERED to an ordinary
    RECONCILIATION mismatch on the artifact -- the distinction tracks the
    evidence, not the id."""
    m, original_receipt = _setup_p6_tampered(workspace)
    findings = m.resume()
    check("byte-restore-precondition-tampered",
          findings == ["RECEIPT-TAMPERED:p6-1"])

    m.store.receipt_path("p6-1").write_bytes(original_receipt)
    rev = m.acknowledge_receipt_loss("p6-1")
    st = m.status()
    check("byte-restore-ack-revision", st["revision"] == rev)
    check("byte-restore-marker-cleared",
          "RECEIPT-TAMPERED:p6-1" not in st["state"]["unresolved_verdicts"])
    check("byte-restore-status-active", st["status"] == "active")
    check("byte-restore-id-kept", "p6-1" in st["receipt_ids"])
    check("byte-restore-noted-as-restored",
          any(n.startswith("receipt restored: p6-1") for n in st["state"]["notes"]))
    check("byte-restore-artifact-drift-now-reconciliation",
          m.resume() == ["notes/a.md"])


def test_tampered_receipt_not_byte_restored_retires_id(workspace: Path) -> None:
    """The OLD path-match heuristic alone would have wrongly called this
    RESTORED: the tampered receipt's artifact_path field is untouched, so it
    still agrees with the chain-recorded path. With a chained sha, restore
    requires the STRONGER byte-provable check -- agreeing paths on a receipt
    proven to hold different bytes than the chain attested is not proof of
    anything, and acknowledge_receipt_loss must not be fooled by it."""
    m, _original_receipt = _setup_p6_tampered(workspace)
    findings = m.resume()
    check("not-restored-precondition-tampered",
          findings == ["RECEIPT-TAMPERED:p6-1"])

    # receipt file is left exactly as tampered -- artifact_path field intact,
    # only after_sha256 forged to match the tampered artifact.
    rev = m.acknowledge_receipt_loss("p6-1")
    st = m.status()
    check("not-restored-ack-revision", st["revision"] == rev)
    check("not-restored-marker-cleared",
          "RECEIPT-TAMPERED:p6-1" not in st["state"]["unresolved_verdicts"])
    check("not-restored-id-retired", "p6-1" not in st["receipt_ids"])
    check("not-restored-recover-obligation",
          st["state"]["unresolved_verdicts"] == ["RECOVER:notes/a.md"]
          and st["status"] == "reopened")
    check("not-restored-reason-recorded",
          any("bytes do not match the chain-attested hash" in n
              for n in st["state"]["notes"]))
    # T3-1: tamper-retirement carries its OWN note prefix, distinct from an
    # honest loss's -- otherwise the distinction survives only as free text
    # nothing downstream can act on.
    check("not-restored-uses-tamper-prefix",
          any(n.startswith('receipt tamper acknowledged: "p6-1"')
              for n in st["state"]["notes"]))
    check("not-restored-does-not-use-loss-prefix",
          not any(n.startswith('receipt loss acknowledged: "p6-1"')
                  for n in st["state"]["notes"]))

    try:
        m.record_effect("notes/unrelated.md", "other", "p6-1")
        check("not-restored-id-reuse-refused", False)
    except CustodyError:
        check("not-restored-id-reuse-refused", True)


def test_tampered_retired_id_reuse_message_names_retirement(workspace: Path) -> None:
    """_retired_receipt_ids must recognize a TAMPER-retired id, not merely
    an honest-loss-retired one (T3-1), AND the reuse-refusal message must
    say so specifically -- 'receipt tamper', not 'receipt loss' (T3-4b,
    fix round 2): the two are now a distinct, machine-actionable state, and
    a message that calls a tamper-retirement a 'loss' misdescribes exactly
    the thing this task made distinguishable.

    While the receipt file for p6-1 still exists, reuse is refused before
    _retired_receipt_ids is ever consulted (an earlier, unrelated 'receipt
    already exists' check fires first) -- so this test deletes the file
    first to reach the actual retired-id check. And while ANY
    previously-used id is refused via _all_receipt_ids_ever as a safety
    net regardless of retirement bookkeeping, that fallback produces a
    DIFFERENT, generic message -- only the SPECIFIC 'retired by an
    acknowledged receipt tamper' message proves _retired_receipt_ids
    itself recognized the tamper-retired id AND its kind, rather than
    silently missing it (or misreporting it as a loss) and relying on the
    fallback to still (accidentally) refuse the reuse."""
    m, _original = _setup_p6_tampered(workspace)
    m.resume()
    m.acknowledge_receipt_loss("p6-1")
    m.store.receipt_path("p6-1").unlink()
    try:
        m.record_effect("notes/unrelated.md", "other", "p6-1")
        check("tamper-retired-reuse-refused", False)
    except CustodyError as exc:
        check("tamper-retired-reuse-refused", True)
        check("tamper-retired-reuse-names-tamper-not-loss",
              "retired by an acknowledged receipt tamper" in str(exc))


def _setup_tampered_then_superseded(workspace: Path) -> Mission:
    """id-A's receipt sha is chained (the same two-write dance
    _setup_p6_tampered uses, for the same _write_next-hazard reason: the
    latest checkpoint must be checkpoint@1-shaped before any further
    state-mutating call), then id-A's RECEIPT is tampered -- the artifact is
    left alone, because what matters here is that id-A's OWN receipt fails
    its chain-attested hash, which resume() must catch regardless of the
    live artifact's content. id-B then supersedes id-A's path with a fresh,
    valid effect via the ordinary record_effect API, so 'notes/a.md' is
    genuinely, currently covered by id-B when the caller proceeds.

    Shared by two fix-round-1 tests (es#118 Task 3, round 1):
    - T3-2: RECEIPT-TAMPERED must still be reported for id-A even though
      id-B has superseded it (resume() must not route tampered ids through
      the one-artifact-one-current-receipt supersession logic).
    - T3-3: acknowledge_receipt_loss retiring id-A must NOT raise a
      RECOVER obligation for 'notes/a.md' -- id-B already, genuinely covers
      it, so the obligation would be spurious, discharged only by a
      redundant rewrite."""
    m = open_mission(workspace, "m-super", "Supersession.")
    m.approve()
    m.record_effect("notes/a.md", "v1", "id-A")
    receipt_path = m.store.receipt_path("id-A")
    sha = sha256_file(receipt_path)
    _write_reattestation(m, "id-A", sha)
    attested, attested_path = m.store.load_latest()
    continued = json.loads(json.dumps(attested))
    continued["record"] = "checkpoint@1"
    continued["revision"] = attested["revision"] + 1
    continued["prev_checkpoint_sha256"] = sha256_file(attested_path)
    continued["receipt_ids"] = ["id-A"]
    continued["written_utc"] = now_utc()
    m.store.write_checkpoint(continued)
    record = json.loads(receipt_path.read_bytes().decode("utf-8"))
    record["after_sha256"] = sha256_bytes(b"forged")
    receipt_path.write_bytes(
        (json.dumps(record, indent=1, sort_keys=True) + "\n").encode("utf-8"))
    m.record_effect("notes/a.md", "v2", "id-B")
    return m


def test_tamper_reported_despite_supersession(workspace: Path) -> None:
    """T3-2: a tampered id must be reported unconditionally, not routed
    through the one-artifact-one-current-receipt supersession logic. id-B
    has already superseded id-A for 'notes/a.md' by the time resume() runs
    -- silence on id-A here would be the false-clean direction: the tamper
    happened and is provable from the chain regardless of what superseded
    it afterward."""
    m = _setup_tampered_then_superseded(workspace)
    findings = m.resume()
    check("supersession-tamper-still-reported",
          "RECEIPT-TAMPERED:id-A" in findings)
    check("supersession-tamper-not-misreported-as-missing",
          "RECEIPT-MISSING:id-A" not in findings)
    # id-B's own coverage is genuinely clean -- it must not be dragged into
    # the finding just because it shares id-A's superseded path.
    check("supersession-superseding-id-not-flagged",
          not any(f.endswith(":id-B") for f in findings))
    st = m.status()
    check("supersession-tamper-marker-persisted",
          "RECEIPT-TAMPERED:id-A" in st["state"]["unresolved_verdicts"])


def test_acknowledge_tampered_superseded_id_no_spurious_recover(
        workspace: Path) -> None:
    """T3-3: retiring a tampered, ALREADY-SUPERSEDED id must not raise a
    RECOVER obligation for a path a surviving, loadable id (id-B) still
    genuinely covers -- that obligation would be spurious, discharged only
    by a redundant rewrite of an artifact that was never actually
    uncovered."""
    m = _setup_tampered_then_superseded(workspace)
    findings = m.resume()
    check("spurious-recover-precondition-tampered",
          "RECEIPT-TAMPERED:id-A" in findings)

    rev = m.acknowledge_receipt_loss("id-A")
    st = m.status()
    check("spurious-recover-ack-revision", st["revision"] == rev)
    check("spurious-recover-id-a-retired", "id-A" not in st["receipt_ids"])
    check("spurious-recover-id-b-kept", "id-B" in st["receipt_ids"])
    check("spurious-recover-no-recover-obligation",
          not any(marker.startswith("RECOVER:")
                  for marker in st["state"]["unresolved_verdicts"]))
    check("spurious-recover-marker-cleared",
          "RECEIPT-TAMPERED:id-A" not in st["state"]["unresolved_verdicts"])
    check("spurious-recover-mission-active", st["status"] == "active")
    # id-B's coverage is real, not merely assumed: a follow-up resume() must
    # stay clean.
    check("spurious-recover-resume-still-clean", m.resume() == [])


def test_covered_by_other_id_rejects_tampered_covering_receipt(
        workspace: Path) -> None:
    """T3-4a (fix round 2): _covered_by_other_id must source shas from
    _expected_sha_map -- the chain-wide latest attestation per id -- not
    each entry's OWN embedded sha. On the @1-tail chain shape (the only
    shape _write_next can produce today) every entry in receipt_ids carries
    sha=None regardless of whether an EARLIER checkpoint attested one, so
    using the embedded value skips the tamper check inside the coverage
    walk entirely and can credit a TAMPERED id as 'coverage'.

    Two ids, id-A and id-B, both attested and both later tampered, id-B
    superseding id-A for the same path. Retiring id-A must still raise
    RECOVER: id-B nominally 'wins' the path by append order, but id-B does
    NOT genuinely load either -- crediting it as coverage would suppress
    the obligation even though nothing currently, honestly covers the
    path. (This is a deferred obligation, not a full false-clean: id-B's
    own RECEIPT-TAMPERED marker stays open regardless, so the mission
    stays reopened either way -- the RECOVER marker specifically is the
    discriminating signal, not overall status.)"""
    m = open_mission(workspace, "m-t34a", "Both tampered.")
    m.approve()
    m.record_effect("notes/a.md", "v1", "id-A")
    m.record_effect("notes/a.md", "v2", "id-B")
    sha_a = sha256_file(m.store.receipt_path("id-A"))
    sha_b = sha256_file(m.store.receipt_path("id-B"))

    # One @2 checkpoint attesting BOTH ids, then one @1-shaped continuation
    # -- same _write_next-hazard dance _setup_p6_tampered uses, extended to
    # two entries instead of one.
    latest, path = m.store.load_latest()
    attested = json.loads(json.dumps(latest))
    attested["record"] = "checkpoint@2"
    attested["revision"] = latest["revision"] + 1
    attested["prev_checkpoint_sha256"] = sha256_file(path)
    attested["receipt_ids"] = [
        {"request_id": "id-A", "receipt_sha256": sha_a},
        {"request_id": "id-B", "receipt_sha256": sha_b},
    ]
    attested["written_utc"] = now_utc()
    m.store.write_checkpoint(attested)
    attested_latest, attested_path = m.store.load_latest()
    continued = json.loads(json.dumps(attested_latest))
    continued["record"] = "checkpoint@1"
    continued["revision"] = attested_latest["revision"] + 1
    continued["prev_checkpoint_sha256"] = sha256_file(attested_path)
    continued["receipt_ids"] = ["id-A", "id-B"]
    continued["written_utc"] = now_utc()
    m.store.write_checkpoint(continued)

    for rid, forged in (("id-A", b"forged-a"), ("id-B", b"forged-b")):
        rp = m.store.receipt_path(rid)
        record = json.loads(rp.read_bytes().decode("utf-8"))
        record["after_sha256"] = sha256_bytes(forged)
        rp.write_bytes(
            (json.dumps(record, indent=1, sort_keys=True) + "\n").encode("utf-8"))

    findings = m.resume()
    check("t34a-both-tampered-caught",
          sorted(findings) == ["RECEIPT-TAMPERED:id-A", "RECEIPT-TAMPERED:id-B"])

    m.acknowledge_receipt_loss("id-A")
    st = m.status()
    check("t34a-id-a-retired", "id-A" not in st["receipt_ids"])
    check("t34a-id-b-tampered-marker-still-open",
          "RECEIPT-TAMPERED:id-B" in st["state"]["unresolved_verdicts"])
    # The discriminating check: id-B does not genuinely cover the path
    # (it is itself tampered), so RECOVER must be raised, not suppressed.
    check("t34a-recover-raised-despite-non-covering-later-id",
          "RECOVER:notes/a.md" in st["state"]["unresolved_verdicts"])


def test_double_marker_window_kind_agrees_with_evidence(workspace: Path) -> None:
    """T3-4d (fix round 3): when BOTH RECEIPT-MISSING and RECEIPT-TAMPERED
    are open for the same id -- delete a receipt, resume (MISSING), place a
    forged one back, resume again (TAMPERED persists alongside the stale
    MISSING marker: resume only APPENDS markers for its current findings,
    it never retracts one no longer re-detected) -- acknowledge_receipt_loss
    selects MISSING by priority (checked first in the if/elif chain). The
    retirement prefix must still read 'tamper', taken from still_tampered
    (the live evidence re-checked at discharge time), NOT from which marker
    won that priority selection -- otherwise the note's own prefix
    contradicts the 'why' evidence clause written beside it in the SAME
    note (round 1's reasoning -- 'the prefix records which marker was
    discharged' -- does not survive this scenario: here the marker that
    won priority is MISSING, but the live evidence is unambiguously
    tamper).

    Bounded even before this fix: the leftover TAMPERED marker stays open,
    the mission stays reopened, and begin_verification refuses -- so
    acceptance was never reachable in the mislabeled state. Fixed anyway
    because under-reporting a tamper as a loss is the wrong direction to
    leave an escalation-policy consumer in."""
    m = open_mission(workspace, "m-t34d", "Double marker window.")
    m.approve()
    m.record_effect("notes/a.md", "v1", "x-1")
    sha = sha256_file(m.store.receipt_path("x-1"))
    _write_reattestation(m, "x-1", sha)
    attested, attested_path = m.store.load_latest()
    continued = json.loads(json.dumps(attested))
    continued["record"] = "checkpoint@1"
    continued["revision"] = attested["revision"] + 1
    continued["prev_checkpoint_sha256"] = sha256_file(attested_path)
    continued["receipt_ids"] = ["x-1"]
    continued["written_utc"] = now_utc()
    m.store.write_checkpoint(continued)

    receipt_path = m.store.receipt_path("x-1")
    receipt_path.unlink()
    findings1 = m.resume()
    check("t34d-first-resume-missing", findings1 == ["RECEIPT-MISSING:x-1"])

    forged = {
        "record": "receipt@1",
        "mission_id": m.status()["mission_id"],
        "request_id": "x-1",
        "actor": "agent:attacker",
        "utc": now_utc(),
        "artifact_path": "notes/a.md",
        "before_sha256": None,
        "after_sha256": sha256_bytes(b"forged"),
    }
    receipt_path.write_bytes(
        (json.dumps(forged, indent=1, sort_keys=True) + "\n").encode("utf-8"))
    findings2 = m.resume()
    check("t34d-second-resume-tampered", findings2 == ["RECEIPT-TAMPERED:x-1"])
    st_before = m.status()
    check("t34d-double-marker-window",
          "RECEIPT-MISSING:x-1" in st_before["state"]["unresolved_verdicts"]
          and "RECEIPT-TAMPERED:x-1" in st_before["state"]["unresolved_verdicts"])

    m.acknowledge_receipt_loss("x-1")
    st = m.status()
    check("t34d-missing-marker-cleared-by-priority",
          "RECEIPT-MISSING:x-1" not in st["state"]["unresolved_verdicts"])
    check("t34d-tampered-marker-left-open",
          "RECEIPT-TAMPERED:x-1" in st["state"]["unresolved_verdicts"])
    check("t34d-recover-obligation-raised",
          "RECOVER:notes/a.md" in st["state"]["unresolved_verdicts"])
    check("t34d-mission-still-reopened", st["status"] == "reopened")
    # The load-bearing check: the recorded kind agrees with the LIVE
    # evidence (still tampered), not with which marker won priority.
    check("t34d-kind-reads-tamper-at-first-discharge",
          m._retired_receipt_ids(st).get("x-1") == "tamper")
    check("t34d-note-uses-tamper-prefix",
          any(n.startswith('receipt tamper acknowledged: "x-1"')
              for n in st["state"]["notes"]))
    check("t34d-note-does-not-use-loss-prefix",
          not any(n.startswith('receipt loss acknowledged: "x-1"')
                  for n in st["state"]["notes"]))
    # acceptance is unreachable while the leftover marker is open --
    # bounded even before the fix, and still true after it.
    try:
        m.begin_verification()
        check("t34d-verification-refused-while-open", False)
    except CustodyError:
        check("t34d-verification-refused-while-open", True)


def test_tamper_marker_survives_deleting_the_receipt(workspace: Path) -> None:
    """Case A of the discharge case table: a RECEIPT-TAMPERED marker is
    open and the forged receipt file is DELETED before discharge. The
    retirement must still be recorded as a tamper.

    This is the cheapest possible downgrade attack -- one extra step on an
    ordinary tamper: get caught, then delete the receipt. Deleting it makes
    the live re-check (still_tampered) False, because there is no longer a
    file whose bytes can fail the chain-attested hash. Keying the prefix on
    that live signal ALONE therefore rewrote a tamper the chain had already
    recorded into an honest 'loss' -- and nothing downstream brakes it: the
    id retires, RECOVER is raised, a fresh effect re-covers the artifact
    honestly, and the mission returns to active carrying a durable record
    that says 'loss'. The prose 'why' clause still reads loss-shaped
    (correctly -- the file really is gone); it is the machine-readable
    kind, the exact artifact this feature exists to produce, that must not
    lie. Tamper-taint is monotone: only a byte-provable restoration clears
    it, and that path returns before the prefix is ever selected."""
    m, _original_receipt = _setup_p6_tampered(workspace)
    findings = m.resume()
    check("t34e-a-precondition-tampered", findings == ["RECEIPT-TAMPERED:p6-1"])

    receipt_path = m.store.receipt_path("p6-1")
    receipt_path.unlink()
    check("t34e-a-receipt-really-gone", not receipt_path.exists())
    st_before = m.status()
    check("t34e-a-only-tampered-marker-open",
          st_before["state"]["unresolved_verdicts"] == ["RECEIPT-TAMPERED:p6-1"])

    m.acknowledge_receipt_loss("p6-1")
    st = m.status()
    # The load-bearing check: the chain recorded a tamper, so the kind stays
    # 'tamper' even though the file is now absent and the live re-check is
    # silent.
    check("t34e-a-kind-stays-tamper",
          m._retired_receipt_ids(st).get("p6-1") == "tamper")
    check("t34e-a-note-uses-tamper-prefix",
          any(n.startswith('receipt tamper acknowledged: "p6-1"')
              for n in st["state"]["notes"]))
    check("t34e-a-note-does-not-use-loss-prefix",
          not any(n.startswith('receipt loss acknowledged: "p6-1"')
                  for n in st["state"]["notes"]))
    # The scenario really does run to completion -- there is no downstream
    # brake that would have caught the mislabel anyway. Asserted, not
    # assumed: the marker clears, the id retires, and the only thing left
    # open is the honest re-cover obligation.
    check("t34e-a-marker-cleared",
          "RECEIPT-TAMPERED:p6-1" not in st["state"]["unresolved_verdicts"])
    check("t34e-a-id-retired", "p6-1" not in st["receipt_ids"])
    check("t34e-a-recover-obligation-raised",
          st["state"]["unresolved_verdicts"] == ["RECOVER:notes/a.md"])


def test_double_marker_deleted_receipt_still_names_tamper(workspace: Path) -> None:
    """Case E of the discharge case table: BOTH RECEIPT-MISSING and
    RECEIPT-TAMPERED are open for one id, and the receipt is DELETED again
    before discharge. The retirement must still be recorded as a tamper.

    This is the row that decides MEMBERSHIP over EQUALITY. MISSING wins the
    priority selection, so `marker` is the MISSING one; and the file is
    gone, so the live re-check is silent. Both `still_tampered` alone and
    `still_tampered or marker == tampered_marker` therefore report 'loss'
    for an id the chain holds an undischarged RECEIPT-TAMPERED for. Only
    reading that marker's MEMBERSHIP in the open set -- what the chain
    recorded, rather than which marker the discharge order happened to
    pick -- gets it right.

    Distinct from test_double_marker_window_kind_agrees_with_evidence,
    which leaves the forged receipt in place: there the live evidence
    still fires, so that test cannot discriminate equality from
    membership. The delete is the whole point."""
    m = open_mission(workspace, "m-t34e-e", "Double marker, then deleted.")
    m.approve()
    m.record_effect("notes/a.md", "v1", "x-1")
    receipt_path = m.store.receipt_path("x-1")
    original_receipt = receipt_path.read_bytes()
    _write_reattestation(m, "x-1", sha256_file(receipt_path))
    attested, attested_path = m.store.load_latest()
    continued = json.loads(json.dumps(attested))
    continued["record"] = "checkpoint@1"
    continued["revision"] = attested["revision"] + 1
    continued["prev_checkpoint_sha256"] = sha256_file(attested_path)
    continued["receipt_ids"] = ["x-1"]
    continued["written_utc"] = now_utc()
    m.store.write_checkpoint(continued)

    receipt_path.unlink()
    check("t34e-e-first-resume-missing", m.resume() == ["RECEIPT-MISSING:x-1"])
    forged = json.loads(original_receipt.decode("utf-8"))
    forged["after_sha256"] = sha256_bytes(b"forged")
    receipt_path.write_bytes(
        (json.dumps(forged, indent=1, sort_keys=True) + "\n").encode("utf-8"))
    check("t34e-e-second-resume-tampered", m.resume() == ["RECEIPT-TAMPERED:x-1"])
    st_before = m.status()
    check("t34e-e-double-marker-window",
          "RECEIPT-MISSING:x-1" in st_before["state"]["unresolved_verdicts"]
          and "RECEIPT-TAMPERED:x-1" in st_before["state"]["unresolved_verdicts"])

    # ...and now the receipt goes away again, silencing the live re-check
    # while the chain's tamper record stays open.
    receipt_path.unlink()
    check("t34e-e-receipt-really-gone", not receipt_path.exists())

    m.acknowledge_receipt_loss("x-1")
    st = m.status()
    check("t34e-e-missing-marker-cleared-by-priority",
          "RECEIPT-MISSING:x-1" not in st["state"]["unresolved_verdicts"])
    check("t34e-e-tampered-marker-left-open",
          "RECEIPT-TAMPERED:x-1" in st["state"]["unresolved_verdicts"])
    check("t34e-e-kind-stays-tamper",
          m._retired_receipt_ids(st).get("x-1") == "tamper")
    check("t34e-e-note-uses-tamper-prefix",
          any(n.startswith('receipt tamper acknowledged: "x-1"')
              for n in st["state"]["notes"]))
    check("t34e-e-note-does-not-use-loss-prefix",
          not any(n.startswith('receipt loss acknowledged: "x-1"')
                  for n in st["state"]["notes"]))


def test_live_tamper_under_a_missing_marker_alone_names_tamper(
        workspace: Path) -> None:
    """The row that keeps the still_tampered limb honest: ONLY
    RECEIPT-MISSING is open, and a forged receipt is placed back at the id's
    path with NO intervening resume to raise RECEIPT-TAMPERED. The chain
    therefore holds no tamper marker at all, and the marker being discharged
    is the MISSING one -- so every marker-derived limb is silent. Only the
    LIVE re-check sees it, and the retirement must still read 'tamper'.

    Written because a mutation found the hole: dropping still_tampered and
    keying the prefix on marker membership alone left the ENTIRE suite green
    (0 of 250 checks failing). Membership covers the tamper the chain
    recorded; still_tampered covers the tamper the chain has not caught up
    with yet. Neither limb subsumes the other, and until this test existed
    only one of them was defended -- the same unenumerated-case mechanism
    that produced rounds 1, 3 and this one."""
    m = open_mission(workspace, "m-t34e-i", "Live tamper, missing marker only.")
    m.approve()
    m.record_effect("notes/a.md", "v1", "x-1")
    receipt_path = m.store.receipt_path("x-1")
    original_receipt = receipt_path.read_bytes()
    _write_reattestation(m, "x-1", sha256_file(receipt_path))
    attested, attested_path = m.store.load_latest()
    continued = json.loads(json.dumps(attested))
    continued["record"] = "checkpoint@1"
    continued["revision"] = attested["revision"] + 1
    continued["prev_checkpoint_sha256"] = sha256_file(attested_path)
    continued["receipt_ids"] = ["x-1"]
    continued["written_utc"] = now_utc()
    m.store.write_checkpoint(continued)

    receipt_path.unlink()
    check("t34e-i-resume-missing", m.resume() == ["RECEIPT-MISSING:x-1"])
    forged = json.loads(original_receipt.decode("utf-8"))
    forged["after_sha256"] = sha256_bytes(b"forged")
    receipt_path.write_bytes(
        (json.dumps(forged, indent=1, sort_keys=True) + "\n").encode("utf-8"))
    # Deliberately NO second resume: the chain never learns about the forgery,
    # so no RECEIPT-TAMPERED marker is ever written.
    st_before = m.status()
    check("t34e-i-no-tamper-marker-recorded",
          st_before["state"]["unresolved_verdicts"] == ["RECEIPT-MISSING:x-1"])

    m.acknowledge_receipt_loss("x-1")
    st = m.status()
    check("t34e-i-kind-reads-tamper",
          m._retired_receipt_ids(st).get("x-1") == "tamper")
    check("t34e-i-note-uses-tamper-prefix",
          any(n.startswith('receipt tamper acknowledged: "x-1"')
              for n in st["state"]["notes"]))
    check("t34e-i-note-does-not-use-loss-prefix",
          not any(n.startswith('receipt loss acknowledged: "x-1"')
                  for n in st["state"]["notes"]))
    check("t34e-i-why-clause-names-the-hash-mismatch",
          any("bytes do not match the chain-attested hash" in n
              for n in st["state"]["notes"]))


def _attested_effect(m: Mission, request_id: str, artifact: str) -> bytes:
    """record_effect + chain its receipt sha + continue the chain back to @1
    shape. Returns the receipt's ORIGINAL bytes. The two-write dance is
    _setup_p6_tampered's, for the reason documented there: _write_next cannot
    emit checkpoint@2 yet, so a mission left tail-@2 bricks on the next state
    change."""
    m.record_effect(artifact, "v1", request_id)
    receipt_path = m.store.receipt_path(request_id)
    original = receipt_path.read_bytes()
    _write_reattestation(m, request_id, sha256_file(receipt_path))
    attested, attested_path = m.store.load_latest()
    continued = json.loads(json.dumps(attested))
    continued["record"] = "checkpoint@1"
    continued["revision"] = attested["revision"] + 1
    continued["prev_checkpoint_sha256"] = sha256_file(attested_path)
    continued["receipt_ids"] = [request_id]
    continued["written_utc"] = now_utc()
    m.store.write_checkpoint(continued)
    return original


def test_corrupt_restore_under_a_missing_marker_alone_names_tamper(
        workspace: Path) -> None:
    """R4-1, row M/corrupt-attested: the SECOND row where `still_tampered` is
    the only limb that fires. `t34e-i-` pins the first (M/forged-attested);
    this one is not a duplicate of it, because the bytes here do NOT parse.

    Reachable without any adversary: receipt deleted, `resume` raises
    RECEIPT-MISSING, then a truncated or partially-written restore leaves
    unparseable bytes at the id's path, and the loss is acknowledged with no
    intervening `resume`. No tamper marker is ever recorded, so membership is
    silent; the id is attested, so the raw-bytes hash still fails and the
    live re-check calls it what it is.

    The shipped answer is already correct -- this is coverage, not a defect.
    It earns a test because a plausible tightening (count `still_tampered`
    only when the bytes also parse, on the theory that unparseable means
    unloadable) flips this row from tamper to loss and, before this test,
    killed NOTHING across the whole suite. A single reachable edit silently
    changing a row is the condition this round was convened to fix; here it
    is one row over.

    Why it is not `t34e-i-` twice: the tightening kills this test and leaves
    `t34e-i-` green, because a forged receipt is still valid JSON. The two
    rows are separated by exactly the predicate a future edit is most likely
    to add."""
    m = open_mission(workspace, "m-t34e-mcorrupt", "Corrupt restore, M only.")
    m.approve()
    _attested_effect(m, "x-1", "notes/a.md")

    receipt_path = m.store.receipt_path("x-1")
    receipt_path.unlink()
    check("t34e-mc-resume-missing", m.resume() == ["RECEIPT-MISSING:x-1"])

    # A truncated restore: bytes are present at the id's path but do not parse.
    receipt_path.write_bytes(b"{not json")
    # Deliberately NO second resume: no RECEIPT-TAMPERED marker is recorded,
    # so membership cannot see this and only the live re-check can.
    check("t34e-mc-no-tamper-marker-recorded",
          m.status()["state"]["unresolved_verdicts"] == ["RECEIPT-MISSING:x-1"])

    m.acknowledge_receipt_loss("x-1")
    st = m.status()
    check("t34e-mc-kind-reads-tamper",
          m._retired_receipt_ids(st).get("x-1") == "tamper")
    check("t34e-mc-note-uses-tamper-prefix",
          any(n.startswith('receipt tamper acknowledged: "x-1"')
              for n in st["state"]["notes"]))
    check("t34e-mc-note-does-not-use-loss-prefix",
          not any(n.startswith('receipt loss acknowledged: "x-1"')
                  for n in st["state"]["notes"]))
    check("t34e-mc-why-clause-names-the-hash-mismatch",
          any("bytes do not match the chain-attested hash" in n
              for n in st["state"]["notes"]))
    check("t34e-mc-id-retired", "x-1" not in st["receipt_ids"])


def test_corrupt_attested_receipt_is_tamper_not_loss(workspace: Path) -> None:
    """Row T/corrupt: the receipt file for an ATTESTED id is replaced with
    bytes that do not parse at all. Unparseable is not unloadable here --
    the chain attests specific bytes for this id and these are not them,
    whether or not they happen to be valid JSON.

    Looks redundant against the forged-receipt rows and is not. It pins an
    ORDERING everything above silently rests on: _load_receipt hashes the
    RAW bytes BEFORE it parses them, so corrupt-but-attested bytes raise
    _ReceiptTampered instead of returning the unloadable None. Move the hash
    check below the json.loads -- an entirely plausible tidy-up, since every
    other check in that function runs on the parsed record -- and this
    receipt becomes an honest 'loss' under any live-evidence rule.

    The first assertion is the actual pin: resume must classify a corrupt
    attested receipt as RECEIPT-TAMPERED, not RECEIPT-MISSING. Under
    hash-after-parse it reports MISSING and this test dies there, before the
    prefix is ever reached."""
    m = open_mission(workspace, "m-t34e-corrupt", "Corrupt attested receipt.")
    m.approve()
    _attested_effect(m, "x-1", "notes/a.md")

    receipt_path = m.store.receipt_path("x-1")
    receipt_path.write_bytes(b"{not json at all\x00\xff")
    check("t34e-c-corrupt-is-tampered-not-missing",
          m.resume() == ["RECEIPT-TAMPERED:x-1"])

    m.acknowledge_receipt_loss("x-1")
    st = m.status()
    check("t34e-c-kind-reads-tamper",
          m._retired_receipt_ids(st).get("x-1") == "tamper")
    check("t34e-c-note-uses-tamper-prefix",
          any(n.startswith('receipt tamper acknowledged: "x-1"')
              for n in st["state"]["notes"]))
    check("t34e-c-note-does-not-use-loss-prefix",
          not any(n.startswith('receipt loss acknowledged: "x-1"')
                  for n in st["state"]["notes"]))


def test_corrupt_receipt_under_an_open_tamper_marker_stays_tamper(
        workspace: Path) -> None:
    """Row T/corrupt, second construction: the RECEIPT-TAMPERED marker is
    already open from an earlier forgery, and THEN the file is corrupted.

    The pair matters because the two constructions diverge under exactly the
    refactor the sibling test guards. Measured, with the hash check moved
    below the parse:

      marker sourced from the corrupt file   -- resume reports MISSING, so
        no tamper marker is ever recorded and BOTH rules retire it 'loss'.
        Membership has nothing to read; the damage is upstream in resume's
        classification, where no prefix rule can reach it.
      marker already open (this test)        -- membership holds the kind at
        'tamper'; the live-evidence-only rule flips it to 'loss'.

    So membership removes the ordering dependency only when the marker came
    from somewhere else. That is a narrower guarantee than 'R3 is robust to
    the ordering', and the two tests together are what keep the difference
    honest instead of leaving one of them standing for both."""
    m = open_mission(workspace, "m-t34e-corrupt2", "Open marker, then corrupt.")
    m.approve()
    original_receipt = _attested_effect(m, "x-1", "notes/a.md")

    receipt_path = m.store.receipt_path("x-1")
    forged = json.loads(original_receipt.decode("utf-8"))
    forged["after_sha256"] = sha256_bytes(b"forged")
    receipt_path.write_bytes(
        (json.dumps(forged, indent=1, sort_keys=True) + "\n").encode("utf-8"))
    check("t34e-c2-resume-tampered", m.resume() == ["RECEIPT-TAMPERED:x-1"])

    receipt_path.write_bytes(b"{not json at all\x00\xff")
    check("t34e-c2-marker-open-before-discharge",
          m.status()["state"]["unresolved_verdicts"] == ["RECEIPT-TAMPERED:x-1"])

    m.acknowledge_receipt_loss("x-1")
    st = m.status()
    check("t34e-c2-kind-reads-tamper",
          m._retired_receipt_ids(st).get("x-1") == "tamper")
    check("t34e-c2-note-uses-tamper-prefix",
          any(n.startswith('receipt tamper acknowledged: "x-1"')
              for n in st["state"]["notes"]))
    check("t34e-c2-note-does-not-use-loss-prefix",
          not any(n.startswith('receipt loss acknowledged: "x-1"')
                  for n in st["state"]["notes"]))


def test_double_marker_restore_clears_only_the_missing_marker(
        workspace: Path) -> None:
    """Row BOTH/original: both markers open and the ORIGINAL receipt bytes
    are back. This row never reaches the prefix at all -- it takes the
    byte-provable `restored` early return -- and nothing else in the suite
    covers a restored row.

    Pinned because discharge is PER-MARKER, not per-evidence: the call
    clears only RECEIPT-MISSING (which won priority) and leaves
    RECEIPT-TAMPERED open, so the mission stays reopened and a SECOND call
    is required. That is self-healing rather than broken -- the second call
    takes the same restored path and clears the rest -- but it is exactly
    the shape a later round would 'simplify' into a single-marker clear
    without noticing the marker it dropped. It also demonstrates the one
    thing that legitimately clears tamper-taint along the file axis: the id
    survives, no retirement note is written, and coverage continues."""
    m = open_mission(workspace, "m-t34e-both-orig", "Both markers, restored.")
    m.approve()
    original_receipt = _attested_effect(m, "x-1", "notes/a.md")

    receipt_path = m.store.receipt_path("x-1")
    receipt_path.unlink()
    check("t34e-r-first-resume-missing", m.resume() == ["RECEIPT-MISSING:x-1"])
    forged = json.loads(original_receipt.decode("utf-8"))
    forged["after_sha256"] = sha256_bytes(b"forged")
    receipt_path.write_bytes(
        (json.dumps(forged, indent=1, sort_keys=True) + "\n").encode("utf-8"))
    check("t34e-r-second-resume-tampered", m.resume() == ["RECEIPT-TAMPERED:x-1"])

    # The genuine article is back, byte for byte.
    receipt_path.write_bytes(original_receipt)
    m.acknowledge_receipt_loss("x-1")
    st = m.status()
    check("t34e-r-missing-cleared",
          "RECEIPT-MISSING:x-1" not in st["state"]["unresolved_verdicts"])
    check("t34e-r-tampered-still-open",
          "RECEIPT-TAMPERED:x-1" in st["state"]["unresolved_verdicts"])
    check("t34e-r-no-retirement-note",
          m._retired_receipt_ids(st).get("x-1") is None)
    check("t34e-r-id-kept", "x-1" in st["receipt_ids"])
    check("t34e-r-restored-note-written",
          any(n.startswith("receipt restored: x-1") for n in st["state"]["notes"]))
    check("t34e-r-no-spurious-recover",
          not any(v.startswith("RECOVER:")
                  for v in st["state"]["unresolved_verdicts"]))
    check("t34e-r-still-reopened", st["status"] == "reopened")

    # Second call, same restored path, clears the leftover marker.
    m.acknowledge_receipt_loss("x-1")
    st2 = m.status()
    check("t34e-r-second-call-clears-tampered",
          st2["state"]["unresolved_verdicts"] == [])
    check("t34e-r-second-call-still-no-retirement",
          m._retired_receipt_ids(st2).get("x-1") is None)
    check("t34e-r-second-call-active", st2["status"] == "active")


_RAW_RECEIPT_IDS_TOKEN_RE = re.compile(r"""["']receipt_ids["']""")
_RECEIPT_IDS_DICT_KEY_RE = re.compile(r"""["']receipt_ids["']\s*:""")


def test_no_raw_receipt_ids_indexing(workspace: Path) -> None:
    """Grep guard over every file that reads receipt_ids. Four latent defects
    in the predecessor came from exactly this: a consumer comparing a string
    against dict entries, or hashing a dict, or filtering by identity that
    never matches.

    Matches the quoted token by REGEX, not the exact ["receipt_ids"] literal,
    and scans custody_cli.py too. An earlier version of this guard (exact
    literal, custody_mission.py only) missed single-quoted ['receipt_ids'],
    .get("receipt_ids", ...), a read split across lines, AND every raw site
    in custody_cli.py -- including the exact unhashable-dict TypeError the
    brief warns about, reintroduced at the clean-resume summary, which a
    file-scoped guard cannot see regardless of how the line itself is
    written. A dict-LITERAL key declaration ("receipt_ids": value) is a
    write, not a read, and needs no exemption; anything else quoting the
    token is a read and must carry ALLOW-RAW-RECEIPT-IDS.

    The dict-key exemption is applied per-OCCURRENCE, not per-line: strip
    every matched key-declaration substring out of the line first, then
    search what remains. A whole-line exemption would let a legitimate
    declaration on one part of a line hide an unrelated raw read elsewhere on
    the SAME line -- e.g. a mutated copy-forward like
    `"receipt_ids": list(latest["receipt_ids"]),` starts with a real
    dict-key declaration, but also silently discards the computed
    receipt_ids local (breaking add_receipt_id and the retirement filter);
    a whole-line check reads that first declaration and stops looking."""
    offenders = []
    for fname in ("custody_mission.py", "custody_cli.py"):
        source = (ROOT / fname).read_text(encoding="utf-8")
        for i, line in enumerate(source.splitlines(), 1):
            if not _RAW_RECEIPT_IDS_TOKEN_RE.search(line):
                continue
            remainder = _RECEIPT_IDS_DICT_KEY_RE.sub("", line)
            if not _RAW_RECEIPT_IDS_TOKEN_RE.search(remainder):
                continue  # every occurrence was a dict-literal key declaration
            if "def _receipt_entries" in line or "ALLOW-RAW-RECEIPT-IDS" in line:
                continue
            offenders.append(f"{fname}:{i}: {line.strip()}")
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
    test_receipt_entries_normalises_at2_and_mixed,
    test_expected_sha_latest_wins,
    test_load_receipt_expected_sha_check,
    test_probe_p6_receipt_tamper_is_caught,
    test_tampered_receipt_byte_restored_survives_acknowledge,
    test_tampered_receipt_not_byte_restored_retires_id,
    test_tampered_retired_id_reuse_message_names_retirement,
    test_tamper_reported_despite_supersession,
    test_acknowledge_tampered_superseded_id_no_spurious_recover,
    test_covered_by_other_id_rejects_tampered_covering_receipt,
    test_double_marker_window_kind_agrees_with_evidence,
    test_tamper_marker_survives_deleting_the_receipt,
    test_double_marker_deleted_receipt_still_names_tamper,
    test_live_tamper_under_a_missing_marker_alone_names_tamper,
    test_corrupt_restore_under_a_missing_marker_alone_names_tamper,
    test_corrupt_attested_receipt_is_tamper_not_loss,
    test_corrupt_receipt_under_an_open_tamper_marker_stays_tamper,
    test_double_marker_restore_clears_only_the_missing_marker,
]


def main() -> int:
    for fn in TESTS:
        with tempfile.TemporaryDirectory() as td:
            fn(Path(td))
    print(f"\n{len(FAILURES)} failures")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    raise SystemExit(main())
