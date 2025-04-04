"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Part of the 'OpenAI API' module.
- Functionality: Enables model inference using supported APIs.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2025 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QLineEdit, QSizePolicy, QPlainTextEdit, QSpinBox, QSlider
from PySide6.QtWidgets import QScrollArea
from PySide6.QtNetwork import QNetworkRequest, QNetworkAccessManager, QNetworkReply

import os
import json
import logging

import asyncio
from asyncio import Task
from qasync import asyncSlot

from typing import TYPE_CHECKING, Callable

from .api_helper import ApiHelper
from .prompt_manager import PromptManager

from ..base_ai_core import BaseAiCore

from .. import Settings
from .. import AppConfig
from .. import Lexemes

from ...enums.openai_model_names import OpenAiModelNames
from ...ui.enum_combo_box import EnumComboBox
from ...ui.ai_assistant.ai_assistant import EnumMessageType, EnumMessageStyle
from ...ui.horizontal_line_spacer import HorizontalLineSpacer
from ...ui.label_with_hint import LabelWithHint

if TYPE_CHECKING:
    from PySide6.QtCore import QByteArray  # noqa


class ModuleCore(BaseAiCore):
    update_signal = Signal(str, object, object, EnumMessageType, EnumMessageStyle)
    # prompt_tokens, completion_tokens, total_tokens
    update_usage_signal = Signal(str, object, object, object, object)

    # Default name, use lexeme for the translated one
    module_name = 'OpenAI API'

    # Functionality extended by the module.
    extensions = ['ai_assistant', 'settings_dialog']

    init_callback: Callable = None
    finished_callback: Callable = None

    generator_task: Task = None

    prompt_manager: PromptManager = None

    parent: None

    def __init__(self):
        super(ModuleCore, self).__init__()

        self.settings = Settings(parent=self)
        self.settings.value_changed.connect(
            lambda v: self.settings_update_handler(v))

        self.logger = logging.getLogger('module_openai_api')

        # Load lexemes for the selected language and scope
        self.lexemes = Lexemes(self.settings.app_language,
                               default_scope='settings_dialog',
                               lexemes_dir=self.get_lexemes_path())

        # Extend Settings explicitly as it's a global object which may cause circular recursion
        self.extend_settings_create_property(self.settings.create_property)
        # Add this module to the inference modules selection list
        inference_modules = self.settings.ai_config_inference_modules
        default_module = [key for key, value in inference_modules.items() if isinstance(value, tuple) and True in value]
        inference_modules.update({'openai_api': (self.lexemes.get('module_openai_api_name', scope='common'),
                                                 True if not default_module else False)})
        self.settings.ai_config_inference_modules = inference_modules

        # API requirements
        self.openai_api_url = self.settings.module_openai_api_url
        self.openai_api_key = self.settings.module_openai_api_key
        self.openai_api_model = OpenAiModelNames.__getitem__(self.settings.module_openai_api_model).value

        # Additional request params
        self.response_temperature = self.settings.module_openai_api_base_response_temperature
        self.response_max_tokens = self.settings.module_openai_api_base_response_max_tokens

        # API helper
        self.api_helper = ApiHelper()

        # Just in case of debug of async events
        # asyncio.get_event_loop().set_debug(True)

        self.logger.debug(f'Module {__name__} loaded')

    def init_prompt_manager(self, ai_dialog):
        """
        Prompt manager for prompt management and to add / append messages to prompt history.
        Note: It may not be initiated if called out of the context, from settings for example.
        """
        self.prompt_manager = PromptManager(
            system_prompt=self.settings.module_openai_api_base_system_prompt,
            max_history_size=self.settings.module_openai_api_prompt_history_size,
            parent=ai_dialog)

    def get_prompt_manager(self):
        return self.prompt_manager

    @staticmethod
    def get_lexemes_path():
        return os.path.join(os.path.dirname(__file__), 'lexemes')

    def attach_dialog(self, ai_dialog):
        # Catch parent dialog closing event
        ai_dialog.dialog_closed.connect(self.parent_closed)
        # Request cancelled event
        ai_dialog.request_cancelled.connect(self.request_cancelled)
        # Connect update signal to the dialog
        self.update_signal.connect(ai_dialog.append_to_message)
        # Connect to the token usage update signal
        self.update_usage_signal.connect(ai_dialog.update_usage)
        # Init and connect prompt manager
        self.init_prompt_manager(ai_dialog)

    @asyncSlot()
    async def parent_closed(self):
        ai_dialog = self.sender()
        # try/except because of an object might be deleted during processing callbacks asynchronously.
        # Explicitly check everything is disconnected.
        try:
            if ai_dialog:
                # Disconnect from the messages updating signal
                self.update_signal.disconnect(ai_dialog.append_to_message)
                # Disconnect from the token usage update signal
                self.update_usage_signal.disconnect(ai_dialog.update_usage)
                if hasattr(ai_dialog, 'dialog_closed'):
                    # Parent window might be closed
                    ai_dialog.dialog_closed.disconnect(self.parent_closed)
        except RuntimeError as e:  # Object might be already deleted
            self.logger.warning(f'Error occurred during the closing process {e}')
        # Clear prompt history
        PromptManager.reload()
        # Stop the generator thread before the dialog closes
        await self.stop_generator()

    @asyncSlot()
    async def request_cancelled(self):
        # Stop the generator thread before the dialog closes
        await self.stop_generator()

    @asyncSlot()
    async def request(self, user_prompt: str, request_msg_id: int, response_msg_id: int,
                      init_callback: Callable = None, finished_callback: Callable = None):

        if not asyncio.get_running_loop().is_running():
            return

        # Check the prompt manager is activated
        if not hasattr(self, 'prompt_manager') or self.prompt_manager is None:
            return

        # Store callbacks
        self.init_callback = init_callback
        self.finished_callback = finished_callback

        if not self.generator_task or self.generator_task.done():
            # self.generator_task = await asyncio.create_task(
            #    self.run_generator(user_prompt, request_msg_id, response_msg_id))
            self.generator_task = asyncio.ensure_future(
                self.run_generator(user_prompt, request_msg_id, response_msg_id))
            # Finished callback
            # This part will be completed in the handle_response() method after the async network reply.
            # if self.finished_callback and callable(self.finished_callback):
            #    self.generator_task.add_done_callback(
            #        lambda _task, _request_msg_id=request_msg_id, _response_msg_id=response_msg_id:
            #        self.finished_callback(request_msg_id=_request_msg_id, response_msg_id=_response_msg_id,
            #                               message_type=EnumMessageType.RESPONSE))
            # Run task asynchronously
            done, pending = await asyncio.wait([self.generator_task], return_when=asyncio.FIRST_COMPLETED)

            for task in done:
                if not task.cancelled():
                    exception = task.exception()
                    if exception:
                        self.logger.warning(f"Task raised an exception: {exception}")
                        # Error message to show in UI
                        outputs = self.lexemes.get('module_openai_api_task_exception', scope='common')
                        # Emit update message signal
                        self.update_signal.emit(outputs, None, None, EnumMessageType.DEFAULT,
                                                EnumMessageStyle.ERROR)
                    else:
                        result = task.result()
                        self.logger.debug(f"Task completed with result: {result}")

    async def run_generator(self, user_prompt, request_msg_id, response_msg_id):
        """
        Other params:
            "temperature": 0.2, "top_p": 1, "n": 1, "stream": False, ...
        """
        temperature_float = self.api_helper.convert_temperature(self.response_temperature)
        options = {'temperature': temperature_float}
        if self.response_max_tokens > 0:
            options.update({'max_tokens': self.response_max_tokens})
        # Request
        request = self.api_helper.init_request(api_url=self.openai_api_url, api_key=self.openai_api_key)
        # Request data
        request_data = self.api_helper.init_request_params(
            prompt_messages=user_prompt, api_model=self.openai_api_model, options=options)

        # Set request data
        manager = QNetworkAccessManager(self)
        reply = manager.post(request, request_data)

        # Connect finished signal
        reply.finished.connect(
            lambda _reply=reply: self.handle_response(_reply, request_msg_id, response_msg_id))
        # Connect error signal
        reply.errorOccurred.connect(
            lambda error, _reply=reply: self.handle_response(_reply, request_msg_id, response_msg_id, error))

    def handle_response(self, reply: QNetworkReply, request_msg_id, response_msg_id, error_code=None):
        # Get received status code, say 200
        status_code = reply.attribute(QNetworkRequest.Attribute.HttpStatusCodeAttribute)

        self.logger.debug(f'API response: {reply}, {error_code}, {status_code}')

        # Make sure there is no error
        if reply.error() == QNetworkReply.NetworkError.NoError:
            result_message = self.process_response(reply, request_msg_id, response_msg_id, status_code)
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
        # elif reply.error() == QNetworkReply.NetworkError.AuthenticationRequiredError:
        #    result_message = reply.errorString()
        else:
            # Handle other errors
            result_message = self.lexemes.get('network_connection_error_generic_with_status_code', scope='common',
                                              status_code=status_code)

        if error_code is not None:
            self.logger.warning(result_message)
            self.logger.warning(f"Failed to fetch information [{status_code}]: {reply.errorString()}")
            # Emit update message signal
            self.update_signal.emit(result_message if result_message else '[%s] %s' % (status_code, reply.errorString()),
                                    None, None, EnumMessageType.DEFAULT, EnumMessageStyle.ERROR)

        # Call API initialized callback here to update waiting status
        if self.init_callback and callable(self.init_callback):
            self.init_callback()

        # Call finished callback
        if self.finished_callback and callable(self.finished_callback):
            self.finished_callback(request_msg_id=request_msg_id, response_msg_id=response_msg_id,
                                   message_type=EnumMessageType.RESPONSE)

        reply.finished.disconnect()
        reply.errorOccurred.disconnect()
        reply.deleteLater()  # Clean up the QNetworkReply object

    def process_response(self, reply: QNetworkReply, request_msg_id, response_msg_id, status_code) -> str:
        # The request was successful
        data = reply.readAll()  # type: QByteArray

        self.logger.debug(f'Raw RESPONSE [{status_code}]: {data}')

        # json_document = QJsonDocument.fromJson(data)
        # json_data = json_document.object()

        # Convert QByteArray to string
        res_string = data.toStdString()  # Or: str(data.data(), encoding='utf-8')
        self.logger.debug(f'Result multi-line STRING: {res_string}')

        # Clean up the string and make one line
        json_str = ''.join(line.strip() for line in res_string.splitlines())

        self.logger.debug(f'Result STRING: {json_str}')

        result_message = self.lexemes.get('network_connection_error_empty', scope='common')
        # Parse JSON response
        try:
            json_data = json.loads(json_str)
            self.logger.debug(f"Result JSON: {json_data}")
            if ('choices' in json_data
                    and len(json_data['choices']) > 0
                    # Legacy completions
                    # and 'text' in json_data['choices'][0]):
                    and 'message' in json_data['choices'][0]
                    and 'content' in json_data['choices'][0]['message']):
                # Legacy completions
                # outputs = str(json_data['choices'][0]['text']).strip()
                outputs = str(json_data['choices'][0]['message']['content']).strip()
                # Emit update message signal
                self.update_signal.emit(outputs, request_msg_id, response_msg_id,
                                        EnumMessageType.RESPONSE, EnumMessageStyle.DEFAULT)
            if 'usage' in json_data:
                prompt_tokens, response_tokens, total_tokens = 0, 0, 0
                try:
                    # Ensure that all expected keys are present
                    keys = ('prompt_tokens', 'completion_tokens', 'total_tokens')
                    prompt_tokens, response_tokens, total_tokens = (json_data['usage'][key] for key in keys)
                except KeyError as e:
                    self.logger.warning(f"Missing key: {e}")
                except ValueError as e:
                    self.logger.warning(f"Value error: {e}")
                finally:
                    # Inference model
                    model = json_data['model'] if 'model' in json_data else None
                    # Emit update usage signal
                    self.update_usage_signal.emit(model, prompt_tokens, response_tokens, total_tokens, False)
        except json.JSONDecodeError as e:
            self.logger.warning("Error decoding JSON: %s" % e)

        return result_message

    async def stop_generator(self):
        # Cancel async task(s)
        if self.generator_task and not self.generator_task.done():
            # Allow to finish callback, do not remove:
            # > self.generator_task.remove_done_callback(self.finished_callback)
            self.generator_task.cancel()

    def extend_settings_dialog_fields_conf(self, tab_widget) -> list:
        # OpenAI API Config
        tab_openai_api_config = QWidget()

        # Create the scroll area
        scroll_area = QScrollArea()
        scroll_area.setObjectName('settings_dialog_tab_openai_api_config')
        scroll_area.setWidgetResizable(True)

        # Define the layout for the  OpenAI API configuration tab
        tab_openai_api_config_layout = QVBoxLayout(tab_openai_api_config)

        # Set the content widget inside the scroll area
        scroll_area.setWidget(tab_openai_api_config)

        tab_widget.addTab(scroll_area, self.lexemes.get('tab_openai_api_config'))

        return [
            # [OpenAI API config]
            # Label for the OpenAI API configuration block
            {"type": QLabel, "name": "settings_dialog_module_openai_api_label",
             "props": {"setProperty": ("class", "group-header-label")},
             "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('module_openai_api_label'), "style": {"bold": True},
             "callback": lambda obj: tab_openai_api_config_layout.addWidget(obj)},
            # OpenAI API url label
            {"type": LabelWithHint, "kwargs": {
                "tooltip": ('module_openai_api_url_input_accessible_description',
                            self.lexemes.get('module_openai_api_url_input_accessible_description'))},
             "name": "settings_dialog_module_openai_api_url_label",
             "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('module_openai_api_url_label'),
             "callback": lambda obj: tab_openai_api_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop)},
            # OpenAI API url line input
            {"type": QLineEdit, "name": "settings_dialog_module_openai_api_url_input:module_openai_api_url",
             "read_only": False, "max_length": 2048,
             "callback": lambda obj: tab_openai_api_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop),
             "placeholder_text": self.lexemes.get('module_openai_api_url_input_placeholder_text'),
             "accessible_description":
                 self.lexemes.get('module_openai_api_url_input_accessible_description')},
            # OpenAI API url label
            {"type": LabelWithHint, "kwargs": {"tooltip": ('module_openai_api_key_input_accessible_description',
                                               self.lexemes.get('module_openai_api_key_input_accessible_description'))},
             "name": "settings_dialog_module_openai_api_key_label",
             "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('module_openai_api_key_label'),
             "callback": lambda obj: tab_openai_api_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop)},
            # OpenAI API key line input
            {"type": QLineEdit, "name": "settings_dialog_module_openai_api_key_input:module_openai_api_key",
             "read_only": False, "max_length": 2048, "props": {"setEchoMode": QLineEdit.EchoMode.Password},
             "callback": lambda obj: tab_openai_api_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop),
             "placeholder_text": self.lexemes.get('module_openai_api_key_input_placeholder_text'),
             "accessible_description":
                 self.lexemes.get('module_openai_api_key_input_accessible_description')},
            # Vertical spacer
            {"type": QWidget, "name": None, "size_policy": (QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum),
             "callback": lambda obj: tab_openai_api_config_layout.addWidget(obj)},
            # Label for supported chat formats
            {"type": LabelWithHint, "kwargs": {
                "tooltip": ('module_openai_api_model_names_combo_accessible_description',
                            self.lexemes.get('module_openai_api_model_names_combo_accessible_description'))},
             "name": "settings_dialog_module_openai_api_supported_models_label",
             "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('module_openai_api_supported_models_label'),
             "callback": lambda obj: tab_openai_api_config_layout.addWidget(obj)},
            # Dropdown for selecting a supported chat format
            {"type": EnumComboBox, "args": [sorted(OpenAiModelNames, key=lambda member: member.legacy)],  # legacy below
             "name": "settings_dialog_module_openai_api_model_names_combo:module_openai_api_model",
             "callback": lambda obj: tab_openai_api_config_layout.addWidget(obj),
             "placeholder_text": self.lexemes.get('module_openai_api_model_names_combo_placeholder_text'),
             "accessible_description":
                 self.lexemes.get('module_openai_api_model_names_combo_accessible_description')},
            # Horizontal spacer
            {"type": HorizontalLineSpacer, "callback": lambda obj: tab_openai_api_config_layout.addWidget(obj)},
            # Label for the system prompt text editor
            {"type": LabelWithHint, "kwargs": {
                "tooltip": ('module_openai_api_base_system_prompt_edit_accessible_description',
                            self.lexemes.get('module_openai_api_base_system_prompt_edit_accessible_description'))},
             "name": "settings_dialog_module_openai_api_base_system_prompt_label",
             "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('module_openai_api_base_system_prompt_label'),
             "callback": lambda obj: tab_openai_api_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop)},
            # Text editor field for the system prompt
            {"type": QPlainTextEdit,
             "name": "settings_dialog_module_openai_api_base_system_prompt_edit:"
                     "module_openai_api_base_system_prompt",
             "callback": lambda obj: tab_openai_api_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop),
             "placeholder_text": self.lexemes.get('module_openai_api_base_system_prompt_edit_placeholder_text'),
             "accessible_description":
                 self.lexemes.get('module_openai_api_base_system_prompt_edit_accessible_description'), "text_lines": 7},
            # Vertical spacer
            {"type": QWidget, "name": None, "size_policy": (QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum),
             "callback": lambda obj: tab_openai_api_config_layout.addWidget(obj)},
            # Label for the temperature slider
            {"type": LabelWithHint, "kwargs": {
                "tooltip": ('module_openai_api_base_response_temperature_input_accessible_description',
                            self.lexemes.get('module_openai_api_base_response_temperature_input_accessible_description'))},
             "name": "settings_dialog_module_openai_api_base_response_temperature_label",
             "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('module_openai_api_base_response_temperature_label',
                                      temperature=self.settings.module_openai_api_base_response_temperature),
             "callback": lambda obj: tab_openai_api_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop)},
            # Slider to adjust the temperature setting
            {"type": QSlider, "args": [Qt.Orientation.Horizontal],
             "props": {'setFocusPolicy': Qt.FocusPolicy.StrongFocus, 'setTickPosition': QSlider.TickPosition.TicksAbove,
                       'setTickInterval': 5, 'setSingleStep': 5, 'setMinimum': 0, 'setMaximum': 100},
             "name": "settings_dialog_module_openai_api_base_response_temperature:"
                     "module_openai_api_base_response_temperature",  # Lexeme key : Setting name
             "callback": lambda obj: tab_openai_api_config_layout.addWidget(obj),
             "on_value_change": self.temperature_change_handler,
             "accessible_description":
                 self.lexemes.get('module_openai_api_base_response_temperature_input_accessible_description')},
            # Vertical spacer
            {"type": QWidget, "name": None, "size_policy": (QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum),
             "callback": lambda obj: tab_openai_api_config_layout.addWidget(obj)},
            # Label for the maximum token count setting
            {"type": LabelWithHint, "kwargs": {
                "tooltip": ('module_openai_api_base_response_max_tokens_input_accessible_description',
                            self.lexemes.get('module_openai_api_base_response_max_tokens_input_accessible_description'))},
             "name": "settings_dialog_module_openai_api_base_response_max_tokens_label",
             "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('module_openai_api_base_response_max_tokens_label'),
             "callback": lambda obj: tab_openai_api_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop)},
            # Input field for the maximum token count setting
            {"type": QSpinBox, "props": {'setMinimum': 0, 'setMaximum': 65536},  # Update the highest range
             "size_policy": (QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred),
             "name": "settings_dialog_module_openai_api_base_response_max_tokens:"
                     "module_openai_api_base_response_max_tokens",
             "callback": lambda obj: tab_openai_api_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop),
             "accessible_description":
                 self.lexemes.get('module_openai_api_base_response_max_tokens_input_accessible_description')},
            # Horizontal line spacer
            {"type": HorizontalLineSpacer, "callback": lambda obj: tab_openai_api_config_layout.addWidget(obj)},
            # Label for the prompt history maximum capacity settings
            {"type": LabelWithHint, "kwargs": {
                "tooltip": ('module_openai_api_config_prompt_history_size_input_accessible_description',
                            self.lexemes.get('module_openai_api_config_prompt_history_size_input_accessible_description'))},
             "name": "settings_dialog_module_openai_api_config_prompt_history_size_label",
             "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('module_openai_api_config_prompt_history_size_label'),
             "callback": lambda obj: tab_openai_api_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop)},
            # Input field for the prompt history maximum capacity setting
            {"type": QSpinBox, "props": {'setMinimum': 0, 'setMaximum': 65536},  # Update the highest range
             "size_policy": (QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred),
             "name": "settings_dialog_module_openai_api_config_prompt_history_size:"
                     "module_openai_api_prompt_history_size",
             "callback": lambda obj: tab_openai_api_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop),
             "accessible_description":
                 self.lexemes.get('module_openai_api_config_prompt_history_size_input_accessible_description')},
            # Spacer to align elements at the top of the layout
            {"type": QWidget, "name": None, "size_policy": (QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding),
             "callback": lambda obj: tab_openai_api_config_layout.addWidget(obj)},
        ]

    @staticmethod
    def extend_settings_create_property(extend_func: Callable):
        if callable(extend_func):
            extend_func("module_openai_api_url", str, "https://api.openai.com/v1/chat/completions")
            extend_func("module_openai_api_key", str, "", encrypt=True)
            extend_func("module_openai_api_model", str, str(OpenAiModelNames.default()))

            extend_func("module_openai_api_base_system_prompt", str, "")
            extend_func("module_openai_api_base_response_temperature", int, 20)
            extend_func("module_openai_api_base_response_max_tokens", int, 0)
            extend_func("module_openai_api_prompt_history_size", int, 0)

    def settings_update_handler(self, data) -> None:
        """
        Perform actions upon settings change.

        Data is provided as a dictionary, where the key represents the setting name, and the value is its corresponding value.
        Note: This operation updates UI elements and internal properties, which may be resource-intensive.

        Args:
            data dict: say {"module_openai_api_model": "..."}

        Return:
            None
        """

        AppConfig().logger.debug(f'Settings update handler is processing: {data}')

        options = [
            'module_openai_api_url',
            'module_openai_api_key',
            'module_openai_api_model',
            'module_openai_api_base_system_prompt',
            'module_openai_api_base_response_temperature',
            'module_openai_api_base_response_max_tokens',
        ]
        if any(option in data for option in options) or 'ai_config_inference_module' in data:
            pass

    def temperature_change_handler(self, source_object, source_widget):
        if source_object.objectName() and source_widget:
            # Parse the object name in case it contains a combination of lexeme and setting keys
            _lexeme_key, setting_name = self.settings.settings_helper.parse_object_name(source_object.objectName())
            if setting_name == 'module_openai_api_base_response_temperature':
                # Get the latest value from the object, as settings might not yet be updated
                temperature_int = source_object.value()  # source_object type: QSlider
                temperature_float = self.api_helper.convert_temperature(temperature_int)
                temperature_label = source_widget.findChild(
                    QLabel,
                    'settings_dialog_module_openai_api_base_response_temperature_label'
                )
                if temperature_label:
                    temperature_label.setText(
                        self.lexemes.get('module_openai_api_base_response_temperature_label',
                                         temperature=temperature_float))
