"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Regression tests for speech preparation, setup, playback, and cancellation.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

import asyncio
import time
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, PropertyMock

import markdown
import pytest
from PySide6.QtCore import QSettings
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QCheckBox, QLineEdit, QMainWindow, QMenu, QTabWidget

from notolog.modules.text_to_speech import config, runtime
from notolog.modules.text_to_speech.text import prepare_text, speech_chunks
from notolog.modules.text_to_speech.controller import SpeechController
from notolog.modules.text_to_speech.module_core import ModuleCore
from notolog.modules.text_to_speech.actions import append_selection_action
from notolog.edit_widget import EditWidget
from notolog.view_widget import ViewWidget


@pytest.fixture
def settings(qapp, tmp_path, monkeypatch):
    monkeypatch.setattr(config, 'find_spec', lambda _: object())
    monkeypatch.setattr(config, 'portaudio_library', lambda: 'libportaudio.so.2')
    settings = config.speech_settings()
    monkeypatch.setattr(settings, 'settings', QSettings(str(tmp_path / 'speech.ini'), QSettings.Format.IniFormat))
    settings.app_language = 'en'
    settings.tts_enabled = False
    settings.tts_model_directory = str(tmp_path / 'models')
    yield settings


@pytest.mark.parametrize('inline,multiline,expected', [
    (True, True, 'Inline code block'),
    (False, True, 'inline_secret'),
    (True, False, 'Inline code block'),
    (False, False, 'inline_secret'),
])
def test_independent_code_options(inline, multiline, expected):
    result = prepare_text('Before `inline_secret` after\n\n```python\nblock_secret\n```',
                          skip_inline=inline, skip_multiline=multiline)
    assert expected in result
    assert ('Multiline code block' in result) == multiline
    assert ('block_secret' in result) != multiline
    assert ('inline_secret' in result) != inline


def test_prose_and_metadata():
    result = prepare_text('---\ntitle: hidden\n---\n# Heading\n\n[Guide](https://example.com "title") '
                          '&amp; **bold**\n\n<!-- private -->\n\n    secret\n\nAfter')
    assert result == 'Heading\nGuide & bold\nMultiline code block.\nAfter'
    assert 'https' not in result


@pytest.mark.parametrize('skip', [True, False])
def test_nested_code_uses_multiline_speech_option(skip):
    source = '1. Item\n\n    ```python\n    secret_value\n    ```\n\n2. Next'
    result = prepare_text(source, skip_inline=True, skip_multiline=skip)
    assert ('Multiline code block' in result) == skip
    assert ('secret_value' in result) != skip
    assert 'Inline code block' not in result
    assert 'Next' in result


def test_code_spans_containing_backticks_and_literal_html():
    assert prepare_text('A ``code ` inside`` B') == 'A  Inline code block  B'
    assert prepare_text('<script>private</script>\n\nVisible') == 'Visible'
    assert prepare_text('Text\u2029next') == 'Text\nnext'


def test_chunks_bound_even_unbroken_text():
    chunks = list(speech_chunks('x' * 1201))
    assert [len(chunk) for chunk in chunks] == [500, 500, 201]
    assert ''.join(chunks) == 'x' * 1201


def test_missing_models_do_not_hide_settings(settings):
    tabs = QTabWidget()
    module = ModuleCore()
    assert module.extend_settings_dialog_fields_conf(tabs) == []
    assert tabs.tabText(0) == 'Text-to-Speech'
    panel = tabs.widget(0)
    panel.findChild(QCheckBox, 'tts_skip_inline_code').setChecked(False)
    assert not settings.tts_skip_inline_code
    assert settings.tts_skip_multiline_code
    assert panel.findChild(QLineEdit, 'tts_runtime_path') is not None
    tabs.close()


def test_model_paths_need_complete_set(settings, tmp_path):
    settings.tts_model_directory = str(tmp_path)
    with pytest.raises(ValueError, match='Download'):
        config.model_paths(settings)
    (tmp_path / 'magpie.gguf').write_bytes(b'GGUF')
    (tmp_path / 'nano_codec.gguf').write_bytes(b'GGUF')
    tokenizer = tmp_path / 'tokenizer'
    tokenizer.mkdir()
    (tokenizer / 'model_config.yaml').write_text('model: magpie')
    assert config.model_paths(settings) == (
        str(tmp_path / 'magpie.gguf'), str(tmp_path / 'nano_codec.gguf'), str(tokenizer))
    settings.tts_magpie_path = str(tmp_path / 'missing.gguf')
    with pytest.raises(ValueError):
        config.model_paths(settings)


@pytest.mark.asyncio
async def test_version_rejected_before_download(settings, monkeypatch):
    command = AsyncMock(return_value='nemo-speech 9.0.0')
    monkeypatch.setattr(runtime, 'run_command', command)
    with pytest.raises(ValueError, match='requires'):
        await runtime.download_models(settings, Mock())
    command.assert_awaited_once_with(settings, ['--version'])


@pytest.mark.asyncio
async def test_download_explicitly_pulls_complete_model_set(settings, monkeypatch, tmp_path):
    monkeypatch.setattr(runtime, 'validate_runtime', AsyncMock())
    magpie, codec, tokenizer = tmp_path / 'voice.gguf', tmp_path / 'decoder.gguf', tmp_path / 'assets'
    magpie.touch()
    codec.touch()
    tokenizer.mkdir()
    command = AsyncMock(return_value=f'repo\ttts\t{magpie}\nrepo\tcodec\t{codec}\nrepo\ttokenizer\t{tokenizer}\n')
    monkeypatch.setattr(runtime, 'run_command', command)
    progress = Mock()
    assert await runtime.download_models(settings, progress) == (str(magpie), str(codec), str(tokenizer))
    command.assert_awaited_once_with(settings, ['--verbose', 'pull', 'magpie'], progress=progress, timeout=None)


@pytest.mark.parametrize('view', [False, True])
def test_selection_context_action_preserves_code(settings, view):
    host = QMainWindow()
    host.speech_enabled = lambda: True
    host.action_read_aloud = Mock()
    widget = ViewWidget(host) if view else EditWidget(host)
    host.setCentralWidget(widget)
    source = 'Text `secret` end\n\n```\nprivate\n```'
    if view:
        widget.setHtml(markdown.markdown(source, extensions=['extra']))
    else:
        widget.setPlainText(source)
    cursor = widget.textCursor()
    cursor.select(QTextCursor.SelectionType.Document)
    widget.setTextCursor(cursor)
    menu = QMenu()
    append_selection_action(widget, menu, html=view)
    action = next(action for action in menu.actions() if action.text() == 'Read selection aloud')
    assert not action.icon().isNull()
    from notolog.modules.text_to_speech.actions import speech_action_icon
    assert action.icon().pixmap(24, 24).toImage() == speech_action_icon().pixmap(24, 24).toImage()
    assert action.isIconVisibleInMenu()
    action.trigger()
    spoken = prepare_text(host.action_read_aloud.call_args.kwargs['source'])
    assert 'secret' not in spoken
    assert 'private' not in spoken
    assert spoken.count('Multiline code block') == 1
    host.close()


def test_empty_selection_disabled(settings):
    host = QMainWindow()
    host.speech_enabled = lambda: True
    widget = EditWidget(host)
    menu = QMenu()
    append_selection_action(widget, menu)
    assert not next(action for action in menu.actions() if action.text() == 'Read selection aloud').isEnabled()
    host.close()


@pytest.mark.asyncio
async def test_new_read_cancels_previous_before_start(settings, monkeypatch):
    settings.tts_enabled = True
    controller = SpeechController()
    controller.runtime = SimpleNamespace(start=AsyncMock(), close=Mock())
    order = []
    entered = asyncio.Event()

    async def synthesize(text):
        order.append(text)
        if text == 'first':
            entered.set()
            try:
                await asyncio.Event().wait()
            finally:
                order.append('cancelled')
        return b'audio'

    controller._play_stream = synthesize
    controller.read('first')
    first = controller.task
    await entered.wait()
    controller.read('second')
    await controller.task
    assert first.cancelled()
    assert order == ['first', 'cancelled', 'second']
    controller.stop()


async def with_qt_events(qapp, awaitable):
    async def pump():
        while True:
            qapp.processEvents()
            await asyncio.sleep(0.001)

    task = asyncio.create_task(pump())
    try:
        return await asyncio.wait_for(awaitable, 10)
    finally:
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)


@pytest.mark.asyncio
async def test_process_adapter_reports_failure_and_version(settings, qapp):
    import sys
    settings.tts_runtime_path = sys.executable
    result = await with_qt_events(qapp, runtime.run_command(settings, ['-c', 'print("nemo-speech 0.1.0")']))
    assert result.strip() == 'nemo-speech 0.1.0'
    with pytest.raises(RuntimeError, match='broken runtime'):
        await with_qt_events(qapp, runtime.run_command(
            settings, ['-c', 'import sys; print("broken runtime"); sys.exit(2)']))


@pytest.mark.asyncio
async def test_process_timeout_does_not_leave_worker(settings, qapp):
    import sys
    settings.tts_runtime_path = sys.executable
    with pytest.raises(RuntimeError, match='did not respond within 0.05 seconds'):
        await with_qt_events(qapp, runtime.run_command(
            settings, ['-c', 'import time; time.sleep(60)'], timeout=0.05))


@pytest.mark.asyncio
@pytest.mark.parametrize('platform', ['linux', 'darwin', 'win32'])
@pytest.mark.parametrize('crashed', [False, True])
async def test_runtime_launch_failure_offers_macos_approval_guidance(settings, monkeypatch, platform, crashed):
    from PySide6.QtCore import QProcess

    class FailedProcess(QProcess):
        def start(self, *args):
            self.errorOccurred.emit(QProcess.ProcessError.Crashed if crashed else QProcess.ProcessError.FailedToStart)

        def errorString(self):
            return 'Process crashed' if crashed else 'Failed to start'

    monkeypatch.setattr(runtime, 'QProcess', FailedProcess)
    monkeypatch.setattr(runtime, 'sys', SimpleNamespace(platform=platform))
    monkeypatch.setattr(runtime, 'runtime_path', lambda _: '/runtime/nemo-speech')
    monkeypatch.setattr(runtime, 'isolate_process', Mock())
    stop = Mock()
    monkeypatch.setattr(runtime, 'stop_process', stop)
    with pytest.raises(RuntimeError) as failure:
        await runtime.run_command(settings, ['--version'])
    message = str(failure.value)
    assert message.startswith('Process crashed' if crashed else 'Failed to start')
    assert ('Privacy & Security' in message) == (platform == 'darwin')
    assert ('only if you trust' in message) == (platform == 'darwin')
    assert ('text-to-speech.md#macos-runtime-approval' in message) == (platform == 'darwin')
    stop.assert_called_once()


def test_reading_current_document_prefers_unsaved_buffer(settings):
    from notolog.notolog_editor import NotologEditor
    from notolog.editor_state import Mode
    controller = Mock()
    widget = EditWidget()
    widget.setPlainText('Unsaved text')
    host = SimpleNamespace(speech_enabled=lambda: True, get_mode=lambda: Mode.EDIT,
                           get_edit_widget=lambda: widget, get_speech_controller=lambda: controller,
                           content='Saved text')
    NotologEditor.action_read_aloud(host, whole_document=True)
    controller.read.assert_called_once_with('Unsaved text', html=False)
    widget.close()


@pytest.mark.parametrize('source,needle,label', [
    ('😀 A `secret` B', 'secret', 'Inline code block'),
    ('```python\nprivate\n```', 'private', 'Multiline code block'),
])
def test_partial_edit_selection_keeps_code_context(settings, source, needle, label):
    from notolog.highlight.md_highlighter import MdHighlighter
    from notolog.modules.text_to_speech.actions import selection_source
    widget = EditWidget()
    widget.setPlainText(source)
    highlighter = MdHighlighter(widget.document())
    highlighter.rehighlight()
    widget.setTextCursor(widget.document().find(needle))
    selected = selection_source(widget)
    assert label in prepare_text(selected)
    assert needle in prepare_text(selected, skip_inline=False, skip_multiline=False)
    highlighter.setDocument(None)
    widget.close()


def test_module_inside_full_settings_dialog(settings, monkeypatch, caplog):
    from notolog.ui.settings_dialog import SettingsDialog
    from notolog.modules.modules import Modules
    from notolog.modules import text_to_speech
    monkeypatch.setattr(Modules, 'get_by_extension', lambda *_: [text_to_speech])
    host = QMainWindow()
    host.settings = settings
    dialog = SettingsDialog(host)
    assert 'Text-to-Speech' in [dialog.tab_widget.tabText(i) for i in range(dialog.tab_widget.count())]
    dialog.findChild(QLineEdit, 'tts_voice').setText('0')
    assert settings.tts_voice == '0'
    check = dialog.findChild(QCheckBox, 'tts_skip_inline_code')
    check.setChecked(False)
    assert not settings.tts_skip_inline_code
    from notolog.modules.text_to_speech.settings_widget import SpeechSettingsWidget
    speech = dialog.findChild(SpeechSettingsWidget)
    from notolog.modules.text_to_speech.languages import SpeechLanguage
    speech.language.setCurrentIndex(list(SpeechLanguage).index(SpeechLanguage.ES))
    assert settings.tts_language == 'es'
    caplog.clear()
    speech.report('Download status changed')
    assert 'qt_tts_status' not in caplog.text
    dialog.close()
    host.close()


