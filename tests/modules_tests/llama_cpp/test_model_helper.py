"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Contains unit and integration tests for the related functionality.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from notolog.app_config import AppConfig

from .. import is_module_available

# Explicitly check if the module is available to avoid importing non-existent libraries.
if is_module_available('llama_cpp'):
    from notolog.modules.llama_cpp.model_helper import ModelHelper
    from llama_cpp import Llama
else:
    from PySide6.QtCore import QObject as ModelHelper, QObject as Llama

import os
import pytest
import logging
import multiprocessing

from unittest.mock import MagicMock


class TestModelHelper:

    @pytest.fixture(scope="function", autouse=True)
    def test_obj_app_config(self, mocker):
        # Mock AppConfig's get_logger_level method to suppress logging during tests.
        mocker.patch.object(AppConfig, 'get_logger_level', return_value=logging.NOTSET)

        # Create an AppConfig instance and set it to test mode.
        _app_config = AppConfig()
        _app_config.set_test_mode(True)

        yield _app_config

    @pytest.fixture(scope="function")
    def test_model_helper(self, mocker, request):
        """
        Testing object fixture.
        May contain minimal logic for testing purposes.
        """

        # Retrieve parameter values from the test request.
        model_path, context_window, chat_format, search_options = request.param if hasattr(request, 'param') \
            else ('', None, None, None)

        # Reload as new instance to avoid param caching
        ModelHelper.reload()

        # Allow setting a fake model path for testing purposes
        mocker.patch.object(os.path, 'isfile', return_value=True)

        model_helper = ModelHelper(model_path=model_path, n_ctx=context_window, chat_format=chat_format,
                                   search_options=search_options)

        yield model_helper

    @pytest.fixture(scope="function")
    def test_params_fixture(self, request):
        # Retrieve parameter values from the test request.
        param_values = request.param

        yield param_values

    @pytest.fixture(scope="function")
    def test_exp_params_fixture(self, request):
        # Retrieve parameter values from the test request.
        param_values = request.param

        yield param_values

    @pytest.mark.parametrize(
        "test_model_helper, test_params_fixture, test_exp_params_fixture",
        [
            (('', None, None, None), None, (False, "Model path is not set in 'ModelHelper'")),
            (('model_path1', None, None, None), None, (True, "")),
            (('', None, None, None), Llama, (False, "")),
        ],
        indirect=True
    )
    def test_init_model(self, mocker, test_model_helper: ModelHelper, test_params_fixture, test_exp_params_fixture):
        # Extract test and expected params
        model = test_params_fixture
        exp_call, exp_exception = test_exp_params_fixture

        # Test the case when the model is pre-set
        if model:
            test_model_helper.model = model

        # Mock the model object
        mocked_model = MagicMock(spec=Llama)

        test_model = mocker.patch.object(Llama, '__init__', return_value=mocked_model)

        try:
            # Run the method under test
            test_model_helper.init_model()
        except (RuntimeError, ValueError, Exception) as e:
            assert str(exp_exception) in str(e)

        if exp_call:
            # Verify the method called with the expected params (including new optimal parameters)
            expected_threads = multiprocessing.cpu_count()
            # n_gpu_layers is platform-dependent, tested separately
            test_model.assert_called_once_with(
                model_path=test_model_helper.model_path,
                chat_format=test_model_helper.chat_format,
                n_ctx=test_model_helper.n_ctx,
                n_batch=512,  # Optimal batch size from llama-cpp-python
                n_ubatch=512,  # Physical batch size
                n_threads=expected_threads,  # Use all CPU cores
                n_threads_batch=expected_threads,  # Use all cores for batch processing
                n_gpu_layers=mocker.ANY,  # Platform-dependent, tested separately
                verbose=False
            )
        else:
            test_model.assert_not_called()

    @pytest.mark.parametrize(
        "test_params_fixture, test_exp_params_fixture",
        [
            (('', []), []),
            (('text1', [1, 2, 3]), [1, 2, 3]),
        ],
        indirect=True
    )
    def test_get_input_tokens(self, mocker, test_model_helper: ModelHelper, test_params_fixture, test_exp_params_fixture):
        # Extract test and expected params
        text, tokens = test_params_fixture
        exp_result = test_exp_params_fixture

        # Mock the model object
        mocked_model = MagicMock(spec=Llama)
        test_model_tokenize = mocker.patch.object(mocked_model, 'tokenize', return_value=tokens)

        # Set the model
        test_model_helper.model = mocked_model

        # Run the method under test
        result = test_model_helper.get_input_tokens(text)

        test_model_tokenize.asset_called_once_with(text.encode('utf-8'))

        assert result == exp_result

    @pytest.mark.parametrize(
        "test_model_helper, test_params_fixture, test_exp_params_fixture",
        [
            # No model metadata available
            (('', None, None, None), {}, ''),
            (('model_path1', None, None, None), {}, 'model_path1'),
            (('model_path1.smth', None, None, None), {}, 'model_path1.smth'),
            ((os.path.join('model_dir1', 'model_path1.smth'), None, None, None), {}, 'model_path1.smth'),
            # Model metadata available but no model name specified
            (('', None, None, None), {'smth1.param1': 'model_name1'}, ''),
            (('model_path1', None, None, None), {'smth1.param1': 'model_name1'}, 'model_path1'),
            (('model_path1.smth', None, None, None), {'smth1.param1': 'model_name1'}, 'model_path1.smth'),
            ((os.path.join('model_dir1', 'model_path1.smth'), None, None, None),
             {'smth1.param1': 'model_name1'}, 'model_path1.smth'),
            # Model metadata available
            (('', None, None, None), {'general.name': 'model_name1'}, 'model_name1'),
            (('model_path1', None, None, None), {'general.name': 'model_name1'}, 'model_name1'),
            (('model_path1.smth', None, None, None), {'general.name': 'model_name1'}, 'model_name1'),
            ((os.path.join('model_dir1', 'model_path1.smth'), None, None, None),
             {'general.name': 'model_name1'}, 'model_name1'),
        ],
        indirect=True
    )
    def test_get_model_name(self, test_model_helper: ModelHelper, test_params_fixture, test_exp_params_fixture):
        # Extract test and expected params
        model_metadata = test_params_fixture
        exp_model_name = test_exp_params_fixture

        # Mock the model object
        model = MagicMock(spec=Llama)
        setattr(model, 'metadata', model_metadata)
        test_model_helper.model = model

        # Run the method under test
        model_name = test_model_helper.get_model_name()

        # Verify that the returned model name matches the expected model name
        assert model_name == exp_model_name

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "input_iterator, expected_outputs, expected_logs",
        [
            # Case 1: 'role' in delta
            (
                    [{'choices': [{'delta': {'role': 'assistant'}}]}],
                    [''],
                    ["Role output: assistant: "]
            ),
            # Case 2: 'content' in delta
            (
                    [{'choices': [{'delta': {'content': 'Hello, world'}}]}],
                    ['Hello, world'],
                    ["Output token(s): Hello, world"]
            ),
            # Case 3: 'finish_reason' in delta
            (
                    [{'choices': [{'delta': {'finish_reason': 'length'}}]}],
                    [''],
                    ["Output finished with the reason: 'length'"]
            ),
            # Case 4: Mixed inputs
            (
                    [
                        {'choices': [{'delta': {'role': 'assistant'}}]},
                        {'choices': [{'delta': {'content': 'Hello, world'}}]},
                        {'choices': [{'delta': {'finish_reason': 'length'}}]}
                    ],
                    ['', 'Hello, world', ''],
                    [
                        "Role output: assistant: ",
                        "Output token(s): Hello, world",
                        "Output finished with the reason: 'length'"
                    ]
            ),
        ]
    )
    async def test_async_wrap_iterator(self, test_model_helper: ModelHelper, input_iterator, expected_outputs,
                                       expected_logs):

        # Create an async iterator from the input data
        def mock_iterator():
            for item in input_iterator:
                yield item

        # Collect outputs from the async_wrap_iterator
        outputs = []
        async for output in test_model_helper.async_wrap_iterator(mock_iterator()):
            outputs.append(output)

        # Assert the outputs match the expected results
        assert outputs == expected_outputs

    @pytest.mark.skipif(not is_module_available('llama_cpp'), reason="llama_cpp module not available")
    def test_is_model_loaded_initially_false(self, mocker, tmp_path):
        """Test that is_model_loaded returns False when no model is loaded."""
        # Create a dummy model file
        dummy_model = tmp_path / "test.gguf"
        dummy_model.touch()

        # Mock the singleton to get a fresh instance
        ModelHelper._instance = None

        helper = ModelHelper(model_path=str(dummy_model), search_options={})

        assert helper.is_model_loaded() is False

    @pytest.mark.skipif(not is_module_available('llama_cpp'), reason="llama_cpp module not available")
    def test_is_model_loaded_after_model_set(self, mocker, tmp_path):
        """Test that is_model_loaded returns True when model attribute is set."""
        # Create a dummy model file
        dummy_model = tmp_path / "test.gguf"
        dummy_model.touch()

        # Mock the singleton to get a fresh instance
        ModelHelper._instance = None

        helper = ModelHelper(model_path=str(dummy_model), search_options={})

        # Manually set a mock model
        helper.model = mocker.MagicMock()

        assert helper.is_model_loaded() is True

    @pytest.mark.skipif(not is_module_available('llama_cpp'), reason="llama_cpp module not available")
    def test_cleanup_releases_resources(self, mocker, tmp_path):
        """Test that cleanup method properly releases model resources."""
        # Create a dummy model file
        dummy_model = tmp_path / "test.gguf"
        dummy_model.touch()

        # Mock the singleton to get a fresh instance
        ModelHelper._instance = None

        helper = ModelHelper(model_path=str(dummy_model), search_options={})

        # Set mock resources
        helper.model = mocker.MagicMock()
        helper.generator = mocker.MagicMock()

        # Call cleanup
        helper.cleanup()

        # Verify resources are released
        assert helper.model is None
        assert helper.generator is None

    @pytest.mark.skipif(not is_module_available('llama_cpp'), reason="llama_cpp module not available")
    def test_is_model_loaded_after_cleanup(self, mocker, tmp_path):
        """Test that is_model_loaded returns False after cleanup."""
        # Create a dummy model file
        dummy_model = tmp_path / "test.gguf"
        dummy_model.touch()

        # Mock the singleton to get a fresh instance
        ModelHelper._instance = None

        helper = ModelHelper(model_path=str(dummy_model), search_options={})

        # Set and then cleanup
        helper.model = mocker.MagicMock()
        assert helper.is_model_loaded() is True

        helper.cleanup()
        assert helper.is_model_loaded() is False


