"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Provides app status bar UI.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import Qt, QDir, QSize, QTimer
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QStatusBar, QWidget, QHBoxLayout, QLabel, QPushButton, QSizePolicy

from collections import deque
import logging
import os
import psutil
from typing import TYPE_CHECKING, Any, Dict, List

from . import AppConfig
from . import Settings
from . import Lexemes
from . import ThemeHelper
from . import TooltipHelper
from . import ClipboardHelper

from .sort_filter_proxy_model import SortFilterProxyModel
from .file_system_model import get_file_type_icon
from .vertical_line_spacer import VerticalLineSpacer

from ..file_history_manager import FileHistoryManager

if TYPE_CHECKING:
    from typing import Union  # noqa


class SystemLoadGraph(QWidget):
    """Compact rolling utilization graph for the status bar."""

    HISTORY_SIZE = 30
    COLUMN_WIDTH = 1
    COLUMN_GAP = 0
    INNER_PADDING = 1
    BORDER_WIDTH = 1

    def __init__(self, metric_key: str, parent=None):
        super().__init__(parent)
        self.metric_key = metric_key
        self.current_value = None  # type: Union[int, None]
        self.values = deque([0.0] * self.HISTORY_SIZE, maxlen=self.HISTORY_SIZE)
        self.border_color = QColor()
        self.column_color = QColor()
        self.setObjectName(f'statusbar_{metric_key}_load_graph')
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setAttribute(Qt.WidgetAttribute.WA_AlwaysShowToolTips, True)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setMouseTracking(True)
        self.set_unavailable()

    def set_graph_size(self, font_height: int) -> None:
        width = (self.BORDER_WIDTH + self.INNER_PADDING) * 2
        width += self.HISTORY_SIZE * self.COLUMN_WIDTH
        width += (self.HISTORY_SIZE - 1) * self.COLUMN_GAP
        self.setFixedSize(width, max(12, font_height))

    def set_colors(self, border_color: QColor, column_color: QColor) -> None:
        self.border_color = QColor(border_color)
        self.column_color = QColor(column_color)
        self.update()

    def set_value(self, value: float) -> None:
        value = max(0.0, min(100.0, float(value)))
        self.values.append(value)
        self.current_value = round(value)
        self.update()

    def set_unavailable(self) -> None:
        self.current_value = None

    def set_status_text(self, text: str) -> None:
        self.setToolTip(text)
        self.setAccessibleName(text)

    def paintEvent(self, event) -> None:  # noqa: ARG002
        painter = QPainter(self)
        width = self.width()
        height = self.height()
        painter.fillRect(0, 0, width, self.BORDER_WIDTH, self.border_color)
        painter.fillRect(0, height - self.BORDER_WIDTH,
                         width, self.BORDER_WIDTH, self.border_color)
        painter.fillRect(0, self.BORDER_WIDTH, self.BORDER_WIDTH,
                         height - 2 * self.BORDER_WIDTH, self.border_color)
        painter.fillRect(width - self.BORDER_WIDTH, self.BORDER_WIDTH,
                         self.BORDER_WIDTH, height - 2 * self.BORDER_WIDTH,
                         self.border_color)

        # Border and padding each occupy one logical unit around the data.
        inset = self.BORDER_WIDTH + self.INNER_PADDING
        graph_height = height - 2 * inset
        for index, value in enumerate(self.values):
            bar_height = round(graph_height * value / 100)
            if bar_height <= 0:
                continue
            x_pos = inset + index * (self.COLUMN_WIDTH + self.COLUMN_GAP)
            y_pos = height - inset - bar_height
            painter.fillRect(x_pos, y_pos, self.COLUMN_WIDTH, bar_height, self.column_color)


