"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Part of the 'Module llama.cpp' module.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2025 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

# This import is essential for proper module loading.
from .module_core import ModuleCore

from .. import AppConfig

import sys
import importlib.util


def get_name():
    """
    Readable module name.
    """
    return ModuleCore.module_name


def is_available() -> bool:
    # Required packages for a local LLM inference
    for package_name in ["llama_cpp"]:
        module_spec = importlib.util.find_spec(package_name)
        if module_spec is None:
            AppConfig().logger.info(f"The package '{package_name}' is required for the module '{get_name()}'")
            return False

    return True
