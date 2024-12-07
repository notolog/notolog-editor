# tests/ui_tests/test_settings_dialog.py

from PySide6.QtCore import Qt, QObject
from PySide6.QtWidgets import QWidget, QTabWidget, QLabel, QCheckBox, QLineEdit, QSlider
from PySide6.QtWidgets import QScrollArea, QVBoxLayout, QSizePolicy, QPlainTextEdit, QComboBox, QSpinBox, QDoubleSpinBox
from PySide6.QtTest import QTest

from notolog.ui.settings_dialog import SettingsDialog
from notolog.ui.enum_combo_box import EnumComboBox
from notolog.ui.label_with_hint import LabelWithHint
from notolog.ui.dir_path_line_edit import DirPathLineEdit
from notolog.ui.file_path_line_edit import FilePathLineEdit
from notolog.ui.horizontal_line_spacer import HorizontalLineSpacer
from notolog.notolog_editor import NotologEditor
from notolog.settings import Settings
from notolog.enums.languages import Languages
from notolog.modules.modules import Modules

from ..test_enums.something_enum import SomethingEnum

from . import test_app  # noqa: F401

import pytest

from unittest.mock import MagicMock


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

    def test_ui_object_state(self, mocker, ui_obj: SettingsDialog, settings_obj):
        # Check app language set correctly
        assert settings_obj.app_language == 'la'

        # Check default window title
        assert ui_obj.windowTitle() == "Configurationes"

        # Retrieve callback methods for verification.
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
        assert isinstance(ui_obj.tab_widget.currentWidget(), QScrollArea)
        assert ui_obj.tab_widget.currentWidget().objectName() == 'settings_dialog_tab_general'
        # Test that clicking the edit button updates the editor state
        QTest.mouseClick(
            # ui_obj.tab_widget.tabBar().tabButton(1, QTabBar.ButtonPosition.LeftSide), Qt.MouseButton.LeftButton)
            # This simply targets the middle of the tab, ensuring the interaction is as expected.
            ui_obj.tab_widget.tabBar(), Qt.MouseButton.LeftButton, pos=ui_obj.tab_widget.tabBar().tabRect(1).center())
        # Check the result
        assert ui_obj.tab_widget.currentIndex() == 1
        assert isinstance(ui_obj.tab_widget.currentWidget(), QScrollArea)
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

    @pytest.mark.parametrize(
        "test_params_fixture, test_exp_params_fixture",
        [
            ('', ['', '']),
            (':', ['', '']),
            ('obj1_name', ['obj1_name', 'obj1_name']),
            ('obj1_name:setting1_name', ['obj1_name', 'setting1_name']),
            (':setting2_name', ['', 'setting2_name']),
        ],
        indirect=True
    )
    def test_parse_object_name(self, ui_obj: SettingsDialog, test_params_fixture, test_exp_params_fixture):
        """
        Covers:
        - SettingsDialog.parse_object_name
        """

        # Extract the test method name and expected parameters
        test_object_name = test_params_fixture
        exp_result = test_exp_params_fixture

        # Run the method under test
        result = ui_obj.parse_object_name(str(test_object_name))

        assert result == exp_result

    @pytest.mark.parametrize(
        "test_params_fixture, test_exp_params_fixture",
        [
            ('get_general_fields', 'settings_dialog_tab_general'),
            ('get_editor_config_fields', 'settings_dialog_tab_editor_config'),
            ('get_viewer_config_fields', 'settings_dialog_tab_viewer_config'),
            ('get_ai_config_fields', 'settings_dialog_tab_ai_config'),
        ],
        indirect=True
    )
    def test_get_tab_fields(self, mocker, ui_obj: SettingsDialog, test_params_fixture, test_exp_params_fixture):
        """
        Covers:
        - SettingsDialog.get_general_fields
        - SettingsDialog.get_editor_config_fields
        - SettingsDialog.get_viewer_config_fields
        - SettingsDialog.get_ai_config_fields
        """

        # Extract the test method name and expected parameters
        test_method_name = test_params_fixture
        exp_tab_name = test_exp_params_fixture

        # Mock the tab widget (QTabWidget instance)
        mock_tab_widget = MagicMock(spec=QTabWidget)
        mock_mock_tab_widget_add_tab = mocker.patch.object(mock_tab_widget, 'addTab')

        # Assign the mocked tab widget to the testing object
        ui_obj.tab_widget = mock_tab_widget

        # Mock QVBoxLayout's addWidget method
        mock_vbox_layout_add_widget = mocker.patch.object(QVBoxLayout, 'addWidget', return_value=None)

        # Mock the tab's main widget's setObjectName method
        mock_tab_widget_set_object_name = mocker.patch.object(QWidget, 'setObjectName')

        # Mock the scroll area containing the main tab widget
        mock_scroll_area_set_widget = mocker.patch.object(QScrollArea, 'setWidget')

        # Run the method under test
        test_method = getattr(ui_obj, str(test_method_name))
        assert callable(test_method), f"Method {test_method_name} is not callable."
        result = test_method()

        # Assert the result is of the expected type
        assert isinstance(result, list), "Expected the result to be a list."

        # Check that setObjectName methods were called with the expected parameters
        mock_tab_widget_set_object_name.assert_called_once_with(exp_tab_name)

        # Assert that the tab's main widget was added to the scroll area
        mock_scroll_area_set_widget.assert_called_once()
        assert 'QWidget' in str(mock_scroll_area_set_widget.call_args), "Expected a QWidget in the call arguments."

        # Verify that the tab was added to the tab widget
        mock_mock_tab_widget_add_tab.assert_called_once()

        # Validate the result by examining one of its dictionary values
        config_item = result.pop(0)
        assert 'callback' in config_item, "Expected 'callback' in the configuration item."
        assert callable(config_item['callback']), "Expected 'callback' to be callable."

        # Test the callback in the configuration
        mock_obj = MagicMock(spec=QObject)
        config_item['callback'](mock_obj)

        # Verify that the layout processed the callback and added the config's value to it
        mock_vbox_layout_add_widget.assert_called_once_with(mock_obj, alignment=Qt.AlignmentFlag.AlignTop)

    @pytest.mark.parametrize(
        "test_params_fixture, test_exp_params_fixture",
        [
            ({"type": HorizontalLineSpacer},
             (HorizontalLineSpacer, lambda v: True)),
            ({"type": QWidget, "size_policy": (QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)},
             (QWidget, lambda v: True)),
            ({"type": QCheckBox, "name": "obj1"},
             (QCheckBox, lambda v: v.objectName() == "obj1")),
            ({"type": QLineEdit, "placeholder_text": "text1"},
             (QLineEdit, lambda v: v.placeholderText() == "text1")),
            ({"type": QLabel, "props": {"setProperty": ("class", "class1")}},
             (QLabel, lambda v: v.property("class") == "class1")),
            ({"type": QSlider, "props": {"setTickInterval": 123}},
             (QSlider, lambda v: v.property("tickInterval") == 123)),
            ({"type": QPlainTextEdit, "text_lines": 3},
             (QPlainTextEdit, lambda v: v.height() > 1)),
            ({"type": QSpinBox, "props": {"setMinimum": 1, "setMaximum": 65536}},
             (QSpinBox, lambda v: (v.property("minimum") == 1, v.property("maximum") == 65536))),
            ({"type": QDoubleSpinBox, "props": {"setMinimum": 0.0, "setMaximum": 9.9}},
             (QDoubleSpinBox, lambda v: (v.property("minimum") == 0.0, v.property("maximum") == 9.9))),
            ({"type": QComboBox, "callback": lambda obj: obj.setProperty('param1', 'value1')},
             (QComboBox, lambda v: v.property('param1') == 'value1')),
            ({"type": EnumComboBox, "args": [
                sorted(SomethingEnum, key=lambda member: (not member.is_default, str(member.value)))]},
             (EnumComboBox, lambda v: (v.count() == 3, isinstance(v.currentIndex(), int)))),
            ({"type": LabelWithHint, "kwargs": {"tooltip": ("lexeme1_key", "lexeme1_text")}, "text": "text1"},
             (LabelWithHint, lambda v: (v.property("tooltip_lexeme") == "lexeme1_key", v.text == "text1"))),
            ({"type": DirPathLineEdit, "kwargs": {"default_directory": "dir1"}},
             (DirPathLineEdit, lambda v: (v.default_directory == "dir1"))),
            ({"type": FilePathLineEdit, "kwargs": {"ext_filter": "ext1"}},
             (FilePathLineEdit, lambda v: (v.ext_filter == "ext1"))),
        ],
        indirect=True
    )
    def test_create_setting_field(self, mocker, ui_obj: SettingsDialog, test_params_fixture, test_exp_params_fixture):
        # Extract test and expected params
        test_config = test_params_fixture
        exp_result_type, exp_check = test_exp_params_fixture

        # Run the method under test
        result_obj = ui_obj.create_setting_field(dict(test_config))

        # Assert the result is of the expected type
        assert isinstance(result_obj, exp_result_type)  # noqa

        # Test the callable check method
        assert callable(exp_check)
        assert exp_check(result_obj)
