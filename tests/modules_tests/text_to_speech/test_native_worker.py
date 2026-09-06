"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Verify native worker messages, PCM callbacks, privacy, and resource cleanup.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

import base64
import ctypes
import io
import json
import os
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from notolog.modules.text_to_speech import native_worker as worker

CONFIGURATION = {'library': '/runtime/lib/speech', 'paths': ['magpie.gguf', 'codec.gguf', 'tokenizers']}
REQUEST = {'text': 'Hello, 世界.', 'language': 'en', 'voice': 'Aria'}
PCM = b'\x01\x02\x03\x04'


class FakeLibrary:
    """Exercise the real ctypes structures and callback with a controlled native API."""

    def __init__(self, *, version=b'nemo-speech-tts 0.1.0', create_code=0, code=0,
                 detail=b'private note text', diagnostics=False):
        self.create_code = create_code
        self.code = code
        self.diagnostics = diagnostics
        self.requests = []
        self.nemo_speech_tts_version = Mock(return_value=version)
        self.nemo_speech_tts_create = Mock(side_effect=self.create)
        self.nemo_speech_tts_destroy = Mock()
        self.nemo_speech_tts_sample_rate = Mock(return_value=22050)
        self.nemo_speech_tts_runtime_config_default = Mock(side_effect=worker.Runtime)
        self.nemo_speech_tts_synthesis_options_default = Mock(side_effect=worker.Options)
        self.nemo_speech_tts_last_error = Mock(return_value=detail)
        self.nemo_speech_tts_synthesize_text = Mock(side_effect=self.synthesize)

    def create(self, config_pointer, handle_pointer):
        config = ctypes.cast(config_pointer, ctypes.POINTER(worker.Config)).contents
        model = config.model.contents
        self.paths = (model.magpie, model.codec, model.tokenizer)
        self.longform = config.runtime.contents.longform_mode
        ctypes.cast(handle_pointer, ctypes.POINTER(ctypes.c_void_p))[0] = ctypes.c_void_p(42)
        if self.diagnostics:
            os.write(1, b'private native stdout\n')
            os.write(2, b'private native stderr\n')
        return self.create_code

    def synthesize(self, handle, options_pointer, text, callback, user_data, cancel):
        options = ctypes.cast(options_pointer, ctypes.POINTER(worker.Options)).contents
        self.requests.append((text, options.language, options.voice, options.speaker))
        samples = (ctypes.c_uint8 * len(PCM)).from_buffer_copy(PCM)
        if not callback(samples, len(PCM), None):
            return 4
        return self.code


@pytest.fixture
def harness(monkeypatch):
    def run(lines, *, library=None, platform=sys.platform, output=None):
        library = library or FakeLibrary()
        output = output if output is not None else io.StringIO()
        native_os = SimpleNamespace(
            devnull=os.devnull, path=os.path, dup=Mock(return_value=10), dup2=Mock(),
            fdopen=Mock(return_value=output), add_dll_directory=Mock(return_value=Mock()),
        )
        monkeypatch.setattr(worker, 'os', native_os)
        monkeypatch.setattr(worker, 'sys', SimpleNamespace(
            platform=platform, stdin=io.StringIO(lines),
            stdout=SimpleNamespace(fileno=lambda: 1), stderr=SimpleNamespace(fileno=lambda: 2),
        ))
        monkeypatch.setattr(worker.c, 'CDLL', Mock(return_value=library))
        if platform != 'win32':
            resource = SimpleNamespace(RLIMIT_CORE=4, setrlimit=Mock())
            monkeypatch.setitem(sys.modules, 'resource', resource)
        worker.main()
        events = [json.loads(line) for line in output.getvalue().splitlines()]
        if platform != 'win32':
            resource.setrlimit.assert_called_once_with(resource.RLIMIT_CORE, (0, 0))
        return events, library, native_os

    return run


def protocol(*requests, acknowledgement='continue', configuration=None):
    lines = [json.dumps(CONFIGURATION if configuration is None else configuration)]
    for request in requests:
        lines.extend((json.dumps(request), acknowledgement))
    return '\n'.join(lines) + '\n'


@pytest.mark.parametrize('platform', ['linux', 'darwin', 'win32'])
def test_worker_streams_multiple_requests_and_releases_resources(harness, platform):
    second = dict(REQUEST, text='Another sentence.', language='de', voice='Jason')
    events, library, native_os = harness(protocol(REQUEST, second), platform=platform)
    assert events == [{'ready': 22050}, {'pcm': base64.b64encode(PCM).decode()}, {'done': True},
                      {'pcm': base64.b64encode(PCM).decode()}, {'done': True}]
    assert library.requests == [(r['text'].encode(), r['language'].encode(), r['voice'].encode(), -1)
                                for r in (REQUEST, second)]
    assert library.paths == tuple(path.encode() for path in CONFIGURATION['paths'])
    assert library.longform == 1
    library.nemo_speech_tts_create.assert_called_once()
    library.nemo_speech_tts_destroy.assert_called_once()
    assert library.nemo_speech_tts_destroy.call_args.args[0].value == 42
    if platform == 'win32':
        native_os.add_dll_directory.assert_called_once_with(os.path.dirname(CONFIGURATION['library']))
        native_os.add_dll_directory.return_value.close.assert_called_once()
    else:
        native_os.add_dll_directory.assert_not_called()


