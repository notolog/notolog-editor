"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Opt-in smoke test for the installed speech runtime, local models, and optional playback.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

import asyncio
import os
from types import SimpleNamespace

import pytest
from PySide6.QtCore import QProcess

from notolog.modules.text_to_speech.config import DEFAULTS, model_paths, runtime_path
from notolog.modules.text_to_speech.native_runtime import NativeRuntime


@pytest.mark.asyncio
async def test_real_runtime_streams_reuses_models_and_stops(qapp):
    executable = os.environ.get('NOTOLOG_TTS_RUNTIME', '')
    models = os.environ.get('NOTOLOG_TTS_MODEL_DIR', '')
    playback = os.environ.get('NOTOLOG_TTS_PLAYBACK', '')
    if not (executable or models or playback):
        pytest.skip('Set NOTOLOG_TTS_RUNTIME and NOTOLOG_TTS_MODEL_DIR to test local speech inference.')
    assert executable and models, 'Both NOTOLOG_TTS_RUNTIME and NOTOLOG_TTS_MODEL_DIR are required.'
    assert playback in ('', '0', '1'), 'NOTOLOG_TTS_PLAYBACK must be 0 or 1.'
    settings = SimpleNamespace(**{name: default for name, (_, default) in DEFAULTS.items()})
    settings.tts_runtime_path = executable
    settings.tts_model_directory = models
    assert runtime_path(settings), 'NOTOLOG_TTS_RUNTIME must name an executable file.'
    model_paths(settings)
    adapter = NativeRuntime(settings)
    sink = None

    async def pump_events():
        while True:
            qapp.processEvents()
            await asyncio.sleep(0.005)

    async def synthesize():
        nonlocal sink
        await adapter.start()
        assert adapter.loaded
        assert 8000 <= adapter.rate <= 192000
        process = adapter.process
        pid = process.processId()
        assert pid > 0
        if playback == '1':
            from notolog.modules.text_to_speech.audio_output import AudioOutput
            sink = AudioOutput(adapter.rate)
        for text in ('Hello from Notolog.', 'This is a second speech request.'):
            await adapter.start()
            assert adapter.process is process and process.processId() == pid
            byte_count = 0
            audible = False
            async for pcm in adapter.stream(text):
                assert pcm and len(pcm) % 2 == 0
                byte_count += len(pcm)
                assert byte_count <= adapter.rate * 2 * 60, 'Unexpectedly long output for a short sentence.'
                audible |= any(pcm)
                if sink is not None:
                    offset = 0
                    while offset < len(pcm):
                        offset += sink.write(pcm[offset:])
                        await asyncio.sleep(0.005)
            assert byte_count >= adapter.rate // 5 and audible
            if sink is not None:
                while not sink.drained:
                    await asyncio.sleep(0.01)

        # Stop while the worker is waiting for acknowledgement of a real PCM chunk.
        stream = adapter.stream('Stop this speech request before it finishes.')
        try:
            assert await anext(stream)
            adapter.close()
            assert process.state() == QProcess.ProcessState.NotRunning
            assert not adapter.loaded
        finally:
            await stream.aclose()

    pump = asyncio.create_task(pump_events())
    try:
        await asyncio.wait_for(synthesize(), timeout=600)
    finally:
        adapter.close()
        if sink is not None:
            sink.close()
        pump.cancel()
        await asyncio.gather(pump, return_exceptions=True)
