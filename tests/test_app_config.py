# tests/test_app_config.py

from notolog.app_package import AppPackage
from notolog.app_config import AppConfig

import pytest

import os
import tomli
import shutil
import logging


class TestAppConfig:

    @pytest.fixture(scope="function")
    def test_obj_app_package(self, mocker, request):
        get_config = request.param

        # Mock methods
        mocker.patch.object(AppPackage, 'get_config', return_value=get_config)
        mocker.patch.object(AppPackage, 'set_config', return_value=None)
        mocker.patch.object(AppPackage, 'set_type', return_value=None)

        # Init object
        _app_package = AppPackage()

        # Mock get package type results
        mocker.patch.object(_app_package, 'get_type', wraps=_app_package.get_type)

        yield _app_package

    @pytest.fixture(scope="function")
    def test_obj_app_config(self, mocker, request):
        app_config, skip_validation = request.param if isinstance(request.param, tuple) else (request.param, False)

        if skip_validation:
            # Allow updates without validating complete configuration.
            mocker.patch.object(AppConfig, 'validate_config', return_value=True)
        mocker.patch.object(AppConfig, 'load_config', return_value=app_config)

        # Mock libs results
        mocker.patch.object(tomli, 'loads', wraps=tomli.loads)
        mocker.patch.object(shutil, 'copy', return_value=None)
        # mocker.patch.object(os, 'remove', return_value=None)

        _app_config = AppConfig()
        _app_config.set_test_mode(True)
        _app_config.load_initial_conf()

        yield _app_config

    @pytest.fixture(scope="function")
    def test_exp_params_fixture(self, request):
        # Retrieve parameter values from the test request.
        param_values = request.param

        yield param_values

    @pytest.mark.parametrize(
        "test_obj_app_package, test_obj_app_config, test_exp_params_fixture",
        [
            (({}), dict({'package': {'type': ''}, 'font': {'base_size': 13}}),
             ('notolog_app_config_qa.toml', 'pip', False)),
            (({}), dict({'package': {'type': 'smth1'}, 'font': {'base_size': 13}}),
             ('notolog_app_config_qa.toml', 'pip', False)),
            (({'package': {'type': 'bin'}}), dict({'package': {'type': 'smth1'}, 'font': {'base_size': 13}}),
             ('notolog_app_config_qa_bin.toml', 'bin', True)),
            (({'package': {'type': 'bin'}}), dict({'package': {'type': 'bin'}, 'font': {'base_size': 13}}),
             ('notolog_app_config_qa_bin.toml', 'bin', True)),
            (({'package': {'type': 'bin'}}), dict({'package': {'type': 'pip'}, 'font': {'base_size': 13}}),
             ('notolog_app_config_qa_bin.toml', 'bin', True)),
        ],
        indirect=True
    )
    def test_general_checks(self, mocker, test_obj_app_package: AppPackage, test_obj_app_config: AppConfig,
                            test_exp_params_fixture):

        exp_file_path, exp_package_type, exp_result = test_exp_params_fixture

        mock_app_config_update_handler = mocker.patch.object(test_obj_app_config, 'app_config_update_handler',
                                                             return_value=None)
        mock_app_config_logger_warning = mocker.patch.object(test_obj_app_config.logger, 'warning',
                                                             return_value=None)

        mock_app_package_set_config = mocker.patch.object(test_obj_app_package, 'set_config', return_value=None)
        mock_app_package_set = mocker.patch.object(test_obj_app_package, 'set_type', return_value=None)

        expected_app_config = test_obj_app_config.app_config

        test_obj_app_config.load_initial_conf()

        # Match package file and config results
        assert (test_obj_app_config.get_package_type() == test_obj_app_package.get_type()) == exp_result

        assert test_obj_app_config.get_package_type() == exp_package_type
        assert test_obj_app_config.get_font_base_size() == test_obj_app_config.app_config['font']['base_size']

        assert os.path.basename(test_obj_app_config.get_app_config_path()) == os.path.basename(exp_file_path)
        assert test_obj_app_config.app_config == expected_app_config

        # The config is forced with mocked data; the below approach will not work.
        # assert test_obj_app_config.toml_file_path == test_obj_app_config.get_app_config_path()

        if test_obj_app_config.toml_file_path != test_obj_app_config.get_app_config_path():
            assert mock_app_config_logger_warning.call_count == 1
            assert test_obj_app_config.app_config['package']['type'] != test_obj_app_package.get_type()

        mock_app_config_update_handler.assert_not_called()
        mock_app_package_set_config.assert_not_called()
        mock_app_package_set.assert_not_called()

    @pytest.mark.parametrize(
        "test_obj_app_package, test_obj_app_config, test_exp_params_fixture",
        [
            (({}), {'package': {'type': None}, 'font': {'base_size': None}}, ('', 'pip')),
            (({}), {'package': {'type': None}, 'font': {'base_size': None}}, ('test1', 'pip')),
            (({}), {'package': {'type': None}, 'font': {'base_size': None}}, ('bin', 'bin')),
            (({}), {'package': {'type': 'pip'}, 'font': {'base_size': None}}, ('bin', 'bin')),
            (({'package': {'type': 'pip'}}), {'package': {'type': 'smth1'}, 'font': {'base_size': None}}, ('bin', 'bin')),
            (({}), {'package': {'type': None}, 'font': {'base_size': None}}, ('', 'pip')),
        ],
        indirect=True
    )
    def test_setup_package(self, mocker, test_obj_app_package: AppPackage, test_obj_app_config: AppConfig,
                           test_exp_params_fixture):

        setup_type, exp_result = test_exp_params_fixture

        mock_app_config_update_handler = mocker.patch.object(test_obj_app_config, 'app_config_update_handler',
                                                             return_value=None)
        mock_app_config_load_initial_conf = mocker.patch.object(test_obj_app_config, 'load_initial_conf',
                                                                return_value=None)
        mock_app_config_save_app_config = mocker.patch.object(test_obj_app_config, 'save_app_config',
                                                              return_value=None)

        mock_app_package_set_config = mocker.patch.object(test_obj_app_package, 'set_config', return_value=None)
        mock_app_package_set = mocker.patch.object(test_obj_app_package, 'set_type', return_value=None)

        previously_set_package = test_obj_app_config.get_package_type()

        test_obj_app_config.setup_package(setup_type)

        mock_app_config_load_initial_conf.assert_called_once()

        mock_app_config_save_app_config.assert_called_once()

        if not previously_set_package:
            mock_app_config_update_handler.assert_called_once_with({'package_type': exp_result})

        if test_obj_app_package.get_type() != exp_result:
            mock_app_package_set.assert_called_once_with(exp_result)
            assert str(mock_app_package_set.call_args) == "call('%s')" % exp_result
        else:
            mock_app_package_set_config.assert_not_called()
            mock_app_package_set.assert_not_called()

    @pytest.mark.parametrize(
        "test_obj_app_package, test_obj_app_config, test_exp_params_fixture",
        [
            (
                {'package': {'type': 'smth1'}}, {},
                ({'package': {'type': 'smth2'}, 'font': {'base_size': None}}, False, False)
            ),
            (
                {'package': {'type': 'smth1'}}, {},
                ({'package': {'type': 'pip'}, 'font': {'base_size': None}}, False, False)
            ),
            (
                    {'package': {'type': 'bin'}}, {},
                    ({'package': {'type': 'smth1'}, 'font': {'base_size': None}}, True, False)
            ),
            (
                {'package': {'type': 'bin'}}, {},
                ({'package': {'type': 'pip'}, 'font': {'base_size': None}}, True, False)
            ),
            (
                {'package': {'type': 'smth1'}}, {},
                (AppConfig().get_default_app_config(), False, True)
            ),
            (
                {'package': {'type': 'bin'}}, {},
                (AppConfig().get_default_app_config(), True, True)
            ),

        ],
        indirect=True
    )
    def test_validate_configs(self, test_obj_app_package: AppPackage, test_obj_app_config: AppConfig,
                              test_exp_params_fixture):

        app_config_to_check, exp_app_package_result, exp_app_config_result = test_exp_params_fixture

        app_package_config = test_obj_app_package.get_config()

        assert test_obj_app_package.validate_config(app_package_config) == exp_app_package_result
        assert test_obj_app_config.validate_config(app_config_to_check) == exp_app_config_result

        assert 'package' in app_package_config
        assert 'type' in app_package_config['package']

        assert test_obj_app_package.validate_type(test_obj_app_package.get_type()) == exp_app_package_result

    @pytest.mark.parametrize(
        "test_obj_app_package, test_obj_app_config",
        [
            # This creates a separate file for each package value
            ({'package': {'type': 'pip'}}, AppConfig().get_config()),
            ({'package': {'type': 'bin'}}, AppConfig().get_config()),
            # Restore the real app config to reset pytest object state
            ({'package': {'type': AppPackage.default_package}}, AppConfig().get_config()),
        ],
        indirect=True
    )
    def test_finish(self, test_obj_app_package: AppPackage, test_obj_app_config: AppConfig):
        # Verify the test file's suffix
        app_config_path = test_obj_app_config.get_app_config_path()
        assert '_qa' in app_config_path
        # Deleting the config file and ensures it was existed
        assert test_obj_app_config.delete_app_config()
        assert not os.path.exists(app_config_path)

    @pytest.mark.parametrize(
        "test_obj_app_package, test_obj_app_config, test_exp_params_fixture",
        [
            (({}), ({'logger': {'level': ''}}, True), logging.INFO),
            (({}), ({'logger': {'level': 'notset'}}, True), logging.NOTSET),
            (({}), ({'logger': {'level': 'info'}}, True), logging.INFO),
            (({}), ({'logger': {'level': 'DEBUG'}}, True), logging.DEBUG),
            (({}), ({'logger': {'level': 'cRitICaL'}}, True), logging.CRITICAL),
        ],
        indirect=True
    )
    def test_get_logger_level(self, test_obj_app_package: AppPackage, test_obj_app_config: AppConfig,
                              test_exp_params_fixture):
        exp_logger_level_result = test_exp_params_fixture

        logger_level_result = test_obj_app_config.get_logger_level()

        assert logger_level_result == exp_logger_level_result
