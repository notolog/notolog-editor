"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Extends QLabel functionality by adding an icon with a customizable hint tooltip.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2025 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QLabel, QToolButton, QHBoxLayout
from PySide6.QtGui import QIcon, QColor, QPixmap

import logging

from ..settings import Settings
from ..helpers.theme_helper import ThemeHelper

from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from ..notolog_editor import NotologEditor  # noqa: F401


class LabelWithHint(QLabel):
    def __init__(self, parent, text=None, action=None, theme_icon=None, tooltip: Union[dict, tuple] = None):
        super().__init__(parent)

        self.parent = parent  # type: NotologEditor

        if self.parent and hasattr(self.parent, 'font'):
            # Apply font from the main window to the dialog
            self.setFont(self.parent.font())

        self.logger = logging.getLogger('label_with_hint')

        self.text = text
        self.action = action
        self.tooltip = tooltip
        self.theme_icon = theme_icon

        # Default icon
        if not self.theme_icon:
            self.theme_icon = 'question-circle.svg'

        self.theme_helper = ThemeHelper()

        self.settings = Settings()

        self.layout = None  # type: Union[QHBoxLayout, None]
        self.text_label = None  # type: Union[QLabel, None]
        self.icon_button = None  # type: Union[QToolButton, None]

        self.init_ui()

    def init_ui(self):
        # Main layout
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)
        self.setLayout(self.layout)

        # Create icon button
        self.icon_button = QToolButton()
        self.icon_button.setCursor(Qt.CursorShape.WhatsThisCursor)
        self.icon_button.setStyleSheet("border: none;")  # Remove button border
        # Load icon
        self.load_icon()
        # Set the tooltip text for the icon if applicable
        if self.tooltip:
            self.load_tooltip(self.tooltip)

        # Set the click action for the icon
        if self.action:
            self.icon_button.clicked.connect(self.action)

        # Create the text label
        self.text_label = QLabel(self.text)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        # Add icon and text to the layout
        self.layout.addWidget(self.text_label)
        self.layout.addWidget(self.icon_button, alignment=Qt.AlignmentFlag.AlignRight)

    def load_icon(self):
        """
        Load and set the icon for the button.
        """

        # Retrieve the icon color from the theme
        icon_color = self.theme_helper.get_color('settings_dialog_hint_icon_color')

        # Get the icon path with the specified theme and color
        icon_path = self.theme_helper.get_icon(theme_icon=self.theme_icon, color=QColor(icon_color))

        # Determine the text height using font metrics
        font_metrics = self.fontMetrics()
        text_height = font_metrics.height()

        # Create a QPixmap for the icon, scaled to match the text height
        pixmap = QPixmap(icon_path.pixmap(QSize(text_height, text_height)))
        pixmap.scaled(text_height, text_height,
                      Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

        # Set the icon on the button
        self.icon_button.setIcon(QIcon(pixmap))

    def load_tooltip(self, tooltip):
        """
        Extract and set the tooltip data for the button.

        Args:
            tooltip (dict or tuple): Tooltip data containing the lexeme and text.
        """

        # Extract tooltip data based on type
        if isinstance(tooltip, dict):  # Handle dict
            tooltip_lexeme, tooltip_text = next(iter(tooltip.items()))
        elif isinstance(tooltip, tuple):  # Handle tuple
            tooltip_lexeme, tooltip_text = tooltip
        else:
            raise TypeError(f"Expected a dict or tuple: {tooltip}")

        # Store the tooltip lexeme for potential future use
        self.setProperty("tooltip_lexeme", tooltip_lexeme)

        # Set the tooltip text and appearance
        self.set_tooltip(tooltip_text)

    def set_tooltip(self, tooltip_text):
        """
        Set the tooltip text and style.

        Args:
            tooltip_text (str): The text to display in the tooltip.
        """

        # Determine the text height using font metrics
        font_metrics = self.fontMetrics()
        text_height = font_metrics.height()

        # Set the tooltip text
        self.icon_button.setToolTip(tooltip_text)

        # Customize the tooltip font size
        self.setStyleSheet("QToolTip { font-size: %dpx; }" % (text_height * 0.8))
