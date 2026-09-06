"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Text-to-Speech module registration and settings integration.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from ..base_core import BaseCore
from .config import speech_settings
from .i18n import LEXEMES_PATH, tr


class ModuleCore(BaseCore):
    module_name = 'Text-to-Speech'
    extensions = ['settings_dialog', 'text_to_speech']

    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = speech_settings()

    @staticmethod
    def get_lexemes_path():
        return str(LEXEMES_PATH)

    def extend_settings_dialog_fields_conf(self, tab_widget):
        from PySide6.QtWidgets import QScrollArea
        from .settings_widget import SpeechSettingsWidget
        scroll = QScrollArea(tab_widget)
        scroll.setFont(tab_widget.font())
        scroll.setWidgetResizable(True)
        widget = SpeechSettingsWidget(scroll)
        scroll.setWidget(widget)
        tab_widget.addTab(scroll, tr('module_text_to_speech_name'))
        widget.translations.bind(lambda text: tab_widget.setTabText(tab_widget.indexOf(scroll), text),
                                 'module_text_to_speech_name', scope='common')
        return []
