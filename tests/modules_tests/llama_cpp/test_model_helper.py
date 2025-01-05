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
            (('', None, None, None), None, (False, "Model path is not set in 'ModelHelper'")),
            (('model_path1', None, None, None), None, (True, "")),
            (('', None, None, None), Llama, (False, "")),
        ],
        indirect=True
    )
    def test_init_model(self, mocker, test_model_helper: ModelHelper, test_params_fixture, test_exp_params_fixture):
        # Extract test and expected params
        model = test_params_fixture
        exp_call, exp_exception = test_exp_params_fixture

        # Test the case when the model is pre-set
        if model:
            test_model_helper.model = model

        # Mock the model object
        mocked_model = MagicMock(spec=Llama)

        test_model = mocker.patch.object(Llama, '__init__', return_value=mocked_model)

        try:
            # Run the method under test
            test_model_helper.init_model()
        except (RuntimeError, ValueError, Exception) as e:
            assert str(exp_exception) in str(e)

        if exp_call:
            # Verify the method called with the expected params
            test_model.assert_called_once_with(
                model_path=test_model_helper.model_path,
                chat_format=test_model_helper.chat_format,
                n_ctx=test_model_helper.n_ctx,
                verbose=False
            )
        else:
            test_model.assert_not_called()

    @pytest.mark.parametrize(
        "test_params_fixture, test_exp_params_fixture",
        [
            (('', []), []),
            (('text1', [1, 2, 3]), [1, 2, 3]),
        ],
        indirect=True
    )
    def test_get_input_tokens(self, mocker, test_model_helper: ModelHelper, test_params_fixture, test_exp_params_fixture):
        # Extract test and expected params
        text, tokens = test_params_fixture
        exp_result = test_exp_params_fixture

        # Mock the model object
        mocked_model = MagicMock(spec=Llama)
        test_model_tokenize = mocker.patch.object(mocked_model, 'tokenize', return_value=tokens)

        # Set the model
        test_model_helper.model = mocked_model

        # Run the method under test
        result = test_model_helper.get_input_tokens(text)

        test_model_tokenize.asset.called_once_with(text.encode('utf-8'))

        assert result == exp_result

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

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "input_iterator, expected_outputs, expected_logs",
        [
            # Case 1: 'role' in delta
            (
                    [{'choices': [{'delta': {'role': 'assistant'}}]}],
                    [''],
                    ["Role output: assistant: "]
            ),
            # Case 2: 'content' in delta
            (
                    [{'choices': [{'delta': {'content': 'Hello, world'}}]}],
                    ['Hello, world'],
                    ["Output token(s): Hello, world"]
            ),
            # Case 3: 'finish_reason' in delta
            (
                    [{'choices': [{'delta': {'finish_reason': 'length'}}]}],
                    [''],
                    ["Output finished with the reason: 'length'"]
            ),
            # Case 4: Mixed inputs
            (
                    [
                        {'choices': [{'delta': {'role': 'assistant'}}]},
                        {'choices': [{'delta': {'content': 'Hello, world'}}]},
                        {'choices': [{'delta': {'finish_reason': 'length'}}]}
                    ],
                    ['', 'Hello, world', ''],
                    [
                        "Role output: assistant: ",
                        "Output token(s): Hello, world",
                        "Output finished with the reason: 'length'"
                    ]
            ),
        ]
    )
    async def test_async_wrap_iterator(self, test_model_helper: ModelHelper, input_iterator, expected_outputs,
                                       expected_logs):

        # Create an async iterator from the input data
        def mock_iterator():
            for item in input_iterator:
                yield item

        # Collect outputs from the async_wrap_iterator
        outputs = []
        async for output in test_model_helper.async_wrap_iterator(mock_iterator()):
            outputs.append(output)

        # Assert the outputs match the expected results
        assert outputs == expected_outputs
