from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QStatusBar, QWidget, QLabel, QPushButton, QSizePolicy

import logging
from typing import Union

from . import Settings
from . import AppConfig
from . import Lexemes
from . import ThemeHelper

from .sort_filter_proxy_model import SortFilterProxyModel
from .vertical_line_spacer import VerticalLineSpacer


class StatusBar(QStatusBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent = parent

        if self.parent and hasattr(self.parent, 'font'):
            # Apply font from the dialog instance to the label
            self.setFont(self.parent.font())

        self.logger = logging.getLogger('statusbar')

        self.logging = AppConfig().get_logging()
        self.debug = AppConfig().get_debug()

        self.settings = Settings(parent=self)

        self.theme_helper = ThemeHelper()

        # Default language setup, change to settings value to modify it via UI
        self.lexemes = Lexemes(self.settings.app_language, default_scope='statusbar')

        self._elements = {}  # Label storage

        self.litter_bin_label = None  # type: Union[QPushButton, None]

        self.data_size_label = None  # type: Union[QLabel, None]
        self.mode_label = None  # type: Union[QLabel, None]
        self.save_progress_label = None  # type: Union[QLabel, None]
        self.encryption_label = None  # type: Union[QLabel, None]
        self.source_label = None  # type: Union[QLabel, None]
        self.cursor_label = None  # type: Union[QLabel, None]

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
                self.litter_bin_label.setIcon(self.theme_helper.get_icon(theme_icon='trash3-fill.svg',
                    color=QColor(self.theme_helper.get_color('statusbar_litter_bin_icon_color_active'))))
                self.settings.show_deleted_files = True
            else:
                # Remove 'deleted' extension from the tree
                tree_proxy_model.remove_extension('del'),
                self.litter_bin_label.setIcon(self.theme_helper.get_icon(theme_icon='trash3.svg',
                    color=QColor(self.theme_helper.get_color('statusbar_litter_bin_icon_color'))))
                self.settings.show_deleted_files = False

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
            elif self.logging:
                self.logger.warning(f'Trying to set object that is not a QLabel type {type(value)}')