@pytest.mark.parametrize('platform', ['linux', 'win32'])
def test_worker_rejects_version_before_loading_models(harness, platform):
    library = FakeLibrary(version=b'nemo-speech-tts 9.9.9')
    events, _, native_os = harness(protocol(), library=library, platform=platform)
    assert len(events) == 1 and 'version 0.1.0' in events[0]['error']
    library.nemo_speech_tts_create.assert_not_called()
    library.nemo_speech_tts_destroy.assert_not_called()
    if platform == 'win32':
        native_os.add_dll_directory.return_value.close.assert_called_once()


def test_worker_cleans_partial_initialization(harness):
    library = FakeLibrary(create_code=1)
    events, _, _ = harness(protocol(), library=library)
    assert len(events) == 1 and 'initialization failed' in events[0]['error']
    library.nemo_speech_tts_destroy.assert_called_once()
    library.nemo_speech_tts_synthesize_text.assert_not_called()


@pytest.mark.parametrize('acknowledgement', ['stop', ''])
def test_worker_cancels_without_acknowledgement(harness, acknowledgement):
    events, library, _ = harness(protocol(REQUEST, acknowledgement=acknowledgement))
    assert 'pcm' in events[1]
    assert 'cancelled' in events[2]['error']
    assert not any('done' in event for event in events)
    library.nemo_speech_tts_destroy.assert_called_once()


@pytest.mark.parametrize('code,detail,expected', [
    (1, b'tokenizer: private note text', 'text preparation failed'),
    (1, b'unknown voice_name: private note text', 'voice is not supported'),
    (2, b'private note text', 'out of memory'),
    (3, b'private note text', 'status 3'),
    (4, b'private note text', 'cancelled'),
])
def test_worker_sanitizes_native_failures_and_cleans_up(harness, code, detail, expected):
    events, library, _ = harness(protocol(REQUEST), library=FakeLibrary(code=code, detail=detail))
    assert expected in events[-1]['error']
    assert 'private' not in json.dumps(events)
    assert not any('done' in event for event in events)
    library.nemo_speech_tts_destroy.assert_called_once()


@pytest.mark.parametrize('line', ['', '{invalid\n', '{}\n'])
def test_worker_rejects_invalid_configuration(harness, line):
    events, library, _ = harness(line)
    assert len(events) == 1 and 'error' in events[0]
    library.nemo_speech_tts_create.assert_not_called()
    library.nemo_speech_tts_destroy.assert_not_called()


@pytest.mark.parametrize('line', ['{invalid\n', '{}\n'])
def test_worker_rejects_invalid_request_and_releases_model(harness, line):
    events, library, _ = harness(protocol() + line)
    assert events[0] == {'ready': 22050}
    assert 'error' in events[1]
    library.nemo_speech_tts_synthesize_text.assert_not_called()
    library.nemo_speech_tts_destroy.assert_called_once()


def test_worker_cancels_callback_when_pcm_pipe_breaks(harness):
    class BrokenPCMOutput(io.StringIO):
        def write(self, value):
            if '"pcm"' in value:
                raise BrokenPipeError('reader closed')
            return super().write(value)

    events, library, _ = harness(protocol(REQUEST, acknowledgement=''), output=BrokenPCMOutput())
    assert len(events) == 2 and 'cancelled' in events[1]['error']
    library.nemo_speech_tts_destroy.assert_called_once()


def test_worker_releases_model_when_protocol_output_closes(harness):
    class BrokenOutput(io.StringIO):
        def write(self, value):
            raise BrokenPipeError('reader closed')

    library = FakeLibrary()
    with pytest.raises(BrokenPipeError):
        harness(protocol(), library=library, output=BrokenOutput())
    library.nemo_speech_tts_destroy.assert_called_once()


def test_worker_suppresses_actual_native_stdout_and_stderr(tmp_path):
    # Windows registers the DLL directory even when library loading is mocked.
    configuration = dict(CONFIGURATION, library=str(tmp_path / 'speech'))
    bootstrap = (
        'import runpy, sys; namespace = runpy.run_path(sys.argv[1]); '
        'worker = namespace["worker"]; '
        'worker.c.CDLL = lambda _: namespace["FakeLibrary"](diagnostics=True); worker.main()'
    )
    result = subprocess.run(
        [sys.executable, '-c', bootstrap, str(Path(__file__).resolve())],
        input=protocol(REQUEST, configuration=configuration), capture_output=True, text=True, timeout=20, check=True,
    )
    events = [json.loads(line) for line in result.stdout.splitlines()]
    assert events == [{'ready': 22050}, {'pcm': base64.b64encode(PCM).decode()}, {'done': True}]
    assert result.stderr == ''
