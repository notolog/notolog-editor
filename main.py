"""
Notolog main file to start up the app and to set up an async loop.

This module is the main entry point for the Notolog app. It handles the initialization of the
application environment, processes command line arguments, and starts the main application loop.

Detailed Description:
- Initializes the GUI by calling the main module.
- Set up global logging and debug settings.
- Initializes the async loop.

Usage:
Run the module directly from the command line with the necessary arguments:
python3 main.py

GitHub Repository: https://github.com/notolog/notolog-editor

Author: Vadim Bakhrenkov
License: MIT License
"""

from PySide6.QtWidgets import QStyleFactory
from qasync import QEventLoop, QApplication

from notolog.app_config import AppConfig
from notolog.notolog_editor import NotologEditor

import platform
import logging
import asyncio
import sys


def main():
    """
    Possible params:
    filename='notolog.log'
    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s'
    """
    logging.basicConfig(level=logging.DEBUG, format='[%(name)s] %(funcName)s: %(levelname)s: %(message)s')

    # Enable logging
    AppConfig.set_logging(True)
    # Enable debug mode (a lot of logs)
    AppConfig.set_debug(False)

    # Main application
    app = QApplication(sys.argv)

    # Detect the operating system to choose the style
    current_os = platform.system()
    if current_os == "Windows":
        app.setStyle(QStyleFactory.create("WindowsVista"))
    # elif current_os == "Darwin":  # MacOS
    #    app.setStyle(QStyleFactory.create("Macintosh"))  # Renders not as expected
    else:  # Or: current_os == "Linux"
        app.setStyle(QStyleFactory.create("Fusion"))  # Fusion is a cross-platform choice

    # Maintain a unique style regardless of the user's system settings
    app.setDesktopSettingsAware(False)

    logging.getLogger('notolog').info('Application dir path "%s"' % QApplication.applicationDirPath())

    # Get the screen to pass it to the main module
    screen = app.screens()[0]

    # Main loop
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    app_close_event = asyncio.Event()
    app.aboutToQuit.connect(app_close_event.set)

    # Start up the editor
    editor = NotologEditor(screen=screen)
    editor.show()

    with loop:
        """
        Contains run_forever() which is contain app.exec(),
        No need to run sys.exit(app.exec()) in this case.
        """
        loop.run_until_complete(app_close_event.wait())


if __name__ == '__main__':
    main()
