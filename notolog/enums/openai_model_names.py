"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Enum class for the supported OpenAI API models.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2025 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from .enum_base import EnumBase

assert hasattr(EnumBase, 'default'), "Check default() method is implemented in the base class"


class OpenAiModelNames(EnumBase):

    # First param is model name
    # Second param is a legacy flag (e.g. legacy completions)
    # Third param in the tuple corresponds to default value
    GPT_4O_MINI = ("gpt-4o-mini", False, True)
    GPT_4 = "gpt-4-turbo"
    GPT_3_5 = ("gpt-3.5-turbo", True)
    GPT_3_5_LEGACY = ("gpt-3.5-turbo-instruct", True)

    def __init__(self, value, legacy=False, is_default=False, *args, **kwargs):
        super().__init__(value, is_default=is_default, *args, **kwargs)
        # Additional argument
        self.legacy = legacy

    @classmethod
    def legacy_members(cls):
        # Legacy means the outdated model, e.g. legacy completions that is still supported.
        return [member for member in cls if member.legacy]

    @classmethod
    def legacy(cls, member):
        # Legacy means the outdated model, e.g. legacy completions that is still supported.
        return member in cls.legacy_members()
