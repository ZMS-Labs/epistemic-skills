#!/usr/bin/env python3
"""Rebuild the self-contained documentation diagrams. Requires fonttools only."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from xml.sax.saxutils import escape

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).resolve().parent
INK, PAPER, ORANGE, MUTED, LINE = '#152c35', '#f5f3ed', '#ffac70', '#b7c8cc', '#48616a'


@lru_cache(maxsize=12)
def face(weight=500, width=100):
    return instantiateVariableFont(TTFont(ROOT / 'fonts/Archivo.ttf'),
                                   {'wght': weight, 'wdth': width}, inplace=True)


class Drawing:
    def __init__(self, width, height, title, description, background=INK):
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
                      f'<title id="title">{escape(title)}</title>',
                      f'<desc id="desc">{escape(description)}</desc>',
                      f'<rect width="{width}" height="{height}" fill="{background}"/>']

    def path(self, d, color=LINE, stroke=2, fill='none', extra=''):
        self.parts.append(f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{stroke}" {extra}/>')

    def rect(self, x, y, w, h, fill, rx=0):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"/>')

    def circle(self, x, y, r, fill, stroke='none', sw=0):
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def text(self, text, x, y, size=24, color=PAPER, weight=500, width=100):
        font = face(weight, width)
        glyphs, cmap = font.getGlyphSet(), font.getBestCmap()
        scale = size / font['head'].unitsPerEm
        pen = SVGPathPen(glyphs)
        cursor = 0
        from fontTools.pens.transformPen import TransformPen
        for char in text:
            name = cmap[ord(char)]
            glyphs[name].draw(TransformPen(pen, (1, 0, 0, 1, cursor, 0)))
            cursor += font['hmtx'][name][0]
        self.parts.append(f'<path d="{pen.getCommands()}" transform="translate({x} {y}) scale({scale} {-scale})" fill="{color}"/>')
        return cursor * scale

    def save(self, name):
        (ROOT / name).write_text('\n'.join(self.parts) + '\n</svg>\n', encoding='utf-8')


def cover():
    d = Drawing(1280, 490, 'Epistemic Skills — better questions, grounded action',
                'A field guide for agent reasoning. A branching diagram connects a question to an observation and a supported next step. Other possibilities remain open; this is a conceptual illustration, not a mandatory skill sequence.')
    d.text('epistemic', 62, 145, 110, weight=750, width=93)
    word_width = d.text('skills', 62, 250, 110, weight=750, width=93)
    d.circle(62 + word_width + 19, 235, 10, ORANGE)
    d.text('Better questions.', 66, 347, 39, weight=580)
    d.text('Evidence that changes the next step.', 66, 393, 28, MUTED)
    d.path('M66 443 H1214', LINE, 1)
    d.text('Reusable methods for agent reasoning', 66, 469, 17, MUTED)
    d.text('Open source / Agent Skills', 968, 469, 17, MUTED)
    # A question branches into competing explanations. The observed route is solid.
    d.path('M836 104 H936 Q962 104 962 130 V181 M836 320 H936 Q962 320 962 294 V240', LINE, 2)
    d.path('M776 210 H840', ORANGE, 3)
    d.path('M852 210 H948', MUTED, 2, extra='stroke-dasharray="5 8"')
    d.path('M975 210 H1128', ORANGE, 3)
    d.path('M948 161 H975 M948 161 V259 H975', PAPER, 3)
    d.circle(776, 210, 11, INK, ORANGE, 3)
    d.circle(836, 104, 6, INK, MUTED, 2)
    d.circle(836, 320, 6, INK, MUTED, 2)
    d.circle(962, 210, 8, ORANGE)
    d.circle(1138, 210, 12, ORANGE)
    d.path('M1109 162 L1138 133 L1167 162 M1138 133 V190', LINE, 2)
    d.text('Question', 732, 252, 23, weight=550)
    d.text('Observe', 918, 307, 23, weight=550)
    d.text('Act', 1117, 252, 23, ORANGE, 600)
    d.text('Keep alternatives open.', 805, 374, 20, MUTED)
    d.save('epistemic-cover.svg')

    m = Drawing(640, 520, 'Epistemic Skills — better questions, grounded action',
                'Reusable methods for agent reasoning. Better questions; evidence that changes the next step.')
    m.text('epistemic', 38, 133, 103, weight=750, width=93)
    word_width = m.text('skills', 38, 231, 103, weight=750, width=93)
    m.circle(38 + word_width + 19, 218, 10, ORANGE)
    m.text('Better questions.', 41, 311, 38, weight=580)
    m.text('Evidence that changes', 41, 359, 28, MUTED)
    m.text('the next step.', 41, 395, 28, MUTED)
    m.path('M42 454 H157 M180 454 H291', MUTED, 2, extra='stroke-dasharray="5 8"')
    m.path('M315 454 H571', ORANGE, 3)
    m.path('M296 430 H319 M296 430 V478 H319', PAPER, 3)
    m.circle(578, 454, 9, ORANGE)
    m.save('epistemic-cover-mobile.svg')


def method_map():
    d = Drawing(1280, 635, 'Choose a method for the question in front of you',
                'Four families: frame the question with Metacognate, Recon, Resolve and Open Questions; examine a decision with Perspective and Gauntlet; verify an outcome with Health, Triage, Did-it-land, Watch and Evidence-locked UAT; carry work forward with Write-goal, Decision Ledger, Manifest, Outsource and Context Audit. Epistemic is the shared usage guide. These are choices, not stages.', PAPER)
    d.text('One task. The method it needs.', 48, 74, 43, INK, 700)
    d.text('Choose by the question. Return to the work.', 50, 114, 24, '#3f5d67')
    groups = [
        (48, 167, 'Frame the question', 'What do we need to understand?', ['Metacognate / Recon', 'Resolve / Open Questions']),
        (674, 167, 'Examine a decision', 'What could change our judgment?', ['Perspective / Gauntlet']),
        (48, 340, 'Verify an outcome', 'What actually happened?', ['Health / Triage / Did-it-land', 'Watch / Evidence-locked UAT']),
        (674, 340, 'Carry work forward', 'What needs to survive this session?', ['Write-goal / Decision Ledger / Manifest', 'Outsource / Context Audit']),
    ]
    d.path('M630 170 V499', '#c7d1d0', 1)
    for x, y, heading, question, members in groups:
        d.rect(x, y, 34, 5, '#a74316')
        d.text(heading, x, y+47, 30, INK, 650)
        d.text(question, x, y+82, 22, '#3f5d67')
        for i, line in enumerate(members):
            d.text(line, x, y+119+i*30, 21, INK)
    d.rect(0, 537, 1280, 98, INK)
    d.text('epistemic', 48, 579, 24, ORANGE, 650)
    d.text('Discover. Load. Apply. Acknowledge. Continue.', 228, 579, 24, PAPER)
    d.text('The shared usage guide. Routine work can finish with an ordinary targeted check.', 228, 611, 19, MUTED)
    d.save('method-map.svg')
    m = Drawing(640, 1135, 'Choose a method for the question in front of you',
                'The same four families as the wide diagram, stacked for a narrow screen. These groups are choices, not required stages.', PAPER)
    m.text('One task.', 36, 66, 36, INK, 700)
    m.text('The method it needs.', 36, 110, 36, INK, 700)
    m.text('Choose by the question. Return to the work.', 36, 154, 22, '#3f5d67')
    for index, (_, _, heading, question, members) in enumerate(groups):
        y = 205 + index * 182
        m.rect(36, y, 34, 5, '#a74316')
        m.text(heading, 36, y+44, 29, INK, 650)
        m.text(question, 36, y+78, 21, '#3f5d67')
        for i, line in enumerate(members):
            m.text(line, 36, y+113+i*29, 21, INK)
    m.rect(0, 939, 640, 196, INK)
    m.text('epistemic', 36, 983, 27, ORANGE, 650)
    m.text('Discover. Load. Apply.', 36, 1023, 24, PAPER)
    m.text('Acknowledge. Continue.', 36, 1056, 24, PAPER)
    m.text('The shared usage guide. Routine work can finish', 36, 1091, 19, MUTED)
    m.text('with an ordinary targeted check.', 36, 1118, 19, MUTED)
    m.save('method-map-mobile.svg')


if __name__ == '__main__':
    cover()
    method_map()
    print('Rendered 4 self-contained, outlined-type SVGs.')
