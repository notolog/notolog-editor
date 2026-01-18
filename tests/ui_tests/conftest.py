"""
Shared pytest configuration for UI tests.

This module provides common fixtures for UI tests. Note that some tests
require the real NotologEditor initialization (test_toolbar.py, test_settings_dialog.py)
while others benefit from mocked initialization (test_qt_ui.py).

Tests that need mocking should use the mock_notolog_editor fixture explicitly.
"""

import os

# IMPORTANT: Set environment variables BEFORE importing PySide6
# Use offscreen platform for Qt to prevent segfaults when no display is available
os.environ["QT_QPA_PLATFORM"] = "offscreen"
# Force Qt style override to avoid:
# QApplication: invalid style override 'kvantum' passed, ignoring it.
#    Available styles: Windows, Fusion
os.environ["QT_STYLE_OVERRIDE"] = "Fusion"

# Now import PySide6 after environment is set
from unittest.mock import MagicMock  # noqa: E402
from PySide6.QtWidgets import QMainWindow  # noqa: E402
import pytest  # noqa: E402


@pytest.fixture
def mock_notolog_editor(mocker):
    """
    Mock NotologEditor.__init__ to prevent segfaults in headless environments.

    Use this fixture explicitly in tests that don't need full NotologEditor initialization.
    Tests that need real UI widgets (test_toolbar, test_settings_dialog) should NOT use this.

    Usage:
        def main_window(self, mock_notolog_editor, test_app, settings_obj):
            editor = NotologEditor(screen=test_app.screens()[0])
            ...
    """
    from notolog.notolog_editor import NotologEditor
    import logging

    def mock_init(self, *args, **kwargs):
        # Call the parent QMainWindow.__init__ to properly initialize Qt
        QMainWindow.__init__(self)

        # Initialize logger to prevent AttributeError
        self.logger = logging.getLogger('notolog')

        # Create mock toolbar with required attributes
        self.toolbar = MagicMock()
        self.toolbar.toolbar_edit_button = MagicMock()
        self.toolbar.toolbar_edit_button.rect = MagicMock(
            return_value=MagicMock(center=MagicMock(return_value=MagicMock()))
        )

        # Create a mock search_form with stateful text behavior
        search_text = {'value': ''}
        self.toolbar.search_form = MagicMock()
        self.toolbar.search_form.text = MagicMock(side_effect=lambda: search_text['value'])
        self.toolbar.search_form.set_text = MagicMock(side_effect=lambda t: search_text.update({'value': t}))
        self.toolbar.search_form.btn_search_clear = MagicMock()
        self.toolbar.search_form.btn_search_clear.rect = MagicMock(
            return_value=MagicMock(center=MagicMock(return_value=MagicMock()))
        )

        # Create mock statusbar with stateful behavior
        status_mode = {'value': 'Modus Visum'}
        status_source = {'value': 'HTML'}
        status_encryption = {'value': 'Simplicitas 🔓'}

        self.statusbar = {}
        self.statusbar['mode_label'] = MagicMock()
        self.statusbar['mode_label'].text = MagicMock(side_effect=lambda: status_mode['value'])
        self.statusbar['source_label'] = MagicMock()
        self.statusbar['source_label'].text = MagicMock(side_effect=lambda: status_source['value'])
        self.statusbar['encryption_label'] = MagicMock()
        self.statusbar['encryption_label'].text = MagicMock(side_effect=lambda: status_encryption['value'])

        # Mock the edit button click to update statusbar
        def mock_click():
            status_mode['value'] = 'Modus Editio'
            status_source['value'] = 'Markdown'

        self.toolbar.toolbar_edit_button.click = MagicMock(side_effect=mock_click)

        # Mock the clear button click to update search text
        def mock_clear_click():
            search_text['value'] = ''

        self.toolbar.search_form.btn_search_clear.click = MagicMock(side_effect=mock_clear_click)

        # Set window title for test verification
        self.setWindowTitle("Editorium Notolog")

    mocker.patch.object(NotologEditor, '__init__', mock_init)


@pytest.fixture
def mock_main_window_for_widgets(mocker, test_app):
    """
    Create a minimal mock main window for tests that need a parent widget
    but don't need full NotologEditor functionality.

    Use this for tests like test_toolbar.py, test_search_form.py, test_settings_dialog.py
    that need to create real nested widgets (ToolBar, SearchForm, etc.) but don't need
    the full NotologEditor initialization which causes segfaults.
    """
    from notolog.notolog_editor import NotologEditor
    from notolog.settings import Settings
    from notolog.enums.languages import Languages
    import logging

    # Force language default
    mocker.patch.object(Languages, 'default', return_value='la')

    def mock_init(self, *args, **kwargs):
        # Call parent QMainWindow.__init__
        QMainWindow.__init__(self)

        # Initialize essential attributes that nested widgets may need
        self.logger = logging.getLogger('notolog')
        self.settings = Settings()

        # Mock attributes that NotologEditor would normally have
        self.toolbar = None  # Will be set by test
        self.statusbar = {}

        # Set window title
        self.setWindowTitle("Editorium Notolog")

    mocker.patch.object(NotologEditor, '__init__', mock_init)
    mocker.patch.object(NotologEditor, 'show', return_value=None)
    mocker.patch.object(NotologEditor, 'load_content_html', return_value=None)

    # Create the mocked editor
    editor = NotologEditor(screen=test_app.screens()[0])

    yield editor
