"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Part of the 'Module llama.cpp' module.
- Functionality: Provides helper functions to initialize and manage ONNX Runtime sessions for supported LLMs.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

import os
import logging
import asyncio

from threading import Lock

from typing import Union, Iterator

from llama_cpp import Llama, CreateChatCompletionResponse, CreateChatCompletionStreamResponse


class ModelHelper:

    model: Llama
    generator: Union[
        CreateChatCompletionResponse, Iterator[CreateChatCompletionStreamResponse]
    ]
    tokenizer: None  # LlamaTokenizer

    _instance = None  # Singleton instance
    _lock = Lock()

    search_options = {}

    def __new__(cls, *args, **kwargs):
        # Implement singleton pattern to ensure only one instance exists.
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

    def __init__(self, model_path: str, n_ctx: int = None, chat_format: str = None, search_options: dict = None):
        # Prevent reinitialization if the instance is already configured
        if hasattr(self, 'logger'):
            return

        # Use a lock to ensure initialization is thread-safe and atomic.
        with self._lock:
            # Double-check to prevent race conditions during initialization.
            if hasattr(self, 'logger'):
                return

            super(ModelHelper, self).__init__()

            self.logger = logging.getLogger('llama_cpp_model_helper')

            # Check model path is correct
            self.model_path = model_path
            if not os.path.isfile(self.model_path):
                self.logger.warning(f"Model not found in '{self.model_path}'")
                self.model_path = None

            # Context window. Refer to the logger for messages related to this value.
            # llama_new_context_with_model:
            #   n_ctx_per_seq (2048) < n_ctx_train (8192) -- the full capacity of the model will not be utilized
            self.n_ctx = n_ctx if n_ctx else 2048  # Default context window if not specified

            # Chat format specification
            self.chat_format = chat_format

            # Validate and set search options
            if search_options:
                supported_search_options = [
                    'temperature', 'top_p', 'top_k', 'min_p', 'typical_p', 'max_tokens',
                    'presence_penalty', 'frequency_penalty', 'repeat_penalty', 'tfs_z',
                    'mirostat_mode', 'mirostat_tau', 'mirostat_eta',  # Mirostat sampling
                ]
                # Check and filter supported
                search_options = {key: value for key, value in search_options.items() if key in supported_search_options}
                # Convert the integer value of temperature to a float
                if 'temperature' in search_options and isinstance(search_options['temperature'], int):
                    search_options['temperature'] = self.convert_temperature(search_options['temperature'])
                # Add or rewrite params if passed
                self.search_options.update(search_options)

    def init_model(self):
        """
        Lazily initializes the model with the given configuration. If the model is already initialized,
        the method exits early.

        Raises:
            ValueError: If `model_path` is not set or does not exist.
            RuntimeError: If an error occurs during the model instantiation due to configuration issues.
            Exception: For any unexpected errors.
        """

        # Check if the model is already initialized
        if getattr(self, 'model', None):
            return

        # Validate the model path
        if not self.model_path:
            raise ValueError(f"Model path is not set in '{type(self).__name__}'")

        self.logger.info(f"Initializing model: {self.model_path}")

        try:
            # Initialize the model
            self.model = Llama(
                model_path=self.model_path,
                chat_format=self.chat_format,  # e.g., 'chatml', 'llama-2', 'gemma', etc.
                n_ctx=self.n_ctx,  # Context window
                verbose=False  # Disable verbose output
            )
        except (RuntimeError, ValueError) as e:
            self.logger.error(f"Model initialization failed for path '{self.model_path}' with error: {e}")
            raise
        except Exception as e:
            self.logger.critical(f"Unexpected error during model initialization: {e}")
            raise

    def is_model_loaded(self) -> bool:
        """Check if the model is already initialized."""
        return getattr(self, 'model', None) is not None

    def get_input_tokens(self, text):
        # Check if the model is initialized
        if not getattr(self, 'model', None):
            return None

        # Tokenize the input text using the model's tokenizer
        input_tokens = self.model.tokenize(text.encode("utf-8"))

        return input_tokens

    def init_generator(self, prompt_messages, search_options):
        """
        Initialize the completion stream with the given prompt and options.

        Output example:
        [
            {"role": "system", "content": "You are ..."},
            {
                "role": "user",
                "content": "Describe ..."
            }
        ]
        """

        # Check if the model is initialized
        if not getattr(self, 'model', None):
            return None

        generator = self.model.create_chat_completion(
            messages=prompt_messages,
            stream=True,
            **search_options
        )

        return generator

    async def async_wrap_iterator(self, iterator):
        # Asynchronously handle output from generator
        for chunk in iterator:
            delta = chunk['choices'][0]['delta']
            if 'role' in delta:
                output = f"{delta['role']}: "  # 'assistant: '
                self.logger.debug(f"Role output: {output}")
                await asyncio.sleep(0)  # Yield control to the event loop
                yield ''  # output
            elif 'content' in delta:
                tokens = delta['content']  # content might contain a space symbol, so do not do the split() on it
                output = f"{tokens}"
                self.logger.debug(f"Output token(s): {tokens}")
                await asyncio.sleep(0)  # Yield control to the event loop
                yield output
            elif 'finish_reason' in delta:
                # For instance, if max_tokens limit reached: 'finish_reason': 'length'
                if delta['finish_reason'] is not None:
                    self.logger.debug(f"Output finished with the reason: '{delta['finish_reason']}'")
                    yield ''

    async def generate_output(self, generator):
        # Generate outputs for the model asynchronously.
        async for item in self.async_wrap_iterator(generator):
            return item

        # To stop the iteration
        raise StopAsyncIteration

    def get_model_name(self):
        # Check if the model is initialized, verify it has a 'metadata' attribute,
        # and confirm that the 'general.name' key exists in metadata.
        if (getattr(self, 'model', None)
                and hasattr(self.model, 'metadata')
                and 'general.name' in self.model.metadata):
            return self.model.metadata['general.name']

        # Safely return the model name, truncating if too long.
        return ModelHelper.truncate_string(os.path.basename(self.model_path))

    @staticmethod
    def truncate_string(text, max_length=32):
        # Truncate the string to the specified length, adding an ellipsis if necessary.
        if len(text) <= max_length:
            return text

        # Calculating the space to be allocated to the start and end of the string around the ellipsis
        part_length = (max_length - 3) // 2
        start_part = text[:part_length]
        end_part = text[-part_length:]

        # Create the truncated string with an ellipsis in the middle
        return f"{start_part}...{end_part}"

    @staticmethod
    def convert_temperature(temperature: int = 0):
        """
        Convert an integer temperature to a float for use in model settings.
        """
        return temperature / 100

    def cleanup(self):
        """
        Release model resources explicitly.
        Call this method when the model is no longer needed to free memory.
        """
        if hasattr(self, 'generator') and self.generator:
            self.generator = None
        if hasattr(self, 'model') and self.model:
            del self.model
            self.model = None
        self.logger.info("Model resources released")
