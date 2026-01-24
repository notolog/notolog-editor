<!-- {"notolog.app": {"created": "2026-01-18 13:57:00.794379", "updated": "2026-01-24 00:00:00.000000"}} -->
# FAQ & Troubleshooting

Common questions and solutions for Notolog users.

## Table of Contents

* [Installation Issues](#installation-issues)
* [General Usage](#general-usage)
* [AI Assistant Issues](#ai-assistant-issues)
* [File & Encryption Issues](#file-encryption-issues)
* [Getting Help](#getting-help)

---

## Installation Issues

### Q: Qt platform plugin "xcb" error on Linux

**Error**: `qt.qpa.plugin: Could not load the Qt platform plugin "xcb"`

**Solution**:
```bash
sudo apt-get install -y libxcb-cursor0
```

---

### Q: llama-cpp-python won't install

**Error**: `CMake Error: CMAKE_CXX_COMPILER not set`

**Solution**:
```bash
# Ubuntu/Debian
sudo apt-get install build-essential

# Fedora
sudo dnf install gcc-c++

# macOS
xcode-select --install
```

---

### Q: PySide6 installation fails

**Solution**: Ensure you have Python 3.10 or higher:
```bash
python3 --version
```

If using an older Python version, upgrade Python or create a new virtual environment with a supported version.

---

## General Usage

### Q: How do I change the notes folder?

Go to `Settings` → `General` tab → `Default folder for notes` and select your preferred directory.

---

### Q: How do I change the theme?

Go to `Settings` → `General` tab → `Theme` and select from 6 available themes.

---

### Q: Can I use custom fonts?

Font size can be adjusted in `Settings` → `General` tab → `Font Size` slider (range: 5-42). Custom font families are not currently supported.

---

### Q: How do I show/hide line numbers?

Go to `Settings` → `Editor` tab → `Show Line Numbers` checkbox.

---

### Q: Does Notolog auto-save my work?

Yes, Notolog automatically saves your work periodically. This is a built-in feature and does not require configuration.

---

## AI Assistant Issues

### Q: Model takes very long to load (ONNX)

First-time ONNX model loading can take **up to 60 seconds**. Subsequent loads are faster due to caching. A loading message is displayed during initialization.

---

### Q: Out of memory with local LLMs

**Solutions**:
1. Use smaller quantized models (e.g., `Q4_K_M` instead of `Q8_0`)
2. Close other applications to free RAM
3. Reduce context window size in settings
4. Consider using the OpenAI API instead

---

### Q: "Model not found" error

**Causes**:
* Incorrect model path in settings
* Model files are corrupted or incomplete
* Insufficient file permissions

**Solution**: Verify the model path in Settings and ensure all required model files are present.

---

### Q: OpenAI API returns errors

**Common causes**:
* Invalid API key
* Exceeded rate limits or quota
* Network connectivity issues

**Solution**: Verify your API key in Settings and check your OpenAI account status.

---

## File & Encryption Issues

### Q: I forgot my encryption password

**Unfortunately, there is no password recovery**. Notolog uses strong encryption (AES-128 with PBKDF2) specifically to protect your data. Always keep secure backups of important encrypted files.

---

### Q: File won't open after encryption

Ensure you're entering the exact password used during encryption. Passwords are case-sensitive.

---

### Q: Can I decrypt files outside of Notolog?

Encrypted files use the Fernet encryption format. While technically possible to decrypt programmatically, Notolog is the recommended interface for managing encrypted files.

---

## Getting Help

* **Documentation**: [notolog.app](https://notolog.app)
* **GitHub Issues**: [Report bugs or request features](https://github.com/notolog/notolog-editor/issues){:target="_blank"}
* **GitHub Discussions**: [Ask questions and discuss](https://github.com/notolog/notolog-editor/discussions){:target="_blank"}
* **Repository**: [github.com/notolog/notolog-editor](https://github.com/notolog/notolog-editor){:target="_blank"}

---

*Can't find your answer? [Start a discussion](https://github.com/notolog/notolog-editor/discussions){:target="_blank"} on GitHub.*
