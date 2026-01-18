"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Part of the 'OpenAI API' module.
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
from typing import Union

from ...ui.ai_assistant.ai_assistant import EnumMessageType


class PromptManager(QObject):

    prompt_template = None
    prompt_multi_template = None

    supported_roles = ['system', 'user', 'assistant']  # 'tool', 'function'

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

            self.logger = logging.getLogger('openai_api_prompt_manager')

            self.system_input = system_prompt
            self.max_history_size = max_history_size

            self.init_history()

            if parent and hasattr(parent, 'message_added'):
                # Catch new message added signal
                parent.message_added.connect(self.add_message)

    def init_history(self):
        self.logger.info('Initializing prompt history')
        # Start from new
        self.history = []
        # Init system prompt if set
        if self.system_input:
            self.add_system(self.system_input)

    def get_prompt_message(self, role: str, content: str) -> Union[dict, None]:
        if role not in PromptManager.supported_roles:
            self.logger.warning(f'Role "{role}" is not supported yet')
            return None
        return {'role': role, 'content': content}

    def get_prompt(self, multi_turn=True):
        if multi_turn:
            prompt = self.format_history()
        else:
            prompt = [
                self.get_prompt_message(role='system', content=self.system_input),
            ]
            last_user_message = self.find_last_message_by_role('user')
            if last_user_message:
                prompt.append(last_user_message)
            else:
                self.logger.warning('No user message has found for prompt')
                return None
        return prompt

    def add_message(self, message_text, request_msg_id, response_msg_id, message_type: EnumMessageType):
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
        self.update_or_add_entry(msg_id=msg_id,
                                 data=self.get_prompt_message(role='system', content=system_instruct))

    def add_request(self, request_text, request_msg_id):
        """
        Add a new request to the history, initially without a response.

        Args:
            request_text (str): The text of the request.
            request_msg_id (int): The unique message ID of the request.
        """
        self.update_or_add_entry(msg_id=request_msg_id,
                                 data=self.get_prompt_message(role='user', content=request_text))

    def add_response(self, response_text, response_msg_id, request_msg_id):
        """
        Update the corresponding request with a response, identified by request message ID.

        Args:
            response_text (str): The text of the response.
            response_msg_id (int): The message ID of the response.
            request_msg_id (int): The request message ID to which this response corresponds.
        """
        self.update_or_add_entry(msg_id=response_msg_id,
                                 data=self.get_prompt_message(role='assistant', content=response_text))

    def update_or_add_entry(self, msg_id, data):
        """
        Update the entry with the specified ID, or add a new entry if ID does not exist.

        Args:
        - msg_id (int): The ID to search for in the messages.
        - data (dict): The new data to replace the old 'data' dictionary or to add if ID is new.

        Returns:
        - None; the list is modified in place.
        """
        for message in self.history:
            if message['id'] == msg_id:
                message['data'] = data
                return

        # If no entry with the specified ID is found, add a new one
        self.history.append({'id': msg_id, 'data': data})

        # Limit history records size (if applicable)
        self.limit_history_size()

    def format_history(self):
        """
        Format the stored history of requests and responses into a text format.

        Returns:
            str: A string representing the formatted history.
        """
        formatted_history = []  # In the API itself it looks like a: history = {"messages": [...]}

        for message in self.history:
            data = message['data']
            formatted_history.append(data)
        return formatted_history

    def get_history(self) -> str:
        # Get history object
        history = self.format_history()

        # Format each entry and combine them into a text
        result = "\n\n".join(f"**{entry['role']}**:\n{entry['content']}" for entry in history)

        return result

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
            if 'data' in message and 'role' in message['data'] and message['data']['role'] == role:
                # Return the last role's message
                return message['data']
        return None
