"""
Helper for file operations
"""

from PySide6.QtCore import QFile, QDir

import os
import sys

from typing import Union


def res_path(rel_path):
    # Get absolute path for resources which works either for dev and for build
    try:
        # PyInstaller creates a temporary folder and store its path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # base_path = os.path.abspath(".")
        base_path = os.path.abspath(QDir.currentPath())

    return os.path.join(base_path, rel_path)


def size_f(size: int, suffix: str="B") -> str:
    """
    Human-readable file/content size
    @param size: size in bytes
    @param suffix: suffix at the end of the formatted string
    @return: formatted string of file size
    """
    units = ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]
    unit_size = 1024.0
    i = 0
    while abs(size) >= unit_size and i < len(units) - 1:
        size /= unit_size
        i += 1
    return f"{round(size, 1)}{units[i]}{suffix}"


def read_file(file_path: str, b: bool=False) -> Union[str, bytearray]:
    """
    Read file content
    @param file_path: file path string
    @param b: as a bytearray
    @return: file content either as a string, bytearray or None

    # Qt implementation could be like
    file = QFile(file_path)
    if file.open(QIODevice.OpenModeFlag.ReadOnly):
        # file.size()
        return file.readAll()
    """
    # a bytes-like object or string
    mode = 'rb' if b else 'r'
    # without 3-char extension: file_path[:-4]
    with open(file_path, mode) if b else open(file_path, mode, encoding='utf-8') as file:  # No encoding in bin mode
        return file.read()


def save_file(file_path: str, data: Union[str, bytearray], b: bool=False) -> bool:
    """
    Save content to the file
    @param file_path: file path string
    @param data: file content either as a string or bytearray
    @param b: as a bytearray
    @return: boolean result
    """
    # a bytes-like object or string
    mode = 'wb' if b else 'w'
    # without 3-char extension: crypted_file_path[:-4]
    with open(file_path, mode) if b else open(file_path, mode, encoding='utf-8') as file:  # No encoding in bin mode
        file.write(data)
        return True


def remove_trailing_numbers(text) -> str:
    """
    Remove trailing numbers from text, mostly file extension with incremental digital addon.
    @param text: text to remove trailing digits from
    @return: string without trailing digits if they are exist
    """
    # Start from the end of the string and find the first non-digit character
    i = len(text)
    while i > 0 and text[i - 1].isdigit():
        i -= 1
    # Return the string up to the first trailing digit
    return text[:i]