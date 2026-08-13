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


def record_effect_as_historical(m: Mission, artifact_relpath: str,
                                 content: str, request_id: str) -> dict:
    """Mint an effect the way record_effect did BEFORE the es#153 ingestion
    guard, to construct pre-guard history: records carrying control-char
    paths exist in the wild, and the comparison/discharge machinery for
    them must survive forever even though the front door now refuses to
    mint new ones. Mirrors record_effect's body minus the guard -- if
    record_effect's shape changes, change this with it."""
    latest, path = m.store.load_latest()
    m._verify_manifest(latest)
    receipt = m._write_effect(latest, artifact_relpath, content, request_id)
    m._write_next(latest, path, status=latest["status"],
                  add_receipt_id=request_id,
                  unresolved_verdicts=latest["state"]["unresolved_verdicts"],
                  note=f"effect: {artifact_relpath}")
    return receipt


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


def test_scope_consistency_and_acceptance_boundary(workspace: Path) -> None:
    """`scope` earns exactly one machine job: the acceptance comparison.

    Not a runtime gate. Prevention was never available for the failure this
    addresses -- most of the measured contamination was note text no path
    predicate ranges over, plus work in a different repo where the gate is
    structurally inert, during a stretch when the work was operator-AUTHORIZED
    but `amend` did not yet exist (a block with no discharge = the rejected
    RECOVER-UNKNOWN wedge).

    Refusing the CLAIM is different: every artifact already exists, so it
    cannot wedge, and the constrained actor cannot disarm it, because scope
    lives in the manifest tamper-compare and is not a guard key."""
    m = open_mission(workspace, "m-scope", "Bounded work.",
                     scope_in=["docs/**"], scope_out=["secrets/**"])
    m.approve()
    m.record_effect("docs/a.md", "in scope", "sc-1")
    m.record_effect("src/b.py", "outside scope.in", "sc-2")
    m.record_effect("secrets/c.env", "matches scope.out", "sc-3")

    findings = m.scope_consistency()
    by_path = {f["artifact_path"]: f["reason"] for f in findings}
    check("scope-flags-outside-in", by_path.get("src/b.py") == "outside scope.in")
    check("scope-flags-matching-out",
          by_path.get("secrets/c.env") == "matches scope.out")
    check("scope-does-not-flag-in-scope", "docs/a.md" not in by_path)

    m.begin_verification()
    acceptor = Mission.load(workspace, actor="agent:acceptor")
    try:
        acceptor.record_verdict("PASS", acceptor_id="agent:acceptor",
                                 assurance_tier="declared-role-separation",
                                 reason="done")
        check("scope-pass-refused-without-amendment", False)
    except AcceptanceRefused as exc:
        # must refuse for THIS reason, not incidentally for another rule
        check("scope-pass-refused-without-amendment",
              "crossed the declared scope" in str(exc))

    # The amendment is recorded because it is the operator's word, but the
    # DISCHARGE is the acceptor's explicit acknowledgement -- prose cannot
    # establish a grant (see test_scope_ack_is_the_only_discharge).
    Mission.load(workspace, actor="agent:worker").amend_authority(
        "operator: the src/ and secrets/ work was authorized")
    acceptor = Mission.load(workspace, actor="agent:acceptor")
    revision = acceptor.record_verdict(
        "PASS", acceptor_id="agent:acceptor",
        assurance_tier="declared-role-separation", reason="done",
        scope_ack=["src/b.py", "secrets/c.env"])
    check("scope-pass-accepted-after-ack", isinstance(revision, int))


def test_scope_entry_classification_table(workspace: Path) -> None:
    """`scope` is free text and always has been. Which entries can take part
    in a path comparison is therefore a CASE TABLE, not one asserted example.

    The error directions are asymmetric: mistaking a glob for prose loses one
    comparison (status quo, benign); mistaking prose for a glob makes a
    scope.in that matches nothing, flags every receipt, and wedges an honest
    mission's close. Everything ambiguous is prose."""
    from custody_mission import _is_path_pattern
    cases = [
        # genuine path patterns
        ("docs/**", True), ("secrets/**", True), ("*.md", True),
        ("a?b", True), ("plugins/epistemic-skills/**", True),
        # prose that real manifests actually carry -- the bundled examples use
        # the first two, and the third was written during this very change
        ("monitored-missing reconciliation", False),
        ("indexer changes", False),
        ("media acquisition, arr/Plex/NAS operations", False),
        ("VPN configuration", False),
        # BARE FILENAMES. The first version required a slash or a wildcard, so
        # `scope.out=["secrets.env"]` -- the most natural exclusion an operator
        # can write -- was silently discarded and PASS succeeded after writing
        # the one file the mission was told not to touch. The asymmetry that
        # justified "ambiguous -> prose" was reasoned about scope.IN; for
        # scope.OUT, dropping an entry is the FALSE-CLEAN direction.
        ("secrets.env", True), ("README.md", True), ("config.yaml", True),
        (".env", True), (".gitignore", True),
        # a single bare word with no extension stays prose: `notes` could be a
        # directory or a noun and nothing in the string decides which. This
        # residue is REPORTED (uncompared_scope_entries), never silent.
        ("reconciliation", False), ("notes", False),
        # PATHS CONTAINING SPACES. Testing whitespace BEFORE the slash test
        # made every one of these prose, so the comparison silently ran with
        # them dropped: writing exactly the excluded path produced a clean
        # scope_consistency() and an accepted PASS.
        ("My Documents/secrets.env", True), ("docs/release notes/**", True),
        ("a/b c/d.txt", True), ("docs/release notes/", True),
        # ...while genuine prose that happens to carry a slash still reads as
        # prose, because it ends in a bare word rather than a path ending
        ("TCP/IP tuning", False), ("arr/Plex/NAS operations", False),
        ("docs and/or specs", False),
        # ambiguous -> prose, deliberately
        ("docs and/or specs", False), ("TCP/IP tuning", False),
        ("", False),
    ]
    for entry, want in cases:
        check(f"scope-classify-{entry[:26] or 'empty'}",
              _is_path_pattern(entry) == want)


def test_uncompared_scope_entries_are_reported(workspace: Path) -> None:
    """Every entry the comparison declines has a surface.

    A comparison that silently ignores half a declaration is this estate's
    keystone failure in miniature: the boundary reads as enforced and checks
    nothing. Naming the blind spot is what keeps "scope is compared" from
    being read as "all of scope is compared"."""
    from custody_mission import uncompared_scope_entries
    m = open_mission(workspace, "m-uncompared", "Mixed scope.",
                     scope_in=["docs/**", "indexer changes"],
                     scope_out=["secrets.env", "VPN configuration"])
    latest, _ = m.store.load_latest()
    uncompared = uncompared_scope_entries(latest["manifest"])
    check("uncompared-reports-prose-in", uncompared["in"] == ["indexer changes"])
    check("uncompared-reports-prose-out",
          uncompared["out"] == ["VPN configuration"])
    check("uncompared-omits-real-patterns",
          "docs/**" not in uncompared["in"] and "secrets.env" not in uncompared["out"])


def test_bare_filename_exclusion_is_enforced(workspace: Path) -> None:
    """The defect this predicate change exists for, end to end.

    Before: scope.out=["secrets.env"] classified as prose, excludes empty,
    scope_consistency() clean, PASS accepted -- the mission asserts a boundary
    it demonstrably crossed."""
    m = open_mission(workspace, "m-bare", "Bare-filename exclusion.",
                     scope_out=["secrets.env"])
    m.approve()
    m.record_effect("secrets.env", "KEY=value", "bf-1")
    findings = m.scope_consistency()
    check("bare-filename-exclusion-flagged",
          [f["artifact_path"] for f in findings] == ["secrets.env"])
    m.begin_verification()
    acceptor = Mission.load(workspace, actor="agent:acceptor")
    try:
        acceptor.record_verdict("PASS", acceptor_id="agent:acceptor",
                                 assurance_tier="declared-role-separation",
                                 reason="done")
        check("bare-filename-pass-refused", False)
    except AcceptanceRefused as exc:
        check("bare-filename-pass-refused", "crossed the declared scope" in str(exc))


def test_prose_scope_does_not_refuse_acceptance(workspace: Path) -> None:
    """A populated PROSE scope must not break a legitimate close.

    Treating every scope entry as a glob classified ordinary receipts as
    outside scope.in and refused PASS on every mission with a prose
    declaration -- a silent compatibility break dressed as a security check."""
    m = open_mission(workspace, "m-prose", "Prose-bounded work.",
                     scope_in=["monitored-missing reconciliation"],
                     scope_out=["indexer changes"])
    m.approve()
    m.record_effect("notes/a.md", "ordinary work", "pr-1")
    check("prose-scope-flags-nothing", m.scope_consistency() == [])
    m.begin_verification()
    acceptor = Mission.load(workspace, actor="agent:acceptor")
    check("prose-scope-pass-accepted",
          isinstance(acceptor.record_verdict(
              "PASS", acceptor_id="agent:acceptor",
              assurance_tier="declared-role-separation", reason="done"), int))


def test_unrelated_amendment_never_discharges_regardless_of_order(
        workspace: Path) -> None:
    """An unrelated grant discharges nothing, before OR after the drift.

    The predecessor tested ORDER: an earlier unrelated amendment must not
    discharge later drift. That test could not see the rule it claimed to
    prove -- its amendment named nothing, so it passed identically with the
    ordering rule removed. Naming is what does the work; this asserts that
    directly, in both orders."""
    m = open_mission(workspace, "m-order", "Ordered work.", scope_in=["docs/**"])
    m.approve()
    m.amend_authority("operator: unrelated cost allowance")   # amendment FIRST
    m.record_effect("src/late.py", "drift AFTER it", "ord-1")  # drift SECOND
    m.amend_authority("operator: you may restart the pod")     # and one AFTER
    m.begin_verification()
    acceptor = Mission.load(workspace, actor="agent:acceptor")
    try:
        acceptor.record_verdict("PASS", acceptor_id="agent:acceptor",
                                 assurance_tier="declared-role-separation",
                                 reason="done")
        check("unrelated-amendments-never-discharge", False)
    except AcceptanceRefused as exc:
        check("unrelated-amendments-never-discharge",
              "crossed the declared scope" in str(exc))


def test_mixed_prose_and_path_scope_in_does_not_flag_everything(
        workspace: Path) -> None:
    """A partially-prose scope.in must not report every receipt outside it.

    "outside scope.in" is an ABSENCE inference: it concludes from a receipt
    matching no include that it is out of bounds. With one path entry and one
    prose entry, the prose was dropped, `includes` stayed non-empty, and every
    artifact the prose covered was flagged against a boundary that in fact
    permits it -- wedging an honest close.

    "matches scope.out" is a PRESENCE inference, so a partly-prose exclusion
    list still contributes everything it can. Only the absence side is gated."""
    m = open_mission(workspace, "m-mixed", "Mixed declaration.",
                     scope_in=["src/**", "monitored-missing reconciliation"],
                     scope_out=["secrets.env", "VPN configuration"])
    m.approve()
    m.record_effect("docs/notes.md", "covered by the prose entry", "mx-1")
    m.record_effect("README.md", "also covered by prose", "mx-2")
    check("mixed-scope-in-flags-nothing-outside", m.scope_consistency() == [])
    # the exclusion half still works: presence needs only one comparable entry
    m.record_effect("secrets.env", "TOKEN=x", "mx-3")
    check("mixed-scope-out-still-flags",
          [f["artifact_path"] for f in m.scope_consistency()] == ["secrets.env"])


def test_scope_ack_is_the_only_discharge(workspace: Path) -> None:
    """An amendment that plainly grants the path still does not discharge it.

    This test used to assert the opposite. Three rounds of trying to read
    authorisation out of prose ended at a measurement: the denial-marker list
    caught 1 of 14 denial shapes, and two of the misses -- a denial header with
    paths listed beneath, and a grant plus a prohibition in one clause --
    cannot be fixed by adding vocabulary. A substring test establishes MENTION;
    it cannot establish a GRANT.

    So discharge moved to a party who can judge: the acceptor, who is already
    required to be distinct from the steward. The record now asserts "an
    acceptor judged these covered" -- true and attributable -- instead of "an
    amendment covers these", which the parser cannot establish."""
    m = open_mission(workspace, "m-ack", "Ack required.", scope_in=["docs/**"])
    m.approve()
    m.amend_authority("operator: you may write src/early.py")
    m.record_effect("src/early.py", "authorised in advance", "pre-1")
    m.begin_verification()
    acceptor = Mission.load(workspace, actor="agent:acceptor")
    try:
        acceptor.record_verdict("PASS", acceptor_id="agent:acceptor",
                                 assurance_tier="declared-role-separation",
                                 reason="done")
        check("plain-grant-alone-does-not-discharge", False)
    except AcceptanceRefused as exc:
        check("plain-grant-alone-does-not-discharge",
              "crossed the declared scope" in str(exc))
        # the parse survives as a HINT that points the acceptor at the text
        check("refusal-names-the-mentioning-amendment",
              "MENTION" in str(exc) and "a mention is not a grant" in str(exc))

    # the acceptor's explicit acknowledgement is what discharges
    revision = acceptor.record_verdict(
        "PASS", acceptor_id="agent:acceptor",
        assurance_tier="declared-role-separation", reason="done",
        scope_ack=["src/early.py"])
    check("scope-ack-discharges", isinstance(revision, int))

    # and it is a chain fact naming who judged what, not a side effect
    # read the chain directly: the mission is COMPLETED, so Mission.load --
    # which looks for an ACTIVE mission -- correctly finds nothing
    final, _ = acceptor.store.load_latest()
    notes = " ".join(final["state"]["notes"])
    check("scope-ack-recorded-in-the-chain",
          "scope-ack by agent:acceptor" in notes and "src/early.py" in notes)


