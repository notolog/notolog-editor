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

from PySide6.QtCore import Qt
from PySide6.QtTest import QTest

from notolog.notolog_editor import NotologEditor
from notolog.settings import Settings
from notolog.enums.languages import Languages

from . import test_app  # noqa: F401

import pytest


class TestQtUi:

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

        yield settings

    @pytest.fixture
    def main_window(self, mocker, test_app):  # noqa: F811 redefinition of unused 'test_app'
        # Force to override system language as a default
        mocker.patch.object(Languages, 'default', return_value='la')

        # Do not show actual window; return object instance only
        mocker.patch.object(NotologEditor, 'show', return_value=None)
        # Prevent resource processing, including 'process_document_images'
        mocker.patch.object(NotologEditor, 'load_content_html', return_value=None)

        # Fixture to create and return main window instance
        yield NotologEditor(screen=test_app.screens()[0])

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
        # assert button
        QTest.mouseClick(button, Qt.MouseButton.LeftButton, pos=button.rect().center())

        assert main_window.statusbar['mode_label'].text() == 'Modus Editio'
        assert main_window.statusbar['source_label'].text() == 'Markdown'
        assert main_window.statusbar['encryption_label'].text() == 'Simplicitas 🔓'

    def test_search_elements(self, main_window):
        assert hasattr(main_window.toolbar, 'search_form')
        main_window.toolbar.search_form.set_text('Test search')
        assert main_window.toolbar.search_form.text() == 'Test search'

        assert hasattr(main_window.toolbar.search_form, 'btn_search_clear')
        # Test that clicking the button updates the search field
        QTest.mouseClick(main_window.toolbar.search_form.btn_search_clear, Qt.MouseButton.LeftButton)  # noqa
        assert main_window.toolbar.search_form.text() == ''
