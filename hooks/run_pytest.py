#!/usr/bin/env python3
"""Run the pre-commit pytest check with the interpreter that owns the Git hook."""

from __future__ import annotations

import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys


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

    return subprocess.call([python, '-m', 'pytest', *PYTEST_ARGS])


if __name__ == '__main__':
    raise SystemExit(main())
