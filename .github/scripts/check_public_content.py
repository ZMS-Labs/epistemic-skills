#!/usr/bin/env python3
"""Check publishable text for personal data and machine-specific coordinates.

All tracked and non-ignored new files are inspected. Historical records have no
exemption: public copies use synthetic identifiers and keep redaction provenance
in docs/public-content-redactions.json. This checks current-tree text, not Git
history, and does not replace credential scanning or contextual review.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ('windows-user-path', re.compile(r'[A-Za-z]:[\\/]+Users[\\/]+[A-Za-z0-9._-]+', re.I)),
    ('posix-user-path', re.compile(r'(?<![A-Za-z:])/(?:Users|home)/[A-Za-z0-9._-]+/')),
    ('local-development-root', re.compile(r'\b[A-Za-z]:[\\/]+dev(?:[\\/]|\b)', re.I)),
    ('rfc1918-address', re.compile(r'\b(?:10\.\d{1,3}|192\.168|172\.(?:1[6-9]|2\d|3[01]))\.\d{1,3}\.\d{1,3}\b')),
    ('unc-ip-share', re.compile(r'(?<!:)(?:\\\\|//)(?:\d{1,3}\.){3}\d{1,3}[\\/][A-Za-z0-9._$-]+')),
    ('email-address', re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b')),
    ('build-host-scratch-path', re.compile(r'/tmp/claude-\d+/')),
    ('internal-domain', re.compile(r'(?:\b[\w-]+|\*)?\.internal\.[a-z][a-z0-9.-]*', re.I)),
    ('device-hostname', re.compile(r'\b[a-z]{2,8}-pc-\d{4}\b', re.I)),
]


def tracked_files(root: Path = REPO_ROOT) -> list[Path]:
    result = subprocess.run(
        ['git', '-C', str(root), 'ls-files', '-z', '--cached', '--others', '--exclude-standard'],
        check=True, capture_output=True,
    )
    return [root / rel for rel in dict.fromkeys(result.stdout.decode('utf-8').split('\0')) if rel]


def scan_text(path: Path, text: str) -> list[str]:
    # Only explicitly fictional examples are exempt, never entire files.
    sanitized = re.sub(r'([A-Za-z]:[\\/]+Users[\\/]+|/(?:Users|home)/)example\b', r'\1<example>', text, flags=re.I)
    sanitized = re.sub(r'\b[A-Za-z0-9._%+-]+@example\.(?:com|org|net|test)\b', '<example-email>', sanitized, flags=re.I)
    # Existing path-parser fixtures use this deliberately synthetic location.
    sanitized = sanitized.replace('D:' + '/dev/thing', '<example-path>')
    # RFC 5737 documentation ranges are examples, not private topology.
    sanitized = re.sub(r'\b(?:192\.0\.2|198\.51\.100|203\.0\.113)\.\d{1,3}\b', '<example-address>', sanitized)
    rel = path.relative_to(REPO_ROOT).as_posix()
    return [f'{name}: {rel}' for name, pattern in PATTERNS if pattern.search(sanitized)]


def run_check() -> int:
    defects: list[str] = []
    count = 0
    for path in tracked_files():
        if path.is_symlink() or not path.is_file():
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            continue
        count += 1
        defects.extend(scan_text(path, text))
    for defect in defects:
        print(f'public-content defect: {defect}', file=sys.stderr)
    if defects:
        return 1
    print(f'public-content gate ok: {count} text files, {len(PATTERNS)} patterns, no whole-file exemptions')
    return 0


def run_self_test() -> int:
    import tempfile
    failures: list[str] = []
    # Construct private-shaped seeds so the checker can scan its own source.
    address = '.'.join(['10', '42', '7', '9'])
    seeds = {
        'windows-user-path': 'C:' + '/Users/' + 'fixture-person/private',
        'posix-user-path': '/home/' + 'fixture-person/private',
        'local-development-root': 'Q:' + '/dev/fixture-project',
        'rfc1918-address': 'https://' + address + '/api',
        'unc-ip-share': '//' + address + '/share',
        'email-address': 'fixture-person@' + 'private.invalid',
        'build-host-scratch-path': '/tmp/' + 'claude-7/session',
        'internal-domain': 'service.internal.' + 'invalid',
        'device-hostname': 'abc-pc-' + '2099',
    }
    assert set(seeds) == {name for name, _ in PATTERNS}
    for expected, blob in seeds.items():
        for rel in ('docs/new.md', 'docs/release/PUBLIC-RELEASE-REVIEW-2026-07-17.md', '.github/scripts/check_public_content.py'):
            hits = scan_text(REPO_ROOT / rel, blob)
            if not any(hit.startswith(expected + ':') for hit in hits):
                failures.append(f'{expected} not detected at {rel}')
    allowed = [
        'maintainer@example.org', 'C:/Users/example/project',
        r'C:\\Users\\example\\project', '/home/example/project',
        '//192.0.2.10/share', 'https://example.invalid/api', '/workspace/project',
    ]
    for blob in allowed:
        if scan_text(REPO_ROOT / 'examples/synthetic.md', blob):
            failures.append('synthetic example rejected')
    if not scan_text(REPO_ROOT / 'examples/synthetic.md', allowed[0] + ' ' + seeds['email-address']):
        failures.append('mixed synthetic/private content was accepted')
    # Both tracked and new files must be inspected, excluding local output.
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        subprocess.run(['git', 'init', '-q', str(root)], check=True, capture_output=True)
        (root / '.gitignore').write_text('local/\n', encoding='utf-8')
        (root / 'tracked.md').write_text('example', encoding='utf-8')
        subprocess.run(['git', '-C', str(root), 'add', '.gitignore', 'tracked.md'], check=True, capture_output=True)
        (root / 'new.md').write_text(seeds['email-address'], encoding='utf-8')
        (root / 'local').mkdir()
        (root / 'local/private.md').write_text('local', encoding='utf-8')
        found = {p.relative_to(root).as_posix() for p in tracked_files(root)}
        if found != {'.gitignore', 'tracked.md', 'new.md'}:
            failures.append('publishable-file discovery failed')
    for failure in failures:
        print(f'SELF-TEST FAILURE: {failure}', file=sys.stderr)
    if failures:
        return 1
    print(f'public-content self-test ok: {len(seeds)} seeded controls; historical/self-file coverage, synthetic examples and file discovery')
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args(argv)
    return run_self_test() if args.self_test else run_check()


if __name__ == '__main__':
    raise SystemExit(main())
