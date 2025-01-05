"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Enum class for the app's supported fonts.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2025 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

import os

from .enum_base import EnumBase

assert hasattr(EnumBase, 'default'), "Check default() method is implemented in the base class"


class Fonts(EnumBase):
    NOTO_SANS = (os.path.join('NotoSans', 'NotoSans-Regular.ttf'), 'Noto Sans', False, True)
    IBM_PLEX_MONO = (os.path.join('IBMPlexMono', 'IBMPlexMono-Regular.ttf'), 'IBM Plex Mono', True)

    def __init__(self, path, display_name, is_monospace, is_default=False, *args, **kwargs):
        super().__init__(path, is_default=is_default, *args, **kwargs)

        self._display_name = display_name
        self._is_monospace = is_monospace

    @property
    def path(self):
        # Get the font file path.
        return self.value

    @property
    def display_name(self):
        # Get the display name of the font.
        return self._display_name

    @property
    def is_monospace(self):
        # Check if the font is monospace.
        return self._is_monospace

    @staticmethod
    def get_by_name(name):
        # Retrieve a font by its display name.
        for font in Fonts:
            if font.display_name == name:
                return font
        return None

    @staticmethod
    def get_all_monospace():
        # Retrieve all monospace fonts.
        return [font for font in Fonts if font.is_monospace]