@pytest.mark.asyncio
async def test_settings_missing_runtime_reports_visible_error(settings, monkeypatch):
    from notolog.modules.text_to_speech import settings_widget
    monkeypatch.setattr(settings_widget, 'runtime_path', lambda _: '')
    widget = settings_widget.SpeechSettingsWidget()
    await widget._run(widget._download)
    assert 'Error:' in widget.status.text()
    assert 'Select a speech runtime first.' in widget.status.text()
    assert not widget.status.isHidden()
    assert not widget.download.isEnabled()
    assert not widget.test.isEnabled()
    widget.close()


@pytest.mark.parametrize('saved,expected', [
    ('en', 'EN'), ('es-ES', 'ES'), ('fr_FR', 'FR'), ('zh-CN', 'ZH'), ('ja', 'JA'), ('invalid', 'EN'),
])
def test_language_selector_preserves_supported_codes(settings, saved, expected):
    from notolog.modules.text_to_speech.settings_widget import SpeechSettingsWidget
    from notolog.modules.text_to_speech.languages import SpeechLanguage
    from notolog.ui.enum_combo_box import EnumComboBox
    settings.tts_language = saved
    widget = SpeechSettingsWidget()
    assert isinstance(widget.language, EnumComboBox)
    assert widget.language.currentData() is SpeechLanguage[expected]
    assert settings.tts_language == expected.lower()
    assert widget.language.count() == 9
    assert widget.language.itemData(0) is SpeechLanguage.EN
    assert config.DEFAULTS['tts_language'][1] == 'en'
    widget.close()


@pytest.mark.parametrize('expanded', [False, True])
@pytest.mark.parametrize('font_size', [12, 20])
def test_settings_spinner_has_reserved_space_below_status(settings, qapp, expanded, font_size):
    from PySide6.QtGui import QFont
    from notolog.modules.text_to_speech.settings_widget import SpeechSettingsWidget
    widget = SpeechSettingsWidget()
    widget.setFont(QFont('Sans', font_size))
    widget.sync_font()
    widget.details.setChecked(expanded)
    widget.report('Ready')
    widget.show()
    qapp.processEvents()
    positions = [(item.pos().x(), item.pos().y()) for item in (widget.status_icon, widget.activity, widget.download)]
    for message, state in [('Loading', 'busy'), ('Failed', 'error'), ('Verified', 'success')]:
        widget.report(message, state)
        qapp.processEvents()
        assert widget.status_icon.isVisible()
        assert widget.activity.isVisible() == (state == 'busy')
        assert [(item.pos().x(), item.pos().y()) for item in (
            widget.status_icon, widget.activity, widget.download)] == positions
        assert widget.activity.x() == widget.status_icon.x()
        assert widget.activity.y() >= widget.status_icon.y() + widget.status_icon.height()
        assert widget.output.isVisible() == expanded
        if not expanded:
            assert widget.activity.y() + widget.activity.height() <= (
                    widget.progress_status.y() + widget.progress_status.height())
            assert len({widget.panel.layout().rowMinimumHeight(row) for row in (0, 1, 3)}) == 1
    widget.close()


@pytest.mark.parametrize('html', [False, True])
def test_heading_sections_keep_structure_without_announcements(html):
    from notolog.modules.text_to_speech.text import prepare_sections, SpeechSection
    source = ('<p>Before.</p><h2>Topic</h2><p>After.</p>' if html else 'Before.\n\n## Topic\n\nAfter.')
    assert prepare_sections(source, html=html) == [
        SpeechSection('Before.'), SpeechSection('Topic', heading=True), SpeechSection('After.')]
    assert prepare_sections('```\n# Code heading\n```', skip_multiline=False) == [SpeechSection('# Code heading')]
    assert prepare_sections('<script><h2>Hidden</h2></script><p>Visible</p>', html=True) == [SpeechSection('Visible')]
    assert prepare_sections('Chapter: plain prose') == [SpeechSection('Chapter: plain prose')]


@pytest.mark.asyncio
@pytest.mark.parametrize('speed', [.5, 1.0, 2.0])
async def test_heading_break_is_one_second_and_uses_separate_requests(settings, monkeypatch, speed):
    from notolog.modules.text_to_speech import controller as controller_module
    from notolog.modules.text_to_speech.text import SpeechSection
    captured = bytearray()
    sink = Mock()
    sink.write.side_effect = lambda data: captured.extend(data) or len(data)
    sink.write_available = 4096
    sink.drained = True
    monkeypatch.setattr(controller_module, 'AudioOutput', lambda *_: sink)
    settings.tts_speed = speed
    controller = SpeechController()
    requested = []

    async def stream(text):
        requested.append(text)
        yield b'\x01\x00' * 4

    controller.runtime = SimpleNamespace(rate=22050, stream=stream, close=Mock())
    await controller._play_stream([SpeechSection('Start', True), SpeechSection('Before.'),
                                   SpeechSection('Next topic', True), SpeechSection('After.')])
    assert requested == ['Start.', 'Before.', 'Next topic.', 'After.']
    assert captured == b'\x01\x00' * 8 + bytes(round(22050 * speed) * 2) + b'\x01\x00' * 8


@pytest.mark.asyncio
@pytest.mark.parametrize('inline,multiline', [(False, True), (True, False), (False, False)])
async def test_unchecked_code_options_reach_speech_controller(settings, inline, multiline):
    settings.tts_enabled = True
    settings.tts_skip_inline_code = inline
    settings.tts_skip_multiline_code = multiline
    controller = SpeechController()
    controller.runtime = SimpleNamespace(start=AsyncMock(), close=Mock())
    controller._play_stream = AsyncMock()
    controller.read('Say `hello world`\n\n```\ngood morning\n```')
    await controller.task
    spoken = controller._play_stream.call_args.args[0]
    assert ('hello world' in spoken) == (not inline)
    assert ('good morning' in spoken) == (not multiline)
    controller.stop()


@pytest.mark.parametrize('extension', ['md', 'txt'])
def test_file_tree_read_action_has_speaker_icon(settings, tmp_path, extension):
    from notolog.ui.file_tree_context_menu import FileTreeContextMenu
    from notolog.modules.text_to_speech.actions import speech_action_icon
    note = tmp_path / f'note.{extension}'
    note.write_text('Hello')
    host = QMainWindow()
    host.get_tree_active_dir = lambda: str(tmp_path)
    host.speech_enabled = lambda: True
    host.is_file_safely_deleted = lambda _: False
    host.action_read_file_aloud = Mock()
    menu = FileTreeContextMenu(str(note), host)
    action = next(action for action in menu.actions() if action.text() == 'Read file aloud')
    assert not action.icon().isNull()
    assert action.icon().pixmap(24, 24).toImage() == speech_action_icon(filled=True).pixmap(24, 24).toImage()
    assert action.isIconVisibleInMenu()
    action.trigger()
    host.action_read_file_aloud.assert_called_once_with(str(note))
    menu.close()
    host.close()


@pytest.mark.asyncio
async def test_settings_download_progress_success_and_cancel(settings, monkeypatch, tmp_path):
    from notolog.modules.text_to_speech import settings_widget
    monkeypatch.setattr(settings_widget, 'runtime_path', lambda _: '/runtime')
    settings.tts_enabled = True
    widget = settings_widget.SpeechSettingsWidget()
    settings.tts_model_directory = str(tmp_path)
    paths = [str(tmp_path / name) for name in ('magpie.gguf', 'codec.gguf', 'tokenizer')]

    async def download(_, progress):
        assert widget.download.isEnabled()
        assert widget.download.text() == 'Cancel'
        assert not widget.test.isEnabled()
        progress('[model] downloading repo@revision (tts, 427.8 MiB)\n')
        (tmp_path / 'magpie.gguf').touch()
        (tmp_path / 'codec.gguf').touch()
        (tmp_path / 'tokenizer').mkdir()
        (tmp_path / 'tokenizer' / 'model_config.yaml').write_text('model: magpie')
        return paths

    monkeypatch.setattr(settings_widget, 'download_models', download)
    await widget._run(widget._download)
    assert 'downloaded and verified' in widget.status.text()
    assert settings.tts_magpie_path == ''

    async def blocked():
        await asyncio.Future()

    widget.launch(blocked)
    await asyncio.sleep(0)
    widget.cancel_task()
    await widget.task
    assert 'Cancelled' in widget.status.text()
    assert widget.test.isEnabled()
    widget.close()


@pytest.mark.asyncio
async def test_settings_test_voice_checks_runtime_before_models(settings, monkeypatch):
    from notolog.modules.text_to_speech import settings_widget
    settings.tts_enabled = True
    monkeypatch.setattr(settings_widget, 'validate_runtime', AsyncMock(side_effect=ValueError('Missing runtime')))
    widget = settings_widget.SpeechSettingsWidget()
    model_check = Mock()
    monkeypatch.setattr(settings_widget, 'model_paths', model_check)
    with pytest.raises(ValueError, match='Missing runtime'):
        await widget._test_voice()
    model_check.assert_not_called()
    await widget._run(widget._test_voice)
    assert widget.status.text() == 'Error: Missing runtime'
    widget.close()


@pytest.mark.asyncio
async def test_settings_keeps_voice_failure_visible(settings, monkeypatch):
    from notolog.modules.text_to_speech import settings_widget
    settings.tts_enabled = True
    monkeypatch.setattr(settings_widget, 'validate_runtime', AsyncMock())
    monkeypatch.setattr(settings_widget, 'model_paths', Mock())
    widget = settings_widget.SpeechSettingsWidget()
    controller = SpeechController()
    controller.runtime = SimpleNamespace(start=AsyncMock(side_effect=RuntimeError('Model cannot load')), close=Mock())
    host = SimpleNamespace(get_speech_controller=lambda: controller,
                           action_read_aloud=lambda source: controller.read(source))
    monkeypatch.setattr(widget, 'editor', lambda: host)
    await widget._run(widget._test_voice)
    assert widget.status.text() == 'Model cannot load'
    controller.stop()
    widget.close()


def test_file_tree_read_uses_clicked_file_without_loading_it(settings, tmp_path):
    from notolog.notolog_editor import NotologEditor
    path = tmp_path / 'other.md'
    path.write_text('# Another note\n\nRead me.')
    host = SimpleNamespace(get_current_file_path=lambda: str(tmp_path / 'current.md'), action_read_aloud=Mock())
    NotologEditor.action_read_file_aloud(host, str(path))
    host.action_read_aloud.assert_called_once_with(source='# Another note\n\nRead me.')


def test_encrypted_file_tree_read_requires_unlock(settings, tmp_path, monkeypatch):
    from notolog.notolog_editor import NotologEditor
    from notolog.file_header import FileHeader
    path = tmp_path / 'private.md'
    path.write_text('ciphertext')
    header = Mock()
    header.is_file_encrypted.return_value = True
    monkeypatch.setattr(FileHeader, 'load_file', lambda *_: (header, 'ciphertext'))
    message = Mock()
    monkeypatch.setattr('notolog.notolog_editor.MessageBox', message)
    host = SimpleNamespace(get_current_file_path=lambda: '', action_read_aloud=Mock())
    NotologEditor.action_read_file_aloud(host, str(path))
    host.action_read_aloud.assert_not_called()
    message.assert_called_once()


@pytest.mark.asyncio
async def test_finished_read_keeps_runtime_warm(settings, monkeypatch):
    settings.tts_enabled = True
    controller = SpeechController()
    controller.runtime = SimpleNamespace(start=AsyncMock(), close=Mock())
    controller._play_stream = AsyncMock()
    controller.read('First sentence.')
    await controller.task
    controller.read('Another sentence.')
    await controller.task
    controller.runtime.close.assert_not_called()
    controller.stop()
    controller.runtime.close.assert_called_once()


@pytest.mark.asyncio
async def test_cached_models_show_completion_without_claiming_download(settings, monkeypatch, tmp_path):
    from notolog.modules.text_to_speech import settings_widget
    monkeypatch.setattr(settings_widget, 'runtime_path', lambda _: '/runtime')
    magpie, codec, tokenizers = tmp_path / 'magpie.gguf', tmp_path / 'codec.gguf', tmp_path / 'tokenizers'
    magpie.touch()
    codec.touch()
    tokenizers.mkdir()
    (tokenizers / 'model_config.yaml').write_text('model: magpie')
    settings.tts_model_directory = str(tmp_path)
    monkeypatch.setattr(settings_widget, 'download_models', AsyncMock(
        return_value=(str(magpie), str(codec), str(tokenizers))))
    widget = settings_widget.SpeechSettingsWidget()
    await widget._run(widget._download)
    assert widget.status.text() == 'Existing models verified. Ready to read.'
    assert widget.download.text() == 'Verify models'
    assert not widget.timer.isActive()
    widget.close()


