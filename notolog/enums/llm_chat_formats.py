"""
Notolog Editor
Open-source markdown editor developed in Python.

File Details:
- Purpose: Enum class with possible LLM chat formats, e.g. 'chatml', 'llama-2', 'gemma', etc..

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from .enum_base import EnumBase

assert hasattr(EnumBase, 'default'), "Check default() method is implemented in the base class"


class LlmChatFormats(EnumBase):

    # First param is format name
    # Second param in the tuple corresponds to default value
    CHATML = ("chatml", True)
    LLAMA2 = "llama-2"
    GEMMA = "gemma"
