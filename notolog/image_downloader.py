"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Async image downloader.
- Functionality: Automatically downloads image resources mentioned in the markdown document and caches them in memory
  or on the drive.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2025 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import Signal, QObject, QUrl, QDir, QByteArray
from PySide6.QtGui import QPixmap, QPixmapCache
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

from .settings import Settings
from .app_config import AppConfig
from .lexemes.lexemes import Lexemes
from .helpers.file_helper import size_f, save_file

from urllib.parse import urlparse
from typing import Union

from qasync import asyncSlot
import asyncio

import os
import re
import hashlib
import logging


class ImageDownloader(QObject):  # QObject to allow signal emitting

    # Signal to emit upon single resource was downloaded
    downloaded = Signal(dict)

    # Signal to emit upon all downloading tasks in queue have been finished
    finished = Signal(int)

    RESOURCE_DIR = AppConfig().get_editor_media_dir()

    event_loop = None  # async event loop
    resource_tasks: list = []  # async downloads task queue
    folder: Union[QDir, None] = None  # active folder to work with resources
    base_folder: str = None  # base folder to work with
    downloaded_cnt: int = 0  # downloads counter, counts till finished emitted
    network_manager: QNetworkAccessManager = None

    def __init__(self, base_folder: str = None):
        super().__init__()

        self.settings = Settings(parent=self)

        self.logger = logging.getLogger('image_downloader')

        self.lexemes = Lexemes()

        self.base_folder = base_folder

        # Setup start up params
        self.initialize()

    def initialize(self):
        self.update_resource_folder(self.base_folder)
        self.network_manager = QNetworkAccessManager(self)

    def get_resource_folder(self, base_folder: str = None) -> QDir:
        # Check folder and make it QDir
        if base_folder:
            folder = os.path.join(base_folder, self.RESOURCE_DIR)
        else:
            folder = os.path.join(QDir.currentPath(), self.RESOURCE_DIR)
        if isinstance(folder, str):
            folder = QDir(folder)
        return folder

    def update_resource_folder(self, base_folder: str = None) -> None:
        # Validate folder and make it QDir
        self.folder = self.get_resource_folder(base_folder)

        self.logger.debug(f'Folder to save downloaded resources: {self.folder.path()}')

    def download_image(self, url: str) -> None:
        if not self.is_external_url(url):
            self.logger.debug(f"Skip downloading as the provided url is not an external url: {url}")
            return

        self.logger.debug(f'Downloading resource from "{url}"')

        request = QNetworkRequest(QUrl(url))
        reply = self.network_manager.get(request)

        # Connecting finished signal
        reply.finished.connect(lambda _reply=reply: self.handle_network_reply(_reply))
        # Connecting error signal
        reply.errorOccurred.connect(lambda error, _reply=reply: self.handle_network_reply_error(_reply, error))

    def save_image(self, url: str, data: QByteArray) -> None:
        # file_name = os.path.basename(url)
        file_name = self.url_to_filename(url)
        # Alternative approach:
        # file_extension = self.mime_to_extension(mime_type)
        # file_name = f"{file_name}{file_extension}"
        # Create resource folder if not yet created
        if os.access(os.path.dirname(self.folder.path()), os.W_OK):
            os.makedirs(self.folder.path(), exist_ok=True)
        else:
            self.logger.warning(f"Permission denied: Cannot create directory {self.folder.path()}")
            return
        # File path to save
        file_path = os.path.join(self.folder.path(), file_name)
        # Save received data
        if save_file(file_path, data, as_bytearray=True):
            self.logger.debug(f"Resource saved {url} to {file_path} [{size_f(len(data))}]")
        else:
            self.logger.debug(f"Resource not saved {url} to {file_path} [{size_f(len(data))}]")

    def handle_network_reply(self, reply):
        # Get received status code, say 200
        status_code = reply.attribute(QNetworkRequest.Attribute.HttpStatusCodeAttribute)

        self.logger.debug(f'Network reply, reply: {reply}, status_code: {status_code}')

        # Make sure there is no error
        if reply.error() == QNetworkReply.NetworkError.NoError:
            # No error, processing the image
            result_message = self.lexemes.get('network_connection_error_empty')
            self.logger.debug(result_message)

            # Check if the resource is an image
            mime_type = reply.header(QNetworkRequest.KnownHeaders.ContentTypeHeader)
            if 'image' in mime_type:
                url = reply.url().toString()
                data = reply.readAll()  # type: QByteArray

                self.logger.debug(f"Resource data downloaded {url} [{size_f(len(data))}]")

                # Store the image within the app's cache first
                self.cache_pixmap(url, data)

                # Save file if settings allow
                if self.settings.viewer_save_resources:
                    # Saving downloaded files
                    self.save_image(url, data)

                # Emit the file downloaded signal
                self.downloaded.emit({'resource_name': url})
                self.downloaded_cnt += 1

        reply.finished.disconnect()
        reply.errorOccurred.disconnect()
        reply.deleteLater()  # Clean up the QNetworkReply object

    def cache_pixmap(self, url: str, data: QByteArray):
        # Store the image within the app's cache first
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        QPixmapCache.insert(url, pixmap)

    def handle_network_reply_error(self, reply, error_code=None):
        # Get received status code, say 404
        status_code = reply.attribute(QNetworkRequest.Attribute.HttpStatusCodeAttribute)

        self.logger.debug(f'Network reply, reply: {reply}, error_code: {error_code}, status_code: {status_code}')

        if reply.error() == QNetworkReply.NetworkError.HostNotFoundError:
            # The host was not found, indicating possible DNS issues or no internet connection
            result_message = self.lexemes.get('network_connection_error_connection_or_dns')
        elif reply.error() == QNetworkReply.NetworkError.ConnectionRefusedError:
            # Connection was refused, indicating the server might be down or there are network issues
            result_message = self.lexemes.get('network_connection_error_connection_refused')
        elif reply.error() == QNetworkReply.NetworkError.TimeoutError:
            # The connection timed out, indicating network issues
            result_message = self.lexemes.get('network_connection_error_connection_timed_out')
        elif reply.error() == QNetworkReply.NetworkError.ContentNotFoundError:
            # The requested page or resource is not found
            result_message = self.lexemes.get('network_connection_error_connection_404_error')
        else:
            # Handle other errors
            result_message = self.lexemes.get('network_connection_error_generic_with_status_code',
                                              status_code=status_code)

        self.logger.warning(result_message)
        self.logger.warning(f'Failed to download resource "{reply.errorString()}" with error code [{error_code}]')

        reply.finished.disconnect()
        reply.errorOccurred.disconnect()
        reply.deleteLater()  # Clean up the QNetworkReply object

    @asyncSlot()
    async def download_resource_in_queue(self, resource_url) -> None:
        # Check async loop is running
        if not asyncio.get_event_loop().is_running():
            self.logger.debug('Skipping the task because the async loop is not running.')
            return

        self.logger.debug('Downloading resource %d tasks in queue' % len(self.resource_tasks))

        task = asyncio.ensure_future(self.resource_download_async(resource_url))  # task: .download_resource_in_queue()
        # Add task to the local pool first
        self.resource_tasks.append(task)
        # Callback method to set up further actions
        task.add_done_callback(lambda _task: self.resource_task_callback(_task))  # task: .resource_download_async()

        try:
            done, pending = await asyncio.wait(
                self.resource_tasks,
                return_when=asyncio.ALL_COMPLETED,  # There is no pending tasks check
                # timeout = 1.5  # to return after the timeout, some task could be pending
            )
            self.logger.debug(f'Downloading resource tasks progress. Done {len(done)}, pending {len(pending)}')
        except asyncio.CancelledError:
            # All tasks will be cancelled later upon close event
            pass

        if len(self.resource_tasks) <= 1:
            # Hold this method a particular amount of time to allow completed tasks to settle as this step is
            # typically ahead.
            try:
                await asyncio.sleep(0.25, self.event_loop)
            except asyncio.CancelledError:
                # All tasks will be cancelled later upon close event
                pass
            if self.downloaded_cnt > 0:
                # All tasks in queue have finished
                self.finished.emit(self.downloaded_cnt)
                self.downloaded_cnt = 0

    def resource_task_callback(self, task):
        self.logger.debug('%s from total %d completed with callback'
                          % (task.get_name(), len(self.resource_tasks)))

        # Remove finished task from the queue
        self.resource_tasks.remove(task)

    async def resource_download_async(self, image_url) -> None:
        """
        Downloading resource which will be processed by resource_downloaded_handler() then.
        """
        self.download_image(image_url)

    @staticmethod
    def is_external_url(url, base_domain='example.com'):
        """
        Determine if the given URL is an external URL.
        """
        parsed_url = urlparse(url)
        return not (parsed_url.netloc == '' or parsed_url.netloc.endswith(base_domain))

    @staticmethod
    def url_to_filename(url):
        """
        Generate a filename from a URL by hashing the URL except its basename and combining it with the basename.
        Convert a URL into a safe filename by replacing non-alphanumeric characters with underscores.
        """
        # Extract the basename
        basename = os.path.basename(url)

        # Hash the URL excluding the basename
        url_hash = hashlib.sha256(url.replace(basename, '').encode('utf-8')).hexdigest()
        short_hash = url_hash[:8]  # Use only first 8 characters of the hash

        # Combine the short hash with the basename
        safe_basename = basename.replace(os.path.splitext(basename)[1], '')
        safe_basename = re.sub(r'\W+', '_', safe_basename)  # sanitize to make sure it's a valid file name part
        return f"{short_hash}_{safe_basename}{os.path.splitext(basename)[1]}"

    @staticmethod
    def mime_to_extension(mime_type):
        # Map of common image MIME types to file extensions
        mime_map = {
            'image/jpeg': '.jpg',
            'image/png': '.png',
            'image/gif': '.gif',
            'image/bmp': '.bmp',
            'image/svg+xml': '.svg',
            'image/tiff': '.tiff',
            'image/webp': '.webp'
        }
        return mime_map.get(mime_type, '.dat')  # Default to .dat if MIME type is unknown
