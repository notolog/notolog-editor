"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Simple unit tests for llama_cpp module without Qt dependencies

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License
"""

import pytest
from unittest.mock import MagicMock, patch

# Skip all tests if llama_cpp not available
llama_cpp = pytest.importorskip("llama_cpp", reason="llama_cpp module not available")


class TestModelHelperCore:
    """Core functionality tests without Qt dependencies."""

    def test_convert_temperature(self):
        """Test temperature conversion from int to float."""
        from notolog.modules.llama_cpp.model_helper import ModelHelper

        assert ModelHelper.convert_temperature(0) == 0.0
        assert ModelHelper.convert_temperature(20) == 0.20
        assert ModelHelper.convert_temperature(80) == 0.80
        assert ModelHelper.convert_temperature(100) == 1.00

    def test_truncate_string(self):
        """Test string truncation."""
        from notolog.modules.llama_cpp.model_helper import ModelHelper

        # Short string - no truncation
        assert ModelHelper.truncate_string("short", 32) == "short"

        # Long string - should truncate
        long_str = "a" * 100
        truncated = ModelHelper.truncate_string(long_str, 32)
        assert len(truncated) <= 32  # May be 31 or 32 depending on implementation
        assert "..." in truncated

    @pytest.mark.asyncio
    async def test_async_wrap_iterator_basic(self):
        """Test basic async iterator wrapping."""
        from notolog.modules.llama_cpp.model_helper import ModelHelper

        # Create instance without Qt
        with patch('os.path.isfile', return_value=True):
            ModelHelper._instance = None
            helper = ModelHelper(model_path="/fake/path.gguf", search_options={})

        # Mock iterator data
        mock_data = [
            {'choices': [{'delta': {'content': 'Hello'}}]},
            {'choices': [{'delta': {'content': ' world'}}]},
        ]

        def mock_iterator():
            for item in mock_data:
                yield item

        # Collect outputs
        outputs = []
        async for output in helper.async_wrap_iterator(mock_iterator()):
            outputs.append(output)

        assert 'Hello' in outputs
        assert ' world' in outputs

    @pytest.mark.asyncio
    async def test_async_wrap_iterator_role(self):
        """Test role handling in async iterator."""
        from notolog.modules.llama_cpp.model_helper import ModelHelper

        with patch('os.path.isfile', return_value=True):
            ModelHelper._instance = None
            helper = ModelHelper(model_path="/fake/path.gguf", search_options={})

        mock_data = [{'choices': [{'delta': {'role': 'assistant'}}]}]

        def mock_iterator():
            for item in mock_data:
                yield item

        outputs = []
        async for output in helper.async_wrap_iterator(mock_iterator()):
            outputs.append(output)

        # Role should return empty string
        assert outputs == ['']

    @pytest.mark.asyncio
    async def test_async_wrap_iterator_finish_reason(self):
        """Test finish_reason handling in async iterator."""
        from notolog.modules.llama_cpp.model_helper import ModelHelper

        with patch('os.path.isfile', return_value=True):
            ModelHelper._instance = None
            helper = ModelHelper(model_path="/fake/path.gguf", search_options={})

        mock_data = [{'choices': [{'delta': {'finish_reason': 'stop'}}]}]

        def mock_iterator():
            for item in mock_data:
                yield item

        outputs = []
        async for output in helper.async_wrap_iterator(mock_iterator()):
            outputs.append(output)

        # finish_reason should return empty string
        assert outputs == ['']

    @pytest.mark.asyncio
    async def test_generate_output_stops_on_empty(self):
        """Test that generate_output raises StopAsyncIteration when iterator is empty."""
        from notolog.modules.llama_cpp.model_helper import ModelHelper

        with patch('os.path.isfile', return_value=True):
            ModelHelper._instance = None
            helper = ModelHelper(model_path="/fake/path.gguf", search_options={})

        def empty_iterator():
            return
            yield  # Never reached

        with pytest.raises(StopAsyncIteration):
            await helper.generate_output(empty_iterator())

    def test_is_model_loaded_false_by_default(self):
        """Test that is_model_loaded returns False when no model is set."""
        from notolog.modules.llama_cpp.model_helper import ModelHelper

        with patch('os.path.isfile', return_value=True):
            ModelHelper._instance = None
            helper = ModelHelper(model_path="/fake/path.gguf", search_options={})

        assert helper.is_model_loaded() is False

    def test_is_model_loaded_true_when_set(self):
        """Test that is_model_loaded returns True when model is set."""
        from notolog.modules.llama_cpp.model_helper import ModelHelper

        with patch('os.path.isfile', return_value=True):
            ModelHelper._instance = None
            helper = ModelHelper(model_path="/fake/path.gguf", search_options={})

        # Manually set a mock model
        helper.model = MagicMock()
        assert helper.is_model_loaded() is True

    def test_cleanup_releases_resources(self):
        """Test that cleanup properly releases resources."""
        from notolog.modules.llama_cpp.model_helper import ModelHelper

        with patch('os.path.isfile', return_value=True):
            ModelHelper._instance = None
            helper = ModelHelper(model_path="/fake/path.gguf", search_options={})

        # Set mock resources
        helper.model = MagicMock()
        helper.generator = MagicMock()

        # Cleanup
        helper.cleanup()

        # Verify cleanup
        assert helper.model is None
        assert helper.generator is None

    def test_search_options_filtering(self):
        """Test that only supported search options are kept."""
        from notolog.modules.llama_cpp.model_helper import ModelHelper

        with patch('os.path.isfile', return_value=True):
            ModelHelper._instance = None

            search_options = {
                'temperature': 80,
                'top_p': 0.9,
                'unsupported_option': 'value',
            }

            helper = ModelHelper(model_path="/fake/path.gguf", search_options=search_options)

        # Unsupported option should be filtered out
        assert 'unsupported_option' not in helper.search_options
        # Supported options should be present
        assert 'temperature' in helper.search_options
        assert 'top_p' in helper.search_options
        # Temperature should be converted to float
        assert helper.search_options['temperature'] == 0.80


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
