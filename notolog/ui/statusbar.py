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

from PySide6.QtCore import Qt, QDir
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QStatusBar, QWidget, QLabel, QPushButton, QSizePolicy

import logging
from typing import TYPE_CHECKING, Any, Dict, List

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
        self.settings.value_changed.connect(
            lambda v: self.settings_update_handler(v))

        self.theme_helper = ThemeHelper()

        # Load lexemes for selected language and scope
        self.lexemes = Lexemes(self.settings.app_language, default_scope='statusbar')

        self._elements = {}  # Label storage

        self.data_size_label = None  # type: Union[QLabel, None]
        self.mode_label = None  # type: Union[QLabel, None]
        self.save_progress_label = None  # type: Union[QLabel, None]
        self.encryption_label = None  # type: Union[QLabel, None]
        self.source_label = None  # type: Union[QLabel, None]
        self.cursor_label = None  # type: Union[QLabel, None]

        self.warning_label = None  # type: Union[QPushButton, None]

        self.init()

    def init(self):
        # Attach styles to the QStatusBar
        self.setStyleSheet(self.theme_helper.get_css('statusbar'))

        # Draw the statusbar icons
        self.draw_icons()

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
        Do not set object name similar to the lexeme to avoid double update with the unprocessed lexeme's placeholders.
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

    def get_statusbar_icons(self) -> List[Dict[str, Any]]:
        """
        Main statusbar items map for convenience.
        """
        return [
            # Litter bin (inactive)
            {'type': 'action', 'weight': 1, 'name': 'statusbar_litter_bin_label', 'system_icon': 'user-trash',
             'theme_icon': 'trash3.svg', 'color': self.theme_helper.get_color('statusbar_litter_bin_icon_color'),
             'label': self.lexemes.get('statusbar_litter_bin_label'),
             'accessible_name': self.lexemes.get('statusbar_litter_bin_accessible_name'),
             'action': lambda: self.set_litter_bin_visibility(True), 'var_name': 'litter_bin_label',
             'active_state_check': lambda: not self.settings.show_deleted_files},
            # Litter bin (active)
            {'type': 'action', 'weight': 1, 'name': 'statusbar_litter_bin_label_active', 'system_icon': 'user-trash-full',
             'theme_icon': 'trash3-fill.svg', 'color': self.theme_helper.get_color('statusbar_litter_bin_icon_color_active'),
             'label': self.lexemes.get('statusbar_litter_bin_label'),
             'accessible_name': self.lexemes.get('statusbar_litter_bin_accessible_name'),
             'action': lambda: self.set_litter_bin_visibility(False), 'var_name': 'litter_bin_label',
             'active_state_check': lambda: self.settings.show_deleted_files},
            # Home button
            {'type': 'action', 'weight': 2, 'name': 'statusbar_path_home_label', 'system_icon': 'go-home',
             'theme_icon': 'house-door.svg', 'color': self.theme_helper.get_color('statusbar_path_home_icon_color'),
             'label': self.lexemes.get('statusbar_path_home_label'),
             'accessible_name': self.lexemes.get('statusbar_path_home_accessible_name'),
             'action': self.action_path_home, 'var_name': 'path_home_label'},
        ]

    def get_statusbar_icon_by_name(self, name):
        """
        Get particular button config by name.
        """
        for button in self.get_statusbar_icons():
            if 'name' in button and button['name'] == name:
                return button

    def draw_icons(self):
        # Iterate over action configurations.
        for conf in self.get_statusbar_icons():
            if conf['type'] == 'action':
                # Skip if the icon's active state check function returns False.
                if ('active_state_check' in conf
                        and callable(conf['active_state_check'])
                        and not conf['active_state_check']()):
                    continue
                # Add the statusbar icon if all conditions are met
                existed_icon = getattr(self, conf['var_name']) if hasattr(self, conf['var_name']) else None
                self.append_statusbar_icon(conf, existed_icon)

    def append_statusbar_icon(self, conf, button=None):
        """
        Helper to create, add to the statusbar and return button with an icon.
        """
        # Use a themed icon with a fallback to a system icon
        system_icon = conf['system_icon'] if 'system_icon' in conf else None
        theme_icon = conf['theme_icon'] if 'theme_icon' in conf else None
        theme_icon_color = QColor(conf['color']) if 'color' in conf \
            else self.theme_helper.get_color('statusbar_icon_color_default')
        icon = self.theme_helper.get_icon(theme_icon=theme_icon, system_icon=system_icon, color=theme_icon_color)

        # Button with an icon
        label = conf['label'] if 'label' in conf else ''
        icon_button = button if isinstance(button, QPushButton) else QPushButton(self)
        icon_button.setFlat(True)
        icon_button.setIcon(icon)
        icon_button.setCursor(Qt.CursorShape.PointingHandCursor)
        action = conf['action'] if 'action' in conf else None  # Action triggered on click
        if action is not None:
            icon_button.clicked.connect(action)
        if 'name' in conf:
            icon_button.setObjectName(conf['name'])
        icon_button.setToolTip(label)
        # icon_button.setChecked(True)
        if 'accessible_name' in conf:
            icon_button.setAccessibleName(conf['accessible_name'])

        # Add the button to the statusbar
        self.addWidget(icon_button)

        # Add an internal variable to access the icon later, e.g., for state toggling
        if 'var_name' in conf:
            if hasattr(self, conf['var_name']):
                self.logger.debug('Variable "%s" is already set! Re-writing it...' % conf['var_name'])
            setattr(self, conf['var_name'], icon_button)  # type: QPushButton
        # If the icon has a switched-off check, handle it here
        if ('switched_off_check' in conf
                and callable(conf['switched_off_check'])
                and conf['switched_off_check']()):
            # Switch the icon off
            icon_button.setDisabled(True)

    def action_path_home(self) -> None:
        # Use QDir.homePath() or QDir.currentPath() as a fallback option
        default_path = self.settings.default_path if self.settings.default_path else QDir.homePath()
        if self.parent and hasattr(self.parent, 'set_current_path') and callable(self.parent.set_current_path):
            self.parent.set_current_path(default_path)

    def settings_update_handler(self, data: dict) -> None:
        """
        Perform actions upon settings change.
        Data comes in a view of a dictionary, where is the key is the setting name, and the value is the actual value.
        Can be resource greedy.

        @param data: dict, say {"show_deleted_files": True}
        @return: None
        """

        self.logger.debug('Settings update handler is in use "%s"' % data)

        if 'show_deleted_files' in data and hasattr(self, 'litter_bin_label'):
            # Update the state of the litter bin icon button
            if self.settings.show_deleted_files:
                conf = self.get_statusbar_icon_by_name('statusbar_litter_bin_label_active')
            else:
                conf = self.get_statusbar_icon_by_name('statusbar_litter_bin_label')
            # Update an existing button
            self.append_statusbar_icon(conf, self.litter_bin_label)

        if 'app_theme' in data:
            self.draw_icons()

    def toggle_litter_bin_button(self):
        self.set_litter_bin_visibility(not self.settings.show_deleted_files)

    def set_litter_bin_visibility(self, visible: bool = False):
        if (hasattr(self, 'parent')
                and hasattr(self.parent, 'tree_proxy_model')
                and isinstance(self.parent.tree_proxy_model, SortFilterProxyModel)):
            # Get tree proxy model to obtain the data
            tree_proxy_model = self.parent.tree_proxy_model  # type: SortFilterProxyModel
            if visible:
                # Add the 'deleted' extension to the tree
                tree_proxy_model.add_extension('del'),
                self.settings.show_deleted_files = True
            else:
                # Remove the 'deleted' extension from the tree
                tree_proxy_model.remove_extension('del'),
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
