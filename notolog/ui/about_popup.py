"""
Notolog Editor
Open-source markdown editor developed in Python.

File Details:
- Purpose: About the app dialog class for displaying app's info to the user.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import Qt, QEvent, QUrl
from PySide6.QtGui import QPixmap, QCursor, QDesktopServices
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout, QDialog, QLabel, QFrame, QPushButton, QWidget
from PySide6.QtWidgets import QSizePolicy

from . import Settings
from . import AppConfig
from . import Lexemes
from . import ThemeHelper

from functools import partial

import logging


class AboutPopup(QDialog):
    def __init__(self, parent=None):
        # Popup type may block a screen lock action.
        # Popup is not closing on macOS and no pointing hand cursor.
        # Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint
        super().__init__(parent, Qt.WindowType.Dialog)

        self.parent = parent

        # Apply font from the dialog instance to the label
        self.setFont(self.parent.font())

        self.settings = Settings(parent=self)

        self.logger = logging.getLogger('about_popup')

        # Load lexemes for selected language and scope
        self.lexemes = Lexemes(self.settings.app_language, default_scope='common')

        # Theme helper
        self.theme_helper = ThemeHelper()

        self.init_ui()

        self.setModal(True)  # Set the dialog modal to manage focus more effectively

        # self.adjustSize()  # Adjust size based on content
        """
        main_window_size = self.parent.size()
        dialog_width = int(main_window_size.width() * 0.25)
        dialog_height = int(main_window_size.height() * 0.25)
        # Set dialog size derived from the main window size
        self.setMinimumSize(dialog_width, dialog_height)
        """

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        if self.sizeHint().isValid():
            self.setMinimumSize(self.sizeHint())

    def init_ui(self):
        self.setWindowTitle(self.lexemes.get('popup_about_title'))

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        frame = QFrame(self)
        frame_layout = QGridLayout(frame)
        frame_layout.setVerticalSpacing(15)
        frame_layout.setHorizontalSpacing(25)
        frame.setLayout(frame_layout)

        # Header with an icon and app name
        icon_label = QLabel(self)
        icon_label.setObjectName('app_icon')
        pixmap = (QPixmap(self.theme_helper.get_app_icon_path())
                  .scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio,
                          Qt.TransformationMode.SmoothTransformation))
        icon_label.setPixmap(pixmap)
        frame_layout.addWidget(icon_label, 0, 1, Qt.AlignmentFlag.AlignLeft, 1)

        app_name_widget = QWidget(self)
        app_name_layout = QVBoxLayout(app_name_widget)
        app_name_layout.setSpacing(0)
        app_name_layout.setContentsMargins(0, 0, 0, 0)

        app_name = QLabel(AppConfig().get_app_name(), app_name_widget)
        app_name_font = self.font()
        app_name_font.setPointSizeF(app_name_font.pointSize() * 1.7)
        app_name.setFont(app_name_font)
        app_name.setObjectName('app_name')
        app_name_layout.addWidget(app_name)
        app_name_caption = QLabel(self.lexemes.get('popup_about_app_name_description'), app_name_widget)
        app_name_caption.sizeHint()
        app_name_caption.setObjectName('app_name_caption')
        app_name_layout.addWidget(app_name_caption)

        frame_layout.addWidget(app_name_widget, 0, 2, Qt.AlignmentFlag.AlignLeft, 2)

        # Information fields
        info_fields = [
            (self.lexemes.get('popup_about_version'), AppConfig().get_app_version(), []),
            (self.lexemes.get('popup_about_license'), AppConfig().get_app_license(), []),
            (self.lexemes.get('popup_about_website'), AppConfig().get_app_website(),
             [{'icon': 'box-arrow-up-right.svg', 'link': AppConfig().get_app_website()}]),
            (self.lexemes.get('popup_about_repository'), AppConfig().get_app_repository(),
             [{'icon': 'star-fill.svg', 'link': AppConfig().get_app_repository()}]),
            (self.lexemes.get('popup_about_pypi'), AppConfig().get_app_pypi(),
             [{'icon': 'box-arrow-up-right.svg', 'link': AppConfig().get_app_pypi()}]),
            (self.lexemes.get('popup_about_date'), AppConfig().get_app_date(), [])
        ]

        for i, row in enumerate(info_fields):
            label, value, value_icons = row
            # Label widget
            label_widget = QLabel(f"{label}:", self)
            label_widget.sizeHint()
            label_widget.setObjectName('label_widget')
            # Add label widget to the layout
            frame_layout.addWidget(label_widget, i+1, 1, Qt.AlignmentFlag.AlignLeft, 1)

            # Value widget
            value_widget = QWidget(self)
            value_widget.setObjectName('value_widget')
            value_widget.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            value_layout = QHBoxLayout()
            value_layout.setContentsMargins(0, 0, 0, 0)
            value_layout.setSpacing(5)
            value_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
            value_widget.setLayout(value_layout)

            if value.startswith('http'):
                value_widget_link = QPushButton(value, self)
                value_widget_link.sizeHint()
                value_widget_link.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
                value_widget_link.setObjectName('value_widget_link')
                value_widget_link.clicked.connect(partial(lambda v: QDesktopServices.openUrl(v), value))
                value_widget_link.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                """
                # In case of adding icon ahead of the link:
                value_widget_icon = self.theme_helper.get_icon(theme_icon='...')
                value_widget.setIcon(value_widget_icon)
                """
                value_layout.addWidget(value_widget_link, alignment=Qt.AlignmentFlag.AlignLeft)
            else:
                value_widget_text = QLabel(value, self)
                value_widget_text.sizeHint()
                value_widget_text.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
                value_layout.addWidget(value_widget_text, alignment=Qt.AlignmentFlag.AlignLeft)

            if value_icons:
                for value_icon in value_icons:
                    value_widget_icon_link = QPushButton(self)
                    value_widget_icon_link.setObjectName('value_widget_icon_link')
                    value_widget_icon_link.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                    value_widget_icon_link.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
                    value_widget_icon = self.theme_helper.get_icon(
                        theme_icon=value_icon['icon'], color=self.theme_helper.get_color('popup_about_icon_link'))
                    # If using QLabel instead of QPushButton, the pixmap could be set like this:
                    # value_widget_icon_link.setPixmap(value_widget_icon.pixmap(16, 16))
                    value_widget_icon_link.setIcon(value_widget_icon)
                    value_widget_icon_link.clicked.connect(
                        partial(lambda url: QDesktopServices.openUrl(QUrl(url)), value_icon['link']))
                    value_layout.addWidget(value_widget_icon_link, alignment=Qt.AlignmentFlag.AlignLeft)

            # Add value widget to the layout
            frame_layout.addWidget(value_widget, i+1, 2, Qt.AlignmentFlag.AlignLeft, 2)

        layout.addWidget(frame)

        # Attach CSS-styles
        self.setStyleSheet(self.theme_helper.get_css('about_popup'))

    def eventFilter(self, obj, event):
        # Close the dialog when clicking outside it
        if (event.type() == QEvent.Type.MouseButtonPress
                or event.type() == QEvent.Type.Leave
                or event.type() == QEvent.Type.FocusOut):
            self.close()
        return super().eventFilter(obj, event)
