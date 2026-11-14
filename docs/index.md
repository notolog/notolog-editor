# Notolog Documentation

[![PyPI - Version](https://img.shields.io/pypi/v/notolog)](https://pypi.org/project/notolog/)
[![GitHub License](https://img.shields.io/github/license/notolog/notolog-editor)](https://github.com/notolog/notolog-editor/blob/main/LICENSE)
[![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/notolog)](https://anaconda.org/conda-forge/notolog)

Welcome to the official documentation for **Notolog** - an open-source Markdown editor built with Python and PySide6.

## Quick Links

* [Getting Started](getting-started.md) - Installation and first steps
* [User Guide](user-guide.md) - Complete feature overview
* [Markdown Syntax](markdown-syntax.md) - Markdown syntax reference and examples
* [AI Assistant](ai-assistant.md) - Using AI features (OpenAI, ONNX, llama.cpp)
* [Text-to-Speech](text-to-speech.md) - Read documents and selections aloud locally
* [Configuration](configuration.md) - Settings and customization
* [API Reference](api-reference.md) - For developers and contributors
* [FAQ & Troubleshooting](faq.md) - Common questions and solutions

---
![Notolog - Python Markdown Editor - UI Example](assets/images/ui/notolog-ui-example.png)

## What is Notolog?

Notolog is a privacy-focused Markdown editor that combines:

- **Clean Markdown editing** with syntax highlighting
- **AI-powered assistance** via OpenAI API or local LLMs (ONNX, GGUF)
- **Local Text-to-Speech** for documents, selections, and reading from the cursor
- **File encryption** using AES-128 with Fernet
- **Multi-language support** (19 languages)
- **Customizable themes** (6 built-in themes)

## System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Python | 3.11–3.14 | A version supported by all selected dependencies |
| OS | Windows, macOS, or Linux with compatible native dependencies | See [installation requirements](getting-started.md#platform-compatibility) |
| RAM | 4 GB (base editor) | Additional RAM or VRAM required by the selected local models and context |
| Storage | Space for Notolog and its Python/Qt dependencies | Additional space for downloaded models and notes |

!!! note "Local LLM Memory Requirements"
    Memory use depends on the model, quantization, context length, and runtime.
    Follow the selected model's requirements; parameter count alone does not determine RAM or VRAM needs.

## Installation Overview

```bash
# Using pip (recommended)
pip install notolog

# Using conda
conda install notolog -c conda-forge

# With llama.cpp support
pip install "notolog[llama]"
```

See [Getting Started](getting-started.md) for detailed installation instructions.

## Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/notolog/notolog-editor/issues)
- **GitHub Discussions**: [Ask questions and discuss](https://github.com/notolog/notolog-editor/discussions)
- **Repository**: [github.com/notolog/notolog-editor](https://github.com/notolog/notolog-editor)
- **Website**: [notolog.app](https://notolog.app)

## License

Notolog is released under the [MIT License](https://github.com/notolog/notolog-editor/blob/main/LICENSE).

---

*Documentation for Notolog 1.2.5.*
