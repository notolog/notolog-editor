from PySide6.QtCore import QObject, Signal

import os
import tomli
import tomli_w
import logging

from typing import Any
from threading import Lock

toml_base_app_config = """
[app]
name = "Notolog"
version = "1.0.5"
license = "MIT License"
date = "2024"
website = "https://notolog.app"
repository = "https://github.com/notolog/notolog-editor"
pypi = "https://pypi.org/project/notolog"
author = "Vadim Bakhrenkov"

[repository]

    [repository.github]
    username = "notolog"
    project = "notolog-editor"
    api_release_url = "https://api.github.com/repos/notolog/notolog-editor/releases/latest"
    release_url = "https://github.com/notolog/notolog-editor/releases/latest"
    bug_report_url = "https://github.com/notolog/notolog-editor/issues"

[settings]
org_name = "Notolog"
org_domain = "notolog.app"
app_name = "notolog_editor"
"""

toml_app_config_header = """# Notolog
# An open-source markdown editor developed in Python.

# Application-Level Configuration
# --------------------------------
# This section contains default configuration options for the application.
# These settings can be overridden programmatically at runtime.
#
# IMPORTANT:
# This file is auto-generated. Changes made to this file may be overwritten.
# To customize configuration safely, ensure modifications are done through
# the application's interface or according to the documented process.
#
# Modifying this file directly is not recommended as it could lead to
# unexpected behavior or loss of your settings upon the next auto-generation.\n
"""

# This is a fallback option if app_config.toml is not found
toml_app_config = """
[font]
base_size = 12
min_size = 5
max_size = 42

[logger]
logging = true
debug = false

[security]
app_secret = ""

[editor]
media_dir = "images"
"""