@pytest.mark.asyncio
@pytest.mark.parametrize('error,expected', [
    (PermissionError(13, 'Permission denied'), 'Permission denied. Choose a writable model folder'),
    (OSError(28, 'No space left on device'), 'No space left on device'),
    (RuntimeError('curl failed while downloading (exit code 6): host not found'), 'host not found'),
    (RuntimeError('downloaded artifact failed size or SHA-256 verification'), 'SHA-256 verification'),
])
async def test_download_errors_remain_visible_and_allow_retry(settings, monkeypatch, error, expected):
    from notolog.modules.text_to_speech import settings_widget
    monkeypatch.setattr(settings_widget, 'runtime_path', lambda _: '/runtime')
    monkeypatch.setattr(settings_widget, 'download_models', AsyncMock(side_effect=error))
    widget = settings_widget.SpeechSettingsWidget()
    await widget._run(widget._download)
    assert expected in widget.status.text()
    assert widget.state == 'error'
    assert widget.download.isEnabled()
    assert widget.download.text() == 'Download models'
    assert not widget.test.isEnabled()
    assert str(error) in widget.output.toPlainText()
    widget.close()


@pytest.mark.asyncio
async def test_download_rejects_read_only_directory_before_pull(settings, monkeypatch, tmp_path):
    import os
    if os.name == 'nt' or os.geteuid() == 0:
        pytest.skip('POSIX directory permission test requires an unprivileged user')
    root = tmp_path / 'read-only'
    root.mkdir()
    root.chmod(0o500)
    settings.tts_model_directory = str(root)
    monkeypatch.setattr(runtime, 'validate_runtime', AsyncMock())
    command = AsyncMock()
    monkeypatch.setattr(runtime, 'run_command', command)
    try:
        with pytest.raises(PermissionError):
            await runtime.download_models(settings, Mock())
        command.assert_not_awaited()
    finally:
        root.chmod(0o700)


@pytest.mark.asyncio
async def test_download_rejects_incomplete_runtime_result(settings, monkeypatch):
    monkeypatch.setattr(runtime, 'validate_runtime', AsyncMock())
    monkeypatch.setattr(runtime, 'run_command', AsyncMock(return_value='repo\ttts\t/nonexistent.gguf'))
    with pytest.raises(ValueError, match='complete model set'):
        await runtime.download_models(settings, Mock())


def test_download_stage_output_handles_split_lines(settings):
    from notolog.modules.text_to_speech.settings_widget import SpeechSettingsWidget
    widget = SpeechSettingsWidget()
    widget.download_pending = ''
    widget.download_started = False
    widget.download_output('[model] down')
    widget.download_output('loading nvidia/model@rev (codec, 75.2 MiB)\n')
    assert widget.download_started
    assert widget.status.text() == 'File 1/3 · Downloading audio decoder · 75.2 MiB…'
    widget.download_output('[model] verifying size and SHA-256...\n')
    assert widget.status.text() == 'File 1/3 · Verifying downloaded file…'
    widget.close()


def test_compact_layout_has_visible_labels_and_expanded_details(settings):
    from notolog.modules.text_to_speech.settings_widget import SpeechSettingsWidget
    from notolog.ui.label_with_hint import LabelWithHint
    widget = SpeechSettingsWidget()
    widget.show()
    assert widget.advanced.isHidden()
    assert not widget.details.isHidden()
    for hint in widget.findChildren(LabelWithHint):
        assert hint.sizeHint().width() >= hint.layout.minimumSize().width()
        assert hint.sizeHint().height() > 0
    widget.advanced_toggle.click()
    assert not widget.advanced.isHidden()
    assert widget.details.isChecked()
    assert widget.output.isVisible()
    widget.details.click()
    assert widget.output.isHidden()
    widget.details.click()
    assert widget.output.isVisible()
    widget.close()


@pytest.mark.asyncio
async def test_switching_tabs_keeps_download_but_closing_cancels(settings, qapp, monkeypatch):
    from PySide6.QtWidgets import QWidget
    from notolog.modules.text_to_speech.settings_widget import SpeechSettingsWidget
    host = QMainWindow()
    tabs = QTabWidget(host)
    host.setCentralWidget(tabs)
    widget = SpeechSettingsWidget(tabs)
    tabs.addTab(widget, 'Speech')
    tabs.addTab(QWidget(), 'Other')
    host.show()

    async def blocked():
        await asyncio.Future()

    widget.launch(blocked)
    await asyncio.sleep(0)
    tabs.setCurrentIndex(1)
    qapp.processEvents()
    await asyncio.sleep(0)
    assert not widget.task.done()
    from PySide6.QtWidgets import QMessageBox
    question = Mock(return_value=QMessageBox.StandardButton.No)
    monkeypatch.setattr(QMessageBox, 'question', question)
    assert not host.close()
    assert not widget.task.done()
    question.return_value = QMessageBox.StandardButton.Yes
    assert host.close()
    qapp.processEvents()
    await asyncio.wait_for(widget.task, .5)
    assert question.call_count == 2


def test_reading_preferences_do_not_clear_verified_status(settings):
    from notolog.modules.text_to_speech.settings_widget import SpeechSettingsWidget
    widget = SpeechSettingsWidget()
    widget.report('Existing models verified. Ready to read.', 'success')
    widget.completed_files = 3
    settings.tts_enabled = True
    settings.tts_speed = 1.2
    assert widget.status.text() == 'Existing models verified. Ready to read.'
    assert widget.completed_files == 3
    assert not widget.refresh_timer.isActive()
    widget.close()


def test_speech_disabled_actions_are_dimmed_and_explain_prerequisite(settings, monkeypatch):
    from notolog.modules.text_to_speech import settings_widget
    monkeypatch.setattr(settings_widget, 'runtime_path', lambda _: '')
    widget = settings_widget.SpeechSettingsWidget()
    assert not widget.test.isEnabled()
    assert widget.test.graphicsEffect().opacity() == .4
    assert widget.download.graphicsEffect().opacity() == .4
    assert widget.test_hint.text() == 'Select a speech runtime first.'
    settings.tts_enabled = True
    monkeypatch.setattr(settings_widget, 'runtime_path', lambda _: '/runtime')
    monkeypatch.setattr(widget, 'have_models', lambda **_: True)
    widget.refresh_controls()
    assert widget.test.isEnabled()
    assert widget.test.graphicsEffect().opacity() == 1.0
    assert widget.test_hint.isHidden()
    widget.close()


def test_block_hints_differ_from_inline_and_long_help_wraps(settings):
    from notolog.modules.text_to_speech.settings_widget import SpeechSettingsWidget
    from notolog.ui.label_with_hint import LabelWithHint
    widget = SpeechSettingsWidget()
    hints = widget.findChildren(LabelWithHint)
    assert sum(hint.theme_icon == 'question-circle.svg' for hint in hints) == 2
    assert any(hint.theme_icon == 'info-circle.svg' for hint in hints)
    assert all('-fill.svg' not in hint.theme_icon for hint in hints)
    label = LabelWithHint(widget)
    text = 'A long help message containing useful information. ' * 5
    label.set_tooltip(text)
    assert '\n' in label.icon_button.toolTip()
    assert all(len(line) <= 55 for line in label.icon_button.toolTip().splitlines())
    label.set_tooltip('<b>Rich text</b>')
    assert label.icon_button.toolTip() == '<b>Rich text</b>'
    widget.close()


def test_download_file_steps_include_cached_artifacts(settings):
    from notolog.modules.text_to_speech.settings_widget import SpeechSettingsWidget
    widget = SpeechSettingsWidget()
    widget.download_pending = ''
    widget.download_output('[model] cached: /model.gguf\n')
    assert widget.completed_files == 1
    widget.download_output('[model] downloading repo@rev (tokenizer, 32.0 MiB)\n')
    assert 'File 2/3' in widget.status.text()
    widget.download_output('[model] verifying size and SHA-256...\n')
    assert widget.completed_files == 1
    widget.download_output('[model] cached: /codec.gguf\n')
    assert widget.completed_files == 3
    assert widget.completed_files == 3
    widget.close()


def test_short_lines_share_synthesis_request():
    assert list(speech_chunks('Heading\nFirst sentence.\nSecond sentence.')) == [
        'Heading. First sentence. Second sentence.']


@pytest.mark.asyncio
@pytest.mark.parametrize('cancel', [False, True])
async def test_next_passage_prepared_during_playback_and_cancelled(settings, monkeypatch, cancel):
    from notolog.modules.text_to_speech import controller as module
    from notolog.modules.text_to_speech import controller as controller_module
    monkeypatch.setattr(module, 'speech_chunks', lambda *_, **__: iter(['first', 'second']))
    settings.tts_enabled = True
    controller = SpeechController()
    next_started = asyncio.Event()
    release_playback = asyncio.Event()
    next_cancelled = asyncio.Event()
    played = []

    async def stream(text):
        if text == 'second':
            next_started.set()
            if cancel:
                try:
                    await asyncio.Future()
                except asyncio.CancelledError:
                    next_cancelled.set()
                    raise
        yield text.encode()

    sink = Mock()
    sink.write.side_effect = lambda data: played.append(bytes(data)) or len(data)
    sink.write_available = 100
    type(sink).drained = PropertyMock(side_effect=release_playback.is_set)
    monkeypatch.setattr(controller_module, 'AudioOutput', Mock(return_value=sink))
    controller.runtime = SimpleNamespace(start=AsyncMock(), close=Mock(), rate=22050, stream=stream)
    controller.read('A note')
    task = controller.task
    await asyncio.wait_for(next_started.wait(), 1)
    assert played[0] == b'first'
    if cancel:
        controller.stop()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert next_cancelled.is_set()
        assert played == [b'first']
    else:
        release_playback.set()
        await task
        assert played == [b'first', b'second']
        controller.stop()


@pytest.mark.asyncio
async def test_adjacent_passages_are_queued_before_device_drain(settings, monkeypatch):
    from notolog.modules.text_to_speech import controller as module
    monkeypatch.setattr(module, 'speech_chunks', lambda *_, **__: iter(['first', 'second']))
    played = []

    async def stream(text):
        yield text.encode()

    def drained():
        assert played == [b'first', b'second']
        return True

    sink = Mock(write_available=100)
    sink.write.side_effect = lambda data: played.append(bytes(data)) or len(data)
    type(sink).drained = PropertyMock(side_effect=drained)
    monkeypatch.setattr(module, 'AudioOutput', lambda _: sink)
    controller = SpeechController()
    controller.runtime = SimpleNamespace(rate=22050, stream=stream)
    await controller._play_stream('A note')
    sink.close.assert_called_once()


def test_first_speech_request_is_shorter_without_losing_text():
    text = 'A short first sentence. ' + 'More words for the next passage. ' * 15
    chunks = list(speech_chunks(text, limit=80, first_limit=32))
    assert len(chunks[0]) <= 32
    assert all(len(chunk) <= 80 for chunk in chunks)
    assert ' '.join(chunks) == text.strip()


@pytest.mark.asyncio
async def test_synthesis_builds_bounded_lookahead_while_current_passage_plays(settings, monkeypatch):
    from notolog.modules.text_to_speech import controller as module
    passages = ['first', 'second', 'third', 'fourth']
    monkeypatch.setattr(module, 'speech_chunks', lambda *_, **__: iter(passages))
    generated = []
    third_started = asyncio.Event()

    async def stream(text):
        generated.append(text)
        if text == 'third':
            third_started.set()
        yield text.encode()

    played = bytearray()
    sink = Mock(write_available=2, drained=True)

    def write(data):
        played.extend(data)
        if len(played) == 2:
            sink.write_available = 0
        return len(data)

    sink.write.side_effect = write
    monkeypatch.setattr(module, 'AudioOutput', lambda _: sink)
    controller = SpeechController()
    controller.runtime = SimpleNamespace(rate=22050, stream=stream)
    task = asyncio.create_task(controller._play_stream('A note'))
    try:
        await asyncio.wait_for(third_started.wait(), 1)
        assert generated == passages[:3]
        assert played == b'fi'
        # A full ready queue prevents synthesizing the rest of the document.
        await asyncio.sleep(.03)
        assert generated == passages[:3]
        sink.write_available = 100
        await asyncio.wait_for(task, 1)
        assert played == ''.join(passages).encode()
    finally:
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)


def test_inline_details_preserve_hint_size(settings):
    from PySide6.QtWidgets import QToolButton
    from notolog.modules.text_to_speech.settings_widget import SpeechSettingsWidget
    from notolog.ui.label_with_hint import LabelWithHint
    widget = SpeechSettingsWidget()
    default_size = QToolButton().iconSize()
    for hint in widget.findChildren(LabelWithHint):
        assert hint.icon_button.iconSize() == default_size
    widget.close()


