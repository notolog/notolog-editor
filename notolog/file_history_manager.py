"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Manages file navigation history.
- Functionality: Stores, tracks, and retrieves previously opened files, allowing navigation through history.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2025 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import Signal, QObject

from threading import Lock

import os
import logging


class FileHistoryManager(QObject):
    history_updated = Signal(str)  # Signal emitted when history is updated

    _instance = None  # Singleton instance
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        # Overriding __new__ to control the instantiation process
        if not cls._instance:
            with cls._lock:
                # Create the instance if it doesn't exist
                cls._instance = super(FileHistoryManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, max_history=10):
        # Prevent re-initialization if the instance is already set up.
        if hasattr(self, 'initialized'):
            return

        # Ensure that the initialization check and the setting of base_app_config are atomic.
        with self._lock:
            # Double-check to prevent race conditions during initialization.
            if hasattr(self, 'initialized'):
                return

            super().__init__()

            self.logger = logging.getLogger('file_history_manager')

            self.logger.debug('File history manager is activated')

            # Set the maximum number of history entries that can be stored
            self.max_history = max_history

            # Initialize the history list
            self.history = []
            self.current_index = -1  # Tracks the current position in history

            # Initialize a separate log for history tracking
            self.history_log = []

            # Mark this instance as initialized
            self.initialized = True

    def add_file(self, file_path: str):
        """
        Add a file path to the history.
        """

        # Ignore duplicates if it's the same as the current file
        if not file_path or (self.history and self.history[self.current_index] == file_path):
            self.logger.debug('Skipping file addition to history (same as the last opened)')
            return

        # Update the history with proper handling of forward history and reversing
        self.update_file(file_path)

        # Emit signal to notify the UI that the history has been updated
        self.history_updated.emit(file_path)

    def update_file(self, file_path):
        """
        Update the file history.
        """

        # Add the new file to the history (appended to the most recent position)
        self.history_log.append(file_path)
        if len(self.history_log) > self.max_history:
            # Ensure the history log does not exceed the maximum size by trimming older entries
            self.history_log = self.history_log[-self.max_history:]

        if self.current_index != len(self.history) - 1:
            # Reset history to match the exact history log
            self.history = self.history_log
        else:
            # Add the new file to the end of the history list
            self.history.append(file_path)

        # Ensure the history does not exceed the maximum size
        if len(self.history) > self.max_history:
            self.history.pop(0)  # Maintain the max history size

        # Update current index to the most recently added file
        self.current_index = len(self.history) - 1

    def get_current(self):
        """
        Get the currently opened file from history.
        """
        if 0 <= self.current_index < len(self.history):
            return self.history[self.current_index]
        return None

    def get_valid_file_index(self, direction):
        """
        Get the next or previous valid file index in history.

        @param direction: -1 for previous, 1 for next.
        @return: New valid index if found, else None.
        """
        history_size = len(self.history)  # List of file paths

        # Target index in history (ensuring it points to a valid file)
        index = self.current_index + direction
        # Iterate in the given direction until a valid file is found
        while 0 <= index < history_size:
            # Check if file exists
            if os.path.isfile(self.history[index]):
                return index  # Return the valid index
            index += direction  # Move forward or backward
        return None  # No valid file found

    def prev_file(self):
        """
        Move backward in the history and return the previous file if available.
        """
        prev_index = self.get_valid_file_index(direction=-1)
        if prev_index is not None:
            self.current_index = prev_index
            file_path = self.history[self.current_index]
            self.history_log.append(file_path)  # Append to history log
            self.history_updated.emit(file_path)
            return file_path
        return None  # No previous file

    def next_file(self):
        """
        Move forward in the history and return the next file if available.
        """
        next_index = self.get_valid_file_index(direction=1)
        if next_index is not None:
            self.current_index = next_index
            file_path = self.history[self.current_index]
            self.history_log.append(file_path)  # Append to history log
            self.history_updated.emit(file_path)
            return file_path
        return None  # No next file

    def has_prev(self):
        """
        Check if there is a previous file in history.
        """
        return self.current_index > 0

    def has_next(self):
        """
        Check if there is a next file in history.
        """
        return self.current_index < len(self.history) - 1