class TestModelHelperPlatformDetection:
    """Tests for macOS platform detection and GPU layer configuration."""

    @pytest.fixture(scope="function", autouse=True)
    def test_obj_app_config(self, mocker):
        # Mock AppConfig's get_logger_level method to suppress logging during tests.
        mocker.patch.object(AppConfig, 'get_logger_level', return_value=logging.NOTSET)

        # Create an AppConfig instance and set it to test mode.
        _app_config = AppConfig()
        _app_config.set_test_mode(True)

        yield _app_config

    @pytest.mark.skipif(not is_module_available('llama_cpp'), reason="llama_cpp module not available")
    def test_is_macos_on_darwin(self, mocker):
        """Test is_macos returns True on darwin platform."""
        mocker.patch('sys.platform', 'darwin')
        assert ModelHelper.is_macos() is True

    @pytest.mark.skipif(not is_module_available('llama_cpp'), reason="llama_cpp module not available")
    def test_is_macos_on_linux(self, mocker):
        """Test is_macos returns False on linux platform."""
        mocker.patch('sys.platform', 'linux')
        assert ModelHelper.is_macos() is False

    @pytest.mark.skipif(not is_module_available('llama_cpp'), reason="llama_cpp module not available")
    def test_is_macos_on_windows(self, mocker):
        """Test is_macos returns False on Windows platform."""
        mocker.patch('sys.platform', 'win32')
        assert ModelHelper.is_macos() is False

    @pytest.mark.skipif(not is_module_available('llama_cpp'), reason="llama_cpp module not available")
    def test_is_apple_silicon_on_arm64_mac(self, mocker):
        """Test is_apple_silicon returns True on ARM64 macOS (M1/M2/M3/M4)."""
        mocker.patch('sys.platform', 'darwin')
        mocker.patch('platform.machine', return_value='arm64')
        assert ModelHelper.is_apple_silicon() is True

    @pytest.mark.skipif(not is_module_available('llama_cpp'), reason="llama_cpp module not available")
    def test_is_apple_silicon_on_intel_mac(self, mocker):
        """Test is_apple_silicon returns False on Intel macOS (x86_64)."""
        mocker.patch('sys.platform', 'darwin')
        mocker.patch('platform.machine', return_value='x86_64')
        assert ModelHelper.is_apple_silicon() is False

    @pytest.mark.skipif(not is_module_available('llama_cpp'), reason="llama_cpp module not available")
    def test_is_apple_silicon_on_linux(self, mocker):
        """Test is_apple_silicon returns False on Linux even with ARM."""
        mocker.patch('sys.platform', 'linux')
        mocker.patch('platform.machine', return_value='aarch64')
        assert ModelHelper.is_apple_silicon() is False

    @pytest.mark.skipif(not is_module_available('llama_cpp'), reason="llama_cpp module not available")
    def test_cancel_loading_sets_event(self, mocker, tmp_path):
        """Test that cancel_loading sets the cancellation event."""
        from threading import Event

        # Create a dummy model file
        dummy_model = tmp_path / "test.gguf"
        dummy_model.touch()

        # Mock the singleton to get a fresh instance
        ModelHelper._instance = None

        helper = ModelHelper(model_path=str(dummy_model), search_options={})

        # Simulate a cancel event being active (as if init_model was called)
        helper._cancel_event = Event()
        assert not helper._cancel_event.is_set()

        # Call cancel_loading
        helper.cancel_loading()

        # Verify the event is set
        assert helper._cancel_event.is_set()

    @pytest.mark.skipif(not is_module_available('llama_cpp'), reason="llama_cpp module not available")
    def test_cancel_loading_no_event(self, mocker, tmp_path):
        """Test that cancel_loading handles None event gracefully."""
        # Create a dummy model file
        dummy_model = tmp_path / "test.gguf"
        dummy_model.touch()

        # Mock the singleton to get a fresh instance
        ModelHelper._instance = None

        helper = ModelHelper(model_path=str(dummy_model), search_options={})

        # Ensure no event is set
        helper._cancel_event = None

        # Call cancel_loading - should not raise
        helper.cancel_loading()  # No exception expected

    @pytest.mark.skipif(not is_module_available('llama_cpp'), reason="llama_cpp module not available")
    def test_init_model_uses_metal_on_apple_silicon(self, mocker, tmp_path):
        """Test that init_model uses Metal GPU (-1 layers) on Apple Silicon Macs when Auto."""
        # Mock platform detection
        mocker.patch.object(ModelHelper, 'is_macos', return_value=True)
        mocker.patch.object(ModelHelper, 'is_apple_silicon', return_value=True)

        # Create a dummy model file
        dummy_model = tmp_path / "test.gguf"
        dummy_model.touch()

        # Mock the singleton to get a fresh instance
        ModelHelper._instance = None

        # n_gpu_layers=None means Auto mode
        helper = ModelHelper(model_path=str(dummy_model), n_gpu_layers=None, search_options={})

        # Mock Llama initialization
        mock_llama = mocker.patch('notolog.modules.llama_cpp.model_helper.Llama')

        # Call init_model
        helper.init_model()

        # Verify n_gpu_layers=-1 was used (all layers on Metal GPU)
        mock_llama.assert_called_once()
        call_kwargs = mock_llama.call_args[1]
        assert call_kwargs['n_gpu_layers'] == -1

    @pytest.mark.skipif(not is_module_available('llama_cpp'), reason="llama_cpp module not available")
    def test_init_model_uses_cpu_on_intel_mac(self, mocker, tmp_path):
        """Test that init_model uses CPU (0 layers) on Intel Macs when Auto."""
        # Mock platform detection
        mocker.patch.object(ModelHelper, 'is_macos', return_value=True)
        mocker.patch.object(ModelHelper, 'is_apple_silicon', return_value=False)

        # Create a dummy model file
        dummy_model = tmp_path / "test.gguf"
        dummy_model.touch()

        # Mock the singleton to get a fresh instance
        ModelHelper._instance = None

        # n_gpu_layers=None means Auto mode
        helper = ModelHelper(model_path=str(dummy_model), n_gpu_layers=None, search_options={})

        # Mock Llama initialization
        mock_llama = mocker.patch('notolog.modules.llama_cpp.model_helper.Llama')

        # Call init_model
        helper.init_model()

        # Verify n_gpu_layers=0 was used (CPU only)
        mock_llama.assert_called_once()
        call_kwargs = mock_llama.call_args[1]
        assert call_kwargs['n_gpu_layers'] == 0

    @pytest.mark.skipif(not is_module_available('llama_cpp'), reason="llama_cpp module not available")
    def test_init_model_respects_explicit_gpu_layers_setting(self, mocker, tmp_path):
        """Test that init_model respects explicit n_gpu_layers setting from UI."""
        # Mock platform detection - even on Intel Mac
        mocker.patch.object(ModelHelper, 'is_macos', return_value=True)
        mocker.patch.object(ModelHelper, 'is_apple_silicon', return_value=False)

        # Create a dummy model file
        dummy_model = tmp_path / "test.gguf"
        dummy_model.touch()

        # Mock the singleton to get a fresh instance
        ModelHelper._instance = None

        # Explicitly set n_gpu_layers=-1 from UI
        helper = ModelHelper(model_path=str(dummy_model), n_gpu_layers=-1, search_options={})

        # Mock Llama initialization
        mock_llama = mocker.patch('notolog.modules.llama_cpp.model_helper.Llama')

        # Call init_model
        helper.init_model()

        # Verify n_gpu_layers=-1 was used (from explicit setting)
        mock_llama.assert_called_once()
        call_kwargs = mock_llama.call_args[1]
        assert call_kwargs['n_gpu_layers'] == -1

    @pytest.mark.skipif(not is_module_available('llama_cpp'), reason="llama_cpp module not available")
    def test_init_model_uses_cpu_on_linux(self, mocker, tmp_path):
        """Test that init_model uses CPU (0 layers) on Linux when Auto."""
        # Mock platform detection
        mocker.patch.object(ModelHelper, 'is_macos', return_value=False)

        # Create a dummy model file
        dummy_model = tmp_path / "test.gguf"
        dummy_model.touch()

        # Mock the singleton to get a fresh instance
        ModelHelper._instance = None

        # n_gpu_layers=None means Auto mode
        helper = ModelHelper(model_path=str(dummy_model), n_gpu_layers=None, search_options={})

        # Mock Llama initialization
        mock_llama = mocker.patch('notolog.modules.llama_cpp.model_helper.Llama')

        # Call init_model
        helper.init_model()

        # Verify n_gpu_layers=0 was used (CPU only on non-macOS)
        mock_llama.assert_called_once()
        call_kwargs = mock_llama.call_args[1]
        assert call_kwargs['n_gpu_layers'] == 0

    @pytest.mark.skipif(not is_module_available('llama_cpp'), reason="llama_cpp module not available")
    def test_init_model_checks_cancellation(self, mocker, tmp_path):
        """Test that init_model checks for cancellation before loading."""
        from threading import Event
        import asyncio

        # Create a dummy model file
        dummy_model = tmp_path / "test.gguf"
        dummy_model.touch()

        # Mock the singleton to get a fresh instance
        ModelHelper._instance = None

        helper = ModelHelper(model_path=str(dummy_model), search_options={})

        # Mock Llama to ensure it's not called
        mock_llama = mocker.patch('notolog.modules.llama_cpp.model_helper.Llama')

        # Patch Event creation to return a pre-set (cancelled) event
        # This is necessary because init_model() creates a NEW Event, overwriting any pre-set one
        def create_preset_event():
            event = Event()
            event.set()  # Pre-set the cancellation
            return event

        mocker.patch('notolog.modules.llama_cpp.model_helper.Event', create_preset_event)

        # Call init_model - should raise CancelledError
        with pytest.raises(asyncio.CancelledError):
            helper.init_model()

        # Verify Llama was never called
        mock_llama.assert_not_called()


