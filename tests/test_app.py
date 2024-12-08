# tests/test_app.py

from PySide6.QtCore import QEventLoop
from PySide6.QtWidgets import QApplication, QStyleFactory

from notolog.app import main
from notolog.app_config import AppConfig
from notolog.notolog_editor import NotologEditor

from types import SimpleNamespace

from unittest.mock import AsyncMock

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

    @pytest.mark.asyncio
    async def test_app(self, test_obj_app_config: AppConfig, mocker, monkeypatch):
        # Simulate command-line arguments
        monkeypatch.setattr(sys, "argv", [])

        event_loop = mocker.patch.object(QEventLoop, '__init__', return_value=None)
        mocker.patch.object(asyncio, 'set_event_loop', return_value=None)
        # AsyncMock mock class is designed to simulate asynchronous calls and can be awaited.
        mocker.patch.object(asyncio, 'Event', return_value=SimpleNamespace(**{'set': lambda: None, 'wait': AsyncMock()}))
        mocker.patch.object(event_loop, 'run_until_complete', return_value=None)

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

    @pytest.mark.asyncio
    async def test_async(self):
        assert await asyncio.sleep(0, result=True)
