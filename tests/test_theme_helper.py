# tests/test_themes.py

from notolog.helpers.theme_helper import ThemeHelper
from notolog.enums.themes import Themes
from notolog.theme import Theme
from notolog.settings import Settings
from notolog.app_config import AppConfig

from logging import Logger

import os
import pytest


class TestThemeHelper:

    @pytest.fixture(scope="function", autouse=True)
    def test_obj_theme_helper(self, mocker, request):
        """
        Testing object fixture.
        May contain minimal logic for testing purposes.
        """

        # Get the parameter value(s) from the request
        theme = request.param if hasattr(request, 'param') else None

        mocker.patch.object(AppConfig, 'get_debug', return_value=False)
        # Or: monkeypatch.setattr(Settings, 'theme', theme)
        mocker.patch('notolog.settings.Settings.app_theme', theme)

        """
        If themes dir is set read themes from there.
        For test purposes to check theme files are readable.
        """
        test_themes_dir = os.path.join(os.path.dirname(__file__), 'test_themes')
        mocker.patch.object(Theme, 'get_themes_dir', return_value=test_themes_dir)

        yield ThemeHelper()

    @pytest.fixture(scope="function")
    def test_exp_params_fixture(self, request):
        """
        Fixture to pass params and get expected results.
        This method is used only for passing params via pytest fixture.
        """

        # Get the parameter value(s) from the request
        param_values = request.param

        yield param_values

    @pytest.mark.parametrize(
        "test_obj_theme_helper, test_exp_params_fixture",
        [
            ((None), ('default')),
            ((''), ('default')),
            (('default'), ('default')),  # Because of method default()
            (('DEFAULT'), ('default')),
            (('anyval'), ('default')),
        ],
        indirect=True
    )
    def test_theme_helper_init(self, test_obj_theme_helper, test_exp_params_fixture):
        """
        Test and check initial params are exist in the testing object.
        """
        assert isinstance(test_obj_theme_helper.logger, Logger)

        exp_theme = test_exp_params_fixture

        assert hasattr(test_obj_theme_helper, 'theme')
        assert isinstance(test_obj_theme_helper.theme, Theme)
        assert isinstance(test_obj_theme_helper.settings, Settings)
        assert test_obj_theme_helper.theme.theme == exp_theme

    @pytest.mark.parametrize(
        "test_obj_theme_helper, test_exp_params_fixture",
        [
            (None, (None, None, None)),
            ('default', ('test_red', None, 0xFF0000)),
            ('default', ('test_green', True, '#00FF00')),
            ('default', ('test_blue', False, 0x0000FF)),
            ('default', ('test_undefined', None, None)),
            ('noir', ('test_non_red', False, 0x00FFFF)),
            ('noir', ('test_light', True, '#FFFFFF')),
            ('test_undefined', (None, None, None)),
            ('test_undefined', ('undefined_name', True, None)),
        ],
        indirect=True
    )
    def test_themes_get_color(self, test_obj_theme_helper, test_exp_params_fixture):
        """
        Test getter for correctly loaded and really existent theme's colors.
        """
        param_name, param_css_format, exp_result = test_exp_params_fixture

        assert test_obj_theme_helper.get_color(param_name, param_css_format) == exp_result

    @pytest.mark.parametrize(
        "test_obj_theme_helper, test_exp_params_fixture",
        [
            (None, (None, None)),
            ('default', ('test_smth', None)),
            ('default', ('test_styles', 'QTextEdit {}')),
            ('noir', ('test_smth', 'QTextEdit {}')),
        ],
        indirect=True
    )
    def test_themes_get_css(self, test_obj_theme_helper, test_exp_params_fixture):
        """
        Test getter for correctly loaded and really existent theme's css files.
        """
        param_css_name, exp_result = test_exp_params_fixture

        assert test_obj_theme_helper.get_css(param_css_name) == exp_result