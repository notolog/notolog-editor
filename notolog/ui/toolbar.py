from PySide6.QtGui import QAction
from PySide6.QtWidgets import QToolBar, QMenu

from ..app_config import AppConfig
from ..settings import Settings

import logging


class ToolBar(QToolBar):
    # Main window toolbar class

    def __init__(self, parent=None, labels=None, refresh=None):
        """
        Args:
            parent (optional): Parent object
            labels (List[Dict[str, Any]], optional): The map with the toolbar's buttons
            refresh (Callable[[int, int], int], optional): A lambda function that refreshes a toolbar
        """
        super(ToolBar, self).__init__(parent)

        if self.parent and hasattr(self.parent, 'font'):
            # Apply font from the main window to the dialog
            self.setFont(self.parent.font())

        self.logger = logging.getLogger('toolbar')

        self.logging = AppConfig.get_logging()
        self.debug = AppConfig.get_debug()

        self.labels = labels
        self.refresh = refresh

        self.settings = Settings()

        # Sometimes (when weights changed) the values could be reset like this:
        # self.settings.toolbar_icons = None

        if self.settings.toolbar_icons is None or self.settings.toolbar_icons == 0:
            """
            Default bit-mask is 131070 when all icons are checked.
            """
            self.settings.toolbar_icons = 131070
            if self.debug:
                self.logger.info('Starting with default icons mask "%d"' % self.settings.toolbar_icons)

        self.buttons = {}

    def contextMenuEvent(self, event):
        """
        Render context menu event upon the toolbar right mouse click
        """
        current_action = self.actionAt(event.pos())
        if current_action is None:
            return

        if self.labels is None:
            return

        menu = QMenu(self)

        _weights = 0
        for index, label in enumerate(self.labels, 1):
            if 'type' not in label or label['type'] != 'action':
                menu.addSeparator()
                continue

            # Get settings weight of the item
            settings_weight = pow(2, label['weight'])

            if _weights & settings_weight:
                # The item is already added or the active state item that shouldn't be duplicated
                continue

            button = QAction(label['label'], self)
            button.setFont(self.font())

            slot = lambda checked, i=label['weight']: self.toolbar_menu_item(checked, i)
            # Check button.toggled.connect()
            button.triggered[bool].connect(slot)
            button.setCheckable(True)
            # Check the item is in the settings weights
            button.setChecked(self.settings.toolbar_icons & settings_weight)

            button_action = menu.addAction(button)

            self.buttons[index] = button

            # Collect items already added to the context menu
            _weights |= settings_weight

        # PoC remove element from the toolbar
        # delete_action  = menu.addAction("Hide")

        action = menu.exec(event.globalPos())

        # PoC Remove element from the toolbar
        # if action == delete_action:
        #    self.removeAction(current_action)

    def toolbar_menu_item(self, checked: bool, index: int) -> None:
        """
        Draw context menu item with a checkbox

        Args:
            checked (bool): Checked or not
            index (int): Index in a toolbar menu mapping
        """
        pi = pow(2, index)
        if self.debug:
            self.logger.info('checked:{} index:{} pi:{}' . format(checked, index, pi))
        if index in self.buttons:
            self.buttons[index].setChecked(checked)
        if checked:
            self.settings.toolbar_icons |= pi
        else:
            self.settings.toolbar_icons ^= pi
        # Re-draw toolbar with a callback
        if callable(self.refresh):
            self.refresh()

    # PoC Remove element from the toolbar
    # def removeAction(self, action):
    #    """
    #    Override removeAction() method upon QWidgetAction
    #
    #    Args:
    #        action (QAction):
    #    """
    #    super(ToolBar, self).removeAction(action)
    #
    #    if self.debug:
    #        self.logger.info('Remove element action "%s"' % action)
