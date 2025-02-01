"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: This class is intended to help with the line numbers area on the left side of the main document editor.

Features:
  - Shows line/block numbers for better text recognition.
  - Highlights the current line where the cursor is located.

Note:
  - If used with PyQt6, ensure slots and signals are declared correctly, as there are some differences:
    `from PyQt6.QtCore import pyqtSlot as Slot`

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2025 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import Qt, QRect, QSize, Slot
from PySide6.QtWidgets import QWidget, QTextEdit, QPlainTextEdit
from PySide6.QtGui import QPainter, QColor, QTextFormat

from typing import TYPE_CHECKING, Union

from . import Settings
from . import ThemeHelper

from ..edit_widget import EditWidget

if TYPE_CHECKING:
    from PySide6.QtCore import QObject  # noqa: F401
    from PySide6.QtGui import QTextCharFormat  # noqa: F401


class LineNumbers(QWidget):
    def __init__(self, editor: Union[EditWidget, QPlainTextEdit] = None):
        QWidget.__init__(self, editor)

        self.editor = editor

        """
        # Alternatively it can be get from AppConfig:
        font = QFont()
        font.setPointSize(AppConfig().get_font_size())
        self.setFont(font)
        """
        self.setFont(self.editor.document().defaultFont())  # Set global font to the line area

        # Theme helper
        self.theme_helper = ThemeHelper()

        # Settings
        self.settings = Settings(parent=self)

        # Connect editor's change events to line numbers updates
        self.editor.updateRequest.connect(self.update_request)
        self.editor.blockCountChanged.connect(self.update_width)

        # The current method of mixing background colors does not yield clear results.
        # editor.cursorPositionChanged.connect(self.highlight_current_line)

        # Init object with direct updates
        self.update_numbers()

        # self.highlight_current_line()

    def sizeHint(self) -> QSize:
        return QSize(self.line_numbers_width(), 0)

    def get_numbers_area(self, area_block) -> QRect:
        """
        Calculates the area occupied by the line numbers widget for a given block, adjusted for
        the block's position within the document.

        For more information on QPainter usage, see: https://doc.qt.io/qt-6/qpainter.html#translate-2

        Args:
            area_block (QTextBlock): The text block for which to calculate the area,
                                     typically retrieved with self.editor.firstVisibleBlock().

        Returns:
            QRect: The calculated rectangular area that the line numbers widget occupies.
        """

        # Get the bounding rectangle adjusted for the block's position within the document,
        # which can include translation offsets:
        area_top = self.editor.blockBoundingGeometry(area_block).translated(self.editor.contentOffset()).top()

        # Calculate the height of the block's bounding rectangle (local coordinates)
        area_height = self.editor.blockBoundingRect(area_block).height()

        # Alternative approach (constant line height):
        # self.fontMetrics().height() * block.lineCount()

        # Return the computed QRect for the area
        return QRect(0, int(area_top) + 1, self.width(), int(area_height))

    def paintEvent(self, event) -> None:
        painter = QPainter(self)

        # Line number and background colors
        number_color = QColor(self.theme_helper.get_color('edit_widget_line_numbers_color'))
        number_background = QColor(self.theme_helper.get_color('edit_widget_line_numbers_background'))
        # Current line number and background colors
        current_number_color = QColor(self.theme_helper.get_color('edit_widget_line_numbers_active_number'))
        current_number_background = QColor(
            self.theme_helper.get_color('edit_widget_line_numbers_active_number_background'))

        # Get current line number (block) to highlight
        cursor = self.editor.textCursor()
        current_line_block_number = cursor.block().blockNumber()

        block = self.editor.firstVisibleBlock()
        block_number = block.blockNumber()

        # Calculate the line numbers area for the specified block
        numbers_area = self.get_numbers_area(block)

        # Get the editor's geometry (position and size)
        background_area = self.editor.geometry()
        background_area.adjust(1, 1, 0, -1)  # Reduce by 1 pixel on each corresponding side

        # Set the width of the background area to match the line numbers widget
        background_area.setWidth(self.width())

        # Fill the adjusted area with the background color
        painter.fillRect(background_area, number_background)

        while block.isValid() and numbers_area.top() <= event.rect().bottom():
            if numbers_area.bottom() >= event.rect().top():
                if current_line_block_number == block_number:
                    """
                    Highlight current line number
                    More info of how to fill rectangle area https://doc.qt.io/qt-6/qpainter.html#fillRect-4
                    """
                    painter.fillRect(numbers_area, current_number_background)
                    painter.setPen(current_number_color)
                else:
                    # Not selected number color
                    painter.fillRect(numbers_area, Qt.GlobalColor.transparent)
                    """
                    Also:
                    - painter.setPen(Qt.GlobalColor.darkGray)
                    - QColor(Qt.GlobalColor.green).lighter(179)
                    Global color enum https://doc.qt.io/qt-6/qt.html#GlobalColor-enum
                    It can be a color value or pre-set enum's value by name, like: Qt.GlobalColor.transparent
                    """
                    painter.setPen(number_color)

                number = str(block_number + 1)
                # Shift to the left to get the right padding from the overall padding
                painter.drawText(-2, numbers_area.top(), self.width(), self.fontMetrics().height(),
                                 Qt.AlignmentFlag.AlignRight, number)

            block = block.next()
            if block.isValid():
                block_number = block.blockNumber()
                numbers_area = self.get_numbers_area(block)

        painter.end()

    @Slot(QRect, int)
    def update_request(self, rect, dy) -> None:
        visible_rect = self.editor.viewport().rect()
        if dy:
            # Scroll the widget vertically by dy pixels
            self.scroll(0, dy)

        if rect.contains(visible_rect):
            # If the entire viewport is contained within rect, update rect area
            self.update(rect)  # Explicitly requests a repaint
            self.update_width()
        else:
            # Otherwise, update only the visible viewport area
            self.update(visible_rect)  # Explicitly requests a repaint
            # Previous approach:
            # self.update(0, rect.y(), self.width(), rect.height())

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
            _format = selection.format  # type: ignore
            _format.setBackground(line_color)
            _format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            # extra_selections.append(selection)
            selection.format = _format
            self.editor.setExtraSelections([selection])

    def update_numbers(self) -> None:
        # Get element parent's contents size as the text edit widget may not be resized yet
        parent_obj = self.editor.parent()  # type: Union[QObject, QWidget]
        element_cr = parent_obj.contentsRect()
        # Update width first
        self.update_width()
        # Or it can be like this: height = self.editor.frameGeometry().height()
        self.setGeometry(
            QRect(element_cr.left(), element_cr.top(),
                  self.line_numbers_width(), element_cr.height() + self.fontMetrics().height())
        )

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
