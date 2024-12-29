# Changelog
All notologable changes to this project will be documented in this file.

## [1.0.9] - 2024-12-29

### Added
- Added tests for the 'Module llama.cpp' model helper class.

### Changed
- Made the `llama-cpp-python` package optional, allowing it to be installed separately on top of the base installation. When installed, it will automatically enable the 'Module llama.cpp' in the application settings.

### Updated
- Modified the `pyproject.toml` file to support optional package installation and set the maximum supported Python version to `<3.14`.

### Fixed
- Resolved a potential error when `logging.getLevelNamesMapping` was unavailable in Python versions below 3.11.

## [1.0.8] - 2024-12-08

### Updated
- Refactored the logging strategy by moving the logger level to the app config and removing redundant checks to simplify the code. Default logging level is now set to `logging.INFO`.
- Updated the model initialization process for 'Module llama.cpp', now allowing the model name to be retrieved from the model's metadata if available.
- The 'OpenAI API' and 'On Device LLM' modules now only consider the 'Maximum Response Tokens' setting if its value is greater than zero; otherwise, the model utilizes its full context window.

### Fixed
- Fixed an issue where entering text directly into one QSpinBox field on a settings tab would inadvertently change the values in all QSpinBox fields on the same tab. This issue was caused by specific event handling in the QSpinBox and its internal QLineEdit components.

## [1.0.7] - 2024-12-07

### Added
- Added the 'Module llama.cpp' to the AI Assistant to support the GGUF model format and inference capabilities. This module utilizes the `llama-cpp-python` package, which provides Python bindings for `llama.cpp`.
- Added text hints to the settings dialog labels to help distinguish the fields, providing quick notes on their purpose.
- Added more tests, particularly for AI Assistant modules and their prompt managers.
- Added new lexemes and updated existing ones to support release changes.

### Changed
- Renamed `AiMessageLabel` to `AIMessageLabel` to match the `AIAssistant` class name convention.
- Changed the location of the `AppPackage` config file to the app's root directory.

### Updated
- Refactored the settings dialog to enable scrolling through tab content and to expand the set of adjustable fields for AI Assistant modules.
- Updated the prompt managers in AI Assistant modules to enhance performance and improve user interactions.
- Enhanced the message copying functionality in the AI Assistant window by ensuring that text is checked for Markdown conversion when needed and is appropriately handled.
- Set the minimum token count to zero for the 'OpenAI API' and 'On Device LLM' modules.
- Adjusted dependency specification constraints in `pyproject.toml` to enhance compatibility.

### Fixed
- Fixed missing link color properties that were defaulting to the default styles of the 'Nocturne', 'Dark Noir', and 'Spooky' themes.

## [1.0.6] - 2024-11-24

### Added
- Introduced the `AppPackage` class to distinguish different sources of app code installations.
- Added a 'Temperature' slider to both the 'On Device LLM' and 'OpenAI API' modules, and a 'Maximum Response Tokens' field to the 'On Device LLM' module.
- Added support for ONNX Runtime GenAI 0.5.1 on macOS, along with numpy 2.1.0 or newer, compatible with Python versions 3.10 to 3.12.
- Added the `argparse` package to process CLI arguments in `app.py`.
- Added the 'on_value_change' callback to handle object value changes within the settings UI, event parameters include the object itself and source widget.
- Added 'ai_assistant_status_icon_color' parameter to the color management to set the loading icon color in the AI Assistant and adjusted corresponding themes.

### Changed
- Settings now depend on the app package type, allowing different installation types to function independently. A new app config parameter 'package' was added.
- Changed the location of the app config TOML file, which now automatically imports settings from a previous installation once, if they weren't set before.
- Modified app config checks to merge base data and validate the configuration, falling back to default values if any required parameter is unset or invalid.
- Changed the warning message about the missing file header to a debug message as it may be a valid situation.

### Updated
- Updated project dependencies: `Markdown` to version 3.7, the `emoji` library to version 2.14.0, and the `cffi` package to version 1.17.0.
- Optimized the settings file path retrieval based on the actual package set.
- Enhanced the line numbers area by adding extra background fill and reducing padding between the edit widget's edges and the line numbers widget.
- Improved various tests and implemented a quiet mode for testing UI elements without interruptions.
- Updated lexemes related to the app's corresponding changes.
- The content in code blocks in edit mode now uses monospace formatting to preview the result's style.
- Updated the README.md with information about app features, refined other texts, and updated the UI example images.

