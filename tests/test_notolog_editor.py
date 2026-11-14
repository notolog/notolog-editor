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

from PySide6.QtCore import QTimer, QDir
from PySide6.QtCore import Qt, QSortFilterProxyModel, QUrl
from PySide6.QtGui import QTextDocument, QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QListView, QPlainTextEdit

from notolog.notolog_editor import NotologEditor
from notolog.settings import Settings
from notolog.editor_state import Mode
from notolog.lexemes.lexemes import Lexemes
from notolog.edit_widget import EditWidget
from notolog.file_header import FileHeader
from notolog.encrypt.enc_helper import EncHelper
from notolog.encrypt.enc_password import EncPassword
from notolog.editor_state import Encryption
from notolog.ui.message_box import MessageBox
from notolog.ui.statusbar import StatusBar

from logging import Logger

from unittest.mock import Mock, MagicMock

from types import SimpleNamespace

import pytest
import asyncio

import os
import logging


class TestNotologEditor:

    @pytest.fixture
    def file_switch(self, qapp, mocker, test_obj_notolog_editor, tmp_path):
        editor = test_obj_notolog_editor
        source = tmp_path / 'active.md'
        target = tmp_path / 'locked.enc'
        source.write_text('original text', encoding='utf-8')
        header = FileHeader().get_new(is_enc=True)
        header.set_enc_param('itr', 1024)
        password = EncPassword()
        password.password = 'synthetic-switch-password'
        helper = EncHelper(password, header.get_enc_param('slt'), header.get_enc_param('itr'))
        target.write_text(header.pack(helper.encrypt_data(b'locked document').decode()), encoding='utf-8')

        model = QStandardItemModel()
        paths = [str(source), str(target)]
        for path in paths:
            item = QStandardItem(os.path.basename(path))
            item.setData(path, Qt.ItemDataRole.UserRole)
            model.appendRow(item)
        proxy = QSortFilterProxyModel()
        proxy.setSourceModel(model)
        tree = QListView()
        tree.setModel(proxy)
        editor.tree_view = tree
        editor.tree_proxy_model = proxy
        editor.file_model = Mock()
        editor.file_model.index.side_effect = lambda path: model.index(paths.index(path), 0)
        editor.file_model.filePath.side_effect = lambda index: index.data(Qt.ItemDataRole.UserRole)
        editor.file_watcher = Mock()
        editor.theme_helper = Mock()
        editor.history_manager = Mock()
        editor.file_path = str(source)
        editor.header = FileHeader()
        editor.content = 'original text'
        editor.estate = SimpleNamespace(mode=Mode.EDIT, encryption=Encryption.PLAIN, allow_save_empty=None)
        editor.enc_password = None
        editor.encrypt_helpers = {}
        editor.line_num = 2
        editor.col_num = 3
        editor.settings = SimpleNamespace(file_path=str(source), line_num=2, col_num=3,
                                         cursor_pos=5, viewport_pos=[0, 7])
        widget = QPlainTextEdit()
        widget.setPlainText(editor.content)
        cursor = widget.textCursor()
        cursor.setPosition(5)
        widget.setTextCursor(cursor)
        mocker.patch.object(editor, 'get_edit_widget', return_value=widget)
        mocker.patch.object(editor, 'adjust_tree_current_root_index')
        mocker.patch.object(QTimer, 'singleShot')
        fallback = mocker.patch.object(editor, 'load_default_page', return_value=True)
        message = mocker.patch('notolog.notolog_editor.MessageBox')
        editor.set_current_path(str(source))
        yield SimpleNamespace(editor=editor, source=source, target=target, widget=widget,
                              tree=tree, proxy=proxy, model=model, password=password,
                              fallback=fallback, message=message)
        tree.deleteLater()
        widget.deleteLater()

    @pytest.mark.parametrize('route', ['tree', 'open'])
    def test_password_cancel_keeps_active_document_and_autosave_target(self, file_switch, mocker, route):
        switch = file_switch
        editor = switch.editor
        encrypted_bytes = switch.target.read_bytes()
        original_header = editor.header

        def cancel_password(**kwargs):
            # The modal dialog's event loop can deliver the autosave timer.
            assert editor.get_current_file_path() == str(switch.source)
            assert switch.tree.currentIndex().data(Qt.ItemDataRole.UserRole) == str(switch.target)
            assert [index.data(Qt.ItemDataRole.UserRole) for index in switch.tree.selectedIndexes()] == [str(switch.target)]
            assert editor.get_encryption() == Encryption.PLAIN
            assert switch.widget.toPlainText() == 'original text'
            switch.widget.setPlainText('changed during password prompt')
            cursor = switch.widget.textCursor()
            cursor.setPosition(5)
            switch.widget.setTextCursor(cursor)
            editor.auto_save_file()
            assert switch.source.read_text(encoding='utf-8') == 'changed during password prompt'
            assert switch.target.read_bytes() == encrypted_bytes
            return None

        mocker.patch.object(editor, 'enc_password_dialog', side_effect=cancel_password)
        if route == 'tree':
            switch.tree.setCurrentIndex(switch.proxy.index(1, 0))
            editor.action_nav_select_file(switch.proxy.index(1, 0))
        else:
            editor.safely_open_file(str(switch.target))

        assert editor.file_path == editor.settings.file_path == str(switch.source)
        assert switch.tree.currentIndex().data(Qt.ItemDataRole.UserRole) == str(switch.source)
        assert [index.data(Qt.ItemDataRole.UserRole) for index in switch.tree.selectedIndexes()] == [str(switch.source)]
        assert editor.get_mode() == Mode.EDIT
        assert editor.get_encryption() == Encryption.PLAIN
        assert repr(editor.header) == repr(original_header)
        assert switch.widget.toPlainText() == editor.content == 'changed during password prompt'
        assert switch.widget.textCursor().position() == 5
        assert (editor.settings.line_num, editor.settings.col_num) == (2, 3)
        assert (editor.settings.cursor_pos, editor.settings.viewport_pos) == (5, [0, 7])
        assert switch.target.read_bytes() == encrypted_bytes
        editor.history_manager.add_file.assert_not_called()
        editor.file_watcher.addPath.assert_called_with(str(switch.source))
        assert all(call.args != (str(switch.target),) for call in editor.file_watcher.addPath.call_args_list)
        switch.fallback.assert_not_called()
        switch.message.assert_not_called()

    def test_successful_unlock_commits_file_and_selection(self, file_switch, mocker):
        switch = file_switch
        editor = switch.editor

        def accept_password(**kwargs):
            assert switch.tree.currentIndex().data(Qt.ItemDataRole.UserRole) == str(switch.target)
            assert editor.file_path == editor.settings.file_path == str(switch.source)
            return switch.password

        mocker.patch.object(editor, 'enc_password_dialog', side_effect=accept_password)

        def load_content(header, content):
            assert editor.file_path == str(switch.target)
            assert editor.get_encryption() == Encryption.ENCRYPTED
            editor.header, editor.content = header, content
            switch.widget.setPlainText(content)

        mocker.patch.object(editor, 'load_content', side_effect=load_content)
        editor.action_nav_select_file(switch.proxy.index(1, 0))

        assert editor.file_path == editor.settings.file_path == str(switch.target)
        assert switch.tree.currentIndex().data(Qt.ItemDataRole.UserRole) == str(switch.target)
        assert switch.widget.toPlainText() == editor.content == 'locked document'
        assert (editor.settings.line_num, editor.settings.col_num, editor.settings.cursor_pos) == (0, 0, 0)
        editor.history_manager.add_file.assert_called_once_with(str(switch.target))

    def test_password_prompt_previews_another_folder_without_changing_document_base(self, file_switch, mocker):
        switch = file_switch
        editor = switch.editor
        folder = switch.target.parent / 'other'
        folder.mkdir()
        target = folder / switch.target.name
        target.write_bytes(switch.target.read_bytes())
        folder_item = QStandardItem('other')
        folder_item.setData(str(folder), Qt.ItemDataRole.UserRole)
        target_item = QStandardItem(target.name)
        target_item.setData(str(target), Qt.ItemDataRole.UserRole)
        folder_item.appendRow(target_item)
        switch.model.appendRow(folder_item)
        editor.file_model.index.side_effect = lambda path: (
            target_item.index() if path == str(target) else switch.model.index(0, 0))
        document = QTextDocument()
        base_url = QUrl.fromLocalFile(str(switch.source.parent) + os.sep)
        document.setBaseUrl(base_url)
        mocker.patch.object(editor, 'get_view_doc', return_value=document)

        def cancel_password(**kwargs):
            assert switch.tree.currentIndex().data(Qt.ItemDataRole.UserRole) == str(target)
            assert switch.tree.rootIndex().data(Qt.ItemDataRole.UserRole) == str(folder)
            assert editor.tree_active_dir == str(folder)
            assert editor.file_path == editor.settings.file_path == str(switch.source)
            assert document.baseUrl() == base_url
            return None

        mocker.patch.object(editor, 'enc_password_dialog', side_effect=cancel_password)
        editor.safely_open_file(str(target))

        assert switch.tree.currentIndex().data(Qt.ItemDataRole.UserRole) == str(switch.source)
        assert not switch.tree.rootIndex().isValid()
        assert editor.tree_active_dir == str(switch.source.parent)
        assert document.baseUrl() == base_url

    @pytest.mark.parametrize('mode', [Mode.VIEW, Mode.SOURCE])
    def test_password_cancel_keeps_view_mode_and_cursor(self, file_switch, mocker, mode):
        editor = file_switch.editor
        editor.estate.mode = mode
        mocker.patch.object(editor, 'enc_password_dialog', return_value=None)

        assert editor.load_file(str(file_switch.target)) is False

        assert editor.get_mode() == mode
        assert editor.content == 'original text'
        assert editor.file_path == editor.settings.file_path == str(file_switch.source)
        assert file_switch.tree.currentIndex().data(Qt.ItemDataRole.UserRole) == str(file_switch.source)
        assert (editor.settings.cursor_pos, editor.settings.viewport_pos) == (5, [0, 7])
        file_switch.fallback.assert_not_called()

    def test_failed_password_limit_restores_active_path(self, file_switch, mocker):
        editor = file_switch.editor
        wrong_password = EncPassword()
        wrong_password.password = 'synthetic-wrong-password'
        editor.enc_password_dialog_cnt = 3
        mocker.patch.object(editor, 'enc_password_dialog', return_value=wrong_password)

        assert editor.load_file(str(file_switch.target)) is False

        assert editor.file_path == editor.settings.file_path == str(file_switch.source)
        assert file_switch.tree.currentIndex().data(Qt.ItemDataRole.UserRole) == str(file_switch.source)
        assert editor.content == 'original text'
        file_switch.fallback.assert_not_called()

    def test_startup_password_cancel_uses_default_page(self, file_switch, mocker):
        editor = file_switch.editor
        editor.file_path = None
        editor.header = None
        editor.content = None
        mocker.patch.object(editor, 'enc_password_dialog', return_value=None)

        editor.load_file(str(file_switch.target))

        file_switch.fallback.assert_called_once_with(ignore_settings=True)

    @pytest.fixture
    def encrypted_file_switch(self, file_switch):
        editor = file_switch.editor
        active_header = FileHeader().get_new(is_enc=True)
        active_header.set_enc_param('itr', 1024)
        password = EncPassword()
        password.password = 'synthetic-active-password'
        helper = EncHelper(password, active_header.get_enc_param('slt'), active_header.get_enc_param('itr'))
        original = active_header.pack(helper.encrypt_data(editor.content.encode()).decode())
        file_switch.source.write_text(original, encoding='utf-8')
        editor.header = active_header
        editor.enc_password = password
        editor.encrypt_helpers = {active_header.get_enc_param('slt'): helper}
        editor.estate.encryption = Encryption.ENCRYPTED
        file_switch.active_helper = helper
        file_switch.active_password = password
        return file_switch

    @pytest.mark.parametrize('result', ['cancel', 'reject_reset', 'wrong_password', 'missing_target', 'success'])
    def test_password_switch_preserves_active_key_until_commit(self, encrypted_file_switch, mocker, result):
        switch = encrypted_file_switch
        editor = switch.editor
        active_header = editor.header
        original = switch.source.read_bytes()
        target_bytes = switch.target.read_bytes()

        def reset_password(reset_callback):
            assert editor.enc_password is switch.active_password
            if result != 'reject_reset':
                reset_callback()

        wrong_password = EncPassword()
        wrong_password.password = 'synthetic-wrong-password'

        def enter_password(**kwargs):
            assert editor.enc_password is switch.active_password
            assert editor.encrypt_helpers[active_header.get_enc_param('slt')] is switch.active_helper
            assert editor.file_path == str(switch.source)
            assert switch.tree.currentIndex().data(Qt.ItemDataRole.UserRole) == str(switch.target)
            # Exercise autosave inside the dialog, including after requesting a password reset.
            switch.widget.setPlainText('updated original document')
            editor.auto_save_file()
            _, body = FileHeader().load_file(str(switch.source))
            assert switch.active_helper.decrypt_data(body.encode()) == b'updated original document'
            assert switch.target.read_bytes() == target_bytes
            if result == 'missing_target':
                switch.target.unlink()
            return {'cancel': None, 'wrong_password': wrong_password}.get(result, switch.password)

        reset = mocker.patch.object(editor, 'enc_password_reset_dialog', side_effect=reset_password)
        prompt = mocker.patch.object(editor, 'enc_password_dialog', side_effect=enter_password)

        def load_content(header, body):
            editor.header, editor.content = header, body
            switch.widget.setPlainText(body)

        load = mocker.patch.object(editor, 'load_content', side_effect=load_content)
        assert editor.load_file(str(switch.target)) is (result == 'success')
        reset.assert_called_once()
        assert editor.enc_password_dialog_cnt == 0
        assert prompt.call_count == (0 if result == 'reject_reset' else 3 if result == 'wrong_password' else 1)

        if result == 'success':
            assert editor.file_path == editor.settings.file_path == str(switch.target)
            assert editor.enc_password is switch.password
            switch.widget.setPlainText('updated target document')
            assert editor.save_active_file() is True
            header, body = FileHeader().load_file(str(switch.target))
            helper = EncHelper(switch.password, header.get_enc_param('slt'), header.get_enc_param('itr'))
            assert helper.decrypt_data(body.encode()) == b'updated target document'
            return

        load.assert_not_called()
        assert editor.file_path == editor.settings.file_path == str(switch.source)
        assert switch.tree.currentIndex().data(Qt.ItemDataRole.UserRole) == str(switch.source)
        assert editor.header is active_header
        assert editor.get_encryption() == Encryption.ENCRYPTED
        assert editor.enc_password is switch.active_password
        assert editor.encrypt_helpers[active_header.get_enc_param('slt')] is switch.active_helper
        if result == 'reject_reset':
            assert switch.source.read_bytes() == original
        switch.fallback.assert_not_called()
        editor.history_manager.add_file.assert_not_called()

        # Saving after cancellation must keep the original password without asking again.
        prompt.reset_mock()
        switch.widget.setPlainText('saved after cancellation')
        assert editor.save_active_file() is True
        _, body = FileHeader().load_file(str(switch.source))
        assert switch.active_helper.decrypt_data(body.encode()) == b'saved after cancellation'
        prompt.assert_not_called()

        destination = switch.source.parent / 'saved-copy.md'
        editor.supported_file_extensions = ['md', 'enc']
        mocker.patch('notolog.notolog_editor.QFileDialog.getSaveFileName', return_value=(str(destination), ''))
        editor.action_save_as_file()
        _, body = FileHeader().load_file(str(destination))
        assert switch.active_helper.decrypt_data(body.encode()) == b'saved after cancellation'
        prompt.assert_not_called()

    @pytest.mark.parametrize('change', ['deleted', 'unreadable'])
    def test_target_unavailable_after_unlock_keeps_active_document(self, file_switch, mocker, change):
        switch = file_switch
        editor = switch.editor
        source_bytes = switch.source.read_bytes()
        original_header = editor.header

        def accept_password(**kwargs):
            if change == 'deleted':
                switch.target.unlink()
            else:
                # Simulate permissions changing at the final path check, independently of the host user.
                mocker.patch('notolog.notolog_editor.file_helper.is_file_openable',
                             side_effect=lambda path: path != str(switch.target))
            return switch.password

        mocker.patch.object(editor, 'enc_password_dialog', side_effect=accept_password)
        load = mocker.patch.object(editor, 'load_content')

        assert editor.load_file(str(switch.target)) is False

        load.assert_not_called()
        assert editor.file_path == editor.settings.file_path == str(switch.source)
        assert switch.tree.currentIndex().data(Qt.ItemDataRole.UserRole) == str(switch.source)
        assert editor.header is original_header
        assert editor.content == switch.widget.toPlainText() == 'original text'
        assert editor.get_encryption() == Encryption.PLAIN
        assert editor.enc_password is None
        assert editor.encrypt_helpers == {}
        assert switch.source.read_bytes() == source_bytes
        assert (editor.settings.line_num, editor.settings.col_num, editor.settings.cursor_pos) == (2, 3, 5)
        editor.history_manager.add_file.assert_not_called()
        switch.message.assert_called_once()

    @pytest.mark.parametrize('body', ['', 'plain document'])
    def test_plain_file_load_preserves_source(self, file_switch, mocker, body):
        switch = file_switch
        switch.target.write_text(body, encoding='utf-8')
        load = mocker.patch.object(switch.editor, 'load_content')
        prompt = mocker.patch.object(switch.editor, 'enc_password_dialog')

        assert switch.editor.load_file(str(switch.target)) is True

        assert load.call_args.args[1] == body
        assert switch.editor.file_path == switch.editor.settings.file_path == str(switch.target)
        assert switch.editor.get_encryption() == Encryption.PLAIN
        prompt.assert_not_called()

    def test_password_retry_succeeds_without_recursive_loading(self, file_switch, mocker):
        switch = file_switch
        wrong = EncPassword()
        wrong.password = 'synthetic-wrong-password'
        prompt = mocker.patch.object(switch.editor, 'enc_password_dialog', side_effect=[wrong, switch.password])
        load = mocker.patch.object(switch.editor, 'load_content')

        assert switch.editor.load_file(str(switch.target)) is True

        assert prompt.call_count == 2
        switch.message.assert_called_once()
        load.assert_called_once()
        assert load.call_args.args[1] == 'locked document'
        assert switch.editor.enc_password is switch.password
        assert switch.editor.enc_password_dialog_cnt == 0

    def test_successful_load_keeps_header_state_if_file_disappears_after_path_commit(self, file_switch, mocker):
        switch = file_switch
        editor = switch.editor
        mocker.patch.object(editor, 'enc_password_dialog', return_value=switch.password)

        def load_content(header, body):
            assert editor.file_path == str(switch.target)
            editor.header, editor.content = header, body
            switch.widget.setPlainText(body)
            switch.target.unlink()

        mocker.patch.object(editor, 'load_content', side_effect=load_content)
        assert editor.load_file(str(switch.target)) is True

        assert editor.file_path == editor.settings.file_path == str(switch.target)
        assert editor.get_encryption() == Encryption.ENCRYPTED
        switch.widget.setPlainText('restored encrypted document')
        assert editor.save_active_file() is True
        header, body = FileHeader().load_file(str(switch.target))
        helper = EncHelper(switch.password, header.get_enc_param('slt'), header.get_enc_param('itr'))
        assert helper.decrypt_data(body.encode()) == b'restored encrypted document'
        assert switch.source.read_text(encoding='utf-8') == 'original text'

    @pytest.mark.parametrize('route', ['tree', 'open'])
    def test_failed_save_prevents_file_switch(self, file_switch, mocker, route):
        editor = file_switch.editor
        mocker.patch.object(editor, 'save_active_file', return_value=False)
        load = mocker.patch.object(editor, 'load_file')
        if route == 'tree':
            file_switch.tree.setCurrentIndex(file_switch.proxy.index(1, 0))
            editor.action_nav_select_file(file_switch.proxy.index(1, 0))
        else:
            editor.safely_open_file(str(file_switch.target))
        assert editor.file_path == str(file_switch.source)
        if route == 'tree':
            assert file_switch.tree.currentIndex().data(Qt.ItemDataRole.UserRole) == str(file_switch.source)
        load.assert_not_called()

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
        result = test_obj_notolog_editor.load_default_page(ignore_settings=True)
        assert result is True

        # Current working directory
        # test_run_from_dir = os.getcwd()
        test_file_dir = os.path.dirname(os.path.realpath(__file__))
        test_file_parent_dir = os.path.dirname(test_file_dir)
        # Assert that the method was called once
        mock_method1.assert_not_called()
        # Assert that the method was called once with the param(s)
        mock_method2.assert_called_once_with(os.path.normpath('%s/README.md') % test_file_parent_dir)

    @pytest.mark.parametrize('dialog_error', [None, RuntimeError('dialog failed')])
    def test_action_settings_releases_dialog(self, mocker, test_obj_notolog_editor, dialog_error):
        dialog = mocker.patch('notolog.notolog_editor.SettingsDialog').return_value
        save_active_file = mocker.patch.object(test_obj_notolog_editor, 'save_active_file')
        if dialog_error is not None:
            dialog.show.side_effect = dialog_error

        if dialog_error is None:
            test_obj_notolog_editor.action_settings()
            assert test_obj_notolog_editor.settings_dialog is dialog
            dialog.deleteLater.assert_not_called()
            dialog.finished.connect.call_args.args[0]()
        else:
            with pytest.raises(RuntimeError, match='dialog failed'):
                test_obj_notolog_editor.action_settings()

        save_active_file.assert_called_once_with(clear_after=False)
        dialog.show.assert_called_once_with()
        dialog.exec.assert_not_called()
        dialog.deleteLater.assert_called_once_with()
        assert test_obj_notolog_editor.settings_dialog is None

    @pytest.mark.parametrize('allow_close', [False, True, None])
    def test_reset_settings_respects_settings_dialog_cancellation(self, mocker, allow_close):
        dialog = Mock() if allow_close is not None else None
        if dialog is not None:
            dialog.close.return_value = allow_close
        editor = SimpleNamespace(logger=Mock(), settings_dialog=dialog, settings=Mock(), close=Mock())
        app_config = mocker.patch('notolog.notolog_editor.AppConfig').return_value
        dismiss = Mock()

        NotologEditor.reset_settings_dialog_callback(editor, dismiss)

        dismiss.assert_called_once_with()
        if allow_close is False:
            editor.settings.clear.assert_not_called()
            editor.settings.sync.assert_not_called()
            app_config.delete_app_config.assert_not_called()
            editor.close.assert_not_called()
        else:
            editor.settings.clear.assert_called_once_with()
            editor.settings.sync.assert_called_once_with()
            app_config.delete_app_config.assert_called_once_with()
            editor.close.assert_called_once_with()

    @pytest.mark.asyncio
    async def test_finish_shutdown_cancels_and_drains_tasks(self, mocker, test_obj_notolog_editor):
        blocker = asyncio.create_task(asyncio.Event().wait(), name='test-blocker')
        current_task = asyncio.current_task()
        mocker.patch.object(asyncio, 'all_tasks', return_value={current_task, blocker})
        close = mocker.patch.object(test_obj_notolog_editor, 'close')

        await test_obj_notolog_editor.finish_shutdown()

        assert blocker.cancelled()
        assert test_obj_notolog_editor._shutdown_complete is True
        close.assert_called_once_with()

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

        mock_statusbar = MagicMock(spec=StatusBar)
        setattr(test_obj_notolog_editor, 'statusbar', mock_statusbar)

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
        mocker.patch.object(mock_header, 'is_file_encrypted', return_value=encryption == Encryption.ENCRYPTED)
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

    def test_delete_file_reversibly(self, mocker, test_obj_notolog_editor, tmp_path):
        source_path = tmp_path / 'private-note.md'
        source_path.write_text('plaintext', encoding='utf-8')
        test_obj_notolog_editor.settings = SimpleNamespace(reversible_file_deletion=True)
        mocker.patch.object(test_obj_notolog_editor, 'get_current_file_path', return_value='another-file.md')

        assert test_obj_notolog_editor.delete_file(str(source_path)) is True
        assert not source_path.exists()
        assert (tmp_path / 'private-note.md.del').read_text(encoding='utf-8') == 'plaintext'

    @pytest.mark.parametrize('mode', [Mode.EDIT, Mode.VIEW, Mode.SOURCE])
    @pytest.mark.parametrize('suffix', ['.enc', '.md'])
    @pytest.mark.parametrize('body', ['private synthetic note Ω', ''])
    def test_save_as_preserves_encryption(self, mocker, test_obj_notolog_editor, tmp_path, mode, suffix, body):
        editor = test_obj_notolog_editor
        destination = tmp_path / f'copy{suffix}'
        source = tmp_path / 'original.enc'
        header = FileHeader().get_new(is_enc=True)
        header.set_enc_param('itr', 1024)
        password = EncPassword()
        password.password = 'synthetic-test-password'
        helper = EncHelper(password, header.get_enc_param('slt'), header.get_enc_param('itr'))
        original = header.pack(helper.encrypt_data(b'previous contents').decode())
        source.write_text(original, encoding='utf-8')
        editor.header = header
        editor.content = body if mode != Mode.EDIT else 'previous contents'
        original_header = repr(header)
        editor.supported_file_extensions = ['md', 'enc']
        mocker.patch.object(editor, 'get_current_file_path', return_value=str(source))
        mocker.patch.object(editor, 'get_mode', return_value=mode)
        mocker.patch.object(editor, 'get_encryption', return_value=Encryption.ENCRYPTED)
        widget = Mock()
        widget.toPlainText.return_value = body if mode == Mode.EDIT else 'stale editor text'
        get_edit_widget = mocker.patch.object(editor, 'get_edit_widget', return_value=widget)
        mocker.patch.object(editor, 'get_encrypt_helper', return_value=helper)
        mocker.patch('notolog.notolog_editor.QFileDialog.getSaveFileName', return_value=(str(destination), ''))

        editor.action_save_as_file()

        saved_header, ciphertext = FileHeader().load_file(str(destination))
        assert saved_header.is_file_encrypted()
        assert helper.decrypt_data(ciphertext.encode()).decode() == body
        if body:
            assert body not in destination.read_text(encoding='utf-8')
        assert source.read_text(encoding='utf-8') == original
        assert repr(editor.header) == original_header
        assert editor.content == (body if mode != Mode.EDIT else 'previous contents')
        assert get_edit_widget.call_count == int(mode == Mode.EDIT)

    @pytest.mark.parametrize('failure', ['missing_header', 'invalid_metadata', 'no_key', 'encryption_error'])
    def test_save_as_failure_does_not_touch_destination(self, mocker, test_obj_notolog_editor, tmp_path, failure):
        editor = test_obj_notolog_editor
        destination = tmp_path / 'existing.enc'
        destination.write_bytes(b'original destination bytes')
        editor.header = FileHeader().get_new(is_enc=True)
        editor.content = 'synthetic private note'
        editor.supported_file_extensions = ['md', 'enc']
        mocker.patch.object(editor, 'get_current_file_path', return_value=str(tmp_path))
        mocker.patch.object(editor, 'get_mode', return_value=Mode.VIEW)
        mocker.patch.object(editor, 'get_encryption', return_value=Encryption.ENCRYPTED)
        helper = Mock(spec=EncHelper)
        helper.encrypt_data.return_value = None
        mocker.patch.object(editor, 'get_encrypt_helper', return_value=helper)
        if failure == 'missing_header':
            editor.header = None
        elif failure == 'invalid_metadata':
            editor.header.set_enc_param('slt', '')
        elif failure == 'encryption_error':
            helper.encrypt_data.side_effect = ValueError('synthetic failure')
        mocker.patch('notolog.notolog_editor.QFileDialog.getSaveFileName', return_value=(str(destination), ''))
        message = mocker.patch('notolog.notolog_editor.MessageBox')
        save = mocker.patch.object(editor, 'save_file_content')

        editor.action_save_as_file()

        save.assert_not_called()
        message.assert_called_once()
        assert destination.read_bytes() == b'original destination bytes'

    @pytest.mark.parametrize('mode', [Mode.EDIT, Mode.VIEW, Mode.SOURCE])
    def test_save_as_plain_document(self, mocker, test_obj_notolog_editor, tmp_path, mode):
        editor = test_obj_notolog_editor
        editor.header = FileHeader()
        editor.content = 'stored source'
        editor.supported_file_extensions = ['md']
        destination = tmp_path / 'copy.md'
        mocker.patch.object(editor, 'get_current_file_path', return_value=str(tmp_path))
        mocker.patch.object(editor, 'get_mode', return_value=mode)
        mocker.patch.object(editor, 'get_encryption', return_value=Encryption.PLAIN)
        widget = Mock()
        widget.toPlainText.return_value = 'edited source'
        mocker.patch.object(editor, 'get_edit_widget', return_value=widget)
        mocker.patch('notolog.notolog_editor.QFileDialog.getSaveFileName', return_value=(str(destination), ''))

        editor.action_save_as_file()

        assert destination.read_text(encoding='utf-8') == ('edited source' if mode == Mode.EDIT else 'stored source')

    def test_save_as_cancel_does_not_prepare_or_write(self, mocker, test_obj_notolog_editor, tmp_path):
        editor = test_obj_notolog_editor
        editor.supported_file_extensions = ['md', 'enc']
        mocker.patch.object(editor, 'get_current_file_path', return_value=str(tmp_path))
        mocker.patch('notolog.notolog_editor.QFileDialog.getSaveFileName', return_value=('', ''))
        prepare = mocker.patch.object(editor, 'pack_file_content')
        save = mocker.patch.object(editor, 'save_file_content')

        editor.action_save_as_file()

        prepare.assert_not_called()
        save.assert_not_called()

    def test_header_encryption_is_preserved_if_editor_state_is_plain(self, mocker, test_obj_notolog_editor):
        editor = test_obj_notolog_editor
        header = FileHeader().get_new(is_enc=True)
        mocker.patch.object(editor, 'get_encryption', return_value=Encryption.PLAIN)
        helper = Mock(spec=EncHelper)
        helper.encrypt_data.return_value = b'encrypted-payload'
        mocker.patch.object(editor, 'get_encrypt_helper', return_value=helper)

        packed = editor.pack_file_content(header, 'synthetic secret')

        assert 'synthetic secret' not in packed
        assert packed.endswith('encrypted-payload')
        helper.encrypt_data.assert_called_once_with(b'synthetic secret')

    def test_search_does_not_log_selection(self, mocker, test_obj_notolog_editor, caplog):
        editor = test_obj_notolog_editor
        editor.logger = logging.getLogger('notolog_editor')
        secret = 'synthetic private selection'
        widget = Mock()
        widget.textCursor.return_value.selectedText.return_value = secret
        mocker.patch.object(editor, 'get_mode', return_value=Mode.EDIT)
        mocker.patch.object(editor, 'get_edit_widget', return_value=widget)
        mocker.patch.object(editor, 'action_search_next')

        with caplog.at_level(logging.DEBUG):
            editor.search_text()

        editor.toolbar.search_form.set_text.assert_called_once_with(secret)
        assert secret not in caplog.text

    def test_encryption_check_reads_only_file_header(self, mocker, test_obj_notolog_editor):
        encrypted_header = FileHeader().get_new(is_enc=True)
        read_header = mocker.patch.object(FileHeader, 'read', return_value=repr(encrypted_header))
        load_file = mocker.patch.object(FileHeader, 'load_file')

        assert test_obj_notolog_editor.is_file_encrypted('/notes/large.enc') is True
        read_header.assert_called_once_with('/notes/large.enc')
        load_file.assert_not_called()

    def test_encrypted_save_never_falls_back_to_plaintext(self, mocker, test_obj_notolog_editor):
        file_path = '/notes/private.enc'
        mocker.patch.object(test_obj_notolog_editor, 'get_mode', return_value=Mode.EDIT)
        mocker.patch.object(test_obj_notolog_editor, 'get_encryption', return_value=Encryption.ENCRYPTED)
        mocker.patch.object(test_obj_notolog_editor, 'get_current_file_path', return_value=file_path)
        mocker.patch.object(test_obj_notolog_editor, 'store_doc_cursor_pos')
        mocker.patch.object(os.path, 'exists', return_value=True)
        mocker.patch.object(os, 'access', return_value=True)
        mocker.patch.object(QTimer, 'singleShot')
        mocker.patch.object(test_obj_notolog_editor, 'toggle_save_timer')
        MessageBox.__new__ = MagicMock(return_value=None)

        edit_widget = MagicMock(spec=EditWidget)
        edit_widget.toPlainText.return_value = 'updated plaintext'
        mocker.patch.object(test_obj_notolog_editor, 'get_edit_widget', return_value=edit_widget)
        test_obj_notolog_editor.content = 'old plaintext'
        test_obj_notolog_editor.estate = SimpleNamespace(allow_save_empty=None)

        header = MagicMock(spec=FileHeader)
        header.is_valid.return_value = True
        header.get_enc_param.side_effect = lambda key: {'slt': 'salt', 'itr': 1024}[key]
        test_obj_notolog_editor.header = header
        encrypt_helper = MagicMock(spec=EncHelper)
        encrypt_helper.encrypt_data.return_value = None
        mocker.patch.object(test_obj_notolog_editor, 'get_encrypt_helper', return_value=encrypt_helper)
        save_file_content = mocker.patch.object(test_obj_notolog_editor, 'save_file_content')

        assert test_obj_notolog_editor.save_active_file() is False
        save_file_content.assert_not_called()
        header.pack.assert_not_called()

    def test_delete_file_permanently(self, mocker, test_obj_notolog_editor, tmp_path):
        source_path = tmp_path / 'private-note.md'
        source_path.write_text('plaintext', encoding='utf-8')
        test_obj_notolog_editor.settings = SimpleNamespace(reversible_file_deletion=False)
        mocker.patch.object(test_obj_notolog_editor, 'get_current_file_path', return_value='another-file.md')

        assert test_obj_notolog_editor.delete_file(str(source_path)) is True
        assert not source_path.exists()
        assert not (tmp_path / 'private-note.md.del').exists()

    def test_delete_encrypted_source_uses_global_policy(self, mocker, test_obj_notolog_editor):
        test_obj_notolog_editor.settings = SimpleNamespace(reversible_file_deletion=True)
        delete_file = mocker.patch.object(test_obj_notolog_editor, 'delete_file', return_value=True)
        close_dialog = Mock()

        test_obj_notolog_editor.delete_encrypted_source_dialog_callback(close_dialog, '/notes/private.md')

        delete_file.assert_called_once_with('/notes/private.md')
        close_dialog.assert_called_once()

    @pytest.mark.parametrize(
        'encrypted_file_opened, reversible_deletion, expected_text_lexeme',
        [
            (True, True, 'dialog_encrypt_delete_source_text'),
            (True, False, 'dialog_file_delete_completely_text'),
            (False, True, None),
        ],
    )
    def test_encrypt_offers_source_deletion_only_after_verified_open(
            self, mocker, test_obj_notolog_editor, encrypted_file_opened,
            reversible_deletion, expected_text_lexeme):
        source_path = '/notes/private.md'
        encrypted_path = f'{source_path}.enc'
        header = MagicMock(spec=FileHeader)
        header.is_valid.return_value = True
        header.is_file_encrypted.return_value = False
        header.get_enc_param.side_effect = lambda key: {'slt': 'salt', 'itr': 1, 'hint': ''}[key]
        header.pack.return_value = 'encrypted-content'
        mocker.patch.object(FileHeader, 'load_file', return_value=(header, 'plaintext'))
        mocker.patch.object(os.path, 'isfile', side_effect=lambda path: path == source_path)
        mocker.patch('notolog.helpers.file_helper.is_file_openable', return_value=True)
        encrypt_helper = MagicMock(spec=EncHelper)
        encrypt_helper.encrypt_data.return_value = b'encrypted'
        mocker.patch.object(test_obj_notolog_editor, 'get_encrypt_helper', return_value=encrypt_helper)
        mocker.patch.object(test_obj_notolog_editor, 'save_file_content', return_value=True)
        mocker.patch.object(test_obj_notolog_editor, 'load_file', return_value=encrypted_file_opened)
        common_dialog = mocker.patch.object(test_obj_notolog_editor, 'common_dialog')
        close_dialog = Mock()
        test_obj_notolog_editor.enc_password = None
        test_obj_notolog_editor.settings = SimpleNamespace(reversible_file_deletion=reversible_deletion)

        test_obj_notolog_editor.encrypt_file_dialog_callback(
            close_dialog, source_path, encrypted_path)

        close_dialog.assert_called_once()
        assert common_dialog.call_count == int(encrypted_file_opened)
        if expected_text_lexeme:
            test_obj_notolog_editor.lexemes.get.assert_any_call(
                name=expected_text_lexeme, file_name='private.md')

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

    @pytest.mark.parametrize(
        "test_exp_params_fixture",
        [
            # Anchors - should return True (local)
            ('#section-1', None, True),
            ('#heading', None, True),
            # Expandable/collapsible - should return True
            ('expandable-1', None, True),
            ('collapsible-2', None, True),
            # External http/https URLs - should return False (external)
            ('https://example.com', None, False),
            ('http://example.com/page', None, False),
            ('https://github.com/notolog/notolog-editor', None, False),
            # Dangerous schemes - should return None (blocked)
            ('javascript:alert(1)', None, None),
            ('ftp://example.com', None, None),
            ('data:text/html,<script>alert(1)</script>', None, None),
            # Note: file:// is allowed as it's a valid local file scheme
        ],
        indirect=True
    )
    def test_check_local_link_schemes(self, mocker, test_obj_notolog_editor, test_exp_params_fixture):
        """Test check_local_link correctly identifies different URL schemes."""
        from PySide6.QtCore import QUrl

        url_string, _, expected_result = test_exp_params_fixture
        url = QUrl(url_string)

        result = test_obj_notolog_editor.check_local_link(url, execute=False)

        assert result == expected_result

    @pytest.mark.parametrize(
        "test_exp_params_fixture",
        [
            # Relative markdown links - should return True if file exists
            ('readme.md', 'readme.md', True),
            ('./relative.md', 'relative.md', True),
            # Non-existent files - should return None
            ('nonexistent.md', None, None),
            # Unsupported extensions (no extension or blocked) - should return None
            ('script.py', 'script.py', None),
        ],
        indirect=True
    )
    def test_check_local_link_relative_paths(self, mocker, test_obj_notolog_editor, test_exp_params_fixture, tmp_path):
        """Test check_local_link correctly resolves relative paths."""
        from PySide6.QtCore import QUrl

        url_string, file_to_create, expected_result = test_exp_params_fixture

        # Set up required attributes for check_local_link
        test_obj_notolog_editor.supported_file_extensions = ['md', 'txt', 'htm', 'html', 'enc']

        # Set current file path (used by get_current_file_path()) to a file in tmp_path
        current_file = tmp_path / 'current.md'
        current_file.touch()
        test_obj_notolog_editor.file_path = str(current_file)

        # Create the target file if needed
        if file_to_create:
            target_path = tmp_path / file_to_create
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.touch()

        url = QUrl(url_string)
        result = test_obj_notolog_editor.check_local_link(url, execute=False)

        assert result == expected_result


