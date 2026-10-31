"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Supported speech languages.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from enum import Enum


class SpeechLanguage(Enum):
    EN = 'English'
    ES = 'Spanish'
    DE = 'German'
    FR = 'French'
    IT = 'Italian'
    HI = 'Hindi'
    ZH = 'Chinese (Mandarin; requires runtime support)'
    JA = 'Japanese (requires runtime support)'
    KO = '한국어'
    PT_BR = 'Português (Brasil)'

    @property
    def code(self):
        return self.name.lower().replace('_', '-')

    @property
    def sample(self):
        """Speech examples follow the document language, independently of the UI."""
        return {
            'en': 'Welcome to Notolog. This is a test of your reading voice.',
            'es': 'Hola. Esta es una prueba de la voz de lectura.',
            'de': 'Hallo. Dies ist ein Test der Vorlesestimme.',
            'fr': 'Bonjour. Ceci est un test de la voix de lecture.',
            'it': 'Ciao. Questa è una prova della voce di lettura.',
            'hi': 'नमस्ते। यह पढ़ने की आवाज़ का परीक्षण है।',
            'zh': '你好。这是朗读声音测试。',
            'ja': 'こんにちは。読み上げ音声のテストです。',
            'ko': '안녕하세요. 읽기 음성 테스트입니다.',
            'pt-br': 'Olá. Este é um teste da voz de leitura.',
        }[self.code]

    @classmethod
    def from_code(cls, code):
        code = code.strip().replace('-', '_').upper()
        if code in cls.__members__:
            return cls[code]
        # Locale aliases can use an offered base language (e.g. en-US -> en).
        # Portuguese requires the explicit pt-BR choice; there is no PT member.
        base = code.split('_')[0]
        return cls.__members__.get(base)
