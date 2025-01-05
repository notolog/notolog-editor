"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Manages application package functionality.
- Functionality: Provides methods to initialize and manage the package configuration.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2025 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import QObject, QDir

import os
import sys
import logging
import tomli
import tomli_w

from typing import Union
from threading import Lock


class AppPackage(QObject):
    """
    App package configuration.
    """

    _instance = None  # Singleton instance
    _lock = Lock()

    default_package = 'pip'
    package_file_path = None

    def __new__(cls, *args, **kwargs):
        # Overriding __new__ to control the instantiation process
        if not cls._instance:
            with cls._lock:
                # Create the instance if it doesn't exist
                cls._instance = super(AppPackage, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        # Prevent re-initialization if the instance is already set up.
        if hasattr(self, 'initialized'):
            return

        # Ensure that the initialization check and the setting of base_app_config are atomic.
        with self._lock:
            # Double-check to prevent race conditions during initialization.
            if hasattr(self, 'initialized'):
                return

            # Initialize the QObject part only once
            super(AppPackage, self).__init__()

            self.logger = logging.getLogger('app_package')

            self.package_file_path = self.package_path('package_config.toml')

            self.initialized = True

    def package_path(self, rel_path=None):
        """
        Get an absolute path for the app files. This method accommodates both development and deployment environments,
        including those using PyInstaller.

        The function attempts to determine the base path set by PyInstaller, which stores it
        in the `_MEIPASS` attribute during the runtime of the bundled application. If the application
        is not running as a PyInstaller bundle, it defaults to the absolute path of the current directory.

        Args:
            rel_path (str): The relative path to the resource.

        Returns:
            str: The absolute path corresponding to the given relative path.
        """
        try:
            # PyInstaller creates a temporary folder and store its path in _MEIPASS
            package_path = sys._MEIPASS  # noqa
        except AttributeError:
            # If running as a live Python script, not a bundled application
            package_path = os.path.abspath(QDir.currentPath())

        if rel_path:
            return os.path.join(package_path, rel_path)

        return package_path

    def validate_config(self, package_config) -> bool:
        return ('package' in package_config
                and 'type' in package_config['package']
                and self.validate_type(package_config['package']['type']))

    def validate_type(self, package_type):
        return package_type in self.supported_packages()

    def get_config(self) -> dict:
        try:
            # Read from the package file
            with open(self.package_file_path, 'r') as package_file:
                return tomli.loads(package_file.read())
        except FileNotFoundError:
            pass
        except PermissionError:
            self.logger.warning(f"Permission denied when accessing the default package file '{self.package_file_path}'.")
        except tomli.TOMLDecodeError as e:
            self.logger.warning(f"Check the package file data '{self.package_file_path}': {e}")
        return {}

    def set_config(self, package_config):
        if not self.validate_config(package_config):
            return
        try:
            # Write to the package file
            with open(self.package_file_path, 'wb') as package_file:
                tomli_w.dump(package_config, package_file)
        except FileNotFoundError:
            self.logger.warning(f"Cannot create a file '{self.package_file_path}' in a non-existent directory.")
        except PermissionError:
            self.logger.warning(f"Permission denied while accessing the default package file '{self.package_file_path}'.")

    def get_type(self) -> Union[str, None]:
        package_config = self.get_config()
        return (package_config['package']['type']
                if 'package' in package_config and 'type' in package_config['package']
                else None)

    def set_type(self, package_type):
        if self.validate_type(package_type):
            self.set_config({'package': {'type': package_type}})

    def supported_packages(self) -> []:
        """
        Return a list of available package formats.
        """
        return [self.default_package, 'bin']
