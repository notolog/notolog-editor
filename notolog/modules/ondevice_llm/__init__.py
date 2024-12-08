"""
Notolog Editor
Open-source markdown editor developed in Python.

File Details:
- Purpose: Part of the 'On-Device LLM' module.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024 Vadim Bakhrenkov
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
    # The required packages are not supported
    if sys.platform == "darwin" and sys.version_info < (3, 10):
        AppConfig().logger.info(f"The system is not supported by the module '{get_name()}'")
        return False

    # Required packages for a local LLM inference
    for package_name in ["onnxruntime_genai", "numpy"]:
        module_spec = importlib.util.find_spec(package_name)
        if module_spec is None:
            AppConfig().logger.info(f"The package '{package_name}' is required for the module '{get_name()}'")
            return False

    return True
