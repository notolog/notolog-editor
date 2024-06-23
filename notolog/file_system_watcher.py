"""
Notolog Editor
Open-source markdown editor developed in Python.

File Details:
- Purpose: File changes observer.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import QFileSystemWatcher, QDir

import os
import logging

from .app_config import AppConfig


class FileSystemWatcher:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, '_initialized', False):
            return
        self._initialized = True

        self.logger = logging.getLogger('file_system_watcher')

        self.logging = AppConfig().get_logging()
        self.debug = AppConfig().get_debug()

        self.dir = None

        self.files = set()

        self.watcher = QFileSystemWatcher()
        self.watcher.directoryChanged.connect(self.on_dir_changed)
        self.watcher.fileChanged.connect(self.on_file_changed)

    def update_files(self):
        if self.dir:
            files = set(self.dir.entryList())
            files.discard(".")  # Ignore current directory entry
            files.discard("..")  # Ignore parent directory entry
            self.files.update(files)

    def watch(self, directory):
        # Disconnect signals from the previous directory
        if self.dir:
            self.watcher.directoryChanged.disconnect()
            self.watcher.fileChanged.disconnect()

        # Clear the previous directory's file list
        self.files.clear()

        # Set up the QFileSystemWatcher to monitor the new directory
        self.dir = QDir(directory)
        self.watcher.addPath(directory)

        # Connect signals for the new directory
        self.watcher.directoryChanged.connect(self.on_dir_changed)
        self.watcher.fileChanged.connect(self.on_file_changed)

        self.update_files()

    def on_dir_changed(self, path):
        new_files = set(self.dir.entryList())

        new_files.discard(".")  # Ignore current dir
        new_files.discard("..")  # Ignore parent dir

        added_files = new_files - self.files
        removed_files = self.files - new_files

        renamed_files = set()
        for added_file in added_files:
            potential_renamed_file = os.path.join(self.dir.path(), added_file)
            if os.path.exists(potential_renamed_file):
                renamed_files.add((added_file, potential_renamed_file))

        if added_files:
            if self.debug:
                self.logger.debug(f"New file(s) added: {', '.join(added_files)}")
        if removed_files:
            if self.debug:
                self.logger.debug(f"File(s) removed: {', '.join(removed_files)}")
        if renamed_files:
            if self.debug:
                self.logger.debug(f"File(s) renamed: {', '.join([f[0] for f in renamed_files])}")

        self.files = new_files

    def on_file_changed(self, path):
        if self.debug:
            self.logger.debug(f"File changed: {path}")
