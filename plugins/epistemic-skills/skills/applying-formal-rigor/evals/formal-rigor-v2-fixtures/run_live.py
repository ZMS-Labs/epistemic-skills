#!/usr/bin/env python3
"""Resumable, no-retry live runner for the formal-rigor v2 battery."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from typing import Callable, NamedTuple
import uuid


ROOT = Path(__file__).resolve().parent
SKILL_ROOT = ROOT.parents[1]
REPO_ROOT = ROOT.parents[5]
FIXTURES_ROOT = ROOT / "fixtures"
PROMPTS_ROOT = ROOT / "prompts"
RED_BASELINE_ROOT = ROOT / "results" / "2026-07-24-red-baseline"

PARODY_ARMS = (
    "parody-always-cautious",
    "parody-always-decide",
    "parody-closed-taxonomy",
    "parody-formal-only",
    "parody-full-ceremony",
    "parody-jargon-only",
)
ARM_PROMPTS = {
    "neutral": "neutral.txt",
    "v1-current": "v1-current.txt",
    "v2-candidate": "v2-candidate.txt",
    **{arm: f"{arm}.txt" for arm in PARODY_ARMS},
}
SEMANTIC_VERDICTS = {"VALID", "INVALID", "INCONCLUSIVE"}
OBLIGATION_STATES = {"SATISFIED", "VIOLATED", "INCONCLUSIVE"}


class ArmTask(NamedTuple):
    arm: str
    repetition: int
    fixture: str


class SemanticTask(NamedTuple):
    repetition: int
    fixture: str
    seat: str


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def fixture_ids() -> list[str]:
    return sorted(path.name for path in FIXTURES_ROOT.iterdir() if path.is_dir())


def full_arm_plan() -> list[ArmTask]:
    tasks: list[ArmTask] = []
    for arm in ("neutral", "v1-current"):
        for repetition in (2, 3):
            tasks.extend(ArmTask(arm, repetition, fixture) for fixture in fixture_ids())
    for repetition in (1, 2, 3):
        tasks.extend(ArmTask("v2-candidate", repetition, fixture) for fixture in fixture_ids())
    for arm in PARODY_ARMS:
        tasks.extend(ArmTask(arm, 1, fixture) for fixture in fixture_ids())
    return tasks


def full_semantic_plan() -> list[SemanticTask]:
    return [
        SemanticTask(repetition, fixture, seat)
        for repetition in (1, 2, 3)
        for fixture in fixture_ids()
        for seat in ("a", "b")
    ]


def filter_arm_tasks(
    tasks: list[ArmTask], *, arms: set[str] | None = None,
    fixtures: set[str] | None = None, repetitions: set[int] | None = None,
) -> list[ArmTask]:
    return [
        task for task in tasks
        if (arms is None or task.arm in arms)
        and (fixtures is None or task.fixture in fixtures)
        and (repetitions is None or task.repetition in repetitions)
    ]


def filter_semantic_tasks(
    tasks: list[SemanticTask], *, fixtures: set[str] | None = None,
    repetitions: set[int] | None = None, seats: set[str] | None = None,
) -> list[SemanticTask]:
    return [
        task for task in tasks
        if (fixtures is None or task.fixture in fixtures)
        and (repetitions is None or task.repetition in repetitions)
        and (seats is None or task.seat in seats)
    ]


def copy_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def build_arm_packet(
    destination: Path,
    arm: str,
    fixture_dir: Path,
    *,
    v1_source_dir: Path | None = None,
) -> None:
    if arm not in ARM_PROMPTS:
        raise ValueError(f"unknown arm: {arm}")
    destination.mkdir(parents=True, exist_ok=False)
    copy_file(fixture_dir / "scenario.md", destination / "scenario.md")
    shutil.copytree(fixture_dir / "artifacts", destination / "artifacts")
    copy_file(ROOT / "formal-rigor-fixture-response.schema.json", destination / "formal-rigor-fixture-response.schema.json")
    copy_file(ROOT / "formal-rigor-record.schema.json", destination / "formal-rigor-record.schema.json")
    copy_file(PROMPTS_ROOT / ARM_PROMPTS[arm], destination / "ARM_PROMPT.txt")

    if arm == "v1-current":
        if v1_source_dir is None:
            raise ValueError("v1-current packet requires a pinned v1 source directory")
        copy_file(v1_source_dir / "SKILL.md", destination / "v1" / "SKILL.md")
        copy_file(v1_source_dir / "theory-battery.md", destination / "v1" / "theory-battery.md")
    elif arm == "v2-candidate" or arm in PARODY_ARMS:
        copy_file(SKILL_ROOT / "SKILL.md", destination / "candidate" / "SKILL.md")
        copy_file(SKILL_ROOT / "theory-battery.md", destination / "candidate" / "theory-battery.md")
        shutil.copytree(
            SKILL_ROOT / "reference" / "modules",
            destination / "candidate" / "reference" / "modules",
        )


def adjudication_rubric(truth: dict) -> dict:
    return {
        "fixture": truth["fixture_id"],
        "claims": [
            {
                "id": claim["id"],
                "proof_obligations": claim.get("proof_obligations", []),
                "forbidden_propositions": claim.get("forbidden_propositions", []),
            }
            for claim in truth["claims"]
        ],
    }


def build_adjudication_packet(
    destination: Path,
    fixture_dir: Path,
    candidate_response: Path,
    truth: dict,
) -> None:
    destination.mkdir(parents=True, exist_ok=False)
    copy_file(fixture_dir / "scenario.md", destination / "scenario.md")
    shutil.copytree(fixture_dir / "artifacts", destination / "artifacts")
    copy_file(candidate_response, destination / "candidate-response.json")
    write_json(destination / "rubric.json", adjudication_rubric(truth))


def packet_manifest(packet_dir: Path) -> dict[str, str]:
    return {
        path.relative_to(packet_dir).as_posix(): sha256_file(path)
        for path in sorted(packet_dir.rglob("*"))
        if path.is_file()
    }


def codex_command(
    *, codex: str, model: str, packet_dir: Path, response_path: Path, prompt: str,
) -> list[str]:
    return [
        codex, "exec", "--ephemeral", "--ignore-user-config", "--ignore-rules",
        "--disable", "plugins", "--disable", "apps", "--disable", "remote_plugin",
        "--disable", "plugin_sharing", "--sandbox", "read-only",
        "--skip-git-repo-check", "--color", "never", "--json",
        "-c", 'model_reasoning_effort="high"', "--model", model,
        "--cd", str(packet_dir), "--output-last-message", str(response_path), prompt,
    ]


def call_needed(result_dir: Path) -> bool:
    return not (result_dir / "call.json").is_file()


def arm_prompt(fixture: str) -> str:
    return f"""You are a context-isolated run agent for fixture {fixture}.
