"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Speech session coordination and audio playback.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

import asyncio

from PySide6.QtCore import QObject, Signal

from .config import speech_settings
from .native_runtime import NativeRuntime
from .audio_output import AudioOutput
from .text import prepare_sections, SpeechSection, speech_chunks, normalize_numbers


class SpeechController(QObject):
    status_changed = Signal(str)
    error = Signal(str)
    details_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = speech_settings()
        self.runtime = NativeRuntime(self.settings)
        self.sink = None
        self.task = None
        self.paused = False
        self.preparing = False
        self.status_key = 'module_text_to_speech_status_ready'
        self.status_changed.connect(lambda key: setattr(self, 'status_key', key))
        self.settings.value_changed.connect(self._settings_changed)

    def _settings_changed(self, values):
        model_settings = {'tts_enabled', 'tts_runtime_path', 'tts_model_directory',
                          'tts_magpie_path', 'tts_codec_path', 'tts_tokenizer_directory'}
        if model_settings.intersection(values) or (self.task and any(key.startswith('tts_') for key in values)):
            self.stop()

    def read(self, source, *, html=False):
        previous = self.task
        if previous or not self.settings.tts_enabled:
            self.stop()
        if not self.settings.tts_enabled:
            return
        sections = prepare_sections(source, html=html, skip_inline=self.settings.tts_skip_inline_code,
                                    skip_multiline=self.settings.tts_skip_multiline_code,
                                    announce_headings=self.settings.tts_announce_headings)
        for section in sections:
            section.text = normalize_numbers(section.text, self.settings.tts_language)
        text = sections[0].text if len(sections) == 1 and not sections[0].heading else sections
        if not text:
            self.status_changed.emit('module_text_to_speech_status_empty')
            return
        self.task = asyncio.get_running_loop().create_task(self._read(text, previous))

    async def _read(self, text, previous=None):
        try:
            if previous:
                await asyncio.gather(previous, return_exceptions=True)
            self.status_changed.emit('module_text_to_speech_status_preparing' if getattr(self.runtime, 'loaded', False)
                                     else 'module_text_to_speech_status_loading')
            self.preparing = True
            try:
                await self.runtime.start()
            finally:
                self.preparing = False
            await self._play_stream(text)
            self.status_changed.emit('module_text_to_speech_status_finished')
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            self.runtime.close()
            self.status_changed.emit('module_text_to_speech_status_unavailable')
            self.error.emit(str(exc))
        finally:
            if self.task is asyncio.current_task():
                self.task = None
                self.paused = False

    async def _play_stream(self, text):
        rate = round(self.runtime.rate * self.settings.tts_speed)
        self.sink = AudioOutput(rate)

        # Native callbacks are codec frames, not word boundaries. Buffer a bounded
        # passage before playback so slower CPUs cannot interrupt individual words.

        async def prepare(item):
            passage, pause = item
            # PCM silence keeps the heading break at one second at any playback speed.
            audio = bytearray(rate * 2 if pause else 0)
            self.preparing = True
            try:
                async for pcm in self.runtime.stream(passage):
                    audio.extend(pcm)
                    if len(audio) > 64 * 1024 * 1024:
                        raise RuntimeError('Speech audio exceeded the memory limit. Reduce the context length.')
                return audio
            finally:
                self.preparing = False

        def chunks():
            spoken = False
            for section in [SpeechSection(text)] if isinstance(text, str) else text:
                passage = section.text
                if section.heading and passage[-1:] not in '.!?':
                    passage += '.'
                pause = spoken and section.heading
                for chunk in speech_chunks(passage, limit=max(0, self.settings.tts_context_length)):
                    yield chunk, pause
                    pause = False
                    spoken = True

        # One completed passage may wait while another is synthesized and the current one plays.
        ready = asyncio.Queue(maxsize=1)

        async def produce():
            try:
                for item in chunks():
                    await ready.put(await prepare(item))
                await ready.put(None)
            except Exception as exc:
                await ready.put(exc)

        producer = asyncio.create_task(produce())
        try:
            while True:
                self.status_changed.emit('module_text_to_speech_status_preparing')
                pcm = await ready.get()
                if pcm is None:
                    break
                if isinstance(pcm, Exception):
                    raise pcm
                while self.paused:
                    await asyncio.sleep(.02)
                if pcm:
                    self.status_changed.emit('module_text_to_speech_status_reading')
                    offset = 0
                    while offset < len(pcm):
                        self.sink.check()
                        if self.paused:
                            await asyncio.sleep(.02)
                            continue
                        count = min(len(pcm) - offset, self.sink.write_available)
                        if count:
                            written = self.sink.write(memoryview(pcm)[offset:offset + count])
                            if written < 0:
                                raise RuntimeError('Cannot write speech audio to the output device.')
                            if written == 0:
                                await asyncio.sleep(.01)
                                continue
                            offset += written
                        else:
                            await asyncio.sleep(.01)
            # Queue adjacent passages continuously; drain the device only at the end.
            while not self.sink.drained:
                await asyncio.sleep(.02)
        finally:
            producer.cancel()
            await asyncio.gather(producer, return_exceptions=True)
            self.sink.close()
            self.sink = None

    def pause_resume(self):
        if not self.task:
            return
        self.paused = not self.paused
        if self.sink:
            self.sink.paused = self.paused
        self.status_changed.emit(
            'module_text_to_speech_status_paused' if self.paused else 'module_text_to_speech_status_reading')

    def stop(self):
        self.preparing = False
        if self.task:
            self.task.cancel()
        if self.sink:
            self.sink.close()
        self.paused = False
        # Terminating the local worker also cancels synthesis immediately.
        self.runtime.close()
        self.status_changed.emit('module_text_to_speech_status_stopped')
