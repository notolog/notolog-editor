"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Extends QWidget functionality to provide vertical UI spacer.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2025 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtWidgets import QFrame


class VerticalLineSpacer(QFrame):
    """
    Vertical line separator for the status bar.
    """

    def __init__(self):
        super(VerticalLineSpacer, self).__init__()

        # https://doc.qt.io/qt-6/qframe.html#Shape-enum
        self.setFrameShape(QFrame.Shape.VLine)

        # https://doc.qt.io/qt-6/qframe.html#Shadow-enum
        self.setFrameShadow(QFrame.Shadow.Raised)

        self.setLineWidth(1)
