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
        cursor = QTextCursor(self.doc)
        cursor.movePosition(QTextCursor.MoveOperation.Start)
        while not (cursor.atEnd()
                   # Sometimes, cursor.atEnd() doesn't work as the cursor unable to move next block at the very end
                   or (cursor.block().blockNumber() > 0 and cursor.block().blockNumber() == self.doc.blockCount() - 1)):
            current_block = cursor.block()
            # current_block_number = current_block.blockNumber()
            block_pos = current_block.position()

            for tag, oi, ci, fmt_key, repl in self.rules:
                if tag == 'todo' and not self.settings.viewer_highlight_todos:
                    continue
                if repl is None:
                    repl = ""
                # Get theme's style format from the highlighter to keep single config and maintain overrides.
                fmt = self.highlighter.theme[fmt_key]
                data_storage = current_block.userData()  # type: Union[QTextBlockUserData, TextBlockData]
                if (data_storage is not None
                        and hasattr(data_storage, 'block_number')
                        and data_storage.get_one(tag)):

                    # Each text cut reduced by token's length
                    len_reduced = 0

                    for block_data in data_storage.get_all(tag):
                        self.logger.debug(
                            'Current block data [%d]~[%d] "%s", in:%r, opened:%r, closed:%r, start: %d, end: %d'
                            % (current_block.blockNumber(), data_storage.block_number, tag, block_data['within'],
                               block_data['opened'], block_data['closed'], block_data['start'], block_data['end']))

                        _r = {'o': block_pos + block_data['start'],
                              'c': block_pos + block_data['end'],
                              'oi': oi, 'ci': ci, 'fmt': fmt, 'repl': repl}

                        find_cursor = QTextCursor(current_block)

                        """
                        # Proof of concept
                        find_cursor = self.doc.find(pattern, find_cursor)
                        if find_cursor.isNull():
                           continue
                        _r = {'o': find_cursor.selectionStart(), 'c': find_cursor.selectionEnd(),
                              'oi': oi, 'ci': ci, 'fmt': fmt, 'repl': repl}
                        self.logger.debug('Cursor position match block: %d, abs: %d, open: %d, close: %d, text: %s'
                            % (find_cursor.positionInBlock(), find_cursor.position(), find_cursor.selectionStart(),
                               find_cursor.selectionEnd(), find_cursor.selectedText()))
                        """

                        # Edit the block
                        find_cursor.beginEditBlock()

                        # Cursor opening
                        open_pos = _r['o'] - len_reduced
                        if _r['oi'] != 0:
                            # open_pos = int(4 * (i - 1))
                            """
                            More about text cursor anchor and movement
                            * https://doc.qt.io/qt-6/qtextcursor.html#anchor
                            * https://doc.qt.io/qt-6/qtextcursor.html#MoveMode-enum

                            More about text cursor position movement
                            * https://doc.qt.io/qt-6/qtextcursor.html#movePosition
                            * https://doc.qt.io/qt-6/qtextcursor.html#MoveOperation-enum

                            `find_cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor, 1)`

                            More about text cursor selection
                            * https://doc.qt.io/qt-6/qtextcursor.html#SelectionType-enum

                            `find_cursor.select(QTextCursor.SelectionType.WordUnderCursor)`
                            `find_cursor.removeSelectedText()`
                            """
                            find_cursor.setPosition(open_pos, QTextCursor.MoveMode.MoveAnchor)
                            # KeepAnchor - the cursor selects the text it moves over.
                            # The same effect as Shift key + moving cursor.
                            find_cursor.setPosition(open_pos + _r['oi'], QTextCursor.MoveMode.KeepAnchor)
                            find_cursor.insertText(_r['repl'])
                            len_reduced += _r['oi'] - (len(_r['repl']) if _r['repl'] else 0)
                        # Cursor closing
                        close_pos = _r['c'] - len_reduced
                        if _r['ci'] != 0:
                            # close_pos = int(2 * (i - 1)) - int(2 * i) # works only for open-close pair of tokens
                            find_cursor.setPosition(close_pos - _r['ci'], QTextCursor.MoveMode.MoveAnchor)
                            find_cursor.setPosition(close_pos, QTextCursor.MoveMode.KeepAnchor)
                            find_cursor.insertText(_r['repl'])
                            len_reduced += _r['ci'] - (len(_r['repl']) if _r['repl'] else 0)

                        find_cursor.setPosition(open_pos, QTextCursor.MoveMode.MoveAnchor)
                        find_cursor.setPosition(close_pos - _r['ci'], QTextCursor.MoveMode.KeepAnchor)

                        if _r['fmt'] is not None:
                            cfc = _r['fmt'].copy()
                            find_cursor.mergeCharFormat(self.highlighter.cf(**cfc))

                        find_cursor.endEditBlock()

            # Move cursor at the end of the block first if the next command fails
            cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock)
            # Next block
            cursor.movePosition(QTextCursor.MoveOperation.NextBlock)

        # Restore original cursor position
        self.restore_cursor_pos()
