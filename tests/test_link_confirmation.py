"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Tests open link confirmation dialog functionality with deferred URL opening.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

import sys
import pytest
from unittest.mock import Mock, patch
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QApplication


@pytest.fixture(scope="module")
def qapp():
    """Create QApplication instance for tests"""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app


@pytest.fixture
def mock_notolog_editor(qapp):
    """Create a mock NotologEditor instance with necessary attributes"""
    from notolog.notolog_editor import NotologEditor

    # Create a minimal mock
    editor = Mock(spec=NotologEditor)

    # Mock settings
    editor.settings = Mock()
    editor.settings.viewer_open_link_confirmation = True

    # Mock lexemes
    editor.lexemes = Mock()

    def mock_lexemes_get(key=None, name=None, **kwargs):
        """Mock lexemes.get that handles both 'key' and 'name' arguments"""
        lookup_key = name if name else key
        return {
            'dialog_open_link_title': 'Open Link',
            'dialog_open_link_text': f"Open {kwargs.get('url', 'URL')}?"
        }.get(lookup_key, lookup_key)

    editor.lexemes.get = Mock(side_effect=mock_lexemes_get)

    # Mock logger
    editor.logger = Mock()

    # Create real method bindings
    editor.open_link_dialog_proxy = NotologEditor.open_link_dialog_proxy.__get__(editor, NotologEditor)
    editor._open_url_deferred = NotologEditor._open_url_deferred.__get__(editor, NotologEditor)
    editor.check_local_link = Mock(return_value=False)  # Return False = external URL
    editor.common_dialog = Mock()

    return editor


def test_link_confirmation_callback_structure(mock_notolog_editor):
    """Test that the link confirmation creates proper callback structure"""
    test_url = QUrl("https://example.com")

    # Get the handler
    handler = mock_notolog_editor.open_link_dialog_proxy()

    # Call the handler with a URL
    handler(test_url)

    # Verify common_dialog was called
    assert mock_notolog_editor.common_dialog.called
    call_args = mock_notolog_editor.common_dialog.call_args

    # Extract the callback argument
    assert 'callback' in call_args.kwargs
    callback = call_args.kwargs['callback']

    # Verify callback is callable
    assert callable(callback)

    print("✓ Callback structure created correctly")


@patch('PySide6.QtGui.QDesktopServices.openUrl')
@patch('PySide6.QtCore.QTimer.singleShot')
def test_link_opens_with_deferred_pattern(mock_timer, mock_openUrl, mock_notolog_editor):
    """Test that link opening is properly deferred with QTimer"""
    test_url = QUrl("https://example.com")
    mock_openUrl.return_value = True

    # Track whether dialog_callback was called
    dialog_closed = []

    def mock_common_dialog(title, text, callback=None, reject_callback=None):
        """Simulate the dialog accepting"""
        def mock_dialog_callback():
            dialog_closed.append(True)

        # Simulate user clicking "Yes"
        if callback:
            callback(mock_dialog_callback)

    mock_notolog_editor.common_dialog = mock_common_dialog

    # Get the handler and call it
    handler = mock_notolog_editor.open_link_dialog_proxy()
    handler(test_url)

    # Verify dialog was closed
    assert len(dialog_closed) == 1
    print("✓ Dialog closed: True")

    # Verify QTimer.singleShot was called with 100ms delay
    assert mock_timer.called
    assert mock_timer.call_args[0][0] == 100  # First arg should be 100ms
    print("✓ QTimer.singleShot called with 100ms delay")

    # Execute the deferred callback manually (simulating timer firing)
    deferred_callback = mock_timer.call_args[0][1]  # Second arg is the lambda
    deferred_callback()

    # Now verify QDesktopServices.openUrl was called
    assert mock_openUrl.called
    mock_openUrl.assert_called_once()
    print("✓ QDesktopServices.openUrl called after deferral")


@patch('PySide6.QtGui.QDesktopServices.openUrl')
def test_link_opens_without_confirmation(mock_openUrl, mock_notolog_editor):
    """Test that link opens directly when confirmation is disabled"""
    test_url = QUrl("https://example.com")
    mock_openUrl.return_value = True

    # Disable confirmation
    mock_notolog_editor.settings.viewer_open_link_confirmation = False

    # Get the handler and call it
    handler = mock_notolog_editor.open_link_dialog_proxy()
    handler(test_url)

    # Verify QDesktopServices.openUrl was called directly
    assert mock_openUrl.called
    mock_openUrl.assert_called_once_with(test_url)

    # Verify common_dialog was NOT called
    assert not mock_notolog_editor.common_dialog.called

    print("✓ Link opens without confirmation")


def test_local_links_skip_confirmation(mock_notolog_editor):
    """Test that local file links skip confirmation dialog"""
    test_url = QUrl("file:///path/to/file.md")

    # Make check_local_link return True for local files
    mock_notolog_editor.check_local_link = Mock(return_value=True)

    # Get the handler and call it
    handler = mock_notolog_editor.open_link_dialog_proxy()
    handler(test_url)

    # Verify common_dialog was NOT called for local files
    assert not mock_notolog_editor.common_dialog.called

    # Verify check_local_link was called with execute=True
    calls = mock_notolog_editor.check_local_link.call_args_list
    assert any(call.kwargs.get('execute') is True for call in calls)

    print("✓ Local links skip confirmation dialog")


if __name__ == '__main__':
    # Run tests with verbose output
    pytest.main([__file__, '-v', '-s'])
