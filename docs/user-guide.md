<!-- {"notolog.app": {"created": "2026-01-18 13:57:00.794379", "updated": "2026-01-18 13:57:00.794379"}} -->
# User Guide

Complete guide to all Notolog features and functionality.

## Table of Contents

- [Markdown Editing](#markdown-editing)
- [View Mode](#view-mode)
- [File Management](#file-management)
- [Search Features](#search-features)
- [Encryption](#encryption)
- [Themes](#themes)
- [Multi-Language Support](#multi-language-support)
- [Settings Overview](#settings-overview)

---

## Markdown Editing

### Syntax Highlighting

Notolog provides real-time syntax highlighting for:

- **Headers** (`# H1`, `## H2`, etc.)
- **Bold** (`**text**`) and *Italic* (`*text*`)
- **Code blocks** (fenced with ``` or indented)
- **Links** (`[text](url)`)
- **Lists** (ordered and unordered)
- **Blockquotes** (`> quote`)
- **Tables**
- **TODO items** (`@todo`)

### Supported Markdown Extensions

Notolog uses the Python Markdown library with these extensions:

| Extension | Description |
|-----------|-------------|
| `extra` | Abbreviations, attribute lists, definition lists, fenced code, footnotes, tables, Markdown in HTML |
| `toc` | Table of Contents with header anchors |
| `codehilite` | Syntax highlighting for code blocks |

### Code Blocks

Fenced code blocks with language specification:

~~~markdown
```python
def hello():
    print("Hello, Notolog!")
```
~~~

### TODO Highlighting

Mark tasks with `@todo`:

```markdown
@todo Review documentation
@todo Add more examples
```

These are highlighted for easy identification.

---

## View Mode

Toggle between Edit and View modes:

- **Edit Mode**: Write and modify Markdown
- **View Mode**: See rendered HTML output

### View Features

- Rendered Markdown with proper styling
- Clickable links (opens in browser)
- Syntax-highlighted code blocks
- Image display (local and remote)
- Table formatting

### Image Handling

Images are automatically:
1. Cached in memory for fast display
2. Optionally saved to a local `images` directory
3. Displayed with proper scaling

Configure in `Settings` → `Viewer` tab → `Auto-save external images to disk`.

---

## File Management

### File Tree

The left panel shows your notes directory:

- **Folders**: Displayed with folder icon
- **Markdown files**: `.md`, `.txt`, `.htm`, `.html`
- **Encrypted files**: `.enc` extension

### Creating Files and Folders

**New File**:
- Right-click → `New File`
- Or use toolbar

**New Folder**:
- Right-click → `New Folder`

### Renaming and Deleting

- Right-click on file/folder → `Rename` or `Delete`
- Confirmation dialog prevents accidental deletion

### File Meta-Headers

Notolog stores metadata in HTML comment headers:

```html
<!-- {"notolog.app": {"created": "2024-01-15 10:30:00", "updated": "2024-01-15 14:45:00"}} -->
# My Note
```

This preserves:
- Creation timestamp
- Last modification time
- Future: Custom metadata

---

## Search Features

### In-File Search

Press `Ctrl+F` to open the search bar:

- **Case Sensitive**: Toggle with button
- **Navigation**: Previous/Next match buttons
- **Counter**: Shows "X of Y" matches

### Quick File Filter

Type in the file tree search box to filter:

- Filters by filename
- Real-time filtering
- Clear with `X` button or `Esc`

---

## Encryption

Notolog provides AES-128 encryption for sensitive notes.

### Encryption Details

| Property | Value |
|----------|-------|
| Algorithm | AES-128 CBC (via Fernet) |
| Key Derivation | PBKDF2HMAC with SHA-256 |
| Iterations | 768,000 |
| Salt | 32 bytes, cryptographically random |

### Encrypting a File

1. Open the file you want to encrypt
2. Go to `File` → `Encrypt File` (or toolbar button)
3. Enter a strong password
4. Optionally add a password hint
5. File is saved with `.enc` extension

### Opening Encrypted Files

1. Click on `.enc` file
2. Enter your password
3. File decrypts in memory
4. Edit and save as normal

### Password Best Practices

- Use strong, unique passwords
- Consider a password manager
- Password hints are stored unencrypted
- No password recovery - keep backups!

---

## Themes

Notolog includes 6 built-in themes:

| Theme | Description |
|-------|-------------|
| **Default** | Clean, neutral design |
| **Calligraphy** | Rice paper aesthetic with ink-style text |
| **Nocturne** | Dark theme for night work |
| **Noir Dark** | High-contrast dark theme |
| **Spooky** | Halloween-inspired colors |
| **Strawberry** | Playful, warm colors |

### Changing Themes

`Settings` → `General` tab → `Theme`

Changes apply immediately.

---

## Multi-Language Support

Notolog supports 18 languages:

- English (default)
- Chinese (Simplified) - 简体中文
- Dutch - Nederlands
- Finnish - Suomi
- French - Français
- Georgian - ქართული
- German - Deutsch
- Greek - Ελληνικά
- Hindi - हिन्दी
- Italian - Italiano
- Japanese - 日本語
- Korean - 한국어
- Latin - Latina
- Portuguese - Português
- Russian - Русский
- Spanish - Español
- Swedish - Svenska
- Turkish - Türkçe

### Changing Language

`Settings` → `General` → `Language`

Restart may be required for full effect.

---

## Settings Overview

Access via `Settings` menu or toolbar.

### General Tab

- **Language**: UI language
- **Theme**: Visual theme selection
- **Default folder for notes**: Primary directory for notes
- **Show Main Menu**: Toggle main menu visibility
- **Status Bar options**: Navigation arrows, cursor position
- **Font Size**: Adjust text size (range: 5-42)

### Editor Tab

- **Show Line Numbers**: Display line numbers in editor

### Viewer Tab

- **Convert Text Emojis to Graphics**: Render emojis graphically
- **Highlight TODOs**: Emphasize @todo tags
- **Require Confirmation to Open Links**: Confirm before opening external links
- **Auto-save external images to disk**: Save downloaded images locally

### AI Config Tab

- **Active Inference Module**: Select AI backend
- **Multi-turn dialogue**: Enable conversational memory
- **Convert result to Markdown**: Format AI output as Markdown

See [AI Assistant Guide](ai-assistant.md) for AI module-specific settings.

---

*For AI features, continue to the [AI Assistant Guide](ai-assistant.md).*
