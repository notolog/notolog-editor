"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Part of the base module.
- Functionality: Base class for modules that extend AI Assistant functionality.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
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
