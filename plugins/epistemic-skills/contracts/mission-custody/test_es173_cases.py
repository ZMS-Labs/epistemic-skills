#!/usr/bin/env python3
"""es#173 concurrent missions -- the case tables as an executable spec.

Every test here is one or more rows of the adjudicated design's product
space (docs/design/2026-08-25-es173-concurrent-missions-design.md, Tables
A and B in section 7, plus the section 9 test obligations). The tables are
the spec; this file is the tables made falsifiable. Rows the implementation
does not yet satisfy are listed in XFAIL below and MUST fail until the
implementing commit lands -- an XFAIL row that passes is itself a failure
(the spec would be pinning nothing).

One deliberate departure from the design text, per the verification report
this implementation was ordered to honor: the resume-time sibling receipt
scan ranges over ALL readable sibling mission stores, not only the ACTIVE
ones -- the adjudication ("resume-time scan of sibling receipt stores") and
the gauntlet repair carry no active-only narrowing, and a sibling that
completed between its write and A's resume must still explain the drift.
"""
from __future__ import annotations

import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import custody_mission as cm  # noqa: E402
from custody_mission import (  # noqa: E402
    CustodyError, IllegalTransition, Mission, NoActiveMission,
)
from custody_gate import run_gate  # noqa: E402
from custody_store import MissionStore, sha256_file  # noqa: E402
from verify_mission_custody import validate_record  # noqa: E402

# New names the implementation must provide; resolved lazily so this spec
# can run (and fail where expected) against the pre-change core.
BindingRequired = getattr(cm, "BindingRequired", None)
BindingInvalid = getattr(cm, "BindingInvalid", None)
UnionDegraded = getattr(cm, "UnionDegraded", None)

CLI = ROOT / "custody_cli.py"

FAILURES: list[str] = []

# Rows not yet implemented. Every name here must FAIL when run; the
# implementing commits shrink this set to empty.
XFAIL: set[str] = {
    "test_a1_a3_draft_vs_active_union_membership",
    "test_a2_reopened_never_approved_contributes_nothing",
    "test_a6_a7_terminal_states_binding_invalid",
    "test_a8_unreadable_dir_binding_invalid",
    "test_b4_binding_with_nothing_active",
    "test_b5_b10_open_beside_active_is_legal",
    "test_b8_bound_resolves_to_bound",
    "test_b9_b15_stale_binding_never_falls_through",
    "test_b11_plural_unbound_lifecycle_requires_binding",
    "test_binding_channels_cli_flag_env_precedence",
    "test_missions_list_verb",
    "test_b7_lone_unapproved_draft_contributes_nothing",
    "test_b12_union_names_all_matching_pairs",
    "test_b14_b16_binding_never_changes_exposure",
    "test_b13_effect_union_evaluated_before_write",
    "test_b13_own_guards_gate_own_effect",
    "test_b30_audit_channels_unblockable",
    "test_gate_runs_leave_every_chain_byte_identical",
    "test_b17_open_refuses_unreadable_sibling",
    "test_b22_gate_degraded_union_is_disclosed",
    "test_b23_effect_refuses_union_degraded",
    "test_b21_crossing_writes_side_channel_never_the_chain",
    "test_b26_never_approved_sibling_never_launders",
    "test_b27_no_authorization_amendment_no_downgrade",
    "test_b28_all_three_legs_yield_drift_sibling",
    "test_scan_covers_non_active_siblings",
    "test_b29_sibling_touched_prefix_forgery_refused",
    "test_receipt_at_1_closure_regression",
    "test_scope_overlap_disclosure_deterministic",
}


def check(name: str, cond: bool) -> None:
    if not cond:
        FAILURES.append(name)
        print(f"FAIL {name}")
        if "PYTEST_CURRENT_TEST" in os.environ:
            raise AssertionError(f"es173 case check failed: {name}")
    else:
        print(f"ok   {name}")


def open_mission(workspace: Path, mission_id: str, instruction: str = "i",
                 actor: str = "agent:worker", **kwargs) -> Mission:
    return Mission.open(
        workspace, mission_id=mission_id, instruction=instruction,
        operator_ref="operator:zach", steward_ref="agent:worker",
        required_tier="declared-role-separation", actor=actor, **kwargs)


def load_bound(workspace: Path, mission_id: str,
               actor: str = "agent:worker") -> Mission:
    return Mission.load(workspace, actor=actor, mission_id=mission_id)


def guard(name: str, globs: list[str], tools: list[str] | None = None,
          regexes: list[str] | None = None) -> dict:
    return {"name": name, "tool_names": tools or ["Write"],
            "command_regexes": regexes or [], "path_globs": globs}


def corrupt_dir(workspace: Path, name: str) -> Path:
    """Plant a mission dir whose latest checkpoint cannot be loaded."""
    src = None
    for d in sorted((workspace / "missions").iterdir()):
        if d.is_dir():
            src = d
            break
    target = workspace / "missions" / name
    if src is not None and src.name != name:
        shutil.copytree(src, target)
    else:
        (target / "checkpoints").mkdir(parents=True)
    tail = sorted((target / "checkpoints").glob("r*.json"))
    if tail:
        tail[-1].write_text("{not json", encoding="utf-8")
    else:
        (target / "checkpoints" / "r00000001.json").write_text(
            "{not json", encoding="utf-8")
    return target


