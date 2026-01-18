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

from notolog.app_config import AppConfig
from notolog.ui.ai_assistant.ai_assistant import AIAssistant
from notolog.ui.ai_assistant.ai_message_label import AIMessageLabel
from notolog.settings import Settings
from notolog.enums.languages import Languages
from notolog.helpers.clipboard_helper import ClipboardHelper
from notolog.helpers.tooltip_helper import TooltipHelper

from . import test_app  # noqa: F401

import pytest
import logging


class TestAIMessageLabel:

    @pytest.fixture(scope="function", autouse=True)
    def test_obj_app_config(self, mocker):
        # Mock AppConfig's get_logger_level method to suppress logging during tests.
        mocker.patch.object(AppConfig, 'get_logger_level', return_value=logging.NOTSET)

        # Create an AppConfig instance and set it to test mode.
        _app_config = AppConfig()
        _app_config.set_test_mode(True)

        yield _app_config

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
    def ai_assistant_obj(self, main_window):
        # Fixture to initialize object.
        yield AIAssistant(parent=main_window)

    @pytest.fixture(autouse=True)
    def ui_obj(self, settings_obj, ai_assistant_obj, request):
        """
        Testing object fixture.
        May contain minimal logic for testing purposes.
        """

        # Retrieve parameter values from the test request.
        text = request.param if hasattr(request, 'param') else None

        yield AIMessageLabel(parent=ai_assistant_obj, text=text, settings=settings_obj)

    @pytest.fixture(scope="function")
    def test_params_fixture(self, request):
        # Retrieve parameter values from the test request.
        param_values = request.param

        yield param_values

    @pytest.fixture(scope="function")
    def test_exp_params_fixture(self, request):
        """
        Fixture to pass params and get expected results.
        This method is used only for passing params via pytest fixture.
        """
        # Retrieve parameter values from the test request.
        param_values = request.param

        yield param_values

    def test_ui_object_state(self, ui_obj: AIMessageLabel, settings_obj):
        # Check app language set correctly
        assert settings_obj.app_language == 'la'

    @pytest.mark.parametrize(
        "test_params_fixture",
        [
            None,
            '',
            'Test Message',
        ],
        indirect=True
    )
    def test_copy_content(self, mocker, ui_obj: AIMessageLabel, test_params_fixture):
        # Extract the test method name and expected parameters
        text_to_copy = test_params_fixture

        mocker.patch.object(ui_obj, 'get_text_to_copy', return_value=text_to_copy)

        mock_clipboard_helper_set_text = mocker.patch.object(ClipboardHelper, 'set_text', return_value=None)
        mock_tooltip_helper_show_tooltip = mocker.patch.object(TooltipHelper, 'show_tooltip')

        # Run the method under test
        ui_obj.copy_content()

        mock_clipboard_helper_set_text.assert_called_once_with(text_to_copy)
        mock_tooltip_helper_show_tooltip.assert_called_once()
        assert "text" in str(mock_tooltip_helper_show_tooltip.call_args)
        assert "QPushButton" in str(mock_tooltip_helper_show_tooltip.call_args)

    @pytest.mark.parametrize(
        "ui_obj, test_params_fixture, test_exp_params_fixture",
        [
            (None, False, ''),
            (None, True, ''),
            ('', False, ''),
            ('', True, ''),
            ("Test Message", False, "Test Message"),
            ("Test Message", True, "Test Message"),
            ("<b>Test Message</b>", False, "<b>Test Message</b>"),
            ("<b>Test Message</b>", True, "Test Message"),
            ("**Test Message**", False, "**Test Message**"),
            ("**Test Message**", True, "**Test Message**"),
        ],
        indirect=True
    )
    def test_get_text_to_copy(self, settings_obj: Settings, ai_assistant_obj: AIAssistant, ui_obj: AIMessageLabel,
                              test_params_fixture, test_exp_params_fixture):
        # Check if the result needs to be converted from HTML to raw text.
        convert_to_md = test_params_fixture

        settings_obj.ai_config_convert_to_md = convert_to_md

        # Run the method under test
        result = ui_obj.get_text_to_copy()

        assert result == test_exp_params_fixture