def test_every_violating_representation_must_be_acknowledged(
        workspace: Path) -> None:
    """When BOTH representations violate, acking one must not cover the other.

    Recording only the FIRST violating path meant discharging it was enough:
    with secrets/alias -> keys/ and scope.out=["secrets/**","keys/**"], an
    acknowledgement naming secrets/alias/leak.pem let a private key land in
    keys/leak.pem -- forbidden by a separate exclusion, covered by nothing."""
    m = open_mission(workspace, "m-both", "Two exclusions.",
                     scope_out=["secrets/**", "keys/**"])
    m.approve()
    (workspace / "keys").mkdir(parents=True, exist_ok=True)
    (workspace / "secrets").mkdir(exist_ok=True)
    try:
        (workspace / "secrets" / "alias").symlink_to(workspace / "keys",
                                                      target_is_directory=True)
    except (OSError, NotImplementedError):
        print("skip both-representations (symlinks unavailable on this host)")
        return
    m.record_effect("secrets/alias/leak.pem", "KEY", "bo-1")
    paths = m.scope_consistency()[0]["violating_paths"]
    check("both-representations-recorded",
          "secrets/alias/leak.pem" in paths and "keys/leak.pem" in paths)
    m.begin_verification()
    acceptor = Mission.load(workspace, actor="agent:acceptor")
    try:
        acceptor.record_verdict("PASS", acceptor_id="agent:acceptor",
                                 assurance_tier="declared-role-separation",
                                 reason="done",
                                 scope_ack=["secrets/alias/leak.pem"])
        check("acking-the-lexical-path-does-not-cover-the-landing", False)
    except AcceptanceRefused as exc:
        check("acking-the-lexical-path-does-not-cover-the-landing",
              "keys/leak.pem" in str(exc))


def test_scope_ack_is_normalised_like_the_findings(workspace: Path) -> None:
    """The acceptor must not have to guess an internal spelling.

    `violating_paths` hold `_norm_path` output and the comparison was exact
    string equality, so the only string that worked appeared nowhere except the
    refusal message -- not the path the operator wrote, not the path in the
    receipt. "./secrets.env" and a trailing space both refused, and because
    `_norm_path` folds case only on NT, an ack captured in a runbook was
    platform-specific."""
    spellings = ["secrets.env", "./secrets.env", "secrets.env ", ".\secrets.env"]
    for i, spelling in enumerate(spellings):
        # a fresh workspace per spelling: reusing one store would collide on
        # revision ordering and mask the thing under test
        m = open_mission(workspace / f"ws{i}", "m-norm", "Norm.",
                         scope_out=["secrets.env"])
        m.approve()
        m.record_effect("secrets.env", "TOKEN=x", "nm-1")
        m.begin_verification()
        acceptor = Mission.load(m.workspace, actor="agent:acceptor")
        # An escaping AcceptanceRefused would abort main() mid-registry, so
        # every later test would silently not run and a mutation harness could
        # not tell CAUGHT from CRASHED-EARLY.
        try:
            landed = acceptor.record_verdict(
                "PASS", acceptor_id="agent:acceptor",
                assurance_tier="declared-role-separation", reason="done",
                scope_ack=[spelling])
        except AcceptanceRefused:
            landed = None
        check(f"ack-accepts-{spelling.strip() or 'blank'}",
              isinstance(landed, int))


def test_scope_ack_note_cannot_be_forged_by_narrative(workspace: Path) -> None:
    """The ack note is machine state, so an ordinary note must not imitate it.

    The acknowledgement's whole value is that an auditor can see WHO took
    responsibility. While any caller could write the same bytes through the
    `note` verb, a genuine ack and a forged one were byte-identical -- so the
    only durable evidence was a string the constrained party could write at
    will."""
    m = open_mission(workspace, "m-forge-ack", "Forge.", scope_out=["x.env"])
    m.approve()
    genuine = "scope-ack by agent:acceptor: x.env"
    # Four shapes got past a startswith() check on the whole string. The
    # multi-line one is load-bearing: the note CONTAINS a byte-identical ack
    # line while starting with something innocuous.
    for label, text in (
            ("exact", genuine),
            ("leading-space", " " + genuine),
            ("capitalised", genuine.capitalize()),
            ("second-line", "session note" + chr(10) + genuine),
            ("leading-newline", chr(10) + genuine)):
        try:
            m.note(text)
            check(f"narrative-cannot-forge-a-scope-ack-{label}", False)
        except CustodyError as exc:
            check(f"narrative-cannot-forge-a-scope-ack-{label}",
                  "may not contain a line beginning with" in str(exc))
    # ...and an amendment must not be able to smuggle one either
    try:
        m.amend_authority("operator: fine" + chr(10) + genuine)
        check("amend-cannot-forge-a-scope-ack", False)
    except CustodyError:
        check("amend-cannot-forge-a-scope-ack", True)
    # a note that merely MENTIONS the phrase mid-line is legitimate narrative
    check("mid-line-mention-is-allowed",
          isinstance(m.note("I read the scope-ack by the acceptor"), int))


def test_reserved_note_refusal_names_a_working_discharge(workspace: Path) -> None:
    """A refusal with no stated discharge is a dead end -- the #25 class,
    second member.

    SKILL.md instructs the steward to record an operator grant VERBATIM, and
    a grant may legitimately begin with a reserved machine-note prefix
    ('effect: allow ...'). The guard must stay -- narrative must not be able
    to imitate machine state -- so the refusal message is the only exit, and
    it must name a discharge that actually works. The obvious one does NOT:
    the guard strips leading whitespace before comparing, so indentation
    discharges nothing. The one that works is a '> ' quote marker, and both
    facts are pinned here so the message can never drift into suggesting the
    dead one and a later 'tidy-up' that strips the quote marker before the
    comparison has to argue with a red suite, not a comment."""
    m = open_mission(workspace, "m-disch", "Discharge.", scope_in=["docs/**"])
    m.approve()
    grant = "effect: allow writes outside docs/ for this mission"
    msg = None
    try:
        m.amend_authority(grant)
    except CustodyError as exc:
        msg = str(exc)
    check("reserved-refusal-fires", msg is not None)
    check("reserved-refusal-names-the-discharge",
          msg is not None and "'> '" in msg)
    check("reserved-refusal-shows-the-offending-line",
          msg is not None and repr(grant) in msg)

    # the named discharge WORKS: the quoted grant is recorded, word for word
    # behind the marker, on the single-line and the multi-line shape alike.
    # Caught, not bare: under the mutation this exists to catch (a 'tidy-up'
    # that strips the quote marker before the comparison), the call refuses,
    # and an escaping CustodyError would abort main() mid-registry -- every
    # later check would read ABSENT, which cannot be told from passing.
    try:
        rev = m.amend_authority("> " + grant)
    except CustodyError:
        rev = None
    check("quoted-grant-is-recorded", isinstance(rev, int))
    latest, _ = m.store.load_latest()
    amendments = latest["manifest"]["authority"]["amendments"]
    recorded = amendments[-1]["text"] if amendments else None
    check("quoted-grant-text-is-exact", recorded == "> " + grant)
    try:
        rev2 = m.amend_authority("operator said:\n> effect: also this one")
    except CustodyError:
        rev2 = None
    check("quoted-line-inside-multiline-is-recorded", isinstance(rev2, int))

    # indentation is NOT a discharge: leading whitespace is stripped before
    # the comparison, deliberately (the forge test's leading-space row is the
    # same strip seen from the attacker's side)
    try:
        m.amend_authority("    " + grant)
        check("indentation-is-not-a-discharge", False)
    except CustodyError:
        check("indentation-is-not-a-discharge", True)

    # an invisible character inside the prefix is still refused, and the
    # refusal's repr of the line is what makes the invisible visible -- the
    # caller who typed what LOOKS benign can see why it refused
    try:
        m.note("eff" + chr(0x200B) + "ect: x")
        check("invisible-prefix-still-refused", False)
    except CustodyError as exc:
        check("invisible-prefix-still-refused", True)
        check("invisible-char-is-visible-in-the-refusal",
              "\\u200b" in str(exc))


def test_identity_is_one_visible_line(workspace: Path) -> None:
    """A newline in the acting identity forges a machine-note line.

    `acceptor_id` was schema'd as any nonempty string, and the scope-ack note
    interpolates it: an actor named
    'agent:acceptor\\nscope-ack by operator: forged.env' produced a chained
    note whose SECOND LINE reads as an acknowledgement by the operator --
    reproduced live before this fix. `_refuse_reserved_note` exists precisely
    so an auditor can trust those lines; the identity field walked around it.

    The guard is at INGESTION (Mission construction / open refs), and it
    refuses the CHARACTER CLASS, not reserved content: routing identities
    through the reserved-note check instead would still admit a harmless-
    looking newline (which breaks the one-line note structure) and an ANSI
    escape (which rewrites the terminal on every resume), while falsely
    refusing an identity that merely CONTAINS reserved-looking text -- safe,
    because interpolation is mid-line. Those three rows separate the rules."""
    from custody_store import MissionStore
    evil = "agent:acceptor\nscope-ack by operator: forged.env"

    def refused(actor):
        try:
            Mission(MissionStore(workspace / "missions" / "m-x"), workspace,
                    actor=actor)
            return None
        except CustodyError as exc:
            return str(exc)

    check("identity-forge-newline-refused", refused(evil) is not None)
    check("identity-harmless-newline-refused",
          refused("agent\nsecond line") is not None)
    check("identity-with-ansi-escape-refused",
          refused("agent" + chr(0x1B) + "[2J") is not None)
    msg = refused("agent" + chr(0x200B) + "acceptor")
    check("identity-with-invisible-char-refused", msg is not None)
    check("identity-refusal-makes-the-invisible-visible",
          msg is not None and "\\u200b" in msg)
    check("reserved-looking-identity-is-legal",
          refused("effect: agent") is None)
    check("clean-unicode-identity-is-legal", refused("agent:josé") is None)

    # The predicate is splitlines+isprintable on the RAW value, not a category
    # list -- these rows are exactly the ones the Cc+Cf enumeration missed. A
    # full-range census puts the splitlines boundary set at
    # {0A,0B,0C,0D,1C,1D,1E,85,2028,2029}; 8 of 10 are Cc, and U+2028/U+2029
    # are the two Z ones the enumeration walked past.
    check("identity-line-separator-refused",
          refused("agent\u2028second") is not None)
    check("identity-paragraph-separator-refused",
          refused("agent\u2029second") is not None)
    check("identity-nbsp-refused", refused("agent\xa0acceptor") is not None)
    check("identity-lone-surrogate-refused",
          refused("agent\ud800x") is not None)
    # Edge whitespace is its own refusal, and the forcing row is pure ASCII:
    # 'agent:worker-1 ' vs 'agent:worker-1' is display-identical and
    # byte-distinct, which defeats the acceptor != worker separation check.
    check("identity-trailing-space-refused",
          refused("agent:worker-1 ") is not None)
    check("identity-leading-space-refused",
          refused(" agent:worker-1") is not None)
    # Interior ASCII spaces stay legal (spaced human names), as do composed
    # AND decomposed accents -- the battery the predicate was measured on.
    check("identity-interior-space-is-legal",
          refused("operator:John Smith") is None)
    check("identity-decomposed-accent-is-legal",
          refused("agent:Jose\u0301") is None)
    # The claim is scoped: NOT display-uniqueness. CGJ is invisible AND
    # printable -- the same category granularity that admits the combining
    # acute above -- so it passes, disclosed in the docstring and deferred to
    # es#150's structured record. Deleting this row would let the docstring
    # claim drift back to 'display-unique' unchallenged.
    check("identity-invisible-but-printable-residual-is-disclosed-not-caught",
          refused("agent:x\u034fy") is None)

    for field, kwargs in (
            ("steward", {"steward_ref": "a\nb", "operator_ref": "op"}),
            ("operator", {"steward_ref": "st", "operator_ref": "a\nb"})):
        try:
            Mission.open(workspace / field, "m-id", "T.", actor="agent:x",
                         **kwargs)
            check(f"open-refuses-unprintable-{field}-ref", False)
        except CustodyError:
            check(f"open-refuses-unprintable-{field}-ref", True)

    # The ACTOR validates before the load-probe and before any write. The
    # constructor's guard sat on the wrong side of the first write: on an
    # empty workspace the load-probe raises NoActiveMission before any
    # Mission is constructed, so revision 1 landed on disk carrying the
    # rejected written_by and only then did open() refuse -- an active
    # draft nobody legitimate could have opened, wedging every subsequent
    # open in the workspace (reproduced live pre-fix).
    ws_actor = workspace / "actor-first"
    try:
        Mission.open(ws_actor, "m-evil-actor", "T.",
                     operator_ref="op", steward_ref="st", actor=evil)
        check("open-refuses-unprintable-actor", False)
    except CustodyError:
        check("open-refuses-unprintable-actor", True)
    check("refused-open-leaves-no-residue",
          not (ws_actor / "missions").exists())
    relegit = Mission.open(ws_actor, "m-legit", "T.",
                           operator_ref="op", steward_ref="st",
                           actor="agent:x")
    check("workspace-not-wedged-after-refused-open",
          relegit.status()["revision"] == 1)

    # end to end: the reproduced forge can no longer reach the chain. The
    # acceptor's Mission cannot even be CONSTRUCTED under the forging
    # identity, so no verdict path exists for it; the chain keeps zero note
    # lines attributing an acknowledgement to the operator.
    m = open_mission(workspace, "m-forge-id", "Forge.",
                     scope_out=["secrets/**"])
    m.approve()
    m.record_effect("secrets/x.env", "TOKEN", "fid-1")
    m.begin_verification()
    try:
        Mission(MissionStore(m.store.mission_dir), workspace, actor=evil)
        check("forging-acceptor-cannot-be-constructed", False)
    except CustodyError:
        check("forging-acceptor-cannot-be-constructed", True)
    latest, _ = m.store.load_latest()
    forged = [ln for n in latest["state"].get("notes", [])
              for ln in n.splitlines()
              if ln.strip().startswith("scope-ack by operator:")]
    check("forged-ack-line-cannot-enter-the-chain", forged == [])


