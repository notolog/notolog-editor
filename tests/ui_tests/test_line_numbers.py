"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Contains unit and integration tests for the related functionality.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QTextDocument, QFontMetrics

from notolog.settings import Settings
from notolog.edit_widget import EditWidget
from notolog.enums.languages import Languages
from notolog.ui.line_numbers import LineNumbers

from . import test_app  # noqa: F401

from unittest.mock import MagicMock

import pytest


class TestLineNumbers:

    @pytest.fixture(scope="class", autouse=True)
    def settings_obj(self):
        """
        Use 'autouse=True' to enable automatic setup, or pass 'settings_obj' directly to main_window()
        """
        # Fixture to create and return settings instance
        settings = Settings()
        # Clear settings to be sure start over without side effects
        settings.clear()
        # Reset singleton (qa functionality)
        Settings.reload()

        # Remember to pass the fixture to the other fixtures (check ui_obj())
        yield settings

    @pytest.fixture
    def main_window(self, mocker, test_app):  # noqa: F811 redefinition of unused 'test_app'
        # Force to override system language as a default
        mocker.patch.object(Languages, 'default', return_value='la')

        # Fixture to create and return main window instance
        yield QMainWindow()

    @pytest.fixture(autouse=True)
    def ui_obj(self, mocker, settings_obj, main_window):

        mock_text_document = MagicMock(spec=QTextDocument)
        mocker.patch.object(mock_text_document, 'defaultFont', return_value='smth1')

        mocker.patch.object(EditWidget, 'document', return_value=mock_text_document)
        mocker.patch.object(EditWidget, 'parent', return_value=main_window)
        mock_edit_widget = EditWidget()

        # Fixture to initialize object.
        yield LineNumbers(editor=mock_edit_widget)

    @pytest.fixture(scope="function")
    def test_exp_params_fixture(self, request):
        """
        Fixture to pass params and get expected results.
        This method is used only for passing params via pytest fixture.
        """
        # Retrieve parameter values from the test request.
        param_values = request.param

        yield param_values

    def test_ui_object(self, mocker, ui_obj: LineNumbers, settings_obj):
        # Check app language set correctly
        assert settings_obj.app_language == 'la'

        mock_update_numbers = mocker.patch.object(ui_obj, 'update_numbers', return_value=None)
        mock_update_request = mocker.patch.object(ui_obj, 'update_request', return_value=None)
        mock_update_width = mocker.patch.object(ui_obj, 'update_width', return_value=None)

        ui_obj.editor.setPlainText('smth1')

        mock_update_request.assert_called()
        assert 'QRect' in str(mock_update_request.call_args)
        mock_update_width.assert_not_called()

        ui_obj.editor.setPlainText('smth1\nsmth2\nsmth3')
        mock_update_width.assert_called_once()
        assert str(mock_update_width.call_args) == 'call()'

        assert ui_obj.line_numbers_width() > 0

        # In test mode it's only callable from the init method;
        # otherwise on block count changed from the outside
        mock_update_numbers.assert_not_called()

    @pytest.mark.parametrize(
        "test_exp_params_fixture",
        [
            (0, 0, 5),  # Digits: max(2, block_count)
            (1, 10, 25),  # Digits: max(2, block_count)
            (10, 10, 25),  # Digits: max(2, block_count)
            (100, 10, 35),
            (1000, 10, 45),
            (10000, 10, 55),
            (10000, 11, 60),
        ],
        indirect=True
    )
    def test_line_numbers_width(self, mocker, ui_obj: LineNumbers, settings_obj, test_exp_params_fixture):
        block_count, horizontal_advance, exp_result = test_exp_params_fixture

        mock_font_metrics = MagicMock(spec=QFontMetrics)
        mocker.patch.object(mock_font_metrics, 'horizontalAdvance', return_value=horizontal_advance)

        mocker.patch.object(ui_obj.editor, 'blockCount', return_value=block_count)
        mocker.patch.object(ui_obj, 'fontMetrics', return_value=mock_font_metrics)

        result = ui_obj.line_numbers_width()

        assert result == exp_result
