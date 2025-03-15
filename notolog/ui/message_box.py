"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Provides a user interface for a message box.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2025 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QMessageBox, QStyle

from . import AppConfig
from . import Settings
from . import Lexemes

import logging


class MessageBox(QMessageBox):

    def __init__(self, title=None, text=None, icon_type=None, callback=None, frameless=None, timer_sec=None, parent=None):
        super().__init__(parent)

        if self.is_quiet_mode():
            return

        self.icon_type = icon_type if icon_type else QMessageBox.Icon.Warning
        self.callback = callback if callback else lambda: True
        self.frameless = frameless
        self.timer_sec = timer_sec
        self.parent = parent

        if self.parent and hasattr(self.parent, 'font'):
            # Apply the font from the main window to this dialog
            self.setFont(self.parent.font())

        self.settings = Settings(parent=self)

        self.logger = logging.getLogger('message_box')

        # Load lexemes for the selected language and scope
        self.lexemes = Lexemes(self.settings.app_language, default_scope='common')

        self.title = title if title else self.lexemes.get('dialog_message_box_title')
        self.text = text if text else ''

        self.button_ok = None

        self.init_ui()

    def init_ui(self):
        if self.frameless:
            # Set the dialog to be frameless
            self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
            # Disable all standard buttons
            self.setStandardButtons(QMessageBox.StandardButton.NoButton)
            self.setModal(False)
            self.setContentsMargins(0, 10, 20, 0)
        else:
            """
            More info about the enum: https://doc.qt.io/qt-6/qmessagebox.html#StandardButton-enum
            Variants:
            * QMessageBox.StandardButton.Yes
            * QMessageBox.StandardButton.No
            """
            self.setStandardButtons(QMessageBox.StandardButton.Ok)
            button_ok = self.button(QMessageBox.StandardButton.Ok)
            button_ok.setText(self.lexemes.get('dialog_message_box_button_ok'))
            # Set default button
            self.setDefaultButton(QMessageBox.StandardButton.Ok)

        """
        More info about the enum: https://doc.qt.io/qt-6/qmessagebox.html#Icon-enum
        Variants:
        * NoIcon(0)
        * Information(1)
        * Warning(2)
        * Critical(3)
        * Question(4)
        """
        self.setIcon(QMessageBox.Icon(self.icon_type))
        self.setWindowTitle(self.title)
        self.setText(self.text)

        if self.parent:
            self.setGeometry(QStyle.alignedRect(
                Qt.LayoutDirection.LeftToRight,
                Qt.AlignmentFlag.AlignCenter,
                self.size(),
                self.parent.geometry()))

        # Start the timer before showing the dialog
        if self.timer_sec is not None:
            QTimer.singleShot(self.timer_sec * 1000, lambda: self.accept())

        if self.frameless:
            # Use open() to display a non-blocking message box
            self.open()
            return

        # Show the dialog
        self.exec()

        if self.clickedButton() == self.button_ok:
            self.logger.debug('Message box button clicked')
            # Execute the callback function if it is defined
            if callable(self.callback):
                self.callback()

    @staticmethod
    def is_quiet_mode():
        """ Setting quiet mode for test purposes. """
        return AppConfig().get_test_mode()
