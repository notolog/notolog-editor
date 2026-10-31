import sys

import pytest
from PySide6.QtGui import QFont


@pytest.mark.skipif(sys.implementation.name != 'cpython' or sys.version_info >= (3, 12),
                    reason='None is immortal in CPython 3.12 and newer')
def test_qt_void_calls_preserve_none_references():
    font = QFont()
    for _ in range(10):
        font.setBold(False)
    before = sys.getrefcount(None)
    for _ in range(100):
        font.setBold(False)
    after = sys.getrefcount(None)
    assert after >= before, 'Qt calls must not consume references to None'
