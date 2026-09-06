"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Speech runtime validation and model downloads.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

import asyncio
import os
import re
import signal
import sys
import tempfile
from pathlib import Path

from PySide6.QtCore import QProcess, QProcessEnvironment

from .config import model_directory, runtime_path


SUPPORTED_VERSION = '0.1.0'


def process_environment(settings):
    env = QProcessEnvironment.systemEnvironment()
    # A frozen application may inject its private libraries into child processes.
    for key in ('LD_LIBRARY_PATH', 'DYLD_LIBRARY_PATH'):
        original = os.environ.get(key + '_ORIG')
        if original is not None:
            env.insert(key, original)
        elif getattr(sys, 'frozen', False):
            env.remove(key)
    for key in env.keys():
        if key.startswith('NEMO_SPEECH_'):
            env.remove(key)
    env.insert('NEMO_SPEECH_MODEL_DIR', str(model_directory(settings)))
    return env


def isolate_process(process):
    if sys.platform != 'win32':
        parameters = QProcess.UnixProcessParameters()
        parameters.flags = QProcess.UnixProcessFlag.CreateNewSession
        process.setUnixProcessParameters(parameters)


def stop_process(process):
    """Stop the runtime and its download helper, including an active curl child."""
    if process.state() == QProcess.ProcessState.NotRunning:
        return
    pid = process.processId()
    if pid:
        if sys.platform == 'win32':
            killer = QProcess()
            killer.start('taskkill', ['/PID', str(pid), '/T', '/F'])
            killer.waitForFinished(1000)
        else:
            try:
                os.killpg(pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
    process.kill()
    process.waitForFinished(1000)


async def run_command(settings, arguments, progress=None, timeout=30):
    executable = runtime_path(settings)
    if not executable:
        raise ValueError('Select an installed nemo-speech executable in Text-to-Speech settings.')
    process = QProcess()
    isolate_process(process)
    process.setProcessEnvironment(process_environment(settings))
    process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
    loop = asyncio.get_running_loop()
    done = loop.create_future()
    output = bytearray()

    def read_output():
        data = bytes(process.readAllStandardOutput())
        output.extend(data)
        del output[:-65536]
        if progress and data:
            progress(data.decode('utf-8', 'replace'))

    def finished(code, status):
        read_output()
        if not done.done():
            done.set_result((code, status))

    def command_error(message):
        if sys.platform == 'darwin':
            message += (' If macOS blocked nemo-speech, check System Settings > Privacy & Security. '
                        'Use Open Anyway only if you trust the downloaded runtime. '
                        'For repeated library prompts, see macOS runtime approval: '
                        'https://github.com/notolog/notolog-editor/blob/main/docs/text-to-speech.md#macos-runtime-approval')
        return RuntimeError(message)

    def error(reason):
        if not done.done():
            message = process.errorString()
            done.set_exception(command_error(message) if reason in (
                QProcess.ProcessError.FailedToStart, QProcess.ProcessError.Crashed) else RuntimeError(message))

    process.readyReadStandardOutput.connect(read_output)
    process.finished.connect(finished)
    process.errorOccurred.connect(error)
    process.start(executable, arguments)
    try:
        code, status = await asyncio.wait_for(done, timeout)
        result = output.decode('utf-8', 'replace')
        if code or status != QProcess.ExitStatus.NormalExit:
            raise RuntimeError(result[-3000:] or 'The speech runtime exited unexpectedly.')
        return result
    except asyncio.TimeoutError as exc:
        raise command_error(f'The speech runtime did not respond within {timeout:g} seconds.') from exc
    finally:
        stop_process(process)
        process.deleteLater()


async def validate_runtime(settings):
    output = await run_command(settings, ['--version'])
    match = re.search(r'\b(\d+\.\d+\.\d+)\b', output)
    if not match or match.group(1) != SUPPORTED_VERSION:
        raise ValueError(f'This integration requires NeMo-Speech.cpp {SUPPORTED_VERSION}. Detected: {output.strip()}')


async def download_models(settings, progress):
    await validate_runtime(settings)
    model_directory(settings).mkdir(parents=True, exist_ok=True)
    # Check actual write access, including ACLs and read-only filesystems, before starting a long download.
    with tempfile.TemporaryFile(dir=model_directory(settings)):
        pass
    # The pinned runtime verifies hashes/sizes and fetches the codec and tokenizers too.
    output = await run_command(settings, ['--verbose', 'pull', 'magpie'], progress=progress, timeout=None)
    artifacts = {}
    for line in output.splitlines():
        fields = line.split('\t')
        if len(fields) == 3 and fields[1] in ('tts', 'codec', 'tokenizer'):
            artifacts[fields[1]] = fields[2]
    if (not all(role in artifacts for role in ('tts', 'codec', 'tokenizer'))
            or not Path(artifacts['tts']).is_file() or not Path(artifacts['codec']).is_file()
            or not Path(artifacts['tokenizer']).is_dir()):
        raise ValueError('Download finished without a complete model set. '
                         'Check the runtime output or select the model paths manually.')
    return artifacts['tts'], artifacts['codec'], artifacts['tokenizer']
