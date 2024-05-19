from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QDialogButtonBox, QSizePolicy
from PySide6.QtGui import QFontMetrics

from typing import Optional, Callable, Any

from . import Settings
from . import AppConfig
from . import Lexemes

import logging


class EncPasswordResetDialog(QDialog):

    def __init__(self, callback: Optional[Callable[..., Any]] = None, parent=None):
        super().__init__(parent)

        self.parent = parent

        if self.parent and hasattr(self.parent, 'font'):
            # Apply font from the main window to the dialog
            self.setFont(self.parent.font())

        self.settings = Settings(parent=self)

        self.logger = logging.getLogger('enc_password_reset_dialog')

        self.logging = AppConfig().get_logging()
        self.debug = AppConfig().get_debug()

        # Default language setup, change to settings value to modify it via UI
        self.lexemes = Lexemes(self.settings.app_language, default_scope='common')

        title = self.lexemes.get('dialog_encrypt_password_reset_title')
        self.setWindowTitle(title)
        self.setObjectName('dialog_encrypt_password_reset_title')

        # Adjust dialog size
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        if self.sizeHint().isValid():
            self.setMinimumSize(self.sizeHint())

        label = QLabel()
        label.setObjectName('dialog_encrypt_password_reset_text')
        label.setText(self.lexemes.get('dialog_encrypt_password_reset_text'))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if label.sizeHint().isValid():
            label.setMinimumSize(label.sizeHint())
        label.adjustSize()

        button_box = QDialogButtonBox()
        button_box.setObjectName('dialog_encrypt_password_reset_button_box')
        button_box.setOrientation(Qt.Orientation.Horizontal)
        # Check translations
        button_box.setStandardButtons(QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Yes)
        button_box.setCenterButtons(True)

        button_cancel = button_box.button(QDialogButtonBox.StandardButton.Cancel)
        button_cancel.setText(self.lexemes.get('dialog_encrypt_password_reset_button_cancel'))
        button_yes = button_box.button(QDialogButtonBox.StandardButton.Yes)
        button_yes.setText(self.lexemes.get('dialog_encrypt_password_reset_button_yes'))

        # not `self` to avoid: 'Attempting to add QLayout "" to ... "", which already has a layout
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button_box)
        self.setLayout(layout)

        self.adjust_minimum_width(title)

        button_box.accepted.connect(lambda: callback(callback=self.reject) if callable(callback) else self.reject)
        button_box.rejected.connect(self.reject)

    def adjust_minimum_width(self, title: str) -> None:
        # Calculate width required for the title text
        font_metrics = QFontMetrics(self.font())
        title_width = font_metrics.horizontalAdvance(title)

        # Set minimum width for the dialog
        self.setMinimumWidth(title_width + 150)  # Add some padding
