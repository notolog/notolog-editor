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
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

import os
import logging
import platform

from threading import Lock
from enum import Enum

# ONNX Runtime GenAI
from onnxruntime_genai import Config, Generator, GeneratorParams, Model, Tokenizer, TokenizerStream


class ExecutionProvider(Enum):
    """
    Supported ONNX Runtime execution providers for hardware acceleration.

    Reference: https://github.com/microsoft/onnxruntime-genai

    Supported providers:
    - DML/DmlExecutionProvider - DirectML (Windows)
    - QNN/QNNExecutionProvider - Qualcomm Neural Network
    - OpenVINO/OpenVINOExecutionProvider - Intel OpenVINO
    - SNPE/SNPEExecutionProvider - Snapdragon NPE
    - XNNPACK/XnnpackExecutionProvider - XNNPACK (mobile/web)
    - WEBNN/WebNNExecutionProvider - Web Neural Network
    - WebGPU/WebGpuExecutionProvider - WebGPU
    - AZURE/AzureExecutionProvider - Azure
    - JS/JsExecutionProvider - JavaScript
    - VitisAI/VitisAIExecutionProvider - AMD Vitis AI
    - CoreML/CoreMLExecutionProvider - Apple Core ML
    - NvTensorRtRtx/NvTensorRTRTXExecutionProvider - NVIDIA TensorRT RTX
    - MIGraphX/MIGraphXExecutionProvider - AMD MIGraphX

    Note: CUDA is handled separately via onnxruntime-genai-cuda package, not as a provider.
    """
    # CPU is always available (default when no provider specified)
    CPU = ("cpu", "CPU (Default)")

    # NVIDIA CUDA - requires onnxruntime-genai-cuda package
    CUDA = ("cuda", "CUDA (NVIDIA GPUs)")

    # Windows DirectX 12 - requires DirectX 12 compatible GPU
    DML = ("DML", "DirectML (Windows)")

    # Intel OpenVINO - requires Intel CPU/GPU/VPU
    OPENVINO = ("OpenVINO", "OpenVINO (Intel)")

    # Apple Core ML - requires macOS with Apple Silicon or Neural Engine
    COREML = ("CoreML", "CoreML (Apple)")

    # NVIDIA TensorRT RTX - requires NVIDIA RTX GPU
    TENSORRT_RTX = ("NvTensorRtRtx", "TensorRT RTX (NVIDIA)")

    # Qualcomm QNN - requires Qualcomm Snapdragon with NPU
    QNN = ("QNN", "QNN (Qualcomm)")

    # AMD MIGraphX - requires AMD GPU with ROCm
    MIGRAPHX = ("MIGraphX", "MIGraphX (AMD)")

    # AMD Vitis AI - requires AMD FPGA/AI accelerator
    VITISAI = ("VitisAI", "Vitis AI (AMD FPGA)")

    # Snapdragon NPE - requires Qualcomm Snapdragon
    SNPE = ("SNPE", "SNPE (Snapdragon)")

    # XNNPACK - CPU optimization for mobile/embedded
    XNNPACK = ("XNNPACK", "XNNPACK (Mobile)")

    def __init__(self, provider_name: str, display_name: str):
        self.provider_name = provider_name
        self.display_name = display_name

    @property
    def value(self):
        """Return the provider name for ONNX Runtime."""
        return self.provider_name

    def __str__(self):
        """Return display name for UI."""
        return self.display_name

    @classmethod
    def get_available_providers(cls) -> list:
        """
        Get list of execution providers likely available on the current platform.
        Note: Actual availability depends on installed ONNX Runtime packages and hardware.
        """
        providers = [cls.CPU]  # CPU is always available

        system = platform.system().lower()

        if system == "windows":
            providers.extend([cls.DML, cls.CUDA, cls.TENSORRT_RTX, cls.OPENVINO])
        elif system == "linux":
            providers.extend([cls.CUDA, cls.TENSORRT_RTX, cls.OPENVINO, cls.QNN, cls.MIGRAPHX, cls.VITISAI])
        elif system == "darwin":  # macOS
            providers.extend([cls.COREML])

        return providers

    @classmethod
    def default(cls):
        """Return the default execution provider (CPU)."""
        return cls.CPU

    @classmethod
    def from_string(cls, value: str):
        """Get ExecutionProvider from string value."""
        for provider in cls:
            if provider.provider_name == value or provider.name == value:
                return provider
        return cls.default()


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

    def __init__(self, model_path: str, search_options: dict = None,
                 execution_provider: ExecutionProvider = None):
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
                    or not any(f.endswith('.onnx') for f in os.listdir(self.model_path) if
                               os.path.isfile(os.path.join(self.model_path, f)))):
                self.logger.warning(f'Model not found in {self.model_path}')
                self.model_path = None

            # Execution provider for hardware acceleration
            self.execution_provider = execution_provider or ExecutionProvider.default()

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
        """
        Lazily initialize the ONNX Runtime GenAI model with configuration.

        If the model is already initialized, this method exits early. The model is
        loaded with the configuration from the model directory.

        Raises:
            AttributeError: If model_path is not set or is None
            RuntimeError: If model initialization fails due to missing files or invalid config
            Exception: For any unexpected errors during initialization
        """
        if hasattr(self, 'model') and self.model:
            return
        if self.model_path is None:
            raise AttributeError(f"'{type(self).__name__}' model path is not set")

        # Log event
        self.logger.info(f'Initializing ONNX model: {self.model_path}')

        try:
            # Configure the model settings
            config = Config(self.model_path)
            config.clear_providers()

            # Set execution provider for hardware acceleration
            provider_name = self.execution_provider.provider_name
            provider_added = False

            if self.execution_provider != ExecutionProvider.CPU:
                try:
                    config.append_provider(provider_name)
                    provider_added = True
                    self.logger.info(f"Using execution provider: {provider_name} ({self.execution_provider.display_name})")
                except Exception as ep_error:
                    error_msg = str(ep_error)
                    # Provide specific guidance based on error type
                    if 'cuda' in provider_name.lower():
                        if 'libcublasLt' in error_msg or 'libcudnn' in error_msg or 'libcublas' in error_msg:
                            self.logger.warning(
                                f"CUDA runtime libraries missing: {ep_error}. "
                                f"Install CUDA Toolkit and cuDNN: "
                                f"Falling back to CPU.")
                        elif 'not enabled' in error_msg.lower():
                            self.logger.warning(
                                f"CUDA provider requires onnxruntime-genai-cuda package: {ep_error}. "
                                f"Falling back to CPU.")
                        else:
                            self.logger.warning(
                                f"Failed to initialize CUDA provider: {ep_error}. "
                                f"Falling back to CPU.")
                    elif provider_name == 'DML':
                        self.logger.warning(
                            f"DirectML provider requires onnxruntime-genai-directml package: {ep_error}. "
                            f"Falling back to CPU.")
                    else:
                        self.logger.warning(
                            f"Failed to add provider '{provider_name}': {ep_error}. "
                            f"Ensure the provider is supported and required packages are installed. "
                            f"Falling back to CPU.")
                    # Will use CPU as fallback (no provider = CPU)

            if not provider_added:
                self.logger.info("Using CPU execution provider")

            # Initialize model and tokenizer
            self.model = Model(config)
            self.tokenizer = Tokenizer(self.model)
            self.tokenizer_stream = self.tokenizer.create_stream()

            self.logger.info(f"Model initialized successfully: {self.model_path}")
        except (RuntimeError, ValueError) as e:
            error_msg = str(e)
            # Check for GPU memory allocation errors
            if 'Failed to allocate memory' in error_msg or 'BFCArena' in error_msg:
                self.logger.error(
                    f"GPU memory allocation failed: {e}. "
                    f"Model may be too large for available GPU memory.")
            else:
                self.logger.error(f"Model initialization failed for path '{self.model_path}': {e}")
            raise
        except Exception as e:
            self.logger.critical(f"Unexpected error during model initialization: {e}")
            raise

    def is_model_loaded(self) -> bool:
        """Check if the model is already initialized."""
        return hasattr(self, 'model') and self.model is not None

    def get_input_tokens(self, prompt):
        """
        Encode a text prompt into tokens using the model's tokenizer.

        Args:
            prompt (str): The text prompt to encode

        Returns:
            list: Encoded token IDs
        """
        input_tokens = self.tokenizer.encode(prompt)
        return input_tokens

    def init_generator(self, input_tokens, search_options):
        """
        Initialize the ONNX generator with tokens and search options.

        Args:
            input_tokens (list): Encoded token IDs to start generation from
            search_options (dict): Search parameters (max_length, temperature, top_p, etc.)

        Returns:
            Generator: The initialized ONNX Runtime GenAI generator
        """
        # Configure generator with necessary parameters
        params = GeneratorParams(self.model)
        vocab_size = getattr(params, 'vocab_size', 0)
        self.logger.debug(f'Model vocabulary size: {vocab_size}')

        # Set search options (temperature, max_length, top_p, etc.)
        params.set_search_options(**search_options)

        # For older API compatibility (v0.5.2 and earlier)
        if hasattr(params, 'input_ids'):
            params.input_ids = input_tokens

        # Initialize the generator
        self.generator = Generator(self.model, params)  # type: Generator

        # Append input tokens (v0.6.0+ API)
        if hasattr(self.generator, 'append_tokens'):
            self.generator.append_tokens(input_tokens)

        return self.generator

    def generate_output(self):
        """
        Generate the next token(s) from the model.

        Important: Following onnxruntime-genai v0.11.0+ API changes for improved
        multi-turn conversation quality. The decoding loop must now:
        1. Call generate_next_token() FIRST
        2. Check is_done() AFTER generating
        3. Only get and decode tokens if not done

        Returns:
            str: Decoded token(s) or None if generation is complete
        """
        # Generate next token (v0.11.0+: generate BEFORE checking is_done)
        self.generator.generate_next_token()

        # Check if generation is complete (v0.11.0+: check AFTER generating)
        if self.generator.is_done():
            return None

        # Get and decode the new token(s)
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

    def cleanup(self):
        """
        Release ONNX model resources explicitly.

        Call this method when the model is no longer needed to free memory.
        Properly releases generator, tokenizer stream, tokenizer, and model in order.
        """
        try:
            if hasattr(self, 'generator') and self.generator:
                self.generator = None
            if hasattr(self, 'tokenizer_stream') and self.tokenizer_stream:
                self.tokenizer_stream = None
            if hasattr(self, 'tokenizer') and self.tokenizer:
                self.tokenizer = None
            if hasattr(self, 'model') and self.model:
                del self.model
                self.model = None
            self.logger.info("Model resources released successfully")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
            # Still set to None to avoid partial cleanup state
            self.model = None
            self.tokenizer = None
            self.tokenizer_stream = None
            self.generator = None
