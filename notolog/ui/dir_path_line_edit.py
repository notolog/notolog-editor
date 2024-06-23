from PySide6.QtWidgets import QStyle, QLineEdit, QPushButton, QFileDialog
from PySide6.QtCore import Qt

from . import AppConfig
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

        self.logging = AppConfig().get_logging()
        self.debug = AppConfig().get_debug()

        # Load lexemes for selected language and scope
        self.lexemes = Lexemes(self.settings.app_language, default_scope='common')

        self.theme_helper = ThemeHelper()

        self.default_directory = default_directory

        self.init_ui()

    def init_ui(self):

        self.button = QPushButton(self)

        # folder_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon)  # Set an icon using standard icons
        folder_icon = self.theme_helper.get_icon(theme_icon='folder.svg')
        self.button.setIcon(folder_icon)

        self.button.clicked.connect(self.open_file_dialog)
        self.button.setCursor(Qt.CursorShape.ArrowCursor)
        self.button.setStyleSheet("QPushButton { border: none; padding: 0; }")
        self.button.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Set the default directory text if provided
        if self.default_directory:
            self.setText(self.default_directory)

        # Ensure the text doesn't overlap the button
        self.setTextMargins(0, 0, 30, 0)

    def resizeEvent(self, event):
        button_size = self.button.sizeHint()
        frame_width = self.style().pixelMetric(QStyle.PixelMetric.PM_DefaultFrameWidth)
        self.button.move(self.rect().right() - frame_width - button_size.width(),
                         (self.rect().bottom() - button_size.height() + 1) // 2)
        super(DirPathLineEdit, self).resizeEvent(event)

    def open_file_dialog(self):
        directory = QFileDialog.getExistingDirectory(self, self.lexemes.get('field_dir_path_line_edit'), self.text())
        if directory:
            self.setText(directory)