def chain_bytes(workspace: Path, mission: str) -> list[bytes]:
    return [p.read_bytes() for p in sorted(
        (workspace / "missions" / mission / "checkpoints").glob("r*.json"))]


def run_cli(args: list[str], *, env_extra: dict | None = None,
            stdin: str | None = None) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env.pop("ZMS_MISSION_ID", None)
    env["PYTHONIOENCODING"] = "utf-8"
    if env_extra:
        env.update(env_extra)
    return subprocess.run([sys.executable, str(CLI)] + args, env=env,
                          input=stdin, capture_output=True, text=True)


# ---------------------------------------------------------------------------
# Table A -- mission status x discovery x binding x union (guard-source)
# ---------------------------------------------------------------------------

def test_a1_a3_draft_vs_active_union_membership(workspace: Path) -> None:
    """A1 + A3 + B24/B25 mirror: the SAME armed guard contributes nothing
    while its mission is a never-approved draft, and blocks the moment
    approve() lands. Approval is the arming event (OD-4)."""
    g = [guard("no-secrets", ["secrets/**"], tools=["Write"])]
    open_mission(workspace, "m-draft", guard_mode="enforce",
                 actuator_guards=g)
    call = {"tool_name": "Write", "command": None,
            "file_path": "secrets/x.env"}
    v = run_gate(workspace, call, actor="hook:test")
    check("A1-draft-guards-not-in-union", v["decision"] == "allow")
    load_bound(workspace, "m-draft").approve()
    v2 = run_gate(workspace, call, actor="hook:test")
    check("A3-approved-guards-arm-union", v2["decision"] == "block")
    check("B25-block-names-mission-and-rule",
          "m-draft" in v2["reason"] and "no-secrets" in v2["reason"])


def test_a2_reopened_never_approved_contributes_nothing(workspace: Path) -> None:
    """A2: a never-approved mission wedged in `reopened` (drift on a draft)
    must not arm the union -- the chain test, not latest status, decides
    (OD-4 / FATAL-3 leg 2 share this discriminator)."""
    g = [guard("no-secrets", ["secrets/**"], tools=["Write"])]
    m = open_mission(workspace, "m-re", guard_mode="enforce",
                     actuator_guards=g)
    m.record_effect("a.txt", "aa", "req-1")  # legal in draft
    (workspace / "a.txt").write_text("tampered", encoding="utf-8")
    m.resume()  # draft -> reopened, never approved
    check("A2-setup-reopened",
          m.store.load_latest()[0]["status"] == "reopened")
    call = {"tool_name": "Write", "command": None,
            "file_path": "secrets/x.env"}
    v = run_gate(workspace, call, actor="hook:test")
    check("A2-never-approved-reopened-not-in-union",
          v["decision"] == "allow")


def test_a4_reopened_approved_lineage_stays_armed(workspace: Path) -> None:
    g = [guard("no-secrets", ["secrets/**"], tools=["Write"])]
    m = open_mission(workspace, "m-re-appr", guard_mode="enforce",
                     actuator_guards=g)
    m.approve()
    m.record_effect("a.txt", "aa", "req-1")
    (workspace / "a.txt").write_text("tampered", encoding="utf-8")
    m.resume()
    check("A4-setup-reopened",
          m.store.load_latest()[0]["status"] == "reopened")
    v = run_gate(workspace, {"tool_name": "Write", "command": None,
                             "file_path": "secrets/x.env"},
                 actor="hook:test")
    check("A4-approved-reopened-still-armed", v["decision"] == "block")


def test_a5_verifying_guards_keep_binding_effect_illegal(workspace: Path) -> None:
    g = [guard("no-secrets", ["secrets/**"], tools=["Write"])]
    m = open_mission(workspace, "m-ver", guard_mode="enforce",
                     actuator_guards=g)
    m.approve()
    m.begin_verification()
    v = run_gate(workspace, {"tool_name": "Write", "command": None,
                             "file_path": "secrets/x.env"},
                 actor="hook:test")
    check("A5-verifying-guards-still-armed", v["decision"] == "block")
    try:
        m.record_effect("b.txt", "bb", "req-2")
        check("A5-effect-illegal-in-verifying", False)
    except IllegalTransition:
        check("A5-effect-illegal-in-verifying", True)


def test_a6_a7_terminal_states_binding_invalid(workspace: Path) -> None:
    m = open_mission(workspace, "m-done")
    m.approve()
    m.begin_verification()
    acceptor = Mission.load(workspace, actor="agent:acceptor")
    acceptor.record_verdict("PASS", acceptor_id="agent:acceptor",
                            assurance_tier="declared-role-separation",
                            reason="done")
    try:
        load_bound(workspace, "m-done")
        check("A6-bound-to-completed-refused", False)
    except Exception as exc:
        check("A6-bound-to-completed-refused",
              BindingInvalid is not None and isinstance(exc, BindingInvalid)
              and "completed" in str(exc))
    c = open_mission(workspace, "m-gone")
    c.cancel("abandoned")
    try:
        load_bound(workspace, "m-gone")
        check("A7-bound-to-cancelled-refused", False)
    except Exception as exc:
        check("A7-bound-to-cancelled-refused",
              BindingInvalid is not None and isinstance(exc, BindingInvalid)
              and "cancelled" in str(exc))


