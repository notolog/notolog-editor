"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Extends QTextBlockUserData to support data storage for text editing cross-actions.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtGui import QTextBlockUserData

from typing import Any, Type


class TextBlockData(QTextBlockUserData):
    def __init__(self, block_number):
        super().__init__()

        self.block_number = block_number
        self.data = {}

    def put(self, tag=str, opened=bool, within=bool, closed=bool, start: int = 0, end: int = 0) -> None:
        new_data = {'opened': opened, 'within': within, 'closed': closed, 'start': start, 'end': end}
        existing_data = self.get_all(tag)
        if existing_data is not None:
            for data_index, data_row in enumerate(existing_data):
                # The equal element is already exist
                if data_row == new_data:
                    return
                # Check either update needed or not
                # TODO: Improve the check algorithm as it's quite simple at the moment.
                if data_row['start'] == new_data['start'] and data_row['end'] == new_data['end']:
                    existing_data[data_index].update(new_data)
            if isinstance(existing_data, list):
                existing_data.append(new_data)
            elif isinstance(existing_data, dict):
                existing_data = [existing_data, new_data]
            else:
                existing_data = [new_data]
            self.data[tag] = existing_data
        else:
            self.data[tag] = [new_data]

    def update(self, tag=str, index=Type[int], opened=bool, within=bool, closed=bool,
               start: int = 0, end: int = 0) -> None:
        existing_data = self.get_one(tag, index)
        if existing_data is not None:
            existing_data.update({'opened': opened, 'within': within, 'closed': closed, 'start': start, 'end': end})
            self.data[tag][index] = existing_data

    def get_one(self, tag=str, index=0) -> Any:
        """
        This method returns a single piece of list data.
        Consider using it with code blocks only where the multiple occurrences are not supported.
        """
        if (tag in self.data
                and self.data[tag]
                and 0 <= index < len(self.data[tag])):
            return self.data[tag][index]
        return None

    def get_all(self, tag=str) -> Any:
        """
        This method returns all stored pieces of list data.
        Consider using it with the multiple occurrences, like a few strikethrough elements within one line.
        """
        if tag in self.data and self.data[tag]:
            return self.data[tag]
        return None

    def get_param(self, tag=str, param=str) -> Any:
        item = self.get_one(tag)
        if item and param in item:
            return item[param]
        return None

    def drop(self, tag=str):
        if tag in self.data:
            self.data.__delitem__(tag)

    def drop_index(self, tag=str, index=0) -> None:
        if tag in self.data:
            if 0 <= index < len(self.data[tag]):
                # These variants are also work:
                # self.data[tag].__delitem__(index)
                # self.data[tag] = [item for key, item in enumerate(self.data[tag]) if key != index]
                del self.data[tag][index]

    def search(self, tag=str, key=str, value=any) -> Any:
        if tag in self.data:
            return [data for data in self.data[tag] if key in data and data[key] == value][0]
        return None

    def __repr__(self):
        return '\n'.join([f'[{self.block_number}] {tag}: {item}' for tag, item in self.data.items()])
