"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Contains unit and integration tests for the related functionality.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

import atexit
import os
from pathlib import Path
import shutil
import tempfile

import pytest

# Configure Qt and all user-scoped storage before importing PySide6. Tests must
# never read or modify real application data.
_test_profile = Path(tempfile.mkdtemp(prefix='notolog-tests-'))
for directory in ('config', 'data', 'appdata', 'localappdata', 'settings'):
    (_test_profile / directory).mkdir()
os.environ['HOME'] = str(_test_profile)
os.environ['XDG_CONFIG_HOME'] = str(_test_profile / 'config')
os.environ['XDG_DATA_HOME'] = str(_test_profile / 'data')
os.environ['APPDATA'] = str(_test_profile / 'appdata')
os.environ['LOCALAPPDATA'] = str(_test_profile / 'localappdata')
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
os.environ['ORT_DISABLE_TELEMETRY'] = '1'
atexit.register(shutil.rmtree, _test_profile, ignore_errors=True)

from PySide6.QtCore import QCoreApplication, QSettings  # noqa: E402

from notolog.app_config import AppConfig  # noqa: E402

QSettings.setPath(
    QSettings.Format.IniFormat,
    QSettings.Scope.UserScope,
    str(_test_profile / 'settings'),
)


@pytest.fixture(autouse=True)
def test_core_app():

    # To correctly set up app settings
    QCoreApplication.setOrganizationName(AppConfig().get_settings_org_name())
    QCoreApplication.setApplicationName(AppConfig().get_settings_app_name_qa())

    AppConfig().set_test_mode(True)

    yield None
