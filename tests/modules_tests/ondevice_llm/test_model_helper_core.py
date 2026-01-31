"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Unit tests for ondevice_llm module

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License
"""

import pytest
from unittest.mock import MagicMock, patch
import platform

# Skip all tests if onnxruntime-genai not available
onnxruntime_genai = pytest.importorskip("onnxruntime_genai", reason="onnxruntime-genai module not available")


class TestExecutionProvider:
    """Test ExecutionProvider enum functionality."""

    def test_execution_provider_values(self):
        """Test ExecutionProvider enum has correct provider_name values."""
        from notolog.modules.ondevice_llm.model_helper import ExecutionProvider

        # Test provider_name (used for ONNX Runtime)
        assert ExecutionProvider.CPU.provider_name == "cpu"
        assert ExecutionProvider.CUDA.provider_name == "cuda"
        assert ExecutionProvider.DML.provider_name == "DML"
        assert ExecutionProvider.OPENVINO.provider_name == "OpenVINO"
        assert ExecutionProvider.QNN.provider_name == "QNN"
        assert ExecutionProvider.COREML.provider_name == "CoreML"
        assert ExecutionProvider.TENSORRT_RTX.provider_name == "NvTensorRtRtx"

    def test_execution_provider_display_names(self):
        """Test ExecutionProvider enum has correct display names."""
        from notolog.modules.ondevice_llm.model_helper import ExecutionProvider

        assert "CPU" in ExecutionProvider.CPU.display_name
        assert "CUDA" in ExecutionProvider.CUDA.display_name
        assert "DirectML" in ExecutionProvider.DML.display_name
        assert "OpenVINO" in ExecutionProvider.OPENVINO.display_name
        assert "CoreML" in ExecutionProvider.COREML.display_name

    def test_default_provider(self):
        """Test default provider is CPU."""
        from notolog.modules.ondevice_llm.model_helper import ExecutionProvider

        assert ExecutionProvider.default() == ExecutionProvider.CPU

    def test_get_available_providers_includes_cpu(self):
        """Test that CPU is always in available providers."""
        from notolog.modules.ondevice_llm.model_helper import ExecutionProvider

        providers = ExecutionProvider.get_available_providers()
        assert ExecutionProvider.CPU in providers

    def test_get_available_providers_platform_specific(self):
        """Test platform-specific providers are returned correctly."""
        from notolog.modules.ondevice_llm.model_helper import ExecutionProvider

        providers = ExecutionProvider.get_available_providers()
        system = platform.system().lower()

        if system == "windows":
            assert ExecutionProvider.DML in providers
            assert ExecutionProvider.CUDA in providers
        elif system == "linux":
            assert ExecutionProvider.CUDA in providers
        elif system == "darwin":
            assert ExecutionProvider.COREML in providers

    def test_from_string(self):
        """Test from_string class method."""
        from notolog.modules.ondevice_llm.model_helper import ExecutionProvider

        assert ExecutionProvider.from_string("cpu") == ExecutionProvider.CPU
        assert ExecutionProvider.from_string("cuda") == ExecutionProvider.CUDA
        assert ExecutionProvider.from_string("DML") == ExecutionProvider.DML
        assert ExecutionProvider.from_string("OpenVINO") == ExecutionProvider.OPENVINO
        # Test fallback to default for unknown
        assert ExecutionProvider.from_string("unknown") == ExecutionProvider.CPU
        # Test by enum name
        assert ExecutionProvider.from_string("CUDA") == ExecutionProvider.CUDA


class TestModelHelperCore:
    """Core functionality tests for ONNX model helper."""

    def test_convert_temperature(self):
        """Test temperature conversion from int to float."""
        from notolog.modules.ondevice_llm.model_helper import ModelHelper

        assert ModelHelper.convert_temperature(0) == 0.0
        assert ModelHelper.convert_temperature(20) == 0.20
        assert ModelHelper.convert_temperature(80) == 0.80
        assert ModelHelper.convert_temperature(100) == 1.00

    def test_truncate_string(self):
        """Test string truncation."""
        from notolog.modules.ondevice_llm.model_helper import ModelHelper

        # Short string - no truncation
        assert ModelHelper.truncate_string("short", 32) == "short"

        # Long string - should truncate
        long_str = "a" * 100
        truncated = ModelHelper.truncate_string(long_str, 32)
        assert len(truncated) <= 32
        assert "..." in truncated

    def test_is_model_loaded_false_by_default(self):
        """Test that is_model_loaded returns False when no model is set."""
        from notolog.modules.ondevice_llm.model_helper import ModelHelper

        with patch('os.path.isdir', return_value=True):
            with patch('os.listdir', return_value=['model.onnx']):
                ModelHelper._instance = None
                helper = ModelHelper(model_path="/fake/path", search_options={})

        assert helper.is_model_loaded() is False

    def test_is_model_loaded_true_when_set(self):
        """Test that is_model_loaded returns True when model is set."""
        from notolog.modules.ondevice_llm.model_helper import ModelHelper

        with patch('os.path.isdir', return_value=True):
            with patch('os.listdir', return_value=['model.onnx']):
                ModelHelper._instance = None
                helper = ModelHelper(model_path="/fake/path", search_options={})

        # Manually set a mock model
        helper.model = MagicMock()
        assert helper.is_model_loaded() is True

    def test_cleanup_releases_resources(self):
        """Test that cleanup properly releases resources."""
        from notolog.modules.ondevice_llm.model_helper import ModelHelper

        with patch('os.path.isdir', return_value=True):
            with patch('os.listdir', return_value=['model.onnx']):
                ModelHelper._instance = None
                helper = ModelHelper(model_path="/fake/path", search_options={})

        # Set mock resources
        helper.model = MagicMock()
        helper.tokenizer = MagicMock()
        helper.tokenizer_stream = MagicMock()
        helper.generator = MagicMock()

        # Cleanup
        helper.cleanup()

        # Verify cleanup
        assert helper.model is None
        assert helper.tokenizer is None
        assert helper.tokenizer_stream is None
        assert helper.generator is None

    def test_search_options_filtering(self):
        """Test that only supported search options are kept."""
        from notolog.modules.ondevice_llm.model_helper import ModelHelper

        with patch('os.path.isdir', return_value=True):
            with patch('os.listdir', return_value=['model.onnx']):
                ModelHelper._instance = None

                search_options = {
                    'temperature': 80,
                    'max_length': 2048,
                    'unsupported_option': 'value',
                }

                helper = ModelHelper(model_path="/fake/path", search_options=search_options)

        # Unsupported option should be filtered out
        assert 'unsupported_option' not in helper.search_options
        # Supported options should be present
        assert 'temperature' in helper.search_options
        assert 'max_length' in helper.search_options
        # Temperature should be converted to float
        assert helper.search_options['temperature'] == 0.80

    def test_model_path_validation(self):
        """Test model path validation."""
        from notolog.modules.ondevice_llm.model_helper import ModelHelper

        # Invalid path - not a directory
        with patch('os.path.isdir', return_value=False):
            ModelHelper._instance = None
            helper = ModelHelper(model_path="/fake/path", search_options={})
            assert helper.model_path is None

        # Valid directory but no ONNX files
        with patch('os.path.isdir', return_value=True):
            with patch('os.listdir', return_value=['config.json']):
                ModelHelper._instance = None
                helper = ModelHelper(model_path="/fake/path", search_options={})
                assert helper.model_path is None

        # Valid directory with ONNX files
        with patch('os.path.isdir', return_value=True):
            with patch('os.listdir', return_value=['model.onnx', 'config.json']):
                with patch('os.path.isfile', return_value=True):
                    ModelHelper._instance = None
                    helper = ModelHelper(model_path="/fake/path", search_options={})
                    assert helper.model_path == "/fake/path"

    def test_has_model_files_with_onnx(self):
        """Test _has_model_files returns True when .onnx files exist."""
        from notolog.modules.ondevice_llm.model_helper import ModelHelper

        with patch('os.path.isdir', return_value=True):
            with patch('os.listdir', return_value=['model.onnx']):
                with patch('os.path.isfile', return_value=True):
                    ModelHelper._instance = None
                    helper = ModelHelper(model_path="/fake/path", search_options={})
                    assert helper._has_model_files("/fake/path") is True

    def test_has_model_files_without_onnx(self):
        """Test _has_model_files returns False when no .onnx files exist."""
        from notolog.modules.ondevice_llm.model_helper import ModelHelper

        with patch('os.path.isdir', return_value=True):
            with patch('os.listdir', return_value=['model.onnx']):
                with patch('os.path.isfile', return_value=True):
                    ModelHelper._instance = None
                    helper = ModelHelper(model_path="/fake/path", search_options={})

        # Now test with no onnx files
        with patch('os.listdir', return_value=['config.json', 'tokenizer.json']):
            with patch('os.path.isfile', return_value=True):
                assert helper._has_model_files("/another/path") is False

    def test_onnx_subdirectory_with_genai_config(self):
        """Test onnx/ subdirectory is used when it has genai_config.json."""
        from notolog.modules.ondevice_llm.model_helper import ModelHelper
        import os

        fake_path = "/fake/path"
        onnx_subdir = os.path.join(fake_path, "onnx")

        def mock_isdir(path):
            # Normalize for cross-platform comparison
            norm_path = os.path.normpath(path)
            return norm_path in [os.path.normpath(fake_path), os.path.normpath(onnx_subdir)]

        def mock_listdir(path):
            norm_path = os.path.normpath(path)
            if norm_path == os.path.normpath(fake_path):
                return ["config.json", "onnx"]  # No .onnx in root
            elif norm_path == os.path.normpath(onnx_subdir):
                return ["model.onnx", "genai_config.json"]
            return []

        def mock_isfile(path):
            return path.endswith('.onnx') or path.endswith('.json')

        with patch('os.path.isdir', side_effect=mock_isdir):
            with patch('os.listdir', side_effect=mock_listdir):
                with patch('os.path.isfile', side_effect=mock_isfile):
                    ModelHelper._instance = None
                    helper = ModelHelper(model_path=fake_path, search_options={})
                    # Compare normalized paths for cross-platform compatibility
                    assert os.path.normpath(helper.model_path) == os.path.normpath(onnx_subdir)

    def test_onnx_subdirectory_without_genai_config(self):
        """Test onnx/ subdirectory is rejected when genai_config.json is missing."""
        from notolog.modules.ondevice_llm.model_helper import ModelHelper
        import os

        fake_path = "/fake/path"
        onnx_subdir = os.path.join(fake_path, "onnx")

        def mock_isdir(path):
            norm_path = os.path.normpath(path)
            return norm_path in [os.path.normpath(fake_path), os.path.normpath(onnx_subdir)]

        def mock_listdir(path):
            norm_path = os.path.normpath(path)
            if norm_path == os.path.normpath(fake_path):
                return ["config.json", "onnx"]  # No .onnx in root
            elif norm_path == os.path.normpath(onnx_subdir):
                return ["model.onnx"]  # No genai_config.json
            return []

        def mock_isfile(path):
            # genai_config.json does not exist
            if 'genai_config.json' in path:
                return False
            return path.endswith('.onnx') or path.endswith('.json')

        with patch('os.path.isdir', side_effect=mock_isdir):
            with patch('os.listdir', side_effect=mock_listdir):
                with patch('os.path.isfile', side_effect=mock_isfile):
                    ModelHelper._instance = None
                    helper = ModelHelper(model_path=fake_path, search_options={})
                    # Should reject the model - transformers.js style without genai_config.json
                    assert helper.model_path is None

    def test_generate_output_v011_api(self):
        """Test generate_output follows v0.11.0+ API pattern."""
        from notolog.modules.ondevice_llm.model_helper import ModelHelper

        with patch('os.path.isdir', return_value=True):
            with patch('os.listdir', return_value=['model.onnx']):
                ModelHelper._instance = None
                helper = ModelHelper(model_path="/fake/path", search_options={})

        # Mock generator that is done
        mock_generator = MagicMock()
        mock_generator.is_done.return_value = True
        helper.generator = mock_generator

        # Should return None when done (v0.11.0+ behavior)
        result = helper.generate_output()
        assert result is None

        # Verify generate_next_token was called first
        mock_generator.generate_next_token.assert_called_once()
        # Verify is_done was checked after
        mock_generator.is_done.assert_called_once()

    def test_generate_output_returns_token_when_not_done(self):
        """Test generate_output returns token when generation not complete."""
        from notolog.modules.ondevice_llm.model_helper import ModelHelper

        with patch('os.path.isdir', return_value=True):
            with patch('os.listdir', return_value=['model.onnx']):
                ModelHelper._instance = None
                helper = ModelHelper(model_path="/fake/path", search_options={})

        # Mock generator that is not done
        mock_generator = MagicMock()
        mock_generator.is_done.return_value = False
        mock_generator.get_next_tokens.return_value = [123]

        mock_tokenizer_stream = MagicMock()
        mock_tokenizer_stream.decode.return_value = "Hello"

        helper.generator = mock_generator
        helper.tokenizer_stream = mock_tokenizer_stream

        # Should return decoded token
        result = helper.generate_output()
        assert result == "Hello"

        # Verify correct API call sequence
        mock_generator.generate_next_token.assert_called_once()
        mock_generator.is_done.assert_called_once()
        mock_generator.get_next_tokens.assert_called_once()
        mock_tokenizer_stream.decode.assert_called_once_with(123)

    def test_init_generator_retries_with_smaller_max_length(self):
        """Test init_generator retries with smaller max_length on memory error."""
        from notolog.modules.ondevice_llm.model_helper import ModelHelper

        with patch('os.path.isdir', return_value=True):
            with patch('os.listdir', return_value=['model.onnx']):
                ModelHelper._instance = None
                helper = ModelHelper(model_path="/fake/path", search_options={})

        # Mock model
        helper.model = MagicMock()

        # Track max_length values used in calls
        max_lengths_tried = []

        def mock_create_generator(input_tokens, options):
            max_lengths_tried.append(options.get('max_length'))
            if options.get('max_length', 4096) > 1024:
                raise RuntimeError("Could not allocate the key-value cache buffer")
            # Success with max_length <= 1024
            return MagicMock()

        helper._create_generator = mock_create_generator

        # Call with max_length=4096, should retry and succeed with 1024
        search_options = {'max_length': 4096, 'temperature': 0.7}
        result = helper.init_generator([1, 2, 3], search_options)

        assert result is not None
        # Should have tried 4096, 2048, then succeeded with 1024
        assert 4096 in max_lengths_tried
        assert 2048 in max_lengths_tried
        assert 1024 in max_lengths_tried

    def test_init_generator_raises_on_non_memory_error(self):
        """Test init_generator raises immediately on non-memory errors."""
        from notolog.modules.ondevice_llm.model_helper import ModelHelper

        with patch('os.path.isdir', return_value=True):
            with patch('os.listdir', return_value=['model.onnx']):
                ModelHelper._instance = None
                helper = ModelHelper(model_path="/fake/path", search_options={})

        helper.model = MagicMock()

        def mock_create_generator(input_tokens, options):
            raise RuntimeError("Invalid model configuration")

        helper._create_generator = mock_create_generator

        with pytest.raises(RuntimeError, match="Invalid model configuration"):
            helper.init_generator([1, 2, 3], {'max_length': 4096})

    def test_init_generator_retries_on_cublas_error(self):
        """Test init_generator retries with smaller max_length on CUBLAS errors."""
        from notolog.modules.ondevice_llm.model_helper import ModelHelper

        with patch('os.path.isdir', return_value=True):
            with patch('os.listdir', return_value=['model.onnx']):
                ModelHelper._instance = None
                helper = ModelHelper(model_path="/fake/path", search_options={})

        helper.model = MagicMock()

        max_lengths_tried = []

        def mock_create_generator(input_tokens, options):
            max_lengths_tried.append(options.get('max_length'))
            if options.get('max_length', 4096) > 1024:
                raise RuntimeError("CUBLAS failure 3: CUBLAS_STATUS_ALLOC_FAILED")
            return MagicMock()

        helper._create_generator = mock_create_generator

        result = helper.init_generator([1, 2, 3], {'max_length': 4096})

        assert result is not None
        assert 4096 in max_lengths_tried
        assert 1024 in max_lengths_tried


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