def test_a8_unreadable_dir_binding_invalid(workspace: Path) -> None:
    open_mission(workspace, "m-live").approve()
    corrupt_dir(workspace, "m-corrupt")
    try:
        with contextlib.redirect_stderr(io.StringIO()):
            load_bound(workspace, "m-corrupt")
        check("A8-bound-to-unreadable-refused", False)
    except Exception as exc:
        check("A8-bound-to-unreadable-refused",
              BindingInvalid is not None and isinstance(exc, BindingInvalid))


def test_b4_binding_with_nothing_active(workspace: Path) -> None:
    """Row 4: a binding naming a mission in an empty workspace is
    BindingInvalid -- never silently unbound."""
    try:
        load_bound(workspace, "m-ghost")
        check("B4-binding-nothing-active-refused", False)
    except Exception as exc:
        check("B4-binding-nothing-active-refused",
              BindingInvalid is not None and isinstance(exc, BindingInvalid))


# ---------------------------------------------------------------------------
# Table B -- binding mechanics (rows 1, 2, 5, 6, 8, 9, 10, 11, 15)
# ---------------------------------------------------------------------------

def test_b1_b2_zero_active_unchanged(workspace: Path) -> None:
    try:
        Mission.load(workspace, actor="agent:x")
        check("B2-zero-active-lifecycle-refuses", False)
    except NoActiveMission:
        check("B2-zero-active-lifecycle-refuses", True)
    m = open_mission(workspace, "m-first")
    check("B1-open-yields-draft",
          m.store.load_latest()[0]["status"] == "draft")


def test_b5_b10_open_beside_active_is_legal(workspace: Path) -> None:
    """Rows 5 and 10: plurality is legal -- open no longer refuses on an
    existing active mission, and the new mission is a union-inert draft."""
    open_mission(workspace, "m-one").approve()
    second = open_mission(workspace, "m-two")
    check("B5-second-open-succeeds",
          second.store.load_latest()[0]["status"] == "draft")
    third = open_mission(workspace, "m-three")
    check("B10-nth-open-succeeds",
          third.store.load_latest()[0]["status"] == "draft")


def test_b6_single_active_unbound_flow_preserved(workspace: Path) -> None:
    """Row 6: the single-mission workflow must not grow ceremony."""
    m = open_mission(workspace, "m-solo")
    m.approve()
    loaded = Mission.load(workspace, actor="agent:worker")
    check("B6-unbound-resolves-to-the-one-active",
          loaded.store.mission_dir.name == "m-solo")


def test_b8_bound_resolves_to_bound(workspace: Path) -> None:
    open_mission(workspace, "m-solo").approve()
    loaded = load_bound(workspace, "m-solo")
    check("B8-bound-same-as-unbound-when-ids-coincide",
          loaded.store.mission_dir.name == "m-solo")


def test_b9_b15_stale_binding_never_falls_through(workspace: Path) -> None:
    open_mission(workspace, "m-one").approve()
    try:
        load_bound(workspace, "m-nonexistent")
        check("B9-stale-binding-no-fallback-to-the-one-active", False)
    except Exception as exc:
        check("B9-stale-binding-no-fallback-to-the-one-active",
              BindingInvalid is not None and isinstance(exc, BindingInvalid))
    open_mission(workspace, "m-two")
    try:
        load_bound(workspace, "m-nonexistent")
        check("B15-stale-binding-no-fallback-to-union", False)
    except Exception as exc:
        check("B15-stale-binding-no-fallback-to-union",
              BindingInvalid is not None and isinstance(exc, BindingInvalid))


def test_b11_plural_unbound_lifecycle_requires_binding(workspace: Path) -> None:
    open_mission(workspace, "m-one").approve()
    open_mission(workspace, "m-two")
    try:
        Mission.load(workspace, actor="agent:worker")
        check("B11-plural-unbound-refuses", False)
    except Exception as exc:
        ok = (BindingRequired is not None
              and isinstance(exc, BindingRequired))
        check("B11-plural-unbound-refuses", ok)
        if ok:
            msg = str(exc)
            check("B11-refusal-lists-ids",
                  "m-one" in msg and "m-two" in msg)
            check("B11-refusal-names-channels",
                  "--mission" in msg and "ZMS_MISSION_ID" in msg)


def test_binding_channels_cli_flag_env_precedence(workspace: Path) -> None:
    """Section 1: flag > env > unbound, on the CLI surface."""
    ws = str(workspace)
    r = run_cli(["open", "--workspace", ws, "--actor", "agent:t",
                 "--mission-id", "m-a", "--instruction", "i",
                 "--operator", "operator:t", "--steward", "agent:t"])
    check("cli-open-a", r.returncode == 0)
    check("cli-open-prints-binding-line", "ZMS_MISSION_ID=m-a" in
          (r.stdout + r.stderr))
    r = run_cli(["open", "--workspace", ws, "--actor", "agent:t",
                 "--mission-id", "m-b", "--instruction", "i",
                 "--operator", "operator:t", "--steward", "agent:t"])
    check("cli-open-b", r.returncode == 0)
    # unbound with two active: refusal
    r = run_cli(["note", "--workspace", ws, "--actor", "agent:t",
                 "--text", "x"])
    check("cli-plural-unbound-note-refuses", r.returncode == 2)
    # env binds
    r = run_cli(["note", "--workspace", ws, "--actor", "agent:t",
                 "--text", "via-env"], env_extra={"ZMS_MISSION_ID": "m-a"})
    check("cli-env-binding-works", r.returncode == 0)
    # flag beats env
    r = run_cli(["note", "--workspace", ws, "--actor", "agent:t",
                 "--text", "via-flag", "--mission", "m-b"],
                env_extra={"ZMS_MISSION_ID": "m-a"})
    check("cli-flag-beats-env", r.returncode == 0)
    got_a = json.loads(run_cli(
        ["status", "--workspace", ws, "--actor", "agent:t",
         "--mission", "m-a"]).stdout)
    got_b = json.loads(run_cli(
        ["status", "--workspace", ws, "--actor", "agent:t",
         "--mission", "m-b"]).stdout)
    check("cli-notes-landed-by-binding",
          "via-env" in got_a["state"]["notes"]
          and "via-flag" in got_b["state"]["notes"]
          and "via-flag" not in got_a["state"]["notes"])


