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

from notolog.file_history_manager import FileHistoryManager


class TestFileHistoryManager:
    call_cnt = 0

    @pytest.fixture(scope="function")
    def history_manager(self, mocker, request):
        # Check if we need to reset the singleton
        reset_singleton, isfile_values = request.param if hasattr(request, "param") else [(False, None)]

        if isinstance(isfile_values, dict):
            # Mock the method's return value to verify that the manager checks the correct file
            mocker.patch('os.path.isfile', side_effect=lambda k: isfile_values.get(k, None))
        else:
            # Mock the method's return value to verify that the manager checks only the file index
            mocker.patch('os.path.isfile', return_value=True)

        if reset_singleton and FileHistoryManager._instance:
            # Reset the singleton instance before creating a fresh instance
            FileHistoryManager._instance = None

        # Return the (possibly new) instance
        return FileHistoryManager(max_history=5)

    @pytest.mark.parametrize("history_manager", [(False, None)], indirect=True)
    def test_singleton_behavior(self, history_manager):
        # Ensure singleton behavior (only one instance)
        instance1 = FileHistoryManager()
        instance2 = FileHistoryManager()

        assert instance1 is instance2
        assert history_manager is instance1

    @pytest.mark.parametrize("history_manager", [(True, None)], indirect=True)
    def test_add_file(self, history_manager):
        # Test adding a file to the history
        history_manager.add_file("file1.txt")
        assert history_manager.history == ["file1.txt"]
        assert history_manager.get_current() == "file1.txt"

    @pytest.mark.parametrize("history_manager", [(True, None)], indirect=True)
    def test_add_multiple_files(self, history_manager):
        # Test adding multiple files and checking history
        history_manager.add_file("file1.txt")
        history_manager.add_file("file2.txt")
        history_manager.add_file("file3.txt")
        assert history_manager.history == ["file1.txt", "file2.txt", "file3.txt"]

    @pytest.mark.parametrize("history_manager", [(True, None)], indirect=True)
    def test_history_limit(self, history_manager):
        # Ensure that the history does not exceed the max size
        history_manager.add_file("file1.txt")
        history_manager.add_file("file2.txt")
        history_manager.add_file("file3.txt")
        history_manager.add_file("file4.txt")
        history_manager.add_file("file5.txt")
        history_manager.add_file("file6.txt")  # This should remove "file1.txt"

        assert history_manager.history == ["file2.txt", "file3.txt", "file4.txt", "file5.txt", "file6.txt"]

    @pytest.mark.parametrize("history_manager", [(True, None)], indirect=True)
    def test_no_duplicate_files(self, history_manager):
        # Ensure that the current file is not added twice to the history.
        # If the file already exists and is the same as the current file, it should be ignored.
        history_manager.add_file("file1.txt")
        history_manager.add_file("file1.txt")  # Should be ignored
        assert history_manager.history == ["file1.txt"]

    @pytest.mark.parametrize("history_manager", [(True, None)], indirect=True)
    def test_prev_file(self, history_manager):
        # Test navigating backward in history and ensuring the correct previous file is returned.
        history_manager.add_file("file1.txt")
        history_manager.add_file("file2.txt")
        history_manager.add_file("file3.txt")

        prev_file = history_manager.prev_file()
        assert prev_file == "file2.txt"
        assert history_manager.get_current() == "file2.txt"

    @pytest.mark.parametrize("history_manager", [(False, None)], indirect=True)
    def test_prev_file_in_history(self, history_manager):
        # Test navigating to the previous file and ensure the correct file is returned when navigating back.
        prev_file = history_manager.prev_file()
        assert prev_file == "file1.txt"
        assert history_manager.get_current() == "file1.txt"

    @pytest.mark.parametrize("history_manager", [(True, None)], indirect=True)
    def test_next_file(self, history_manager):
        # Test navigating forward in history and ensure the correct next file is returned.
        history_manager.add_file("file1.txt")
        history_manager.add_file("file2.txt")
        history_manager.add_file("file3.txt")
        history_manager.prev_file()  # Go to "file2.txt"

        next_file = history_manager.next_file()
        assert next_file == "file3.txt"
        assert history_manager.get_current() == "file3.txt"

    @pytest.mark.parametrize("history_manager", [(False, None)], indirect=True)
    def test_next_file_in_history(self, history_manager):
        # Test navigating backward and forward in the history and ensure the correct file is returned
        # when moving forward.
        history_manager.prev_file()  # Go to "file2.txt"
        # Test navigating to the next file
        next_file = history_manager.next_file()
        assert next_file == "file3.txt"
        assert history_manager.get_current() == "file3.txt"

    @pytest.mark.parametrize("history_manager", [(True, None)], indirect=True)
    def test_no_prev_file(self, history_manager):
        # Test when there is no previous file to navigate to (i.e., at the beginning of the history).
        history_manager.add_file("file1.txt")
        assert history_manager.prev_file() is None

    @pytest.mark.parametrize("history_manager", [(True, None)], indirect=True)
    def test_no_next_file(self, history_manager):
        # Test when there is no next file available to navigate to (i.e., at the end of the history).
        history_manager.add_file("file1.txt")
        history_manager.add_file("file2.txt")
        history_manager.add_file("file3.txt")
        history_manager.prev_file()  # Go to "file2.txt"
        history_manager.prev_file()  # Go to "file1.txt"

        assert history_manager.current_index == 0
        assert history_manager.next_file()  # Go to "file2.txt"
        assert history_manager.current_index == 1
        assert history_manager.next_file()  # Go to "file3.txt"
        assert history_manager.current_index == 2
        assert history_manager.next_file() is None

    @pytest.mark.parametrize("history_manager", [(True, None)], indirect=True)
    def test_has_prev(self, history_manager):
        # Test if the user can check whether a previous file exists in history,
        # and ensure that the state is correctly updated when navigating back.
        history_manager.add_file("file1.txt")
        history_manager.add_file("file2.txt")
        history_manager.add_file("file3.txt")
        assert history_manager.has_prev() is True
        assert history_manager.has_next() is False
        file_name = history_manager.prev_file()  # Go to "file2.txt"
        assert file_name == "file2.txt"
        assert history_manager.has_prev() is True
        assert history_manager.has_next() is True
        file_name = history_manager.prev_file()  # Go to "file1.txt"
        assert file_name == "file1.txt"
        assert history_manager.has_prev() is False
        assert history_manager.has_next() is True

    @pytest.mark.parametrize(
        "history_manager",
        [(True, {'file1.txt': True, 'file2.txt': False, 'file3.txt': True})],
        indirect=True
    )
    def test_has_prev_and_valid(self, history_manager):
        # Test if the user can check whether a previous file exists in history,
        # and ensure that the state is correctly updated when navigating back.
        history_manager.add_file("file1.txt")
        history_manager.add_file("file2.txt")
        history_manager.add_file("file3.txt")
        assert history_manager.has_prev() is True
        assert history_manager.has_next() is False
        file_name = history_manager.prev_file()  # Navigate to "file1.txt" because "file2.txt" is not accessible.
        assert file_name == "file1.txt"
        assert history_manager.has_prev() is False
        assert history_manager.has_next() is True
        file_name = history_manager.prev_file()  # Stay at "file1.txt"
        assert file_name is None
        assert history_manager.has_prev() is False
        assert history_manager.has_next() is True

    @pytest.mark.parametrize("history_manager", [(True, None)], indirect=True)
    def test_has_next(self, history_manager):
        # Test if the user can check whether a next file exists in history,
        # and ensure that the state is correctly updated when navigating forward.
        history_manager.add_file("file1.txt")
        history_manager.add_file("file2.txt")
        history_manager.add_file("file3.txt")
        file_name = history_manager.prev_file()  # Go to "file2.txt"
        assert file_name == "file2.txt"
        assert history_manager.has_next() is True
        assert history_manager.has_prev() is True
        file_name = history_manager.next_file()  # Go to "file3.txt"
        assert file_name == "file3.txt"
        assert history_manager.has_next() is False

    @pytest.mark.parametrize(
        "history_manager",
        [(True, {'file1.txt': True, 'file2.txt': False, 'file3.txt': True})],
        indirect=True
    )
    def test_has_next_and_valid(self, history_manager):
        # Test if the user can check whether a next file exists in history,
        # and ensure that the state is correctly updated when navigating forward.
        history_manager.add_file("file1.txt")
        history_manager.add_file("file2.txt")
        history_manager.add_file("file3.txt")
        file_name = history_manager.prev_file()  # Navigate to "file1.txt" because "file2.txt" is not accessible.
        assert file_name == "file1.txt"
        assert history_manager.has_next() is True
        assert history_manager.has_prev() is False
        file_name = history_manager.next_file()  # Navigate to "file3.txt" because "file2.txt" is not accessible.
        assert file_name == "file3.txt"
        assert history_manager.has_next() is False

    @pytest.mark.parametrize("history_manager", [(True, None)], indirect=True)
    def test_add_empty_file(self, history_manager):
        # Test how the system handles empty file paths (they should be ignored and not added to history).
        history_manager.add_file("")
        assert history_manager.history == []

    @pytest.mark.parametrize("history_manager", [(True, None)], indirect=True)
    def test_add_duplicate_current_file(self, history_manager):
        """
        Test adding the same current file (which is already at the last position in history).
        Ensure the file is moved to the last position.
        """
        history_manager.add_file("file1.txt")
        history_manager.add_file("file2.txt")
        history_manager.add_file("file3.txt")

        # History should now be ["file1.txt", "file2.txt", "file3.txt"]
        assert history_manager.history == ["file1.txt", "file2.txt", "file3.txt"]

        # Adding file1.txt again
        history_manager.add_file("file1.txt")
        # After file1.txt is added again, it should move to the last position
        assert history_manager.history == ["file1.txt", "file2.txt", "file3.txt", "file1.txt"]

        # Adding file3.txt again should move it to the last position
        history_manager.add_file("file3.txt")
        assert history_manager.history == ["file1.txt", "file2.txt", "file3.txt", "file1.txt", "file3.txt"]

        history_manager.prev_file()
        history_manager.add_file("file2.txt")
        assert history_manager.history == ["file3.txt", "file1.txt", "file3.txt", "file1.txt", "file2.txt"]

    @pytest.mark.parametrize("history_manager", [(True, None)], indirect=True)
    def test_history_navigation(self, history_manager):
        """
        Test history navigation and ensure the order is maintained when moving backward and forward in history.
        Also, ensure that the correct file is returned when navigating through history.
        """
        history_manager.add_file("file1.txt")
        history_manager.add_file("file2.txt")
        history_manager.add_file("file3.txt")

        # History should now be ["file1.txt", "file2.txt", "file3.txt"]
        assert history_manager.history == ["file1.txt", "file2.txt", "file3.txt"]

        history_manager.add_file("file3.txt")
        history_manager.add_file("file4.txt")
        history_manager.add_file("file5.txt")
        assert history_manager.history == ["file1.txt", "file2.txt", "file3.txt", "file4.txt", "file5.txt"]

        history_manager.prev_file()
        history_manager.prev_file()
        history_manager.prev_file()
        history_manager.prev_file()
        history_manager.prev_file()
        assert history_manager.history == ["file1.txt", "file2.txt", "file3.txt", "file4.txt", "file5.txt"]
        assert history_manager.current_index == 0

        history_manager.next_file()
        assert history_manager.current_index == 1
        history_manager.next_file()
        assert history_manager.history == ["file1.txt", "file2.txt", "file3.txt", "file4.txt", "file5.txt"]
        assert history_manager.current_index == 2

        history_manager.add_file("file1.txt")
        assert history_manager.history == ["file2.txt", "file1.txt", "file2.txt", "file3.txt", "file1.txt"]
