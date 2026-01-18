"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Text view widget.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QTextBrowser

from .app_config import AppConfig

import logging


class ViewWidget(QTextBrowser):
    """
    Class to implement document view functionality.
    It utilises QTextBrowser power by extending or modifying of the original widget methods.
    """

    content_set = Signal()

    def __init__(self, parent=None):
        """
        Args:
            parent (optional): Parent object
        """
        super(ViewWidget, self).__init__(parent)

        # Get app's global font size
        font = QFont()
        font.setPointSize(AppConfig().get_font_size())
        self.setFont(font)

        self.logger = logging.getLogger('view_widget')

        # Initialize storage for positions and indexes of searched text occurrences.
        self._searched_text_positions = []

    def setDocument(self, document):
        # Override setDocument() to allow additional actions like emit the document set signal
        super().setDocument(document)
        # Emit document set signal to notify listeners
        self.content_set.emit()

    def setHtml(self, html_text):
        # Override setDocument() to allow additional actions like emit the document set signal
        super().setHtml(html_text)
        # Emit document set signal to notify listeners
        self.content_set.emit()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)

        cursor_pos = event.pos()

        anchor = self.anchorAt(cursor_pos)
        # Ensure hyperlink clicks are not processed when clicking on expandable/collapsible blocks.
        if anchor and (anchor.startswith('expandable') or anchor.startswith('collapsible')):
            self.logger.debug("Anchor URL at cursor:", anchor)
            return

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

    def loadResource(self, resource_type, url):
        # Log the resource request
        self.logger.debug(f"Requesting resource of type {resource_type} at URL: {url.toString()}")

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
