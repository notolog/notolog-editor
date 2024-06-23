"""
Notolog Editor
Open-source markdown editor developed in Python.

File Details:
- Purpose: Clipboard helper class.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtWidgets import QApplication


class ClipboardHelper:
    @staticmethod
    def set_text(text):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
