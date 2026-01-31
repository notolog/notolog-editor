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

from notolog.helpers.theme_helper import ThemeHelper
from notolog.theme import Theme
from notolog.settings import Settings
from notolog.app_config import AppConfig

from logging import Logger

from . import test_core_app  # noqa: F401

import os
import pytest
import logging


class TestThemeHelper:

    @pytest.fixture(autouse=True)
    def test_settings_fixture(self, request, test_core_app):  # noqa: F811 redefinition of unused 'test_app'
        # The test_app fixture sets up the app environment explicitly.
        setting = Settings()
        # Retrieve parameter values from the test request.
        setting.app_theme = request.param
        yield setting

    @pytest.fixture(autouse=True)
    def test_obj_theme_helper(self, mocker, test_settings_fixture):
        """
        Testing object fixture.
        May contain minimal logic for testing purposes.
        """

        # Mock AppConfig's get_logger_level method to suppress logging during tests.
        mocker.patch.object(AppConfig, 'get_logger_level', return_value=logging.NOTSET)

        """
        If themes dir is set read themes from there.
        For test purposes to check theme files are readable.
        """
        test_themes_dir = os.path.join(os.path.dirname(__file__), 'test_themes')
        mocker.patch.object(Theme, 'get_themes_dir', return_value=test_themes_dir)

        # Allow to change theme name during test cycle with no caching
        AppConfig().set_test_mode(True)

        yield ThemeHelper()

    @pytest.fixture(scope="function")
    def test_exp_params_fixture(self, request):
        """
        Fixture to pass params and get expected results.
        This method is used only for passing params via pytest fixture.
        """

        # Retrieve parameter values from the test request.
        param_values = request.param

        yield param_values

    @pytest.mark.parametrize(
        "test_settings_fixture, test_obj_theme_helper, test_exp_params_fixture",
        [
            ((None), (None), ('default')),
            ((''), (None), ('default')),
            (('default'), (None), ('default')),  # Because of default() method
            (('DEFAULT'), (None), ('default')),
            (('anyval'), (None), ('default')),
        ],
        indirect=True
    )
    def test_theme_helper_init(self, test_settings_fixture, test_obj_theme_helper: ThemeHelper,
                               test_exp_params_fixture):
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
        "test_settings_fixture, test_obj_theme_helper, test_exp_params_fixture",
        [
            (None, None, (None, None, None)),
            ('default', None, ('test_red', None, 0xFF0000)),
            ('default', None, ('test_green', True, '#00FF00')),
            ('default', None, ('test_blue', False, 0x0000FF)),
            ('default', None, ('test_undefined', None, None)),
            # 'noir_dark' is real as it can be checked with Themes enum
            ('noir_dark', None, ('test_non_red', False, 0x00FFFF)),
            ('noir_dark', None, ('test_light', True, '#FFFFFF')),
            ('test_undefined', None, (None, None, None)),
            ('test_undefined', None, ('undefined_name', True, None)),
        ],
        indirect=True
    )
    def test_themes_get_color(self, test_settings_fixture, test_obj_theme_helper, test_exp_params_fixture):
        """
        Test getter for correctly loaded and really existent theme's colors.
        """
        param_name, param_css_format, exp_result = test_exp_params_fixture

        assert test_obj_theme_helper.get_color(param_name, param_css_format) == exp_result

    @pytest.mark.parametrize(
        "test_settings_fixture, test_obj_theme_helper, test_exp_params_fixture",
        [
            (None, None, (None, None)),
            ('default', None, ('test_smth', None)),
            ('default', None, ('test_styles', 'QTextEdit {}\n')),
            ('noir_dark', None, ('test_smth', 'QTextEdit {}\n')),
        ],
        indirect=True
    )
    def test_themes_get_css(self, test_settings_fixture, test_obj_theme_helper, test_exp_params_fixture):
        """
        Test getter for correctly loaded and really existent theme's css files.
        """
        param_css_name, exp_result = test_exp_params_fixture

        assert test_obj_theme_helper.get_css(param_css_name) == exp_result