def test_missions_list_verb(workspace: Path) -> None:
    """Section 6: plurality needs an enumeration verb."""
    open_mission(workspace, "m-one").approve()
    open_mission(workspace, "m-two")
    r = run_cli(["missions", "--workspace", str(workspace),
                 "--actor", "agent:t"])
    check("cli-missions-exit-0", r.returncode == 0)
    if r.returncode == 0:
        rows = json.loads(r.stdout)
        by_id = {row["mission"]: row for row in rows}
        check("cli-missions-lists-both",
              set(by_id) >= {"m-one", "m-two"})
        check("cli-missions-approved-flag",
              by_id.get("m-one", {}).get("approved") is True
              and by_id.get("m-two", {}).get("approved") is False)
        check("cli-missions-carries-status-steward-frontier",
              all(k in by_id.get("m-one", {})
                  for k in ("status", "steward_ref", "frontier")))


# ---------------------------------------------------------------------------
# Union guard evaluation (rows 7, 12, 13, 14, 16, 24, 25, 30 + section 9)
# ---------------------------------------------------------------------------

def test_b7_lone_unapproved_draft_contributes_nothing(workspace: Path) -> None:
    g = [guard("no-secrets", ["secrets/**"], tools=["Write"])]
    open_mission(workspace, "m-draft", guard_mode="enforce",
                 actuator_guards=g)
    v = run_gate(workspace, {"tool_name": "Write", "command": None,
                             "file_path": "secrets/x.env"},
                 actor="hook:test")
    check("B7-lone-draft-allows", v["decision"] == "allow")


def test_b12_union_names_all_matching_pairs(workspace: Path) -> None:
    """Row 12: a call matching guards in TWO approved missions is blocked
    naming every (mission, rule) pair -- the operator needs the full bill."""
    open_mission(workspace, "m-a", guard_mode="enforce",
                 actuator_guards=[guard("rule-a", ["shared/**"],
                                        tools=["Write"])]).approve()
    open_mission(workspace, "m-b", guard_mode="enforce",
                 actuator_guards=[guard("rule-b", ["shared/**"],
                                        tools=["Write"])]).approve()
    v = run_gate(workspace, {"tool_name": "Write", "command": None,
                             "file_path": "shared/f.txt"},
                 actor="hook:test")
    check("B12-union-blocks", v["decision"] == "block")
    check("B12-names-all-pairs",
          all(t in v["reason"] for t in ("m-a", "rule-a", "m-b", "rule-b")))
    for mid in ("m-a", "m-b"):
        log = workspace / "missions" / mid / "guard-log.jsonl"
        check(f"B12-guard-log-appended-{mid}", log.exists())


def test_b14_b16_binding_never_changes_exposure(workspace: Path) -> None:
    """Rows 14/16 + the section 9 adversarial exposure test: a session bound
    to mission A attempting an actuator guarded ONLY by approved sibling B
    MUST be blocked (OD-1); a bad binding still gets the union."""
    open_mission(workspace, "m-a").approve()
    open_mission(workspace, "m-b", guard_mode="enforce",
                 actuator_guards=[guard("b-only", ["frozen/**"],
                                        tools=["Write"])]).approve()
    call = {"tool_name": "Write", "command": None,
            "file_path": "frozen/f.txt"}
    v = run_gate(workspace, call, actor="hook:test")
    check("B14-union-regardless-of-binding", v["decision"] == "block")
    # CLI: gate bound to m-a is still blocked by m-b's guard
    r = run_cli(["gate", "--workspace", str(workspace), "--actor", "hook:t",
                 "--mission", "m-a"], stdin=json.dumps(call))
    check("B14-cli-bound-gate-still-blocked", r.returncode == 2)
    # bad binding: union still evaluated, block stands (row 16)
    r = run_cli(["gate", "--workspace", str(workspace), "--actor", "hook:t",
                 "--mission", "m-ghost"], stdin=json.dumps(call))
    check("B16-bad-binding-gate-still-union", r.returncode == 2)


