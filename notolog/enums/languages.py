"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Enum class for the app's supported languages.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import QLocale

from .enum_base import EnumBase

assert hasattr(EnumBase, 'default'), "Check default() method is implemented in the base class"


class Languages(EnumBase):

    DE = "German"
    EN = ("English", True)  # Fallback default option
    ES = "Spanish"
    FI = "Finnish"
    FR = "French"
    GE = "Georgian"
    GR = "Greek"
    ID = "Indonesian"
    IN = "Hindi"
    IT = "Italian"
    JA = "Japanese"
    KO = "Korean"
    LA = "Latin"
    NL = "Dutch"
    PT = "Portuguese"
    RU = "Russian"
    SE = "Swedish"
    TR = "Turkish"
    ZH = "Chinese"

    @classmethod
    def default(cls):
        """
        Returns the default value of the Enum.
        Usage:
            self.default()
        @return: Any
        """

        locale = QLocale.system()  # Get the system's locale
        iso_language_code = locale.name().split('_')[0]  # Extract the language part and ignore the country part

        # Find and return the default enum member based on the system locale
        for member in cls:
            # System locale as a default locale
            if iso_language_code and member.name.lower() == iso_language_code:
                return member

        # Fallback to the parent's logic
        return super().default()
