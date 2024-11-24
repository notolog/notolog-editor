# tests/ui_tests/test_settings_dialog.py

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox
from PySide6.QtTest import QTest

from notolog.ui.settings_dialog import SettingsDialog
from notolog.notolog_editor import NotologEditor
from notolog.settings import Settings
from notolog.enums.languages import Languages
from notolog.modules.modules import Modules

from . import test_app  # noqa: F401

import pytest


class TestSettingsDialog:

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

    @pytest.fixture(autouse=True)
    def modules_obj(self):
        # Fixture to create and return modules instance
        modules = Modules()
        modules.modules = []
        yield modules

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

    @pytest.fixture(autouse=True)
    def ui_obj(self, mocker, main_window):
        # No modules
        mocker.patch.object(Modules, 'get_by_extension', return_value=[])
        # Fixture to initialize object.
        ui_obj = SettingsDialog(parent=main_window)
        yield ui_obj

    def test_ui_object_state(self, mocker, ui_obj: SettingsDialog, settings_obj):
        # Check app language set correctly
        assert settings_obj.app_language == 'la'

        # Check default window title
        assert ui_obj.windowTitle() == "Configurationes"

        # Get callback methods to check
        mock_init_ui = mocker.patch.object(ui_obj, 'init_ui', wraps=ui_obj.init_ui)

        # Check the method wasn't called as no ui_obj.exec() executed
        mock_init_ui.assert_not_called()

        # Mind the Latin translation
        assert ui_obj.tab_widget.tabText(0) == 'Generale'
        assert ui_obj.tab_widget.tabText(1) == 'Editor'
        assert ui_obj.tab_widget.tabText(2) == 'Visor'
        assert ui_obj.tab_widget.tabText(3) == 'Configuratio AI'
        assert ui_obj.tab_widget.tabText(4) == ''

        # Ensure the initial tab is the first tab
        assert ui_obj.tab_widget.currentIndex() == 0
        assert ui_obj.tab_widget.currentWidget().objectName() == 'settings_dialog_tab_general'
        # Test that clicking the edit button updates the editor state
        QTest.mouseClick(
            # ui_obj.tab_widget.tabBar().tabButton(1, QTabBar.ButtonPosition.LeftSide), Qt.MouseButton.LeftButton)
            # This simply targets the middle of the tab, ensuring the interaction is as expected.
            ui_obj.tab_widget.tabBar(), Qt.MouseButton.LeftButton, pos=ui_obj.tab_widget.tabBar().tabRect(1).center())
        # Check the result
        assert ui_obj.tab_widget.currentIndex() == 1
        assert ui_obj.tab_widget.currentWidget().objectName() == 'settings_dialog_tab_editor_config'

        checkboxes = ui_obj.findChildren(QCheckBox)
        for checkbox in checkboxes:
            if isinstance(checkbox, QCheckBox):
                # Parse the object name in case it contains a combination of lexeme and setting keys
                _lexeme_key, setting_name = ui_obj.parse_object_name(checkbox.objectName())
                if setting_name == 'show_main_menu':
                    # Either Qt.CheckState.Checked or Qt.CheckState.Unchecked
                    prev_state = checkbox.checkState()
                    QTest.mouseClick(checkbox, Qt.MouseButton.LeftButton)
                    assert checkbox.checkState() != prev_state
