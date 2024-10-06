"""
Notolog Editor
Open-source markdown editor developed in Python.

File Details:
- Purpose: Provides app toolbar UI.
- Functionality: Displays the app's toolbar icons and search form. Supports context menu for adjusting icon elements.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import QSize
from PySide6.QtGui import QAction, QColor
from PySide6.QtWidgets import QToolBar, QWidget, QMenu, QToolButton, QSizePolicy

from . import Settings
from . import AppConfig
from . import Lexemes
from . import ThemeHelper

from ..ui.search_form import SearchForm

from typing import TYPE_CHECKING

import logging

if TYPE_CHECKING:
    from typing import Union  # noqa
    from ..notolog_editor import NotologEditor  # noqa


class ToolBar(QToolBar):
    # Main window toolbar class

    def __init__(self, parent, actions=None, refresh=None):
        """
        Args:
            parent (optional): Parent object
            actions (List[Dict[str, Any]], optional): The map with the toolbar's icons
            refresh (Callable[[int, int], int], optional): A lambda function that refreshes a toolbar
        """
        super(ToolBar, self).__init__(parent)

        self.parent = parent  # type: NotologEditor

        if self.parent and hasattr(self.parent, 'font'):
            # Apply font from the main window to the dialog
            self.setFont(self.parent.font())

        self.logger = logging.getLogger('toolbar')

        self.logging = AppConfig().get_logging()
        self.debug = AppConfig().get_debug()

        self.actions = actions if actions else {}
        self.refresh = refresh

        self.settings = Settings()

        self.theme_helper = ThemeHelper()

        # Load lexemes for selected language and scope
        self.lexemes = Lexemes(self.settings.app_language, default_scope='toolbar')

        if self.settings.toolbar_icons is None or self.settings.toolbar_icons == 0:
            """
            Default bit-mask is 131070 when all icons are checked.
            """
            self.settings.toolbar_icons = 131070
            if self.debug:
                self.logger.info('Starting with default icons mask "%d"' % self.settings.toolbar_icons)

        self.search_form = None  # type: Union[SearchForm, QWidget, None]

        self.toolbar_save_button = None  # type: Union[QToolButton, None]
        self.toolbar_edit_button = None  # type: Union[QToolButton, None]

        self.setMovable(False)

        self.init_ui()

    def init_ui(self):
        """
        Build the toolbar's UI components by dynamically creating toolbar icons and adding a search form
        based on defined actions and settings.
        """

        # Initialize previous icon type to manage delimiters.
        prev_type = None

        # Iterate over action configurations.
        for icon in self.actions:
            if icon['type'] == 'action':
                # Skip the icon addition if it's not enabled in the settings.
                if not (self.settings.toolbar_icons & pow(2, icon['weight'])):
                    continue
                # Skip if the icon's active state check function returns False.
                if ('active_state_check' in icon
                        and callable(icon['active_state_check'])
                        and not icon['active_state_check']()):
                    continue
                # Add the toolbar icon if all conditions are met.
                self.append_toolbar_icon(icon)
            # Add a separator unless the last added item was also a delimiter.
            elif icon['type'] == 'delimiter' and prev_type != 'delimiter':
                self.addSeparator()
            # Update previous icon type to manage delimiters correctly.
            prev_type = icon['type']

        # Add a spacer to separate icons from the search form.
        central_spacer = QWidget(self)
        central_spacer.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        self.addWidget(central_spacer)

        # Initialize and add the search form.
        self.search_form = SearchForm(parent=self)
        self.addWidget(self.search_form)

        # Set the toolbar's stylesheet from the theme helper.
        self.setStyleSheet(self.theme_helper.get_css('toolbar'))

    def append_toolbar_icon(self, conf):
        """
        Helper to create, add to the toolbar and return button with an icon.
        """
        # Theme icon with a fallback to a system one
        system_icon = conf['system_icon'] if 'system_icon' in conf else None
        theme_icon = conf['theme_icon'] if 'theme_icon' in conf else None
        theme_icon_color = QColor(conf['color']) if 'color' in conf \
            else self.theme_helper.get_color('toolbar_icon_color_default')
        icon = self.theme_helper.get_icon(theme_icon=theme_icon, system_icon=system_icon, color=theme_icon_color)

        # Button's action
        label = conf['label'] if 'label' in conf else ''
        icon_action = QAction(icon, label, self)
        action = conf['action'] if 'action' in conf else None  # Action triggered on click
        if action is not None:
            icon_action.triggered.connect(action)

        # Toolbar button itself
        icon_button = QToolButton(self)
        if 'name' in conf:
            icon_button.setObjectName(conf['name'])
        icon_button.setToolTip(label)
        # Set the button height to match the search input field height, maintaining the aspect ratio.
        icon_width = icon_height = int(icon_button.height() * 0.8)
        icon_button.setIconSize(QSize(icon_width, icon_height))
        icon_button.setDefaultAction(icon_action)
        # icon_action.setChecked(True)
        if 'accessible_name' in conf:
            icon_button.setAccessibleName(conf['accessible_name'])

        # Add the button to the toolbar
        self.addWidget(icon_button)

        # Add internal variable to access the icon later, say for state toggle
        if 'var_name' in conf:
            if self.debug and hasattr(self, conf['var_name']):
                self.logger.debug('Variable "%s" is already set! Re-writing it...' % conf['var_name'])
            setattr(self, conf['var_name'], icon_button)  # type: QToolButton
        # If the icon has a switched off check, check it here
        if ('switched_off_check' in conf
                and callable(conf['switched_off_check'])
                and conf['switched_off_check']()):
            # Switch the icon off
            icon_button.setDisabled(True)

    def contextMenuEvent(self, event):
        """
        Render context menu event upon the toolbar right mouse click
        """
        current_action = self.actionAt(event.pos())
        if current_action is None:
            return

        if self.actions is None:
            return

        context_menu = QMenu(self)

        _weights = 0
        for index, label in enumerate(self.actions, 1):
            if 'type' not in label or label['type'] != 'action':
                context_menu.addSeparator()
                continue

            # Get settings weight of the item
            settings_weight = pow(2, label['weight'])

            if _weights & settings_weight:
                # The item is already added or the active state item that shouldn't be duplicated
                continue

            button = QAction(label['label'], self)
            button.setFont(self.font())

            # Method def instead of lambda
            def slot(checked, i=label['weight']):
                self.toolbar_menu_item(checked, i)

            # Check button.toggled.connect()
            button.triggered[bool].connect(slot)
            button.setCheckable(True)
            # Check the item is in the settings weights
            button.setChecked(self.settings.toolbar_icons & settings_weight)

            context_menu.addAction(button)

            # Collect items already added to the context menu
            _weights |= settings_weight

        # PoC remove element from the toolbar
        # delete_action  = menu.addAction("Hide")

        context_menu.exec(event.globalPos())

        # PoC Remove element from the toolbar
        # if action == delete_action:
        #    self.removeAction(current_action)

    def toolbar_menu_item(self, checked: bool, index: int) -> None:
        """
        Draw context menu item with a checkbox

        Args:
            checked (bool): Checked or not
            index (int): Index in a toolbar menu mapping
        """
        pi = pow(2, index)
        if self.debug:
            self.logger.info('checked:{} index:{} pi:{}' . format(checked, index, pi))
        if checked:
            self.settings.toolbar_icons |= pi
        else:
            self.settings.toolbar_icons ^= pi
        # Re-draw toolbar with a callback
        if callable(self.refresh):
            self.refresh()

    # PoC Remove element from the toolbar
    # def removeAction(self, action):
    #    """
    #    Override removeAction() method upon QWidgetAction
    #
    #    Args:
    #        action (QAction):
    #    """
    #    super(ToolBar, self).removeAction(action)
    #
    #    if self.debug:
    #        self.logger.info('Remove element action "%s"' % action)
