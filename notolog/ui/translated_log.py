"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Bounded operation logs with translatable application messages and verbatim process output.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from collections import deque

from PySide6.QtCore import QSignalBlocker
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QPlainTextEdit


class TranslatedLog(QPlainTextEdit):
    MAX_CHARACTERS = 65536

    def __init__(self, translations, parent=None):
        super().__init__(parent)
        self.translations = translations
        self.entries = deque()
        self.setReadOnly(True)
        self.setMaximumBlockCount(200)
        translations.language_changed.connect(self.refresh_language)

    def entry_text(self, entry):
        key, values, raw = entry
        return self.translations.get(key, **values) + '\n' if key else raw

    def append_message(self, key, **values):
        self.append_entry((key, values, ''))

    def append_output(self, text):
        if not text:
            return
        self.append_entry((None, {}, text))

    def clear(self):
        self.entries.clear()
        super().clear()

    def append_entry(self, entry):
        text = self.entry_text(entry)
        if not entry[0] and self.entries and not self.entries[-1][0]:
            previous = self.entries.pop()[2]
            entry = (None, {}, previous + text)
        self.entries.append(entry)
        self.trim_entries()
        if self.document().characterCount() + len(text) > self.MAX_CHARACTERS:
            self.refresh_language()
            self.moveCursor(QTextCursor.MoveOperation.End)
            self.ensureCursorVisible()
            return
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText(text)
        self.setTextCursor(cursor)
        self.ensureCursorVisible()

    def trim_entries(self):
        remaining_lines = self.maximumBlockCount() - 1
        remaining_characters = self.MAX_CHARACTERS
        retained = deque()
        for entry in reversed(self.entries):
            text = self.entry_text(entry)
            if remaining_lines < 0 or not remaining_characters:
                break
            tail = '\n'.join(text.split('\n')[-(remaining_lines + 1):])[-remaining_characters:]
            if tail:
                retained.appendleft(entry if tail == text else (None, {}, tail))
            if tail != text:
                break
            remaining_lines -= tail.count('\n')
            remaining_characters -= len(tail)
        self.entries = retained

    def refresh_language(self):
        self.trim_entries()
        cursor = self.textCursor()
        anchor, position = cursor.anchor(), cursor.position()
        scroll = self.verticalScrollBar()
        value, at_end = scroll.value(), scroll.value() == scroll.maximum()
        with QSignalBlocker(self):
            self.setPlainText(''.join(self.entry_text(entry) for entry in self.entries))
            end = self.document().characterCount() - 1
            cursor = self.textCursor()
            cursor.setPosition(min(anchor, end))
            cursor.setPosition(min(position, end), QTextCursor.MoveMode.KeepAnchor)
            self.setTextCursor(cursor)
        scroll.setValue(scroll.maximum() if at_end else value)
