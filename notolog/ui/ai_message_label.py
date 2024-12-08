"""
Notolog Editor
Open-source markdown editor developed in Python.

File Details:
- Purpose: Extends AI Assistant Dialog Class by formatting and displaying messages from and to the user.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtWidgets import QStyle, QLabel, QPushButton
from PySide6.QtGui import QTextDocument, QColor
from PySide6.QtCore import Qt

from . import Lexemes
from . import ThemeHelper
from . import ClipboardHelper
from . import TooltipHelper

import logging


class AIMessageLabel(QLabel):

    button: QPushButton = None

    def __init__(self, parent=None, text=None, settings=None):
        super(AIMessageLabel, self).__init__(parent)

        self.parent = parent

        if self.parent and hasattr(self.parent, 'font'):
            # Apply font from the main window to the element
            self.setFont(self.parent.font())

        # The class may be in use within settings itself
        self.settings = settings if settings else self.parent.settings  # type: ignore

        self.logger = logging.getLogger('ai_message_label')

        # Load lexemes for selected language and scope
        self.lexemes = Lexemes(self.settings.app_language, default_scope='ai_assistant')

        self.theme_helper = ThemeHelper()

        # Set text
        if text:
            self.setText(text)

        self.init_ui()

    def init_ui(self):

        self.button = QPushButton(self)

        # copy_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon)  # Set an icon using standard icons
        copy_icon = self.theme_helper.get_icon(
            theme_icon='copy.svg',
            color=QColor(self.theme_helper.get_color('ai_assistant_message_icon_color', css_format=True))
        )
        self.button.setIcon(copy_icon)

        self.button.clicked.connect(self.copy_content)
        self.button.setCursor(Qt.CursorShape.ArrowCursor)
        self.button.setFixedSize(20, 20)
        self.button.setStyleSheet("QPushButton { border: none; padding: 0; }")
        self.button.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Ensure the text doesn't overlap the button
        button_size = self.button.sizeHint()
        self.setContentsMargins(0, 0, button_size.width(), 0)

    def resizeEvent(self, event):
        button_size = self.button.sizeHint()
        frame_width = self.style().pixelMetric(QStyle.PixelMetric.PM_DefaultFrameWidth)
        self.button.move(self.rect().right() - frame_width - button_size.width(),
                         (self.rect().top() + button_size.height() + 2) // 2)
        super(AIMessageLabel, self).resizeEvent(event)

    def copy_content(self):
        # Copy text to the clipboard
        ClipboardHelper.set_text(self.get_text_to_copy())
        # Show tooltip
        TooltipHelper.show_tooltip(widget=self.button, text=self.lexemes.get('dialog_message_copied_tooltip'))

    def get_text_to_copy(self):
        # Check if the result needs to be converted from HTML to raw text.
        if getattr(self.settings, 'ai_config_convert_to_md', False):
            # Create a QTextDocument from the label's HTML content.
            doc = QTextDocument()
            doc.setHtml(self.text())

            # Convert the HTML content to raw text.
            return doc.toRawText()

        return self.text()
