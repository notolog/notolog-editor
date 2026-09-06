"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Text-to-Speech settings, model setup, and operation feedback.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

import asyncio
import re
import time
from pathlib import Path

from shiboken6 import isValid
from PySide6.QtCore import QUrl, Qt, QTimer, QEvent, QSignalBlocker
from PySide6.QtGui import QDesktopServices, QColor
from PySide6.QtWidgets import (
    QWidget, QFormLayout, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QCheckBox, QDoubleSpinBox, QFrame, QToolButton,
    QGridLayout, QSizePolicy, QGraphicsOpacityEffect, QSlider, QMessageBox,
)

from ...ui.label_with_hint import LabelWithHint
from ...ui.widget_translations import WidgetTranslations
from ...ui.translated_log import TranslatedLog
from ...ui.file_path_line_edit import FilePathLineEdit
from ...ui.dir_path_line_edit import DirPathLineEdit
from ...ui.horizontal_line_spacer import HorizontalLineSpacer
from ...ui.enum_combo_box import EnumComboBox
from ...helpers.theme_helper import ThemeHelper
from .config import speech_settings, runtime_path, model_directory, model_paths, CONTEXT_LENGTHS, audio_requirements
from .config import default_model_directory
from .runtime import download_models, validate_runtime
from .playback_bar import SpeechActivity
from .languages import SpeechLanguage
from .i18n import catalog, language_label


class SpeechButton(QPushButton):
    """Make disabled actions visibly inactive even with a theme's custom button colors."""

    def __init__(self, text):
        super().__init__(text)
        self.fade = QGraphicsOpacityEffect(self)
        self.fade.setOpacity(1.0)
        self.setGraphicsEffect(self.fade)

    def changeEvent(self, event):
        if event.type() == QEvent.Type.EnabledChange:
            self.fade.setOpacity(1.0 if self.isEnabled() else 0.4)
        super().changeEvent(event)


class SpeechSettingsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        if parent:
            self.setFont(parent.font())
        self.settings = speech_settings()
        self.translations = WidgetTranslations(
            self, self.settings, lambda language: catalog(language, default_scope='settings_dialog'))
        self._message_translation = None
        self._model_directory = model_directory(self.settings)
        self._close_approved = False
        self.task = None
        self.operation = None
        self.completed_files = 0
        self.active_file = False
        self.fields = []
        self.setObjectName('settings_dialog_text_to_speech')
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        title = QLabel()
        self.translations.bind(title.setText, 'module_text_to_speech_name', scope='common')
        title.setObjectName('speech_tab_title')
        title.setProperty('class', 'group-header-label')
        layout.addWidget(title)
        enabled = QCheckBox()
        self.translations.bind(enabled.setText, 'module_text_to_speech_config_enabled_label')
        enabled.setObjectName('tts_enabled')
        enabled.setChecked(self.settings.tts_enabled)
        enabled.toggled.connect(lambda value: setattr(self.settings, 'tts_enabled', value))
        layout.addWidget(enabled)
        self.heading(layout, 'module_text_to_speech_config_setup_label',
                     'module_text_to_speech_config_setup_accessible_description')
        form = self.form(layout)
        self.path(form, 'module_text_to_speech_config_runtime_label', 'tts_runtime_path', False,
                  'module_text_to_speech_config_runtime_input_accessible_description')
        self.runtime_link = QLabel()
        self.translations.bind(lambda text: self.runtime_link.setText(
            '<a href="https://github.com/NVIDIA/NeMo-Speech.cpp/releases/tag/v0.1.0">' + text + '</a>'),
                               'module_text_to_speech_config_get_runtime_link', version='0.1.0')
        self.runtime_link.linkActivated.connect(lambda url: QDesktopServices.openUrl(QUrl(url)))
        form.addRow('', self.runtime_link)
        self.path(form, 'module_text_to_speech_config_model_directory_label', 'tts_model_directory',
                  True,
                  'module_text_to_speech_config_model_directory_input_accessible_description')

        self.panel = QFrame()
        self.panel.setObjectName('speech_operation_panel')
        self.panel.setStyleSheet(
            'QFrame#speech_operation_panel { border: 1px solid palette(mid); border-radius: 6px; }')
        panel_row = QGridLayout(self.panel)
        panel_row.setContentsMargins(12, 10, 12, 10)
        panel_row.setColumnStretch(1, 1)
        self.status_icon = QLabel()
        panel_row.addWidget(self.status_icon, 0, 0, alignment=Qt.AlignmentFlag.AlignVCenter)
        self.activity = SpeechActivity(scale=1)
        policy = self.activity.sizePolicy()
        policy.setRetainSizeWhenHidden(True)
        self.activity.setSizePolicy(policy)
        panel_row.addWidget(self.activity, 1, 0, alignment=Qt.AlignmentFlag.AlignVCenter)
        status_row = QHBoxLayout()
        self.status = QLabel()
        self.status.setTextFormat(Qt.TextFormat.PlainText)
        self.status.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.status.setWordWrap(True)
        self.status.setMinimumWidth(0)
        self.status.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        status_row.addWidget(self.status, 1)
        self.details = QToolButton()
        self.translations.bind(self.details.setText, 'module_text_to_speech_config_details_label')
        self.translations.bind(self.details.setToolTip, 'module_text_to_speech_config_details_accessible_description')
        self.details.setCheckable(True)
        self.details.setChecked(True)
        self.details.setArrowType(Qt.ArrowType.DownArrow)
        self.details.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.details.toggled.connect(self.show_details)
        status_row.addWidget(self.details, alignment=Qt.AlignmentFlag.AlignVCenter)
        panel_row.addLayout(status_row, 0, 1)
        self.progress_status = QLabel()
        self.progress_status.setTextFormat(Qt.TextFormat.PlainText)
        self.progress_status.setWordWrap(True)
        self.progress_status.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        panel_row.addWidget(self.progress_status, 1, 1)
        self.output = TranslatedLog(self.translations)
        self.output.setObjectName('qt_tts_status')
        self.translations.bind(self.output.setAccessibleName, 'module_text_to_speech_config_details_label')
        panel_row.addWidget(self.output, 2, 1)
        actions = QHBoxLayout()
        model_label = QLabel('MagpieTTS')
        actions.addWidget(model_label)
        license_link = QLabel()
        self.translations.bind(lambda text: license_link.setText(
            '<a href="https://www.nvidia.com/en-us/agreements/enterprise-software/'
            'nvidia-open-model-license/">' + text + '</a>'),
                               'module_text_to_speech_config_model_license_label')
        license_link.linkActivated.connect(lambda url: QDesktopServices.openUrl(QUrl(url)))
        actions.addWidget(license_link)
        actions.addStretch()
        self.download = SpeechButton(self.lexemes.get('module_text_to_speech_config_download_models_button'))
        self.download.clicked.connect(self.download_clicked)
        actions.addWidget(self.download)
        panel_row.addLayout(actions, 3, 1)
        layout.addWidget(self.panel)

        self.advanced = QWidget()
        advanced_form = self.form(QVBoxLayout(self.advanced))
        self.path(advanced_form, None, 'tts_magpie_path', False, literal_title='Magpie (.gguf)')
        self.path(advanced_form, None, 'tts_codec_path', False, literal_title='NanoCodec (.gguf)')
        self.path(advanced_form, 'module_text_to_speech_config_tokenizer_directory_label',
                  'tts_tokenizer_directory', True)
        self.advanced_toggle = QToolButton()
        self.translations.bind(self.advanced_toggle.setText, 'module_text_to_speech_config_custom_models_label')
        self.translations.bind(self.advanced_toggle.setToolTip,
                               'module_text_to_speech_config_custom_models_accessible_description')
        self.advanced_toggle.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.advanced_toggle.setCheckable(True)
        self.advanced_toggle.setArrowType(Qt.ArrowType.RightArrow)
        self.advanced_toggle.toggled.connect(self.toggle_advanced)
        layout.addWidget(self.advanced_toggle, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.advanced)
        self.advanced.hide()
        layout.addWidget(HorizontalLineSpacer(self))
        self.heading(layout, 'module_text_to_speech_config_reading_label',
                     'module_text_to_speech_config_reading_accessible_description')
        reading = self.form(layout)
        self.language = EnumComboBox(SpeechLanguage)
        for index, language in enumerate(SpeechLanguage):
            self.language.setItemText(index, language_label(language))
        self.language.setObjectName('tts_language')
        self.language.setCurrentIndex(list(SpeechLanguage).index(SpeechLanguage.from_code(self.settings.tts_language)))
        self.language.currentIndexChanged.connect(
            lambda _: setattr(self.settings, 'tts_language', self.language.currentData().name.lower()))
        reading.addRow(self.hint('module_text_to_speech_config_language_label',
                                 'module_text_to_speech_config_language_input_accessible_description'), self.language)
        self.fields.append(self.language)
        voice = QLineEdit(self.settings.tts_voice)
        voice.setObjectName('tts_voice')
        voice.textChanged.connect(lambda value: setattr(self.settings, 'tts_voice', value.strip()))
        reading.addRow(self.hint('module_text_to_speech_config_voice_label',
                                 'module_text_to_speech_config_voice_input_accessible_description'),
                       voice)
        self.fields.append(voice)
        speed = QDoubleSpinBox()
        speed.setObjectName('tts_speed')
        speed.setRange(0.5, 2.0)
        speed.setSingleStep(0.1)
        speed.setSuffix(' ×')
        self.translations.bind(speed.setToolTip, 'module_text_to_speech_config_speed_input_accessible_description')
        speed.setValue(self.settings.tts_speed)
        speed.valueChanged.connect(lambda value: setattr(self.settings, 'tts_speed', value))
        reading.addRow(self.label('module_text_to_speech_config_speed_label'), speed)
        self.fields.append(speed)
        context_row = QHBoxLayout()
        context_row.setContentsMargins(0, 0, 8, 0)
        context_row.setSpacing(8)
        self.context = QSlider(Qt.Orientation.Horizontal)
        self.context.setObjectName('qt_tts_context_length')
        self.context.setRange(0, len(CONTEXT_LENGTHS) - 1)
        self.context.setTracking(False)
        saved_context = self.settings.tts_context_length
        self.context.setValue(CONTEXT_LENGTHS.index(saved_context if saved_context in CONTEXT_LENGTHS else 160))
        self.translations.bind(self.context.setAccessibleName, 'module_text_to_speech_config_context_length_label')
        self.context_value = QLabel()
        self.context_value.setMinimumWidth(self.fontMetrics().horizontalAdvance(
            self.lexemes.get('module_text_to_speech_config_context_whole_document')))
        context_row.addWidget(self.context, 1)
        context_row.addWidget(self.context_value)
        self.context.valueChanged.connect(self.context_changed)
        self.context.sliderMoved.connect(self.preview_context)
        self.context_changed(self.context.value())
        reading.addRow(self.hint('module_text_to_speech_config_context_length_label',
                                 'module_text_to_speech_config_context_length_accessible_description'),
                       context_row)
        self.fields.append(self.context)
        for title, name, hint in (
                ('module_text_to_speech_config_announce_headings_label', 'tts_announce_headings',
                 'module_text_to_speech_config_announce_headings_accessible_description'),
                ('module_text_to_speech_config_skip_inline_code_label', 'tts_skip_inline_code',
                 'module_text_to_speech_config_skip_inline_code_accessible_description'),
                ('module_text_to_speech_config_skip_multiline_code_label', 'tts_skip_multiline_code',
                 'module_text_to_speech_config_skip_multiline_code_accessible_description')):
            field = QCheckBox()
            self.translations.bind(field.setText, title)
            field.setObjectName(name)
            field.setChecked(getattr(self.settings, name))
            field.toggled.connect(lambda value, name=name: setattr(self.settings, name, value))
            row = QHBoxLayout()
            row.addWidget(field)
            row.addWidget(self.hint('', hint))
            row.addStretch()
            reading.addRow(row)
            self.fields.append(field)
        self.test = SpeechButton(self.lexemes.get('module_text_to_speech_config_test_voice_button'))
        self.test.clicked.connect(self.test_voice)
        test_row = QHBoxLayout()
        test_row.addWidget(self.test)
        self.test_hint = QLabel()
        self.test_hint.setWordWrap(True)
        test_row.addWidget(self.test_hint, 1)
        layout.addLayout(test_row)
        layout.addStretch()

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.tick)
        self.refresh_timer = QTimer(self)
        self.refresh_timer.setSingleShot(True)
        self.refresh_timer.setInterval(200)
        self.refresh_timer.timeout.connect(self.refresh_setup)
        self.settings.value_changed.connect(self.settings_changed)
        self.translations.language_changed.connect(self.refresh_language)
        self.sync_font()
        self.refresh_setup()
        self.settings_window = self.window()
        self.settings_window.installEventFilter(self)
        self.destroyed.connect(self.cancel_task)

    def sync_font(self):
        if not isValid(self):
            return
        self.setFont(self.window().font())
        # Match SettingsDialog's configured fields, including stylesheet-owned children.
        for child in self.findChildren(QWidget):
            font = self.font()
            font.setBold(child.property('class') == 'group-header-label')
            child.setFont(font)
        for hint in self.findChildren(LabelWithHint):
            hint.load_icon()
        self.output.setFixedHeight(self.fontMetrics().lineSpacing() * 5 + 12)
        self.activity.setFixedSize(self.fontMetrics().height(), self.fontMetrics().height())
        context_labels = [self.lexemes.get('module_text_to_speech_config_context_characters', count=value) for value in
                          CONTEXT_LENGTHS if value]
        context_labels.append(self.lexemes.get('module_text_to_speech_config_context_whole_document'))
        self.context_value.setFixedWidth(max(self.fontMetrics().horizontalAdvance(label) for label in context_labels))
        row_height = max(self.details.sizeHint().height(), self.download.sizeHint().height(), self.activity.height())
        self.status.setMinimumHeight(row_height)
        self.progress_status.setMinimumHeight(row_height)
        for row in (0, 1, 3):
            self.panel.layout().setRowMinimumHeight(row, row_height)
        self.show_details(self.details.isChecked())

    @property
    def lexemes(self):
        return self.translations.lexemes

    def label(self, key):
        label = QLabel()
        self.translations.bind(label.setText, key)
        return label

    def refresh_language(self):
        with QSignalBlocker(self.language):
            for index, language in enumerate(SpeechLanguage):
                self.language.setItemText(index, language_label(language))
        self.preview_context(self.context.sliderPosition())
        self.sync_font()
        if self.operation:
            self.refresh_operation_buttons()
        else:
            self.refresh_controls(rescan=False, update_enabled=False)
        if self._message_translation:
            key, values = self._message_translation
            self.show_message(self.translations.get(key, **values))
        if self.timer.isActive():
            self.tick()

    def heading(self, layout, title, help_text):
        row = QHBoxLayout()
        label = self.label(title)
        label.setProperty('class', 'group-header-label')
        font = label.font()
        font.setBold(True)
        label.setFont(font)
        row.addWidget(label)
        row.addStretch()
        hint = self.hint(title, help_text, block=True)
        row.addWidget(hint)
        layout.addLayout(row)

    def hint(self, title, help_text, parent=None, block=False):
        label = LabelWithHint(parent or self, text='',
                           theme_icon='question-circle.svg' if block else 'info-circle.svg')
        if title and not block:
            self.translations.bind(label.setText, title)
        self.translations.bind(label.set_tooltip, help_text)
        self.translations.bind(label.icon_button.setAccessibleName, 'module_text_to_speech_config_about_label',
                               title=lambda: self.lexemes.get(title or 'module_text_to_speech_config_reading_label'))
        return label

    @staticmethod
    def form(layout):
        form = QFormLayout()
        form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        form.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapLongRows)
        form.setVerticalSpacing(8)
        layout.addLayout(form)
        return form

    def path(self, form, title, name, directory, help_text=None, *, literal_title=''):
        field = (DirPathLineEdit(self, settings=self.settings) if directory else
                 FilePathLineEdit(self, settings=self.settings))
        field.setObjectName(name)
        field.setText(getattr(self.settings, name))
        field.setMinimumWidth(0)
        if directory and name == 'tts_model_directory':
            field.setPlaceholderText(str(default_model_directory()))
        elif name == 'tts_runtime_path':
            self.translations.bind(field.setPlaceholderText,
                                   'module_text_to_speech_config_runtime_input_placeholder_text')
        else:
            self.translations.bind(field.setPlaceholderText,
                                   'module_text_to_speech_config_model_input_placeholder_text')
        for setter in (field.button.setAccessibleName, field.button.setToolTip):
            self.translations.bind(setter, 'module_text_to_speech_config_choose_path_label',
                                   title=lambda: self.lexemes.get(title) if title else literal_title)
        field.textChanged.connect(lambda value: setattr(self.settings, name, value.strip()))
        form.addRow(self.hint(title, help_text) if help_text else self.label(title) if title else literal_title, field)
        self.fields.append(field)

    def toggle_advanced(self, checked):
        self.advanced.setVisible(checked)
        self.advanced_toggle.setArrowType(Qt.ArrowType.DownArrow if checked else Qt.ArrowType.RightArrow)

    def context_changed(self, index):
        self.settings.tts_context_length = CONTEXT_LENGTHS[index]
        self.preview_context(index)

    def preview_context(self, index):
        length = CONTEXT_LENGTHS[index]
        label = self.lexemes.get('module_text_to_speech_config_context_characters',
                                 count=length) if length else self.lexemes.get(
            'module_text_to_speech_config_context_whole_document')
        self.context_value.setText(label)
        self.context.setToolTip(label)

    def show_details(self, visible=True):
        self.output.setVisible(visible)
        self.details.setArrowType(Qt.ArrowType.DownArrow if visible else Qt.ArrowType.RightArrow)

    def settings_changed(self, values):
        if 'app_font_size' in values:
            QTimer.singleShot(0, self.sync_font)
        paths = {'tts_runtime_path', 'tts_model_directory', 'tts_magpie_path',
                 'tts_codec_path', 'tts_tokenizer_directory'}
        if 'tts_model_directory' in values:
            previous = self._model_directory
            self._model_directory = model_directory(self.settings)
            for name in ('tts_magpie_path', 'tts_codec_path', 'tts_tokenizer_directory'):
                value = getattr(self.settings, name)
                if value and Path(value).is_relative_to(previous):
                    self.findChild(QLineEdit, name).clear()
        if paths.intersection(values) and not self.operation:
            self.download.setEnabled(False)
            self.test.setEnabled(False)
            self.refresh_timer.start()
        elif 'tts_enabled' in values and not self.operation:
            self.refresh_controls(rescan=False)

    def have_models(self, *, overrides=True):
        try:
            model_paths(self.settings, overrides=overrides)
            return True
        except (ValueError, OSError):
            return False

    def refresh_controls(self, *, rescan=True, update_enabled=True):
        if rescan:
            self._have_models = self.have_models()
            self._folder_models = self.have_models(overrides=False)
        available = bool(runtime_path(self.settings))
        self.runtime_link.setVisible(not available)
        self.download.setText(self.lexemes.get(
            'module_text_to_speech_config_verify_models_button') if self._folder_models else self.lexemes.get(
            'module_text_to_speech_config_download_models_button'))
        if update_enabled:
            self.download.setEnabled(available)
        self.download.setToolTip(
            self.lexemes.get('module_text_to_speech_config_verify_models_accessible_description') if available
            else self.lexemes.get('module_text_to_speech_config_runtime_required'))
        self.test.setText(self.lexemes.get('module_text_to_speech_config_test_voice_button'))
        requirements = audio_requirements()
        enabled = self.findChild(QCheckBox, 'tts_enabled')
        if update_enabled:
            enabled.setEnabled(not requirements)
        enabled.setToolTip(self.lexemes.get('module_text_to_speech_dependency_required', scope='common',
                                            value=requirements) if requirements else '')
        if update_enabled:
            self.test.setEnabled(not requirements and available and self._have_models and self.settings.tts_enabled)
        reason = (self.lexemes.get('module_text_to_speech_dependency_required', scope='common',
                                   value=requirements) if requirements else
                  self.lexemes.get('module_text_to_speech_config_runtime_required') if not available else
                  self.lexemes.get('module_text_to_speech_config_models_required') if not self._have_models else
                  self.lexemes.get(
                      'module_text_to_speech_config_enable_required') if not self.settings.tts_enabled else '')
        self.test_hint.setText(reason)
        self.test_hint.setVisible(bool(reason))

    def refresh_setup(self):
        if self.operation:
            return
        self.refresh_controls()
        if not runtime_path(self.settings):
            self.report_key('module_text_to_speech_config_status_runtime_missing', 'info')
        elif self._have_models and not self._folder_models:
            self.report_key('module_text_to_speech_config_status_custom_models', 'info')
        elif self._folder_models:
            self.report_key('module_text_to_speech_config_status_models_found', 'info')
        else:
            self.report_key('module_text_to_speech_config_status_models_missing', 'info')

    def download_clicked(self):
        if self.operation == 'download':
            self.cancel_task()
        else:
            self.launch(self._download)

    def launch(self, operation):
        if self.task and not self.task.done():
            return
        self.task = asyncio.get_running_loop().create_task(self._run(operation))

    def refresh_operation_buttons(self):
        self.download.setText(self.lexemes.get(
            'module_text_to_speech_config_cancel_button') if self.operation == 'download' else self.lexemes.get(
            'module_text_to_speech_config_download_models_button'))
        self.download.setEnabled(self.operation == 'download')
        self.test.setText(self.lexemes.get(
            'module_text_to_speech_config_stop_button') if self.operation == 'test' else self.lexemes.get(
            'module_text_to_speech_config_test_voice_button'))
        self.test.setEnabled(self.operation == 'test')

    async def _run(self, operation):
        self.refresh_timer.stop()
        self._close_approved = False
        self.operation = 'test' if operation == self._test_voice else 'download'
        for field in self.fields:
            field.setEnabled(False)
        self.refresh_operation_buttons()
        self.test_hint.hide()
        self.completed_files = 0
        self.started = time.monotonic()
        self.timer.start()
        self.report_key('module_text_to_speech_config_status_checking_runtime', 'busy')
        outcome = 'Complete'
        try:
            await operation()
            outcome = 'Failed' if self.state == 'error' else 'Complete'
        except asyncio.CancelledError:
            outcome = 'Cancelled'
            if self.operation == 'test':
                self.report_key('module_text_to_speech_status_stopped', scope='common')
            else:
                self.report_key('module_text_to_speech_config_status_download_cancelled')
        except Exception as exc:
            if not isValid(self):
                return
            outcome = 'Failed'
            self.append_details(str(exc) + '\n')
            if isinstance(exc, PermissionError):
                self.report_key('module_text_to_speech_config_error_permission_denied', 'error')
            elif isinstance(exc, OSError):
                self.report_key('module_text_to_speech_config_error_file_access', 'error',
                                error=exc.strerror or str(exc))
            else:
                self.report_key('module_text_to_speech_error', 'error', scope='common', error=str(exc))
        finally:
            if isValid(self):
                self.timer.stop()
                self.activity.set_running(False)
                self.progress_status.clear()
                self.status.setText(self.message)
                self.operation = None
                if outcome == 'Complete' and self.state != 'success':
                    self.report(self.message, 'success', translation=self._message_translation)
                for field in self.fields:
                    field.setEnabled(True)
                self.refresh_controls()

    def report_key(self, key, state='info', **values):
        self.report(self.translations.get(key, **values), state, translation=(key, values))

    def show_message(self, message):
        self.message = message
        if len(self.message) > 200:
            self.message = self.message[:200] + '… ' + self.lexemes.get('module_text_to_speech_config_details_label')
        self.status.setText(self.message)
        self.status_icon.setAccessibleName(self.message)

    def report(self, message, state='info', *, translation=None):
        if not isValid(self):
            return
        self._message_translation = translation
        self.state = state
        if state == 'error':
            self.timer.stop()
        self.show_message(message)
        separator = '\n' if self.output.document().lastBlock().text() else ''
        self.append_details(separator)
        if translation:
            key, values = translation
            self.output.append_message(key, **values)
        else:
            self.append_details(message + '\n')
        if self.timer.isActive():
            self.tick()
        else:
            self.progress_status.clear()
        icon = {'error': 'x-square-fill.svg', 'success': 'check-square-fill.svg'}.get(
            state, 'info-square-fill.svg')
        size = self.fontMetrics().height()
        theme = ThemeHelper()
        color = QColor(theme.get_color('settings_dialog_hint_icon_color'))
        self.status_icon.setPixmap(theme.get_icon(theme_icon=icon, color=color).pixmap(size, size))
        self.status_icon.setFixedWidth(size)
        self.activity.set_running(state == 'busy')

    def tick(self):
        elapsed = int(time.monotonic() - self.started)
        files = ''
        if self.operation == 'download':
            files = self.lexemes.get('module_text_to_speech_config_progress_files_complete',
                                     count=self.completed_files) + ' · '
        self.progress_status.setText(files + self.lexemes.get('module_text_to_speech_config_progress_elapsed',
                                                              time=f'{elapsed // 60}:{elapsed % 60:02d}'))

    async def _download(self):
        if not runtime_path(self.settings):
            raise ValueError(self.lexemes.get('module_text_to_speech_config_runtime_required'))
        self.download_started = False
        self.download_pending = ''
        self.completed_files = 0
        self.active_file = False
        self.report_key('module_text_to_speech_config_status_checking_models', 'busy')
        await download_models(self.settings, self.download_output)
        self.completed_files = 3
        for name in ('tts_magpie_path', 'tts_codec_path', 'tts_tokenizer_directory'):
            self.findChild(QLineEdit, name).clear()
        self.report_key(
            'module_text_to_speech_config_status_models_downloaded' if self.download_started else
            'module_text_to_speech_config_status_models_verified', 'success')

    def finish_file(self):
        self.completed_files = min(3, self.completed_files + 1)
        if self.timer.isActive():
            self.tick()

    def download_output(self, output):
        if not isValid(self):
            return
        self.append_details(output)
        # Process complete lines: QProcess may split a status message across reads.
        self.download_pending += output
        lines = self.download_pending.split('\n')
        self.download_pending = lines.pop()[-4096:]
        for line in lines:
            match = re.search(r'\[model\] downloading .*\((\w+), ([\d.]+) MiB\)', line)
            if match:
                if self.active_file:
                    self.finish_file()
                self.active_file = True
                self.download_started = True
                role = {'tts': 'module_text_to_speech_config_download_role_voice',
                        'codec': 'module_text_to_speech_config_download_role_codec',
                        'tokenizer': 'module_text_to_speech_config_download_role_tokenizers'}.get(
                    match[1], 'module_text_to_speech_config_download_role_model')
                self.report_key('module_text_to_speech_config_progress_downloading', 'busy',
                                number=self.completed_files + 1,
                                role=lambda key=role: self.lexemes.get(key), size=match[2])
            elif '[model] cached:' in line:
                if self.active_file:
                    self.finish_file()
                    self.active_file = False
                self.finish_file()
                self.report_key('module_text_to_speech_config_progress_cached', 'busy', count=self.completed_files)
            elif '[model] verifying' in line:
                self.report_key('module_text_to_speech_config_progress_verifying', 'busy',
                                number=self.completed_files + 1)

    def cancel_task(self, *_):
        if self.task and not self.task.done():
            self.task.cancel()

    def editor(self):
        parent = self.parentWidget()
        while parent:
            if hasattr(parent, 'get_speech_controller'):
                return parent
            parent = parent.parentWidget()
        return None

    def test_voice(self):
        if self.operation == 'test':
            self.cancel_task()
        else:
            self.launch(self._test_voice)

    async def _test_voice(self):
        if not self.settings.tts_enabled:
            raise ValueError(self.lexemes.get('module_text_to_speech_config_enable_required'))
        await validate_runtime(self.settings)
        model_paths(self.settings)
        editor = self.editor()
        if not editor:
            raise ValueError(self.lexemes.get('module_text_to_speech_config_editor_required'))
        controller = editor.get_speech_controller()
        controller.status_changed.connect(self.report_status)
        controller.error.connect(self.voice_error)
        controller.details_changed.connect(self.append_details)
        try:
            self.report_key('module_text_to_speech_config_status_testing_voice', 'busy')
            editor.action_read_aloud(source='Welcome to Notolog. This is a test of your reading voice.')
            if controller.task:
                await controller.task
        except asyncio.CancelledError:
            controller.stop()
            raise
        finally:
            if isValid(self):
                controller.status_changed.disconnect(self.report_status)
                controller.error.disconnect(self.voice_error)
                controller.details_changed.disconnect(self.append_details)

    def voice_error(self, message):
        self.report(message, 'error')

    def report_status(self, key):
        active = self.operation == 'test' and key in (
            'module_text_to_speech_status_loading', 'module_text_to_speech_status_preparing',
            'module_text_to_speech_status_reading')
        state = ('error' if key == 'module_text_to_speech_status_unavailable' else
                 'busy' if active else 'info')
        self.report_key(key, state, scope='common')

    def append_details(self, output):
        output = re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]', '', output)
        self.output.append_output(output.replace('\r\n', '\n').replace('\r', '\n'))

    def confirm_close(self):
        if self.task and not self.task.done() and self.operation == 'download' and not self._close_approved:
            answer = QMessageBox.question(
                self, self.lexemes.get('module_text_to_speech_config_cancel_download_title'),
                self.lexemes.get('module_text_to_speech_config_cancel_download_confirmation'),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No)
            if answer != QMessageBox.StandardButton.Yes:
                return False
            self._close_approved = True
            self.cancel_task()
        return True

    def eventFilter(self, watched, event):
        if watched is self.settings_window:
            closing = event.type() == QEvent.Type.Close
            escape = event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Escape
            if (closing or escape) and not self.confirm_close():
                event.ignore()
                return True
        # Observe the window too: closing it must cancel even while this tab is hidden.
        if watched is self.settings_window and event.type() == QEvent.Type.Hide:
            self.cancel_task()
        return super().eventFilter(watched, event)
