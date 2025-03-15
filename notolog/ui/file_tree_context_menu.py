"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: File tree context menu that displays context actions for files to the user.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2025 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtGui import QAction, QColor
from PySide6.QtWidgets import QMenu

from . import Settings
from . import Lexemes
from . import ThemeHelper
from . import ClipboardHelper

from ..ui.create_new_dir_dialog import CreateNewDirDialog

import os
import logging


class FileTreeContextMenu(QMenu):
    def __init__(self, file_path: str = None, parent=None):
        super().__init__(parent)

        self.parent = parent
        # Target file path
        self.file_path = file_path

        # Apply font from the parent instance to the menu
        self.setFont(self.parent.font())

        self.settings = Settings(parent=self)

        self.logger = logging.getLogger('file_tree_context_menu')

        # Load lexemes for the selected language and scope
        self.lexemes = Lexemes(self.settings.app_language, default_scope='common')

        # Theme helper
        self.theme_helper = ThemeHelper()

        self.init_ui()

    def init_ui(self):
        # menu = QMenu(self)
        # Font is already set in constructor
        # menu.setFont(self.font())

        current_dir_path = self.parent.get_tree_active_dir()

        if self.file_path:
            if os.path.isfile(self.file_path):
                self.file_menu()
            elif os.path.isdir(self.file_path):
                # Create a sub-directory
                current_dir_path = self.file_path

        self.tree_menu(dir_path=current_dir_path)

    def file_menu(self):
        # Copy file path context action
        copy_file_path_icon = self.theme_helper.get_icon(
            theme_icon='signpost-split.svg', system_icon='edit-copy',
            color=QColor(self.theme_helper.get_color('main_tree_context_menu_copy_file_path')))
        self.addAction(copy_file_path_icon, self.lexemes.get('menu_action_copy_file_path'),
                       lambda: self.copy_file_path_dialog(self.file_path))

        # Rename file context action
        rename_icon = self.theme_helper.get_icon(
            theme_icon='cursor-text.svg', system_icon='document-properties',
            color=QColor(self.theme_helper.get_color('main_tree_context_menu_rename')))
        self.addAction(rename_icon, self.lexemes.get('menu_action_rename'),
                       lambda: self.parent.rename_file_dialog(self.file_path))

        if self.parent.is_file_safely_deleted(self.file_path):
            # Restore deleted file context action
            restore_icon = self.theme_helper.get_icon(
                theme_icon='box-arrow-up.svg', system_icon='edit-undo',
                color=QColor(self.theme_helper.get_color('main_tree_context_menu_restore')))
            self.addAction(restore_icon, self.lexemes.get('menu_action_restore'),
                           lambda: self.parent.restore_file_dialog(self.file_path))
            # Delete completely file context action
            delete_icon = self.theme_helper.get_icon(
                theme_icon='x-square-fill.svg', system_icon='edit-delete',
                color=QColor(self.theme_helper.get_color('main_tree_context_menu_delete_completely')))
            self.addAction(delete_icon, self.lexemes.get('menu_action_delete_completely'),
                           lambda: self.parent.delete_completely_file_dialog(self.file_path))
        else:
            # Delete file context action
            delete_icon = self.theme_helper.get_icon(
                theme_icon='x-square.svg', system_icon='edit-delete',
                color=QColor(self.theme_helper.get_color('main_tree_context_menu_delete')))
            self.addAction(delete_icon, self.lexemes.get('menu_action_delete'),
                           lambda: self.parent.delete_file_dialog(self.file_path))

    def tree_menu(self, dir_path: str):
        # Create new dir context action
        create_new_dir_icon = self.theme_helper.get_icon(
            theme_icon='folder-plus.svg', system_icon='folder-new',
            color=QColor(self.theme_helper.get_color('main_tree_context_menu_create_new_dir')))
        create_new_dir_action = QAction(self.lexemes.get('menu_action_create_new_dir'), self)
        create_new_dir_action.setIcon(create_new_dir_icon)
        create_new_dir_action.triggered.connect(lambda: self.create_new_dir_dialog(base_dir=dir_path))
        # Set as not accessible if no write access
        if not os.access(dir_path, os.W_OK):
            create_new_dir_action.setEnabled(False)
        # Add the action to the toolbar
        self.addAction(create_new_dir_action)

    def copy_file_path_dialog(self, file_path):
        # Copy text to the clipboard
        ClipboardHelper.set_text(file_path)

    def create_new_dir_dialog(self, base_dir):
        # Show create a new folder dialog
        dialog = CreateNewDirDialog(base_dir, parent=self.parent)
        dialog.exec()
