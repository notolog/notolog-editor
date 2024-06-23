"""
Notolog Editor
Open-source markdown editor developed in Python.

File Details:
- Purpose: Part of the base module.
- Functionality: Facilitates access to the module's API functions.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import QObject

from abc import abstractmethod

from typing import Union


class BaseCore(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent = parent

    @property
    @abstractmethod
    def extensions(self) -> list:
        pass

    @property
    @abstractmethod
    def module_name(self):
        pass

    def get_name(self) -> str:
        return str(self)

    @staticmethod
    @abstractmethod
    def get_lexemes_path() -> Union[str, None]:
        # Subclasses are expected to override this method.
        raise NotImplementedError("Subclasses must implement get_lexemes_path()")

    def __str__(self) -> str:
        """
        Return module's name.
        """
        return self.module_name
