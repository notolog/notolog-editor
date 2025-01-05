"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Provides app status bar UI.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2025 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QStatusBar, QWidget, QLabel, QPushButton, QSizePolicy

import logging
from typing import TYPE_CHECKING

from . import Settings
from . import Lexemes
from . import ThemeHelper
from . import TooltipHelper

from .sort_filter_proxy_model import SortFilterProxyModel
from .vertical_line_spacer import VerticalLineSpacer

if TYPE_CHECKING:
    from typing import Union  # noqa


class StatusBar(QStatusBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent = parent

        if self.parent and hasattr(self.parent, 'font'):
            # Apply font from the dialog instance to the label
            self.setFont(self.parent.font())

        self.logger = logging.getLogger('statusbar')

        self.settings = Settings(parent=self)

        self.theme_helper = ThemeHelper()

        # Load lexemes for selected language and scope
        self.lexemes = Lexemes(self.settings.app_language, default_scope='statusbar')

        self._elements = {}  # Label storage

        self.litter_bin_label = None  # type: Union[QPushButton, None]

        self.data_size_label = None  # type: Union[QLabel, None]
        self.mode_label = None  # type: Union[QLabel, None]
        self.save_progress_label = None  # type: Union[QLabel, None]
        self.encryption_label = None  # type: Union[QLabel, None]
        self.source_label = None  # type: Union[QLabel, None]
        self.cursor_label = None  # type: Union[QLabel, None]

        self.warning_label = None  # type: Union[QPushButton, None]

        self.init()

    def init(self):
        # Attach style to the QStatusBar and QLabel
        self.setStyleSheet(self.theme_helper.get_css('statusbar'))

        # Litter bin button to show/hide deleted files
        self.litter_bin_label = QPushButton(self)
        self.litter_bin_label.setCursor(Qt.CursorShape.PointingHandCursor)
        self.litter_bin_label.setFont(self.font())
        self.litter_bin_label.setObjectName('statusbar_litter_bin_label')
        self.litter_bin_label.setFlat(True)
        # Theme icon with a fallback to a system one if needed
        # self.theme_helper.get_color('statusbar_...')
        icon = self.theme_helper.get_icon(theme_icon='trash3.svg',
                                          color=QColor(self.theme_helper.get_color('statusbar_litter_bin_icon_color')))
        self.litter_bin_label.setIcon(icon)
        self.litter_bin_label.setText(self.lexemes.get('statusbar_litter_bin_label'))
        self.litter_bin_label.setToolTip(self.lexemes.get('statusbar_litter_bin_label'))
        self.litter_bin_label.setAccessibleName(self.lexemes.get('statusbar_litter_bin_accessible_name'))
        self.litter_bin_label.clicked.connect(lambda: self.toggle_litter_bin_button())

        self.addWidget(self.litter_bin_label)

        central_spacer = QWidget(self)
        central_spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.addPermanentWidget(central_spacer)

        self.data_size_label = QLabel(self)
        self.data_size_label.setFont(self.font())
        self.addPermanentWidget(self.data_size_label)

        self.save_progress_label = QLabel(self)
        self.save_progress_label.setFont(self.font())
        self.save_progress_label.setVisible(False)
        self.save_progress_label.setText(self.lexemes.get('statusbar_save_progress_label'))
        self.addPermanentWidget(self.save_progress_label)

        self.addPermanentWidget(VerticalLineSpacer())

        self.mode_label = QLabel(self)
        self.mode_label.setFont(self.font())
        """
        Do not set object name similar to the lexeme to avoid double update with unprocessed lexeme's placeholders.
        E.g.: self.mode_label.setObjectName('statusbar_mode_label')
        """
        self.addPermanentWidget(self.mode_label)

        self.addPermanentWidget(VerticalLineSpacer())

        self.encryption_label = QLabel(self)
        self.encryption_label.setFont(self.font())
        self.addPermanentWidget(self.encryption_label)

        self.addPermanentWidget(VerticalLineSpacer())

        self.source_label = QLabel(self)
        self.source_label.setFont(self.font())
        self.addPermanentWidget(self.source_label)

        self.addPermanentWidget(VerticalLineSpacer())

        self.cursor_label = QLabel(self)
        self.cursor_label.setFont(self.font())
        self.addPermanentWidget(self.cursor_label)

        self.warning_label = QPushButton(self)
        self.warning_label.setVisible(False)
        self.warning_label.setFlat(True)
        self.warning_label.setFont(self.font())
        self.warning_label.setObjectName('statusbar_warning_label')
        icon = self.theme_helper.get_icon(theme_icon='exclamation-triangle-fill.svg',
                                          color=QColor(self.theme_helper.get_color('statusbar_warning_icon_color')))
        self.warning_label.setIcon(icon)
        self.addPermanentWidget(self.warning_label)
        self.warning_label.clicked.connect(
            lambda: TooltipHelper.show_tooltip(widget=self.warning_label, text=self.warning_label.toolTip()))

    def toggle_litter_bin_button(self):
        self.set_litter_bin_visibility(not self.settings.show_deleted_files)

    def set_litter_bin_visibility(self, visible: bool = False):
        if (hasattr(self, 'parent')
                and hasattr(self.parent, 'tree_proxy_model')
                and isinstance(self.parent.tree_proxy_model, SortFilterProxyModel)):
            # Get tree proxy model to obtain the data
            tree_proxy_model = self.parent.tree_proxy_model  # type: SortFilterProxyModel
            if visible:
                # Add 'deleted' extension to the tree
                tree_proxy_model.add_extension('del'),
                self.litter_bin_label.setIcon(self.theme_helper.get_icon(
                    theme_icon='trash3-fill.svg',
                    color=QColor(self.theme_helper.get_color('statusbar_litter_bin_icon_color_active'))))
                self.settings.show_deleted_files = True
            else:
                # Remove 'deleted' extension from the tree
                tree_proxy_model.remove_extension('del'),
                self.litter_bin_label.setIcon(self.theme_helper.get_icon(
                    theme_icon='trash3.svg',
                    color=QColor(self.theme_helper.get_color('statusbar_litter_bin_icon_color'))))
                self.settings.show_deleted_files = False

    def show_warning(self, visible: bool = False, tooltip: str = None):
        if visible:
            self.warning_label.setVisible(True)
            if tooltip:
                self.warning_label.setToolTip(tooltip)
        else:
            self.warning_label.setVisible(False)
            self.warning_label.setToolTip('')

    def __getitem__(self, name) -> QLabel:
        """
        To get items like:
            self.statusbar['mode_label']
        @param name: string name of the object
        @return: QLabel object
        """
        return self._elements.get(name, f"Label '{name}' not found")

    def __getattr__(self, name) -> QLabel:
        """
        To get items like:
            self.statusbar.mode_label
        @param name: string name of the object
        @return: QLabel object
        """
        return self._elements.get(name, f"Label '{name}' not found")

    def __setattr__(self, name, value):
        if name == '_attributes' or not name.endswith('_label'):
            super().__setattr__(name, value)
        else:
            if (isinstance(value, QLabel)
                    or isinstance(value, QPushButton)
                    or value is None):
                self._elements[name] = value
            else:
                self.logger.warning(f'Trying to set object that is not a QLabel type {type(value)}')
