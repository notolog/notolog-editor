from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QDialogButtonBox, QSizePolicy
from PySide6.QtGui import QFontMetrics

from . import AppConfig

import logging


class CommonDialog(QDialog):

    debug = AppConfig.get_debug()

    def __init__(self, title=str, text=str, callback=None, parent=None):
        super().__init__(parent)

        self.parent = parent

        if self.parent and hasattr(self.parent, 'font'):
            # Apply font from the main window to the dialog
            self.setFont(self.parent.font())

        self.logger = logging.getLogger('common_dialog')

        self.setWindowTitle(str(title))
        self.setObjectName('common_dialog')

        # Set dialog size derived from the main window size
        """
        main_window_size = parent.size()
        # Will be adjusted with size hint later at resizeEvent()
        dialog_width = int(main_window_size.width() * 0.33)
        dialog_height = int(main_window_size.height() * 0.33)
        self.resize(dialog_width, dialog_height)
        """
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        if self.sizeHint().isValid():
            self.setMinimumSize(self.sizeHint())

        label = QLabel()
        label.setObjectName('common_label')
        label.setMargin(10)  # Set vertical padding for the dialog label
        label.setText(str(text))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.adjustSize()
        """
        Other examples of the widget geometry's adjustments:
        label.move(128, 64)
        label.setGeometry(QStyle.alignedRect(
            Qt.LayoutDirection.LeftToRight,
            Qt.AlignmentFlag.AlignCenter,
            dialog.size(),
            dialog.geometry()))
        """

        button_box = QDialogButtonBox()
        button_box.setObjectName('button_box')
        button_box.setOrientation(Qt.Orientation.Horizontal)
        button_box.setStandardButtons(QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Yes)
        button_box.setCenterButtons(True)

        # not QVBoxLayout(self) to avoid: 'Attempting to add QLayout "" to ... "", which already has a layout
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button_box)
        self.setLayout(layout)

        self.adjust_minimum_width(str(title))

        if callable(callback):
            button_box.accepted.connect(lambda: callback(self.reject))
        else:
            if self.debug:
                self.logger.warning('No callback method provided for the dialog!')
            button_box.accepted.connect(self.close)

        button_box.rejected.connect(self.reject)

    def resizeEvent(self, event) -> None:
        """
        To make dialog stretch if the content size is longer than expected
        @param event: QEvent
        @return: None
        """
        # Get the preferred size of the dialog's content
        preferred_size = self.layout().sizeHint()
        # Adjust the dialog's size based on the preferred size then
        if preferred_size.isValid():
            self.resize(preferred_size)

    def adjust_minimum_width(self, title: str) -> None:
        # Calculate width required for the title text
        font_metrics = QFontMetrics(self.font())
        title_width = font_metrics.horizontalAdvance(title)

        # Set minimum width for the dialog
        self.setMinimumWidth(title_width + 150)  # Add some padding