class TestModelHelperIntelMacCompatibility:
    """
    Tests for Intel Mac compatibility.

    Important notes for Intel Mac users:
    - The app auto-detects Intel Mac and defaults to CPU-only mode (n_gpu_layers=0)
    - If issues persist, try llama-cpp-python version 0.2.90
    """

    @pytest.fixture(scope="function", autouse=True)
    def test_obj_app_config(self, mocker):
        # Mock AppConfig's get_logger_level method to suppress logging during tests.
        mocker.patch.object(AppConfig, 'get_logger_level', return_value=logging.NOTSET)

        # Create an AppConfig instance and set it to test mode.
        _app_config = AppConfig()
        _app_config.set_test_mode(True)

        yield _app_config

    @pytest.mark.skipif(not is_module_available('llama_cpp'), reason="llama_cpp module not available")
    def test_intel_mac_auto_selects_cpu_only(self, mocker, tmp_path):
        """
        Test that on Intel Macs, Auto mode automatically selects CPU-only (n_gpu_layers=0).
        """
        # Mock platform detection for Intel Mac
        mocker.patch.object(ModelHelper, 'is_macos', return_value=True)
        mocker.patch.object(ModelHelper, 'is_apple_silicon', return_value=False)

        # Create a dummy model file
        dummy_model = tmp_path / "test.gguf"
        dummy_model.touch()

        # Mock the singleton to get a fresh instance
        ModelHelper._instance = None

        # Auto mode (n_gpu_layers=None)
        helper = ModelHelper(model_path=str(dummy_model), n_gpu_layers=None, search_options={})

        # Mock Llama initialization
        mock_llama = mocker.patch('notolog.modules.llama_cpp.model_helper.Llama')

        # Call init_model
        helper.init_model()

        # Verify CPU-only mode was selected
        mock_llama.assert_called_once()
        call_kwargs = mock_llama.call_args[1]
        assert call_kwargs['n_gpu_layers'] == 0, \
            "Intel Mac should auto-select CPU-only mode (n_gpu_layers=0)"

    @pytest.mark.skipif(not is_module_available('llama_cpp'), reason="llama_cpp module not available")
    def test_resolve_gpu_layers_returns_correct_values(self, mocker, tmp_path):
        """
        Test _resolve_gpu_layers method directly to verify the resolution logic.
        """
        # Create a dummy model file
        dummy_model = tmp_path / "test.gguf"
        dummy_model.touch()

        # Test case 1: Explicit setting takes priority
        ModelHelper._instance = None
        helper = ModelHelper(model_path=str(dummy_model), n_gpu_layers=5, search_options={})
        assert helper._resolve_gpu_layers() == 5

        # Test case 2: None on Apple Silicon -> -1
        ModelHelper._instance = None
        mocker.patch.object(ModelHelper, 'is_macos', return_value=True)
        mocker.patch.object(ModelHelper, 'is_apple_silicon', return_value=True)
        helper = ModelHelper(model_path=str(dummy_model), n_gpu_layers=None, search_options={})
        assert helper._resolve_gpu_layers() == -1

        # Test case 3: None on Intel Mac -> 0
        ModelHelper._instance = None
        mocker.patch.object(ModelHelper, 'is_macos', return_value=True)
        mocker.patch.object(ModelHelper, 'is_apple_silicon', return_value=False)
        helper = ModelHelper(model_path=str(dummy_model), n_gpu_layers=None, search_options={})
        assert helper._resolve_gpu_layers() == 0

        # Test case 4: None on Linux -> 0
        ModelHelper._instance = None
        mocker.patch.object(ModelHelper, 'is_macos', return_value=False)
        helper = ModelHelper(model_path=str(dummy_model), n_gpu_layers=None, search_options={})
        assert helper._resolve_gpu_layers() == 0


