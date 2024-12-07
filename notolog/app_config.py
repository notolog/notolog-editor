from PySide6.QtCore import QObject, QStandardPaths, Signal

import os
import tomli
import tomli_w
import logging
import shutil

from notolog.app_package import AppPackage

from typing import Union
from threading import Lock

toml_base_app_config = """
[app]
name = "Notolog"
version = "1.0.7"
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

[package]
type = ""
"""


class AppConfig(QObject):
    """
    App configuration to share between app's objects.
    """

    _instance = None  # Singleton instance
    _lock = Lock()

    value_changed = Signal(dict)  # type: Signal[dict]

    default_package = AppPackage().default_package

    def __new__(cls, *args, **kwargs):
        # Overriding __new__ to control the instantiation process
        if not cls._instance:
            with cls._lock:
                # Create the instance if it doesn't exist
                cls._instance = super(AppConfig, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        # Prevent re-initialization if the instance is already set up.
        if hasattr(self, 'base_app_config'):
            return

        # Ensure that the initialization check and the setting of base_app_config are atomic.
        with self._lock:
            # Double-check to prevent race conditions during initialization.
            if hasattr(self, 'base_app_config'):
                return

            # Initialize the QObject part only once
            super(AppConfig, self).__init__()

            self.logger = logging.getLogger('app_config')

            # Config variables
            self.base_app_config = None  # type: Union[dict, None]
            self.toml_file_path = None  # type: Union[str, None]
            self.app_config = None  # type: Union[dict, None]

            # Font settings
            self._font_size = None  # Base value
            self._prev_font_size = None  # Previous value

            # For pytest to allow override some params
            self._test_mode = False

            # Initialize
            self.load_initial_conf()

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
        """
        Method to get app config file path which is depends on the app package type stored in the 'package' file.
        The method can be called before the actual package type if the 'package' file yet not exists in some cases.

        Package file purpose to distinguish the actual installation whither through pip, deb or similar packages.
        This approach allows to keep app config and it's settings separately from each other.

        returns: str path to the config file stored in a preferred system location (QStandardPaths.ApplicationsLocation).
        """

        # Get the standard configuration path
        config_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.ApplicationsLocation)

        try:
            # Ensure the config directory exists
            os.makedirs(config_dir, exist_ok=True)
        except OSError as e:
            # Handle specific errors, e.g., permission errors
            self.logger.warning(f"Error: Unable to create directory '{config_dir}'; error occurred {e}")

        # Suffix for testing to avoid modifying the real configuration
        file_name_suffix = '_qa' if self.get_test_mode() else ''

        # Add package type suffix if it's not the default
        app_package = self.get_package_type()
        if app_package != self.default_package:
            file_name_suffix += f'_{app_package}'

        # Get complete app_config.toml file path
        config_path = os.path.join(
            config_dir,
            f'notolog_app_config{file_name_suffix}.toml'
        )

        # For compatibility with previous versions, clone config from the previous location
        if not os.path.exists(config_path):
            # Get this file dir path
            script_dir = os.path.dirname(os.path.realpath(__file__))
            prev_conf_path = os.path.join(os.path.dirname(script_dir), 'app_config.toml')
            if os.path.exists(prev_conf_path):
                # Copy previous version of the config to the new one
                shutil.copy(prev_conf_path, config_path)
                # Delete previous file
                os.remove(prev_conf_path)

        return config_path

    @staticmethod
    def get_base_app_config():
        return tomli.loads(toml_base_app_config)

    @staticmethod
    def get_default_app_config():
        return tomli.loads(toml_app_config)

    def get_config(self):
        return self.app_config

    def load_config(self, config_file_path) -> Union[dict, None]:
        if not (os.path.exists(config_file_path) and os.access(config_file_path, os.R_OK)):
            return None
        try:
            # Read from the actual app_config.toml file
            with open(config_file_path, 'r') as config_file:
                return tomli.loads(config_file.read())
        except FileNotFoundError:
            self.logger.warning(f"The configuration file '{config_file_path}' was not found.")
        except PermissionError:
            self.logger.warning(f"Permission denied while accessing the file '{config_file_path}'.")
        except tomli.TOMLDecodeError:
            self.logger.warning(f"Error decoding TOML from the file '{config_file_path}'.")
        except Exception as e:
            self.logger.warning(f"An unexpected error occurred while loading the config: {e}")
        return None

    def load_initial_conf(self):
        # Clear stored data if set
        self.app_config = {}

        # Get base config
        self.base_app_config = self.get_base_app_config()

        # Load the default configuration schema from a TOML string
        self.app_config = self.get_default_app_config()

        # Load package config to update the configuration file if needed
        app_config_package = AppPackage().get_config()
        if not AppPackage().validate_config(app_config_package):
            # self.logger.warning(f"Package config contains unsupported data '{str(app_config_package)[:255]}' or missing.")
            pass
        else:
            # Merge the existing package config into the default one
            self.app_config.update(app_config_package)

        # Get the current app config file path (it might have just been updated)
        self.toml_file_path = self.get_app_config_path()

        # In case the config file is missing
        if not os.path.exists(self.toml_file_path) and os.access(os.path.dirname(self.toml_file_path), os.W_OK):
            # Create the config.
            self.save_app_config()

        stored_app_config = self.load_config(self.toml_file_path)
        # Check if existing config is available
        if self.validate_config(stored_app_config):
            # Merge the existing app config into the default one
            self.app_config.update(stored_app_config)
            if ('package' in self.app_config
                    and 'package' in app_config_package
                    and self.app_config['package'] != app_config_package['package']):
                # Such discrepancy can possibly occur for various reasons
                self.logger.warning(f"The configuration file package {self.app_config['package']} "
                                    f"and {app_config_package['package']} are differ.")
                # Merge the package config into the combined one again to restore
                self.app_config.update(app_config_package)

        # Font settings
        self._font_size = self.app_config['font']['base_size']  # Base value
        self._prev_font_size = self.app_config['font']['base_size']  # Previous value

    def delete_app_config(self) -> bool:
        """
        Attempts to delete configuration file if it exists and is writable.

        Returns:
            bool: True if the file was successfully deleted, False otherwise.
        """

        # Check if file exists and is writable
        if os.path.exists(self.toml_file_path) and os.access(self.toml_file_path, os.W_OK):
            try:
                os.remove(self.toml_file_path)
                self.toml_file_path = None
                return True
            except OSError as e:
                if self.logging:
                    self.logger.warning(f"Error deleting configuration file {self.toml_file_path}: {e}")
                return False
        else:
            if self.logging:
                self.logger.warning(f"Configuration file does not exist or is not writable: {self.toml_file_path}")
            return False

    def save_app_config(self):
        try:
            # Regenerate the app_config.toml file with new settings
            with open(self.toml_file_path, 'wb') as f:
                f.write(toml_app_config_header.encode('utf-8'))
                tomli_w.dump(self.app_config, f)
        except PermissionError:
            self.logger.warning(f"Permission denied: Cannot write to the file {self.toml_file_path}.")
        except IOError as e:
            self.logger.warning(f"Failed to write config to file {self.toml_file_path}: {e}")
        except Exception as e:
            self.logger.warning(f"An unexpected error occurred: {e}")

    def app_config_update_handler(self, data: dict) -> None:
        # Data contains information about the changes made
        if self.debug:
            self.logger.debug('App config handler is in use "%s"' % data)

        # Save the current config
        self.save_app_config()

    def setup_package(self, app_package) -> None:
        # Validate package
        if not AppPackage().validate_type(app_package):
            self.logger.warning(
                f"Trying to setup unsupported package '{str(app_package)[:16]}'; "
                f"fallback to the default package '{self.default_package}'")
            app_package = self.default_package

        # Save default config
        AppPackage().set_type(app_package)

        # Reinitialize the updated config and its path
        self.load_initial_conf()

        # Block signals
        was_blocked = self.blockSignals(True)

        # Verify the initial setup and update the config
        self.save_app_config()

        # Restore signals
        self.blockSignals(was_blocked)

    def validate_config(self, app_config):
        return all(key in app_config for key in self.get_default_app_config())

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

    def set_package_type(self, value) -> None:
        self.app_config['package']['type'] = value
        self.value_changed.emit({'package_type': value})

    def get_package_type(self) -> str:
        """
        Retrieves the package type specified in the app's configuration.
        If no package is found, the method returns `self.default_package` as a fallback.

        Returns:
            str: The package name or `self.default_package` if no package is found.
        """

        package = None
        if self.app_config and 'package' in self.app_config and 'type' in self.app_config['package']:
            package = self.app_config['package']['type']

        # Return the package
        return package if package else self.default_package

    """
    Class system variables.
    Do not emit signals upon their update.
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
