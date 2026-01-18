"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Provides a UI for selecting the default application path for documents in a dialog.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import Qt, QDir
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStyle, QSizePolicy
from PySide6.QtWidgets import QDialog, QLineEdit, QLabel, QPushButton
from PySide6.QtGui import QFontMetrics

from . import Settings
from . import Lexemes

from .dir_path_line_edit import DirPathLineEdit
from .message_box import MessageBox

from typing import Union

import os
import logging


class DefaultPathDialog(QDialog):

    def __init__(self, default_path: str = None, parent=None):
        super(DefaultPathDialog, self).__init__(parent)

        self.path = QDir.homePath() if self.check_selected_dir(QDir.homePath()) else QDir.currentPath()
        self.parent = parent

        if self.parent and hasattr(self.parent, 'font'):
            # Apply the font from the main window to this dialog
            self.setFont(self.parent.font())

        self.settings = Settings(parent=self)
        # Set a default path if explicitly provided,
        # or select one from the settings with a fallback to the current directory.
        self.path = default_path if default_path \
            else (self.settings.default_path
                  if hasattr(self.settings, 'default_path') and self.settings.default_path
                  else self.path)

        self.logger = logging.getLogger('path_dialog')

        # Load lexemes for the selected language and scope
        self.lexemes = Lexemes(self.settings.app_language, default_scope='common')

        self.path_field = None  # type: Union[DirPathLineEdit, QLineEdit, None]
        self.ok_button = None  # type: Union[QPushButton, None]
        self.cancel_button = None  # type: Union[QPushButton, None]

        self.init_ui()

    def init_ui(self):
        title = self.lexemes.get('dialog_select_default_dir_title')
        self.setWindowTitle(title)

        path_field_layout = QVBoxLayout()
        path_field_layout.addWidget(QLabel(self.lexemes.get('dialog_select_default_dir_label')))

        # Set parent to None to allow manual addition of the widget
        self.path_field = DirPathLineEdit(parent=None, settings=self.settings, default_directory=self.path)

        self.path_field.setPlaceholderText(self.lexemes.get('dialog_select_default_dir_input_placeholder_text'))
        self.path_field.setEchoMode(QLineEdit.EchoMode.Normal)
        self.path_field.setFocus()
        path_field_layout.addWidget(self.path_field)

        buttons_layout = QHBoxLayout()

        self.ok_button = QPushButton(self.lexemes.get('dialog_select_default_dir_button_ok'))
        self.ok_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon))
        self.ok_button.clicked.connect(self.validate_and_accept)  # or `self.accept`
        self.ok_button.setEnabled(self.check_selected_dir(self.path))

        # https://doc.qt.io/qt-6/qt.html#FocusPolicy-enum
        self.cancel_button = QPushButton(self.lexemes.get('dialog_select_default_dir_button_cancel'),  # noqa
                                         focusPolicy=Qt.FocusPolicy.NoFocus)
        self.cancel_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton))
        self.cancel_button.clicked.connect(self.reject)

        buttons_layout.addWidget(self.cancel_button)
        # Fill the space between the buttons
        spacer_widget = QWidget()
        spacer_widget.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        buttons_layout.addWidget(spacer_widget)
        buttons_layout.addWidget(self.ok_button)

        layout = QVBoxLayout()
        layout.addLayout(path_field_layout)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        self.adjust_minimum_width(title)

        self.path_field.textChanged.connect(self.check_input)

    def check_input(self, dir_name):

        self.path = dir_name

        dir_is_openable = self.check_selected_dir(self.path)

        if not dir_is_openable:
            MessageBox(text=self.lexemes.get('open_dir_permission_error'), icon_type=2, parent=self)

        # Enable the OK button only if the directory is accessible
        self.ok_button.setEnabled(dir_is_openable)

    def check_selected_dir(self, dir_name):
        # Check if the directory exists and is readable
        if dir_name and os.path.exists(dir_name):
            return os.access(dir_name, os.R_OK)
        return False

    def get_path(self) -> Union[str, None]:
        return self.path

    def validate_and_accept(self):
        dir_name = self.path_field.text()

        # Re-check the selected directory
        if self.check_selected_dir(dir_name):
            self.path = dir_name
            # Accept the dialog
            self.accept()
        else:
            MessageBox(text=self.lexemes.get('open_dir_permission_error'), icon_type=2, parent=self)
            return

    def adjust_minimum_width(self, title):
        # Calculate the width required for the title text
        font_metrics = QFontMetrics(self.font())
        title_width = font_metrics.horizontalAdvance(title)

        # Set the minimum width for the dialog
        self.setMinimumWidth(title_width + 150)  # Add some padding

        parent_width = int(self.parent.width() * 0.33) if self.parent else 0
        if self.minimumWidth() < parent_width:
            self.setMinimumWidth(parent_width)
