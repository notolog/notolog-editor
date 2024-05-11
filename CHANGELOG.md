# Changelog
All notologable changes to this project will be documented in this file.

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
