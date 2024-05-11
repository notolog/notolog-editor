from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication  # Sync with main.py
from PySide6.QtTest import QTest

from notolog.notolog_editor import NotologEditor

import os
import sys
import pytest


@pytest.fixture(scope="session")
def qt_application():
    # Force Qt style override
    """
    QApplication: invalid style override 'kvantum' passed, ignoring it.
        Available styles: Windows, Fusion
    """
    os.environ["QT_STYLE_OVERRIDE"] = "Fusion"
    # Fixture to initialize QApplication.
    return QApplication(sys.argv)


@pytest.fixture
def main_window(qt_application):
    # Fixture to create and return main window instance
    window = NotologEditor(screen=qt_application.screens()[0])
    yield window


def test_editor_state(main_window):
    # Check default window title
    assert main_window.windowTitle() == "Notolog Editor"

    assert main_window.statusbar['mode_label'].text() == 'View mode'
    assert main_window.statusbar['source_label'].text() == 'HTML'
    assert main_window.statusbar['encryption_label'].text() == 'Plain 🔓'

    # Test that clicking the edit button updates the editor state
    QTest.mouseClick(main_window.toolbar.toolbar_edit_button, Qt.MouseButton.LeftButton)

    assert main_window.statusbar['mode_label'].text() == 'Edit mode'
    assert main_window.statusbar['source_label'].text() == 'Markdown'
    assert main_window.statusbar['encryption_label'].text() == 'Plain 🔓'


def test_search_elements(main_window):
    assert hasattr(main_window.toolbar, 'search_input')
    main_window.toolbar.search_input.setText('Test search')
    assert main_window.toolbar.search_input.text() == 'Test search'

    assert hasattr(main_window.toolbar, 'btn_search_clear')
    # Test that clicking the button updates the search field
    QTest.mouseClick(main_window.toolbar.btn_search_clear, Qt.MouseButton.LeftButton)
    assert main_window.toolbar.search_input.text() == ''

