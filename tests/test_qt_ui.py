from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from PySide6.QtTest import QTest

from notolog.notolog_editor import NotologEditor
from notolog.enums.languages import Languages
from notolog.settings import Settings

import os
import sys
import pytest


class TestQtUi:

    @pytest.fixture(autouse=True, scope="session")
    def qt_app(self):
        # Check to avoid:
        # RuntimeError: Please destroy the QApplication singleton before creating a new QApplication instance.
        app = QApplication.instance()
        if not app:
            # Force Qt style override
            """
            QApplication: invalid style override 'kvantum' passed, ignoring it.
                Available styles: Windows, Fusion
            """
            os.environ["QT_STYLE_OVERRIDE"] = "Fusion"
            # Fixture to initialize QApplication.
            app = QApplication(sys.argv)

        yield app

        # Properly close the QApplication after each test
        app.quit()

    @pytest.fixture
    def settings_obj(self, qt_app):
        # Fixture to create and return settings instance
        settings = Settings()
        yield settings

    @pytest.fixture
    def main_window(self, mocker, qt_app):
        # Force to override system language as a default
        mocker.patch.object(Languages, 'default', return_value='la')

        # Fixture to create and return main window instance
        window = NotologEditor(screen=qt_app.screens()[0])
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
