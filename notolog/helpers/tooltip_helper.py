from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QWidget, QToolTip


class TooltipHelper(QWidget):

    @staticmethod
    def show_tooltip(widget: QWidget, text: str, offset=QPoint(20, -20)) -> None:
        """
        # Using the static method to show the tooltip
        TooltipManager.show_tooltip(self.button, "Copied!", QPoint(20, -20)
        @param widget: tooltip's target
        @param text: tooltip's text
        @param offset: tooltip's offset
        @return: None
        """

        # Adjust where the tooltip should appear
        global_pos = widget.mapToGlobal(QPoint(0, 0)) + offset

        # Show tooltip
        QToolTip.showText(global_pos, text, widget)
