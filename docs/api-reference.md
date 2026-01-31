<!-- {"notolog.app": {"created": "2026-01-18 13:57:00.794379", "updated": "2026-01-31 00:00:00.000000"}} -->
# API Reference

Developer documentation for extending and integrating with Notolog.

## Table of Contents

- [Module Architecture](#module-architecture)
- [Creating Custom Modules](#creating-custom-modules)
- [Settings Integration](#settings-integration)
- [Signal System](#signal-system)
- [Key Classes](#key-classes)
- [Contributing](#contributing)

---

## Module Architecture

Notolog uses a modular architecture for AI backends and extensions:

```
notolog/modules/
├── base_core.py         # Base module class
├── base_ai_core.py      # AI module base class
├── modules.py           # Module loader and registry
├── openai_api/          # OpenAI API module
│   ├── module_core.py   # Module implementation
│   ├── api_helper.py    # API client
│   └── prompt_manager.py
├── ondevice_llm/        # ONNX Runtime module
│   ├── module_core.py
│   ├── model_helper.py  # Model loading and inference
│   └── prompt_manager.py
└── llama_cpp/           # Module llama.cpp
    ├── module_core.py
    ├── model_helper.py
    └── prompt_manager.py
```

---

## Creating Custom Modules

### Base Class

All AI modules extend `BaseAiCore`:

```python
from notolog.modules.base_ai_core import BaseAiCore

class ModuleCore(BaseAiCore):
    """Custom AI module implementation."""

    module_name = 'My Custom Module'
    extensions = ['ai_assistant', 'settings_dialog']

    def __init__(self, parent=None):
        super().__init__(parent)
        # Initialize your module

    def get_prompt_manager(self):
        """Return the prompt manager instance."""
        return self.prompt_manager

    async def request(self, user_prompt, request_msg_id, response_msg_id,
                      init_callback=None, finished_callback=None):
        """
        Handle inference requests.

        Args:
            user_prompt: The user's input text
            request_msg_id: ID for the request message
            response_msg_id: ID for the response message
            init_callback: Called when inference starts
            finished_callback: Called when inference completes
        """
        # Implement inference logic
        pass
```

### Required Methods

| Method | Description |
|--------|-------------|
| `get_prompt_manager()` | Return the prompt manager instance |
| `request()` | Handle inference requests (async) |
| `attach_dialog()` | Connect to AI Assistant dialog |

### Optional Methods

| Method | Description |
|--------|-------------|
| `is_model_loaded()` | Check if model is initialized |
| `cleanup()` | Release resources when module is unloaded |
| `cancel_request()` | Cancel ongoing inference |

---

## Settings Integration

Modules can extend the settings dialog dynamically:

```python
@staticmethod
def extend_settings_create_property(extend_func):
    """Register custom settings properties."""
    if callable(extend_func):
        # Add a string setting
        extend_func("my_module_setting", str, "default_value")
        # Add an integer setting
        extend_func("my_module_number", int, 100)
        # Add a boolean setting
        extend_func("my_module_enabled", bool, True)
```

### Settings Dialog Fields

```python
def extend_settings_dialog_fields_conf(self, tab_widget) -> list:
    """Return configuration for settings UI fields."""
    return [
        {
            'type': 'line_edit',
            'key': 'my_module_setting',
            'label': 'My Setting',
            'tooltip': 'Description of this setting'
        },
        {
            'type': 'spin_box',
            'key': 'my_module_number',
            'label': 'Number Value',
            'min': 0,
            'max': 1000
        }
    ]
```

---

## Signal System

AI modules use Qt signals for UI communication:

### Update Signal

```python
from PySide6.QtCore import Signal

# Emit text updates to the UI
update_signal = Signal(str, object, object, EnumMessageType, EnumMessageStyle)

# Usage:
self.update_signal.emit(
    "Response text",           # Message content
    request_msg_id,            # Request message ID (or -1 for None)
    response_msg_id,           # Response message ID (or -1 for None)
    EnumMessageType.DEFAULT,   # Message type
    EnumMessageStyle.DEFAULT   # Message style
)
```

### Usage Signal

```python
# Emit token usage statistics
update_usage_signal = Signal(str, object, object, object, object)

# Usage:
self.update_usage_signal.emit(
    "usage",          # Signal type
    input_tokens,     # Input token count
    output_tokens,    # Output token count
    total_tokens,     # Total token count
    model_name        # Model identifier
)
```

---

## Key Classes

### AppConfig

Singleton for application configuration:

```python
from notolog.app_config import AppConfig

config = AppConfig()
version = config.get_app_version()
logger_level = config.get_logger_level()
```

### Settings

User settings management:

```python
from notolog.settings import Settings

settings = Settings()
theme = settings.theme
language = settings.app_language
```

### Lexemes

Internationalization support:

```python
from notolog.lexemes.lexemes import Lexemes

lexemes = Lexemes(language='en', scope='ai_assistant')
text = lexemes.get('dialog_title')
```

---

## Contributing

For contribution guidelines, see:
- [Contributing Guidelines](https://github.com/notolog/notolog-editor/blob/main/CONTRIBUTING.md){:target="_blank"}
- [Code of Conduct](https://github.com/notolog/notolog-editor/blob/main/CODE_OF_CONDUCT.md){:target="_blank"}

---

*For user documentation, see [User Guide](user-guide.md).*