### Fixed
- Fixed collapsible/expandable blocks behavior where reopening of a collapsed block might produce duplicated text artifacts.
- Addressed a potential logger message issue in `AppConfig` related to missing `self.logging`.
- Fixed an issue where an unchanged file was attempted to be saved without write permissions. Similar fixes were made regarding the app config file and when creating the 'images' resource directory.
- Fixed the blockquote color for the 'Calligraphy' theme.

## [1.0.5] - 2024-11-03

### Added
- Added a check to allow saving an opened file if the file no longer exists but directory permissions permit saving.
- Added an exit confirmation dialog for cases where the file cannot be saved due to a lack of write permissions.
- Added test cases for saving active files to cover crucial functionality and emulate permission checks, as well as to validate overall expected behavior.
- Added a new color setting, 'ai_assistant_button_icon_color', for AI Assistant button icons.
- Added a rejected dialog callback for the `CommonDialog` class.
- Added a callback for the app's `message_box()` method.
- Added corresponding lexeme translations.

### Changed
- Removed `PySide6` and `PySide6_Addons` packages from the dependencies, retaining `PySide6_Essentials` to streamline installation. To keep the working environment clean, please remove them using `pip uninstall -y pyside6 pyside6-addons`.
- Made minor adjustments to the About popup for the Nocturne, Dark Noir, and Spooky themes, along with other tweaks.

### Updated
- Updated active line number highlighting in edit mode to align with line height and handle word-wrapped blocks that span multiple lines.
- Improved the waiting indicator for the OpenAI API module during requests and updated related tests.
- Enhanced processing of `QNetworkReply` where applicable.
- Revised permission checks for the app's configuration file.
- Updated corresponding tests.

### Fixed
- Fixed a potential issue with the update check that could lead to a sudden app closing event.
- Fixed an issue with file permission checks for existing files when saving content.
- Fixed a background reset issue for line numbers that could occur after line changes in word-wrapped blocks when working in edit mode.

## [1.0.4] - 2024-10-27

### Added
- Introduced the 'Spooky' theme to celebrate the Halloween season with its vivid colors.

### Updated
- Upgraded the `PySide6` package dependencies to support the installation of the most recent versions.
- Extended support for Python 3.13 to ensure compatibility with the latest Python releases.
- Updated README.md to include a description of the 'Spooky' theme.
- Updated lexemes to reflect recent changes.

### Fixed
- Fixed an issue with creating new files due to incorrect directory permission checks.
- Resolved potential issues with the 'css_format' parameter when creating new themes.

## [1.0.3] - 2024-10-06

### Changed
- Renamed lexeme key from 'search_case_sensitive_label' to 'search_case_sensitive_accessible_name' within the 'toolbar' lexeme scope.

### Updated
- Updated the search form to feature a case-sensitive button that is highlighted based on its state, replacing the previous checkbox and labels.
- Moved search form buttons' configurations to the `SearchForm` class and refactored search button event handling.
- Enhanced the README.md file with detailed information on color schemes and other minor updates.

### Fixed
- Fixed the font size for the settings dialog close button.

## [1.0.2] - 2024-09-29

### Added
- Added the index of searched text occurrences within the document, alongside the count of such occurrences. This enhancement provides more detailed search results and helps users locate text more precisely.

### Changed
- Extracted SearchForm from the ToolBar class into a separate file and updated relevant lexeme names for case-sensitive search.

### Updated
- Updated themes to enhance the document's search field, ensuring compatibility with the new functionality.
- Upgraded the `cryptography` package dependency from version '42.0.7' to '43.0.1' or later to incorporate the latest security improvements.
- Updated tests, particularly for the ToolBar and SearchForm classes.

### Fixed
- Adjusted the searched occurrence counter to respond to the case-sensitive search checkbox for accurate results.

## [1.0.1] - 2024-09-15

### Added
- Count occurrences of searched text within a document, display the count in the search field, and enable/disable navigation buttons accordingly.
- Added `get_by_scope()` method to the `Lexemes` class to retrieve all lexemes related to a particular scope.

### Changed
- Renamed the lexeme key from 'md_background_color_blockquote_friendly' to 'md_background_color_blockquote_inner', which contains the background color value for inner elements within a blockquote.

### Updated
- Modules tabs now respond to language changes in settings by reloading the `settings_dialog` scope.
- Updated the 'Nocturne' theme styles (comments, blockquote inner elements background, and the selected tree element style), along with minor tweaks to other themes.
- Updated tests related to the `Lexemes` class functionality.

