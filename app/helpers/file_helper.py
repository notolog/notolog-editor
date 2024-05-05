"""
Helper for file operations.
"""

from PySide6.QtCore import QFile, QDir

import os
import sys

from typing import Union


def res_path(rel_path):
    """
    Generate an absolute path for resource files. This method accommodates environments
    both during development and after deployment using PyInstaller.

    The function tries to determine the base path set by PyInstaller, which stores it
    in the `_MEIPASS` attribute during the bundled application's runtime. If the application
    is not running as a PyInstaller bundle, it defaults to the current directory's absolute path.

    Args:
        rel_path (str): The relative path to the resource.

    Returns:
        str: The absolute path combined from the base path and the relative path.
    """
    try:
        # PyInstaller creates a temporary folder and store its path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # If running as a live Python script, not a bundled application
        base_path = os.path.abspath(QDir.currentPath())

    return os.path.join(base_path, rel_path)


def size_f(size: int, suffix: str = "B") -> str:
    """
    Convert a file size to human-readable form.

    Args:
        size (int): File size in bytes.
        suffix (str): Suffix for the size unit. Defaults to 'B' (bytes).

    Returns:
        str: Formatted string representing the file size in a human-readable form.
    """
    units = ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]
    unit_size = 1024.0
    i = 0
    while abs(size) >= unit_size and i < len(units) - 1:
        size /= unit_size
        i += 1
    return f"{round(size, 1)}{units[i]}{suffix}"


def read_file(file_path: str, as_bytearray: bool = False) -> Union[str, bytearray]:
    """
    Read file content from the specified path.

    Args:
        file_path (str): The path to the file.
        as_bytearray (bool): If True, returns the content as a bytearray;
            if False, returns the content as a string. Defaults to False.

    Returns:
        str or bytearray or None: Returns the file content as a string or bytearray depending on the value of `b`.
        Returns None if the file cannot be read.
    """

    """
    # Qt implementation could be like
    file = QFile(file_path)
    if file.open(QIODevice.OpenModeFlag.ReadOnly):
        # file.size()
        return file.readAll()
    """
    # a bytes-like object or string
    mode = 'rb' if as_bytearray else 'r'
    # without 3-char extension: file_path[:-4]
    with (open(file_path, mode) if as_bytearray
          else open(file_path, mode, encoding='utf-8') as file):  # No encoding in bin mode
        return file.read()


def save_file(file_path: str, data: Union[str, bytearray], as_bytearray: bool = False) -> bool:
    """
    Save content to the specified file.

    Args:
        file_path (str): The path to the file where content will be saved.
        data (str or bytearray): The content to save, which can be either a string or a bytearray.
        as_bytearray (bool): Indicates whether the data should be saved as a bytearray.
            If False and data is a bytearray, it will be converted to a string before saving.
            Defaults to False.

    Returns:
        bool: True if the content was successfully saved, False otherwise.
    """
    # a bytes-like object or string
    mode = 'wb' if as_bytearray else 'w'
    # without 3-char extension: crypted_file_path[:-4]
    with (open(file_path, mode) if as_bytearray
          else open(file_path, mode, encoding='utf-8') as file):  # No encoding in bin mode
        file.write(data)
        return True


def remove_trailing_numbers(text) -> str:
    """
    Remove trailing numbers from the given text. This is commonly used to strip incremental numeric suffixes from
    file names or extensions.

    Args:
        text (str): The text from which trailing digits will be removed.

    Returns:
        str: The text stripped of any trailing digits, if they exist.
    """
    # Start from the end of the string and find the first non-digit character
    i = len(text)
    while i > 0 and text[i - 1].isdigit():
        i -= 1
    # Return the string up to the first trailing digit
    return text[:i]