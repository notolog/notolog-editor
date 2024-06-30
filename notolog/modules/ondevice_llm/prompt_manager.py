"""
Notolog Editor
Open-source markdown editor developed in Python.

File Details:
- Purpose: Part of the 'On-Device LLM' module.
- Functionality: Manages prompt formatting and prompt history.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import QObject

import logging

from threading import Lock
from typing import Any, Union

from .. import AppConfig
from ...ui.ai_assistant import EnumMessageType


class PromptManager(QObject):

    """
    Ensure to include a BOS (<|endoftext|>) token at the start of the conversation
    in some applications/frameworks. This inclusion often yields more reliable results.
    """
    bos_token = '<|endoftext|>'
    prompt_template = '<|user|>\n{input}<|end|>\n<|assistant|>\n'
    prompt_multi_template = '<|user|>\n{input}<|end|>\n<|assistant|>\n{output}<|end|>\n'

    supported_roles = ['user', 'assistant']

    _instance = None  # Singleton instance
    _lock = Lock()

    history: list = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    # Create the instance if it doesn't exist
                    cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def reload(cls, *args, **kwargs):
        """
       Reinitialize the singleton instance. This method allows for the controlled
       re-creation of the singleton instance.
       """
        with cls._lock:
            # Create a new instance
            cls._instance = super().__new__(cls)

    def __init__(self, max_history_size=10, parent=None):

        # Check if instance is already initialized
        if hasattr(self, 'logger'):
            return

        # Ensure that the initialization check and the setting of 'modules' param are atomic.
        with self._lock:
            # This prevents race conditions.
            if hasattr(self, 'logger'):
                return

            super().__init__(parent)

            self.parent = parent

            self.logger = logging.getLogger('ondevice_llm_prompt_manager')

            self.logging = AppConfig().get_logging()
            self.debug = AppConfig().get_debug()

            self.max_history_size = max_history_size

            self.init_history()

            # Catch new message added signal
            self.parent.message_added.connect(self.add_message)

    def init_history(self):
        if self.logging:
            self.logger.info('Re-initializing prompt history')
        # Start from new
        self.history = []

    def get_prompt_message(self, request_text: str) -> str:
        # The conversation template: a simple prompt with an open <|assistant|> token.
        # Since this is a one-message request conversation, there is no response yet.
        # The history must already contain the last input.
        prompt = f'{PromptManager.prompt_template.format(input=request_text)}'
        return prompt

    def get_multi_turn_prompt_message(self, request_text: str, response_text: str = '', is_last_input=False) -> str:
        # The conversation template: a multi-turn template.
        # The history must already contain the last input.
        if not is_last_input:
            # multi-turn template with response
            prompt = f'{PromptManager.prompt_multi_template.format(input=request_text, output=response_text)}'
        else:
            # last user message is a simple prompt with an open <|assistant|> token
            prompt = f'{PromptManager.prompt_template.format(input=request_text)}'
        return prompt

    def get_prompt(self, multi_turn=True) -> Any:
        if multi_turn:
            prompt = self.format_history()
        else:
            last_user_message = self.find_last_message_by_role('user')
            if last_user_message and 'text' in last_user_message:
                prompt = self.get_prompt_message(request_text=last_user_message['text'])
            else:
                if self.logging:
                    self.logger.warning('No user message has found for prompt')
                return None
        return prompt

    def add_message(self, message_text, request_msg_id, response_msg_id, message_type: EnumMessageType):
        if self.debug:
            self.logger.debug('Add message:', message_text, response_msg_id, message_type)
        if message_type == EnumMessageType.USER_INPUT:
            self.add_request(message_text, request_msg_id)
        elif message_type == EnumMessageType.RESPONSE:
            self.add_response(message_text, response_msg_id, request_msg_id)
        else:
            # Default or info message; not for prompt
            pass

    def add_request(self, request_text, request_msg_id):
        """
        Add a new request to the history, initially without a response.

        Args:
            request_text (str): The text of the request.
            request_msg_id (int): The unique message ID of the request.
        """
        self.history.append({
            'user': {'text': request_text, 'msg_id': request_msg_id},
            'assistant': None  # Initially, no response is available
        })
        self.limit_history_size()

    def add_response(self, response_text, response_msg_id, request_msg_id):
        """
        Update the corresponding request with a response, identified by request message ID.

        Args:
            response_text (str): The text of the response.
            response_msg_id (int): The message ID of the response.
            request_msg_id (int): The request message ID to which this response corresponds.
        """
        for i, record in enumerate(self.history):
            if record['user']['msg_id'] == request_msg_id:
                record['assistant'] = {'text': response_text, 'msg_id': response_msg_id}
                # Update history
                self.history[i] = record
                return

        if self.logging:
            self.logger.warning(f"No matching request {request_msg_id} found for response {response_msg_id}.")

        # Handle unmatched response by finding empty response
        for i, record in enumerate(self.history):
            if record['assistant'] is None:  # Find the first request without a response
                record['assistant'] = {'text': response_text, 'msg_id': response_msg_id}
                # Update history
                self.history[i] = record
                break

    def format_history(self):
        """
        Format the stored history of requests and responses into a text format.

        Returns:
            str: A string representing the formatted history.
        """

        last_user_msg_id = None
        # Find the last message id for user input (assistant message is in the same object)
        last_user_message = self.find_last_message_by_role('user')
        if last_user_message and 'msg_id' in last_user_message:
            last_user_msg_id = last_user_message['msg_id']

        formatted_history = self.bos_token
        for record in self.history:
            request_text = record['user']['text']
            response_text = record['assistant']['text'] if record['assistant'] else ""
            formatted_history += self.get_multi_turn_prompt_message(
                request_text=request_text, response_text=response_text,
                # History is always multi-turn, check either the input was a last message
                is_last_input=(last_user_msg_id == record['user']['msg_id']
                               and not hasattr(record['assistant'], 'msg_id')))
        # Return formatted history prompt
        return formatted_history

    def get_history(self) -> str:
        result = ''
        # Format each entry and combine them into a text
        for entry in self.history:
            # Extracting user information
            user = entry['user']
            user_text = f"**User**:\n{user['text']}\n\n"

            # Extracting assistant information if it exists
            assistant_text = ""
            if 'assistant' in entry and entry['assistant'] is not None:
                assistant = entry['assistant']
                assistant_text = f"**Assistant**:\n{assistant['text']}\n\n"

            # Concatenating user and assistant text
            result += user_text + assistant_text

        return result.strip()

    def limit_history_size(self):
        """
        Ensures the history does not exceed the maximum size.
        """
        while len(self.history) > self.max_history_size:
            self.history.pop(0)  # Remove the oldest record

    def find_last_message_by_role(self, role: str) -> Union[dict, None]:
        if role not in PromptManager.supported_roles:
            if self.logging:
                self.logger.warning(f'Role "{role}" is not supported yet')
            return None
        for message in reversed(self.history):
            _data = message
            # Assume both roles are set
            if role in _data:
                return _data[role]
        return None
