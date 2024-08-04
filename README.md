<!-- {"notolog.app": {"created": "2023-12-25 18:59:43.806614", "updated": "2024-08-04 16:58:29.040241"}} -->
# Notolog

![Notolog - Python Markdown Editor](https://raw.githubusercontent.com/notolog/notolog-editor/main/notolog/assets/notolog-example-image.png)

## Python Markdown Editor

[![PyPI - Version](https://img.shields.io/pypi/v/notolog)](https://pypi.org/project/notolog/) [![GitHub License](https://img.shields.io/github/license/notolog/notolog-editor)](https://github.com/notolog/notolog-editor/blob/master/LICENSE) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/notolog)](https://pypi.org/project/notolog/) [![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/notolog/notolog-editor/tests.yaml)](https://github.com/notolog/notolog-editor/actions/workflows/tests.yaml)

Notolog is an open-source Python Markdown editor that blends simplicity with functionality. Designed using PySide6, it not only helps tackle daily programming challenges but also enhances proficiency in both Markdown and Python for those interested in diving deeper into the code.

---

![Notolog UI example](https://raw.githubusercontent.com/notolog/notolog-editor/main/docs/notolog-ui-settings.png)


## Features

- **Open-source and Transparent**: Licensed under MIT, promoting transparency and collaboration.
- **Markdown Support**:
    - Editor mode with smooth highlighting, line numbers, and extended syntax.
    - View mode, which uses the Python Markdown library for accurate rendering to HTML.
    - Improves readability and structure through custom parsing of disclosure widgets, including nested hierarchies.
    - Supports multi-line block open-close tokens.
- **AI Assistant**: Incorporate module extensions able to work either with AI APIs or with on-device large language models (LLMs).
- **Accessibility Features**:
    - Descriptive elements for enhanced usability.
    - Adjustable font sizes for improved readability.
- **Auto-Save**: Changes are saved automatically, ensuring that data is not lost unexpectedly.
- **Enhanced Search Functionality**:
    - In-file content search.
    - Quick file name search within the file tree.
- **File Encryption**:
    - Securely encrypts files using Fernet, which employs AES-128 in CBC mode, providing strong encryption.
- **File Meta-Headers**:
    - Stores essential file information securely in meta-headers formatted as HTML comments, thus enhancing privacy and security.
- **Multi-language Support**: Available in several languages, with easy addition of new languages.
- **Customizable UI**:
    - Multiple color themes for personalization.
    - Supports hotkeys like Ctrl+S (save) and Ctrl+F (search).
    - Right-click context menus for file management in the file tree.
- **TODOs Highlighting**: Notolog includes specialized highlighting for TODOs. By typing '@todo something,' users can mark tasks, thus enhancing the ability to track and manage future plans efficiently.
- **Unit Testing Suite**: Ensures reliability and maintainability of the code.

*Remember: Strong password enforcement is recommended to protect access to encrypted files.*


## Translations

Notolog supports multiple languages out of the box, enhancing its accessibility globally. Here are the languages currently supported:

- Chinese (Simplified), Dutch, Finnish, French, Georgian, German, Greek, Hindi, Italian, Japanese, Korean, Latin, Portuguese, Russian, Spanish, Swedish, Turkish

Here's a glimpse of the UI in Japanese, featuring the Strawberry theme:

![Notolog UI translation example](https://raw.githubusercontent.com/notolog/notolog-editor/main/docs/notolog-ui-settings-strawberry-ja.png)


## Prerequisites

Ensure **Python 3.9 or higher** is installed on your system. For installation details, visit [python.org](https://python.org).

Check the installed Python version:

```bash
python3 -V
```

Verify pip availability:

```bash
pip --version
```

**Virtual Environment**

Using a virtual environment is highly recommended as it helps avoid version conflicts and interference from other packages.


## Installation

### Using pip (Recommended)

Set up a virtual environment (highly recommended):
```sh
python3 -m venv notolog
# On Unix-like systems (macOS and Linux):
source notolog/bin/activate
# On Windows:
notolog\Scripts\activate
```

Install Notolog quickly using pip:
```sh
pip install notolog
```

That's it! Starting the app is as simple as running `notolog`.

To update Notolog to the latest version:
```sh
pip install --upgrade notolog
```

### From Source

To install from source for more control over the installation process:

1. Clone the GitHub repository:
```sh
git clone https://github.com/notolog/notolog-editor.git
```

2. Navigate to the project directory:
```sh
cd notolog-editor
```

3. Set up a virtual environment (highly recommended):
```sh
python3 -m venv notolog
# On Unix-like systems:
source notolog/bin/activate
# On Windows:
notolog\Scripts\activate
```

4. Install dependencies:
```sh
pip install .
```

Start Notolog using:
```sh
python -m notolog.app
```

### Tests and Test Coverage

To minimize installation overhead and streamline dependency management, dependencies required solely for testing are isolated in test-specific requirements.

To install these dependencies, run: `python dev_install.py test`. The `tomli` package is required to execute this script; you can install it using `pip install tomli`.

This approach helps manage test dependencies independently from the main application dependencies, ensuring a cleaner and more manageable setup.

<details>
<summary>Run Tests</summary>

To execute all available tests:
```sh
pytest
```

To run tests from a specific file:
```sh
pytest tests/test_pkg_integration.py
```
</details>

<details>
<summary>Run Tests with Coverage Reports</summary>

To run all tests with a coverage report:
```sh
pytest tests/ --cov=notolog --cov-report=term
```

Alternatively, to exclude UI tests from execution:
```sh
pytest tests/ --cov=notolog --cov-report=term --ignore=tests/ui_tests/
```
</details>

### Dev Tools

To maintain high standards of code quality and ensure comprehensive test coverage, we utilize several development tools. Flake8, which combines PyFlakes, pycodestyle, and McCabe's complexity checker, is employed to enforce code quality, manage code complexity, and ensure adherence to PEP 8 style conventions.

To install these dependencies, run: `python dev_install.py dev`. The `tomli` package is required to execute this script; you can install it using `pip install tomli`.

### Build Tools

Make sure `poetry-core` and `build` are installed:
```
pip install poetry-core build
```

The following command generates distribution packages. Specifically, it creates both a source distribution and a wheel distribution:
```
python -m build
```

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


## Third-Party Acknowledgements

This project incorporates various third-party libraries and components, each subject to their own licenses. These packages may also install additional dependencies necessary for their functionality. For detailed information about these components and their licenses, please see the [ThirdPartyNotices.md](https://github.com/notolog/notolog-editor/blob/main/ThirdPartyNotices.md) file.

Users and contributors are encouraged to consult this document to fully understand the licensing obligations and acknowledgements related to these third-party components.


## AI Integration Disclaimers

### OpenAI API

**Disclaimer**: This project is independent and not affiliated with, endorsed by, or sponsored by OpenAI. The OpenAI API is integrated 'as is'. The creators disclaim liability for misuse or any consequences arising from this integration.

**Usage**: This project uses the OpenAI API to access AI assistant capabilities, and enhance natural language processing. Users must provide their own OpenAI API keys and should refer to the [OpenAI API reference](https://platform.openai.com/docs/api-reference) for detailed usage guidelines.

**Responsibility**: Users are responsible for obtaining and managing their OpenAI API keys in compliance with OpenAI's terms of service.

**Security**: Users are expected to handle their API keys securely to avoid unauthorized access.

*This section was generated with the assistance of AI to ensure accurate and concise information regarding the use of the OpenAI API.*

### ONNX Runtime GenAI

**Disclaimer**: The 'On Device LLM' module, part of this application, utilizes the ONNX Runtime functionality to provide specialized capabilities for generative AI features. The application is an independent project and is not officially associated with ONNX Runtime, maintained by Microsoft, or with any other third-party entities.


## Security Disclaimer

### File Encryption

- **Encryption Details**: Notolog uses PBKDF2HMAC for key derivation and Fernet for encryption, which employs AES-128 in CBC mode. Although 256-bit key material is generated, only the first 128 bits are utilized for encryption. Future updates aim to enhance security by employing the full 256 bits.

### File Meta-Headers

- **Privacy by Design**: Essential file information is stored securely in meta-headers formatted as HTML comments, enhancing privacy and security.

### Data Integrity and Security

- **Auto-Save Feature**: Changes are automatically saved, minimizing the risk of data loss.
- **Password Protection**: Strong password practices are recommended to safeguard access to encrypted files.

### General Information

- **Open Source**: This application is open-source, licensed under the MIT License. Users must comply with applicable laws and regulations when using this software.
- **Liability**: The developers disclaim any liability for misuse or legal non-compliance related to the use of this software.


## Trademark Disclaimer

All company names, product names, logos, and brands mentioned in this document, code, or comments are the property of their respective owners. All company, product, and service names used in this document, code, or comments are for identification purposes only. Use of these names, logos, and brands does not imply endorsement or affiliation. Mention of third-party names, logos, and brands is solely for identification and does not constitute an endorsement or affiliation with any trademark holder.

---
_This README.md file has been carefully crafted and edited using the Notolog editor itself._