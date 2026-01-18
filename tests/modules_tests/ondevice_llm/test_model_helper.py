"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Contains unit tests for model_helper functionality.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

import pytest
import tempfile

# Check if onnxruntime_genai is actually importable at module level
try:
    import onnxruntime_genai  # noqa: F401
    ONNX_GENAI_AVAILABLE = True
except ImportError:
    ONNX_GENAI_AVAILABLE = False

# Skip entire module if onnxruntime-genai is not available
pytestmark = pytest.mark.skipif(
    not ONNX_GENAI_AVAILABLE,
    reason="onnxruntime-genai not installed"
)


class TestModelHelper:
    """Tests for OnDevice LLM ModelHelper class."""

    @pytest.fixture(scope="class")
    def model_helper_class(self):
        """Import ModelHelper only when tests are not skipped."""
        from notolog.modules.ondevice_llm.model_helper import ModelHelper
        return ModelHelper

    @pytest.fixture(scope="function")
    def temp_model_dir(self):
        """Create a temporary directory to use as model path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    def test_is_model_loaded_initially_false(self, model_helper_class, temp_model_dir):
        """Test that is_model_loaded returns False when no model is loaded."""
        ModelHelper = model_helper_class

        # Reset singleton for clean test
        ModelHelper._instance = None

        helper = ModelHelper(model_path=temp_model_dir, search_options={})

        assert helper.is_model_loaded() is False

    def test_is_model_loaded_after_model_set(self, model_helper_class, temp_model_dir, mocker):
        """Test that is_model_loaded returns True when model attribute is set."""
        ModelHelper = model_helper_class

        # Reset singleton for clean test
        ModelHelper._instance = None

        helper = ModelHelper(model_path=temp_model_dir, search_options={})

        # Manually set a mock model
        helper.model = mocker.MagicMock()

        assert helper.is_model_loaded() is True

    def test_cleanup_releases_resources(self, model_helper_class, temp_model_dir, mocker):
        """Test that cleanup method properly releases model resources."""
        ModelHelper = model_helper_class

        # Reset singleton for clean test
        ModelHelper._instance = None

        helper = ModelHelper(model_path=temp_model_dir, search_options={})

        # Set mock resources
        helper.model = mocker.MagicMock()
        helper.tokenizer = mocker.MagicMock()
        helper.tokenizer_stream = mocker.MagicMock()
        helper.generator = mocker.MagicMock()

        # Call cleanup
        helper.cleanup()

        # Verify resources are released
        assert helper.model is None
        assert helper.tokenizer is None
        assert helper.tokenizer_stream is None
        assert helper.generator is None

    def test_is_model_loaded_after_cleanup(self, model_helper_class, temp_model_dir, mocker):
        """Test that is_model_loaded returns False after cleanup."""
        ModelHelper = model_helper_class

        # Reset singleton for clean test
        ModelHelper._instance = None

        helper = ModelHelper(model_path=temp_model_dir, search_options={})

        # Set and then cleanup
        helper.model = mocker.MagicMock()
        assert helper.is_model_loaded() is True

        helper.cleanup()
        assert helper.is_model_loaded() is False
