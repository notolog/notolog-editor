<!-- {"notolog.app": {"created": "2026-01-18 13:57:00.794379", "updated": "2026-01-18 13:57:00.794379"}} -->
# Notolog Documentation

Welcome to the official documentation for **Notolog** - an open-source Markdown editor built with Python and PySide6.

## Quick Links

- [Getting Started](getting-started.md) - Installation and first steps
- [User Guide](user-guide.md) - Complete feature overview
- [Markdown Examples](examples.md) - Markdown syntax reference and examples
- [AI Assistant](ai-assistant.md) - Using AI features (OpenAI, ONNX, llama.cpp)
- [Configuration](configuration.md) - Settings and customization
- [API Reference](api-reference.md) - For developers and contributors
- [FAQ & Troubleshooting](faq.md) - Common questions and solutions

## What is Notolog?

Notolog is a privacy-focused Markdown editor that combines:

- **Clean Markdown editing** with syntax highlighting
- **AI-powered assistance** via OpenAI API or local LLMs (ONNX, GGUF)
- **File encryption** using AES-128 with Fernet
- **Multi-language support** (18 languages)
- **Customizable themes** (6 built-in themes)

## System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Python | 3.10+ | 3.11+ |
| OS | Windows 10, macOS 10.14, Ubuntu 20.04 | Latest versions |
| RAM | 4 GB | 8 GB (16 GB for local LLMs) |
| Storage | 100 MB | 500 MB+ (depends on models) |

## Installation Overview

```bash
# Using pip (recommended)
pip install notolog

# Using conda
conda install notolog -c conda-forge

# With llama.cpp support
pip install notolog[llama]
```

See [Getting Started](getting-started.md) for detailed installation instructions.

## Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/notolog/notolog-editor/issues)
- **Repository**: [github.com/notolog/notolog-editor](https://github.com/notolog/notolog-editor)
- **Website**: [notolog.app](https://notolog.app)

## License

Notolog is released under the [MIT License](https://github.com/notolog/notolog-editor/blob/main/LICENSE).

---

*Documentation version: 1.1.7*
