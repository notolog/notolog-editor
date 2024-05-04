# tests/test_settings.py
from app.settings import Settings

import pytest

class TestSettings():

    def test_settings_defaults(self):
        obj = Settings()
        assert obj.ui_width == 0
        assert obj.ui_height == 0
        assert obj.ui_pos_x == 0
        assert obj.ui_pos_y == 0
        assert obj.file_path is ''
        assert obj.toolbar_icons is 0

    def test_settings_setter_getter(self):
        settings_a = Settings()
        # Reset to test
        settings_a.clear()

        # Set values in A object
        settings_a.ui_width = 11
        settings_a.ui_height = 22
        settings_a.ui_pos_x = 33
        settings_a.ui_pos_y = 44
        settings_a.file_path = 'test/path/file.txt'
        settings_a.toolbar_icons = 8

        settings_b = Settings()

        # Assert values are stored correctly
        assert settings_b.ui_width == 11
        assert settings_b.ui_height == 22
        assert settings_b.ui_pos_x == 33
        assert settings_b.ui_pos_y == 44
        assert settings_b.file_path == 'test/path/file.txt'
        assert settings_b.toolbar_icons is 8

        # Reset to restore
        settings_b.clear()
