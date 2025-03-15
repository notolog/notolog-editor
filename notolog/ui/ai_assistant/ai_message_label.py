"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Extends AI Assistant Dialog Class by formatting and displaying messages from and to the user.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2025 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtWidgets import QStyle, QSizePolicy, QLabel, QPushButton
from PySide6.QtGui import QTextDocument, QColor
from PySide6.QtCore import Qt

from . import Lexemes
from . import ThemeHelper
from . import ClipboardHelper
from . import TooltipHelper

import logging


class AIMessageLabel(QLabel):

    button: QPushButton = None

    def __init__(self, parent=None, text=None, color=None, bg_color=None, settings=None):
        super(AIMessageLabel, self).__init__(parent)

        self.parent = parent

        if self.parent and hasattr(self.parent, 'font'):
            # Apply font from the main window to the element
            self.setFont(self.parent.font())

        # The class may be in use within settings itself
        self.settings = settings if settings else self.parent.settings  # type: ignore

        self.logger = logging.getLogger('ai_message_label')

        # Load lexemes for the selected language and scope
        self.lexemes = Lexemes(self.settings.app_language, default_scope='ai_assistant')

        self.theme_helper = ThemeHelper()

        # Set the text
        if text:
            self.setText(text)

        # Assign colors to QLabel for styling
        self.color = color if color else 'palette(text)'
        self.bg_color = bg_color if bg_color else 'palette(base)'

        self.init_ui()

    def init_ui(self):
        # Set QLabel attributes (e.g., text, font, and interaction flags)
        self.setWordWrap(True)
        self.setStyleSheet(""" QLabel {
            border-radius: 5px;
            margin: 5px 0;
            padding: 5px;
            color: %s;
            background-color: %s;
        } """ % (self.color, self.bg_color))

        palette = self.palette()
        palette.setColor(self.foregroundRole(), QColor(self.color))
        palette.setColor(self.backgroundRole(), QColor(self.bg_color))

        self.setPalette(palette)
        self.setAutoFillBackground(True)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        self.button = QPushButton(self)

        # copy_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon)  # Set an icon using standard icons
        copy_icon = self.theme_helper.get_icon(
            theme_icon='copy.svg',
            color=QColor(self.theme_helper.get_color('ai_assistant_message_icon_color', css_format=True))
        )
        self.button.setIcon(copy_icon)

        self.button.clicked.connect(self.copy_content)
        self.button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button.setFixedSize(20, 20)
        self.button.setStyleSheet("QPushButton { border: none; padding: 0; }")
        self.button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.button.setToolTip(self.lexemes.get('dialog_message_copy_tooltip'))

        # Ensure the text doesn't overlap the button
        button_size = self.button.sizeHint()
        self.setContentsMargins(0, 0, button_size.width(), 0)

        # Enable text selection in QLabel using the mouse
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

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
