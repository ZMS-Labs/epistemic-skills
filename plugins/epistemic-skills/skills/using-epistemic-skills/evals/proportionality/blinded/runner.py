#!/usr/bin/env python3
"""Prepare and score isolated blinded proportionality packets."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import subprocess
import sys
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
ARMS = HERE / "arms.json"
SCENARIOS = HERE / "scenarios.json"
FIXTURES = PARENT / "fixtures.json"
SCORER = PARENT / "score.py"
RESPONSE_SCHEMA = HERE / "proportionality-fixture-response.schema.json"
REPO_ROOT = HERE.parents[6]
SKILL_PATHS = [
    "plugins/epistemic-skills/skills/using-epistemic-skills/SKILL.md",
    "plugins/epistemic-skills/skills/using-epistemic-skills/reference/routine-fast-path.md",
    "plugins/epistemic-skills/skills/blindspot-pass/SKILL.md",
    "plugins/epistemic-skills/skills/applying-formal-rigor/SKILL.md",
    "plugins/epistemic-skills/skills/gauntlet/SKILL.md",
    "plugins/epistemic-skills/skills/helix/SKILL.md",
    "plugins/epistemic-skills/skills/evidence-locked-uat/SKILL.md",
    "plugins/epistemic-skills/skills/decision-ledger/SKILL.md",
]

sys.path.insert(0, str(PARENT))
from score import format_report, score_run  # noqa: E402

RESPONSE_FIELDS = {
    "path": "routine | micro-recon | routed",
    "fired_skills": "array of skill ids actually fired",
    "process_artifacts": "array of process artifact kinds actually created",
    "visible_process_words": "non-negative integer",
    "role_invocations": "non-negative integer",
    "emitted_skip_inventory": "boolean",
    "direct_check": "bounded verification performed or proposed, else empty string",
    "required_signal_observed": "boolean",
    "escalated": "boolean",
}
PRINT_LOCK = threading.Lock()


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical(data: Any) -> bytes:
    return (json.dumps(data, sort_keys=True, separators=(",", ":")) + "\n").encode()


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest_file(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def source_skill_hashes(source_root: Path) -> dict[str, str | None]:
    """Hash each pinned skill artifact, preserving historical absence explicitly."""
    return {
        path: digest_file(source_root / path) if (source_root / path).is_file() else None
        for path in SKILL_PATHS
    }


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical(data))


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def codex_live_prompt(packet_path: Path) -> str:
    """Build the scorer-free adapter prompt for a pinned source checkout."""
    packet = packet_path.read_text(encoding="utf-8")
    return (
        "The current working directory is the pinned source checkout for this arm. "
        "Activate its epistemic router by reading "
        "plugins/epistemic-skills/skills/using-epistemic-skills/SKILL.md. "
        "Follow that router and read only member skill files whose positive triggers apply. "
        "Do not inspect evaluation directories, scorer code, ground truth, other fixtures, "
        "other arms, or repository history. Treat the JSON below as the complete task packet. "
        "Follow its instruction and task, then return exactly one JSON object matching its "
        "response_contract and the enforced output schema. Report only skills actually fired; "
        "do not add process for the evaluation. Do not wrap the JSON in Markdown.\n\n"
        "BEGIN INPUT PACKET\n"
        f"{packet.rstrip()}\n"
        "END INPUT PACKET\n"
    )


def codex_live_command(
    codex: Path, source_root: Path, response_path: Path, model: str
) -> list[str]:
    """Return a command whose sealed task payload is supplied separately on stdin."""
    return [
        str(codex),
        "exec",
        "--ephemeral",
        "--ignore-user-config",
        "--ignore-rules",
        "--disable",
        "plugins",
        "--disable",
        "apps",
        "--disable",
        "remote_plugin",
        "--disable",
        "plugin_sharing",
        "--sandbox",
        "read-only",
        "--skip-git-repo-check",
        "--color",
        "never",
        "--json",
        "-c",
        'model_reasoning_effort="high"',
        "--model",
        model,
        "--cd",
        str(source_root),
        "--output-last-message",
        str(response_path),
        "--output-schema",
        str(RESPONSE_SCHEMA),
        "-",
    ]


def indexed(items: list[dict[str, Any]], label: str) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for item in items:
        item_id = item.get("id")
        if not isinstance(item_id, str) or item_id in result:
            raise SystemExit(f"{label} requires unique string ids")
        result[item_id] = item
    return result


def arm_by_id(arm_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    arms_data = load(ARMS)
    if arms_data.get("schema") != "proportionality-arms@1":
        raise SystemExit("invalid arms schema")
    arms = indexed(arms_data.get("arms", []), "arms")
    if arm_id not in arms:
        raise SystemExit(f"unknown arm {arm_id!r}; choose one of {sorted(arms)}")
    return arms[arm_id], arms_data["invocation"]


def git_output(source_root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(source_root), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def prepare(
    arm_id: str,
    repetition: int,
    out: Path,
    source_root: Path,
    *,
    _source_already_verified: bool = False,
) -> int:
    arm, invocation = arm_by_id(arm_id)
    maximum = arm.get("repetitions")
    if not isinstance(maximum, int) or not 1 <= repetition <= maximum:
        raise SystemExit(f"repetition must be between 1 and {maximum} for {arm_id}")
    if out.exists() and any(out.iterdir()):
        raise SystemExit(f"refusing to overwrite non-empty packet directory: {out}")

    source_root = source_root.resolve()
    try:
        observed_commit = git_output(source_root, "rev-parse", "HEAD")
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        raise SystemExit(f"cannot resolve source checkout {source_root}: {exc}") from exc
    if not _source_already_verified and observed_commit != arm["source_commit"]:
        raise SystemExit(
            f"source checkout is {observed_commit}, expected {arm['source_commit']} for {arm_id}"
        )
    dirty = subprocess.run(
        ["git", "-C", str(source_root), "diff", "--quiet", "HEAD", "--", *SKILL_PATHS]
    ).returncode
    if dirty and not _source_already_verified:
        raise SystemExit("source checkout has tracked changes in pinned skill files")

    fixture_data = load(FIXTURES)
    scenario_data = load(SCENARIOS)
    fixtures = indexed(fixture_data.get("fixtures", []), "fixtures")
    scenarios = indexed(scenario_data.get("scenarios", []), "scenarios")
    if set(fixtures) != set(scenarios):
        raise SystemExit(
            "scenario inventory mismatch: "
            f"missing={sorted(set(fixtures) - set(scenarios))}, "
            f"unknown={sorted(set(scenarios) - set(fixtures))}"
        )

    prompt_path = HERE / arm["prompt"]
    instruction = prompt_path.read_text(encoding="utf-8").strip()
    packet_hashes: dict[str, str] = {}
    for fixture_id in fixtures:
        scenario = scenarios[fixture_id]
        packet = {
            "schema": "proportionality-blinded-input@1",
            "fixture_id": fixture_id,
            "instruction": instruction,
            "task": {
                "scenario": scenario["scenario"],
                "artifacts": scenario["artifacts"],
            },
            "response_contract": {
                "schema": "proportionality-fixture-response@1",
                "fixture_id": fixture_id,
                "fields": RESPONSE_FIELDS,
            },
        }
        path = out / "packets" / fixture_id / "input.json"
        write_json(path, packet)
        packet_hashes[fixture_id] = digest_file(path)

    (out / "responses").mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema": "proportionality-packet-manifest@1",
        "arm": arm,
        "repetition": repetition,
        "invocation": invocation,
        "source_hashes": {
            "arms.json": digest_file(ARMS),
            "scenarios.json": digest_file(SCENARIOS),
            "fixtures.json": digest_file(FIXTURES),
            "score.py": digest_file(SCORER),
            "runner.py": digest_file(HERE / "runner.py"),
            "proportionality-fixture-response.schema.json": digest_file(RESPONSE_SCHEMA),
            arm["prompt"]: digest_file(prompt_path),
            **source_skill_hashes(source_root),
        },
        "packet_hashes": packet_hashes,
    }
    write_json(out / "manifest.json", manifest)
    print(f"prepared {len(packet_hashes)} blinded packets for {arm_id} repetition {repetition}")
    return 0


def validate_response(data: Any, fixture_id: str) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("response must be a JSON object")
    if data.get("schema") != "proportionality-fixture-response@1":
        raise ValueError("response schema must be proportionality-fixture-response@1")
    if data.get("fixture_id") != fixture_id:
        raise ValueError(f"fixture_id must be {fixture_id!r}")
    missing = sorted(set(RESPONSE_FIELDS) - set(data))
    unknown = sorted(set(data) - set(RESPONSE_FIELDS) - {"schema", "fixture_id"})
    if missing or unknown:
        raise ValueError(f"field mismatch: missing={missing}, unknown={unknown}")
    return {"fixture_id": fixture_id, **{key: data[key] for key in RESPONSE_FIELDS}}


def run_live(
    packet_dir: Path,
    source_root: Path,
    codex: Path,
    workers: int,
    timeout_seconds: int,
    fixtures: list[str] | None = None,
) -> int:
    """Execute one prepared arm against its pinned source in isolated Codex turns."""
    manifest_path = packet_dir / "manifest.json"
    manifest = load(manifest_path)
    if manifest.get("schema") != "proportionality-packet-manifest@1":
        raise SystemExit("invalid or missing packet manifest")
    if workers < 1:
        raise SystemExit("workers must be positive")
    source_root = source_root.resolve()
    observed_commit = git_output(source_root, "rev-parse", "HEAD")
    expected_commit = manifest["arm"]["source_commit"]
    if observed_commit != expected_commit:
        raise SystemExit(
            f"source checkout is {observed_commit}, expected {expected_commit} for live arm"
        )
    expected_skill_hashes = {
        path: manifest["source_hashes"].get(path) for path in SKILL_PATHS
    }
    observed_skill_hashes = source_skill_hashes(source_root)
    if observed_skill_hashes != expected_skill_hashes:
        raise SystemExit("source skill hashes no longer match the prepared manifest")
    model = manifest["invocation"]["model"]

    def execute(fixture_id: str) -> dict[str, Any]:
        packet_path = packet_dir / "packets" / fixture_id / "input.json"
        expected_packet_hash = manifest["packet_hashes"][fixture_id]
        if not packet_path.is_file() or digest_file(packet_path) != expected_packet_hash:
            raise RuntimeError(f"{fixture_id}: input packet is missing or changed")
        call_path = packet_dir / "calls" / f"{fixture_id}.json"
        if call_path.is_file():
            return load(call_path)
        response_path = packet_dir / "responses" / f"{fixture_id}.json"
        if response_path.exists():
            raise RuntimeError(
                f"{fixture_id}: response exists without terminal call record; refusing retry"
            )
        events_path = packet_dir / "events" / f"{fixture_id}.jsonl"
        stderr_path = packet_dir / "stderr" / f"{fixture_id}.txt"
        events_path.parent.mkdir(parents=True, exist_ok=True)
        stderr_path.parent.mkdir(parents=True, exist_ok=True)
        prompt = codex_live_prompt(packet_path)
        command = codex_live_command(codex, source_root, response_path, model)
        started = utc_now()
        transport = "failed"
        exit_code: int | None = None
        stdout = ""
        stderr = ""
        try:
            completed = subprocess.run(
                command,
                cwd=source_root,
                input=prompt,
                text=True,
                encoding="utf-8",
                errors="replace",
                capture_output=True,
                timeout=timeout_seconds,
                check=False,
            )
            exit_code = completed.returncode
            stdout = completed.stdout
            stderr = completed.stderr
            transport = "completed" if exit_code == 0 else "failed"
        except subprocess.TimeoutExpired as exc:
            stdout = (
                exc.stdout.decode("utf-8", errors="replace")
                if isinstance(exc.stdout, bytes)
                else (exc.stdout or "")
            )
            stderr = (
                exc.stderr.decode("utf-8", errors="replace")
                if isinstance(exc.stderr, bytes)
                else (exc.stderr or "")
            )
            transport = "timeout"
        events_path.write_text(stdout, encoding="utf-8")
        stderr_path.write_text(stderr, encoding="utf-8")
        parseable = False
        fixture_match = False
        response_hash: str | None = None
        if response_path.is_file():
            response_hash = digest_file(response_path)
            try:
                response = load(response_path)
                validate_response(response, fixture_id)
                parseable = True
                fixture_match = response.get("fixture_id") == fixture_id
            except (json.JSONDecodeError, ValueError):
                pass
        record = {
            "schema": "proportionality-live-call@2",
            "fixture_id": fixture_id,
            "provider": manifest["invocation"]["provider"],
            "model": model,
            "harness": manifest["invocation"]["harness"],
            "reasoning_effort": manifest["invocation"]["settings"]["reasoning_effort"],
            "source_commit": observed_commit,
            "started_at": started,
            "completed_at": utc_now(),
            "transport": transport,
            "exit_code": exit_code,
            "json_parseable": parseable,
            "fixture_id_matches": fixture_match,
            "response_sha256": response_hash,
            "input_sha256": expected_packet_hash,
            "adapter_prompt_sha256": digest_bytes(prompt.encode("utf-8")),
            "retry_policy": "no-retry; call record presence is terminal",
        }
        write_json(call_path, record)
        with PRINT_LOCK:
            print(
                f"{fixture_id}: {transport} parseable={parseable} "
                f"fixture_match={fixture_match}",
                flush=True,
            )
        return record

    fixture_ids = sorted(fixtures or manifest["packet_hashes"])
    unknown_fixtures = sorted(set(fixture_ids) - set(manifest["packet_hashes"]))
    if unknown_fixtures:
        raise SystemExit(f"unknown fixtures for packet: {unknown_fixtures}")
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        records = list(pool.map(execute, fixture_ids))
    terminal = sum(record.get("transport") == "completed" for record in records)
    parseable = sum(record.get("json_parseable") is True for record in records)
    matched = sum(record.get("fixture_id_matches") is True for record in records)
    summary = {
        "schema": "proportionality-live-call-summary@2",
        "planned": len(records),
        "completed": terminal,
        "parseable": parseable,
        "fixture_id_matches": matched,
        "source_commit": observed_commit,
        "model": model,
        "workers": workers,
    }
    write_json(packet_dir / "call-summary.json", summary)
    print(json.dumps(summary, sort_keys=True))
    return 0 if terminal == parseable == matched == len(records) else 1


def score_packets(packet_dir: Path) -> int:
    manifest_path = packet_dir / "manifest.json"
    manifest = load(manifest_path)
    if manifest.get("schema") != "proportionality-packet-manifest@1":
        raise SystemExit("invalid or missing packet manifest")

    results: list[dict[str, Any]] = []
    response_hashes: dict[str, str] = {}
    errors: list[str] = []
    for fixture_id, expected_hash in manifest.get("packet_hashes", {}).items():
        input_path = packet_dir / "packets" / fixture_id / "input.json"
        if not input_path.exists() or digest_file(input_path) != expected_hash:
            errors.append(f"{fixture_id}: input packet is missing or changed")
            continue
        response_path = packet_dir / "responses" / f"{fixture_id}.json"
        if not response_path.exists():
            errors.append(f"{fixture_id}: raw response is missing")
            continue
        try:
            results.append(validate_response(load(response_path), fixture_id))
            response_hashes[fixture_id] = digest_file(response_path)
        except (json.JSONDecodeError, ValueError) as exc:
            errors.append(f"{fixture_id}: {exc}")
    if errors:
        raise SystemExit("cannot score packet:\n- " + "\n- ".join(errors))

    run = {
        "schema": "proportionality-run@1",
        "arm": manifest["arm"]["id"],
        "results": results,
    }
    run_path = packet_dir / "run.json"
    write_json(run_path, run)
    score = score_run(run, load(FIXTURES))
    report = format_report(score)
    (packet_dir / "score.txt").write_text(report + "\n", encoding="utf-8")
    evidence = {
        "schema": "proportionality-evidence@1",
        "status": "PASS" if score.passed else "FAIL",
        "manifest_sha256": digest_file(manifest_path),
        "run_sha256": digest_file(run_path),
        "response_hashes": response_hashes,
        "failures": score.failures,
    }
    write_json(packet_dir / "evidence.json", evidence)
    print(report)
    return 0 if score.passed else 1


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    prep = commands.add_parser("prepare")
    prep.add_argument("--arm", required=True)
    prep.add_argument("--repetition", type=int, default=1)
    prep.add_argument("--out", required=True, type=Path)
    prep.add_argument("--source-root", type=Path, default=REPO_ROOT)
    live = commands.add_parser("run-live")
    live.add_argument("--packet-dir", required=True, type=Path)
    live.add_argument("--source-root", required=True, type=Path)
    live.add_argument("--codex", required=True, type=Path)
    live.add_argument("--workers", type=int, default=1)
    live.add_argument("--timeout-seconds", type=int, default=600)
    live.add_argument("--fixture", action="append", dest="fixtures")
    scoring = commands.add_parser("score")
    scoring.add_argument("--packet-dir", required=True, type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    if args.command == "prepare":
        return prepare(args.arm, args.repetition, args.out, args.source_root)
    if args.command == "run-live":
        return run_live(
            args.packet_dir,
            args.source_root,
            args.codex,
            args.workers,
            args.timeout_seconds,
            args.fixtures,
        )
    return score_packets(args.packet_dir)


if __name__ == "__main__":
    raise SystemExit(main())
