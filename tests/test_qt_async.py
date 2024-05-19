import asyncio

from notolog.async_highlighter import AsyncHighlighter

import pytest


class TestQtAsync:

    @pytest.fixture
    def async_highlighter_obj(self):
        # Fixture to create and return main window instance
        async_highlighter = AsyncHighlighter(callback=lambda check: check)
        yield async_highlighter

    @pytest.fixture
    async def cleanup_tasks(self):
        yield
        # Cancel and clean up all pending asyncio tasks
        for task in asyncio.all_tasks():
            if task is not asyncio.current_task():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

    @pytest.mark.asyncio
    async def test_ui_interaction(self, mocker, async_highlighter_obj, cleanup_tasks):
        # Get callback method to check
        mock_rehighlight = mocker.patch.object(async_highlighter_obj, 'rehighlight_task_callback')

        # Check local task pool is empty
        assert len(async_highlighter_obj.rehighlight_tasks) == 0

        # Queue re-highlight tasks
        task0 = await async_highlighter_obj.rehighlight_in_queue()
        mock_rehighlight.assert_called_once_with(task0)
        # One more
        task1 = await async_highlighter_obj.rehighlight_in_queue()
        mock_rehighlight.assert_called_with(task1)
        # Another one more
        task2 = await async_highlighter_obj.rehighlight_in_queue()
        mock_rehighlight.assert_called_with(task2)
        # Add more tasks
        await async_highlighter_obj.rehighlight_in_queue()
        await async_highlighter_obj.rehighlight_in_queue()
        await async_highlighter_obj.rehighlight_in_queue()
        await async_highlighter_obj.rehighlight_in_queue()
        await async_highlighter_obj.rehighlight_in_queue()
        # Max count in a short period of time is 3
        assert mock_rehighlight.call_count == 3

        # Checking of local task pool doesn't work properly if run from IDE, but works from CLI
        assert len(async_highlighter_obj.rehighlight_tasks) == 3

        # The cleanup_tasks fixture is used implicitly; no need to assert its presence
        # assert cleanup_tasks
