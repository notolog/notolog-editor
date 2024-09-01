"""
Notolog Editor
Open-source markdown editor developed in Python.

File Details:
- Purpose: Enum class for the app's supported themes.

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


class Themes(EnumBase):

    DEFAULT = ("Default", True)  # The second item in the tuple marks this as the default
    CALLIGRAPHY = "Calligraphy"
    NOIR_DARK = "Noir Dark"
    STRAWBERRY = "Strawberry"
    NOCTURNE = "Nocturne"
