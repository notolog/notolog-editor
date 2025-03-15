"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Settings functionality.
- Functionality: Allows adding new setting elements via the config map and handling settings change signals.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2025 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import Signal, QSettings

from .app_config import AppConfig
from .enums.themes import Themes
from .enums.languages import Languages
from .helpers.settings_helper import SettingsHelper
from .helpers import file_helper

from typing import TYPE_CHECKING, Any
from threading import Lock

import os
import logging

if TYPE_CHECKING:
    from typing import Union  # noqa: F401


class Settings(QSettings):
    """
    Class to store app settings params.
    """

    value_changed = Signal(object)  # type: Signal[Union[object, QSettings]]

    _instance = None  # Singleton instance
    _lock = Lock()

    ai_config_inference_modules: dict = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    # Create the instance if it doesn't exist
                    cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def reload(cls, *args, **kwargs):
        """
        Reinitialize the singleton instance. This method allows for the controlled
        re-creation of the singleton instance.
        """
        with cls._lock:
            # Create a new instance
            cls._instance = super().__new__(cls)

    def __init__(self, parent=None):
        """
        Args:
            parent (optional): Parent object
        """

        # Prevent re-initialization if the instance is already set up.
        if hasattr(self, 'settings'):
            return

        # Use a lock to ensure initialization is thread-safe and atomic.
        with self._lock:
            # Double-check to prevent race conditions during initialization.
            if hasattr(self, 'settings'):
                return

            super(Settings, self).__init__(parent)

            self.logger = logging.getLogger('settings')

            self.settings = self.get_instance()
            self.settings_helper = SettingsHelper()

            # Attributes may not be set at the very beginning
            self.logger.debug('Window size %d x %d' % (getattr(self, 'ui_width', 0), getattr(self, 'ui_height', 0)))

            self.value_changed.connect(lambda v: self.settings.sync())

            self.protected_attr = []
            self.init_fields()

    def get_instance(self):
        settings_file_path = self.get_filename()
        # Check file permissions
        if not file_helper.is_writable_path(settings_file_path):
            self.logger.warning(f"Permission denied: Cannot write to the file {settings_file_path}")
            settings_file_path = None
        # Initialize settings with either a custom or the default path
        if settings_file_path:
            return QSettings(settings_file_path, QSettings.Format.NativeFormat)
        else:
            return QSettings()

    def get_filename(self):
        # Get app's package
        app_package = AppConfig().get_package_type()
        # Get default path based on the application config
        settings_file_path = self.fileName()
        # Adjust path if the specific package is in use
        if app_package != AppConfig.default_package:
            # Split the file path into directory, filename without extension, and extension
            directory, file = os.path.split(settings_file_path)
            _file_name, _file_ext = os.path.splitext(file)
            settings_file_path = os.path.join(directory, f'{_file_name}_{app_package}{_file_ext}')
        return settings_file_path

    def init_fields(self):
        # App's UI settings
        self.create_property("app_theme", str, str(Themes.default()))
        self.create_property("app_language", str, str(Languages.default()))
        self.create_property("app_font_size", int, AppConfig().get_font_base_size(),
                             set_prev_func=lambda prev_value: AppConfig().set_prev_font_size(prev_value))
        # Window positioning and size
        self.create_property("ui_width", int, 0)
        self.create_property("ui_height", int, 0)
        self.create_property("ui_pos_x", int, 0)
        self.create_property("ui_pos_y", int, 0)
        # Splitter between navigation tree and view/edit widget position
        self.create_property("ui_splitter_pos", int, 0)
        # Global settings
        self.create_property("show_main_menu", bool, True)
        self.create_property("show_deleted_files", bool, False)
        self.create_property("show_navigation_arrows", bool, True)
        self.create_property("show_global_cursor_position", bool, False)
        self.create_property("default_path", str, "")
        self.create_property("ui_init_ts", int, 0)
        # Editor state
        self.create_property("file_path", str, "")
        self.create_property("mode", int, 0)
        self.create_property("source", int, 0)
        self.create_property("line_num", int, 0)
        self.create_property("col_num", int, 0)
        self.create_property("cursor_pos", int, 0)
        self.create_property("viewport_pos", list, [0, 0])  # Scroll doc to this position
        self.create_property("show_line_numbers", bool, True)
        # Viewer state
        self.create_property("viewer_process_emojis", bool, True)
        self.create_property("viewer_highlight_todos", bool, True)
        self.create_property("viewer_open_link_confirmation", bool, True)
        self.create_property("viewer_save_resources", bool, True)
        # Icons to show on the toolbar. Can be checked like:
        # if value is not None and value.isValid() and isinstance(value.toInt()[0], int): ...
        self.create_property("toolbar_icons", int, None)
        self.create_property("enc_iterations", int, None)
        # AI assistant
        self.create_property("ai_config_inference_module", str, "openai_api")
        self.create_property("ai_config_multi_turn_dialogue", bool, True)
        self.create_property("ai_config_convert_to_md", bool, False)

    def create_property(self, param_name: str, param_type: Any, default_value: Any, set_prev_func: Any = None,
                        encrypt: bool = False):
        def getter(_self):
            # Type is crucial here
            value = _self.settings.value(param_name, default_value, type=param_type)
            if encrypt:
                try:
                    value = self.settings_helper.decrypt_data(value)
                except (ValueError, EnvironmentError) as e:
                    self.logger.warning(f'Settings protected parameter "{param_name}" getting error: {e}')
            return param_type(value)

        def setter(_self, value):
            _prev_value = _self.settings.value(param_name)
            if _prev_value != value:
                if callable(set_prev_func):
                    # Save previous value
                    set_prev_func(_prev_value)
                if encrypt:
                    try:
                        value = self.settings_helper.encrypt_data(value)
                    except (ValueError, EnvironmentError) as e:
                        self.logger.warning(f'Settings protected parameter "{param_name}" setting error: {e}')
                _self.settings.setValue(param_name, value)
                _self.value_changed.emit({param_name: value})

        # Dynamically create the property and its setter
        setattr(Settings, param_name, property(getter, setter))

        # Add param to the protected list if applicable
        if encrypt:
            self.protected_attr.append(param_name)

    """
    Example of how to set up for each settings property
    """

    @property
    def show_main_menu(self) -> bool:
        # From settings UI dialog
        return self.settings.value("show_main_menu", True, type=bool)  # type: ignore

    @show_main_menu.setter
    def show_main_menu(self, value) -> None:
        self.settings.setValue("show_main_menu", value)
        self.value_changed.emit({'show_main_menu': value})

    def __getattr__(self, name: str) -> Any:
        """
        Handle attribute access dynamically. Helps to avoid undefined attribute error highlighting within IDE.

        When an AttributeError is raised during attribute access, the __getattr__ method is invoked to handle the
        attribute access dynamically. In your case, after the AttributeError is raised and caught by __getattr__,
        the getter() function is invoked as part of the dynamic attribute access.

        Here's how it works:
        1. The code attempts to access an attribute, such as settings.app_font_size.
        2. If the attribute is not found in the object's namespace, Python raises an AttributeError.
        3. The __getattr__ method intercepts the AttributeError and handles it by providing a custom behavior.
           In this case, it raises another AttributeError with a descriptive message.
        4. After the __getattr__ method completes its execution, the original attribute access attempt is retried.
        5. Since the attribute access is retried, Python again tries to access settings.app_font_size.
        6. This time, the attribute settings.app_font_size exists because it was dynamically created using the
           create_property method.
        7. The getter() function associated with the dynamically created property is invoked to retrieve the value of
           app_font_size
        """
        if name in self.__dict__:
            return self.__dict__[name]
        else:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def clear(self):
        # Clear all entries in the QSettings instance to reset settings
        self.settings.clear()

        # Delete the settings file
        settings_file_path = self.get_filename()
        # Check if file exists and is writable
        if os.path.exists(settings_file_path) and os.access(settings_file_path, os.W_OK):
            try:
                os.remove(settings_file_path)
                return True
            except OSError as e:
                self.logger.warning(f"Error deleting settings file {settings_file_path}: {e}")
                return False
        else:
            self.logger.warning(f"Settings file does not exist or is not writable: {settings_file_path}")
            return False
