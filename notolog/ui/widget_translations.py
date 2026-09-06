"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Shared language updates for widgets using Lexemes catalogues.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QLabel, QAbstractButton, QScrollArea

from .label_with_hint import LabelWithHint


class WidgetTranslations(QObject):
    language_changed = Signal()

    def __init__(self, parent, settings, load_catalog):
        super().__init__(parent)
        self.settings = settings
        self.load_catalog = load_catalog
        self.lexemes = load_catalog(settings.app_language)
        self.bindings = []
        settings.value_changed.connect(self.settings_changed)

    def get(self, key, *, scope=None, **values):
        return self.lexemes.get(key, scope=scope, **{
            name: value() if callable(value) else value for name, value in values.items()})

    def bind(self, setter, key, **values):
        """Retain a stable key for a widget property, including formatted text."""
        self.bindings.append((setter, key, values))
        setter(self.get(key, **values))

    def settings_changed(self, values):
        if 'app_language' not in values:
            return
        self.lexemes = self.load_catalog(self.settings.app_language)
        for setter, key, values in self.bindings:
            setter(self.get(key, **values))
        self.language_changed.emit()

    def bind_named_widgets(self, root, *, format_text, set_tab_text):
        """Use the settings dialog's scope_key:setting_name naming convention."""
        for obj in root.findChildren(QObject):
            name = obj.objectName().split(':', 1)[0]
            if not name:
                continue
            for scope, entries in self.lexemes.get_all().items():
                key = name.removeprefix(scope + '_')
                if key in entries:
                    if isinstance(obj, QLabel):
                        self.bind(lambda text, obj=obj: obj.setText(format_text(obj, text)), key, scope=scope)
                    elif isinstance(obj, QAbstractButton):
                        if obj.text():
                            self.bind(obj.setText, key, scope=scope)
                        if obj.toolTip():
                            self.bind(obj.setToolTip, key, scope=scope)
                    elif isinstance(obj, QScrollArea):
                        self.bind(lambda text, name=name: set_tab_text(name, text), key, scope=scope)
                if isinstance(obj, LabelWithHint):
                    tooltip_key = obj.property('tooltip_lexeme')
                    if tooltip_key in entries:
                        self.bind(obj.set_tooltip, tooltip_key, scope=scope)
                for suffix, method in (('_placeholder_text', 'setPlaceholderText'),
                                       ('_accessible_description', 'setAccessibleDescription')):
                    setter = getattr(obj, method, None)
                    if callable(setter) and key + suffix in entries:
                        self.bind(setter, key + suffix, scope=scope)
