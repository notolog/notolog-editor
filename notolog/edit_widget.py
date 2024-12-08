"""
Notolog Editor
Open-source markdown editor developed in Python.

File Details:
- Purpose: Text edit widget.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QTextCursor, QTextBlock, QFont
from PySide6.QtWidgets import QPlainTextEdit

from typing import TYPE_CHECKING, Union

from .app_config import AppConfig

import logging

if TYPE_CHECKING:
    from PySide6.QtGui import QTextBlockUserData  # noqa: F401
    from .text_block_data import TextBlockData  # noqa: F401


class EditWidget(QPlainTextEdit):
    # Class to extend or to modify of the original QPlainTextEdit

    content_set = Signal()

    def __init__(self, parent=None):
        """
        Args:
            parent (optional): Parent object
        """
        super(EditWidget, self).__init__(parent)

        # Get app's global font size
        font = QFont()
        font.setPointSize(AppConfig().get_font_size())
        self.setFont(font)

        self.logger = logging.getLogger('edit_widget')

        # Initialize storage for positions and indexes of searched text occurrences.
        self._searched_text_positions = []

        # Disable line wrapping
        # self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        # Disable word wrapping
        # self.setWordWrapMode(QTextOption.WrapMode.NoWrap)

    def setDocument(self, document):
        # Override setDocument() to allow additional actions like emit the document set signal
        super().setDocument(document)
        # Emit document set signal to notify listeners
        self.content_set.emit()

    def setPlainText(self, text):
        # Override setDocument() to allow additional actions like emit the document set signal
        super().setPlainText(text)
        # Emit document set signal to notify listeners
        self.content_set.emit()

    def find_block_by_number(self, block_number: int) -> Union[QTextBlock, None]:
        """
        Notice: Very resource greedy method, avoid it, refactor or change the logic.

        Args:
            block_number (int): Block number to find

        Returns:
            Union[QTextBlock, None]: Returns either a block found by number or None
        """
        cursor = QTextCursor(self.document())
        cursor.movePosition(QTextCursor.MoveOperation.Start)

        while not (cursor.atEnd()
                   # Sometimes, cursor.atEnd() doesn't work, check it
                   or cursor.block().blockNumber() == self.document().blockCount() - 1):
            current_block = cursor.block()
            user_data = current_block.userData()  # type: Union[QTextBlockUserData, TextBlockData]

            if user_data and user_data.block_number == block_number:
                return current_block

            cursor.movePosition(QTextCursor.MoveOperation.NextBlock)

        return None

    def get_current_block(self) -> QTextBlock:
        return self.textCursor().block()

    def keyPressEvent(self, event):
        """
        This method handle key press events.

        Args:
            event (QKeyEvent): Event object
        """
        if event.key() == Qt.Key.Key_Backtab:
            # Shift + Tab action to shift the text block left either on a one tab or 4 spaces.
            self.process_back_tab()
        elif event.key() == Qt.Key.Key_Return and (event.modifiers() & Qt.KeyboardModifier.ShiftModifier):
            # Process Shift + Enter combination to allow Enter-style behaviour
            self.insertPlainText("\n")
            event.accept()
        else:
            # Default behavior for all other key events
            return QPlainTextEdit.keyPressEvent(self, event)

    def process_back_tab(self) -> None:
        """
        Shift the text block left either on a one tab or 4 spaces.
        """
        find_cursor = self.textCursor()
        """
        Current position and selection
        pos - is the position right after the char located behind the cursor; end of selection if selected
        anchor - either the beginning of the selection or the same as pos
        """
        pos = find_cursor.position()
        anchor = find_cursor.anchor()  # Where a selection starts (can be the same as above)

        # Start batch editing
        find_cursor.beginEditBlock()

        # QTextCursor.MoveMode.MoveAnchor applied by default
        find_cursor.setPosition(pos)

        # Count the number of spaces to reduce
        spaces_cnt = 0

        # Start moving the cursor position one symbol backward (QTextCursor.MoveOperation.Left)
        find_cursor.setPosition(pos - 1, QTextCursor.MoveMode.KeepAnchor)
        # Get the character on that new position
        curr_char = find_cursor.document().characterAt(find_cursor.position())
        if curr_char == " ":
            spaces_cnt += 1

        # If non-space characters continue moving cursor to any space alike position
        while (not find_cursor.document().characterAt(find_cursor.position()).isspace()
               and find_cursor.positionInBlock() > 0):
            """
            KeepAnchor makes text selected if combine it with: self.setTextCursor(find_cursor)
            """
            find_cursor.movePosition(QTextCursor.MoveOperation.Left, QTextCursor.MoveMode.MoveAnchor, 1)
            if not find_cursor.document().characterAt(find_cursor.position()).isspace():
                self.setTextCursor(find_cursor)

        # if the cursor text is a space
        if str(find_cursor.selectedText()) == " ":
            # Continue while space characters and not at beginning of the line or when a limit of spaces reached
            while (str(find_cursor.selectedText()).strip() == ""
                   and find_cursor.positionInBlock() > 0
                   and spaces_cnt < 4):
                # Move cursor to the left
                find_cursor.movePosition(QTextCursor.MoveOperation.Left, QTextCursor.MoveMode.KeepAnchor, 1)
                self.setTextCursor(find_cursor)
                cursor_char = find_cursor.document().characterAt(find_cursor.position())
                # Non-space symbol
                if cursor_char != " ":
                    """
                    " "  – Space
                    "\t" – Horizontal tab
                    "\v" – Vertical tab
                    "\n" – Newline
                    "\r" – Carriage return
                    "\f" – Feed
                    """
                    # Non-space character
                    if not cursor_char.isspace():
                        # Move anchor to a new non-space position
                        find_cursor.setPosition(find_cursor.position() + 1, QTextCursor.MoveMode.MoveAnchor)
                        # Move cursor to a new position before the non-space character
                        self.setTextCursor(find_cursor)
                        # Do not process spaces
                        spaces_cnt = 0
                    elif cursor_char == "\t":
                        # Keep anchor to add the preceding spaces to selection
                        find_cursor.setPosition(find_cursor.position() + 1, QTextCursor.MoveMode.KeepAnchor)
                        # Move cursor to a new position before the tab
                        self.setTextCursor(find_cursor)
                    break
                # Count a spaces to reduce
                spaces_cnt += 1

        if spaces_cnt > 0:
            # Reduce the spaces if any exist
            find_cursor.removeSelectedText()
        elif str(find_cursor.selectedText()) == "\t":
            # The prior character is a tab, remove it
            find_cursor.removeSelectedText()
            # Move cursor further left
            find_cursor.setPosition(anchor - 1)
            # Keep anchor from previous setPosition() and continue to move further left
            find_cursor.setPosition(pos - 1, QTextCursor.MoveMode.KeepAnchor)
        else:
            # Restore position
            find_cursor.setPosition(anchor)
            find_cursor.setPosition(pos, QTextCursor.MoveMode.KeepAnchor)

        # Stop batch editing
        find_cursor.endEditBlock()

    def searched_text_count(self, searched_text, find_flags) -> int:
        """
        Counts the number of occurrences of a given text within the document.

        Args:
            searched_text (str): The text string to search for within the document.
            find_flags (QTextDocument.FindFlags): Flags to control the search behavior,
                                                  such as case sensitivity or whole word matching.

        Returns:
            int: The number of times the searched text appears in the document.
        """
        count = 0
        # Reset stored text positions from previous searches to prepare for a new search.
        self._searched_text_positions = []
        # Create a temporary cursor for the search
        # This way, the actual cursor position that the user sees will not be affected.
        temp_cursor = self.textCursor()

        # Move the temporary cursor to the start of the document
        temp_cursor.movePosition(temp_cursor.MoveOperation.Start)

        # Find and count occurrences
        while temp_cursor := self.document().find(searched_text, temp_cursor, find_flags):
            count += 1
            pos = temp_cursor.position()
            if pos not in self._searched_text_positions:
                self._searched_text_positions.append(pos)

        # Reset the stored positions if no occurrence index is found.
        if count == 0:
            self._searched_text_positions = []

        # No need to reset the visual cursor since the original cursor was not moved
        return count

    def searched_text_index(self, position) -> int:
        """
        Shows the index of the occurrence at a given cursor position within the document.

        Args:
            position (int): The cursor position within the document.

        Returns:
            int: The index of the occurrence at a given cursor position within the document.
        """

        if position in self._searched_text_positions:
            return self._searched_text_positions.index(position) + 1
        else:
            return 0

    def contextMenuEvent(self, event):
        # Create the standard context menu
        menu = self.createStandardContextMenu()

        # Modify the menu font to hint the size
        menu.setFont(self.font())

        """
        # Optionally add new actions or modify existing ones
        customAction = menu.addAction("Custom Action")
        customAction.triggered.connect(self.custom_action_triggered)
        """

        # Display the menu
        menu.exec_(event.globalPos())