@pytest.mark.asyncio
async def test_native_audio_uses_continuous_device(settings, monkeypatch):
    from notolog.modules.text_to_speech import controller as controller_module
    captured = bytearray()

    class Sink:
        write_available = 4
        drained = True

        def __init__(self, *args):
            pass

        def check(self):
            pass

        def write(self, data):
            captured.extend(data)
            return len(data)

        def close(self):
            pass

    monkeypatch.setattr(controller_module, 'AudioOutput', Sink)
    controller = SpeechController()
    requested = []

    async def stream(text):
        requested.append(text)
        yield b'\0\0' * 10
        # A codec callback may end in the middle of a word: do not play it yet.
        assert not captured
        await asyncio.sleep(0)
        yield b'\1\0' * 10

    controller.runtime = SimpleNamespace(rate=22050, stream=stream, close=Mock())
    await controller._play_stream('First sentence.\nSecond sentence.')
    assert requested == ['First sentence. Second sentence.']
    assert captured == b'\0\0' * 10 + b'\1\0' * 10
    assert controller.sink is None


@pytest.mark.asyncio
async def test_native_pipe_applies_backpressure(settings):
    import base64
    from notolog.modules.text_to_speech.native_runtime import NativeRuntime
    adapter = NativeRuntime(settings)
    adapter.process = Mock()
    adapter.events = asyncio.Queue()
    adapter.events.put_nowait({'pcm': base64.b64encode(b'1234').decode()})
    adapter.events.put_nowait({'done': True})
    stream = adapter.stream('Private note')
    assert await anext(stream) == b'1234'
    assert adapter.process.write.call_count == 1  # request only, no acknowledgement yet
    with pytest.raises(StopAsyncIteration):
        await anext(stream)
    assert adapter.process.write.call_args.args == (b'continue\n',)


def test_speech_error_stops_timer_before_modal_error_handler(settings):
    from notolog.modules.text_to_speech.settings_widget import SpeechSettingsWidget
    widget = SpeechSettingsWidget()
    widget.timer.start()
    widget.report_status('module_text_to_speech_status_unavailable')
    assert not widget.timer.isActive()
    widget.voice_error('Playback failed')
    assert widget.state == 'error'
    assert not widget.timer.isActive()
    widget.close()


def test_status_column_and_tab_header(settings):
    from PySide6.QtWidgets import QLabel
    from notolog.modules.text_to_speech.settings_widget import SpeechSettingsWidget
    widget = SpeechSettingsWidget()
    assert widget.findChild(QLabel, 'speech_tab_title').text() == 'Text-to-Speech'
    panel = widget.panel.layout()
    assert panel.itemAtPosition(0, 0).widget() is widget.status_icon
    assert panel.itemAtPosition(1, 0).widget() is widget.activity
    assert panel.itemAtPosition(2, 1).widget() is widget.output
    assert widget.status_icon.contentsMargins().top() == 0
    widget.close()


def test_playback_bar_does_not_move_icons_when_status_changes(settings, monkeypatch):
    from notolog.modules.text_to_speech.playback_bar import PlaybackBar
    from notolog.modules.text_to_speech.i18n import catalog
    monkeypatch.setitem(catalog('en').get_by_scope('common'), 'module_text_to_speech_status_loading',
                        'An unusually long native speech loading message')
    controller = SpeechController()
    host = SimpleNamespace(get_speech_controller=lambda: controller, action_read_aloud=Mock(),
                           action_pause_speech=Mock(), action_stop_speech=Mock())
    bar = PlaybackBar(host)
    bar.show()
    assert bar.status.isHidden()
    before = bar.sizeHint().width()
    controller.preparing = True
    bar.update_status('module_text_to_speech_status_loading')
    assert bar.sizeHint().width() == before
    assert bar.status.toolTip() == 'An unusually long native speech loading message'
    assert bar.status.timer.isActive()
    assert not bar.status.isHidden()
    controller.preparing = False
    bar.update_status('module_text_to_speech_status_finished')
    assert not bar.status.timer.isActive()
    assert bar.status.isHidden()
    assert not bar.pause.isEnabled()
    assert not bar.stop.isEnabled()
    bar.close()


@pytest.mark.parametrize('message,paused,play_icon,pause_icon,file_icon', [
    ('module_text_to_speech_status_ready', False, 'play-fill.svg', 'pause-fill.svg', 'soundwave.svg'),
    ('module_text_to_speech_status_reading', False, 'play-fill.svg', 'pause-fill.svg', 'soundwave.svg'),
    ('module_text_to_speech_status_paused', True, 'play-fill.svg', 'pause-fill.svg', 'soundwave.svg'),
    ('module_text_to_speech_status_finished', False, 'play-fill.svg', 'pause-fill.svg', 'soundwave.svg'),
])
def test_playback_buttons_remain_filled_and_metadata_tracks_playback(
        settings, message, paused, play_icon, pause_icon, file_icon):
    from PySide6.QtGui import QColor
    from notolog.helpers.theme_helper import ThemeHelper
    from notolog.modules.text_to_speech.playback_bar import PlaybackBar
    controller = SpeechController()
    host = SimpleNamespace(get_speech_controller=lambda: controller, action_read_aloud=Mock(),
                           action_pause_speech=Mock(), action_stop_speech=Mock())
    bar = PlaybackBar(host)
    controller.paused = paused
    controller.sink = SimpleNamespace(playing=message == 'module_text_to_speech_status_reading')
    bar.update_status(message)
    theme = ThemeHelper()
    for widget, icon, name in [(bar.play, play_icon, 'play'), (bar.pause, pause_icon, 'pause'),
                               (bar.metadata, file_icon, 'metadata')]:
        selected = (message == 'module_text_to_speech_status_reading' and name in ('play', 'metadata')) or (
                paused and name == 'pause')
        key = f'toolbar_icon_color_tts_{name}' + ('_act' if selected else '')
        expected = theme.get_icon(theme_icon=icon, color=QColor(theme.get_color(key))).pixmap(bar.icon_size)
        actual = widget.pixmap() if widget is bar.metadata else widget.icon().pixmap(bar.icon_size)
        assert actual.toImage() == expected.toImage()
    assert bar.layout().itemAt(bar.layout().count() - 1).widget() is bar.metadata
    assert bar.metadata.size() == bar.stop.size()
    bar.close()


def test_playback_metadata_uses_loaded_runtime_and_refreshes_preferences(settings):
    from notolog.modules.text_to_speech.playback_bar import PlaybackBar
    controller = SpeechController()
    host = SimpleNamespace(get_speech_controller=lambda: controller, action_read_aloud=Mock(),
                           action_pause_speech=Mock(), action_stop_speech=Mock())
    bar = PlaybackBar(host)
    assert 'Sample rate: Not loaded' in bar.metadata.toolTip()
    assert bar.metadata.toolTip().startswith('Voice:')
    tooltip = bar.metadata.toolTip()
    assert tooltip.index('Runtime:') < tooltip.index('Model:') < tooltip.index('Codec model:')
    assert 'Stopped' not in bar.metadata.toolTip()
    gap = bar.layout().itemAt(bar.layout().count() - 2).spacerItem()
    assert gap.sizeHint().width() > 0
    controller.runtime = SimpleNamespace(
        loaded=True, rate=22050, close=Mock(),
        configuration=('/runtime', ('/models/magpie.gguf', '/models/codec.gguf', '/tok')))
    settings.tts_voice = 'Sofia'
    settings.tts_language = 'es'
    settings.tts_speed = 1.5
    bar.update_status('module_text_to_speech_status_reading')
    assert 'Reading aloud' not in bar.metadata.toolTip()
    for detail in ['Model: magpie.gguf', 'Codec model: codec.gguf', 'Voice: Sofia', 'Language: Spanish (es)',
                   'Sample rate: 22,050 Hz', 'Playback rate: 33,075 Hz', 'PCM, 16-bit signed, mono', 'Speed: 1.5 ×']:
        assert detail in bar.metadata.toolTip()
    settings.tts_voice = 'John'
    assert 'Voice: John' in bar.metadata.toolTip()
    bar.close()


@pytest.mark.asyncio
async def test_speech_failure_while_paused_does_not_pause_next_read(settings):
    settings.tts_enabled = True
    controller = SpeechController()
    controller.runtime = SimpleNamespace(start=AsyncMock(), close=Mock())
    controller._play_stream = AsyncMock(side_effect=RuntimeError('Synthesis failed'))
    controller.read('First read.')
    controller.paused = True
    await controller.task
    assert controller.task is None
    assert not controller.paused
    controller._play_stream = AsyncMock()
    controller.read('Next read.')
    await controller.task
    controller._play_stream.assert_awaited_once_with('Next read.')
    controller.stop()


@pytest.mark.parametrize('font_size', [12, 20])
def test_playback_matches_search_buttons_and_has_separator(settings, qapp, font_size):
    from PySide6.QtGui import QAction, QFont
    from notolog.ui.toolbar import ToolBar
    from notolog.modules.text_to_speech.playback_bar import PlaybackBar
    host = QMainWindow()
    host.setFont(QFont('Sans', font_size))
    controller = SpeechController(host)
    host.speech_enabled = lambda: True
    host.get_speech_controller = lambda: controller
    host.action_read_aloud = host.action_pause_speech = host.action_stop_speech = Mock()
    toolbar = ToolBar(host)
    host.addToolBar(toolbar)
    host.show()
    qapp.processEvents()
    bar = toolbar.findChild(PlaybackBar)
    reference = toolbar.search_form.btn_search_next
    for button in (bar.play, bar.pause, bar.stop):
        assert type(button) is type(reference)
        assert button.size() == reference.size()
        assert button.iconSize() == reference.iconSize()
    assert bar.layout().spacing() == 0
    assert bar.layout().contentsMargins().left() == 0
    separator = toolbar.findChild(QAction, 'speech_search_separator')
    assert separator.isSeparator()
    assert bar.x() < toolbar.actionGeometry(separator).x() < toolbar.search_form.x()
    bar.update_status('module_text_to_speech_status_preparing')
    controller.paused = True
    bar.update_status('module_text_to_speech_status_paused')
    assert bar.pause.isChecked()
    assert bar.status.isHidden()
    assert not bar.status.timer.isActive()
    bar.hide()
    assert not bar.status.timer.isActive()
    host.close()


def test_idle_reading_preferences_preserve_loaded_models(settings):
    controller = SpeechController()
    controller.runtime = SimpleNamespace(close=Mock())
    for key, value in [('tts_voice', 'Sofia'), ('tts_language', 'en'), ('tts_speed', 1.2),
                       ('tts_skip_inline_code', False)]:
        setattr(settings, key, value)
    controller.runtime.close.assert_not_called()
    settings.tts_model_directory = '/changed/models'
    controller.runtime.close.assert_called_once()


@pytest.mark.asyncio
async def test_native_runtime_reuses_the_same_loaded_process(settings, monkeypatch):
    from PySide6.QtCore import QProcess
    from notolog.modules.text_to_speech import native_runtime
    adapter = native_runtime.NativeRuntime(settings)
    paths = ('magpie.gguf', 'codec.gguf', 'tokenizers')
    monkeypatch.setattr(native_runtime, 'model_paths', lambda _: paths)
    monkeypatch.setattr(native_runtime, 'runtime_path', lambda _: '/runtime/bin/nemo-speech')
    validate = AsyncMock()
    monkeypatch.setattr(native_runtime, 'validate_runtime', validate)
    process = adapter.process = Mock()
    process.state.return_value = QProcess.ProcessState.Running
    adapter.configuration = ('/runtime/bin/nemo-speech', paths)
    assert adapter.loaded
    for _ in range(3):
        await adapter.start()
    assert adapter.process is process
    validate.assert_not_awaited()
    process.start.assert_not_called()


@pytest.mark.asyncio
@pytest.mark.parametrize('frozen', [False, True])
@pytest.mark.parametrize('platform,key,separator', [
    ('linux', 'LD_LIBRARY_PATH', ':'),
    ('darwin', 'DYLD_LIBRARY_PATH', ':'),
    ('win32', 'PATH', ';'),
])
@pytest.mark.parametrize('inherited', [None, '', '{sep}/first{sep}{sep}/second{sep}'])
@pytest.mark.parametrize('directory', ['runtime', 'Speech runtime 世界'])
async def test_native_runtime_launches_worker_for_installation_type(
        settings, monkeypatch, frozen, platform, key, separator, inherited, directory):
    from pathlib import PurePosixPath, PureWindowsPath
    from PySide6.QtCore import QProcessEnvironment
    from notolog.modules.text_to_speech import native_runtime

    class RuntimePath(PureWindowsPath if platform == 'win32' else PurePosixPath):
        def resolve(self):
            return self

        def is_file(self):
            return self == library

    root = RuntimePath('C:/' if platform == 'win32' else '/') / directory
    library = root / {'linux': 'lib/libnemo_speech_tts.so.1', 'darwin': 'lib/libnemo_speech_tts.dylib',
                      'win32': 'bin/nemo_speech_tts.dll'}[platform]
    monkeypatch.setattr(native_runtime, 'Path', RuntimePath)
    monkeypatch.setattr(native_runtime.sys, 'frozen', frozen, raising=False)
    monkeypatch.setattr(native_runtime.sys, 'platform', platform)
    monkeypatch.setattr(native_runtime.os, 'pathsep', separator)
    env = QProcessEnvironment()
    if inherited is not None:
        env.insert(key, inherited.format(sep=separator))
    monkeypatch.setattr(native_runtime, 'process_environment', lambda _: env)
    monkeypatch.setattr(native_runtime, 'runtime_path', lambda _: str(root / 'bin' / 'nemo-speech'))
    monkeypatch.setattr(native_runtime, 'model_paths', lambda _: ('model', 'codec', 'tokenizers'))
    monkeypatch.setattr(native_runtime, 'validate_runtime', AsyncMock())
    monkeypatch.setattr(native_runtime, 'isolate_process', Mock())
    monkeypatch.setattr(native_runtime, 'stop_process', Mock())
    process = Mock()
    monkeypatch.setattr(native_runtime, 'QProcess', Mock(return_value=process))
    adapter = native_runtime.NativeRuntime(settings)
    adapter.event = AsyncMock(return_value={'ready': 22050})
    await adapter.start()
    worker_env = process.setProcessEnvironment.call_args.args[0]
    expected_paths = [str(library.parent)] + (['/first', '/second'] if inherited else [])
    assert worker_env.value(key).split(separator) == expected_paths
    executable, arguments = process.start.call_args.args
    assert executable == native_runtime.sys.executable
    if frozen:
        assert arguments == ['--tts-worker']
    else:
        assert arguments[0] == '-u'
        assert arguments[1] == str(RuntimePath(native_runtime.__file__).with_name('native_worker.py'))
    assert adapter.rate == 22050
    adapter.close()


