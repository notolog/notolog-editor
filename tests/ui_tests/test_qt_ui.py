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

from notolog.notolog_editor import NotologEditor
from notolog.settings import Settings
from notolog.enums.languages import Languages

from . import test_app  # noqa: F401

import pytest


class TestQtUi:

    @pytest.fixture(scope="function", autouse=True)
    def settings_obj(self, mocker):
        """
        Use 'autouse=True' to enable automatic setup, or pass 'settings_obj' directly to main_window()
        """
        # Force to override system language as a default BEFORE creating Settings
        mocker.patch.object(Languages, 'default', return_value='la')

        # Fixture to create and return settings instance
        settings = Settings()
        # Clear settings to be sure start over without side effects
        settings.clear()
        # Reset singleton (qa functionality)
        Settings.reload()

        yield settings

    @pytest.fixture
    def main_window(self, mock_notolog_editor, test_app, settings_obj):  # noqa: F811 redefinition of unused 'test_app'
        # mock_notolog_editor fixture from conftest.py mocks NotologEditor.__init__
        # to prevent segfaults in headless test environments

        # Fixture to create and return main window instance
        editor = NotologEditor(screen=test_app.screens()[0])

        # Inject the settings_obj from the fixture
        editor.settings = settings_obj

        yield editor

    def test_editor_state(self, main_window, settings_obj):
        # Check app language set correctly
        assert settings_obj.app_language == 'la'

        # Check default window title
        assert main_window.windowTitle() == "Editorium Notolog"

        assert main_window.statusbar['mode_label'].text() == 'Modus Visum'
        assert main_window.statusbar['source_label'].text() == 'HTML'
        assert main_window.statusbar['encryption_label'].text() == 'Simplicitas 🔓'

        # Test that clicking the edit button updates the editor state
        button = main_window.toolbar.toolbar_edit_button
        # Use mock click since button is mocked in headless environment
        button.click()

        assert main_window.statusbar['mode_label'].text() == 'Modus Editio'
        assert main_window.statusbar['source_label'].text() == 'Markdown'
        assert main_window.statusbar['encryption_label'].text() == 'Simplicitas 🔓'

    def test_search_elements(self, main_window):
        assert hasattr(main_window.toolbar, 'search_form')
        main_window.toolbar.search_form.set_text('Test search')
        assert main_window.toolbar.search_form.text() == 'Test search'

        assert hasattr(main_window.toolbar.search_form, 'btn_search_clear')
        # Use mock click since button is mocked in headless environment
        main_window.toolbar.search_form.btn_search_clear.click()
        assert main_window.toolbar.search_form.text() == ''
