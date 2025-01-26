"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Extends QSortFilterProxyModel.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2025 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import QModelIndex, QSortFilterProxyModel, QRegularExpression

import os
import logging

from ..helpers import file_helper


class SortFilterProxyModel(QSortFilterProxyModel):

    def __init__(self, extensions: list = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logger = logging.getLogger('sort_filter_proxy_model')

        self._extensions = extensions  # Allow specific file extensions

    def get_extensions(self):
        # Get allowed file extensions
        return self._extensions

    def set_extensions(self, extensions):
        # Set allowed file extensions
        self._extensions = extensions
        self.invalidateFilter()  # Reapply the filter to the model to update view

    def add_extension(self, extension):
        # Add specific file extension
        if extension not in self._extensions:
            self._extensions.append(extension)
            self.invalidateFilter()  # Reapply the filter with the new extension

    def remove_extension(self, extension):
        # Remove specific file extension
        if extension in self._extensions:
            self._extensions.remove(extension)
            self.invalidateFilter()  # Reapply the filter without the removed extension

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        source_model = self.sourceModel()
        index = source_model.index(source_row, 0, source_parent)
        if not index.isValid():
            return False

        regex = self.filterRegularExpression()  # Retrieve regex set with setFilterRegularExpression()
        if regex and regex.pattern():
            re = QRegularExpression(regex)
            match = re.match(index.data())
            if not (match.capturedTexts() and match.captured()):
                self.logger.debug('Filter row: %s' % index.data())
                return False

        if source_model.isDir(index):  # noqa
            return True  # Always show directories
        else:
            file_path = source_model.filePath(index)  # noqa
            extension = file_path.split(".")[-1]
            return not self._extensions or file_helper.remove_trailing_numbers(extension).lower() in self._extensions

    def lessThan(self, left: QModelIndex, right: QModelIndex) -> bool:
        # Get the source model
        source_model = self.sourceModel()

        # Get the file names for the left and the right indexes
        left_name = source_model.fileName(left)  # noqa
        right_name = source_model.fileName(right)  # noqa

        # Sort "dotdot" always at the top (check the "dot" is not visible)
        if left_name == ".." and right_name != "..":
            return True
        elif right_name != ".." and left_name == "..":
            return False

        left_path = source_model.filePath(left)  # noqa
        right_path = source_model.filePath(right)  # noqa

        if os.path.isdir(left_path) and not os.path.isdir(right_path):
            return True
        elif not os.path.isdir(left_path) and os.path.isdir(right_path):
            return False

        # Default sorting order
        return super().lessThan(left, right)