def test_b13_effect_union_evaluated_before_write(workspace: Path) -> None:
    """Row 13 + OD-2: effect IS the file write, union-evaluated BEFORE
    _write_effect; a block is side-effect-free -- no bytes, no receipt."""
    open_mission(workspace, "m-guard", guard_mode="enforce",
                 actuator_guards=[guard("no-frozen", ["frozen/**"],
                                        tools=["Write"])]).approve()
    b = open_mission(workspace, "m-writer")
    b.approve()
    b = load_bound(workspace, "m-writer")
    try:
        b.record_effect("frozen/f.txt", "content", "req-1")
        check("B13-effect-blocked", False)
    except CustodyError as exc:
        check("B13-effect-blocked", not isinstance(exc, IllegalTransition))
        check("B13-block-names-pair",
              "m-guard" in str(exc) and "no-frozen" in str(exc))
    check("B13-no-bytes-written",
          not (workspace / "frozen" / "f.txt").exists())
    check("B13-no-receipt-minted",
          not b.store.receipt_path("req-1").exists())
    check("B13-request-id-still-fresh",
          "req-1" not in b.store.load_latest()[0]["receipt_ids"])


def test_b13_own_guards_gate_own_effect(workspace: Path) -> None:
    """Union includes the acting mission itself once approved: complete
    mediation for actuation has no self-exemption."""
    m = open_mission(workspace, "m-self", guard_mode="enforce",
                     actuator_guards=[guard("self-frozen", ["frozen/**"],
                                            tools=["Write"])])
    m.approve()
    try:
        m.record_effect("frozen/own.txt", "x", "req-1")
        check("B13-own-guard-gates-own-effect", False)
    except CustodyError:
        check("B13-own-guard-gates-own-effect", True)


def test_b30_audit_channels_unblockable(workspace: Path) -> None:
    """Row 30 + OD-2 paired test: the same union guard that blocks effect
    leaves note, amend, and frontier recorded on the same surface."""
    open_mission(workspace, "m-guard", guard_mode="enforce",
                 actuator_guards=[guard("no-frozen", ["frozen/**"],
                                        tools=["Write"])]).approve()
    b = open_mission(workspace, "m-writer")
    b.approve()
    b = load_bound(workspace, "m-writer")
    try:
        b.record_effect("frozen/f.txt", "content", "req-1")
        check("B30-effect-blocked-for-contrast", False)
    except CustodyError:
        check("B30-effect-blocked-for-contrast", True)
    check("B30-note-recorded", isinstance(
        b.note("blocked on frozen/f.txt; escalating"), int))
    check("B30-amend-recorded", isinstance(
        b.amend_authority("operator: granted frozen/f.txt to m-writer"), int))
    check("B30-frontier-recorded", isinstance(
        b.set_frontier("await operator on frozen/"), int))


def test_gate_runs_leave_every_chain_byte_identical(workspace: Path) -> None:
    """Section 9: byte-identity of gate runs under N missions."""
    open_mission(workspace, "m-a", guard_mode="enforce",
                 actuator_guards=[guard("rule-a", ["shared/**"],
                                        tools=["Write"])]).approve()
    open_mission(workspace, "m-b", guard_mode="audit",
                 actuator_guards=[guard("rule-b", ["shared/**"],
                                        tools=["Write"])]).approve()
    before = {m: chain_bytes(workspace, m) for m in ("m-a", "m-b")}
    run_gate(workspace, {"tool_name": "Write", "command": None,
                         "file_path": "shared/f.txt"}, actor="hook:test")
    after = {m: chain_bytes(workspace, m) for m in ("m-a", "m-b")}
    check("gate-chains-byte-identical", before == after)


# ---------------------------------------------------------------------------
# Degraded stores (rows 17, 18, 22, 23)
# ---------------------------------------------------------------------------

def test_b17_open_refuses_unreadable_sibling(workspace: Path) -> None:
    open_mission(workspace, "m-live").approve()
    corrupt_dir(workspace, "m-corrupt")
    with contextlib.redirect_stderr(io.StringIO()):
        try:
            open_mission(workspace, "m-new")
            check("B17-open-refuses-unreadable-sibling", False)
        except CustodyError:
            check("B17-open-refuses-unreadable-sibling", True)
        check("B17-refused-open-left-no-dir",
              not (workspace / "missions" / "m-new").exists())
        # acknowledged: open proceeds and records the acknowledgement
        m = open_mission(workspace, "m-new",
                         acknowledge_unreadable=["m-corrupt"])
    notes = m.store.load_latest()[0]["state"]["notes"]
    check("B17-acknowledgement-recorded-in-opening-checkpoint",
          any("m-corrupt" in n for n in notes))


def test_b22_gate_degraded_union_is_disclosed(workspace: Path) -> None:
    """Row 22: hook path stays fail-open, but the verdict reason AND stderr
    must name the skipped sibling and say its guards are NOT enforced."""
    open_mission(workspace, "m-live").approve()
    corrupt_dir(workspace, "m-corrupt")
    buf = io.StringIO()
    with contextlib.redirect_stderr(buf):
        v = run_gate(workspace, {"tool_name": "Bash", "command": "ls",
                                 "file_path": None}, actor="hook:test")
    check("B22-gate-still-allows", v["decision"] == "allow")
    check("B22-reason-names-degradation",
          "m-corrupt" in v["reason"] and "NOT enforced" in v["reason"])
    check("B22-stderr-names-degradation", "m-corrupt" in buf.getvalue())


