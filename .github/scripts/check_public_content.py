#!/usr/bin/env python3
"""Fail-closed public-content pattern gate for exact release candidates.

Drift disease this prevents: treating a green credential scan as proof that the
public tree contains no private-fleet topology. The July 21 public-release
addendum already classified private-repository identifiers and user-specific
local paths as scrub targets. Those strings need not look like secrets.

This check scans the tracked tree for a narrow, seeded pattern set and fails
closed on any hit outside an explicit allowlist of historical review receipts
that intentionally document the scrub vocabulary.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# Patterns drawn from docs/release/PUBLIC-RELEASE-REVIEW-ADDENDUM-2026-07-21.md
# and the v5.1.0 publication gauntlet (docs/gauntlet-runs/es-v510-publication-
# 2026-08-15, panel-1 SK-2: the original four patterns could not see the
# RFC1918/UNC/email classes item 6 enumerates, and the full-window review had
# to catch them by hand). Keep the list small and reasoned. Each entry must
# have a RED seed below.
PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("private-fleet-repo-name", re.compile(r"\bzms-homelab\b", re.I)),
    # Windows user homes in either slash form.
    ("windows-user-path", re.compile(r"[A-Za-z]:[\\/]Users[\\/][A-Za-z0-9._-]+", re.I)),
    # POSIX user homes. Negative lookbehind avoids matching the `/Users/`
    # substring inside `C:/Users/...`.
    ("posix-user-path", re.compile(r"(?<![A-Za-z:])/Users/[A-Za-z0-9._-]+/")),
    ("y-drive-private-checkout", re.compile(r"[Yy]:[/\\]dev[/\\]zms-homelab", re.I)),
    # Internal-network topology (es#186 / panel-1 SK-2). RFC1918 ranges only:
    # internet-facing hosts have legitimate public IPs and must not trip this.
    ("rfc1918-address", re.compile(
        r"\b(?:10\.\d{1,3}|192\.168|172\.(?:1[6-9]|2\d|3[01]))\.\d{1,3}\.\d{1,3}\b")),
    # SMB share paths whose host is an IP, either slash form
    # (`\\10.0.0.5\share` / `//10.0.0.5/share`). The lookbehind excludes
    # URL schemes (`http://...`); bare IPs inside URLs are the pattern above's
    # job.
    ("unc-ip-share", re.compile(
        r"(?<!:)(?:\\\\|//)(?:\d{1,3}\.){3}\d{1,3}[\\/][A-Za-z0-9._$-]+")),
    # Personal-data class: any real-looking email address. Synthetic RFC
    # example addresses are neutralized before scanning (see scan_text).
    ("email-address", re.compile(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
]

# Files that must remain able to name the scrub vocabulary so the review trail
# stays intelligible. Hits elsewhere fail closed.
ALLOWLIST_PREFIXES = (
    "docs/release/PUBLIC-RELEASE-REVIEW-",
    "docs/release/PUBLIC-CONTENT-POST-RELEASE-REVIEW-",
    "docs/release/RELEASE-5.0.0-ERRATA-",
    "docs/release/POST-RELEASE-INDEPENDENT-REVIEW-",
    "docs/release/V5.0.0-DESIGN-CONFORMANCE-",
    ".github/scripts/check_public_content.py",
)

# Exact-file exemptions for content that predates these pattern classes or is
# itself the disposition record. EXACT files, never prefixes: a new file at a
# different path still fails closed, and adding a file here is a visible,
# reviewable act. Rationale per entry:
#   - "disposition record": the v5.1.0 full-window review (RELEASE-5.1.0.md)
#     and its committed gauntlet record name the disclosed strings — the same
#     purpose the review-receipt prefixes serve.
#   - "dispositioned fixture": custody guard fixtures/tests exercising
#     path-scoping rules with private-range literals; accepted in the v5.1.0
#     record, no credential accompanies any occurrence.
#   - "pre-gate historical record": plan/spec/audit/handoff documents that
#     carried the operator DCO email (public git-history floor) or custody
#     design literals before this gate existed. The gate is forward-looking
#     for this class; editing these files does NOT re-expose anything not
#     already immutable in git history.
ALLOWLIST_EXACT_FILES = {
    # disposition record
    "docs/release/RELEASE-5.1.0.md": "disposition record (names the disclosed strings)",
    "docs/gauntlet-runs/es-v510-publication-2026-08-15/arbitration.md": "disposition record",
    "docs/gauntlet-runs/es-v510-publication-2026-08-15/reports/script-kiddie.md": "disposition record",
    # dispositioned fixtures (v5.1.0 full-window review)
    "plugins/epistemic-skills/contracts/mission-custody/examples/valid-manifest-guards.json": "dispositioned fixture",
    "plugins/epistemic-skills/contracts/mission-custody/examples/invalid-manifest-guard-bad-mode.json": "dispositioned fixture",
    "plugins/epistemic-skills/contracts/mission-custody/examples/invalid-manifest-guard-bad-regex.json": "dispositioned fixture",
    "plugins/epistemic-skills/contracts/mission-custody/examples/invalid-manifest-guard-empty-rule.json": "dispositioned fixture",
    "plugins/epistemic-skills/contracts/mission-custody/examples/invalid-manifest-guard-unknown-field.json": "dispositioned fixture",
    "plugins/epistemic-skills/contracts/mission-custody/test_custody_gate.py": "dispositioned fixture",
    # pre-gate historical records
    "docs/superpowers/plans/2026-08-12-stage-c-custody-hook.md": "pre-gate historical record",
    "docs/superpowers/specs/2026-08-12-stage-c-custody-hook-design.md": "pre-gate historical record",
    "docs/audits/2026-07-23-suite-stress-test/08-changes-and-verification.md": "pre-gate historical record",
    "docs/audits/2026-07-23-suite-stress-test/09-final-verification.md": "pre-gate historical record",
    "docs/gauntlet-runs/epistemic-flexibility-v3-2026-07-22/arbitration.json": "pre-gate historical record",
    "docs/gauntlet-runs/epistemic-flexibility-v3-2026-07-22/dossier.md": "pre-gate historical record",
    "docs/gauntlet-runs/epistemic-flexibility-v3-2026-07-22/reports/compliance-litigator.json": "pre-gate historical record",
    "docs/gauntlet-runs/epistemic-flexibility-v3-2026-07-22/workflow-result.json": "pre-gate historical record",
    "docs/gauntlet-runs/upgrades-landing-2026-08-03/arbitration.md": "pre-gate historical record",
    "docs/gauntlet-runs/upgrades-landing-2026-08-03/evidence/commits.txt": "pre-gate historical record",
    "docs/gauntlet-runs/upgrades-landing-2026-08-03/evidence/dco-check.txt": "pre-gate historical record",
    "docs/gauntlet-runs/upgrades-landing-2026-08-03/reports/decision-rights-auditor.md": "pre-gate historical record",
    "docs/gauntlet-runs/upgrades-landing-2026-08-03/reports/disgruntled-maintainer.md": "pre-gate historical record",
    "docs/gauntlet-runs/upgrades-landing-2026-08-03/reports/ecological-systems-analyst.md": "pre-gate historical record",
    "docs/outsource/epistemic-skills-pr43-readonly-review/HANDOFF.md": "pre-gate historical record",
    "docs/outsource/epistemic-skills-suite-stress-test/HANDOFF.md": "pre-gate historical record",
    "docs/superpowers/plans/2026-07-29-open-questions.md": "pre-gate historical record",
    "docs/superpowers/plans/2026-08-06-openai-plugin-bundles.md": "pre-gate historical record",
    "docs/superpowers/plans/2026-08-07-commission-watch-clarification.md": "pre-gate historical record",
    "docs/superpowers/plans/2026-08-07-practical-agency-bootstrap.md": "pre-gate historical record",
    "docs/superpowers/plans/2026-08-11-mission-custody-contracts.md": "pre-gate historical record",
    "docs/superpowers/specs/2026-08-07-practical-agency-and-commission-watch-design.md": "pre-gate historical record",
    "docs/wiki-updates/v4.0.0/v4.0.0-wiki-update.patch": "pre-gate historical record",
}


def tracked_files() -> list[Path]:
    result = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "ls-files", "-z"],
        check=True,
        capture_output=True,
    )
    return [REPO_ROOT / rel for rel in result.stdout.decode("utf-8").split("\0") if rel]


def is_allowlisted(path: Path) -> bool:
    rel = path.relative_to(REPO_ROOT).as_posix()
    if rel in ALLOWLIST_EXACT_FILES:
        return True
    return any(rel.startswith(prefix) or rel == prefix for prefix in ALLOWLIST_PREFIXES)


def scan_text(path: Path, text: str) -> list[str]:
    defects: list[str] = []
    if is_allowlisted(path):
        return defects
    rel = path.relative_to(REPO_ROOT).as_posix()
    # Synthetic RED-seed usernames and RFC example emails used by package
    # tests/docs (not real operator data).
    sanitized = re.sub(r"([A-Za-z]:[\\/]Users[\\/]|/Users/)example\b", r"\1<synthetic>", text, flags=re.I)
    sanitized = re.sub(
        r"\b[A-Za-z0-9._%+-]+@example\.(?:com|org|net|test)\b",
        "<synthetic-email>",
        sanitized,
        flags=re.I,
    )
    for name, pattern in PATTERNS:
        if pattern.search(sanitized):
            defects.append(f"{name}: {rel}")
    return defects


def run_check() -> int:
    defects: list[str] = []
    for path in tracked_files():
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        defects.extend(scan_text(path, text))
    if defects:
        for defect in defects:
            print(f"public-content defect: {defect}", file=sys.stderr)
        return 1
    print(
        "public-content gate ok: "
        f"{len(PATTERNS)} patterns, {len(ALLOWLIST_PREFIXES)} allowlist prefixes, "
        f"{len(ALLOWLIST_EXACT_FILES)} allowlisted exact files"
    )
    return 0


def run_self_test() -> int:
    failures: list[str] = []
    seeds = {
        "private-fleet-repo-name": "see also ZMS-Labs/zms-homelab for fleet overlays",
        "windows-user-path": r"probe under C:\Users\example\.claude\skills",
        "posix-user-path": "probe under /Users/example/.claude/skills",
        "y-drive-private-checkout": r"checkout at Y:\dev\zms-homelab-main",
        "rfc1918-address": "the service answers on 10.10.10.50 today",
        "unc-ip-share": r"media lives at \\10.10.10.107\Media and //10.10.10.107/Media",
        "email-address": "reach the operator at z.stern@personalmailbox.org",
    }
    for expected, blob in seeds.items():
        hits = []
        for name, pattern in PATTERNS:
            if pattern.search(blob):
                hits.append(name)
        if expected not in hits:
            failures.append(f"seeded {expected} was not detected in {blob!r}: {hits}")

    # Allowlisted historical review text must not fail the check when scanned alone.
    allowlisted = scan_text(
        REPO_ROOT / "docs/release/PUBLIC-RELEASE-REVIEW-ADDENDUM-2026-07-21.md",
        "Patterns swept: private-repo name (`zms-homelab`)",
    )
    if allowlisted:
        failures.append(f"allowlisted review text was rejected: {allowlisted}")

    # Allowlisted EXACT files (disposition records/fixtures) must pass; the
    # same content at a NON-allowlisted path must fail (exact-file semantics:
    # the exemption is bound to the path, not the content).
    exact_hit = scan_text(
        REPO_ROOT / "docs/release/RELEASE-5.1.0.md",
        "the endpoint was http://10.10.10.50:7878/api/v3/series",
    )
    if exact_hit:
        failures.append(f"allowlisted exact file was rejected: {exact_hit}")
    exact_miss = scan_text(
        REPO_ROOT / "docs/some-new-file.md",
        "the endpoint was http://10.10.10.50:7878/api/v3/series",
    )
    if not exact_miss:
        failures.append("non-allowlisted path with identical content was NOT rejected (exact-file semantics broken)")

    # Synthetic example emails must not trip the email pattern in tree scans.
    synthetic = scan_text(REPO_ROOT / "docs/some-new-file.md", "contact us at maintainer@example.com anytime")
    if synthetic:
        failures.append(f"synthetic example email was rejected: {synthetic}")

    if failures:
        for failure in failures:
            print(f"SELF-TEST FAILURE: {failure}", file=sys.stderr)
        return 1
    print(f"public-content self-test ok: {len(seeds)} seeded RED controls passed")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        return run_self_test()
    return run_check()


if __name__ == "__main__":
    raise SystemExit(main())