@pytest.mark.asyncio
async def test_voice_test_has_no_settings_progress_bar(settings, monkeypatch, qapp):
    from PySide6.QtWidgets import QProgressBar
    from notolog.modules.text_to_speech.settings_widget import SpeechSettingsWidget
    widget = SpeechSettingsWidget()
    widget.show()

    async def voice():
        widget.report('Preparing speech…')
        widget.tick()
        qapp.processEvents()
        assert not widget.findChildren(QProgressBar)
        assert 'elapsed' in widget.progress_status.text()

    monkeypatch.setattr(widget, '_test_voice', voice)
    await widget._run(widget._test_voice)
    assert not widget.findChildren(QProgressBar)
    assert not widget.timer.isActive()
    widget.close()


@pytest.mark.asyncio
async def test_native_failed_passage_never_plays_partial_words(settings, monkeypatch):
    from notolog.modules.text_to_speech import controller as controller_module
    sink = Mock()
    monkeypatch.setattr(controller_module, 'AudioOutput', Mock(return_value=sink))
    controller = SpeechController()

    async def stream(_):
        yield b'\0\0' * 10
        raise RuntimeError('Synthesis failed')

    controller.runtime = SimpleNamespace(rate=22050, stream=stream, close=Mock())
    with pytest.raises(RuntimeError, match='Synthesis failed'):
        await controller._play_stream('An incomplete sentence.')
    sink.write.assert_not_called()
    sink.close.assert_called_once()
    assert controller.sink is None


@pytest.mark.parametrize('code,detail,expected', [
    (3, 'MagpieTTS synthesis failed', 'generation failed'),
    (1, "unknown voice_name 'secret'", 'voice is not supported'),
    (2, 'out of memory', 'ran out of memory'),
])
def test_native_error_messages_do_not_leak_text_or_misidentify_runtime_failures(code, detail, expected):
    from notolog.modules.text_to_speech.native_worker import synthesis_error
    message = synthesis_error(code, detail)
    assert expected in message
    assert 'secret' not in message


@pytest.mark.parametrize('source,expected', [
    ('Header 1. Header 2. Header 3. Header 4. Header 5. Header 6.',
     'Header one. Header two. Header three. Header four. Header five. Header six.'),
    ('There are 12 items and 1,234 files.', 'There are twelve items and one thousand two hundred thirty four files.'),
    ('Value 3.14, ID 007.', 'Value three point one four, ID zero zero seven.'),
    ('Python3 v1.2.3', 'Python3 v1.2.3'),
])
def test_english_numbers_are_spoken_words(source, expected):
    from notolog.modules.text_to_speech.text import normalize_numbers
    assert normalize_numbers(source, 'en-US') == expected
    assert normalize_numbers(source, 'de-DE') == source


@pytest.mark.asyncio
async def test_headings_keep_distinct_numbers_when_sent_to_runtime(settings):
    settings.tts_enabled = True
    controller = SpeechController()
    controller.runtime = SimpleNamespace(start=AsyncMock(), close=Mock())
    controller._play_stream = AsyncMock()
    controller.read('\n'.join('#' * n + f' Header {n}' for n in range(1, 7)))
    await controller.task
    assert all(section.heading for section in controller._play_stream.call_args.args[0])
    assert '\n'.join(section.text for section in controller._play_stream.call_args.args[0]) == (
        'Chapter: Header one\nSection: Header two\nSubsection: Header three\n'
        'Sub-subsection: Header four\nHeading level five: Header five\nHeading level six: Header six')
    controller.stop()


@pytest.mark.parametrize('html', [False, True])
def test_heading_announcements_are_optional_and_follow_levels(html):
    source = ('<h1>Title</h1><h2>Topic</h2><h3>Detail</h3><h4>Part</h4><h5>Branch</h5><h6>Leaf</h6>' if html else
              '# Title\n## Topic\n### Detail\n#### Part\n##### Branch\n###### Leaf')
    assert prepare_text(source, html=html, announce_headings=True) == (
        'Chapter: Title\nSection: Topic\nSubsection: Detail\nSub-subsection: Part\n'
        'Heading level 5: Branch\nHeading level 6: Leaf')
    assert prepare_text(source, html=html) == 'Title\nTopic\nDetail\nPart\nBranch\nLeaf'


def test_settings_details_loader_stops_for_terminal_states(settings):
    from notolog.modules.text_to_speech.settings_widget import SpeechSettingsWidget
    widget = SpeechSettingsWidget()
    widget.show()
    width = widget.activity.width()
    assert widget.activity.scale == 1
    assert width == widget.status_icon.pixmap().deviceIndependentSize().width()
    for message, state, running in [('Checking files', 'busy', True), ('Verified', 'success', False),
                                    ('module_text_to_speech_status_loading', None, True),
                                    ('module_text_to_speech_status_paused', None, False),
                                    ('module_text_to_speech_status_reading', None, True),
                                    ('module_text_to_speech_status_unavailable', None, False),
                                    ('module_text_to_speech_status_stopped', None, False),
                                    ('module_text_to_speech_status_finished', None, False)]:
        widget.operation = 'test'
        if state is None:
            widget.report_status(message)
        else:
            widget.report(message, state)
        assert widget.activity.running == running
        assert widget.status_icon.isVisible()
        assert widget.activity.width() == width
    widget.append_details('\x1b[32m10%\r20%\x1b[0m\n')
    assert '10%\n20%' in widget.output.toPlainText()
    assert '\x1b' not in widget.output.toPlainText()
    widget.report('Ready')
    widget.append_details('Loading')
    widget.append_details(' files\n')
    assert widget.output.toPlainText().endswith('Ready\nLoading files\n')
    widget.close()


def test_translation_catalogs_match_app_languages_and_placeholders():
    from string import Formatter
    from notolog.enums.languages import Languages
    from notolog.modules.text_to_speech.i18n import LEXEMES_PATH, catalog

    languages = {language.name.lower() for language in Languages}
    available = {path.name for path in LEXEMES_PATH.iterdir() if path.is_dir() and not path.name.startswith('_')}
    assert available == languages

    def fields(text):
        return {name for _, name, _, _ in Formatter().parse(text) if name is not None}

    english = catalog('en').get_all()
    assert english.keys() == {'common', 'settings_dialog'}
    for language in languages:
        translated = catalog(language).get_all()
        assert translated.keys() == english.keys(), language
        for scope, sources in english.items():
            entries = translated[scope]
            assert entries.keys() == sources.keys(), (language, scope)
            for key, source in sources.items():
                assert key.startswith('module_text_to_speech_'), key
                assert key.startswith('module_text_to_speech_config_') == (scope == 'settings_dialog'), key
                assert entries[key].strip(), (language, key)
                assert fields(entries[key]) == fields(source), (language, key)
    assert catalog('unknown').get('module_text_to_speech_name') == 'Text-to-Speech'
    assert catalog('unknown', default_scope='settings_dialog').get(
        'module_text_to_speech_config_test_voice_button') == 'Test voice'


def test_translation_keys_survive_english_copy_changes(settings, monkeypatch):
    from notolog.modules.text_to_speech.i18n import catalog, tr
    from notolog.modules.text_to_speech.settings_widget import SpeechSettingsWidget
    settings.app_language = 'es'
    english = catalog('en').get_by_scope('common')
    for key in ('module_text_to_speech_action_read', 'module_text_to_speech_action_read_selection'):
        expected = catalog('es').get(key)
        monkeypatch.setitem(english, key, 'The same revised English label')
        assert tr(key) == expected
    key = 'module_text_to_speech_config_test_voice_button'
    expected = catalog('es', default_scope='settings_dialog').get(key)
    monkeypatch.setitem(catalog('en').get_by_scope('settings_dialog'), key, 'Try this voice')
    widget = SpeechSettingsWidget()
    assert widget.test.text() == expected
    # Runtime diagnostics and formatted values are opaque text, not translation identifiers.
    message = 'Text-to-Speech {unchanged}'
    widget.report(tr('module_text_to_speech_error', error=message), 'error')
    assert widget.status.text().endswith(message)
    widget.report('Text-to-Speech')
    assert widget.status.text() == 'Text-to-Speech'
    widget.close()


def test_playback_state_does_not_depend_on_translated_words(settings, monkeypatch):
    from notolog.modules.text_to_speech.i18n import catalog
    from notolog.modules.text_to_speech.playback_bar import PlaybackBar
    from notolog.modules.text_to_speech.settings_widget import SpeechSettingsWidget
    settings.app_language = 'es'
    for entries in (catalog('es').get_by_scope('common'),
                    catalog('es', default_scope='settings_dialog').get_by_scope('common')):
        for suffix in ('preparing', 'stopped'):
            monkeypatch.setitem(entries, 'module_text_to_speech_status_' + suffix, 'Identical display text')
    controller = SpeechController()
    editor = SimpleNamespace(get_speech_controller=lambda: controller, action_read_aloud=Mock(),
                             action_pause_speech=Mock(), action_stop_speech=Mock())
    bar = PlaybackBar(editor)
    widget = SpeechSettingsWidget()
    widget.operation = 'test'
    controller.status_changed.connect(widget.report_status)
    for suffix, active in [('preparing', True), ('stopped', False)]:
        key = 'module_text_to_speech_status_' + suffix
        controller.status_changed.emit(key)
        assert controller.status_key == key
        assert bar.status.toolTip() == widget.status.text() == 'Identical display text'
        assert bar.pause.isEnabled() == active
        assert bar.stop.isEnabled() == active
        assert widget.activity.running == active
    controller.status_changed.disconnect(widget.report_status)
    widget.operation = None
    widget.close()
    bar.close()


def test_settings_language_dropdown_refreshes_existing_speech_tab(settings, monkeypatch):
    from PySide6.QtWidgets import QLabel
    from notolog.enums.languages import Languages
    from notolog.ui.enum_combo_box import EnumComboBox
    from notolog.ui.settings_dialog import SettingsDialog
    from notolog.modules.modules import Modules
    from notolog.modules import text_to_speech
    from notolog.modules.text_to_speech.settings_widget import SpeechSettingsWidget
    from notolog.modules.text_to_speech.i18n import tr
    monkeypatch.setattr(Modules, 'get_by_extension', lambda *_: [text_to_speech])
    host = QMainWindow()
    host.settings = settings
    dialog = SettingsDialog(host)
    widget = dialog.findChild(SpeechSettingsWidget)
    tab = widget.parentWidget().parentWidget()
    combo = dialog.findChild(EnumComboBox, 'settings_dialog_general_app_language_combo:app_language')
    widget.report_status('module_text_to_speech_status_reading')
    try:
        for language in (Languages.ES, Languages.EN):
            combo.setCurrentIndex(combo.findData(language))
            assert settings.app_language == language.name.lower()
            assert dialog.findChild(SpeechSettingsWidget) is widget
            assert widget.findChild(QLabel, 'speech_tab_title').text() == tr('module_text_to_speech_name')
            assert dialog.tab_widget.tabText(dialog.tab_widget.indexOf(tab)) == tr('module_text_to_speech_name')
            assert widget.findChild(QCheckBox, 'tts_enabled').text() == tr(
                'module_text_to_speech_config_enabled_label', scope='settings_dialog')
            assert widget.output.toPlainText().endswith(tr('module_text_to_speech_status_reading') + '\n')
    finally:
        dialog.close()
        host.deleteLater()


