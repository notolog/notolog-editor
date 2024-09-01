"""
Notolog Editor
Open-source markdown editor developed in Python.

File Details:
- Purpose: Part of the 'On-Device LLM' module.
- Functionality: Enables local inference for supported LLMs.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QSizePolicy

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

from ...ui.ai_assistant import EnumMessageType, EnumMessageStyle
from ...ui.dir_path_line_edit import DirPathLineEdit

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
        # TODO check connections
        self.settings.value_changed.connect(
            lambda v: self.settings_update_handler(v))

        self.logger = logging.getLogger('ondevice_llm_module')

        self.logging = AppConfig().get_logging()
        self.debug = AppConfig().get_debug()

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
        # Cached helper instance
        self.model_helper = ModelHelper(model_path=model_path)

        # Just in case of debug of async events
        # if self.debug:
        #    asyncio.get_event_loop().set_debug(True)

        if self.logging:
            self.logger.info(f'Module {__name__} loaded')

    def init_prompt_manager(self, ai_dialog):
        """
        Prompt manager for prompt management and to add / append messages to prompt history.
        Note: It may not be initiated if called out of the context, from settings for example.
        """
        self.prompt_manager = PromptManager(parent=ai_dialog)

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
            if self.logging:
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
            if self.logging:
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
                        if self.logging:
                            self.logger.warning(f"Task raised an exception: {exception}")
                        # Error message to show in UI
                        outputs = self.lexemes.get('module_ondevice_llm_task_exception', scope='common',
                                                   error_msg=str(exception))
                        # Emit update message signal
                        self.update_signal.emit(outputs, None, None, EnumMessageType.DEFAULT, EnumMessageStyle.ERROR)
                    else:
                        result = task.result()
                        if self.debug:
                            self.logger.debug(f"Task completed with result: {result}")

    async def run_generator(self, input_tokens, request_msg_id, response_msg_id):

        try:
            generator = self.model_helper.init_generator(input_tokens, ModelHelper.search_options)  # type: Generator
        except ModuleNotFoundError as e:
            if self.logging:
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
            if self.logging:
                self.logger.info("Generation cancelled")
        except (WindowsError, RecursionError) as e:
            if self.logging:
                self.logger.error(f"Error occurred: {e}")
            # raise
        except (SystemExit, Exception) as e:
            if self.logging:
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
        tab_ondevice_llm_config.setObjectName('settings_dialog_tab_ondevice_llm_config')

        # Layout for the On Device LLM Config tab
        tab_ondevice_llm_config_layout = QVBoxLayout(tab_ondevice_llm_config)

        tab_widget.addTab(tab_ondevice_llm_config, self.lexemes.get('tab_ondevice_llm_config'))

        return [
            # [On Device LLM config]
            # Block label
            {"type": QLabel, "name": "settings_dialog_module_ondevice_llm_config_label",
             "props": {"setProperty": ("class", "group-header-label")},
             "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('module_ondevice_llm_config_label'), "style": {"bold": True},
             "callback": lambda obj: tab_ondevice_llm_config_layout.addWidget(obj)},
            # Base response max tokens label
            {"type": QLabel, "name": "settings_dialog_ondevice_llm_config_path_label",
             "alignment": Qt.AlignmentFlag.AlignLeft,
             "text": self.lexemes.get('module_ondevice_llm_config_path_label'),
             "callback": lambda obj: tab_ondevice_llm_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop)},
            # Model path line input
            {"type": DirPathLineEdit, "kwargs": {"settings": self.settings},
             "name": "settings_dialog_ondevice_llm_config_path:module_ondevice_llm_model_path",
             "read_only": False, "max_length": 256,
             "callback": lambda obj: tab_ondevice_llm_config_layout.addWidget(obj, alignment=Qt.AlignmentFlag.AlignTop),
             "placeholder_text": self.lexemes.get('module_ondevice_llm_config_path_input_placeholder_text'),
             "accessible_description":
                 self.lexemes.get('module_ondevice_llm_config_path_input_accessible_description')},
            # Spacer to keep elements above on top
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

        if AppConfig().get_debug():
            AppConfig().logger.debug('Settings update handler is in use "%s"' % data)

        if 'module_ondevice_llm_model_path' in data or 'ai_config_inference_module' in data:

            # Reload model helper
            ModelHelper.reload()

            # Set up updated value or one from settings
            model_path = (self.settings.module_ondevice_llm_model_path if 'ai_config_inference_module' in data
                          else data['module_ondevice_llm_model_path'])

            # The model will be reloaded next time with
            self.model_helper = ModelHelper(model_path=model_path)