def test_disabled_scope_in_comparison_is_disclosed_as_such(
        workspace: Path) -> None:
    """One prose entry disables the include comparison ENTIRELY, and the
    disclosure must say that rather than listing the one entry.

    Listing only the prose entry let a reader conclude the OTHER entries were
    compared. They were not -- nothing was -- while `status --brief` showed a
    populated scope.in that reads as bounded."""
    from custody_mission import uncompared_scope_entries
    m = open_mission(workspace, "m-disabled", "Mixed.",
                     scope_in=["docs/**", "the reconciliation work"])
    latest, _ = m.store.load_latest()
    report = uncompared_scope_entries(latest["manifest"])
    check("mixed-scope-in-reports-comparison-disabled",
          report.get("in_comparison_disabled") is True)

    m2 = open_mission(workspace / "pure", "m-pure", "Pure patterns.",
                      scope_in=["docs/**"])
    latest2, _ = m2.store.load_latest()
    check("pure-pattern-scope-in-is-not-disabled",
          uncompared_scope_entries(latest2["manifest"])
          .get("in_comparison_disabled") is False)


def test_unmatchable_patterns_are_disclosed_not_silently_inert(
        workspace: Path) -> None:
    """A pattern that can never match must be REPORTED, not silently dropped.

    `_is_path_pattern` asks whether an entry looks like a path. It does not ask
    whether the compiler can use it, and `_glob_regex` implements only
    `* ** ?` -- everything else becomes an escaped literal. Verified against the
    live compiler: `!secrets/**`, `/etc/passwd`, `~/.ssh/id_rsa` and
    `C:/Windows` all classify as patterns and match NOTHING.

    That is worse than being called prose, and the difference is disclosure: a
    prose entry appears in `uncompared_scope_entries`, so the operator learns
    their boundary is unchecked. An unmatchable pattern appeared nowhere -- the
    declaration read as enforced, compared nothing, and said nothing.

    Demoting them weakens no comparison; they matched nothing already. It only
    makes the nothing visible."""
    from custody_mission import uncompared_scope_entries
    m = open_mission(workspace, "m-inert", "Inert excludes.",
                     scope_out=["!secrets/**", "/etc/passwd", "docs/**"])
    latest, _ = m.store.load_latest()
    report = uncompared_scope_entries(latest["manifest"])
    check("unmatchable-negation-disclosed", "!secrets/**" in report["out"])
    check("unmatchable-absolute-disclosed", "/etc/passwd" in report["out"])
    check("real-glob-still-compared", "docs/**" not in report["out"])

    # The comparison and the disclosure ask ONE question, so they cannot drift.
    # The unmatchable excludes fire on nothing (they always did); the real glob
    # still fires. Writing to the excluded path must still be caught.
    m.approve()
    m.record_effect("notes/ok.md", "not excluded by anything", "in-1")
    check("unmatchable-excludes-flag-nothing", m.scope_consistency() == [])
    m.record_effect("docs/inside.md", "matches the real exclude", "in-2")
    check("real-exclude-still-fires",
          [f["artifact_path"] for f in m.scope_consistency()] == ["docs/inside.md"])

    # A `..` SEGMENT is the shape this predicate's first case table did not
    # enumerate, and it is the worst one it missed: `_normalize_relpath`
    # collapses `./` and `//` but NOT `..`, while every receipted path IS
    # normalized before comparison. So `docs/../secrets/**` can only match the
    # literal spelling `docs/../secrets/...`, which no normalized path ever
    # produces -- an operator writes a traversal, gets a COMPARED boundary, and
    # it binds nothing while appearing in no disclosure.
    # `workspace / "ws2"`, NEVER `workspace.parent` -- the harness hands each
    # test a `TemporaryDirectory`, whose parent is the SYSTEM temp root. A
    # sibling there escapes the per-test sandbox, persists across runs (the
    # second run fails "an active mission already exists"), and writes durable
    # state outside the permitted scratchpad. Verified by doing it: the first
    # draft of this test left a mission under the system temp root.
    m2 = open_mission(workspace / "ws2", "m-dotdot",
                      "Traversal excludes.",
                      scope_out=["docs/../secrets/**", "../outside/**",
                                 "a..b/**", "secrets/**"])
    latest2, _ = m2.store.load_latest()
    rep2 = uncompared_scope_entries(latest2["manifest"])
    check("dotdot-traversal-disclosed", "docs/../secrets/**" in rep2["out"])
    check("dotdot-leading-disclosed", "../outside/**" in rep2["out"])
    # SEGMENT, not substring: dots INSIDE a segment are a legal filename and
    # must still compare. This is the ONLY row separating the correct fix from
    # the plausible one -- a substring test demotes it.
    check("dots-inside-a-segment-still-compared", "a..b/**" not in rep2["out"])
    check("plain-glob-still-compared-2", "secrets/**" not in rep2["out"])


def test_every_caller_text_surface_refuses_a_forged_note_line(
        workspace: Path) -> None:
    """All five surfaces that embed caller text, not just the two with tests.

    A mutation removing the guard from `note` or `amend` was caught; removing it
    from VERDICT REASONS and CANCEL REASONS survived a green suite. The
    verdict-reason guard is load-bearing by positive control: with it removed, a
    PASS reason of "work done{NL}scope-ack by ..." puts a forged
    acknowledgement line straight into the chain and nothing fails.

    `set_frontier` is included because a frontier is not a note but IS displayed
    by status/resume and lives in the same checkpoint JSON, so an auditor
    grepping for the prefix hits it identically."""
    forged = "scope-ack by agent:acceptor: secrets.env"
    payload = "legitimate text" + chr(10) + forged

    m = open_mission(workspace, "m-surfaces", "Surfaces.", scope_out=["s.env"])
    m.approve()
    for label, call in (("note", lambda: m.note(payload)),
                        ("amend", lambda: m.amend_authority(payload)),
                        ("frontier", lambda: m.set_frontier(payload))):
        try:
            call()
            check(f"{label}-refuses-forged-line", False)
        except CustodyError:
            check(f"{label}-refuses-forged-line", True)

    # cancel reason
    c = open_mission(workspace / "cancel", "m-cancel", "Cancel.")
    c.approve()
    try:
        c.cancel(payload)
        check("cancel-reason-refuses-forged-line", False)
    except CustodyError:
        check("cancel-reason-refuses-forged-line", True)

    # verdict reason -- the load-bearing one
    v = open_mission(workspace / "verdict", "m-verdict", "Verdict.")
    v.approve()
    v.begin_verification()
    acceptor = Mission.load(v.workspace, actor="agent:acceptor")
    try:
        acceptor.record_verdict("PASS", acceptor_id="agent:acceptor",
                                 assurance_tier="declared-role-separation",
                                 reason=payload)
        check("verdict-reason-refuses-forged-line", False)
    except CustodyError:
        check("verdict-reason-refuses-forged-line", True)
    # and refusal happens BEFORE any state change
    after, _ = v.store.load_latest()
    check("verdict-refusal-writes-nothing", after["status"] == "verifying")


def test_invisible_characters_cannot_disguise_a_forged_note_line(
        workspace: Path) -> None:
    """strip()/splitlines() see whitespace and separators, not INVISIBLES.

    ZWSP, BOM, LRM, WORD JOINER and SOFT HYPHEN are none of those, so each
    walked past the guard while the stored note rendered identically to a
    genuine acknowledgement on screen. NFKC + dropping Unicode category Cf
    closes the class, for the comparison only -- the text is stored verbatim.

    Homoglyphs are deliberately out of scope: confusables are unbounded and
    enumerating them would repeat the denial-marker mistake. The structural fix
    is a validated field on the acceptance-verdict record (es#150)."""
    from custody_mission import _refuse_reserved_note
    genuine = "scope-ack by agent:acceptor: secrets.env"
    for label, prefix in (("zwsp", "​"), ("bom", "﻿"),
                          ("lrm", "‎"), ("word-joiner", "⁠"),
                          ("soft-hyphen", "­")):
        try:
            _refuse_reserved_note(prefix + genuine)
            check(f"invisible-{label}-refused", False)
        except CustodyError:
            check(f"invisible-{label}-refused", True)
    try:
        _refuse_reserved_note("note" + chr(10) + "​" + genuine)
        check("invisible-on-second-line-refused", False)
    except CustodyError:
        check("invisible-on-second-line-refused", True)
    # and ordinary narrative is still not blocked
    check("plain-narrative-still-allowed",
          _refuse_reserved_note("an ordinary session note") is None)
    check("mid-line-mention-still-allowed",
          _refuse_reserved_note("I read the scope-ack by hand") is None)


def test_scope_ack_note_records_only_outstanding_paths(workspace: Path) -> None:
    """An ack naming something that was never a finding must not enter the note.

    It is inert for the gate -- acking a non-finding discharges nothing -- but
    it pollutes the one record that says what the acceptor judged, which is
    that record's entire purpose. An auditor reading
    "scope-ack by X: everything-was-fine, keys.pem, secrets.env" cannot tell
    which of those the acceptor actually took responsibility for."""
    m = open_mission(workspace, "m-ack-note", "Note hygiene.",
                     scope_out=["secrets.env"])
    m.approve()
    m.record_effect("secrets.env", "TOKEN=x", "an-1")
    m.begin_verification()
    acceptor = Mission.load(workspace, actor="agent:acceptor")
    acceptor.record_verdict(
        "PASS", acceptor_id="agent:acceptor",
        assurance_tier="declared-role-separation", reason="done",
        scope_ack=["secrets.env", "never-a-finding.txt", "docs/imaginary.md"])
    final, _ = acceptor.store.load_latest()
    ack = [n for n in final["state"]["notes"] if n.startswith("scope-ack by ")]
    check("ack-note-present", len(ack) == 1)
    check("ack-note-records-the-real-crossing", "secrets.env" in ack[0])
    check("ack-note-omits-non-findings",
          "never-a-finding.txt" not in ack[0]
          and "docs/imaginary.md" not in ack[0])


def test_partial_scope_ack_does_not_discharge_the_rest(workspace: Path) -> None:
    """Acknowledging one path must not carry the others.

    With two exclusions firing through a link, recording only the first meant
    discharging it was enough -- a private key landed in keys/ under a grant
    that named only secrets/alias/. Every path that crossed a boundary must be
    acknowledged, so an ack list is checked per path, never as a token gesture."""
    m = open_mission(workspace, "m-partial", "Two drifts.", scope_in=["docs/**"])
    m.approve()
    m.record_effect("src/one.py", "drift a", "pa-1")
    m.record_effect("etc/two.conf", "drift b", "pa-2")
    m.begin_verification()
    acceptor = Mission.load(workspace, actor="agent:acceptor")
    try:
        acceptor.record_verdict("PASS", acceptor_id="agent:acceptor",
                                 assurance_tier="declared-role-separation",
                                 reason="done", scope_ack=["src/one.py"])
        check("partial-ack-does-not-discharge", False)
    except AcceptanceRefused as exc:
        check("partial-ack-does-not-discharge",
              "etc/two.conf" in str(exc) and "src/one.py" not in str(exc))
    check("full-ack-discharges",
          isinstance(acceptor.record_verdict(
              "PASS", acceptor_id="agent:acceptor",
              assurance_tier="declared-role-separation", reason="done",
              scope_ack=["src/one.py", "etc/two.conf"]), int))


def test_bare_wildcard_is_not_a_discharge_key(workspace: Path) -> None:
    """A markdown bullet list must not discharge every drifted path.

    `_is_path_pattern` accepts `*` and `**` -- correct for a scope declaration,
    catastrophic for a discharge token: _glob_regex('*') is '[^/]*$' and
    _glob_regex('**') is '.*$'. `amend` carries the operator's words VERBATIM
    and a multi-part grant is most naturally a bullet list, so the bullets
    themselves became a universal key. Demonstrated end to end: a genuine,
    entirely unrelated two-line grant discharged an out-of-scope write to
    secrets.env."""
    from custody_mission import _amendment_names
    bullets = "* you may spend up to 20 dollars on API calls\n* you may restart the pod"
    check("bullet-list-does-not-name", not _amendment_names(bullets, "secrets.env"))
    check("double-star-does-not-name",
          not _amendment_names("go ahead ** proceed **", "secrets/prod.env"))
    check("parenthesised-star-does-not-name",
          not _amendment_names("approved for all files (*)", "src/app.py"))
    check("arithmetic-star-does-not-name",
          not _amendment_names("budget is 5 * 4 dollars", "src/app.py"))
    # a wildcard that still names something specific must keep working
    check("extension-glob-still-names",
          _amendment_names("operator: *.env files are fine", "secrets.env"))

    m = open_mission(workspace, "m-star", "Bulleted grant.",
                     scope_out=["secrets.env"])
    m.approve()
    m.record_effect("secrets.env", "TOKEN=hunter2", "st-1")
    m.amend_authority(bullets)
    m.begin_verification()
    acceptor = Mission.load(workspace, actor="agent:acceptor")
    try:
        acceptor.record_verdict("PASS", acceptor_id="agent:acceptor",
                                 assurance_tier="declared-role-separation",
                                 reason="done")
        check("bullet-list-does-not-discharge-e2e", False)
    except AcceptanceRefused as exc:
        check("bullet-list-does-not-discharge-e2e",
              "crossed the declared scope" in str(exc))


