"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Text-to-Speech settings and local runtime and model discovery.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

import os
from importlib.util import find_spec
from ctypes.util import find_library
from functools import lru_cache
from pathlib import Path
import shutil
import sys

from PySide6.QtCore import QStandardPaths

from ...settings import Settings
from .languages import SpeechLanguage


DEFAULTS = {
    'tts_enabled': (bool, True),
    'tts_runtime_path': (str, ''),
    'tts_model_directory': (str, ''),
    'tts_magpie_path': (str, ''),
    'tts_codec_path': (str, ''),
    'tts_tokenizer_directory': (str, ''),
    'tts_language': (str, 'en'),
    'tts_voice': (str, 'Aria'),
    'tts_speed': (float, 1.0),
    'tts_context_length': (int, 160),
    'tts_skip_inline_code': (bool, True),
    'tts_skip_multiline_code': (bool, True),
    'tts_announce_headings': (bool, True),
}

CONTEXT_LENGTHS = (10, 20, 40, 80, 160, 320, 640, 1280, 2560, 0)


@lru_cache(maxsize=1)
def portaudio_library():
    # Discover the library once without initializing audio devices on the GUI thread.
    return find_library('portaudio')


def audio_requirements():
    missing = []
    if find_spec('sounddevice') is None:
        missing.append('pip install "notolog[tts]"')
    if sys.platform.startswith('linux') and not portaudio_library():
        missing.append('libportaudio2 (Debian/Ubuntu: sudo apt install libportaudio2)')
    return '; '.join(missing)


def audio_available():
    return not audio_requirements()


def speech_settings():
    settings = Settings()
    for name, (kind, default) in DEFAULTS.items():
        if not hasattr(type(settings), name):
            settings.create_property(name, kind, audio_available() if name == 'tts_enabled' else default)
    if 0 < settings.tts_context_length < 10:
        settings.tts_context_length = 10
    language = SpeechLanguage.from_code(settings.tts_language).name.lower()
    if settings.tts_language != language:
        settings.tts_language = language
    return settings


def runtime_path(settings):
    configured = settings.tts_runtime_path.strip()
    if configured:
        return configured if Path(configured).is_file() and os.access(configured, os.X_OK) else ''
    return shutil.which('nemo-speech') or ''


def default_model_directory():
    return Path(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppLocalDataLocation)) / 'speech-models'


def model_directory(settings):
    return Path(settings.tts_model_directory) if settings.tts_model_directory else default_model_directory()


def model_paths(settings, *, overrides=True):
    """Use explicit local files, or discover the runtime's downloaded model set."""
    root = model_directory(settings)
    magpie = settings.tts_magpie_path if overrides else ''
    codec = settings.tts_codec_path if overrides else ''
    tokenizer = settings.tts_tokenizer_directory if overrides else ''
    if root.is_dir():
        files = list(root.rglob('*.gguf'))
        if not magpie:
            candidates = [p for p in files if 'magpie' in p.name.lower()]
            if len(candidates) == 1:
                magpie = str(candidates[0])
        if not codec:
            candidates = [p for p in files if 'codec' in p.name.lower()]
            if len(candidates) == 1:
                codec = str(candidates[0])
        if not tokenizer:
            candidates = list(root.rglob('model_config.yaml'))
            if len(candidates) == 1:
                tokenizer = str(candidates[0].parent)
    if not (magpie and Path(magpie).is_file() and codec and Path(codec).is_file()
            and tokenizer and Path(tokenizer).is_dir()):
        raise ValueError('Download the model set or select Magpie, NanoCodec, and the tokenizer folder '
                         'in Text-to-Speech settings.')
    return magpie, codec, tokenizer
