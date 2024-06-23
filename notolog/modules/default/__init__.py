"""
Notolog Editor
Open-source markdown editor developed in Python.

File Details:
- Purpose: Part of the default module.

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
    Readable module name, for example, 'Default Module'.
    """
    return ModuleCore.module_name


def is_available() -> bool:
    """
    Check for any additional requirements for the module here.
    """
    return True
