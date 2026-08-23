"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Extends QFileSystemModel functionality to provide data for file tree UI.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QFileSystemModel

import os

from typing import Any

from . import ThemeHelper

from ..helpers import file_helper


def get_file_type_icon(file_path: str, theme_helper: ThemeHelper, color: QColor = None):
    """Return the same themed icon used by the file tree for a file path."""
    suffix = os.path.splitext(file_path)[1].lstrip('.').lower()
    icon_name = 'file-earmark.svg'
    color_name = 'main_tree_file_type_default'

    if suffix == 'md':
        icon_name, color_name = 'filetype-md.svg', 'main_tree_file_type_md'
    elif suffix == 'txt':
        icon_name, color_name = 'filetype-txt.svg', 'main_tree_file_type_txt'
    elif suffix == 'html':
        icon_name, color_name = 'filetype-html.svg', 'main_tree_file_type_html'
    elif suffix == 'enc':
        icon_name, color_name = 'file-earmark-lock2.svg', 'main_tree_file_type_enc'
    elif file_helper.remove_trailing_numbers(suffix) == 'del':
        icon_name, color_name = 'file-earmark-x.svg', 'main_tree_file_type_del'

    return theme_helper.get_icon(
        theme_icon=icon_name,
        color=color if color is not None else QColor(theme_helper.get_color(color_name)),
    )


class FileSystemModel(QFileSystemModel):
    def __init__(self, *args, **kwargs):
        super(FileSystemModel, self).__init__(*args, **kwargs)

        self.condition = None
        self.color = None

        # Theme helper
        self.theme_helper = ThemeHelper()

        self.highlighted_indexes = []

    def highlight(self, index, condition, color):
        """
        Keep in mind: the method has invoked on prev items atm.
        @param index: File index
        @param condition: File condition (name in this case)
        @param color: QColor for the role
        @return: None
        """
        self.condition = condition
        self.color = color

        if index.isValid():
            if not any(d.get('condition') == self.condition for d in self.highlighted_indexes):
                self.highlighted_indexes.append({'index': index, 'condition': condition})
                if len(self.highlighted_indexes) > 3:
                    # Or: self.highlighted_indexes = self.highlighted_indexes[-3:]
                    self.highlighted_indexes.pop(0)  # Store only the last X of them, remove the others
            # Data changed signal
            self.dataChanged.emit(index, index, [Qt.ItemDataRole.BackgroundRole])

    def clear_highlights(self):
        """
        Clear last X elements in the file tree. It may help when previous elements were highlighted special way.
        @return: None
        """
        for idx in self.highlighted_indexes:
            index = idx['index']
            condition = idx['condition']
            # Params the data() will be called with
            self.condition = condition
            # Allow to re-draw the role with default fallback color
            self.color = self.theme_helper.get_color('main_tree_background', True)
            # Emit the change
            self.dataChanged.emit(index, index, [Qt.ItemDataRole.BackgroundRole])
        self.highlighted_indexes.clear()

    def data(self, index=int, role=Qt.ItemDataRole.DisplayRole) -> Any:
        """
        Items view decoration.
        More info about ItemDataRole https://doc.qt.io/qt-6/qt.html#ItemDataRole-enum
        """

        # Item's background decoration
        if self.condition and role == Qt.ItemDataRole.BackgroundRole:
            text = index.data(Qt.ItemDataRole.DisplayRole)
            """
            Search 'like' match:
            if self.condition in text:
            """
            # Search exact match
            if self.condition == text:
                return QColor(self.color)

        # Item's text color decoration
        if role == Qt.ItemDataRole.ForegroundRole:
            file_path = self.filePath(index)
            if file_helper.remove_trailing_numbers(file_path).endswith('del'):
                color = self.theme_helper.get_color('main_tree_file_type_del')
                return QColor(color)

        # Item's icon decoration
        if role == Qt.ItemDataRole.DecorationRole:
            info = self.fileInfo(index)
            """
            Decorate file's tree icon by file extension
            """
            # TODO more variants
            if os.path.isfile(info.filePath()):
                return get_file_type_icon(info.filePath(), self.theme_helper)
            elif os.path.isdir(info.filePath()):
                if info.fileName() == "..":
                    color = self.theme_helper.get_color('main_tree_folder_dotdot')
                    return self.theme_helper.get_icon(theme_icon='folder2-open.svg', color=QColor(color))
                else:
                    color = self.theme_helper.get_color('main_tree_folder')
                    return self.theme_helper.get_icon(theme_icon='folder.svg', color=QColor(color))

        return super(FileSystemModel, self).data(index, role)
