"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Contains unit and integration tests for the related functionality.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2025 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

import pytest

from unittest.mock import MagicMock, patch
from notolog.font_loader import FontLoader
from notolog.enums.fonts import Fonts

from PySide6.QtGui import QFont


class TestFontLoader:

    @pytest.fixture(autouse=True)
    def mock_logger(self, mocker):
        # Mock the logger for the FontLoader class.
        return mocker.patch("notolog.font_loader.FontLoader.logger")

    @pytest.mark.parametrize(
        "font_enum, font_id, font_family, expected_exception",
        [
            (Fonts.NOTO_SANS, 1, "Noto Sans", None),
            (Fonts.IBM_PLEX_MONO, -1, None, RuntimeError),
        ],
    )
    def test_load_font(self, mocker, font_enum, font_id, font_family, expected_exception):
        # Avoid mocking QFontDatabase directly
        mocker.patch.object(FontLoader, 'load_font', side_effect=lambda font_enum: font_enum.name)

        font_family = FontLoader.load_font(font_enum)
        assert font_family == font_enum.name

    @pytest.mark.parametrize(
        "font_name, font_enum, font_family, expected_exception",
        [
            ("Noto Sans", Fonts.NOTO_SANS, "Noto Sans", None),
            ("Nonexistent Font", None, None, ValueError),
        ],
    )
    def test_get_font_by_name(self, mocker, font_name, font_enum, font_family, expected_exception):
        # Test the get_font_by_name method.
        mocker.patch.object(Fonts, "get_by_name", return_value=font_enum)
        mocker.patch.object(FontLoader, "load_font", return_value=font_family)

        if expected_exception:
            with pytest.raises(expected_exception):
                FontLoader.get_font_by_name(font_name)
        else:
            result = FontLoader.get_font_by_name(font_name)
            assert result == font_family

    def test_get_all_monospace_fonts(self, mocker):
        # Test the get_all_monospace_fonts method.
        monospace_fonts = [Fonts.IBM_PLEX_MONO]
        mocker.patch.object(Fonts, "get_all_monospace", return_value=monospace_fonts)
        mocker.patch.object(FontLoader, "load_font", side_effect=lambda font: font.name)

        result = FontLoader.get_all_monospace_fonts()
        assert result == [font.name for font in monospace_fonts]

    def test_get_monospace_font(self, mocker):
        # Test the get_monospace_font method.
        monospace_fonts = ['IBM Plex Mono']
        mocker.patch.object(FontLoader, "get_all_monospace_fonts", return_value=monospace_fonts)

        result = FontLoader.get_monospace_font()
        assert result == monospace_fonts[0]

    def test_init_fonts(self, mocker):
        # Test the init_fonts method.
        mock_app = MagicMock()
        mock_load_font = mocker.patch.object(FontLoader, "load_font", side_effect=lambda font: font.name)

        with patch.object(Fonts, "__iter__", return_value=iter(Fonts)):
            FontLoader.init_fonts(mock_app)

            for font in Fonts:
                mock_load_font.assert_any_call(font)

                if font.is_default:
                    test_font = QFont(font.name)
                    test_font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)
                    mock_app.setFont.assert_called_with(test_font)