def test_b23_effect_refuses_union_degraded(workspace: Path) -> None:
    """Row 23: effect CAN refuse without bricking anything, so it does."""
    m = open_mission(workspace, "m-live")
    m.approve()
    corrupt_dir(workspace, "m-corrupt")
    with contextlib.redirect_stderr(io.StringIO()):
        try:
            m.record_effect("a.txt", "aa", "req-1")
            check("B23-effect-refuses-degraded", False)
        except Exception as exc:
            check("B23-effect-refuses-degraded",
                  UnionDegraded is not None and isinstance(exc, UnionDegraded)
                  and "m-corrupt" in str(exc))
        check("B23-refused-effect-wrote-nothing",
              not (workspace / "a.txt").exists())
        # recorded acknowledgement lets work continue, and persists
        m.record_effect("a.txt", "aa", "req-1",
                        acknowledge_unreadable=["m-corrupt"])
        check("B23-acknowledged-effect-proceeds",
              (workspace / "a.txt").exists())
        m2 = Mission.load(workspace, actor="agent:worker",
                          mission_id="m-live")
        m2.record_effect("b.txt", "bb", "req-2")
        check("B23-acknowledgement-persists-in-chain",
              (workspace / "b.txt").exists())


def test_b18_open_refuses_epoch_skew_sibling(workspace: Path) -> None:
    m = open_mission(workspace, "m-old")
    m.approve()
    m.begin_verification()
    acceptor = Mission.load(workspace, actor="agent:acceptor")
    acceptor.record_verdict("PASS", acceptor_id="agent:acceptor",
                            assurance_tier="declared-role-separation",
                            reason="done")
    # relabel the tail to a future epoch: the store CLAIMS a newer contract
    tail = sorted((workspace / "missions" / "m-old" / "checkpoints")
                  .glob("r*.json"))[-1]
    rec = json.loads(tail.read_text(encoding="utf-8"))
    rec["record"] = "checkpoint@99"
    tail.write_text(json.dumps(rec), encoding="utf-8")
    with contextlib.redirect_stderr(io.StringIO()):
        try:
            open_mission(workspace, "m-new")
            check("B18-open-refuses-epoch-skew", False)
        except CustodyError:
            check("B18-open-refuses-epoch-skew", True)


# ---------------------------------------------------------------------------
# Sibling crossings (rows 19, 21, 26, 27, 28, 29 + section 9)
# ---------------------------------------------------------------------------

def _two_missions_one_artifact(workspace: Path) -> tuple[Mission, Mission]:
    """A receipts shared.txt; returns (A, B) both approved and bound."""
    a = open_mission(workspace, "m-alpha")
    a.approve()
    a = load_bound(workspace, "m-alpha")
    a.record_effect("shared.txt", "alpha-1", "req-a1")
    b = open_mission(workspace, "m-beta", actor="agent:other")
    b.approve()
    b = load_bound(workspace, "m-beta", actor="agent:other")
    return a, b


def test_b21_crossing_writes_side_channel_never_the_chain(workspace: Path) -> None:
    """Row 21 + FATAL-4 + section 9 byte-identity: B's effect on a path A
    receipted appends one advisory JSONL line to A's sibling-touch.jsonl;
    A's checkpoint chain stays byte-identical."""
    a, b = _two_missions_one_artifact(workspace)
    before = chain_bytes(workspace, "m-alpha")
    receipt = b.record_effect("shared.txt", "beta-1", "req-b1")
    check("B21-effect-succeeded", receipt["after_sha256"] is not None)
    check("B21-sibling-chain-byte-identical",
          chain_bytes(workspace, "m-alpha") == before)
    side = workspace / "missions" / "m-alpha" / "sibling-touch.jsonl"
    check("B21-side-channel-written", side.exists())
    if side.exists():
        entry = json.loads(side.read_text(encoding="utf-8").splitlines()[-1])
        check("B21-entry-fields",
              entry.get("from_mission") == "m-beta"
              and entry.get("receipt_id") == "req-b1"
              and entry.get("artifact_path") == "shared.txt"
              and set(entry) >= {"utc", "actor", "session_id",
                                 "after_sha256"})


def test_b26_never_approved_sibling_never_launders(workspace: Path) -> None:
    """Row 26 + the FATAL-3 laundering test, never-approved leg: an
    adversary opens a throwaway sibling, effects the tampered bytes, and A's
    resume must report plain drift -- no DRIFT-SIBLING."""
    a, _ = _two_missions_one_artifact(workspace)
    evil = open_mission(workspace, "m-evil", actor="agent:evil")
    evil = load_bound(workspace, "m-evil", actor="agent:evil")
    evil.record_effect("shared.txt", "tampered", "req-e1")  # legal in draft
    a = load_bound(workspace, "m-alpha")
    findings = a.resume()
    check("B26-plain-drift-not-sibling",
          findings == ["shared.txt"])
    latest = a.store.load_latest()[0]
    check("B26-reconciliation-marker",
          "RECONCILIATION:shared.txt" in latest["state"]["unresolved_verdicts"])
    check("B26-evidence-reported",
          any("m-evil" in n and "req-e1" in n
              for n in latest["state"]["notes"]))


def test_b27_no_authorization_amendment_no_downgrade(workspace: Path) -> None:
    """Row 27: hash match + approved sibling, but no cross-mission
    authorization amendment in A's own chain -> plain drift + evidence."""
    a, b = _two_missions_one_artifact(workspace)
    b.record_effect("shared.txt", "beta-1", "req-b1")
    a = load_bound(workspace, "m-alpha")
    findings = a.resume()
    check("B27-plain-drift-not-sibling", findings == ["shared.txt"])
    latest = a.store.load_latest()[0]
    check("B27-evidence-reported",
          any("m-beta" in n and "req-b1" in n
              for n in latest["state"]["notes"]))


