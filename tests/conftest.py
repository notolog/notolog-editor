"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Pytest configuration and shared fixtures.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

import pytest
import sys
from PySide6.QtWidgets import QApplication


@pytest.fixture(scope="session")
def qapp():
    """
    Create a single QApplication instance for the entire test session.
    This prevents multiple QApplication instances and ensures proper cleanup.
    """
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    yield app

    # Cleanup: close all top-level widgets and quit the application
    for widget in app.topLevelWidgets():
        widget.close()

    # Note: We don't call app.quit() here as it may cause issues with pytest teardown
    # The application will be cleaned up when the Python process exits