def test_live_settings_translations_match_new_widgets_in_every_language(settings):
    from PySide6.QtWidgets import QWidget
    from notolog.enums.languages import Languages
    from notolog.modules.text_to_speech.settings_widget import SpeechSettingsWidget
    settings.tts_language = 'ja'
    settings.tts_voice = 'Sofia'
    settings.tts_context_length = 0
    widget = SpeechSettingsWidget()

    def texts(panel):
        result = []
        for child in panel.findChildren(QWidget):
            for name in ('text', 'toolTip', 'accessibleName', 'placeholderText'):
                getter = getattr(child, name, None)
                if callable(getter):
                    result.append((type(child).__name__, child.objectName(), name, getter()))
        return result

    changed = Mock()
    settings.value_changed.connect(changed)
    try:
        for language in Languages:
            changed.reset_mock()
            settings.app_language = language.name.lower()
            assert all(set(call.args[0]) == {'app_language'} for call in changed.call_args_list)
            fresh = SpeechSettingsWidget()
            try:
                assert texts(widget) == texts(fresh), language
                assert [widget.language.itemText(i) for i in range(widget.language.count())] == [
                    fresh.language.itemText(i) for i in range(fresh.language.count())]
                assert widget.language.currentData().name == 'JA'
                assert settings.tts_language == 'ja'
                assert widget.findChild(QLineEdit, 'tts_voice').text() == 'Sofia'
                assert widget.context.value() == len(config.CONTEXT_LENGTHS) - 1
            finally:
                fresh.deleteLater()
        widget.findChild(QLineEdit, 'tts_runtime_path').setText('/pending/runtime')
        assert widget.refresh_timer.isActive()
        settings.app_language = 'en'
        assert not widget.download.isEnabled() and not widget.test.isEnabled()
    finally:
        settings.value_changed.disconnect(changed)
        widget.deleteLater()


@pytest.mark.asyncio
@pytest.mark.parametrize('operation', ['download', 'test'])
async def test_live_language_refresh_preserves_running_speech_operations(settings, monkeypatch, operation):
    from notolog.modules.text_to_speech import settings_widget
    from notolog.modules.text_to_speech.i18n import tr
    from notolog.modules.text_to_speech.playback_bar import PlaybackBar
    widget = settings_widget.SpeechSettingsWidget()
    controller = SpeechController()
    editor = SimpleNamespace(get_speech_controller=lambda: controller, action_read_aloud=Mock(),
                             action_pause_speech=Mock(), action_stop_speech=Mock())
    bar = PlaybackBar(editor)
    started = asyncio.Event()
    finish = asyncio.Event()

    async def pending_operation():
        if operation == 'download':
            widget.download_pending = ''
            widget.download_output('[model] downloading model.gguf (tts, 128.0 MiB)\n')
        else:
            widget.report_status('module_text_to_speech_status_preparing')
        started.set()
        await finish.wait()

    if operation == 'test':
        monkeypatch.setattr(widget, '_test_voice', pending_operation)
    widget.task = asyncio.create_task(widget._run(pending_operation))
    await started.wait()
    controller.paused = True
    controller.status_changed.emit('module_text_to_speech_status_paused')
    log_lines = widget.output.toPlainText().count('\n')
    start_time = widget.started
    try:
        for language in ('es', 'ru', 'en'):
            settings.app_language = language
            await asyncio.sleep(0)
            assert not widget.task.done()
            assert widget.operation == operation
            assert widget.started == start_time
            assert widget.timer.isActive() and widget.activity.running
            assert all(not field.isEnabled() for field in widget.fields)
            assert widget.output.toPlainText().count('\n') == log_lines
            button, key = ((widget.download, 'module_text_to_speech_config_cancel_button')
                           if operation == 'download' else (widget.test, 'module_text_to_speech_config_stop_button'))
            assert button.isEnabled()
            assert button.text() == tr(key, scope='settings_dialog')
            expected = (tr('module_text_to_speech_config_progress_downloading', scope='settings_dialog',
                           number=1, role=tr('module_text_to_speech_config_download_role_voice',
                                             scope='settings_dialog'), size='128.0')
                        if operation == 'download' else tr('module_text_to_speech_status_preparing'))
            assert widget.status.text() == expected
            assert widget.status_icon.accessibleName() == expected
            assert widget.output.toPlainText().endswith(expected + '\n')
            if operation == 'download':
                assert '[model] downloading model.gguf (tts, 128.0 MiB)\n' in widget.output.toPlainText()
            assert bar.pause.isChecked() and bar.pause.isEnabled() and bar.stop.isEnabled()
            assert bar.status.toolTip() == tr('module_text_to_speech_status_paused')
            assert bar.play.toolTip() == tr('module_text_to_speech_action_read')
            assert bar.pause.accessibleName() == tr('module_text_to_speech_action_pause_resume')
            assert bar.stop.toolTip() == tr('module_text_to_speech_action_stop')
            assert bar.metadata.accessibleName() == tr('module_text_to_speech_playback_details')
            assert tr('module_text_to_speech_playback_voice', value=settings.tts_voice) in bar.metadata.toolTip()
        finish.set()
        await widget.task
        widget.report_key('module_text_to_speech_error', 'error', scope='common', error='/tmp/{file}')
        settings.app_language = 'es'
        assert widget.status.text() == tr('module_text_to_speech_error', error='/tmp/{file}')
        assert widget.state == 'error' and not widget.timer.isActive()
        widget.voice_error('Native error {verbatim}')
        settings.app_language = 'en'
        assert widget.status.text() == 'Native error {verbatim}'
        assert widget.output.toPlainText().endswith('Native error {verbatim}\n')
        assert tr('module_text_to_speech_error', error='/tmp/{file}') in widget.output.toPlainText()
    finally:
        finish.set()
        await widget.task
        widget.deleteLater()
        bar.deleteLater()


@pytest.mark.parametrize('module_name', ['llama_cpp', 'ondevice_llm', 'openai_api'])
def test_settings_modules_share_language_updates(settings, monkeypatch, module_name):
    from PySide6.QtCore import QSignalBlocker
    from PySide6.QtWidgets import QLabel
    from notolog.lexemes.lexemes import Lexemes
    from notolog.modules.modules import Modules
    from notolog.modules import text_to_speech
    from notolog.ui.settings_dialog import SettingsDialog
    from notolog.ui.widget_translations import WidgetTranslations
    from notolog.ui.label_with_hint import LabelWithHint
    from notolog.modules.text_to_speech.settings_widget import SpeechSettingsWidget
    module = pytest.importorskip('notolog.modules.' + module_name)
    monkeypatch.setattr(Modules, 'get_by_extension', lambda *_: [module, text_to_speech])
    host = QMainWindow()
    host.settings = settings
    dialog = SettingsDialog(host)
    speech = dialog.findChild(SpeechSettingsWidget)
    assert isinstance(dialog.translations, WidgetTranslations)
    assert isinstance(speech.translations, WidgetTranslations)
    key = 'module_openai_api_label' if module_name == 'openai_api' else f'module_{module_name}_config_label'
    label = dialog.findChild(QLabel, 'settings_dialog_' + key)
    assert label is not None
    field = next(item for item in dialog.findChildren(QLineEdit)
                 if item.objectName().startswith(f'settings_dialog_module_{module_name}_'))
    with QSignalBlocker(field):
        field.setText('Uncommitted {value}')
    create = Mock(side_effect=AssertionError('Language changes must not instantiate modules'))
    monkeypatch.setattr(Modules, 'create', create)
    try:
        for language in ('es', 'ru', 'en'):
            settings.app_language = language
            expected = Lexemes(language, default_scope='settings_dialog',
                               lexemes_dir=module.ModuleCore.get_lexemes_path())
            assert label.text() == expected.get(key)
            assert field.text() == 'Uncommitted {value}'
            for hint in dialog.findChildren(LabelWithHint):
                tooltip_key = hint.property('tooltip_lexeme')
                if tooltip_key and tooltip_key.startswith(f'module_{module_name}_'):
                    assert ' '.join(hint.icon_button.toolTip().split()) == ' '.join(expected.get(tooltip_key).split())
            tab_key = ('tab_module_llama_cpp_config' if module_name == 'llama_cpp'
                       else f'tab_{module_name}_config')
            assert expected.get(tab_key) in [dialog.tab_widget.tabText(i)
                                             for i in range(dialog.tab_widget.count())]
            assert speech.lexemes.language == dialog.lexemes.language == language
            assert speech.output.toPlainText() == speech.status.text() + '\n'
        create.assert_not_called()
    finally:
        dialog.close()
        host.deleteLater()


def test_speech_terminal_retranslates_retained_messages_and_new_messages(settings):
    from notolog.modules.text_to_speech.i18n import tr
    from notolog.modules.text_to_speech.settings_widget import SpeechSettingsWidget
    widget = SpeechSettingsWidget()
    widget.report_status('module_text_to_speech_status_reading')
    widget.append_details('Native {output} <untouched>\nPartial')
    try:
        for language in ('es', 'ru', 'ja', 'en', 'es'):
            settings.app_language = language
            log = widget.output.toPlainText()
            assert tr('module_text_to_speech_status_reading') + '\n' in log
            assert log.endswith('Native {output} <untouched>\nPartial')
            assert log.count('Native {output}') == 1
        widget.append_details(' chunk\n')
        widget.report_status('module_text_to_speech_status_finished')
        assert widget.output.toPlainText().endswith(tr('module_text_to_speech_status_finished') + '\n')
        settings.app_language = 'en'
        assert 'Partial chunk\n' in widget.output.toPlainText()
        assert widget.output.toPlainText().endswith('Finished reading.\n')
    finally:
        widget.deleteLater()


def test_speech_terminal_history_stays_bounded_across_language_changes(settings):
    from notolog.modules.text_to_speech.settings_widget import SpeechSettingsWidget
    widget = SpeechSettingsWidget()
    widget.report_status('module_text_to_speech_status_reading')
    try:
        for index in range(300):
            widget.append_details(f'native line {index}\n')
        retained = widget.output.toPlainText()
        for language in ('es', 'ru', 'en'):
            settings.app_language = language
            assert widget.output.toPlainText() == retained
            assert widget.output.document().blockCount() <= 200
        widget.append_details('x' * 100000)
        assert len(widget.output.toPlainText()) <= widget.output.MAX_CHARACTERS
        settings.app_language = 'es'
        assert widget.output.toPlainText() == 'x' * widget.output.MAX_CHARACTERS
        widget.output.clear()
        settings.app_language = 'en'
        assert widget.output.toPlainText() == ''
    finally:
        widget.deleteLater()


def test_speech_translation_call_sites_use_existing_scoped_keys():
    import ast
    from notolog.modules.text_to_speech.i18n import LEXEMES_PATH, catalog
    module = LEXEMES_PATH.parent
    app = module.parents[1]
    files = [*module.glob('*.py'), app / 'notolog_editor.py', app / 'ui/file_tree_context_menu.py']
    for path in files:
        for node in ast.walk(ast.parse(path.read_text(encoding='utf-8'))):
            if not isinstance(node, ast.Call) or not node.args or not isinstance(node.args[0], ast.Constant):
                continue
            direct = isinstance(node.func, ast.Name) and node.func.id in ('tr', 'speech_tr')
            settings_lookup = (path.name == 'settings_widget.py' and isinstance(node.func, ast.Attribute)
                               and ast.unparse(node.func) == 'self.lexemes.get')
            if not (direct or settings_lookup):
                continue
            key = node.args[0].value
            scope = 'settings_dialog' if settings_lookup else 'common'
            scope = next((kw.value.value for kw in node.keywords if kw.arg == 'scope'), scope)
            assert key.startswith('module_text_to_speech_'), (path, node.lineno, key)
            assert catalog('en').get(key, scope=scope), (path, node.lineno, scope, key)


@pytest.mark.parametrize('language,title,reading', [
    ('es', 'Texto a voz', 'Leyendo en voz alta…'),
    ('ru', 'Озвучивание текста', 'Чтение вслух…'),
    ('ja', 'テキスト読み上げ', '読み上げ中…'),
])
def test_translated_settings_keep_speech_language_and_activity(settings, language, title, reading):
    from notolog.modules.text_to_speech.settings_widget import SpeechSettingsWidget
    from notolog.modules.text_to_speech.i18n import tr
    from PySide6.QtWidgets import QLabel
    settings.app_language = language
    settings.tts_language = 'en'
    widget = SpeechSettingsWidget()
    assert widget.findChild(QLabel, 'speech_tab_title').text() == title
    assert widget.test.text() == tr('module_text_to_speech_config_test_voice_button', scope='settings_dialog')
    assert widget.language.currentData().name == 'EN'
    assert settings.tts_language == 'en'
    widget.operation = 'test'
    widget.report_status('module_text_to_speech_status_reading')
    assert widget.status.text() == reading
    assert widget.activity.running
    widget.report(tr('module_text_to_speech_status_unavailable'), 'error')
    assert not widget.activity.running
    assert widget.status.text() == tr('module_text_to_speech_status_unavailable')
    widget.operation = 'download'
    widget.started = time.monotonic()
    widget.completed_files = 2
    widget.tick()
    assert tr('module_text_to_speech_config_progress_files_complete', scope='settings_dialog',
              count=2) in widget.progress_status.text()
    assert tr('module_text_to_speech_config_progress_elapsed', scope='settings_dialog',
              time='0:00') in widget.progress_status.text()
    assert tr('module_text_to_speech_error', error='/path/{unchanged}').endswith('/path/{unchanged}')
    widget.operation = None
    widget.close()


