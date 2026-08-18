#!/usr/bin/env python3
"""Audit CI workflow path filters against step input paths (ES6-ORACLE-AUDIT)."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - stdlib-only fallback for minimal envs
    yaml = None

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKFLOW_DIR = REPO_ROOT / ".github/workflows"

# Paths referenced by steps but intentionally global (always run on dispatch/main).
GLOBAL_ALLOW = {
    ".github/workflows/",
    ".github/scripts/",
    "README.md",
}

PATH_TOKEN = re.compile(
    r"(?:^|[\s'\"])([\w./-]+\.(?:py|yml|yaml|json|md|sh|jsonl))(?:[\s'\"]|$)"
)


@dataclass
class Finding:
    workflow: str
    kind: str
    path: str
    detail: str


def _load_workflow(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if yaml is not None:
        return yaml.safe_load(text)
    raise RuntimeError("PyYAML required for workflow audit; pip install pyyaml")


def _event_path_filters(doc: dict) -> dict[str, list[str]]:
    on = doc.get("on") or doc.get(True) or {}
    if isinstance(on, str):
        on = {on: {}}
    out: dict[str, list[str]] = {}
    for event, cfg in on.items():
        if isinstance(cfg, dict) and "paths" in cfg:
            out[event] = list(cfg["paths"])
        elif event in ("push", "pull_request") and isinstance(cfg, list):
            pass
    return out


def _extract_step_paths(step: dict) -> set[str]:
    found: set[str] = set()
    run = step.get("run")
    if not isinstance(run, str):
        return found
    for match in PATH_TOKEN.finditer(run):
        token = match.group(1)
        if token.startswith("plugins/") or token.startswith("docs/"):
            found.add(token)
        if token.startswith(".github/"):
            found.add(token)
    return found


def _path_covered(path: str, filters: list[str]) -> bool:
    if any(path.startswith(prefix) for prefix in GLOBAL_ALLOW):
        return True
    for pattern in filters:
        if pattern.endswith("/**"):
            if path.startswith(pattern[:-3]) or path + "/" == pattern:
                return True
        elif pattern.endswith("**"):
            base = pattern.rstrip("*").rstrip("/")
            if path.startswith(base):
                return True
        else:
            if path == pattern or path.startswith(pattern.rstrip("/") + "/"):
                return True
    return False


def audit_workflow(path: Path) -> list[Finding]:
    doc = _load_workflow(path)
    name = path.name
    filters = _event_path_filters(doc)
    push_filters = filters.get("push", [])
    pr_filters = filters.get("pull_request", [])
    if not push_filters and not pr_filters:
        return []

    findings: list[Finding] = []
    jobs = doc.get("jobs") or {}
    for job_name, job in jobs.items():
        if job.get("if") and "workflow_dispatch" in str(job.get("if")):
            continue
        steps = job.get("steps") or []
        for step in steps:
            for ref in sorted(_extract_step_paths(step)):
                if push_filters and not _path_covered(ref, push_filters):
                    findings.append(
                        Finding(
                            workflow=name,
                            kind="uncovered_push_path",
                            path=ref,
                            detail=f"job={job_name}; not matched by push.paths",
                        )
                    )
                if pr_filters and not _path_covered(ref, pr_filters):
                    findings.append(
                        Finding(
                            workflow=name,
                            kind="uncovered_pr_path",
                            path=ref,
                            detail=f"job={job_name}; not matched by pull_request.paths",
                        )
                    )
    return findings


def run_audit() -> list[Finding]:
    findings: list[Finding] = []
    for wf in sorted(WORKFLOW_DIR.glob("*.yml")):
        findings.extend(audit_workflow(wf))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        type=Path,
        help="Write JSON audit report to this path",
    )
    parser.add_argument(
        "--allow-findings",
        action="store_true",
        help="Exit 0 even when findings exist (report-only mode)",
    )
    args = parser.parse_args()

    findings = run_audit()
    report = {
        "schema": "workflow-oracle-audit@1",
        "generated_at": datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "finding_count": len(findings),
        "findings": [asdict(f) for f in findings],
    }
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(f"wrote workflow oracle audit: {args.write} ({len(findings)} findings)")
    else:
        print(json.dumps(report, indent=2))

    if findings and not args.allow_findings:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
