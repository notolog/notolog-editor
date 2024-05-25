# tests/ui_tests/test_qt_ui.py

from PySide6.QtCore import Qt
from PySide6.QtTest import QTest

from notolog.notolog_editor import NotologEditor
from notolog.settings import Settings
from notolog.enums.languages import Languages

from . import test_app  # noqa: F401

import pytest


class TestQtUi:

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

    def test_editor_state(self, main_window, settings_obj):
        # Check app language set correctly
        assert settings_obj.app_language == 'la'

        # Check default window title
        assert main_window.windowTitle() == "Editorium Notolog"

        assert main_window.statusbar['mode_label'].text() == 'Modus Visum'
        assert main_window.statusbar['source_label'].text() == 'HTML'
        assert main_window.statusbar['encryption_label'].text() == 'Simplicitas 🔓'

        # Test that clicking the edit button updates the editor state
        QTest.mouseClick(main_window.toolbar.toolbar_edit_button, Qt.MouseButton.LeftButton)

        assert main_window.statusbar['mode_label'].text() == 'Modus Editio'
        assert main_window.statusbar['source_label'].text() == 'Markdown'
        assert main_window.statusbar['encryption_label'].text() == 'Simplicitas 🔓'

    def test_search_elements(self, main_window):
        assert hasattr(main_window.toolbar, 'search_input')
        main_window.toolbar.search_input.setText('Test search')
        assert main_window.toolbar.search_input.text() == 'Test search'

        assert hasattr(main_window.toolbar, 'btn_search_clear')
        # Test that clicking the button updates the search field
        QTest.mouseClick(main_window.toolbar.btn_search_clear, Qt.MouseButton.LeftButton)
        assert main_window.toolbar.search_input.text() == ''
