# tests/ui_tests/test_toolbar.py

from PySide6.QtCore import Qt
from PySide6.QtTest import QTest

from notolog.ui.search_form import SearchForm
from notolog.ui.toolbar import ToolBar
from notolog.notolog_editor import NotologEditor
from notolog.settings import Settings
from notolog.enums.languages import Languages
from notolog.modules.modules import Modules

from . import test_app  # noqa: F401

import pytest


class TestToolBar:

    _test_var_click_assert_cnt = 0

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

    @pytest.fixture
    def ui_obj(self, mocker, main_window):
        # No modules
        mocker.patch.object(Modules, 'get_by_extension', return_value=[])
        # Fixture to initialize object.
        _test_action = {'type': 'action', 'weight': 1, 'name': 'toolbar_actions_label_test',
                        'theme_icon': '', 'color': 'green',
                        'label': 'Test label text', 'accessible_name': 'Test accessible name text',
                        'var_name': 'test_var', 'action': lambda: self._test_var_click_assert()}
        # TODO: Mock class to override main window actions
        ui_obj = ToolBar(parent=main_window, actions=[_test_action], refresh=False)
        yield ui_obj

    def test_ui_object_state(self, main_window, ui_obj: ToolBar, settings_obj):
        # Check app language set correctly
        assert settings_obj.app_language == 'la'

        assert isinstance(main_window.toolbar, ToolBar)
        assert isinstance(ui_obj, ToolBar)
        # Both objects differ in the test environment
        assert main_window.toolbar != ui_obj

        assert isinstance(ui_obj.search_form, SearchForm)

        assert ui_obj.settings.toolbar_icons == 131070

        # Variable for testing action button
        assert hasattr(ui_obj, 'test_var')

        # Verifying click action via _test_var_click_assert()
        assert self._test_var_click_assert_cnt == 0
        QTest.mouseClick(ui_obj.test_var, Qt.MouseButton.LeftButton, pos=ui_obj.test_var.rect().center())  # noqa
        assert self._test_var_click_assert_cnt == 1

    def _test_var_click_assert(self):
        assert True
        self._test_var_click_assert_cnt += 1
