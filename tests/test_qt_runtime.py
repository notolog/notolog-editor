"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Verify native Qt calls remain stable on supported Python versions.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

import subprocess
import sys
import textwrap


def test_qt_setters_and_signals_do_not_abort(tmp_path):
    # Isolate native failures so pytest can report them instead of aborting.
    # PYSIDE-3474: Qt 6.12.0 decrements borrowed None/True references on Python 3.11.
    script = textwrap.dedent("""\
        from PySide6.QtCore import QObject, Signal

        class Emitter(QObject):
            triggered = Signal()

        emitter = Emitter()
        emitter.triggered.connect(lambda: None)
        for _ in range(20_000):
            emitter.setObjectName('runtime-check')
            emitter.triggered.emit()
    """)
    result = subprocess.run(
        [sys.executable, '-X', 'faulthandler', '-c', script],
        cwd=tmp_path, capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr
