# tests/ui_tests/test_search_form.py

from notolog.ui.search_form import SearchForm
from notolog.ui.toolbar import ToolBar
from notolog.notolog_editor import NotologEditor
from notolog.settings import Settings
from notolog.enums.languages import Languages
from notolog.modules.modules import Modules

from . import test_app  # noqa: F401

import pytest


class TestSearchForm:

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

    @pytest.fixture(autouse=True)
    def toolbar_obj(self, main_window):
        # Fixture to create and return toolbar instance
        toolbar_obj = ToolBar(parent=main_window, actions=[], refresh=False)
        yield toolbar_obj

    @pytest.fixture(autouse=True)
    def ui_obj(self, mocker, main_window, toolbar_obj):
        # No modules
        mocker.patch.object(Modules, 'get_by_extension', return_value=[])
        # Fixture to initialize object.
        ui_obj = SearchForm(parent=toolbar_obj)
        yield ui_obj

    def test_ui_object_state(self, mocker, ui_obj: SearchForm, settings_obj):
        # Check app language set correctly
        assert settings_obj.app_language == 'la'

        # Searched text update
        assert ui_obj.text() == ''
        ui_obj.set_text('test_text')
        assert ui_obj.text() == 'test_text'

        # Check searched occurrences values
        assert ui_obj._search_pos_label.text() == ''
        assert ui_obj._search_count_label.text() == ''
        # Set counter value
        ui_obj.set_counter_text('123')
        assert ui_obj._search_pos_label.text() == ''  # remains the same
        assert ui_obj._search_count_label.text() == '123'  # updated
        # Set index position value
        ui_obj.set_position_text('111')
        assert ui_obj._search_pos_label.text() == '111'  # updated
        assert ui_obj._search_count_label.text() == '123'  # remains the same
        # Set new counter value
        ui_obj.set_counter_text('456')
        assert ui_obj._search_pos_label.text() == ''  # reset
        assert ui_obj._search_count_label.text() == '456'  # updated
