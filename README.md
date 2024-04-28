<!-- {"notolog.app": {"created": "2023-12-25 18:59:43.806614", "updated": "2024-04-28 23:13:43.036897"}} -->
# Notolog

## Overview

Notolog is a markdown editor crafted in Python and Qt, offered as an open-source solution.

In short, I was in search of a simple, lightweight, and cross-platform editor to fulfill my daily needs as a software developer. Concurrently, I aimed to deepen my understanding of Python, leading me to embark on creating my own editor. Thus, the Notolog editor was born.

The editor has no aim but the path, hence its proof-of-concept nature and many tasks yet to be completed. Speaking of tasks, the editor features special highlighting for the word 'TODO'; simply type it with '@', like '@todo something', and see what happens.

## Features

* Open sourced under the MIT license for full transparency and collaboration.
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
* File meta-headers in the form of HTML comments to avoid excess visibility.
* Password-based file symmetric encryption and decryption:
	* Employing AES-256 in CBC mode (Cipher Block Chaining) with the power of the Fernet library.
	* Key derivation based on a 256-bit key using PBKDF2HMAC from the cryptography library, using SHA-256 as the hash function.
	* Fernet provides an easy-to-use and secure way of performing symmetric (also known as "secret key") encryption.
	* File meta-headers to keep encryption params to allow a seamless decryption process.
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

---
There is no classical web engine integration to make overall package more lightweight and to achieve the best possible performance.

## Prerequisites:

**Python 3.9 or higher installed on your system.**

If you haven't already, download and install Python from the official website [python.org](python.org).

Check the version of Python available with this command:
```sh
python3 -V
```

**pip (Python package installer) should be available.**
You can check if pip is installed by running `pip3 --version` in your terminal/command prompt.

## Installation

### <span style="color: green">Run the Python code</span>

0. Open Terminal.
1. Clone project's GitHub repository to get a latest version.
	* `git clone https://github.com/notolog/notolog-editor.git`
2. Navigate to your project directory using the **cd** command.
3. Make sure the virtual environment is activated as it's a common practice to isolate project code (described below).
4. Simply run this command to set up project dependencies:

```sh
pip3 install -r requirements.txt
```

That's it! Starting the app is as simple as `python3 main.py`

### Using Virtual Environments

