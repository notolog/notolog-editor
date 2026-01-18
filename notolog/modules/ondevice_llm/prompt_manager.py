"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Part of the 'On-Device LLM' module.
- Functionality: Manages prompt formatting and prompt history.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import QObject

import logging

from threading import Lock
from typing import Any, Union

from ...ui.ai_assistant.ai_assistant import EnumMessageType


class PromptManager(QObject):

    """
    Ensure to include a BOS (<|endoftext|>) token at the start of the conversation
    in some applications/frameworks. This inclusion often yields more reliable results.
    """
    bos_token = '<|endoftext|>'
    system_prompt_template = '<|system|>\n{system}<|end|>\n'
    prompt_template = '<|user|>\n{input}<|end|>\n<|assistant|>\n'
    prompt_multi_template = '<|user|>\n{input}<|end|>\n<|assistant|>\n{output}<|end|>\n'

    supported_roles = ['system', 'user', 'assistant']

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
        Reinitialize the singleton instance to allow controlled re-creation.
        """
        with cls._lock:
            # Create a new instance
            cls._instance = super().__new__(cls, *args, **kwargs)

    def __init__(self, system_prompt=None, max_history_size=None, parent=None):

        # Prevent re-initialization if the instance is already set up.
        if hasattr(self, 'logger'):
            return

        # Use a lock to ensure initialization is thread-safe and atomic.
        with self._lock:
            # Double-check to prevent race conditions during initialization.
            if hasattr(self, 'logger'):
                return

            super().__init__(parent)

            self.logger = logging.getLogger('ondevice_llm_prompt_manager')

            self.system_input = system_prompt  # Not yet supported
            self.max_history_size = max_history_size

            self.init_history()

            if parent and hasattr(parent, 'message_added'):
                # Catch new message added signal
                parent.message_added.connect(self.add_message)

    def init_history(self):
        """
        Initializes or resets the prompt history.
        This method clears existing history and sets up a system prompt if one is provided.
        """

        self.logger.info('Initializing prompt history')

        # Start from new
        self.history = []

        # Init system prompt if set
        if self.system_input is not None:
            self.add_system(self.system_input)

    def get_system_prompt_message(self) -> str:
        if self.system_input is None:
            return ''
        # Template with the <|system|> token.
        return f'{PromptManager.system_prompt_template.format(system=self.system_input)}'

    def get_prompt_message(self, request_text: str) -> str:
        # The conversation template: a simple prompt with an open <|assistant|> token.
        # Since this is a one-message request conversation, there is no response yet.
        # The history must already contain the last input.
        prompt = f'{PromptManager.prompt_template.format(input=request_text)}'
        return prompt

    def get_multi_turn_prompt_message(self, request_text: str, response_text: str = '', is_last_input=False) -> str:
        # The conversation template: a multi-turn template.
        prompt = self.get_system_prompt_message()

        if not is_last_input:
            # multi-turn template with response
            prompt += f'{PromptManager.prompt_multi_template.format(input=request_text, output=response_text)}'
        else:
            # last user message is a simple prompt with an open <|assistant|> token
            prompt += f'{PromptManager.prompt_template.format(input=request_text)}'

        return prompt

    def get_prompt(self, multi_turn=True) -> Any:
        if multi_turn:
            prompt = self.format_history()
        else:
            prompt = self.get_system_prompt_message()
            last_user_message = self.find_last_message_by_role('user')
            if last_user_message and 'text' in last_user_message:
                prompt += self.get_prompt_message(request_text=last_user_message['text'])
            else:
                self.logger.warning('No user message has found for prompt')
                return None
        return prompt

    def add_message(self, message_text, request_msg_id, response_msg_id, message_type: EnumMessageType):
        # Convert sentinel value -1 back to None (used to avoid C++ type conversion errors)
        if request_msg_id == -1:
            request_msg_id = None
        if response_msg_id == -1:
            response_msg_id = None

        self.logger.debug(f'Add message: {message_text}, {response_msg_id}, {message_type}')
        if message_type == EnumMessageType.USER_INPUT:
            self.add_request(message_text, request_msg_id)
        elif message_type == EnumMessageType.RESPONSE:
            self.add_response(message_text, response_msg_id, request_msg_id)
        else:
            # Default or info message; not for prompt
            pass

    def add_system(self, system_instruct, msg_id=None):
        """
        Add a new request to the history, initially without a response.

        Args:
            system_instruct (str): The text of the request.
            msg_id (int, optional): The unique message ID of the request.
        """

        if self.find_last_message_by_role('system'):
            return

        self.history.append({
            'system': {'text': system_instruct, 'msg_id': msg_id},
        })

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
            if 'user' in record and record['user']['msg_id'] == request_msg_id:
                record['assistant'] = {'text': response_text, 'msg_id': response_msg_id}
                # Update history
                self.history[i] = record
                return

        self.logger.warning(f"No matching request {request_msg_id} found for response {response_msg_id}.")

        # Handle unmatched response by finding empty response
        for i, record in enumerate(self.history):
            if 'assistant' in record and record['assistant'] is None:  # Find the first request without a response
                record['assistant'] = {'text': response_text, 'msg_id': response_msg_id}
                # Update history
                self.history[i] = record
                break

    def format_history(self):
        """
        Formats the stored history of prompts into a structured text format suitable for use in generating responses.
        This includes structuring each entry with proper roles and ensuring they are correctly sequenced for
        dialogue continuation.

        Returns:
            str: A string representing the formatted history.
        """

        formatted_history = self.bos_token + self.get_system_prompt_message()

        last_user_msg_id = None
        # Find the last message id for user input (assistant message is in the same object)
        last_user_message = self.find_last_message_by_role('user')
        if last_user_message and 'msg_id' in last_user_message:
            last_user_msg_id = last_user_message['msg_id']
        else:
            return formatted_history

        for record in self.history:
            request_text = record['user']['text']
            response_text = record['assistant']['text'] if record['assistant'] is not None else ""
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
            # Extracting system information
            system_text = ""
            if 'system' in entry and entry['system'] is not None:
                system = entry['system']
                system_text = f"**system**:\n{system['text']}\n\n"

            # Extracting user information
            user_text = ""
            if 'user' in entry and entry['user'] is not None:
                user = entry['user']
                user_text = f"**user**:\n{user['text']}\n\n"

            # Extracting assistant information if it exists
            assistant_text = ""
            if 'assistant' in entry and entry['assistant'] is not None:
                assistant = entry['assistant']
                assistant_text = f"**assistant**:\n{assistant['text']}\n\n"

            # Concatenating system, user and assistant texts
            result += system_text + user_text + assistant_text

        return result.strip()

    def limit_history_size(self):
        """
        Ensures the history does not exceed the maximum specified size.
        If a system prompt is set, it retains the system prompt at the beginning of the history,
        and removes the oldest records to maintain the history within the specified size limit.
        """

        if self.max_history_size:
            # Calculate the additional index offset if a system prompt is included
            system_prompt_shift = 1 if self.system_input else 0
            # Calculate the total allowed history size including the system prompt
            allowed_history_size = self.max_history_size + system_prompt_shift

            # Remove entries until the history size is within the allowed limit
            while len(self.history) > allowed_history_size:
                # Remove the oldest record, keeping the system prompt intact if present
                self.history.pop(system_prompt_shift)  # Pop from the first non-prompt position

    def find_last_message_by_role(self, role: str) -> Union[dict, None]:
        if role not in PromptManager.supported_roles:
            self.logger.warning(f'Role "{role}" is not supported yet')
            return None
        for message in reversed(self.history):
            _data = message
            # Assume both roles are set
            if role in _data:
                return _data[role]
        return None
