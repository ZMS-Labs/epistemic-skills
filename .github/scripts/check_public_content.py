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
import hashlib
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

# Allowlist: EXACT files only (es#186 / panel-1 SK-4 — the old whole-file
# PREFIX exemptions meant any future file parked under a receipt-ish name
# would ship uninspected for every class; exact files make every exemption
# a visible, reviewable act), each bound to the sha256 OF ITS CONTENT AT
# EXEMPTION TIME (gauntlet ruling R11, es-v6-candidate-freeze-2026-08-18:
# an exemption without a digest exempts every FUTURE state of the file, so
# new private strings could ride into an already-allowlisted path without
# review). The gate fails closed when an allowlisted file's bytes differ
# from the recorded digest: re-review the file and update the digest in the
# same commit, or the exemption does not apply. An entry whose file is
# absent from this branch is dormant (it exempts nothing here; the digest
# binds the moment the file lands, e.g. via a cross-branch record merge).
#
# Ownership and cadence (R11d): the repository operator owns this list;
# entries are re-reviewed at every release's public-content review step
# (RELEASING.md) and any stale-digest failure forces an immediate review.
# 2026-08-18: four inert entries retired (5.0.0-era review receipts with
# zero pattern hits on the current tree — they exempted nothing).
#
# Rationale per entry:
#   - "review receipt": historical release-review records that intentionally
#     document the scrub vocabulary (and, for the 2026-07-17 review, the
#     operator DCO email — public git-history floor).
#   - "self": this script quotes its own pattern vocabulary. Digest None:
#     a file cannot embed its own sha256; the script is reviewed as code in
#     every diff that touches it.
#   - "disposition record": the v5.1.0 full-window review (RELEASE-5.1.0.md)
#     and its committed gauntlet record name the disclosed strings — the same
#     purpose the review receipts serve.
#   - "dispositioned fixture": custody guard fixtures/tests exercising
#     path-scoping rules with private-range literals; accepted in the v5.1.0
#     record, no credential accompanies any occurrence.
#   - "pre-gate historical record": plan/spec/audit/handoff documents that
#     carried the operator DCO email (public git-history floor) or custody
#     design literals before this gate existed. The gate is forward-looking
#     for this class; editing these files does NOT re-expose anything not
#     already immutable in git history.
ALLOWLIST_EXACT_FILES: dict[str, tuple[str, str | None]] = {
    "docs/release/PUBLIC-RELEASE-REVIEW-2026-07-17.md": ("review receipt", "8420cb7dbfc0ab486d2d76b91f89242d8e35e7288574b995148567ab39999891"),
    "docs/release/PUBLIC-RELEASE-REVIEW-ADDENDUM-2026-07-21.md": ("review receipt", "8c60bde388cc716ada8b9147053723876aa7def84a24f85aa7bf012f3892f159"),
    ".github/scripts/check_public_content.py": ("self (quotes its own pattern vocabulary)", None),
    "docs/release/RELEASE-5.1.0.md": ("disposition record (names the disclosed strings)", "731eab7452519b2e93034a9e924f4b56263f15c29bde527f1c09fb396e3dc2cc"),
    "docs/gauntlet-runs/es-v510-publication-2026-08-15/arbitration.md": ("disposition record", "9413ff64a547be38f4a88d0b057b01e027b6a9aea87bdb3377d79ebea7a173ef"),
    "docs/gauntlet-runs/es-v510-publication-2026-08-15/reports/script-kiddie.md": ("disposition record", "25af88208a4b59b08bc06fff80a590bb454b25afc350ca58fdaad11b51a80333"),
    "plugins/epistemic-skills/contracts/mission-custody/examples/valid-manifest-guards.json": ("dispositioned fixture", "595e586d3da23c63f3bcebced94c3d4a78adb926348e1984a99feb6fe056f966"),
    "plugins/epistemic-skills/contracts/mission-custody/examples/invalid-manifest-guard-bad-mode.json": ("dispositioned fixture", "d92a3ccfc054d0879592d2303d62aa8c8d5881f80ee7eee13d7f488b571d8317"),
    "plugins/epistemic-skills/contracts/mission-custody/examples/invalid-manifest-guard-bad-regex.json": ("dispositioned fixture", "f2d2967ca8b12ab95816287f12b8bf0b84b9baabe75a2c751b06e02e4ba297db"),
    "plugins/epistemic-skills/contracts/mission-custody/examples/invalid-manifest-guard-empty-rule.json": ("dispositioned fixture", "80dcaaceac508adfb5c02fc0b83849d1e584f3892a1f510485d1ece395faee26"),
    "plugins/epistemic-skills/contracts/mission-custody/examples/invalid-manifest-guard-unknown-field.json": ("dispositioned fixture", "13769cffbccb9e4d49602938d01dd34b310772ab1d60d0a7ac23ccdc23e3316e"),
    "plugins/epistemic-skills/contracts/mission-custody/test_custody_gate.py": ("dispositioned fixture", "f87e8cf14256c5f332572545f9ded71602fb227544cb56769cc80766aec5f984"),
    "docs/superpowers/plans/2026-08-12-stage-c-custody-hook.md": ("pre-gate historical record", "c0e6b949fcc34e498dd3b1af25beb42c17e52f28c84a32f92beb35c04c438fe6"),
    "docs/superpowers/specs/2026-08-12-stage-c-custody-hook-design.md": ("pre-gate historical record", "cc6ba6f53b172178124e3fde706dd6fa0ce6231ef105e9e14130d174c5b2854c"),
    "docs/audits/2026-07-23-suite-stress-test/08-changes-and-verification.md": ("pre-gate historical record", "aa1ec0490d028a56a8376cb9176d7ef2b8687373d0e1be987206989f3c3fd05b"),
    "docs/audits/2026-07-23-suite-stress-test/09-final-verification.md": ("pre-gate historical record", "23c7bab9eda7f1602ad49eaf7706128e442e2b47e53680bfe938509df80f53eb"),
    "docs/gauntlet-runs/epistemic-flexibility-v3-2026-07-22/arbitration.json": ("pre-gate historical record", "6aa9c9da2ce77de967bf480b728927b5c2f75f745eadbaf71a33bb47bf9cb24e"),
    "docs/gauntlet-runs/epistemic-flexibility-v3-2026-07-22/dossier.md": ("pre-gate historical record", "5ff434be25b053f420bbc9cb5c3299ae13871bb6c6d440b350326d9368bbfb52"),
    "docs/gauntlet-runs/epistemic-flexibility-v3-2026-07-22/reports/compliance-litigator.json": ("pre-gate historical record", "2d5687c433f36f14316d34b3b4911292d23990ad201a89c6d1db64ce9a44e898"),
    "docs/gauntlet-runs/epistemic-flexibility-v3-2026-07-22/workflow-result.json": ("pre-gate historical record", "69e54ef33066ed43221b5e4930c68720460d0f81b0e68678adecb7e961deb4c2"),
    "docs/gauntlet-runs/upgrades-landing-2026-08-03/arbitration.md": ("pre-gate historical record", "7122588feadb9ac54c5054ef3d9ce160d8f0022628b129e88b870f9bd3d8f641"),
    "docs/gauntlet-runs/upgrades-landing-2026-08-03/evidence/commits.txt": ("pre-gate historical record", "2958df43bbcfe248168e8e26a05e27b745f6e58efc7d9109c8a661ce9e992004"),
    "docs/gauntlet-runs/upgrades-landing-2026-08-03/evidence/dco-check.txt": ("pre-gate historical record", "a80820988848a4adec2f11d582c5c5b2498c5130019fba24c1408df685ef7d96"),
    "docs/gauntlet-runs/upgrades-landing-2026-08-03/reports/decision-rights-auditor.md": ("pre-gate historical record", "e5e400885977a3dbe394a420f9b93597336c172d25dac87d959d1f87cf2820d4"),
    "docs/gauntlet-runs/upgrades-landing-2026-08-03/reports/disgruntled-maintainer.md": ("pre-gate historical record", "620b2ce4433ddefdec54d35e5cefd7ee7e2d2278e82fe6befd1d15f7d0e2d197"),
    "docs/gauntlet-runs/upgrades-landing-2026-08-03/reports/ecological-systems-analyst.md": ("pre-gate historical record", "dcefefe11e279aaceb922e7ca107ad75f403138a4d25b1ff0acae53eaa416919"),
    "docs/outsource/epistemic-skills-pr43-readonly-review/HANDOFF.md": ("pre-gate historical record", "c0ada1ded21bce898dc148b23e7d43475cccf3360685caf6dd87e1968453fcfd"),
    "docs/outsource/epistemic-skills-suite-stress-test/HANDOFF.md": ("pre-gate historical record", "0d1a3e5947f8ad934822a44cfe0094f297dafd8bb10f50fee318d1aad5153569"),
    "docs/superpowers/plans/2026-07-29-open-questions.md": ("pre-gate historical record", "57ab46785471caf73beb04ff97c5c8c60f358447e3e704f3cc33ece0e7f65916"),
    "docs/superpowers/plans/2026-08-06-openai-plugin-bundles.md": ("pre-gate historical record", "c044618d4d1d14d8a6a20a804782da1e32a78c2657a0985e4da666482952c57d"),
    "docs/superpowers/plans/2026-08-07-commission-watch-clarification.md": ("pre-gate historical record", "f48b87307de7ed6972996c05aa42ab8064a077f026c3099c6638cd1c81920f1a"),
    "docs/superpowers/plans/2026-08-07-practical-agency-bootstrap.md": ("pre-gate historical record", "89b220240d8e1d79669e9e8ce04e51a9edc8be65fe3888c8f62875aa15693fe6"),
    "docs/superpowers/plans/2026-08-11-mission-custody-contracts.md": ("pre-gate historical record", "ec4eea32e2e6448103b6c730dd6f7e0008618895f09a446fcfd79c214b6d760b"),
    "docs/superpowers/specs/2026-08-07-practical-agency-and-commission-watch-design.md": ("pre-gate historical record", "29c4601b17375a618821ab38b25c5449e6591e641f4dc1f14551eba4807b1db9"),
    "docs/wiki-updates/v4.0.0/v4.0.0-wiki-update.patch": ("pre-gate historical record", "5ce514bfbe9066e38ec606c202f57259061cbd804c6331e5cc868d512d01c548"),
    # Independent-gauntlet run record that quotes the scrub vocabulary as
    # review-trail evidence (operator decision D7: exact-file allowlist, no
    # scrub — the dossier pin and seat-binding hash chain stay intact).
    # REMOVED 2026-08-20: the gauntlet-run dossier no longer needs an
    # exemption. Its three occurrences of the private fleet repo name were
    # redacted when the verdict lineage came in-tree, so the file now hits
    # zero patterns and the allowlist narrows by one. That panel's own P1
    # was that this class should be REMEDIATED rather than allowlisted;
    # this is that disposition applied to the record of the finding.
    "docs/v6/ES6-ZI-001/exact-start-receipt.json": ("v6 program parent tracker coordinate", "8ce838da0f9a32756d2ea0d5a7fd2cdc65447562e16a6b122a9307d8038e8154"),
    ".github/scripts/v6_generate_baseline_claims.py": ("v6 program parent tracker coordinate", "7296a40a03985ddfe2a9c1c83759074daba50888cd6fc4165a515f2d300bee8b"),
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
    return rel in ALLOWLIST_EXACT_FILES


def allowlist_defects(path: Path, data: bytes) -> list[str]:
    """Digest guard (R11): an exemption applies only to the exempted bytes."""
    rel = path.relative_to(REPO_ROOT).as_posix()
    _, recorded = ALLOWLIST_EXACT_FILES[rel]
    if recorded is None:  # the self entry: a file cannot embed its own hash
        return []
    actual = hashlib.sha256(data).hexdigest()
    if actual != recorded:
        return [
            f"allowlist-stale: {rel} changed since exemption "
            f"(recorded {recorded[:12]}…, actual {actual[:12]}…) — re-review the "
            "file and update the recorded digest in the same commit"
        ]
    return []


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
    present_allowlisted = 0
    for path in tracked_files():
        if not path.is_file():
            continue
        if is_allowlisted(path):
            present_allowlisted += 1
            defects.extend(allowlist_defects(path, path.read_bytes()))
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
    dormant = len(ALLOWLIST_EXACT_FILES) - present_allowlisted
    print(
        "public-content gate ok: "
        f"{len(PATTERNS)} patterns, {present_allowlisted} allowlisted exact files "
        f"digest-verified ({dormant} dormant entries name files absent from this branch)"
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

    # Prefix-wedge control (SK-4): a NEW file under a formerly prefix-exempt
    # name shape must be REJECTED — exemptions are exact-file, not by name shape.
    wedge = scan_text(
        REPO_ROOT / "docs/release/PUBLIC-RELEASE-REVIEW-2099-01-01.md",
        "Patterns swept: private-repo name (`zms-homelab`)",
    )
    if not wedge:
        failures.append("new file under a former prefix shape was NOT rejected (prefix wedge open)")

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

    # Digest guard (R11): planted TAMPERED bytes at an allowlisted path must
    # fail closed; the file's true bytes must verify; the self entry (digest
    # None) must not be asked to hash itself.
    digested = REPO_ROOT / "docs/release/RELEASE-5.1.0.md"
    stale = allowlist_defects(digested, b"tampered content that was never reviewed")
    if not any(d.startswith("allowlist-stale") for d in stale):
        failures.append("planted tampered allowlisted file was NOT rejected (digest guard inert)")
    fresh = allowlist_defects(digested, digested.read_bytes())
    if fresh:
        failures.append(f"true bytes of an allowlisted file failed the digest guard: {fresh}")
    self_entry = allowlist_defects(
        REPO_ROOT / ".github/scripts/check_public_content.py", b"any bytes"
    )
    if self_entry:
        failures.append(f"self entry (digest None) wrongly produced defects: {self_entry}")

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