def test_later_amendment_must_name_the_drift_it_discharges(workspace: Path) -> None:
    """Ordering is necessary but NOT sufficient, which the first fix missed.

    "Some amendment was recorded after the drift" makes every later grant a
    universal key: a cost allowance mentioning no boundary would discharge an
    out-of-scope write it never named. A gate whose key is any key is not a
    gate. The amendment must NAME the artifact -- literally, by glob, or by
    directory prefix.

    The error direction is chosen: a false BLOCK is discharged by re-running
    `amend` with the path named, leaving the record strictly better; a false
    ALLOW writes "the chain is clean" over work no grant covers."""
    m = open_mission(workspace, "m-attrib", "Attributed.", scope_in=["docs/**"])
    m.approve()
    m.record_effect("src/late.py", "drift", "att-1")          # drift FIRST
    m.amend_authority("operator: budget raised to 50 dollars")  # later, unrelated
    m.begin_verification()
    acceptor = Mission.load(workspace, actor="agent:acceptor")
    try:
        acceptor.record_verdict("PASS", acceptor_id="agent:acceptor",
                                 assurance_tier="declared-role-separation",
                                 reason="done")
        check("unrelated-later-amendment-does-not-discharge", False)
    except AcceptanceRefused as exc:
        check("unrelated-later-amendment-does-not-discharge",
              "crossed the declared scope" in str(exc))

    # An amendment that NAMES the path still does not discharge it. This
    # assertion used to be the opposite; see test_scope_ack_is_the_only_
    # discharge for why reading authorisation out of prose was abandoned.
    Mission.load(workspace, actor="agent:worker").amend_authority(
        "operator: src/late.py was authorized")
    acceptor = Mission.load(workspace, actor="agent:acceptor")
    try:
        acceptor.record_verdict("PASS", acceptor_id="agent:acceptor",
                                 assurance_tier="declared-role-separation",
                                 reason="done")
        check("naming-amendment-still-does-not-discharge", False)
    except AcceptanceRefused as exc:
        check("naming-amendment-still-does-not-discharge",
              "crossed the declared scope" in str(exc))


def test_amendment_naming_is_token_wise_not_substring(workspace: Path) -> None:
    """`data.py` must not discharge drift on `a.py`.

    A raw substring test is the false-ALLOW direction: unrelated prose that
    happens to contain the path as a fragment would answer for it."""
    from custody_mission import _amendment_names
    check("names-exact-token", _amendment_names("operator: src/a.py ok", "src/a.py"))
    check("names-glob-token", _amendment_names("operator: src/*.py ok", "src/a.py"))
    check("names-dir-prefix", _amendment_names("operator: the src/ work", "src/a.py"))
    check("names-trailing-punctuation",
          _amendment_names("authorized src/a.py.", "src/a.py"))
    check("substring-fragment-does-not-name",
          not _amendment_names("operator: src/data.py ok", "src/a.py"))
    check("unrelated-prose-does-not-name",
          not _amendment_names("operator: budget raised", "src/a.py"))
    check("dir-prefix-does-not-overreach",
          not _amendment_names("operator: the src/ work", "srcx/a.py"))


def test_a_denial_is_not_a_grant(workspace: Path) -> None:
    """Naming a path in order to FORBID it must not discharge drift on it.

    A token match cannot tell a grant from a denial, so "secrets.env remains
    forbidden" -- the one amendment that explicitly withheld authority --
    unlocked the PASS for writing secrets.env. Prose cannot establish grant
    semantics; es#150 proposes the structured field that can. Until then a
    clause carrying a denial marker discharges nothing.

    Error direction is chosen: a genuine grant phrased with one of these words
    is a false BLOCK, re-amendable in plainer terms. Reading a prohibition as
    permission writes "clean" over exactly the work the operator forbade."""
    from custody_mission import _amendment_names
    # `_amendment_names` is now a HINT and deliberately does NOT judge intent:
    # it reports that the text mentions the path, which is all a substring test
    # can honestly claim. A denial mentions the path too -- that is the point.
    check("denial-mentions-the-path",
          _amendment_names("secrets.env remains forbidden", "secrets.env"))
    check("grant-mentions-the-path",
          _amendment_names("you may rotate secrets.env now", "secrets.env"))
    check("unrelated-text-mentions-nothing",
          not _amendment_names("budget raised to 50 dollars", "secrets.env"))

    m = open_mission(workspace, "m-deny", "Denied.", scope_out=["secrets.env"])
    m.approve()
    m.record_effect("secrets.env", "TOKEN=x", "dn-1")
    m.amend_authority("operator: secrets.env remains forbidden")
    m.begin_verification()
    acceptor = Mission.load(workspace, actor="agent:acceptor")
    try:
        acceptor.record_verdict("PASS", acceptor_id="agent:acceptor",
                                 assurance_tier="declared-role-separation",
                                 reason="done")
        check("denial-does-not-discharge-e2e", False)
    except AcceptanceRefused as exc:
        check("denial-does-not-discharge-e2e",
              "crossed the declared scope" in str(exc))


def test_whitespace_bearing_path_can_be_acknowledged(workspace: Path) -> None:
    """A finding on a name that really ends in a space had no operator exit.

    The ack was `_np(p.strip())`, the finding was `_np(p)`: two different
    functions on the two sides of one comparison. Measured against the shipped
    code, a receipted `'secret.env '` refused every ack an acceptor could
    reach -- `'secret.env '`, `'secret.env'`, `'  secret.env  '`,
    `'./secret.env '`. (The strip runs before `_normalize_relpath`, so
    `'secret.env /'` did discharge it; an exit produced by an implementation
    detail and printed nowhere is not an exit.)

    The fix is NOT to strip the finding too: a name ending in a space is a
    legal POSIX filename, and equating it with the stripped name would let an
    ack for `secret.env` silently retire custody of `secret.env `."""
    from custody_store import MissionStore
    m = open_mission(workspace, "m-ws", "Whitespace.", scope_in=["docs/**"])
    m.approve()
    m.record_effect("secret.env ", "leak", "ws-1")
    m.begin_verification()
    violating = {p for f in m.scope_consistency() for p in f["violating_paths"]}
    check("whitespace-finding-keeps-the-real-name", "secret.env " in violating)

    acceptor = Mission(MissionStore(m.store.mission_dir), workspace,
                       actor="agent:acceptor")
    shown = None
    try:
        acceptor.record_verdict("PASS", acceptor_id="agent:acceptor",
                                 assurance_tier="declared-role-separation",
                                 reason="done")
    except AcceptanceRefused as exc:
        shown = str(exc)
    # the acceptor cannot type a spelling the message hides
    check("whitespace-path-is-visible-in-the-refusal",
          shown is not None and '"secret.env "' in shown)
    check("whitespace-refusal-explains-the-quoting",
          shown is not None and "part of the NAME" in shown)

    # Every representation must be acked; on NT resolve() drops the trailing
    # space, so the finding legitimately carries both spellings. Catching the
    # refusal matters: under the mutation this test exists to catch, the ack
    # does NOT discharge, and an escaping AcceptanceRefused would abort main()
    # mid-registry -- so every later check would read ABSENT, which cannot be
    # told from passing.
    try:
        landed = acceptor.record_verdict(
            "PASS", acceptor_id="agent:acceptor",
            assurance_tier="declared-role-separation", reason="done",
            scope_ack=sorted(violating))
    except (AcceptanceRefused, IllegalTransition):
        landed = None
    check("whitespace-path-is-acknowledgeable", isinstance(landed, int))


def test_scope_ack_whitespace_case_table(workspace: Path) -> None:
    """The ack rule is a case table, not one example -- and the row that looks
    redundant is the one that decides it.

    Rows 3 and 4 differ only in which of two colliding paths the acceptor
    typed. Row 3 alone is satisfied by stripping both sides, by exact matching,
    and by a union of the two; only row 4 separates exact-first from the union,
    because only there does the stripped form of the ack ALSO name the other
    outstanding path."""
    from custody_mission import _acknowledged_paths
    pair = {"secret.env", "secret.env "}
    cases = [
        # (label, outstanding, ack, expected matched set)
        ("paste-tolerance", {"secrets.env"}, ["secrets.env "], {"secrets.env"}),
        ("exact-trailing-space", {"secret.env "}, ["secret.env "],
         {"secret.env "}),
        ("collision-bare-ack", pair, ["secret.env"], {"secret.env"}),
        ("collision-spaced-ack", pair, ["secret.env "], {"secret.env "}),
        ("stripped-ack-does-not-reach-spaced-path", {"secret.env "},
         ["secret.env"], set()),
        ("interior-whitespace", {"a  b.env"}, ["a  b.env"], {"a  b.env"}),
        ("leading-space", {" secret.env"}, [" secret.env"], {" secret.env"}),
        ("trailing-tab", {"secret.env\t"}, ["secret.env\t"], {"secret.env\t"}),
        ("all-whitespace-name", {"   "}, ["   "], {"   "}),
        ("ack-naming-nothing", {"secrets.env"}, ["never-a-finding.txt"], set()),
        ("empty-ack-is-inert", {"secrets.env"}, [""], set()),
    ]
    for label, outstanding, ack, expected in cases:
        got = _acknowledged_paths(ack, set(outstanding))
        check(f"ack-table-{label}", got == expected)


def _pass_with_racer(workspace: Path, label: str, racer_action):
    """Drive a PASS-with-drift, letting `racer_action` write inside the window
    between the scope-ack checkpoint and the `completed` checkpoint.

    The racer fires on the first load that OBSERVES the scope-ack note, not on
    the Nth call: a count-based injection silently stops testing the window the
    moment anyone adds or removes a `load_latest`, and it would still go green.
    The racer uses its own MissionStore so it does not recurse through this
    wrapper."""
    from custody_store import MissionStore
    m = open_mission(workspace, f"m-{label}", "Raced.",
                     scope_out=["secrets.env"])
    m.approve()
    m.record_effect("secrets.env", "leak", f"{label}-1")
    m.begin_verification()

    store = m.store
    real_load = store.load_latest
    fired: list[bool] = []

    def racing_load():
        latest, path = real_load()
        if not fired and any(n.startswith("scope-ack by ")
                             for n in latest["state"]["notes"]):
            fired.append(True)
            racer_action(Mission(MissionStore(store.mission_dir), workspace,
                                 actor="agent:other"))
            return real_load()
        return latest, path

    store.load_latest = racing_load
    acceptor = Mission(store, workspace, actor="agent:acceptor")
    try:
        outcome = acceptor.record_verdict(
            "PASS", acceptor_id="agent:acceptor",
            assurance_tier="declared-role-separation", reason="looks fine",
            scope_ack=["secrets.env"])
    except CustodyError as exc:
        outcome = exc
    finally:
        store.load_latest = real_load
    final, _ = MissionStore(store.mission_dir).load_latest()
    verdicts_dir = store.mission_dir / "verdicts"
    written = (sorted(p.name for p in verdicts_dir.glob("*.json"))
               if verdicts_dir.is_dir() else [])
    return fired, outcome, final, written


def test_status_is_revalidated_after_the_scope_ack_checkpoint(
        workspace: Path) -> None:
    """The scope-ack write opened a window that the `completed` write ignored.

    `_write_next(scope_note)` -> `load_latest()` -> `_write_next("completed")`.
    The status validated at entry is stale by the time it is used, and the line
    it races into predates this change -- the pre-existing line is the victim,
    not the cause. Measured against the shipped code: a concurrent `cancel`
    produced a FINAL status of 'completed' with notes reading 'cancelled:
    operator pulled the plug' then 'PASS: looks fine'; a concurrent FAIL
    produced 'completed' while unresolved_verdicts still held 'FAIL:no good'.
    A cancelled mission and a failed mission both closed as PASSED."""
    rows = [
        ("cancel", lambda r: r.cancel("operator pulled the plug"), "cancelled"),
        ("fail", lambda r: r.record_verdict(
            "FAIL", acceptor_id="agent:other",
            assurance_tier="declared-role-separation", reason="no good"),
         "reopened"),
        # The row that refuted "status is the COMPLETE discriminator":
        # amend_authority leaves status 'verifying' while changing the
        # AUTHORITY the PASS asserts against. Reproduced pre-fix as a chain
        # ending scope-ack -> 'authority amended: operator now also requires
        # B' -> 'PASS: looks fine' -- an acceptance recorded against a
        # manifest the acceptor never evaluated. Unchanged drift does not
        # make an authority change benign, so the reloaded manifest must BE
        # the evaluated one.
        ("amend", lambda r: r.amend_authority("operator now also requires B"),
         "verifying"),
    ]
    for label, action, expected in rows:
        fired, outcome, final, written = _pass_with_racer(
            workspace / f"ws-{label}", label, action)
        check(f"race-{label}-window-was-entered", bool(fired))
        check(f"race-{label}-pass-refused",
              isinstance(outcome, IllegalTransition))
        check(f"race-{label}-status-not-overwritten",
              final["status"] == expected)
        check(f"race-{label}-no-pass-note",
              not any(n.startswith("PASS: ") for n in final["state"]["notes"]))
        # the refusal must land BEFORE _store_verdict, or the mission keeps a
        # verdict record for a PASS that never entered the chain
        check(f"race-{label}-no-orphan-pass-verdict",
              not any(n.endswith("-PASS.json") for n in written))


def test_benign_write_in_the_window_does_not_block_the_pass(
        workspace: Path) -> None:
    """The row that distinguishes the adopted rule from the stricter one.

    Re-validating `status` allows a concurrent `note`; requiring the reloaded
    checkpoint to be the exact one just written would refuse it. Nothing that
    leaves status 'verifying' can change the drift set -- scope is immutable
    under _verify_manifest and receipt_ids cannot grow outside _EFFECT_STATES
    or 'reopened' -- so the stricter rule buys no safety and costs a false
    block. Deleting this test is what makes the stricter rule look free."""
    fired, outcome, final, _written = _pass_with_racer(
        workspace / "ws-note", "note", lambda r: r.note("just looking"))
    check("race-note-window-was-entered", bool(fired))
    check("benign-note-in-window-still-passes", isinstance(outcome, int))
    check("benign-note-in-window-preserved",
          "just looking" in final["state"]["notes"])
    check("benign-note-in-window-completes", final["status"] == "completed")


def test_hard_link_is_reported_not_silent(workspace: Path) -> None:
    """A hard link defeats path resolution, so the exposure must be DISCLOSED.

    Resolution follows symlinks. A hard link is not a link to a path -- it is a
    second name for one inode -- and `realpath` cannot see it. Measured against
    the shipped code: docs/alias.txt hard-linked to secrets/data.txt, an effect
    on the alias, scope.out=["secrets/**"] -> scope_consistency() returned []
    while secrets/data.txt read 'changed'.

    What is closed here is the SILENCE, not the boundary. `st_nlink` proves
    another name exists and cannot say where; naming it needs a workspace walk
    whose cost scales with the workspace rather than the mission (see
    _link_count). So the finding exists, has teeth (it must be acknowledged),
    and says plainly what it did not check."""
    from custody_mission import _MULTIPLY_LINKED
    m = open_mission(workspace, "m-hard", "Hard-linked.",
                     scope_in=["docs/**"], scope_out=["secrets/**"])
    m.approve()
    (workspace / "docs").mkdir(parents=True, exist_ok=True)
    (workspace / "secrets").mkdir(exist_ok=True)
    (workspace / "secrets" / "data.txt").write_text("orig", encoding="utf-8")
    try:
        os.link(workspace / "secrets" / "data.txt",
                workspace / "docs" / "alias.txt")
    except (OSError, NotImplementedError, AttributeError):
        print("skip hard-link (hard links unavailable on this host)")
        return
    m.record_effect("docs/alias.txt", "changed", "hl-1")
    check("hard-link-write-really-landed-in-secrets",
          (workspace / "secrets" / "data.txt").read_text(encoding="utf-8")
          == "changed")
    findings = m.scope_consistency()
    check("hard-link-is-not-silent",
          [(f["artifact_path"], f["reason"]) for f in findings]
          == [("docs/alias.txt", _MULTIPLY_LINKED)])
    # Indexing findings[0] unguarded would raise on the very mutation this
    # test exists to catch, aborting main() mid-registry -- so the checks
    # below would read ABSENT, and absent cannot be told from passing.
    check("hard-link-count-recorded",
          bool(findings) and findings[0].get("link_count") == 2)

    # teeth: a PASS is refused, and the refusal says what was NOT checked
    m.begin_verification()
    acceptor = Mission.load(workspace, actor="agent:acceptor")
    refusal = None
    try:
        acceptor.record_verdict("PASS", acceptor_id="agent:acceptor",
                                 assurance_tier="declared-role-separation",
                                 reason="done")
    except AcceptanceRefused as exc:
        refusal = str(exc)
    check("hard-link-refuses-pass",
          refusal is not None and "docs/alias.txt" in refusal)
    check("hard-link-refusal-discloses-the-limit",
          refusal is not None
          and "MULTIPLY LINKED" in refusal and "CANNOT see" in refusal)
    # the refusal names the QUALIFIED spelling: this obligation is not the
    # boundary judgement, and its ack must not look like one
    check("hard-link-refusal-names-the-linked-token",
          refusal is not None and "linked:docs/alias.txt" in refusal)
    # A BARE ack no longer discharges a link obligation: 'the operator
    # authorised this path' and 'I found the other name and checked where it
    # points' are different judgements, and the cheaper one used to absorb
    # the dearer one under the shared path key. This assertion changed
    # DELIBERATELY (it pinned the bare-ack discharge when the two kinds
    # shared a key); the surface is #143's own unreleased one.
    try:
        acceptor.record_verdict(
            "PASS", acceptor_id="agent:acceptor",
            assurance_tier="declared-role-separation", reason="done",
            scope_ack=["docs/alias.txt"])
        check("hard-link-bare-ack-does-not-discharge", False)
    except AcceptanceRefused:
        check("hard-link-bare-ack-does-not-discharge", True)
    try:
        landed = acceptor.record_verdict(
            "PASS", acceptor_id="agent:acceptor",
            assurance_tier="declared-role-separation", reason="done",
            scope_ack=["linked:docs/alias.txt"])
    except (AcceptanceRefused, IllegalTransition):
        landed = None
    check("hard-link-is-dischargeable-by-linked-ack", isinstance(landed, int))
    final, _ = acceptor.store.load_latest()
    check("hard-link-ack-recorded-in-qualified-spelling",
          any(n.startswith("scope-ack by agent:acceptor: ")
              and "linked:docs/alias.txt" in n
              for n in final["state"]["notes"]))


def test_ordinary_artifact_is_not_multiply_linked(workspace: Path) -> None:
    """Positive control for the absence claim the check above rests on.

    "Ordinary receipted artifacts do not trip this" is an absence claim, and
    its control has to match the class: an artifact written by record_effect,
    on the same filesystem, stat'ed the same way, must report st_nlink == 1 --
    otherwise the hard-link finding fires on every mission and the suite above
    proves only that SOMETHING was reported. A symlinked spelling is included
    because os.stat follows links, so it is the shape most likely to produce a
    false positive."""
    m = open_mission(workspace, "m-plain", "Plain.", scope_in=["docs/**"])
    m.approve()
    m.record_effect("docs/plain.md", "x", "pl-1")
    check("ordinary-artifact-nlink-is-1",
          os.stat(workspace / "docs" / "plain.md").st_nlink == 1)
    check("ordinary-artifact-flags-nothing", m.scope_consistency() == [])
    try:
        (workspace / "docs" / "alias").symlink_to(workspace / "docs",
                                                   target_is_directory=True)
    except (OSError, NotImplementedError):
        print("skip nlink-symlink-control (symlinks unavailable on this host)")
        return
    check("symlinked-spelling-nlink-is-1",
          os.stat(workspace / "docs" / "alias" / "plain.md").st_nlink == 1)


def test_link_count_is_none_when_the_artifact_is_gone(workspace: Path) -> None:
    """Unknown is never reported as one. A deleted or unreadable artifact must
    answer None and produce no finding, rather than crashing the read-only
    surface that acceptance depends on."""
    m = open_mission(workspace, "m-gone", "Gone.", scope_out=["secrets/**"])
    m.approve()
    m.record_effect("docs/gone.md", "x", "gn-1")
    (workspace / "docs" / "gone.md").unlink()
    check("link-count-none-when-absent", m._link_count("docs/gone.md") is None)
    check("absent-artifact-flags-nothing", m.scope_consistency() == [])


def test_exclusion_match_does_not_shadow_the_inclusion_check(
        workspace: Path) -> None:
    """An exclusion match on ONE representation must not skip the inclusion
    test for the OTHERS.

    `elif includes:` meant the first exclusion hit ended the comparison for the
    whole effect. With scope.in=["docs/**"], scope.out=["alias/**"] and
    alias -> src, the finding named `alias/x.py` and nothing anywhere named
    `src/x.py` -- the path the write actually landed on, outside scope.in. An
    acceptor acking the only path the record showed them permitted a write to
    a destination the record never mentioned.

    Row 4 of the case table is pinned by the sibling assertion below: a path
    that both matches scope.out AND sits outside scope.in stays ONE finding
    under the specific reason. That is the row that separates this fix from
    "run both checks independently", which the two rules' identical union of
    violating paths cannot distinguish."""
    m = open_mission(workspace, "m-shadow", "Both boundaries.",
                     scope_in=["docs/**"], scope_out=["alias/**"])
    m.approve()
    (workspace / "src").mkdir(parents=True, exist_ok=True)
    try:
        (workspace / "alias").symlink_to(workspace / "src",
                                          target_is_directory=True)
    except (OSError, NotImplementedError):
        print("skip exclusion-shadow (symlinks unavailable on this host)")
        return
    m.record_effect("alias/x.py", "lands in src/", "sh-1")
    findings = m.scope_consistency()
    covered = {p for f in findings for p in f["violating_paths"]}
    check("resolved-target-outside-scope-in-is-reported",
          covered == {"alias/x.py", "src/x.py"})
    check("both-reasons-reported",
          {f["reason"] for f in findings}
          == {"matches scope.out", "outside scope.in"})
    # ROW 4, and it looks redundant next to the assertions above: one path that
    # violates BOTH ways is reported once, under the exclusion. Deleting this
    # assertion is what makes "just run both checks" look correct.
    m2 = open_mission(workspace / "ws4", "m-row4", "One path, both ways.",
                      scope_in=["docs/**"], scope_out=["secrets/**"])
    m2.approve()
    m2.record_effect("secrets/c.env", "TOKEN=x", "r4-1")
    row4 = m2.scope_consistency()
    check("path-violating-both-ways-reported-once",
          [(f["reason"], f["violating_paths"]) for f in row4]
          == [("matches scope.out", ["secrets/c.env"])])


def test_symlinked_path_must_satisfy_scope_in_too(workspace: Path) -> None:
    """Inclusion is tested against where the write LANDS, like exclusion.

    The exclusion side checked both the declared and the resolved path while
    this one stayed lexical, so scope.in=["docs/**"] with docs/alias -> src/
    accepted a write to src/a.py. "Where it was not permitted to go" is the
    same defect as "where it was forbidden to go"."""
    m = open_mission(workspace, "m-in-link", "Included.", scope_in=["docs/**"])
    m.approve()
    (workspace / "src").mkdir(parents=True, exist_ok=True)
    (workspace / "docs").mkdir(exist_ok=True)
    try:
        (workspace / "docs" / "alias").symlink_to(workspace / "src",
                                                   target_is_directory=True)
    except (OSError, NotImplementedError):
        print("skip scope-in-symlink (symlinks unavailable on this host)")
        return
    m.record_effect("docs/alias/a.py", "lands in src/", "il-1")
    flagged = [(f["artifact_path"], f["reason"]) for f in m.scope_consistency()]
    check("scope-in-resolved-target-flagged",
          flagged == [("docs/alias/a.py", "outside scope.in")])


def test_amendment_must_name_the_path_that_actually_violated(
        workspace: Path) -> None:
    """A grant for the ALLOWED path must not discharge the FORBIDDEN landing.

    The finding carried only the lexical path, so with docs/alias -> secrets/
    an amendment naming docs/** discharged a write that landed in secrets/.
    The operator authorised docs/; nothing authorised secrets/x; PASS was
    accepted anyway."""
    m = open_mission(workspace, "m-viol", "Linked drift.",
                     scope_in=["docs/**"], scope_out=["secrets/**"])
    m.approve()
    (workspace / "secrets").mkdir(parents=True, exist_ok=True)
    (workspace / "docs").mkdir(exist_ok=True)
    try:
        (workspace / "docs" / "alias").symlink_to(workspace / "secrets",
                                                   target_is_directory=True)
    except (OSError, NotImplementedError):
        print("skip violating-path (symlinks unavailable on this host)")
        return
    m.record_effect("docs/alias/x.txt", "lands in secrets/", "vp-1")
    findings = m.scope_consistency()
    check("violating-paths-recorded",
          bool(findings) and findings[0].get("violating_paths") == ["secrets/x.txt"])
    m.amend_authority("operator: you may write under docs/**")
    m.begin_verification()
    acceptor = Mission.load(workspace, actor="agent:acceptor")
    try:
        acceptor.record_verdict("PASS", acceptor_id="agent:acceptor",
                                 assurance_tier="declared-role-separation",
                                 reason="done")
        check("grant-for-allowed-path-does-not-discharge-landing", False)
    except AcceptanceRefused as exc:
        check("grant-for-allowed-path-does-not-discharge-landing",
              "secrets/x.txt" in str(exc))


def test_symlinked_path_cannot_dodge_an_exclusion(workspace: Path) -> None:
    """A lexical path test alone lets a symlink walk around scope.out.

    With scope.out=["secrets/**"], a receipt for `docs/alias/k.env` -- where
    `docs/alias` links into `secrets/` -- passes a lexical check while the
    write landed exactly where it was forbidden. Both the chained declared
    path and the resolved target are tested, because neither is sound alone:
    the declared path is tamper-evident but lexical, and a link resolved at
    acceptance time is the true target but re-pointable afterwards."""
    m = open_mission(workspace, "m-link", "Linked.", scope_out=["secrets/**"])
    m.approve()
    (workspace / "secrets").mkdir(parents=True, exist_ok=True)
    try:
        (workspace / "docs").mkdir(exist_ok=True)
        (workspace / "docs" / "alias").symlink_to(workspace / "secrets",
                                                   target_is_directory=True)
    except (OSError, NotImplementedError):
        # Windows needs Developer Mode or admin to create links; CI is Linux
        # and does exercise this. Reported, never silently counted as passing.
        print("skip symlinked-exclusion (symlinks unavailable on this host)")
        return
    m.record_effect("docs/alias/k.env", "KEY=v", "ln-1")
    flagged = [f["artifact_path"] for f in m.scope_consistency()]
    check("symlinked-exclusion-flagged", flagged == ["docs/alias/k.env"])


def test_forged_receipt_path_cannot_dodge_scope(workspace: Path) -> None:
    """Scope classification reads the CHAINED effect note, not the mutable
    receipt file. A schema-valid receipt keeping the same request_id but
    claiming a different artifact_path would otherwise move out-of-scope work
    into scope and let PASS through."""
    m = open_mission(workspace, "m-forge", "Bounded.", scope_in=["docs/**"])
    m.approve()
    m.record_effect("src/b.py", "out of scope", "fg-1")
    receipt_path = m.store.receipt_path("fg-1")
    record = json.loads(receipt_path.read_text(encoding="utf-8"))
    record["artifact_path"] = "docs/decoy.md"
    receipt_path.write_text(json.dumps(record, indent=1, sort_keys=True) + "\n",
                            encoding="utf-8")
    check("forged-receipt-path-still-flagged",
          any(f["artifact_path"] == "src/b.py" for f in m.scope_consistency()))


def test_empty_scope_declares_nothing_and_flags_nothing(workspace: Path) -> None:
    """Every mission opened before this change has scope.in=[] and
    scope.out=[]. An empty declaration is UNBOUNDED, so it must flag nothing
    and refuse nothing -- otherwise this change retroactively breaks every
    existing mission's ability to close."""
    m = open_mission(workspace, "m-noscope", "Unbounded work.")
    m.approve()
    m.record_effect("anything/at/all.md", "x", "ns-1")
    check("empty-scope-flags-nothing", m.scope_consistency() == [])
    m.begin_verification()
    acceptor = Mission.load(workspace, actor="agent:acceptor")
    revision = acceptor.record_verdict(
        "PASS", acceptor_id="agent:acceptor",
        assurance_tier="declared-role-separation", reason="done")
    check("empty-scope-pass-accepted", isinstance(revision, int))


def test_normalize_relpath_dot_segment_case_table(workspace: Path) -> None:
    """'.' SEGMENTS collapse to a fixed point; '..' and in-name dots do not.

    The terminal-'/.'  rows are the change; the untouched rows are the
    boundary that keeps NT-only trailing-dot filename semantics out of a
    cross-platform lexical normaliser. 'docs/.//' is the fixed-point row:
    the terminal-dot rule exposes a spelling the separator rule must see
    again."""
    from custody_mission import _normalize_relpath
    cases = [
        ("docs/x.txt/.", "docs/x.txt"),
        ("docs/.", "docs"),
        ("docs/./.", "docs"),
        ("docs/.//", "docs"),
        ("./docs/x.txt", "docs/x.txt"),
        ("docs/./x.txt", "docs/x.txt"),
        ("././docs", "docs"),
        (".", ""),
        ("./", ""),
        ("./.", ""),
        # untouched: a dot INSIDE a final segment name is a legal character
        ("weird.", "weird."),
        ("docs/weird.", "docs/weird."),
        ("a..b/x", "a..b/x"),
        ("docs/.../x", "docs/.../x"),
        # '..' is never collapsed -- the resolver refuses it, the pattern
        # side discloses it, and folding it here would be resolution
        ("docs/../x", "docs/../x"),
    ]
    for raw, expected in cases:
        check(f"normrel-{raw!r}", _normalize_relpath(raw) == expected)


def test_terminal_dot_spelling_agrees_with_the_resolver(
        workspace: Path) -> None:
    """Lexical and resolver disagreed on a terminal '/.', in both directions.

    Receipt side (the reported row, false FLAG -- safe, but noise): a receipt
    spelled 'docs/x.txt/.' names the file 'docs/x.txt' to the resolver while
    the old normaliser kept the dot, so scope.in=['docs/*.txt'] read its own
    in-scope write as outside the boundary.

    Pattern side (the mirror row the derivation hunted down, false CLEAN --
    the priority flip): a scope.out entry carrying one '/.' spelling
    compiled to a regex no normalized receipt path can ever match, silently
    disabling a boundary the operator wrote -- and
    `uncompared_scope_entries` did not list it, so nothing disclosed the
    nothing."""
    m = open_mission(workspace, "m-dot", "Dotted.",
                     scope_in=["docs/*.txt"], scope_out=["secrets/**/."])
    m.approve()
    m.record_effect("docs/x.txt/.", "in scope", "dot-1")
    m.record_effect("secrets/leak.env", "excluded", "dot-2")
    findings = [(f["artifact_path"], f["reason"])
                for f in m.scope_consistency()]
    check("terminal-dot-receipt-is-not-false-flagged",
          ("docs/x.txt/.", "outside scope.in") not in findings)
    check("terminal-dot-exclusion-is-not-silently-disabled",
          ("secrets/leak.env", "matches scope.out") in findings)


def test_whole_workspace_include_is_disclosed_not_wedged(
        workspace: Path) -> None:
    """scope.in=['./'] is a natural spelling of 'the whole workspace is in
    scope' -- the include-side twin of the terminal-dot exclusion row, and
    stronger against the 'no honest manifest contains that' objection. It
    normalizes to the EMPTY path, which no receipt ever spells, so compiling
    it wedges every close behind a boundary that permits everything. Demoted
    to uncompared instead: the declared meaning (nothing is outside) and the
    disclosure (no machine checked it) are both delivered."""
    from custody_mission import uncompared_scope_entries
    m = open_mission(workspace, "m-dotslash", "Everything in scope.",
                     scope_in=["./"])
    m.approve()
    m.record_effect("anything/x.py", "work", "ds-1")
    check("dot-slash-include-flags-nothing", m.scope_consistency() == [])
    latest, _ = m.store.load_latest()
    disclosed = uncompared_scope_entries(latest["manifest"])
    check("dot-slash-include-is-disclosed",
          disclosed["in"] == ["./"] and disclosed["in_comparison_disabled"])
    m.begin_verification()
    acceptor = Mission.load(workspace, actor="agent:acceptor")
    # a regression here must read as FAIL, not abort the registry mid-run
    try:
        revision = acceptor.record_verdict(
            "PASS", acceptor_id="agent:acceptor",
            assurance_tier="declared-role-separation", reason="done")
    except AcceptanceRefused:
        revision = None
    check("dot-slash-include-does-not-wedge-the-close",
          isinstance(revision, int))


def test_trailing_newline_path_is_flagged_and_dischargeable(
        workspace: Path) -> None:
    """The '$' anchor matched one character too many, and the fix must bring
    its own discharge recipe.

    'safe.txt\\n' is a different file from 'safe.txt', and '$' matches just
    before a trailing newline, so the glob said the undeclared file was
    inside scope.in -- a false CLEAN one byte past the declaration. With \\Z
    the receipt is flagged; the refusal shows the path JSON-quoted; and the
    recipe it prints must WORK, including after a shell eats the outer
    quotes and delivers backslash-n as two literal characters -- a refusal
    whose printed exit does not discharge is the dead-end class this PR
    already paid for twice."""
    if os.name == "nt":
        print("skip trailing-newline path (NT filenames cannot carry one)")
        return
    m = open_mission(workspace, "m-nl", "Anchored.", scope_in=["*.txt"])
    m.approve()
    # HISTORICAL record: the es#153 guard refuses minting this path now,
    # and the discharge machinery for pre-guard records is what this pins
    record_effect_as_historical(m, "safe.txt\n", "x", "nl-1")
    findings = [(f["artifact_path"], f["reason"])
                for f in m.scope_consistency()]
    check("trailing-newline-path-is-outside-scope-in",
          findings == [("safe.txt\n", "outside scope.in")])
    m.begin_verification()
    acceptor = Mission.load(workspace, actor="agent:acceptor")
    refusal = None
    try:
        acceptor.record_verdict("PASS", acceptor_id="agent:acceptor",
                                 assurance_tier="declared-role-separation",
                                 reason="done")
    except AcceptanceRefused as exc:
        refusal = str(exc)
    check("trailing-newline-refusal-shows-json-quoting",
          refusal is not None and json.dumps("safe.txt\n") in refusal)
    check("trailing-newline-refusal-says-the-quoting-works",
          refusal is not None and "itself accepted" in refusal)
    # what the shell actually delivers from the printed recipe: outer quotes
    # eaten, backslash-n as TWO literal characters
    try:
        landed = acceptor.record_verdict(
            "PASS", acceptor_id="agent:acceptor",
            assurance_tier="declared-role-separation", reason="done",
            scope_ack=["safe.txt\\n"])
    except (AcceptanceRefused, IllegalTransition):
        # IllegalTransition is the regression shape where the FIRST verdict
        # wrongly landed: it must read as FAIL here, not abort the registry
        landed = None
    check("printed-recipe-discharges-after-shell-mangling",
          isinstance(landed, int))


def test_scope_ack_json_spelling_case_table(workspace: Path) -> None:
    """A backslash-bearing ack has TWO readings -- separator-folded and
    JSON-decoded -- and neither is exact: both are interpretations of
    keystrokes a shell already rewrote. An ack discharges only when its
    readings agree on ONE outstanding path; naming two distinct outstanding
    paths is AMBIGUOUS and discharges nothing, because over-matching
    silently retires custody of a path nobody named. The collision row
    changed DELIBERATELY: it used to pin the folded reading as 'exact
    first', and the round-3 refutation executed that rule discharging a
    slash-twin the acceptor never named -- the pinned row was the defect.
    The fixpoint rows are the cure's other half: discharging the twin by
    its own unambiguous spelling makes the mangled spelling unambiguous, so
    the full printed recipe converges in one call, in either order."""
    from custody_mission import _acknowledged_paths
    nl = "safe.txt\n"
    cases = [
        # (label, outstanding, ack list, expected matched set)
        ("bare-escape-decodes", {nl}, ["safe.txt\\n"], {nl}),
        ("quoted-verbatim-decodes", {nl}, ['"safe.txt\\n"'], {nl}),
        ("backslash-collision-is-ambiguous-and-inert", {"safe.txt/n", nl},
         ["safe.txt\\n"], set()),
        ("fixpoint-slash-first", {"safe.txt/n", nl},
         ["safe.txt/n", "safe.txt\\n"], {"safe.txt/n", nl}),
        ("fixpoint-mangled-first", {"safe.txt/n", nl},
         ["safe.txt\\n", "safe.txt/n"], {"safe.txt/n", nl}),
        ("duplicated-ambiguous-ack-stays-inert", {"safe.txt/n", nl},
         ["safe.txt\\n", "safe.txt\\n"], set()),
        ("one-ack-never-discharges-two", {"secret.env", "secret.env "},
         ["secret.env "], {"secret.env "}),
        ("real-newline-ack-still-exact", {nl}, [nl], {nl}),
        ("decode-that-names-nothing-is-inert", {"other.txt"},
         ["safe.txt\\n"], set()),
        ("embedded-quote-is-never-wrapped", {"a\nb"}, ['a"b\\n'], set()),
        ("plain-acks-unchanged", {"secrets.env"}, ["secrets.env"],
         {"secrets.env"}),
    ]
    for label, outstanding, ack, expected in cases:
        got = _acknowledged_paths(ack, set(outstanding))
        check(f"json-ack-{label}", got == expected)


def test_slash_twin_cannot_be_discharged_by_the_newline_files_recipe(
        workspace: Path) -> None:
    """The round-3 P1, end to end: with BOTH 'safe.txt/n' (a real nested
    path) and 'safe.txt\\n' (a newline-bearing filename) outstanding, the
    newline file's shell-mangled recipe used to silently discharge the
    slash-twin -- a PASS closed with a path the acceptor never judged, and
    the permanent note attributed it to them. Now the ambiguous ack is
    inert on its own, and the full recipe discharges each path under its
    own spelling."""
    if os.name == "nt":
        print("skip slash-twin (NT filenames cannot carry a newline)")
        return
    m = open_mission(workspace, "m-twin", "Twinned.", scope_in=["docs/**"])
    m.approve()
    m.record_effect("safe.txt/n", "nested", "tw-1")
    # HISTORICAL record: the newline twin predates the es#153 guard
    record_effect_as_historical(m, "safe.txt\n", "newline", "tw-2")
    m.begin_verification()
    acceptor = Mission.load(workspace, actor="agent:acceptor")
    # the mangled spelling alone: ambiguous, discharges NOTHING -- before
    # the fix it silently discharged the slash-twin
    try:
        acceptor.record_verdict(
            "PASS", acceptor_id="agent:acceptor",
            assurance_tier="declared-role-separation", reason="done",
            scope_ack=["safe.txt\\n", "safe.txt\\n"])
        check("ambiguous-recipe-discharges-nothing", False)
    except AcceptanceRefused as exc:
        # both paths still outstanding: the refusal names both
        check("ambiguous-recipe-discharges-nothing",
              "safe.txt/n" in str(exc) and json.dumps("safe.txt\n") in str(exc))
    except IllegalTransition:
        check("ambiguous-recipe-discharges-nothing", False)
    # the full printed recipe: each path under its own spelling, one call
    try:
        landed = acceptor.record_verdict(
            "PASS", acceptor_id="agent:acceptor",
            assurance_tier="declared-role-separation", reason="done",
            scope_ack=["safe.txt\\n", "safe.txt/n"])
    except (AcceptanceRefused, IllegalTransition):
        landed = None
    check("full-twin-recipe-discharges-both", isinstance(landed, int))
    final, _ = acceptor.store.load_latest()
    ack_notes = [n for n in final["state"]["notes"]
                 if n.startswith("scope-ack by ")]
    check("twin-note-attributes-both-paths-correctly",
          len(ack_notes) == 1
          and "safe.txt/n" in ack_notes[0]
          and json.dumps("safe.txt\n") in ack_notes[0])


