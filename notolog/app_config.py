from typing import Union

import tomli

toml_app_config = """
[app]
name = "Notolog"
version = "0.9.0b0"
license = "MIT"
date = "2024"
website = "https://notolog.app"
repository = "https://github.com/notolog/notolog-editor"

[repository]

    [repository.github]
    username = "notolog"
    project = "editor"
    release_url = "https://api.github.com/repos/notolog/notolog-editor/releases/latest"
    bug_report_url = "https://github.com/notolog/notolog-editor/issues"

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

    app_config = tomli.loads(toml_app_config)

    # Font settings
    _font_size = app_config['font']['base_size']  # Base value
    _prev_font_size = app_config['font']['base_size']  # Previous value

    """
    Constant values with getters.
    """

    @classmethod
    def get_app_name(cls) -> str:
        return cls.app_config['app']['name']

    @classmethod
    def get_app_version(cls) -> str:
        return cls.app_config['app']['version']

    @classmethod
    def get_app_license(cls) -> str:
        return cls.app_config['app']['license']

    @classmethod
    def get_app_date(cls) -> str:
        return cls.app_config['app']['date']

    @classmethod
    def get_app_website(cls) -> str:
        return cls.app_config['app']['website']

    @classmethod
    def get_repository_github_username(cls) -> str:
        return cls.app_config['repository']['github']['username']

    @classmethod
    def get_repository_github_project(cls) -> str:
        return cls.app_config['repository']['github']['username']

    @classmethod
    def get_repository_github_release_url(cls) -> str:
        return cls.app_config['repository']['github']['release_url']

    @classmethod
    def get_repository_github_bug_report_url(cls) -> str:
        return cls.app_config['repository']['github']['bug_report_url']

    @classmethod
    def get_font_base_size(cls) -> int:
        return cls.app_config['font']['base_size']

    @classmethod
    def get_app_repository(cls) -> str:
        return cls.app_config['app']['repository']

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
