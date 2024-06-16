# tests/ui_tests/test_ai_assistant.py
import asyncio

from PySide6.QtCore import Qt
from PySide6.QtTest import QTest

from notolog.ui.ai_assistant import AIAssistant, EnumMessageType
from notolog.ui.ai_message_label import AiMessageLabel
from notolog.notolog_editor import NotologEditor
from notolog.settings import Settings
from notolog.enums.languages import Languages
# from notolog.modules.openai_api import ModuleCore as TestModuleCore

from . import test_app  # noqa: F401

import pytest


class TestAiAssistant:

    @pytest.fixture
    def settings_obj(self, mocker):
        # Fixture to create and return settings instance
        settings = Settings()
        # Clear settings to be sure start over without side effects
        settings.clear()
        # Reset singleton (qa functionality)
        settings.reload()

        # Remember to pass the fixture to the other fixtures (check ui_obj())
        yield settings

    @pytest.fixture
    def main_window(self, mocker, test_app):  # noqa: F811 redefinition of unused 'test_app'
        # Force to override system language as a default
        mocker.patch.object(Languages, 'default', return_value='la')

        # Do not show actual window; return object instance only
        mocker.patch.object(NotologEditor, 'show', return_value=None)

        # Fixture to create and return main window instance
        window = NotologEditor(screen=test_app.screens()[0])

        yield window

    @pytest.fixture(autouse=True)
    def ui_obj(self, mocker, settings_obj, main_window):
        # Fixture to initialize object.
        ui_obj = AIAssistant(parent=main_window)
        yield ui_obj

    @pytest.fixture(scope="function")
    def test_exp_params_fixture(self, request):
        """
        Fixture to pass params and get expected results.
        This method is used only for passing params via pytest fixture.
        """
        # Get the parameter value(s) from the request
        param_values = request.param

        yield param_values

    def test_ui_object_state(self, mocker, ui_obj: AIAssistant, settings_obj):
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
        # Get callback methods to check
        mock_send_request = mocker.patch.object(ui_obj, 'send_request', wraps=ui_obj.send_request)
        mock_update_usage = mocker.patch.object(ui_obj, 'update_usage', wraps=ui_obj.update_usage)

        mock_status_waiting = mocker.patch.object(ui_obj, 'set_status_waiting')
        mock_status_ready = mocker.patch.object(ui_obj, 'set_status_ready')

        mock_init_module = mocker.patch.object(ui_obj, 'init_module', wraps=ui_obj.init_module)

        mock_send_request_finished_callback = mocker.patch.object(
            ui_obj, 'send_request_finished_callback', wraps=ui_obj.send_request_finished_callback)

        # Wraps doesn't work
        # mock_request = mocker.patch.object(TestModuleCore, 'request', wraps=TestModuleCore.request)

        def _check_message_added(message_text):
            assert test_exp_params_fixture in message_text

        # Assert 'downloaded' signal
        ui_obj.message_added.connect(_check_message_added)

        # Check the there are no messages in conversation
        messages = ui_obj.messages_area.findChildren(AiMessageLabel)
        assert len(messages) == 0
        # Test that clicking the edit button updates the editor state
        ui_obj.prompt_input.setText(test_exp_params_fixture)
        QTest.mouseClick(ui_obj.send_button, Qt.MouseButton.LeftButton, pos=ui_obj.send_button.rect().center())
        # Check the conversation message was added
        messages = ui_obj.messages_area.findChildren(AiMessageLabel)
        assert len(messages) == 1
        for _message in messages:
            assert isinstance(_message, AiMessageLabel)
            assert _message.text() == test_exp_params_fixture

        # Check the method called
        mock_send_request.assert_called_once()

        # Check these methods were called
        mock_status_waiting.assert_called_once()
        mock_init_module.assert_called_once()

        # To allow completion of an async task
        await asyncio.sleep(0.05)

        # Module core methods
        # mock_request.assert_called_once()

        # Check these methods weren't called
        mock_status_ready.assert_called()

        # Finished signal with expected results
        _expected_params = {'message_type': EnumMessageType.RESPONSE, 'request_msg_id': 3, 'response_msg_id': 6}
        mock_send_request_finished_callback.assert_called_once_with(**_expected_params)

        # Ensure the method is not called, as it originates from the actual network response handling method.
        mock_update_usage.assert_not_called()
