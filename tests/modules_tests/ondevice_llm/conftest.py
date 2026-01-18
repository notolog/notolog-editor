"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Contains unit and integration tests for the related functionality.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

import pytest

from .. import is_module_available


def pytest_collection_modifyitems(config, items):
    """
    Conditionally skip tests in a specific directory.
    """
    # Check if the condition is not met
    if not is_module_available('ondevice_llm'):
        skip_marker = pytest.mark.skip(reason="Condition is not met. Skipping tests in 'ondevice_llm'.")
        # Skip all tests in the 'ondevice_llm' directory
        for item in items:
            if 'ondevice_llm' in item.nodeid:
                item.add_marker(skip_marker)
