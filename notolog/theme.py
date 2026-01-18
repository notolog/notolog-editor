"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: App themes manager.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

import os
import logging

from typing import Union

from PySide6.QtCore import QFile, QIODevice

from .app_config import AppConfig
from .helpers import file_helper
from .enums.themes import Themes


class Theme:

    ASSETS_DIR_NAME = "assets"

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None or AppConfig().get_test_mode():  # No cache in test mode
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, theme: str = None):
        # Load exact theme once
        if getattr(self, 'theme', None) and self.theme == theme:
            return

        self.logger = logging.getLogger('theme')

        # Custom Enum logic return name.lower() when cast to string
        # Same as: Themes.default().name.lower()
        self.default_theme = str(Themes.default())

        if not theme or theme in ('.', '..'):  # in case of file dependant
            theme = self.default_theme

        self.theme = theme

        # Can be seen in logs a few times as the already initialised object could be requested from anywhere.
        self.logger.info(f"Themes helper is activated and set to the theme: '{self.theme}'")

        self.colors = None
        self.css = None

        self.load_from_files()

    @staticmethod
    def get_assets_dir(join_parts: Union[str, list] = None) -> str:
        """
        Get the directory path with all assets files.
        @return: string with the themes directory path
        """
        join_parts = join_parts if isinstance(join_parts, list) else [join_parts] if isinstance(join_parts, str) else []
        return str(os.path.join(os.path.dirname(__file__), Theme.ASSETS_DIR_NAME, *join_parts))

    def get_themes_dir(self):
        """
        Get the directory path with themes files relative to this file.
        @return: string with the themes directory path
        """
        return self.get_assets_dir('themes')

    def get_theme_dir(self):
        """
        Get current theme directory.
        @return:
        """
        return os.path.join(self.get_themes_dir(), self.theme)

    def get_default_theme_dir(self):
        """
        Get current theme directory.
        @return:
        """
        return os.path.join(self.get_themes_dir(), self.default_theme)

    def load_from_files(self) -> None:
        # Init the vars
        self.colors = {}
        self.css = {}

        # Get current theme directory
        theme_dir = self.get_theme_dir()

        theme_files = []
        if os.path.isdir(theme_dir):
            theme_file_names = os.listdir(theme_dir)
            theme_file_paths = [os.path.join(theme_dir, _file_name) for _file_name in theme_file_names]
            for theme_file_path in theme_file_paths:
                if os.path.isfile(theme_file_path):
                    theme_files.append(theme_file_path)

        for file_path in theme_files:
            # Process css file
            if file_path.endswith('.css'):
                if self.theme not in self.css:
                    self.css[self.theme] = {}
                if os.path.isfile(file_path):
                    css_name = os.path.splitext(os.path.basename(file_path))[0]
                    self.css[self.theme].update({css_name: file_path})
                continue

            # Process colors file
            if not file_path.endswith('.ini'):
                continue

            if self.theme not in self.colors:
                self.colors[self.theme] = {}
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    # Remove leading/trailing whitespace
                    line = line.strip()
                    # Skip empty lines
                    if line:
                        parts = line.split('=')
                        if len(parts) == 2:
                            color_name = parts[0].strip()
                            color_value = parts[1].strip()
                            self.colors[self.theme][color_name] = color_value
                        else:
                            self.logger.debug(f"Ignoring not valid color line: {line}")

    def set_theme(self, theme: str) -> None:
        """
        Set theme and re-load all corresponded colors.
        @param theme: string key of the theme to load
        @return: None
        """
        self.theme = theme
        self.load_from_files()

    def get_colors(self, css_format: bool = False) -> Union[dict, None]:
        """
        Get the theme colors in a form of a dictionary.
        @param css_format: bool whether to convert to CSS format or not
        @return: dictionary with the theme colors
        """
        hex_colors_str = self.colors.get(self.theme, {}).items()
        if not hex_colors_str:
            return None
        hex_colors = {key: (int(value, 16) if value.startswith('0x') else value) for key, value in hex_colors_str}
        if css_format:
            # Convert each item value to CSS format (#RRGGBB)
            return dict({key: "#{:06x}".format(value).upper() for key, value in hex_colors})
        return dict(hex_colors)

    def get_css(self) -> Union[dict, None]:
        """
        Get the theme css in a form of a dictionary.
        @return: dictionary with the theme css
        """
        return self.css.get(self.theme, {})

    def load_css(self, path: str) -> Union[str, None]:
        """
        Load CSS file and return result as a string.
        QTextEdit implementation
        """
        file_path = QFile(file_helper.res_path(path))
        if not file_path.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
            return None
        # with open(file_path, 'r', encoding='utf-8') as file:
        #    css_content = file.read()
        return file_path.readAll().data().decode("utf-8")
