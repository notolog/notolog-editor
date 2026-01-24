"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Implements the file tree UI for navigation and management.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QVBoxLayout, QWidget, QListView, QAbstractItemView, QLineEdit, QLabel, QHBoxLayout
from PySide6.QtGui import QCursor

import logging
from typing import TYPE_CHECKING, Optional, Callable, Any

from . import Settings
from . import Lexemes
from . import ThemeHelper

if TYPE_CHECKING:
    from PySide6.QtCore import QAbstractItemModel


class FileTree(QWidget):
    """
    File tree widget with integrated search/filter functionality.

    Provides a list view of files with a search filter input and clear button.
    Supports theme and font size changes, accessibility features, and customizable callbacks.

    Attributes:
        FILTER_MAX_LENGTH: Maximum characters allowed in filter input
        CLEAR_BUTTON_TEXT: Text displayed on the clear filter button
        CLEAR_BUTTON_SIZE_RATIO: Button size ratio relative to filter input height
    """

    # Constants for configuration
    FILTER_MAX_LENGTH: int = 512
    CLEAR_BUTTON_TEXT: str = '×'
    CLEAR_BUTTON_SIZE_RATIO: float = 1.0  # Button is same size as filter height

    def __init__(
        self,
        parent: QWidget,
        proxy_model: 'QAbstractItemModel',
        minimum_width: int,
        clicked_callback: Optional[Callable] = None,
        text_changed_callback: Optional[Callable] = None,
        context_menu_callback: Optional[Callable] = None
    ) -> None:
        """
        Initialize the file tree widget.

        Args:
            parent: Parent widget
            proxy_model: Qt model for the list view (typically a proxy filter model)
            minimum_width: Minimum width for the filter input
            clicked_callback: Called when an item is clicked (receives QModelIndex)
            text_changed_callback: Called when filter text changes (receives str)
            context_menu_callback: Called on right-click (receives QPoint)
        """
        super().__init__(parent)

        # Store configuration parameters
        self.parent = parent
        self.proxy_model: 'QAbstractItemModel' = proxy_model
        self.minimum_width: int = minimum_width
        self.clicked_callback: Optional[Callable] = clicked_callback
        self.text_changed_callback: Optional[Callable] = text_changed_callback
        self.context_menu_callback: Optional[Callable] = context_menu_callback

        # Apply parent font if available
        if self.parent and hasattr(self.parent, 'font'):
            self.setFont(self.parent.font())

        # Initialize logger
        self.logger: logging.Logger = logging.getLogger('file_tree')

        # Initialize settings and connect to change handler
        self.settings: Settings = Settings(parent=self)
        self.settings.value_changed.connect(self.settings_update_handler)

        # Initialize theme helper
        self.theme_helper: ThemeHelper = ThemeHelper()

        # Load localization for current language
        self.lexemes: Lexemes = Lexemes(self.settings.app_language, default_scope='common')

        # UI components (initialized in init_ui)
        self.list_view: Optional[QListView] = None
        self.tree_filter: Optional[QLineEdit] = None
        self.tree_filter_clear_btn: Optional[QLabel] = None

        # Initialize UI
        self.init_ui()

    def init_ui(self) -> None:
        """
        Initialize and configure all UI elements.

        Creates the file list view, filter input, and clear button with proper
        layout, styling, and event connections.
        """
        # Initialize list view
        self._init_list_view()

        # Initialize filter container with input and clear button
        filter_container = self._init_filter_container()

        # Setup main layout
        tree_layout = QVBoxLayout(self)
        tree_layout.setContentsMargins(0, 0, 0, 0)
        tree_layout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetMinimumSize)
        tree_layout.addWidget(filter_container)
        tree_layout.addWidget(self.list_view)

        # Apply theme stylesheet
        self.setStyleSheet(self.theme_helper.get_css('tree_view'))

    def _init_list_view(self) -> None:
        """Initialize the file list view with proper configuration."""
        self.list_view = QListView(self)
        self.list_view.setModel(self.proxy_model)
        self.list_view.setFont(self.font())

        # Prevent selection on right-click (selection happens in set_current_path)
        # See: https://doc.qt.io/qt-6/qabstractitemview.html#SelectionMode-enum
        self.list_view.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.list_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        # Connect callbacks if provided
        if callable(self.clicked_callback):
            self.list_view.clicked.connect(self.clicked_callback)
        if callable(self.context_menu_callback):
            self.list_view.customContextMenuRequested.connect(self.context_menu_callback)

    def _init_filter_container(self) -> QWidget:
        """
        Initialize the filter input container with clear button.

        Returns:
            QWidget containing the filter input and clear button
        """
        container = QWidget(self)
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Initialize filter input
        self._init_filter_input(container)
        layout.addWidget(self.tree_filter)

        # Initialize clear button
        self._init_clear_button(container)

        return container

    def _init_filter_input(self, parent: QWidget) -> None:
        """Initialize the filter input field."""
        self.tree_filter = QLineEdit(parent)
        self.tree_filter.setFont(self.font())
        self.tree_filter.setReadOnly(False)
        self.tree_filter.setMaxLength(self.FILTER_MAX_LENGTH)
        self.tree_filter.setMinimumWidth(self.minimum_width)
        self.tree_filter.setPlaceholderText(self.lexemes.get('tree_filter_input_placeholder_text'))
        self.tree_filter.setAccessibleDescription(self.lexemes.get('tree_filter_input_accessible_desc'))

        # Install event filter to intercept key events
        self.tree_filter.installEventFilter(self)

        # Connect text change handler
        self.tree_filter.textChanged.connect(self.on_filter_text_changed)

    def _init_clear_button(self, parent: QWidget) -> None:
        """Initialize the clear button (QLabel acting as clickable icon)."""
        self.tree_filter_clear_btn = QLabel(parent)
        self.tree_filter_clear_btn.setObjectName('tree_filter_clear_btn')
        self.tree_filter_clear_btn.setFont(self.font())

        # Make clickable with pointer cursor
        self.tree_filter_clear_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.tree_filter_clear_btn.setMouseTracking(True)

        # Set accessibility properties
        self.tree_filter_clear_btn.setToolTip(
            self.lexemes.get('tree_filter_clear_button_tooltip', scope='common')
        )
        self.tree_filter_clear_btn.setAccessibleName(
            self.lexemes.get('tree_filter_clear_button_accessible_name', scope='common')
        )

        # Initially hidden (shown when text is entered)
        self.tree_filter_clear_btn.setVisible(False)

        # Configure button appearance
        self.update_clear_button()

        # Position button on top of input field
        self.tree_filter_clear_btn.raise_()

    def get_list_view(self) -> QListView:
        """
        Get the underlying list view widget.

        Returns:
            QListView instance used for file display
        """
        return self.list_view

    def on_filter_text_changed(self, text: str) -> None:
        """
        Handle text changes in the filter input.

        Shows/hides the clear button based on text presence and triggers
        the configured callback.

        Args:
            text: Current filter text
        """
        # Toggle clear button visibility based on text presence
        if self.tree_filter_clear_btn:
            has_text = len(text) > 0
            self.tree_filter_clear_btn.setVisible(has_text)

            # Update button layout when shown
            if has_text:
                self.update_clear_button()

        # Notify callback of filter change
        if callable(self.text_changed_callback):
            self.text_changed_callback(text)

    def clear_filter(self) -> None:
        """Clear the filter input field and hide the clear button."""
        if self.tree_filter:
            self.tree_filter.clear()

    def update_clear_button(self) -> None:
        """
        Update clear button appearance, size, and position.

        Recalculates button size based on filter input dimensions,
        applies theme colors, and updates layout.
        """
        if not self.tree_filter_clear_btn or not self.tree_filter:
            return

        # Size button to match filter input height
        filter_height = self.tree_filter.sizeHint().height()
        button_size = int(filter_height * self.CLEAR_BUTTON_SIZE_RATIO)
        self.tree_filter_clear_btn.setFixedSize(QSize(button_size, button_size))

        # Apply theme color
        theme_icon_color = self._get_theme_color()

        # Configure button text and styling
        self.tree_filter_clear_btn.setText(self.CLEAR_BUTTON_TEXT)
        self.tree_filter_clear_btn.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tree_filter_clear_btn.setStyleSheet(f"color: {theme_icon_color};")

        # Update input padding and button position
        self._update_filter_padding()
        self._adjust_clear_button_position()

    def _get_theme_color(self) -> str:
        """
        Get the appropriate theme color for the clear button.

        Returns:
            Hex color string
        """
        color = self.theme_helper.get_color('main_menu_icon_color')
        if not color:
            color = self.theme_helper.get_color('color_default')
        return color or '#888888'  # Fallback to gray

    def _update_filter_padding(self) -> None:
        """
        Update filter input padding to prevent text overlap with clear button.

        Adds right padding equal to button width so user text doesn't hide
        behind the button.
        """
        if not self.tree_filter_clear_btn or not self.tree_filter:
            return

        button_width = self.tree_filter_clear_btn.width()
        self.tree_filter.setStyleSheet(f"QLineEdit {{ padding-right: {button_width}px; }}")

    def _adjust_clear_button_position(self) -> None:
        """
        Position clear button to overlay on the right side of the filter input.

        Calculates position to right-align the button within the input field
        bounds, maintaining proper visual alignment.
        """
        if not self.tree_filter_clear_btn or self.tree_filter_clear_btn.isHidden():
            return

        button_width = self.tree_filter_clear_btn.width()
        input_width = self.tree_filter.width()
        input_y = self.tree_filter.y()

        # Right-align button within input field
        x_pos = input_width - button_width
        self.tree_filter_clear_btn.move(x_pos, input_y)

    def resizeEvent(self, event: Any) -> None:
        """
        Handle widget resize events.

        Ensures clear button maintains proper position when widget is resized.

        Args:
            event: Qt resize event
        """
        super().resizeEvent(event)
        self._adjust_clear_button_position()

    def mousePressEvent(self, event: Any) -> None:
        """
        Handle mouse press events.

        Detects clicks on the clear button and triggers filter clearing.
        Passes other clicks to parent handler.

        Args:
            event: Qt mouse event
        """
        if self.tree_filter_clear_btn and not self.tree_filter_clear_btn.isHidden():
            # Use position().toPoint() instead of deprecated pos()
            click_pos = event.position().toPoint()
            if self.tree_filter_clear_btn.geometry().contains(click_pos):
                self.clear_filter()
                event.accept()
                return
        super().mousePressEvent(event)

    def eventFilter(self, obj: Any, event: Any) -> bool:
        """
        Event filter to intercept key events from nested widgets.

        Specifically handles Esc key press on the filter input to clear the filter
        when it has content (i.e., when the clear button would be visible).

        Args:
            obj: The object that received the event
            event: The event to filter

        Returns:
            True if event was handled and should be filtered out, False otherwise
        """
        # Check if this is a key press event on the filter input
        if obj == self.tree_filter and event.type() == event.Type.KeyPress:
            # Check if Esc key was pressed
            if event.key() == Qt.Key.Key_Escape:
                # Check if filter has content (clear button visible)
                if (self.tree_filter_clear_btn and
                        not self.tree_filter_clear_btn.isHidden()):
                    # Clear the filter (same action as clicking clear button)
                    self.clear_filter()
                    return True  # Event handled, don't propagate

        # Pass event to parent event filter
        return super().eventFilter(obj, event)

    def settings_update_handler(self, data: dict) -> None:
        """
        Handle application settings changes.

        Responds to theme, font size, and language changes by updating
        relevant UI elements. This operation may be resource-intensive.

        Args:
            data: Dictionary of setting changes, e.g., {"app_theme": "dark"}
                 Supported keys: app_theme, app_font_size, app_language

        Raises:
            RuntimeError: If Qt widget operations fail during update
        """
        self.logger.debug(f'Settings update handler processing: {data}')

        try:
            if 'app_theme' in data:
                self._handle_theme_change()

            if 'app_font_size' in data:
                self._handle_font_size_change()

            if 'app_language' in data:
                self._handle_language_change()

        except RuntimeError as e:
            self.logger.warning(f"Error updating settings: {e}")

    def _handle_theme_change(self) -> None:
        """Apply theme changes to the widget and its components."""
        self.setStyleSheet(self.theme_helper.get_css('tree_view'))
        self.update_clear_button()

    def _handle_font_size_change(self) -> None:
        """Apply font size changes to all text-based components."""
        # Apply new font to all widgets
        self.setFont(self.parent.font())
        self.list_view.setFont(self.font())
        self.tree_filter.setFont(self.font())
        self.tree_filter_clear_btn.setFont(self.font())

        # Update clear button to scale with new font size
        self.update_clear_button()

    def _handle_language_change(self) -> None:
        """Update UI text strings for the new language."""
        # Reload lexemes for new language
        self.lexemes = Lexemes(self.settings.app_language, default_scope='common')

        # Update filter input text
        self.tree_filter.setPlaceholderText(
            self.lexemes.get('tree_filter_input_placeholder_text')
        )
        self.tree_filter.setAccessibleDescription(
            self.lexemes.get('tree_filter_input_accessible_desc')
        )

        # Update clear button text
        if self.tree_filter_clear_btn:
            self.tree_filter_clear_btn.setToolTip(
                self.lexemes.get('tree_filter_clear_button_tooltip', scope='common')
            )
            self.tree_filter_clear_btn.setAccessibleName(
                self.lexemes.get('tree_filter_clear_button_accessible_name', scope='common')
            )
