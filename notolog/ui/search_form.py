"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Provides app search UI form.
- Functionality: Displays the app's search form.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2025 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QSizePolicy
from PySide6.QtGui import QColor

from . import Settings
from . import Lexemes
from . import ThemeHelper

from typing import TYPE_CHECKING, Any, List, Dict, Union  # noqa: F401

import logging

if TYPE_CHECKING:
    from ..ui.toolbar import ToolBar  # noqa: F401


class SearchForm(QWidget):
    """
    Custom search form widget that integrates a QLineEdit for input, QLabel for displaying input labels,
    and other elements to show the actual label and count of search results. This widget also exposes signals
    similar to a QLineEdit for external interaction.
    """

    # Signals to mimic QLineEdit's textChanged and returnPressed events.
    textChanged = Signal(str)
    returnPressed = Signal()
    searchButtonClear = Signal()
    searchButtonNext = Signal()
    searchButtonPrev = Signal()
    caseSensitive = Signal(Qt.CheckState)

    def __init__(self, parent):
        super().__init__()

        self.parent = parent  # type: Union[QWidget, ToolBar]

        if self.parent and hasattr(self.parent, 'font'):
            # Apply font from the parent widget to the dialog
            self.setFont(self.parent.font())

        self.logger = logging.getLogger('search_form')

        self.settings = Settings()

        self.theme_helper = ThemeHelper()

        self.lexemes = Lexemes(self.settings.app_language, default_scope='toolbar')

        # Placeholder attributes for component widgets, initialized in init_ui.
        self._search_input = None  # type: Union[QLineEdit, None]
        self._search_pos_label = None  # type: Union[QLabel, None]
        self._search_count_label = None  # type: Union[QLabel, None]

        self.case_sensitive_state = False
        # Search navigation button variables will be set via mapping

        self.init_ui()

    def get_toolbar_search_buttons(self) -> List[Dict[str, Any]]:
        """
        Retrieves the configuration map for search-related toolbar buttons.

        Note: The 'var_name' parameter will be initialized in the final object that utilizes this map.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries detailing the configuration of each toolbar search button.
        """

        return [
            {'type': 'action', 'name': 'search_clear', 'system_icon': 'window-close', 'theme_icon': 'x-circle-fill.svg',
             'action': self.searchButtonClear.emit, 'enabled': False, 'default': False,
             'tooltip': self.lexemes.get('search_buttons_label_clear', scope='toolbar'),
             'accessible_name': self.lexemes.get('search_buttons_accessible_name_clear', scope='toolbar'),
             'var_name': 'btn_search_clear', 'color': self.theme_helper.get_color('toolbar_search_button_clear')},
            {'type': 'action', 'name': 'search_prev', 'system_icon': 'go-up', 'theme_icon': 'caret-up-fill.svg',
             'action': self.searchButtonPrev.emit, 'enabled': False, 'default': False,
             'tooltip': self.lexemes.get('search_buttons_label_prev', scope='toolbar'),
             'accessible_name': self.lexemes.get('search_buttons_accessible_name_prev', scope='toolbar'),
             'var_name': 'btn_search_prev', 'color': self.theme_helper.get_color('toolbar_search_button_prev')},
            {'type': 'action', 'name': 'search_next', 'system_icon': 'go-down', 'theme_icon': 'caret-down-fill.svg',
             'action': self.searchButtonNext.emit, 'enabled': False, 'default': True,
             'tooltip': self.lexemes.get('search_buttons_label_next', scope='toolbar'),
             'accessible_name': self.lexemes.get('search_buttons_accessible_name_next', scope='toolbar'),
             'var_name': 'btn_search_next', 'color': self.theme_helper.get_color('toolbar_search_button_next')},
            {'type': 'action', 'name': 'search_case_sensitive', 'system_icon': '', 'theme_icon': None,
             'var_name': 'btn_search_case_sensitive', 'enabled': True, 'default': False, 'color': None,
             'tooltip': self.lexemes.get('search_case_sensitive_tooltip', scope='toolbar'),
             'accessible_name': self.lexemes.get('search_case_sensitive_accessible_name', scope='toolbar'),
             'text': 'aA',  # the 'aA' notation is commonly used universally to depict case sensitivity
             'action': self.case_sensitive_toggle},
        ]

    def init_ui(self):

        # Create the main vertical layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)  # Equal top and bottom margins
        main_layout.setSpacing(0)

        # Create a container widget to hold the vertically centered search form
        search_container = QWidget()
        main_layout.addWidget(search_container)

        # Set up the horizontal layout
        search_layout = QHBoxLayout(search_container)
        # Adjust layout margins for proper spacing inside the toolbar
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.setSpacing(0)

        # Text search input
        self._search_input = QLineEdit(self)
        self._search_input.setObjectName('search_input')
        self._search_input.setReadOnly(False)
        self._search_input.setMaxLength(512)
        self._search_input.setPlaceholderText(self.lexemes.get('search_input_placeholder_text'))
        self._search_input.setAccessibleDescription(self.lexemes.get('search_input_accessible_description'))

        # Connect the QLineEdit's textChanged signal to the custom widget's textChanged signal
        self._search_input.textChanged.connect(self.emit_text_changed)
        self._search_input.returnPressed.connect(self.returnPressed.emit)

        # Count occurrences of the searched text within the document.
        self._search_count_label = QLabel('', self)
        self._search_count_label.setObjectName('search_count_label')
        self._search_count_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self._search_count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center text in QLabel

        # The position of the current occurrence of the searched text within the document.
        self._search_pos_label = QLabel('', self)
        self._search_pos_label.setObjectName('search_pos_label')
        self._search_pos_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self._search_pos_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center text in QLabel

        # Add UI component to the layout
        search_layout.addWidget(self._search_input)

        # Adjust the display properties of labels showing the number of searched text occurrences.
        self.set_counter_text('')

        # Ensure this QLabel is visually layered above other widgets if overlapping.
        self._search_pos_label.raise_()
        self._search_count_label.raise_()

        for search_button in self.get_toolbar_search_buttons():
            if search_button['type'] == 'action':
                # Create and append toolbar button
                self.append_toolbar_button(button_conf=search_button, layout=search_layout)

        # Connect to the event that clears the search form
        self.searchButtonClear.connect(self.action_search_clear)

    def action_search_clear(self) -> None:
        """
        Clears the search field, resets case sensitivity, and updates the interface
        to reflect the cleared state.
        """

        # Clears the search field by setting the current search text to an empty string.
        self.set_text('')

        # Reset case sensitivity.
        # Unused: This line is commented out to allow independent handling of the button's toggle state.
        # self.set_case_sensitive(False)

        # Refresh the state of search buttons
        self.action_search_buttons_refresh()

        # Hide the occurrences counter
        self.set_counter_text('')

    def action_search_buttons_refresh(self):
        """
        Updates the enable/disable state of the search buttons based on the presence of search text and occurrences.
        """

        try:
            search_occurrences = int(self.counter_text())
        except ValueError:
            search_occurrences = 0

        # Retrieve the current search text.
        text = self.text()
        if hasattr(self, 'btn_search_clear'):
            self.btn_search_clear.setEnabled(True if len(text) > 0 else False)

        # Determine the state for navigation buttons based on occurrences.
        btn_state = bool(search_occurrences)
        if hasattr(self, 'btn_search_next'):
            self.btn_search_next.setEnabled(btn_state)
        if hasattr(self, 'btn_search_prev'):
            self.btn_search_prev.setEnabled(btn_state)

        # Highlight the case-sensitive button if that mode is active.
        if hasattr(self, 'btn_search_case_sensitive'):
            self.search_button_highlight(button=self.btn_search_case_sensitive, state=self.case_sensitive())

    def case_sensitive_toggle(self):
        """
        This method switches the state of case sensitivity and notifies other components
        of this change by emitting a caseSensitive signal with the current state.
        """

        # Toggle the case sensitivity state
        self.case_sensitive_state ^= True

        # Emit the caseSensitive signal with the current state to notify other components
        self.caseSensitive.emit(self.case_sensitive_state)

    def search_button_highlight(self, button: QPushButton, state: bool = False):
        if state:
            button.setStyleSheet("QPushButton { background: %s; }"
                                 % self.theme_helper.get_color('toolbar_search_button_highlight', True))
        else:
            button.setStyleSheet("QPushButton { }")

    def append_toolbar_button(self, button_conf: dict, layout: QHBoxLayout) -> None:
        """
        Appends a search button to the toolbar based on the provided configuration.

        Args:
            button_conf (dict): Configuration dictionary for the button, specifying properties like text, icons, tooltips, etc.
            layout (QHBoxLayout): The layout to which the button will be added.

        This helper function creates and adds a search button to the specified layout of the toolbar.
        """

        system_icon = button_conf['system_icon'] if 'system_icon' in button_conf else None
        theme_icon = button_conf['theme_icon'] if 'theme_icon' in button_conf else None
        theme_icon_color = QColor(button_conf['color']) if 'color' in button_conf \
            else self.theme_helper.get_color('toolbar_icon_color_default')

        icon = None
        if theme_icon:
            # Get the theme icon, using a system default as a fallback.
            icon = self.theme_helper.get_icon(theme_icon=theme_icon, system_icon=system_icon, color=theme_icon_color)

        # Initialize a toolbar button with an icon.
        icon_button = QPushButton(self)
        if 'name' in button_conf:
            icon_button.setObjectName(button_conf['name'])  # Set object name from configuration.
        icon_button.setFont(self.font())

        # Match button size to the search input field's height, maintaining aspect ratio.
        size_hint = self._search_input.sizeHint()
        icon_button.setMinimumSize(QSize(size_hint.height(), size_hint.height()))

        # Configure button to display either an icon or text based on configuration.
        if icon:
            # Calculate and set icon size based on the search input height.
            icon_width = icon_height = int(size_hint.height() * 0.7)
            icon_button.setIconSize(QSize(icon_width, icon_height))
            icon_button.setIcon(icon)  # Set the icon.
        elif 'text' in button_conf and button_conf['text']:
            # Adjust and set the button's font size.
            icon_button_font = icon_button.font()
            icon_button_font.setPointSizeF(icon_button_font.pointSize() * 0.8)
            icon_button.setFont(icon_button_font)
            icon_button.setText(button_conf['text'])  # Set button text.

        action = button_conf['action'] if 'action' in button_conf else None  # Action when clicked
        if action is not None and callable(action):
            icon_button.clicked.connect(action)
        if 'accessible_name' in button_conf:
            icon_button.setAccessibleName(button_conf['accessible_name'])
        if 'tooltip' in button_conf:
            icon_button.setToolTip(button_conf['tooltip'])
        if 'default' in button_conf:
            icon_button.setDefault(button_conf['default'])
        if 'enabled' in button_conf:
            icon_button.setEnabled(button_conf['enabled'])

        # Add the button to the layout
        layout.addWidget(icon_button)

        if 'var_name' in button_conf:
            if hasattr(self, button_conf['var_name']):
                self.logger.debug('Variable "%s" is already set! Re-writing it...' % button_conf['var_name'])
            setattr(self, button_conf['var_name'], icon_button)  # type: QPushButton

    def emit_text_changed(self, text):
        """
        Emit the custom textChanged signal with the current text as the argument to notify of text changes.
        """
        self.textChanged.emit(text)

    def text(self):
        """
        Retrieve the current text from the underlying QLineEdit.

        Returns:
            str: The text currently displayed in the QLineEdit.
        """
        return self._search_input.text()

    def set_text(self, text):
        """
        Proxy method to set the text of the underlying QLineEdit to the specified value.

        Args:
            text (str): The text to display in the QLineEdit.

        Returns:
            None: This method does not return a value.
        """
        return self._search_input.setText(text)

    def case_sensitive(self) -> bool:
        """
        Determine whether the case-sensitive search option is enabled in the search settings.

        Returns:
            bool: True if the case-sensitive search is enabled, False otherwise.
        """

        return self.case_sensitive_state

    def set_case_sensitive(self, checked: bool = False):
        """
        Enable or disable the case-sensitive search option based on the checked parameter.

        Args:
            checked (bool): If True, enables case-sensitive search; if False, disables it.

        Returns:
            None: This method does not return a value.
        """

        self.case_sensitive_state = True if checked else False

    def set_focus(self):
        self._search_input.setFocus()

    def set_maximum_width(self, width):
        self.setMaximumWidth(width)

    def set_placeholder_text(self, text):
        self._search_input.setPlaceholderText(text)

    def counter_text(self):
        """
        Retrieve the text from the label displaying the count of searched text occurrences.

        Returns:
            str: The text indicating the number of occurrences of the searched text.
        """
        return self._search_count_label.text()

    def set_counter_text(self, count: str):
        """
        Sets the text of the embedded QLabel which displays the count of searched text occurrences.

        Args:
            count (str): The text to display in the count label; representing the number of occurrences.
        """

        self._search_count_label.setText(count)
        self.adjust_occurrence_label_size(label=self._search_count_label)
        self.set_position_text('')
        # Refresh the state of search buttons based on current search conditions.
        self.action_search_buttons_refresh()

    def position_text(self):
        """
        Retrieve the text from the label displaying the current position of the searched text occurrence.

        Returns:
            str: The text indicating the current position of occurrences of the searched text.
        """
        return self._search_pos_label.text()

    def set_position_text(self, index: str):
        """
        Sets the text of the embedded QLabel that shows the position of the current search result.

        Args:
            index (str): The position of the current search result to display.
                         If this is '0', the label will be hidden.
        """

        try:
            pos_text = index if len(index) > 0 and int(index) > 0 else ''
        except ValueError:
            pos_text = ''

        self._search_pos_label.setText(pos_text)
        self.adjust_occurrence_label_size(label=self._search_pos_label, shift=self._search_count_label.width())

    def adjust_occurrence_label_size(self, label: QLabel, shift: int = 0):
        """
        Adjusts the visibility and dimensions of a QLabel based on its content and related UI elements.

        The label's visibility is controlled by its content (visible if not empty).
        Its size and position are dynamically adjusted to ensure proper layout within the interface,
        particularly in relation to the search input field.

        Args:
            label (QLabel): The label whose size and visibility are to be adjusted.
            shift (int, optional): The horizontal offset to apply when positioning the label. Defaults to 0.
        """

        # Show occurrence label if not an empty text
        try:
            visible = True if len(label.text()) > 0 and int(label.text()) >= 0 else False
        except ValueError:
            visible = False

        label.setVisible(visible)

        if not visible:
            return

        # First, calculate the width of the count label
        digits = max(1, len(str(label.text())))
        # '10' represents the total left and right padding
        space = 10 + self.fontMetrics().horizontalAdvance("0") * digits
        # Set the size of QLabel to achieve the desired overlap
        label.resize(space, self._search_input.height())

        # Adjust the label's size and position dynamically when the widget is resized
        label.move(self._search_input.width() - label.width() - shift, self._search_input.y())
        self._search_pos_label.resize(label.width(), self._search_input.height())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Adjust the size of the count label
        self.adjust_occurrence_label_size(label=self._search_count_label)
        self.adjust_occurrence_label_size(label=self._search_pos_label, shift=self._search_count_label.width())
