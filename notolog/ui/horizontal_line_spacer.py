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
