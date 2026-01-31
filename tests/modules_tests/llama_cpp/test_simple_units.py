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


class TestModelHelperPlatformDetection:
    """Tests for macOS platform detection and GPU layer configuration."""

    def test_is_macos_on_darwin(self):
        """Test is_macos returns True on darwin platform."""
        from notolog.modules.llama_cpp.model_helper import ModelHelper

        with patch('notolog.modules.llama_cpp.model_helper.sys.platform', 'darwin'):
            assert ModelHelper.is_macos() is True

    def test_is_macos_on_linux(self):
        """Test is_macos returns False on linux platform."""
        from notolog.modules.llama_cpp.model_helper import ModelHelper

        with patch('notolog.modules.llama_cpp.model_helper.sys.platform', 'linux'):
            assert ModelHelper.is_macos() is False

    def test_is_macos_on_windows(self):
        """Test is_macos returns False on Windows platform."""
        from notolog.modules.llama_cpp.model_helper import ModelHelper

        with patch('notolog.modules.llama_cpp.model_helper.sys.platform', 'win32'):
            assert ModelHelper.is_macos() is False

    def test_is_apple_silicon_on_arm64_mac(self):
        """Test is_apple_silicon returns True on ARM64 macOS (M1/M2/M3/M4)."""
        from notolog.modules.llama_cpp.model_helper import ModelHelper

        with patch('notolog.modules.llama_cpp.model_helper.sys.platform', 'darwin'):
            with patch('platform.machine', return_value='arm64'):
                assert ModelHelper.is_apple_silicon() is True

    def test_is_apple_silicon_on_intel_mac(self):
        """Test is_apple_silicon returns False on Intel macOS (x86_64)."""
        from notolog.modules.llama_cpp.model_helper import ModelHelper

        with patch('notolog.modules.llama_cpp.model_helper.sys.platform', 'darwin'):
            with patch('platform.machine', return_value='x86_64'):
                assert ModelHelper.is_apple_silicon() is False

    def test_is_apple_silicon_on_linux_arm(self):
        """Test is_apple_silicon returns False on Linux ARM."""
        from notolog.modules.llama_cpp.model_helper import ModelHelper

        with patch('notolog.modules.llama_cpp.model_helper.sys.platform', 'linux'):
            with patch('platform.machine', return_value='aarch64'):
                assert ModelHelper.is_apple_silicon() is False

    def test_cancel_loading_sets_event(self):
        """Test that cancel_loading sets the cancellation event."""
        from notolog.modules.llama_cpp.model_helper import ModelHelper
        from threading import Event

        with patch('os.path.isfile', return_value=True):
            ModelHelper._instance = None
            helper = ModelHelper(model_path="/fake/path.gguf", search_options={})

        # Simulate a cancel event being active (as if init_model was called)
        helper._cancel_event = Event()
        assert not helper._cancel_event.is_set()

        # Call cancel_loading
        helper.cancel_loading()

        # Verify the event is set
        assert helper._cancel_event.is_set()

    def test_cancel_loading_no_event_graceful(self):
        """Test that cancel_loading handles None event gracefully."""
        from notolog.modules.llama_cpp.model_helper import ModelHelper

        with patch('os.path.isfile', return_value=True):
            ModelHelper._instance = None
            helper = ModelHelper(model_path="/fake/path.gguf", search_options={})

        # Ensure no event is set
        helper._cancel_event = None

        # Call cancel_loading - should not raise
        helper.cancel_loading()  # No exception expected

    def test_init_model_gpu_layers_apple_silicon(self):
        """Test that init_model uses Metal GPU (-1 layers) on Apple Silicon when Auto."""
        from notolog.modules.llama_cpp.model_helper import ModelHelper

        with patch('os.path.isfile', return_value=True):
            ModelHelper._instance = None
            # n_gpu_layers=None means Auto mode
            helper = ModelHelper(model_path="/fake/path.gguf", n_gpu_layers=None, search_options={})

        with patch.object(ModelHelper, 'is_macos', return_value=True):
            with patch.object(ModelHelper, 'is_apple_silicon', return_value=True):
                with patch('notolog.modules.llama_cpp.model_helper.Llama') as mock_llama:
                    helper.init_model()
                    mock_llama.assert_called_once()
                    call_kwargs = mock_llama.call_args[1]
                    assert call_kwargs['n_gpu_layers'] == -1

    def test_init_model_gpu_layers_intel_mac_default(self):
        """Test that init_model uses CPU (0 layers) on Intel Mac when Auto."""
        from notolog.modules.llama_cpp.model_helper import ModelHelper

        with patch('os.path.isfile', return_value=True):
            ModelHelper._instance = None
            # n_gpu_layers=None means Auto mode
            helper = ModelHelper(model_path="/fake/path.gguf", n_gpu_layers=None, search_options={})

        with patch.object(ModelHelper, 'is_macos', return_value=True):
            with patch.object(ModelHelper, 'is_apple_silicon', return_value=False):
                with patch('notolog.modules.llama_cpp.model_helper.Llama') as mock_llama:
                    helper.init_model()
                    mock_llama.assert_called_once()
                    call_kwargs = mock_llama.call_args[1]
                    assert call_kwargs['n_gpu_layers'] == 0

    def test_init_model_gpu_layers_explicit_setting(self):
        """Test that init_model respects explicit n_gpu_layers setting from UI."""
        from notolog.modules.llama_cpp.model_helper import ModelHelper

        with patch('os.path.isfile', return_value=True):
            ModelHelper._instance = None
            # Explicitly set n_gpu_layers=-1 (all layers on GPU)
            helper = ModelHelper(model_path="/fake/path.gguf", n_gpu_layers=-1, search_options={})

        # Even on Intel Mac, if user explicitly sets -1, use it
        with patch.object(ModelHelper, 'is_macos', return_value=True):
            with patch.object(ModelHelper, 'is_apple_silicon', return_value=False):
                with patch('notolog.modules.llama_cpp.model_helper.Llama') as mock_llama:
                    helper.init_model()
                    mock_llama.assert_called_once()
                    call_kwargs = mock_llama.call_args[1]
                    assert call_kwargs['n_gpu_layers'] == -1

    def test_init_model_gpu_layers_cpu_only_setting(self):
        """Test that n_gpu_layers=0 forces CPU-only mode."""
        from notolog.modules.llama_cpp.model_helper import ModelHelper

        with patch('os.path.isfile', return_value=True):
            ModelHelper._instance = None
            # Explicitly set n_gpu_layers=0 (CPU only)
            helper = ModelHelper(model_path="/fake/path.gguf", n_gpu_layers=0, search_options={})

        # Even on Apple Silicon, if user explicitly sets 0, use CPU
        with patch.object(ModelHelper, 'is_macos', return_value=True):
            with patch.object(ModelHelper, 'is_apple_silicon', return_value=True):
                with patch('notolog.modules.llama_cpp.model_helper.Llama') as mock_llama:
                    helper.init_model()
                    mock_llama.assert_called_once()
                    call_kwargs = mock_llama.call_args[1]
                    assert call_kwargs['n_gpu_layers'] == 0

    def test_init_model_gpu_layers_linux(self):
        """Test that init_model uses CPU (0 layers) on Linux when Auto."""
        from notolog.modules.llama_cpp.model_helper import ModelHelper

        with patch('os.path.isfile', return_value=True):
            ModelHelper._instance = None
            helper = ModelHelper(model_path="/fake/path.gguf", n_gpu_layers=None, search_options={})

        with patch.object(ModelHelper, 'is_macos', return_value=False):
            with patch('notolog.modules.llama_cpp.model_helper.Llama') as mock_llama:
                helper.init_model()
                mock_llama.assert_called_once()
                call_kwargs = mock_llama.call_args[1]
                assert call_kwargs['n_gpu_layers'] == 0

    def test_init_model_checks_cancellation(self):
        """Test that init_model checks for cancellation before loading."""
        from notolog.modules.llama_cpp.model_helper import ModelHelper
        from threading import Event
        import asyncio

        with patch('os.path.isfile', return_value=True):
            ModelHelper._instance = None
            helper = ModelHelper(model_path="/fake/path.gguf", search_options={})

        # Mock Llama to check if it gets called
        with patch('notolog.modules.llama_cpp.model_helper.Llama') as mock_llama:
            # Patch Event creation to return a pre-set event
            def create_preset_event():
                event = Event()
                event.set()  # Pre-set the cancellation
                return event

            with patch('notolog.modules.llama_cpp.model_helper.Event', create_preset_event):
                with pytest.raises(asyncio.CancelledError):
                    helper.init_model()

            # Llama should NOT have been called since we cancelled first
            mock_llama.assert_not_called()


