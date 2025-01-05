"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Color Picker dialog class.
- Functionality: Allows displaying, inserting, or copying a selected color.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2025 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QGridLayout, QDialog, QPushButton

from . import Settings
from . import Lexemes

from ..enums.colors import Colors

from functools import partial

import logging


class ColorPickerDialog(QDialog):

    color_selected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowType.Window | Qt.WindowType.WindowStaysOnTopHint)

        self.parent = parent

        self.settings = Settings(parent=self)

        self.logger = logging.getLogger('color_picker_dialog')

        # Load lexemes for selected language and scope
        self.lexemes = Lexemes(self.settings.app_language, default_scope='color_picker_dialog')

        self.setWindowTitle(self.lexemes.get('color_picker_title'))
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.layout = QGridLayout(self)
        self.layout.setSpacing(3)

        self.init_ui()

    def init_ui(self):
        row = col = 0
        for color in Colors:
            button = QPushButton(self)
            button.setToolTip(self.lexemes.get(f'color_picker_color_{color.name.lower()}'))
            # The style is not theme dependant, hence no need to move it out from the code.
            # The border color can be adjusted, place it to the theme's .ini file.
            button.setStyleSheet("""
            QPushButton {
                background-color: %s;
                border: 1px solid silver;
            }
            """ % color.name)
            button.setFixedSize(32, 32)
            button.clicked.connect(partial(self.color_chosen, color.name.lower()))
            self.layout.addWidget(button, row, col)
            col += 1
            if col >= 13:  # Based on colors count
                col = 0
                row += 1

    def color_chosen(self, color):
        self.color_selected.emit(color)
        # Close the dialog if any color selected
        self.accept()