def test_b28_all_three_legs_yield_drift_sibling(workspace: Path) -> None:
    """Row 28: hash match + approved sibling + authorization amendment in
    A's chain -> DRIFT-SIBLING, reconciled by acknowledgement with the
    machine note, written by A's own bound session."""
    a, b = _two_missions_one_artifact(workspace)
    a.amend_authority("operator: mission m-beta is authorized to write "
                      "shared.txt during the overlap")
    b.record_effect("shared.txt", "beta-1", "req-b1")
    a = load_bound(workspace, "m-alpha")
    findings = a.resume()
    check("B28-drift-sibling-classified",
          findings == ["DRIFT-SIBLING:shared.txt"])
    latest = a.store.load_latest()[0]
    check("B28-marker-raised",
          "DRIFT-SIBLING:shared.txt" in latest["state"]["unresolved_verdicts"])
    check("B28-note-names-mission-and-receipt",
          any("m-beta" in n and "req-b1" in n
              for n in latest["state"]["notes"]))
    rev = a.acknowledge_sibling("shared.txt")
    check("B28-acknowledge-returns-revision", isinstance(rev, int))
    latest = a.store.load_latest()[0]
    check("B28-marker-cleared",
          latest["state"]["unresolved_verdicts"] == [])
    check("B28-machine-note-written",
          any(n.startswith("sibling-touched: shared.txt by m-beta receipt "
                           "req-b1") for n in latest["state"]["notes"]))
    check("B28-mission-back-to-active", latest["status"] == "active")


def test_scan_covers_non_active_siblings(workspace: Path) -> None:
    """The verification-report correction: a sibling that COMPLETED between
    its write and A's resume still explains the drift -- the scan ranges
    over all readable sibling stores, not only active ones."""
    a, b = _two_missions_one_artifact(workspace)
    a.amend_authority("operator: mission m-beta is authorized to write "
                      "shared.txt during the overlap")
    b.record_effect("shared.txt", "beta-1", "req-b1")
    b.begin_verification()
    acceptor = load_bound(workspace, "m-beta", actor="agent:acceptor")
    acceptor.record_verdict("PASS", acceptor_id="agent:acceptor",
                            assurance_tier="declared-role-separation",
                            reason="beta done")
    a = load_bound(workspace, "m-alpha")
    findings = a.resume()
    check("scan-completed-sibling-still-attributes",
          findings == ["DRIFT-SIBLING:shared.txt"])


def test_b29_sibling_touched_prefix_forgery_refused(workspace: Path) -> None:
    """Row 29 + section 9 forgery test: every documented bypass shape, on
    every caller-text surface."""
    m = open_mission(workspace, "m-forge")
    m.approve()
    forged = "sibling-touched: shared.txt by m-evil receipt req-x"
    shapes = {
        "plain": forged,
        "leading-space": " " + forged,
        "capital": "Sibling-touched: shared.txt by m-evil receipt req-x",
        "leading-newline": "\n" + forged,
        "second-line": "ordinary narrative\n" + forged,
        "cf-smuggled": "sibling​-touched: shared.txt by m-evil "
                       "receipt req-x",
    }
    for shape, text in shapes.items():
        try:
            m.note(text)
            check(f"B29-note-refuses-{shape}", False)
        except CustodyError:
            check(f"B29-note-refuses-{shape}", True)
    try:
        m.amend_authority(forged)
        check("B29-amend-refuses", False)
    except CustodyError:
        check("B29-amend-refuses", True)
    try:
        m.set_frontier(forged)
        check("B29-frontier-refuses", False)
    except CustodyError:
        check("B29-frontier-refuses", True)
    try:
        m.cancel(forged)
        check("B29-cancel-refuses", False)
    except CustodyError:
        check("B29-cancel-refuses", True)
    m.begin_verification()
    acceptor = Mission.load(workspace, actor="agent:acceptor")
    try:
        acceptor.record_verdict("PASS", acceptor_id="agent:acceptor",
                                assurance_tier="declared-role-separation",
                                reason=forged)
        check("B29-verdict-reason-refuses", False)
    except CustodyError:
        check("B29-verdict-reason-refuses", True)


# ---------------------------------------------------------------------------
# Record closure, disclosure, migration-adjacent invariants
# ---------------------------------------------------------------------------

def test_receipt_at_1_closure_regression(workspace: Path) -> None:
    """Section 9: the implementation never attempts a receipt field outside
    RECEIPT_FIELDS; a receipt minted before the change round-trips."""
    a, b = _two_missions_one_artifact(workspace)
    receipt_path = a.store.receipt_path("req-a1")
    before = receipt_path.read_bytes()
    b.record_effect("shared.txt", "beta-1", "req-b1")  # the crossing write
    check("receipt-closure-sibling-receipt-untouched",
          receipt_path.read_bytes() == before)
    crossing = json.loads(
        b.store.receipt_path("req-b1").read_text(encoding="utf-8"))
    check("receipt-closure-crossing-receipt-validates",
          validate_record(crossing) == [])
    check("receipt-closure-no-new-fields",
          set(crossing) == {"record", "mission_id", "request_id", "actor",
                            "utc", "artifact_path", "before_sha256",
                            "after_sha256"})


