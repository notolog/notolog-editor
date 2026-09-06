"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Communication with the native speech worker over local pipes.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""
import asyncio
import base64
import json
import os
from pathlib import Path
import sys

from PySide6.QtCore import QProcess

from .config import runtime_path, model_paths
from .runtime import validate_runtime, process_environment, isolate_process, stop_process


class NativeRuntime:
    def __init__(self, settings):
        self.settings = settings
        self.process = None
        self.configuration = None
        self.rate = None

    @property
    def loaded(self):
        return bool(self.configuration and self.process
                    and self.process.state() == QProcess.ProcessState.Running)

    async def event(self):
        try:
            event = await asyncio.wait_for(self.events.get(), 180)
        except asyncio.TimeoutError as exc:
            raise RuntimeError('Native speech worker timed out while preparing audio.') from exc
        if 'error' in event:
            raise RuntimeError(event['error'])
        return event

    def send(self, message):
        self.process.write((json.dumps(message) + '\n').encode())

    async def start(self):
        paths = model_paths(self.settings)
        configuration = runtime_path(self.settings), paths
        if self.process and self.process.state() == QProcess.ProcessState.Running:
            if self.configuration == configuration:
                return
        self.close()
        await validate_runtime(self.settings)
        root = Path(configuration[0]).resolve().parent.parent
        candidates = [root / 'lib' / 'libnemo_speech_tts.so.1', root / 'lib' / 'libnemo_speech_tts.dylib',
                      root / 'lib' / 'libnemo_speech_tts.1.dylib', root / 'bin' / 'nemo_speech_tts.dll']
        library = next((path for path in candidates if path.is_file()), None)
        if library is None:
            raise ValueError('Native streaming needs the complete runtime archive, including its lib directory.')
        events = self.events = asyncio.Queue()
        pending = bytearray()
        process = self.process = QProcess()
        isolate_process(process)
        env = process_environment(self.settings)
        key = ('PATH' if sys.platform == 'win32' else
               'DYLD_LIBRARY_PATH' if sys.platform == 'darwin' else 'LD_LIBRARY_PATH')
        search_paths = [str(library.parent), *env.value(key).split(os.pathsep)]
        env.insert(key, os.pathsep.join(path for path in search_paths if path))
        process.setProcessEnvironment(env)

        def receive():
            nonlocal pending
            pending.extend(bytes(process.readAllStandardOutput()))
            while b'\n' in pending:
                line, _, tail = pending.partition(b'\n')
                pending = bytearray(tail)
                try:
                    events.put_nowait(json.loads(line))
                except (ValueError, UnicodeError):
                    events.put_nowait({'error': 'Invalid native speech worker response.'})

        process.readyReadStandardOutput.connect(receive)

        # Native diagnostics may contain note text; never forward them to logs.
        process.setStandardErrorFile(QProcess.nullDevice())
        process.errorOccurred.connect(lambda _: events.put_nowait({'error': process.errorString()}))
        process.finished.connect(lambda *_: events.put_nowait({'error': 'Native speech worker exited.'}))
        arguments = (['--tts-worker'] if getattr(sys, 'frozen', False) else
                     ['-u', str(Path(__file__).with_name('native_worker.py'))])
        process.start(sys.executable, arguments)
        self.send({'library': str(library), 'paths': paths})
        try:
            event = await self.event()
            self.rate = event['ready']
            self.configuration = configuration
        except BaseException:
            self.close()
            raise

    async def stream(self, text):
        self.send({'text': text, 'voice': self.settings.tts_voice, 'language': self.settings.tts_language})
        while True:
            event = await self.event()
            if event.get('done'):
                return
            yield base64.b64decode(event['pcm'], validate=True)
            self.process.write(b'continue\n')

    def close(self):
        if self.process:
            stop_process(self.process)
            self.process.deleteLater()
            self.process = None
        self.configuration = None
        if hasattr(self, 'events'):
            while not self.events.empty():
                self.events.get_nowait()
