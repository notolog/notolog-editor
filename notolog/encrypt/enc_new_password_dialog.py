"""
Notolog Editor
Open-source markdown editor developed in Python.

File Details:
- Purpose: Encrypt file new password UI dialog.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QStyle, QMessageBox
from PySide6.QtGui import QFontMetrics, QFont

from . import Settings
from . import AppConfig
from . import Lexemes
from . import ThemeHelper

import logging


class EncNewPasswordDialog(QDialog):

    HINT_MAX_LENGTH = 32

    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent = parent

        if self.parent and hasattr(self.parent, 'font'):
            # Apply font from the main window to the dialog
            self.setFont(self.parent.font())

        self.settings = Settings(parent=self)

        self.logger = logging.getLogger('enc_new_password_dialog')

        self.logging = AppConfig().get_logging()
        self.debug = AppConfig().get_debug()

        # Load lexemes for selected language and scope
        self.lexemes = Lexemes(self.settings.app_language, default_scope='common')

        self.theme_helper = ThemeHelper()

        title = self.lexemes.get('dialog_encrypt_new_password_title')
        self.setWindowTitle(title)

        password_layout = QVBoxLayout()
        password_layout.addWidget(QLabel(self.lexemes.get('dialog_encrypt_new_password_label')))
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText(self.lexemes.get('dialog_encrypt_new_password_input_placeholder_text'))
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setFocus()
        password_layout.addWidget(self.password_edit)

        hint_layout = QVBoxLayout()
        self.hint_edit = QLineEdit()
        self.hint_edit.setMaxLength(self.HINT_MAX_LENGTH)  # set maximum length of the input text
        hint_layout.addWidget(QLabel(self.lexemes.get('dialog_encrypt_new_password_hint_label')))
        hint_description = QLabel(self.lexemes.get('dialog_encrypt_new_password_hint_label_description'))
        hint_description.setFont(QFont(hint_description.font().family(), italic=True))
        hint_description.setStyleSheet("color: %s" % self.theme_helper.get_color('dialog_encrypt_new_password_hint',
                                                                                 css_format=True))
        self.set_font_size(hint_description, 85)
        hint_layout.addWidget(hint_description)
        self.hint_edit.setPlaceholderText(self.lexemes.get('dialog_encrypt_new_password_hint_input_placeholder_text'))
        hint_layout.addWidget(self.hint_edit)

        buttons_layout = QHBoxLayout()

        self.ok_button = QPushButton(self.lexemes.get('dialog_encrypt_new_password_button_ok'))
        self.ok_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogOkButton))
        self.ok_button.clicked.connect(self.validate_and_accept)  # or `self.accept`
        self.ok_button.setEnabled(False)

        # https://doc.qt.io/qt-6/qt.html#FocusPolicy-enum
        self.cancel_button = QPushButton(self.lexemes.get('dialog_encrypt_new_password_button_cancel'),
                                         focusPolicy=Qt.FocusPolicy.NoFocus)
        self.cancel_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton))
        self.cancel_button.clicked.connect(self.reject)

        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addWidget(self.ok_button)

        layout = QVBoxLayout()
        layout.addLayout(password_layout)
        layout.addLayout(hint_layout)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        self.adjust_minimum_width(title)

        self.password_edit.textChanged.connect(self.check_input_length)
        self.hint_edit.textChanged.connect(self.check_input_length)

    def check_input_length(self):
        password_length = len(self.password_edit.text())
        hint_length = len(self.hint_edit.text())

        # Enable OK button only if both fields have non-zero lengths
        self.ok_button.setEnabled(
            password_length > 0
            and (hint_length and 0 < hint_length <= self.HINT_MAX_LENGTH
                 or hint_length == 0)
        )

    def validate_and_accept(self):
        password = self.password_edit.text()
        hint = self.hint_edit.text()

        if not password:
            QMessageBox.warning(self,
                                self.lexemes.get('dialog_encrypt_new_password_warning_empty_title'),
                                self.lexemes.get('dialog_encrypt_new_password_warning_empty_text'))
            return

        if len(hint) > self.HINT_MAX_LENGTH:
            # This statement shouldn't be reachable anyway
            QMessageBox.warning(self,
                                self.lexemes.get('dialog_encrypt_new_password_warning_too_long_title'),
                                self.lexemes.get('dialog_encrypt_new_password_warning_too_long_text',
                                                 symbols=self.HINT_MAX_LENGTH))
            return

        self.accept()

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
