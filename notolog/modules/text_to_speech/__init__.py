"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Text-to-Speech module initialization.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from .module_core import ModuleCore

__all__ = ['ModuleCore', 'get_name', 'is_available']


def get_name():
    return 'Text-to-Speech'


def is_available():
    # Keep setup accessible even before a runtime or model has been installed.
    # Reading actions are independently gated by the enabled setting.
    return True
