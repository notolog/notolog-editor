"""
Base class for modules that extend AI Assistant functionality.
"""

from abc import abstractmethod

from .base_core import BaseCore


class BaseAiCore(BaseCore):

    @abstractmethod
    def get_prompt_manager(self):
        # Subclasses are expected to override this method.
        raise NotImplementedError("Subclasses must implement get_prompt_manager()")

    @abstractmethod
    def request(self, *args, **kwargs):
        # Subclasses are expected to override this method.
        raise NotImplementedError("Subclasses must implement request()")
