from PySide6.QtCore import Qt, QObject, QRegularExpression
from PySide6.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QWidget, QFrame, QSizePolicy, QPlainTextEdit
from PySide6.QtWidgets import QLabel, QCheckBox, QLineEdit, QPushButton, QComboBox, QSpinBox, QSlider, QSpacerItem

import logging
from typing import Union

from ..app_config import AppConfig
from ..lexemes.lexemes import Lexemes
from ..helpers.theme_helper import ThemeHelper
from ..enums.languages import Languages
from ..enums.ai_model_names import AiModelNames
from ..enums.themes import Themes
from ..ui.enum_combo_box import EnumComboBox


class SettingsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent, Qt.WindowType.Dialog)

        self.parent = parent

        # Apply font from the dialog instance to the label
        self.setFont(self.parent.font())

        # self.settings = Settings(parent=self)
        # Use parent's settings to allow the Settings emitted signals to be caught
        self.settings = self.parent.settings  # type: ignore

        self.theme_helper = ThemeHelper()

        self.logger = logging.getLogger('settings_dialog')

        self.logging = AppConfig.get_logging()
        self.debug = AppConfig.get_debug()

        # Default language setup, change to settings value to modify it via UI
        self.lexemes = Lexemes(self.settings.app_language, default_scope='settings_dialog')

        self.setWindowTitle(self.lexemes.get('window_title'))

        # Set dialog size derived from the main window size
        main_window_size = self.parent.size()
        dialog_width = int(main_window_size.width() * 0.33)
        dialog_height = int(main_window_size.height() * 0.33)
        self.setMinimumSize(dialog_width, dialog_height)

        # Tabs widget as a main one
        self.tab_widget = Union[QWidget, None]

        self.setStyleSheet(self.theme_helper.get_css('settings_dialog'))

        self.init_ui()

    def init_ui(self):
        # Dialog widget's main layout
        layout = QVBoxLayout(self)

        # Main tabs widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        layout.addWidget(self.tab_widget)

        # Add tabs to the main widget
        # General
        tab_general = QWidget(self)
        tab_general.setObjectName('settings_dialog_tab_general')
        # Editor
        tab_editor_config = QWidget(self)
        tab_editor_config.setObjectName('settings_dialog_tab_editor_config')
        # Viewer
        tab_viewer_config = QWidget(self)
        tab_viewer_config.setObjectName('settings_dialog_tab_viewer_config')
        # AI Config
        tab_ai_config = QWidget(self)
        tab_ai_config.setObjectName('settings_dialog_tab_ai_config')

        self.tab_widget.addTab(tab_general, self.lexemes.get('tab_general'))
        self.tab_widget.addTab(tab_editor_config, self.lexemes.get('tab_editor_config'))
        self.tab_widget.addTab(tab_viewer_config, self.lexemes.get('tab_viewer_config'))
        self.tab_widget.addTab(tab_ai_config, self.lexemes.get('tab_ai_config'))

        # Layout for the General tab
        tab_general_layout = QVBoxLayout(tab_general)
        # Layout for the Editor Config tab
        tab_editor_config_layout = QVBoxLayout(tab_editor_config)
        # Layout for the Viewer Config tab
        tab_viewer_config_layout = QVBoxLayout(tab_viewer_config)
        # Layout for the AI Config tab
        tab_ai_config_layout = QVBoxLayout(tab_ai_config)
        """
        Set spacing between widgets if needed:
        tab_ai_config_layout.setSpacing(5)
        """

        fields_conf = [
            # [General]
            # General settings block label
            {"type": QLabel, "name": "settings_dialog_general_app_config_label", "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('general_app_config_label'), "style": {"bold": True},
             "callback": lambda obj: tab_general_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop)},
            # Available languages label
            {"type": QLabel, "name": "settings_dialog_general_app_language_label", "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('general_app_language_label'),
             "callback": lambda obj: tab_general_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop)},
            # Available languages dropdown list
            {"type": EnumComboBox, "args": [Languages],
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
            {"type": EnumComboBox, "args": [Themes],
             "name": "settings_dialog_general_app_theme_combo:app_theme",  # Lexeme key : Object name
             "callback": lambda obj: tab_general_layout.addWidget(obj),
             "placeholder_text": self.lexemes.get('general_app_theme_combo_placeholder_text'),
             "accessible_description":
                 self.lexemes.get('general_app_theme_combo_accessible_description')},
            # Horizontal spacer
            {"type": self.layout_horizontal_spacer, "args": [tab_general_layout]},
            # Main menu label
            {"type": QLabel, "name": "settings_dialog_general_app_main_menu_label",
             "alignment": Qt.AlignmentFlag.AlignLeft, "style": {"bold": True},
             "text": self.lexemes.get('general_app_main_menu_label'),
             "callback": lambda obj: tab_general_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop)},
            # Either show or not main menu
            {"type": QCheckBox,
             # Lexeme key : Object name
             "name": "settings_dialog_general_app_main_menu_checkbox:show_main_menu",
             "callback": lambda obj: tab_general_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop),
             "text": self.lexemes.get('general_app_main_menu_checkbox'),
             "accessible_description":
                 self.lexemes.get('general_app_main_menu_checkbox_accessible_description')},
            # Horizontal spacer
            {"type": self.layout_horizontal_spacer, "args": [tab_general_layout]},
            # Status bar settings block label
            {"type": QLabel, "name": "settings_dialog_general_statusbar_label", "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('general_statusbar_label'), "style": {"bold": True},
             "callback": lambda obj: tab_general_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop)},
            # Either show or not global position at status bar
            {"type": QCheckBox,
             # Lexeme key : Object name
             "name": "settings_dialog_general_statusbar_show_global_cursor_position_checkbox"
                     ":show_global_cursor_position",
             "callback": lambda obj: tab_general_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop),
             "text": self.lexemes.get('general_statusbar_show_global_cursor_position_checkbox'),
             "accessible_description":
                 self.lexemes.get('general_statusbar_show_global_cursor_position_checkbox_accessible_description')},
            # Horizontal spacer
            {"type": self.layout_horizontal_spacer, "args": [tab_general_layout]},
            # Main menu label
            {"type": QLabel, "name": "settings_dialog_general_app_font_size_label",
             "alignment": Qt.AlignmentFlag.AlignLeft, "style": {"bold": True},
             "text": self.lexemes.get('general_app_font_size_label', size=self.settings.app_font_size),
             "callback": lambda obj: tab_general_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop)},
            {"type": QSlider, "args": [Qt.Orientation.Horizontal],
             "props": {'setFocusPolicy': Qt.FocusPolicy.StrongFocus, 'setTickPosition': QSlider.TickPosition.TicksAbove,
                       'setTickInterval': 5, 'setSingleStep': 1,
                       'setMinimum': AppConfig.get_font_min_size(), 'setMaximum': AppConfig.get_font_max_size()},
             "name": "settings_dialog_general_app_font_size_slider:app_font_size",  # Lexeme key : Object name
             "callback": lambda obj: tab_general_layout.addWidget(obj),
             "accessible_description":
                 self.lexemes.get('general_app_font_size_slider_accessible_description')},
            # Spacer to keep elements above on top
            {"type": QWidget, "name": None, "size_policy": (QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding),
             "callback": lambda obj: tab_general_layout.addWidget(obj)},

            # [Editor config]
            # Editor block label
            {"type": QLabel, "name": "settings_dialog_editor_config_label", "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('editor_config_label'), "style": {"bold": True},
             "callback": lambda obj: tab_editor_config_layout.addWidget(obj)},
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

            # [Viewer config]
            # Viewer block label
            {"type": QLabel, "name": "settings_dialog_viewer_config_label", "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('viewer_config_label'), "style": {"bold": True},
             "callback": lambda obj: tab_viewer_config_layout.addWidget(obj)},
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
            # Spacer to keep elements above on top
            {"type": QWidget, "name": None, "size_policy": (QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding),
             "callback": lambda obj: tab_viewer_config_layout.addWidget(obj)},

            # [AI config]
            # OpenAI API block label
            {"type": QLabel, "name": "settings_dialog_ai_config_openai_api_label", "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('ai_config_openai_api_label'), "style": {"bold": True},
             "callback": lambda obj: tab_ai_config_layout.addWidget(obj)},
            # OpenAI API url line input
            {"type": QLineEdit, "name": "settings_dialog_ai_config_openai_url:ai_config_openai_url",
             "read_only": False, "max_length": 128,
             "callback": lambda obj: tab_ai_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop),
             "placeholder_text": self.lexemes.get('ai_config_openai_api_url_input_placeholder_text'),
             "accessible_description":
                 self.lexemes.get('ai_config_openai_api_url_input_accessible_description')},
            # OpenAI API key line input
            {"type": QLineEdit, "name": "settings_dialog_ai_config_openai_key:ai_config_openai_key",
             "read_only": False, "max_length": 128,
             "callback": lambda obj: tab_ai_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop),
             "placeholder_text": self.lexemes.get('ai_config_openai_api_key_input_placeholder_text'),
             "accessible_description":
                 self.lexemes.get('ai_config_openai_api_key_input_accessible_description')},
            # Spacer
            {"type": QWidget, "name": None, "size_policy": (QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum),
             "callback": lambda obj: tab_ai_config_layout.addWidget(obj)},
            # Supported models label
            {"type": QLabel, "name": "settings_dialog_ai_config_openai_api_supported_models_label",
             "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('ai_config_openai_api_supported_models_label'),
             "callback": lambda obj: tab_ai_config_layout.addWidget(obj)},
            # Supported models dropdown list
            {"type": EnumComboBox, "args": [sorted(AiModelNames, key=lambda member: member.legacy)],  # legacy below
             "name": "settings_dialog_ai_config_ai_model_names_combo:ai_config_openai_model",
             "callback": lambda obj: tab_ai_config_layout.addWidget(obj),
             "placeholder_text": self.lexemes.get('ai_config_ai_model_names_combo_placeholder_text'),
             "accessible_description":
                 self.lexemes.get('ai_config_ai_model_names_combo_accessible_description')},
            # Horizontal spacer
            {"type": self.layout_horizontal_spacer, "args": [tab_ai_config_layout]},
            # Status bar settings block label
            {"type": QLabel, "name": "settings_dialog_ai_config_base_label", "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('ai_config_base_label'), "style": {"bold": True},
             "callback": lambda obj: tab_ai_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop)},
            # Base system prompt label
            {"type": QLabel, "name": "settings_dialog_ai_config_base_system_prompt_label",
             "alignment": Qt.AlignmentFlag.AlignLeft, "text": self.lexemes.get('ai_config_base_system_prompt_label'),
             "callback": lambda obj: tab_ai_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop)},
            # Base system prompt text edit
            {"type": QPlainTextEdit, "name": "settings_dialog_ai_config_base_system_prompt:ai_config_base_system_prompt",
             "callback": lambda obj: tab_ai_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop),
             "placeholder_text": self.lexemes.get('ai_config_base_system_prompt_edit_placeholder_text'),
             "accessible_description":
                 self.lexemes.get('ai_config_base_system_prompt_edit_accessible_description'), "text_lines": 7},
            # Spacer
            {"type": QWidget, "name": None, "size_policy": (QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum),
             "callback": lambda obj: tab_ai_config_layout.addWidget(obj)},
            # Base response max tokens label
            {"type": QLabel, "name": "settings_dialog_ai_config_base_response_max_tokens_label",
             "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('ai_config_base_response_max_tokens_label'),
             "callback": lambda obj: tab_ai_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop)},
            # Base response max tokens input
            {"type": QSpinBox, "props": {'setMinimum': 1, 'setMaximum': 65536},  # Update the highest range
             "size_policy": (QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred),
             "name": "settings_dialog_ai_config_base_response_max_tokens:ai_config_base_response_max_tokens",
             "callback": lambda obj: tab_ai_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop),
             "accessible_description":
                 self.lexemes.get('ai_config_base_response_max_tokens_input_accessible_description')},
            # Spacer to keep elements above on top
            {"type": QWidget, "name": None, "size_policy": (QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding),
             "callback": lambda obj: tab_ai_config_layout.addWidget(obj)},
        ]

        for conf in fields_conf:
            self.create_setting_field(conf)

        # Close button
        close_button = QPushButton(self.lexemes.get('button_close'))
        close_button.setObjectName('settings_dialog_button_close')
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.connect_widgets()

        # Adjust size policy to allow for dynamic resizing
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.adjustSize()

        # Get the preferred size of the dialog's content
        preferred_size = self.layout().sizeHint()
        # Adjust the dialog's size based on the preferred size then
        if preferred_size.isValid():
            self.resize(preferred_size)

    def apply_props(self, widget, properties):
        for prop, value in properties.items():
            # Get the method based on the property name
            setter = getattr(widget, prop, None)
            if callable(setter):
                setter(value)  # Call the setter with the provided value

    def create_setting_field(self, conf) -> Union[QCheckBox, QLineEdit, QPlainTextEdit, QComboBox, QSpinBox, QSlider]:
        """
        Method to create setting field with ease.
        @param conf: Config of the field. As the param bounded to the particular method it will be called then.
        @return: Any object instance
        """
        args = conf['args'] if 'args' in conf else [self]
        obj = conf['type'](*args)  # type: conf['type']
        # Align with the dialog font size (mostly for QLabel)
        if hasattr(obj, 'sizeHint'):
            """
            # Also possible to set the font directly:
            obj.setFont(self.font())
            """
            obj.sizeHint()
        # Apply methods from props
        if 'props' in conf:
            self.apply_props(obj, conf['props'])
        if 'name' in conf and conf['name']:
            """
            Let's set up object name to make it easier to understand any further callbacks later.
            [ Keep object's name consistent with the corresponding variable in Settings class to link them. ]
            and the var name for convenient reading and in case of refactoring.
            """
            obj.setObjectName(conf['name'])
        if 'text' in conf:
            obj.setText(conf['text'])
        if 'read_only' in conf:
            obj.setReadOnly(conf['read_only'])
        if 'max_length' in conf:
            obj.setMaxLength(conf['max_length'])
        if 'placeholder_text' in conf:
            obj.setPlaceholderText(conf['placeholder_text'])
        if 'accessible_description' in conf:
            obj.setAccessibleDescription(conf['accessible_description'])
        if 'size_policy' in conf:
            params = conf['size_policy']
            if isinstance(params, tuple):
                obj.setSizePolicy(*params)  # Contains a few params
            else:
                obj.setSizePolicy(params)
        if 'alignment' in conf:
            obj.setAlignment(conf['alignment'])
        if 'callback' in conf and callable(conf['callback']):
            conf['callback'](obj)
        if 'style' in conf:
            styles = []
            if 'bold' in conf['style']:
                styles.append('font-weight: bold;')  # Bold
            if 'italic' in conf['style']:
                styles.append('font-style: italic;')  # Italic
            if 'color' in conf['style']:
                styles.append(f"color: {conf['style']['color']};")  # Color
            if styles:
                obj.setStyleSheet('QObject { %s }' % ' '.join(styles))
        if 'text_lines' in conf and isinstance(obj, QPlainTextEdit) and int(conf['text_lines']) > 0:
            font_metrics = obj.fontMetrics()
            # Calculate the height needed for N lines based on font metrics
            lines_height = font_metrics.height() * conf['text_lines']
            obj.setFixedHeight(lines_height)
        # Return created object
        return obj

    def parse_object_name(self, object_name: str):
        if object_name.__contains__(":"):
            object_name_parts = object_name.split(":")
            if len(object_name_parts) == 2:
                # lexeme_key, setting_name
                return object_name_parts
            else:
                if self.logging:
                    self.logger.warning(f"Object name in a wrong format {object_name}")
        else:
            # lexeme_key, setting_name
            return object_name, object_name

    def connect_widgets(self):
        # Find children of type QCheckBox
        checkboxes = self.findChildren(QCheckBox)
        for checkbox in checkboxes:
            if isinstance(checkbox, QCheckBox):
                # Parse object name in case it consists of composed data of lexeme and setting names
                _lexeme_key, setting_name = self.parse_object_name(checkbox.objectName())
                if hasattr(self.settings, setting_name):
                    checkbox.setChecked(getattr(self.settings, setting_name, False))
                # Connect signal after set up defaults or restore saved value to avoid signal emitting right after.
                checkbox.stateChanged.connect(self.save_settings)

        # Find children of type QComboBox
        combo_boxes = self.findChildren(QComboBox)
        for combo_box in combo_boxes:
            if isinstance(combo_box, EnumComboBox):
                # Parse object name in case it consists of composed data of lexeme and setting names
                _lexeme_key, setting_name = self.parse_object_name(combo_box.objectName())
                if hasattr(self.settings, setting_name):
                    setting_value = getattr(self.settings, setting_name, None)
                    # Get the index of the Enum member by the name stored in the settings (e.g. Language's 'EN')
                    index = next((i for i, val in enumerate(combo_box.enum_class) if val.name.lower() == setting_value),
                                 None)
                    if self.debug:
                        self.logger.debug(f'Enum {combo_box.enum_class} index for value: {index} [{setting_value}]')
                    if index is not None:
                        combo_box.setCurrentIndex(index)
                # Connect signal after set up defaults or restore saved value to avoid signal emitting right after.
                combo_box.currentIndexChanged.connect(self.save_settings)

        # Find children of type QSpinBox
        spin_boxes = self.findChildren(QSpinBox)
        for spin_box in spin_boxes:
            if isinstance(spin_box, QSpinBox):
                # Parse object name in case it consists of composed data of lexeme and setting names
                _lexeme_key, setting_name = self.parse_object_name(spin_box.objectName())
                if hasattr(self.settings, setting_name):
                    spin_box.setValue(getattr(self.settings, setting_name, 0))
                spin_box.valueChanged.connect(self.save_settings)

        # Find children of type QLineEdit
        line_edits = self.findChildren(QLineEdit)
        for line_edit in line_edits:
            if isinstance(line_edit, QLineEdit):
                # Parse object name in case it consists of composed data of lexeme and setting names
                _lexeme_key, setting_name = self.parse_object_name(line_edit.objectName())
                if hasattr(self.settings, setting_name):
                    line_edit.setText(str(getattr(self.settings, setting_name, '')))
                # Connect signal after set up defaults or restore saved value to avoid signal emitting right after.
                line_edit.textChanged.connect(self.save_settings)

        # Find children of type QPlainTextEdit
        text_edits = self.findChildren(QPlainTextEdit)
        for text_edit in text_edits:
            if isinstance(text_edit, QPlainTextEdit):
                # Parse object name in case it consists of composed data of lexeme and setting names
                _lexeme_key, setting_name = self.parse_object_name(text_edit.objectName())
                if hasattr(self.settings, setting_name):
                    text_edit.setPlainText(getattr(self.settings, setting_name, ''))
                # Connect signal after set up defaults or restore saved value to avoid signal emitting right after.
                text_edit.textChanged.connect(self.save_settings)

        # Find children of type QSpinBox
        sliders = self.findChildren(QSlider)
        for slider in sliders:
            if isinstance(slider, QSlider):
                # Parse object name in case it consists of composed data of lexeme and setting names
                _lexeme_key, setting_name = self.parse_object_name(slider.objectName())
                if hasattr(self.settings, setting_name):
                    slider.setValue(getattr(self.settings, setting_name, 0))
                slider.valueChanged.connect(self.save_settings)

    def save_settings(self):
        # Signal sender
        sender = self.sender()

        # Determine which widget emitted the signal by the object name set
        sender_widget = self.sender()
        sender_name = sender_widget.objectName()

        # Parse object name in case it consists of composed data of lexeme and setting names
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
        elif isinstance(sender_widget, QLineEdit):
            setting_value = sender_widget.text()
            setting_text = sender_widget.placeholderText()
        elif isinstance(sender_widget, QPlainTextEdit):
            setting_value = sender_widget.toPlainText()
            setting_text = sender_widget.placeholderText()
        elif isinstance(sender_widget, QSlider):
            setting_value = sender_widget.value()
            setting_text = sender_widget.accessibleDescription()

        if self.debug:
            self.logger.debug(f"Saving setting '{setting_name}': {setting_value} ({setting_text})")

        try:
            setattr(self.settings, setting_name, setting_value)
        except AttributeError as e:
            if self.logging:
                self.logger.warning(f'ERROR: {e}')

        if self.debug:
            self.logger.debug(f"Setting new value: {getattr(self.settings, setting_name)}")

        """
        In case of language change try to update as much text labels as possible.
        It may not cover all the labels, but may help with update anyway.
        """
        if setting_name == 'app_language' or sender.objectName().endswith('app_language'):
            # Update lexemes object as app language has just been changed
            self.lexemes = Lexemes(self.settings.app_language, default_scope='settings_dialog')
            # Get all the new lexemes
            app_language_lexemes = self.lexemes.get_all()
            # Update dialog title at first
            self.setWindowTitle(self.lexemes.get('window_title'))
            # Iterate each lexeme's scope to match it with object name to update the text if applicable
            for scope in app_language_lexemes:
                if self.debug:
                    self.logger.debug(f'Lexeme scope to check updates {scope}')
                # Iterate each lexeme from the scope
                for lexeme_key in app_language_lexemes[scope].keys():
                    """
                    Some objects may have name set with ":" delimiter, which means "lexeme_key:setting_name".
                    It may help to transfer more params with object name with ease.
                    """
                    # Parse object name in case it consists of composed data of lexeme and setting names
                    lexeme_key, setting_name = self.parse_object_name(lexeme_key)

                    # Get lexeme in the new language set
                    lexeme = app_language_lexemes[scope][lexeme_key]

                    # Search with regex as the object name should contain scope and may contain setting name as well,
                    # but the lexeme contains a key only.
                    regex = QRegularExpression(f"(?={scope}_)?{lexeme_key}.*?")
                    # self.findChildren() contains only the elements related to this dialog
                    found_objects = self.findChildren(QObject, regex, Qt.FindChildOption.FindChildrenRecursively)
                    if not found_objects:
                        # Try to find it in the parent dialog
                        found_objects = self.parent.findChildren(QObject, regex,
                                                                 Qt.FindChildOption.FindChildrenRecursively)
                        if self.debug and found_objects:
                            self.logger.debug(f"Found object to update (?={scope}_)?{lexeme_key}.*?: {found_objects}")

                    # Search by full object name
                    # object_name = self.lexemes.get_full_key(lexeme_key)
                    # found_objects = self.findChildren(QObject, object_name, Qt.FindChildrenRecursively)

                    for obj in found_objects:
                        if self.debug:
                            self.logger.debug(
                                f'Object for lexeme update: {obj.objectName()} with id: {id(obj)}, lexeme "{lexeme}"')
                        if ((isinstance(obj, (QLabel, QCheckBox, QComboBox, QPushButton)))
                                and hasattr(obj, 'setText')
                                and callable(getattr(obj, 'setText'))):
                            obj.setText(lexeme)
                        if isinstance(obj, QWidget):
                            # Add iterable map of the tabs to change the search by QWidget to explicitly set tab text.
                            self.set_tab_text(obj.objectName(), lexeme)
                        # Exclusions
                        if obj.objectName() == "settings_dialog_general_app_font_size_label":
                            obj.setText(
                                self.lexemes.get('general_app_font_size_label', size=self.settings.app_font_size))

        if setting_name == 'app_theme' or sender.objectName().endswith('app_theme'):
            self.theme_helper = ThemeHelper()
            # Update self styles
            self.setStyleSheet(self.theme_helper.get_css('settings_dialog'))

        if setting_name == 'app_font_size' or sender.objectName().endswith('app_font_size'):
            # Update font from parent as it should be updated and incorporates new font size as well.
            # Simple update of the font size should also work.
            self.setFont(self.parent.font())
            # Find all QLabel objects
            found_objects = self.findChildren(QLabel)
            for obj in found_objects:
                # Align with the dialog font size (mostly for QLabel)
                if hasattr(obj, 'sizeHint'):
                    obj.setFont(self.font())
                if obj.objectName() == "settings_dialog_general_app_font_size_label":
                    """
                    # Update the font weight of the label
                    font = QFont()
                    font.setPointSize(setting_value)
                    app_font_size_label.setFont(font)
                    """
                    obj.setText(self.lexemes.get('general_app_font_size_label', size=setting_value))

    def set_tab_text(self, object_name, text):
        # Iterate through all the tabs
        for index in range(self.tab_widget.count()):
            # Get the widget for the current index
            widget = self.tab_widget.widget(index)

            # Check if this widget matches the object name
            if widget.objectName() == object_name:
                # Set the text
                self.tab_widget.setTabText(index, text)
                break

    def layout_horizontal_spacer(self, layout: QVBoxLayout):
        # Add spacer above the line
        layout.addSpacerItem(QSpacerItem(0, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # Add horizontal delimiter
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

        # Add spacer below the line
        layout.addSpacerItem(QSpacerItem(0, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
