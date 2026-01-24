"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Contains async integration tests for the llama_cpp module.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

import pytest
import asyncio
import logging
from unittest.mock import MagicMock, patch

from notolog.app_config import AppConfig

from .. import is_module_available

# Explicitly check if the module is available
if is_module_available('llama_cpp'):
    from notolog.modules.llama_cpp.model_helper import ModelHelper
else:
    from PySide6.QtCore import QObject as ModelHelper


class TestAsyncIntegration:
    """Test async integration and event loop handling."""

    @pytest.fixture(scope="function", autouse=True)
    def test_obj_app_config(self, mocker):
        """Mock AppConfig to suppress logging during tests."""
        mocker.patch.object(AppConfig, 'get_logger_level', return_value=logging.NOTSET)
        _app_config = AppConfig()
        _app_config.set_test_mode(True)
        yield _app_config

    @pytest.mark.skipif(not is_module_available('llama_cpp'), reason="llama_cpp module not available")
    @pytest.mark.asyncio
    async def test_async_wrap_iterator_yields_control(self, mocker, tmp_path):
        """Test that async_wrap_iterator properly yields control to event loop."""
        # Create a dummy model file
        dummy_model = tmp_path / "test.gguf"
        dummy_model.touch()

        # Mock the singleton to get a fresh instance
        ModelHelper._instance = None

        helper = ModelHelper(model_path=str(dummy_model), search_options={})

        # Create mock iterator with multiple chunks
        mock_data = [
            {'choices': [{'delta': {'role': 'assistant'}}]},
            {'choices': [{'delta': {'content': 'Hello'}}]},
            {'choices': [{'delta': {'content': ' world'}}]},
            {'choices': [{'delta': {'finish_reason': 'stop'}}]},
        ]

        def mock_iterator():
            for item in mock_data:
                yield item

        # Track how many times asyncio.sleep was called
        sleep_count = 0
        original_sleep = asyncio.sleep

        async def counted_sleep(delay):
            nonlocal sleep_count
            sleep_count += 1
            await original_sleep(delay)

        # Collect outputs
        outputs = []
        with patch('asyncio.sleep', side_effect=counted_sleep):
            async for output in helper.async_wrap_iterator(mock_iterator()):
                outputs.append(output)

        # Should have yielded control multiple times
        assert sleep_count >= len(mock_data), "Should yield control for each chunk"
        # Should have correct outputs (role is empty, content is preserved)
        assert '' in outputs  # Role output
        assert 'Hello' in outputs
        assert ' world' in outputs

    @pytest.mark.skipif(not is_module_available('llama_cpp'), reason="llama_cpp module not available")
    @pytest.mark.asyncio
    async def test_generate_output_stops_correctly(self, mocker, tmp_path):
        """Test that generate_output raises StopAsyncIteration when done."""
        dummy_model = tmp_path / "test.gguf"
        dummy_model.touch()

        ModelHelper._instance = None
        helper = ModelHelper(model_path=str(dummy_model), search_options={})

        # Empty iterator
        def empty_iterator():
            return
            yield  # Never reached

        # Should raise StopAsyncIteration
        with pytest.raises(StopAsyncIteration):
            await helper.generate_output(empty_iterator())

    @pytest.mark.skipif(not is_module_available('llama_cpp'), reason="llama_cpp module not available")
    def test_cleanup_handles_errors_gracefully(self, mocker, tmp_path):
        """Test that cleanup handles errors without crashing."""
        dummy_model = tmp_path / "test.gguf"
        dummy_model.touch()

        ModelHelper._instance = None
        helper = ModelHelper(model_path=str(dummy_model), search_options={})

        # Create a mock model that raises on close
        mock_model = MagicMock()
        mock_model.close = MagicMock(side_effect=RuntimeError("Close failed"))
        helper.model = mock_model

        # Should not raise, should handle error gracefully
        helper.cleanup()

        # Model should still be set to None despite error
        assert helper.model is None

    @pytest.mark.skipif(not is_module_available('llama_cpp'), reason="llama_cpp module not available")
    def test_init_model_with_optimal_threads(self, mocker, tmp_path):
        """Test that init_model uses optimal thread count."""
        import multiprocessing

        dummy_model = tmp_path / "test.gguf"
        dummy_model.touch()

        ModelHelper._instance = None
        helper = ModelHelper(model_path=str(dummy_model), search_options={})

        # Mock Llama constructor
        mock_llama = mocker.patch('notolog.modules.llama_cpp.model_helper.Llama')

        try:
            helper.init_model()
        except Exception:
            pass  # We just want to check the call

        # Verify it was called with thread count
        expected_threads = multiprocessing.cpu_count()
        mock_llama.assert_called_once()
        call_kwargs = mock_llama.call_args[1]
        assert call_kwargs['n_threads'] == expected_threads
        assert call_kwargs['n_threads_batch'] == expected_threads
        assert call_kwargs['n_batch'] == 512
        assert call_kwargs['n_ubatch'] == 512

    @pytest.mark.skipif(not is_module_available('llama_cpp'), reason="llama_cpp module not available")
    @pytest.mark.asyncio
    async def test_concurrent_async_operations(self, mocker, tmp_path):
        """Test that multiple async operations can run concurrently."""
        dummy_model = tmp_path / "test.gguf"
        dummy_model.touch()

        ModelHelper._instance = None
        helper = ModelHelper(model_path=str(dummy_model), search_options={})

        # Create multiple mock iterators
        async def process_iterator(data):
            def iterator():
                for item in data:
                    yield item

            results = []
            async for output in helper.async_wrap_iterator(iterator()):
                results.append(output)
            return results

        # Run multiple iterations concurrently
        data1 = [{'choices': [{'delta': {'content': 'A'}}]}]
        data2 = [{'choices': [{'delta': {'content': 'B'}}]}]
        data3 = [{'choices': [{'delta': {'content': 'C'}}]}]

        results = await asyncio.gather(
            process_iterator(data1),
            process_iterator(data2),
            process_iterator(data3),
        )

        # All should complete successfully
        assert len(results) == 3
        assert 'A' in results[0]
        assert 'B' in results[1]
        assert 'C' in results[2]
