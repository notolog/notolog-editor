"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Part of the 'On-Device LLM' module.
- Functionality: Provides helper functions to initialize and manage ONNX Runtime sessions for supported LLMs.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2025 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

import os
import logging

from threading import Lock

# ONNX Runtime GenAI
from onnxruntime_genai import Config, Generator, GeneratorParams, Model, Tokenizer, TokenizerStream


class ModelHelper:

    model: Model
    generator: Generator
    tokenizer: Tokenizer
    tokenizer_stream: TokenizerStream

    _instance = None  # Singleton instance
    _lock = Lock()

    # Set the max length to something sensible by default,
    # since otherwise it will be set to the entire context length
    search_options = {'max_length': 4096}

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
            cls._instance = super().__new__(cls)

    def __init__(self, model_path: str, search_options: dict = None):
        # Prevent re-initialization if the instance is already set up.
        if hasattr(self, 'logger'):
            return

        # Use a lock to ensure initialization is thread-safe and atomic.
        with self._lock:
            # Double-check to prevent race conditions during initialization.
            if hasattr(self, 'logger'):
                return

            super(ModelHelper, self).__init__()

            self.logger = logging.getLogger('ondevice_llm_model_helper')

            # Check model path is correct
            self.model_path = model_path
            if (not os.path.isdir(self.model_path)
                    or not os.path.isfile(os.path.join(self.model_path, 'tokenizer.model'))):
                self.logger.warning(f'Model not found in {self.model_path}')
                self.model_path = None

            if search_options:
                # The list of the supported options
                supported_search_options = [
                    'do_sample', 'max_length', 'min_length', 'top_p', 'top_k', 'temperature', 'repetition_penalty']
                # Check and filter supported
                search_options = {key: value for key, value in search_options.items() if key in supported_search_options}
                # Convert the integer value of temperature to a float
                if 'temperature' in search_options and type(search_options['temperature']) is int:
                    search_options['temperature'] = self.convert_temperature(search_options['temperature'])
                # Add or rewrite params if passed
                self.search_options.update(search_options)

    def init_model(self):
        if hasattr(self, 'model') and self.model:
            return
        if self.model_path is None:
            raise AttributeError(f"'{type(self).__name__}' model path is not set")
        # Log event
        self.logger.info(f'Initializing model: {self.model_path}')
        # Configure the model settings
        config = Config(self.model_path)
        config.clear_providers()
        # config.append_provider(execution_provider := "cuda")
        # Init model
        self.model = Model(config)
        self.tokenizer = Tokenizer(self.model)
        self.tokenizer_stream = self.tokenizer.create_stream()

    def get_input_tokens(self, prompt):
        input_tokens = self.tokenizer.encode(prompt)
        return input_tokens

    def init_generator(self, input_tokens, search_options):
        # Configure your generator with necessary parameters
        params = GeneratorParams(self.model)
        vocab_size = getattr(params, 'vocab_size', 0)
        self.logger.debug(f'Model vocabulary size: {vocab_size}')
        params.set_search_options(**search_options)
        if hasattr(params, 'input_ids'):  # v0.5.2: input_ids not set in GeneratorParams
            params.input_ids = input_tokens
        # params.use_cuda = False
        self.generator = Generator(self.model, params)  # type: Generator
        if hasattr(self.generator, 'append_tokens'):
            self.generator.append_tokens(input_tokens)
        return self.generator

    def generate_output(self):
        if not self.generator.is_done():
            # Get tokens for this iteration
            if hasattr(self.generator, 'compute_logits'):  # v0.5.2: Must call ComputeLogits before GenerateNextToken
                self.generator.compute_logits()
            self.generator.generate_next_token()
            new_tokens = self.generator.get_next_tokens()
            # Only one token, double check token counting logic if changed
            new_token = new_tokens[0]
            outputs = self.tokenizer_stream.decode(new_token)
            # Or via decoding a batch
            # outputs = ''.join(self.tokenizer.decode_batch(new_tokens))
            self.logger.debug(f'Output: {outputs}: {new_token}')
            return outputs

    def get_model_name(self):
        # Safely truncate a long name
        return ModelHelper.truncate_string(os.path.basename(self.model_path))

    @staticmethod
    def truncate_string(text, max_text_length=32):
        if len(text) <= max_text_length:
            return text

        # Calculating the space to be allocated to the start and end of the string around the ellipsis
        part_length = (max_text_length - 3) // 2
        start_part = text[:part_length]
        end_part = text[-part_length:]

        # Create the truncated string with an ellipsis in the middle
        return f"{start_part}...{end_part}"

    @staticmethod
    def convert_temperature(temperature: int = 0):
        """ Convert the integer value of temperature to a float. """
        return temperature / 100
