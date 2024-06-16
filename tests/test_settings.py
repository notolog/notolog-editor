# tests/test_settings.py

from notolog.settings import Settings
from notolog.app_config import AppConfig

from . import test_core_app  # noqa: F401

import os
import pytest


class TestSettings:

    @pytest.fixture(scope="function")
    def test_obj_settings(self, test_core_app):  # noqa: F811 redefinition of unused 'test_app'
        # The test_app fixture sets up the app environment explicitly.
        settings = Settings()
        # Clear settings to be sure start over without side effects
        settings.clear()
        # Reset singleton (qa functionality)
        settings.reload()

        yield settings

    def test_settings_defaults(self, test_obj_settings):
        assert test_obj_settings.ui_width == 0
        assert test_obj_settings.ui_height == 0
        assert test_obj_settings.ui_pos_x == 0
        assert test_obj_settings.ui_pos_y == 0
        assert test_obj_settings.file_path == ''
        assert test_obj_settings.toolbar_icons == 0

    def test_settings_setter_getter(self, test_obj_settings):
        # Reset settings to test
        test_obj_settings.clear()

        # Set values in A object
        test_obj_settings.ui_width = 11
        test_obj_settings.ui_height = 22
        test_obj_settings.ui_pos_x = 33
        test_obj_settings.ui_pos_y = 44
        test_obj_settings.file_path = os.path.normpath('test/path/file.txt')
        test_obj_settings.toolbar_icons = 8

        # Sync changes
        test_obj_settings.sync()

        # Reset singleton (qa functionality)
        test_obj_settings.reload()

        # Get fresh settings instance
        settings = Settings()

        # Assert values are stored correctly
        assert settings.ui_width == 11
        assert settings.ui_height == 22
        assert settings.ui_pos_x == 33
        assert settings.ui_pos_y == 44
        assert settings.file_path == os.path.normpath('test/path/file.txt')
        assert settings.toolbar_icons == 8

        # Linux: /home/runner/.config/Notolog/notolog_editor_tests.conf (notolog_editor_qa.conf)
        # macOS: '/Users/runner/Library/Preferences/com.notolog.notolog_editor_tests.plist'
        # Windows: '\\HKEY_CURRENT_USER\\Software\\Notolog\\notolog_editor_tests'
        assert AppConfig().get_settings_app_name_qa() in settings.fileName()
        assert test_obj_settings.fileName() == settings.fileName()

        # Reset to restore
        settings.clear()
