"""
Notolog Editor
Open-source markdown editor developed in Python.

File Details:
- Purpose: Extends QWidget functionality to provide horizontal UI spacer.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QSpacerItem, QSizePolicy


class HorizontalLineSpacer(QWidget):
    """
    Vertical line separator for the status bar.
    """

    def __init__(self, parent=None):
        super(HorizontalLineSpacer, self).__init__(parent)

        # Main spacer layout
        main_layout = QVBoxLayout(self)

        # Add spacer above the line
        main_layout.addSpacerItem(QSpacerItem(0, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # Add horizontal delimiter
        line = QFrame(self)
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(line)

        # Add spacer below the line
        main_layout.addSpacerItem(QSpacerItem(0, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
