import os
import tomli

toml_base_app_config = """
[app]
name = "Notolog"
version = "0.9.1b0"
license = "MIT"
date = "2024"
website = "https://notolog.app"
repository = "https://github.com/notolog/notolog-editor"
pypi = "https://pypi.org/project/notolog"
author = "Vadim Bakhrenkov"

[repository]

    [repository.github]
    username = "notolog"
    project = "notolog-editor"
    release_url = "https://api.github.com/repos/notolog/notolog-editor/releases/latest"
    bug_report_url = "https://github.com/notolog/notolog-editor/issues"
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
"""


class AppConfig:
    """
    App configuration to share between app's objects.
    """

    base_app_config = tomli.loads(toml_base_app_config)

    # Get this file dir path
    script_dir = os.path.dirname(os.path.realpath(__file__))
    # Get parent dir path
    parent_dir = os.path.dirname(script_dir)
    # Get app_config.toml file path which is located at parent dir
    toml_file_path = os.path.join(parent_dir, 'app_config.toml')

    if not os.path.exists(toml_file_path):
        # Backup option
        app_config = tomli.loads(toml_app_config)
    else:
        # Read actual app_config.toml
        with open(toml_file_path, 'r') as config_file:
            app_config = tomli.loads(config_file.read())

    # Font settings
    _font_size = app_config['font']['base_size']  # Base value
    _prev_font_size = app_config['font']['base_size']  # Previous value

    # For pytest to allow override some params
    _test_mode = False

    """
    Constant values with getters.
    """

    @classmethod
    def get_app_name(cls) -> str:
        return cls.base_app_config['app']['name']

    @classmethod
    def get_app_version(cls) -> str:
        return cls.base_app_config['app']['version']

    @classmethod
    def get_app_license(cls) -> str:
        return cls.base_app_config['app']['license']

    @classmethod
    def get_app_date(cls) -> str:
        return cls.base_app_config['app']['date']

    @classmethod
    def get_app_website(cls) -> str:
        return cls.base_app_config['app']['website']

    @classmethod
    def get_app_repository(cls) -> str:
        return cls.base_app_config['app']['repository']

    @classmethod
    def get_app_pypi(cls) -> str:
        return cls.base_app_config['app']['pypi']

    @classmethod
    def get_app_author(cls) -> str:
        return cls.base_app_config['app']['author']

    @classmethod
    def get_repository_github_username(cls) -> str:
        return cls.base_app_config['repository']['github']['username']

    @classmethod
    def get_repository_github_project(cls) -> str:
        return cls.base_app_config['repository']['github']['username']

    @classmethod
    def get_repository_github_release_url(cls) -> str:
        return cls.base_app_config['repository']['github']['release_url']

    @classmethod
    def get_repository_github_bug_report_url(cls) -> str:
        return cls.base_app_config['repository']['github']['bug_report_url']

    @classmethod
    def get_font_base_size(cls) -> int:
        return cls.app_config['font']['base_size']

    """
    Methods with setter to override default value.
    """

    @classmethod
    def set_logging(cls, value) -> None:
        cls.app_config['logger']['logging'] = value

    @classmethod
    def get_logging(cls) -> bool:
        return cls.app_config['logger']['logging']

    @classmethod
    def set_debug(cls, value) -> None:
        cls.app_config['logger']['debug'] = value

    @classmethod
    def get_debug(cls) -> bool:
        return cls.app_config['logger']['debug']

    @classmethod
    def set_font_min_size(cls, value) -> None:
        cls.app_config['font']['min_size'] = value

    @classmethod
    def get_font_min_size(cls) -> int:
        return cls.app_config['font']['min_size']

    @classmethod
    def set_font_max_size(cls, value) -> None:
        cls.app_config['font']['max_size'] = value

    @classmethod
    def get_font_max_size(cls) -> int:
        return cls.app_config['font']['max_size']

    """
    Class system variables
    """

    @classmethod
    def set_font_size(cls, value) -> None:
        cls._font_size = value

    @classmethod
    def get_font_size(cls) -> int:
        return cls._font_size

    @classmethod
    def set_prev_font_size(cls, value) -> None:
        cls._prev_font_size = value

    @classmethod
    def get_prev_font_size(cls) -> int:
        return cls._prev_font_size

    @classmethod
    def set_test_mode(cls, value) -> None:
        cls._test_mode = value

    @classmethod
    def get_test_mode(cls) -> bool:
        return cls._test_mode
