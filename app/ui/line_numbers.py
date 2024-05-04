# This class is intended to help with line numbers area on the left side of the main document editor.
# The bale functions are:
# - Show line/block number for better text recognition.
# - Highlight current line where the cursor located.

# If used with PyQt6 make sure slots and signals are declared correctly, as there are some differences:
# from PyQt6.QtCore import pyqtSlot as Slot

from PySide6.QtCore import Qt, QObject, QRect, QSize, Slot
from PySide6.QtWidgets import QWidget, QTextEdit, QPlainTextEdit
from PySide6.QtGui import QPainter, QColor, QTextFormat, QTextCharFormat, QFont

from typing import Union

from ..app_config import AppConfig
from ..edit_widget import EditWidget
from ..helpers.theme_helper import ThemeHelper
from ..settings import Settings


class LineNumbers(QWidget):
    def __init__(self, editor: Union[EditWidget, QPlainTextEdit] = None):
        QWidget.__init__(self, editor)

        self.editor = editor

        """
        # Alternatively it can be get from AppConfig:
        font = QFont()
        font.setPointSize(AppConfig.get_font_size())
        self.setFont(font)
        """
        self.setFont(self.editor.document().defaultFont())  # Set global font to the line area

        # Theme helper
        self.theme_helper = ThemeHelper()

        # Settings
        self.settings = Settings(parent=self)

        editor.updateRequest.connect(self.update_request)
        editor.blockCountChanged.connect(self.update_width)
        # TODO set up in settings and find out the better way to highlight the line (when mixing backgrounds)
        # editor.cursorPositionChanged.connect(self.highlight_current_line)

        # Init object with direct updates
        self.update_numbers()

        # self.highlight_current_line()

    def sizeHint(self) -> QSize:
        return QSize(self.line_numbers_width(), 0)

    def paintEvent(self, event) -> None:
        self.line_numbers_paint_event(event)

    @Slot(QRect, int)
    def update_request(self, rect, dy) -> None:
        if dy:
            self.scroll(0, dy)
        else:
            self.update(0, rect.y(), self.width(), rect.height())
        if rect.contains(self.editor.viewport().rect()):
            self.update_width()

    @Slot(int)
    def update_width(self) -> None:
        self.editor.setViewportMargins(self.line_numbers_width(), 0, 0, 0)

    @Slot()
    def highlight_current_line(self) -> None:
        # The text edit widget is not intended to be a read only atm, but check it anyway to make it future-proof
        if not self.editor.isReadOnly():
            selection = QTextEdit.ExtraSelection()  # type: Union[QTextEdit.ExtraSelection, QTextCharFormat, None]
            if not selection:
                return
            selection.cursor = self.editor.textCursor()
            selection.cursor.clearSelection()
            # Set selection properties
            # line_color = QColor(Qt.GlobalColor.green).lighter(175)  # As an example of how to shift base color tone
            line_color = QColor(self.theme_helper.get_color('edit_widget_line_numbers_active_line_background'))
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            # extra_selections.append(selection)
            self.editor.setExtraSelections([selection])

    def update_numbers(self) -> None:
        # Get element parent's contents size as the text edit widget may not be resized yet
        parent_obj = self.editor.parent()  # type: Union[QObject, QWidget]
        element_cr = parent_obj.contentsRect()
        # Update width first
        self.update_width()
        # Or it can be like this: height = self.editor.frameGeometry().height()
        self.setGeometry(
            QRect(element_cr.left(), element_cr.top(), self.line_numbers_width(), element_cr.height())
        )

    def line_numbers_paint_event(self, event) -> None:
        painter = QPainter(self)
        """
        More info about painter https://doc.qt.io/qt-6/qpainter.html#translate-2
        Example: painter.translate(3, 0)

        Global color enum https://doc.qt.io/qt-6/qt.html#GlobalColor-enum
        It can be a color value or pre-set enum's value by name, like: Qt.GlobalColor.transparent
        """
        painter.fillRect(event.rect(), QColor(self.theme_helper.get_color('edit_widget_line_numbers_background')))

        # Get current line number (block) to highlight
        cursor = self.editor.textCursor()
        current_line_block_number = cursor.block().blockNumber()

        block = self.editor.firstVisibleBlock()
        block_number = block.blockNumber()

        top = self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top()
        bottom = top + self.editor.blockBoundingRect(block).height()

        number_color = QColor(self.theme_helper.get_color('edit_widget_line_numbers_color'))
        # Also: current_number_color = QColor(Qt.GlobalColor.green).lighter(179)
        current_number_color = QColor(self.theme_helper.get_color('edit_widget_line_numbers_active_number'))
        current_number_background = QColor(
            self.theme_helper.get_color('edit_widget_line_numbers_active_number_background'))

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                if current_line_block_number == block_number:
                    """
                    Highlight current line number
                    More info of how to fill rectangle area https://doc.qt.io/qt-6/qpainter.html#fillRect-4
                    """
                    painter.fillRect(0, int(top) + 1, self.width(), self.fontMetrics().height(),
                                     current_number_background)
                    painter.setPen(current_number_color)
                else:
                    # Common number color
                    # Also: painter.setPen(Qt.GlobalColor.darkGray)
                    painter.setPen(number_color)

                number = str(block_number + 1)
                # Minus shift to the left to get the right padding from the overall padding
                painter.drawText(-2, int(top) + 1, self.width(),
                                 self.fontMetrics().height(),
                                 Qt.AlignmentFlag.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + self.editor.blockBoundingRect(block).height()
            block_number += 1

    def line_numbers_width(self) -> int:
        """
        Get line space width
        @return: int value of space occupied by digits (incl. paddings)
        """
        if not self.visible():
            return 0

        digits = max(2, len(str(self.editor.blockCount())))
        # '5' is an overall value of left and right padding
        space = 5 + self.fontMetrics().horizontalAdvance("0") * digits
        return space

    def visible(self) -> bool:
        return self.settings.show_line_numbers