@pytest.mark.parametrize('view', [False, True])
@pytest.mark.parametrize('accepted', [False, True])
@pytest.mark.parametrize('target', [0, 1, 2, 3, 4])
def test_go_to_line_moves_only_after_acceptance(qapp, mocker, view, accepted, target):
    from PySide6.QtGui import QFont
    from PySide6.QtWidgets import QInputDialog, QPlainTextEdit, QTextBrowser, QDialog
    widget = QTextBrowser() if view else QPlainTextEdit()
    widget.setPlainText('first\nsecond\nthird')
    window = QPlainTextEdit()
    window.setFont(QFont('Sans Serif', 24))
    settings = Mock()
    settings.app_language = 'en'
    settings.value_changed = Mock()
    # Use a real Qt parent and input widget, while driving the modal result synthetically.
    owner = window
    owner.get_active_widget = lambda: widget
    owner.settings = settings
    def execute(dialog):
        minimum_width = dialog.minimumWidth()
        dialog.show()
        qapp.processEvents()
        assert dialog.minimumWidth() == minimum_width
        assert dialog.width() >= minimum_width
        assert dialog.intMinimum() == 1
        assert dialog.intMaximum() == 3
        assert dialog.intValue() == 1
        dialog.setIntValue(target)
        return QDialog.DialogCode.Accepted if accepted else QDialog.DialogCode.Rejected
    mocker.patch.object(QInputDialog, 'exec', execute)
    NotologEditor.go_to_line(owner)
    assert widget.textCursor().blockNumber() == (min(3, max(1, target)) - 1 if accepted else 0)
    assert widget.toPlainText() == 'first\nsecond\nthird'
    widget.deleteLater()
    window.deleteLater()
