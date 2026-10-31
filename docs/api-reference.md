# API Reference

Source guide for contributors extending Notolog. These are internal interfaces; use the
implementation from the application version you are targeting.

## Module Architecture

Modules live under `notolog/modules/<module_name>/`. The
[module loader](https://github.com/notolog/notolog-editor/blob/main/notolog/modules/modules.py)
discovers directories containing `module_core.py`, imports their package, and checks its
`is_available()` function. Available packages expose `ModuleCore`.

- [BaseCore](https://github.com/notolog/notolog-editor/blob/main/notolog/modules/base_core.py)
  defines module identity, extensions, and lexeme location.
- [BaseAiCore](https://github.com/notolog/notolog-editor/blob/main/notolog/modules/base_ai_core.py)
  additionally requires `get_prompt_manager()` and `request()`.
- [OpenAI API](https://github.com/notolog/notolog-editor/tree/main/notolog/modules/openai_api),
  [ONNX](https://github.com/notolog/notolog-editor/tree/main/notolog/modules/ondevice_llm),
  and [llama.cpp](https://github.com/notolog/notolog-editor/tree/main/notolog/modules/llama_cpp)
  implement AI Assistant integration.
- [Text-to-Speech](https://github.com/notolog/notolog-editor/tree/main/notolog/modules/text_to_speech)
  extends `BaseCore` for speech, settings, and playback integration.

Within a backend, `module_core.py` owns integration, `prompt_manager.py` owns
conversation construction, and `model_helper.py` owns local model loading and
generation. The API backend uses `api_helper.py` for request construction instead.
Its package `__init__.py` exports `ModuleCore` and provides the availability check.

## Creating Custom Modules

Use an existing module with the same extension points as your starting reference.
Implement its package availability check, `ModuleCore`, `module_name`, `extensions`,
and `get_lexemes_path()`.

AI modules also manage their prompt manager, asynchronous requests, dialog signal connections,
and cancellation. Existing implementations use `attach_dialog()`, `parent_closed()`, and
`request_cancelled()`; these are integration methods, not additional abstract methods on `BaseAiCore`.

Cancellation and shutdown must release tasks and native resources without blocking the Qt event loop.
Keep QWidget changes on the GUI thread.

### AI request contract

The existing backends use this request signature:

```python
async def request(self, user_prompt, request_msg_id, response_msg_id,
                  init_callback=None, finished_callback=None):
    ...
```

This is an interface fragment, not a complete module. Create the prompt manager
before a request is accepted and return it from `get_prompt_manager()`. Preserve
the request and response IDs when emitting updates. Existing implementations call
`init_callback()` when generation starts and invoke the completion callback with
`request_msg_id`, `response_msg_id`, and `message_type` keyword arguments.

| Integration point | Responsibility |
|-------------------|----------------|
| `attach_dialog()` | Connect text/usage signals and dialog cancellation/closure; initialize the prompt manager. |
| `request_cancelled()` | Stop the active request and release its resources. |
| `parent_closed()` | Stop work and disconnect signals belonging to the closing dialog. |

Connect module-specific cleanup helpers to the cancellation and shutdown methods above.

## Settings Integration

Register properties through `extend_settings_create_property(extend_func)`, called with
`Settings.create_property`. For example:

```python
@staticmethod
def extend_settings_create_property(extend_func):
    if callable(extend_func):
        extend_func("module_example_text", str, "")
        extend_func("module_example_limit", int, 100)
        extend_func("module_example_enabled", bool, False)
```

`extend_settings_dialog_fields_conf(tab_widget)` creates the tab/layout and returns widget
configuration dictionaries. These use actual Qt widget classes under `type`, object names under
`name`, and callbacks to place widgets in the layout. Use the
[OpenAI settings implementation](https://github.com/notolog/notolog-editor/blob/main/notolog/modules/openai_api/module_core.py)
for the complete schema and translated labels.

For example, inside a module with its lexemes initialized:

```python
from PySide6.QtWidgets import QLabel, QLineEdit, QSpinBox, QVBoxLayout, QWidget

def extend_settings_dialog_fields_conf(self, tab_widget):
    page = QWidget()
    layout = QVBoxLayout(page)
    tab_widget.addTab(page, self.lexemes.get("module_example_tab"))
    return [
        {"type": QLabel, "name": "module_example_text_label",
         "text": self.lexemes.get("module_example_text_label"),
         "callback": layout.addWidget},
        {"type": QLineEdit, "name": "module_example_text_input:module_example_text",
         "callback": layout.addWidget},
        {"type": QSpinBox, "name": "module_example_limit_input:module_example_limit",
         "props": {"setMinimum": 0, "setMaximum": 1000},
         "callback": layout.addWidget},
    ]
```

Register the properties first and add the example label keys to the module's
Python lexeme catalogs. The suffix after `:` binds a control to its settings
property. Give translated controls stable object names and integrate them with
language refresh, as the existing modules do.

Follow the shared language-refresh mechanism so translated controls update without losing settings
or cancelling unrelated operations. Catalogs are Python files under the module's `lexemes/` directory.

## Signal System

Existing AI modules connect these signals to the AI Assistant:

| Signal | Arguments |
|--------|-----------|
| `update_signal` | text, request ID, response ID, message type, message style |
| `update_usage_signal` | model name, input tokens, output tokens, total tokens, incremental-update flag |

Use the application's message enums and the same signal signatures as the target release.
The final usage flag distinguishes incremental streamed counts from replacement totals.

For a complete response and replacement usage totals, the emission forms are:

```python
from notolog.ui.ai_assistant.ai_assistant import EnumMessageType, EnumMessageStyle

self.update_signal.emit(
    "Response text", request_msg_id, response_msg_id,
    EnumMessageType.RESPONSE, EnumMessageStyle.DEFAULT,
)
self.update_usage_signal.emit(
    model_name, input_tokens, output_tokens, total_tokens, False,
)
```

Declare these as Qt signals on the module class, following the backend examples.
Built-in backends use `None` for absent message IDs in text updates, such as
status and error messages.

## Key Classes

```python
from notolog.app_config import AppConfig
from notolog.settings import Settings
from notolog.lexemes.lexemes import Lexemes

version = AppConfig().get_app_version()
logger_level = AppConfig().get_logger_level()
theme = Settings().app_theme
language = Settings().app_language
lexemes = Lexemes(language="en", default_scope="ai_assistant")
title = lexemes.get("dialog_title")
```

Choose lexeme keys from the relevant catalog and scope.
Settings changes emit `Settings.value_changed`; module implementations decide which changes require work.

## Contributing

See [CONTRIBUTING.md](https://github.com/notolog/notolog-editor/blob/main/CONTRIBUTING.md)
for development setup, and [the security policy](https://github.com/notolog/notolog-editor/blob/main/SECURITY.md)
for private vulnerability reporting.
