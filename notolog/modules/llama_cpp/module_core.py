"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Component of the 'Module llama.cpp' module.
- Functionality: Facilitates local inference for supported Large Language Models (LLMs)
                 in the GPT-Generated Unified Format (GGUF).

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2025 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QSpinBox, QSlider, QSizePolicy, QPlainTextEdit, QScrollArea

import os
import logging

import asyncio
from asyncio import Task
from qasync import asyncSlot

from typing import Callable

from .model_helper import ModelHelper
from .prompt_manager import PromptManager

from ..base_ai_core import BaseAiCore

from .. import Settings
from .. import AppConfig
from .. import Lexemes

from ...ui.ai_assistant.ai_assistant import EnumMessageType, EnumMessageStyle
from ...ui.file_path_line_edit import FilePathLineEdit
from ...ui.horizontal_line_spacer import HorizontalLineSpacer
from ...ui.enum_combo_box import EnumComboBox
from ...ui.label_with_hint import LabelWithHint

from ...enums.llm_chat_formats import LlmChatFormats


class ModuleCore(BaseAiCore):
    update_signal = Signal(str, object, object, EnumMessageType, EnumMessageStyle)
    # prompt_tokens, completion_tokens, total_tokens
    update_usage_signal = Signal(str, object, object, object, object)

    # Default name, use lexeme for the translated version
    module_name = 'Module llama.cpp'

    # Functionality extended by this module
    extensions = ['ai_assistant', 'settings_dialog']

    init_callback: Callable = None
    finished_callback: Callable = None

    generator_task: Task = None

    prompt_manager: PromptManager = None

    def __init__(self):
        super(ModuleCore, self).__init__()

        self.settings = Settings(parent=self)
        self.settings.value_changed.connect(
            lambda v: self.settings_update_handler(v))

        self.logger = logging.getLogger('module_llama_cpp')

        # Load lexemes for the selected language and scope
        self.lexemes = Lexemes(self.settings.app_language,
                               default_scope='settings_dialog',
                               lexemes_dir=self.get_lexemes_path())

        # Explicitly extend settings to avoid circular recursion due to its global nature
        self.extend_settings_create_property(self.settings.create_property)
        # Register this module in the inference modules selection list
        inference_modules = self.settings.ai_config_inference_modules
        default_module = [key for key, value in inference_modules.items() if isinstance(value, tuple) and True in value]
        inference_modules.update({'llama_cpp': (self.lexemes.get('module_llama_cpp_name', scope='common'),
                                                True if not default_module else False)})
        self.settings.ai_config_inference_modules = inference_modules

        model_path = self.settings.module_llama_cpp_model_path
        context_window = self.settings.module_llama_cpp_context_window
        chat_format = self.settings.module_llama_cpp_chat_format
        search_options = self.get_search_options()
        # Cached helper instance for efficiency
        self.model_helper = ModelHelper(model_path=model_path, n_ctx=context_window, chat_format=chat_format,
                                        search_options=search_options)

        # Use for debugging asynchronous events if necessary:
        # asyncio.get_event_loop().set_debug(True)

        self.logger.debug(f'Module {__name__} loaded')

    def get_search_options(self):
        search_options = {}
        if hasattr(self.settings, 'module_llama_cpp_response_temperature'):
            search_options.update({'temperature': self.settings.module_llama_cpp_response_temperature})
        if hasattr(self.settings, 'module_llama_cpp_response_max_tokens'):
            search_options.update({'max_tokens': self.settings.module_llama_cpp_response_max_tokens})
        return search_options

    def init_prompt_manager(self, ai_dialog):
        """
        Prompt manager handles prompt management and appends messages to the prompt history.
        Note: It may not be initiated if called out of context, such as from settings.
        """
        self.prompt_manager = PromptManager(system_prompt=self.settings.module_llama_cpp_system_prompt,
                                            max_history_size=self.settings.module_llama_cpp_prompt_history_size,
                                            parent=ai_dialog)

    def get_prompt_manager(self):
        return self.prompt_manager

    @staticmethod
    def get_lexemes_path():
        return os.path.join(os.path.dirname(__file__), 'lexemes')

    def attach_dialog(self, ai_dialog):
        # Catch parent dialog's closing event to handle cleanup
        ai_dialog.dialog_closed.connect(self.parent_closed)
        # Handle request cancelled events gracefully
        ai_dialog.request_cancelled.connect(self.request_cancelled)
        # Connect update signal to the dialog for real-time updates
        self.update_signal.connect(ai_dialog.append_to_message)
        # Connect to the token usage update signal for monitoring usage
        self.update_usage_signal.connect(ai_dialog.update_usage)
        # Initialize and connect the prompt manager
        self.init_prompt_manager(ai_dialog)

    @asyncSlot()
    async def parent_closed(self):
        ai_dialog = self.sender()
        # Use try/except to handle potential asynchronous deletions of objects during callback processing.
        # Explicitly check that all connections are disconnected to prevent memory leaks.
        try:
            if ai_dialog:
                # Disconnect from the messages updating signal
                self.update_signal.disconnect(ai_dialog.append_to_message)
                # Disconnect from the token usage update signal
                self.update_usage_signal.disconnect(ai_dialog.update_usage)
                if hasattr(ai_dialog, 'dialog_closed'):
                    # Ensure handling when the parent window might be closed
                    ai_dialog.dialog_closed.disconnect(self.parent_closed)
        except RuntimeError as e:  # Object might be already deleted
            self.logger.warning(f'Error occurred during the closing process {e}')
        # Clear the prompt history when no longer needed
        PromptManager.reload()
        # Stop the generator thread before closing the dialog to avoid crashes
        await self.stop_generator()

    @asyncSlot()
    async def request_cancelled(self):
        # Stop the generator thread before closing the dialog to avoid crashes
        await self.stop_generator()

    @asyncSlot()
    async def request(self, user_prompt: list, request_msg_id: int, response_msg_id: int,
                      init_callback: Callable = None, finished_callback: Callable = None):
        """
        Builds a request to the selected LLM functionality.

        Args:
            user_prompt (list): A list of dictionaries that form a chat history, managed by a prompt manager.
            request_msg_id (int): The ID of the request message.
            response_msg_id (int): The ID of the response message, which is the actual reply to the requested message.
            init_callback (Callable): The initialization callback that is triggered when the model is ready to start
                                      inferencing.
            finished_callback (Callable): The callback that is triggered upon completion of the inference.

        Returns:
            None
        """

        if not asyncio.get_running_loop().is_running():
            return

        # Verify that the prompt manager is activated before proceeding
        if not hasattr(self, 'prompt_manager') or self.prompt_manager is None:
            return

        # Store callbacks for later use or cleanup
        self.init_callback = init_callback
        self.finished_callback = finished_callback

        # Initialize the model
        try:
            self.model_helper.init_model()
        except (RuntimeError, ValueError, Exception) as e:
            self.logger.error(f'{e}')
            # Complete the initialization process
            if self.init_callback and callable(self.init_callback):
                self.init_callback()
            # Prepare error messages for display in the UI
            outputs = self.lexemes.get("module_llama_cpp_model_exception", scope='common', error_msg=str(e))
            # Emit update message signal
            self.update_signal.emit(outputs, None, None, EnumMessageType.DEFAULT, EnumMessageStyle.ERROR)
            # Emit finished signal
            self.finished_callback(request_msg_id=request_msg_id, response_msg_id=response_msg_id,
                                   message_type=EnumMessageType.RESPONSE)
            return

        user_prompt_str = self.prompt_manager.get_history()
        input_tokens = self.model_helper.get_input_tokens(user_prompt_str)

        # Emit update usage signal to reflect new token counts
        self.update_usage_signal.emit(self.get_model_name(), len(input_tokens), 0, len(input_tokens), False)

        if not self.generator_task or self.generator_task.done():
            # self.generator_task = await asyncio.create_task(self.run_generator(search_options, input_tokens))
            # Initialize generator task asynchronously with the configured prompt and message ids
            self.generator_task = asyncio.ensure_future(
                self.run_generator(user_prompt, request_msg_id, response_msg_id))
            # Handle the completion of tasks with the appropriate callback
            if self.finished_callback and callable(self.finished_callback):
                self.generator_task.add_done_callback(
                    lambda _task, _request_msg_id=request_msg_id, _response_msg_id=response_msg_id:
                    self.finished_callback(request_msg_id=_request_msg_id, response_msg_id=_response_msg_id,
                                           message_type=EnumMessageType.RESPONSE))
            # Run the task asynchronously
            done, pending = await asyncio.wait([self.generator_task], return_when=asyncio.FIRST_COMPLETED)

            for task in done:
                if not task.cancelled():
                    exception = task.exception()
                    if exception:
                        self.logger.warning(f"Task raised an exception: {exception}")
                        # Prepare error messages for UI display if exceptions occur
                        outputs = self.lexemes.get('module_llama_cpp_task_exception', scope='common',
                                                   error_msg=str(exception))
                        # Emit update message signal
                        self.update_signal.emit(outputs, None, None, EnumMessageType.DEFAULT, EnumMessageStyle.ERROR)
                    else:
                        result = task.result()
                        self.logger.debug(f"Task completed with result: {result}")

    async def run_generator(self, user_prompt, request_msg_id, response_msg_id):

        try:
            generator = self.model_helper.init_generator(user_prompt, ModelHelper.search_options)
        except ModuleNotFoundError as e:
            self.logger.error(f'Cannot init model generator: {e}', exc_info=False)
            # Re-raise exceptions to indicate unresolved issues to the caller
            raise
        finally:
            # Mark the end of the initialization stage
            if self.init_callback and callable(self.init_callback):
                self.init_callback()

        try:
            while not self.generator_task.done():
                await self.async_generator(generator, request_msg_id, response_msg_id)
                await asyncio.sleep(0.01)  # Sleep briefly to allow the UI to update
        except StopAsyncIteration:
            self.logger.debug("Async generation completed")
        except asyncio.CancelledError:
            self.logger.info("Generation cancelled")
        except RecursionError as e:
            self.logger.error(f"Error occurred: {e}")
        except (SystemExit, Exception) as e:
            self.logger.error(f"Exception raised: {e}")
        finally:  # Mark the end of the generation process
            await self.stop_generator()

    async def async_generator(self, generator, request_msg_id, response_msg_id):
        # Retrieve outputs for this iteration to process or display
        outputs = await self.model_helper.generate_output(generator)
        if len(outputs) > 0:  # there might be a space symbol
            # Emit update message signal
            self.update_signal.emit(outputs, request_msg_id, response_msg_id,
                                    EnumMessageType.RESPONSE, EnumMessageStyle.DEFAULT)
            # Emit update usage signal
            self.update_usage_signal.emit(self.get_model_name(), 0, 1, 1, True)  # One token at the moment

    async def stop_generator(self):
        # Cancel asynchronous tasks cleanly when necessary.
        if self.generator_task and not self.generator_task.done():
            # Ensure to finish callback execution; do not remove:
            # > self.generator_task.remove_done_callback(self.finished_callback)
            self.generator_task.cancel()

    def extend_settings_dialog_fields_conf(self, tab_widget) -> list:
        # Configuration settings for Module llama.cpp
        tab_module_llama_cpp_config = QWidget()

        # Create the scroll area
        scroll_area = QScrollArea()
        scroll_area.setObjectName('settings_dialog_tab_module_llama_cpp_config')
        scroll_area.setWidgetResizable(True)

        # Define the layout for the Module llama.cpp configuration tab
        tab_module_llama_cpp_config_layout = QVBoxLayout(tab_module_llama_cpp_config)

        # Set the content widget inside the scroll area
        scroll_area.setWidget(tab_module_llama_cpp_config)

        tab_widget.addTab(scroll_area, self.lexemes.get('tab_module_llama_cpp_config'))

        return [
            # [Module llama.cpp config]
            # Label for the configuration block
            {"type": QLabel, "name": "settings_dialog_module_llama_cpp_config_label",
             "props": {"setProperty": ("class", "group-header-label")},
             "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('module_llama_cpp_config_label'), "style": {"bold": True},
             "callback": lambda obj: tab_module_llama_cpp_config_layout.addWidget(obj)},
            # Label for the model path input field
            {"type": LabelWithHint, "kwargs": {
                "tooltip": ('module_llama_cpp_config_path_input_accessible_description',
                            self.lexemes.get('module_llama_cpp_config_path_input_accessible_description'))},
             "name": "settings_dialog_module_llama_cpp_config_path_label",
             "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('module_llama_cpp_config_path_label'),
             "callback": lambda obj: tab_module_llama_cpp_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop)},
            # Input field for the model path
            {"type": FilePathLineEdit, "kwargs": {"settings": self.settings, "ext_filter": "%s (*.gguf)" %
                                                  # The only GGUF files are now supported
                                                  self.lexemes.get('module_llama_cpp_config_path_input_filter_text')},
             "name": "settings_dialog_module_llama_cpp_config_path_input:module_llama_cpp_model_path",
             "read_only": False, "max_length": 2048,
             "callback": lambda obj: tab_module_llama_cpp_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop),
             "placeholder_text": self.lexemes.get('module_llama_cpp_config_path_input_placeholder_text'),
             "accessible_description":
                 self.lexemes.get('module_llama_cpp_config_path_input_accessible_description')},
            # Vertical spacer
            {"type": QWidget, "name": None, "size_policy": (QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum),
             "callback": lambda obj: tab_module_llama_cpp_config_layout.addWidget(obj)},
            # Label for the context window setting
            {"type": LabelWithHint, "kwargs": {
                "tooltip": ('module_llama_cpp_config_context_window_input_accessible_description',
                            self.lexemes.get('module_llama_cpp_config_context_window_input_accessible_description'))},
             "name": "settings_dialog_module_llama_cpp_config_context_window_label",
             "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('module_llama_cpp_config_context_window_label'),
             "callback": lambda obj: tab_module_llama_cpp_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop)},
            # Input field for the context window setting
            {"type": QSpinBox, "props": {'setMinimum': 1, 'setMaximum': 65536},  # Update the highest range
             "size_policy": (QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred),
             "name": "settings_dialog_module_llama_cpp_config_context_window:"
                     "module_llama_cpp_context_window",
             "callback": lambda obj: tab_module_llama_cpp_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop),
             "accessible_description":
                 self.lexemes.get('module_llama_cpp_config_context_window_input_accessible_description')},
            # Vertical spacer
            {"type": QWidget, "name": None, "size_policy": (QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum),
             "callback": lambda obj: tab_module_llama_cpp_config_layout.addWidget(obj)},
            # Label for supported chat formats
            {"type": LabelWithHint, "kwargs": {
                "tooltip": ('module_llama_cpp_config_chat_formats_combo_accessible_description',
                            self.lexemes.get('module_llama_cpp_config_chat_formats_combo_accessible_description'))},
             "name": "settings_dialog_module_llama_cpp_config_chat_formats_label",
             "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('module_llama_cpp_config_chat_formats_label'),
             "callback": lambda obj: tab_module_llama_cpp_config_layout.addWidget(obj)},
            # Dropdown for selecting a supported chat format
            {"type": EnumComboBox, "args": [sorted(LlmChatFormats, key=lambda member: member.is_default)],
             "name": "settings_dialog_module_llama_cpp_config_chat_formats_combo:"
                     "module_llama_cpp_chat_format",
             "callback": lambda obj: tab_module_llama_cpp_config_layout.addWidget(obj),
             "placeholder_text": self.lexemes.get('module_llama_cpp_config_chat_formats_combo_placeholder_text'),
             "accessible_description":
                 self.lexemes.get('module_llama_cpp_config_chat_formats_combo_accessible_description')},
            # Horizontal line spacer
            {"type": HorizontalLineSpacer, "callback": lambda obj: tab_module_llama_cpp_config_layout.addWidget(obj)},
            # Label for the system prompt text editor
            {"type": LabelWithHint, "kwargs": {
                "tooltip": ('module_llama_cpp_config_system_prompt_edit_accessible_description',
                            self.lexemes.get('module_llama_cpp_config_system_prompt_edit_accessible_description'))},
             "name": "settings_dialog_module_llama_cpp_config_system_prompt_label",
             "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('module_llama_cpp_config_system_prompt_label'),
             "callback": lambda obj: tab_module_llama_cpp_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop)},
            # Text editor field for the system prompt
            {"type": QPlainTextEdit,
             "name": "settings_dialog_module_llama_cpp_config_system_prompt_edit:"
                     "module_llama_cpp_system_prompt",
             "callback": lambda obj: tab_module_llama_cpp_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop),
             "placeholder_text": self.lexemes.get('module_llama_cpp_config_system_prompt_edit_placeholder_text'),
             "accessible_description":
                 self.lexemes.get('module_llama_cpp_config_system_prompt_edit_accessible_description'),
             "text_lines": 7},
            # Vertical spacer
            {"type": QWidget, "name": None, "size_policy": (QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum),
             "callback": lambda obj: tab_module_llama_cpp_config_layout.addWidget(obj)},
            # Label for the temperature slider
            {"type": LabelWithHint, "kwargs": {
                "tooltip": ('module_llama_cpp_config_response_temperature_input_accessible_description',
                            self.lexemes.get('module_llama_cpp_config_response_temperature_input_accessible_description'))},
             "name": "settings_dialog_module_llama_cpp_config_response_temperature_label",
             "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('module_llama_cpp_config_response_temperature_label',
                                      temperature=self.settings.module_llama_cpp_response_temperature),
             "callback": lambda obj: tab_module_llama_cpp_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop)},
            # Slider to adjust the temperature setting
            {"type": QSlider, "args": [Qt.Orientation.Horizontal],
             "props": {'setFocusPolicy': Qt.FocusPolicy.StrongFocus, 'setTickPosition': QSlider.TickPosition.TicksAbove,
                       'setTickInterval': 5, 'setSingleStep': 5, 'setMinimum': 0, 'setMaximum': 100},
             "name": "settings_dialog_module_llama_cpp_config_response_temperature:"
                     "module_llama_cpp_response_temperature",  # Lexeme key : Setting name
             "callback": lambda obj: tab_module_llama_cpp_config_layout.addWidget(obj),
             "on_value_change": self.temperature_change_handler,
             "accessible_description":
                 self.lexemes.get('module_llama_cpp_config_response_temperature_input_accessible_description')},
            # Vertical spacer
            {"type": QWidget, "name": None, "size_policy": (QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum),
             "callback": lambda obj: tab_module_llama_cpp_config_layout.addWidget(obj)},
            # Label for the maximum token count setting
            {"type": LabelWithHint, "kwargs": {
                "tooltip": ('module_llama_cpp_config_response_max_tokens_input_accessible_description',
                            self.lexemes.get('module_llama_cpp_config_response_max_tokens_input_accessible_description'))},
             "name": "settings_dialog_module_llama_cpp_config_response_max_tokens_label",
             "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('module_llama_cpp_config_response_max_tokens_label'),
             "callback": lambda obj: tab_module_llama_cpp_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop)},
            # Input field for the maximum token count setting
            {"type": QSpinBox, "props": {'setMinimum': 0, 'setMaximum': 65536},  # Update the highest range
             "size_policy": (QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred),
             "name": "settings_dialog_module_llama_cpp_config_response_max_tokens:"
                     "module_llama_cpp_response_max_tokens",
             "callback": lambda obj: tab_module_llama_cpp_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop),
             "accessible_description":
                 self.lexemes.get('module_llama_cpp_config_response_max_tokens_input_accessible_description')},
            # Horizontal line spacer
            {"type": HorizontalLineSpacer, "callback": lambda obj: tab_module_llama_cpp_config_layout.addWidget(obj)},
            # Label for the prompt history maximum capacity settings
            {"type": LabelWithHint, "kwargs": {
                "tooltip": ('module_llama_cpp_config_prompt_history_size_input_accessible_description',
                            self.lexemes.get('module_llama_cpp_config_prompt_history_size_input_accessible_description'))},
             "name": "settings_dialog_module_llama_cpp_config_prompt_history_size_label",
             "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('module_llama_cpp_config_prompt_history_size_label'),
             "callback": lambda obj: tab_module_llama_cpp_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop)},
            # Input field for the prompt history maximum capacity setting
            {"type": QSpinBox, "props": {'setMinimum': 0, 'setMaximum': 65536},  # Update the highest range
             "size_policy": (QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred),
             "name": "settings_dialog_module_llama_cpp_config_prompt_history_size:"
                     "module_llama_cpp_prompt_history_size",
             "callback": lambda obj: tab_module_llama_cpp_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop),
             "accessible_description":
                 self.lexemes.get('module_llama_cpp_config_prompt_history_size_input_accessible_description')},
            # Spacer to align elements at the top of the layout
            {"type": QWidget, "name": None, "size_policy": (QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding),
             "callback": lambda obj: tab_module_llama_cpp_config_layout.addWidget(obj)},
        ]

    def get_model_name(self):
        # Retrieve the LLM model name
        return f'({self.model_helper.get_model_name()})'

    @staticmethod
    def extend_settings_create_property(extend_func: Callable):
        if callable(extend_func):
            extend_func("module_llama_cpp_model_path", str, "")
            extend_func("module_llama_cpp_context_window", int, 2048)
            extend_func("module_llama_cpp_chat_format", str, str(LlmChatFormats.default()))
            extend_func("module_llama_cpp_system_prompt", str, "")
            extend_func("module_llama_cpp_response_temperature", int, 20)
            extend_func("module_llama_cpp_response_max_tokens", int, 0)
            extend_func("module_llama_cpp_prompt_history_size", int, 0)

    def settings_update_handler(self, data) -> None:
        """
        Perform actions upon settings change.

        Data is provided as a dictionary, where the key represents the setting name, and the value is its corresponding value.
        Note: This operation updates UI elements and internal properties, which may be resource-intensive.

        Args:
            data (dict): Dictionary containing settings changes, e.g., {"module_llama_cpp_model_path": "..."}

        Returns:
            None
        """

        AppConfig().logger.debug(f'Settings update handler is processing: {data}')

        options = [
            'module_llama_cpp_model_path',
            'module_llama_cpp_context_window',
            'module_llama_cpp_chat_format',
            'module_llama_cpp_response_temperature',
            'module_llama_cpp_response_max_tokens',
            # 'module_llama_cpp_system_prompt',
            # 'module_llama_cpp_prompt_history_size',
        ]
        if any(option in data for option in options) or 'ai_config_inference_module' in data:
            # Apply updated values or revert to settings if necessary
            model_path = self.settings.module_llama_cpp_model_path
            if 'module_llama_cpp_model_path' in data:
                model_path = data['module_llama_cpp_model_path']

            context_window = self.settings.module_llama_cpp_context_window
            if 'module_llama_cpp_context_window' in data:
                context_window = data['module_llama_cpp_context_window']

            chat_format = self.settings.module_llama_cpp_chat_format
            if 'module_llama_cpp_chat_format' in data:
                chat_format = data['module_llama_cpp_chat_format']

            # Reload the model helper
            ModelHelper.reload()

            search_options = self.get_search_options()

            # The model will be reloaded for the next session
            self.model_helper = ModelHelper(model_path=model_path, n_ctx=context_window, chat_format=chat_format,
                                            search_options=search_options)

    def temperature_change_handler(self, source_object, source_widget):
        if source_object.objectName() and source_widget:
            # Parse the object name to handle combinations of lexeme and setting keys
            _lexeme_key, setting_name = self.settings.settings_helper.parse_object_name(source_object.objectName())
            if setting_name == 'module_llama_cpp_response_temperature':
                # Fetch the latest value from the object, considering that settings might not be fully updated yet.
                temperature_int = source_object.value()  # source_object type: QSlider
                temperature_float = self.model_helper.convert_temperature(temperature_int)
                temperature_label = source_widget.findChild(
                    QLabel,
                    'settings_dialog_module_llama_cpp_config_response_temperature_label'
                )
                if temperature_label:
                    temperature_label.setText(
                        self.lexemes.get('module_llama_cpp_config_response_temperature_label',
                                         temperature=temperature_float))
