from PySide6.QtCore import QTimer

from qasync import asyncSlot
import asyncio

import logging

from typing import Any, Callable

from .app_config import AppConfig


class AsyncHighlighter:

    def __init__(self, callback: Callable[..., Any]):

        self.callback = callback

        self.logger = logging.getLogger('async_highlighter')

        self.logging = AppConfig().get_logging()
        self.debug = AppConfig().get_debug()

        self.rehighlight_tasks = []

        self.loop = asyncio.get_event_loop()

    @asyncSlot()
    async def rehighlight_in_queue(self, full_rehighlight: bool = False) -> Any:
        """
        More info about asyncio tasks: https://docs.python.org/3/library/asyncio-task.html
        """
        if self.debug:
            self.logger.debug('Re-highlight %d tasks in queue' % len(self.rehighlight_tasks))

        postpone = False if len(self.rehighlight_tasks) == 0 else True
        if self.debug:
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

        done, pending = await asyncio.wait(
            self.rehighlight_tasks,
            return_when=asyncio.ALL_COMPLETED,  # There is no pending tasks check
        )

        if self.debug:
            self.logger.debug(f'Re-highlight tasks progress. Done {len(done)}, pending {len(pending)}')

        return task

    def rehighlight_task_callback(self, task) -> None:
        if self.debug:
            self.logger.debug('%s from total %d completed with callback'
                              % (task.get_name(), len(self.rehighlight_tasks)))

        self.rehighlight_tasks.remove(task)

        if len(self.rehighlight_tasks) == 0:
            QTimer.singleShot(750, lambda: self.callback(True))

    async def rehighlight_async(self, full_rehighlight: bool = False, postpone: bool = False) -> None:
        """
        Run this method not too often to avoid overwhelming the system.
        """
        # Postpone before re-highlighting set
        if postpone:
            if self.debug:
                self.logger.debug('Re-highlighting the text > postpone')
            # Keep this method particular amount of time to avoid overwhelming
            await asyncio.sleep(0.25, self.loop)
        # Re-highlight
        self.callback(full_rehighlight)
        if self.debug:
            self.logger.debug('Async re-highlighting queue task processed')
        # Postpone after re-highlighting to keep the queue busy
        if self.debug:
            self.logger.debug('Re-highlighting the text > wait to return')
        # Keep this method particular amount of time to avoid overwhelming
        await asyncio.sleep(0.5, self.loop)

    async def cancel_tasks(self):
        tasks_total = len(self.rehighlight_tasks)
        for i, task in enumerate(self.rehighlight_tasks):
            if not task.done():
                task_res = task.cancel()
                if self.logging:
                    self.logger.info(
                        f'[{i + 1}/{tasks_total}] Pending task "{task.get_name()}" canceled with result "{task_res}"')
                # Gather all tasks to ensure they are completed before closing
                await asyncio.gather(*self.rehighlight_tasks, return_exceptions=True)
