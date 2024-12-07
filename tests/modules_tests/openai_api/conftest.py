import pytest

from .. import is_module_available


def pytest_collection_modifyitems(config, items):
    """
    Conditionally skip tests in a specific directory.
    """
    # Check if the condition is not met
    if not is_module_available('openai_api'):
        skip_marker = pytest.mark.skip(reason="Condition is not met. Skipping tests in 'openai_api'.")
        # Skip all tests in the 'openai_api' directory
        for item in items:
            if 'openai_api' in item.nodeid:
                item.add_marker(skip_marker)