def test_unknown_finding_kind_fails_closed_and_says_so(
        workspace: Path) -> None:
    """The unknown-kind branch is defensive against a FUTURE finding kind
    shipped without its ack shape, so no real mission can reach it -- and
    an unexercised guarantee is exactly the unpinned-claim shape round 3
    flagged. Driven here by substituting the finding source: the PASS must
    refuse, no token form may discharge it, and the message must name the
    dead end rather than advertising a recipe that does not exist."""
    m = open_mission(workspace, "m-unk", "Future kind.",
                     scope_out=["secrets.env"])
    m.approve()
    m.record_effect("secrets.env", "leak", "unk-1")
    m.begin_verification()
    acceptor = Mission.load(workspace, actor="agent:acceptor")
    real = acceptor.scope_consistency

    def with_unknown_kind():
        findings = real()
        return findings + [{"artifact_path": "secrets.env",
                            "request_id": "unk-1",
                            "violating_paths": ["secrets.env"],
                            "reason": "quantum drift"}]

    acceptor.scope_consistency = with_unknown_kind
    try:
        refusal = None
        try:
            acceptor.record_verdict(
                "PASS", acceptor_id="agent:acceptor",
                assurance_tier="declared-role-separation", reason="done",
                scope_ack=["secrets.env", "linked:secrets.env",
                           "quantum drift:secrets.env"])
        except AcceptanceRefused as exc:
            refusal = str(exc)
        check("unknown-kind-refuses-every-token-form", refusal is not None)
        check("unknown-kind-names-the-dead-end",
              refusal is not None
              and "No acknowledgement form exists" in refusal
              and "fails closed" in refusal)
    finally:
        acceptor.scope_consistency = real


def test_link_count_probes_only_inside_the_workspace(
        workspace: Path) -> None:
    """The raw stat probed wherever a forged receipt pointed.

    `self.workspace / rel` with an ABSOLUTE rel ignores the workspace
    entirely (Path join semantics), so acceptance stat-probed arbitrary
    filesystem paths named by a mutable receipt file -- an information-probe
    surface -- and could report MULTIPLY LINKED about bytes that were never
    the receipted artifact. And a forged rel of '.' resolves to the
    workspace root, whose st_nlink >= 2 on POSIX by construction: a false
    claim about a directory, which is what the S_ISREG gate refuses."""
    m = open_mission(workspace, "m-probe", "Probed.", scope_in=["docs/**"])
    m.approve()
    m.record_effect("docs/real.md", "x", "pr-1")
    receipt_path = m.store.receipt_path("pr-1")
    record = json.loads(receipt_path.read_text(encoding="utf-8"))

    def forge(path):
        record["artifact_path"] = path
        receipt_path.write_text(
            json.dumps(record, indent=1, sort_keys=True) + "\n",
            encoding="utf-8")

    # the chained note still says docs/real.md, so scope comparison is
    # unaffected; the link probe is what the forged spelling reaches
    check("workspace-root-is-not-multiply-linked",
          m._link_count(".") is None)
    check("absolute-path-is-not-probed",
          m._link_count("/etc/passwd") is None)
    check("escaping-path-is-not-probed",
          m._link_count("../outside.txt") is None)
    forge("/etc/passwd")
    check("forged-absolute-receipt-yields-no-link-finding",
          all(f["reason"] != _MULTIPLY_LINKED_REASON()
              for f in m.scope_consistency()))


def _MULTIPLY_LINKED_REASON():
    from custody_mission import _MULTIPLY_LINKED
    return _MULTIPLY_LINKED


def test_symlink_loop_cannot_crash_acceptance(workspace: Path) -> None:
    """A symlink loop is attacker-influenceable filesystem state, and
    `Path.resolve` raises RuntimeError on one (CPython 3.11: 'RuntimeError:
    Symlink loop') -- an uncaught raise on the acceptance path is a denial
    of service by exactly the tampering the comparison exists to catch.
    RuntimeError therefore joins the caught set; the mission still refuses
    or completes on the merits, it never crashes."""
    m = open_mission(workspace, "m-loop", "Looped.", scope_in=["docs/**"])
    m.approve()
    m.record_effect("docs/x.txt", "x", "lp-1")
    # replace docs/ with half of a docs <-> other loop AFTER the write
    shutil.rmtree(workspace / "docs")
    try:
        os.symlink("other", workspace / "docs")
        os.symlink("docs", workspace / "other")
    except (OSError, NotImplementedError, AttributeError):
        print("skip symlink-loop (symlinks unavailable on this host)")
        return
    check("loop-link-count-is-unknowable", m._link_count("docs/x.txt") is None)
    try:
        findings = m.scope_consistency()
        check("loop-scope-consistency-does-not-crash", True)
    except Exception:
        check("loop-scope-consistency-does-not-crash", False)
        return
    m.begin_verification()
    acceptor = Mission.load(workspace, actor="agent:acceptor")
    try:
        acceptor.record_verdict("PASS", acceptor_id="agent:acceptor",
                                 assurance_tier="declared-role-separation",
                                 reason="done",
                                 scope_ack=[p for f in findings
                                            for p in f["violating_paths"]])
        check("loop-acceptance-does-not-crash", True)
    except AcceptanceRefused:
        # refusing on the merits is a legal outcome; crashing is not
        check("loop-acceptance-does-not-crash", True)
    except Exception:
        check("loop-acceptance-does-not-crash", False)


def test_link_ack_is_categorical(workspace: Path) -> None:
    """The link ack acknowledges the CONDITION -- another name exists and the
    acceptor went and looked -- not a particular st_nlink value. Settled
    explicitly rather than left implied: a third name (count 2 -> 3) does
    not create a new obligation, because the judgement recorded is about the
    condition, and the finding never keyed on the number."""
    m = open_mission(workspace, "m-cat", "Counted.",
                     scope_in=["docs/**"])
    m.approve()
    (workspace / "docs").mkdir(parents=True, exist_ok=True)
    (workspace / "elsewhere").mkdir(exist_ok=True)
    (workspace / "docs" / "a.txt").write_text("x", encoding="utf-8")
    try:
        os.link(workspace / "docs" / "a.txt",
                workspace / "elsewhere" / "b.txt")
        os.link(workspace / "docs" / "a.txt",
                workspace / "elsewhere" / "c.txt")
    except (OSError, NotImplementedError, AttributeError):
        print("skip categorical-link (hard links unavailable on this host)")
        return
    m.record_effect("docs/a.txt", "y", "cat-1")
    findings = m.scope_consistency()
    check("three-name-artifact-has-one-link-obligation",
          [f.get("link_count") for f in findings] == [3])
    m.begin_verification()
    acceptor = Mission.load(workspace, actor="agent:acceptor")
    try:
        landed = acceptor.record_verdict(
            "PASS", acceptor_id="agent:acceptor",
            assurance_tier="declared-role-separation", reason="done",
            scope_ack=["linked:docs/a.txt"])
    except AcceptanceRefused:
        landed = None
    check("one-linked-ack-discharges-regardless-of-count",
          isinstance(landed, int))


def test_same_path_boundary_and_link_are_two_obligations(
        workspace: Path) -> None:
    """One path, two findings, two judgements, two acks. The bare ack alone
    used to discharge both; now each kind must be acknowledged in its own
    spelling, in either order, in one accept."""
    m = open_mission(workspace, "m-two", "Doubled.",
                     scope_out=["docs/**"])
    m.approve()
    (workspace / "docs").mkdir(parents=True, exist_ok=True)
    (workspace / "keep").mkdir(exist_ok=True)
    (workspace / "docs" / "a.txt").write_text("x", encoding="utf-8")
    try:
        os.link(workspace / "docs" / "a.txt", workspace / "keep" / "b.txt")
    except (OSError, NotImplementedError, AttributeError):
        print("skip two-obligation (hard links unavailable on this host)")
        return
    m.record_effect("docs/a.txt", "y", "two-1")
    reasons = sorted(f["reason"] for f in m.scope_consistency())
    check("both-findings-exist",
          reasons == sorted(["matches scope.out", _MULTIPLY_LINKED_REASON()]))
    m.begin_verification()
    acceptor = Mission.load(workspace, actor="agent:acceptor")
    for label, acks in (
            ("bare-only", ["docs/a.txt"]),
            ("linked-only", ["linked:docs/a.txt"])):
        try:
            acceptor.record_verdict(
                "PASS", acceptor_id="agent:acceptor",
                assurance_tier="declared-role-separation", reason="done",
                scope_ack=acks)
            check(f"two-obligation-{label}-is-not-enough", False)
        except AcceptanceRefused:
            check(f"two-obligation-{label}-is-not-enough", True)
        except IllegalTransition:
            # the regression shape where an EARLIER attempt wrongly landed:
            # FAIL, but never abort the registry
            check(f"two-obligation-{label}-is-not-enough", False)
    # A duplicated BARE path never widens: the exhausted-boundary
    # fallthrough only reaches tokens that parse as qualifiers, so repeating
    # 'docs/a.txt' cannot quietly discharge the link obligation the way a
    # repeated 'linked:...' token deliberately can in the shadow case.
    try:
        acceptor.record_verdict(
            "PASS", acceptor_id="agent:acceptor",
            assurance_tier="declared-role-separation", reason="done",
            scope_ack=["docs/a.txt", "docs/a.txt"])
        check("two-obligation-duplicated-bare-path-does-not-widen", False)
    except AcceptanceRefused:
        check("two-obligation-duplicated-bare-path-does-not-widen", True)
    except IllegalTransition:
        check("two-obligation-duplicated-bare-path-does-not-widen", False)
    try:
        landed = acceptor.record_verdict(
            "PASS", acceptor_id="agent:acceptor",
            assurance_tier="declared-role-separation", reason="done",
            scope_ack=["docs/a.txt", "linked:docs/a.txt"])
    except (AcceptanceRefused, IllegalTransition):
        landed = None
    check("two-obligation-both-acks-discharge", isinstance(landed, int))


def test_shadowed_linked_token_prints_a_working_recipe(
        workspace: Path) -> None:
    """A receipted file literally named 'linked:foo.txt' that crossed the
    boundary shares its bare ack spelling with the link obligation on
    foo.txt -- and exact-path-first consumes every bare 'linked:foo.txt' as
    the literal path, so a refusal printing that token for BOTH obligations
    is a recipe that cannot work no matter how often it is repeated (the
    dead-end class, third occurrence). The parser has always read
    'linked:"foo.txt"' as a qualifier; the message must print that spelling
    exactly when the bare one is shadowed, and the printed recipe must
    discharge both obligations in one accept."""
    m = open_mission(workspace, "m-shadow", "Shadowed.",
                     scope_out=["linked:foo.txt"])
    m.approve()
    (workspace / "keep").mkdir(exist_ok=True)
    (workspace / "foo.txt").write_text("x", encoding="utf-8")
    try:
        os.link(workspace / "foo.txt", workspace / "keep" / "other.txt")
    except (OSError, NotImplementedError, AttributeError):
        print("skip shadowed-token (hard links unavailable on this host)")
        return
    m.record_effect("linked:foo.txt", "crossing", "sh-1")
    m.record_effect("foo.txt", "linked bytes", "sh-2")
    m.begin_verification()
    acceptor = Mission.load(workspace, actor="agent:acceptor")
    refusal = None
    try:
        acceptor.record_verdict("PASS", acceptor_id="agent:acceptor",
                                 assurance_tier="declared-role-separation",
                                 reason="done")
    except AcceptanceRefused as exc:
        refusal = str(exc)
    check("shadow-refusal-exists", refusal is not None)
    check("shadow-refusal-prints-the-quoted-spelling",
          refusal is not None and 'linked:"foo.txt"' in refusal)
    check("shadow-refusal-still-names-the-literal-path",
          refusal is not None
          and "--scope-ack linked:foo.txt" in refusal)
    # ONE bare token is one judgement: it discharges the literal boundary
    # path only, and the link obligation stays outstanding
    try:
        acceptor.record_verdict(
            "PASS", acceptor_id="agent:acceptor",
            assurance_tier="declared-role-separation", reason="done",
            scope_ack=["linked:foo.txt"])
        check("shadow-single-bare-token-is-not-enough", False)
    except AcceptanceRefused:
        check("shadow-single-bare-token-is-not-enough", True)
    except IllegalTransition:
        check("shadow-single-bare-token-is-not-enough", False)
    # SHELL TRUTH: bash, PowerShell and CommandLineToArgvW all strip the
    # interior quotes from `linked:"foo.txt"`, so BOTH printed flags arrive
    # as the same bare token. This assertion previously pinned the opposite
    # (duplicate bare token refused) -- inverted DELIBERATELY when the
    # parser gained the exhausted-boundary fallthrough, because a recipe
    # that only works when quotes survive the shell is a dead end on the
    # one channel the refusal text addresses.
    try:
        landed = acceptor.record_verdict(
            "PASS", acceptor_id="agent:acceptor",
            assurance_tier="declared-role-separation", reason="done",
            scope_ack=["linked:foo.txt", "linked:foo.txt"])
    except (AcceptanceRefused, IllegalTransition):
        landed = None
    check("shadow-shell-argv-recipe-discharges-both", isinstance(landed, int))


