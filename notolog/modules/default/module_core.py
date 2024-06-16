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