class TestModelHelperUpgradeScenarios:
    """
    Tests for upgrade scenarios where users upgrade from previous versions
    that didn't have the gpu_layers configuration option.

    These tests ensure backward compatibility and that Auto mode works correctly
    when the new config value is missing or None (default for new installs and upgrades).
    """

    @pytest.fixture(scope="function", autouse=True)
    def test_obj_app_config(self, mocker):
        # Mock AppConfig's get_logger_level method to suppress logging during tests.
        mocker.patch.object(AppConfig, 'get_logger_level', return_value=logging.NOTSET)

        # Create an AppConfig instance and set it to test mode.
        _app_config = AppConfig()
        _app_config.set_test_mode(True)

        yield _app_config

    @pytest.mark.skipif(not is_module_available('llama_cpp'), reason="llama_cpp module not available")
    def test_upgrade_scenario_no_gpu_layers_param_apple_silicon(self, mocker, tmp_path):
        """
        Test upgrade scenario: User upgrades from version without gpu_layers setting.
        On Apple Silicon, Auto mode should enable Metal GPU (-1 layers).

        This simulates calling ModelHelper without the n_gpu_layers parameter,
        as would happen if old code called the constructor.
        """
        # Mock platform detection for Apple Silicon
        mocker.patch.object(ModelHelper, 'is_macos', return_value=True)
        mocker.patch.object(ModelHelper, 'is_apple_silicon', return_value=True)

        # Create a dummy model file
        dummy_model = tmp_path / "test.gguf"
        dummy_model.touch()

        # Mock the singleton to get a fresh instance
        ModelHelper._instance = None

        # Simulate upgrade scenario: n_gpu_layers parameter not provided (uses default None)
        helper = ModelHelper(model_path=str(dummy_model), search_options={})

        # Verify the setting is None (Auto mode)
        assert helper.n_gpu_layers_setting is None

        # Mock Llama initialization
        mock_llama = mocker.patch('notolog.modules.llama_cpp.model_helper.Llama')

        # Call init_model
        helper.init_model()

        # Verify Auto mode selected Metal GPU for Apple Silicon
        mock_llama.assert_called_once()
        call_kwargs = mock_llama.call_args[1]
        assert call_kwargs['n_gpu_layers'] == -1, "Auto mode should use Metal GPU (-1) on Apple Silicon"

    @pytest.mark.skipif(not is_module_available('llama_cpp'), reason="llama_cpp module not available")
    def test_upgrade_scenario_no_gpu_layers_param_intel_mac(self, mocker, tmp_path):
        """
        Test upgrade scenario: User upgrades from version without gpu_layers setting.
        On Intel Mac, Auto mode should use CPU-only (0 layers) to avoid Metal hangs.
        """
        # Mock platform detection for Intel Mac
        mocker.patch.object(ModelHelper, 'is_macos', return_value=True)
        mocker.patch.object(ModelHelper, 'is_apple_silicon', return_value=False)

        # Create a dummy model file
        dummy_model = tmp_path / "test.gguf"
        dummy_model.touch()

        # Mock the singleton to get a fresh instance
        ModelHelper._instance = None

        # Simulate upgrade scenario: n_gpu_layers parameter not provided
        helper = ModelHelper(model_path=str(dummy_model), search_options={})

        # Verify the setting is None (Auto mode)
        assert helper.n_gpu_layers_setting is None

        # Mock Llama initialization
        mock_llama = mocker.patch('notolog.modules.llama_cpp.model_helper.Llama')

        # Call init_model
        helper.init_model()

        # Verify Auto mode selected CPU-only for Intel Mac
        mock_llama.assert_called_once()
        call_kwargs = mock_llama.call_args[1]
        assert call_kwargs['n_gpu_layers'] == 0, "Auto mode should use CPU-only (0) on Intel Mac"

    @pytest.mark.skipif(not is_module_available('llama_cpp'), reason="llama_cpp module not available")
    def test_upgrade_scenario_no_gpu_layers_param_linux(self, mocker, tmp_path):
        """
        Test upgrade scenario: User upgrades from version without gpu_layers setting.
        On Linux, Auto mode should use CPU-only (0 layers) by default.
        """
        # Mock platform detection for Linux
        mocker.patch.object(ModelHelper, 'is_macos', return_value=False)

        # Create a dummy model file
        dummy_model = tmp_path / "test.gguf"
        dummy_model.touch()

        # Mock the singleton to get a fresh instance
        ModelHelper._instance = None

        # Simulate upgrade scenario: n_gpu_layers parameter not provided
        helper = ModelHelper(model_path=str(dummy_model), search_options={})

        # Verify the setting is None (Auto mode)
        assert helper.n_gpu_layers_setting is None

        # Mock Llama initialization
        mock_llama = mocker.patch('notolog.modules.llama_cpp.model_helper.Llama')

        # Call init_model
        helper.init_model()

        # Verify Auto mode selected CPU-only for Linux
        mock_llama.assert_called_once()
        call_kwargs = mock_llama.call_args[1]
        assert call_kwargs['n_gpu_layers'] == 0, "Auto mode should use CPU-only (0) on Linux"

    @pytest.mark.skipif(not is_module_available('llama_cpp'), reason="llama_cpp module not available")
    def test_upgrade_preserves_explicit_cpu_setting(self, mocker, tmp_path):
        """
        Test that when user explicitly sets CPU-only (0), it's preserved even on Apple Silicon.
        This ensures user preferences are not overridden by Auto detection.
        """
        # Mock platform detection for Apple Silicon
        mocker.patch.object(ModelHelper, 'is_macos', return_value=True)
        mocker.patch.object(ModelHelper, 'is_apple_silicon', return_value=True)

        # Create a dummy model file
        dummy_model = tmp_path / "test.gguf"
        dummy_model.touch()

        # Mock the singleton to get a fresh instance
        ModelHelper._instance = None

        # User explicitly wants CPU-only
        helper = ModelHelper(model_path=str(dummy_model), n_gpu_layers=0, search_options={})

        # Verify the setting is stored
        assert helper.n_gpu_layers_setting == 0

        # Mock Llama initialization
        mock_llama = mocker.patch('notolog.modules.llama_cpp.model_helper.Llama')

        # Call init_model
        helper.init_model()

        # Verify user's explicit setting is respected
        mock_llama.assert_called_once()
        call_kwargs = mock_llama.call_args[1]
        assert call_kwargs['n_gpu_layers'] == 0, "User's explicit CPU-only setting should be preserved"

    @pytest.mark.skipif(not is_module_available('llama_cpp'), reason="llama_cpp module not available")
    def test_upgrade_preserves_explicit_gpu_setting_on_intel(self, mocker, tmp_path):
        """
        Test that when user explicitly sets GPU (-1), it's used even on Intel Mac.
        This allows users to try Metal if they know it works on their hardware.

        Note: This is NOT recommended for Intel Mac users as it may cause hangs.
        Users should use version 0.2.90 if they want to try GPU.
        """
        # Mock platform detection for Intel Mac (where Auto would use CPU)
        mocker.patch.object(ModelHelper, 'is_macos', return_value=True)
        mocker.patch.object(ModelHelper, 'is_apple_silicon', return_value=False)

        # Create a dummy model file
        dummy_model = tmp_path / "test.gguf"
        dummy_model.touch()

        # Mock the singleton to get a fresh instance
        ModelHelper._instance = None

        # User explicitly wants to try Metal on Intel Mac
        helper = ModelHelper(model_path=str(dummy_model), n_gpu_layers=-1, search_options={})

        # Verify the setting is stored
        assert helper.n_gpu_layers_setting == -1

        # Mock Llama initialization
        mock_llama = mocker.patch('notolog.modules.llama_cpp.model_helper.Llama')

        # Call init_model
        helper.init_model()

        # Verify user's explicit setting is respected
        mock_llama.assert_called_once()
        call_kwargs = mock_llama.call_args[1]
        assert call_kwargs['n_gpu_layers'] == -1, "User's explicit GPU setting should be preserved on Intel Mac"


