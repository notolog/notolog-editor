"""
Notolog Editor
Open-source markdown editor developed in Python.

File Details:
- Purpose: Password object class to store password-related data.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""


class EncPassword:

    def __init__(self):
        self._password = None
        self._hint = None

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def hint(self):
        return self._hint

    @hint.setter
    def hint(self, value):
        self._hint = value

    def is_valid(self):
        if self._password is None:
            return False
        if len(self._password) < 8:
            return False
        return True
