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

from PySide6.QtWidgets import QApplication, QStyleFactory

from notolog.app import main
from notolog.app_config import AppConfig
from notolog.notolog_editor import NotologEditor

import sys
import pytest
import logging
import asyncio


class TestApp:

    @pytest.fixture(scope="function")
    def test_obj_app_config(self, mocker):
        # Mock AppConfig's get_logger_level method to suppress logging during tests.
        mocker.patch.object(AppConfig, 'get_logger_level', return_value=logging.NOTSET)

        _app_config = AppConfig()
        _app_config.set_test_mode(True)

        yield _app_config

    @pytest.fixture(scope="function")
    def test_exp_params_fixture(self, request):
        # Retrieve parameter values from the test request.
        param_values = request.param

        yield param_values

    @pytest.mark.parametrize(
        "test_exp_params_fixture",
        [
            ('-smth1', '', 2),
            ('-v', f'Notolog {AppConfig().get_app_version()}', 0),
            ('--version', f'Notolog {AppConfig().get_app_version()}', 0),
        ],
        indirect=True
    )
    def test_main_args(self, test_obj_app_config: AppConfig, test_exp_params_fixture, monkeypatch, capsys):
        arg, exp_result, exp_exit_code = test_exp_params_fixture

        # Simulate command-line arguments
        monkeypatch.setattr(sys, "argv", ['app.py', arg])

        # Call the main function
        with pytest.raises(SystemExit) as excinfo:
            main()

        # Validate the output and the exit code
        captured = capsys.readouterr()
        assert captured.out.strip() == exp_result
        assert excinfo.value.code == exp_exit_code

    def test_app(self, test_obj_app_config: AppConfig, mocker, monkeypatch, qapp):
        # Simulate command-line arguments
        monkeypatch.setattr(sys, "argv", [])

        # Reuse the session application regardless of test collection order.
        application_factory = mocker.patch('notolog.app.QApplication', return_value=qapp)

        # Create a mock event loop with proper methods
        mock_loop = mocker.MagicMock()
        mock_loop.__enter__ = mocker.MagicMock(return_value=mock_loop)
        mock_loop.__exit__ = mocker.MagicMock(return_value=False)
        scheduled_callbacks = []
        mock_loop.call_soon = mocker.MagicMock(side_effect=scheduled_callbacks.append)
        mock_loop.run_forever = mocker.MagicMock(side_effect=lambda: scheduled_callbacks.pop(0)())

        # Mock QEventLoop to return our mock_loop instance
        mocker.patch('notolog.app.QEventLoop', return_value=mock_loop)

        test_set_event_loop = mocker.patch.object(asyncio, 'set_event_loop', return_value=None)

        # Mock NotologEditor initialization to prevent UI creation that causes segfault
        mocker.patch.object(NotologEditor, '__init__', return_value=None)
        test_notolog_editor_show = mocker.patch.object(NotologEditor, 'show', wraps=lambda: None)
        # Prevent resource processing, including 'process_document_images'
        mocker.patch.object(NotologEditor, 'load_content_html', return_value=None)
        test_logging_basic_config = mocker.patch.object(logging, 'basicConfig', return_value=None)
        test_set_organisation_name = mocker.patch.object(QApplication, 'setOrganizationName')
        test_set_organisation_domain = mocker.patch.object(QApplication, 'setOrganizationDomain')
        test_set_application_name = mocker.patch.object(QApplication, 'setApplicationName')
        test_set_application_version = mocker.patch.object(QApplication, 'setApplicationVersion')
        test_set_desktop_settings_aware = mocker.patch.object(QApplication, 'setDesktopSettingsAware')
        test_qstylefactory_create = mocker.patch.object(QStyleFactory, 'create', wraps=QStyleFactory.create)
        test_set_style = mocker.patch.object(QApplication, 'setStyle')

        # Call the main function
        main()

        application_factory.assert_called_once_with([])
        test_logging_basic_config.assert_called_once()

        test_set_organisation_name.assert_called_once()
        assert str(test_set_organisation_name.call_args) == "call('%s')" % test_obj_app_config.get_settings_org_name()

        test_set_organisation_domain.assert_called_once()
        assert (str(test_set_organisation_domain.call_args) == "call('%s')" % test_obj_app_config.get_settings_org_domain())

        test_set_application_name.assert_called_once()
        assert (str(test_set_application_name.call_args) == "call('%s')" % test_obj_app_config.get_settings_app_name())

        test_set_application_version.assert_called_once()
        assert (str(test_set_application_version.call_args) == "call('%s')" % test_obj_app_config.get_app_version())

        test_set_desktop_settings_aware.assert_called_once()
        assert (str(test_set_desktop_settings_aware.call_args) == "call(%s)" % 'False')

        test_qstylefactory_create.assert_called_once()
        assert (str(test_qstylefactory_create.call_args) == "call('%s')" % 'Fusion')

        test_set_style.assert_called_once()

        test_notolog_editor_show.assert_called()
        mock_loop.call_soon.assert_called_once()
        mock_loop.run_forever.assert_called_once_with()
        assert test_set_event_loop.call_args_list == [mocker.call(mock_loop), mocker.call(None)]

    @pytest.mark.asyncio
    async def test_async(self):
        assert await asyncio.sleep(0, result=True)
