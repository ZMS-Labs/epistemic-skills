#!/usr/bin/env python3
"""Focused publication boundary tests; no network access or remote mutations."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import subprocess
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('current_handbook', Path(__file__).with_name('stage_wiki.py'))
publisher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publisher)
SHA = 'a' * 40


class PublicationGuards(unittest.TestCase):
    def test_requires_exact_documentation_identity(self):
        for ref in ('main', 'HEAD', SHA[:12], SHA + ':docs/handbook', 'A' * 40):
            with self.subTest(ref=ref), self.assertRaises(RuntimeError):
                publisher.validate_docs_ref(ref)

    def test_public_main_ancestry_and_immutable_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            def git(*args):
                result = subprocess.run(['git', *args], cwd=root, capture_output=True,
                                        text=True, encoding='utf-8', check=True)
                return result.stdout.strip()

            git('init', '-q', '-b', 'main')
            git('config', 'user.name', 'Documentation Fixture')
            git('config', 'user.email', 'fixture@example.org')
            git('config', 'commit.gpgsign', 'false')
            git('remote', 'add', 'origin', publisher.BASE + '.git')
            page = root / publisher.PAGES / 'Home.md'
            page.parent.mkdir(parents=True)
            page.write_text('Published content\n', encoding='utf-8')
            git('add', '.')
            git('commit', '-qm', 'Published documentation')
            published = git('rev-parse', 'HEAD')
            page.write_text('Private uncommitted draft\n', encoding='utf-8')

            def command(*args, **kwargs):
                if args[:2] == ('git', 'ls-remote'):
                    return published + '\trefs/heads/main'
                try:
                    return git(*args[1:])
                except subprocess.CalledProcessError as exc:
                    raise RuntimeError('Git verification failed') from exc

            with patch.object(publisher, 'command', side_effect=command):
                self.assertEqual(publisher.validate_docs_ref(published), published)
                self.assertEqual(publisher.committed_pages(published), {'Home.md': 'Published content\n'})
                git('add', '.')
                git('commit', '-qm', 'Unpublished draft')
                unpublished = git('rev-parse', 'HEAD')
                with self.assertRaises(RuntimeError):
                    publisher.validate_docs_ref(unpublished)
            git('remote', 'set-url', 'origin', 'https://example.invalid/unrelated.git')
            with patch.object(publisher, 'command', side_effect=command), self.assertRaises(RuntimeError):
                publisher.validate_docs_ref(published)

    def test_ref_without_current_pages_is_rejected(self):
        with patch.object(publisher, 'command', return_value=''), self.assertRaises(RuntimeError):
            publisher.committed_pages(SHA)

    def test_committed_symlink_is_rejected(self):
        listing = '120000 blob ' + SHA + '\tdocs/handbook/pages/Home.md'
        with patch.object(publisher, 'command', return_value=listing), self.assertRaises(RuntimeError):
            publisher.committed_pages(SHA)

    def test_raw_assets_and_current_sources_pin_without_rewriting_release(self):
        originals = [publisher.BASE + '/blob/main/docs/guide.md',
                     publisher.BASE + '/tree/main/docs',
                     publisher.BASE + '/raw/main/docs/assets/cover.svg',
                     publisher.RAW + '/main/docs/assets/cover.svg',
                     publisher.BASE + '/raw/refs/heads/main/docs/assets/cover.svg',
                     publisher.RAW + '/refs/heads/main/docs/assets/cover.svg']
        for original in originals:
            with self.subTest(original=original):
                pinned = publisher.pin_current_links(original, SHA)
                self.assertIn('/' + SHA + '/', pinned)
                self.assertNotIn('/main/', pinned)
        released = publisher.BASE + '/blob/v7.0.0/plugins/epistemic-skills/skills/epistemic/SKILL.md'
        self.assertEqual(publisher.pin_current_links(released, SHA), released)

    def test_unknown_page_is_preserved_by_refusing_plan(self):
        with self.assertRaisesRegex(RuntimeError, 'unrecognized legacy'):
            publisher.plan({'Home.md': '# Home\n'}, {'Private-Notes.md'}, SHA)

    def test_current_pages_take_precedence_over_legacy_redirects(self):
        pages = {'Home.md': '[Glossary](Glossary.md#evidence)\n',
                 'Glossary.md': '# Glossary\n\nActual definitions.\n',
                 'How-the-Pieces-Fit.md': '# How the pieces fit\n'}
        output = publisher.plan(pages, {'Glossary.md', 'Architecture-and-Contracts.md'}, SHA)
        self.assertIn('Actual definitions.', output['Glossary.md'])
        self.assertNotIn('Retired page', output['Glossary.md'])
        self.assertIn('(Glossary#evidence)', output['Home.md'])
        self.assertIn('(How-the-Pieces-Fit)', output['Architecture-and-Contracts.md'])
        self.assertIn(SHA, output['_Footer.md'])
        self.assertIn('[Glossary](Glossary)', output['_Sidebar.md'])
        with patch.object(publisher, 'command', return_value=''):
            publisher.validate_links(output, SHA)

    def test_pages_carry_no_banner_and_footer_keeps_the_version_marker(self):
        source = '> **Applies to:** epistemic-skills v7.0.0.\n\n# Home\n\nBody.\n'
        output = publisher.plan({'Home.md': source}, set(), SHA)
        self.assertEqual(output['Home.md'], '# Home\n\nBody.\n')
        # The exact marker check_wiki RULE 2 reads must survive, outside link text.
        marker = re.compile(r'\*\*Applies to:\*\*\s+epistemic-skills\s+v(\d+\.\d+\.\d+)')
        self.assertEqual(marker.findall(output['_Footer.md']), [publisher.TAG[1:]])
        self.assertIn(f'/tree/{SHA}/docs/handbook/pages', output['_Footer.md'])
        self.assertIn(f'/tree/{publisher.TAG}/plugins/epistemic-skills/skills', output['_Footer.md'])
        self.assertNotIn('Editorial source', output['_Footer.md'])

    def test_retired_pages_name_their_destination(self):
        pages = {name + '.md': f'# {name}\n' for name in
                 ('Home', 'How-the-Pieces-Fit', 'Start-Here', 'Design-Rationale', 'Testing-and-Evaluations')}
        output = publisher.plan(pages, {'The-Epistemic-Arc.md', 'Contributing.md', 'Version-History.md'}, SHA)
        arc = output['The-Epistemic-Arc.md']
        self.assertTrue(arc.startswith('# The Epistemic Arc\n\nRetired page from the v6 handbook. '))
        self.assertIn('see [How the Pieces Fit](How-the-Pieces-Fit).', arc)
        self.assertIn('/blob/v7.0.0/docs/wiki-updates/v6.0.0/pages/The-Epistemic-Arc.md', arc)
        self.assertIn(f'[the contributing guide]({publisher.BASE}/blob/{SHA}/CONTRIBUTING.md)',
                      output['Contributing.md'])
        self.assertIn(f'its history, see [the list of releases]({publisher.BASE}/releases).',
                      output['Version-History.md'])
        for stub in (arc, output['Contributing.md'], output['Version-History.md']):
            self.assertNotIn('Applies to', stub)
        with self.assertRaisesRegex(RuntimeError, 'no reviewed label'):
            publisher.redirect_sentence('https://example.invalid/elsewhere')

    def test_skill_catalog_leads_the_use_section(self):
        pages = {name + '.md': f'# {name}\n' for name in
                 ('Home', 'Skill-Catalog', 'How-the-Pieces-Fit', 'Workflow-Recipes')}
        sidebar = publisher.plan(pages, set(), SHA)['_Sidebar.md']
        section = sidebar.split('**Use the skills**\n\n', 1)[1].split('\n\n', 1)[0]
        self.assertEqual(section.splitlines(), ['- [Skill Catalog](Skill-Catalog)',
                                                '- [How the Pieces Fit](How-the-Pieces-Fit)',
                                                '- [Workflow Recipes](Workflow-Recipes)'])

    def test_dirty_wiki_cannot_reach_a_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / 'Home.md'
            page.write_text('Keep my work', encoding='utf-8')
            with patch.object(publisher, 'clean_wiki', side_effect=RuntimeError('dirty wiki')):
                with self.assertRaises(RuntimeError):
                    publisher.apply_plan(Path(tmp), {'Home.md': 'New content'})
            self.assertEqual(page.read_text(encoding='utf-8'), 'Keep my work')

    def test_symlink_guard_precedes_all_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            wiki = Path(tmp)
            page = wiki / 'Home.md'
            page.write_text('Keep my work', encoding='utf-8')
            # Mock the platform-independent predicate: Windows may require a
            # separate privilege to create symbolic links in a fixture.
            with patch.object(publisher, 'clean_wiki', return_value=wiki), patch.object(Path, 'is_symlink', return_value=True):
                with self.assertRaisesRegex(RuntimeError, 'symlinked'):
                    publisher.apply_plan(wiki, {'Home.md': 'New content'})
            self.assertEqual(page.read_text(encoding='utf-8'), 'Keep my work')

    def test_release_guards_remain_in_force(self):
        good = {'tagName': publisher.TAG, 'isDraft': False, 'publishedAt': '2026-09-19T00:00:00Z'}
        refs = SHA + ' refs/tags/v7.0.0\n' + SHA + ' refs/tags/v7.0.0^{}'
        publisher.validate_publication(good, refs, SHA)
        for release, remote, expected in (({**good, 'isDraft': True}, refs, SHA),
                                          (good, refs.splitlines()[0], SHA),
                                          (good, refs, 'b' * 40)):
            with self.subTest(release=release, remote=remote), self.assertRaises(RuntimeError):
                publisher.validate_publication(release, remote, expected)


if __name__ == '__main__':
    unittest.main(verbosity=2)
