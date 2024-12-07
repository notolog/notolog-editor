# tests/test_image_downloader.py

from PySide6.QtCore import Signal, QUrl
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest

from notolog.image_downloader import ImageDownloader
from notolog.settings import Settings
from notolog.app_config import AppConfig

from . import test_core_app  # noqa: F401

from unittest.mock import AsyncMock, MagicMock, patch
from pytest_mock import MockerFixture

import pytest
import asyncio


class TestImageDownloader:

    @staticmethod
    async def cleanup_tasks():
        # Cancel and clean up all pending asyncio tasks
        for task in asyncio.all_tasks():
            if task is not asyncio.current_task():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

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
    def test_downloader_obj(self, mocker: MockerFixture):
        """
        Testing object fixture.
        May contain minimal logic for testing purposes.
        """
        mocker.patch.object(AppConfig, 'get_logging', return_value=False)
        mocker.patch.object(AppConfig, 'get_debug', return_value=False)

        yield ImageDownloader()

        # await obj_mock.cancel_tasks()

    @pytest.fixture(scope="function")
    def test_exp_params_fixture(self, request):
        # Retrieve parameter values from the test request.
        param_values = request.param

        yield param_values

    @staticmethod
    def add_mock_signal(callback):
        signal = MagicMock(spec=Signal)
        # signal.emit = MagicMock(name='emit')
        # Explicitly add 'connect' to the signal
        signal.connect = lambda v: callback()
        signal.disconnect = lambda: None

        return signal

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "test_settings_fixture, test_exp_params_fixture, test_downloader_obj",
        [
            (False, (QNetworkReply.NetworkError.NoError, None, 'some_url1',
                     {QNetworkRequest.KnownHeaders.ContentTypeHeader: 'image'}, b'image_byte_array_data'), None),
            (True, (QNetworkReply.NetworkError.NoError, None, 'some_url1',
                    {QNetworkRequest.KnownHeaders.ContentTypeHeader: 'image'}, b'image_byte_array_data'), None),
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
                               test_downloader_obj: ImageDownloader):
        # Test params
        reply_error, error_code, resource_url, header_params, resource_data = test_exp_params_fixture

        # Get callback method to check
        mock_handle_network_reply = mocker.patch.object(
            test_downloader_obj, 'handle_network_reply', wraps=test_downloader_obj.handle_network_reply)
        mock_handle_network_reply_error = mocker.patch.object(
            test_downloader_obj, 'handle_network_reply_error',
            wraps=test_downloader_obj.handle_network_reply_error)
        # Download in async queue
        mock_download_resource_in_queue = mocker.patch.object(
            test_downloader_obj, 'download_resource_in_queue', new_callable=AsyncMock,
            wraps=test_downloader_obj.download_resource_in_queue)
        mock_resource_download_async = mocker.patch.object(
            test_downloader_obj, 'resource_download_async', wraps=test_downloader_obj.resource_download_async)
        # Get download callback method to check
        mock_callback = mocker.patch.object(
            test_downloader_obj, 'resource_task_callback', wraps=test_downloader_obj.resource_task_callback)
        # Downloading resource
        mock_download_image = mocker.patch.object(
            test_downloader_obj, 'download_image', wraps=test_downloader_obj.download_image)
        # Cache and save downloaded resource
        mock_save_image = mocker.patch.object(test_downloader_obj, 'save_image', return_value=None)
        mock_cache_pixmap = mocker.patch.object(test_downloader_obj, 'cache_pixmap', return_value=None)

        # AsyncMock mock class is designed to simulate asynchronous calls and can be awaited.
        mocker.patch.object(asyncio, 'wait', AsyncMock(return_value=(None, None)))

        # Check that the local task pool is empty.
        # An error here indicates that the queue was used in previous tests.
        assert len(test_downloader_obj.resource_tasks) == 0
        # Check default resource folder
        assert test_downloader_obj.folder.path().endswith(ImageDownloader.RESOURCE_DIR)

        # Mock QNetworkReply using create_autospec
        # mock_reply = create_autospec(QNetworkReply, instance=True)
        mock_reply = MagicMock(spec=QNetworkReply)
        mock_reply.error.return_value = reply_error
        mock_reply.readAll.return_value = resource_data
        mock_reply.url.return_value = QUrl(resource_url)
        assert mock_reply.url().toString() == resource_url

        # with patch('PySide6.QtGui.QPixmap') as MockPixmap:
        #    mock_pixmap_instance = MockPixmap.return_value
        #    mock_pixmap_instance.loadFromData = MagicMock()  # MagicMock(spec=QPixmap)

        mocker.patch.object(mock_reply, 'header', side_effect=lambda k: header_params.get(k, None))

        # Add 'finished' signal to mock_reply with an 'emit' method
        mock_reply.finished = self.add_mock_signal(
            lambda: test_downloader_obj.handle_network_reply(mock_reply))
        mock_reply.errorOccurred = self.add_mock_signal(
            lambda: test_downloader_obj.handle_network_reply_error(mock_reply, error_code))

        # Mock QNetworkAccessManager and its get method
        mock_manager = MagicMock(QNetworkAccessManager)
        mock_manager.get.return_value = mock_reply

        # Monkeypatch the network manager in the application
        monkeypatch.setattr(test_downloader_obj, 'network_manager', mock_manager)
        # monkeypatch.setattr("PySide6.QtNetwork.QNetworkAccessManager", lambda: mock_manager)

        mocker.patch.object(test_downloader_obj, 'is_external_url', return_value=True)

        await test_downloader_obj.download_resource_in_queue(resource_url)
        assert test_downloader_obj.downloaded_cnt == 0

        await asyncio.sleep(0.025)  # Faster sleeps may not work on macOS or Windows test environments

        mock_callback.assert_called_once()
        mock_download_resource_in_queue.assert_awaited_once_with(resource_url)

        await test_downloader_obj.download_resource_in_queue(resource_url)
        await asyncio.sleep(0.05)  # Or 0.251, slightly more than described in a queue method, to get all completed

        assert mock_callback.call_count == 2

        def _check_downloaded(url):
            assert 'resource_name' in url
            assert url['resource_name'] == resource_url
            assert test_downloader_obj.downloaded_cnt == 1
            assert len(test_downloader_obj.resource_tasks) == 0
        # Assert 'downloaded' signal
        test_downloader_obj.downloaded.connect(_check_downloaded)

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

        # The cleanup async tasks to speed up checks and exit
        await self.cleanup_tasks()

    @pytest.mark.parametrize(
        "test_exp_params_fixture, test_downloader_obj",
        [
            (('some_url1', 'some_exp|ected_hash', 'some_exp_some_url1'), None),
            (('some_url2', 'some_exp|ected_hash', 'some_exp_some_url2'), None),
            (('notolog.app/example.png', 'some_exp|ected_hash', 'some_exp_example.png'), None),
        ],
        indirect=True
    )
    def test_url_to_filename(self, monkeypatch, test_exp_params_fixture, test_downloader_obj: ImageDownloader):
        # Test params
        resource_url, hash256, expected_filename = test_exp_params_fixture

        # Mocking hashlib.sha256().hexdigest() using patch
        with patch('hashlib.sha256') as mock_sha256:
            # Mocking the return value of hexdigest() method
            mock_sha256.return_value.hexdigest.return_value = hash256

            assert test_downloader_obj.url_to_filename(resource_url) == expected_filename

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
