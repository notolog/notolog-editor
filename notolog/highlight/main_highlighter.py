"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Base Syntax Highlighter class tailored for Notolog.
- Functionality: This module contains shared functionality for subclasses like the MdHighlighter.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2025 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QTextDocument, QSyntaxHighlighter, QTextCharFormat
from PySide6.QtGui import QColor, QBrush, QFont

from typing import TYPE_CHECKING

from . import AppConfig
from . import ThemeHelper

from ..font_loader import FontLoader

import logging

if TYPE_CHECKING:
    from typing import Union  # noqa: F401
    from . import TextBlockData  # noqa: F401
    from PySide6.QtGui import QTextBlock, QTextBlockUserData  # noqa: F401


class MainHighlighter(QSyntaxHighlighter):
    """
    Syntax highlighter class
    """

    theme = {}
    # Keep it consistent with ini-file name, say 'main.ini', item prefix 'main_color_h1_text'
    theme_ini_prefix = 'main'

    """
    Elements order is matter!
    Say, i* first, b** second, bi*** third one-by-one to override prev token.
        i_, b__, bi___
        code `...`, code ```...```

    nth 0 is a whole string
    nth > 1 calculates as: start = end - length
    """
    re_rules = []

    def __init__(self, document: QTextDocument = None):
        super().__init__(document)

        self.logger = logging.getLogger('highlighter')

        # Get app's global font size
        self.font_size = AppConfig().get_font_size()

        # Walk rules to create QRegExp for each pattern
        self.rules = [(self.get_regex(pattern), nth, tag, group, duple, fmt, reckon)
                      for (pattern, nth, tag, group, duple, fmt, reckon) in self.re_rules]

        # Collect found tokens
        self.tokens = {}
        # Tokens which belong the same line
        self.line_tokens = {}

        # For debug purposes
        self.line_number = None
        self.line_number_log = None

        # Whether a group formatted or not
        self.formatted_group = {}

        # Indicate that the process is a re-highlighting process
        self.rehighlight_block = None

        self.current_block = None  # type: Union[QTextBlock, None]
        self.prev_block = None  # type: Union[QTextBlock, None]

        self.user_data = None  # type: Union[TextBlockData, QTextBlockUserData, None]
        self.prev_user_data = None  # type: Union[TextBlockData, QTextBlockUserData, None]

        self.theme_helper = ThemeHelper()

        self.override_colors()

    def __init_subclass__(cls):
        # Check the required methods are implemented
        if not hasattr(cls, 'highlightBlock'):
            raise NotImplementedError(f'Method highlightBlock() have to be implemented in subclass {cls.__name__}.')

    def override_colors(self):
        """
        Proof-of-concept method for overriding the colors applied to the highlighter's syntax.
        Consider replacing the entire style map, such as with background patterns.
        """
        for item in self.theme:
            # Retrieve color values from the theme helper.
            # Example: 'md_color_h1_text', where 'md' is the theme prefix and 'h1_text' is the item.
            _color = self.theme_helper.get_color(f'{self.theme_ini_prefix}_color_{item}', css_format=True)
            _alt_color = self.theme_helper.get_color(f'{self.theme_ini_prefix}_alt_color_{item}', css_format=True)
            _background_color = self.theme_helper.get_color(f'{self.theme_ini_prefix}_background_color_{item}')
            _background_color_inner = self.theme_helper.get_color(
                f'{self.theme_ini_prefix}_background_color_{item}_inner')
            self.logger.debug(
                f"Prefix[{self.theme_ini_prefix}] '{item}', color: '{_color}', bg color: '{_background_color}'")
            # Currently, all colors are set as strings, such as 'red', 'darkCyan', etc.
            if _color and isinstance(_color, str):
                # Set up the color regardless of whether it was already configured
                self.theme[item]['color'] = _color
            # Alt color refers to the underline or strikethrough line color, formatted the same as 'color'
            if _alt_color and isinstance(_alt_color, str):
                # Set up the alt color regardless of whether it was already configured
                self.theme[item]['alt_color'] = _alt_color
            # Background override
            if _background_color and isinstance(_background_color, str):
                if 'bg' in self.theme[item]:
                    if 'color' in self.theme[item]['bg']:
                        self.theme[item]['bg']['color'] = _background_color
                    elif isinstance(self.theme[item]['bg'], str):
                        self.theme[item]['bg'] = _background_color
                else:
                    # Set up the background color regardless of whether it was already configured
                    self.theme[item]['bg'] = _background_color
            # Inner color applied to elements nested within another, such as italic text in a blockquote
            if _background_color_inner and isinstance(_background_color_inner, str):
                if 'bg_inner' in self.theme[item]:
                    if 'color' in self.theme[item]['bg_inner']:
                        self.theme[item]['bg_inner']['color'] = _background_color_inner
                    elif isinstance(self.theme[item]['bg_inner'], str):
                        self.theme[item]['bg_inner'] = _background_color_inner

    def get_regex(self, pattern) -> QRegularExpression:
        """
        Get either QRegularExpression or regular Python re
        """
        return QRegularExpression(pattern)

    #
    # Text block style format
    #
    # @staticmethod
    def cf(self, **kwargs):  # noqa: C901
        """
        Return a QTextCharFormat with style attributes

        Example of color names:
        https://doc.qt.io/qt-6/qcolor.html#predefined-colors
        """

        color = kwargs['color'] if 'color' in kwargs else ''
        alt_color = kwargs['alt_color'] if 'alt_color' in kwargs else ''
        style = kwargs['style'] if 'style' in kwargs else ''
        bg = kwargs['bg'] if 'bg' in kwargs else {}
        font_size_ratio = kwargs['font_size_ratio'] if 'font_size_ratio' in kwargs else 1.0

        if not (color or alt_color or style or bg or font_size_ratio):
            return

        cformat = QTextCharFormat()

        # Foreground
        if color:
            color_obj = QColor(color)
            cformat.setForeground(color_obj)

        # Background
        if bg:
            bg_color = None  # type: Union[str, None]
            """
            Qt::BrushStyle https://doc.qt.io/qt-6/qt.html#BrushStyle-enum
            """
            bg_pattern = Qt.BrushStyle.SolidPattern
            if type(bg) is str:
                bg_color = bg  # type: ignore
            elif type(bg) is dict:
                if 'color' in bg:
                    bg_color = bg['color']
                if 'pattern' in bg and bg['pattern'] in Qt.BrushStyle:
                    bg_pattern = bg['pattern']
            # Color required
            if bg_color is not None:
                bg_color_obj = QColor(bg_color)
                """
                https://doc.qt.io/qt-6/qbrush.html
                """
                cformat.setBackground(QBrush(bg_color_obj, bg_pattern))

        if 'bold' in style:
            cformat.setFontWeight(QFont.Weight.Bold)
        if 'italic' in style:
            cformat.setFontItalic(True)
        if 'underline' in style:
            cformat.setFontUnderline(True)
            if alt_color:
                cformat.setUnderlineColor(QColor(alt_color))
        if 'strikethrough' in style:
            cformat.setFontStrikeOut(True)
            if alt_color:
                cformat.setUnderlineColor(QColor(alt_color))
        if 'monospace' in style:
            if loaded_monospace_font := FontLoader.get_monospace_font():
                monospace_font = QFont(loaded_monospace_font)
                monospace_font.setStyleHint(QFont.StyleHint.Monospace)
                # 100% means normal spacing, no extra spacing
                monospace_font.setLetterSpacing(QFont.SpacingType.PercentageSpacing, 100)
                cformat.setFont(monospace_font)

        # Explicitly set the font size after any potential font style changes
        if font_size_ratio and self.font_size:
            # The actual size is determined based on the base size set in the constructor
            cformat.setFontPointSize(int(self.font_size * font_size_ratio))

        return cformat

    def rehighlightBlock(self, block):
        self.logger.debug('Re-highlighting block data')

        # Leave as default
        self.rehighlight_block = True

        # Initial values
        self.tokens = {}
        self.line_tokens = {}
        self.line_number = None

        super().rehighlightBlock(block)

    def rehighlight(self):
        self.logger.debug('Re-highlighting the whole document')

        self.rehighlight_block = False

        # Initial values
        self.tokens = {}
        self.line_tokens = {}
        self.line_number = None

        super().rehighlight()

        self.rehighlight_block = True

    def get_open_close_token_map(self):
        return []

    def get_nl_closing_tokens(self):
        return []

    def highlightBlock(self, text_str):
        """
        Apply a syntax highlighting to each line of the text.
        https://doc.qt.io/qt-6/qsyntaxhighlighter.html#highlightBlock
        """
        pass

    def get_opened_group_token(self, group):
        for token_data in self.get_open_close_token_map():
            if (group == token_data['group']
                    and token_data['open'] in self.tokens
                    and self.tokens[token_data['open']]['o'] is True):
                return token_data['open']
        return None

    def is_any_formatted(self):
        return True if self.formatted_group else False

    def is_group_formatted(self, group):
        return True if group in self.formatted_group else False

    def set_formatted(self, group):
        # token group
        if group in self.formatted_group:
            self.formatted_group[group] += 1
        else:
            self.formatted_group[group] = 1

    def clear_formatted(self):
        self.formatted_group = {}
