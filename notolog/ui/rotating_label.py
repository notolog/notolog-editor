"""
Notolog Editor
Open-source markdown editor developed in Python.

File Details:
- Purpose: Provides a waiting UI element to emphasize in-progress operations.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QTransform, QPainter


class RotatingLabel(QLabel):
    def __init__(self, pixmap: QPixmap, parent=None):
        super().__init__(parent)

        self.rotation_angle = 0

        # Or just: self.pixmap = QPixmap("pixmap.png")
        self.pixmap = pixmap

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_rotation)
        self.timer.start(50)  # Rotate every X milliseconds

    def setPixmap(self, pixmap):
        super().setPixmap(pixmap)
        self.pixmap = pixmap

    def paintEvent(self, event) -> None:
        """
        Works when self.show() triggered
        @param event: QPainter event
        @return: None
        """
        painter = QPainter(self)
        transform = QTransform().rotate(self.rotation_angle)
        rotated_pixmap = self.pixmap.transformed(transform, Qt.TransformationMode.SmoothTransformation)
        painter.drawPixmap(self.rect(), rotated_pixmap)

    def update_rotation(self):
        self.rotation_angle += 5  # Rotate by X degrees
        self.rotation_angle %= 360  # Ensure rotation angle stays within the range
        self.update()
