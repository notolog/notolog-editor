"""
AI Assistant Dialog Class

This class is designed to facilitate and manage interactions between the user and various external plugins or APIs.
It acts as a bridge to send queries to and receive responses from selected plugins, ensuring seamless integration and
efficient data handling. The class leverages user inputs and contextual information to interact with APIs dynamically.

Features:
- Sends requests and receives responses based on user inputs or context.
- Supports robust error handling to manage API limitations or failures, ensuring consistent application performance.
- Provides functionality that can be adjusted based on the app
"""

from PySide6.QtCore import Qt, QUrl, QByteArray, QSize
from PySide6.QtNetwork import QNetworkRequest, QNetworkAccessManager, QNetworkReply
from PySide6.QtWidgets import QDialog, QVBoxLayout, QWidget, QLineEdit, QTextEdit, QPushButton
from PySide6.QtWidgets import QLabel, QSizePolicy, QHBoxLayout
from PySide6.QtGui import QPixmap

import json
import logging

from ..settings import Settings
from ..app_config import AppConfig
from ..lexemes.lexemes import Lexemes
from ..helpers.theme_helper import ThemeHelper
from ..ui.rotating_label import RotatingLabel
from ..enums.ai_model_names import AiModelNames
from .vertical_line_spacer import VerticalLineSpacer


