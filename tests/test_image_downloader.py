"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Contains unit and integration tests for the related functionality.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import (
    QObject, Signal, QUrl, QIODevice, QCoreApplication, QEvent, QBuffer, QByteArray, QDir, QElapsedTimer,
)
from PySide6.QtGui import QImage, QPixmap, QPixmapCache, QImageReader, QTextDocument
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PySide6.QtTest import QSignalSpy, QTest

from notolog.image_downloader import ImageDownloader
from notolog.settings import Settings
from notolog.app_config import AppConfig

from . import test_core_app  # noqa: F401

from unittest.mock import MagicMock, Mock, call, patch
from pytest_mock import MockerFixture
from types import SimpleNamespace
from pathlib import Path

import pytest
import asyncio
import logging
import struct


class ReplySignals(QObject):
    finished = Signal()
    errorOccurred = Signal(object)
    readyRead = Signal()
    metaDataChanged = Signal()


class BufferedReply(QNetworkReply):
    """An in-memory Qt reply with no socket or external requests."""

    def __init__(self, parent):
        super().__init__(parent)
        self.body = bytearray()
        self.abort_count = 0
        self.setUrl(QUrl('https://images.invalid/picture.png'))
        self.setHeader(QNetworkRequest.KnownHeaders.ContentTypeHeader, 'image/png')
        self.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Unbuffered)

    def readData(self, size):
        chunk = bytes(self.body[:size])
        del self.body[:size]
        return chunk

    def bytesAvailable(self):
        return len(self.body) + super().bytesAvailable()

    def abort(self):
        self.abort_count += 1
        self.setError(QNetworkReply.NetworkError.OperationCanceledError, 'Cancelled')
        self.errorOccurred.emit(self.error())
        self.setFinished(True)
        self.finished.emit()


