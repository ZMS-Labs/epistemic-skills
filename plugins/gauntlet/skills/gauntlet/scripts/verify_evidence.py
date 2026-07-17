#!/usr/bin/env python3
"""
verify_evidence.py — Sovereign-Gauntlet evidence verifier.

Walks a lens report (or directory of lens reports) for [V <path>:<line>] tags,
resolves each <path> against an evidence root, downgrades unverifiable tags
to [H], and emits the per-lens Sovereign Fingerprint (total / verified /
hallucinated / accuracy%).

Behavior, not language, is canonical. This is a Python reimplementation of
the original PowerShell verifier; semantics are identical.

Usage:
    python verify_evidence.py --report lens-1.md --evidence-root /path/to/repo
    python verify_evidence.py --reports-dir reports/ --evidence-root /path/to/repo
    python verify_evidence.py --report lens-1.md --evidence-root . --rewrite

Exit codes:
    0  ran cleanly (regardless of accuracy)
    2  invalid invocation or missing inputs
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

TAG_RE = re.compile(r"\[V\s+([^\]:]+?):(\d+)\]")
# Tier system (2026-07-10): [V path:line] = directly verified (mechanically checked here);
# [I <- ...] = inference derived from cited verified evidence (counted, anchors spot-checked
# by the arbitrator); [H] = unverified hypothesis (zero weight). A bare [V] with no
# path:line is malformed and counts as hallucinated.
I_TAG_RE = re.compile(r"\[I\b[^\]]*\]")
H_TAG_RE = re.compile(r"\[H\b[^\]]*\]")
BARE_V_RE = re.compile(r"\[V\](?!\S)")


@dataclass
class TagResult:
    raw: str
    path: str
    line: int
    status: str  # "V" or "H"
    reason: str  # "" or "File Not Found" / "Line Out of Bounds"


@dataclass
class ReportFingerprint:
    report_path: str
    total: int
    verified: int
    hallucinated: int
    accuracy_pct: float
    i_tags: int
    h_tags: int
    malformed_v: int
    tag_results: list[TagResult]


def _file_line_count(path: Path) -> int | None:
    """Return line count, or None if the file can't be read."""
    try:
        with path.open("rb") as fh:
            return sum(1 for _ in fh)
    except OSError:
        return None


def _is_binary(path: Path) -> bool | None:
    """True if the file looks binary, None if it can't be read.

    Same NUL-in-prefix heuristic git uses. Exists because a line-oriented oracle
    cannot observe the contents of a binary blob: counting newlines in a .pyc
    yields a number, so a bare line-bounds check would certify [V some.pyc:5] as
    verified even though "line 5" is meaningless there. See ORACLE ADEQUACY below.
    """
    try:
        with path.open("rb") as fh:
            return b"\x00" in fh.read(8000)
    except OSError:
        return None


def verify_tag(path: str, line: int, evidence_root: Path) -> TagResult:
    raw = f"[V {path}:{line}]"
    # Resolve path against evidence root. Treat path as relative if not absolute.
    p = Path(path)
    resolved = p if p.is_absolute() else (evidence_root / p)
    try:
        resolved = resolved.resolve()
    except OSError:
        return TagResult(raw=raw, path=path, line=line, status="H", reason="File Not Found")

    if not resolved.exists() or not resolved.is_file():
        return TagResult(raw=raw, path=path, line=line, status="H", reason="File Not Found")

    # ORACLE ADEQUACY (F13, gauntlet-plugin-publish-2026-07-17): fail CLOSED when the
    # oracle cannot observe what the tag asserts. A line citation into a binary blob is
    # not verifiable by a line-oriented check, so it must never be certified [V] —
    # downgrade to [H] and say why. The precedent: a text-grep scrub certified that a
    # committed .pyc embedded no local path; it did (marshalled co_filename), and the
    # grep was structurally incapable of seeing it. An oracle that cannot fail is not
    # evidence.
    binary = _is_binary(resolved)
    if binary is None:
        return TagResult(raw=raw, path=path, line=line, status="H", reason="File Not Readable")
    if binary:
        return TagResult(
            raw=raw, path=path, line=line, status="H",
            reason="Binary File - line citation not verifiable by a text oracle",
        )

    if line < 1:
        return TagResult(raw=raw, path=path, line=line, status="H", reason="Line Out of Bounds")

    eof = _file_line_count(resolved)
    if eof is None:
        return TagResult(raw=raw, path=path, line=line, status="H", reason="File Not Found")
    if line > eof:
        return TagResult(raw=raw, path=path, line=line, status="H", reason="Line Out of Bounds")

    return TagResult(raw=raw, path=path, line=line, status="V", reason="")