def test_translated_selection_menu_and_metadata(settings):
    from notolog.modules.text_to_speech.i18n import tr
    from notolog.modules.text_to_speech.playback_bar import PlaybackBar
    settings.app_language = 'ru'
    host = QMainWindow()
    host.speech_enabled = lambda: True
    host.action_read_aloud = Mock()
    widget = EditWidget(host)
    widget.setPlainText('Hello')
    cursor = widget.textCursor()
    cursor.select(QTextCursor.SelectionType.Document)
    widget.setTextCursor(cursor)
    menu = QMenu()
    append_selection_action(widget, menu)
    action = next(
        action for action in menu.actions() if action.text() == tr('module_text_to_speech_action_read_selection'))
    assert action.text() == tr('module_text_to_speech_action_read_selection')
    assert not action.icon().isNull()
    action.trigger()
    host.action_read_aloud.assert_called_once_with(source='Hello')
    controller = SpeechController()
    editor = SimpleNamespace(get_speech_controller=lambda: controller, action_read_aloud=Mock(),
                             action_pause_speech=Mock(), action_stop_speech=Mock())
    bar = PlaybackBar(editor)
    bar.update_status('module_text_to_speech_status_stopped')
    assert tr('module_text_to_speech_status_stopped') not in bar.metadata.toolTip()
    assert tr('module_text_to_speech_playback_model',
              value=tr('module_text_to_speech_model_not_loaded')) in bar.metadata.toolTip()
    assert bar.play.toolTip() == tr('module_text_to_speech_action_read')
    bar.close()
    host.close()


@pytest.mark.parametrize('limit', [10, 20, 40, 80, 160, 640, 0])
def test_context_length_keeps_all_text_and_bounds_requests(limit):
    text = 'word ' * 240
    chunks = list(speech_chunks(text, limit=limit))
    assert ' '.join(chunks) == text.strip()
    if limit:
        assert all(len(chunk) <= limit for chunk in chunks)
    else:
        assert chunks == [text.strip()]


def test_context_slider_saves_lengths_and_whole_document(settings, caplog):
    from notolog.modules.text_to_speech.settings_widget import SpeechSettingsWidget
    from notolog.modules.text_to_speech.config import CONTEXT_LENGTHS
    from notolog.ui.settings_dialog import SettingsDialog
    host = QMainWindow()
    host.settings = settings
    dialog = SettingsDialog(host)
    widget = dialog.findChild(SpeechSettingsWidget)
    for index, length in enumerate(CONTEXT_LENGTHS):
        widget.context.setValue(index)
        assert settings.tts_context_length == length
    assert widget.context_value.text() == 'Whole document'
    assert 'Unhandled internal widget type: qt_tts_context_length' not in caplog.text
    dialog.close()
    host.close()
    restored = SpeechSettingsWidget()
    assert restored.context.value() == restored.context.maximum()
    restored.close()


@pytest.mark.asyncio
@pytest.mark.parametrize('length', [80, 320, 0])
async def test_controller_uses_saved_context_length(settings, monkeypatch, length):
    from notolog.modules.text_to_speech import controller as controller_module
    sink = Mock()
    sink.drained = True
    monkeypatch.setattr(controller_module, 'AudioOutput', Mock(return_value=sink))
    settings.tts_context_length = length
    controller = SpeechController()
    requested = []

    async def stream(text):
        requested.append(text)
        if False:
            yield b''

    controller.runtime = SimpleNamespace(rate=22050, stream=stream, close=Mock())
    text = 'word ' * 100
    await controller._play_stream(text)
    assert requested == list(speech_chunks(text, limit=length))


def test_native_close_discards_queued_audio(settings, monkeypatch):
    from notolog.modules.text_to_speech import native_runtime
    adapter = native_runtime.NativeRuntime(settings)
    adapter.process = Mock()
    adapter.events = asyncio.Queue()
    adapter.events.put_nowait({'pcm': 'private audio'})
    monkeypatch.setattr(native_runtime, 'stop_process', Mock())
    adapter.close()
    assert adapter.events.empty()
    assert adapter.process is None


@pytest.mark.parametrize('selected', [False, True])
def test_read_selection_action_never_falls_back_to_document(settings, selected):
    from notolog.notolog_editor import NotologEditor
    from notolog.editor_state import Mode
    widget = Mock()
    widget.textCursor.return_value.hasSelection.return_value = selected
    host = SimpleNamespace(get_mode=lambda: Mode.EDIT, get_edit_widget=lambda: widget, action_read_aloud=Mock())
    NotologEditor.action_read_selection_aloud(host)
    assert host.action_read_aloud.call_count == int(selected)


def test_context_drag_previews_without_saving_until_release(settings):
    from notolog.modules.text_to_speech.settings_widget import SpeechSettingsWidget
    widget = SpeechSettingsWidget()
    assert settings.tts_context_length == 160
    slider = widget.context
    slider.setSliderDown(True)
    slider.setSliderPosition(slider.minimum())
    assert widget.context_value.text() == '10 characters'
    assert settings.tts_context_length == 160
    slider.setSliderPosition(slider.maximum())
    assert widget.context_value.text() == 'Whole document'
    assert settings.tts_context_length == 160
    slider.setSliderDown(False)
    assert settings.tts_context_length == 0
    widget.close()


@pytest.mark.parametrize('status', ['module_text_to_speech_status_ready', 'module_text_to_speech_status_reading'])
def test_play_icon_follows_selection_and_editor_mode(settings, status):
    from PySide6.QtGui import QColor
    from PySide6.QtWidgets import QPlainTextEdit, QTextBrowser, QWidget, QHBoxLayout
    from notolog.editor_state import EditorState, Mode
    from notolog.helpers.theme_helper import ThemeHelper
    from notolog.notolog_editor import NotologEditor
    from notolog.modules.text_to_speech.playback_bar import PlaybackBar
    host = QMainWindow()
    host.logger = Mock()
    host.estate = EditorState(host)
    host.estate.mode = Mode.EDIT
    edit, view = QPlainTextEdit(host), QTextBrowser(host)
    edit.setPlainText('Selected words')
    view.setPlainText('Rendered words')
    host.get_active_widget = lambda: edit if host.estate.mode == Mode.EDIT else view
    controller = SpeechController(host)
    host.get_speech_controller = lambda: controller
    host.action_read_aloud = host.action_pause_speech = host.action_stop_speech = Mock()
    host.toolbar = QWidget(host)
    bar = PlaybackBar(host, host.toolbar)
    QHBoxLayout(host.toolbar).addWidget(bar)
    for widget in (edit, view):
        widget.selectionChanged.connect(lambda: NotologEditor.on_selection_changed(host))
    controller.status_changed.emit(status)
    theme = ThemeHelper()
    color = QColor(theme.get_color(
        'toolbar_icon_color_tts_play' + ('_act' if status == 'module_text_to_speech_status_reading' else '')))

    def check(icon):
        expected = theme.get_icon(theme_icon=icon, color=color).pixmap(bar.icon_size).toImage()
        assert bar.play.icon().pixmap(bar.icon_size).toImage() == expected

    check('play-fill.svg')
    edit.selectAll()
    check('play.svg')
    host.estate.mode = Mode.VIEW
    check('play-fill.svg')
    view.selectAll()
    check('play.svg')
    cursor = view.textCursor()
    cursor.clearSelection()
    view.setTextCursor(cursor)
    check('play-fill.svg')
    host.close()


def test_main_menu_distinguishes_selection_and_document_icons(settings):
    from notolog.notolog_editor import NotologEditor
    host = SimpleNamespace(speech_enabled=lambda: True, action_read_selection_aloud=Mock(),
                           action_read_aloud=Mock(), action_pause_speech=Mock(), action_stop_speech=Mock())
    items = NotologEditor.speech_menu_actions(host)
    assert items[-1] == {'type': 'delimiter'}
    actions = {action['name']: action for action in items if action['type'] == 'action'}
    assert actions['read_aloud']['theme_icon'] == 'play.svg'
    assert actions['read_document']['theme_icon'] == 'play-fill.svg'


def test_playback_and_processing_indicators_are_independent(settings):
    from notolog.modules.text_to_speech.playback_bar import PlaybackBar
    controller = SpeechController()
    host = SimpleNamespace(get_speech_controller=lambda: controller, action_read_aloud=Mock(),
                           action_pause_speech=Mock(), action_stop_speech=Mock())
    bar = PlaybackBar(host)
    controller.preparing = True
    controller.sink = SimpleNamespace(playing=True)
    bar.update_status('module_text_to_speech_status_preparing')
    assert bar.activity_state == (True, True)
    controller.preparing = False
    bar.update_activity()
    assert bar.activity_state == (True, False)
    assert bar.status.isHidden()
    controller.sink.playing = False
    bar.update_activity()
    assert bar.activity_state == (False, False)
    controller.preparing = True
    bar.update_activity()
    assert bar.activity_state == (False, True)
    controller.paused = True
    bar.update_activity()
    assert bar.activity_state == (False, False)
    bar.close()


def test_status_info_icon_is_filled_while_field_hints_are_outline(settings):
    from PySide6.QtGui import QColor
    from notolog.helpers.theme_helper import ThemeHelper
    from notolog.modules.text_to_speech.settings_widget import SpeechSettingsWidget
    from notolog.ui.label_with_hint import LabelWithHint
    widget = SpeechSettingsWidget()
    widget.report('Checking speech runtime…', 'info')
    theme = ThemeHelper()
    size = widget.fontMetrics().height()
    color = QColor(theme.get_color('settings_dialog_hint_icon_color'))
    expected = theme.get_icon(theme_icon='info-square-fill.svg', color=color).pixmap(size, size)
    assert widget.status_icon.pixmap().toImage() == expected.toImage()
    assert all('-fill.svg' not in hint.theme_icon for hint in widget.findChildren(LabelWithHint))
    widget.close()


@pytest.mark.parametrize('rendered', [False, True])
@pytest.mark.parametrize('source,needle,code', [
    ('😀 Earlier text.\n\nRead from here.\n\nLast paragraph.', 'Read from here.', False),
    ('Earlier `private code` after.\n\nLast paragraph.', 'private', True),
    ('Earlier\n\n```python\nprivate code\n```\n\nLast paragraph.', 'private', True),
])
def test_read_from_cursor_preserves_code_and_visible_selection(settings, rendered, source, needle, code):
    from notolog.highlight.md_highlighter import MdHighlighter
    from notolog.modules.text_to_speech.actions import speech_action_icon
    host = QMainWindow()
    host.speech_enabled = lambda: True
    host.action_read_aloud = Mock()
    widget = ViewWidget(host) if rendered else EditWidget(host)
    host.setCentralWidget(widget)
    highlighter = None
    if rendered:
        widget.setHtml(markdown.markdown(source, extensions=['extra']))
    else:
        widget.setPlainText(source)
        highlighter = MdHighlighter(widget.document())
        highlighter.rehighlight()
    cursor = widget.document().find(needle)
    cursor.setPosition(cursor.selectionStart())
    widget.setTextCursor(cursor)
    original = (cursor.position(), cursor.anchor())
    menu = QMenu()
    append_selection_action(widget, menu, html=rendered)
    action = next(action for action in menu.actions() if action.text() == 'Read from cursor aloud')
    assert action.isEnabled() and action.isIconVisibleInMenu()
    assert action.icon().pixmap(24, 24).toImage() == speech_action_icon(filled=True).pixmap(24, 24).toImage()
    action.trigger()
    speech_source = host.action_read_aloud.call_args.kwargs['source']
    spoken = prepare_text(speech_source)
    assert 'Earlier' not in spoken
    assert 'Last paragraph.' in spoken
    assert ('private' not in spoken) if code else ('Read from here.' in spoken)
    assert needle in prepare_text(speech_source, skip_inline=False, skip_multiline=False)
    assert (widget.textCursor().position(), widget.textCursor().anchor()) == original
    if highlighter:
        highlighter.setDocument(None)
    host.close()


