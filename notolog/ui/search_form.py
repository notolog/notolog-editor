"""
Notolog Editor
Open-source markdown editor developed in Python.

File Details:
- Purpose: Provides app search UI form.
- Functionality: Displays the app's search form.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QCheckBox, QHBoxLayout, QSizePolicy
from PySide6.QtGui import QColor

from . import Settings
from . import AppConfig
from . import Lexemes
from . import ThemeHelper

from typing import TYPE_CHECKING, Union  # noqa: F401

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
    caseSensitive = Signal(Qt.CheckState)

    def __init__(self, parent, search_buttons: list):
        super().__init__()

        self.parent = parent  # type: Union[QWidget, ToolBar]

        if self.parent and hasattr(self.parent, 'font'):
            # Apply font from the parent widget to the dialog
            self.setFont(self.parent.font())

        self.logger = logging.getLogger('search_form')

        self.logging = AppConfig().get_logging()
        self.debug = AppConfig().get_debug()

        self.search_buttons = search_buttons

        self.settings = Settings()

        self.theme_helper = ThemeHelper()

        self.lexemes = Lexemes(self.settings.app_language, default_scope='toolbar')

        # Placeholder attributes for component widgets, initialized in init_ui.
        self._search_input = None  # type: Union[QLineEdit, None]
        self._search_input_label = None  # type: Union[QLabel, None]
        self._search_pos_label = None  # type: Union[QLabel, None]
        self._search_count_label = None  # type: Union[QLabel, None]

        # Search navigation button variables will be set via mapping
        self.search_case_sensitive = None  # type: Union[QCheckBox, None]

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

        for search_button in self.search_buttons:
            if search_button['type'] == 'action':
                # Create and append toolbar button
                self.append_toolbar_button(button_conf=search_button, layout=search_layout)

        search_case_sensitive_label = QLabel(self)
        search_case_sensitive_label.setObjectName("search_case_sensitive_label")  # To differentiate it at styles file
        search_case_sensitive_label.sizeHint()
        search_case_sensitive_label.setText(self.lexemes.get('search_case_sensitive_label'))
        search_layout.addWidget(search_case_sensitive_label)

        self.search_case_sensitive = QCheckBox(self)
        self.search_case_sensitive.setObjectName("search_case_sensitive")  # To differentiate it at styles file
        self.search_case_sensitive.sizeHint()
        self.search_case_sensitive.setToolTip(self.lexemes.get('search_case_sensitive_tooltip'))
        self.search_case_sensitive.setCheckState(Qt.CheckState.Unchecked)
        self.search_case_sensitive.stateChanged.connect(self.emit_case_sensitive_changed)

        search_layout.addWidget(self.search_case_sensitive)

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
        # Theme icon with a fallback to a system one
        icon = self.theme_helper.get_icon(theme_icon=theme_icon, system_icon=system_icon, color=theme_icon_color)

        # Toolbar button with an icon
        icon_button = QPushButton(self)
        icon_button.setFont(self.font())
        # Set the size (height) similar to search input field height maintaining the ratio
        size_hint = self._search_input.sizeHint()  # As a real height hint check the line edit height
        icon_button.setFixedSize(QSize(size_hint.height(), size_hint.height()))
        icon_height = int(size_hint.height() * 0.7)
        icon_button.setIconSize(QSize(icon_height, icon_height))
        icon_button.setIcon(icon)

        action = button_conf['action'] if 'action' in button_conf else None  # Action when clicked
        if action is not None:
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
            if self.debug and hasattr(self, button_conf['var_name']):
                self.logger.debug('Variable "%s" is already set! Re-writing it...' % button_conf['var_name'])
            setattr(self, button_conf['var_name'], icon_button)  # type: QPushButton

    def emit_text_changed(self, text):
        """
        Emit the custom textChanged signal with the current text as the argument to notify of text changes.
        """
        self.textChanged.emit(text)

    def emit_case_sensitive_changed(self, state):
        """
        Emit the custom textChanged signal with the current text as the argument to notify of text changes.
        """
        self.caseSensitive.emit(state)

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
        return self.search_case_sensitive.isChecked()

    def set_case_sensitive(self, checked: bool = False):
        """
        Enable or disable the case-sensitive search option based on the checked parameter.

        Args:
            checked (bool): If True, enables case-sensitive search; if False, disables it.

        Returns:
            None: This method does not return a value.
        """
        if checked:
            self.search_case_sensitive.setCheckState(Qt.CheckState.Checked)
        else:
            self.search_case_sensitive.setCheckState(Qt.CheckState.Unchecked)

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

        self._search_pos_label.setText(index if len(index) > 0 and int(index) > 0 else '')
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

        # Show position label if not an empty text
        visible = True if len(label.text()) > 0 and int(label.text()) > 0 else False
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
        label.move(self._search_input_label.width() + self._search_input.width() - label.width() - shift,
                   self._search_input.y())
        self._search_pos_label.resize(label.width(), self._search_input.height())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Adjust the size of the count label
        self.adjust_occurrence_label_size(label=self._search_count_label)
        self.adjust_occurrence_label_size(label=self._search_pos_label, shift=self._search_count_label.width())