def verify_report(report_path: Path, evidence_root: Path) -> ReportFingerprint:
    text = report_path.read_text(encoding="utf-8", errors="replace")
    results: list[TagResult] = []
    for m in TAG_RE.finditer(text):
        path = m.group(1).strip()
        line = int(m.group(2))
        results.append(verify_tag(path, line, evidence_root))

    malformed = len(BARE_V_RE.findall(text))
    total = len(results) + malformed
    verified = sum(1 for r in results if r.status == "V")
    hallucinated = total - verified
    accuracy = (verified / total * 100.0) if total else 0.0

    return ReportFingerprint(
        report_path=str(report_path),
        total=total,
        verified=verified,
        hallucinated=hallucinated,
        accuracy_pct=round(accuracy, 2),
        i_tags=len(I_TAG_RE.findall(text)),
        h_tags=len(H_TAG_RE.findall(text)),
        malformed_v=malformed,
        tag_results=results,
    )


def rewrite_report(report_path: Path, fingerprint: ReportFingerprint, suffix: str = ".verified.md") -> Path:
    """Rewrite the report with [H] downgrades applied to each tag occurrence.

    Each [V path:line] that failed verification becomes
    [H path:line] (reason). [V] tags stay verbatim.
    """
    text = report_path.read_text(encoding="utf-8", errors="replace")
    failures = {(r.path, r.line): r.reason for r in fingerprint.tag_results if r.status == "H"}

    def _sub(m: re.Match[str]) -> str:
        path = m.group(1).strip()
        line = int(m.group(2))
        reason = failures.get((path, line))
        if reason:
            return f"[H {path}:{line}] ({reason})"
        return m.group(0)

    new_text = TAG_RE.sub(_sub, text)
    out = report_path.with_suffix(suffix)
    out.write_text(new_text, encoding="utf-8")
    return out


def render_fingerprint_table(fingerprints: Iterable[ReportFingerprint]) -> str:
    rows = ["| Report | V-total | Verified | Hallucinated | Accuracy % | [I] | [H] |",
            "|---|---:|---:|---:|---:|---:|---:|"]
    total = verified = hallucinated = i_tags = h_tags = 0
    for fp in fingerprints:
        rows.append(
            f"| {fp.report_path} | {fp.total} | {fp.verified} | {fp.hallucinated} | {fp.accuracy_pct:.2f} | {fp.i_tags} | {fp.h_tags} |"
        )
        total += fp.total
        verified += fp.verified
        hallucinated += fp.hallucinated
        i_tags += fp.i_tags
        h_tags += fp.h_tags
    consolidated_acc = (verified / total * 100.0) if total else 0.0
    rows.append(
        f"| **Consolidated** | {total} | {verified} | {hallucinated} | {consolidated_acc:.2f} | {i_tags} | {h_tags} |"
    )
    return "\n".join(rows)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Sovereign-Gauntlet evidence verifier")
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--report", type=Path, help="Single lens report to verify")
    src.add_argument("--reports-dir", type=Path, help="Directory of lens reports (*.md)")
    p.add_argument("--evidence-root", type=Path, required=True,
                   help="Root against which relative [V path:line] paths resolve")
    p.add_argument("--rewrite", action="store_true",
                   help="Emit a <report>.verified.md with [H] downgrades applied")
    p.add_argument("--json", action="store_true",
                   help="Emit machine-readable JSON to stdout (in addition to the table)")
    args = p.parse_args(argv)

    if not args.evidence_root.exists():
        print(f"ERROR: --evidence-root not found: {args.evidence_root}", file=sys.stderr)
        return 2

    reports: list[Path] = []
    if args.report:
        if not args.report.exists():
            print(f"ERROR: report not found: {args.report}", file=sys.stderr)
            return 2
        reports = [args.report]
    else:
        if not args.reports_dir.exists():
            print(f"ERROR: reports-dir not found: {args.reports_dir}", file=sys.stderr)
            return 2
        reports = sorted(args.reports_dir.glob("*.md"))
        if not reports:
            print(f"ERROR: no *.md reports in {args.reports_dir}", file=sys.stderr)
            return 2

    fingerprints = [verify_report(r, args.evidence_root) for r in reports]

    print("# Sovereign Fingerprint\n")
    print(render_fingerprint_table(fingerprints))
    print()

    if args.rewrite:
        for r, fp in zip(reports, fingerprints):
            out = rewrite_report(r, fp)
            print(f"rewrote: {out}")

    if args.json:
        payload = [
            {**asdict(fp), "tag_results": [asdict(t) for t in fp.tag_results]}
            for fp in fingerprints
        ]
        print("\n--- JSON ---")
        print(json.dumps(payload, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
