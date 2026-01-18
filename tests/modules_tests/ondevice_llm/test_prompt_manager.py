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

from notolog.app_config import AppConfig
from notolog.ui.ai_assistant.ai_assistant import EnumMessageType

from .. import is_module_available

# Explicitly check if the module is available to avoid importing non-existent libraries.
if is_module_available('ondevice_llm'):
    from notolog.modules.ondevice_llm.prompt_manager import PromptManager
else:
    from PySide6.QtCore import QObject as PromptManager

import pytest
import logging


class TestPromptManager:

    @pytest.fixture(scope="function", autouse=True)
    def test_obj_app_config(self, mocker):
        # Mock AppConfig's get_logger_level method to suppress logging during tests.
        mocker.patch.object(AppConfig, 'get_logger_level', return_value=logging.NOTSET)

        # Create an AppConfig instance and set it to test mode.
        _app_config = AppConfig()
        _app_config.set_test_mode(True)

        yield _app_config

    @pytest.fixture(scope="function")
    def test_prompt_manager(self, request):
        """
        Testing object fixture.
        May contain minimal logic for testing purposes.
        """

        # Retrieve parameter values from the test request.
        system_prompt, max_history_size, reload = request.param if hasattr(request, 'param') else (None, None, None)

        if reload:
            # Reload the singleton instance to ensure a fresh start for each test.
            PromptManager.reload()

        yield PromptManager(system_prompt=system_prompt, max_history_size=max_history_size, parent=None)

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
        "test_prompt_manager, test_exp_params_fixture",
        [
            (('prompt1', None, False), ('**system**:\nprompt1', '<|endoftext|><|system|>\nprompt1<|end|>\n')),
            ((None, None, False), ('**system**:\nprompt1', '<|endoftext|><|system|>\nprompt1<|end|>\n')),
            (('prompt2', None, True), ('**system**:\nprompt2', '<|endoftext|><|system|>\nprompt2<|end|>\n')),
            ((None, None, True), ('', '<|endoftext|>')),
        ],
        indirect=True
    )
    def test_init_and_get_prompt_history(self, test_prompt_manager: PromptManager, test_exp_params_fixture):
        # Test initialization and prompt history retrieval.
        exp_history_result, exp_prompt_result = test_exp_params_fixture

        history_result = test_prompt_manager.get_history()

        assert history_result == exp_history_result

        prompt_result = test_prompt_manager.get_prompt()

        assert prompt_result == exp_prompt_result

    @pytest.mark.parametrize(
        "test_prompt_manager, test_params_fixture, test_exp_params_fixture",
        [
            # Define test cases for getting a single prompt message with expected results.
            ((None, None, None), None, '<|user|>\nNone<|end|>\n<|assistant|>\n'),
            ((None, None, None), 'content0', '<|user|>\ncontent0<|end|>\n<|assistant|>\n'),
            ((None, None, None), 'content1', '<|user|>\ncontent1<|end|>\n<|assistant|>\n'),
        ],
        indirect=True
    )
    def test_get_prompt_message(self, test_prompt_manager: PromptManager,
                                test_params_fixture, test_exp_params_fixture):
        content = test_params_fixture
        exp_result = test_exp_params_fixture

        result = test_prompt_manager.get_prompt_message(str(content))

        assert result == exp_result

    @pytest.mark.parametrize(
        "test_prompt_manager, test_params_fixture, test_exp_params_fixture",
        [
            # Resetting the history
            (('prompt0', None, True), ('', 0, 0, EnumMessageType.USER_INPUT),
             '**system**:\nprompt0\n\n**user**:'),
            (('prompt1', None, True), ('smthU1', 0, 0, EnumMessageType.USER_INPUT),
             '**system**:\nprompt1\n\n**user**:\nsmthU1'),
            (('prompt2', None, True), ('smthU2', 123, 456, EnumMessageType.USER_INPUT),
             '**system**:\nprompt2\n\n**user**:\nsmthU2'),
            (('prompt3', None, True), ('smthA3', 0, 0, EnumMessageType.RESPONSE),
             '**system**:\nprompt3'),  # Not added as no match found
            (('prompt4', None, True), ('smthU4', 0, 0, EnumMessageType.USER_INPUT),
             '**system**:\nprompt4\n\n**user**:\nsmthU4'),
            # Remembering the history (by msg_id), but with a zero limit
            (('prompt111', 0, True), ('smthU111', 0, 0, EnumMessageType.USER_INPUT),
             '**system**:\nprompt111\n\n**user**:\nsmthU111'),
            (('promptXYZ', None, False), ('smthA222', 0, 1, EnumMessageType.RESPONSE),
             '**system**:\nprompt111\n\n**user**:\nsmthU111\n\n**assistant**:\nsmthA222'),
            # Remembering the history (by msg_id), but with a limit
            (('prompt111', 3, True), ('smthU111', 0, 0, EnumMessageType.USER_INPUT),
             '**system**:\nprompt111\n\n**user**:\nsmthU111'),
            (('promptXYZ', None, False), ('smthA222', 0, 1, EnumMessageType.RESPONSE),
             '**system**:\nprompt111\n\n**user**:\nsmthU111\n\n**assistant**:\nsmthA222'),
            ((None, None, False), ('smthU333', 2, 0, EnumMessageType.USER_INPUT),
             '**system**:\nprompt111\n\n**user**:\nsmthU111\n\n**assistant**:\nsmthA222\n\n**user**:\nsmthU333'),
            ((None, None, False), ('smthA444', 2, 4, EnumMessageType.RESPONSE),
             '**system**:\nprompt111\n\n**user**:\nsmthU111\n\n**assistant**:\nsmthA222\n\n**user**:\nsmthU333'
             '\n\n**assistant**:\nsmthA444'),
            ((None, None, False), ('smthA123', 0, 3, EnumMessageType.RESPONSE),
             '**system**:\nprompt111\n\n**user**:\nsmthU111\n\n**assistant**:\nsmthA123\n\n**user**:\nsmthU333'
             '\n\n**assistant**:\nsmthA444'),
        ],
        indirect=True
    )
    def test_add_message(self, mocker, test_prompt_manager: PromptManager,
                         test_params_fixture, test_exp_params_fixture):
        message_text, request_msg_id, response_msg_id, message_type = test_params_fixture
        exp_result = test_exp_params_fixture

        # Retrieve callback methods for verification.
        mock_add_request = mocker.patch.object(test_prompt_manager, 'add_request', wraps=test_prompt_manager.add_request)
        mock_add_response = mocker.patch.object(test_prompt_manager, 'add_response', wraps=test_prompt_manager.add_response)

        test_prompt_manager.add_message(message_text, request_msg_id, response_msg_id, message_type)

        if message_type == EnumMessageType.USER_INPUT:
            mock_add_request.assert_called_once()
            # Check the parameters passed to the mocked function(s)
            assert str(mock_add_request.call_args) == "call('%s', %d)" % (message_text, request_msg_id)
        elif message_type == EnumMessageType.RESPONSE:
            mock_add_response.assert_called_once()
            # Check the parameters passed to the mocked function(s)
            assert (str(mock_add_response.call_args) == "call('%s', %d, %d)"
                    % (message_text, response_msg_id, request_msg_id))
        else:
            mock_add_request.assert_not_called()
            mock_add_response.assert_not_called()

        result = test_prompt_manager.get_history()

        assert result == exp_result

    @pytest.mark.parametrize(
        "test_prompt_manager, test_params_fixture, test_exp_params_fixture",
        [
            # Reload history and append new system prompt
            ((None, None, True), ('', None), [{'system': {'text': '', 'msg_id': None}}]),
            ((None, None, None), ('smth1', None), [{'system': {'text': '', 'msg_id': None}}]),
        ],
        indirect=True
    )
    def test_add_system(self, mocker, test_prompt_manager: PromptManager,
                        test_params_fixture, test_exp_params_fixture):
        system_instruct, msg_id = test_params_fixture
        exp_history_result = test_exp_params_fixture

        test_prompt_manager.add_system(system_instruct, msg_id)

        assert getattr(test_prompt_manager, 'history') == exp_history_result

    @pytest.mark.parametrize(
        "test_prompt_manager, test_params_fixture, test_exp_params_fixture",
        [
            # Reload history and append new request
            ((None, None, True), ('', 0),
             [{'user': {'text': '', 'msg_id': 0}, 'assistant': None}]),
            # Append to the history
            ((None, None, None), ('smth1', 1),
             [{'user': {'text': '', 'msg_id': 0}, 'assistant': None},
              {'user': {'text': 'smth1', 'msg_id': 1}, 'assistant': None}]),
        ],
        indirect=True
    )
    def test_add_request(self, test_prompt_manager: PromptManager,
                         test_params_fixture, test_exp_params_fixture):
        request_text, request_msg_id = test_params_fixture
        exp_history_result = test_exp_params_fixture

        test_prompt_manager.add_request(request_text, request_msg_id)

        assert getattr(test_prompt_manager, 'history') == exp_history_result

    @pytest.mark.parametrize(
        "test_prompt_manager, test_params_fixture, test_exp_params_fixture",
        [
            # Not added
            ((None, None, True), ('', 0, None, [{'user': {'text': '', 'msg_id': 0}}]),
             [{'user': {'text': '', 'msg_id': 0}}]),
            # Added by matching user request msg_id
            ((None, None, True), ('', 0, 0, [{'user': {'text': '', 'msg_id': 0}}]),
             [{'user': {'text': '', 'msg_id': 0}, 'assistant': {'text': '', 'msg_id': 0}}]),
            # Added by a fallback 'assistant': None match
            ((None, None, True), ('', 0, None, [{'user': {'text': '', 'msg_id': 0}, 'assistant': None}]),
             [{'user': {'text': '', 'msg_id': 0}, 'assistant': {'text': '', 'msg_id': 0}}]),
        ],
        indirect=True
    )
    def test_add_response(self, test_prompt_manager: PromptManager,
                          test_params_fixture, test_exp_params_fixture):
        response_text, response_msg_id, request_msg_id, history = test_params_fixture
        exp_history_result = test_exp_params_fixture

        setattr(test_prompt_manager, 'history', history)

        test_prompt_manager.add_response(response_text, response_msg_id, request_msg_id)

        assert getattr(test_prompt_manager, 'history') == exp_history_result

    @pytest.mark.parametrize(
        "test_prompt_manager, test_params_fixture, test_exp_params_fixture",
        [
            # Mocking the history after reload
            ((None, None, True), ([{'system': {}}], ''), None),
            ((None, None, None), ([{'system': {}}], 'system'), {}),
            ((None, None, None), ([
                {'system': {'text': 'system1', 'msg_id': 1}},
                {'user': {'text': 'user1', 'msg_id': 2}},
                {'assistant': {'text': 'assistant1', 'msg_id': 3}}], 'system'),
             {'msg_id': 1, 'text': 'system1'}),
            ((None, None, None), ([
                {'system': {'text': 'system1', 'msg_id': 1}},
                {'user': {'text': 'user1', 'msg_id': 2}},
                {'assistant': {'text': 'assistant1', 'msg_id': 3}}], 'user'),
             {'msg_id': 2, 'text': 'user1'}),
            ((None, None, None), ([
                {'system': {'text': 'system1', 'msg_id': 1}},
                {'user': {'text': 'user1', 'msg_id': 2}},
                {'assistant': {'text': 'assistant1', 'msg_id': 3}}], 'assistant'),
             {'msg_id': 3, 'text': 'assistant1'}),
            ((None, None, None), ([
                {'system': {'text': 'system1', 'msg_id': 1}},
                {'user': {'text': 'user1', 'msg_id': 2}},
                {'assistant': {'text': 'assistant1', 'msg_id': 3}},
                {'user': {'text': 'user2', 'msg_id': 4}},], 'user'),
             {'msg_id': 4, 'text': 'user2'}),
            ((None, None, None), ([
                {'system': {'text': 'system1', 'msg_id': 1}},
                {'user': {'text': 'user2', 'msg_id': 4}},
                {'assistant': {'text': 'assistant1', 'msg_id': 3}},
                {'user': {'text': 'user1', 'msg_id': 2}}, ], 'user'),
             {'msg_id': 2, 'text': 'user1'}),
        ],
        indirect=True
    )
    def test_find_last_message_by_role(self, test_prompt_manager: PromptManager,
                                       test_params_fixture, test_exp_params_fixture):
        history, role = test_params_fixture
        exp_result = test_exp_params_fixture

        setattr(test_prompt_manager, 'history', history)

        result = test_prompt_manager.find_last_message_by_role(role)

        assert result == exp_result