### Fixed
- Fixed an issue where the Esc-key hidden AI Assistant dialog did not reopen after clicking its button.
- Fixed markdown highlighting for header tags when the header content contains emojis.
- Fixed the potential font size shift of the settings tab widget when changing themes.
- Fixed the persisted code block background color in an open document when changing themes in the settings.

## [1.0.0] - 2024-09-01

### Added
- New dark theme 'Nocturne' for nighttime coders.

### Fixed
- Fixed the issue with updating settings group titles during interactive language changes.
- Resolved `pytest` warning regarding the default fixture loop scope in `asyncio`.

### Changed
- Updated the approach for assigning styles to settings group titles.

## [0.9.9] - 2024-08-18

### Added
- Notolog is now available for installation via Conda Forge. Installation instructions and a version badge have been added to the `README.md` file.
- Introduced the ability to create a new directory from the file tree context menu.

### Changed
- Adjusted palette highlight colors (e.g., selection, search, context menu active background) for the 'Default' and 'Noir Dark' themes.

### Fixed
- The tree filter now returns to the initial directory in the file tree when the filter text is cleared using the backspace key.

## [0.9.8] - 2024-08-04

### Added
- Added the ability to copy the file path from the file tree context menu.
- Added 'gpt-4o-mini' and 'gpt-4-turbo' to the list of supported models in the OpenAI API module.

### Updated
- Updated the URL for new version notifications to point to the latest version page.
- Hid status bar warnings in Edit Mode, as the warnings are now relevant only in View Mode.

## [0.9.7] - 2024-07-14

### Added
- Added a warning label to the status bar to indicate mismatches between `<details>` blocks' open and close tags.

### Updated
- Enhanced the processing of collapsible blocks with several updates:
  - Inserted a zero-width space before expandable anchor tags to prevent continuous anchor sequences.
  - Preserved 'class' attributes and other properties when processing `<details>` and `<summary>` tags.
  - Included the block's summary within the QUrl fragment for better linkage.
  - Updated corresponding UI styles for consistency and visual integration.

### Fixed
- Improved handling of nested expandable/collapsible blocks at the same level.
- Corrected an issue where clicking on the very first character of an expanded block would misplace the expansion.

## [0.9.6] - 2024-06-30

### Added
- Added Markdown to HTML conversion within the expandable blocks.

### Changed
- Highlighted '@todo' token even if there is no space after it but before the end of the line.

### Updated
- Updated translations for the AI Assistant and related functionalities, including the On Device LLM module.

### Fixed
- Fixed a missing tooltip when copying messages from the AI Assistant dialog.
- Fixed an issue where a button in the AI Assistant could become stuck if the request exceeded the length limit. Also added more service messages within the AI Assistant to address potential errors.

## [0.9.5] - 2024-06-23

### Added
- Added `pyproject.toml` file to support the modern way of building packages.
- Added a development and test tools installation script that gets data directly from `pyproject.toml`.
- Added a button to send requests and stop inference for the AI Assistant.

### Changed
- Renamed `main.py` to `app.py` to allow running the app with the `python -m notolog.app` command.
- The application has been tested with less strict dependencies, using version ranges to ensure compatibility and flexibility.

### Updated
- Updated `README.md` with current and additional information about dev tools installation, and other changed parts.

### Fixed
- Fixed building the wheel on the Windows platform.
- Added `QT_API` environment variable to fix Windows CLI run.

## [0.9.5b1] - 2024-06-16

### Added
- Modular functionality with extendable settings and lexemes.
- Introduced the 'On Device LLM' module using ONNX Runtime GenAI, enabling local, CPU-optimized versions of LLMs like Phi-3 without requiring internet access. Added two new packages, `onnxruntime_genai` and `numpy`, to support this feature. Supported systems include Linux and Windows (support for macOS is in progress).

### Changed
- Transformed the OpenAI API into a dedicated module.
- Moved descriptions of third-party packages and their licenses to the `ThirdPartyNotices.md` file from the README.md.

### Updated
- Enhanced the AI Assistant to support multi-turn conversations with optional 'no memory' requests, improved token count management, and added a stop button functionality to halt inference.
- Enabled saving of the entire AI Assistant conversation; individual messages can now be copied to the clipboard as well.
- Implemented caching of settings, which can be reset via the main menu.

