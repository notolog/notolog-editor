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
