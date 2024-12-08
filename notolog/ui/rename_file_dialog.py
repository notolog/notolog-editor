"""
Notolog Editor
Open-source markdown editor developed in Python.

File Details:
- Purpose: Provides a file renaming dialog UI.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QInputDialog, QLineEdit, QDialogButtonBox, QSizePolicy

from . import Settings
from . import Lexemes

import logging


class RenameFileDialog(QInputDialog):

    def __init__(self, file_name: str, parent=None):
        super().__init__(parent)

        self.file_name = file_name
        self.parent = parent

        if self.parent and hasattr(self.parent, 'font'):
            # Apply font from the main window to the dialog
            self.setFont(self.parent.font())

        self.settings = Settings(parent=self)

        self.logger = logging.getLogger('rename_file_dialog')

        # Load lexemes for selected language and scope
        self.lexemes = Lexemes(self.settings.app_language, default_scope='common')

        self.init_ui()

    def init_ui(self):
        """
        More info about the enum: https://doc.qt.io/qt-6/qinputdialog.html#InputDialogOption-enum
        dialog.setOption(QInputDialog.InputDialogOption.UsePlainTextEditForTextInput)
        """
        self.setInputMode(QInputDialog.InputMode.TextInput)
        self.setTextEchoMode(QLineEdit.EchoMode.Normal)
        self.setWindowTitle(self.lexemes.get('dialog_file_rename_title'))
        self.setLabelText(self.lexemes.get('dialog_file_rename_field_label'))
        self.setOkButtonText(self.lexemes.get('dialog_file_rename_button_ok'))
        self.setTextValue(self.file_name)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        if self.sizeHint().isValid():
            self.setMinimumSize(self.sizeHint())

        # Set dialog size derived from the main window size
        main_window_size = self.parent.size()
        dialog_width = int(main_window_size.width() * 0.33)
        dialog_height = int(main_window_size.height() * 0.33)
        self.resize(dialog_width, dialog_height)

        """
        Or use fixed size dialog:
        dialog.setFixedSize(dialog_width, dialog_height)
        """
        self.setMinimumSize(QSize(dialog_width, dialog_height))
        # Get the button box and adjust its alignment to center
        button_box = self.findChild(QDialogButtonBox)

        if isinstance(button_box, QDialogButtonBox):
            button_box.setCenterButtons(True)

        """
        Example with color palette:
        pal = dialog.palette()
        pal.setColor(dialog.backgroundRole(), QColor("cyan"))
        dialog.setPalette(pal)
        """
