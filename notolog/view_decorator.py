"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Document view decorator to support additional highlights in the resulting text.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtGui import QTextCursor, QSyntaxHighlighter

import logging

from typing import TYPE_CHECKING, Union

from .settings import Settings
from .highlight.view_highlighter import ViewHighlighter

if TYPE_CHECKING:
    from PySide6.QtCore import QObject  # noqa: F401
    from PySide6.QtGui import QTextBlockUserData  # noqa: F401
    from PySide6.QtWidgets import QTextBrowser  # noqa: F401
    from .text_block_data import TextBlockData  # noqa: F401


class ViewDecorator:
    """
    View mode result decoration by modifying loaded QTextDocument.
    The source of the data comes from the userData() attached to a block within ViewHighlighter.
    """

    """
    Walking rules to create QRegExp for each pattern
    * tag
    * open index shifting right
    * close index shifting left
    * theme style format key from the highlighter
    * replacement
    """
    rules = [
        # strikethrough
        ('s', 2, 2, 's', None),
        ('s_open', 2, 0, 's', None),
        ('s_close', 0, 2, 's', None),
        ('s_within', 0, 0, 's', None),
        # todos highlighting
        ('todo', 0, 0, 'todo', None),
        # invisible separator
        ('inv_sep', 0, 0, 'inv_sep', None),
    ]

    def __init__(self, highlighter: Union[QSyntaxHighlighter, ViewHighlighter]):
        """
        Args:
            highlighter (Union[QSyntaxHighlighter, ViewHighlighter]):
            Highlighter that holds document to apply any modifications.
        """
        self.highlighter = highlighter
        self.doc = self.highlighter.document()

        self.settings = Settings()

        self.logger = logging.getLogger('view_decorator')

        self.logger.debug('Characters count %d' % self.doc.characterCount())

        cursor = QTextCursor(self.doc)
        self.cursor_pos_orig = cursor.position()

    def restore_cursor_pos(self):
        cursor = QTextCursor(self.doc)
        # Restore original cursor position
        cursor.setPosition(self.cursor_pos_orig, QTextCursor.MoveMode.MoveAnchor)
        parent = self.doc.parent()  # type: QObject
        parent_widget = parent.get_view_widget()  # type: QTextBrowser
        parent_widget.setTextCursor(cursor)

    def process(self):
        """Format original ranges before removing delimiters from right to left."""
        operations = []
        block = self.doc.begin()
        while block.isValid():
            data = block.userData()
            if data is not None and hasattr(data, 'get_all'):
                # Highlighter regex ranges use Python characters; QTextCursor
                # positions count UTF-16 code units, including surrogate pairs.
                offsets = [0]
                for character in block.text():
                    offsets.append(offsets[-1] + (2 if ord(character) > 0xffff else 1))
                for tag, oi, ci, fmt_key, repl in self.rules:
                    if tag == 'todo' and not self.settings.viewer_highlight_todos:
                        continue
                    for row in data.get_all(tag) or ():
                        start, end = row['start'], row['end']
                        if not 0 <= start <= end < len(offsets):
                            continue
                        operations.append((
                            block.position() + offsets[start],
                            block.position() + offsets[end],
                            oi, ci, fmt_key, repl or '',
                        ))
            block = block.next()

        cursor = QTextCursor(self.doc)
        cursor.beginEditBlock()
        try:
            removals = {}
            for start, end, oi, ci, fmt_key, repl in operations:
                cursor.setPosition(start + oi)
                cursor.setPosition(end - ci, QTextCursor.MoveMode.KeepAnchor)
                style = self.highlighter.theme[fmt_key].copy()
                if fmt_key == 'todo':
                    style.setdefault('font_size_ratio', 0)
                cursor.mergeCharFormat(self.highlighter.cf(**style))
                if oi:
                    removals[(start, start + oi)] = repl
                if ci:
                    removals[(end - ci, end)] = repl

            # All tags share the original coordinate system. Deleting later
            # markers first preserves both earlier ranges and other tag types.
            for (start, end), repl in sorted(removals.items(), reverse=True):
                cursor.setPosition(start)
                cursor.setPosition(end, QTextCursor.MoveMode.KeepAnchor)
                cursor.insertText(repl)
        finally:
            cursor.endEditBlock()

        self.restore_cursor_pos()
