"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Implements the file tree UI for navigation and management.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2025 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget, QListView, QAbstractItemView, QLineEdit

import logging
from typing import TYPE_CHECKING

from . import Settings
from . import Lexemes
from . import ThemeHelper

if TYPE_CHECKING:
    from typing import Union  # noqa


class FileTree(QWidget):

    def __init__(self, parent, proxy_model, minimum_width,
                 clicked_callback, text_changed_callback, context_menu_callback):
        super().__init__(parent)

        # Configuration params
        self.parent = parent
        self.proxy_model = proxy_model
        self.minimum_width = minimum_width
        self.clicked_callback = clicked_callback
        self.text_changed_callback = text_changed_callback
        self.context_menu_callback = context_menu_callback

        if self.parent and hasattr(self.parent, 'font'):
            # Apply font from the dialog instance to the label
            self.setFont(self.parent.font())

        self.logger = logging.getLogger('file_tree')

        self.settings = Settings(parent=self)
        self.settings.value_changed.connect(
            lambda v: self.settings_update_handler(v))

        self.theme_helper = ThemeHelper()

        # Load lexemes for the selected language and scope
        self.lexemes = Lexemes(self.settings.app_language, default_scope='common')

        # File tree related objects
        self.list_view = None  # type: Union[QListView, None]
        self.tree_filter = None  # type: Union[QLineEdit, None]

        self.init_ui()

    def init_ui(self):
        """
        Initialize the UI elements for the file tree view.
        """

        # Either QTreeView(self) or QListView(self) are working fine
        self.list_view = QListView(self)
        self.list_view.setModel(self.proxy_model)
        # Apply font from the main window to the widget
        self.list_view.setFont(self.font())
        """
        Prevent selection upon right-click, selection appears in self.set_current_path()
        More info about the enum: https://doc.qt.io/qt-6/qabstractitemview.html#SelectionMode-enum
        """
        self.list_view.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.list_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        # Connect the clicked event to handle file selection
        if callable(self.clicked_callback):
            self.list_view.clicked.connect(self.clicked_callback)

        # Ensure the context menu callback exists before connecting
        if callable(self.context_menu_callback):
            self.list_view.customContextMenuRequested.connect(self.context_menu_callback)

        # Setup filter input
        self.tree_filter = QLineEdit(self, textChanged=self.text_changed_callback)
        self.tree_filter.setFont(self.font())
        self.tree_filter.setReadOnly(False)
        self.tree_filter.setMaxLength(512)
        self.tree_filter.setMinimumWidth(self.minimum_width)
        self.tree_filter.setPlaceholderText(self.lexemes.get('tree_filter_input_placeholder_text'))
        self.tree_filter.setAccessibleDescription(self.lexemes.get('tree_filter_input_accessible_desc'))

        # Layout configuration
        tree_layout = QVBoxLayout(self)
        tree_layout.setContentsMargins(0, 0, 0, 0)
        tree_layout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetMinimumSize)  # Ensure proper resizing
        tree_layout.addWidget(self.tree_filter)
        tree_layout.addWidget(self.list_view)

        # Apply the stylesheet
        self.setStyleSheet(self.theme_helper.get_css('tree_view'))

    def get_list_view(self) -> QListView:
        # Return the list view component.
        return self.list_view

    def settings_update_handler(self, data: dict) -> None:
        """
        Perform actions upon settings change.

        Data is provided as a dictionary, where the key represents the setting name, and the value is its corresponding value.
        Note: This operation updates UI elements and internal properties, which may be resource-intensive.

        Args:
            data (dict): Dictionary of settings updates, e.g., {"show_deleted_files": True}
        """

        self.logger.debug(f'Settings update handler is processing: {data}')

        try:
            if 'app_theme' in data:
                # Re-apply styles to the elements
                self.setStyleSheet(self.theme_helper.get_css('tree_view'))

            if 'app_font_size' in data:
                # Apply the main window's font to all relevant widgets
                self.setFont(self.parent.font())
                self.list_view.setFont(self.font())
                self.tree_filter.setFont(self.font())

            if 'app_language' in data:
                # Reload lexemes for the selected language and scope
                self.lexemes = Lexemes(self.settings.app_language, default_scope='common')
                # Update dependent object lexemes
                self.tree_filter.setPlaceholderText(self.lexemes.get('tree_filter_input_placeholder_text'))
                self.tree_filter.setAccessibleDescription(self.lexemes.get('tree_filter_input_accessible_desc'))

        except RuntimeError as e:
            self.logger.warning(f"Error occurred while updating settings: {e}")
