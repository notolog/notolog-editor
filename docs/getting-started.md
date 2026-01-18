<!-- {"notolog.app": {"created": "2026-01-18 13:57:00.794379", "updated": "2026-01-18 13:57:00.794379"}} -->
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

For Ubuntu/Debian users:

```bash
# Download the latest release
wget https://github.com/notolog/notolog-debian/releases/latest/download/notolog_X.Y.Z_amd64.deb

# Install
sudo dpkg -i notolog_X.Y.Z_amd64.deb
```

### Method 4: From Source

```bash
git clone https://github.com/notolog/notolog-editor.git
cd notolog-editor
python3 -m venv notolog_env
source notolog_env/bin/activate
pip install .
```

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
| New File | `Ctrl+N` | `⌘+N` |
| Save | `Ctrl+S` | `⌘+S` |
| Find | `Ctrl+F` | `⌘+F` |
| Toggle Edit/View | `Ctrl+E` | `⌘+E` |
| Settings | `Ctrl+,` | `⌘+,` |
| AI Assistant | `Ctrl+Shift+A` | `⌘+Shift+A` |

### File Tree Actions

- **Single-click**: Select file
- **Double-click**: Open file
- **Right-click**: Context menu (rename, delete, new file/folder)

### Editor Features

- **Line Numbers**: Click to jump to a line
- **Search**: `Ctrl+F` to find text in the current file
- **Quick Filter**: Type in the file tree search box to filter files

---

## Next Steps

Now that you're set up, explore these features:

1. **[User Guide](user-guide.md)** - Learn all the features
2. **[AI Assistant](ai-assistant.md)** - Set up AI-powered writing help
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

Ensure you have write access to the notes directory:

```bash
chmod 755 ~/Documents/Notes
```

### Python Version Issues

Verify your Python version:

```bash
python3 --version  # Should be 3.10+
```

---

*Need more help? Check the [FAQ](faq.md) or [open an issue](https://github.com/notolog/notolog-editor/issues).*
