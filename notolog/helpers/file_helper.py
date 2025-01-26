"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Helper class for file operations.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2025 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import QDir

import os
import sys
import logging

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


def can_access_file(file_path: str, mode: str) -> bool:
    """
    Check if the file is accessible with the specified mode.

    Args:
        file_path (str): The path to the file.
        mode (str): The mode to check ('r' for read, 'w' for write).

    Returns:
        bool: True if the file is accessible with the specified mode, False otherwise.
    """
    if mode == 'r':
        return file_path and os.path.isfile(file_path) and os.access(file_path, os.R_OK)
    elif mode == 'w':
        dir_path = os.path.dirname(file_path) or '.'
        return os.access(file_path, os.W_OK) if file_path and os.path.isfile(file_path) else os.access(dir_path, os.W_OK)
    return False


def read_file(file_path: str, as_bytearray: bool = False) -> Union[str, bytearray, None]:
    """
    Read file content from the specified path.

    Args:
        file_path (str): The path to the file.
        as_bytearray (bool): If True, returns the content as a bytearray;
            if False, returns the content as a string. Defaults to False.

    Returns:
        Union[str, bytearray, None]: Returns the file content as a string or bytearray,
                                     or None if the file cannot be read.
    """
    if not can_access_file(file_path, 'r'):
        return None

    """
    # Qt implementation could be like
    file = QFile(file_path)
    if file.open(QIODevice.OpenModeFlag.ReadOnly):
        # file.size()
        return file.readAll()
    """

    mode = 'rb' if as_bytearray else 'r'
    try:
        with open(file_path, mode, encoding=None if as_bytearray else 'utf-8') as file:
            return file.read()
    except (OSError, IOError) as e:
        logger = logging.getLogger("file_helper")
        logger.warning(f"Error reading file {file_path}: {e}")
        return None


def save_file(file_path: str, data: Union[str, bytearray], as_bytearray: bool = False) -> bool:
    """
    Save content to the specified file.

    Args:
        file_path (str): The path to the file where content will be saved.
        data (Union[str, bytearray]): The content to save.
        as_bytearray (bool): If True, saves the content as a bytearray;
                             otherwise saves it as a string. Defaults to False.

    Returns:
        bool: True if the content was successfully saved, False otherwise.
    """
    if not can_access_file(file_path, 'w'):
        return False

    # a bytes-like object or string
    mode = 'wb' if as_bytearray else 'w'
    try:
        with open(file_path, mode, encoding=None if as_bytearray else 'utf-8') as file:
            file.write(data)
            return True
    except (OSError, IOError) as e:
        logger = logging.getLogger("file_helper")
        logger.warning(f"Error saving file {file_path}: {e}")
        return False


def is_file_openable(file_path: str) -> bool:
    """
    Check if a file is openable.

    Args:
        file_path (str): The path to the file.

    Returns:
        bool: True if the file can be opened, False otherwise.
    """
    if not can_access_file(file_path, 'r'):
        return False
    try:
        with open(file_path, 'r'):
            pass
        return True
    except (OSError, IOError) as e:
        logger = logging.getLogger("file_helper")
        logger.warning(f"Error opening file {file_path}: {e}")
        return False


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


def is_writable_path(file_path):
    # Check if file exists and if it's writable
    if os.path.exists(file_path):
        if not os.access(file_path, os.W_OK):
            return False
    else:
        # Check if the directory is writable if the file doesn't exist
        parent_dir = os.path.dirname(file_path)
        if not os.access(parent_dir, os.W_OK):
            return False
    return True
