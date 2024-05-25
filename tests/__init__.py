from PySide6.QtCore import QCoreApplication

from notolog.app_config import AppConfig

import os
import pytest

# For headless operation
os.environ["QT_QPA_PLATFORM"] = "offscreen"


@pytest.fixture(autouse=True)
def test_core_app():

    # To correctly set up app settings
    QCoreApplication.setOrganizationName(AppConfig().get_settings_org_name())
    QCoreApplication.setApplicationName(AppConfig().get_settings_app_name_qa())

    yield None
