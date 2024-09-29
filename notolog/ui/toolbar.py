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

from PySide6.QtGui import QAction, QColor
from PySide6.QtWidgets import QToolBar, QWidget, QMenu, QToolButton, QSizePolicy

from . import Settings
from . import AppConfig
from . import Lexemes
from . import ThemeHelper

from ..ui.search_form import SearchForm

from typing import TYPE_CHECKING, Any, List, Dict

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

        self.search_buttons = self.get_toolbar_search_buttons()

        self.init_ui()

    def init_ui(self):
        prev_type = None
        for icon in self.actions:
            if icon['type'] == 'action':
                # Check visible icon is checked in settings
                if not (self.settings.toolbar_icons & pow(2, icon['weight'])):
                    # Skip if not checked in settings
                    continue
                # If the icon has an active state check, check it here
                if ('active_state_check' in icon
                        and callable(icon['active_state_check'])
                        and not icon['active_state_check']()):
                    # Skip if the icon isn't active
                    continue
                # Create and append toolbar icon
                self.append_toolbar_icon(icon)
            elif icon['type'] == 'delimiter' and prev_type != 'delimiter':
                self.addSeparator()
            # Save prev type
            prev_type = icon['type']

        central_spacer = QWidget(self)
        central_spacer.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        self.addWidget(central_spacer)

        self.search_form = SearchForm(parent=self, search_buttons=self.search_buttons)
        self.addWidget(self.search_form)

        """
        It can be done by setting inline styles, but this is not what can be convenient for customisation,
        hence the theme:
        """
        # self.toolbar.setStyleSheet("""QCheckBox {
        #    margin-right: 5px;
        # }""")
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
        # icon_button.setIconSize(QSize(16, 16));
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

    def get_toolbar_search_buttons(self) -> List[Dict[str, Any]]:
        """
        Retrieves the configuration map for search-related toolbar buttons.

        Note: The 'var_name' parameter will be initialized in the final object that utilizes this map.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries detailing the configuration of each toolbar search button.
        """

        return [
            {'type': 'action', 'name': 'search_clear', 'system_icon': 'window-close', 'theme_icon': 'x-circle-fill.svg',
             'action': self.parent.action_search_clear, 'enabled': False, 'default': False,
             'tooltip': self.lexemes.get('search_buttons_label_clear', scope='toolbar'),
             'accessible_name': self.lexemes.get('search_buttons_accessible_name_clear', scope='toolbar'),
             'var_name': 'btn_search_clear', 'color': self.theme_helper.get_color('toolbar_search_button_clear')},
            {'type': 'action', 'name': 'search_prev', 'system_icon': 'go-up', 'theme_icon': 'caret-up-fill.svg',
             'action': self.parent.action_search_prev, 'enabled': False, 'default': False,
             'tooltip': self.lexemes.get('search_buttons_label_prev', scope='toolbar'),
             'accessible_name': self.lexemes.get('search_buttons_accessible_name_prev', scope='toolbar'),
             'var_name': 'btn_search_prev', 'color': self.theme_helper.get_color('toolbar_search_button_prev')},
            {'type': 'action', 'name': 'search_next', 'system_icon': 'go-down', 'theme_icon': 'caret-down-fill.svg',
             'action': self.parent.action_search_next, 'enabled': False, 'default': True,
             'tooltip': self.lexemes.get('search_buttons_label_next', scope='toolbar'),
             'accessible_name': self.lexemes.get('search_buttons_accessible_name_next', scope='toolbar'),
             'var_name': 'btn_search_next', 'color': self.theme_helper.get_color('toolbar_search_button_next')},
        ]

    def get_toolbar_search_button_by_name(self, name: str) -> Dict:
        """
        Get particular search button config by name.
        """
        for button in self.get_toolbar_search_buttons():
            if 'name' in button and button['name'] == name:
                return button

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
