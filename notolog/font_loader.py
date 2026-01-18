"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: App font loader.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtGui import QFontDatabase, QFont

from .theme import Theme
from .enums.fonts import Fonts

import logging


class FontLoader:
    _loaded_fonts = {}

    logger = logging.getLogger("font_loader")

    @staticmethod
    def load_font(font_enum: Fonts):
        """
        Load a font lazily using the Fonts enum.

        Args:
            font_enum (Fonts): The Fonts enum member representing the font.

        Returns:
            str: The font family name if successfully loaded.

        Raises:
            RuntimeError: If the font cannot be loaded.
        """

        if font_enum not in FontLoader._loaded_fonts:
            # Construct the font path using the assets directory
            font_path = Theme.get_assets_dir(['fonts', font_enum.value])
            font_id = QFontDatabase.addApplicationFont(font_path)

            if font_id != -1:
                font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
                FontLoader._loaded_fonts[font_enum] = font_family
                FontLoader.logger.debug(f"Successfully loaded font: {font_family}")
                return font_family
            else:
                FontLoader.logger.warning(f"Failed to load font: {font_path}")
                raise RuntimeError(f"Failed to load font: {font_path}")
        return FontLoader._loaded_fonts[font_enum]

    @staticmethod
    def get_font_by_name(name: str):
        """
        Retrieve the loaded font by its name.

        Args:
            name (str): The display name of the font (e.g., "Noto Sans").

        Returns:
            str: The font family name if loaded successfully.

        Raises:
            ValueError: If the font is not found in the Fonts enum.
        """
        font_enum = Fonts.get_by_name(name)
        if not font_enum:
            raise ValueError(f"Font with name '{name}' not found.")
        return FontLoader.load_font(font_enum)

    @staticmethod
    def get_all_monospace_fonts():
        """
        Retrieve all monospace fonts.

        Returns:
            list: A list of font family names for all loaded monospace fonts.
        """
        monospace_fonts = Fonts.get_all_monospace()
        return [FontLoader.load_font(font) for font in monospace_fonts]

    @staticmethod
    def get_monospace_font():
        """
        Retrieve the first loaded monospace font.

        Returns:
            str: The font family name of the first monospace font.

        Raises:
            RuntimeError: If no monospace fonts are available.
        """
        monospace_fonts = FontLoader.get_all_monospace_fonts()
        if not monospace_fonts:
            FontLoader.logger.warning("No monospace fonts available.")
        return monospace_fonts[0]

    @staticmethod
    def init_fonts(app):
        """
        Initialize and load application fonts.

        This method iterates through the Fonts enumeration, attempts to load each font,
        and sets the default application font if specified in the enumeration.

        Args:
            app (QApplication): The QApplication instance where the fonts will be applied.
        """
        for font in Fonts:
            try:
                # Load the font if not yet loaded
                font_family = FontLoader.load_font(font)
                if font.is_default and hasattr(app, 'setFont'):
                    font = QFont(font_family)
                    # Prefer no hinting to preserve the font's original design, if supported
                    font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)
                    app.setFont(font)
                    FontLoader.logger.info(f"Set default application font: '{font_family}'")
            except ValueError as e:
                FontLoader.logger.warning(f"Font not found: {font} ({str(e)})")