### Fixed
- Resolved an issue where the code block background color was indiscernible in the Dark Noir theme.
- Corrected anchors processing for headers using the 'toc' (Table of Contents) markdown extension.

## [0.9.1b8] - 2024-05-25

### Added
- Added `typing_extensions` package, which is also automatically installed with the `emoji` package.
- New tests and test-related updates, particularly complex async tests for `ImageDownloader`.

### Updated
- Updated the following packages to their latest versions: `PySide6` (including `PySide6_Addons` and `PySide6_Essentials`) to version 6.7.1, `pytest` to version 8.2.1, `pytest-asyncio` to version 0.23.7, `cffi` to version 1.17.0rc1, and `emoji` to version 2.12.1.
- Added processing for the Shift + Enter keyboard combination to avoid soft line breaks, which may alter the perception of how soft line breaks function.
- Updated the package's `setup.py` to include supported languages and additional package information.
- Updated the functionality for getting and storing protected fields in settings, including refactoring and error fixes (re-setup of corresponding values may be required).
- Updated `AppConfig` with additional settings-related options.
- Various `Flake8` linter fixes to ensure the code meets the PEP 8 style guide, along with McCabe complexity updates (current complexity check level is 15).
- Updated and optimized the content of the `README.md` file to enhance the sections on third-party components, and tests-related topics.

### Changed
- Slightly reduced the await time for the async highlighter to make the editing mode more responsive to changes involved in syntax highlighting (experimental).
- Improved the error-proofing of async queue processing upon app closing, particularly if background processes like highlighting or others are still in progress.

### Fixed
- Fixed an issue where resources might be downloaded twice.
- Resolved a problem with the toolbar context menu being unresponsive.

## [0.9.1b5] - 2024-05-19

### Added
- Introduced a GitHub workflow for tests, incorporating Flake8 and pytest coverage reports to maintain high standards of code quality and ensure comprehensive test coverage.
- Added the app's organization name, app name, and version to facilitate correct settings storage.
- Added a media directory to the app_config.toml.
- App settings now support encrypted values to keep sensitive data, like API keys, secure. The encryption key is generated once and stored in the app config file. A Settings helper class was also added.
- New tomli_w package added to support TOML-file writing.

### Updated
- Tests updated to support multi-platform execution.
- Used `os.sep` to ensure correct path separators on each OS and `os.path.normpath()` to normalize path separators.
- Updated the description and disclaimers text in README.md; added a "Code Quality and Test Coverage" paragraph.

### Changed
- Changed the approach to not create a resource directory upfront before any file is available to save.
- Moved async highlighter functionality to a dedicated file.
- Adjusted links markdown highlighter to allow highlighting web links within lines of markdown blocks, and adjusted the web links regex accordingly.
- Refined the AppConfig object to implement the singleton pattern, enabling it to automatically generate the app's config file rather than relying on a predefined version.

### Fixed
- Fixed a potential error in the image downloader when the property is None upon canceling tasks on exiting the app.
- Updated the resource folder path according to the currently active file.

## [0.9.1b4] - 2024-05-12

### Added
- Introduced the pytest-asyncio package to support testing of asyncio code with pytest, enhancing the robustness and reliability of unit tests.
- Added the `.gitattributes` file that was previously omitted to ensure consistent Git configurations across various environments.

### Updated
- Improved the processing and completion of tasks in the asynchronous syntax highlighter, enhancing efficiency and stability.
- Expanded the `.gitignore` file with additional entries to better manage the files included in version control, such as ignoring more temporary files and build artifacts.

## [0.9.1b3] - 2024-05-11

### Added
- Introduced the CODE_OF_CONDUCT.md file to promote a respectful and positive environment for all contributors and participants. This document outlines our commitment to providing a harassment-free experience for everyone and offers guidelines for respectful communication practices.
- Support for highlighting tables in markdown edit mode, enhancing the editing experience.
- A new EnumBase class to incorporate common methods across enums, improving code reusability.
- Additional tests to increase coverage and ensure the stability of new features.

### Changed
- Renamed the main package directory from app to notolog and moved main.py into the notolog directory to better reflect the project structure.
- Refined the handling of external and local links, as well as local files, now routing them through a unified links router for improved security and consistency.
- Updated the table styles in view mode across all themes for more consistent visual presentation.
- Eliminated the need for a preliminary empty line to highlight lists in markdown edit mode, enhancing the user experience by simplifying text formatting.

