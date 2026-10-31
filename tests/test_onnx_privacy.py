import builtins
import logging
import os
from pathlib import Path
import runpy
from types import SimpleNamespace
from unittest.mock import Mock

import pytest


def test_genai_telemetry_is_disabled_before_native_import(monkeypatch):
    original_import = builtins.__import__
    imported = []

    def checked_import(name, *args, **kwargs):
        if name == 'onnxruntime_genai':
            assert os.environ['ORT_DISABLE_TELEMETRY'] == '1'
            imported.append(name)
            return SimpleNamespace(**dict.fromkeys(
                ('Config', 'Generator', 'GeneratorParams', 'Model', 'Tokenizer', 'TokenizerStream'), object))
        return original_import(name, *args, **kwargs)

    monkeypatch.setenv('ORT_DISABLE_TELEMETRY', '0')
    monkeypatch.setattr(builtins, '__import__', checked_import)
    runpy.run_path(str(Path(__file__).resolve().parents[1] / 'notolog/modules/ondevice_llm/model_helper.py'))
    assert imported == ['onnxruntime_genai']


def test_generation_does_not_log_response_content(caplog):
    from notolog.modules.ondevice_llm.model_helper import ModelHelper

    helper = object.__new__(ModelHelper)
    helper.logger = logging.getLogger('test.ondevice')
    helper.generator = Mock()
    helper.generator.is_done.return_value = False
    helper.generator.get_next_tokens.return_value = [42]
    helper.tokenizer_stream = Mock()
    helper.tokenizer_stream.decode.return_value = 'synthetic response'
    with caplog.at_level(logging.DEBUG):
        assert helper.generate_output() == 'synthetic response'
    assert 'synthetic response' not in caplog.text


@pytest.mark.parametrize('message_type', ['USER_INPUT', 'RESPONSE'])
def test_prompt_history_does_not_log_message_content(caplog, message_type):
    from notolog.modules.ondevice_llm.prompt_manager import PromptManager, EnumMessageType

    manager = SimpleNamespace(
        logger=logging.getLogger('test.ondevice.history'), add_request=Mock(), add_response=Mock())
    with caplog.at_level(logging.DEBUG):
        PromptManager.add_message(manager, 'synthetic private message', 1, 2, getattr(EnumMessageType, message_type))
    assert 'synthetic private message' not in caplog.text
    if message_type == 'USER_INPUT':
        manager.add_request.assert_called_once_with('synthetic private message', 1)
    else:
        manager.add_response.assert_called_once_with('synthetic private message', 2, 1)
