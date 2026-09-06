"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Prepare Markdown and HTML content for speech.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from html.parser import HTMLParser
from dataclasses import dataclass
import re

import markdown
from ...fenced_code_extension import NestedFencesExtension


def normalize_numbers(text, language):
    """Expand plain English numbers when no native text-normalization grammar is installed."""
    if language.lower().split('-')[0].split('_')[0] != 'en':
        return text
    units = ('zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen '
             'fifteen sixteen seventeen eighteen nineteen').split()
    tens = 'zero ten twenty thirty forty fifty sixty seventy eighty ninety'.split()

    def integer(value):
        if value < 20:
            return units[value]
        if value < 100:
            return tens[value // 10] + (' ' + units[value % 10] if value % 10 else '')
        for scale, name in ((10**9, 'billion'), (10**6, 'million'), (1000, 'thousand'), (100, 'hundred')):
            if value >= scale:
                return integer(value // scale) + ' ' + name + (' ' + integer(value % scale) if value % scale else '')

    def expand(match):
        whole, dot, fraction = match.group().replace(',', '').partition('.')
        words = (' '.join(units[int(digit)] for digit in whole)
                 if len(whole) > 12 or (len(whole) > 1 and whole[0] == '0') else integer(int(whole)))
        return words + (' point ' + ' '.join(units[int(digit)] for digit in fraction) if dot else '')

    return re.sub(r'(?<![\w.])(?:[0-9]{1,3}(?:,[0-9]{3})+|[0-9]+)(?:\.[0-9]+)?(?!\w|\.[0-9])', expand, text)


@dataclass
class SpeechSection:
    text: str
    heading: bool = False


class SpeechHTMLParser(HTMLParser):
    def __init__(self, skip_inline=True, skip_multiline=True, announce_headings=False):
        super().__init__(convert_charrefs=True)
        self.skip_inline = skip_inline
        self.skip_multiline = skip_multiline
        self.parts = []
        self.stack = []
        self.announce_headings = announce_headings
        self.headings = []
        self.heading_start = None

    def handle_starttag(self, tag, attrs):
        suppressed = any(self.stack)
        skip = tag in ('script', 'style', 'head')
        if not suppressed and not getattr(self, 'pre_depth', 0) and tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            self.heading_start = len(self.parts)
        if self.announce_headings and not suppressed and tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            title = {'h1': 'Chapter', 'h2': 'Section', 'h3': 'Subsection', 'h4': 'Sub-subsection'}.get(
                tag, f'Heading level {tag[1]}')
            self.parts.append(f'\n{title}: ')
        if tag == 'pre' and self.skip_multiline:
            if not suppressed:
                self.parts.append('\nMultiline code block.\n')
            skip = True
        elif tag == 'code' and self.skip_inline and not suppressed:
            # Code inside an included pre block is multiline, not inline.
            if not getattr(self, 'pre_depth', 0):
                self.parts.append(' Inline code block ')
                skip = True
        if tag == 'pre':
            self.pre_depth = getattr(self, 'pre_depth', 0) + 1
        if tag in ('p', 'div', 'li', 'br', 'tr', 'pre') or (
                tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6') and not self.announce_headings):
            self.parts.append('\n')
        if tag == 'img' and not suppressed:
            self.parts.append(dict(attrs).get('alt', ''))
        if tag not in ('br', 'img', 'hr', 'input', 'meta', 'link', 'wbr', 'source', 'area', 'embed', 'col'):
            self.stack.append(skip or suppressed)

    def handle_endtag(self, tag):
        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6') and self.heading_start is not None:
            self.headings.append((self.heading_start, len(self.parts)))
            self.heading_start = None
        if self.stack:
            self.stack.pop()
        if tag == 'pre':
            self.pre_depth = max(0, getattr(self, 'pre_depth', 0) - 1)
        if tag in ('p', 'div', 'li', 'tr', 'pre', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            self.parts.append('\n')
        elif tag in ('td', 'th'):
            self.parts.append(' ')

    def handle_data(self, data):
        if not any(self.stack):
            self.parts.append(data)


def parse_source(source, *, html=False, skip_inline=True, skip_multiline=True,
                 announce_headings=False):
    source = source.replace('\u2029', '\n').replace('\u2028', '\n')
    if not html:
        # YAML front matter is metadata rather than prose. Only remove a closed block.
        source = re.sub(r'\A---[^\S\n]*\n.*?\n(?:---|\.\.\.)[^\S\n]*(?:\n|$)', '', source, flags=re.S)
        source = markdown.markdown(source, extensions=[
            'extra', NestedFencesExtension(),
        ])
    parser = SpeechHTMLParser(skip_inline, skip_multiline, announce_headings)
    parser.feed(source)
    parser.close()
    return parser


def plain_text(parts):
    return '\n'.join(line.strip() for line in ''.join(parts).splitlines() if line.strip())


def prepare_text(source, **options):
    return plain_text(parse_source(source, **options).parts)


def prepare_sections(source, **options):
    """Preserve heading boundaries independently of their spoken labels."""
    parser = parse_source(source, **options)
    sections = []
    previous = 0
    for start, end in parser.headings:
        if text := plain_text(parser.parts[previous:start]):
            sections.append(SpeechSection(text))
        if text := plain_text(parser.parts[start:end]):
            sections.append(SpeechSection(text, heading=True))
        previous = end
    if text := plain_text(parser.parts[previous:]):
        sections.append(SpeechSection(text))
    return sections


def speech_chunks(text, limit=500, first_limit=None):
    """Bound synthesis requests while preferring sentence/word boundaries."""
    # Short Markdown lines should not each require a separate synthesis/playback cycle.
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    paragraph = ' '.join(line if index == len(lines) - 1 or line[-1:] in '.!?;:' else line + '.'
                         for index, line in enumerate(lines))
    if limit == 0:
        if paragraph:
            yield paragraph
        return
    if limit < 0:
        raise ValueError('Speech context length must not be negative.')
    chunk_limit = first_limit or limit
    while len(paragraph) > chunk_limit:
        boundary = max(paragraph.rfind(mark, 0, chunk_limit) for mark in ('. ', '! ', '? ', '; '))
        if boundary < chunk_limit // 2:
            boundary = paragraph.rfind(' ', 0, chunk_limit)
        boundary = boundary + 1 if boundary > 0 else chunk_limit
        yield paragraph[:boundary].strip()
        paragraph = paragraph[boundary:].lstrip()
        chunk_limit = limit
    if paragraph.strip():
        yield paragraph.strip()
