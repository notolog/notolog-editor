from PySide6.QtWidgets import QPushButton

from qasync import QEventLoop, QApplication, asyncSlot
import asyncio

from notolog.notolog_editor import NotologEditor
from notolog.image_downloader import ImageDownloader

import os
import sys
import pytest


class TestQtAsync:

    @pytest.fixture(autouse=True, scope="class")  # Auto-use as this fixture should be used for all tests
    def qt_app(self):
        # Force Qt style override to "Fusion" to avoid issues on environments where "kvantum" is not available
        os.environ["QT_STYLE_OVERRIDE"] = "Fusion"
        # Create the QApplication instance for the tests
        app = QApplication(sys.argv)

        # Initialize the QEventLoop for asyncio integration with Qt
        loop = QEventLoop(app)
        asyncio.set_event_loop(loop)

        yield app

        # Properly close the QApplication after each test
        app.quit()

    @pytest.fixture
    def main_window(self, mocker, qt_app):
        # Avoid downloading resources during tests
        mocker.patch.object(NotologEditor, 'is_resource_attached', return_value=True)
        mocker.patch.object(ImageDownloader, 'download_resource_in_queue', return_value=None)

        # Fixture to create and return main window instance
        window = NotologEditor(screen=qt_app.screens()[0])
        yield window

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

    @asyncSlot()
    async def on_click(self):
        # Simulate some async operation by sleeping
        await asyncio.sleep(0.1)
        # Append "clicked" to the class-level result list
        self.result.append("clicked")

    @pytest.mark.asyncio
    async def test_ui_interaction(self, mocker, qt_app, main_window, cleanup_tasks):
        # Reset result list before each test if needed
        self.result = []

        button = QPushButton("Test Button")
        button.clicked.connect(lambda:
                               asyncio.ensure_future(self.on_click()))

        # Simulate a button click
        button.click()

        # Immediately after click, result should still be empty before the sleep allows on_click to proceed
        assert self.result == []
        # Wait for the sleep in on_click to finish
        await asyncio.sleep(0.25)  # Ensure this is long enough for the on_click task to complete
        # Now, result should have "clicked"
        assert self.result == ["clicked"]

        mock_rehighlight = mocker.patch.object(main_window, 'rehighlight_task_callback')

        # Check local task pool is empty
        assert len(main_window.rehighlight_tasks) == 0

        # Queue re-highlight tasks
        task0 = await main_window.rehighlight_in_queue()
        mock_rehighlight.assert_called_once_with(task0)
        # One more
        task1 = await main_window.rehighlight_in_queue()
        mock_rehighlight.assert_called_with(task1)
        # Another one more
        task2 = await main_window.rehighlight_in_queue()
        mock_rehighlight.assert_called_with(task2)
        # Add more tasks
        await main_window.rehighlight_in_queue()
        await main_window.rehighlight_in_queue()
        await main_window.rehighlight_in_queue()
        await main_window.rehighlight_in_queue()
        await main_window.rehighlight_in_queue()
        # Max count in a short period of time is 3
        assert mock_rehighlight.call_count == 3

        # Checking of local task pool doesn't work properly if run from IDE, but works from CLI
        assert len(main_window.rehighlight_tasks) == 3

        # The cleanup_tasks fixture is used implicitly; no need to assert its presence
        # assert cleanup_tasks
