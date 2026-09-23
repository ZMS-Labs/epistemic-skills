#!/usr/bin/env python3
"""Validate or stage the current handbook from a published documentation commit.

The release snapshot and tag remain immutable. This helper only stages a clean
wiki clone; review, commit and push are separate maintainer actions.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from urllib.parse import unquote, urlsplit

REPO = Path(__file__).resolve().parents[2]
PAGES = 'docs/handbook/pages'
TAG = 'v7.1.0'
BASE = 'https://github.com/ZMS-Labs/epistemic-skills'
RAW = 'https://raw.githubusercontent.com/ZMS-Labs/epistemic-skills'
LINK = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
COMMIT = re.compile(r'[0-9a-f]{40}')
PAGE_NAME = re.compile(r'[A-Za-z0-9][A-Za-z0-9-]*\.md')

spec = importlib.util.spec_from_file_location(
    'release_wiki_staging', REPO / 'docs/wiki-updates/v7.0.0/stage_wiki.py')
release_staging = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release_staging)
command = release_staging.command
clean_wiki = release_staging.clean_wiki


def validate_publication(release, remote_refs, expected):
    """Same contract as the release snapshot's validator, bound to THIS
    handbook's release: the named GitHub Release must be published and the
    annotated tag must peel to the expected source commit. Defined locally
    because the imported module's copy is pinned to its own v7.0.0 tag."""
    if release.get('tagName') != TAG or release.get('isDraft') is not False or not release.get('publishedAt'):
        raise RuntimeError(f'{TAG} GitHub Release is not published')
    refs = dict(line.split()[::-1] for line in remote_refs.splitlines() if line.strip())
    if refs.get(f'refs/tags/{TAG}^{{}}') != expected:
        raise RuntimeError('published annotated tag does not peel to the expected source commit')


def validate_docs_ref(docs_ref):
    """Require an exact commit reachable from the freshly observed public main."""
    if not COMMIT.fullmatch(docs_ref):
        raise RuntimeError('--docs-ref must be a full lowercase 40-character commit SHA')
    if command('git', 'remote', 'get-url', 'origin') != BASE + '.git':
        raise RuntimeError('source origin is not the epistemic-skills repository')
    if command('git', 'cat-file', '-t', docs_ref) != 'commit':
        raise RuntimeError('documentation reference is not a commit')
    remote = command('git', 'ls-remote', BASE + '.git', 'refs/heads/main').split()
    if len(remote) != 2 or remote[1] != 'refs/heads/main' or not COMMIT.fullmatch(remote[0]):
        raise RuntimeError('could not identify the published main branch')
    # Refuse if its object is absent locally. Fetching current main is a separate
    # explicit preparation step; a stale local origin/main cannot grant approval.
    command('git', 'cat-file', '-e', remote[0] + '^{commit}')
    command('git', 'merge-base', '--is-ancestor', docs_ref, remote[0])
    return remote[0]


def committed_pages(docs_ref):
    """Load regular page blobs at an immutable ref, never working-tree content."""
    listing = command('git', 'ls-tree', '-r', docs_ref, '--', PAGES)
    pages = {}
    for line in listing.splitlines():
        metadata, path = line.split('\t', 1)
        mode, kind, _ = metadata.split()
        if not path.endswith('.md'):
            continue
        name = path.removeprefix(PAGES + '/')
        if not PAGE_NAME.fullmatch(name) or mode not in {'100644', '100755'} or kind != 'blob':
            raise RuntimeError('handbook pages must be regular Markdown files directly in pages/')
        pages[name] = command('git', 'show', f'{docs_ref}:{path}') + '\n'
    if not pages:
        raise RuntimeError('documentation commit has no current handbook pages')
    return pages


def local_pages():
    pages = {}
    for path in sorted((REPO / PAGES).glob('*.md')):
        if path.is_symlink() or not PAGE_NAME.fullmatch(path.name):
            raise RuntimeError('handbook pages must be regular, named Markdown files')
        pages[path.name] = path.read_text(encoding='utf-8')
    if not pages:
        raise RuntimeError('current handbook is empty')
    return pages


def pin_current_links(body, docs_ref):
    """Pin repository documentation and raw assets without changing release links."""
    for prefix in (BASE + '/blob/', BASE + '/tree/', BASE + '/raw/', RAW + '/'):
        body = body.replace(prefix + 'main/', prefix + docs_ref + '/')
    # GitHub also emits this raw URL spelling from its download button.
    body = body.replace(BASE + '/raw/refs/heads/main/', BASE + '/raw/' + docs_ref + '/')
    body = body.replace(RAW + '/refs/heads/main/', RAW + '/' + docs_ref + '/')
    return body


