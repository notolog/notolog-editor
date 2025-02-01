"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Provides app settings dialog.
- Functionality: Builds UI elements based on a data map and interactively updates the dialog as settings are changed.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2025 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import Qt, QObject, QSize, QRegularExpression
from PySide6.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QWidget, QSizePolicy, QPlainTextEdit, QScrollArea
from PySide6.QtWidgets import QLabel, QCheckBox, QLineEdit, QPushButton, QComboBox, QSpinBox, QDoubleSpinBox, QSlider

import logging
from typing import TYPE_CHECKING

from . import AppConfig
from . import Lexemes
from . import ThemeHelper

from ..enums.enum_base import EnumBase
from ..enums.languages import Languages
from ..enums.themes import Themes

from ..ui.enum_combo_box import EnumComboBox
from ..ui.horizontal_line_spacer import HorizontalLineSpacer
from ..ui.label_with_hint import LabelWithHint
from ..ui.dir_path_line_edit import DirPathLineEdit
from ..ui.file_path_line_edit import FilePathLineEdit

from ..modules.modules import Modules

if TYPE_CHECKING:
    from typing import Union  # noqa: F401


class SettingsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent, Qt.WindowType.Window)

        self.setWindowState(Qt.WindowState.WindowActive)

        # Make the dialog non-modal
        self.setModal(False)

        self.parent = parent

        # Apply font from the dialog instance to the label
        self.setFont(self.parent.font())

        # self.settings = Settings(parent=self)
        # Use parent's settings to allow the Settings emitted signals to be caught
        self.settings = self.parent.settings  # type: ignore

        self.theme_helper = ThemeHelper()

        self.logger = logging.getLogger('settings_dialog')

        # Load lexemes for selected language and scope
        self.lexemes = Lexemes(self.settings.app_language, default_scope='settings_dialog')

        self.setWindowTitle(self.lexemes.get('window_title'))

        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding)

        # Tabs widget as a main one
        self.tab_widget = None  # type: Union[QTabWidget, None]

        self.setStyleSheet(self.theme_helper.get_css('settings_dialog'))

        self.init_ui()

    def init_ui(self):
        # Dialog widget's main layout
        layout = QVBoxLayout(self)

        # Main tabs widget
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setFont(self.font())
        self.tab_widget.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding)
        # Add main tab widget to the layout
        layout.addWidget(self.tab_widget)

        # Get tabs fields config
        fields_conf = self.get_fields_conf()

        for conf in fields_conf:
            self.create_setting_field(conf)

        # Close button
        close_button = QPushButton(self.lexemes.get('button_close'))
        close_button.setFont(self.font())
        close_button.setObjectName('settings_dialog_button_close')
        close_button.clicked.connect(self.close)
        # Add close button to the layout
        layout.addWidget(close_button)

        self.connect_widgets()

        # Automatically adjust size to fit content
        # self.adjustSize()

        # Get the preferred size of the dialog's content
        preferred_size = self.parent.size()
        # Adjust the dialog's size based on the preferred size then
        if preferred_size.isValid():
            self.resize(QSize(int(preferred_size.width() * 0.5), int(preferred_size.height() * 0.9)))

    def get_fields_conf(self) -> list:
        # Load modules first to enable the loading of extension settings.
        module_instances = []
        for module in Modules().get_by_extension('settings_dialog'):
            # Pass settings object to avoid circular dependencies
            module_instances.append(Modules().create(module))

        fields_config = []
        fields_config.extend(self.get_general_fields())
        fields_config.extend(self.get_editor_config_fields())
        fields_config.extend(self.get_viewer_config_fields())
        fields_config.extend(self.get_ai_config_fields())

        # Extend settings UI based on extended settings
        for module_instance in module_instances:
            if hasattr(module_instance, 'extend_settings_dialog_fields_conf'):
                fields_config.extend(module_instance.extend_settings_dialog_fields_conf(self.tab_widget))
            else:
                self.logger.warning(f'Cannot extend settings_dialog for module {module_instance}')

        return fields_config

    def get_general_fields(self) -> list:
        # General
        tab_general = QWidget(self)

        # Create the scroll area
        scroll_area = QScrollArea(self)
        scroll_area.setObjectName('settings_dialog_tab_general')
        scroll_area.setWidgetResizable(True)

        # Layout for the General tab
        tab_general_layout = QVBoxLayout(tab_general)

        # Set the content widget inside the scroll area
        scroll_area.setWidget(tab_general)

        self.tab_widget.addTab(scroll_area, self.lexemes.get('tab_general'))

        return [
            # [General]
            # General settings block label
            {"type": QLabel, "name": "settings_dialog_general_app_config_label",
             "props": {"setProperty": ("class", "group-header-label")},
             "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('general_app_config_label'), "style": {"bold": True},
             "callback": lambda obj: tab_general_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop)},
            # Available languages label
            {"type": QLabel, "name": "settings_dialog_general_app_language_label",
             "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('general_app_language_label'),
             "callback": lambda obj: tab_general_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop)},
            # Available languages dropdown list
            {"type": EnumComboBox,
             "args": [sorted(Languages, key=lambda member: (not member.is_default, str(member.value)))],
             "name": "settings_dialog_general_app_language_combo:app_language",  # Lexeme key : Object name
             "callback": lambda obj: tab_general_layout.addWidget(obj),
             "placeholder_text": self.lexemes.get('general_app_language_combo_placeholder_text'),
             "accessible_description":
                 self.lexemes.get('app_language_combo_accessible_description')},
            # Available themes label
            {"type": QLabel, "name": "settings_dialog_general_app_theme_label", "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('general_app_theme_label'),
             "callback": lambda obj: tab_general_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop)},
            # Available themes dropdown list
            {"type": EnumComboBox, "args": [sorted(Themes, key=lambda member: (not member.is_default, str(member.value)))],
             "name": "settings_dialog_general_app_theme_combo:app_theme",  # Lexeme key : Object name
             "callback": lambda obj: tab_general_layout.addWidget(obj),
             "placeholder_text": self.lexemes.get('general_app_theme_combo_placeholder_text'),
             "accessible_description":
                 self.lexemes.get('general_app_theme_combo_accessible_description')},
            # Label for the default path input field
            {"type": LabelWithHint, "kwargs": {
                "tooltip": ('general_app_default_path_input_accessible_description',
                            self.lexemes.get('general_app_default_path_input_accessible_description'))},
             "name": "settings_dialog_general_app_default_path_label", "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('general_app_default_path_label'),
             "callback": lambda obj: tab_general_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop)},
            # Input field for the default folder for notes
            {"type": DirPathLineEdit, "kwargs": {"settings": self.settings},
             "name": "settings_dialog_general_app_default_path:default_path", "read_only": False,
             "callback": lambda obj: tab_general_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop),
             "placeholder_text": self.lexemes.get('general_app_default_path_input_placeholder_text'),
             "accessible_description":
                 self.lexemes.get('general_app_default_path_input_accessible_description')},
            # Horizontal spacer
            {"type": HorizontalLineSpacer, "callback": lambda obj: tab_general_layout.addWidget(obj)},
            # Elements visibility label
            {"type": QLabel, "name": "settings_dialog_general_app_main_menu_label",
             "props": {"setProperty": ("class", "group-header-label")},
             "alignment": Qt.AlignmentFlag.AlignLeft, "style": {"bold": True},
             "text": self.lexemes.get('general_app_elements_visibility_label'),
             "callback": lambda obj: tab_general_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop)},
            # Main menu label
            {"type": QLabel, "name": "settings_dialog_general_app_main_menu_label",
             "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('general_app_main_menu_label'),
             "callback": lambda obj: tab_general_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop)},
            # Toggle to show or hide the main menu
            {"type": QCheckBox,
             # Lexeme key : Object name
             "name": "settings_dialog_general_app_main_menu_checkbox:show_main_menu",
             "callback": lambda obj: tab_general_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop),
             "text": self.lexemes.get('general_app_main_menu_checkbox'),
             "accessible_description":
                 self.lexemes.get('general_app_main_menu_checkbox_accessible_description')},
            # Label for the status bar settings block
            {"type": QLabel, "name": "settings_dialog_general_statusbar_label", "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('general_statusbar_label'),
             "callback": lambda obj: tab_general_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop)},
            # Toggle to show or hide the global position in the status bar
            {"type": QCheckBox,
             # Lexeme key : Object name
             "name": "settings_dialog_general_statusbar_show_global_cursor_position_checkbox"
                     ":show_global_cursor_position",
             "callback": lambda obj: tab_general_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop),
             "text": self.lexemes.get('general_statusbar_show_global_cursor_position_checkbox'),
             "accessible_description":
                 self.lexemes.get('general_statusbar_show_global_cursor_position_checkbox_accessible_description')},
            # Horizontal spacer
            {"type": HorizontalLineSpacer, "callback": lambda obj: tab_general_layout.addWidget(obj)},
            # Main menu label
            {"type": QLabel, "name": "settings_dialog_general_app_font_size_label",
             "props": {"setProperty": ("class", "group-header-label")},
             "alignment": Qt.AlignmentFlag.AlignLeft, "style": {"bold": True},
             "text": self.lexemes.get('general_app_font_size_label', size=self.settings.app_font_size),
             "callback": lambda obj: tab_general_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop)},
            {"type": QSlider, "args": [Qt.Orientation.Horizontal],
             "props": {'setFocusPolicy': Qt.FocusPolicy.StrongFocus, 'setTickPosition': QSlider.TickPosition.TicksAbove,
                       'setTickInterval': 5, 'setSingleStep': 1,
                       'setMinimum': AppConfig().get_font_min_size(),
                       'setMaximum': AppConfig().get_font_max_size()},
             "name": "settings_dialog_general_app_font_size_slider:app_font_size",  # Lexeme key : Object name
             "callback": lambda obj: tab_general_layout.addWidget(obj),
             "accessible_description":
                 self.lexemes.get('general_app_font_size_slider_accessible_description')},
            # Spacer to keep elements above on top
            {"type": QWidget, "name": None, "size_policy": (QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding),
             "callback": lambda obj: tab_general_layout.addWidget(obj)},
        ]

    def get_editor_config_fields(self) -> list:
        # Editor
        tab_editor_config = QWidget(self)

        # Create the scroll area
        scroll_area = QScrollArea(self)
        scroll_area.setObjectName('settings_dialog_tab_editor_config')
        scroll_area.setWidgetResizable(True)

        # Layout for the Editor Config tab
        tab_editor_config_layout = QVBoxLayout(tab_editor_config)

        # Set the content widget inside the scroll area
        scroll_area.setWidget(tab_editor_config)

        self.tab_widget.addTab(scroll_area, self.lexemes.get('tab_editor_config'))

        return [
            # [Editor config]
            # Editor block label
            {"type": QLabel, "name": "settings_dialog_editor_config_label", "alignment": Qt.AlignmentFlag.AlignLeft,
             "props": {"setProperty": ("class", "group-header-label")},
             "text": self.lexemes.get('editor_config_label'), "style": {"bold": True},
             "callback": lambda obj: tab_editor_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop)},
            # Either to show or not editor's line numbers
            {"type": QCheckBox,
             # Lexeme key : Object name
             "name": "settings_dialog_editor_config_show_line_numbers_checkbox:show_line_numbers",
             "callback": lambda obj: tab_editor_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop),
             "text": self.lexemes.get('editor_config_show_line_numbers_checkbox'),
             "accessible_description":
                 self.lexemes.get('editor_config_show_line_numbers_checkbox_accessible_description')},
            # Spacer to keep elements above on top
            {"type": QWidget, "name": None, "size_policy": (QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding),
             "callback": lambda obj: tab_editor_config_layout.addWidget(obj)},
        ]

    def get_viewer_config_fields(self) -> list:
        # Viewer
        tab_viewer_config = QWidget(self)

        # Create the scroll area
        scroll_area = QScrollArea(self)
        scroll_area.setObjectName('settings_dialog_tab_viewer_config')
        scroll_area.setWidgetResizable(True)

        # Layout for the Viewer Config tab
        tab_viewer_config_layout = QVBoxLayout(tab_viewer_config)

        # Set the content widget inside the scroll area
        scroll_area.setWidget(tab_viewer_config)

        self.tab_widget.addTab(scroll_area, self.lexemes.get('tab_viewer_config'))

        return [
            # [Viewer config]
            # Viewer block label
            {"type": QLabel, "name": "settings_dialog_viewer_config_label", "alignment": Qt.AlignmentFlag.AlignLeft,
             "props": {"setProperty": ("class", "group-header-label")},
             "text": self.lexemes.get('viewer_config_label'), "style": {"bold": True},
             "callback": lambda obj: tab_viewer_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop)},
            # Either to show or not viewer's emojis
            {"type": QCheckBox,
             # Lexeme key : Object name
             "name": "settings_dialog_viewer_config_process_emojis_checkbox:viewer_process_emojis",
             "callback": lambda obj: tab_viewer_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop),
             "text": self.lexemes.get('viewer_config_process_emojis_checkbox'),
             "accessible_description":
                 self.lexemes.get('viewer_config_process_emojis_checkbox_accessible_description')},
            # Spacer
            {"type": QWidget, "name": None, "size_policy": (QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum),
             "callback": lambda obj: tab_viewer_config_layout.addWidget(obj)},
            # Either to show or not viewer's TODOs
            {"type": QCheckBox,
             # Lexeme key : Object name
             "name": "settings_dialog_viewer_config_highlight_todos_checkbox:viewer_highlight_todos",
             "callback": lambda obj: tab_viewer_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop),
             "text": self.lexemes.get('viewer_config_highlight_todos_checkbox'),
             "accessible_description":
                 self.lexemes.get('viewer_config_highlight_todos_checkbox_accessible_description')},
            # Spacer
            {"type": QWidget, "name": None, "size_policy": (QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum),
             "callback": lambda obj: tab_viewer_config_layout.addWidget(obj)},
            # Either to show open link confirmation dialog or not
            {"type": QCheckBox,
             # Lexeme key : Object name
             "name": "settings_dialog_viewer_config_open_link_confirmation_checkbox:viewer_open_link_confirmation",
             "callback": lambda obj: tab_viewer_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop),
             "text": self.lexemes.get('viewer_config_open_link_confirmation_checkbox'),
             "accessible_description":
                 self.lexemes.get('viewer_config_open_link_confirmation_checkbox_accessible_description')},
            # Spacer
            {"type": QWidget, "name": None, "size_policy": (QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum),
             "callback": lambda obj: tab_viewer_config_layout.addWidget(obj)},
            # Auto save downloaded resources on disk
            {"type": QCheckBox,
             # Lexeme key : Object name
             "name": "settings_dialog_viewer_config_save_resources_checkbox:viewer_save_resources",
             "callback": lambda obj: tab_viewer_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop),
             "text": self.lexemes.get('viewer_config_save_resources_checkbox'),
             "accessible_description":
                 self.lexemes.get('viewer_config_save_resources_checkbox_accessible_description')},
            # Spacer to keep elements above on top
            {"type": QWidget, "name": None, "size_policy": (QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding),
             "callback": lambda obj: tab_viewer_config_layout.addWidget(obj)},
        ]

    def get_ai_config_fields(self) -> list:
        # AI Config
        tab_ai_config = QWidget(self)

        # Create the scroll area
        scroll_area = QScrollArea(self)
        scroll_area.setObjectName('settings_dialog_tab_ai_config')
        scroll_area.setWidgetResizable(True)

        # Layout for the AI Config tab
        tab_ai_config_layout = QVBoxLayout(tab_ai_config)

        # Set the content widget inside the scroll area
        scroll_area.setWidget(tab_ai_config)

        self.tab_widget.addTab(scroll_area, self.lexemes.get('tab_ai_config'))

        return [
            # [AI config]
            # Default inference model label
            {"type": QLabel, "name": "settings_dialog_ai_config_inference_module_label",
             "props": {"setProperty": ("class", "group-header-label")},
             "alignment": Qt.AlignmentFlag.AlignLeft, "style": {"bold": True},
             "text": self.lexemes.get('ai_config_inference_module_label'),
             "callback": lambda obj: tab_ai_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop)},
            # Supported models label
            {"type": LabelWithHint, "kwargs": {
                "tooltip": ('ai_config_inference_module_names_combo_accessible_description',
                            self.lexemes.get('ai_config_inference_module_names_combo_accessible_description'))},
             "name": "settings_dialog_ai_config_inference_module_names_combo_label",
             "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('ai_config_inference_module_names_combo_label'),
             "callback": lambda obj: tab_ai_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop)},
            # Supported models dropdown list
            {"type": EnumComboBox,
             "args": [sorted(EnumBase('InferenceModuleNames', self.settings.ai_config_inference_modules),
                      key=lambda member: (not member.is_default, str(member.value)))],
             "name": "settings_dialog_ai_config_inference_module_names_combo:ai_config_inference_module",
             "callback": lambda obj: tab_ai_config_layout.addWidget(obj),
             "placeholder_text": self.lexemes.get('ai_config_inference_module_names_combo_placeholder_text'),
             "accessible_description":
                 self.lexemes.get('ai_config_inference_module_names_combo_accessible_description')},
            # Horizontal spacer
            {"type": HorizontalLineSpacer, "callback": lambda obj: tab_ai_config_layout.addWidget(obj)},
            # Base AI settings block label
            {"type": QLabel, "name": "settings_dialog_ai_config_base_label", "alignment": Qt.AlignmentFlag.AlignLeft,
             "props": {"setProperty": ("class", "group-header-label")},
             "text": self.lexemes.get('ai_config_base_label'), "style": {"bold": True},
             "callback": lambda obj: tab_ai_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop)},
            # Auto save downloaded resources on disk
            {"type": QCheckBox,
             # Lexeme key : Object name
             "name": "settings_dialog_ai_config_multi_turn_dialogue_checkbox:ai_config_multi_turn_dialogue",
             "callback": lambda obj: tab_ai_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop),
             "text": self.lexemes.get('ai_config_multi_turn_dialogue_checkbox'),
             "accessible_description":
                 self.lexemes.get('ai_config_multi_turn_dialogue_checkbox_accessible_description')},
            # Spacer
            {"type": QWidget, "name": None, "size_policy": (QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum),
             "callback": lambda obj: tab_ai_config_layout.addWidget(obj)},
            # Auto save downloaded resources on disk
            {"type": QCheckBox,
             # Lexeme key : Object name
             "name": "settings_dialog_ai_config_convert_to_md_checkbox:ai_config_convert_to_md",
             "callback": lambda obj: tab_ai_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop),
             "text": self.lexemes.get('ai_config_convert_to_md_checkbox'),
             "accessible_description": self.lexemes.get('ai_config_convert_to_md_checkbox_accessible_description')},
            # Spacer to keep elements above on top
            {"type": QWidget, "name": None, "size_policy": (QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding),
             "callback": lambda obj: tab_ai_config_layout.addWidget(obj)},
        ]

    def apply_props(self, widget, properties):
        for prop, value in properties.items():
            # Get the method based on the property name
            setter = getattr(widget, prop, None)
            if callable(setter):
                if type(value) is tuple:
                    setter(*value)  # Call the setter with the provided values
                else:
                    setter(value)  # Call the setter with the provided value

    def create_setting_field(self, conf) -> QWidget:  # noqa: C901
        """
        Create a UI setting field dynamically based on the provided configuration.

        Args:
            conf (dict): Configuration for the field. Includes type, properties, callbacks, and visual settings.

        Returns:
            QWidget: The dynamically created UI object.
        """

        # Extract arguments for the object initialization
        _args = conf.get('args', [self])  # Default to adding to the dialog
        _kwargs = conf.get('kwargs', {})

        # Instantiate the UI object of the specified type
        obj = conf['type'](*_args, **_kwargs)

        # Apply dialog-wide font if supported (e.g., QLabel, QLineEdit, etc.)
        if hasattr(obj, 'setFont'):
            obj.setFont(self.font())

        # Apply custom properties (if defined in the configuration)
        if 'props' in conf:
            self.apply_props(obj, conf['props'])

        # Set object name for better debugging and callback management
        if 'name' in conf and conf['name']:
            obj.setObjectName(conf['name'])

        # Apply common text-related properties
        for key, method in [
            ('text', 'setText'),
            ('read_only', 'setReadOnly'),
            ('max_length', 'setMaxLength'),
            ('placeholder_text', 'setPlaceholderText'),
            ('accessible_description', 'setAccessibleDescription'),
        ]:
            if key in conf and hasattr(obj, method):
                getattr(obj, method)(conf[key])

        # Apply size policies if specified
        if 'size_policy' in conf:
            params = conf['size_policy']
            if isinstance(params, tuple):
                obj.setSizePolicy(*params)
            else:
                obj.setSizePolicy(params)

        # Set alignment if supported and specified
        if 'alignment' in conf and hasattr(obj, 'setAlignment'):
            obj.setAlignment(conf['alignment'])

        # Handle layout-related callbacks
        if 'callback' in conf and callable(conf['callback']):
            conf['callback'](obj)

        # Handle value change callbacks for interactive widgets
        if 'on_value_change' in conf and callable(conf['on_value_change']):
            obj.valueChanged.connect(lambda: conf['on_value_change'](source_object=obj, source_widget=self))

        # Apply styles (bold, italic, color) via stylesheet
        if 'style' in conf:
            styles = []
            if 'bold' in conf['style']:
                styles.append('font-weight: bold;')
            if 'italic' in conf['style']:
                styles.append('font-style: italic;')
            if 'color' in conf['style']:
                styles.append(f"color: {conf['style']['color']};")
            if styles:
                obj.setStyleSheet(' '.join(styles))

        # Set the height for QPlainTextEdit based on the number of text lines (if specified)
        if 'text_lines' in conf and isinstance(obj, QPlainTextEdit) and int(conf['text_lines']) > 0:
            font_metrics = obj.fontMetrics()
            lines_height = font_metrics.height() * conf['text_lines']
            obj.setFixedHeight(lines_height)

        # Return the dynamically created object
        return obj

    def parse_object_name(self, object_name: str):
        return self.settings.settings_helper.parse_object_name(object_name)

    def connect_widgets(self):  # noqa: C901 - consider simplifying this method
        # Find children of type QCheckBox
        checkboxes = self.findChildren(QCheckBox)
        for checkbox in checkboxes:
            if isinstance(checkbox, QCheckBox):
                # Parse the object name in case it contains a combination of lexeme and setting keys
                _lexeme_key, setting_name = self.parse_object_name(checkbox.objectName())
                if hasattr(self.settings, setting_name):
                    checkbox.setChecked(getattr(self.settings, setting_name, False))
                # Connect signal after set up defaults or restore saved value to avoid signal emitting right after.
                checkbox.stateChanged.connect(self.save_settings)

        # Find children of type QComboBox
        combo_boxes = self.findChildren(QComboBox)
        for combo_box in combo_boxes:
            if isinstance(combo_box, EnumComboBox):
                # Parse the object name in case it contains a combination of lexeme and setting keys
                _lexeme_key, setting_name = self.parse_object_name(combo_box.objectName())
                if hasattr(self.settings, setting_name):
                    setting_value = getattr(self.settings, setting_name, None)
                    # Get the index of the Enum member by the name stored in the settings (e.g. Language's 'EN')
                    index = next((i for i, val in enumerate(combo_box.enum_class) if val.name.lower() == setting_value),
                                 None)
                    self.logger.debug(f'Enum {combo_box.enum_class} index for value: {index} [{setting_value}]')
                    if index is not None:
                        combo_box.setCurrentIndex(index)
                # Connect signal after set up defaults or restore saved value to avoid signal emitting right after.
                combo_box.currentIndexChanged.connect(self.save_settings)

        # Find children of type QSpinBox
        spin_boxes = self.findChildren(QSpinBox)
        for spin_box in spin_boxes:
            if isinstance(spin_box, QSpinBox):
                # Parse the object name in case it contains a combination of lexeme and setting keys
                _lexeme_key, setting_name = self.parse_object_name(spin_box.objectName())
                if hasattr(self.settings, setting_name):
                    spin_box.setValue(getattr(self.settings, setting_name, 0))
                spin_box.valueChanged.connect(self.save_settings)

        # Find children of type QDoubleSpinBox
        double_spin_boxes = self.findChildren(QDoubleSpinBox)
        for double_spin_box in double_spin_boxes:
            if isinstance(double_spin_box, QDoubleSpinBox):
                # Parse the object name in case it contains a combination of lexeme and setting keys
                _lexeme_key, setting_name = self.parse_object_name(double_spin_box.objectName())
                if hasattr(self.settings, setting_name):
                    double_spin_box.setValue(getattr(self.settings, setting_name, 0))
                double_spin_box.valueChanged.connect(self.save_settings)

        # Find children of type QLineEdit
        line_edits = self.findChildren(QLineEdit)
        for line_edit in line_edits:
            if isinstance(line_edit, QLineEdit):
                # Parse the object name in case it contains a combination of lexeme and setting keys
                _lexeme_key, setting_name = self.parse_object_name(line_edit.objectName())
                if hasattr(self.settings, setting_name):
                    line_edit.setText(str(getattr(self.settings, setting_name, '')))
                # Connect signal after set up defaults or restore saved value to avoid signal emitting right after.
                line_edit.textChanged.connect(self.save_settings)

        # Find children of type QPlainTextEdit
        text_edits = self.findChildren(QPlainTextEdit)
        for text_edit in text_edits:
            if isinstance(text_edit, QPlainTextEdit):
                # Parse the object name in case it contains a combination of lexeme and setting keys
                _lexeme_key, setting_name = self.parse_object_name(text_edit.objectName())
                if hasattr(self.settings, setting_name):
                    text_edit.setPlainText(getattr(self.settings, setting_name, ''))
                # Connect signal after set up defaults or restore saved value to avoid signal emitting right after.
                text_edit.textChanged.connect(self.save_settings)

        # Find children of type QSlider
        sliders = self.findChildren(QSlider)
        for slider in sliders:
            if isinstance(slider, QSlider):
                # Parse the object name in case it contains a combination of lexeme and setting keys
                _lexeme_key, setting_name = self.parse_object_name(slider.objectName())
                if hasattr(self.settings, setting_name):
                    slider.setValue(getattr(self.settings, setting_name, 0))
                slider.valueChanged.connect(self.save_settings)

    def save_settings(self):  # noqa: C901 - consider simplifying this method
        # Determine which widget emitted the signal by the object name set
        sender_widget = self.sender()
        sender_name = sender_widget.objectName()

        if sender_name.startswith('qt_'):
            # For QSpinBox or QDoubleSpinBox, 'qt_spinbox_lineedit' refers to the internal QLineEdit widget
            # used for handling text input (e.g., via typing).
            if sender_widget and sender_name == "qt_spinbox_lineedit":
                sender_widget = sender_widget.parent()  # Resolve to the parent widget (QSpinBox).
                sender_name = sender_widget.objectName()
            else:
                self.logger.warning(f"Unhandled internal widget type: {sender_name}")
                return

        # Parse the object name in case it contains a combination of lexeme and setting keys
        lexeme_key, setting_name = self.parse_object_name(sender_name)

        setting_value = None
        setting_text = None
        if isinstance(sender_widget, QCheckBox):
            setting_value = sender_widget.isChecked()
            setting_text = sender_widget.text()
        elif isinstance(sender_widget, QComboBox):
            # Index of the item in the enum
            # index = sender_widget.currentIndex()
            # setting_value = sender_widget.currentData()
            setting_text = sender_widget.currentText()
            """
            To get enum name instead of the value, say for Languages:
            index = sender_widget.currentIndex()
            setting_value = list(Languages)[index].name
            """
            setting_value = sender_widget.currentData().name.lower()  # Save in lower case
        elif isinstance(sender_widget, QSpinBox):
            setting_value = sender_widget.value()
            setting_text = sender_widget.text()
        elif isinstance(sender_widget, QDoubleSpinBox):
            setting_value = sender_widget.value()
            setting_text = sender_widget.text()
        elif isinstance(sender_widget, QLineEdit):
            setting_value = sender_widget.text()
            setting_text = sender_widget.placeholderText()
        elif isinstance(sender_widget, QPlainTextEdit):
            setting_value = sender_widget.toPlainText()
            setting_text = sender_widget.placeholderText()
        elif isinstance(sender_widget, QSlider):
            setting_value = sender_widget.value()
            setting_text = sender_widget.accessibleDescription()

        self.logger.debug(f"Saving setting '{setting_name}': {setting_value} ({setting_text})")

        try:
            setattr(self.settings, setting_name, setting_value)
        except AttributeError as e:
            self.logger.warning(f'ERROR: {e}')

        self.logger.debug(f"Setting new value: {getattr(self.settings, setting_name)}")

        """
        In case of language change try to update as much text labels as possible.
        It may not cover all the labels, but may help with update anyway.
        """
        if setting_name == 'app_language' or sender_widget.objectName().endswith('app_language'):
            # Update lexemes object as app language has just been changed
            self.lexemes = Lexemes(self.settings.app_language, default_scope='settings_dialog')
            # Get all the new lexemes
            app_language_lexemes = self.lexemes.get_all()

            # Load modules to retrieve lexemes for the settings dialog
            for module in Modules().get_by_extension('settings_dialog'):
                # Pass settings object to avoid circular dependencies
                module_instance = Modules().create(module)
                if hasattr(module_instance, 'lexemes'):
                    app_language_lexemes['settings_dialog'].update(
                        module_instance.lexemes.get_by_scope('settings_dialog'))

            # Update dialog title at first
            self.setWindowTitle(self.lexemes.get('window_title'))
            # Iterate each lexeme's scope to match it with object name to update the text if applicable
            for scope in app_language_lexemes:
                self.logger.debug(f'Lexeme scope to check updates {scope}')
                # Iterate each lexeme from the scope
                for lexeme_key in app_language_lexemes[scope].keys():
                    """
                    Some objects may have name set with ":" delimiter, which means "lexeme_key:setting_name".
                    It may help to transfer more params with object name with ease.
                    """
                    # Parse the object name in case it contains a combination of lexeme and setting keys
                    lexeme_key, setting_name = self.parse_object_name(lexeme_key)

                    # Get lexeme in the new language set
                    lexeme = app_language_lexemes[scope][lexeme_key]

                    """
                    Search with regex as the object name should contain scope and may contain setting name as well,
                    but the lexeme key is a crucial part of the name in this search.
                    """
                    regex = QRegularExpression(f"(?={scope}_)?{lexeme_key}.*?")
                    # The self.findChildren() method results contain only the elements related to this dialog
                    found_objects = self.findChildren(QObject, regex, Qt.FindChildOption.FindChildrenRecursively)
                    if not found_objects:
                        # Try to find it in the parent dialog to update the main window elements
                        found_objects = self.parent.findChildren(QObject, regex,
                                                                 Qt.FindChildOption.FindChildrenRecursively)
                        if found_objects:
                            self.logger.debug(f"Found object to update ({scope}){lexeme_key}: {found_objects}")

                    # Search by the full object name
                    # object_name = self.lexemes.get_full_key(lexeme_key)
                    # found_objects = self.findChildren(QObject, object_name, Qt.FindChildrenRecursively)

                    for obj in found_objects:
                        if (isinstance(obj, (QLabel, LabelWithHint, QCheckBox, QComboBox))
                                and hasattr(obj, 'setText')
                                and callable(getattr(obj, 'setText'))):
                            self.logger.debug(
                                f'Object lexeme update: {obj.objectName()} with id: {id(obj)}, lexeme "{lexeme}"')
                            obj.setText(lexeme)
                        if isinstance(obj, QPushButton):
                            self.logger.debug(
                                f'Object lexeme update: {obj.objectName()} with id: {id(obj)}, lexeme "{lexeme}"')
                            if obj.text():  # Update only if a text value was previously set
                                obj.setText(lexeme)
                            if obj.toolTip():  # Update only if a text value was previously set
                                obj.setToolTip(lexeme)
                        if isinstance(obj, LabelWithHint):
                            if obj.property('tooltip_lexeme'):
                                # Lexeme must be default_scope='settings_dialog'
                                obj.set_tooltip(self.lexemes.get(obj.property('tooltip_lexeme')))
                        if isinstance(obj, QScrollArea):
                            # Add iterable map of the tabs to change the search by QWidget to explicitly set tab text.
                            self.set_tab_text(obj.objectName(), lexeme)
                        # Exclusions
                        if obj.objectName() == "settings_dialog_general_app_font_size_label":
                            obj.setText(
                                self.lexemes.get('general_app_font_size_label', size=self.settings.app_font_size))

        if setting_name == 'app_theme' or sender_widget.objectName().endswith('app_theme'):
            # Update the widget's stylesheet with the selected theme
            self.setStyleSheet(self.theme_helper.get_css('settings_dialog'))
            # Update font size to correct the tab widget's font
            self.update_font_size(font_size=self.settings.app_font_size)

            # Search objects to update by their type
            found_objects = self.findChildren(LabelWithHint)
            found_objects += self.findChildren(DirPathLineEdit)
            found_objects += self.findChildren(FilePathLineEdit)
            for obj in found_objects:
                if (isinstance(obj, (LabelWithHint, DirPathLineEdit, FilePathLineEdit))
                        and hasattr(obj, 'load_icon')
                        and callable(getattr(obj, 'load_icon'))):
                    obj.load_icon()

        if setting_name == 'app_font_size' or sender_widget.objectName().endswith('app_font_size'):
            # Update the font size of elements
            self.update_font_size(font_size=setting_value)

    def update_font_size(self, font_size: int):
        # Update the font from the parent to ensure it reflects the new font size.
        # A simple font size update should also work.
        self.setFont(self.parent.font())
        widgets_to_update = [QLabel, QTabWidget, QPushButton, QCheckBox, QLineEdit, QPlainTextEdit, QComboBox,
                             QSpinBox, QDoubleSpinBox, QSlider]
        for _widget in widgets_to_update:
            # Find all QLabel objects
            found_objects = self.findChildren(_widget)
            for obj in found_objects:
                # Align with the dialog font size (mostly for QLabel)
                if hasattr(obj, 'setFont'):
                    obj.setFont(self.font())
                if hasattr(obj, 'toolTip'):
                    obj.setStyleSheet("QToolTip { font-size: %dpt; }" % font_size)
                if obj.objectName() == "settings_dialog_general_app_font_size_label":
                    """
                    # Update the font size on the label
                    font = QFont()
                    font.setPointSize(setting_value)
                    app_font_size_label.setFont(font)
                    """
                    obj.setText(self.lexemes.get('general_app_font_size_label', size=font_size))

    def set_tab_text(self, tab_object_name, text):
        # Iterate through all the tabs
        for index in range(self.tab_widget.count()):
            # Get the widget for the current index
            widget = self.tab_widget.widget(index)  # type: Union[QScrollArea, QWidget]

            # Check if this widget matches the object name
            if widget.objectName() == tab_object_name:
                # Set the text
                self.tab_widget.setTabText(index, text)
                break
