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

import os
import sys
import pytest

# IMPORTANT: Set environment variables BEFORE importing PySide6
# Use offscreen platform for Qt to prevent segfaults when no display is available
os.environ["QT_QPA_PLATFORM"] = "offscreen"
# Force Qt style override to avoid:
# QApplication: invalid style override 'kvantum' passed, ignoring it.
#    Available styles: Windows, Fusion
os.environ["QT_STYLE_OVERRIDE"] = "Fusion"

# Now import PySide6 after environment is set
from PySide6.QtWidgets import QApplication  # noqa: E402
from notolog.app_config import AppConfig  # noqa: E402


@pytest.fixture
def test_app(mocker):
    # Main widgets application; new
    # More info: https://doc.qt.io/qt-6/qcoreapplication.html#details
    app = QApplication.instance()
    if not app:
        # Consider: Fixture to initialize QCoreApplication for Non-GUI Tests
        """
        Virtual Framebuffer on Linux (Xvfb):
        For Linux, use Xvfb to run tests requiring GUI in a virtual framebuffer.
        For Windows, ensure GUI sessions are available for tests.
        """
        app = QApplication(sys.argv)

        # To correctly set up app settings
        app.setOrganizationName(AppConfig().get_settings_org_name())
        app.setApplicationName(AppConfig().get_settings_app_name_qa())

        AppConfig().set_test_mode(True)

    yield app

    # Cleanup - don't call quit() here as it causes segfaults
    # The session-level cleanup in conftest.py will handle it
    app.processEvents()
