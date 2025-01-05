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

import asyncio

from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QMainWindow

from notolog.ui.ai_assistant.ai_assistant import AIAssistant
from notolog.ui.ai_assistant.ai_message_label import AIMessageLabel
from notolog.settings import Settings
from notolog.enums.languages import Languages
from notolog.modules.base_ai_core import BaseAiCore

from . import test_app  # noqa: F401

from unittest.mock import Mock

import pytest


class TestAiAssistant:

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
    def ui_obj(self, settings_obj, main_window):
        # Fixture to initialize object.
        ui_obj = AIAssistant(parent=main_window)
        yield ui_obj

    @pytest.fixture(scope="function")
    def test_exp_params_fixture(self, request):
        """
        Fixture to pass params and get expected results.
        This method is used only for passing params via pytest fixture.
        """
        # Retrieve parameter values from the test request.
        param_values = request.param

        yield param_values

    def test_ui_object_state(self, ui_obj: AIAssistant, settings_obj):
        # Check app language set correctly
        assert settings_obj.app_language == 'la'

        # Check default AI model
        assert ui_obj.inference_module == 'openai_api'

        # Check default window title
        assert ui_obj.windowTitle() == "Postulatio ad AI"

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "test_exp_params_fixture",
        [
            "Test Message",
            "Another Test Message",
        ],
        indirect=True
    )
    async def test_add_message(self, mocker, ui_obj: AIAssistant, settings_obj, test_exp_params_fixture):
        # Retrieve callback methods for verification.
        mock_send_request = mocker.patch.object(ui_obj, 'send_request', wraps=ui_obj.send_request)
        mock_update_usage = mocker.patch.object(ui_obj, 'update_usage', wraps=ui_obj.update_usage)

        mock_status_waiting = mocker.patch.object(ui_obj, 'set_status_waiting')
        mock_status_ready = mocker.patch.object(ui_obj, 'set_status_ready')

        module_core = Mock(spec=BaseAiCore)
        mock_init_module = mocker.patch.object(ui_obj, 'init_module', return_value=module_core)
        mock_cancel_request = mocker.patch.object(ui_obj, 'cancel_request', wraps=ui_obj.cancel_request)

        mock_send_request_finished_callback = mocker.patch.object(
            ui_obj, 'send_request_finished_callback', wraps=ui_obj.send_request_finished_callback)

        setattr(ui_obj.settings, 'ai_config_convert_to_md', False)

        mock_request = mocker.patch.object(module_core, 'request', return_value=Mock)

        self.assert_check_message_added = False

        def _check_message_added(message_text):
            assert test_exp_params_fixture in message_text
            self.assert_check_message_added = True

        # Verify the 'message_added' signal
        ui_obj.message_added.connect(_check_message_added)

        assert not self.assert_check_message_added

        # Check the there are no messages in conversation
        messages = ui_obj.messages_area.findChildren(AIMessageLabel)
        assert len(messages) == 0
        # Test that clicking the edit button updates the editor state
        ui_obj.prompt_input.setText(test_exp_params_fixture)
        QTest.mouseClick(ui_obj.send_button, Qt.MouseButton.LeftButton, pos=ui_obj.send_button.rect().center())
        # Check the conversation message was added
        messages = ui_obj.messages_area.findChildren(AIMessageLabel)
        assert len(messages) == 1
        for _message in messages:
            assert isinstance(_message, AIMessageLabel)
            assert _message.text() == test_exp_params_fixture

        # Check the method called
        mock_send_request.assert_called_once()

        # Check these methods were called
        mock_status_waiting.assert_called_once()
        mock_init_module.assert_called_once()

        assert self.assert_check_message_added

        # To allow completion of an async task
        await asyncio.sleep(0.05)

        # Verify that the method was called
        mock_status_ready.assert_not_called()

        # Finished signal with expected results
        # _expected_params = {'message_type': EnumMessageType.RESPONSE, 'request_msg_id': 3, 'response_msg_id': 6}
        # mock_send_request_finished_callback.assert_called_once_with(**_expected_params)
        mock_send_request_finished_callback.assert_not_called()

        # Ensure the method is not called, as it originates from the actual network response handling method.
        mock_update_usage.assert_not_called()

        mock_request.assert_called_once()
        mock_cancel_request.assert_not_called()  # Either an exception or stop button click
