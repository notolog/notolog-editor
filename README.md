<!-- {"notolog.app": {"created": "2023-12-25 18:59:43.806614", "updated": "2026-01-31 00:00:00.000000"}} -->
# Notolog

<div align="center">

<img src="https://raw.githubusercontent.com/notolog/notolog-editor/main/docs/assets/notolog-logo-blue.png" alt="Notolog Markdown Editor" width="72" height="72" /><br/>

[![PyPI - Version](https://img.shields.io/pypi/v/notolog)](https://pypi.org/project/notolog/)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/notolog)](https://anaconda.org/conda-forge/notolog)
[![Conda Recipe](https://img.shields.io/badge/recipe-notolog-green.svg)](https://anaconda.org/conda-forge/notolog)
[![PyPI - Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://pypi.org/project/notolog/)<br/>
[![GitHub License](https://img.shields.io/github/license/notolog/notolog-editor)](https://github.com/notolog/notolog-editor/blob/master/LICENSE)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/notolog/notolog-editor/tests.yaml)](https://github.com/notolog/notolog-editor/actions/workflows/tests.yaml)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/notolog)](https://pypistats.org/packages/notolog)
[![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/notolog)](https://anaconda.org/conda-forge/notolog)
</div>

Notolog is an open-source Markdown editor built with Python and PySide6, featuring AI-powered assistance and local-first privacy.

📖 **[Documentation](https://notolog.app)** | 🪲 **[Report Issues](https://github.com/notolog/notolog-editor/issues)** | 💡 **[Request Features](https://github.com/notolog/notolog-editor/discussions)** | 💬 **[Discussions](https://github.com/notolog/notolog-editor/discussions)**

---

## Quick Install

```sh
pip install notolog
notolog  # Launch the app
```

<details>
<summary>Other installation methods</summary>

**With llama.cpp support:**
```sh
pip install "notolog[llama]"
```

**Via conda:**
```sh
conda install notolog -c conda-forge
```

**Ubuntu/Debian:** Download from [notolog-debian releases](https://github.com/notolog/notolog-debian/releases/latest)

**From source:**
```sh
git clone https://github.com/notolog/notolog-editor.git
cd notolog-editor
python3 -m venv notolog_env && source notolog_env/bin/activate
pip install .
python -m notolog.app
```
</details>

---

![Notolog - Python Markdown Editor - UI Example](https://raw.githubusercontent.com/notolog/notolog-editor/main/docs/assets/images/ui/notolog-ui-example.png)

## Features

- **Markdown Editor** - Real-time syntax highlighting in edit mode (implemented specifically for Notolog), live preview, adaptive line numbers, code blocks
- **AI Assistant** - Supports: OpenAI API, ONNX Runtime GenAI (local), and llama.cpp (local, GGUF models)
- **File Encryption** - PBKDF2HMAC key derivation with Fernet (AES-128 CBC mode) for optional file encryption
- **Multi-Language** - 19 languages supported
- **Customizable** - 6 built-in themes
- **Cross-Platform** - Windows, macOS, Linux

See the [User Guide](https://notolog.app/user-guide/) for complete feature documentation.


## Requirements

- **Python 3.10+** ([python.org](https://python.org))
- 4 GB RAM minimum (8+ GB for local AI models)


## Installation

Using a virtual environment is recommended:

```sh
python3 -m venv notolog_env
source notolog_env/bin/activate  # Linux/macOS
notolog_env\Scripts\activate     # Windows
pip install notolog
```

For detailed instructions including conda and Debian packages, see [Getting Started](https://notolog.app/getting-started/).


## AI Assistant

Notolog supports three AI backends:

- **OpenAI API** - Cloud-based inference via OpenAI-compatible endpoints
- **On-Device LLM** - Local inference using ONNX Runtime GenAI (e.g. Phi-3, Llama)
- **Module llama.cpp** - Local inference with GGUF quantized models (e.g. Llama, Mistral, Qwen)

See the [AI Assistant Guide](https://notolog.app/ai-assistant/) for setup instructions.


## Development

```sh
git clone https://github.com/notolog/notolog-editor.git
cd notolog-editor
pip install -e .
python -m notolog.app
```

**Run tests:**
```sh
python dev_install.py test
pytest
```

See [CONTRIBUTING.md](https://github.com/notolog/notolog-editor/blob/main/CONTRIBUTING.md) for guidelines.


## License

Notolog is open-source software licensed under the [MIT License](https://github.com/notolog/notolog-editor/blob/main/LICENSE).

This project uses third-party libraries, each subject to its own license. See [ThirdPartyNotices.md](https://github.com/notolog/notolog-editor/blob/main/ThirdPartyNotices.md) for details.


## Security

Notolog prioritizes data protection and user privacy:

- **Encryption**: File encryption (optional) uses PBKDF2HMAC key derivation with Fernet (AES-128 CBC mode).
- **Auto-Save**: Changes are saved automatically to prevent data loss.
- **Privacy**: No telemetry or tracking. Local-only AI inference options available.

For vulnerability reporting, see [SECURITY.md](https://github.com/notolog/notolog-editor/blob/main/SECURITY.md).


## Disclaimers

### Third-Party AI Services and Libraries

This project integrates third-party AI services and libraries:

- **OpenAI API**: Users are required to supply their own API keys and adhere to OpenAI's applicable terms, policies, and [API documentation](https://platform.openai.com/docs/api-reference).
- **ONNX Runtime GenAI**: Used for local ONNX model inference. More info: [onnxruntime-genai](https://github.com/microsoft/onnxruntime-genai)
- **llama.cpp**: Used for local GGUF model inference via [llama-cpp-python](https://github.com/abetlen/llama-cpp-python).

*Notolog is developed independently and is not affiliated with these organizations or projects.*

### Legal

- **Compliance**: Users are responsible for ensuring their use complies with applicable laws and regulations.
- **Liability**: The developers disclaim liability for misuse or non-compliance with legal or regulatory requirements.
- **Trademarks**: All trademarks and brand names are the property of their respective owners and are used for identification purposes only.

---

⭐ If you find Notolog useful, please consider giving it a star on [GitHub](https://github.com/notolog/notolog-editor)!

---
_This README.md file has been crafted and edited using Notolog Editor._
