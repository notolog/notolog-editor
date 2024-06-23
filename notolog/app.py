"""
Notolog Editor
Open-source markdown editor developed in Python.

File Details:
- Purpose: Main file to start up the app and set up an async loop.
- Functionality: This file is the main entry point for the Notolog app. It handles the initialization of the
  application environment, processes command line arguments, and starts the main application loop.

Detailed Description:
- Initializes the GUI by calling the main module.
- Sets up global logging and debug settings.
- Initializes the async loop.

Usage:
Run the module directly from the command line with the necessary arguments:
`python -m notolog.app`

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""


import logging
import asyncio
import sys
import os

from PySide6.QtWidgets import QStyleFactory

from notolog.app_config import AppConfig

# Force Qt API (for qasync).
# It's necessary to set the QT_API environment variable before importing qasync
# because the library uses this environment variable to determine which Qt binding to use.
os.environ["QT_API"] = "PySide6"

from notolog.notolog_editor import NotologEditor  # noqa

from qasync import QEventLoop, QApplication  # noqa

# Force Qt style override
os.environ["QT_STYLE_OVERRIDE"] = "Fusion"


def main():
    # Check if any command line arguments are present
    if len(sys.argv) > 1:
        if any(arg.lower() in ('--version', '-v') for arg in sys.argv):
            print(f'{AppConfig().get_app_name()} {AppConfig().get_app_version()}')
        else:
            print("░░░░░░░░░░░░░░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓███■███▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░░░░░░░░")
            print("╔═══════════════════════════════════════════════════════════════════════════════════════════╗")
            print("║ Notolog Editor is a GUI application. Simply run the command without any options to start. ║")
            print("╚═══════════════════════════════════════════════════════════════════════════════════════════╝")
        sys.exit(0)

    """
    Possible params:
    filename='notolog.log'
    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s'
    """
    logging.basicConfig(level=logging.DEBUG, format='[%(name)s] %(funcName)s: %(levelname)s: %(message)s')

    # Enable logging, uncomment or change app config
    # AppConfig().set_logging(True)
    # Enable debug mode (a lot of logs), uncomment or change app config
    # AppConfig().set_debug(False)

    logger = logging.getLogger('notolog')
    if AppConfig().get_logging():
        logger.info("%s v%s" % (AppConfig().get_app_name(), AppConfig().get_app_version()))
        logger.info("%s" % (AppConfig().get_app_license()))

    # Main application
    app = QApplication(sys.argv)
    # To correctly set up app settings
    app.setOrganizationName(AppConfig().get_settings_org_name())
    app.setOrganizationDomain(AppConfig().get_settings_org_domain())
    # Consider different app names for pip package and for the source files run,
    # as the settings storage depends on it.
    app.setApplicationName(AppConfig().get_settings_app_name())
    app.setApplicationVersion(AppConfig().get_app_version())

    # Custom styling may not render as expected with these themes.
    """
    # Detect the operating system to choose the style
    current_os = platform.system()
    if current_os == "Windows":
        app.setStyle(QStyleFactory.create("WindowsVista"))
    elif current_os == "Darwin":  # macOS
        app.setStyle(QStyleFactory.create("Macintosh"))
    else:  # Or: current_os == "Linux"
    """
    app.setStyle(QStyleFactory.create("Fusion"))  # Fusion is a cross-platform choice

    # Maintain a unique style regardless of the user's system settings
    app.setDesktopSettingsAware(False)

    if AppConfig().get_debug():
        # E.g. /usr/bin and /usr/bin/python3.11
        logger.debug(f'Application dir path "{app.applicationDirPath()}"; file path "{app.applicationFilePath()}"')

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
    # Debug:
    # async def main(): ...
    # asyncio.run(main(), debug=True)
    main()
