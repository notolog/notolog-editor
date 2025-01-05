"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Base Enum class to support extension classes with minimal required functionality.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2025 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from enum import Enum


class EnumBase(Enum):

    def __init__(self, value, is_default=False, *args, **kwargs):
        self._value_ = value
        self.is_default = is_default
        super().__init__(*args, **kwargs)

    def __str__(self):
        return self.name.lower()

    @classmethod
    def __getitem__(cls, key):
        if isinstance(key, str):
            key = key.upper()  # Normalize the key to uppercase
        try:
            return cls._member_map_[key]
        except KeyError:
            raise KeyError(f"{key} is not a valid key for {cls.__name__}")

    @classmethod
    def default(cls):
        """
        Returns the default value of the Enum.

         Returns:
            BaseEnum, None: Returns the enum member marked as default (is_default=True),
                            or None if no member is set as default.

        Example:
            BaseEnum.default()
        """
        # Find and return the default enum member
        for member in cls:
            if hasattr(member, 'is_default') and member.is_default:
                return member
        return None  # If no default is marked, return None or consider raising an error


def enum_factory(name, base_enum: EnumBase, **new_members):
    """
    Create a new enum or extend an existing enum with new members.

    Args:
        name (str): The name of the new enum class
        base_enum (EnumBase): Optional base enum to extend
        new_members: Additional or new members to include

    Example:
        ExtendedColorEnum = enum_factory('ExtendedColorEnum', ColorEnum, ORANGE='orange')
    """
    members = {item.name: item.value for item in base_enum}
    members.update(new_members)
    return Enum(name, members)
