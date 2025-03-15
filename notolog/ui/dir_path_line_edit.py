"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Enhances QLineEdit functionality by adding an icon that triggers a QFileDialog action for dir selection.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2025 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QStyle, QLineEdit, QPushButton, QFileDialog
from PySide6.QtGui import QColor

from . import Lexemes
from . import ThemeHelper

import logging


class DirPathLineEdit(QLineEdit):

    button: QPushButton = None

    def __init__(self, parent=None, settings=None, default_directory=None):
        super(DirPathLineEdit, self).__init__(parent)

        self.parent = parent

        if self.parent and hasattr(self.parent, 'font'):
            # Apply font from the main window to the element
            self.setFont(self.parent.font())

        # The class may be in use within settings itself
        self.settings = settings if settings else self.parent.settings  # type: ignore

        self.logger = logging.getLogger('dir_path_line_edit')

        # Load lexemes for the selected language and scope
        self.lexemes = Lexemes(self.settings.app_language, default_scope='common')

        self.theme_helper = ThemeHelper()

        self.default_directory = default_directory

        self.init_ui()

    def init_ui(self):

        self.button = QPushButton(self)

        # Load the dialog icon
        self.load_icon()

        self.button.clicked.connect(self.select_dir_dialog)
        self.button.setCursor(Qt.CursorShape.ArrowCursor)
        self.button.setStyleSheet("QPushButton { border: none; padding: 0; }")
        self.button.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Set the default directory text if provided
        if self.default_directory:
            self.setText(self.default_directory)

        # Ensure the text doesn't overlap the button
        self.setTextMargins(0, 0, 30, 0)

    def load_icon(self):
        # Use either a standard or a custom icon for file selection.
        # folder_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon)  # Set an icon using standard icons
        icon_color = self.theme_helper.get_color('settings_dialog_hint_icon_color')
        folder_icon = self.theme_helper.get_icon(theme_icon='folder.svg', color=QColor(icon_color))
        self.button.setIcon(folder_icon)

    def resizeEvent(self, event):
        button_size = self.button.sizeHint()
        frame_width = self.style().pixelMetric(QStyle.PixelMetric.PM_DefaultFrameWidth)
        self.button.move(self.rect().right() - frame_width - button_size.width(),
                         (self.rect().bottom() - button_size.height() + 1) // 2)
        super(DirPathLineEdit, self).resizeEvent(event)

    def select_dir_dialog(self):
        directory = QFileDialog.getExistingDirectory(self, caption=self.lexemes.get('field_dir_path_dialog_caption'),
                                                     dir=self.text())
        if directory:
            self.setText(directory)
