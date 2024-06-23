"""
Notolog Editor
Open-source markdown editor developed in Python.

File Details:
- Purpose: Part of the 'OpenAI API' module.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from .module_core import ModuleCore


def get_name():
    """
    Readable module name.
    """
    return ModuleCore.module_name


def is_available() -> bool:
    """
    No additional requirements.
    """
    return True
