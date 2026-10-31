"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Text-to-Speech interface translations.
- Functionality: Uses the app's Lexemes loader and UI language for module text.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from functools import lru_cache, partial
from pathlib import Path

from ...lexemes.lexemes import Lexemes
from ...settings import Settings


LEXEMES_PATH = Path(__file__).with_name('lexemes')


@lru_cache(maxsize=38)
def catalog(language, default_scope='common'):
    if language not in {path.name for path in LEXEMES_PATH.iterdir() if path.is_dir()}:
        language = 'en'
    return Lexemes(language=language, default_scope=default_scope, lexemes_dir=str(LEXEMES_PATH))


def tr(key, *, scope='common', **values):
    """Look up a stable module key in the current UI language."""
    text = catalog(Settings().app_language).get(key, scope=scope)
    if not text:
        text = catalog('en').get(key, scope=scope)
    return text.format(**values) if values else text


class SpeechSetupError(ValueError):
    """Keep setup errors translatable after an interface language change."""

    def __init__(self, key, *, scope='common', **values):
        self.key = key
        self.scope = scope
        self.values = values
        # Widgets can retain this callable without retaining an exception traceback.
        self.message = partial(tr, key, scope=scope, **values)
        super().__init__(key)

    def __str__(self):
        return self.message()


def language_label(language, *, include_requirement=True):
    if language.name in ('KO', 'PT_BR'):
        # Autonyms keep the new model languages identifiable in every UI locale.
        return language.value
    label = tr(f'module_text_to_speech_language_{language.name.lower()}')
    if include_requirement and language.name in ('ZH', 'JA'):
        label += ' (' + tr('module_text_to_speech_language_runtime_required') + ')'
    return label
