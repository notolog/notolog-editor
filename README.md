<!-- {"notolog.app": {"created": "2023-12-25 18:59:43.806614", "updated": "2024-05-19 23:29:34.439703"}} -->
# Notolog

![Notolog - Python Markdown Editor](https://raw.githubusercontent.com/notolog/notolog-editor/main/notolog/assets/notolog-example-image.png)

## Python Markdown Editor

[![PyPI - Version](https://img.shields.io/pypi/v/notolog)](https://pypi.org/project/notolog/) [![GitHub License](https://img.shields.io/github/license/notolog/notolog-editor)](https://github.com/notolog/notolog-editor/blob/master/LICENSE) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/notolog)](https://pypi.org/project/notolog/) [![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/notolog/notolog-editor/tests.yaml)](https://github.com/notolog/notolog-editor/actions/workflows/tests.yaml)

Notolog is an open-source markdown editor developed with Python and PySide6. Born from a personal endeavor to tackle daily programming challenges and deepen Python proficiency, Notolog serves as a proof-of-concept that seamlessly blends simplicity with functionality. It offers an intuitive user experience across various platforms, ensuring users can efficiently manage and edit markdown files with ease.

---

![Notolog UI example](https://raw.githubusercontent.com/notolog/notolog-editor/main/docs/notolog-ui-settings.png)


## Features

* Notolog is open-sourced under the MIT license, promoting full transparency and encouraging collaboration.
* Markdown syntax highlighting:
	* Editor mode offers smooth highlighting tailored specifically for Notolog, with line numbers and extended syntax highlighting.
	* View mode utilizes the Python Markdown library for seamless rendering of Markdown syntax.
	* Supports multi-line block open-close tokens for improved readability and structure.
* Multi-platform support: Compatible with all major platforms where Python is installed, ensuring accessibility across operating systems.
* Accessible features, including:
	* Clear and accessible descriptions for enhanced usability.
	* Font size adjustment for better readability.
* Background and cross-action save changes experience:
	* Automatically saves changes in the background to ensure data integrity and minimize user intervention.
	* Seamlessly handles unsaved changes when performing cross-actions, providing a smooth user experience.
* Search functionality:
	* Allows users to search within the opened file.
	* Quick search by file name within the tree, enabling efficient navigation and content retrieval.
* Password-based File Encryption and Decryption:
	* Utilizes Fernet for encryption, providing a secure and user-friendly method for symmetric (also known as "secret key") encryption.
	* Fernet employs AES-128 in CBC mode. Plans to introduce AES-256 in future updates are aimed at further enhancing security.
* File Meta-Headers:
	* Notolog employs file meta-headers to store encryption/decryption parameters and other essential file information.
	* To minimize visibility, these meta-headers are formatted as HTML comments.
* Translations-friendly file structure:
	* Supports several languages out of the box, with provisions for adding and supporting additional languages.
* Color themes support:
	* Comes with a few predefined color themes to customize the editor's appearance, for both light and dark modes.
* Hotkeys support:
	* It currently supports hotkeys like Ctrl+S for saving and Ctrl+F for searching, with plans for further expansion.
* In-line context menus:
	* Right-click context menu options in the file tree for file rename and delete actions.
	* Customizable toolbar with right-click functionality to show/hide icons based on user preferences.
* Includes a suite of unit tests to ensure code reliability and maintainability, providing confidence in the editor's functionality.
* AI Assistant UI to get all things you need in one place:
	* At the moment the OpenAI API is supported with plans to extend support with other providers.
* Notolog includes specialized highlighting for TODOs. Simply type '@todo something' to mark tasks, enhancing the ability to track and manage future plans efficiently.

There is no classical web engine integration to make overall package more lightweight and to achieve the best possible performance.


## Translations

The Notolog Editor supports several language translations out of the box. Here is the list of languages included alongside the default English translation:

* Chinese (Simplified)
* Dutch
* Finnish
* French
* Georgian
* German
* Greek
* Hindi
* Italian
* Japanese
* Korean
* Latin
* Portuguese
* Russian
* Spanish
* Swedish
* Turkish

Here's an example of what it looks like in the actual UI, featuring the lovely Strawberry theme and Japanese translation:

![Notolog UI translation example](https://raw.githubusercontent.com/notolog/notolog-editor/main/docs/notolog-ui-settings-strawberry-ja.png)

## Prerequisites

**Python 3.9 or higher installed on your system.**

Ensure Python 3.9 or higher is installed on your system. Visit [python.org](https://python.org) for more details.

Check the version of Python available with this command `python3 -V`.

**pip (Python package installer) should be available.**

You can check if pip is installed by running `pip --version` in your terminal/command prompt.

**Virtual Environment**

It is highly recommended to use as it helps avoid version conflicts and interference from other packages. Below is a description of how to set up a virtual environment on your machine.


## Installation

### Method 1: pip installer (Recommended)

```sh
pip install notolog
```

That's it! Starting the app is as simple as `notolog`.

To update to the latest version, use:
```sh
pip install --upgrade notolog
```

### Method 2: Python source code

0. Open Terminal.
1. Clone project's GitHub repository to get a latest version.
	* `git clone https://github.com/notolog/notolog-editor.git`
2. Navigate to the just cloned project's directory using the **cd** command.
3. Make sure the virtual environment is activated as it's a common practice to isolate project code (activation described below).
4. Simply run this command to set up project dependencies:

```sh
pip install -r requirements.txt
```

That's it! Starting the app is as simple as `python -m notolog.main` form the project's root directory.

<details>
<summary>Run tests</summary>

To run all available tests:
```sh
pytest
```

To run a particular file's tests:
```sh
pytest tests/test_notolog_editor.py
```
</details>

### Virtual Environments

The instructions below contain steps of how to set up **venv** virtual environment to run a Python app safely. Starting from Python 3.6 **venv** is a recommended way to create virtual environments. For more information check [Creation of virtual environments](https://docs.python.org/3/library/venv.html). Alternatively, you can execute the Notolog code and set up virtual environment with your favorite Python code editor.

#### Linux and macOS

##### Set Up Virtual Environment
1. Open Terminal.
2. Navigate to your project directory using the cd command.
3. Create a virtual environment by running `python3 -m venv notolog`. Replace **notolog** with the desired name for your virtual environment.

##### Activate Virtual Environment:
To activate the virtual environment, run:
```sh
source notolog/bin/activate
```

To deactivate environment just run this command:
```sh
deactivate
```

<details>
<summary>Install venv on Linux systems</summary>

While Python itself comes pre-installed on many Linux distributions, including Ubuntu, some distributions may not include the venv module by default. Therefore, you need to install it separately using the package manager before you can use it to create virtual environments.

**Ubuntu/Debian**

```sh
sudo apt-get update
sudo apt-get install python3-venv
```

**Fedora**

```sh
sudo dnf install python3-venv
```

**CentOS/RHEL**

```sh
sudo yum install python3-venv
```
</details>

#### Windows

##### Set Up Virtual Environment

1. Open Command Prompt or PowerShell.
2. Navigate to your project directory using the `cd` command.
3. Create a virtual environment by running `python -m venv notolog`. Replace **notolog** with the name you want to give to your virtual environment.

##### Activate Virtual Environment

To activate the virtual environment, run:
```
notolog\Scripts\activate
```
_Mind the environment name (**notolog** or any other selected before)._


## Contributing

If you encounter any issues or would like to contribute to the project, please don't hesitate to [open an issue](https://github.com/notolog/notolog-editor/issues) or submit a [pull request](https://github.com/notolog/notolog-editor/pulls) on the project's [GitHub page](https://github.com/notolog/notolog-editor).

## License

The Notolog project is licensed under the MIT License - see the [LICENSE](https://github.com/notolog/notolog-editor/blob/main/LICENSE) file for details.

## Third-Party Components

### Libraries and Licenses

This project utilizes numerous third-party libraries, each with its own licensing terms. Below is a detailed list of these libraries grouped by license type to help clarify what each license permits and requires. This categorization aids in ensuring compliance with legal terms for use, modification, and distribution of these software components.

#### GNU LGPLv3, GNU GPLv2, or Commercial License

- **Qt (open-source)**: Framework for graphical user interfaces and more. [Project Details](https://www.qt.io), [Qt Licensing](https://www.qt.io/licensing)
- **PySide6**: GUI creation with Qt6 in Python. [Project and License Details](https://pyside.org/), [PyPI](https://pypi.org/project/PySide6/)
- **PySide6_Addons**: Additional modules for PySide6. [Project and License Details](https://pyside.org/), [PyPI](https://pypi.org/project/PySide6-Addons/)
- **PySide6_Essentials**: Core libraries for PySide6. [Project and License Details](https://pyside.org/), [PyPI](https://pypi.org/project/PySide6-Essentials/)
- **shiboken6**: Binding generator for Qt framework. [Project and License Details](https://pyside.org/), [PyPI](https://pypi.org/project/shiboken6/)

#### MIT License

- **Bootstrap Icons**: Icons for UI elements. [Project Details](https://icons.getbootstrap.com/), [License Details](https://github.com/twbs/icons/blob/main/LICENSE)
- **pytest**: Used for unit testing. It provides powerful features like fixtures, assertions, and test parameterization to facilitate writing and running Python tests. [Project Details](https://pytest.org/), [License Details](https://docs.pytest.org/en/8.0.x/license.html)
- **pytest-mock**: Enhances pytest for unit tests by offering a simple interface to powerful mocking functionalities. [License Details](https://github.com/pytest-dev/pytest-mock/blob/main/LICENSE), [PyPI](https://pypi.org/project/pytest-mock/)
- **cffi**: Used for interfacing with C code. [License Details](https://github.com/python-cffi/cffi/blob/main/LICENSE), [PyPI](https://pypi.org/project/cffi/)
- **iniconfig**: For parsing and working with INI configuration files. [License Details](https://github.com/pytest-dev/iniconfig/blob/main/LICENSE), [PyPI](https://pypi.org/project/iniconfig/)
- **tomli**: A Python library used for parsing TOML configuration files effortlessly. [License Details](https://github.com/hukkin/tomli/blob/master/LICENSE), [PyPI](https://pypi.org/project/tomli/)
- **tomli_w**: A Python library used for writing TOML configuration files effortlessly. [License Details](https://github.com/hukkin/tomli-w/blob/master/LICENSE), [PyPI](https://pypi.org/project/tomli-w/)
- **pluggy**: For creating and managing plugin systems in Python applications. [License Details](https://github.com/pytest-dev/pluggy/blob/main/LICENSE), [PyPI](https://pypi.org/project/pluggy/)

#### BSD Licenses

- **Python-Markdown**: Markdown to HTML conversion. [Project Details](https://python-markdown.github.io/), [BSD 3-Clause License](https://github.com/Python-Markdown/markdown/blob/master/LICENSE.md)
- **Emoji library**: Converts emoji text-code to emojis. [New BSD License](https://github.com/carpedm20/emoji/blob/master/LICENSE.txt), [PyPI](https://pypi.org/project/emoji/)
- **qasync**: Async support for Python. [BSD 2-Clause "Simplified" License](https://github.com/CabbageDevelopment/qasync/blob/master/LICENSE), [PyPI](https://pypi.org/project/qasync/)
- **Pygments**: Syntax highlighting for programming languages. [Project Details](https://pygments.org/), [BSD 2-Clause "Simplified" License](https://github.com/pygments/pygments/blob/master/LICENSE)
- **click**: Used for creating command-line interfaces. [Project Details](https://palletsprojects.com/p/click/), [BSD-3-Clause License](https://click.palletsprojects.com/en/8.1.x/license/)
- **pycparser**: C code parser and for generating Abstract Syntax Trees (AST) in Python. [BSD 3-Clause License](https://github.com/eliben/pycparser/blob/main/LICENSE), [PyPI](https://pypi.org/project/pycparser/)

#### Apache License 2.0

- **pytest-asyncio**: A library that provides support for testing asyncio code with pytest. [License Details](https://github.com/pytest-dev/pytest-asyncio/blob/main/LICENSE) , [PyPI](https://pypi.org/project/pytest-asyncio/)

#### Other Dual Licensed

- **cryptography**: Provides cryptographic functions and primitives. [Apache License 2.0](https://github.com/pyca/cryptography/blob/main/LICENSE.APACHE) and [BSD 3-Clause License](https://github.com/pyca/cryptography/blob/main/LICENSE.BSD), [PyPI](https://pypi.org/project/cryptography/)
- **packaging**: Python package metadata and distribution utilities. [Apache License 2.0](https://github.com/pypa/packaging/blob/main/LICENSE.APACHE) and [BSD 2-Clause "Simplified" License](https://github.com/pypa/packaging/blob/main/LICENSE.BSD), [PyPI](https://pypi.org/project/packaging/)

#### Python Standard Library

- **asyncio**: Part of the Python standard library, licensed under the [Python Software Foundation License](https://docs.python.org/3/license.html#psf-license).

#### The Unlicense

- **Codehilite CSS Themes**: Base themes for code highlighting. [The Unlicense](https://github.com/richleland/pygments-css/blob/master/UNLICENSE.txt)

Please note that while the majority of this project is licensed under the MIT License, certain components may have different licensing terms. Always refer to the documentation of each library for detailed information about its license and terms of use.

### APIs

#### OpenAI API Disclaimer

**Disclaimer:** This project is independent and not affiliated with, endorsed by, or sponsored by OpenAI. The integration of the OpenAI API is provided on an "as is" basis, and the creators disclaim all liability for any misuse or consequences resulting from the use of the OpenAI API.

**Usage:** This project uses the OpenAI API to access AI assistant capabilities and enhance natural language processing. Users must provide their own OpenAI API keys and should refer to the [OpenAI API reference](https://platform.openai.com/docs/api-reference) for detailed usage guidelines.

**Responsibility:** Users are responsible for obtaining and managing their OpenAI API keys in compliance with OpenAI's terms of service.

**Security:** Users are expected to handle their API keys securely to avoid unauthorized access.

*This section was generated with the assistance of AI to ensure accurate and concise information regarding the use of the OpenAI API.*

## Security Disclaimer

This application is designed for educational purposes and offers security features through optional file encryption and protected application settings.

### Optional File Encryption

* **Encryption Details:** The application uses PBKDF2HMAC for key derivation and Fernet for encryption, utilizing AES-128 in CBC mode. Although the key material generated is 256 bits, only the first 128 bits (16 bytes) are used for encryption.
* **File Headers:** The encryption salt and iteration counts are stored unencrypted in the file's header. This approach is primarily intended for non-critical applications where data exposure has limited risk.
* **Strong Passwords:** Users are encouraged to use strong passwords to enhance the protection of their encrypted data.

### Protected Application Settings

* **Settings Encryption:** The application may encrypt sensitive data like API keys because these Qt app settings might otherwise be stored as open data. However, the encryption key used is stored on the PC and can be accessed by anyone with physical or user-level access to the computer. This could expose sensitive data to potential unauthorized access.

### General Information

* **Open Source:** This application is open-source and distributed under the MIT License. Users must comply with applicable laws and regulations when using this software.
* **Liability:** The developers disclaim any liability for misuse or legal non-compliance related to the use of this software.


## Code Quality and Test Coverage

To maintain high standards of code quality and ensure comprehensive test coverage, we use several tools:

- **Flake8**: A tool that enforces coding style and checks the quality of Python code by combining PyFlakes, pycodestyle, and McCabe's complexity checker. [MIT License](https://github.com/PyCQA/flake8/blob/main/LICENSE)
- **coverage**: Measures the effectiveness of tests by showing which parts of your code are being executed and which are not. [Apache License 2.0](https://github.com/nedbat/coveragepy/blob/master/LICENSE.txt)
- **pytest-cov**: A pytest plugin that provides test coverage reports, extending pytest to measure code coverage alongside running tests. [MIT License](https://github.com/pytest-dev/pytest-cov/blob/master/LICENSE)

These tools help us maintain a clean and reliable codebase by catching potential issues early and documenting where our tests might be lacking.

---
_This README.md file has been carefully crafted and edited using the Notolog editor itself._