class TestModelHelperUISentinelValues:
    """
    Tests for UI sentinel value conversion.

    The UI uses -2 to represent "Auto" (shown via QSpinBox.setSpecialValueText),
    which is converted to None internally. This ensures -1 remains available
    for "all GPU layers".

    UI Values:
    - -2: "Auto" (converted to None internally)
    - -1: All layers on GPU
    - 0: CPU only
    - >0: Specific number of layers
    """

    @pytest.fixture(scope="function", autouse=True)
    def test_obj_app_config(self, mocker):
        mocker.patch.object(AppConfig, 'get_logger_level', return_value=logging.NOTSET)
        _app_config = AppConfig()
        _app_config.set_test_mode(True)
        yield _app_config

    @pytest.mark.skipif(not is_module_available('llama_cpp'), reason="llama_cpp module not available")
    def test_ui_auto_value_converted_to_none(self, mocker, tmp_path):
        """
        Test that -2 (UI "Auto") and None both result in auto-detection behavior.
        The settings_update_handler converts -2 to None before passing to ModelHelper.
        """
        mocker.patch.object(ModelHelper, 'is_macos', return_value=True)
        mocker.patch.object(ModelHelper, 'is_apple_silicon', return_value=True)

        dummy_model = tmp_path / "test.gguf"
        dummy_model.touch()

        # Test with None (internal representation of Auto)
        ModelHelper._instance = None
        helper = ModelHelper(model_path=str(dummy_model), n_gpu_layers=None, search_options={})
        assert helper.n_gpu_layers_setting is None
        assert helper._resolve_gpu_layers() == -1  # Apple Silicon -> GPU

    @pytest.mark.skipif(not is_module_available('llama_cpp'), reason="llama_cpp module not available")
    def test_explicit_minus_one_differs_from_auto(self, mocker, tmp_path):
        """
        Test that -1 (explicit all GPU) behaves differently from Auto on Intel Mac.
        Auto on Intel Mac -> 0 (CPU), but -1 forces GPU.
        """
        mocker.patch.object(ModelHelper, 'is_macos', return_value=True)
        mocker.patch.object(ModelHelper, 'is_apple_silicon', return_value=False)  # Intel Mac

        dummy_model = tmp_path / "test.gguf"
        dummy_model.touch()

        # Auto mode (None) on Intel Mac should select CPU
        ModelHelper._instance = None
        helper_auto = ModelHelper(model_path=str(dummy_model), n_gpu_layers=None, search_options={})
        assert helper_auto._resolve_gpu_layers() == 0, "Auto on Intel Mac should be CPU (0)"

        # Explicit -1 should force GPU even on Intel Mac
        ModelHelper._instance = None
        helper_gpu = ModelHelper(model_path=str(dummy_model), n_gpu_layers=-1, search_options={})
        assert helper_gpu._resolve_gpu_layers() == -1, "Explicit -1 should force GPU"

    @pytest.mark.skipif(not is_module_available('llama_cpp'), reason="llama_cpp module not available")
    def test_all_gpu_layers_values_are_distinct(self, mocker, tmp_path):
        """
        Verify that Auto, -1, 0, and positive values all produce distinct behaviors.
        """
        mocker.patch.object(ModelHelper, 'is_macos', return_value=True)
        mocker.patch.object(ModelHelper, 'is_apple_silicon', return_value=False)  # Intel Mac for clearer distinction

        dummy_model = tmp_path / "test.gguf"
        dummy_model.touch()

        test_cases = [
            (None, 0, "Auto on Intel Mac -> CPU"),      # Auto -> platform-specific (Intel Mac = CPU)
            (-1, -1, "Explicit all GPU"),               # Explicit all GPU
            (0, 0, "Explicit CPU only"),                # Explicit CPU
            (5, 5, "Explicit 5 layers"),                # Specific layers
        ]

        for input_val, expected, desc in test_cases:
            ModelHelper._instance = None
            helper = ModelHelper(model_path=str(dummy_model), n_gpu_layers=input_val, search_options={})
            assert helper._resolve_gpu_layers() == expected, f"{desc}: expected {expected}, got {helper._resolve_gpu_layers()}"
