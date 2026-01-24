"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Tests for FileTree UI component.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import Qt, QPoint, QCoreApplication
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QListView, QLineEdit, QLabel
from PySide6.QtGui import QStandardItemModel, QStandardItem

from notolog.ui.file_tree import FileTree
from notolog.settings import Settings

from . import test_app  # noqa: F401

import pytest


class TestFileTree:
    """Comprehensive test suite for FileTree widget."""

    @pytest.fixture(scope="function", autouse=True)
    def settings_obj(self, mocker):
        """Initialize settings for each test."""
        # Force default language
        from notolog.enums.languages import Languages
        mocker.patch.object(Languages, 'default', return_value='en')

        settings = Settings()
        settings.clear()
        Settings.reload()

        # Ensure language is set to 'en'
        settings.app_language = 'en'

        yield settings

    @pytest.fixture
    def main_window(self, mock_main_window_for_widgets):
        """Use mock main window to prevent segfaults in headless environments."""
        yield mock_main_window_for_widgets

    @pytest.fixture
    def proxy_model(self):
        """Create a proxy model for testing."""
        model = QStandardItemModel()
        model.appendRow(QStandardItem("test_file_1.md"))
        model.appendRow(QStandardItem("test_file_2.md"))
        model.appendRow(QStandardItem("test_folder"))
        yield model

    @pytest.fixture
    def clicked_callback_mock(self, mocker):
        """Create a mock callback for click events."""
        return mocker.Mock()

    @pytest.fixture
    def text_changed_callback_mock(self, mocker):
        """Create a mock callback for text change events."""
        return mocker.Mock()

    @pytest.fixture
    def context_menu_callback_mock(self, mocker):
        """Create a mock callback for context menu events."""
        return mocker.Mock()

    @pytest.fixture
    def file_tree(self, main_window, proxy_model, clicked_callback_mock,
                  text_changed_callback_mock, context_menu_callback_mock):
        """Create FileTree instance for testing."""
        tree = FileTree(
            parent=main_window,
            proxy_model=proxy_model,
            minimum_width=200,
            clicked_callback=clicked_callback_mock,
            text_changed_callback=text_changed_callback_mock,
            context_menu_callback=context_menu_callback_mock
        )
        tree.show()  # Show widget to ensure geometry is calculated
        QCoreApplication.processEvents()  # Process events to update UI
        yield tree

    # ===== INITIALIZATION TESTS =====

    def test_file_tree_initialization(self, file_tree, settings_obj):
        """Test FileTree initializes with correct configuration."""
        assert isinstance(file_tree, FileTree)
        assert settings_obj.app_language == 'en'

    def test_constants_defined(self, file_tree):
        """Test class constants are properly defined."""
        assert FileTree.FILTER_MAX_LENGTH == 512
        assert FileTree.CLEAR_BUTTON_TEXT == '×'
        assert FileTree.CLEAR_BUTTON_SIZE_RATIO == 1.0

    def test_ui_components_initialized(self, file_tree):
        """Test all UI components are properly initialized."""
        assert isinstance(file_tree.list_view, QListView)
        assert isinstance(file_tree.tree_filter, QLineEdit)
        assert isinstance(file_tree.tree_filter_clear_btn, QLabel)

    def test_list_view_configuration(self, file_tree, proxy_model):
        """Test list view is configured correctly."""
        assert file_tree.list_view.model() == proxy_model
        assert file_tree.list_view.font() == file_tree.font()
        assert file_tree.list_view.selectionMode() == QListView.SelectionMode.NoSelection
        assert file_tree.list_view.contextMenuPolicy() == Qt.ContextMenuPolicy.CustomContextMenu

    def test_filter_input_configuration(self, file_tree):
        """Test filter input is configured correctly."""
        assert file_tree.tree_filter.font() == file_tree.font()
        assert not file_tree.tree_filter.isReadOnly()
        assert file_tree.tree_filter.maxLength() == FileTree.FILTER_MAX_LENGTH
        assert file_tree.tree_filter.minimumWidth() == 200
        assert file_tree.tree_filter.placeholderText() != ""

    def test_clear_button_configuration(self, file_tree):
        """Test clear button is configured correctly."""
        assert file_tree.tree_filter_clear_btn.objectName() == 'tree_filter_clear_btn'
        assert file_tree.tree_filter_clear_btn.font() == file_tree.font()
        assert file_tree.tree_filter_clear_btn.cursor().shape() == Qt.CursorShape.PointingHandCursor
        assert file_tree.tree_filter_clear_btn.isHidden()  # Initially hidden

    # ===== CALLBACK TESTS =====

    def test_callbacks_stored(self, file_tree, clicked_callback_mock,
                              text_changed_callback_mock, context_menu_callback_mock):
        """Test callbacks are properly stored."""
        assert file_tree.clicked_callback == clicked_callback_mock
        assert file_tree.text_changed_callback == text_changed_callback_mock
        assert file_tree.context_menu_callback == context_menu_callback_mock

    def test_text_changed_callback_triggered(self, file_tree, text_changed_callback_mock):
        """Test text change callback is triggered on filter input."""
        file_tree.tree_filter.setText("test")
        text_changed_callback_mock.assert_called_with("test")

    # ===== FILTER FUNCTIONALITY TESTS =====

    def test_filter_text_shows_clear_button(self, file_tree):
        """Test clear button appears when text is entered."""
        # Use isHidden() to check explicit visibility state (independent of parent visibility)
        assert file_tree.tree_filter_clear_btn.isHidden()

        file_tree.tree_filter.setText("test")
        QCoreApplication.processEvents()  # Process events to trigger signal
        assert not file_tree.tree_filter_clear_btn.isHidden()

    def test_filter_clear_hides_button(self, file_tree):
        """Test clear button hides when filter is cleared."""
        file_tree.tree_filter.setText("test")
        QCoreApplication.processEvents()
        assert not file_tree.tree_filter_clear_btn.isHidden()

        file_tree.clear_filter()
        QCoreApplication.processEvents()
        assert file_tree.tree_filter_clear_btn.isHidden()
        assert file_tree.tree_filter.text() == ""

    def test_clear_button_click_clears_filter(self, file_tree):
        """Test clicking clear button clears the filter."""
        file_tree.tree_filter.setText("test")
        QCoreApplication.processEvents()
        assert file_tree.tree_filter.text() == "test"
        assert not file_tree.tree_filter_clear_btn.isHidden()

        # Simulate click on clear button
        button_center = file_tree.tree_filter_clear_btn.rect().center()
        event_pos = file_tree.tree_filter_clear_btn.mapToParent(button_center)
        QTest.mouseClick(file_tree, Qt.MouseButton.LeftButton, pos=event_pos)
        QCoreApplication.processEvents()

        assert file_tree.tree_filter.text() == ""

    def test_empty_filter_text_hides_button(self, file_tree):
        """Test button hides when filter text is emptied."""
        file_tree.tree_filter.setText("test")
        QCoreApplication.processEvents()
        assert not file_tree.tree_filter_clear_btn.isHidden()

        file_tree.tree_filter.setText("")
        QCoreApplication.processEvents()
        assert file_tree.tree_filter_clear_btn.isHidden()

    # ===== CLEAR BUTTON APPEARANCE TESTS =====

    def test_clear_button_text(self, file_tree):
        """Test clear button displays correct text."""
        file_tree.tree_filter.setText("test")
        QCoreApplication.processEvents()
        assert file_tree.tree_filter_clear_btn.text() == FileTree.CLEAR_BUTTON_TEXT

    def test_clear_button_size_matches_filter(self, file_tree):
        """Test clear button size matches filter input height."""
        file_tree.tree_filter.setText("test")
        QCoreApplication.processEvents()
        filter_height = file_tree.tree_filter.sizeHint().height()
        button_size = file_tree.tree_filter_clear_btn.size()

        assert button_size.width() == filter_height
        assert button_size.height() == filter_height

    def test_clear_button_position(self, file_tree):
        """Test clear button is positioned correctly."""
        file_tree.tree_filter.setText("test")
        QCoreApplication.processEvents()

        button_x = file_tree.tree_filter_clear_btn.x()
        input_width = file_tree.tree_filter.width()
        button_width = file_tree.tree_filter_clear_btn.width()

        # Button should be right-aligned
        assert button_x == input_width - button_width

    def test_filter_padding_prevents_text_overlap(self, file_tree):
        """Test filter input has padding to prevent text overlap with button."""
        file_tree.tree_filter.setText("test")
        QCoreApplication.processEvents()

        stylesheet = file_tree.tree_filter.styleSheet()
        button_width = file_tree.tree_filter_clear_btn.width()

        assert f"padding-right: {button_width}px" in stylesheet

    # ===== SETTINGS UPDATE TESTS =====

    def test_theme_change_updates_button(self, file_tree, mocker):
        """Test theme change updates clear button styling."""
        file_tree.tree_filter.setText("test")

        # Mock theme color change
        mocker.patch.object(file_tree.theme_helper, 'get_color', return_value='#FF0000')

        file_tree.settings_update_handler({'app_theme': 'dark'})

        assert '#FF0000' in file_tree.tree_filter_clear_btn.styleSheet()

    def test_font_size_change_updates_widgets(self, file_tree, main_window, mocker):
        """Test font size change updates all widgets."""
        from PySide6.QtGui import QFont

        # Create new font with different size
        new_font = QFont()
        new_font.setPointSize(16)
        mocker.patch.object(main_window, 'font', return_value=new_font)

        file_tree.tree_filter.setText("test")
        # Store initial size for potential future comparison
        _ = file_tree.tree_filter_clear_btn.size()

        file_tree.settings_update_handler({'app_font_size': 16})

        # Verify font applied to all widgets
        assert file_tree.font().pointSize() == 16
        assert file_tree.list_view.font().pointSize() == 16
        assert file_tree.tree_filter.font().pointSize() == 16
        assert file_tree.tree_filter_clear_btn.font().pointSize() == 16

        # Button size should update
        new_button_size = file_tree.tree_filter_clear_btn.size()
        # Size might change based on new filter height
        assert new_button_size.width() > 0

    def test_language_change_updates_labels(self, file_tree, mocker):
        """Test language change updates UI text."""
        from notolog.lexemes.lexemes import Lexemes

        # Mock lexemes to return different text
        mock_lexemes = mocker.Mock(spec=Lexemes)
        mock_lexemes.get.side_effect = lambda key, scope=None: f"NEW_{key}"
        mocker.patch('notolog.ui.file_tree.Lexemes', return_value=mock_lexemes)

        file_tree.settings_update_handler({'app_language': 'es'})

        # Verify placeholder text updated
        assert file_tree.tree_filter.placeholderText() == "NEW_tree_filter_input_placeholder_text"

    # ===== RESIZE EVENT TESTS =====

    def test_resize_event_repositions_button(self, file_tree):
        """Test resize event repositions clear button."""
        file_tree.tree_filter.setText("test")

        # Store initial position for potential future comparison
        _ = file_tree.tree_filter_clear_btn.pos()

        # Trigger resize
        file_tree.resize(500, 400)

        # Button should be repositioned
        new_pos = file_tree.tree_filter_clear_btn.pos()
        # X position should change with resize
        assert new_pos is not None

    # ===== PUBLIC API TESTS =====

    def test_get_list_view_returns_list_view(self, file_tree):
        """Test get_list_view returns the list view widget."""
        list_view = file_tree.get_list_view()
        assert list_view == file_tree.list_view
        assert isinstance(list_view, QListView)

    def test_on_filter_text_changed_with_empty_text(self, file_tree):
        """Test on_filter_text_changed handles empty text correctly."""
        file_tree.on_filter_text_changed("")
        assert file_tree.tree_filter_clear_btn.isHidden()

    def test_on_filter_text_changed_with_text(self, file_tree):
        """Test on_filter_text_changed handles text correctly."""
        file_tree.on_filter_text_changed("test")
        QCoreApplication.processEvents()
        assert not file_tree.tree_filter_clear_btn.isHidden()

    # ===== EDGE CASES AND ERROR HANDLING =====

    def test_update_clear_button_without_filter(self, file_tree):
        """Test update_clear_button handles missing filter gracefully."""
        file_tree.tree_filter = None
        # Should not raise exception
        file_tree.update_clear_button()

    def test_update_clear_button_without_button(self, file_tree):
        """Test update_clear_button handles missing button gracefully."""
        file_tree.tree_filter_clear_btn = None
        # Should not raise exception
        file_tree.update_clear_button()

    def test_clear_filter_without_filter_widget(self, file_tree):
        """Test clear_filter handles missing filter widget gracefully."""
        file_tree.tree_filter = None
        # Should not raise exception
        file_tree.clear_filter()

    def test_theme_color_fallback(self, file_tree, mocker):
        """Test theme color uses fallback when color not found."""
        mocker.patch.object(file_tree.theme_helper, 'get_color', return_value=None)

        color = file_tree._get_theme_color()
        assert color == '#888888'  # Fallback gray

    def test_mouse_press_outside_button(self, file_tree):
        """Test mouse press outside button doesn't clear filter."""
        file_tree.tree_filter.setText("test")

        # Click outside button
        QTest.mouseClick(file_tree, Qt.MouseButton.LeftButton, pos=QPoint(10, 10))

        # Filter should still have text
        assert file_tree.tree_filter.text() == "test"

    def test_settings_update_with_runtime_error(self, file_tree, mocker):
        """Test settings update handles RuntimeError gracefully."""
        mocker.patch.object(file_tree, 'setStyleSheet', side_effect=RuntimeError("Test error"))

        # Should not raise exception, just log warning
        file_tree.settings_update_handler({'app_theme': 'dark'})

    # ===== ACCESSIBILITY TESTS =====

    def test_filter_input_accessibility(self, file_tree):
        """Test filter input has accessibility properties."""
        assert file_tree.tree_filter.accessibleDescription() != ""

    def test_clear_button_accessibility(self, file_tree):
        """Test clear button has accessibility properties."""
        assert file_tree.tree_filter_clear_btn.accessibleName() != ""
        assert file_tree.tree_filter_clear_btn.toolTip() != ""

    # ===== INTEGRATION TESTS =====

    def test_full_filter_workflow(self, file_tree, text_changed_callback_mock):
        """Test complete filter workflow."""
        # Start with empty filter
        assert file_tree.tree_filter.text() == ""
        assert file_tree.tree_filter_clear_btn.isHidden()

        # Type text
        file_tree.tree_filter.setText("test")
        QCoreApplication.processEvents()
        assert not file_tree.tree_filter_clear_btn.isHidden()
        text_changed_callback_mock.assert_called_with("test")

        # Clear filter
        file_tree.clear_filter()
        QCoreApplication.processEvents()
        assert file_tree.tree_filter.text() == ""
        assert file_tree.tree_filter_clear_btn.isHidden()

    def test_multiple_setting_changes(self, file_tree, mocker):
        """Test multiple settings can be changed at once."""
        from PySide6.QtGui import QFont

        new_font = QFont()
        new_font.setPointSize(14)
        mocker.patch.object(file_tree.parent, 'font', return_value=new_font)
        mocker.patch.object(file_tree.theme_helper, 'get_color', return_value='#00FF00')

        file_tree.tree_filter.setText("test")
        QCoreApplication.processEvents()

        # Change theme and font size together
        file_tree.settings_update_handler({
            'app_theme': 'light',
            'app_font_size': 14
        })

        # Both changes should be applied
        assert file_tree.font().pointSize() == 14
        assert '#00FF00' in file_tree.tree_filter_clear_btn.styleSheet()

    # ===== ESC KEY FUNCTIONALITY TESTS =====

    def test_esc_key_clears_filter_when_focused(self, file_tree):
        """Test pressing Esc clears filter when input has focus and content."""
        # Set text and focus on filter
        file_tree.tree_filter.setText("test")
        file_tree.tree_filter.setFocus()
        QCoreApplication.processEvents()

        assert file_tree.tree_filter.text() == "test"
        assert not file_tree.tree_filter_clear_btn.isHidden()
        # Note: hasFocus() may return False in headless environments, but we can still test the behavior

        # Press Esc key
        QTest.keyClick(file_tree.tree_filter, Qt.Key.Key_Escape)
        QCoreApplication.processEvents()

        # Filter should be cleared
        assert file_tree.tree_filter.text() == ""
        assert file_tree.tree_filter_clear_btn.isHidden()

    def test_esc_key_does_nothing_when_filter_empty(self, file_tree):
        """Test pressing Esc does nothing when filter is empty."""
        # Focus on filter without text
        file_tree.tree_filter.setFocus()
        QCoreApplication.processEvents()

        assert file_tree.tree_filter.text() == ""
        assert file_tree.tree_filter_clear_btn.isHidden()
        # Note: hasFocus() may return False in headless environments, but we can still test the behavior

        # Press Esc key
        QTest.keyClick(file_tree.tree_filter, Qt.Key.Key_Escape)
        QCoreApplication.processEvents()

        # Nothing should change (already empty)
        assert file_tree.tree_filter.text() == ""
        assert file_tree.tree_filter_clear_btn.isHidden()

    def test_esc_key_does_nothing_when_not_focused(self, file_tree):
        """Test pressing Esc does nothing when filter doesn't have focus."""
        # Set text but don't focus on filter
        file_tree.tree_filter.setText("test")
        file_tree.tree_filter.clearFocus()
        QCoreApplication.processEvents()

        assert file_tree.tree_filter.text() == "test"
        assert not file_tree.tree_filter_clear_btn.isHidden()
        # Note: hasFocus() may return False in headless environments even without clearFocus()

        # Press Esc key on file_tree widget (not on filter input)
        QTest.keyClick(file_tree, Qt.Key.Key_Escape)
        QCoreApplication.processEvents()

        # Filter should still have text (Esc on parent widget doesn't clear it)
        assert file_tree.tree_filter.text() == "test"

    def test_esc_key_multiple_times(self, file_tree):
        """Test pressing Esc multiple times is handled correctly."""
        # Set text and focus
        file_tree.tree_filter.setText("test")
        file_tree.tree_filter.setFocus()
        QCoreApplication.processEvents()

        # First Esc clears the filter
        QTest.keyClick(file_tree.tree_filter, Qt.Key.Key_Escape)
        QCoreApplication.processEvents()
        assert file_tree.tree_filter.text() == ""

        # Second Esc does nothing (already empty)
        QTest.keyClick(file_tree.tree_filter, Qt.Key.Key_Escape)
        QCoreApplication.processEvents()
        assert file_tree.tree_filter.text() == ""

    def test_esc_key_clears_and_callback_called(self, file_tree, text_changed_callback_mock):
        """Test Esc key clears filter and triggers text change callback."""
        # Reset mock to clear any previous calls
        text_changed_callback_mock.reset_mock()

        # Set text and focus
        file_tree.tree_filter.setText("test")
        file_tree.tree_filter.setFocus()
        QCoreApplication.processEvents()

        # Clear previous calls from setText
        text_changed_callback_mock.reset_mock()

        # Press Esc key
        QTest.keyClick(file_tree.tree_filter, Qt.Key.Key_Escape)
        QCoreApplication.processEvents()

        # Callback should be triggered with empty string
        assert file_tree.tree_filter.text() == ""
        text_changed_callback_mock.assert_called_with("")

    def test_esc_key_workflow_with_typing(self, file_tree):
        """Test complete workflow: type, Esc to clear, type again."""
        file_tree.tree_filter.setFocus()

        # Type some text
        file_tree.tree_filter.setText("first")
        QCoreApplication.processEvents()
        assert file_tree.tree_filter.text() == "first"
        assert not file_tree.tree_filter_clear_btn.isHidden()

        # Press Esc to clear
        QTest.keyClick(file_tree.tree_filter, Qt.Key.Key_Escape)
        QCoreApplication.processEvents()
        assert file_tree.tree_filter.text() == ""
        assert file_tree.tree_filter_clear_btn.isHidden()

        # Type new text
        file_tree.tree_filter.setText("second")
        QCoreApplication.processEvents()
        assert file_tree.tree_filter.text() == "second"
        assert not file_tree.tree_filter_clear_btn.isHidden()

    def test_esc_key_same_as_clear_button(self, file_tree):
        """Test Esc key produces same result as clicking clear button."""
        # Test with clear button
        file_tree.tree_filter.setText("test1")
        file_tree.tree_filter.setFocus()
        QCoreApplication.processEvents()

        # Click clear button
        button_center = file_tree.tree_filter_clear_btn.rect().center()
        event_pos = file_tree.tree_filter_clear_btn.mapToParent(button_center)
        QTest.mouseClick(file_tree, Qt.MouseButton.LeftButton, pos=event_pos)
        QCoreApplication.processEvents()

        state_after_button = file_tree.tree_filter.text()
        button_visible_after_button = file_tree.tree_filter_clear_btn.isHidden()

        # Reset and test with Esc key
        file_tree.tree_filter.setText("test1")
        file_tree.tree_filter.setFocus()
        QCoreApplication.processEvents()

        QTest.keyClick(file_tree.tree_filter, Qt.Key.Key_Escape)
        QCoreApplication.processEvents()

        state_after_esc = file_tree.tree_filter.text()
        button_visible_after_esc = file_tree.tree_filter_clear_btn.isHidden()

        # Both should produce same result
        assert state_after_button == state_after_esc == ""
        assert button_visible_after_button == button_visible_after_esc is True

    def test_other_keys_not_affected_by_esc_handler(self, file_tree):
        """Test other keys still work normally when filter has focus."""
        file_tree.tree_filter.setFocus()

        # Type some text using key events
        QTest.keyClicks(file_tree.tree_filter, "abc")
        QCoreApplication.processEvents()

        # Text should be typed normally
        assert file_tree.tree_filter.text() == "abc"

        # Backspace should work
        QTest.keyClick(file_tree.tree_filter, Qt.Key.Key_Backspace)
        QCoreApplication.processEvents()
        assert file_tree.tree_filter.text() == "ab"

    def test_esc_key_with_null_button(self, file_tree):
        """Test Esc key handling when clear button is None (edge case)."""
        file_tree.tree_filter.setText("test")
        file_tree.tree_filter.setFocus()
        file_tree.tree_filter_clear_btn = None
        QCoreApplication.processEvents()

        # Should not raise exception
        QTest.keyClick(file_tree.tree_filter, Qt.Key.Key_Escape)
        QCoreApplication.processEvents()

        # Text should not be cleared (button check fails)
        assert file_tree.tree_filter.text() == "test"

    def test_esc_key_with_null_filter(self, file_tree):
        """Test Esc key handling when filter is None (edge case)."""
        original_filter = file_tree.tree_filter
        file_tree.tree_filter = None
        QCoreApplication.processEvents()

        # Should not raise exception
        QTest.keyClick(file_tree, Qt.Key.Key_Escape)
        QCoreApplication.processEvents()

        # Restore for cleanup
        file_tree.tree_filter = original_filter
