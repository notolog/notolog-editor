<!-- {"notolog.app": {"created": "2023-12-25 18:59:43.806614", "updated": "2024-05-11 11:15:29.656338"}} -->
# Notolog

![Notolog](https://raw.githubusercontent.com/notolog/notolog-editor/main/notolog/assets/notolog-example-image.png)&nbsp;&nbsp;&nbsp;![PyPI - Version](https://img.shields.io/pypi/v/notolog) ![PyPI - License](https://img.shields.io/pypi/l/notolog) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/notolog)

## Overview

Notolog is a versatile open-source markdown editor developed with Python and Qt, ideal for anyone looking for an efficient and straightforward way to handle markdown files. Born from a personal endeavor to address daily programming challenges and deepen Python proficiency, Notolog stands as a proof-of-concept that seamlessly integrates simplicity with functionality, offering an intuitive user experience across various platforms.

---
![Notolog settings UI example](https://raw.githubusercontent.com/notolog/notolog-editor/main/docs/notolog-ui-settings.png)


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


## Prerequisites

**Python 3.9 or higher installed on your system.**

If you haven't already, download and install Python from the official website [python.org](python.org).

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

#### MacOS and Linux

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

The Notolog project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

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
- **pluggy**: For creating and managing plugin systems in Python applications. [License Details](https://github.com/pytest-dev/pluggy/blob/main/LICENSE), [PyPI](https://pypi.org/project/pluggy/)

#### BSD Licenses

- **Python-Markdown**: Markdown to HTML conversion. [Project Details](https://python-markdown.github.io/), [BSD 3-Clause License](https://github.com/Python-Markdown/markdown/blob/master/LICENSE.md)
- **Emoji library**: Converts emoji text-code to emojis. [New BSD License](https://github.com/carpedm20/emoji/blob/master/LICENSE.txt), [PyPI](https://pypi.org/project/emoji/)
- **qasync**: Async support for Python. [BSD 2-Clause "Simplified" License](https://github.com/CabbageDevelopment/qasync/blob/master/LICENSE), [PyPI](https://pypi.org/project/qasync/)
- **Pygments**: Syntax highlighting for programming languages. [Project Details](https://pygments.org/), [BSD 2-Clause "Simplified" License](https://github.com/pygments/pygments/blob/master/LICENSE)
- **click**: Used for creating command-line interfaces. [Project Details](https://palletsprojects.com/p/click/), [BSD-3-Clause License](https://click.palletsprojects.com/en/8.1.x/license/)
- **pycparser**: C code parser and for generating Abstract Syntax Trees (AST) in Python. [BSD 3-Clause License](https://github.com/eliben/pycparser/blob/main/LICENSE), [PyPI](https://pypi.org/project/pycparser/)

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

**Disclaimer:** This project is independent and neither affiliated with, endorsed by, nor sponsored by OpenAI. Integration of the OpenAI API in this project is provided on an "as is" basis, without any official partnership or endorsement by OpenAI. The creators of this project disclaim all liability for any misuse, harm, or other consequences resulting from the use of the OpenAI API.

**Usage:** Our project employs the OpenAI API to enhance natural language processing capabilities. Users are required to provide their own OpenAI API keys and should refer to the [OpenAI API reference](https://platform.openai.com/docs/api-reference) for detailed usage guidelines.

**Responsibility:** Users are responsible for obtaining, configuring, and managing their OpenAI API keys in accordance with OpenAI's terms of service and usage policies.

**Security:** It is crucial for users to manage their API keys securely, ensuring they are not exposed or shared in public forums.

*This section was generated with the assistance of AI to ensure accurate and concise information regarding the use of the OpenAI API.*

## Security Disclaimer

This application is primarily designed for educational purposes and uses PBKDF2HMAC for key derivation. It employs Fernet, which utilizes AES-128 in CBC mode. The key is initially created at 256 bits but truncated to 128 bits for encryption. The encryption salt and iteration counts are stored unencrypted in the file's header, making this setup suitable for educational and non-critical applications only. As such, while this software provides basic security, it is not intended for high-security needs. Users are encouraged to choose strong passwords to enhance data protection. Distributed under the MIT License, this open-source application requires users to ensure compliance with applicable laws, and the developers disclaim liability for misuse or legal non-compliance.

---
This README.md file has been carefully crafted and edited using the Notolog editor itself.