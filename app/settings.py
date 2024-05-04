from PySide6.QtCore import Signal, QSettings

from .app_config import AppConfig
from .enums.themes import Themes
from .enums.languages import Languages
from .enums.ai_model_names import AiModelNames

from typing import Any, Union

import logging


class Settings(QSettings):
    """
    Class to store app settings params.
    """

    value_changed = Signal(object)  # type: Signal[Union[object, QSettings]]

    def __init__(self, parent=None):
        """
        Args:
            parent (optional): Parent object
        """
        super(Settings, self).__init__(parent)

        self.logger = logging.getLogger('settings')

        self.logging = AppConfig.get_logging()
        self.debug = AppConfig.get_debug()

        self.settings = QSettings()

        if self.debug:
            # Attributes may not be set at the very beginning
            self.logger.debug('Window size %d x %d' % (getattr(self, 'ui_width', 0), getattr(self, 'ui_height', 0)))

        self.value_changed.connect(lambda v: self.settings.sync())

        self.init_fields()

    def init_fields(self):
        # App's UI settings
        self.create_property("app_theme", str, str(Themes.default()))
        self.create_property("app_language", str, str(Languages.default()))
        self.create_property("app_font_size", int, AppConfig.get_font_base_size(),
                             set_prev_func=lambda: AppConfig.set_prev_font_size(self.settings.value("app_font_size")))
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
        self.create_property("show_global_cursor_position", bool, False)
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
        self.create_property("ai_config_openai_url", str, "https://api.openai.com/v1/chat/completions")
        self.create_property("ai_config_openai_key", str, "")
        self.create_property("ai_config_openai_model", str, str(AiModelNames.default()))
        self.create_property("ai_config_base_system_prompt", str, "")
        self.create_property("ai_config_base_response_max_tokens", int, 512)

    def create_property(self, param_name: str, param_type: Any, default_value: Any, set_prev_func: Any = None):
        def getter(_self):
            # Type is crucial here
            return param_type(_self.settings.value(param_name, default_value, type=param_type))

        def setter(_self, value):
            if _self.settings.value(param_name) != value:
                if callable(set_prev_func):
                    # Save previous value
                    set_prev_func()
                _self.settings.setValue(param_name, value)
                _self.value_changed.emit({param_name: value})

        # Dynamically create the property and its setter
        setattr(Settings, param_name, property(getter, setter))

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
