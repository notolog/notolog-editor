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

from PySide6.QtCore import QTimer, QDir
from PySide6.QtGui import QTextDocument

from notolog.notolog_editor import NotologEditor
from notolog.settings import Settings
from notolog.editor_state import Mode
from notolog.lexemes.lexemes import Lexemes
from notolog.edit_widget import EditWidget
from notolog.file_header import FileHeader
from notolog.encrypt.enc_helper import EncHelper
from notolog.editor_state import Encryption
from notolog.ui.message_box import MessageBox

from logging import Logger

from unittest.mock import Mock, MagicMock

from types import SimpleNamespace

import pytest

import os


class TestNotologEditor:

    @pytest.fixture(scope="function")
    def test_obj_lexemes(self, mocker):
        # Return empty lexemes
        mocker.patch.object(Lexemes, 'load_lexemes', return_value={})
        # Initialize lexemes
        _lexemes = Lexemes()
        # Mock get lexeme results
        mocker.patch.object(_lexemes, 'get', return_value='Lorem ipsum')

        yield _lexemes

    @pytest.fixture(scope="function")
    def test_obj_notolog_editor(self, mocker, test_obj_lexemes):
        # Mock __init__ method
        mocker.patch.object(NotologEditor, '__init__', return_value=None)
        # Prevent resource processing
        mocker.patch.object(NotologEditor, 'process_document_images', return_value=None)
        # Activate quiet mode
        mocker.patch.object(NotologEditor, 'is_quiet_mode', return_value=True)

        _obj = NotologEditor()
        # Set lexemes object
        setattr(_obj, 'lexemes', test_obj_lexemes)

        _logger = MagicMock(spec=Logger)
        # Set logger
        setattr(_obj, 'logger', _logger)

        # Create nested mocks for toolbar.search_form
        search_form_mock = Mock()
        toolbar_mock = Mock(search_form=search_form_mock)

        # Assign the mock toolbar to the editor object
        _obj.toolbar = toolbar_mock

        yield _obj

    @pytest.fixture(scope="function")
    def test_obj_settings(self):
        yield Settings()

    @pytest.fixture(scope="function")
    def test_params_fixture(self, request):
        # Retrieve parameter values from the test request.
        param_values = request.param

        yield param_values

    @pytest.fixture(scope="function")
    def test_exp_params_fixture(self, request):
        """
        Fixture to pass params and get expected results.
        This method is used only for passing params via pytest fixture.
        """
        # Retrieve parameter values from the test request.
        param_values = request.param

        yield param_values

    def test_notolog_editor_load_default_page(self, mocker, test_obj_notolog_editor, test_obj_settings):
        """
        Check that the default page is loaded
        @param mocker: pytest fixture
        @param test_obj_notolog_editor: NotologEditor instance
        @param test_obj_settings: Settings instance
        @return: None
        """
        test_obj_notolog_editor.settings = test_obj_settings
        assert isinstance(test_obj_notolog_editor.settings, Settings)

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

    @pytest.mark.parametrize(
        "test_params_fixture, test_exp_params_fixture",
        [
            ((None, {'README.md': True, 'Test_File_Path.Py': True}),  # Test params
             (False, True, False, 'README.md')),  # Expected params
            (('Test_File_Path.Py', {'README.md': False, 'Test_File_Path.Py': True}),  # Test params
             (True, True, False, 'Test_File_Path.Py')),  # Expected params
            (('Test_File_Path.Py', {'README.md': False, 'Test_File_Path.Py': False}),  # Test params
             (True, False, True, 'Test_File_Path.Py')),  # Expected params
        ],
        indirect=True
    )
    def test_notolog_editor_load_default_page_any(self, mocker, test_obj_notolog_editor, test_obj_settings,
                                                  test_params_fixture, test_exp_params_fixture):
        """
        Check that an any page is loaded instead of the default page
        @param mocker: pytest fixture
        @param test_obj_notolog_editor: NotologEditor instance
        @param test_obj_settings: Settings instance
        @param test_params_fixture: Test params
        @param test_exp_params_fixture: Expected params
        @return: None
        """

        any_file_path, is_file_openable_map = test_params_fixture
        get_any_file_called, load_file_called, action_new_file_called, exp_file_path = test_exp_params_fixture

        # test_obj_notolog_editor.settings = mocker.Mock()
        test_obj_notolog_editor.settings = test_obj_settings
        assert isinstance(test_obj_notolog_editor.settings, Settings)

        # Specify a side effect method for the mocked object
        mocker.patch('os.path.dirname', return_value='')  # To assert that the function is only checking the filename
        mocker.patch('notolog.helpers.file_helper.is_file_openable',
                     side_effect=lambda k: is_file_openable_map.get(k, None))

        mock_method1 = mocker.patch.object(test_obj_notolog_editor, 'get_any_file', return_value=any_file_path)
        mock_method2 = mocker.patch.object(test_obj_notolog_editor, 'load_file', return_value=True)
        mock_method3 = mocker.patch.object(test_obj_notolog_editor, 'action_new_file', return_value=True)

        # Call the method under test
        result = test_obj_notolog_editor.load_default_page()
        assert result is True

        if get_any_file_called:
            # Assert that the method was called once
            mock_method1.assert_called_once()
        else:
            mock_method1.assert_not_called()

        if load_file_called:
            # Assert that the method was called once with the param(s)
            mock_method2.assert_called_once_with(exp_file_path)
        else:
            mock_method2.assert_not_called()

        if action_new_file_called:
            # Assert that the method was called once
            mock_method3.assert_called_once()
        else:
            mock_method3.assert_not_called()

    @pytest.mark.parametrize(
        "test_params_fixture, test_exp_params_fixture",
        [
            ((None, QDir.homePath()),  # Test params
             QDir.homePath()),  # Expected params
            (('Test_Dir_Path', QDir.homePath()),  # Test params
             'Test_Dir_Path'),  # Expected params
        ],
        indirect=True
    )
    def test_notolog_editor_load_default_page_nothing(self, mocker, test_obj_notolog_editor, test_obj_settings,
                                                      test_params_fixture, test_exp_params_fixture):
        """
        Check that the default page is loaded
        @param mocker: pytest fixture
        @param test_obj_notolog_editor: NotologEditor instance
        @param test_obj_settings: Settings instance
        @param test_params_fixture: Test params
        @param test_exp_params_fixture: Expected params
        @return: None
        """

        settings_default_path, home_dir_path = test_params_fixture
        exp_default_path = test_exp_params_fixture

        test_obj_notolog_editor.settings = test_obj_settings
        assert isinstance(test_obj_notolog_editor.settings, Settings)

        # Mock the settings object
        settings = MagicMock(spec=Settings)
        setattr(settings, 'default_path', settings_default_path)
        test_obj_notolog_editor.settings = settings

        mocker.patch('notolog.helpers.file_helper.is_file_openable', return_value=False)

        mock_method1 = mocker.patch.object(test_obj_notolog_editor, 'get_any_file', return_value=None)
        mock_method2 = mocker.patch.object(test_obj_notolog_editor, 'load_file', return_value=None)
        mock_method3 = mocker.patch.object(test_obj_notolog_editor, 'action_new_file', return_value=False)
        mock_method4 = mocker.patch.object(test_obj_notolog_editor, 'set_current_path', return_value=True)
        mock_method5 = mocker.patch.object(test_obj_notolog_editor, 'confirm_current_path', return_value=True)

        # Call the method under test
        result = test_obj_notolog_editor.load_default_page()
        assert result is False

        # Assert that the method was called once
        mock_method1.assert_called_once()
        # Assert that the method wasn't called
        mock_method2.assert_not_called()
        # Assert that the method was called once
        mock_method3.assert_called_once()
        # Assert that the methods were called once
        mock_method4.assert_called_once_with(exp_default_path)
        mock_method5.assert_called_once()

    @pytest.mark.parametrize(
        "test_exp_params_fixture",
        [
            (Mode.VIEW, 'new-document-1.md', None, None, 1, True, True, True),
            (Mode.VIEW, 'new-document-1.md', None, None, 1, True, False, False),
            (Mode.VIEW, 'new-document-1.md', None, None, 1, False, None, False),
            (Mode.VIEW, 'new-document-1.md', False, None, 1, True, True, True),
            (Mode.VIEW, 'new-document-9999.md', True, None, 9999, True, True, False),
            (Mode.VIEW, 'new-document-1.md', False, 'Lorem ipsum', 1, True, True, True),
            (Mode.VIEW, 'new-document-1.md', False, 'Lorem ipsum', 1, True, False, False),
        ],
        indirect=True
    )
    def test_notolog_editor_action_new_file(self, mocker, test_obj_notolog_editor, test_exp_params_fixture):
        # Expected params
        mode, file_path, isfile, content, res_path_call_cnt, res_save_file, is_file_openable, res_exp\
            = test_exp_params_fixture

        mocker.patch.object(test_obj_notolog_editor, 'get_mode', return_value=mode)
        mocker.patch.object(test_obj_notolog_editor, 'toggle_mode', return_value=None)
        setattr(test_obj_notolog_editor, 'debug', False)
        setattr(test_obj_notolog_editor, 'logging', False)

        # Message box
        MessageBox.__new__ = MagicMock(return_value=None)

        mock_res_path = mocker.patch.object(test_obj_notolog_editor, 'get_tree_active_dir', return_value=file_path)
        # fixture arg: monkeypatch
        # monkeypatch.setattr('app.notolog_editor.res_path', lambda _file_path: _file_path == file_path)
        mocker.patch.object(os.path, 'isfile', return_value=isfile)
        mocker.patch('notolog.helpers.file_helper.is_file_openable', return_value=is_file_openable)

        mock_save_file_content = mocker.patch.object(test_obj_notolog_editor, 'save_file_content', return_value=res_save_file)
        mocker.patch.object(test_obj_notolog_editor, 'load_file', return_value=True)

        result = test_obj_notolog_editor.action_new_file(content)

        assert result == res_exp
        assert mock_res_path.call_count == res_path_call_cnt
        # Check the parameters passed to the mocked function(s)
        # assert str(mock_res_path.call_args) == "call('%s')" % file_path
        # assert str(mock_save_file_content.call_args) == "call('%s', '%s')" % (file_path, content)
        if content:
            assert str(content) in str(mock_save_file_content.call_args)

    @pytest.mark.parametrize(
        "test_exp_params_fixture",
        [
            # mode, encryption, file_path, file_exists, file_write_ok, dir_write_ok
            (None, None, 'some-doc-1.md', None, None, None,
             # content, prev_content, clear_after, allow_save_empty_content, res_save_file, res_exp
             '', None, None, None, None, None),
            # Verify behavior when running in an unexpected mode
            (Mode.VIEW, Encryption.PLAIN, 'some-doc-1.md', False, False, False,
             '', None, False, None, False, None),
            (Mode.VIEW, Encryption.PLAIN, 'some-doc-1.md', False, False, False,
             'Lorem ipsum', 'To be or not to be?', False, None, False, None),
            # Manage scenarios involving saving empty content to the file
            (Mode.EDIT, Encryption.PLAIN, 'some-doc-1.md', None, None, None,
             '', None, False, None, False, False),
            (Mode.EDIT, Encryption.PLAIN, 'some-doc-1.md', True, True, True,
             '', 'Essentiam vel non essentiam? Hoc quaestio est.', False, None, False, None),
            (Mode.EDIT, Encryption.PLAIN, 'some-doc-1.md', True, True, True,
             '', 'Essentiam vel non essentiam? Hoc quaestio est.', False, True, False, False),
            (Mode.EDIT, Encryption.PLAIN, 'some-doc-1.md', True, True, True,
             '', 'Essentiam vel non essentiam? Hoc quaestio est.', False, True, True, True),
            # Insufficient permissions to save the file
            (Mode.EDIT, Encryption.PLAIN, 'some-doc-1.md', False, False, False,
             'Lorem ipsum', 'To be or not to be?', False, None, False, False),
            (Mode.EDIT, Encryption.PLAIN, 'some-doc-1.md', True, False, True,
             'Lorem ipsum', 'To be or not to be?', False, None, False, False),
            (Mode.EDIT, Encryption.ENCRYPTED, 'some-doc-1.md', False, False, False,
             'Lorem ipsum', 'To be or not to be?', False, None, False, False),
            # Handle other unexpected errors when saving the file
            (Mode.EDIT, Encryption.ENCRYPTED, 'some-doc-1.md', True, True, True,
             'Lorem ipsum', 'To be or not to be?', False, None, False, False),
            # Handle cases where the file can be saved
            (Mode.EDIT, Encryption.PLAIN, 'some-doc-1.md', False, True, True,
             'Lorem ipsum', 'To be or not to be?', False, None, True, True),
            (Mode.EDIT, Encryption.PLAIN, 'some-doc-1.md', True, True, False,
             'Lorem ipsum', 'To be or not to be?', False, None, True, True),
            (Mode.EDIT, Encryption.PLAIN, 'some-doc-1.md', True, True, True,
             'Lorem ipsum', 'To be or not to be?', False, None, True, True),
            (Mode.EDIT, Encryption.ENCRYPTED, 'some-doc-1.md', True, True, True,
             'Lorem ipsum', 'To be or not to be?', False, None, True, True),
            (Mode.EDIT, Encryption.ENCRYPTED, 'some-doc-1.md', True, True, True,
             'Lorem ipsum', 'To be or not to be?', True, None, True, True),
        ],
        indirect=True
    )
    def test_notolog_editor_save_active_file(self, mocker, test_obj_notolog_editor, test_exp_params_fixture):
        (mode, encryption, file_path, file_exists, file_write_ok, dir_write_ok, content, prev_content,
         clear_after, allow_save_empty_content, res_save_file, res_exp) \
            = test_exp_params_fixture

        mocker.patch.object(test_obj_notolog_editor, 'get_mode', return_value=mode)
        mocker.patch.object(test_obj_notolog_editor, 'toggle_mode', return_value=None)
        setattr(test_obj_notolog_editor, 'debug', False)
        setattr(test_obj_notolog_editor, 'logging', False)

        mocker.patch.object(test_obj_notolog_editor, 'get_current_file_path', return_value=file_path)

        mock_store_doc_cursor_pos = mocker.patch.object(test_obj_notolog_editor, 'store_doc_cursor_pos',
                                                        return_value=None)
        mock_toggle_save_timer = mocker.patch.object(test_obj_notolog_editor, 'toggle_save_timer', return_value=None)
        mock_common_dialog = mocker.patch.object(test_obj_notolog_editor, 'common_dialog', return_value=None)
        mock_get_encryption = mocker.patch.object(test_obj_notolog_editor, 'get_encryption', return_value=encryption)

        # Message box
        mock_message_box = MessageBox.__new__ = MagicMock(return_value=None)

        mock_edit_widget = MagicMock(spec=EditWidget)
        mock_edit_widget_to_plain_text = mocker.patch.object(mock_edit_widget, 'toPlainText', return_value=content)
        mock_edit_widget_clear = mocker.patch.object(mock_edit_widget, 'clear', return_value=None)
        mocker.patch.object(test_obj_notolog_editor, 'get_edit_widget', return_value=mock_edit_widget)

        setattr(test_obj_notolog_editor, 'content', prev_content)
        setattr(test_obj_notolog_editor, 'estate', SimpleNamespace(**{'allow_save_empty': allow_save_empty_content}))

        mock_save_timer_ui_icon = mocker.patch.object(QTimer, 'singleShot', return_value=None)

        # Handle file system permissions
        mocker.patch.object(os.path, 'exists', return_value=file_exists)
        write_permissions_matrix = {file_path: file_write_ok, os.path.dirname(file_path): dir_write_ok}
        mocker.patch.object(os, 'access',
                            side_effect=lambda key, _mode: getattr(SimpleNamespace(**write_permissions_matrix), key, None))

        # Lexemes
        mock_lexemes_get = mocker.patch.object(test_obj_notolog_editor.lexemes, 'get')

        # Process the file's header information
        mock_header = MagicMock(spec=FileHeader)
        mock_header_refresh = mocker.patch.object(mock_header, 'refresh', return_value=None)
        mock_header_pack = mocker.patch.object(mock_header, 'pack', wraps=mock_header.pack)
        header_line_tpl = '<!-- %s -->'  # To simplify the emulation of header processing operations
        mocker.patch.object(mock_header, '__repr__', return_value=(header_line_tpl % file_path))
        mocker.patch.object(mock_header, 'is_valid', return_value=True)
        mock_header_validate_enc = mocker.patch.object(mock_header, 'validate_enc', return_value=None)
        mocker.patch.object(mock_header, 'get_enc_param',
                            side_effect=lambda key: getattr(SimpleNamespace(**{'slt': 'any-salt', 'itr': 1}), key, None))
        setattr(test_obj_notolog_editor, 'header', mock_header)

        mock_enc_helper = MagicMock(spec=EncHelper)
        mock_enc_helper_encrypt_data = mocker.patch.object(mock_enc_helper, 'encrypt_data',
                                                           return_value=('ENCRYPTED' + content).encode('utf-8'))
        mock_get_encrypt_helper = mocker.patch.object(test_obj_notolog_editor, 'get_encrypt_helper',
                                                      return_value=mock_enc_helper)

        mock_save_file_content = mocker.patch.object(test_obj_notolog_editor, 'save_file_content',
                                                     return_value=res_save_file)

        # Save the active file
        result = test_obj_notolog_editor.save_active_file(clear_after, allow_save_empty_content)

        assert result == res_exp
        mock_store_doc_cursor_pos.assert_called_once()

        if res_save_file:
            mock_header_refresh.assert_called_once()
            mock_header_pack.assert_called_once()
            # Verify the parameters passed to the mocked function(s)
            # assert str(mock_res_path.call_args) == "call('%s')" % file_path
            # assert str(mock_save_file_content.call_args) == "call('%s', '%s')" % (file_path, content)
            assert str(content) in str(mock_header_pack.call_args)
            mock_edit_widget_to_plain_text.assert_called_once()
            assert mock_edit_widget_clear.call_count == int(clear_after)
            mock_get_encryption.assert_called_once()
            mock_toggle_save_timer.assert_not_called()
            mock_message_box.assert_not_called()
            assert test_obj_notolog_editor.content == content
            assert repr(test_obj_notolog_editor.header) == header_line_tpl % file_path
            # Encrypted file
            if encryption == Encryption.ENCRYPTED:
                mock_header_validate_enc.assert_called_once()
                mock_get_encrypt_helper.assert_called_once_with(salt='any-salt', iterations=1)
                mock_enc_helper_encrypt_data.assert_called_once_with(content.encode('utf-8'))
            else:
                mock_header_validate_enc.assert_not_called()
                mock_get_encrypt_helper.assert_not_called()
        elif mock_save_timer_ui_icon.call_count > 0:
            mock_message_box.assert_called_once()
            # Checks if the method was called with the parameter at least once
            mock_lexemes_get.assert_any_call('save_active_file_error_occurred')

        if (file_exists and file_write_ok) or (not file_exists and dir_write_ok):
            if not content:
                if allow_save_empty_content:
                    mock_save_timer_ui_icon.assert_called_once()
                else:
                    mock_save_timer_ui_icon.assert_not_called()
                    mock_common_dialog.assert_called_once()
                    # Checks if the method was called with the parameter at least once
                    mock_lexemes_get.assert_any_call('dialog_save_empty_file_title')
            elif mode == Mode.EDIT:
                mock_save_file_content.assert_called_once()
                mock_save_timer_ui_icon.assert_called_once()
                if res_save_file:
                    # No lexemes were retrieved for any dialog
                    mock_lexemes_get.assert_not_called()

        if not file_exists and not dir_write_ok and mode == Mode.EDIT:
            mock_toggle_save_timer.assert_called_once()
            mock_message_box.assert_called_once()
            # Checks if the method was called with the parameter at least once
            mock_lexemes_get.assert_any_call('save_active_file_error_occurred')

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

    def test_is_quiet_mode(self, test_obj_notolog_editor):
        assert test_obj_notolog_editor.is_quiet_mode()
