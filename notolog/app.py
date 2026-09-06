"""
Notolog Editor
An open-source Markdown editor built with Python.

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
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""


import argparse
import logging
import asyncio
import sys
import os

from PySide6.QtCore import QLoggingCategory
from PySide6.QtWidgets import QStyleFactory

from notolog.app_config import AppConfig
from notolog.font_loader import FontLoader

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
        class NotologArgumentParser(argparse.ArgumentParser):
            def print_help(self, file=None):
                # Default command line intro
                grey, white, green, reset = ('', '', '', '') if sys.platform == 'win32' else (
                    '\033[90m', '\033[97m', '\033[92m', '\033[0m')
                print(grey, end='')
                print("░░░░░░░░░░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓███"
                      f"{white} NOTOLOG {grey}"
                      "███▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░░░░░░")
                print(green, end='')
                print("╔═══════════════════════════════════════════════════════════════════════════════════════════╗")
                print("║ Notolog Editor is a GUI application. Simply run the command without any options to start. ║")
                print("╚═══════════════════════════════════════════════════════════════════════════════════════════╝")
                print(reset)
                # Call the super method to print the standard help message
                super().print_help()

        # Create the parser
        parser = NotologArgumentParser(description="Notolog Editor: An open-source Markdown editor built with Python.")

        # Add a version argument
        parser.add_argument('-v', '--version', action='version',
                            version=f'{AppConfig().get_app_name()} {AppConfig().get_app_version()}',
                            help='show the version information and exit')

        # Parse the arguments
        # parser.parse_args()
        args = parser.parse_args()

        # Check if the --init=package option was provided
        if args.version:
            pass

        sys.exit(0)

    """
    Possible params:
    filename='notolog.log'
    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s'
    """
    logger_level = AppConfig().get_logger_level()
    logging.basicConfig(level=logger_level, format='[%(name)s] %(funcName)s: %(levelname)s: %(message)s')

    logger = logging.getLogger('notolog')

    logger.info("%s v%s" % (AppConfig().get_app_name(), AppConfig().get_app_version()))
    logger.info("%s" % (AppConfig().get_app_license()))

    if logger_level > logging.DEBUG:
        # Suppress font-related messages in the logs
        QLoggingCategory.setFilterRules("qt.qpa.fonts=false")

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

    # E.g. /usr/bin and /usr/bin/python3.11
    logger.debug(f'Application dir path "{app.applicationDirPath()}"; file path "{app.applicationFilePath()}"')

    # Init the application fonts
    FontLoader.init_fonts(app)

    # Get the screen to pass it to the main module
    screen = app.screens()[0]

    # Main loop
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    editor = None
    startup_error = None

    def start_editor():
        nonlocal editor, startup_error
        try:
            # Initialize the editor once qasync is running.
            editor = NotologEditor(screen=screen)
            editor.show()
        except BaseException as exc:
            startup_error = exc
            app.quit()

    try:
        with loop:
            # Qt owns loop termination; awaiting aboutToQuit races with dispatcher shutdown.
            loop.call_soon(start_editor)
            loop.run_forever()

            if startup_error is not None:
                raise startup_error
    finally:
        asyncio.set_event_loop(None)


if __name__ == '__main__':
    # Debug:
    # async def main(): ...
    # asyncio.run(main(), debug=True)
    main()
