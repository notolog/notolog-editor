# tests/ui_tests/test_ai_assistant.py

from PySide6.QtCore import Qt
from PySide6.QtTest import QTest

from notolog.ui.ai_assistant import AIAssistant
from notolog.notolog_editor import NotologEditor
from notolog.settings import Settings
from notolog.enums.languages import Languages

from . import test_app  # noqa: F401

import pytest


class TestAiAssistant:

    @pytest.fixture
    def settings_obj(self):
        # Fixture to create and return settings instance
        settings = Settings()
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
    def ui_obj(self, main_window):
        # Fixture to initialize object.
        ui_obj = AIAssistant(parent=main_window)
        yield ui_obj

    def test_ui_object_state(self, mocker, ui_obj: AIAssistant, settings_obj):
        # Check app language set correctly
        assert settings_obj.app_language == 'la'
        # Check default AI model
        assert ui_obj.inference_model == 'gpt-3.5-turbo'

        # Check default window title
        assert ui_obj.windowTitle() == "Postulatio ad AI"

        # Get callback methods to check
        mock_send_request = mocker.patch.object(ui_obj, 'send_request', wraps=ui_obj.send_request)
        mock_update_usage = mocker.patch.object(ui_obj, 'update_usage', wraps=ui_obj.update_usage)
        mock_status_waiting = mocker.patch.object(ui_obj, 'set_status_waiting')
        mock_status_ready = mocker.patch.object(ui_obj, 'set_status_ready')

        # Check the output field is empty
        assert ui_obj.response_output.toPlainText() == ''
        # Test that clicking the edit button updates the editor state
        QTest.mouseClick(ui_obj.send_button, Qt.MouseButton.LeftButton)
        # Check the output field is NOT empty
        assert ui_obj.response_output.toPlainText() == 'Praebe textum ad respondendum fere...'

        # Check the method called
        mock_send_request.assert_called_once()

        # Check these methods weren't called
        mock_status_waiting.assert_not_called()
        mock_status_ready.assert_not_called()
        mock_update_usage.assert_not_called()
