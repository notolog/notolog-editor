# Getting Started with Notolog

This guide will help you install Notolog and get up and running quickly.

## Table of Contents

- [Installation Methods](#installation-methods)
- [First Launch](#first-launch)
- [Creating Your First Note](#creating-your-first-note)
- [Basic Navigation](#basic-navigation)
- [Next Steps](#next-steps)

---

## Installation Methods

### Platform Compatibility

Use Python **3.11–3.14**. Notolog's Python wheel is platform-independent, but Qt and AI/audio
dependencies require builds for your operating system and processor. Older Windows and macOS
versions are not supported merely because Python installs on them. Python 3.11 uses Qt for
Python 6.11.3; Python 3.12 and later use Qt for Python 6.12. The dependency installer selects
the compatible version automatically. Check the corresponding
[6.11.3](https://pypi.org/project/PySide6-Essentials/6.11.3/#files) or
[6.12.0 release files](https://pypi.org/project/PySide6-Essentials/6.12.0/#files) and
[Qt platform guidance](https://doc.qt.io/qt-6/supported-platforms.html).
Debian packages have their own architecture and distribution requirements listed with each release.

### Method 1: pip (Recommended)

The simplest way to install Notolog is via pip:

```bash
# Create a virtual environment (recommended)
python3 -m venv notolog_env

# Activate the environment
source notolog_env/bin/activate  # Linux/macOS
notolog_env\Scripts\activate     # Windows

# Install Notolog
pip install notolog

# Or with llama.cpp support for GGUF models
pip install "notolog[llama]"

# Or with both llama.cpp and speech playback dependencies
pip install "notolog[llama,tts]"

# Upgrade to latest version
pip install --upgrade notolog

# Uninstall
pip uninstall notolog
```

### Method 2: Conda

```bash
# Create and activate environment
conda create -n notolog_env python=3.11
conda activate notolog_env

# Install from conda-forge
conda install notolog -c conda-forge
```

### Method 3: Debian Package

Download the `.deb` for your architecture from the
[Debian package releases](https://github.com/notolog/notolog-debian/releases).
Check its supported distribution before installing. From the download directory, replace the
filename below with the exact downloaded filename:

```bash
sudo apt install ./notolog_VERSION_ARCH.deb
```

APT resolves the package's declared system dependencies.

### Method 4: From Source

```bash
git clone https://github.com/notolog/notolog-editor.git
cd notolog-editor
python3 -m venv notolog_env
source notolog_env/bin/activate
pip install .
```

To include both optional backends from the checkout, use `pip install ".[llama,tts]"` instead of
`pip install .`. The speech runtime and models are separate downloads; see the
[Text-to-Speech setup guide](text-to-speech.md).

---

## First Launch

After installation, start Notolog:

```bash
notolog
```

Or from source:

```bash
python -m notolog.app
```

On first launch, you'll see the main editor window with:

1. **File Tree** (left panel) - Navigate your notes
2. **Editor Area** (center) - Write and edit Markdown
3. **Toolbar** (top) - Quick access to common actions
4. **Status Bar** (bottom) - File information and navigation

---

## Creating Your First Note

1. **Set a Notes Directory**:
   - Go to `Settings` → `General` → `Default folder for notes`
   - Choose or create a directory for your notes

2. **Create a New File**:
   - Right-click in the file tree → `New File`
   - Or use the toolbar button

3. **Start Writing**:
   ```markdown
   # My First Note

   This is a **Markdown** note created with Notolog!

   ## Features I Like
   - Syntax highlighting
   - Auto-save
   - Clean interface
   ```

4. **Switch to View Mode**:
   - Click the View/Edit toggle in the toolbar
   - See your Markdown rendered as HTML

---

## Basic Navigation

### Keyboard Shortcuts

| Action | Windows/Linux | macOS |
|--------|---------------|-------|
| Save | `Ctrl+S` | `Cmd+S` |
| Find | `Ctrl+F` | `Cmd+F` |
| Go to line | `Ctrl+G` | `Cmd+G` |

On macOS, `Cmd` is the Command key (`⌘`). See **Settings > Workspace > Hotkeys**
or the [keyboard shortcut reference](user-guide.md#keyboard-shortcuts) for more combinations.

### File Tree Actions

- **Single-click**: Open file
- **Right-click**: Context menu (rename, delete, new file/folder)

### Editor Features

- **Line Numbers**: Show each line's position in the document
- **Search**: `Ctrl+F` (`Cmd+F` on macOS) to find text in the current file
- **Quick Filter**: Type in the file tree search box to filter files

---

## Next Steps

Now that you're set up, explore these features:

1. **[User Guide](user-guide.md)** - Learn all the features
2. **[AI Assistant](ai-assistant.md)** - Chat with AI models locally or via API
3. **[Configuration](configuration.md)** - Customize themes and settings
4. **[File Encryption](user-guide.md#encryption)** - Secure sensitive notes

---

## Troubleshooting First Launch

### Qt Platform Plugin Error (Linux)

If you see: `qt.qpa.plugin: Could not load the Qt platform plugin "xcb"`

```bash
sudo apt-get install -y libxcb-cursor0
```

### Permission Errors

Choose a notes directory owned by your user account with write access. Check ownership and permissions
in your file manager; do not make private notes readable by other users to solve a write-access problem.

### Python Version Issues

Verify your Python version:

```bash
python3 --version  # Supported: 3.11–3.14
```

---

*Need more help? Check the [FAQ](faq.md) or [start a discussion](https://github.com/notolog/notolog-editor/discussions).*
