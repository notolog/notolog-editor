"""
Notolog Editor
Open-source markdown editor developed in Python.

File Details:
- Purpose: Part of the base module.
- Functionality: Manages the loading of modules and performs integrity checks.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

import os
import logging
import importlib

from threading import Lock

from ..app_config import AppConfig


class Modules:

    _instance = None  # Singleton instance
    _lock = Lock()

    modules: dict = {}

    def __new__(cls, *args, **kwargs):
        # Overriding __new__ to control the instantiation process
        if not cls._instance:
            with cls._lock:
                # Create the instance if it doesn't exist
                cls._instance = super(Modules, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        # Check if instance is already initialized
        if hasattr(self, 'logger'):
            return

        # Ensure that the initialization check and the setting of 'modules' param are atomic.
        with self._lock:
            # This prevents race conditions.
            if hasattr(self, 'logger'):
                return

            # Initialize the QObject part only once
            super(Modules, self).__init__()

            self.logger = logging.getLogger('modules')

            self.logging = AppConfig().get_logging()
            self.debug = AppConfig().get_debug()

            self.modules = self.load_modules()

    def load_modules(self) -> dict:
        modules_dir = os.path.dirname(os.path.realpath(__file__))
        modules_list = {}
        for module_name in os.listdir(modules_dir):
            if module_name == '__pycache__':
                continue
            module_dir = os.path.join(modules_dir, module_name)
            if os.path.isdir(module_dir) and os.path.isfile(os.path.join(module_dir, 'module_core.py')):
                # Dynamically import a module
                module = self.import_module(module_name)
                # Check the module is available
                if hasattr(module, 'is_available') and module.is_available():
                    modules_list.update({module_name: module})
        return modules_list

    def get_by_extension(self, extension_name) -> list:
        # Get all modules match the extension name
        return [module for module in self.modules.values()
                if any(extension_name == _name for _name in module.ModuleCore.extensions)]

    def import_module(self, module_name):
        # Check imported module
        if hasattr(self, 'modules') and module_name in self.modules.keys():
            return self.modules.get(module_name)

        # Try to import module
        try:
            module = importlib.import_module(f'notolog.modules.{module_name}')
            if self.logging:
                self.logger.info(f"Module '{module_name}' has been imported.")
                self.modules.update({module_name: module})
            return module
        except ImportError as e:
            if self.logging:
                self.logger.error(f"Failed to import module: {e}")
            return None

    def create(self, module, class_name: str = 'ModuleCore', *args, **kwargs):
        try:
            class_ = getattr(module, class_name)
            instance = class_(*args, **kwargs)
            if self.logging:
                self.logger.info(f"Instance of '{module.__name__}.{class_name}' created.")
            return instance
        except AttributeError:
            if self.logging:
                self.logger.warning(f"Class '{module.__name__}.{class_name}' not found in the module.")
            return None
        except Exception as e:
            if self.logging:
                self.logger.error(f"Failed to create instance of '{module.__name__}.{class_name}': {e}")
            return None
