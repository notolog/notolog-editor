"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Tests for the application status bar.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QImage
from types import SimpleNamespace
import pytest

from notolog.settings import Settings
from notolog.ui.file_system_model import get_file_type_icon
from notolog.ui.statusbar import StatusBar

from . import test_app  # noqa: F401


@pytest.mark.parametrize('language', ['en', 'de'])
def test_failed_save_warning_explains_error_on_hover_and_click(test_app, mocker, language):  # noqa: F811
    from notolog.notolog_editor import NotologEditor
    from notolog.lexemes.lexemes import Lexemes
    from notolog.helpers.tooltip_helper import TooltipHelper
    settings = Settings()
    settings.clear()
    settings.app_language = language
    window = QMainWindow()
    statusbar = StatusBar(window)
    lexemes = Lexemes(language)
    host = SimpleNamespace(statusbar=statusbar, lexemes=lexemes, logger=mocker.Mock())
    mocker.patch('notolog.notolog_editor.file_helper.save_file', return_value=False)
    show_tooltip = mocker.patch.object(TooltipHelper, 'show_tooltip')
    statusbar.show_warning(visible=True, tooltip='Previous warning')

    assert NotologEditor.save_file_content(host, 'note.md', 'Unsaved content') is False
    expected = lexemes.get('save_active_file_error_occurred')
    assert expected and statusbar.warning_label.toolTip() == expected
    assert not statusbar.warning_label.isHidden()
    statusbar.warning_label.click()
    show_tooltip.assert_called_once_with(widget=statusbar.warning_label, text=expected)
    statusbar.show_warning(visible=False)
    assert statusbar.warning_label.toolTip() == ''
    window.close()


def test_current_file_indicator_elides_and_copies_path(test_app, tmp_path):  # noqa: F811
    settings = Settings()
    settings.clear()
    settings.app_language = 'en'
    file_path = tmp_path / ('a-very-long-file-name-' * 20 + '.md')

    window = QMainWindow()
    statusbar = StatusBar(window)
    settings.file_path = str(file_path)

    assert statusbar.file_label.isHidden() is False
    assert statusbar.file_icon_label.toolTip() == f'Click to copy: {file_path}'
    assert statusbar.file_icon_label.focusPolicy() == Qt.FocusPolicy.TabFocus
    assert statusbar.file_icon_label.testAttribute(
        Qt.WidgetAttribute.WA_AlwaysShowToolTips)
    assert statusbar.file_icon_label.hasMouseTracking()
    assert '…' in statusbar.file_label.text()
    assert (statusbar.file_label.palette().color(statusbar.file_label.foregroundRole())
            == statusbar.data_size_label.palette().color(statusbar.data_size_label.foregroundRole()))

    statusbar.file_icon_label.click()
    assert test_app.clipboard().text() == str(file_path)


@pytest.mark.parametrize('filename', [
    'note.md', 'note.txt', 'note.html', 'note.enc', 'note.md.del', 'note.bin',
])
def test_current_file_and_state_icons_are_compact(test_app, tmp_path, filename):  # noqa: F811
    settings = Settings()
    settings.clear()
    file_path = tmp_path / filename
    file_path.touch()

    statusbar = StatusBar(QMainWindow())
    statusbar.set_file_path(str(file_path))
    statusbar.set_encryption_icon(encrypted=True)

    assert statusbar.labels_layout.indexOf(statusbar.file_label) < statusbar.labels_layout.indexOf(
        statusbar.file_icon_container)
    for container in (
            statusbar.file_icon_container,
            statusbar.save_progress_container,
            statusbar.encryption_icon_container,
            statusbar.warning_container):
        assert container.layout().contentsMargins().top() == 1

    compact_size = statusbar._compact_icon_size()
    assert statusbar.file_icon_label.iconSize() == QSize(compact_size, compact_size)
    assert statusbar.save_progress_label.pixmap().width() == compact_size
    assert statusbar.encryption_icon_label.pixmap().width() == compact_size
    assert statusbar.warning_label.iconSize().width() == compact_size
    assert statusbar.path_home_label.iconSize().width() > compact_size
    status_color = QColor(statusbar.theme_helper.get_color('statusbar_icon_color_default'))
    expected_icon = get_file_type_icon(str(file_path), statusbar.theme_helper, color=status_color)
    icon_canvas = statusbar.file_icon_label.iconSize()
    assert (statusbar.file_icon_label.icon().pixmap(icon_canvas).toImage()
            == expected_icon.pixmap(icon_canvas).toImage())