def require_source_path(ref, path, page):
    try:
        command('git', 'cat-file', '-e', f'{ref}:{path}')
    except RuntimeError as exc:
        raise RuntimeError(f'{page}: missing source target {ref}:{path}') from exc


def validate_links(pages, docs_ref=None):
    for name, body in pages.items():
        for _, target in LINK.findall(body):
            url = urlsplit(target)
            if not url.scheme and not url.netloc:
                path = unquote(url.path)
                if not path:
                    continue
                if '/' in path or '\\' in path:
                    raise RuntimeError(f'{name}: relative link must name a handbook page: {path}')
                page = path if path.endswith('.md') else path + '.md'
                if page not in pages:
                    raise RuntimeError(f'{name}: missing navigation target {path}')
                continue
            prefixes = (BASE + '/blob/', BASE + '/tree/', BASE + '/raw/', RAW + '/')
            for prefix in prefixes:
                if not target.startswith(prefix):
                    continue
                remaining = unquote(target[len(prefix):].split('#', 1)[0].split('?', 1)[0])
                remaining = remaining.removeprefix('refs/heads/')
                ref, separator, path = remaining.partition('/')
                if not separator:
                    continue
                # Check our current sources and the released contracts offline.
                if ref == 'main' or (docs_ref and ref == docs_ref):
                    if docs_ref:
                        require_source_path(docs_ref, path, name)
                    elif not (REPO / path).exists():
                        raise RuntimeError(f'{name}: missing current source target {path}')
                elif ref == TAG:
                    require_source_path(TAG, path, name)
                break


def redirect_sentence(destination):
    """The sentence that sends a retired page's reader to its destination."""
    if not destination.startswith('https:'):
        return f'For current guidance, see [{destination.replace("-", " ")}]({destination}).'
    if destination.endswith('/CONTRIBUTING.md'):
        return f'For current guidance, see [the contributing guide]({destination}).'
    if destination == BASE + '/releases':
        return f'For the current version and its history, see [the list of releases]({destination}).'
    raise RuntimeError(f'legacy redirect has no reviewed label: {destination}')


def plan(pages, existing, docs_ref):
    output = {}
    # The version and the documentation source are stated once, in _Footer.md,
    # which keeps the exact "**Applies to:** epistemic-skills vX" marker that
    # check_wiki RULE 2 reads. Pages carry no per-page banner.
    for name, source in pages.items():
        if not PAGE_NAME.fullmatch(name):
            raise RuntimeError(f'invalid handbook page name: {name}')
        body = pin_current_links(source, docs_ref)
        # Remove the source banner, not any historical version references.
        body = re.sub(r'^> \*\*Applies to:\*\*[^\n]*\n(?:\n)?', '', body, count=1)
        body = LINK.sub(lambda m: "[{}]({})".format(m[1], re.sub(r"\.md(?=#|$)", "", m[2]))
                        if not urlsplit(m[2]).scheme else m[0], body)
        output[name] = body
    redirects = dict(release_staging.REDIRECTS)
    redirects.update({
        'Architecture-and-Contracts': 'How-the-Pieces-Fit',
        'Design-History-and-Audits': 'Design-Rationale',
        'Evidence-Status-and-Known-Limitations': 'Testing-and-Evaluations',
        'The-Epistemic-Arc': 'How-the-Pieces-Fit',
        'Contributing': BASE + '/blob/' + docs_ref + '/CONTRIBUTING.md',
    })
    for name in sorted(existing - set(output) - {'_Sidebar.md', '_Footer.md'}):
        slug = Path(name).stem
        if slug not in redirects:
            raise RuntimeError(f'unrecognized legacy page {name}; preserve and review before staging')
        destination = redirects[slug]
        if not destination.startswith('https:') and destination + '.md' not in output:
            raise RuntimeError(f'legacy redirect {name} has no current destination')
        output[name] = (f'# {slug.replace("-", " ")}\n\n'
                        f'Retired page from the v6 handbook. {redirect_sentence(destination)} '
                        f'The [v6 snapshot]({BASE}/blob/{TAG}/docs/wiki-updates/v6.0.0/pages/{name}) '
                        "keeps the original text, and the wiki's Git history is intact.\n")
    sections = {
        'Start here': ['Home', 'Start-Here', 'Core-Concepts'],
        'Use the skills': ['Skill-Catalog', 'How-the-Pieces-Fit', 'Workflow-Recipes'],
        'Understand the design': ['Design-Rationale', 'Glossary'],
        'Install and troubleshoot': ['Installation-and-Harness-Compatibility', 'FAQ-and-Troubleshooting'],
        'Maintain and verify': ['Maintainer-Guide', 'Testing-and-Evaluations', 'Release-Process-and-Versioning'],
    }
    sidebar = []
    for heading, slugs in sections.items():
        links = [f'- [{slug.replace("-", " ")}]({slug})' for slug in slugs if slug + '.md' in pages]
        if heading == 'Maintain and verify' and 'Maintainer-Guide.md' not in pages:
            links.insert(0, f'- [Maintainer guide]({BASE}/blob/{docs_ref}/docs/MAINTAINING.md)')
        if links:
            sidebar.append(f'**{heading}**\n\n' + '\n'.join(links))
    output['_Sidebar.md'] = '\n\n'.join(sidebar) + '\n'
    # Keep "epistemic-skills {TAG}" outside link brackets: check_wiki RULE 2 reads it.
    output['_Footer.md'] = (f'**Applies to:** epistemic-skills {TAG}. '
                            f'[Release notes]({BASE}/releases/tag/{TAG}) · '
                            f'[Source for these pages]({BASE}/tree/{docs_ref}/docs/handbook/pages) · '
                            f'[The skills as released]({BASE}/tree/{TAG}/plugins/epistemic-skills/skills)\n')
    return output


