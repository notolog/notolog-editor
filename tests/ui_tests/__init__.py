"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Contains unit and integration tests for the related functionality.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2025 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtWidgets import QApplication

from notolog.app_config import AppConfig

import os
import sys
import pytest

os.environ.pop("QT_QPA_PLATFORM", None)
# Force Qt style override to avoid:
# QApplication: invalid style override 'kvantum' passed, ignoring it.
#    Available styles: Windows, Fusion
os.environ["QT_STYLE_OVERRIDE"] = "Fusion"


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

    # Cleanup
    app.quit()
    app.processEvents()
