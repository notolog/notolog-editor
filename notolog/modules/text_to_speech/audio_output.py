"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Bounded in-memory PCM playback through PortAudio.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from collections import deque


class AudioOutput:
    def __init__(self, rate):
        try:
            import sounddevice
        except (ImportError, OSError) as exc:
            raise RuntimeError('Install notolog[tts] and the PortAudio library to enable speech playback.') from exc
        self.rate = rate
        self.buffer = bytearray(rate * 4)
        self.view = memoryview(self.buffer)
        self.produced = 0
        self.consumed = 0
        self.paused = False
        self.finished_at = 0.0
        self.audible_intervals = deque()
        self.failure = False
        self.closed = False
        self.silence = bytes(1024)
        self.stream = sounddevice.RawOutputStream(
            samplerate=rate, channels=1, dtype='int16', blocksize=512,
            latency='high', callback=self._callback,
        )
        try:
            self.stream.start()
        except Exception:
            self.stream.close()
            self.closed = True
            raise

    def _callback(self, output, frames, timing, status):
        output[:] = self.silence
        while self.audible_intervals and self.audible_intervals[0][1] <= timing.currentTime:
            self.audible_intervals.popleft()
        if self.paused or self.closed:
            return
        try:
            count = min(len(output), self.produced - self.consumed)
            if not count:
                return
            start = self.consumed % len(self.buffer)
            first = min(count, len(self.buffer) - start)
            output[:first] = self.view[start:start + first]
            if first < count:
                output[first:count] = self.view[:count - first]
            self.finished_at = timing.outputBufferDacTime + count / (self.rate * 2)
            if any(output[:count]):
                self.audible_intervals.append((timing.outputBufferDacTime, self.finished_at))
            self.consumed += count
        except Exception:
            output[:] = self.silence
            self.failure = True

    def check(self):
        if self.closed or self.failure or not self.stream.active:
            raise RuntimeError('Speech audio output stopped unexpectedly.')

    @property
    def write_available(self):
        self.check()
        return len(self.buffer) - (self.produced - self.consumed)

    def write(self, data):
        count = min(len(data), self.write_available) & ~1
        start = self.produced % len(self.buffer)
        first = min(count, len(self.buffer) - start)
        self.view[start:start + first] = data[:first]
        if first < count:
            self.view[:count - first] = data[first:count]
        # The producer publishes only complete samples; the callback alone advances consumed.
        self.produced += count
        return count

    @property
    def playing(self):
        if self.closed or self.paused or self.failure or not self.stream.active:
            return False
        now = self.stream.time
        return any(start <= now < end for start, end in tuple(self.audible_intervals))

    @property
    def drained(self):
        self.check()
        return self.produced == self.consumed and self.stream.time >= self.finished_at

    def close(self):
        if self.closed:
            return
        self.closed = True
        try:
            self.stream.abort()
        finally:
            try:
                self.stream.close()
            finally:
                self.buffer[:] = bytes(len(self.buffer))
