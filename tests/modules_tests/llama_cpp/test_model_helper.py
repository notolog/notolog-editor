# tests/modules_tests/llama_cpp/test_model_helper.py

from notolog.app_config import AppConfig

from .. import is_module_available

# Explicitly check if the module is available to avoid importing non-existent libraries.
if is_module_available('llama_cpp'):
    from notolog.modules.llama_cpp.model_helper import ModelHelper
    from llama_cpp import Llama
else:
    from PySide6.QtCore import QObject as ModelHelper, QObject as Llama

import os
import pytest
import logging

from unittest.mock import MagicMock


class TestModelHelper:

    @pytest.fixture(scope="function", autouse=True)
    def test_obj_app_config(self, mocker):
        # Mock AppConfig's get_logger_level method to suppress logging during tests.
        mocker.patch.object(AppConfig, 'get_logger_level', return_value=logging.NOTSET)

        # Create an AppConfig instance and set it to test mode.
        _app_config = AppConfig()
        _app_config.set_test_mode(True)

        yield _app_config

    @pytest.fixture(scope="function")
    def test_model_helper(self, mocker, request):
        """
        Testing object fixture.
        May contain minimal logic for testing purposes.
        """

        # Retrieve parameter values from the test request.
        model_path, context_window, chat_format, search_options = request.param if hasattr(request, 'param') \
            else ('', None, None, None)

        # Reload as new instance to avoid param caching
        ModelHelper.reload()

        # Allow setting a fake model path for testing purposes
        mocker.patch.object(os.path, 'isfile', return_value=True)

        model_helper = ModelHelper(model_path=model_path, n_ctx=context_window, chat_format=chat_format,
                                   search_options=search_options)

        yield model_helper

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

    @pytest.mark.parametrize(
        "test_model_helper, test_params_fixture, test_exp_params_fixture",
        [
            # No model metadata available
            (('', None, None, None), {}, ''),
            (('model_path1', None, None, None), {}, 'model_path1'),
            (('model_path1.smth', None, None, None), {}, 'model_path1.smth'),
            ((os.path.join('model_dir1', 'model_path1.smth'), None, None, None), {}, 'model_path1.smth'),
            # Model metadata available but no model name specified
            (('', None, None, None), {'smth1.param1': 'model_name1'}, ''),
            (('model_path1', None, None, None), {'smth1.param1': 'model_name1'}, 'model_path1'),
            (('model_path1.smth', None, None, None), {'smth1.param1': 'model_name1'}, 'model_path1.smth'),
            ((os.path.join('model_dir1', 'model_path1.smth'), None, None, None),
             {'smth1.param1': 'model_name1'}, 'model_path1.smth'),
            # Model metadata available
            (('', None, None, None), {'general.name': 'model_name1'}, 'model_name1'),
            (('model_path1', None, None, None), {'general.name': 'model_name1'}, 'model_name1'),
            (('model_path1.smth', None, None, None), {'general.name': 'model_name1'}, 'model_name1'),
            ((os.path.join('model_dir1', 'model_path1.smth'), None, None, None),
             {'general.name': 'model_name1'}, 'model_name1'),
        ],
        indirect=True
    )
    def test_get_model_name(self, test_model_helper: ModelHelper, test_params_fixture, test_exp_params_fixture):
        # Extract test and expected params
        model_metadata = test_params_fixture
        exp_model_name = test_exp_params_fixture

        # Mock the model object
        model = MagicMock(spec=Llama)
        setattr(model, 'metadata', model_metadata)
        test_model_helper.model = model

        # Run the method under test
        model_name = test_model_helper.get_model_name()

        # Verify that the returned model name matches the expected model name
        assert model_name == exp_model_name
