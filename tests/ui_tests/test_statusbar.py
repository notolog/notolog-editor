"""Tests for the application status bar."""

from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor
import pytest

from notolog.settings import Settings
from notolog.ui.file_system_model import get_file_type_icon
from notolog.ui.statusbar import StatusBar

from . import test_app  # noqa: F401


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
