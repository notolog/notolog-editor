"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Render nested code fences using Python-Markdown's existing code renderer.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

import re

from markdown.extensions import Extension
from markdown.extensions.fenced_code import FencedBlockPreprocessor
from markdown.blockprocessors import ParagraphProcessor


class NestedFencesExtension(Extension):
    def extendMarkdown(self, md):
        fences = NestedFencesProcessor(md, {'lang_prefix': 'language-'})
        md.preprocessors.register(fences, 'fenced_code_block', 25)
        md.parser.blockprocessors.register(FencedPlaceholderProcessor(md.parser, fences),
                                           'fenced_placeholder', 85)


class FencedPlaceholderProcessor(ParagraphProcessor):
    def __init__(self, parser, fences):
        super().__init__(parser)
        self.fences = fences

    def test(self, parent, block):
        # Preserve rendered fences after list indentation is consumed, before indented-code processing.
        return block.strip() in self.fences.placeholders


class NestedFencesProcessor(FencedBlockPreprocessor):
    opening = re.compile(r'(?P<prefix>[ \t]*(?:>[ \t]*)*)(?P<fence>`{3,}|~{3,})(?P<info>[^\n]*)$')

    def closing_fences(self, lines):
        """Match fences once, discarding unfinished candidates when their container ends."""
        containers = []
        closing = {}
        for index, line in enumerate(lines):
            if line.strip():
                while containers and not line.startswith(containers[-1][0]):
                    containers.pop()
            match = self.opening.fullmatch(line)
            if match is None:
                continue
            prefix, fence, info = match.group('prefix', 'fence', 'info')
            if self.FENCED_BLOCK_RE.fullmatch(fence + info + '\n\n' + fence) is None:
                continue
            if not containers or containers[-1][0] != prefix:
                containers.append((prefix, {}))
            pending = containers[-1][1]
            if not info.strip(' '):
                for start in pending.pop(fence, []):
                    closing[start] = (prefix, index)
            # A closer may also open a fence if an enclosing block consumes its earlier opener.
            pending.setdefault(fence, []).append(index)
        return closing

    def run(self, lines):
        self.placeholders = set()
        closing = self.closing_fences(lines)
        result = []
        index = 0
        while index < len(lines):
            if index not in closing:
                result.append(lines[index])
                index += 1
                continue
            prefix, end = closing[index]
            block = [line[len(prefix):] if line.startswith(prefix) else '' for line in lines[index:end + 1]]
            rendered = super().run(block)
            self.placeholders.update(value.strip() for value in rendered if value.strip())
            # Preserve the list/quote container around the renderer's HTML placeholder.
            result.extend(prefix + value if value else prefix.rstrip() for value in rendered)
            index = end + 1
        return result