Read only files inside the current packet directory. Follow ARM_PROMPT.txt. The scenario is
scenario.md and its allowed evidence is under artifacts/. Public response contracts are the two
schema files. If candidate/ exists, read candidate/SKILL.md and the module registry, then load only
the module files you determine are material; do not treat module presence as proof.

Return exactly one formal-rigor-fixture-response@1 JSON object for fixture {fixture}. Emit no
Markdown fence, preamble, commentary, score, hidden class guess, or claims about files outside this
packet. Do not read or infer ground truth, thresholds, other fixtures, other arms, or prior results.
"""


def semantic_prompt(fixture: str) -> str:
    return f"""You are one isolated, arm-blinded semantic adjudicator for fixture {fixture}.
Read only scenario.md, artifacts/, candidate-response.json, and rubric.json in this packet. Do not
infer arm identity, model identity, thresholds, prior results, or another adjudicator's report.
Judge whether the response actually satisfies every proof obligation and avoids every forbidden
proposition. Cite exact response coordinates. Structure and fluency are not proof.

Return exactly one JSON object with this shape and no prose outside it:
{{
  "adjudication": "formal-rigor-semantic-adjudication@1",
  "fixture": "{fixture}",
  "verdict": "VALID|INVALID|INCONCLUSIVE",
  "obligations": [{{"claim_id":"c1","obligation":"exact rubric string","status":"SATISFIED|VIOLATED|INCONCLUSIVE","response_coordinates":["path"],"reason":"..."}}],
  "forbidden_propositions": [{{"claim_id":"c1","proposition":"exact rubric string","present":false,"response_coordinates":[],"reason":"..."}}],
  "coverage_limits": []
}}
Include exactly one row for every rubric obligation and forbidden proposition.
"""


def sensitive_markers(text: str) -> list[str]:
    checks = {
        "user-profile-path": "C:\\Users\\",
        "api-key-prefix": "sk-",
        "bearer-token": "Bearer ",
    }
    return [name for name, marker in checks.items() if marker.lower() in text.lower()]


def execute_call(
    *,
    result_dir: Path,
    packet_root: Path,
    packet_builder: Callable[[Path], None],
    prompt: str,
    codex: str,
    model: str,
    identity: dict,
    source_commit: str,
    timeout_seconds: int,
) -> dict:
    if not call_needed(result_dir):
        return json.loads((result_dir / "call.json").read_text(encoding="utf-8"))
    result_dir.mkdir(parents=True, exist_ok=True)
    packet_root.mkdir(parents=True, exist_ok=True)
    packet_dir = packet_root / f"packet-{uuid.uuid4().hex}"
    packet_builder(packet_dir)
    response_path = result_dir / "response.json"
    command = codex_command(
        codex=codex, model=model, packet_dir=packet_dir,
        response_path=response_path, prompt=prompt,
    )
    started = utc_now()
    exit_code: int | None = None
    stdout = ""
    stderr = ""
    transport = "failed"
    try:
        completed = subprocess.run(
            command, cwd=packet_dir, text=True, encoding="utf-8", errors="replace",
            capture_output=True, timeout=timeout_seconds, check=False,
        )
        exit_code = completed.returncode
        stdout = completed.stdout
        stderr = completed.stderr
        transport = "completed" if completed.returncode == 0 else "failed"
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode("utf-8", errors="replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8", errors="replace")
        transport = "timeout"
    (result_dir / "events.jsonl").write_text(stdout, encoding="utf-8", newline="\n")
    (result_dir / "stderr.txt").write_text(stderr, encoding="utf-8", newline="\n")
    parseable = False
    response_hash = None
    if response_path.is_file():
        response_hash = sha256_file(response_path)
        try:
            json.loads(response_path.read_text(encoding="utf-8"))
            parseable = True
        except json.JSONDecodeError:
            pass
    markers = sensitive_markers(stdout + "\n" + stderr + "\n" + (response_path.read_text(encoding="utf-8", errors="replace") if response_path.is_file() else ""))
    record = {
        "schema": "formal-rigor-live-call@1",
        **identity,
        "source_commit": source_commit,
        "model": model,
        "reasoning_effort": "high",
        "harness": "codex exec",
        "started_at": started,
        "completed_at": utc_now(),
        "transport": transport,
        "exit_code": exit_code,
        "json_parseable": parseable,
        "response_sha256": response_hash,
        "packet_sha256": packet_manifest(packet_dir),
        "secret_screen": {"passed": not markers, "markers": markers},
        "retry_policy": "no-retry; call.json presence is terminal",
    }
    write_json(result_dir / "call.json", record)
    shutil.rmtree(packet_dir)
    return record


def prepare_v1_snapshot(destination: Path, commit: str) -> Path:
    destination.mkdir(parents=True, exist_ok=True)
    for filename in ("SKILL.md", "theory-battery.md"):
        target = destination / filename
        if target.is_file():
            continue
        repo_path = f"plugins/epistemic-skills/skills/applying-formal-rigor/{filename}"
        completed = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "show", f"{commit}:{repo_path}"],
            capture_output=True, check=True,
        )
        target.write_bytes(completed.stdout)
    return destination


def run_arm_task(
    task: ArmTask, *, output_root: Path, packet_root: Path, codex: str, model: str,
    source_commit: str, v1_source_dir: Path, timeout_seconds: int,
) -> dict:
    run_dir = output_root / "arms" / task.arm / f"run-{task.repetition}"
    call_dir = run_dir / "calls" / task.fixture
    fixture_dir = FIXTURES_ROOT / task.fixture
    record = execute_call(
        result_dir=call_dir,
        packet_root=packet_root,
        packet_builder=lambda packet: build_arm_packet(
            packet, task.arm, fixture_dir,
            v1_source_dir=v1_source_dir if task.arm == "v1-current" else None,
        ),
        prompt=arm_prompt(task.fixture),
        codex=codex,
        model=model,
        identity={"kind": "arm", "arm": task.arm, "repetition": task.repetition, "fixture": task.fixture},
        source_commit=source_commit,
        timeout_seconds=timeout_seconds,
    )
    response = call_dir / "response.json"
    materialized = run_dir / f"{task.fixture}.response.json"
    if response.is_file() and not materialized.is_file():
        copy_file(response, materialized)
    return record


def validate_adjudication(value: object, truth: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["root must be an object"]
    if value.get("adjudication") != "formal-rigor-semantic-adjudication@1":
        errors.append("invalid adjudication envelope")
    if value.get("fixture") != truth.get("fixture_id"):
        errors.append("fixture mismatch")
    if value.get("verdict") not in SEMANTIC_VERDICTS:
        errors.append("invalid verdict")
    expected_obligations = {
        (claim["id"], obligation)
        for claim in truth.get("claims", [])
        for obligation in claim.get("proof_obligations", [])
    }
    rows = value.get("obligations", [])
    if not isinstance(rows, list):
        rows = []
        errors.append("obligations must be an array")
    actual_obligations = set()
    for row in rows:
        if not isinstance(row, dict):
            errors.append("obligation row must be an object")
            continue
        actual_obligations.add((row.get("claim_id"), row.get("obligation")))
        if row.get("status") not in OBLIGATION_STATES:
            errors.append("invalid obligation status")
        if not isinstance(row.get("response_coordinates"), list) or not row.get("reason"):
            errors.append("obligation row lacks coordinates/reason")
    if actual_obligations != expected_obligations:
        errors.append("obligation set mismatch")
    expected_forbidden = {
        (claim["id"], proposition)
        for claim in truth.get("claims", [])
        for proposition in claim.get("forbidden_propositions", [])
    }
    forbidden_rows = value.get("forbidden_propositions", [])
    if not isinstance(forbidden_rows, list):
        forbidden_rows = []
        errors.append("forbidden_propositions must be an array")
    actual_forbidden = set()
    for row in forbidden_rows:
        if not isinstance(row, dict):
            errors.append("forbidden proposition row must be an object")
            continue
        actual_forbidden.add((row.get("claim_id"), row.get("proposition")))
        if not isinstance(row.get("present"), bool):
            errors.append("forbidden proposition present must be boolean")
        if not isinstance(row.get("response_coordinates"), list) or not row.get("reason"):
            errors.append("forbidden proposition row lacks coordinates/reason")
    if actual_forbidden != expected_forbidden:
        errors.append("forbidden proposition set mismatch")
    if not isinstance(value.get("coverage_limits"), list):
        errors.append("coverage_limits must be an array")
    return errors


def run_semantic_task(
    task: SemanticTask, *, output_root: Path, packet_root: Path, codex: str,
    model: str, source_commit: str, timeout_seconds: int,
) -> dict:
    fixture_dir = FIXTURES_ROOT / task.fixture
    truth = json.loads((fixture_dir / "ground-truth.json").read_text(encoding="utf-8"))
    candidate_response = output_root / "arms" / "v2-candidate" / f"run-{task.repetition}" / f"{task.fixture}.response.json"
    call_dir = output_root / "semantic" / f"run-{task.repetition}" / task.fixture / f"seat-{task.seat}"
    if not candidate_response.is_file():
        raise FileNotFoundError(f"candidate response missing: {candidate_response}")
    record = execute_call(
        result_dir=call_dir,
        packet_root=packet_root,
        packet_builder=lambda packet: build_adjudication_packet(packet, fixture_dir, candidate_response, truth),
        prompt=semantic_prompt(task.fixture),
        codex=codex,
        model=model,
        identity={"kind": "semantic", "repetition": task.repetition, "fixture": task.fixture, "seat": task.seat},
        source_commit=source_commit,
        timeout_seconds=timeout_seconds,
    )
    response = call_dir / "response.json"
    errors: list[str] = []
    if response.is_file():
        try:
            errors = validate_adjudication(json.loads(response.read_text(encoding="utf-8")), truth)
        except json.JSONDecodeError as exc:
            errors = [f"invalid JSON: {exc}"]
    else:
        errors = ["response missing"]
    write_json(call_dir / "validation.json", {"valid": not errors, "errors": errors})
    return record


def run_parallel(tasks: list, worker: Callable[[object], dict], workers: int) -> tuple[int, int]:
    completed = 0
    failed = 0
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(worker, task): task for task in tasks}
        for future in as_completed(futures):
            task = futures[future]
            try:
                record = future.result()
                if record.get("transport") == "completed" and record.get("json_parseable") and record.get("secret_screen", {}).get("passed"):
                    completed += 1
                else:
                    failed += 1
                print(f"{task}: {record.get('transport')} parseable={record.get('json_parseable')}", flush=True)
            except Exception as exc:  # fail-closed while allowing other independent calls to finish
                failed += 1
                print(f"{task}: ERROR {exc}", file=sys.stderr, flush=True)
    return completed, failed


def summarize_semantic(output_root: Path) -> dict:
    results = []
    for repetition in (1, 2, 3):
        for fixture in fixture_ids():
            truth = json.loads((FIXTURES_ROOT / fixture / "ground-truth.json").read_text(encoding="utf-8"))
            seat_values = []
            seat_errors = []
            for seat in ("a", "b"):
                seat_dir = output_root / "semantic" / f"run-{repetition}" / fixture / f"seat-{seat}"
                response_path = seat_dir / "response.json"
                if not response_path.is_file():
                    seat_values.append(None)
                    seat_errors.append(["response missing"])
                    continue
                try:
                    value = json.loads(response_path.read_text(encoding="utf-8"))
                    errors = validate_adjudication(value, truth)
                except json.JSONDecodeError as exc:
                    value = None
                    errors = [f"invalid JSON: {exc}"]
                seat_values.append(value)
                seat_errors.append(errors)
            verdicts = [value.get("verdict") if isinstance(value, dict) and not errors else "INCONCLUSIVE" for value, errors in zip(seat_values, seat_errors)]
            if "INVALID" in verdicts:
                status = "FAIL"
            elif verdicts == ["VALID", "VALID"]:
                status = "PASS"
            elif truth.get("priority") == "P0":
                status = "FAIL"
            else:
                status = "ARBITRATION_REQUIRED"
            results.append({
                "repetition": repetition, "fixture": fixture, "priority": truth.get("priority"),
                "seat_verdicts": verdicts, "seat_errors": seat_errors, "status": status,
            })
    report = {
        "schema": "formal-rigor-semantic-summary@1",
        "results": results,
        "pass": sum(row["status"] == "PASS" for row in results),
        "fail": sum(row["status"] == "FAIL" for row in results),
        "arbitration_required": sum(row["status"] == "ARBITRATION_REQUIRED" for row in results),
    }
    write_json(output_root / "semantic-summary.json", report)
    return report


def default_source_commit() -> str:
    return subprocess.run(
        ["git", "-C", str(REPO_ROOT), "rev-parse", "HEAD"],
        text=True, encoding="utf-8", capture_output=True, check=True,
    ).stdout.strip()


def verify_source_state(source_commit: str, *, require_clean: bool = True) -> None:
    head = default_source_commit()
    if source_commit != head:
        raise ValueError(f"source commit {source_commit} is not checked-out HEAD {head}")
    if require_clean:
        status = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "status", "--porcelain"],
            text=True, encoding="utf-8", capture_output=True, check=True,
        ).stdout
        if status.strip():
            raise ValueError("live run requires a clean worktree")


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("plan")

    arms = sub.add_parser("run-arms")
    arms.add_argument("--output-root", type=Path, required=True)
    arms.add_argument("--packet-root", type=Path, default=Path(tempfile.gettempdir()) / "formal-rigor-live-packets")
    arms.add_argument("--codex", default="codex")
    arms.add_argument("--model", default="gpt-5.6-sol")
    arms.add_argument("--workers", type=int, default=4)
    arms.add_argument("--timeout-seconds", type=int, default=600)
    arms.add_argument("--source-commit", default=None)
    arms.add_argument("--v1-commit", default=None)
    arms.add_argument("--arm", action="append", choices=tuple(ARM_PROMPTS))
    arms.add_argument("--fixture", action="append", choices=fixture_ids())
    arms.add_argument("--repetition", action="append", type=int, choices=(1, 2, 3))

    semantic = sub.add_parser("run-semantic")
    semantic.add_argument("--output-root", type=Path, required=True)
    semantic.add_argument("--packet-root", type=Path, default=Path(tempfile.gettempdir()) / "formal-rigor-semantic-packets")
    semantic.add_argument("--codex", default="codex")
    semantic.add_argument("--model", default="gpt-5.6-sol")
    semantic.add_argument("--workers", type=int, default=4)
    semantic.add_argument("--timeout-seconds", type=int, default=600)
    semantic.add_argument("--source-commit", default=None)
    semantic.add_argument("--fixture", action="append", choices=fixture_ids())
    semantic.add_argument("--repetition", action="append", type=int, choices=(1, 2, 3))
    semantic.add_argument("--seat", action="append", choices=("a", "b"))

    summary = sub.add_parser("summarize-semantic")
    summary.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()

    if args.command == "plan":
        print(json.dumps({"arm_calls": len(full_arm_plan()), "semantic_calls": len(full_semantic_plan()), "maximum_before_arbitration": 418}, indent=2))
        return 0
    if args.command == "summarize-semantic":
        report = summarize_semantic(args.output_root)
        print(json.dumps({key: report[key] for key in ("pass", "fail", "arbitration_required")}, indent=2))
        return 0

    source_commit = args.source_commit or default_source_commit()
    verify_source_state(source_commit)
    if args.command == "run-arms":
        baseline_manifest = json.loads((RED_BASELINE_ROOT / "manifest.json").read_text(encoding="utf-8"))
        v1_commit = args.v1_commit or baseline_manifest["repository_head"]
        v1_source = prepare_v1_snapshot(args.output_root / "metadata" / "v1-source", v1_commit)
        tasks = filter_arm_tasks(
            full_arm_plan(),
            arms=set(args.arm) if args.arm else None,
            fixtures=set(args.fixture) if args.fixture else None,
            repetitions=set(args.repetition) if args.repetition else None,
        )
        completed, failed = run_parallel(
            tasks,
            lambda task: run_arm_task(
                task, output_root=args.output_root, packet_root=args.packet_root,
                codex=args.codex, model=args.model, source_commit=source_commit,
                v1_source_dir=v1_source, timeout_seconds=args.timeout_seconds,
            ),
            args.workers,
        )
        write_json(args.output_root / "arm-run-status.json", {
            "schema": "formal-rigor-live-phase-status@1", "phase": "arms",
            "source_commit": source_commit, "model": args.model,
            "planned": len(tasks), "completed": completed, "failed": failed,
        })
        print(f"arms: planned={len(tasks)} completed={completed} failed={failed}")
        return 0 if failed == 0 else 1
    if args.command == "run-semantic":
        tasks = filter_semantic_tasks(
            full_semantic_plan(),
            fixtures=set(args.fixture) if args.fixture else None,
            repetitions=set(args.repetition) if args.repetition else None,
            seats=set(args.seat) if args.seat else None,
        )
        completed, failed = run_parallel(
            tasks,
            lambda task: run_semantic_task(
                task, output_root=args.output_root, packet_root=args.packet_root,
                codex=args.codex, model=args.model, source_commit=source_commit,
                timeout_seconds=args.timeout_seconds,
            ),
            args.workers,
        )
        write_json(args.output_root / "semantic-run-status.json", {
            "schema": "formal-rigor-live-phase-status@1", "phase": "semantic",
            "source_commit": source_commit, "model": args.model,
            "planned": len(tasks), "completed": completed, "failed": failed,
        })
        print(f"semantic: planned={len(tasks)} completed={completed} failed={failed}")
        return 0 if failed == 0 else 1
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
