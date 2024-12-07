import pytest

from .. import is_module_available


def pytest_collection_modifyitems(config, items):
    """
    Conditionally skip tests in a specific directory.
    """
    # Check if the condition is not met
    if not is_module_available('ondevice_llm'):
        skip_marker = pytest.mark.skip(reason="Condition is not met. Skipping tests in 'ondevice_llm'.")
        # Skip all tests in the 'ondevice_llm' directory
        for item in items:
            if 'ondevice_llm' in item.nodeid:
                item.add_marker(skip_marker)
