"""
Notolog Editor
Open-source markdown editor developed in Python.

File Details:
- Purpose: Text view widget.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024 Vadim Bakhrenkov
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

        self.logging = AppConfig().get_logging()
        self.debug = AppConfig().get_debug()

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
        # Double check not to process hyperlink click if an expandable block was clicked
        if anchor and anchor.startswith('expandable'):
            if self.debug:
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

    def loadResource(self, type, url):
        # Log the resource request
        if self.debug:
            self.logger.debug(f"Requesting resource of type {type} at URL: {url.toString()}")
