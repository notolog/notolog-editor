"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Async lifecycle tests for the OpenAI API module.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

import asyncio
from unittest.mock import MagicMock

import pytest
from PySide6.QtNetwork import QNetworkReply

from notolog.modules.openai_api.module_core import ModuleCore


class SignalStub:
    def __init__(self):
        self.callbacks = []

    def connect(self, callback):
        self.callbacks.append(callback)

    def disconnect(self, callback):
        self.callbacks.remove(callback)

    def emit(self):
        for callback in list(self.callbacks):
            callback()


@pytest.fixture
def module_core(mocker):
    core = ModuleCore()
    core.api_helper = mocker.MagicMock()
    core.api_helper.convert_temperature.return_value = 0.2
    core.api_helper.init_request.return_value = object()
    core.api_helper.init_request_params.return_value = object()
    core.init_callback = mocker.MagicMock()
    core.finished_callback = mocker.MagicMock()
    return core


@pytest.mark.asyncio
async def test_stop_aborts_and_awaits_active_request(module_core):
    reply = MagicMock()
    reply.finished = SignalStub()
    reply.error.return_value = QNetworkReply.NetworkError.NoError
    reply.isRunning.side_effect = [True, False]
    module_core.network_manager = MagicMock()
    module_core.network_manager.post.return_value = reply

    task = asyncio.create_task(module_core.run_generator([], 1, 2))
    module_core.generator_task = task
    await asyncio.sleep(0)

    assert module_core.init_callback.call_count == 1
    await module_core.stop_generator()

    reply.abort.assert_called_once_with()
    assert task.cancelled()
    assert module_core.active_reply is None
    assert module_core.finished_callback.call_count == 1


@pytest.mark.asyncio
async def test_response_is_processed_once_after_reply_finishes(module_core, mocker):
    reply = MagicMock()
    reply.finished = SignalStub()
    reply.error.return_value = QNetworkReply.NetworkError.NoError
    module_core.network_manager = MagicMock()
    module_core.network_manager.post.return_value = reply
    handle_response = mocker.patch.object(module_core, 'handle_response')

    task = asyncio.create_task(module_core.run_generator([], 3, 4))
    module_core.generator_task = task
    await asyncio.sleep(0)
    reply.finished.emit()
    await task

    handle_response.assert_called_once_with(reply, 3, 4, None)
    reply.deleteLater.assert_called_once_with()
    assert module_core.active_reply is None
