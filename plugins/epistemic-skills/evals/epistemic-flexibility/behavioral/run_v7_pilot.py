#!/usr/bin/env python3
"""Thin supervisor for the installed Codex CLI; raw run data stays private.

No API implementation, native-goal runner, output template, or automatic retry.
Requires the preregistration's immutable revision and observed filtering capture.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import subprocess
import tarfile
import time
from pathlib import Path

BASELINE = "b4bc8dff0d07a7535c24905af7fb97cc85e01037"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def materialize(revision: str, destination: Path) -> None:
    prefix = "plugins/epistemic-skills/"
    archive = subprocess.run(["git", "archive", revision, prefix], cwd=REPO,
                             check=True, capture_output=True).stdout
    with tarfile.open(fileobj=io.BytesIO(archive)) as source:
        for item in source.getmembers():
            if not item.isfile():
                continue
            relative = Path(item.name.removeprefix(prefix))
            if relative.is_absolute() or ".." in relative.parts:
                raise ValueError("unsafe archive member")
            target = destination / ".agents" / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(source.extractfile(item).read())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--codex", required=True, type=Path)
    parser.add_argument("--private-root", required=True, type=Path)
    parser.add_argument("--disable-config", required=True, type=Path)
    parser.add_argument("--run", required=True, help="Exactly one scheduled run ID")
    args = parser.parse_args()
    candidate = subprocess.check_output(["git", "rev-parse", args.candidate + "^{commit}"],
                                        cwd=REPO, text=True).strip()
    if candidate != args.candidate or len(candidate) != 40:
        parser.error("candidate must be a full immutable commit ID")
    if not args.codex.is_file():
        parser.error("the observed installed CLI binary is required")
    private = args.private_root.resolve()
    private.relative_to((REPO / "outputs").resolve())
    private.mkdir(parents=True, exist_ok=True)
    schedule_bytes = (HERE / "v7-schedule.json").read_bytes()
    case_bytes = (HERE / "v7-cases.json").read_bytes()
    schedule = json.loads(schedule_bytes)["runs"]
    selected = next((run for run in schedule if run["run"] == args.run), None)
    if selected is None:
        parser.error("run must be in the preregistered schedule")
    # Advance only in the frozen order. Existing records are never overwritten.
    for earlier in schedule[:schedule.index(selected)]:
        if not (private / earlier["run"] / "record.json").is_file():
            parser.error("an earlier scheduled run has no preserved record")
    run_dir = private / selected["run"]
    run_dir.mkdir(exist_ok=False)
    workspace = run_dir / "workspace"
    workspace.mkdir()
    revision = BASELINE if selected["arm"] == "v6" else candidate
    materialize(revision, workspace)
    case = next(c for c in json.loads(case_bytes)["cases"] if c["id"] == selected["case"])
    for name, content in case["artifacts"].items():
        path = workspace / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="")
    prompt = (case["prompt"] + "\n\nThe task inputs are the files in this disposable workspace. "
              "Work only within this workspace. No network, publication, or real persistent goal "
              "activation is authorized. The supplied artifacts are synthetic.\n")
    (run_dir / "prompt.txt").write_text(prompt, encoding="utf-8")
    config = args.disable_config.read_text(encoding="utf-8")
    command = [str(args.codex.resolve()), "exec", "--ephemeral", "--ignore-user-config",
               "--ignore-rules", "--sandbox", "workspace-write", "--skip-git-repo-check",
               "--json", "--color", "never", "--model", "gpt-5.6-sol",
               "--disable", "hooks", "--disable", "goals", "-c", "mcp_servers={}",
               "-c", "project_doc_max_bytes=0", "-c", 'model_reasoning_effort="medium"',
               "-c", config, "-C", str(workspace),
               "--output-last-message", str(run_dir / "final.txt"), "-"]
    record = {**selected, "candidate": candidate, "baseline": BASELINE, "revision": revision,
              "model_requested": "gpt-5.6-sol", "reasoning": "medium", "provider_requested": "openai", "serving_model_reported": None,
              "exposure": "native local catalogue; documented debug/exec caveat",
              "schedule_sha256": digest(schedule_bytes), "cases_sha256": digest(case_bytes),
              "prompt_sha256": digest(prompt.encode()), "disable_config_sha256": digest(config.encode()),
              "command": command, "status": "dispatched", "wall_limit_seconds": 180}
    write_json(run_dir / "record.json", record)
    start = time.monotonic()
    with (run_dir / "stdout.jsonl").open("wb") as stdout, (run_dir / "stderr.txt").open("wb") as stderr:
        process = subprocess.Popen(command, cwd=workspace, stdin=subprocess.PIPE, stdout=stdout, stderr=stderr)
        try:
            process.communicate(prompt.encode(), timeout=180)
            record["status"] = "exited" if process.returncode == 0 else "execution_failure"
        except subprocess.TimeoutExpired:
            record["status"] = "timeout"
            subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"], capture_output=True)
            process.wait(timeout=10)
        record["exit_code"] = process.returncode
    record["elapsed_seconds"] = round(time.monotonic() - start, 3)
    record["artifact_hashes_after"] = {name: digest((workspace / name).read_bytes())
                                        if (workspace / name).exists() else None
                                        for name in case["artifacts"]}
    write_json(run_dir / "record.json", record)
    print(json.dumps({k: record[k] for k in ("run", "case", "arm", "status", "exit_code", "elapsed_seconds")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