def test_scope_overlap_disclosure_deterministic(workspace: Path) -> None:
    """Section 3 + section 9: overlapping scope.in patterns are disclosed
    and recorded at open, deterministically; prose is incomparable."""
    def build(ws: Path) -> list[str]:
        open_mission(ws, "m-one", scope_in=["docs/**", "media acquisition"])\
            .approve()
        m = open_mission(ws, "m-two", scope_in=["docs/plans/*.md"])
        return [n for n in m.store.load_latest()[0]["state"]["notes"]
                if "overlap" in n or "incomparable" in n]
    ws1 = workspace / "w1"
    ws2 = workspace / "w2"
    notes1 = build(ws1)
    notes2 = build(ws2)
    check("overlap-disclosed", any("m-one" in n and "docs/**" in n
                                   for n in notes1))
    check("overlap-deterministic", notes1 == notes2)
    ws3 = workspace / "w3"
    open_mission(ws3, "m-one", scope_in=["src/**"]).approve()
    m = open_mission(ws3, "m-disjoint", scope_in=["docs/**"])
    check("no-false-overlap",
          not any("overlap" in n
                  for n in m.store.load_latest()[0]["state"]["notes"]))


def test_open_still_refuses_duplicate_mission_id(workspace: Path) -> None:
    open_mission(workspace, "m-dup")
    try:
        open_mission(workspace, "m-dup")
        check("open-refuses-duplicate-id", False)
    except (CustodyError, Exception):
        check("open-refuses-duplicate-id", True)
    # exactly one r1 checkpoint exists
    cps = sorted((workspace / "missions" / "m-dup" / "checkpoints")
                 .glob("r*.json"))
    check("duplicate-open-wrote-nothing", len(cps) == 1)


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

TESTS = [
    test_a1_a3_draft_vs_active_union_membership,
    test_a2_reopened_never_approved_contributes_nothing,
    test_a4_reopened_approved_lineage_stays_armed,
    test_a5_verifying_guards_keep_binding_effect_illegal,
    test_a6_a7_terminal_states_binding_invalid,
    test_a8_unreadable_dir_binding_invalid,
    test_b4_binding_with_nothing_active,
    test_b1_b2_zero_active_unchanged,
    test_b5_b10_open_beside_active_is_legal,
    test_b6_single_active_unbound_flow_preserved,
    test_b8_bound_resolves_to_bound,
    test_b9_b15_stale_binding_never_falls_through,
    test_b11_plural_unbound_lifecycle_requires_binding,
    test_binding_channels_cli_flag_env_precedence,
    test_missions_list_verb,
    test_b7_lone_unapproved_draft_contributes_nothing,
    test_b12_union_names_all_matching_pairs,
    test_b14_b16_binding_never_changes_exposure,
    test_b13_effect_union_evaluated_before_write,
    test_b13_own_guards_gate_own_effect,
    test_b30_audit_channels_unblockable,
    test_gate_runs_leave_every_chain_byte_identical,
    test_b17_open_refuses_unreadable_sibling,
    test_b22_gate_degraded_union_is_disclosed,
    test_b23_effect_refuses_union_degraded,
    test_b18_open_refuses_epoch_skew_sibling,
    test_b21_crossing_writes_side_channel_never_the_chain,
    test_b26_never_approved_sibling_never_launders,
    test_b27_no_authorization_amendment_no_downgrade,
    test_b28_all_three_legs_yield_drift_sibling,
    test_scan_covers_non_active_siblings,
    test_b29_sibling_touched_prefix_forgery_refused,
    test_receipt_at_1_closure_regression,
    test_scope_overlap_disclosure_deterministic,
    test_open_still_refuses_duplicate_mission_id,
]


def _check_registry_is_complete() -> None:
    registered = {fn.__name__ for fn in TESTS}
    defined = {name for name, value in globals().items()
               if name.startswith("test_") and callable(value)}
    orphans = sorted(defined - registered)
    if orphans:
        FAILURES.append("unregistered")
        print(f"FAIL registry-complete: defined but never run: {orphans}")


def _run(fn) -> None:
    before = len(FAILURES)
    err: Exception | None = None
    try:
        with tempfile.TemporaryDirectory() as td:
            fn(Path(td))
    except Exception as exc:  # noqa: BLE001
        err = exc
    failed = len(FAILURES) > before or err is not None
    if fn.__name__ in XFAIL:
        # Expected to fail until the implementing commit lands. The recorded
        # failures are rolled back; an unexpected PASS is itself a failure,
        # because a green row that is still listed here pins nothing.
        del FAILURES[before:]
        if failed:
            suffix = f" [{type(err).__name__}]" if err else ""
            print(f"xfail (unimplemented) {fn.__name__}{suffix}")
        else:
            FAILURES.append(f"XPASS:{fn.__name__}")
            print(f"FAIL XPASS {fn.__name__}: passed while marked "
                  "expectedFailure -- remove it from XFAIL")
    elif err is not None:
        FAILURES.append(f"ERROR:{fn.__name__}")
        print(f"FAIL {fn.__name__}: {type(err).__name__}: {err}")


def main() -> int:
    _check_registry_is_complete()
    for fn in TESTS:
        _run(fn)
    print(f"\n{len(FAILURES)} failures")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    raise SystemExit(main())
