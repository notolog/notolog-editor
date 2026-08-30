#!/usr/bin/env python3
"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Run the public pre-commit pytest check.
- Functionality: Reuse the interpreter recorded by pre-commit and isolate application settings during tests.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from __future__ import annotations

import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile


PYTEST_ARGS = (
    '--ignore=tests/ui_tests',
    '--ignore=tests/test_qt_async.py',
    '--ignore=tests/test_enc_helper.py',
    '--ignore=tests/test_file_header.py',
    '-q',
    '--tb=no',
)


def get_hook_python() -> str | None:
    """Read the environment-bound interpreter from pre-commit's generated Git hook."""

    git_executable = shutil.which('git')
    if git_executable is None:
        return None

    result = subprocess.run(
        [git_executable, 'rev-parse', '--git-path', 'hooks/pre-commit'],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None

    hook_path = Path(result.stdout.strip())
    try:
        hook_lines = hook_path.read_text(encoding='utf-8').splitlines()
    except OSError:
        return None

    for line in hook_lines:
        if line.startswith('INSTALL_PYTHON='):
            values = shlex.split(line.partition('=')[2])
            if values and os.access(values[0], os.X_OK):
                return values[0]
    return None


def main() -> int:
    # Manual pre-commit runs may not have an installed Git hook yet. In that case,
    # use the active environment from PATH and provide a useful failure if it is absent.
    python = get_hook_python() or shutil.which('python') or shutil.which('python3')
    if python is None:
        print('No project Python interpreter found. Activate the project environment first.', file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory(prefix='notolog-pytest-') as state_dir:
        env = os.environ.copy()
        env['XDG_CONFIG_HOME'] = os.path.join(state_dir, 'config')
        env['XDG_DATA_HOME'] = os.path.join(state_dir, 'data')
        return subprocess.call([python, '-m', 'pytest', *PYTEST_ARGS], env=env)


if __name__ == '__main__':
    raise SystemExit(main())
