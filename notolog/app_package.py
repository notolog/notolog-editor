from PySide6.QtCore import QObject

import os
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
    default_file_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),  # Get this file's dir path
        'package_config.toml'
    )

    def __new__(cls, *args, **kwargs):
        # Overriding __new__ to control the instantiation process
        if not cls._instance:
            with cls._lock:
                # Create the instance if it doesn't exist
                cls._instance = super(AppPackage, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        # Check if instance is already initialized
        if hasattr(self, 'initialized'):
            return

        # Ensure that the initialization check and the setting of base_app_config are atomic.
        with self._lock:
            # This prevents race conditions.
            if hasattr(self, 'initialized'):
                return

            # Initialize the QObject part only once
            super(AppPackage, self).__init__()

            self.logger = logging.getLogger('app_package')

            self.initialized = True

    def validate_config(self, package_config) -> bool:
        return ('package' in package_config
                and 'type' in package_config['package']
                and self.validate_type(package_config['package']['type']))

    def validate_type(self, package_type):
        return package_type in self.supported_packages()

    def get_config(self) -> dict:
        try:
            # Read from the package file
            with open(self.default_file_path, 'r') as default_file:
                return tomli.loads(default_file.read())
        except FileNotFoundError:
            pass
        except PermissionError:
            self.logger.warning(f"Permission denied when accessing the default package file '{self.default_file_path}'.")
        return {}

    def set_config(self, package_config):
        if not self.validate_config(package_config):
            return
        try:
            # Write to the package file
            with open(self.default_file_path, 'wb') as default_file:
                tomli_w.dump(package_config, default_file)
        except FileNotFoundError:
            self.logger.warning(f"Cannot create a file '{self.default_file_path}' in a non-existent directory.")
        except PermissionError:
            self.logger.warning(f"Permission denied while accessing the default package file '{self.default_file_path}'.")

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
