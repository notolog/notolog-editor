"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Create a new directory UI dialog.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QStyle
from PySide6.QtGui import QFontMetrics

from . import Settings
from . import Lexemes
from . import ThemeHelper

from ..ui.message_box import MessageBox

import os
import logging

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Union  # noqa: F401


class CreateNewDirDialog(QDialog):

    DIR_NAME_MAX_LENGTH = 255

    def __init__(self, base_dir: str, parent=None):
        super().__init__(parent)

        self.parent = parent

        if self.parent and hasattr(self.parent, 'font'):
            # Apply the font from the main window to this dialog
            self.setFont(self.parent.font())

        self.settings = Settings(parent=self)

        self.logger = logging.getLogger('create_new_dir_dialog')

        # Load lexemes for the selected language and scope
        self.lexemes = Lexemes(self.settings.app_language, default_scope='common')

        self.theme_helper = ThemeHelper()

        # Base directory where a new one should be created
        self.base_dir = base_dir

        self.new_dir_name = None  # type: Union[QLineEdit, None]
        self.ok_button = None  # type: Union[QPushButton, None]

        self.init_ui()

    def init_ui(self):

        title = self.lexemes.get('dialog_create_new_dir_title')
        self.setWindowTitle(title)

        new_dir_name_layout = QVBoxLayout()
        new_dir_name_layout.addWidget(QLabel(self.lexemes.get('dialog_create_new_dir_label')))
        self.new_dir_name = QLineEdit()
        self.new_dir_name.setMaxLength(self.DIR_NAME_MAX_LENGTH)  # set maximum length of the input text
        self.new_dir_name.setPlaceholderText(self.lexemes.get('dialog_create_new_dir_input_placeholder_text'))
        self.new_dir_name.setEchoMode(QLineEdit.EchoMode.Normal)
        self.new_dir_name.setFocus()
        new_dir_name_layout.addWidget(self.new_dir_name)

        buttons_layout = QHBoxLayout()

        self.ok_button = QPushButton(self.lexemes.get('dialog_create_new_dir_button_ok'))
        self.ok_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogOkButton))
        self.ok_button.clicked.connect(self.validate_and_accept)  # or `self.accept`
        self.ok_button.setEnabled(False)

        # https://doc.qt.io/qt-6/qt.html#FocusPolicy-enum
        self.cancel_button = QPushButton(self.lexemes.get('dialog_create_new_dir_button_cancel'),  # noqa
                                         focusPolicy=Qt.FocusPolicy.NoFocus)
        self.cancel_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton))
        self.cancel_button.clicked.connect(self.reject)

        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addWidget(self.ok_button)

        layout = QVBoxLayout()
        layout.addLayout(new_dir_name_layout)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        self.adjust_minimum_width(title)

        self.new_dir_name.textChanged.connect(self.check_input_length)

    def check_input_length(self):
        dir_name_length = len(self.new_dir_name.text())

        # Enable OK button only if field have non-zero length
        self.ok_button.setEnabled(dir_name_length and 0 < dir_name_length <= self.DIR_NAME_MAX_LENGTH
                                  or dir_name_length == 0)

    def validate_and_accept(self):
        dir_name = self.new_dir_name.text()

        if not dir_name:
            MessageBox(title=self.lexemes.get('dialog_create_new_dir_warning_empty_title'),
                       text=self.lexemes.get('dialog_create_new_dir_warning_empty_text'), icon_type=2, parent=self)
            return

        if len(dir_name) > self.DIR_NAME_MAX_LENGTH:
            # This statement shouldn't be reachable anyway
            MessageBox(title=self.lexemes.get('dialog_create_new_dir_warning_too_long_title'),
                       text=self.lexemes.get('dialog_create_new_dir_warning_too_long_text',
                                             symbols=self.DIR_NAME_MAX_LENGTH), icon_type=2, parent=self)
            return

        if self.create_new_dir_dialog_callback(new_dir_name=dir_name):
            # Accept dialog result
            self.accept()
        else:
            return

    def create_new_dir_dialog_callback(self, new_dir_name: str) -> bool:
        """
        Actions to perform after create a new directory dialogue.
        """

        # New dir path
        new_dir_path = os.path.join(self.base_dir, new_dir_name)

        self.logger.debug('Creating a new dir "%s" within the "%s" dialog callback'
                          % (new_dir_path, self.base_dir))

        try:
            os.mkdir(new_dir_path)
            self.logger.debug(f"New directory '{new_dir_path}' created successfully.")
            return True
        except FileExistsError:  # if not os.path.exists(new_dir_path):
            self.logger.debug(f"Directory '{new_dir_path}' already exists.")
            # Show error message
            self.parent.message_box(self.lexemes.get('dialog_create_new_dir_error_existed'), icon_type=2)  # noqa
            return False
        except OSError as e:
            self.logger.debug(f"Failed to create directory '{new_dir_path}': {e}")
            # Show error message
            self.parent.message_box(  # noqa
                self.lexemes.get('dialog_create_new_dir_error', base_dir=self.base_dir), icon_type=2)
            return False

    def adjust_minimum_width(self, title):
        # Calculate width required for the title text
        font_metrics = QFontMetrics(self.font())
        title_width = font_metrics.horizontalAdvance(title)

        # Set minimum width for the dialog
        self.setMinimumWidth(title_width + 150)  # Add some padding

    def set_font_size(self, widget, percent):
        default_font_size = self.font().pointSizeF()
        font = widget.font()
        font.setPointSizeF(default_font_size * (percent / 100))
        widget.setFont(font)
