"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Toolbar controls and status for speech playback.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""
from pathlib import Path
import textwrap

from PySide6.QtCore import Qt, QTimer, QRectF
from PySide6.QtGui import QPainter, QPen, QPalette, QColor
from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLineEdit, QLabel

from ...helpers.theme_helper import ThemeHelper
from ...ui.widget_translations import WidgetTranslations
from .languages import SpeechLanguage
from .i18n import tr, language_label, catalog
from .runtime import SUPPORTED_VERSION


class SpeechActivity(QWidget):
    def __init__(self, parent=None, *, scale=.55):
        super().__init__(parent)
        self.scale = scale
        self.angle = 0
        self.running = False
        self.timer = QTimer(self)
        self.timer.setInterval(80)
        self.timer.timeout.connect(self.advance)

    def advance(self):
        self.angle = (self.angle + 24) % 360
        self.update()

    def set_running(self, running):
        self.running = running
        self.setVisible(running)
        self.timer.start() if running and self.isVisible() else self.timer.stop()
        self.update()

    def showEvent(self, event):
        super().showEvent(event)
        if self.running:
            self.timer.start()

    def hideEvent(self, event):
        self.timer.stop()
        super().hideEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        size = min(self.width(), self.height())
        diameter = min(size * self.scale, size - 2)
        rect = QRectF((self.width() - diameter) / 2, (self.height() - diameter) / 2, diameter, diameter)
        color = self.palette().color(QPalette.ColorRole.Text)
        color.setAlpha(180 if self.running else 70)
        painter.setPen(QPen(color, 2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawArc(rect, -self.angle * 16, 270 * 16 if self.running else 360 * 16)


class PlaybackBar(QWidget):
    def __init__(self, editor, parent=None):
        super().__init__(parent)
        if parent:
            self.setFont(parent.font())
        self.setObjectName('speech_playback_bar')
        self.editor = editor
        self.controller = editor.get_speech_controller()
        self.translations = WidgetTranslations(self, self.controller.settings, catalog)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        search = getattr(parent, 'search_form', None)
        reference = search.btn_search_next if search else None
        self.button_size = reference.size() if reference else QLineEdit().sizeHint()
        self.button_size.setWidth(self.button_size.height())
        self.icon_size = reference.iconSize() if reference else self.button_size * .7
        self.status = SpeechActivity(self)
        policy = self.status.sizePolicy()
        policy.setRetainSizeWhenHidden(True)
        self.status.setSizePolicy(policy)
        self.status.setFixedSize(self.button_size)
        layout.addWidget(self.status)
        self.play = self.button(layout, 'module_text_to_speech_action_read', 'play-fill.svg',
                                editor.action_read_aloud)
        self.pause = self.button(layout, 'module_text_to_speech_action_pause_resume', 'pause-fill.svg',
                                 editor.action_pause_speech)
        self.pause.setCheckable(True)
        self.stop = self.button(layout, 'module_text_to_speech_action_stop', 'stop-fill.svg',
                                editor.action_stop_speech)
        layout.addSpacing(3)
        self.metadata = QLabel(self)
        self.metadata.setObjectName('speech_playback_metadata')
        self.metadata.setFixedSize(self.button_size)
        self.metadata.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.translations.bind(self.metadata.setAccessibleName, 'module_text_to_speech_playback_details')
        layout.addWidget(self.metadata)
        self.activity_state = None
        self.activity_timer = QTimer(self)
        self.activity_timer.setInterval(40)
        self.activity_timer.timeout.connect(self.update_activity)
        self.controller.status_changed.connect(self.update_status)
        self.controller.settings.value_changed.connect(self.settings_changed)
        self.translations.language_changed.connect(self.update_selection)
        if hasattr(editor, 'estate'):
            editor.estate.value_changed.connect(self.update_selection)
        self.update_status(self.controller.status_key, check_selection=False)
        QTimer.singleShot(0, self.update_selection)

    def button(self, layout, title, icon, action):
        button = QPushButton(self)
        button.setFont(self.font())
        button.setFixedSize(self.button_size)
        button.setIconSize(self.icon_size)
        self.translations.bind(button.setToolTip, title)
        self.translations.bind(button.setAccessibleName, title)
        button.setIcon(ThemeHelper().get_icon(theme_icon=icon))
        button.clicked.connect(action)
        layout.addWidget(button)
        return button

    def update_status(self, key, *, check_selection=True):
        message = tr(key)
        self.status.setToolTip(message)
        self.status.setAccessibleName(message)
        active = key not in ('module_text_to_speech_status_ready', 'module_text_to_speech_status_stopped',
                             'module_text_to_speech_status_finished', 'module_text_to_speech_status_unavailable',
                             'module_text_to_speech_status_empty')
        self.activity_timer.start() if active else self.activity_timer.stop()
        self.pause.setEnabled(active)
        self.stop.setEnabled(active)
        self.pause.setChecked(active and self.controller.paused)
        theme = ThemeHelper()
        widget = (self.editor.get_active_widget() if check_selection
                                                     and hasattr(self.editor, 'get_active_widget') else None)
        has_selection = widget is not None and widget.textCursor().hasSelection()
        for name, button, selected in (
                ('play', self.play, active and not self.controller.paused),
                ('pause', self.pause, self.pause.isChecked()), ('stop', self.stop, False)):
            key = f'toolbar_icon_color_tts_{name}' + ('_act' if selected else '')
            icon = 'play.svg' if name == 'play' and has_selection else f'{name}-fill.svg'
            button.setIcon(theme.get_icon(theme_icon=icon, color=QColor(theme.get_color(key))))
        self.update_activity()
        self.update_metadata()

    def update_activity(self):
        sink = self.controller.sink
        playing = bool(sink and sink.playing and not self.controller.paused)
        preparing = self.controller.preparing and not self.controller.paused
        state = playing, preparing
        if state == self.activity_state:
            return
        self.activity_state = state
        self.status.set_running(preparing)
        theme = ThemeHelper()
        color = QColor(theme.get_color('toolbar_icon_color_tts_metadata' + ('_act' if playing else '')))
        self.metadata.setPixmap(theme.get_icon(theme_icon='soundwave.svg', color=color).pixmap(self.icon_size))

    def update_selection(self, *_):
        self.update_status(self.controller.status_key)

    def settings_changed(self, values):
        if any(name.startswith('tts_') for name in values):
            self.update_metadata()

    def update_metadata(self):
        settings = self.controller.settings
        runtime = self.controller.runtime
        configuration = getattr(runtime, 'configuration', None)
        loaded = getattr(runtime, 'loaded', False)
        paths = configuration[1] if loaded and configuration else None
        rate = getattr(runtime, 'rate', None) if loaded else None
        language = language_label(SpeechLanguage.from_code(settings.tts_language), include_requirement=False)
        not_loaded = tr('module_text_to_speech_model_not_loaded')
        runtime_label = f'NeMo-Speech.cpp {SUPPORTED_VERSION}'
        if not loaded:
            runtime_label = tr('module_text_to_speech_dependency_required', value=runtime_label)
        lines = [
            tr('module_text_to_speech_playback_voice', value=settings.tts_voice),
            tr('module_text_to_speech_playback_language', value=f'{language} ({settings.tts_language})'),
            tr('module_text_to_speech_playback_sample_rate', value=f'{rate:,} Hz' if rate else not_loaded),
            tr('module_text_to_speech_playback_rate',
               value=f'{round(rate * settings.tts_speed):,} Hz' if rate else not_loaded),
            tr('module_text_to_speech_playback_audio_format'),
            tr('module_text_to_speech_playback_speed', value=f'{settings.tts_speed:g} ×'),
            tr('module_text_to_speech_playback_runtime', value=runtime_label),
            tr('module_text_to_speech_playback_model', value=Path(paths[0]).name if paths else not_loaded),
            tr('module_text_to_speech_playback_codec', value=Path(paths[1]).name if paths else not_loaded),
        ]
        self.metadata.setToolTip('\n'.join(textwrap.fill(line, width=64) for line in lines))
