# tests/test_themes.py

from notolog.theme import Theme

from logging import Logger

import pytest
import os


class TestThemes:

    @pytest.fixture(scope="function", autouse=True)
    def test_obj_themes(self, mocker, request):
        """
        Testing object fixture.
        May contain minimal logic for testing purposes.
        """

        # Get the parameter value(s) from the request
        theme = request.param if hasattr(request, 'param') else None

        """
        If themes dir is set read themes from there.
        For test purposes to check theme files are readable.
        """
        test_themes_dir = os.path.join(os.path.dirname(__file__), 'test_themes')
        mocker.patch.object(Theme, 'get_themes_dir', return_value=test_themes_dir)

        yield Theme(theme=theme)

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
        "test_obj_themes, test_exp_params_fixture",
        [
            ((None), ('default')),
            ((''), ('default')),
            (('default'), ('default')),
            (('anyval'), ('anyval')),
        ],
        indirect=True
    )
    def test_themes_init(self, test_obj_themes, test_exp_params_fixture):
        """
        Test and check initial params are exist in the testing object.
        """
        assert isinstance(test_obj_themes.logger, Logger)

        exp_theme = test_exp_params_fixture

        assert hasattr(test_obj_themes, 'theme')
        assert test_obj_themes.theme == exp_theme
        assert hasattr(test_obj_themes, 'colors')
        assert hasattr(test_obj_themes, 'css')

    @pytest.mark.parametrize(
        "test_obj_themes, test_exp_params_fixture",
        [
            ((None), (None, 'default')),
            ((''), (None, 'default')),
            (('default'), (None, 'default')),
            (('anyval'), (None, 'anyval')),
            (('anyval'), ('new', 'new')),
        ],
        indirect=True
    )
    def test_themes_set_theme(self, test_obj_themes, test_exp_params_fixture):
        """
        Test theme setting for themes after the one was initialized.
        """
        param_theme, exp_theme = test_exp_params_fixture

        if param_theme:
            test_obj_themes.set_theme(param_theme)

        assert hasattr(test_obj_themes, 'theme')
        assert test_obj_themes.theme == exp_theme

    @pytest.mark.parametrize(
        "test_obj_themes, test_exp_params_fixture",
        [
            (None, os.path.join(os.path.dirname(__file__), 'test_themes')),
            ('default', os.path.join(os.path.dirname(__file__), 'test_themes')),
            ('noir_dark', os.path.join(os.path.dirname(__file__), 'test_themes')),
        ],
        indirect=True
    )
    def test_themes_get_themes_dir(self, test_obj_themes, test_exp_params_fixture):
        """
        Test theme dir path.
        """
        exp_themes_dir = test_exp_params_fixture

        assert test_obj_themes.get_themes_dir() == exp_themes_dir

    def test_themes_get_default_theme_dir(self, test_obj_themes):
        """
        Test default theme dir path.
        """
        exp_themes_dir = 'test_themes/default'

        default_theme_dir_parts = test_obj_themes.get_default_theme_dir().split(os.path.sep)[-2:]

        assert os.path.join(*default_theme_dir_parts) == exp_themes_dir

    @pytest.mark.parametrize(
        "test_obj_themes, test_exp_params_fixture",
        [
            (None,
             ('default',
              {'default': {'test_red': '0xFF0000', 'test_green': '0x00FF00', 'test_blue': '0x0000FF',
                           'test_void': '0x000000'},
               'noir_dark': {'test_non_red': '0x00FFFF', 'test_non_green': '0xFF00FF', 'test_non_blue': '0xFFFF00',
                             'test_light': '0xFFFFFF'}})),
        ],
        indirect=True
    )
    def test_themes_load_themes(self, test_obj_themes, test_exp_params_fixture):
        """
        Test actual theme colors loaded.
        """
        exp_theme, exp_colors = test_exp_params_fixture

        assert hasattr(test_obj_themes, 'theme')
        assert test_obj_themes.theme == exp_theme
        assert hasattr(test_obj_themes, 'colors')

    @pytest.mark.parametrize(
        "test_obj_themes, test_exp_params_fixture",
        [
            (None,
             ('default', {'test_red': 0xFF0000, 'test_green': 0x00FF00, 'test_blue': 0x0000FF, 'test_void': 0x000000})),
            ('default',
             ('default',
              {'test_red': 0xFF0000, 'test_green': 0x00FF00, 'test_blue': 0x0000FF, 'test_void': 0x000000})),
            ('noir_dark',
             ('noir_dark',
              {'test_non_red': 0x00FFFF, 'test_non_green': 0xFF00FF, 'test_non_blue': 0xFFFF00,
               'test_light': 0xFFFFFF})),
        ],
        indirect=True
    )
    def test_themes_get_theme_colors(self, test_obj_themes, test_exp_params_fixture):
        """
        Test actual theme colors loaded.
        """
        exp_theme, exp_colors = test_exp_params_fixture

        assert hasattr(test_obj_themes, 'theme')
        assert test_obj_themes.theme == exp_theme
        assert test_obj_themes.get_colors() == exp_colors

    @pytest.mark.parametrize(
        "test_obj_themes, test_exp_params_fixture",
        [
            (None, ('default', {'test_styles': 'default/test_styles.css'})),
            ('default', ('default', {'test_styles': 'default/test_styles.css'})),
            ('noir_dark', ('noir_dark', {'test_smth': 'noir_dark/test_smth.css'})),
        ],
        indirect=True
    )
    def test_themes_get_theme_css(self, mocker, test_obj_themes, test_exp_params_fixture):
        """
        Test actual theme colors loaded.
        """
        exp_theme, exp_css = test_exp_params_fixture

        assert hasattr(test_obj_themes, 'theme')
        assert test_obj_themes.theme == exp_theme
        assert test_obj_themes.get_css().keys() == exp_css.keys()
