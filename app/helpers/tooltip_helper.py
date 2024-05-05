from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QWidget, QToolTip


class TooltipHelper(QWidget):

    @staticmethod
    def show_tooltip(widget: QWidget, text: str, offset=QPoint(20, -20)) -> None:
        """
        Displays a tooltip for a specified widget.

        This static method is used to show a tooltip near a widget with custom text and a positional offset.

        Args:
            widget (QWidget): The widget for which the tooltip is displayed.
            text (str): The text displayed inside the tooltip.
            offset (QPoint): The offset from the widget's position where the tooltip should be shown.

        Returns:
            None
        """

        """
        # Using the static method to show the tooltip
        TooltipManager.show_tooltip(self.button, "Copied!", QPoint(20, -20)
        """

        # Adjust where the tooltip should appear
        global_pos = widget.mapToGlobal(QPoint(0, 0)) + offset

        # Show tooltip
        QToolTip.showText(global_pos, text, widget)
