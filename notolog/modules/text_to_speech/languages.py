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
    VI = 'Vietnamese'
    HI = 'Hindi'
    ZH = 'Chinese (Mandarin; requires runtime support)'
    JA = 'Japanese (requires runtime support)'

    @classmethod
    def from_code(cls, code):
        return cls.__members__.get(code.replace('_', '-').split('-')[0].upper(), cls.EN)
