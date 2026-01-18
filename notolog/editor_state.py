"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Manages text editor state, such as View and Edit modes, content source, and data encryption status.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

import logging

from enum import Enum

# from PyQt6.QtCore import pyqtSignal as Signal, QObject
from PySide6.QtCore import Signal, QObject


class Mode(Enum):
    VIEW = 1  # Default
    EDIT = 2
    SOURCE = 3  # View result source code


class Source(Enum):
    MARKDOWN = 1
    HTML = 2  # Default


class Encryption(Enum):
    PLAIN = 0  # Default
    ENCRYPTED = 1


class EditorState(QObject):
    value_changed = Signal(object)

    def __init__(self, parent=None):
        super(EditorState, self).__init__(parent)

        self.logger = logging.getLogger('editor_state')

        self._mode = None
        self._source = None
        self._encryption = None

        # Previous values for switching back purposes
        self._prev_mode = None
        self._prev_source = None

        # Dialog answer of either to allow to save an empty file or not
        self._allow_save_empty = None

    @property
    def mode(self):
        return self._mode

    @property
    def prev_mode(self):
        return self._prev_mode

    @property
    def source(self):
        return self._source

    @property
    def prev_source(self):
        return self._prev_source

    @property
    def encryption(self):
        return self._encryption

    @property
    def allow_save_empty(self):
        return self._allow_save_empty

    @mode.setter
    def mode(self, value):
        self._prev_mode = self._mode  # Save previous state
        self._mode = value
        """
        c - context
        v - value
        pv - previous value
        """
        self.value_changed.emit({'c': Mode, 'v': value, 'pv': self._prev_mode})  # type: ignore

    @source.setter
    def source(self, value):
        self._prev_source = self._source  # Save previous state
        self._source = value
        self.value_changed.emit({'c': Source, 'v': value, 'pv': self._prev_source})  # type: ignore

    @encryption.setter
    def encryption(self, value):
        self._encryption = value
        self.value_changed.emit({'c': Encryption, 'v': value})  # type: ignore

    @allow_save_empty.setter
    def allow_save_empty(self, value):
        self._allow_save_empty = value

    def refresh(self):
        # To refresh UI upon settings update or at similar situations
        self.mode = self._mode
        self.source = self._source
        self.encryption = self._encryption

    def allow_save_empty_reset(self):
        # Allows to show dialog again
        self._allow_save_empty = None

    def toggle_mode(self):
        """
        Switch between VIEW and EDIT modes to maintain actual state.
        """

        self.logger.debug('Toggle mode %s' % self.mode)

        """
        Switch by this scheme:
        * Mode.SOURCE > Previous mode
        * Mode.EDIT > Mode.VIEW
        * Mode.VIEW > Mode.EDIT

        Mode SOURCE uses the same UI to show the data as VIEW mode.
        """
        if self.mode == Mode.SOURCE:
            """
            Remember the previous state whether it's the mode or source is only relevant for the changed parameter.
            For example: the actual mode is SOURCE, and the previous mode is VIEW. Hence, the parameter was changed.
            However, the previous source MARKDOWN may be unrelated to the previous mode VIEW,
            because of hasn't been changed after the mode switching.
            """
            self.mode = (self.prev_mode if self.prev_mode and self.prev_mode != Mode.SOURCE
                         else (Mode.EDIT if self.source == Source.MARKDOWN else Mode.VIEW))
        elif self.mode == Mode.VIEW:
            self.mode = Mode.EDIT
            self.source = Source.MARKDOWN
        else:
            self.mode = Mode.VIEW
            self.source = Source.HTML
            # To do not count previous answer if edit mode was switched once
            self.allow_save_empty_reset()

        self.logger.debug("Toggled mode to '%s', source to '%s'; previous states are '%s' and '%s' correspondingly"
                          % (self.mode, self.source, self.prev_mode, self.prev_source))