def check_structure(pages):
    with tempfile.TemporaryDirectory() as tmp:
        for name, body in pages.items():
            (Path(tmp) / name).write_text(body, encoding='utf-8')
        return command(sys.executable, str(REPO / 'docs/wiki-updates/v6.0.0/check_wiki.py'),
                       tmp, '--source-ref', TAG)


def apply_plan(wiki, output):
    clean_wiki(wiki)  # Recheck immediately before the first write.
    if any((wiki / name).is_symlink() for name in output):
        raise RuntimeError('refusing to overwrite a symlinked wiki page')
    for name, body in output.items():
        (wiki / name).write_text(body, encoding='utf-8')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check', action='store_true', help='check working-tree sources offline, including new files')
    ap.add_argument('--self-test', action='store_true')
    ap.add_argument('--wiki', type=Path)
    ap.add_argument('--docs-ref', help='full documentation commit SHA already published on origin/main')
    ap.add_argument('--expected-release-sha', help='exact published v7.0.0 release commit')
    ap.add_argument('--apply', action='store_true', help='stage only; default prints a verified plan')
    args = ap.parse_args()
    if args.self_test:
        subprocess.run([sys.executable, str(Path(__file__).with_name('test_stage_wiki.py'))], check=True)
        return 0
    if args.check:
        if args.apply or args.docs_ref or args.expected_release_sha:
            ap.error('--check cannot be combined with publication arguments')
        pages = local_pages()
        validate_links(pages)
        print(check_structure(pages))
        if args.wiki:
            wiki = clean_wiki(args.wiki)
            output = plan(pages, {p.name for p in wiki.glob('*.md')}, '0' * 40)
            print(check_structure(output))
            print(f'Complete wiki preview: {len(output)} pages; destination unchanged')
        print(f'Current handbook: PASS ({len(pages)} pages); publication requires a committed public docs ref')
        return 0
    if not args.wiki or not args.docs_ref or not args.expected_release_sha:
        ap.error('--wiki, --docs-ref and --expected-release-sha are required for publication')
    if not COMMIT.fullmatch(args.expected_release_sha):
        ap.error('--expected-release-sha must be a full lowercase 40-character commit SHA')
    wiki = clean_wiki(args.wiki)
    published_main = validate_docs_ref(args.docs_ref)
    sha = command('git', 'rev-parse', f'refs/tags/{TAG}^{{commit}}')
    if sha != args.expected_release_sha:
        raise RuntimeError('local tag and expected release commit disagree')
    release = json.loads(command('gh', 'release', 'view', TAG, '--repo', 'ZMS-Labs/epistemic-skills',
                                 '--json', 'tagName,isDraft,publishedAt'))
    refs = command('git', 'ls-remote', BASE + '.git', f'refs/tags/{TAG}', f'refs/tags/{TAG}^{{}}')
    validate_publication(release, refs, sha)
    manifest = json.loads(command('git', 'show', f'{sha}:plugins/epistemic-skills/.claude-plugin/plugin.json'))
    if manifest.get('version') != TAG[1:]:
        raise RuntimeError('tagged manifest is not v7.0.0')
    pages = committed_pages(args.docs_ref)
    validate_links(pages, args.docs_ref)
    output = plan(pages, {p.name for p in wiki.glob('*.md')}, args.docs_ref)
    validate_links(output, args.docs_ref)
    print(check_structure(output))
    if args.apply:
        apply_plan(wiki, output)
    print(f'{"Staged" if args.apply else "Would stage"} {len(output)} pages from {args.docs_ref}; '
          f'published main {published_main}; describes {TAG} at {sha}; no commit or push performed.')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (RuntimeError, OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f'wiki staging refused: {exc}', file=sys.stderr)
        raise SystemExit(1)