def test_font_size_change_resizes_compact_icons(test_app, tmp_path):  # noqa: F811
    settings = Settings()
    settings.clear()
    file_path = tmp_path / 'note.md'
    file_path.touch()

    window = QMainWindow()
    statusbar = StatusBar(window)
    statusbar.set_file_path(str(file_path))
    statusbar.set_encryption_icon(encrypted=True)
    previous_size = statusbar._compact_icon_size()
    previous_graph_size = statusbar.cpu_load_graph.size()

    font = window.font()
    font.setPointSize(font.pointSize() + 12)
    window.setFont(font)
    statusbar.settings_update_handler({'app_font_size': font.pointSize()})

    compact_size = statusbar._compact_icon_size()
    assert compact_size > previous_size
    assert statusbar.file_icon_label.iconSize() == QSize(compact_size, compact_size)
    assert statusbar.save_progress_label.pixmap().size() == QSize(compact_size, compact_size)
    assert statusbar.encryption_icon_label.pixmap().size() == QSize(compact_size, compact_size)
    assert statusbar.warning_label.iconSize() == QSize(compact_size, compact_size)
    assert statusbar.cpu_load_graph.width() == previous_graph_size.width()
    assert statusbar.cpu_load_graph.height() > previous_graph_size.height()
    expected_encryption_icon = statusbar.theme_helper.get_icon(
        theme_icon='shield-lock-fill.svg',
        color=QColor(statusbar.theme_helper.get_color('statusbar_icon_color_default')),
    )
    assert (statusbar.encryption_icon_label.pixmap().toImage()
            == expected_encryption_icon.pixmap(QSize(compact_size, compact_size)).toImage())


def test_save_progress_container_does_not_reserve_hidden_spacing(test_app):  # noqa: F811
    statusbar = StatusBar(QMainWindow())

    assert statusbar.save_progress_label.isHidden()
    assert statusbar.save_progress_container.isHidden()

    statusbar.show_save_progress(True)
    assert not statusbar.save_progress_label.isHidden()
    assert not statusbar.save_progress_container.isHidden()

    statusbar.show_save_progress(False)
    assert statusbar.save_progress_label.isHidden()
    assert statusbar.save_progress_container.isHidden()


def test_system_load_indicators_update_without_blocking(test_app, mocker):  # noqa: F811
    settings = Settings()
    settings.clear()
    settings.app_language = 'en'
    cpu_percent = mocker.patch('notolog.ui.statusbar.psutil.cpu_percent', return_value=12.6)
    virtual_memory = mocker.patch(
        'notolog.ui.statusbar.psutil.virtual_memory',
        return_value=SimpleNamespace(percent=54.4),
    )

    statusbar = StatusBar(QMainWindow())

    assert statusbar.cpu_load_graph.current_value is None
    assert statusbar.memory_load_graph.current_value is None
    assert statusbar.cpu_load_graph.toolTip() == 'System CPU usage unavailable'
    assert statusbar.memory_load_graph.toolTip() == 'System memory usage unavailable'
    cpu_percent.assert_called_once_with(interval=None)
    virtual_memory.assert_not_called()

    statusbar.update_system_load()

    assert statusbar.cpu_load_graph.values[-1] == 13
    assert statusbar.memory_load_graph.values[-1] == 54
    assert statusbar.cpu_load_graph.toolTip() == 'System CPU usage: 13%'
    assert statusbar.memory_load_graph.toolTip() == 'System memory usage: 54%'
    assert statusbar.cpu_load_graph.testAttribute(
        Qt.WidgetAttribute.WA_AlwaysShowToolTips)
    assert statusbar.cpu_load_graph.focusPolicy() == Qt.FocusPolicy.NoFocus
    assert statusbar.cpu_load_graph.hasMouseTracking()
    assert statusbar.system_load_timer.isActive()
    assert statusbar.system_load_timer.interval() == statusbar.DEFAULT_SYSTEM_LOAD_INTERVAL_MS
    assert statusbar.DEFAULT_SYSTEM_LOAD_INTERVAL_MS == 1000
    assert (statusbar.labels_layout.indexOf(statusbar.cursor_label)
            < statusbar.labels_layout.indexOf(statusbar.system_load_separator)
            < statusbar.labels_layout.indexOf(statusbar.cpu_load_graph))
    assert statusbar.cpu_load_graph.COLUMN_WIDTH == 1
    assert statusbar.cpu_load_graph.COLUMN_GAP == 0
    assert statusbar.cpu_load_graph.INNER_PADDING == 1
    assert statusbar.cpu_load_graph.HISTORY_SIZE == 30
    assert statusbar.cpu_load_graph.width() == 34
    assert statusbar.cpu_load_graph.border_color == QColor(
        statusbar.theme_helper.get_color('statusbar_cpu_graph_border_color'))
    assert statusbar.cpu_load_graph.column_color == QColor(
        statusbar.theme_helper.get_color('statusbar_cpu_graph_column_color'))
    assert statusbar.memory_load_graph.border_color == QColor(
        statusbar.theme_helper.get_color('statusbar_memory_graph_border_color'))
    assert statusbar.memory_load_graph.column_color == QColor(
        statusbar.theme_helper.get_color('statusbar_memory_graph_column_color'))
    assert cpu_percent.call_count == 2
    virtual_memory.assert_called_once_with()


