"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: App update helper class.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2025 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import QObject, Signal, Slot, QUrl
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply, QSslSocket

from packaging import version
from typing import TYPE_CHECKING

import json
import logging

from . import AppConfig

from ..settings import Settings
from ..lexemes.lexemes import Lexemes

if TYPE_CHECKING:
    from PySide6.QtCore import QByteArray  # noqa: F401


class UpdateHelper(QObject):
    """
    # How to use example:
    update_helper = UpdateHelper()
    update_helper.new_version_available.connect(lambda v:
                                                QMessageBox.information(None, "Update Available",
                                                                        f"A new version {v} is available."))
    update_helper.check_for_updates()
    """

    STATUS_OK = 'ok'
    STATUS_ERROR = 'error'

    # Signal to emit if a new version is available
    new_version_check_response = Signal(object)  # Or: Signal(str)

    def __init__(self):
        super().__init__()

        self.settings = Settings(parent=self)

        self.logger = logging.getLogger('update_helper')

        self.logger.info("SSL supported: %s" % QSslSocket.supportsSsl())

        # Load lexemes for selected language and scope
        self.lexemes = Lexemes(self.settings.app_language, default_scope='common')

        self.current_version = version.parse(AppConfig().get_app_version())

        self.manager = QNetworkAccessManager(self)

    def check_for_updates(self):
        # Updates url
        release_url = AppConfig().get_repository_github_api_release_url()
        request = QNetworkRequest(QUrl(release_url))
        self.logger.info(f'Check for update request to {release_url}')
        # Set request data
        # reply = self.manager.post(request, request_data)  # POST
        reply = self.manager.get(request)  # GET

        # Connect finished signal
        reply.finished.connect(self.handle_network_reply)
        # Connect error signal
        reply.errorOccurred.connect(lambda error: self.handle_network_reply(error))

    @Slot(str)
    def handle_network_reply(self, error_code=None):
        # Get reply object that emitted the signal.
        reply = self.sender()  # type: QNetworkReply

        # Get received status code, say 200
        status_code = reply.attribute(QNetworkRequest.Attribute.HttpStatusCodeAttribute)

        self.logger.debug(f'Update response, reply: {reply}, error_code: {error_code}, status_code: {status_code}')

        # Make sure there is no error
        if reply.error() == QNetworkReply.NetworkError.NoError:
            result_message = self.process_response(reply, status_code)
        elif reply.error() == QNetworkReply.NetworkError.HostNotFoundError:
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

        if error_code is not None:
            self.logger.warning(result_message)
            self.logger.warning(f"Failed to fetch update information: {reply.errorString()}")
            # Emit error signal
            self.new_version_check_response.emit({'status': self.STATUS_ERROR, 'msg': result_message})

        reply.finished.disconnect()
        reply.errorOccurred.disconnect()
        reply.deleteLater()  # Clean up the QNetworkReply object

    def process_response(self, reply: QNetworkReply, status_code) -> str:
        # The request was successful
        data = reply.readAll()  # type: QByteArray
        # Or like this:
        # data = reply.readAll().data().decode('utf-8')
        # json_data = json.loads(data)

        self.logger.debug(f'Raw RESPONSE [{status_code}]: {data}')

        # json_document = QJsonDocument.fromJson(data)
        # json_data = json_document.object()

        # Convert QByteArray to string
        res_string = data.toStdString()  # Or: str(data.data(), encoding='utf-8')
        self.logger.debug(f'Result multi-line STRING: {res_string}')

        # Clean up the string and make one line
        json_str = ''.join(line.strip() for line in res_string.splitlines())

        self.logger.debug(f'Result STRING: {json_str}')

        result_message = self.lexemes.get('network_connection_error_empty')
        # Parse JSON response
        try:
            json_data = json.loads(json_str)
            self.logger.debug(f"Result JSON: {json_data}")

            latest_version_str = json_data['tag_name']
            latest_version = version.parse(latest_version_str)

            if latest_version > self.current_version:
                # 'releases/latest' will redirect to 'releases/tag/v1.2.3'
                update_link = ('<a href="%s">%s</a>'
                               % (AppConfig().get_repository_github_release_url(), latest_version))
                result_message = self.lexemes.get('update_helper_new_version_is_available',
                                                  latest_version=update_link)
                self.logger.info("New version of the app is available: %s. Current version is %s. Response: %s"
                                 % (latest_version, self.current_version, reply.errorString()))
                # Emit the new version signal
                self.new_version_check_response.emit(
                    {'status': self.STATUS_OK, 'msg': result_message,
                     'current_version': self.current_version,
                     # Check new version by this var
                     'new_version': latest_version_str})
            else:
                result_message = self.lexemes.get('update_helper_latest_version_installed')
                self.logger.info("No new version of the app is available, the current version is %s."
                                 % self.current_version)
                self.logger.debug("Version check response: %s, %s" % (reply.readAll(), reply.errorString()))
                # Emit the same version signal
                self.new_version_check_response.emit(
                    {'status': self.STATUS_OK, 'msg': result_message, 'current_version': self.current_version})

        except json.JSONDecodeError as e:
            self.logger.warning("Error decoding JSON: %s" % e)

        return result_message
