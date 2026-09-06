"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Test bounded PCM buffering, pause, drain, and audio-device cleanup.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from types import SimpleNamespace
from unittest.mock import Mock
import sys

import pytest

from notolog.modules.text_to_speech.audio_output import AudioOutput


@pytest.fixture
def device(monkeypatch):
    stream = Mock(active=True, time=0.0)
    factory = Mock(return_value=stream)
    monkeypatch.setitem(sys.modules, 'sounddevice', SimpleNamespace(RawOutputStream=factory))
    audio = AudioOutput(1024)
    yield audio, stream, factory
    audio.close()


def consume(audio, timestamp=0.0):
    result = bytearray(1024)
    audio._callback(result, 512, SimpleNamespace(outputBufferDacTime=timestamp, currentTime=audio.stream.time), None)
    return bytes(result)


def test_ring_wraparound_and_backpressure(device):
    audio, _, _ = device
    content = bytes(range(256)) * 24
    assert audio.write(content) == 4096
    assert audio.write(content) == 0
    played = consume(audio) + consume(audio) + consume(audio)
    assert audio.write(content[4096:]) == 2048
    played += consume(audio) + consume(audio) + consume(audio)
    assert played == content
    assert audio.write_available == len(audio.buffer)


def test_pause_retains_audio_and_drain_waits_for_dac(device):
    audio, stream, _ = device
    pcm = b'\x01\x02' * 512
    audio.write(pcm)
    audio.paused = True
    assert consume(audio) == bytes(1024)
    assert audio.consumed == 0
    assert not audio.drained
    audio.paused = False
    assert consume(audio, 2.0) == pcm
    stream.time = 2.49
    assert not audio.drained
    stream.time = 2.5
    assert audio.drained


def test_close_discards_audio_and_is_idempotent(device):
    audio, stream, _ = device
    audio.write(b'\x01\x02' * 100)
    audio.close()
    audio.close()
    stream.abort.assert_called_once()
    stream.close.assert_called_once()
    assert not any(audio.buffer)
    assert consume(audio) == bytes(1024)
    with pytest.raises(RuntimeError, match='stopped'):
        audio.write(b'\x01\x02')


def test_device_loss_is_reported(device):
    audio, stream, _ = device
    stream.active = False
    with pytest.raises(RuntimeError, match='stopped'):
        _ = audio.drained


def test_failed_start_closes_stream(monkeypatch):
    stream = Mock()
    stream.start.side_effect = RuntimeError('device busy')
    monkeypatch.setitem(sys.modules, 'sounddevice', SimpleNamespace(RawOutputStream=lambda **_: stream))
    with pytest.raises(RuntimeError, match='device busy'):
        AudioOutput(22050)
    stream.close.assert_called_once()


def test_pcm_format_uses_no_decoder(device):
    _, _, factory = device
    options = factory.call_args.kwargs
    assert options['channels'] == 1
    assert options['dtype'] == 'int16'
    assert options['samplerate'] == 1024


def test_activity_follows_dac_time_including_final_samples_and_silence(device):
    audio, stream, _ = device
    audio.write(b'\x01\x02' * 512)
    assert not audio.playing
    consume(audio, 2.0)
    assert not audio.playing
    stream.time = 2.0
    assert audio.playing
    stream.time = 2.49
    assert audio.playing
    stream.time = 2.5
    assert not audio.playing
    audio.write(bytes(1024))
    consume(audio, 2.5)
    assert not audio.playing
    audio.close()
    assert not audio.playing
