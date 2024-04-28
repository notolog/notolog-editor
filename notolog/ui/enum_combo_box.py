from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QComboBox


class EnumComboBox(QComboBox):
    def __init__(self, enum_class):
        super().__init__()
        self._enum_class = enum_class

        # Load the Enum values
        for enum_value in enum_class:
            self.addItem(enum_value.value, userData=enum_value)

            # Check if the current item is a legacy item
            if hasattr(enum_value, 'legacy') and enum_value.legacy:
                # Get the index of the item we just added
                index = self.count() - 1
                # Set a custom style for legacy items (e.g., gray text color)
                self.setItemData(index, QColor('red'), Qt.ItemDataRole.ForegroundRole)
                # Alternatively, disable the item if you don't want it selectable
                # self.model().item(index).setEnabled(False)

    @property
    def enum_class(self):
        return self._enum_class