class TestUpgradeScenarios:
    """
    Tests for upgrade scenarios where users upgrade from previous versions
    that didn't have the gpu_layers configuration option.

    These tests ensure backward compatibility and that Auto mode works correctly
    when the new config value is missing or None (default for new installs and upgrades).
    """

    def test_upgrade_scenario_no_gpu_layers_param_apple_silicon(self):
        """
        Test upgrade scenario: User upgrades from version without gpu_layers setting.
        On Apple Silicon, Auto mode should enable Metal GPU (-1 layers).
        """
        from notolog.modules.llama_cpp.model_helper import ModelHelper

        with patch('os.path.isfile', return_value=True):
            ModelHelper._instance = None
            # Simulate upgrade: n_gpu_layers NOT provided (uses default None)
            helper = ModelHelper(model_path="/fake/path.gguf", search_options={})

        # Verify setting is None (Auto mode)
        assert helper.n_gpu_layers_setting is None

        with patch.object(ModelHelper, 'is_macos', return_value=True):
            with patch.object(ModelHelper, 'is_apple_silicon', return_value=True):
                with patch('notolog.modules.llama_cpp.model_helper.Llama') as mock_llama:
                    helper.init_model()
                    mock_llama.assert_called_once()
                    call_kwargs = mock_llama.call_args[1]
                    assert call_kwargs['n_gpu_layers'] == -1, \
                        "Auto mode should use Metal GPU (-1) on Apple Silicon"

    def test_upgrade_scenario_no_gpu_layers_param_intel_mac(self):
        """
        Test upgrade scenario: On Intel Mac, Auto mode should use CPU-only (0).
        """
        from notolog.modules.llama_cpp.model_helper import ModelHelper

        with patch('os.path.isfile', return_value=True):
            ModelHelper._instance = None
            # Simulate upgrade: n_gpu_layers NOT provided
            helper = ModelHelper(model_path="/fake/path.gguf", search_options={})

        assert helper.n_gpu_layers_setting is None

        with patch.object(ModelHelper, 'is_macos', return_value=True):
            with patch.object(ModelHelper, 'is_apple_silicon', return_value=False):
                with patch('notolog.modules.llama_cpp.model_helper.Llama') as mock_llama:
                    helper.init_model()
                    mock_llama.assert_called_once()
                    call_kwargs = mock_llama.call_args[1]
                    assert call_kwargs['n_gpu_layers'] == 0, \
                        "Auto mode should use CPU-only (0) on Intel Mac"

    def test_upgrade_scenario_no_gpu_layers_param_linux(self):
        """
        Test upgrade scenario: On Linux, Auto mode should use CPU-only (0).
        """
        from notolog.modules.llama_cpp.model_helper import ModelHelper

        with patch('os.path.isfile', return_value=True):
            ModelHelper._instance = None
            # Simulate upgrade: n_gpu_layers NOT provided
            helper = ModelHelper(model_path="/fake/path.gguf", search_options={})

        assert helper.n_gpu_layers_setting is None

        with patch.object(ModelHelper, 'is_macos', return_value=False):
            with patch('notolog.modules.llama_cpp.model_helper.Llama') as mock_llama:
                helper.init_model()
                mock_llama.assert_called_once()
                call_kwargs = mock_llama.call_args[1]
                assert call_kwargs['n_gpu_layers'] == 0, \
                    "Auto mode should use CPU-only (0) on Linux"

    def test_upgrade_scenario_explicit_none_works_as_auto(self):
        """
        Test that explicitly passing n_gpu_layers=None works the same as not passing it.
        This is important for the settings system which may pass None for 'Auto'.
        """
        from notolog.modules.llama_cpp.model_helper import ModelHelper

        with patch('os.path.isfile', return_value=True):
            ModelHelper._instance = None
            # Explicitly pass n_gpu_layers=None (as settings would for "Auto")
            helper = ModelHelper(model_path="/fake/path.gguf", n_gpu_layers=None, search_options={})

        assert helper.n_gpu_layers_setting is None

        with patch.object(ModelHelper, 'is_macos', return_value=True):
            with patch.object(ModelHelper, 'is_apple_silicon', return_value=True):
                with patch('notolog.modules.llama_cpp.model_helper.Llama') as mock_llama:
                    helper.init_model()
                    mock_llama.assert_called_once()
                    call_kwargs = mock_llama.call_args[1]
                    assert call_kwargs['n_gpu_layers'] == -1, \
                        "Explicit None should work as Auto mode"

    def test_upgrade_preserves_explicit_cpu_setting(self):
        """
        Test that when user explicitly sets CPU-only (0), it's preserved even on Apple Silicon.
        """
        from notolog.modules.llama_cpp.model_helper import ModelHelper

        with patch('os.path.isfile', return_value=True):
            ModelHelper._instance = None
            # User explicitly wants CPU-only
            helper = ModelHelper(model_path="/fake/path.gguf", n_gpu_layers=0, search_options={})

        assert helper.n_gpu_layers_setting == 0

        # Even on Apple Silicon, explicit 0 should be respected
        with patch.object(ModelHelper, 'is_macos', return_value=True):
            with patch.object(ModelHelper, 'is_apple_silicon', return_value=True):
                with patch('notolog.modules.llama_cpp.model_helper.Llama') as mock_llama:
                    helper.init_model()
                    mock_llama.assert_called_once()
                    call_kwargs = mock_llama.call_args[1]
                    assert call_kwargs['n_gpu_layers'] == 0, \
                        "User's explicit CPU-only (0) setting should be preserved"

    def test_upgrade_preserves_explicit_gpu_setting_on_intel(self):
        """
        Test that when user explicitly sets GPU (-1), it's used even on Intel Mac.
        """
        from notolog.modules.llama_cpp.model_helper import ModelHelper

        with patch('os.path.isfile', return_value=True):
            ModelHelper._instance = None
            # User explicitly wants Metal on Intel Mac
            helper = ModelHelper(model_path="/fake/path.gguf", n_gpu_layers=-1, search_options={})

        assert helper.n_gpu_layers_setting == -1

        # Even on Intel Mac, explicit -1 should be respected
        with patch.object(ModelHelper, 'is_macos', return_value=True):
            with patch.object(ModelHelper, 'is_apple_silicon', return_value=False):
                with patch('notolog.modules.llama_cpp.model_helper.Llama') as mock_llama:
                    helper.init_model()
                    mock_llama.assert_called_once()
                    call_kwargs = mock_llama.call_args[1]
                    assert call_kwargs['n_gpu_layers'] == -1, \
                        "User's explicit GPU (-1) setting should be preserved on Intel Mac"

    def test_resolve_gpu_layers_returns_correct_values(self):
        """
        Test _resolve_gpu_layers method directly to verify the resolution logic.
        """
        from notolog.modules.llama_cpp.model_helper import ModelHelper

        # Test case 1: Explicit setting takes priority
        with patch('os.path.isfile', return_value=True):
            ModelHelper._instance = None
            helper = ModelHelper(model_path="/fake/path.gguf", n_gpu_layers=5, search_options={})
        assert helper._resolve_gpu_layers() == 5

        # Test case 2: None on Apple Silicon -> -1
        with patch('os.path.isfile', return_value=True):
            ModelHelper._instance = None
            helper = ModelHelper(model_path="/fake/path.gguf", n_gpu_layers=None, search_options={})
        with patch.object(ModelHelper, 'is_macos', return_value=True):
            with patch.object(ModelHelper, 'is_apple_silicon', return_value=True):
                assert helper._resolve_gpu_layers() == -1

        # Test case 3: None on Intel Mac -> 0
        with patch('os.path.isfile', return_value=True):
            ModelHelper._instance = None
            helper = ModelHelper(model_path="/fake/path.gguf", n_gpu_layers=None, search_options={})
        with patch.object(ModelHelper, 'is_macos', return_value=True):
            with patch.object(ModelHelper, 'is_apple_silicon', return_value=False):
                assert helper._resolve_gpu_layers() == 0

        # Test case 4: None on Linux -> 0
        with patch('os.path.isfile', return_value=True):
            ModelHelper._instance = None
            helper = ModelHelper(model_path="/fake/path.gguf", n_gpu_layers=None, search_options={})
        with patch.object(ModelHelper, 'is_macos', return_value=False):
            assert helper._resolve_gpu_layers() == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