def test_shadowed_linked_token_quoted_spelling_still_works(
        workspace: Path) -> None:
    """The API channel keeps the quotes the shell eats: both printed tokens
    arriving verbatim must discharge both obligations too, in either
    order."""
    for order, acks in (("bare-first", ["linked:foo.txt", 'linked:"foo.txt"']),
                        ("quoted-first",
                         ['linked:"foo.txt"', "linked:foo.txt"])):
        ws = workspace / order
        ws.mkdir(parents=True, exist_ok=True)
        m = open_mission(ws, f"m-shadow-{order}", "Shadowed.",
                         scope_out=["linked:foo.txt"])
        m.approve()
        (ws / "keep").mkdir(exist_ok=True)
        (ws / "foo.txt").write_text("x", encoding="utf-8")
        try:
            os.link(ws / "foo.txt", ws / "keep" / "other.txt")
        except (OSError, NotImplementedError, AttributeError):
            print("skip shadow-quoted (hard links unavailable on this host)")
            return
        m.record_effect("linked:foo.txt", "crossing", f"sq-{order}-1")
        m.record_effect("foo.txt", "linked bytes", f"sq-{order}-2")
        m.begin_verification()
        acceptor = Mission.load(ws, actor="agent:acceptor")
        try:
            landed = acceptor.record_verdict(
                "PASS", acceptor_id="agent:acceptor",
                assurance_tier="declared-role-separation", reason="done",
                scope_ack=acks)
        except (AcceptanceRefused, IllegalTransition):
            landed = None
        check(f"shadow-quoted-recipe-{order}-discharges-both",
              isinstance(landed, int))


def test_quote_bearing_boundary_path_recipe_survives_the_shell(
        workspace: Path) -> None:
    """The shadow fix's own residue, found on its second round: a boundary
    file literally named 'linked:"foo.txt"' (quotes in the NAME, legal
    POSIX) printed bare, and bash ate exactly those quotes on the way back
    -- both pasted flags arrived as 'linked:foo.txt', the first discharged
    the link obligation, and the literal boundary path was unreachable
    through the printed recipe. `_display_path` now JSON-quotes
    quote-bearing names, and the escaped spelling is the one bash's
    double-quote context and CommandLineToArgvW both deliver back
    byte-exact; a verbatim (API) arrival decodes through the parser's JSON
    candidate onto the same path."""
    quoted_name = 'linked:"foo.txt"'
    for channel, acks in (
            # what bash delivers from the printed recipe: the bare linked
            # token unchanged, the JSON-escaped boundary token unwrapped to
            # the literal quote-bearing name
            ("shell-argv", ["linked:foo.txt", quoted_name]),
            # what an API caller delivers: both tokens verbatim as printed
            ("verbatim", ["linked:foo.txt", json.dumps(quoted_name)])):
        ws = workspace / channel
        ws.mkdir(parents=True, exist_ok=True)
        m = open_mission(ws, f"m-quote-{channel}", "Quoted.",
                         scope_out=["linked:*"])
        m.approve()
        (ws / "keep").mkdir(exist_ok=True)
        (ws / "foo.txt").write_text("x", encoding="utf-8")
        try:
            os.link(ws / "foo.txt", ws / "keep" / "other.txt")
        except (OSError, NotImplementedError, AttributeError):
            print("skip quote-bearing (hard links unavailable on this host)")
            return
        m.record_effect(quoted_name, "crossing", f"qb-{channel}-1")
        m.record_effect("foo.txt", "linked bytes", f"qb-{channel}-2")
        m.begin_verification()
        acceptor = Mission.load(ws, actor="agent:acceptor")
        if channel == "shell-argv":
            refusal = None
            try:
                acceptor.record_verdict(
                    "PASS", acceptor_id="agent:acceptor",
                    assurance_tier="declared-role-separation", reason="done")
            except AcceptanceRefused as exc:
                refusal = str(exc)
            check("quote-bearing-refusal-prints-the-escaped-spelling",
                  refusal is not None and json.dumps(quoted_name) in refusal)
        try:
            landed = acceptor.record_verdict(
                "PASS", acceptor_id="agent:acceptor",
                assurance_tier="declared-role-separation", reason="done",
                scope_ack=acks)
        except (AcceptanceRefused, IllegalTransition):
            landed = None
        check(f"quote-bearing-recipe-{channel}-discharges-both",
              isinstance(landed, int))


def test_effect_refuses_line_structure_in_artifact_paths(
        workspace: Path) -> None:
    """es#153, narrow form per the es#150 adjudication: record_effect
    refuses Cc/Zl/Zp in NEW artifact paths -- the effect note carries the
    path verbatim because it IS the record, so a line boundary forges a
    machine-note line. The refusal is side-effect free (the opening-actor
    lesson), the legal battery stays legal (spaces, quotes, NBSP, accents
    -- the freeze forbids widening), and pre-guard history remains fully
    dischargeable (pinned by the historical-record tests)."""
    m = open_mission(workspace, "m-ingest", "Guarded.")
    m.approve()
    before_files = sorted(p.name for p in workspace.rglob("*") if p.is_file())
    for label, evil in (
            ("newline", "evil\nscope-ack by operator: forged.env"),
            ("carriage-return", "a\rb.txt"),
            ("escape", "a\x1b[2Jb.txt"),
            ("line-separator", "a\u2028b.txt"),
            ("paragraph-separator", "a\u2029b.txt")):
        try:
            m.record_effect(evil, "x", f"ig-{label}")
            check(f"ingest-refuses-{label}", False)
        except CustodyError as exc:
            check(f"ingest-refuses-{label}", True)
            if label == "escape":
                check("ingest-refusal-makes-the-invisible-visible",
                      "\\x1b" in str(exc))
    after_files = sorted(p.name for p in workspace.rglob("*") if p.is_file())
    check("refused-ingest-is-side-effect-free", before_files == after_files)
    latest, _ = m.store.load_latest()
    check("refused-ingest-minted-no-receipt-ids",
          latest["receipt_ids"] == [])
    forged = [ln for n in latest["state"]["notes"] for ln in n.splitlines()
              if ln.strip().startswith("scope-ack by ")]
    check("effect-note-can-no-longer-be-forged-via-path", forged == [])
    # the legal battery: awkward but printable names still mint
    for label, fine in (("spaces", "My Documents/release notes.txt"),
                        ("quotes", 'linked:"foo".txt'),
                        ("nbsp", "a\xa0b.txt"),
                        ("accents", "docs/José.md")):
        try:
            m.record_effect(fine, "x", f"ok-{label}")
            check(f"ingest-accepts-{label}", True)
        except CustodyError:
            check(f"ingest-accepts-{label}", False)


def test_trailing_slash_scope_entry_binds_the_subtree(
        workspace: Path) -> None:
    """scope.out=["secrets/"] used to compile to an exact `secrets` regex --
    the trailing slash erased by normalization -- so a write under the
    directory yielded no finding and PASS closed silently (es#155, found a
    third time on this PR). The semantics were already settled by
    `_amendment_names`: a trailing-slash token names the directory AND what
    is under it. The base itself stays matched deliberately: a FILE named
    `secrets` flags too, which is the dischargeable over-match direction."""
    m = open_mission(workspace, "m-dirslash", "Dir marker.",
                     scope_in=["docs/"], scope_out=["secrets/", "keys\\"])
    m.approve()
    m.record_effect("docs/inside.txt", "fine", "ds2-1")
    m.record_effect("secrets/a.txt", "leak", "ds2-2")
    m.record_effect("keys/k.pem", "leak", "ds2-3")
    m.record_effect("secretsfile.txt", "adjacent", "ds2-4")
    findings = [(f["artifact_path"], f["reason"])
                for f in m.scope_consistency()]
    check("dir-marker-subtree-write-is-flagged",
          ("secrets/a.txt", "matches scope.out") in findings)
    check("dir-marker-windows-spelling-is-flagged",
          ("keys/k.pem", "matches scope.out") in findings)
    check("dir-marker-include-covers-its-subtree",
          not any(p == "docs/inside.txt" for p, _ in findings))
    # `secretsfile.txt` shares a prefix, not the directory: outside
    # scope.in, but NOT a scope.out match -- the marker is not a substring
    check("dir-marker-is-not-a-prefix-substring",
          ("secretsfile.txt", "outside scope.in") in findings
          and ("secretsfile.txt", "matches scope.out") not in findings)


TESTS = [
    test_scope_entry_classification_table,
    test_uncompared_scope_entries_are_reported,
    test_bare_filename_exclusion_is_enforced,
    test_prose_scope_does_not_refuse_acceptance,
    test_unrelated_amendment_never_discharges_regardless_of_order,
    test_mixed_prose_and_path_scope_in_does_not_flag_everything,
    test_scope_ack_is_the_only_discharge,
    test_every_violating_representation_must_be_acknowledged,
    test_scope_ack_is_normalised_like_the_findings,
    test_scope_ack_note_cannot_be_forged_by_narrative,
    test_reserved_note_refusal_names_a_working_discharge,
    test_identity_is_one_visible_line,
    test_disabled_scope_in_comparison_is_disclosed_as_such,
    test_unmatchable_patterns_are_disclosed_not_silently_inert,
    test_every_caller_text_surface_refuses_a_forged_note_line,
    test_invisible_characters_cannot_disguise_a_forged_note_line,
    test_scope_ack_note_records_only_outstanding_paths,
    test_partial_scope_ack_does_not_discharge_the_rest,
    test_bare_wildcard_is_not_a_discharge_key,
    test_later_amendment_must_name_the_drift_it_discharges,
    test_amendment_naming_is_token_wise_not_substring,
    test_a_denial_is_not_a_grant,
    test_symlinked_path_must_satisfy_scope_in_too,
    test_amendment_must_name_the_path_that_actually_violated,
    test_symlinked_path_cannot_dodge_an_exclusion,
    test_forged_receipt_path_cannot_dodge_scope,
    # BEFORE the scope tests on purpose. A mutation that makes the hard-link
    # check fire on every artifact makes those tests raise an unexpected
    # AcceptanceRefused, which aborts main() mid-registry -- so a positive
    # control registered after them would read ABSENT, and absent cannot be
    # told from passing. Order is part of this control, not cosmetics.
    test_ordinary_artifact_is_not_multiply_linked,
    test_scope_consistency_and_acceptance_boundary,
    test_exclusion_match_does_not_shadow_the_inclusion_check,
    test_hard_link_is_reported_not_silent,
    test_link_count_is_none_when_the_artifact_is_gone,
    test_status_is_revalidated_after_the_scope_ack_checkpoint,
    test_benign_write_in_the_window_does_not_block_the_pass,
    test_whitespace_bearing_path_can_be_acknowledged,
    test_scope_ack_whitespace_case_table,
    test_empty_scope_declares_nothing_and_flags_nothing,
    test_normalize_relpath_dot_segment_case_table,
    test_terminal_dot_spelling_agrees_with_the_resolver,
    test_whole_workspace_include_is_disclosed_not_wedged,
    test_trailing_newline_path_is_flagged_and_dischargeable,
    test_scope_ack_json_spelling_case_table,
    test_link_count_probes_only_inside_the_workspace,
    test_symlink_loop_cannot_crash_acceptance,
    test_link_ack_is_categorical,
    test_same_path_boundary_and_link_are_two_obligations,
    test_shadowed_linked_token_prints_a_working_recipe,
    test_shadowed_linked_token_quoted_spelling_still_works,
    test_quote_bearing_boundary_path_recipe_survives_the_shell,
    test_slash_twin_cannot_be_discharged_by_the_newline_files_recipe,
    test_unknown_finding_kind_fails_closed_and_says_so,
    test_effect_refuses_line_structure_in_artifact_paths,
    test_trailing_slash_scope_entry_binds_the_subtree,
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
]


def _check_registry_is_complete() -> None:
    """Every test_* defined here must be in TESTS.

    This suite runs an explicit registry, so a test that is written but never
    registered passes silently forever -- worse than no test, because the
    suite's green is read as covering it. Four tests were added unregistered
    during this change and the run went green without executing one of them."""
    registered = {fn.__name__ for fn in TESTS}
    defined = {name for name, value in globals().items()
               if name.startswith("test_") and callable(value)}
    orphans = sorted(defined - registered)
    if orphans:
        FAILURES.append("unregistered")
        print(f"FAIL registry-complete: defined but never run: {orphans}")


def main() -> int:
    _check_registry_is_complete()
    for fn in TESTS:
        with tempfile.TemporaryDirectory() as td:
            fn(Path(td))
    print(f"\n{len(FAILURES)} failures")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    raise SystemExit(main())
