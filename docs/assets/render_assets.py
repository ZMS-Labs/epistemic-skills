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


def advance(text, size, weight=500, width=100):
    """Rendered width of a line, in SVG units, without drawing it."""
    font = face(weight, width)
    cmap = font.getBestCmap()
    return sum(font['hmtx'][cmap[ord(char)]][0] for char in text) * size / font['head'].unitsPerEm


def wrap(text, size, limit, weight=500, separator=' '):
    """Greedy line breaks at `separator`; wording is unchanged, only where it breaks."""
    lines = []
    for part in text.split(separator):
        candidate = f'{lines[-1]}{separator}{part}' if lines else part
        if lines and advance(candidate, size, weight) <= limit:
            lines[-1] = candidate
        else:
            lines.append(part)
    too_wide = [line for line in lines if advance(line, size, weight) > limit]
    if too_wide:
        raise ValueError(f'cannot fit {too_wide!r} in {limit} units at {size}px')
    return lines


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
        # newline='\n' keeps the output byte-identical on Windows and POSIX.
        (ROOT / name).write_text('\n'.join(self.parts) + '\n</svg>\n', encoding='utf-8', newline='\n')


def cover():
    d = Drawing(1280, 490, 'Epistemic Skills. Check the cause before naming it. Confirm the change before calling it done.',
                'A field guide for agent reasoning. A branching diagram connects a question to an observation and a supported next step. Other possibilities remain open; this is a conceptual illustration, not a mandatory skill sequence.')
    d.text('epistemic', 62, 145, 110, weight=750, width=93)
    word_width = d.text('skills', 62, 250, 110, weight=750, width=93)
    d.circle(62 + word_width + 19, 235, 10, ORANGE)
    d.text('Check the cause before naming it.', 66, 347, 39, weight=580)
    d.text('Confirm the change before calling it done.', 66, 393, 28, MUTED)
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

    m = Drawing(640, 520, 'Epistemic Skills. Check the cause before naming it. Confirm the change before calling it done.',
                'Reusable methods for agent reasoning. Check the cause before naming it, and confirm the change before calling it done.')
    m.text('epistemic', 38, 133, 103, weight=750, width=93)
    word_width = m.text('skills', 38, 231, 103, weight=750, width=93)
    m.circle(38 + word_width + 19, 218, 10, ORANGE)
    m.text('Check the cause before naming it.', 41, 311, 34, weight=580)
    m.text('Confirm the change', 41, 359, 28, MUTED)
    m.text('before calling it done.', 41, 395, 28, MUTED)
    m.path('M42 454 H157 M180 454 H291', MUTED, 2, extra='stroke-dasharray="5 8"')
    m.path('M315 454 H571', ORANGE, 3)
    m.path('M296 430 H319 M296 430 V478 H319', PAPER, 3)
    m.circle(578, 454, 9, ORANGE)
    m.save('epistemic-cover-mobile.svg')


def method_map():
    d = Drawing(1280, 635, 'Choose a method for the question in front of you',
                'Four families: frame the question with Metacognate, Recon, Resolve and Open Questions; examine a decision with Perspective and Gauntlet; verify an outcome with Health, Triage, Did It Land, Watch and Evidence-Locked UAT; carry work forward with Write Goal, Decision Ledger, Manifest, Outsource and Context Audit. Epistemic is the shared usage guide. These are choices, not stages.', PAPER)
    d.text('One task. The method it needs.', 48, 74, 43, INK, 700)
    d.text('Choose by the question. Return to the work.', 50, 114, 24, '#3f5d67')
    groups = [
        (48, 167, 'Frame the question', 'What do we need to understand?', ['Metacognate / Recon', 'Resolve / Open Questions']),
        (674, 167, 'Examine a decision', 'What could change our judgment?', ['Perspective / Gauntlet']),
        (48, 340, 'Verify an outcome', 'What actually happened?', ['Health / Triage / Did It Land', 'Watch / Evidence-Locked UAT']),
        (674, 340, 'Carry work forward', 'What needs to survive this session?', ['Write Goal / Decision Ledger / Manifest', 'Outsource / Context Audit']),
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
    # Narrow-screen version. A 640-unit image shown in a 256px column (a 320px
    # phone) scales by 0.4, so 30 units is the smallest type that still renders
    # at 12px. Lines break at spaces or at the " / " between method names; the
    # wording is the wide diagram's.
    width, margin, small = 640, 36, 30
    limit = width - 2 * margin
    body, marks, y = [], [], 20
    for text in ('One task.', 'The method it needs.'):
        y += 52
        body.append((text, y, 44, INK, 700))
    y += 4
    for text in ('Choose by the question.', 'Return to the work.'):
        for piece in wrap(text, small, limit):
            y += 42
            body.append((piece, y, small, '#3f5d67', 500))
    for _, _, heading, question, members in groups:
        y += 58
        marks.append(y)
        for text in wrap(heading, 38, limit, 650):
            y += 50
            body.append((text, y, 38, INK, 650))
        for text in wrap(question, small, limit):
            y += 42
            body.append((text, y, small, '#3f5d67', 500))
        y += 6
        for member in members:
            for text in wrap(member, small, limit, separator=' / '):
                y += 42
                body.append((text, y, small, INK, 500))
    band = y + 56
    footer, y = [], band
    y += 58
    footer.append(('epistemic', y, 34, ORANGE, 650))
    for text in ('Discover. Load. Apply.', 'Acknowledge. Continue.'):
        for piece in wrap(text, 32, limit):
            y += 44
            footer.append((piece, y, 32, PAPER, 500))
    y += 8
    for text in wrap('The shared usage guide. Routine work can finish with an ordinary targeted check.', small, limit):
        y += 42
        footer.append((text, y, small, MUTED, 500))
    height = y + 38
    m = Drawing(width, height, 'Choose a method for the question in front of you',
                'The same four families as the wide diagram, stacked for a narrow screen. These groups are choices, not required stages.', PAPER)
    for mark in marks:
        m.rect(margin, mark, 34, 5, '#a74316')
    for text, line_y, size, color, weight in body:
        m.text(text, margin, line_y, size, color, weight)
    m.rect(0, band, width, height - band, INK)
    for text, line_y, size, color, weight in footer:
        m.text(text, margin, line_y, size, color, weight)
    m.save('method-map-mobile.svg')


if __name__ == '__main__':
    cover()
    method_map()
    print('Rendered 4 self-contained, outlined-type SVGs.')
