from PySide6.QtCore import Signal, QSettings

from .app_config import AppConfig
from .enums.languages import Languages
from .enums.ai_model_names import AiModelNames

from typing import Union

import logging


class Settings(QSettings):
    """
    Class to store app settings params
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
            self.logger.debug('Window size %d x %d' % (self.ui_width, self.ui_height))

        self.value_changed.connect(lambda v: self.settings.sync())

    @property
    def app_theme(self) -> str:
        return self.settings.value("app_theme", "", type=str)  # type: ignore

    @property
    def app_font_size(self) -> int:
        return self.settings.value("app_font_size", AppConfig.get_font_base_size(), type=int)  # type: ignore

    @property
    def ui_width(self) -> int:
        return self.settings.value("ui_width", 0, type=int)  # type: ignore

    @property
    def ui_height(self) -> int:
        return self.settings.value("ui_height", 0, type=int)  # type: ignore

    @property
    def ui_pos_x(self) -> int:
        return self.settings.value("ui_pos_x", 0, type=int)  # type: ignore

    @property
    def ui_pos_y(self) -> int:
        return self.settings.value("ui_pos_y", 0, type=int)  # type: ignore

    @property
    def ui_splitter_pos(self) -> int:
        return self.settings.value("ui_splitter_pos", 0, type=int)  # type: ignore

    @property
    def file_path(self) -> str:
        return self.settings.value("file_path", "", type=str)  # type: ignore

    @property
    def mode(self) -> int:
        return self.settings.value("mode", 0, type=int)  # type: ignore

    @property
    def source(self) -> int:
        return self.settings.value("source", 0, type=int)  # type: ignore

    @property
    def toolbar_icons(self) -> int:
        return self.settings.value("toolbar_icons", None, type=int)  # type: ignore

    @property
    def enc_iterations(self) -> int:
        return self.settings.value("enc_iterations", None, type=int)  # type: ignore

    @property
    def line_num(self) -> int:
        return self.settings.value("line_num", 0, type=int)  # type: ignore

    @property
    def col_num(self) -> int:
        return self.settings.value("col_num", 0, type=int)  # type: ignore

    @property
    def cursor_pos(self) -> int:
        return self.settings.value("cursor_pos", 0, type=int)  # type: ignore

    @property
    def viewport_pos(self) -> list:
        return self.settings.value("viewport_pos", [0, 0], type=list)  # type: ignore

    @property
    def show_deleted_files(self) -> bool:
        return self.settings.value("show_deleted_files", False, type=bool)  # type: ignore

    @property
    def show_line_numbers(self) -> bool:
        # From settings UI dialog
        return self.settings.value("show_line_numbers", True, type=bool)  # type: ignore

    @property
    def app_language(self) -> str:
        # From settings UI dialog
        return self.settings.value("app_language", str(Languages.default()), type=str)  # type: ignore

    @property
    def ai_config_openai_url(self) -> str:
        # From settings UI dialog
        return self.settings.value("ai_config_openai_url", '', type=str)  # type: ignore

    @property
    def ai_config_openai_key(self) -> str:
        # From settings UI dialog
        return self.settings.value("ai_config_openai_key", '', type=str)  # type: ignore

    @property
    def ai_config_openai_model(self) -> str:
        # From settings UI dialog
        return self.settings.value("ai_config_openai_model", str(AiModelNames.default()), type=str)  # type: ignore

    @property
    def ai_config_base_system_prompt(self) -> str:
        # From settings UI dialog
        return self.settings.value("ai_config_base_system_prompt", '', type=str)  # type: ignore

    @property
    def ai_config_base_response_max_tokens(self) -> int:
        # From settings UI dialog
        return self.settings.value("ai_config_base_response_max_tokens", 512, type=int)  # type: ignore

    @property
    def show_global_cursor_position(self) -> bool:
        # From settings UI dialog
        return self.settings.value("show_global_cursor_position", False, type=bool)  # type: ignore

    @property
    def viewer_process_emojis(self) -> bool:
        # From settings UI dialog
        return self.settings.value("viewer_process_emojis", True, type=bool)  # type: ignore

    @property
    def viewer_highlight_todos(self) -> bool:
        # From settings UI dialog
        return self.settings.value("viewer_highlight_todos", True, type=bool)  # type: ignore

    @property
    def viewer_open_link_confirmation(self) -> bool:
        # From settings UI dialog
        return self.settings.value("viewer_open_link_confirmation", True, type=bool)  # type: ignore

    @property
    def show_main_menu(self) -> bool:
        # From settings UI dialog
        return self.settings.value("show_main_menu", False, type=bool)  # type: ignore

    @app_theme.setter
    def app_theme(self, value) -> None:
        self.settings.setValue("app_theme", value)
        self.value_changed.emit({'app_theme': value})

    @app_font_size.setter
    def app_font_size(self, value) -> None:
        # Save previous value for zoom in / zoom out
        AppConfig.set_prev_font_size(self.settings.value("app_font_size"))
        self.settings.setValue("app_font_size", value)
        self.value_changed.emit({'app_font_size': value})

    @ui_width.setter
    def ui_width(self, value) -> None:
        self.settings.setValue("ui_width", value)
        self.value_changed.emit({'ui_width': value})

    @ui_height.setter
    def ui_height(self, value) -> None:
        self.settings.setValue("ui_height", value)
        self.value_changed.emit({'ui_height': value})

    @ui_pos_x.setter
    def ui_pos_x(self, value) -> None:
        self.settings.setValue("ui_pos_x", value)
        self.value_changed.emit({'ui_pos_x': value})

    @ui_pos_y.setter
    def ui_pos_y(self, value) -> None:
        self.settings.setValue("ui_pos_y", value)
        self.value_changed.emit({'ui_pos_y': value})

    @ui_splitter_pos.setter
    def ui_splitter_pos(self, value) -> None:
        self.settings.setValue("ui_splitter_pos", value)
        self.value_changed.emit({'ui_splitter_pos': value})

    @file_path.setter
    def file_path(self, value) -> None:
        self.settings.setValue("file_path", value)
        self.value_changed.emit({'file_path': value})

    @mode.setter
    def mode(self, value) -> None:
        self.settings.setValue("mode", value)
        self.value_changed.emit({'mode': value})

    @source.setter
    def source(self, value) -> None:
        self.settings.setValue("source", value)
        self.value_changed.emit({'source': value})

    @toolbar_icons.setter
    def toolbar_icons(self, value) -> None:
        """
        Can be checked like:
        if value is not None and value.isValid() and isinstance(value.toInt()[0], int): ...
        """
        self.settings.setValue("toolbar_icons", value)
        self.value_changed.emit({'toolbar_icons': value})

    @enc_iterations.setter
    def enc_iterations(self, value) -> None:
        self.settings.setValue("enc_iterations", value)
        self.value_changed.emit({'enc_iterations': value})

    @line_num.setter
    def line_num(self, value) -> None:
        self.settings.setValue("line_num", value)
        self.value_changed.emit({'line_num': value})

    @col_num.setter
    def col_num(self, value) -> None:
        self.settings.setValue("col_num", value)
        self.value_changed.emit({'col_num': value})

    @cursor_pos.setter
    def cursor_pos(self, value) -> None:
        self.settings.setValue("cursor_pos", value)
        self.value_changed.emit({'cursor_pos': value})

    @viewport_pos.setter
    def viewport_pos(self, value) -> None:
        self.settings.setValue("viewport_pos", value)
        self.value_changed.emit({'viewport_pos': value})

    @show_deleted_files.setter
    def show_deleted_files(self, value) -> None:
        self.settings.setValue("show_deleted_files", value)
        self.value_changed.emit({'show_deleted_files': value})

    @show_line_numbers.setter
    def show_line_numbers(self, value) -> None:
        self.settings.setValue("show_line_numbers", value)
        self.value_changed.emit({'show_line_numbers': value})

    @app_language.setter
    def app_language(self, value) -> None:
        self.settings.setValue("app_language", value)
        self.value_changed.emit({'app_language': value})

    @ai_config_openai_url.setter
    def ai_config_openai_url(self, value) -> None:
        self.settings.setValue("ai_config_openai_url", value)
        self.value_changed.emit({'ai_config_openai_url': value})

    @ai_config_openai_key.setter
    def ai_config_openai_key(self, value) -> None:
        self.settings.setValue("ai_config_openai_key", value)
        self.value_changed.emit({'ai_config_openai_key': value})

    @ai_config_openai_model.setter
    def ai_config_openai_model(self, value) -> None:
        self.settings.setValue("ai_config_openai_model", value)
        self.value_changed.emit({'ai_config_openai_model': value})

    @ai_config_base_system_prompt.setter
    def ai_config_base_system_prompt(self, value) -> None:
        self.settings.setValue("ai_config_base_system_prompt", value)
        self.value_changed.emit({'ai_config_base_system_prompt': value})

    @ai_config_base_response_max_tokens.setter
    def ai_config_base_response_max_tokens(self, value) -> None:
        self.settings.setValue("ai_config_base_response_max_tokens", value)
        self.value_changed.emit({'ai_config_base_response_max_tokens': value})

    @show_global_cursor_position.setter
    def show_global_cursor_position(self, value) -> None:
        self.settings.setValue("show_global_cursor_position", value)
        self.value_changed.emit({'show_global_cursor_position': value})

    @viewer_process_emojis.setter
    def viewer_process_emojis(self, value) -> None:
        self.settings.setValue("viewer_process_emojis", value)
        self.value_changed.emit({'viewer_process_emojis': value})

    @viewer_highlight_todos.setter
    def viewer_highlight_todos(self, value) -> None:
        self.settings.setValue("viewer_highlight_todos", value)
        self.value_changed.emit({'viewer_highlight_todos': value})

    @viewer_open_link_confirmation.setter
    def viewer_open_link_confirmation(self, value) -> None:
        self.settings.setValue("viewer_open_link_confirmation", value)
        self.value_changed.emit({'viewer_open_link_confirmation': value})

    @show_main_menu.setter
    def show_main_menu(self, value) -> None:
        self.settings.setValue("show_main_menu", value)
        self.value_changed.emit({'show_main_menu': value})
