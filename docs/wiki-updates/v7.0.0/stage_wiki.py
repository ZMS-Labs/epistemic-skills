#!/usr/bin/env python3
"""Check or stage the v7 handbook into a clean wiki clone; never commit or push."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import subprocess
import tempfile
import sys

REPO = Path(__file__).resolve().parents[3]
PAGES = 'docs/wiki-updates/v7.0.0/pages'
TAG = 'v7.0.0'
BASE = 'https://github.com/ZMS-Labs/epistemic-skills'
REDIRECTS = {
    'Architecture-and-Contracts': 'Start-Here', 'Choosing-a-Skill': 'Skill-Catalog',
    'Contributing': BASE+'/blob/v7.0.0/CONTRIBUTING.md',
    'Core-Concepts': 'Start-Here', 'Cross-Harness-Packaging': 'Installation-and-Harness-Compatibility',
    'Design-History-and-Audits': 'Testing-and-Evaluations',
    'Evidence-Status-and-Known-Limitations': 'Testing-and-Evaluations',
    'FAQ-and-Troubleshooting': 'Installation-and-Harness-Compatibility', 'Glossary': 'Start-Here',
    'Helix-Central-Passage': 'Start-Here', 'Routine-Work-and-Proportionality': 'Workflow-Recipes',
    'Security-Provenance-and-DCO': 'Release-Process-and-Versioning',
    'Skill-Agent-Interface-Design': 'Skill-Perspective', 'Skill-Applying-Formal-Rigor': 'Skill-Resolve',
    'Skill-Blindspot-Pass': 'Skill-Perspective', 'Skill-Continuity-Verify': 'Skill-Decision-Ledger',
    'Skill-Evidence-Research': 'Skill-Resolve', 'Skill-Intent-Traced-Merge': 'Release-Process-and-Versioning',
    'Skill-Throwaway-Prototyping': 'Skill-Resolve', 'Skill-Using-Epistemic-Skills': 'Skill-Epistemic',
    'Skill-Wayfinding': 'Skill-Recon', 'The-Epistemic-Arc': 'Start-Here',
    'Version-History': BASE+'/releases',
}
LINK = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')


def command(*args, cwd=REPO):
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True, encoding='utf-8')
    if result.returncode:
        raise RuntimeError(f'{args[0]} {args[1]} failed (exit {result.returncode})')
    return result.stdout.strip()


def validate_links(pages, source_ref=None):
    for name, body in pages.items():
        for _, url in LINK.findall(body):
            if url.startswith('../'):
                raise RuntimeError(f'{name}: source-relative link cannot ship to the wiki')
            if url.endswith('.md') and not url.startswith('https:'):
                if url not in pages:
                    raise RuntimeError(f'{name}: missing navigation target {url}')
            match = re.match(re.escape(BASE)+r'/(?:blob|tree)/v7\.0\.0/([^#]+)',url)
            if match:
                path=match[1]
                if source_ref:
                    command('git','cat-file','-e',f'{source_ref}:{path}')
                elif not (REPO/path).exists():
                    raise RuntimeError(f'{name}: missing canonical target {path}')


def plan(pages, existing):
    output={name: LINK.sub(lambda m: f'[{m[1]}]({m[2][:-3]})' if m[2].endswith('.md') and not m[2].startswith('https:') else m[0], body) for name,body in pages.items()}
    for name in sorted(existing-set(output)-{'_Sidebar.md','_Footer.md'}):
        slug=Path(name).stem
        if slug not in REDIRECTS:
            raise RuntimeError(f'unrecognized legacy page {name}; preserve and review before staging')
        output[name]=(f'> **Applies to:** epistemic-skills {TAG}.\n\n# {slug.replace("-"," ")}\n\n'
                      f'This older handbook address now points to [current guidance]({REDIRECTS[slug]}). '
                      'The old page does not define the current skill contract.\n\n'
                      f'[Historical v6 snapshot]({BASE}/blob/{TAG}/docs/wiki-updates/v6.0.0/pages/{name}) '
                      'preserves the earlier guidance; the wiki Git history also remains intact.\n')
    output['_Sidebar.md']='[Home](Home)\n\n'+'\n'.join(f'- [{name[:-3].replace("-"," ")}]({name[:-3]})' for name in ['Start-Here.md','Skill-Catalog.md','Workflow-Recipes.md','Installation-and-Harness-Compatibility.md','Testing-and-Evaluations.md','Release-Process-and-Versioning.md'])+'\n'
    output['_Footer.md']=f'Handbook for {TAG}. [Canonical source]({BASE}/tree/{TAG}/plugins/epistemic-skills/skills) · [Release]({BASE}/releases/tag/{TAG})\n'
    return output


def validate_publication(release, remote_refs, expected):
    if release.get('tagName') != TAG or release.get('isDraft') is not False or not release.get('publishedAt'):
        raise RuntimeError('v7.0.0 GitHub Release is not published')
    refs=dict(line.split()[::-1] for line in remote_refs.splitlines() if line.strip())
    if refs.get(f'refs/tags/{TAG}^{{}}') != expected:
        raise RuntimeError('published annotated tag does not peel to the expected source commit')


def clean_wiki(wiki):
    wiki=wiki.resolve()
    if Path(command('git','rev-parse','--show-toplevel',cwd=wiki)).resolve()!=wiki:
        raise RuntimeError('destination must be the wiki Git root')
    if command('git','remote','get-url','origin',cwd=wiki) != BASE+'.wiki.git':
        raise RuntimeError('destination is not the epistemic-skills wiki repository')
    if command('git','status','--porcelain',cwd=wiki):
        raise RuntimeError('wiki checkout has changes; preserve them and use a clean clone')
    return wiki


def self_test():
    from unittest.mock import patch
    good={'tagName':TAG,'isDraft':False,'publishedAt':'2026-09-18T00:00:00Z'}
    refs='abc refs/tags/v7.0.0\n123 refs/tags/v7.0.0^{}'
    validate_publication(good,refs,'123')
    for release,remote,sha in [({**good,'isDraft':True},refs,'123'),({**good,'publishedAt':None},refs,'123'),({**good,'tagName':'v6.0.0'},refs,'123'),(good,refs,'456'),(good,'abc refs/tags/v7.0.0','123')]:
        try:validate_publication(release,remote,sha)
        except RuntimeError:pass
        else:raise AssertionError('invalid publication accepted')
    with tempfile.TemporaryDirectory() as tmp:
        with patch(__name__+'.command',side_effect=[tmp,BASE+'.wiki.git',' M Home.md']):
            try:clean_wiki(Path(tmp))
            except RuntimeError:pass
            else:raise AssertionError('dirty wiki accepted')
    pages={'Home.md':'[start](Start-Here.md)','Start-Here.md':'current'}
    result=plan(pages,{'Home.md','Helix-Central-Passage.md'})
    assert '[start](Start-Here)' in result['Home.md']
    assert 'Historical v6 snapshot' in result['Helix-Central-Passage.md']
    try:plan(pages,{'unexpected.md'})
    except RuntimeError:pass
    else:raise AssertionError('unknown legacy page overwritten')
    print('v7 wiki staging self-test: PASS (publication, identity, dirty-worktree, navigation, legacy guards)')


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check',action='store_true',help='validate current snapshot source links without requiring publication')
    ap.add_argument('--self-test',action='store_true')
    ap.add_argument('--wiki',type=Path)
    ap.add_argument('--expected-sha',help='exact approved release commit')
    ap.add_argument('--apply',action='store_true',help='stage files only; otherwise print the verified plan')
    args=ap.parse_args()
    if args.self_test:self_test();return 0
    if args.check and args.apply:ap.error("--check cannot be combined with --apply")
    if args.check:
        pages={p.name:p.read_text(encoding='utf-8') for p in (REPO/PAGES).glob('*.md')}
        if not pages:raise RuntimeError('snapshot is empty')
        validate_links(pages)
        if args.wiki:
            wiki=clean_wiki(args.wiki)
            output=plan(pages,{p.name for p in wiki.glob('*.md')})
            validate_links(output)
            with tempfile.TemporaryDirectory() as tmp:
                for name,body in output.items():(Path(tmp)/name).write_text(body,encoding='utf-8')
                print(command(sys.executable,str(REPO/'docs/wiki-updates/v6.0.0/check_wiki.py'),tmp))
            print(f'Complete wiki preview: {len(output)} pages; destination unchanged')
        print(f'v7 snapshot source links: PASS ({len(pages)} pages); live URLs require published tag')
        return 0
    if not args.wiki or not args.expected_sha:ap.error('--wiki and --expected-sha are required for a publication plan')
    wiki=clean_wiki(args.wiki)
    sha=command('git','rev-parse',f'refs/tags/{TAG}^{{commit}}')
    if sha!=args.expected_sha:raise RuntimeError('local tag and expected release commit disagree')
    release=json.loads(command('gh','release','view',TAG,'--repo','ZMS-Labs/epistemic-skills','--json','tagName,isDraft,publishedAt'))
    refs=command('git','ls-remote',BASE+'.git',f'refs/tags/{TAG}',f'refs/tags/{TAG}^{{}}')
    validate_publication(release,refs,sha)
    manifest=json.loads(command('git','show',f'{sha}:plugins/epistemic-skills/.claude-plugin/plugin.json'))
    if manifest.get('version')!='7.0.0':raise RuntimeError('tagged manifest is not v7.0.0')
    names=command('git','ls-tree','-r','--name-only',sha,'--',PAGES).splitlines()
    pages={Path(name).name:command('git','show',f'{sha}:{name}')+'\n' for name in names if name.endswith('.md')}
    if not pages:raise RuntimeError('tag has no v7 snapshot')
    validate_links(pages,sha)
    output=plan(pages,{p.name for p in wiki.glob('*.md')})
    validate_links(output,sha)
    with tempfile.TemporaryDirectory() as tmp:
        for name,body in output.items():(Path(tmp)/name).write_text(body,encoding='utf-8')
        command(sys.executable,str(REPO/'docs/wiki-updates/v6.0.0/check_wiki.py'),tmp,'--source-ref',TAG)
    if args.apply:
        clean_wiki(wiki)  # Recheck immediately before the first write.
        if any((wiki/name).is_symlink() for name in output):
            raise RuntimeError("refusing to overwrite a symlinked wiki page")
        for name,body in output.items():(wiki/name).write_text(body,encoding='utf-8')
    print(f'{"Staged" if args.apply else "Would stage"} {len(output)} pages from {sha}; no commit or push performed.')
    return 0


if __name__=='__main__':
    try:raise SystemExit(main())
    except (RuntimeError,OSError,ValueError) as exc:
        print(f'wiki staging refused: {exc}',file=sys.stderr);raise SystemExit(1)
