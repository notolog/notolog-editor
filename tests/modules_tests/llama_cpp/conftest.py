import pytest

from .. import is_module_available


def pytest_collection_modifyitems(config, items):
    """
    Conditionally skip tests in a specific directory.
    """
    # Check if the condition is not met
    if not is_module_available('llama_cpp'):
        skip_marker = pytest.mark.skip(reason="Condition is not met. Skipping tests in 'llama_cpp'.")
        # Skip all tests in the 'llama_cpp' directory
        for item in items:
            if 'llama_cpp' in item.nodeid:
                item.add_marker(skip_marker)
