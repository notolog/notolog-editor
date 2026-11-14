"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Shares keyboard bindings between the editor and its Workspace reference.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtGui import QKeySequence


SHORTCUTS = (
    ('save', QKeySequence.StandardKey.Save),
    ('find', QKeySequence.StandardKey.Find),
    ('goto', 'Ctrl+G'),
    ('unindent', 'Shift+Tab'),
    ('newline', 'Shift+Return'),
    ('undo', QKeySequence.StandardKey.Undo),
    ('redo', QKeySequence.StandardKey.Redo),
    ('cut', QKeySequence.StandardKey.Cut),
    ('copy', QKeySequence.StandardKey.Copy),
    ('paste', QKeySequence.StandardKey.Paste),
    ('select_all', QKeySequence.StandardKey.SelectAll),
)


def shortcut_keys(name):
    """Return every native binding, or the portable custom key sequence."""
    key = dict(SHORTCUTS)[name]
    return [QKeySequence(key)] if isinstance(key, str) else QKeySequence.keyBindings(key)
