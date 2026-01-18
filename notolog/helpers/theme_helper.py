"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Themes helper class.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import Qt
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtGui import QColor, QIcon, QPixmap, QPainter

import os
import logging

from typing import Union

from ..settings import Settings
from ..theme import Theme
from ..enums.themes import Themes


class ThemeHelper:
    """
    This class is intended to help with theme assets (colors, icons, etc.)
    """

    def __init__(self):
        super().__init__()

        self.logger = logging.getLogger('theme_helper')

        self.logger.debug('Theme helper is activated')

        self.settings = Settings()

        theme_name = self.settings.app_theme
        # Check the theme is still in the themes list with fallback to the default one
        if theme_name not in [_theme.name.lower() for _theme in Themes]:  # Or: list(Themes.__members__.keys()):
            theme_name = str(Themes.default())

        self.theme = Theme(theme=theme_name)

    def get_app_icon_path(self):
        return self.theme.get_assets_dir('notolog-logo.png')

    def get_color(self, color_name: str, css_format: bool = False) -> Union[int, str, None]:
        """
        Get a particular theme color by its name.
        @param color_name: string the color name
        @param css_format: bool whether to convert to CSS format or not. Works with hex colors.
        @return: the color value
        """

        """
        It's possible to pass css_format param but all colors will be converted in this case.
        It can be too resource greedy if cache is in use.

        The colors have already been converted to int(color, 16) format.
        """
        theme_colors = self.theme.get_colors()
        if not theme_colors:
            return None
        color = theme_colors.get(color_name)\
            if color_name in theme_colors else None  # theme_colors.get('color_default')

        if color is None:
            self.logger.debug(f"Skip not set color '{color_name}', theme '{self.theme.theme}'")
            return None

        if isinstance(color, int):
            # Hex color format
            if color and css_format:
                # Convert to CSS format (#RRGGBB)
                return "#{:06x}".format(color).upper()
            return color

        # String color format
        return color

    def get_css(self, css_name=str) -> Union[str, None]:
        """
        Get CSS file content by its name.
        @param css_name: the name
        @return: string of the CSS file content
        """
        theme_css = self.theme.get_css()
        css_file = theme_css.get(css_name) if theme_css else None
        if css_file and os.path.isfile(css_file):
            # Load CSS-file and return its content
            return self.theme.load_css(css_file)
        return None

    def get_icon(self, theme_icon: str, system_icon: str = None, color: QColor = None,
                 # Can be adjusted independently
                 width: int = 64, height: int = 64) -> QIcon:
        """
        Get QIcon by params

        Args:
            theme_icon (str): Theme icon file name
            system_icon (str, optional): System icon name as a fallback
            color (QColor, optional): Color of the SVG icon
            width (int, optional): Icon width
            height (int, optional): Icon height

        Returns:
            QIcon: Either from file or from the system theme
        """
        theme_icon_dir = os.path.join(self.theme.get_theme_dir(), 'icons')
        if not os.path.exists(theme_icon_dir):
            # Get default icons then
            theme_icon_dir = os.path.join(self.theme.get_default_theme_dir(), 'icons')
        theme_icon_path = os.path.join(theme_icon_dir, theme_icon)
        if os.path.isfile(theme_icon_path):
            if not color:
                default_icon_color = self.get_color('toolbar_icon_color_default')
                color = QColor(default_icon_color)
                self.logger.debug('Applying default color fallback "#%x"' % default_icon_color)
            return QIcon(self.svg_to_pixmap(svg_filepath=theme_icon_path, color=color, width=width, height=height))
        else:
            # With a fallback: QIcon.fromTheme(system_icon, QIcon(theme_icon))
            return QIcon.fromTheme(system_icon)

    def svg_to_pixmap(self, svg_filepath: str, color: QColor, width: int = 64, height: int = 64) -> QPixmap:
        """
        Helps to load an SVG file and convert it to QPixmap

        Args:
            svg_filepath (str): SVG file path
            color (QColor): Color of the SVG icon
            width (int, optional): Width of the icon. Defaults to 64.
            height (int, optional): Height of the icon. Defaults to 64.

        Returns:
            QPixmap: Pixmap data
        """
        renderer = QSvgRenderer(svg_filepath)
        pixmap = QPixmap(width, height)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        # Render destination image
        renderer.render(painter)
        """
        The output is the source, where the alpha is reduced by that of the destination

        More about QPainter.CompositionMode
        * https://doc.qt.io/qt-6/qpainter.html#CompositionMode-enum
        """
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        # Fill source image with color
        painter.fillRect(pixmap.rect(), color)
        painter.end()
        return pixmap
