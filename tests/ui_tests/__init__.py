from PySide6.QtWidgets import QApplication

import os
import sys
import pytest

os.environ.pop("QT_QPA_PLATFORM", None)
# Force Qt style override to avoid:
# QApplication: invalid style override 'kvantum' passed, ignoring it.
#    Available styles: Windows, Fusion
os.environ["QT_STYLE_OVERRIDE"] = "Fusion"


@pytest.fixture
def test_app():
    # Main application; existed
    app = QApplication.instance()
    if app:
        # Destroying the QCoreApplication singleton to avoid RuntimeError.
        app.quit()
        app.deleteLater()
        app.processEvents()
        del app

    # Main application; new
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
        app.setOrganizationName('Notolog')
        app.setApplicationName('notolog_editor_tests')

    yield app

    # Cleanup
    app.quit()
    app.deleteLater()
    app.processEvents()
