<!-- {"notolog.app": {"created": "2026-01-18 13:57:00.794379", "updated": "2026-01-31 00:00:00.000000"}} -->
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

### Q: "zsh: no matches found" when installing extras on macOS

**Error**: `zsh: no matches found: notolog[llama]`

**Cause**: zsh (the default macOS shell) interprets square brackets as glob patterns.

**Solution**:
```bash
# Quote the package specification
pip install "notolog[llama]"

# Or install llama-cpp-python separately
pip install llama-cpp-python
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

### Q: Module llama.cpp model loading hangs on macOS

**Apple Silicon (M1/M2/M3/M4)**: Works automatically with Metal GPU acceleration. Set GPU Layers to "Auto" or "-1" in settings.

**Intel Mac**: If you experience hangs or crashes, try:
1. Set GPU Layers to "0" (CPU-only mode) in Settings → Module llama.cpp
2. If issues persist, downgrade llama-cpp-python:
   ```bash
   pip install llama-cpp-python==0.2.90 --force-reinstall
   ```

---

### Q: Out of memory with local LLMs

**For ONNX models**: Notolog automatically handles memory issues:
1. Falls back from GPU to CPU when model loading fails
2. Reduces response token limit when generator allocation fails

**If issues persist**:
1. Use smaller quantized models (e.g., `Q4_K_M` instead of `Q8_0`)
2. Reduce "Maximum Response Tokens" in AI module settings
3. Close other applications to free RAM/VRAM
4. Manually select CPU provider in ONNX settings

---

### Q: ONNX model won't load (transformers.js models)

**Error**: `Model not found` or `error opening genai_config.json`

**Cause**: Models optimized for transformers.js have a different directory structure than what onnxruntime-genai expects.

**Solution**: Use models specifically built for onnxruntime-genai that include `genai_config.json`:

* [Microsoft official models](https://huggingface.co/microsoft){:target="_blank"} (Phi-3, etc.)
* Models with "onnx-genai" or "onnxruntime-genai" in the name
* Example: Download `microsoft/Phi-3-mini-4k-instruct-onnx`, then set path to the `cpu_and_mobile/cpu-int4-rtn-block-32` subdirectory

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