The instructions below contain steps of how to set up **venv** virtual environment to run a Python app safely. Starting from Python 3.6 **venv** is a recommended way to create virtual environments. For more information check [Creation of virtual environments](https://docs.python.org/3/library/venv.html)

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

#### MacOS and Linux

##### Set Up Virtual Environment

1. Open Terminal.
2. Navigate to your project directory using the cd command.
3. Create a virtual environment by running `python3 -m venv notolog`. Replace **notolog** with the desired name for your virtual environment.

Activate Virtual Environment:
To activate the virtual environment, run:
```sh
source notolog/bin/activate
```

To deactivate environment just run this command:
```sh
deactivate
```

##### Install venv on Linux systems

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

### Using IDE

Alternatively, you can execute the Notolog code with your favorite Python code editor.

## Usage

To start the app simply run this command in a project dir:
```sh
python3 main.py
```

### Run tests

To run all available tests:
```sh
pytest
```

To run a particular file's tests:
```sh
pytest tests/test_notolog_editor.py
```

## Contributing

If you encounter any issues or would like to contribute to the project, please don't hesitate to open an issue or submit a pull request on GitHub.

## License

The Notolog project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Third-Party Components

### Libraries and Dependencies

This project utilizes the following third-party libraries:

* Qt (open-source): Distributed under the GNU LGPLv3, GNU GPLv2, or Qt Commercial License. ([Qt Licensing](https://www.qt.io/licensing))
* PySide6: Used for creating graphical user interfaces with Qt6 in Python. ([PySide6 is available under both Open Source (LGPLv3/GPLv2) and commercial license.](https://pypi.org/project/PySide6/))
	* PySide6_Addons: Additional modules and utilities for PySide6 to enhance functionality. ([PySide6 is available under both Open Source (LGPLv3/GPLv2) and commercial license.](https://pypi.org/project/PySide6-Addons/))
	* PySide6_Essentials: Essential components and tools for PySide6 development, including core libraries and resources. ([PySide6 is available under both Open Source (LGPLv3/GPLv2) and commercial license.](https://pypi.org/project/PySide6-Essentials/))
* shiboken6: A Python binding generator used in conjunction with PySide6 to create Python bindings for the Qt framework. ([PySide6 is available under both Open Source (LGPLv3/GPLv2) and commercial license.](https://pypi.org/project/shiboken6/))
* Python-Markdown: Used for Markdown to HTML conversion. ([The 3-Clause BSD License](https://github.com/Python-Markdown/markdown/blob/master/LICENSE.md))
* Emoji library: Used for converting emoji code to real emoji. ([New BSD License](https://github.com/carpedm20/emoji/blob/master/LICENSE.txt))
* qasync: Used for handling async syntax highlighting. ([BSD 2-Clause "Simplified" License](https://github.com/CabbageDevelopment/qasync/blob/master/LICENSE))
* cryptography: Used for generating cryptographic hashes and keys in this project is dual-licensed under the:
	* ([Apache License 2.0](https://github.com/pyca/cryptography/blob/main/LICENSE.APACHE))
	* ([BSD 3-Clause License](https://github.com/pyca/cryptography/blob/main/LICENSE.BSD))
* Bootstrap Icons: Used for UI toolbar icons and other visual elements. ([The MIT License (MIT)](https://github.com/twbs/icons/blob/main/LICENSE))
* pytest: Used for testing. ([The MIT License (MIT)](https://docs.pytest.org/en/8.0.x/license.html))
* pytest-mock: Used for testing. ([The MIT License (MIT)](https://github.com/pytest-dev/pytest-mock/blob/main/LICENSE))
* asyncio: Used for handling async syntax highlighting is part of the Python standard library, which typically falls under the [Python Software Foundation License](https://docs.python.org/3/license.html#psf-license).
* cffi: Used for interfacing with C code. ([The MIT License (MIT)](https://github.com/python-cffi/cffi/blob/main/LICENSE))
* click: Used for creating command-line interfaces. ([BSD-3-Clause License](https://click.palletsprojects.com/en/8.1.x/license/))
* iniconfig: Used for parsing and working with INI configuration files. ([The MIT License (MIT)](https://github.com/pytest-dev/iniconfig/blob/main/LICENSE))
* packaging: Used for working with Python package metadata and distribution utilities is dual-licensed under the:
	* ([Apache License 2.0](https://github.com/pypa/packaging/blob/main/LICENSE.APACHE))
	* ([BSD 2-Clause "Simplified" License](https://github.com/pypa/packaging/blob/main/LICENSE.BSD))
* tomli: A Python library used for parsing TOML configuration files effortlessly. ([The MIT License (MIT)](https://github.com/hukkin/tomli/blob/master/LICENSE))
* pluggy: Used for creating and managing plugin systems in Python applications. ([The MIT License (MIT)](https://github.com/pytest-dev/pluggy/blob/main/LICENSE))
* pycparser: Used for parsing C code and generating Abstract Syntax Trees (AST) in Python. ([BSD 3-Clause License](https://github.com/eliben/pycparser/blob/main/LICENSE))
* Pygments: Used for syntax highlighting source code in various programming languages. ([BSD 2-Clause "Simplified" License](https://github.com/pygments/pygments/blob/master/LICENSE))

Please note that while the majority of this project is licensed under the MIT License, certain components may have different licensing terms. Please refer to the documentation of each library for information about its license and terms of use.

This project includes code from external sources that are licensed under The Unlicense. We acknowledge and thank the original authors for their contributions.

* [Examples of codehilite CSS themes](https://github.com/richleland/pygments-css): Used to create color themes for code block highlighting. ([The Unlicense](https://github.com/richleland/pygments-css/blob/master/UNLICENSE.txt))

### APIs

#### OpenAI API Disclaimer

**Disclaimer:** This project is independent and neither affiliated with, endorsed by, nor sponsored by OpenAI. Integration of the OpenAI API in this project is provided on an "as is" basis, without any official partnership or endorsement by OpenAI. The creators of this project disclaim all liability for any misuse, harm, or other consequences resulting from the use of the OpenAI API.

**Usage:** Our project employs the OpenAI API to enhance natural language processing capabilities. Users are required to provide their own OpenAI API keys and should refer to the [OpenAI API reference](https://platform.openai.com/docs/api-reference) for detailed usage guidelines.

**Responsibility:** Users are responsible for obtaining, configuring, and managing their OpenAI API keys in accordance with OpenAI's terms of service and usage policies.

**Security:** It is crucial for users to manage their API keys securely, ensuring they are not exposed or shared in public forums.

*This section was generated with the assistance of AI to ensure accurate and concise information regarding the use of the OpenAI API.*

## Security Disclaimer

This application, primarily designed for educational purposes, employs PBKDF2HMAC for key derivation and AES-256 in CBC mode for encryption, using a 256-bit key. Note that the encryption salt and iteration counts are stored unencrypted in the file's header. While secure for educational and non-critical uses, this setup may not meet the highest security standards. Users can opt to add a password hint in the file header, which should be used judiciously to balance convenience against security risks.

As an educational tool, this software is not intended for high-security needs. Users are encouraged to choose strong passwords to enhance data protection. Distributed under the MIT License, this open-source application requires users to ensure compliance with applicable laws. The developers disclaim liability for misuse or for ensuring legal compliance.

---

`░░░░░░░░░░░░░░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓███■███▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░░░░░░░░` 
`╔═══════════════════════════════════════════════════════════════════════════════════════════╗` 
`║ This README.md file has been carefully crafted and edited using the Notolog editor itself ║` 
`╚═══════════════════════════════════════════════════════════════════════════════════════════╝`