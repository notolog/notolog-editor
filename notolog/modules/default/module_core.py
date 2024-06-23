"""
Notolog Editor
Open-source markdown editor developed in Python.

File Details:
- Purpose: Part of the default module.
- Functionality: Facilitates access to the module's API functions.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

import logging

from ..base_core import BaseCore

from .. import Settings
from .. import AppConfig


class ModuleCore(BaseCore):

    module_name = 'Default Module'

    # Functionality extended by the module.
    extensions = []

    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent

        self.settings = Settings(parent=self)

        self.logger = logging.getLogger('default_module')

        self.logging = AppConfig().get_logging()
        self.debug = AppConfig().get_debug()

        if self.logging:
            self.logger.info(f'Module {__name__} loaded')

    @staticmethod
    def get_lexemes_path():
        return None
