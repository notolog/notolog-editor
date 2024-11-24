# tests/test_settings_helper.py

from notolog.app_config import AppConfig
from notolog.helpers.settings_helper import SettingsHelper

from logging import Logger

import os
import pytest
import base64


class TestSettingsHelper:

    @pytest.fixture(scope="function", autouse=True)
    def test_obj_settings_helper(self, mocker, request):
        # Get the parameter value(s) from the request
        env_values, app_config_key, generated_key = request.param

        mocker.patch.object(AppConfig, 'get_logging', return_value=False)
        mocker.patch.object(AppConfig, 'get_debug', return_value=False)

        # Mock methods result
        mocker.patch.object(os, 'getenv', side_effect=lambda k: env_values.get(k, None))
        mocker.patch.object(AppConfig, 'get_security_app_secret', return_value=app_config_key)
        mocker.patch.object(SettingsHelper, 'generate_app_key', return_value=generated_key)
        # Do not call it from test to avoid data loss
        mocker.patch.object(SettingsHelper, 'setup_app_key', return_value=None)

        yield SettingsHelper()

    @pytest.fixture(scope="function")
    def test_exp_param_fixture(self, request):
        # Get the parameter value from the request
        param_value = request.param

        yield param_value

    @pytest.mark.parametrize(
        "test_obj_settings_helper, test_exp_param_fixture",
        [
            (({SettingsHelper.env_secret_name: None}, None, b''), b''),
            (({SettingsHelper.env_secret_name: 'c29tZWtleTFzb21la2V5MnNvbWVrZXkzc29tZWtleTQ='}, None, b''),
             b'c29tZWtleTFzb21la2V5MnNvbWVrZXkzc29tZWtleTQ='),  # 32 len bytes key
            (({SettingsHelper.env_secret_name: None}, 'c29tZWtleTFzb21la2V5MnNvbWVrZXkzc29tZWtleTQ=', b''),
             b'c29tZWtleTFzb21la2V5MnNvbWVrZXkzc29tZWtleTQ='),
            (({SettingsHelper.env_secret_name: None}, None, b'c29tZWtleTFzb21la2V5MnNvbWVrZXkzc29tZWtleTQ='),
             b'c29tZWtleTFzb21la2V5MnNvbWVrZXkzc29tZWtleTQ='),
            (({SettingsHelper.env_secret_name: 'c29tZWtleTFzb21la2V5MnNvbWVrZXkzc29tZWtleTQ='}, 'ANYKEY1', b''),
             b'c29tZWtleTFzb21la2V5MnNvbWVrZXkzc29tZWtleTQ='),
            (({SettingsHelper.env_secret_name: 'c29tZWtleTFzb21la2V5MnNvbWVrZXkzc29tZWtleTQ='}, 'ANYKEY2', b'ANYKEY3'),
             b'c29tZWtleTFzb21la2V5MnNvbWVrZXkzc29tZWtleTQ='),
        ],
        indirect=True
    )
    def test_settings_helper_init(self, test_obj_settings_helper: SettingsHelper, test_exp_param_fixture):
        # Check initial params are exist
        assert isinstance(test_obj_settings_helper.logger, Logger)

        assert hasattr(test_obj_settings_helper, 'key')
        assert test_obj_settings_helper.key == test_exp_param_fixture

    @pytest.mark.parametrize(
        "test_obj_settings_helper, test_exp_param_fixture",
        [
            (({SettingsHelper.env_secret_name: 'c29tZWtleTFzb21la2V5MnNvbWVrZXkzc29tZWtleTQ='}, 'ANYKEY0', b'ANYKEY1'),
             'test_data'),
        ],
        indirect=True
    )
    def test_encrypt_data(self, test_obj_settings_helper: SettingsHelper, test_exp_param_fixture):
        encrypted_data = test_obj_settings_helper.encrypt_data(test_exp_param_fixture)
        assert test_obj_settings_helper.decrypt_data(encrypted_data) == test_exp_param_fixture  # type: ignore

    @pytest.mark.parametrize(
        "test_obj_settings_helper, test_exp_param_fixture",
        [
            (({SettingsHelper.env_secret_name: 'c29tZWtleTFzb21la2V5MnNvbWVrZXkzc29tZWtleTQ='}, 'ANYKEY2', b'ANYKEY3'),
             b'gAAAAABmS0svwU1fjdaizp0LU89WSvLBodh1RLR5E2EGSNp9wt3PZfFZsIrc_N_NuKyws7uC-BGtd0iqIsCTbqSuf7PaZf2oGQ=='),
        ],
        indirect=True
    )
    def test_decrypt_data(self, test_obj_settings_helper: SettingsHelper,
                          test_exp_param_fixture):
        assert test_obj_settings_helper.decrypt_data(test_exp_param_fixture) == 'test_data'  # type: ignore

    @pytest.mark.parametrize(
        "test_obj_settings_helper, test_exp_param_fixture",
        [
            (({SettingsHelper.env_secret_name: 'c29tZWtleTFzb21la2V5MnNvbWVrZXkzc29tZWtleTQ='}, 'ANYKEY0', b'ANYKEY1'),
             b'somekey1somekey2somekey3somekey4'),
        ],
        indirect=True
    )
    def test_get_app_key(self, test_obj_settings_helper: SettingsHelper, test_exp_param_fixture):
        # Try to decode the key string
        decoded_bytes = base64.b64decode(test_obj_settings_helper.key, validate=True)
        assert decoded_bytes == test_exp_param_fixture
        # If decoding is successful, check if encoding back gives the same string
        # This ensures padding and character checks are adhered to
        assert base64.b64encode(decoded_bytes) == test_obj_settings_helper.key

    @pytest.mark.parametrize(
        "test_obj_settings_helper, test_exp_param_fixture",
        [
            (({}, None, b''), ('', '', '')),
            (({}, None, b''), ('object_name1', 'object_name1', 'object_name1')),
            (({}, None, b''), ('lexeme1:key1', 'lexeme1', 'key1')),
            (({}, None, b''), (':key1', '', 'key1')),
        ],
        indirect=True
    )
    def test_parse_object_name(self, test_obj_settings_helper: SettingsHelper, test_exp_param_fixture):
        # Get testing parameters
        object_name, exp_lexeme, exp_setting_key = test_exp_param_fixture
        # Parse the object name in case it contains a combination of lexeme and setting keys
        lexeme, setting_key = test_obj_settings_helper.parse_object_name(object_name)
        assert lexeme == exp_lexeme
        assert setting_key == exp_setting_key