@pytest.mark.parametrize('mode', ['selection', 'reverse-selection', 'cursor'])
@pytest.mark.parametrize('source,multiline', [
    ('Earlier `private code` after.\n\nLast paragraph.', False),
    ('Earlier\n\n```python\nprivate code\n```\n\nLast paragraph.', True),
])
def test_rendered_speech_preserves_code_with_proportional_fallback(settings, mode, source, multiline):
    from PySide6.QtGui import QFontDatabase
    from notolog.modules.text_to_speech.actions import cursor_source, selection_source
    widget = ViewWidget()
    family = QFontDatabase.systemFont(QFontDatabase.SystemFont.GeneralFont).family()
    # Exercise a proportional fallback without depending on the machine's monospace fonts.
    widget.document().setDefaultStyleSheet(f'code {{ font-family: "{family}", monospace; }}')
    widget.setHtml(markdown.markdown(source, extensions=['extra']))
    cursor = widget.document().find('private')
    start, end = cursor.selectionStart(), cursor.selectionEnd()
    if mode == 'reverse-selection':
        cursor.setPosition(end)
        cursor.setPosition(start, QTextCursor.MoveMode.KeepAnchor)
    elif mode == 'cursor':
        cursor.setPosition(start)
    widget.setTextCursor(cursor)
    original = widget.document().toHtml(), cursor.position(), cursor.anchor()
    try:
        speech = (cursor_source(widget, rendered=True) if mode == 'cursor' else
                  selection_source(widget, rendered=True))
        assert 'private' not in prepare_text(speech)
        assert 'private' in prepare_text(speech, skip_inline=False, skip_multiline=False)
        assert ('Multiline code block' in prepare_text(speech)) == multiline
        assert 'private' in prepare_text(speech, skip_inline=multiline, skip_multiline=not multiline)
        if mode == 'cursor':
            assert 'Last paragraph.' in prepare_text(speech)
        assert (widget.document().toHtml(), widget.textCursor().position(), widget.textCursor().anchor()) == original
    finally:
        widget.close()


@pytest.mark.parametrize('mode', ['selection', 'cursor'])
def test_rendered_speech_keeps_prose_with_monospace_default(settings, mode):
    from PySide6.QtGui import QFontDatabase
    from notolog.modules.text_to_speech.actions import cursor_source, selection_source
    widget = ViewWidget()
    widget.setFont(QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont))
    widget.setHtml('<p>Earlier.</p><p>Read `literal` &lt;code&gt; &amp; 😀 and <code>private</code>.</p>'
                   '<p>Last paragraph.</p>')
    cursor = widget.document().find('Read')
    cursor.setPosition(cursor.selectionStart())
    if mode == 'selection':
        cursor.movePosition(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.KeepAnchor)
    widget.setTextCursor(cursor)
    original = widget.document().toHtml(), cursor.position(), cursor.anchor()
    try:
        source = (cursor_source(widget, rendered=True) if mode == 'cursor' else
                  selection_source(widget, rendered=True))
        spoken = prepare_text(source)
        assert 'Read `literal` <code> & 😀' in spoken
        assert 'Last paragraph.' in spoken and 'Earlier' not in spoken
        assert 'private' not in spoken
        assert 'private' in prepare_text(source, skip_inline=False)
        assert (widget.document().toHtml(), widget.textCursor().position(), widget.textCursor().anchor()) == original
    finally:
        widget.close()


def test_rendered_speech_groups_code_fragments_and_preserves_headings_and_alt_text(settings):
    from notolog.modules.text_to_speech.actions import selection_source
    from notolog.modules.text_to_speech.text import prepare_sections
    widget = ViewWidget()
    widget.setHtml('<h2>Topic</h2><p>Text <code>inline <b>private</b> code</code>.</p>'
                   '<pre><code>first\n<b>second</b>\nthird</code></pre>'
                   '<p><img src="missing.png" alt="Diagram"> Last paragraph.</p>')
    cursor = widget.textCursor()
    cursor.select(QTextCursor.SelectionType.Document)
    widget.setTextCursor(cursor)
    try:
        source = selection_source(widget, rendered=True)
        spoken = prepare_text(source)
        assert spoken.count('Inline code block') == 1
        assert spoken.count('Multiline code block') == 1
        assert 'private' not in spoken and 'second' not in spoken
        included = prepare_text(source, skip_inline=False, skip_multiline=False)
        assert 'inline private code' in included and 'first\nsecond\nthird' in included
        assert 'Diagram' in spoken and 'Last paragraph.' in spoken
        sections = prepare_sections(source)
        assert sections[0].heading and sections[0].text == 'Topic'
    finally:
        widget.close()


def test_rendered_speech_is_empty_at_end_of_code_block(settings):
    from notolog.modules.text_to_speech.actions import cursor_source, selection_source
    widget = ViewWidget()
    widget.setHtml('<pre><code>private code</code></pre>')
    cursor = widget.textCursor()
    cursor.movePosition(QTextCursor.MoveOperation.End)
    widget.setTextCursor(cursor)
    try:
        assert selection_source(widget, rendered=True) == ''
        assert cursor_source(widget, rendered=True) == ''
    finally:
        widget.close()


@pytest.mark.parametrize('rendered', [False, True])
def test_read_from_cursor_uses_mouse_position_and_disables_at_end(settings, rendered, qapp):
    from notolog.modules.text_to_speech.actions import cursor_source
    widget = ViewWidget() if rendered else EditWidget()
    widget.setPlainText('Earlier text.\nRead here.')
    widget.resize(500, 200)
    widget.show()
    qapp.processEvents()
    target = widget.document().find('Read here.')
    target.setPosition(target.selectionStart())
    point = widget.cursorRect(target).center()
    original = widget.textCursor().position()
    text = cursor_source(widget, rendered=rendered, position=point)
    assert prepare_text(text) == 'Read here.'
    assert widget.textCursor().position() == original
    target.movePosition(QTextCursor.MoveOperation.End)
    widget.setTextCursor(target)
    assert not cursor_source(widget, rendered=rendered).strip()
    widget.close()


def test_speech_defaults_and_existing_preferences(settings):
    settings.settings.remove('tts_enabled')
    assert settings.tts_enabled == config.audio_available()
    assert settings.tts_voice == 'Aria'
    assert settings.tts_context_length == 160
    assert config.CONTEXT_LENGTHS[0] == 10
    settings.tts_enabled = False
    settings.tts_context_length = 10
    config.speech_settings()
    assert not settings.tts_enabled
    assert settings.tts_context_length == 10


def test_model_folder_placeholder_uses_default_after_clearing_custom_path(settings, tmp_path):
    from notolog.modules.text_to_speech.settings_widget import SpeechSettingsWidget
    custom = str(tmp_path / 'custom-models')
    settings.tts_model_directory = custom
    widget = SpeechSettingsWidget()
    field = widget.findChild(QLineEdit, 'tts_model_directory')
    default = str(config.default_model_directory())
    assert field.text() == custom
    assert field.placeholderText() == default
    field.clear()
    assert settings.tts_model_directory == ''
    assert str(config.model_directory(settings)) == field.placeholderText() == default
    widget.close()
    reopened = SpeechSettingsWidget()
    field = reopened.findChild(QLineEdit, 'tts_model_directory')
    assert field.text() == ''
    assert field.placeholderText() == default
    reopened.close()


def test_model_folder_change_discards_old_download_overrides(settings, tmp_path):
    from notolog.modules.text_to_speech.settings_widget import SpeechSettingsWidget
    root = tmp_path / 'old'
    root.mkdir()
    (root / 'magpie.gguf').touch()
    (root / 'codec.gguf').touch()
    (root / 'tokenizers').mkdir()
    (root / 'tokenizers/model_config.yaml').touch()
    settings.tts_model_directory = str(root)
    settings.tts_magpie_path = str(root / 'magpie.gguf')
    settings.tts_codec_path = str(root / 'codec.gguf')
    settings.tts_tokenizer_directory = str(root / 'tokenizers')
    widget = SpeechSettingsWidget()
    assert widget.download.text() == 'Verify models'
    widget.findChild(QLineEdit, 'tts_model_directory').setText(str(tmp_path / 'empty'))
    widget.refresh_setup()
    assert not settings.tts_magpie_path
    assert widget.download.text() == 'Download models'
    assert not widget.test.isEnabled()
    widget.close()


def test_custom_models_do_not_claim_download_folder_is_complete(settings, tmp_path, monkeypatch):
    from notolog.modules.text_to_speech import settings_widget
    monkeypatch.setattr(settings_widget, 'runtime_path', lambda _: '/runtime')
    for name in ('magpie.gguf', 'codec.gguf'):
        (tmp_path / name).touch()
    tokenizers = tmp_path / 'tokenizers'
    tokenizers.mkdir()
    settings.tts_magpie_path = str(tmp_path / 'magpie.gguf')
    settings.tts_codec_path = str(tmp_path / 'codec.gguf')
    settings.tts_tokenizer_directory = str(tokenizers)
    settings.tts_enabled = True
    widget = settings_widget.SpeechSettingsWidget()
    assert widget.download.text() == 'Download models'
    assert widget.test.isEnabled()
    assert 'Custom model files' in widget.status.text()
    widget.findChild(QLineEdit, 'tts_model_directory').setText(str(tmp_path / 'new'))
    assert settings.tts_magpie_path == str(tmp_path / 'magpie.gguf')
    widget.close()


def test_enabling_speech_does_not_rescan_models(settings, monkeypatch):
    from notolog.modules.text_to_speech.settings_widget import SpeechSettingsWidget
    widget = SpeechSettingsWidget()
    scan = Mock(side_effect=AssertionError('Enabling must not scan models'))
    monkeypatch.setattr(widget, 'have_models', scan)
    settings.tts_enabled = True
    scan.assert_not_called()
    widget.close()


def test_without_audio_dependency_keeps_setup_but_disables_playback(settings, monkeypatch):
    from notolog.modules.text_to_speech.settings_widget import SpeechSettingsWidget
    settings.settings.remove('tts_enabled')
    monkeypatch.delattr(type(settings), 'tts_enabled')
    monkeypatch.setattr(config, 'find_spec', lambda _: None)
    config.speech_settings()
    assert not settings.tts_enabled
    widget = SpeechSettingsWidget()
    enabled = widget.findChild(QCheckBox, 'tts_enabled')
    assert not enabled.isEnabled()
    assert 'notolog[tts]' in enabled.toolTip()
    assert not widget.test.isEnabled()
    widget.close()


def test_missing_linux_portaudio_explains_installation_in_settings(settings, monkeypatch):
    from notolog.modules.text_to_speech.settings_widget import SpeechSettingsWidget
    monkeypatch.setattr(config.sys, 'platform', 'linux')
    monkeypatch.setattr(config, 'portaudio_library', lambda: None)
    assert not config.audio_available()
    widget = SpeechSettingsWidget()
    enabled = widget.findChild(QCheckBox, 'tts_enabled')
    assert not enabled.isEnabled()
    assert 'sudo apt install libportaudio2' in enabled.toolTip()
    assert 'sudo apt install libportaudio2' in widget.test_hint.text()
    assert not widget.test_hint.isHidden()
    assert not widget.test.isEnabled()
    widget.close()


@pytest.mark.parametrize('platform', ['win32', 'darwin'])
def test_audio_wheels_do_not_require_linux_system_library(settings, monkeypatch, platform):
    monkeypatch.setattr(config.sys, 'platform', platform)
    monkeypatch.setattr(config, 'portaudio_library', Mock(side_effect=AssertionError('Linux-only lookup')))
    assert config.audio_available()


@pytest.mark.asyncio
@pytest.mark.parametrize('method', ['close', 'reject', 'escape'])
async def test_settings_dialog_confirms_download_cancellation(settings, monkeypatch, method):
    from PySide6.QtCore import Qt
    from PySide6.QtTest import QTest
    from PySide6.QtWidgets import QMessageBox
    from notolog.ui.settings_dialog import SettingsDialog
    from notolog.modules.modules import Modules
    from notolog.modules import text_to_speech
    from notolog.modules.text_to_speech.settings_widget import SpeechSettingsWidget
    monkeypatch.setattr(Modules, 'get_by_extension', lambda *_: [text_to_speech])
    host = QMainWindow()
    host.settings = settings
    dialog = SettingsDialog(host)
    dialog.show()
    widget = dialog.findChild(SpeechSettingsWidget)
    widget.operation = 'download'
    widget.task = asyncio.create_task(asyncio.sleep(60))
    question = Mock(return_value=QMessageBox.StandardButton.No)
    monkeypatch.setattr(QMessageBox, 'question', question)

    def close():
        if method == 'escape':
            QTest.keyClick(dialog, Qt.Key.Key_Escape)
        else:
            getattr(dialog, method)()

    close()
    assert dialog.isVisible()
    await asyncio.sleep(0)
    assert not widget.task.done()
    question.return_value = QMessageBox.StandardButton.Yes
    close()
    assert not dialog.isVisible()
    with pytest.raises(asyncio.CancelledError):
        await widget.task
    assert question.call_count == 2
    host.close()


def test_toggle_speech_preserves_toolbar_and_search(settings):
    from notolog.ui.toolbar import ToolBar
    host = QMainWindow()
    host.speech_enabled = lambda: settings.tts_enabled
    controller = SpeechController(host)
    host.get_speech_controller = lambda: controller
    host.action_read_aloud = host.action_pause_speech = host.action_stop_speech = Mock()
    toolbar = ToolBar(host)
    search = toolbar.search_form
    field = search.findChild(QLineEdit, 'search_input')
    field.setText('keep this search')
    settings.tts_enabled = True
    toolbar.sync_speech_controls()
    action = toolbar.speech_action
    settings.tts_enabled = False
    toolbar.sync_speech_controls()
    assert not action.isVisible()
    settings.tts_enabled = True
    toolbar.sync_speech_controls()
    assert toolbar.speech_action is action
    assert toolbar.search_form is search
    assert field.text() == 'keep this search'
    host.close()
