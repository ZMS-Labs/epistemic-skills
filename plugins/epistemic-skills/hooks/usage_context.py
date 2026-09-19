#!/usr/bin/env python3
"""Emit canonical usage instructions through verified SessionStart contracts.

No session ledger: replaying a lifecycle event must remain safe after context
loss. Fingerprints expose duplicate/mixed copies without guessing host memory.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys

MAX_BODY_BYTES = 65536
SOURCES = {'codex': {'startup', 'resume', 'clear', 'compact'},
           'claude': {'startup', 'resume', 'clear', 'compact', 'fork'}}
FALLBACK = ('Epistemic usage delivery unavailable. Explicitly load the current '
            'skills/epistemic/SKILL.md from the selected installation before '
            'claiming its use. using-epistemic-skills maps to epistemic in '
            'documentation only; do not assume native alias support.')


def load_usage_context(plugin_root: Path) -> str:
    path = plugin_root / 'skills' / 'epistemic' / 'SKILL.md'
    with path.open('rb') as stream:
        body = stream.read(MAX_BODY_BYTES + 1)
    if len(body) > MAX_BODY_BYTES:
        raise ValueError('canonical usage body exceeds delivery bound')
    text = body.decode('utf-8')
    if not text.strip():
        raise ValueError('canonical usage body is empty')
    return text


def render(plugin_root: Path, harness: str, payload: dict,
           expected_sha256: str | None = None) -> dict:
    if payload.get('hook_event_name') != 'SessionStart' or payload.get('source') not in SOURCES[harness]:
        raise ValueError('unsupported lifecycle event/source')
    versions = set()
    for directory in ('.claude-plugin', '.codex-plugin'):
        manifest = plugin_root / directory / 'plugin.json'
        if manifest.is_file():
            version = json.loads(manifest.read_text(encoding='utf-8')).get('version')
            if version:
                versions.add(version)
    if len(versions) > 1:
        raise ValueError('installed host manifest versions disagree')
    body = load_usage_context(plugin_root)
    digest = hashlib.sha256(body.encode('utf-8')).hexdigest()
    if expected_sha256 and digest != expected_sha256:
        raise ValueError('canonical usage fingerprint differs from selected source')
    context = (f'[epistemic-usage sha256={digest}]\n'
               'Reuse identical usage guidance already in context; do not repeat its '
               'acknowledgment. If fingerprints disagree, explicitly select the current '
               'installation before relying on either copy.\n' + body)
    return {'hookSpecificOutput': {'hookEventName': 'SessionStart',
                                  'additionalContext': context}}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--harness', choices=sorted(SOURCES), required=True)
    parser.add_argument('--expected-sha256')
    args = parser.parse_args(argv)
    try:
        payload = json.load(sys.stdin)
        if not isinstance(payload, dict):
            raise ValueError('hook input must be an object')
        result = render(Path(__file__).resolve().parent.parent, args.harness,
                        payload, args.expected_sha256)
    except (OSError, ValueError, TypeError) as exc:
        # Context delivery must never impersonate a mission-custody refusal.
        # A visible warning + explicit fallback preserves ordinary authorized work.
        reason = str(exc) if isinstance(exc, ValueError) else type(exc).__name__
        result = {'systemMessage': f'Epistemic usage hook: {reason}. {FALLBACK}',
                  'hookSpecificOutput': {'hookEventName': 'SessionStart',
                                         'additionalContext': FALLBACK}}
    print(json.dumps(result, ensure_ascii=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