class AIAssistant(QDialog):

    def __init__(self, parent):
        super().__init__(parent, Qt.WindowType.Dialog)

        self.parent = parent

        # Apply font from the dialog instance to the label
        self.setFont(self.parent.font())

        self.logger = logging.getLogger('ai_assistant')

        self.logging = AppConfig.get_logging()
        self.debug = AppConfig.get_debug()

        self.settings = Settings(parent=self)

        # TODO add more AI providers and a setting of which one is in use
        self.api_url = self.settings.ai_config_openai_url
        self.api_key = self.settings.ai_config_openai_key
        self.inference_model = AiModelNames.__getitem__(self.settings.ai_config_openai_model).value
        self.prompt_system = self.settings.ai_config_base_system_prompt
        self.prompt_user = "%s"
        self.response_max_tokens = self.settings.ai_config_base_response_max_tokens

        self.theme_helper = ThemeHelper()

        # Default language setup, change to settings value to modify it via UI
        self.lexemes = Lexemes(self.settings.app_language, default_scope='ai_assistant')

        self.layout = QVBoxLayout(self)

        self.setWindowTitle(self.lexemes.get('dialog_title'))

        # Set dialog size derived from the main window size
        main_window_size = self.parent.size()
        dialog_width = int(main_window_size.width() * 0.5)
        dialog_height = int(main_window_size.height() * 0.5)
        # self.setMinimumSize(dialog_width, dialog_height)
        self.resize(dialog_width, dialog_height)

        self.setStyleSheet(self.theme_helper.get_css('ai_assistant'))

        # Prompt input field
        self.prompt_input = QLineEdit(self)
        self.prompt_input.sizeHint()
        self.prompt_input.setPlaceholderText(
            self.lexemes.get('dialog_prompt_input_placeholder_text'))
        self.prompt_input.setAccessibleDescription(
            self.lexemes.get('dialog_prompt_input_accessible_description'))
        self.prompt_input.returnPressed.connect(self.send_request)
        self.layout.addWidget(self.prompt_input)

        # Text output field for displaying JSON response
        self.response_output = QTextEdit(self)
        self.response_output.sizeHint()
        self.response_output.setReadOnly(True)
        self.response_output.setPlaceholderText(
            self.lexemes.get('dialog_response_output_placeholder_text'))
        self.response_output.setAccessibleDescription(
            self.lexemes.get('dialog_response_output_accessible_description'))
        self.layout.addWidget(self.response_output)

        label_size = QSize(48, 48)
        label_pixmap = QPixmap(self.theme_helper.get_icon(theme_icon='arrow-repeat.svg').pixmap(label_size))
        # Use custom Pixmap class to asure the transformation (rotation)
        self.background_label = RotatingLabel(pixmap=label_pixmap, parent=self)
        self.background_label.resize(label_size)
        # self.background_label.setPixmap(label_pixmap)
        self.background_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        # Set at the center of the result text field
        self.background_label.setGeometry(self.width() // 2 - self.background_label.width() // 2,
                                          self.height() // 2 - self.background_label.height() // 2,
                                          self.background_label.width(),
                                          self.background_label.height())
        # Rise it up on the first plane
        self.background_label.raise_()
        # Hide on the very beginning as it will be set to visible upon request
        self.background_label.hide()

        status_bar_widget = QWidget(self)
        status_bar_layout = QHBoxLayout(status_bar_widget)

        model_label = QLabel(text=self.lexemes.get('dialog_usage_model_label'))
        model_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        model_label.sizeHint()
        model_label.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        model_label.setObjectName("ai_assistant_dialog_usage_model_label")
        # model_label.setStyleSheet("QLabel {color: grey;}")
        status_bar_layout.addWidget(model_label)

        status_bar_layout.addWidget(VerticalLineSpacer())

        self.model_label = QLabel(text=self.inference_model)
        self.model_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.model_label.sizeHint()
        self.model_label.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        self.model_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        status_bar_layout.addWidget(self.model_label)

        central_spacer = QWidget()
        central_spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        status_bar_layout.addWidget(central_spacer)

        tokens_label = QLabel(text=self.lexemes.get('dialog_usage_tokens_label'))
        tokens_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        tokens_label.sizeHint()
        tokens_label.setObjectName("ai_assistant_dialog_usage_tokens_label")
        # tokens_label.setStyleSheet("QLabel {color: grey;}")
        status_bar_layout.addWidget(tokens_label)
        status_bar_layout.addWidget(VerticalLineSpacer(), alignment=Qt.AlignmentFlag.AlignRight)
        self.tokens_prompt_label = QLabel()
        self.tokens_prompt_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.tokens_prompt_label.sizeHint()
        status_bar_layout.addWidget(self.tokens_prompt_label)
        status_bar_layout.addWidget(VerticalLineSpacer(), alignment=Qt.AlignmentFlag.AlignRight)
        self.tokens_answer_label = QLabel()
        self.tokens_answer_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.tokens_answer_label.sizeHint()
        status_bar_layout.addWidget(self.tokens_answer_label)
        status_bar_layout.addWidget(VerticalLineSpacer(), alignment=Qt.AlignmentFlag.AlignRight)
        self.tokens_total_label = QLabel()
        self.tokens_total_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.tokens_total_label.sizeHint()
        status_bar_layout.addWidget(self.tokens_total_label)

        self.layout.addWidget(status_bar_widget)
        # Update usage with initial params
        self.update_usage()

        # Submit button
        self.send_button = QPushButton(self.lexemes.get('dialog_button_send_request'), self)
        self.send_button.setFont(self.font())
        self.layout.addWidget(self.send_button)
        self.send_button.clicked.connect(self.send_request)

        # Set the main layout for the dialog
        self.setLayout(self.layout)

    def handle_response(self, reply: QNetworkReply, error_code=None):
        # Get received status code, say 200
        status_code = reply.attribute(QNetworkRequest.Attribute.HttpStatusCodeAttribute)

        if self.debug:
            self.logger.debug(f'AI assistant response: {reply}, {error_code}, {status_code}')

        # Return the QNetworkReply object that emitted the signal.
        # For example: NetworkError.UnknownNetworkError
        # reply = self.sender()  # type: QNetworkReply

        error = None
        # Make sure there is no error
        if reply.error() == QNetworkReply.NetworkError.NoError:
            # The request was successful
            data = reply.readAll()  # type: QByteArray

            if self.debug:
                self.logger.debug(f'Raw RESPONSE [{status_code}]: {data}')

            reply.deleteLater()  # Clean up the QNetworkReply object

            # json_document = QJsonDocument.fromJson(data)
            # json_data = json_document.object()

            # Convert QByteArray to string
            res_string = data.toStdString()  # Or: str(data.data(), encoding='utf-8')
            if self.debug:
                self.logger.debug(f'Result multi-line STRING: {res_string}')

            # Clean up the string and make one line
            json_str = ''.join(line.strip() for line in res_string.splitlines())

            if self.debug:
                self.logger.debug(f'Result STRING: {json_str}')

            result_message = self.lexemes.get('network_connection_error_empty', scope='common')
            # Parse JSON response
            try:
                json_data = json.loads(json_str)
                if self.debug:
                    self.logger.debug(f"Result JSON: {json_data}")
                if ('choices' in json_data
                        and len(json_data['choices']) > 0
                        # Legacy completions
                        # and 'text' in json_data['choices'][0]):
                        and 'message' in json_data['choices'][0]
                        and 'content' in json_data['choices'][0]['message']):
                    # Legacy completions
                    # self.response_output.setPlainText(str(json_data['choices'][0]['text']).strip())
                    self.response_output.setPlainText(str(json_data['choices'][0]['message']['content']).strip())
                if 'usage' in json_data:
                    self.update_usage(json_data['usage'])
                if 'model' in json_data:
                    if hasattr(self, 'model_label'):
                        self.model_label.setText(json_data['model'] if len(json_data['model']) > 0 else '?')
            except json.JSONDecodeError as e:
                if self.logging:
                    self.logger.warning("Error decoding JSON: %s" % e)
        elif reply.error() == QNetworkReply.NetworkError.HostNotFoundError:
            # The host was not found, indicating possible DNS issues or no internet connection
            result_message = self.lexemes.get('network_connection_error_connection_or_dns', scope='common')
        elif reply.error() == QNetworkReply.NetworkError.ConnectionRefusedError:
            # Connection was refused, indicating the server might be down or there are network issues
            result_message = self.lexemes.get('network_connection_error_connection_refused', scope='common')
        elif reply.error() == QNetworkReply.NetworkError.TimeoutError:
            # The connection timed out, indicating network issues
            result_message = self.lexemes.get('network_connection_error_connection_timed_out', scope='common')
        elif reply.error() == QNetworkReply.NetworkError.ContentNotFoundError:
            # The requested page or resource is not found
            result_message = self.lexemes.get('network_connection_error_connection_404_error', scope='common')
        else:
            # Handle other errors
            result_message = self.lexemes.get('network_connection_error_generic_with_status_code', scope='common',
                                              status_code=status_code)

        if error_code is not None:
            if self.logging:
                self.logger.warning(result_message)
                self.logger.warning(f"Failed to fetch update information: {reply.errorString()}")
            # Set up response status visible within response field
            self.response_output.setPlainText(result_message)

        self.set_status_ready()

    def update_usage(self, usage: dict = None):
        if hasattr(self, 'tokens_prompt_label'):
            prompt_tokens_cnt = (usage['prompt_tokens'] if usage and 'prompt_tokens' in usage else 0)
            self.tokens_prompt_label.setText(self.lexemes.get('dialog_usage_tokens_prompt',
                                                              tokens=prompt_tokens_cnt))
        if hasattr(self, 'tokens_answer_label'):
            answer_tokens_cnt = (usage['completion_tokens'] if usage and 'completion_tokens' in usage else 0)
            self.tokens_answer_label.setText(self.lexemes.get('dialog_usage_tokens_prompt',
                                                              tokens=answer_tokens_cnt))
        if hasattr(self, 'tokens_total_label'):
            total_tokens_cnt = (usage['total_tokens'] if usage and 'total_tokens' in usage else 0)
            self.tokens_total_label.setText(self.lexemes.get('dialog_usage_tokens_total',
                                                             tokens=total_tokens_cnt))

    def send_request(self) -> None:
        # Get context for the prompt
        prompt_context = self.prompt_input.text()
        if len(prompt_context) == 0:
            self.response_output.setText(self.lexemes.get('dialog_response_output_notice_empty_text'))
            return

        url = QUrl(self.api_url)  # API entrypoint
        request = QNetworkRequest(url)

        # Set Authorization header
        access_token = self.api_key
        request.setRawHeader(b"Authorization", bytes("Bearer " + access_token, encoding="utf-8"))

        # Set Content-Type header
        request.setHeader(QNetworkRequest.KnownHeaders.ContentTypeHeader, "application/json")

        # Legacy completions
        """
        Consider these params as well:
        * "logprobs": None,
        * "echo": false,
        * * "stop": null,
        * "presence_penalty": 0,
        * "frequency_penalty": 0,
        * * "best_of": 1,
        * "logit_bias": None,
        * "user": "",
        """

        # New completions
        post_params = {
            "model": self.inference_model,
            "messages": [
                {
                    "role": "system",
                    "content": self.prompt_system,
                },
                {
                    "role": "user",
                    "content": self.prompt_user % prompt_context,
                }
            ],
            "temperature": 0.2,
            "top_p": 1,
            "n": 1,
            "stream": False,
        }
        # If response max tokens set
        if self.response_max_tokens:
            post_params.update({"max_tokens": self.response_max_tokens})

        json_post_params = json.dumps(post_params)

        # Set request data
        request_data = QByteArray(json_post_params.encode("utf-8"))

        # Set request type to POST
        request.setRawHeader(b"Custom-Request", b"POST")

        self.set_status_waiting()

        # Set request data
        manager = QNetworkAccessManager(self)
        reply = manager.post(request, request_data)

        # Connect finished signal
        reply.finished.connect(lambda _reply=reply: self.handle_response(_reply))
        # Connect error signal
        reply.errorOccurred.connect(lambda error, _reply=reply: self.handle_response(_reply, error))

    def set_status_waiting(self):
        # Set loader cursor whilst loading content
        self.setCursor(Qt.CursorShape.WaitCursor)
        # Disable prompt input field
        self.prompt_input.setDisabled(True)
        # Clear response field from prev results if set
        self.response_output.clear()
        # Disconnect Enter action onto the input field
        self.prompt_input.returnPressed.disconnect()
        # Disable send request button
        self.send_button.setDisabled(True)
        # Show progress label
        self.background_label.show()

    def set_status_ready(self):
        # Set cursor back
        self.setCursor(Qt.CursorShape.ArrowCursor)
        # Enable prompt input field
        self.prompt_input.setEnabled(True)
        # Connect Enter action onto the input field
        self.prompt_input.returnPressed.connect(self.send_request)
        # Enable send request button
        self.send_button.setEnabled(True)
        # Hide progress label
        self.background_label.hide()