class TestImageDownloader:

    def test_resource_urls_and_network_details_are_not_logged(self, mocker, tmp_path, caplog):
        downloader = ImageDownloader(str(tmp_path))
        reply = BufferedReply(downloader)
        secret = 'SYNTHETIC_PRIVATE_RESOURCE'
        url = f'https://images.invalid/{secret}.png?token={secret}'
        reply.setUrl(QUrl(url))
        mocker.patch.object(downloader.network_manager, 'get', return_value=reply)

        with caplog.at_level(logging.DEBUG):
            downloader.download_image(url)
            reply.setError(QNetworkReply.NetworkError.HostNotFoundError, f'Cannot resolve {url}')
            downloader.handle_network_reply_error(reply, reply.error())

        assert caplog.records
        assert secret not in caplog.text
        assert not downloader._downloads

    @pytest.fixture(autouse=True)
    def settings_owner(self, qapp):
        # Temporary downloaders must not own the shared settings singleton.
        settings = Settings(parent=qapp)
        settings.setParent(qapp)
        yield settings

    @pytest.fixture()
    def test_settings_fixture(self, monkeypatch, request, test_core_app):  # noqa: F811 redefinition of unused 'test_app'
        # Retrieve parameter values from the test request.
        # The only 'viewer_save_resources' is in use at the moment
        monkeypatch.setattr(Settings, 'viewer_save_resources', request.param)

        # The test_core_app fixture sets up the app environment explicitly.
        yield Settings()

    def test_initialize_called(self):
        with patch.object(ImageDownloader, 'initialize', MagicMock(name='initialize')) as mock_initialize:
            ImageDownloader()
            # Ensure initialize was called once in the constructor
            mock_initialize.assert_called_once()

        with (patch.object(ImageDownloader, 'update_resource_folder', MagicMock(name='update_resource_folder'))
              as mock_update_resource_folder):
            ImageDownloader()
            # Ensure initialize was called once in the constructor
            mock_update_resource_folder.assert_called_once()

        with (patch.object(ImageDownloader, 'get_resource_folder', MagicMock(name='get_resource_folder'))
              as mock_get_resource_folder):
            ImageDownloader()
            # Ensure initialize was called once in the constructor
            mock_get_resource_folder.assert_called_once()

    @pytest.fixture
    def test_downloader_obj(self, mocker: MockerFixture, qapp):
        """
        Testing object fixture.
        May contain minimal logic for testing purposes.
        """

        # Mock AppConfig's get_logger_level method to suppress logging during tests.
        mocker.patch.object(AppConfig, 'get_logger_level', return_value=logging.NOTSET)

        yield ImageDownloader()

    @pytest.fixture(scope="function")
    def test_exp_params_fixture(self, request):
        # Retrieve parameter values from the test request.
        param_values = request.param

        yield param_values

    @pytest.mark.asyncio
    @pytest.mark.parametrize('defer_download', [False, True])
    @pytest.mark.parametrize(
        "test_settings_fixture, test_exp_params_fixture, test_downloader_obj",
        [
            (False, (QNetworkReply.NetworkError.NoError, None, 'some_url1',
                     {QNetworkRequest.KnownHeaders.ContentTypeHeader: 'image/png'}, b'image_byte_array_data'), None),
            (True, (QNetworkReply.NetworkError.NoError, None, 'some_url1',
                    {QNetworkRequest.KnownHeaders.ContentTypeHeader: 'image/png'}, b'image_byte_array_data'), None),
            (False, (QNetworkReply.NetworkError.HostNotFoundError, 404, 'some_url123',
                     {QNetworkRequest.KnownHeaders.ContentTypeHeader: 'anything'}, b'image_byte_array_data'), None),
        ],
        # This tells pytest that the parameter in a "..." should not be passed directly to the test function.
        # indirect=["test_downloader_obj"]
        indirect=True  # all
    )
    async def test_async_queue(self, mocker: MockerFixture, monkeypatch,
                               test_settings_fixture: Settings,
                               test_exp_params_fixture: dict,
                               test_downloader_obj: ImageDownloader, defer_download):
        # Test params
        reply_error, error_code, resource_url, header_params, resource_data = test_exp_params_fixture

        # Get callback method to check
        mock_handle_network_reply = mocker.patch.object(
            test_downloader_obj, 'handle_network_reply', wraps=test_downloader_obj.handle_network_reply)
        mock_handle_network_reply_error = mocker.patch.object(
            test_downloader_obj, 'handle_network_reply_error',
            wraps=test_downloader_obj.handle_network_reply_error)
        download_started = asyncio.Event()
        allow_download = asyncio.Event()
        resource_download_async = test_downloader_obj.resource_download_async

        async def gated_download(url):
            download_started.set()
            await allow_download.wait()
            await resource_download_async(url)

        mock_resource_download_async = mocker.patch.object(
            test_downloader_obj, 'resource_download_async',
            wraps=gated_download if defer_download else resource_download_async)
        # Get download callback method to check
        mock_callback = mocker.patch.object(
            test_downloader_obj, 'resource_task_callback', wraps=test_downloader_obj.resource_task_callback)
        # Downloading resource
        mock_download_image = mocker.patch.object(
            test_downloader_obj, 'download_image', wraps=test_downloader_obj.download_image)
        # Cache and save downloaded resource
        mock_save_image = mocker.patch.object(test_downloader_obj, 'save_image', return_value=None)
        decoded_pixmap = QPixmap(1, 1)
        decoded_pixmap.fill()
        mock_cache_pixmap = mocker.patch.object(test_downloader_obj, 'cache_pixmap', return_value=('png', decoded_pixmap))

        # Check that the local task pool is empty.
        # An error here indicates that the queue was used in previous tests.
        assert len(test_downloader_obj.resource_tasks) == 0
        # Check default resource folder
        assert test_downloader_obj.folder.path().endswith(ImageDownloader.RESOURCE_DIR)

        # Mock QNetworkReply using create_autospec
        # mock_reply = create_autospec(QNetworkReply, instance=True)
        mock_reply = MagicMock(spec=QNetworkReply)
        mock_reply.error.return_value = reply_error
        mock_reply.url.return_value = QUrl(resource_url)
        assert mock_reply.url().toString() == resource_url

        # with patch('PySide6.QtGui.QPixmap') as MockPixmap:
        #    mock_pixmap_instance = MockPixmap.return_value
        #    mock_pixmap_instance.loadFromData = MagicMock()  # MagicMock(spec=QPixmap)

        mocker.patch.object(mock_reply, 'header', side_effect=lambda k: header_params.get(k, None))

        signals = ReplySignals()
        mock_reply.finished = signals.finished
        mock_reply.errorOccurred = signals.errorOccurred
        mock_reply.readyRead = signals.readyRead
        mock_reply.metaDataChanged = signals.metaDataChanged

        def deliver_reply():
            if reply_error != QNetworkReply.NetworkError.NoError:
                signals.errorOccurred.emit(error_code)
            signals.finished.emit()

        def get_reply(request):
            unread = bytearray(resource_data)

            def read(size):
                chunk = bytes(unread[:size])
                del unread[:size]
                return chunk

            mock_reply.read.side_effect = read
            asyncio.get_running_loop().call_soon(deliver_reply)
            return mock_reply

        # Mock QNetworkAccessManager and its get method
        mock_manager = MagicMock(QNetworkAccessManager)
        mock_manager.get.side_effect = get_reply

        # Monkeypatch the network manager in the application
        monkeypatch.setattr(test_downloader_obj, 'network_manager', mock_manager)
        # monkeypatch.setattr("PySide6.QtNetwork.QNetworkAccessManager", lambda: mock_manager)

        mocker.patch.object(test_downloader_obj, 'is_external_url', return_value=True)

        downloaded = Mock()
        finished = Mock()
        test_downloader_obj.downloaded.connect(downloaded)
        test_downloader_obj.finished.connect(finished)
        queue_tasks = []
        try:
            for attempt in range(1, 3):
                download_started.clear()
                allow_download.clear()
                task = test_downloader_obj.download_resource_in_queue(resource_url)
                queue_tasks.append(task)
                if defer_download:
                    await asyncio.wait_for(download_started.wait(), timeout=5)
                    assert mock_callback.call_count == attempt - 1
                    allow_download.set()
                await asyncio.wait_for(task, timeout=5)
                assert mock_callback.call_count == attempt
                assert test_downloader_obj.resource_tasks == []
                assert test_downloader_obj.downloaded_cnt == 0
        finally:
            owned_tasks = set(queue_tasks) | set(test_downloader_obj.resource_tasks)
            for task in owned_tasks:
                if not task.done():
                    task.cancel()
            await asyncio.gather(*owned_tasks, return_exceptions=True)

        if error_code is None:
            assert downloaded.call_count == 2
            for event in downloaded.call_args_list:
                assert event.args[0]['resource_name'] == resource_url
                assert event.args[0]['pixmap'].cacheKey() == decoded_pixmap.cacheKey()
            assert finished.call_args_list == [call(1)] * 2
        else:
            downloaded.assert_not_called()
            finished.assert_not_called()

        # Assert status code was checked
        mock_reply.attribute.assert_called_with(QNetworkRequest.Attribute.HttpStatusCodeAttribute)

        if error_code is None:
            mock_handle_network_reply.assert_called()
            mock_resource_download_async.assert_called_with(resource_url)
            mock_resource_download_async.assert_awaited_with(resource_url)
            mock_download_image.assert_called_with(resource_url)
            mock_cache_pixmap.assert_called_with(resource_url, resource_data)
        else:
            mock_handle_network_reply_error.assert_called()

        assert test_downloader_obj.settings.viewer_save_resources == test_settings_fixture.viewer_save_resources
        if test_downloader_obj.settings.viewer_save_resources:
            mock_save_image.assert_called()

    @pytest.mark.parametrize(
        "test_exp_params_fixture, test_downloader_obj",
        [
            (('some_url1', 'some_exp|ected_hash', 'some_exp_some_url1'), None),
            (('some_url2', 'some_exp|ected_hash', 'some_exp_some_url2'), None),
            (('notolog.app/example.png', 'some_exp|ected_hash', 'some_exp_example.png'), None),
        ],
        indirect=True
    )
    def test_legacy_url_to_filename(self, monkeypatch, test_exp_params_fixture, test_downloader_obj: ImageDownloader):
        # Test params
        resource_url, hash256, expected_filename = test_exp_params_fixture

        # Mocking hashlib.sha256().hexdigest() using patch
        with patch('hashlib.sha256') as mock_sha256:
            # Mocking the return value of hexdigest() method
            mock_sha256.return_value.hexdigest.return_value = hash256

            assert test_downloader_obj._legacy_filename(resource_url) == expected_filename

    @pytest.mark.parametrize(
        "test_exp_params_fixture, test_downloader_obj",
        [
            (('image/jpeg', '.jpg'), None),
            (('image/png', '.png'), None),
            (('image/gif', '.gif'), None),
            (('image/bmp', '.bmp'), None),
            (('image/svg+xml', '.svg'), None),
            (('image/tiff', '.tiff'), None),
            (('image/webp', '.webp'), None),
            (('image/anything-else', '.dat'), None),
        ],
        indirect=True
    )
    def test_mime_to_extension(self, test_exp_params_fixture, test_downloader_obj: ImageDownloader):
        # Test params
        mime_type, file_extension = test_exp_params_fixture

        assert test_downloader_obj.mime_to_extension(mime_type) == file_extension

    @pytest.mark.parametrize(
        "test_exp_params_fixture, test_downloader_obj",
        [
            # Valid http/https URLs should be detected as external
            (('https://example.com/image.png', 'example.com', False), None),
            (('https://notolog.app/image.png', 'example.com', True), None),
            (('http://notolog.app/image.png', 'example.com', True), None),
            # Invalid schemes should return False for security
            (('file:///etc/passwd', 'example.com', False), None),
            (('javascript:alert(1)', 'example.com', False), None),
            (('data:image/png;base64,abc', 'example.com', False), None),
            (('ftp://example.com/file', 'example.com', False), None),
            # Empty or relative URLs
            (('/local/path/image.png', 'example.com', False), None),
            (('relative/path.png', 'example.com', False), None),
        ],
        indirect=True
    )
    def test_is_external_url_scheme_validation(self, test_exp_params_fixture, test_downloader_obj: ImageDownloader):
        """Test that is_external_url only allows http/https schemes for security."""
        url, base_domain, expected_result = test_exp_params_fixture

        result = test_downloader_obj.is_external_url(url, base_domain)
        assert result == expected_result

    @pytest.fixture
    def bounded_download(self, test_downloader_obj, monkeypatch, mocker, request):
        downloader = test_downloader_obj
        monkeypatch.setattr(downloader, 'MAX_IMAGE_BYTES', 8)
        signals = ReplySignals()
        reply = MagicMock(spec=QNetworkReply)
        for name in ('readyRead', 'metaDataChanged', 'finished', 'errorOccurred'):
            setattr(reply, name, getattr(signals, name))
        headers = {QNetworkRequest.KnownHeaders.ContentTypeHeader: 'image/png'}
        reply.header.side_effect = headers.get
        reply.error.return_value = QNetworkReply.NetworkError.NoError
        url = getattr(request, 'param', 'https://images.invalid/picture.png')
        reply.url.return_value = QUrl(url)
        body = bytearray()

        def read(size):
            chunk = bytes(body[:size])
            del body[:size]
            return chunk

        def abort():
            reply.error.return_value = QNetworkReply.NetworkError.OperationCanceledError
            signals.errorOccurred.emit(reply.error())
            signals.finished.emit()

        reply.read.side_effect = read
        reply.abort.side_effect = abort
        manager = MagicMock(spec=QNetworkAccessManager)
        manager.get.return_value = reply
        monkeypatch.setattr(downloader, 'network_manager', manager)
        decoded_pixmap = QPixmap(1, 1)
        decoded_pixmap.fill()
        cache = mocker.patch.object(downloader, 'cache_pixmap', return_value=('png', decoded_pixmap))
        save = mocker.patch.object(downloader, 'save_image')
        downloaded = Mock()
        downloader.downloaded.connect(downloaded)
        downloader.download_image(reply.url().toString())
        deadline = downloader._downloads[reply][1]
        yield SimpleNamespace(downloader=downloader, reply=reply, signals=signals, headers=headers, url=url,
                              body=body, manager=manager, cache=cache, save=save, downloaded=downloaded,
                              deadline=deadline)
        downloader._dispose_reply(reply, abort=True)

    def test_streamed_image_at_size_limit(self, bounded_download, monkeypatch):
        download = bounded_download
        monkeypatch.setattr(Settings, 'viewer_save_resources', True)
        request = download.manager.get.call_args.args[0]
        assert request.transferTimeout() == download.downloader.TRANSFER_TIMEOUT_MS
        download.reply.setReadBufferSize.assert_called_once_with(download.downloader.READ_BUFFER_BYTES)
        assert download.deadline.isActive()
        assert download.deadline.interval() == download.downloader.DOWNLOAD_TIMEOUT_MS
        for chunk in (b'abc', b'defgh'):
            download.body.extend(chunk)
            download.signals.readyRead.emit()
        download.signals.finished.emit()
        download.cache.assert_called_once_with(download.reply.url().toString(), b'abcdefgh')
        download.save.assert_called_once_with(download.reply.url().toString(), b'abcdefgh', 'png')
        download.downloaded.assert_called_once()
        event = download.downloaded.call_args.args[0]
        assert event['resource_name'] == download.reply.url().toString()
        assert event['pixmap'].cacheKey() == download.cache.return_value[1].cacheKey()
        assert download.downloader.downloaded_cnt == 1
        assert not download.downloader._downloads
        assert not download.deadline.isActive()
        download.reply.abort.assert_not_called()
        download.reply.deleteLater.assert_called_once()

    def test_reject_advertised_oversized_image(self, bounded_download):
        download = bounded_download
        download.headers[QNetworkRequest.KnownHeaders.ContentLengthHeader] = 9
        download.signals.metaDataChanged.emit()
        download.signals.finished.emit()
        download.reply.read.assert_not_called()
        self.assert_rejected_download(download)

    @pytest.mark.parametrize('declared_length', [None, -1, 1, 8])
    def test_reject_oversized_stream_with_unreliable_length(self, bounded_download, declared_length):
        download = bounded_download
        download.headers[QNetworkRequest.KnownHeaders.ContentLengthHeader] = declared_length
        download.body.extend(b'abc')
        download.signals.readyRead.emit()
        download.body.extend(b'x' * 100)
        download.signals.readyRead.emit()
        download.signals.finished.emit()
        assert download.reply.read.call_args_list == [call(9), call(6)]
        self.assert_rejected_download(download)

    def test_reject_oversized_final_buffer(self, bounded_download):
        download = bounded_download
        download.body.extend(b'x' * 100)
        download.signals.finished.emit()
        download.reply.read.assert_called_once_with(9)
        self.assert_rejected_download(download)

    @pytest.mark.parametrize('mime_type', [None, '', 'text/html', 'text/plain; image/png'])
    def test_ignore_non_image_reply(self, bounded_download, mime_type):
        download = bounded_download
        download.headers[QNetworkRequest.KnownHeaders.ContentTypeHeader] = mime_type
        download.body.extend(b'content')
        download.signals.finished.emit()
        download.cache.assert_not_called()
        download.save.assert_not_called()
        download.downloaded.assert_not_called()
        assert not download.downloader._downloads
        assert not download.deadline.isActive()
        download.reply.abort.assert_not_called()
        download.reply.deleteLater.assert_called_once()

    def test_deadline_aborts_even_after_receiving_data(self, bounded_download):
        download = bounded_download
        download.body.extend(b'abc')
        download.signals.readyRead.emit()
        download.deadline.timeout.emit()
        download.signals.readyRead.emit()
        download.signals.finished.emit()
        download.downloader.handle_network_reply(download.reply)
        self.assert_rejected_download(download)

    @pytest.mark.parametrize('error', [
        QNetworkReply.NetworkError.TimeoutError,
        QNetworkReply.NetworkError.HostNotFoundError,
    ])
    def test_error_releases_buffer_and_timer_once(self, bounded_download, error):
        download = bounded_download
        download.body.extend(b'abc')
        download.signals.readyRead.emit()
        download.reply.error.return_value = error
        download.signals.errorOccurred.emit(error)
        download.signals.finished.emit()
        download.downloader.handle_network_reply_error(download.reply, error)
        download.cache.assert_not_called()
        download.save.assert_not_called()
        download.downloaded.assert_not_called()
        assert not download.downloader._downloads
        assert not download.deadline.isActive()
        download.reply.deleteLater.assert_called_once()

    @pytest.mark.parametrize('outcome', ['complete', 'oversized', 'deadline'])
    def test_native_reply_lifecycle(self, test_downloader_obj, monkeypatch, mocker, outcome):
        downloader = test_downloader_obj
        monkeypatch.setattr(Settings, 'viewer_save_resources', False)
        monkeypatch.setattr(downloader, 'MAX_IMAGE_BYTES', 8)
        reply = BufferedReply(downloader)
        destroyed = QSignalSpy(reply.destroyed)
        mocker.patch.object(downloader.network_manager, 'get', return_value=reply)
        decoded_pixmap = QPixmap(1, 1)
        decoded_pixmap.fill()
        cache = mocker.patch.object(downloader, 'cache_pixmap', return_value=('png', decoded_pixmap))
        downloaded = QSignalSpy(downloader.downloaded)
        downloader.download_image(reply.url().toString())
        deadline = downloader._downloads[reply][1]
        timer_destroyed = QSignalSpy(deadline.destroyed)
        reply.body.extend(b'abc')
        reply.readyRead.emit()
        if outcome == 'deadline':
            expired = QSignalSpy(deadline.timeout)
            # Exercise native timeout delivery on the next event turn.
            deadline.start(0)
            wait = QElapsedTimer()
            wait.start()
            while expired.count() == 0 and not wait.hasExpired(5000):
                QTest.qWait(1)
            assert expired.count() == 1
        else:
            reply.body.extend(b'defgh' if outcome == 'complete' else b'x' * 100)
            reply.readyRead.emit()
            reply.setFinished(True)
            reply.finished.emit()
        assert not downloader._downloads
        assert reply.abort_count == (0 if outcome == 'complete' else 1)
        assert downloaded.count() == (1 if outcome == 'complete' else 0)
        if outcome == 'complete':
            cache.assert_called_once_with(reply.url().toString(), b'abcdefgh')
        else:
            cache.assert_not_called()
        QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
        assert destroyed.count() == 1
        assert timer_destroyed.count() == 1

    @staticmethod
    def assert_rejected_download(download):
        download.cache.assert_not_called()
        download.save.assert_not_called()
        download.downloaded.assert_not_called()
        assert not download.downloader._downloads
        assert not download.deadline.isActive()
        download.reply.abort.assert_called_once()
        download.reply.deleteLater.assert_called_once()

    @pytest.fixture
    def png_data(self):
        data = QByteArray()
        buffer = QBuffer(data)
        buffer.open(QIODevice.OpenModeFlag.WriteOnly)
        image = QImage(2, 2, QImage.Format.Format_ARGB32)
        image.fill(0xff008040)
        assert image.save(buffer, 'PNG')
        return bytes(data)

    @pytest.mark.parametrize('payload', [
        b'<html>Not an image</html>', b'MZ executable content', b'#!/bin/sh\nexit 0', b'not an image',
    ])
    def test_reject_non_image_with_image_header(self, bounded_download, monkeypatch, mocker, payload):
        download = bounded_download
        monkeypatch.setattr(Settings, 'viewer_save_resources', True)
        monkeypatch.setattr(download.downloader, 'MAX_IMAGE_BYTES', 1024)
        mocker.stop(download.cache)
        download.body.extend(payload)
        download.signals.finished.emit()
        download.save.assert_not_called()
        download.downloaded.assert_not_called()
        assert download.downloader.downloaded_cnt == 0
        assert not download.downloader._downloads
        download.reply.deleteLater.assert_called_once()

    @pytest.mark.parametrize('bounded_download', [
        'https://images.invalid/badge',
        'https://images.invalid/tests.yaml?color=green',
        'https://images.invalid/picture.exe?name=payload.cmd',
    ], indirect=True)
    def test_save_verified_image_with_safe_extension(self, bounded_download, png_data, tmp_path,
                                                     monkeypatch, mocker):
        download = bounded_download
        monkeypatch.setattr(Settings, 'viewer_save_resources', True)
        monkeypatch.setattr(download.downloader, 'MAX_IMAGE_BYTES', 1024)
        monkeypatch.setattr(download.downloader, 'folder', QDir(str(tmp_path / download.downloader.RESOURCE_DIR)))
        mocker.stop(download.cache)
        mocker.stop(download.save)
        # Redirects must retain the URL used by the document as their cache identity.
        download.reply.url.return_value = QUrl('https://cdn.invalid/redirected.php')
        download.body.extend(png_data)
        download.signals.finished.emit()
        files = list(tmp_path.rglob('*.*'))
        assert len(files) == 1
        path = files[0]
        assert path.suffix == '.png'
        assert '?' not in path.name and '=' not in path.name
        assert path.read_bytes() == png_data
        cached_path = download.downloader.get_cached_image_path(download.url, str(tmp_path))
        assert cached_path is not None
        assert Path(cached_path) == path
        assert QPixmapCache.find(download.url, QPixmap())
        download.downloaded.assert_called_once()
        event = download.downloaded.call_args.args[0]
        assert event['resource_name'] == download.url
        assert event['pixmap'].toImage().convertToFormat(QImage.Format.Format_ARGB32) == QImage.fromData(png_data)

    def test_extensionless_svg_is_saved_as_svg(self, bounded_download, tmp_path, monkeypatch, mocker):
        download = bounded_download
        monkeypatch.setattr(Settings, 'viewer_save_resources', True)
        monkeypatch.setattr(download.downloader, 'MAX_IMAGE_BYTES', 1024)
        monkeypatch.setattr(download.downloader, 'folder', QDir(str(tmp_path / download.downloader.RESOURCE_DIR)))
        mocker.stop(download.cache)
        mocker.stop(download.save)
        data = b'<svg xmlns="http://www.w3.org/2000/svg" width="8" height="8"><rect width="8" height="8"/></svg>'
        download.headers[QNetworkRequest.KnownHeaders.ContentTypeHeader] = 'image/svg+xml'
        download.body.extend(data)
        download.signals.finished.emit()
        path = download.downloader.get_cached_image_path(download.url, str(tmp_path))
        assert path is not None and path.endswith('.svg')
        assert QPixmap(path).size().width() == 8

    def test_corrupt_or_oversized_image_is_not_cached(self, test_downloader_obj, png_data, monkeypatch):
        downloader = test_downloader_obj
        url = 'https://images.invalid/invalid.png'
        QPixmapCache.remove(url)
        assert downloader.cache_pixmap(url, png_data[:33]) is None
        monkeypatch.setattr(downloader, 'MAX_IMAGE_PIXELS', 3)
        assert downloader.cache_pixmap(url, png_data) is None
        assert not QPixmapCache.find(url, QPixmap())

    def test_existing_extensionless_cache_is_still_found(self, test_downloader_obj, png_data, tmp_path):
        downloader = test_downloader_obj
        url = 'https://images.invalid/old-badge'
        folder = tmp_path / downloader.RESOURCE_DIR
        folder.mkdir()
        legacy = folder / downloader._legacy_filename(url)
        legacy.write_bytes(png_data)
        cached_path = downloader.get_cached_image_path(url, str(tmp_path))
        assert cached_path is not None
        assert Path(cached_path) == legacy
        assert not QPixmap(str(legacy)).isNull()

    def test_filename_bounds_and_query_identity(self):
        url = 'https://images.invalid/' + '%2f%5c%00' * 80 + '.exe?color=green'
        name = ImageDownloader.url_to_filename(url, 'png')
        assert len(name) < 110
        assert name.endswith('.png')
        assert not any(character in name for character in '/\\\x00?=:')
        assert ImageDownloader.url_to_filename(url, 'png') != ImageDownloader.url_to_filename(url + '2', 'png')

    @pytest.mark.parametrize('image_format,payload', [
        # A TGA image ID prevents the header from also matching Qt's ICO/CUR probe.
        pytest.param('tga', struct.pack('<BBBHHBHHHHBB', 1, 0, 2, 0, 0, 0, 0, 0, 2, 2, 24, 0x20)
                     + b'I' + b'\x00\x80\xff' * 4 + b'\x00' * 8 + b'TRUEVISION-XFILE.\x00', id='tga'),
        pytest.param('wbmp', b'\x00\x00\x02\x02\x80\x40', id='wbmp'),
    ])
    def test_preserve_native_image_formats(self, test_downloader_obj, tmp_path, monkeypatch, mocker,
                                           image_format, payload):
        if image_format.encode() not in {bytes(value) for value in QImageReader.supportedImageFormats()}:
            pytest.skip(f'The installed Qt plugins do not include {image_format}')
        expected = QPixmap()
        assert expected.loadFromData(payload)
        downloader = test_downloader_obj
        monkeypatch.setattr(Settings, 'viewer_save_resources', True)
        downloader.update_resource_folder(str(tmp_path))
        reply = BufferedReply(downloader)
        url = f'https://images.invalid/format.{image_format}'
        reply.setUrl(QUrl(url))
        reply.setHeader(QNetworkRequest.KnownHeaders.ContentTypeHeader, f'image/{image_format}')
        mocker.patch.object(downloader.network_manager, 'get', return_value=reply)
        downloaded = QSignalSpy(downloader.downloaded)
        downloader.download_image(url)
        reply.body.extend(payload)
        reply.readyRead.emit()
        reply.setFinished(True)
        reply.finished.emit()
        assert downloaded.count() == 1
        path = downloader.get_cached_image_path(url, str(tmp_path))
        assert path is not None and path.endswith(f'.{image_format}')
        assert QPixmap(path).toImage() == expected.toImage()
        cached = QPixmap()
        assert QPixmapCache.find(url, cached)
        assert cached.toImage() == expected.toImage()
        QPixmapCache.remove(url)

    @pytest.fixture
    def document_host(self, test_downloader_obj, tmp_path):
        from notolog.notolog_editor import NotologEditor
        document = QTextDocument()
        downloader = test_downloader_obj
        downloader.update_resource_folder(str(tmp_path))
        host = SimpleNamespace(resource_downloader=downloader, logger=Mock(),
                               get_view_doc=lambda: document, get_view_widget=lambda: document)
        host.get_cached_resource_pixmap = Mock(side_effect=AssertionError('Unexpected cache lookup'))
        host.attach_resource = lambda url, pixmap: NotologEditor.attach_resource(host, url, pixmap)
        return host, document

    @pytest.mark.parametrize('save_to_disk', [False, True])
    def test_large_image_attaches_without_pixmap_cache(
            self, document_host, tmp_path, monkeypatch, mocker, save_to_disk):
        from notolog.notolog_editor import NotologEditor
        host, document = document_host
        downloader = host.resource_downloader
        monkeypatch.setattr(Settings, 'viewer_save_resources', save_to_disk)
        old_limit = QPixmapCache.cacheLimit()
        url = 'https://images.invalid/large-document-image.png'
        try:
            QPixmapCache.setCacheLimit(10240)
            image = QImage(1700, 1700, QImage.Format.Format_ARGB32)
            image.fill(0xff008040)
            data = QByteArray()
            buffer = QBuffer(data)
            buffer.open(QIODevice.OpenModeFlag.WriteOnly)
            assert image.save(buffer, 'PNG')
            assert len(data) < downloader.MAX_IMAGE_BYTES
            document.setHtml(f'<img src="{url}">')
            reply = BufferedReply(downloader)
            reply.setUrl(QUrl(url))
            mocker.patch.object(downloader.network_manager, 'get', return_value=reply)
            save = mocker.spy(downloader, 'save_image')
            downloader.downloaded.connect(lambda values: NotologEditor.resource_downloaded_handler(host, values))
            downloader.download_image(url)
            reply.body.extend(bytes(data))
            reply.readyRead.emit()
            reply.setFinished(True)
            reply.finished.emit()
            assert not QPixmapCache.find(url, QPixmap())
            resource = document.resource(QTextDocument.ResourceType.ImageResource, QUrl(url))
            assert isinstance(resource, QPixmap)
            assert resource.toImage().convertToFormat(image.format()) == image
            host.get_cached_resource_pixmap.assert_not_called()
            assert downloader.downloaded_cnt == 1
            QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
            NotologEditor.resource_downloader_finished_handler(host, downloader.downloaded_cnt)
            resource = document.resource(QTextDocument.ResourceType.ImageResource, QUrl(url))
            assert isinstance(resource, QPixmap)
            assert resource.toImage().convertToFormat(image.format()) == image
            if save_to_disk:
                save.assert_called_once()
                assert downloader.get_cached_image_path(url, str(tmp_path)) is not None
            else:
                save.assert_not_called()
                assert not (tmp_path / downloader.RESOURCE_DIR).exists()
        finally:
            QPixmapCache.remove(url)
            QPixmapCache.setCacheLimit(old_limit)

    def test_completion_survives_cache_eviction(self, document_host, png_data, monkeypatch, mocker):
        from notolog.notolog_editor import NotologEditor
        host, document = document_host
        downloader = host.resource_downloader
        monkeypatch.setattr(Settings, 'viewer_save_resources', False)
        reply = BufferedReply(downloader)
        url = reply.url().toString()
        mocker.patch.object(downloader.network_manager, 'get', return_value=reply)
        downloader.downloaded.connect(lambda _: QPixmapCache.remove(url))
        downloader.downloaded.connect(lambda values: NotologEditor.resource_downloaded_handler(host, values))
        downloader.download_image(url)
        reply.body.extend(png_data)
        reply.readyRead.emit()
        reply.setFinished(True)
        reply.finished.emit()
        assert not QPixmapCache.find(url, QPixmap())
        resource = document.resource(QTextDocument.ResourceType.ImageResource, QUrl(url))
        assert isinstance(resource, QPixmap) and resource.size() == QPixmap.fromImage(QImage.fromData(png_data)).size()
        host.get_cached_resource_pixmap.assert_not_called()

    def test_url_only_completion_keeps_cache_lookup(self, document_host):
        from notolog.notolog_editor import NotologEditor
        host, document = document_host
        url = 'https://images.invalid/legacy-signal.png'
        pixmap = QPixmap(2, 2)
        pixmap.fill()
        host.get_cached_resource_pixmap = Mock(return_value=pixmap)
        NotologEditor.resource_downloaded_handler(host, {'resource_name': url})
        host.get_cached_resource_pixmap.assert_called_once_with(url)
        resource = document.resource(QTextDocument.ResourceType.ImageResource, QUrl(url))
        assert isinstance(resource, QPixmap) and resource.toImage() == pixmap.toImage()
