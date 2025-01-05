<!-- {"notolog.app": {"created": "2023-12-25 18:59:43.806614", "updated": "2025-01-04 14:33:41.680966"}} -->
# Notolog

[![PyPI - Version](https://img.shields.io/pypi/v/notolog)](https://pypi.org/project/notolog/) [![GitHub License](https://img.shields.io/github/license/notolog/notolog-editor)](https://github.com/notolog/notolog-editor/blob/master/LICENSE) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/notolog)](https://pypi.org/project/notolog/) [![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/notolog/notolog-editor/tests.yaml)](https://github.com/notolog/notolog-editor/actions/workflows/tests.yaml) [![Conda Version](https://img.shields.io/conda/vn/conda-forge/notolog)](https://anaconda.org/conda-forge/notolog) [![PyPI - Downloads](https://img.shields.io/pypi/dm/notolog)](https://pypistats.org/packages/notolog)

Notolog is an open-source Markdown editor licensed under the MIT License. Combining simplicity with powerful tools and an AI Assistant, it's built with Python and PySide6 to help you tackle programming challenges and sharpen your Markdown skills in a cozy, efficient way.


## Instant Setup

Using pip:
```sh
pip install notolog
```

Via conda:
```sh
conda install notolog -c conda-forge
```

To start 🚀 the app, simply run:
```
notolog
```

---

![Notolog - Python Markdown Editor - UI Example](https://raw.githubusercontent.com/notolog/notolog-editor/main/docs/notolog-ui-examples.png)

## Features

- **Markdown Support**:
    - Text editor equipped with exclusive Markdown syntax highlighting and extended syntax support.
    - Line numbers adapt to each line's height, enhancing readability.
    - Viewer for precise text rendering, utilizing the integrated Python Markdown library.
    - Processes both multi-line and single-line code blocks, along with custom parsing for `details` and `summary` blocks.
- **AI Assistant**: Provides a chat-style dialogue, supporting both the OpenAI API and on-device local LLM options.
- **Accessibility**: Features adjustable font sizes and descriptive elements to enhance usability.
- **Auto-Save**: Automatically saves changes to prevent data loss.
- **Enhanced Search**:
    - Offers in-file content search with optional case sensitivity.
    - Quick file search within the file tree to efficiently filter results.
- **Encryption**: Provides secure AES-128 encryption with Fernet for files (optional).
- **Meta-Headers**: Securely stores essential file information within HTML-comment-formatted meta-headers.
- **Multi-Language**: Supports multiple languages out of the box.
- **Customizable UI**: Includes a variety of color themes to keep the UI fancy.
- **TODO Highlighting**: Marks @todo statements for efficient task management.


## Translations

Notolog supports multiple languages out of the box, enhancing its accessibility globally. In addition to English, here are the currently supported languages:

- 简体中文 (Chinese Simplified)
- Nederlands (Dutch)
- Suomi (Finnish)
- Français (French)
- ქართული (Georgian)
- Deutsch (German)
- Ελληνικά (Greek)
- हिन्दी (Hindi)
- Italiano (Italian)
- 日本語 (Japanese)
- 한국어 (Korean)
- Latina (Latin)
- Português (Portuguese)
- Русский (Russian)
- Español (Spanish)
- Svenska (Swedish)
- Türkçe (Turkish)


## Themes

Notolog offers several themes to customize the UI:

* **Default**: Every app should have a default theme.
* **Calligraphy**: Inspired by the art of calligraphy, this theme resembles a rice paper sheet marked with black ink.
* **Nocturne**: A dark-themed UI that plays a jazz nocturne at night.
* **Noir Dark**: This theme's name says it all - mystery and style in every pixel.
* **Spooky**: Embrace the spooky season with vivid Halloween-themed colors.
* **Strawberry**: The most playful theme, reminiscent of strawberry jam.

Below is a glimpse of the UI, featuring the settings window:

![Notolog - Python Markdown Editor - UI Example](https://raw.githubusercontent.com/notolog/notolog-editor/main/docs/notolog-ui-settings.png)

## Installation

Ensure **Python 3.9 or higher** is installed. For more details, visit [python.org](https://python.org).

Using a virtual environment is recommended to avoid version conflicts. From Python 3.6, venv is the recommended method to create virtual environments. For more information check [Creation of virtual environments](https://docs.python.org/3/library/venv.html). Alternatively, you can execute the Notolog source code and set up virtual environment with your favorite Python code editor.

### Install with pip

Create and activate a virtual environment:
```sh
python3 -m venv notolog_env
source notolog_env/bin/activate  # macOS and Linux systems
notolog_env\Scripts\activate  # Windows
```

Install Notolog using pip:
```sh
pip install notolog
```

Starting the app is as simple as running:
```sh
notolog
```

The app includes a 'Check for Updates' option accessible through the main menu under 'Help'. Where applicable, run the following command to update Notolog to the latest version: `pip install notolog --upgrade`

<details>
<summary>How to install venv on Linux systems 🔧 </summary>

While Python itself usually comes pre-installed on many Linux distributions, including Ubuntu, some distributions may not include the venv module by default. Therefore, you need to install it separately using the package manager before you can use it to create virtual environments.

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

### Install via conda-forge

Create and activate a new environment:
```sh
conda create -n notolog_env python=3.11
conda activate notolog_env
```

Then, execute the installation command:
```sh
conda install notolog -c conda-forge
```

This will fetch and install the latest version of Notolog compatible with Python 3.9 or newer from the [conda-forge packages](https://anaconda.org/conda-forge/notolog).

Run Notolog:
```sh
notolog
```

Just activate the environment and run the app next time.

### Install from Source

1. Clone the GitHub repository:
```sh
git clone https://github.com/notolog/notolog-editor.git
```

2. Navigate to the project directory:
```sh
cd notolog-editor
```

3. Create and activate a virtual environment:
```sh
python3 -m venv notolog_env
source notolog_env/bin/activate  # macOS and Linux systems
notolog_env\Scripts\activate  # Windows
```

4. Install dependencies:
```sh
pip install .
```

5. Start Notolog using:
```sh
python -m notolog.app
```


## Extensions

### Module llama.cpp

By default, the module is included in the base installation but not activated. However, it can be enabled by installing the `llama-cpp-python` package (Python Bindings for llama.cpp). Below is a quick installation summary:

```sh
pip install llama-cpp-python
```

The package requires a C compiler to be installed. If a compiler is not available, you may encounter an error such as:
*CMake Error: CMAKE_CXX_COMPILER not set, after EnableLanguage*

This error indicates that the system cannot find a suitable C++ compiler to build the necessary components. Installing a compatible compiler, such as GCC or Clang, should resolve the issue.

For Linux systems, installing the `build-essential` package is often sufficient to resolve this. For example, on Ubuntu, run:

```sh
sudo apt-get install build-essential
```

For platform-specific or more detailed instructions, refer to the [official documentation](https://github.com/abetlen/llama-cpp-python#installation) provided with the `llama-cpp-python` package.

After successful installation, the **Module llama.cpp** will be available in the application settings and ready to use.


## Tests and Test Coverage

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


## Dev Tools

To maintain high standards of code quality and ensure comprehensive test coverage, we utilize several development tools. Flake8, which combines PyFlakes, pycodestyle, and McCabe's complexity checker, is employed to enforce code quality, manage code complexity, and ensure adherence to PEP 8 style conventions.

To install these dependencies, run: `python dev_install.py dev`. The `tomli` package is required to execute this script; you can install it using `pip install tomli`.


## Build Tools

Make sure `poetry-core` and `build` are installed:
```
pip install poetry-core build
```

The following command generates distribution packages. Specifically, it creates both a source distribution and a wheel distribution:
```
python -m build
```


## Contributing

If you encounter any issues or would like to contribute to the project, please don't hesitate to [open an issue](https://github.com/notolog/notolog-editor/issues) or submit a [pull request](https://github.com/notolog/notolog-editor/pulls) on the project's [GitHub page](https://github.com/notolog/notolog-editor).


## License

Notolog is open-source software licensed under the MIT License, which provides flexibility and freedom to use, modify, and distribute the software. To comply with the license when redistributing this software or derivative works, you must include a copy of the original MIT License, found in the [LICENSE](https://github.com/notolog/notolog-editor/blob/main/LICENSE) file.


## Third-Party Acknowledgements

This project uses third-party libraries and components, each subject to its own license. Additional dependencies may be installed as necessary. For details on licensing, see [ThirdPartyNotices.md](https://github.com/notolog/notolog-editor/blob/main/ThirdPartyNotices.md).


## AI Integration Disclaimers

### OpenAI API

**Disclaimer**: This project integrates the OpenAI API 'as is' and is independent, not affiliated with OpenAI. The creators disclaim any liability for misuse or resulting consequences.

**Usage**: Users are required to supply their own API keys and adhere to the [OpenAI API reference](https://platform.openai.com/docs/api-reference) guidelines.

**Security**: Proper management of API keys is essential for maintaining the security of your data. Ensure that API keys are stored and handled securely to prevent unauthorized access.

### ONNX Runtime GenAI

**Disclaimer**: The 'On Device LLM' module uses ONNX Runtime to enable generative AI features and is not associated with Microsoft or ONNX Runtime.

### Python Bindings for llama.cpp

**Disclaimer**: The 'Module llama.cpp' module in this application utilizes the Python Bindings for llama.cpp to facilitate LLM inference with models in GGUF format. This module is independently developed and is not officially connected to either the llama-cpp-python or the llama.cpp projects.


## Security Disclaimer

### File Encryption

- **Details**: Notolog uses PBKDF2HMAC for key derivation and Fernet (AES-128 CBC mode) for encryption. Future updates may enhance encryption strength.

### File Meta-Headers

- **Privacy by Design**: Essential information is stored in HTML-comment-formatted meta-headers to preserve essential data.

### Data Integrity and Security

- **Auto-Save Feature**: Automatically saves changes to minimize data loss.
- **Password Protection**: Strong password practices are recommended to protect access to encrypted files.

### Legal and Compliance

- **Open Source Compliance**: Licensed under the MIT License. Users are responsible for ensuring that their use of the software complies with applicable local laws and regulations.
- **Liability**: Developers disclaim liability for misuse or non-compliance with legal and regulatory standards.


## Trademark Disclaimer

All trademarks, registered trademarks, product names, and company names or logos mentioned herein are the property of their respective owners. References to these trademarks in any documentation, code, or API communications are for identification purposes only and do not imply endorsement or affiliation.


## Support Us

If you find Notolog useful, consider giving it a star 🌟 on the [GitHub page](https://github.com/notolog/notolog-editor). This helps others discover the project and contributes to its growth. Thank you for your support!

---
_This README.md file has been carefully crafted and edited using the Notolog editor itself._