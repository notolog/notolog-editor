# tests/test_notolog_editor.py

from PySide6.QtGui import QTextDocument

from notolog.notolog_editor import NotologEditor
from notolog.settings import Settings
from notolog.editor_state import Mode
from notolog.lexemes.lexemes import Lexemes

from unittest.mock import Mock

import pytest

import os


class TestNotologEditor:

    @pytest.fixture(scope="function")
    def test_obj_lexemes(self, mocker):
        # Return empty lexemes
        mocker.patch.object(Lexemes, 'load_lexemes', return_value={})
        # Init lexemes
        _lexemes = Lexemes()
        # Mock get lexeme results
        mocker.patch.object(_lexemes, 'get', return_value='Lorem ipsum')

        yield _lexemes

    @pytest.fixture(scope="function")
    def test_obj_notolog_editor(self, mocker, test_obj_lexemes):
        # Mock __init__ method
        mocker.patch.object(NotologEditor, '__init__', return_value=None)

        _obj = NotologEditor()
        # Set lexemes object
        setattr(_obj, 'lexemes', test_obj_lexemes)

        # Create nested mocks for toolbar.search_form
        search_form_mock = Mock()
        toolbar_mock = Mock(search_form=search_form_mock)

        # Assign the mock toolbar to the editor object
        _obj.toolbar = toolbar_mock

        yield _obj

    @pytest.fixture(scope="function")
    def test_obj_settings(self):
        yield Settings()

    def test_notolog_editor_load_default_page(self, mocker, test_obj_notolog_editor, test_obj_settings, tmp_path):
        """
        Check that the default page is loaded
        @param mocker: pytest fixture
        @param test_obj_notolog_editor: NotologEditor instance
        @param test_obj_settings: Settings instance
        @param tmp_path: fixture to get the path to a temporary directory
        @return: None
        """
        test_obj_notolog_editor.settings = test_obj_settings
        assert isinstance(test_obj_notolog_editor.settings, Settings)

        # Specify a side effect method for the mocked object
        mocker.patch('os.path.isfile', side_effect=lambda filename: filename.endswith('.md'))

        mock_method1 = mocker.patch.object(test_obj_notolog_editor, 'get_any_file', return_value=None)
        mock_method2 = mocker.patch.object(test_obj_notolog_editor, 'load_file', return_value=True)

        # Call the method under test
        result = test_obj_notolog_editor.load_default_page()
        assert result is True

        # Current working directory
        # test_run_from_dir = os.getcwd()
        test_file_dir = os.path.dirname(os.path.realpath(__file__))
        test_file_parent_dir = os.path.dirname(test_file_dir)
        # Assert that the method was called once
        mock_method1.assert_not_called()
        # Assert that the method was called once with the param(s)
        mock_method2.assert_called_once_with(os.path.normpath('%s/README.md') % test_file_parent_dir)

    def test_notolog_editor_load_default_page_any(self, mocker, test_obj_notolog_editor, test_obj_settings):
        """
        Check that an any page is loaded instead of default page
        @param mocker: pytest fixture
        @param test_obj_notolog_editor: NotologEditor instance
        @param test_obj_settings: Settings instance
        @return: None
        """
        # test_obj_notolog_editor.settings = mocker.Mock()
        test_obj_notolog_editor.settings = test_obj_settings
        assert isinstance(test_obj_notolog_editor.settings, Settings)

        mocker.patch.object(os.path, 'isfile', return_value=False)

        mock_method1 = mocker.patch.object(test_obj_notolog_editor, 'get_any_file', return_value='Test_File_Path.Py')
        mock_method2 = mocker.patch.object(test_obj_notolog_editor, 'load_file', return_value=True)

        # Call the method under test
        result = test_obj_notolog_editor.load_default_page()
        assert result is True

        # Assert that the method was called once
        mock_method1.assert_called_once()
        # Assert that the method was called once with the param(s)
        mock_method2.assert_called_once_with('Test_File_Path.Py')

    @pytest.fixture(scope="function")
    def test_exp_params_fixture(self, request):
        # Get the parameter value(s) from the request
        param_values = request.param

        yield param_values

    @pytest.mark.parametrize(
        "test_exp_params_fixture",
        [
            (Mode.VIEW, 'new-document-1.md', None, None, 1),
            (Mode.VIEW, 'new-document-1.md', False, None, 1),
            (Mode.VIEW, 'new-document-9999.md', True, None, 9999),
            (Mode.VIEW, 'new-document-1.md', False, 'Lorem ipsum', 1),
        ],
        indirect=True
    )
    def test_notolog_editor_action_new_file(self, mocker, test_obj_notolog_editor, test_exp_params_fixture):
        mode, file_path, isfile, content, res_path_call_cnt = test_exp_params_fixture

        mocker.patch.object(test_obj_notolog_editor, 'get_mode', return_value=mode)
        mocker.patch.object(test_obj_notolog_editor, 'toggle_mode', return_value=None)
        setattr(test_obj_notolog_editor, 'debug', False)

        mock_res_path = mocker.patch.object(test_obj_notolog_editor, 'get_tree_active_dir', return_value=file_path)
        # mock_res_path = mocker.patch('app.notolog_editor.res_path', return_value=file_path)
        # fixture arg: monkeypatch
        # monkeypatch.setattr('app.notolog_editor.res_path', lambda _file_path: _file_path == file_path)
        mocker.patch.object(os.path, 'isfile', return_value=isfile)

        mock_save_file_content = mocker.patch.object(test_obj_notolog_editor, 'save_file_content', return_value=None)
        mocker.patch.object(test_obj_notolog_editor, 'load_file', return_value=None)

        test_obj_notolog_editor.action_new_file(content)

        assert mock_res_path.call_count == res_path_call_cnt
        # Check the parameters passed to the mocked function(s)
        # assert str(mock_res_path.call_args) == "call('%s')" % file_path
        # assert str(mock_save_file_content.call_args) == "call('%s', '%s')" % (file_path, content)
        if content:
            assert str(content) in str(mock_save_file_content.call_args)

    @pytest.mark.parametrize(
        "test_exp_params_fixture",
        [
            (True, None, ''),
            (False, '', ''),
            (False, 'Test Text', 'Test Text'),
        ],
        indirect=True
    )
    def test_get_action_search_text(self, mocker, test_obj_notolog_editor, test_exp_params_fixture):
        param_default, param_text, text_result = test_exp_params_fixture

        setattr(test_obj_notolog_editor, 'debug', False)

        # Mock the search_form directly on the already provided fixture object
        search_form_mock = mocker.Mock()

        mocker.patch.object(test_obj_notolog_editor.toolbar, 'search_form', new=search_form_mock)
        # Set return values or side effects on this mock
        search_form_mock.text.return_value = param_text

        if param_default:
            # Force the method to use its default value by omitting the required parameter
            delattr(test_obj_notolog_editor.toolbar, 'search_form')

        result = test_obj_notolog_editor.get_action_search_text()

        assert result == text_result

        if not param_default:
            search_form_mock.text.assert_called_once()

    @pytest.mark.parametrize(
        "test_exp_params_fixture",
        [
            (None, None, QTextDocument.FindFlag(0)),
            (False, None, QTextDocument.FindFlag(0)),
            (True, None, QTextDocument.FindFlag.FindBackward),
            (False, False, QTextDocument.FindFlag(0)),
            (True, False, QTextDocument.FindFlag.FindBackward),
            (False, True, QTextDocument.FindFlag.FindCaseSensitively),
            (True, True, QTextDocument.FindFlag.FindBackward | QTextDocument.FindFlag.FindCaseSensitively),
        ],
        indirect=True
    )
    def test_get_action_search_flags(self, mocker, test_obj_notolog_editor, test_exp_params_fixture):
        param_backward, param_case_sensitive, flags_result = test_exp_params_fixture

        setattr(test_obj_notolog_editor, 'debug', False)

        # Mock the search_form directly on the already provided fixture object
        search_form_mock = mocker.Mock()
        mocker.patch.object(test_obj_notolog_editor.toolbar, 'search_form', new=search_form_mock)

        # Set return values or side effects on this mock
        search_form_mock.case_sensitive.return_value = param_case_sensitive

        result = test_obj_notolog_editor.get_action_search_flags(param_backward)

        assert result == flags_result
        search_form_mock.case_sensitive.assert_called_once()
