"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Extends AI Assistant Dialog Class by providing custom QTextEdit functionality for the prompt input field.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtWidgets import QTextEdit
from PySide6.QtGui import QTextOption
from PySide6.QtCore import Qt

from . import Lexemes

import logging


class AIPromptInput(QTextEdit):
    def __init__(self, send_callback, parent=None):
        super().__init__(parent)

        self.parent = parent

        if self.parent and hasattr(self.parent, 'font'):
            # Apply font from the main window to the element
            self.setFont(self.parent.font())

        # Parent settings
        self.settings = self.parent.settings  # type: ignore

        self.logger = logging.getLogger('ai_prompt_input')

        # Load lexemes for the selected language and scope
        self.lexemes = Lexemes(self.settings.app_language, default_scope='ai_assistant')

        # Callback function to handle send request
        self.send_callback = send_callback

        self.init_ui()

    def init_ui(self):
        # Set QTextEdit attributes (e.g., placeholders, font, and interaction flags)
        self.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.setFont(self.parent.font())
        self.setFocus()

        # Calculate height: font metrics height * 2 + some padding
        text_height = self.fontMetrics().height()
        self.setFixedHeight(text_height * 3 + 10)  # Adjust 10 for padding

        self.setPlaceholderText(
            self.lexemes.get('dialog_prompt_input_placeholder_text'))
        self.setAccessibleDescription(
            self.lexemes.get('dialog_prompt_input_accessible_description'))

        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

    def keyPressEvent(self, event):
        # Check for Enter key
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                # Ctrl + Enter: Add a new line
                self.insertPlainText("\n")
            else:
                # Enter: Send the request
                self.send_callback()
        else:
            # Pass other keys to the base class
            super().keyPressEvent(event)
