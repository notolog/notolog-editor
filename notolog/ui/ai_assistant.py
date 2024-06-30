"""
Notolog Editor
Open-source markdown editor developed in Python.

File Details:
- Purpose: AI Assistant Dialog Class.
- Functionality: This class facilitates interactions between the user and various external plugins or APIs.
  It acts as a bridge, sending queries to and receiving responses from selected plugins, ensuring seamless integration
  and efficient data handling. It dynamically leverages user inputs and contextual information for API interactions.

Features:
- Sends requests and receives responses based on user inputs or contextual cues.
- Implements robust error handling to manage API limitations or failures, ensuring consistent application performance.
- Adaptable functionality to suit different application needs.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtWidgets import QDialog, QVBoxLayout, QWidget, QLineEdit, QPushButton
from PySide6.QtWidgets import QLabel, QSizePolicy, QHBoxLayout, QScrollArea
from PySide6.QtGui import QPixmap, QColor

import logging

from typing import Union

from . import Settings
from . import AppConfig
from . import Lexemes
from . import ThemeHelper

from .vertical_line_spacer import VerticalLineSpacer

from ..ui.rotating_label import RotatingLabel
from ..ui.ai_message_label import AiMessageLabel
from ..modules.modules import Modules
from ..modules.base_ai_core import BaseAiCore
from ..enums.enum_base import EnumBase

from qasync import asyncClose
from datetime import datetime

import markdown


class EnumMessageType(EnumBase):
    # Sync with corresponding CSS-styles
    DEFAULT = ("default", True)  # Fallback default option
    USER_INPUT = "user_input"
    RESPONSE = "response"


class EnumMessageStyle(EnumBase):
    DEFAULT = ("default", True)  # Fallback default option
    INFO = "info"
    ERROR = "error"


class AIAssistant(QDialog):

    dialog_closed = Signal()
    request_cancelled = Signal()

    message_added = Signal(str, int, int, EnumMessageType)

    md: markdown.Markdown = None

    module: None
    # Inference module core
    module_core: BaseAiCore = None

    def __init__(self, parent):
        super().__init__(parent, Qt.WindowType.Window)

        # self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowState(Qt.WindowState.WindowActive)

        # Make the dialog non-modal
        self.setModal(False)  # or self.setWindowModality(Qt.WindowModality.NonModal)

        # Parent instance
        self.parent = parent

        # Apply font from the dialog instance to the label
        self.setFont(self.parent.font())

        self.logger = logging.getLogger('ai_assistant')

        self.logging = AppConfig().get_logging()
        self.debug = AppConfig().get_debug()

        self.settings = Settings(parent=self)
        self.settings.value_changed.connect(
            lambda v: self.settings_update_handler(v))

        # Load modules first to enable the loading of extension settings.
        module_instances = []
        for module in Modules().get_by_extension('ai_assistant'):
            # Pass settings object to avoid circular dependencies
            module_instances.append(Modules().create(module))

        # A module to use for inference
        self.inference_module = self.settings.ai_config_inference_module
        try:
            # Get the name of the inference module
            self.inference_module_name = Modules().modules.get(self.inference_module).get_name()
        except Exception as e:
            if self.logging:
                self.logger.warning(f"Inference module '{self.inference_module}' name is not set {e}")
            # Try to find any suitable module
            for module_name in self.settings.ai_config_inference_modules.keys():
                # Set up first available module as a default one
                self.settings.ai_config_inference_module = module_name
                self.inference_module = self.settings.ai_config_inference_module
                break
            # Update with the default module name
            self.inference_module_name = self.inference_module
            if self.logging:
                self.logger.warning(f"Fallback to the inference module named '{self.inference_module}'")

        self.theme_helper = ThemeHelper()

        # Load lexemes for selected language and scope
        self.lexemes = Lexemes(self.settings.app_language, default_scope='ai_assistant')

        # Dialog layout
        self.layout = QVBoxLayout(self)

        self.setWindowTitle(self.lexemes.get('dialog_title'))

        # UI element variables
        self.prompt_input = Union[QLineEdit, None]
        self.messages_area = Union[QScrollArea, None]
        self.messages_layout = Union[QWidget, None]
        self.background_label = Union[QLabel, None]
        self.module_name_label = Union[QLabel, None]
        self.model_name_label = Union[QLabel, None]
        self.tokens_prompt_label = Union[QLabel, None]
        self.tokens_answer_label = Union[QLabel, None]
        self.tokens_total_label = Union[QLabel, None]
        self.send_button = Union[QPushButton, None]
        self.save_history_button = Union[QPushButton, None]

        # Last added message id
        self.message_id = 0

        # Last requested message id
        self.request_message_id = 0

        # Message ids
        self.message_ids = []

        # Prompt and response tokens
        self.token_usage = {}

        self.init_ui()

    def init_ui(self):
        # Set dialog size derived from the main window size
        main_window_size = self.parent.size()
        dialog_width = int(main_window_size.width() * 0.7)
        dialog_height = int(main_window_size.height() * 0.7)
        # self.setMinimumSize(dialog_width, dialog_height)
        self.resize(dialog_width, dialog_height)

        # Main view margins
        self.setContentsMargins(5, 5, 5, 5)
        # Corresponding styles
        self.setStyleSheet(self.theme_helper.get_css('ai_assistant'))

        self.messages_area = QScrollArea(self)
        self.messages_area.setWidgetResizable(True)
        self.messages_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.messages_area.setStyleSheet("QScrollArea { border: none; }")
        self.messages_area.setAccessibleDescription(
            self.lexemes.get('dialog_response_output_accessible_description'))

        scroll_widget = QWidget()
        self.messages_layout = QVBoxLayout(scroll_widget)
        self.messages_layout.setContentsMargins(0, 0, 0, 5)
        self.messages_layout.setSpacing(0)
        # scroll_widget.setLayout(self.messages_layout)
        self.messages_area.setWidget(scroll_widget)

        self.layout.addWidget(self.messages_area)

        # To fill the space atop
        spacer_widget = QWidget()
        spacer_widget.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.messages_layout.addWidget(spacer_widget)

        # Prompt input field
        self.prompt_input = QLineEdit(self)
        self.prompt_input.setFont(self.font())
        self.prompt_input.setFocus()
        # Calculate height: font metrics height * 2 + some padding
        text_height = self.prompt_input.fontMetrics().height()
        self.prompt_input.setFixedHeight(text_height * 2 + 10)  # Adjust 10 for padding
        self.prompt_input.sizeHint()
        self.prompt_input.setPlaceholderText(
            self.lexemes.get('dialog_prompt_input_placeholder_text'))
        self.prompt_input.setAccessibleDescription(
            self.lexemes.get('dialog_prompt_input_accessible_description'))
        self.prompt_input.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.prompt_input)

        label_size = QSize(48, 48)
        label_pixmap = QPixmap(self.theme_helper.get_icon(theme_icon='clock-fill.svg').pixmap(label_size))
        # Use custom Pixmap class to assure the transformation (rotation)
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

        model_label = QLabel(text=self.lexemes.get('dialog_usage_module_label'))
        model_label.setObjectName("ai_assistant_dialog_usage_module_name_label")
        model_label.setFont(self.font())
        model_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        model_label.sizeHint()
        model_label.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        # model_label.setStyleSheet("QLabel {color: grey;}")
        status_bar_layout.addWidget(model_label)

        status_bar_layout.addWidget(VerticalLineSpacer())

        self.module_name_label = QLabel(self.inference_module_name)
        self.module_name_label.setFont(self.font())
        self.module_name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.module_name_label.sizeHint()
        self.module_name_label.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        self.module_name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        status_bar_layout.addWidget(self.module_name_label)

        self.model_name_label = QLabel()  # Text will be updated later
        self.model_name_label.setObjectName("ai_assistant_dialog_usage_model_name_label")
        self.model_name_label.setFont(self.font())
        self.model_name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.model_name_label.sizeHint()
        self.model_name_label.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        self.model_name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        status_bar_layout.addWidget(self.model_name_label)

        central_spacer = QWidget()
        central_spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        status_bar_layout.addWidget(central_spacer)

        tokens_label = QLabel(text=self.lexemes.get('dialog_usage_tokens_label'))
        tokens_label.setFont(self.font())
        tokens_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        tokens_label.sizeHint()
        tokens_label.setObjectName("ai_assistant_dialog_usage_tokens_label")
        # tokens_label.setStyleSheet("QLabel {color: grey;}")
        status_bar_layout.addWidget(tokens_label)
        status_bar_layout.addWidget(VerticalLineSpacer(), alignment=Qt.AlignmentFlag.AlignRight)
        self.tokens_prompt_label = QLabel()
        self.tokens_prompt_label.setFont(self.font())
        self.tokens_prompt_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.tokens_prompt_label.sizeHint()
        status_bar_layout.addWidget(self.tokens_prompt_label)
        status_bar_layout.addWidget(VerticalLineSpacer(), alignment=Qt.AlignmentFlag.AlignRight)
        self.tokens_answer_label = QLabel()
        self.tokens_answer_label.setFont(self.font())
        self.tokens_answer_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.tokens_answer_label.sizeHint()
        status_bar_layout.addWidget(self.tokens_answer_label)
        status_bar_layout.addWidget(VerticalLineSpacer(), alignment=Qt.AlignmentFlag.AlignRight)
        self.tokens_total_label = QLabel()
        self.tokens_total_label.setFont(self.font())
        self.tokens_total_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.tokens_total_label.sizeHint()
        status_bar_layout.addWidget(self.tokens_total_label)

        self.layout.addWidget(status_bar_widget)
        # Update usage with initial params
        self.update_usage('')

        buttons_layout = QHBoxLayout()
        buttons_widget = QWidget()
        buttons_widget.setLayout(buttons_layout)

        # Save button
        self.save_history_button = QPushButton()
        self.save_history_button.setFont(self.font())
        self.save_history_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.save_history_button.setIcon(self.theme_helper.get_icon(theme_icon='floppy2.svg'))
        self.save_history_button.clicked.connect(self.save_history_action)
        self.save_history_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_history_button.setDisabled(True)
        self.save_history_button.setToolTip(self.lexemes.get('dialog_button_save_history'))
        buttons_layout.addWidget(self.save_history_button)

        # To fill the space between
        spacer_widget = QWidget()
        spacer_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        buttons_layout.addWidget(spacer_widget, 3)

        # Submit button
        self.send_button = QPushButton(self.lexemes.get('dialog_button_send_request'), self)
        self.send_button.setFont(self.font())
        self.send_button.setIcon(self.theme_helper.get_icon(theme_icon='play-fill.svg'))
        self.send_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.send_button.clicked.connect(self.send_request)
        buttons_layout.addWidget(self.send_button, 1)

        self.layout.addWidget(buttons_widget)

        # Set the main layout for the dialog
        self.setLayout(self.layout)

    def get_message_color(self, message_type: EnumMessageType, message_style: EnumMessageStyle) -> tuple:
        if message_style == EnumMessageStyle.INFO:
            color = self.theme_helper.get_color('ai_assistant_message_info_color', True)
            bg_color = self.theme_helper.get_color('ai_assistant_message_info_background_color', True)
        elif message_style == EnumMessageStyle.ERROR:
            color = self.theme_helper.get_color('ai_assistant_message_error_color', True)
            bg_color = self.theme_helper.get_color('ai_assistant_message_error_background_color', True)
        else:
            if message_type == EnumMessageType.USER_INPUT:
                color = self.theme_helper.get_color('ai_assistant_message_user_input_color', True)
                bg_color = self.theme_helper.get_color('ai_assistant_message_user_input_background_color', True)
            elif message_type == EnumMessageType.RESPONSE:
                color = self.theme_helper.get_color('ai_assistant_message_response_color', True)
                bg_color = self.theme_helper.get_color('ai_assistant_message_response_background_color', True)
            else:
                color = self.theme_helper.get_color('ai_assistant_message_default_color', True)
                bg_color = self.theme_helper.get_color('ai_assistant_message_default_background_color', True)
        return color, bg_color

    def add_message(self, message, request_msg_id=None, response_msg_id=None,
                    message_type: EnumMessageType = EnumMessageType.default(),
                    message_style: EnumMessageStyle = EnumMessageStyle.default()) -> int:
        # Message background color
        color, bg_color = self.get_message_color(message_type, message_style)

        if message_type == EnumMessageType.USER_INPUT:
            if request_msg_id is None:
                # Message id might not be set in case of a new message needed
                request_msg_id = self.gen_next_message_id()
            message_id = request_msg_id
        elif message_type == EnumMessageType.RESPONSE:
            if response_msg_id is None:
                # Message id might not be set in case of a new message needed
                response_msg_id = self.gen_next_message_id()
            message_id = response_msg_id
        else:
            # Default or info; new internal id
            message_id = self.gen_next_message_id()

        # Remove leading spaces if exist
        message_text = message.lstrip()

        message_label = AiMessageLabel(text=message_text, parent=self)
        message_label.setFont(self.font())
        message_label.setWordWrap(True)
        message_label.setObjectName(f'msg_{message_type}_{message_id}')
        message_label.setStyleSheet(""" QLabel {
            border-radius: 5px;
            margin: 5px 0;
            padding: 5px;
            color: %s;
            background-color: %s;
        } """ % (color, bg_color))

        palette = message_label.palette()
        palette.setColor(message_label.foregroundRole(), QColor(color))
        palette.setColor(message_label.backgroundRole(), QColor(bg_color))

        message_label.setPalette(palette)
        message_label.setAutoFillBackground(True)
        message_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.messages_layout.setAlignment(message_label, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        message_label.sizeHint()
        self.messages_layout.addWidget(message_label, alignment=Qt.AlignmentFlag.AlignBottom)
        # self.messages_layout.addSpacerItem(QSpacerItem(0, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        self.messages_area.verticalScrollBar().setValue(self.messages_area.verticalScrollBar().maximum())

        # Emit message added signal
        self.message_added.emit(message_text, request_msg_id, response_msg_id, message_type)

        # Unique message id
        return message_id

    def append_to_message(self, additional_text, request_msg_id=None, response_msg_id=None,
                          message_type: EnumMessageType = EnumMessageType.default(),
                          message_style: EnumMessageStyle = EnumMessageStyle.DEFAULT):
        last_message = None
        if response_msg_id:
            # Message with the same id
            last_message = self.findChild(QLabel, f'msg_{message_type}_{response_msg_id}')
        # Double check found object type
        if isinstance(last_message, QLabel):
            current_text = last_message.text()
            new_text = current_text + additional_text
            last_message.setText(new_text)
            last_message.adjustSize()
        else:
            self.add_message(additional_text, request_msg_id, response_msg_id, message_type, message_style)

        self.messages_area.verticalScrollBar().setValue(self.messages_area.verticalScrollBar().maximum())

    def gen_next_message_id(self) -> int:
        # Update with gaps to allow extra space in case of race condition
        self.message_id += 3
        self.message_ids.append(self.message_id)
        return self.message_id

    def get_prev_message_id(self) -> Union[int, None]:
        # Check if there are at least two items in the list
        if len(self.message_ids) > 1:
            # Return the second-to-last item
            return self.message_ids[-2]
        else:
            # Return None if there are not enough items
            return None

    def init_md(self) -> None:
        """
        Init Markdown object and set it to variable.
        """
        extensions = ['markdown.extensions.extra']
        # Init markdown object with the selected extensions
        self.md = markdown.Markdown(extensions=extensions)

    def convert_markdown_to_html(self, md_content: str) -> str:
        """
        Process Markdown syntax and convert it to html.
        """
        if not self.md:
            self.init_md()
        # Convert markdown to html
        html_content = self.md.convert(md_content)
        # Converted html data
        return html_content

    def update_usage(self, model, prompt_tokens=None, response_tokens=None, total_tokens=None, append=False):
        if not append:
            # Count token usage
            self.token_usage = {model: {'prompt_tokens': 0, 'response_tokens': 0, 'total_tokens': 0}}
        # Update model from response
        if hasattr(self, 'model_name_label'):
            self.model_name_label.setText(model if len(model) > 0 else '')
        # Tokens spent in user's prompt
        prompt_tokens_cnt = prompt_tokens if prompt_tokens else 0
        if append:
            prompt_tokens_cnt += self.token_usage[model]['prompt_tokens']
        self.token_usage[model]['prompt_tokens'] = prompt_tokens_cnt
        if hasattr(self, 'tokens_prompt_label'):
            self.tokens_prompt_label.setText(self.lexemes.get('dialog_usage_tokens_prompt',
                                                              tokens=prompt_tokens_cnt))
        # Tokens spent in response
        response_tokens_cnt = response_tokens if response_tokens else 0
        if append:
            response_tokens_cnt += self.token_usage[model]['response_tokens']
        self.token_usage[model]['response_tokens'] = response_tokens_cnt
        if hasattr(self, 'tokens_answer_label'):
            self.tokens_answer_label.setText(self.lexemes.get('dialog_usage_tokens_answer',
                                                              tokens=response_tokens_cnt))
        # Total tokens spent (combined)
        total_tokens_cnt = total_tokens if total_tokens else 0
        if append:
            total_tokens_cnt += self.token_usage[model]['total_tokens']
        self.token_usage[model]['total_tokens'] = total_tokens_cnt
        if hasattr(self, 'tokens_total_label'):
            self.tokens_total_label.setText(self.lexemes.get('dialog_usage_tokens_total',
                                                             tokens=total_tokens_cnt))

    def init_module(self) -> Union[BaseAiCore, None]:
        self.module = Modules().import_module(self.inference_module)
        if not self.module:
            return None
        if self.module_core:
            return self.module_core
        try:
            # Create an instance of the inference module
            self.module_core = Modules().create(self.module)
            # Connect dialog first before posting any messages to allow correct stream processing
            self.module_core.attach_dialog(self)  # type: ignore
            # Return module core instance
            return self.module_core
        except (RuntimeError, Exception) as e:
            if self.logging:
                self.logger.warning(f'Error occurred during module {self.inference_module} init {e}')
        return None

    def send_request(self) -> None:
        # Check previous request id
        if self.request_message_id and self.request_message_id == self.message_id:
            if self.logging:
                self.logger.warning(
                    f"Duplicate request message id {self.request_message_id}")
            return

        # Get context for the prompt
        prompt_context = self.prompt_input.text()
        if len(prompt_context) == 0:
            self.add_message(self.lexemes.get('dialog_response_output_notice_empty_text'), None, None,
                             EnumMessageType.DEFAULT, EnumMessageStyle.INFO)
            return
        # Do not show placeholder text after first input for user convenience
        self.prompt_input.setPlaceholderText('')

        try:
            # Get an instance of the inference module
            module_core = self.init_module()
            # Get a prompt manager
            prompt_manager = module_core.get_prompt_manager()
            # Add request message first to allow it to appear within prompt history
            self.request_message_id = self.add_message(prompt_context, None, None,
                                                       EnumMessageType.USER_INPUT)
            # Either a multi-turn or stateless prompt
            user_prompt = prompt_manager.get_prompt(multi_turn=self.settings.ai_config_multi_turn_dialogue)
            if self.debug:
                self.logger.debug(f'The prompt:\n{user_prompt}\n')
            self.set_status_waiting()  # Pending status
            # Obtain new message id
            response_msg_id = self.gen_next_message_id()
            # Assume the previous message was a request
            check_request_msg_id = self.get_prev_message_id()
            if self.request_message_id != check_request_msg_id:
                if self.logging:
                    self.logger.warning(
                        f"Request message id doesn't match: {self.request_message_id} vs {check_request_msg_id}")
            module_core.request(
                user_prompt=user_prompt,
                request_msg_id=self.request_message_id,
                response_msg_id=response_msg_id,
                init_callback=self.set_status_processing,  # Processing status
                finished_callback=self.send_request_finished_callback)  # Finished status
        except (AttributeError, ValueError) as e:
            if self.logging:
                self.logger.warning(f'Error occurred during the request: {e}')
            # Set up response status visible within response field
            self.add_message(self.lexemes.get('dialog_error_loading_model'), None, None,
                             EnumMessageType.DEFAULT, EnumMessageStyle.ERROR)
            self.cancel_request()
            self.set_status_ready()
        except (RuntimeError, Exception) as e:
            if self.logging:
                self.logger.error(f'Error occurred during the request: {e}')
            self.cancel_request()
            self.set_status_ready()

    def send_request_finished_callback(self, request_msg_id=None, response_msg_id=None,
                                       message_type=EnumMessageType.RESPONSE):
        # Objects might be deleted
        try:
            # Return ready status
            self.set_status_ready()
            # Find the target message
            finished_msg = None
            if response_msg_id:
                # Message (response) with the same id
                finished_msg = self.findChild(QLabel, f'msg_{message_type}_{response_msg_id}')
            # Double check found object type
            if isinstance(finished_msg, QLabel):
                plain_text = finished_msg.text()
                # Check if postprocessing is needed
                if self.settings.ai_config_convert_to_md:
                    # Convert markdown response
                    md_text = self.convert_markdown_to_html(plain_text)
                    finished_msg.setText(md_text)
                # Emit message added signal to update final variant of the message (might not be completed yet)
                self.message_added.emit(plain_text, request_msg_id, response_msg_id, EnumMessageType.RESPONSE)
        except RuntimeError as e:  # Object is already deleted
            if self.logging:
                self.logger.warning(f'Finished event callback interrupted, probably an object already deleted {e}')

    def set_status_waiting(self):
        # Set loader cursor whilst loading content
        self.setCursor(Qt.CursorShape.WaitCursor)
        # Disable prompt input field
        self.prompt_input.setDisabled(True)
        # Clear prompt field as it have to be in the chat already
        self.prompt_input.clear()
        # Disable send request button
        self.send_button.setDisabled(True)
        # Disable save button
        self.save_history_button.setDisabled(True)
        # Show progress label
        self.background_label.show()

    def set_status_processing(self):
        try:
            # Set cursor back
            self.setCursor(Qt.CursorShape.ArrowCursor)
            # Hide progress label
            self.background_label.hide()
            # Replace with stop button
            self.request_button_stop()
            # Enable send request button
            self.send_button.setEnabled(True)
        except RuntimeError:
            raise

    def set_status_ready(self):
        try:
            # Set cursor back
            self.setCursor(Qt.CursorShape.ArrowCursor)
            # Enable prompt input field
            self.prompt_input.setEnabled(True)
            self.prompt_input.setFocus()
            # Return request button
            self.request_button_on()
            # Enable save button
            self.save_history_button.setEnabled(True)
            # Hide progress label
            self.background_label.hide()
        except RuntimeError:
            raise

    def request_button_on(self):
        # Sen request button
        self.send_button.clicked.disconnect()
        self.send_button.setText(self.lexemes.get('dialog_button_send_request'))
        self.send_button.setIcon(self.theme_helper.get_icon(theme_icon='play-fill.svg'))
        self.send_button.clicked.connect(self.send_request)

    def request_button_stop(self):
        # Stop request button
        self.send_button.clicked.disconnect()
        self.send_button.setText(self.lexemes.get('dialog_button_stop_request'))
        self.send_button.setIcon(self.theme_helper.get_icon(theme_icon='stop-fill.svg'))
        self.send_button.clicked.connect(self.cancel_request)

    def cancel_request(self):
        self.request_cancelled.emit()

    def save_history_action(self):
        if not hasattr(self.parent, 'action_new_file'):
            if self.logging:
                self.logger.error("Cannot save history to the file, no method available")
            return

        # Get an instance of the inference module
        module_core = self.init_module()
        # Get a prompt manager
        prompt_manager = module_core.get_prompt_manager()
        # Get history
        history = prompt_manager.get_history()

        # Get current date and time
        current_datetime = datetime.now()
        # Format the date and time in the specified format
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        # Add header
        history = (self.lexemes.get('dialog_prompt_history_file_header', datetime=formatted_datetime)
                   + f'\n\n{history}')

        # Save history
        self.parent.action_new_file(history)  # noqa

        # Disable save button until next update
        self.save_history_button.setDisabled(True)

    @asyncClose
    async def closeEvent(self, event):
        if self.logging:
            self.logger.info('Closing AI Assistant')
        self.dialog_closed.emit()
        self.deleteLater()
        # event.accept()  # Event handled
        super().closeEvent(event)  # Ensure the dialog and base object are closed properly

    def settings_update_handler(self, data) -> None:
        """
        Perform actions upon settings change.
        Data comes in a view of a dictionary, where is the key is the setting name, and the value is the actual value.
        Can be resource greedy.

        Args:
            data dict: say {"settings_key": "..."}

        Return:
            None
        """

        if self.debug:
            self.logger.debug('Settings update handler is in use "%s"' % data)

        if 'module_ondevice_llm_model_path' in data or 'ai_config_inference_module' in data:
            try:
                if hasattr(self, 'model_name_label'):
                    # Update model name (any updates in settings)
                    self.model_name_label.setText('')
            except RuntimeError:
                # Object can be deleted already
                pass
