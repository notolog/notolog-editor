"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Async syntax highlighter to support background operation and avoid UI blocks.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import QTimer

from qasync import asyncSlot
import asyncio

import logging

from typing import Any, Callable


class AsyncHighlighter:

    def __init__(self, callback: Callable[..., Any]):

        self.callback = callback

        self.logger = logging.getLogger('async_highlighter')

        self.rehighlight_tasks = []

        self.loop = asyncio.get_event_loop()

    @asyncSlot()
    async def rehighlight_in_queue(self, full_rehighlight: bool = False) -> Any:
        """
        Re-highlight code asynchronously here.
        More info about asyncio tasks: https://docs.python.org/3/library/asyncio-task.html
        """

        # Check async loop is running
        if not asyncio.get_event_loop().is_running():
            self.logger.debug('Skipping the task because the async loop is not running.')
            return

        self.logger.debug('Re-highlight %d tasks in queue' % len(self.rehighlight_tasks))

        postpone = False if len(self.rehighlight_tasks) == 0 else True
        self.logger.debug('Re-highlight is to postpone "%r"' % postpone)

        task = None
        # To keep only a few tasks in queue
        if len(self.rehighlight_tasks) < 3:
            task = asyncio.ensure_future(self.rehighlight_async(full_rehighlight, postpone))
            # task = asyncio.create_task(self.rehighlight_async(full_rehighlight, postpone))
            # Add task to the local pool first
            self.rehighlight_tasks.append(task)
            # Callback method to set up further actions
            task.add_done_callback(lambda _task: self.rehighlight_task_callback(_task))

        try:
            done, pending = await asyncio.wait(
                self.rehighlight_tasks,
                return_when=asyncio.ALL_COMPLETED,  # There is no pending tasks check
            )
            self.logger.debug(f'Re-highlight tasks progress. Done {len(done)}, pending {len(pending)}')
        except asyncio.CancelledError:
            # All tasks will be cancelled later upon close event
            pass

        return task

    def rehighlight_task_callback(self, task) -> None:
        self.logger.debug('%s from total %d completed with callback'
                          % (task.get_name(), len(self.rehighlight_tasks)))

        self.rehighlight_tasks.remove(task)

        if len(self.rehighlight_tasks) == 0:
            QTimer.singleShot(500, lambda: self.callback(True))

    async def rehighlight_async(self, full_rehighlight: bool = False, postpone: bool = False) -> None:
        """
        Run this method not too often to avoid overwhelming the system.
        """
        try:
            # Postpone before re-highlighting set
            if postpone:
                self.logger.debug('Re-highlighting the text > postpone')
                # Keep this method particular amount of time to avoid overwhelming
                await asyncio.sleep(0.15, self.loop)
            # Re-highlight
            self.callback(full_rehighlight)
            self.logger.debug('Async re-highlighting queue task processed')
            # Postpone after re-highlighting to keep the queue busy
            self.logger.debug('Re-highlighting the text > wait to return')
            # Keep this method particular amount of time to avoid overwhelming
            await asyncio.sleep(0.3, self.loop)
        except asyncio.CancelledError:
            # All tasks will be cancelled later upon close event
            pass