### Updated
- Enhanced the language selection mechanism to prefer the system language by default, with a fallback to a predefined language if the system language is not available.
- Optimized the checking of image downloader statuses and the updating of signal processing for increased performance and reliability.

### Fixed
- Corrected the processing for confirming external links to eliminate unintended navigational behaviors and enhance user security.
- Various minor fixes to address small issues in the codebase, enhancing stability and performance without significantly changing functionality.

## [0.9.1b1] - 2024-05-06

### Added
- New interface language: Dutch

### Updated
- Upgraded `cryptography` to version 42.0.7 to align with the latest standards and enhance security.

### Changed
- Updated requirements.txt to match the actual package list.

## [0.9.1b0] - 2024-05-05

### Added
- New interface languages: Finnish and Swedish, expanding accessibility for users in these regions.
- Additional entries to the `.gitignore` and `.gitattributes` files to improve version control practices.
- A dedicated `app_config.toml` file with initial configuration parameters, simplifying initial setup and customization.

### Updated
- Updated the `Libraries and Licenses` section within the README.md file to provide comprehensive information about third-party dependencies and their licenses.
- Updated `cryptography` to version 42.0.6 and `Pygments` to version 2.18.0 to ensure compatibility with the latest standards and to incorporate the newest features and security enhancements.

### Changed
- Modified file handling: The file header can now be the only content of the file, streamlining setups where minimal data is required.
- Updated encryption description to clarify that Fernet uses AES-128 for encryption, derived from a 256-bit key, accurately reflecting the cryptographic standards employed.

## [0.9.0b11] - 2024-05-04

### Added
- Support for embedding external images within documents, with caching.
- Option to auto-save downloaded image resources on local disk and reuse them in subsequent document sessions.
- New interface languages: Greek, Hindi, Turkish.
- Expanded example content and resources.
- Added `CHANGELOG.md` to document all notable changes to the project, enhancing transparency and trackability for developers and users alike.

### Updated
- Updated pytest to version 8.2.0 to take advantage of improved test suite performance and new features. (Previously listed under "Changed")

### Changed
- Updated pip installer related packages and file structure.
- Current directory now persists during file events, even if no files are actively open.
- Minor logo adjustment.

### Fixed
- Resolved sudden crashes when switching between edit and view modes.
- Addressed UI style issues for improved text visibility under various color schemes.

## [0.9.0b10] - 2024-04-29

### Changed
- Updated pip installer related packages and file structure.

### Fixed
- Corrected startup failures following pip installation.

## [0.9.0b0] - 2024-04-29

### Added
- Initial release features, open sourced under the MIT license for full transparency and collaboration.
- Markdown syntax highlighting:
    - Editor mode offers smooth highlighting tailored specifically for Notolog by our development team, including line numbers and extended syntax highlighting.
    - View mode utilizes the Python Markdown library for seamless rendering of Markdown syntax.
    - Supports multi-line block open-close tokens for enhanced readability and structure.
- Multi-platform support: Compatible with all major platforms where Python is installed, ensuring accessibility across operating systems.
- Accessible features:
    - Clear and accessible descriptions for enhanced usability.
    - Font size adjustment for better readability.
- Background and cross-action save changes experience:
    - Automatically saves changes in the background to ensure data integrity and minimize user intervention.
    - Seamlessly handles unsaved changes when performing cross-actions, providing a smooth user experience.
- Search functionality:
    - Enables users to search within the opened file.
    - Quick search by file name within the tree for efficient navigation and content retrieval.
- File meta-headers in the form of HTML comments to avoid excess visibility.
- Password-based file symmetric encryption and decryption:
    - Utilizes AES-256 in CBC (Cipher Block Chaining) mode with secure key management via PBKDF2HMAC employing SHA-256, provided by the Fernet library.
    - File meta-headers keep encryption parameters for seamless decryption processes.
- Translations-friendly file structure:
    - Supports several languages out of the box, with provisions for adding and supporting additional languages.
- Color themes support:
    - Includes predefined color themes for customizing the editor's appearance in both light and dark modes.
- Hotkeys support:
    - Supports essential hotkeys like Ctrl+S for saving and Ctrl+F for searching, with plans for further expansion.
- In-line context menus:
    - Right-click context menu options in the file tree for file rename and delete actions.
    - Customizable toolbar with right-click functionality to show/hide icons based on user preferences.
- A suite of unit tests to ensure code reliability and maintainability, providing confidence in the editor's functionality.
- AI Assistant UI integrated with the OpenAI API, with plans to extend support to other providers.
