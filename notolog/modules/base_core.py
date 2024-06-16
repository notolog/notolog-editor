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
