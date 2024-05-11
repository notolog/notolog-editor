from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QComboBox


class EnumComboBox(QComboBox):
    def __init__(self, enum_class):
        super().__init__()
        self._enum_class = enum_class

        # Sort the Enum members by value
        # sorted_members = sorted(enum_class, key=lambda x: x.value)

        # Load the Enum values
        for enum_value in enum_class:  # Or: sorted_members
            self.addItem(enum_value.value, userData=enum_value)

            # Add separator. It also adds extra index to the QComboBox
            # if hasattr(enum_value, 'is_default') and enum_value.is_default:
            #    self.insertSeparator(i + 1)

            # Check if the current item is a legacy item
            if hasattr(enum_value, 'legacy') and enum_value.legacy:
                # Get the index of the item we just added
                index = self.count() - 1
                # Set a custom style for legacy items (e.g., gray text color)
                self.setItemData(index, QColor('gray'), Qt.ItemDataRole.ForegroundRole)
                # Alternatively, disable the item if you don't want it selectable
                # self.model().item(index).setEnabled(False)

    @property
    def enum_class(self):
        return self._enum_class