class AppConfig(QObject):
    """
    App configuration to share between app's objects.
    """

    _instance = None  # Singleton instance
    _lock = Lock()

    value_changed = Signal(dict)  # type: Signal[dict]

    def __new__(cls, *args, **kwargs):
        # Overriding __new__ to control the instantiation process
        if not cls._instance:
            with cls._lock:
                # Create the instance if it doesn't exist
                cls._instance = super(AppConfig, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        # Check if instance is already initialized
        if hasattr(self, 'base_app_config'):
            return

        # Ensure that the initialization check and the setting of base_app_config are atomic.
        with self._lock:
            # This prevents race conditions.
            if hasattr(self, 'base_app_config'):
                return

            # Initialize the QObject part only once
            super(AppConfig, self).__init__()

            # Config variables
            self.base_app_config = Any
            self.toml_file_path = Any
            self.app_config = Any

            # Font settings
            self._font_size = Any  # Base value
            self._prev_font_size = Any  # Previous value

            # For pytest to allow override some params
            self._test_mode = Any

            # Initialize
            self.load_initial_conf()

            self.logger = logging.getLogger('app_config')

            self.logging = self.get_logging()
            self.debug = self.get_debug()

            if self.debug:
                self.logger.info('App config is engaged')

            self.value_changed.connect(self.app_config_update_handler)

    @classmethod
    def get_instance(cls):
        # Class method to get the singleton instance
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_app_config_path(self):
        # Get this file dir path
        script_dir = os.path.dirname(os.path.realpath(__file__))
        # Get parent dir path
        parent_dir = os.path.dirname(script_dir)
        # Get app_config.toml file path which is located at parent dir
        return os.path.join(parent_dir, 'app_config.toml')

    def load_initial_conf(self):
        self.base_app_config = tomli.loads(toml_base_app_config)

        # Get app_config.toml file path
        self.toml_file_path = self.get_app_config_path()

        if not os.path.exists(self.toml_file_path):
            # Backup option
            self.app_config = tomli.loads(toml_app_config)
        else:
            try:
                # Read from the actual app_config.toml file
                with open(self.toml_file_path, 'r') as config_file:
                    self.app_config = tomli.loads(config_file.read())
            except FileNotFoundError:
                if self.logging:
                    self.logger.warning(f"The configuration file {self.toml_file_path} was not found.")
            except PermissionError:
                if self.logging:
                    self.logger.warning(f"Permission denied when accessing the file {self.toml_file_path}.")
            except tomli.TOMLDecodeError:
                if self.logging:
                    self.logger.warning(f"Error decoding TOML from the file {self.toml_file_path}.")
            except Exception as e:
                if self.logging:
                    self.logger.warning(f"An unexpected error occurred while loading the config: {str(e)}")

        # Font settings
        self._font_size = self.app_config['font']['base_size']  # Base value
        self._prev_font_size = self.app_config['font']['base_size']  # Previous value

        # For pytest to allow override some params
        self._test_mode = False

    def delete_app_config(self):
        if os.path.exists(self.toml_file_path):
            # Delete file
            os.remove(self.toml_file_path)

    def app_config_update_handler(self, data: dict) -> None:
        if self.debug:
            self.logger.debug('App config handler is in use "%s"' % data)

        try:
            # Regenerate the app_config.toml file with new settings
            with open(self.toml_file_path, 'wb') as f:
                f.write(toml_app_config_header.encode('utf-8'))
                tomli_w.dump(self.app_config, f)
        except PermissionError:
            if self.logging:
                self.logger.warning(f"Permission denied: Cannot write to the file {self.toml_file_path}.")
        except IOError as e:
            if self.logging:
                self.logger.warning(f"Failed to write config to file {self.toml_file_path}: {e}")
        except Exception as e:
            if self.logging:
                self.logger.warning(f"An unexpected error occurred: {e}")

    """
    Constant values with getters.
    """

    def get_app_name(self) -> str:
        return self.base_app_config['app']['name']

    def get_app_version(self) -> str:
        return self.base_app_config['app']['version']

    def get_app_license(self) -> str:
        return self.base_app_config['app']['license']

    def get_app_date(self) -> str:
        return self.base_app_config['app']['date']

    def get_app_website(self) -> str:
        return self.base_app_config['app']['website']

    def get_app_repository(self) -> str:
        return self.base_app_config['app']['repository']

    def get_app_pypi(self) -> str:
        return self.base_app_config['app']['pypi']

    def get_app_author(self) -> str:
        return self.base_app_config['app']['author']

    def get_repository_github_username(self) -> str:
        return self.base_app_config['repository']['github']['username']

    def get_repository_github_project(self) -> str:
        return self.base_app_config['repository']['github']['username']

    def get_repository_github_api_release_url(self) -> str:
        return self.base_app_config['repository']['github']['api_release_url']

    def get_repository_github_release_url(self) -> str:
        return self.base_app_config['repository']['github']['release_url']

    def get_repository_github_bug_report_url(self) -> str:
        return self.base_app_config['repository']['github']['bug_report_url']

    def get_settings_org_name(self) -> str:
        return self.base_app_config['settings']['org_name']

    def get_settings_org_domain(self) -> str:
        return self.base_app_config['settings']['org_domain']

    def get_settings_app_name(self) -> str:
        return self.base_app_config['settings']['app_name']

    def get_settings_app_name_qa(self) -> str:
        return f"{self.base_app_config['settings']['app_name']}_qa"

    def get_font_base_size(self) -> int:
        return self.app_config['font']['base_size']

    def get_editor_media_dir(self) -> str:
        return self.app_config['editor']['media_dir']

    """
    Methods with setter to override default value.
    """

    def set_logging(self, value) -> None:
        self.app_config['logger']['logging'] = value
        self.value_changed.emit({'logger_logging': value})

    def get_logging(self) -> bool:
        return self.app_config['logger']['logging']

    def set_debug(self, value) -> None:
        self.app_config['logger']['debug'] = value
        self.value_changed.emit({'logger_debug': value})

    def get_debug(self) -> bool:
        return self.app_config['logger']['debug']

    def set_font_min_size(self, value) -> None:
        self.app_config['font']['min_size'] = value
        self.value_changed.emit({'font_min_size': value})

    def get_font_min_size(self) -> int:
        return self.app_config['font']['min_size']

    def set_font_max_size(self, value) -> None:
        self.app_config['font']['max_size'] = value
        self.value_changed.emit({'font_max_size': value})

    def get_font_max_size(self) -> int:
        return self.app_config['font']['max_size']

    def set_security_app_secret(self, value) -> None:
        self.app_config['security']['app_secret'] = value
        self.value_changed.emit({'security_app_secret': value})

    def get_security_app_secret(self) -> str:
        return self.app_config['security']['app_secret']

    """
    Class system variables.
    Do not emit signal upon theirs update.
    """

    def set_font_size(self, value) -> None:
        self._font_size = value

    def get_font_size(self) -> int:
        return self._font_size

    def set_prev_font_size(self, value) -> None:
        self._prev_font_size = value

    def get_prev_font_size(self) -> int:
        return self._prev_font_size

    def set_test_mode(self, value) -> None:
        self._test_mode = value

    def get_test_mode(self) -> bool:
        return self._test_mode
