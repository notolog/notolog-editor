"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Part of the 'On-Device LLM' module.
- Functionality: Enables local inference for supported LLMs.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2025 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QSpinBox, QSlider, QSizePolicy, QScrollArea

import os
import logging

import asyncio
from asyncio import Task
from qasync import asyncSlot

from typing import TYPE_CHECKING, Callable

from .model_helper import ModelHelper
from .prompt_manager import PromptManager

from ..base_ai_core import BaseAiCore

from .. import Settings
from .. import AppConfig
from .. import Lexemes

from ...ui.ai_assistant.ai_assistant import EnumMessageType, EnumMessageStyle
from ...ui.dir_path_line_edit import DirPathLineEdit
from ...ui.horizontal_line_spacer import HorizontalLineSpacer
from ...ui.label_with_hint import LabelWithHint

if TYPE_CHECKING:
    # ONNX Runtime GenAI
    from onnxruntime_genai import Generator  # noqa


class ModuleCore(BaseAiCore):
    update_signal = Signal(str, object, object, EnumMessageType, EnumMessageStyle)
    # prompt_tokens, completion_tokens, total_tokens
    update_usage_signal = Signal(str, object, object, object, object)

    # Default name, use lexeme for the translated one
    module_name = 'On Device LLM'

    # Functionality extended by the module.
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

        self.logger = logging.getLogger('module_ondevice_llm')

        # Load lexemes for selected language and scope
        self.lexemes = Lexemes(self.settings.app_language,
                               default_scope='settings_dialog',
                               lexemes_dir=self.get_lexemes_path())

        # Extend Settings explicitly as it's a global object which may cause circular recursion
        self.extend_settings_create_property(self.settings.create_property)
        # Add this module to the inference modules selection list
        inference_modules = self.settings.ai_config_inference_modules
        default_module = [key for key, value in inference_modules.items() if isinstance(value, tuple) and True in value]
        inference_modules.update({'ondevice_llm': (self.lexemes.get('module_ondevice_llm_name', scope='common'),
                                                   True if not default_module else False)})
        self.settings.ai_config_inference_modules = inference_modules

        model_path = self.settings.module_ondevice_llm_model_path
        search_options = self.get_search_options()
        # Cached helper instance
        self.model_helper = ModelHelper(model_path=model_path, search_options=search_options)

        # Just in case of debug of async events
        # asyncio.get_event_loop().set_debug(True)

        self.logger.debug(f'Module {__name__} loaded')

    def get_search_options(self):
        search_options = {'batch_size': 1}
        if hasattr(self.settings, 'module_ondevice_llm_response_temperature'):
            search_options.update({'temperature': self.settings.module_ondevice_llm_response_temperature})
        if (hasattr(self.settings, 'module_ondevice_llm_response_max_tokens')
                and self.settings.module_ondevice_llm_response_max_tokens > 0):
            search_options.update({'max_length': self.settings.module_ondevice_llm_response_max_tokens})
        return search_options

    def init_prompt_manager(self, ai_dialog):
        """
        Prompt manager for prompt management and to add / append messages to prompt history.
        Note: It may not be initiated if called out of the context, from settings for example.
        """
        self.prompt_manager = PromptManager(max_history_size=self.settings.module_ondevice_llm_prompt_history_size,
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

        # Init model
        try:
            self.model_helper.init_model()
        except (AttributeError, Exception) as e:
            self.logger.error(f'{e}')
            # Complete init
            if self.init_callback and callable(self.init_callback):
                self.init_callback()
            # Error message to show in UI
            outputs = self.lexemes.get("module_ondevice_llm_model_exception", scope='common', error_msg=str(e))
            # Emit update message signal
            self.update_signal.emit(outputs, None, None, EnumMessageType.DEFAULT, EnumMessageStyle.ERROR)
            # Emit finished signal
            self.finished_callback(request_msg_id=request_msg_id, response_msg_id=response_msg_id,
                                   message_type=EnumMessageType.RESPONSE)
            return

        input_tokens = self.model_helper.get_input_tokens(user_prompt)

        # Emit update usage signal
        self.update_usage_signal.emit(self.get_model_name(), len(input_tokens), 0, len(input_tokens), False)

        if not self.generator_task or self.generator_task.done():
            # self.generator_task = await asyncio.create_task(self.run_generator(search_options, input_tokens))
            self.generator_task = asyncio.ensure_future(
                self.run_generator(input_tokens, request_msg_id, response_msg_id))
            # Finished callback
            if self.finished_callback and callable(self.finished_callback):
                self.generator_task.add_done_callback(
                    lambda _task, _request_msg_id=request_msg_id, _response_msg_id=response_msg_id:
                    self.finished_callback(request_msg_id=_request_msg_id, response_msg_id=_response_msg_id,
                                           message_type=EnumMessageType.RESPONSE))
            # Run task asynchronously
            done, pending = await asyncio.wait([self.generator_task], return_when=asyncio.FIRST_COMPLETED)

            for task in done:
                if not task.cancelled():
                    exception = task.exception()
                    if exception:
                        self.logger.warning(f"Task raised an exception: {exception}")
                        # Error message to show in UI
                        outputs = self.lexemes.get('module_ondevice_llm_task_exception', scope='common',
                                                   error_msg=str(exception))
                        # Emit update message signal
                        self.update_signal.emit(outputs, None, None, EnumMessageType.DEFAULT, EnumMessageStyle.ERROR)
                    else:
                        result = task.result()
                        self.logger.debug(f"Task completed with result: {result}")

    async def run_generator(self, input_tokens, request_msg_id, response_msg_id):

        try:
            generator = self.model_helper.init_generator(input_tokens, ModelHelper.search_options)  # type: Generator
        except ModuleNotFoundError as e:
            self.logger.error(f'Cannot init model generator: {e}', exc_info=False)
            # Re-raise to indicate unresolved issues to the caller
            raise
        finally:
            # The init stage has concluded
            if self.init_callback and callable(self.init_callback):
                self.init_callback()

        try:
            while not generator.is_done():
                await self.async_generator(request_msg_id, response_msg_id)
                await asyncio.sleep(0.05)  # Sleep to allow UI to update
        except asyncio.CancelledError:
            self.logger.info("Generation cancelled")
        except RecursionError as e:
            self.logger.error(f"Error occurred: {e}")
            # raise
        except (SystemExit, Exception) as e:
            self.logger.error(f"Exception raised: {e}")
            # raise
        finally:  # Generation ended
            await self.stop_generator()

    async def async_generator(self, request_msg_id, response_msg_id):
        # Get outputs for this iteration
        outputs = self.model_helper.generate_output()
        if outputs:
            # Emit update message signal
            self.update_signal.emit(outputs, request_msg_id, response_msg_id,
                                    EnumMessageType.RESPONSE, EnumMessageStyle.DEFAULT)
            # Emit update usage signal
            self.update_usage_signal.emit(self.get_model_name(), 0, 1, 1, True)  # One token at the moment

    async def stop_generator(self):
        # Cancel async task(s)
        if self.generator_task and not self.generator_task.done():
            # Allow to finish callback, do not remove:
            # > self.generator_task.remove_done_callback(self.finished_callback)
            self.generator_task.cancel()

    def extend_settings_dialog_fields_conf(self, tab_widget) -> list:
        # On Device LLM Config
        tab_ondevice_llm_config = QWidget()

        # Create the scroll area
        scroll_area = QScrollArea()
        scroll_area.setObjectName('settings_dialog_tab_ondevice_llm_config')
        scroll_area.setWidgetResizable(True)

        # Define the layout for the On Device LLM configuration tab
        tab_ondevice_llm_config_layout = QVBoxLayout(tab_ondevice_llm_config)

        # Set the content widget inside the scroll area
        scroll_area.setWidget(tab_ondevice_llm_config)

        tab_widget.addTab(scroll_area, self.lexemes.get('tab_ondevice_llm_config'))

        return [
            # [On Device LLM config]
            # Label for the configuration block
            {"type": QLabel, "name": "settings_dialog_module_ondevice_llm_config_label",
             "props": {"setProperty": ("class", "group-header-label")},
             "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('module_ondevice_llm_config_label'), "style": {"bold": True},
             "callback": lambda obj: tab_ondevice_llm_config_layout.addWidget(obj)},
            # Label for the model path input field
            {"type": LabelWithHint, "kwargs": {
                "tooltip": ('module_ondevice_llm_config_path_input_accessible_description',
                            self.lexemes.get('module_ondevice_llm_config_path_input_accessible_description'))},
             "name": "settings_dialog_module_ondevice_llm_config_path_label",
             "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('module_ondevice_llm_config_path_label'),
             "callback": lambda obj: tab_ondevice_llm_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop)},
            # Input field for the model path
            {"type": DirPathLineEdit, "kwargs": {"settings": self.settings},
             "name": "settings_dialog_ondevice_llm_config_path:module_ondevice_llm_model_path",
             "read_only": False, "max_length": 256,
             "callback": lambda obj: tab_ondevice_llm_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop),
             "placeholder_text": self.lexemes.get('module_ondevice_llm_config_path_input_placeholder_text'),
             "accessible_description":
                 self.lexemes.get('module_ondevice_llm_config_path_input_accessible_description')},
            # Vertical spacer
            {"type": QWidget, "name": None, "size_policy": (QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum),
             "callback": lambda obj: tab_ondevice_llm_config_layout.addWidget(obj)},
            # Label for the temperature slider
            {"type": LabelWithHint, "kwargs": {
                "tooltip": ('module_ondevice_llm_config_response_temperature_input_accessible_description',
                            self.lexemes.get('module_ondevice_llm_config_response_temperature_input_accessible_description'))},
             "name": "settings_dialog_module_ondevice_llm_config_response_temperature_label",
             "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('module_ondevice_llm_config_response_temperature_label',
                                      temperature=self.settings.module_ondevice_llm_response_temperature),
             "callback": lambda obj: tab_ondevice_llm_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop)},
            # Slider to adjust the temperature setting
            {"type": QSlider, "args": [Qt.Orientation.Horizontal],
             "props": {'setFocusPolicy': Qt.FocusPolicy.StrongFocus, 'setTickPosition': QSlider.TickPosition.TicksAbove,
                       'setTickInterval': 5, 'setSingleStep': 5, 'setMinimum': 0, 'setMaximum': 100},
             "name": "settings_dialog_module_ondevice_llm_config_response_temperature:"
                     "module_ondevice_llm_response_temperature",  # Lexeme key : Object name
             "callback": lambda obj: tab_ondevice_llm_config_layout.addWidget(obj),
             "on_value_change": self.temperature_change_handler,
             "accessible_description":
                 self.lexemes.get('module_ondevice_llm_config_response_temperature_input_accessible_description')},
            # Vertical spacer
            {"type": QWidget, "name": None, "size_policy": (QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum),
             "callback": lambda obj: tab_ondevice_llm_config_layout.addWidget(obj)},
            # Label for the maximum token count setting
            {"type": LabelWithHint, "kwargs": {
                "tooltip": ('module_ondevice_llm_config_response_max_tokens_input_accessible_description',
                            self.lexemes.get('module_ondevice_llm_config_response_max_tokens_input_accessible_description'))},
             "name": "settings_dialog_module_ondevice_llm_config_response_max_tokens_label",
             "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('module_ondevice_llm_config_response_max_tokens_label'),
             "callback": lambda obj: tab_ondevice_llm_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop)},
            # Input field for the maximum token count setting
            {"type": QSpinBox, "props": {'setMinimum': 0, 'setMaximum': 65536},  # Update the highest range
             "size_policy": (QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred),
             "name": "settings_dialog_module_ondevice_llm_config_response_max_tokens:"
                     "module_ondevice_llm_response_max_tokens",
             "callback": lambda obj: tab_ondevice_llm_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop),
             "accessible_description":
                 self.lexemes.get('module_ondevice_llm_config_response_max_tokens_input_accessible_description')},
            # Horizontal line spacer
            {"type": HorizontalLineSpacer, "callback": lambda obj: tab_ondevice_llm_config_layout.addWidget(obj)},
            # Label for the prompt history maximum capacity settings
            {"type": LabelWithHint, "kwargs": {
                "tooltip": ('module_ondevice_llm_config_prompt_history_size_input_accessible_description',
                            self.lexemes.get('module_ondevice_llm_config_prompt_history_size_input_accessible_description'))},
             "name": "settings_dialog_module_ondevice_llm_config_prompt_history_size_label",
             "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('module_ondevice_llm_config_prompt_history_size_label'),
             "callback": lambda obj: tab_ondevice_llm_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop)},
            # Input field for the prompt history maximum capacity setting
            {"type": QSpinBox, "props": {'setMinimum': 0, 'setMaximum': 65536},  # Update the highest range
             "size_policy": (QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred),
             "name": "settings_dialog_module_ondevice_llm_config_prompt_history_size:"
                     "module_ondevice_llm_prompt_history_size",
             "callback": lambda obj: tab_ondevice_llm_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop),
             "accessible_description":
                 self.lexemes.get('module_ondevice_llm_config_prompt_history_size_input_accessible_description')},
            # Spacer to align elements at the top of the layout
            {"type": QWidget, "name": None, "size_policy": (QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding),
             "callback": lambda obj: tab_ondevice_llm_config_layout.addWidget(obj)},
        ]

    def get_model_name(self):
        # Get LLM model name
        return f'({self.model_helper.get_model_name()})'

    @staticmethod
    def extend_settings_create_property(extend_func: Callable):
        if callable(extend_func):
            extend_func("module_ondevice_llm_model_path", str, "")
            extend_func("module_ondevice_llm_response_temperature", int, 20)
            extend_func("module_ondevice_llm_response_max_tokens", int, 0)
            extend_func("module_ondevice_llm_prompt_history_size", int, 0)

    def settings_update_handler(self, data) -> None:
        """
        Perform actions upon settings change.
        Data comes in a view of a dictionary, where is the key is the setting name, and the value is the actual value.
        Can be resource greedy.

        Args:
            data dict: say {"module_ondevice_llm_model_path": "..."}

        Return:
            None
        """

        AppConfig().logger.debug('Settings update handler is in use "%s"' % data)

        options = [
            'module_ondevice_llm_model_path',
            'module_ondevice_llm_response_temperature',
            'module_ondevice_llm_response_max_tokens',
        ]
        if any(option in data for option in options) or 'ai_config_inference_module' in data:
            # Set up updated value or one from settings
            model_path = self.settings.module_ondevice_llm_model_path
            if 'module_ondevice_llm_model_path' in data:
                model_path = data['module_ondevice_llm_model_path']

            if model_path:
                # Reload model helper
                ModelHelper.reload()

                search_options = self.get_search_options()

                # The model will be reloaded next time with
                self.model_helper = ModelHelper(model_path=model_path, search_options=search_options)

    def temperature_change_handler(self, source_object, source_widget):
        if source_object.objectName() and source_widget:
            # Parse the object name in case it contains a combination of lexeme and setting keys
            _lexeme_key, setting_name = self.settings.settings_helper.parse_object_name(source_object.objectName())
            if setting_name == 'module_ondevice_llm_response_temperature':
                # Get the latest value from the object, as settings might not yet be updated
                temperature_int = source_object.value()  # source_object type: QSlider
                temperature_float = self.model_helper.convert_temperature(temperature_int)
                temperature_label = source_widget.findChild(
                    QLabel,
                    'settings_dialog_module_ondevice_llm_config_response_temperature_label'
                )
                if temperature_label:
                    temperature_label.setText(
                        self.lexemes.get('module_ondevice_llm_config_response_temperature_label',
                                         temperature=temperature_float))