def test_system_load_graph_has_exact_border_and_inner_padding(test_app):  # noqa: F811
    statusbar = StatusBar(QMainWindow())
    graph = statusbar.cpu_load_graph
    border_color = QColor('#123456')
    column_color = QColor('#abcdef')
    graph.set_colors(border_color, column_color)
    for _ in range(graph.HISTORY_SIZE):
        graph.set_value(100)

    image = QImage(graph.size(), QImage.Format.Format_ARGB32)
    image.fill(Qt.GlobalColor.transparent)
    graph.render(image)

    assert image.pixelColor(0, 0) == border_color
    assert image.pixelColor(graph.width() - 1, graph.height() - 1) == border_color
    assert image.pixelColor(1, 2) != column_color
    assert image.pixelColor(2, 2) == column_color
    assert image.pixelColor(graph.width() - 3, 2) == column_color
    assert image.pixelColor(graph.width() - 2, 2) != column_color
    assert image.pixelColor(2, graph.height() - 3) == column_color
    assert image.pixelColor(2, graph.height() - 2) != column_color


def test_system_load_indicators_handle_monitoring_failure(test_app, mocker):  # noqa: F811
    settings = Settings()
    settings.clear()
    settings.app_language = 'en'
    mocker.patch('notolog.ui.statusbar.psutil.cpu_percent', side_effect=OSError)

    statusbar = StatusBar(QMainWindow())

    assert statusbar.cpu_load_graph.toolTip() == 'System CPU usage unavailable'
    assert statusbar.memory_load_graph.toolTip() == 'System memory usage unavailable'


def test_system_load_tooltips_follow_language_changes(test_app, mocker):  # noqa: F811
    mocker.patch('notolog.ui.statusbar.psutil.cpu_percent', return_value=12.6)
    mocker.patch(
        'notolog.ui.statusbar.psutil.virtual_memory',
        return_value=SimpleNamespace(percent=54.4),
    )
    settings = Settings()
    settings.clear()
    settings.app_language = 'en'
    statusbar = StatusBar(QMainWindow())

    statusbar.update_system_load()

    settings.app_language = 'de'

    assert statusbar.cpu_load_graph.toolTip() == 'System-CPU-Auslastung: 13 %'
    assert statusbar.memory_load_graph.toolTip() == 'Systemspeicherauslastung: 54 %'
    assert statusbar.cpu_load_graph.accessibleName() == statusbar.cpu_load_graph.toolTip()


def test_system_load_visibility_stops_sampling_and_hides_separator(test_app, mocker):  # noqa: F811
    settings = Settings()
    settings.clear()
    statusbar = StatusBar(QMainWindow())
    update_system_load = mocker.patch.object(statusbar, 'update_system_load')
    cpu_percent = mocker.patch('notolog.ui.statusbar.psutil.cpu_percent')

    settings.show_system_load_graphs = False

    assert statusbar.system_load_separator.isHidden()
    assert statusbar.cpu_load_graph.isHidden()
    assert statusbar.memory_load_graph.isHidden()
    assert not statusbar.system_load_timer.isActive()

    settings.show_system_load_graphs = True

    assert not statusbar.system_load_separator.isHidden()
    assert not statusbar.cpu_load_graph.isHidden()
    assert not statusbar.memory_load_graph.isHidden()
    assert statusbar.system_load_timer.isActive()
    update_system_load.assert_not_called()
    assert cpu_percent.call_args_list[-1].kwargs == {'interval': None}


def test_system_load_interval_setting_is_applied_and_bounded(test_app):  # noqa: F811
    settings = Settings()
    settings.clear()
    statusbar = StatusBar(QMainWindow())

    settings.system_load_interval_ms = 2500
    assert statusbar.system_load_timer.interval() == 2500

    settings.system_load_interval_ms = 1
    assert statusbar.system_load_timer.interval() == statusbar.MIN_SYSTEM_LOAD_INTERVAL_MS

    settings.system_load_interval_ms = 100000
    assert statusbar.system_load_timer.interval() == statusbar.MAX_SYSTEM_LOAD_INTERVAL_MS
