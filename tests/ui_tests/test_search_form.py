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

    @pytest.fixture(scope="function")
    def test_params_fixture(self, request):
        # Retrieve parameter values from the test request.
        param_values = request.param

        yield param_values

    @pytest.fixture(scope="function")
    def test_exp_params_fixture(self, request):
        # Retrieve parameter values from the test request.
        param_values = request.param

        yield param_values

    def test_ui_object_state(self, ui_obj: SearchForm, settings_obj):
        # Check app language set correctly
        assert settings_obj.app_language == 'la'

        # Searched text update
        assert ui_obj.text() == ''
        ui_obj.set_text('test_text')
        assert ui_obj.text() == 'test_text'

    @pytest.mark.parametrize(
        "test_params_fixture, test_exp_params_fixture",
        [
            (('', ''), ('', '')),
            (('anything', ''), ('anything', '')),
            (('0', ''), ('0', '')),
            (('1', ''), ('1', '')),
            (('1', 'anything'), ('1', '')),
            (('anything', '3'), ('anything', '3')),
            (('2', '3'), ('2', '3')),
            (('', '4'), ('', '4')),
            (('', '0'), ('', '')),
            (('0', '5'), ('0', '5')),  # Note: The position label is not displayed
            (('0', 'five'), ('0', '')),  # Note: The position label is not displayed
        ],
        indirect=True
    )
    def test_counter(self, mocker, ui_obj, test_params_fixture, test_exp_params_fixture):
        counter_text, position_text = test_params_fixture
        exp_count_result, exp_pos_result = test_exp_params_fixture

        # Check initial occurrence values
        assert ui_obj._search_count_label.text() == ''
        assert ui_obj._search_pos_label.text() == ''

        mock_count_label_set_visible_called = mocker.patch.object(ui_obj._search_count_label, 'setVisible', return_value=None)
        mock_pos_label_set_visible_called = mocker.patch.object(ui_obj._search_pos_label, 'setVisible', return_value=None)

        # Set counter value
        ui_obj.set_counter_text(counter_text)

        # Set index position value
        ui_obj.set_position_text(position_text)

        # Check searched occurrence values
        assert ui_obj._search_count_label.text() == exp_count_result
        assert ui_obj._search_pos_label.text() == exp_pos_result

        mock_count_label_set_visible_called.assert_called_once()
        # Once during set_counter_text() and once when setting a value
        assert mock_pos_label_set_visible_called.call_count == 2
