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

from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QAction, QColor
from PySide6.QtWidgets import QToolBar, QWidget, QMenu, QLabel, QLineEdit, QCheckBox, QToolButton, QPushButton, QHBoxLayout
from PySide6.QtWidgets import QSizePolicy

from . import Settings
from . import AppConfig
from . import Lexemes
from . import ThemeHelper

from typing import TYPE_CHECKING

import logging

if TYPE_CHECKING:
    from typing import Union  # noqa


class ToolBar(QToolBar):
    # Main window toolbar class

    def __init__(self, parent=None, actions=None, search_buttons=None, refresh=None):
        """
        Args:
            parent (optional): Parent object
            actions (List[Dict[str, Any]], optional): The map with the toolbar's icons
            search_buttons (List[Dict[str, Any]], optional): The map with the toolbar's search buttons
            refresh (Callable[[int, int], int], optional): A lambda function that refreshes a toolbar
        """
        super(ToolBar, self).__init__(parent)

        if self.parent and hasattr(self.parent, 'font'):
            # Apply font from the main window to the dialog
            self.setFont(self.parent.font())

        self.logger = logging.getLogger('toolbar')

        self.logging = AppConfig().get_logging()
        self.debug = AppConfig().get_debug()

        self.actions = actions if actions else {}
        self.search_buttons = search_buttons if search_buttons else {}
        self.refresh = refresh

        self.settings = Settings()

        self.theme_helper = ThemeHelper()

        # Load lexemes for selected language and scope
        self.lexemes = Lexemes(self.settings.app_language, default_scope='toolbar')

        # Sometimes (when weights changed) the values could be reset like this:
        # self.settings.toolbar_icons = None

        if self.settings.toolbar_icons is None or self.settings.toolbar_icons == 0:
            """
            Default bit-mask is 131070 when all icons are checked.
            """
            self.settings.toolbar_icons = 131070
            if self.debug:
                self.logger.info('Starting with default icons mask "%d"' % self.settings.toolbar_icons)

        self.search_input = None  # type: Union[ToolBar.SearchLineEdit, QWidget, None]
        self.search_match_case = None  # type: Union[QCheckBox, None]
        self.search_match_case = None  # type: Union[QCheckBox, None]
        # Search navigation button variables will be set via mapping

        self.toolbar_save_button = None  # type: Union[QToolButton, None]
        self.toolbar_edit_button = None  # type: Union[QToolButton, None]

        self.setMovable(False)

        self.init_ui()

    class SearchLineEdit(QWidget):
        """
        Custom search line edit widget that integrates a QLineEdit for input, QLabel for input labels,
        to show the actual label and count of search results.
        This widget also exposes signals similar to a QLineEdit for external interaction.
        """

        # Signals to mimic QLineEdit's textChanged and returnPressed events.
        textChanged = Signal(str)
        returnPressed = Signal()

        def __init__(self, lexemes):
            super().__init__()

            self.lexemes = lexemes

            # Placeholder attributes for component widgets, initialized in init_ui.
            self._search_input = None  # type: Union[QLineEdit, None]
            self._search_input_label = None  # type: Union[QLabel, None]
            self._search_count_label = None  # type: Union[QLabel, None]

            self.init_ui()

        def init_ui(self):
            # Set up the main layout and internal components
            search_layout = QHBoxLayout(self)
            search_layout.setContentsMargins(0, 0, 0, 0)
            search_layout.setSpacing(0)

            self._search_input_label = QLabel(self)
            # Apply font from the main window to the widget
            self._search_input_label.sizeHint()
            self._search_input_label.setText(self.lexemes.get('search_input_label'))
            self._search_input_label.setObjectName('search_input_label')  # To differentiate it at styles file

            search_layout.addWidget(self._search_input_label)

            # Searched text
            self._search_input = QLineEdit(self)
            self._search_input.setObjectName('search_input')
            self._search_input.sizeHint()
            self._search_input.setReadOnly(False)
            self._search_input.setMaxLength(128)
            self._search_input.setPlaceholderText(self.lexemes.get('search_input_placeholder_text'))
            self._search_input.setAccessibleDescription(self.lexemes.get('search_input_accessible_description'))

            # Connect the QLineEdit's textChanged signal to the custom widget's textChanged signal
            self._search_input.textChanged.connect(self.emit_text_changed)
            self._search_input.returnPressed.connect(self.returnPressed.emit)

            # Count occurrences of the searched text
            self._search_count_label = QLabel('', self)
            self._search_count_label.setObjectName('search_count_label')
            self._search_count_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
            self._search_count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center text in QLabel

            # Add UI component to the layout
            search_layout.addWidget(self._search_input)

            self.adjust_size()

            self._search_count_label.raise_()  # Ensure QLabel is visually layered above other widgets if overlapping.

        def emit_text_changed(self, text):
            """ Emit the custom textChanged signal with the current text as the argument to notify of text changes. """
            self.textChanged.emit(text)

        def text(self):
            return self._search_input.text()

        def set_text(self, text):
            """
            Proxy method to set the text of the underlying QLineEdit.
            """
            return self._search_input.setText(text)

        def set_focus(self):
            self._search_input.setFocus()

        def set_maximum_width(self, width):
            self.setMaximumWidth(width)

        def set_placeholder_text(self, text):
            self._search_input.setPlaceholderText(text)

        def set_counter_text(self, text):
            """ Set the text of the embedded QLineEdit. """
            self._search_count_label.setText(text)
            self.adjust_size()

        def adjust_size(self):
            """
            Adjusts the visibility and dimensions of the search count label based on its content and the search input's size.
            Only shows the count label if there are search results to display.
            """

            # Show label if not an empty text
            self._search_count_label.setVisible(True if len(self._search_count_label.text()) > 0 else False)

            # First, calculate the width of the count label
            digits = max(1, len(str(self._search_count_label.text())))
            # '10' represents the total left and right padding
            space = 10 + self.fontMetrics().horizontalAdvance("0") * digits
            # Set the size of QLabel to achieve the desired overlap
            self._search_count_label.resize(space, self._search_input.height())

            # Adjust the label's size and position dynamically when the widget is resized
            self._search_count_label.move(self._search_input_label.width() + self._search_input.width()
                                          - self._search_count_label.width(), self._search_input.y())
            self._search_count_label.resize(self._search_count_label.width(), self._search_input.height())

        def resizeEvent(self, event):
            super().resizeEvent(event)
            # Adjust the size of the count label
            self.adjust_size()

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
        central_spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.addWidget(central_spacer)

        self.search_input = self.SearchLineEdit(lexemes=self.lexemes)
        self.addWidget(self.search_input)

        for button in self.search_buttons:
            if button['type'] == 'action':
                # Create and append toolbar button
                self.append_toolbar_button(button)

        search_match_case_label = QLabel(self)
        search_match_case_label.sizeHint()
        search_match_case_label.setText(self.lexemes.get('search_case_sensitive'))
        search_match_case_label.setObjectName("search_case_sensitive")  # To differentiate it at styles file
        self.addWidget(search_match_case_label)

        self.search_match_case = QCheckBox(self)
        self.search_match_case.sizeHint()
        self.search_match_case.setToolTip(self.lexemes.get('search_match_case_tooltip'))
        self.search_match_case.setCheckState(Qt.CheckState.Unchecked)
        self.addWidget(self.search_match_case)

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

    def append_toolbar_button(self, conf):
        """
        Helper to create and return toolbar push button.
        """
        # Theme icon with a fallback to a system one
        system_icon = conf['system_icon'] if 'system_icon' in conf else None
        theme_icon = conf['theme_icon'] if 'theme_icon' in conf else None
        theme_icon_color = QColor(conf['color']) if 'color' in conf \
            else self.theme_helper.get_color('toolbar_icon_color_default')
        # Theme icon with a fallback to a system one
        icon = self.theme_helper.get_icon(theme_icon=theme_icon, system_icon=system_icon, color=theme_icon_color)

        # Toolbar button with an icon
        icon_button = QPushButton(self)
        icon_button.setFont(self.font())
        # Set the size (height) similar to search input field height
        if hasattr(self, 'search_input'):
            # Adjust size to maintain ratio
            size_hint = self.search_input.sizeHint()  # As a real height hint check the line edit height
            icon_button.setFixedSize(QSize(size_hint.height(), size_hint.height()))
            icon_height = int(size_hint.height() * 0.7)
            icon_button.setIconSize(QSize(icon_height, icon_height))
        icon_button.setIcon(icon)

        action = conf['action'] if 'action' in conf else None  # Action when clicked
        if action is not None:
            icon_button.clicked.connect(action)
        if 'accessible_name' in conf:
            icon_button.setAccessibleName(conf['accessible_name'])
        if 'tooltip' in conf:
            icon_button.setToolTip(conf['tooltip'])
        if 'default' in conf:
            icon_button.setDefault(conf['default'])
        if 'enabled' in conf:
            icon_button.setEnabled(conf['enabled'])

        # Add the button to the toolbar
        self.addWidget(icon_button)

        if 'var_name' in conf:
            if self.debug and hasattr(self, conf['var_name']):
                self.logger.debug('Variable "%s" is already set! Re-writing it...' % conf['var_name'])
            setattr(self, conf['var_name'], icon_button)  # type: QPushButton

    def contextMenuEvent(self, event):
        """
        Render context menu event upon the toolbar right mouse click
        """
        current_action = self.actionAt(event.pos())
        if current_action is None:
            return

        if self.actions is None:
            return

        menu = QMenu(self)

        _weights = 0
        for index, label in enumerate(self.actions, 1):
            if 'type' not in label or label['type'] != 'action':
                menu.addSeparator()
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

            menu.addAction(button)

            if index in self.search_buttons:
                self.search_buttons[index] = button

            # Collect items already added to the context menu
            _weights |= settings_weight

        # PoC remove element from the toolbar
        # delete_action  = menu.addAction("Hide")

        menu.exec(event.globalPos())

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
        if index in self.search_buttons:
            self.search_buttons[index].setChecked(checked)
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