class StatusBar(QStatusBar):

    BASE_ICON_SIZE = 64  # type: int
    MAX_FILE_NAME_WIDTH = 180  # pixels
    DEFAULT_SYSTEM_LOAD_INTERVAL_MS = 1000
    MIN_SYSTEM_LOAD_INTERVAL_MS = 250
    MAX_SYSTEM_LOAD_INTERVAL_MS = 60000

    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent = parent

        if self.parent and hasattr(self.parent, 'font'):
            # Apply font from the dialog instance to the label
            self.setFont(self.parent.font())

        self.logger = logging.getLogger('statusbar')

        self.settings = Settings(parent=self)
        self.settings.value_changed.connect(self.settings_update_handler)

        self.theme_helper = ThemeHelper()

        # Load lexemes for the selected language and scope
        self.lexemes = Lexemes(self.settings.app_language, default_scope='statusbar')

        # File navigation history manager instance
        self.history_manager = FileHistoryManager()
        self.history_manager.history_updated.connect(self.update_history_buttons)

        self._elements = {}  # Label storage

        self.labels_layout = None  # type: Union[QHBoxLayout, None]
        self.file_icon_label = None  # type: Union[QPushButton, None]
        self.file_label = None  # type: Union[QLabel, None]
        self.data_size_label = None  # type: Union[QLabel, None]
        self.mode_label = None  # type: Union[QLabel, None]
        self.save_progress_label = None  # type: Union[QLabel, None]
        self.encryption_icon_label = None  # type: Union[QLabel, None]
        self.encryption_label = None  # type: Union[QLabel, None]
        self.source_label = None  # type: Union[QLabel, None]
        self.cursor_label = None  # type: Union[QLabel, None]
        self.cpu_load_graph = None  # type: Union[SystemLoadGraph, None]
        self.memory_load_graph = None  # type: Union[SystemLoadGraph, None]
        self.system_load_separator = None  # type: Union[VerticalLineSpacer, None]

        self.warning_label = None  # type: Union[QPushButton, None]
        self._encryption_encrypted = False
        self._system_load_error_logged = False
        self.system_load_timer = None  # type: Union[QTimer, None]

        self.init()

    def init(self):
        # Apply styles to the QStatusBar
        self.setStyleSheet(self.theme_helper.get_css('statusbar'))

        # Adjust margins for better alignment
        self.setContentsMargins(5, 0, 0, 0)

        # Create a container widget to hold the labels
        labels_container = QWidget(self)

        # Set up the horizontal layout
        self.labels_layout = QHBoxLayout(labels_container)
        # Adjust layout margins for proper spacing inside the toolbar
        self.labels_layout.setContentsMargins(0, 0, 0, 0)

        # Add text labels to the status bar
        self.add_labels()

        # Render status bar icons
        self.draw_icons()

        self.system_load_timer = QTimer(self)
        self.system_load_timer.timeout.connect(self.update_system_load)
        self.update_system_load_visibility(prime=True)

        central_spacer = QWidget(self)
        central_spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        # Add a central spacer to balance layout spacing
        self.addPermanentWidget(central_spacer)

        # Add the labels container widget to the status bar
        self.addPermanentWidget(labels_container)

    def add_labels(self):
        # Current file name remains ordinary status text.
        self.file_label = QLabel(self)
        self.file_label.setFont(self.font())
        self.file_label.setObjectName('statusbar_file_label')
        self.file_label.setMaximumWidth(self.MAX_FILE_NAME_WIDTH)
        self.labels_layout.addWidget(self.file_label)

        # The adjacent file-type icon copies the full path.
        self.file_icon_label = QPushButton(self)
        self.file_icon_label.setFlat(True)
        self.file_icon_label.setFocusPolicy(Qt.FocusPolicy.TabFocus)
        self.file_icon_label.setAttribute(
            Qt.WidgetAttribute.WA_AlwaysShowToolTips, True)
        self.file_icon_label.setMouseTracking(True)
        self.file_icon_label.setCursor(Qt.CursorShape.PointingHandCursor)
        self.file_icon_label.setObjectName('statusbar_file_icon_label')
        self.file_icon_label.clicked.connect(self.copy_file_path)
        self.file_icon_container = self._add_compact_icon(self.file_icon_label)

        self.labels_layout.addWidget(VerticalLineSpacer())

        # File size label
        self.data_size_label = QLabel(self)
        self.data_size_label.setFont(self.font())
        self.labels_layout.addWidget(self.data_size_label)

        # Save in progress label
        self.save_progress_label = QLabel(self)
        self.save_progress_label.setFont(self.font())
        self.save_progress_label.setVisible(False)
        self._set_compact_label_icon(self.save_progress_label, 'floppy2.svg')
        self.save_progress_container = self._add_compact_icon(self.save_progress_label)
        self.save_progress_container.setVisible(False)

        self.labels_layout.addWidget(VerticalLineSpacer())

        # Main editor area mode label
        self.mode_label = QLabel(self)
        self.mode_label.setFont(self.font())
        """
        Do not set object name similar to the lexeme to avoid double update with the unprocessed lexeme's placeholders.
        E.g.: self.mode_label.setObjectName('statusbar_mode_label')
        """
        self.labels_layout.addWidget(self.mode_label)

        self.labels_layout.addWidget(VerticalLineSpacer())

        # File encryption label and icon
        self.encryption_label = QLabel(self)
        self.encryption_label.setFont(self.font())
        self.labels_layout.addWidget(self.encryption_label)

        self.encryption_icon_label = QLabel(self)
        self.encryption_icon_label.setFont(self.font())
        self.encryption_icon_container = self._add_compact_icon(self.encryption_icon_label)

        self.labels_layout.addWidget(VerticalLineSpacer())

        # Document source label
        self.source_label = QLabel(self)
        self.source_label.setFont(self.font())
        self.labels_layout.addWidget(self.source_label)

        self.labels_layout.addWidget(VerticalLineSpacer())

        # Cursor position label
        self.cursor_label = QLabel(self)
        self.cursor_label.setFont(self.font())
        self.labels_layout.addWidget(self.cursor_label)

        # Compact rolling system utilization graphs.
        self.system_load_separator = VerticalLineSpacer()
        self.labels_layout.addWidget(self.system_load_separator)
        self.cpu_load_graph = SystemLoadGraph('cpu', self)
        self.labels_layout.addWidget(self.cpu_load_graph)
        self.memory_load_graph = SystemLoadGraph('memory', self)
        self.labels_layout.addWidget(self.memory_load_graph)
        self.refresh_system_load_graphs()
        self.refresh_system_load_tooltips()

        # Warning label (initially hidden)
        self.warning_label = QPushButton(self)
        self.warning_label.setVisible(False)
        self.warning_label.setFlat(True)
        self.warning_label.setFont(self.font())
        self.warning_label.setObjectName('statusbar_warning_label')
        icon = self.theme_helper.get_icon(theme_icon='exclamation-triangle-fill.svg',
                                          color=QColor(self.theme_helper.get_color('statusbar_warning_icon_color')))
        self.warning_label.setIcon(icon)
        self._size_compact_button(self.warning_label)
        self.warning_container = self._add_compact_icon(self.warning_label)
        self.warning_container.setVisible(False)
        self.warning_label.clicked.connect(
            lambda: TooltipHelper.show_tooltip(widget=self.warning_label, text=self.warning_label.toolTip()))

        self.set_file_path(self.settings.file_path)

    def get_statusbar_icons(self) -> List[Dict[str, Any]]:
        """
        Main statusbar items map for convenience.
        """

        icons = [
            # Home button (static position; other buttons may replace one another)
            {'type': 'action', 'weight': 1, 'name': 'statusbar_path_home_label', 'system_icon': 'go-home',
             'theme_icon': 'house-door.svg', 'color': self.theme_helper.get_color('statusbar_path_home_icon_color'),
             'label': self.lexemes.get('statusbar_path_home_label'),
             'accessible_name': self.lexemes.get('statusbar_path_home_accessible_name'),
             'action': self.action_path_home, 'var_name': 'path_home_label'},
            # Litter bin (inactive)
            {'type': 'action', 'weight': 2, 'name': 'statusbar_litter_bin_label', 'system_icon': 'user-trash',
             'theme_icon': 'trash3.svg', 'color': self.theme_helper.get_color('statusbar_litter_bin_icon_color'),
             'label': self.lexemes.get('statusbar_litter_bin_label'),
             'accessible_name': self.lexemes.get('statusbar_litter_bin_accessible_name'),
             'action': lambda: self.toggle_litter_bin_button(), 'var_name': 'litter_bin_label',
             'active_state_check': lambda: not self.settings.show_deleted_files},
            # Litter bin (active)
            {'type': 'action', 'weight': 3, 'name': 'statusbar_litter_bin_label_active', 'system_icon': 'user-trash-full',
             'theme_icon': 'trash3-fill.svg', 'color': self.theme_helper.get_color('statusbar_litter_bin_icon_color_active'),
             'label': self.lexemes.get('statusbar_litter_bin_label'),
             'accessible_name': self.lexemes.get('statusbar_litter_bin_accessible_name'),
             'action': lambda: self.toggle_litter_bin_button(), 'var_name': 'litter_bin_label',
             'active_state_check': lambda: self.settings.show_deleted_files},
        ]

        # Add navigation arrows at the end if enabled in the settings
        if hasattr(self.settings, 'show_navigation_arrows') and self.settings.show_navigation_arrows:
            ic_idx = len(icons)  # Icon index
            icons += [
                # Backward navigation button for file history (static position; other buttons may replace one another)
                {'type': 'action', 'weight': ic_idx+1, 'name': 'statusbar_previous_path_label',
                 'system_icon': 'go-previous',
                 'theme_icon': 'arrow-left.svg',
                 'color': self.theme_helper.get_color('statusbar_previous_path_icon_color'),
                 'label': self.lexemes.get('statusbar_previous_path_label'),
                 'accessible_name': self.lexemes.get('statusbar_previous_path_accessible_name'),
                 'action': self.action_previous_path, 'var_name': 'previous_path_label'},
                # Forward navigation button for file history (static position; other buttons may replace one another)
                {'type': 'action', 'weight': ic_idx+2, 'name': 'statusbar_next_path_label', 'system_icon': 'go-next',
                 'theme_icon': 'arrow-right.svg',
                 'color': self.theme_helper.get_color('statusbar_next_path_icon_color'),
                 'label': self.lexemes.get('statusbar_next_path_label'),
                 'accessible_name': self.lexemes.get('statusbar_next_path_accessible_name'),
                 'action': self.action_next_path, 'var_name': 'next_path_label'},
            ]

        return icons

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
                existing_icon = getattr(self, conf['var_name']) if hasattr(self, conf['var_name']) else None
                self.append_statusbar_icon(conf, icon_button=existing_icon)

    def append_statusbar_icon(self, conf, icon_button=None):
        """
        Helper to create, add to the statusbar and return button with an icon.
        """

        # Validate that the passed icon button exists and hasn't been deleted already
        try:
            icon_button.objectName()
        except (AttributeError, RuntimeError):
            icon_button = QPushButton(self)
            # Ensure action is only set once to avoid multiple assignments
            action = conf['action'] if 'action' in conf else None
            if action is not None:
                icon_button.clicked.connect(action)

        # Dynamically set the button height based on the labels size
        button_width = button_height = self.labels_layout.sizeHint().height()
        icon_button.setMinimumWidth(button_width)
        icon_button.setMinimumHeight(button_height)
        icon_width = icon_height = int(button_height * 0.7)
        icon_button.setIconSize(QSize(icon_width, icon_height))

        # Use a themed icon with a fallback to a system icon
        system_icon = conf['system_icon'] if 'system_icon' in conf else None
        theme_icon = conf['theme_icon'] if 'theme_icon' in conf else None
        theme_icon_color = QColor(conf['color']) if 'color' in conf \
            else self.theme_helper.get_color('statusbar_icon_color_default')
        # Increase the icon size based on the ratio between the actual and base font sizes
        width = height = max(self.BASE_ICON_SIZE,
                             int(self.settings.app_font_size / AppConfig().get_font_base_size()) * self.BASE_ICON_SIZE)
        # Retrieve a new icon with the specified parameters
        icon = self.theme_helper.get_icon(theme_icon=theme_icon, system_icon=system_icon, color=theme_icon_color,
                                          width=width, height=height)

        # Button with an icon
        label = conf['label'] if 'label' in conf else ''
        icon_button.setFlat(True)
        icon_button.setIcon(icon)
        icon_button.setCursor(Qt.CursorShape.PointingHandCursor)
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

    def action_previous_path(self):
        """
        Navigate to the previous file in history.
        """
        file_path = self.history_manager.prev_file()
        if file_path and self.parent and hasattr(self.parent, 'safely_open_file'):
            self.parent.safely_open_file(file_path)

    def action_next_path(self):
        """
        Navigate to the next file in history.
        """
        file_path = self.history_manager.next_file()
        if file_path and self.parent and hasattr(self.parent, 'safely_open_file'):
            self.parent.safely_open_file(file_path)

    def update_history_buttons(self):
        """
        Enable or disable navigation buttons based on history state.
        """
        try:
            if hasattr(self, 'previous_path_label') and isinstance(self.previous_path_label, QPushButton):
                self.previous_path_label.setEnabled(self.history_manager.has_prev())
                if hasattr(self.settings, 'show_navigation_arrows'):
                    self.previous_path_label.setVisible(self.settings.show_navigation_arrows)
            if hasattr(self, 'next_path_label') and isinstance(self.next_path_label, QPushButton):
                self.next_path_label.setEnabled(self.history_manager.has_next())
                if hasattr(self.settings, 'show_navigation_arrows'):
                    self.next_path_label.setVisible(self.settings.show_navigation_arrows)
        except RuntimeError as e:
            # Handle specific errors, e.g., object already deleted
            self.logger.warning(f"Error occurred {e}")

    def settings_update_handler(self, data: dict) -> None:
        """
        Perform actions upon settings change.

        Data is provided as a dictionary, where the key represents the setting name, and the value is its corresponding value.
        Note: This operation updates UI elements and internal properties, which may be resource-intensive.

        @param data: dict, say {"show_deleted_files": True}
        @return: None
        """

        self.logger.debug(f'Settings update handler is processing: {data}')

        if 'show_deleted_files' in data:
            # Update the status bar buttons
            self.draw_icons()

        if 'app_theme' in data:
            # Re-draw the statusbar icons
            try:
                self.draw_icons()
            except RuntimeError as e:
                # Handle specific errors, e.g., object already deleted
                self.logger.warning(f"Error occurred {e}")
            self.set_file_path(getattr(self, '_file_path', ''))
            self.refresh_system_load_graphs()

        if 'app_font_size' in data:
            try:
                self.refresh_element_fonts()
                self.draw_icons()
                self.refresh_compact_icons()
                self.refresh_system_load_graphs()
            except RuntimeError as e:
                # Handle specific errors, e.g., object already deleted
                self.logger.warning(f"Error occurred {e}")

        if 'app_language' in data:
            # Reload lexemes for the selected language and scope
            self.lexemes = Lexemes(self.settings.app_language, default_scope='statusbar')
            self.set_file_path(getattr(self, '_file_path', ''))
            self.refresh_system_load_tooltips()

        if 'file_path' in data:
            self.set_file_path(data['file_path'])

        if {'show_navigation_arrows', 'ui_init_ts'} & data.keys():
            # Update the status bar buttons
            self.draw_icons()
            self.update_history_buttons()

        if 'show_system_load_graphs' in data:
            self.update_system_load_visibility(prime=True)

        if 'system_load_interval_ms' in data:
            self.update_system_load_interval()

    def refresh_element_fonts(self, parent=None):
        if parent is None:
            self.setFont(self.parent.font())
            parent = self
        for widget in parent.children():
            if hasattr(widget, 'setFont'):
                widget.setFont(self.parent.font())
                self.refresh_element_fonts(parent=widget)

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
        self.warning_container.setVisible(visible)
        if visible:
            self.warning_label.setVisible(True)
            if tooltip:
                self.warning_label.setToolTip(tooltip)
        else:
            self.warning_label.setVisible(False)
            self.warning_label.setToolTip('')

    def show_save_progress(self, visible: bool) -> None:
        """Toggle the save icon and its layout container together."""
        self.save_progress_label.setVisible(visible)
        self.save_progress_container.setVisible(visible)

    def set_file_path(self, file_path: str = '') -> None:
        """Update the compact current-file icon and text."""
        self._file_path = str(file_path or '')
        file_name = os.path.basename(self._file_path)
        metrics = self.file_label.fontMetrics()
        self.file_label.setText(metrics.elidedText(
            file_name, Qt.TextElideMode.ElideMiddle, self.MAX_FILE_NAME_WIDTH))
        self.file_label.setAccessibleName(file_name)
        self.file_label.setVisible(bool(self._file_path))

        icon_color = QColor(self.theme_helper.get_color('statusbar_icon_color_default'))
        self.file_icon_label.setIcon(get_file_type_icon(self._file_path, self.theme_helper, color=icon_color))
        self._size_compact_button(self.file_icon_label)
        self.file_icon_label.setToolTip(self.lexemes.get(
            'statusbar_file_path_copy_tooltip', file_path=self._file_path))
        self.file_icon_label.setAccessibleName(file_name)
        self.file_icon_label.setVisible(bool(self._file_path))
        self.file_icon_container.setVisible(bool(self._file_path))

    def set_encryption_icon(self, encrypted: bool) -> None:
        """Render encryption state without relying on platform emoji glyphs."""
        self._encryption_encrypted = encrypted
        self._set_compact_label_icon(
            self.encryption_icon_label,
            'shield-lock-fill.svg' if encrypted else 'shield-lock.svg',
        )

    def refresh_compact_icons(self) -> None:
        """Resize compact status icons after an application font change."""
        self.set_file_path(getattr(self, '_file_path', ''))
        self._set_compact_label_icon(self.save_progress_label, 'floppy2.svg')
        self.set_encryption_icon(self._encryption_encrypted)
        self._size_compact_button(self.warning_label)

    def refresh_system_load_graphs(self) -> None:
        """Keep system-load graphs aligned with the active theme and font."""
        font_height = self.fontMetrics().height()
        graph_colors = (
            (self.cpu_load_graph, 'statusbar_cpu_graph_border_color', 'statusbar_cpu_graph_column_color'),
            (self.memory_load_graph, 'statusbar_memory_graph_border_color',
             'statusbar_memory_graph_column_color'),
        )
        for graph, border_key, column_key in graph_colors:
            graph.set_colors(
                QColor(self.theme_helper.get_color(border_key)),
                QColor(self.theme_helper.get_color(column_key)),
            )
            graph.set_graph_size(font_height)

    def refresh_system_load_tooltips(self) -> None:
        """Localize current system-load state without taking a new sample."""
        for graph in (self.cpu_load_graph, self.memory_load_graph):
            key = f'statusbar_system_{graph.metric_key}_usage'
            if graph.current_value is None:
                key += '_unavailable'
                text = self.lexemes.get(key)
            else:
                text = self.lexemes.get(key, percentage=graph.current_value)
            graph.set_status_text(text)

    def system_load_interval(self) -> int:
        """Return a safe polling interval from persisted settings."""
        interval = getattr(self.settings, 'system_load_interval_ms', self.DEFAULT_SYSTEM_LOAD_INTERVAL_MS)
        return max(self.MIN_SYSTEM_LOAD_INTERVAL_MS, min(self.MAX_SYSTEM_LOAD_INTERVAL_MS, interval))

    def update_system_load_interval(self) -> None:
        if self.system_load_timer is not None:
            self.system_load_timer.setInterval(self.system_load_interval())

    def update_system_load_visibility(self, prime: bool = False) -> None:
        """Show or suspend the complete system-load status-bar segment."""
        visible = bool(getattr(self.settings, 'show_system_load_graphs', True))
        for widget in (self.system_load_separator, self.cpu_load_graph, self.memory_load_graph):
            widget.setVisible(visible)

        if not visible:
            self.system_load_timer.stop()
            return

        if prime:
            try:
                psutil.cpu_percent(interval=None)
            except (OSError, RuntimeError, psutil.Error) as error:
                self.logger.warning(f'Unable to initialize CPU monitoring: {error}')
                self._system_load_error_logged = True
        self.system_load_timer.start(self.system_load_interval())

    def update_system_load(self) -> None:
        """Refresh non-blocking whole-system CPU and memory utilization."""
        try:
            cpu_percent = round(psutil.cpu_percent(interval=None))
            memory_percent = round(psutil.virtual_memory().percent)
        except (OSError, RuntimeError, psutil.Error) as error:
            if not self._system_load_error_logged:
                self.logger.warning(f'Unable to read system utilization: {error}')
                self._system_load_error_logged = True
            self.cpu_load_graph.set_unavailable()
            self.memory_load_graph.set_unavailable()
            self.refresh_system_load_tooltips()
            return

        self._system_load_error_logged = False
        self.cpu_load_graph.set_value(cpu_percent)
        self.memory_load_graph.set_value(memory_percent)
        self.refresh_system_load_tooltips()

    def _compact_icon_size(self) -> int:
        return max(10, int(self.fontMetrics().height() * 0.6))

    def _add_compact_icon(self, widget: QWidget) -> QWidget:
        """Place a compact right-side icon one pixel below the text baseline."""
        container = QWidget(self)
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 1, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(widget)
        self.labels_layout.addWidget(container)
        return container

    def _size_compact_button(self, button: QPushButton) -> None:
        icon_size = self._compact_icon_size()
        button.setIconSize(QSize(icon_size, icon_size))
        button.setFixedSize(QSize(icon_size, icon_size))

    def _set_compact_label_icon(self, label: QLabel, theme_icon: str) -> None:
        icon_size = self._compact_icon_size()
        icon = self.theme_helper.get_icon(
            theme_icon=theme_icon,
            color=QColor(self.theme_helper.get_color('statusbar_icon_color_default')),
        )
        label.setPixmap(icon.pixmap(QSize(icon_size, icon_size)))
        label.setFixedSize(QSize(icon_size, icon_size))

    def copy_file_path(self) -> None:
        """Copy the complete current file path to the system clipboard."""
        if getattr(self, '_file_path', ''):
            ClipboardHelper.set_text(self._file_path)

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
