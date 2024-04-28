"""
Notolog: An open-source markdown editor written in Python. (https://github.com/notolog/notolog-editor)

Description:
The project began as part of the developer's journey to learn Python, which may explain some seemingly redundant
features. It was developed as a proof of concept to showcase what a markdown editor might look like and to assist
the developer with daily tasks. Hopefully, you will find it useful too.

The README.md file, located at the very beginning, was created using this editor and serves as a good demonstration
of the app’s features.

Code Style Disclaimer: While mixing code styles like camelCase and snake_case is generally avoided, many Qt methods
use camelCase. However, the preferred style for Python 3 is typically PEP-8, which advocates for snake_case. Therefore,
a compromise has been made in the Notolog codebase to predominantly use snake_case. This deliberate choice helps
distinguish between the Qt and Notolog codebases, making it easier to identify which methods or classes belong to each.

---

Additional Information:
- GitHub Repository: https://github.com/notolog/notolog-editor
- WebSite: https://notolog.app
- Author: Vadim Bakhrenkov
- License: MIT License
- Version: 0.9.0b0
"""

"""
Main UI class to set up the application's UI and to process any user actions.
"""

from .settings import Settings
from .ui.settings_dialog import SettingsDialog
from .app_config import AppConfig
from .file_header import FileHeader
from .edit_widget import EditWidget
from .view_widget import ViewWidget
from .view_processor import ViewProcessor
from .view_decorator import ViewDecorator
from .ui.ai_assistant import AIAssistant
from .ui.about_popup import AboutPopup

# UI
from .ui.file_system_model import FileSystemModel
from .ui.sort_filter_proxy_model import SortFilterProxyModel
from .ui.toolbar import ToolBar
from .ui.statusbar import StatusBar
from .ui.line_numbers import LineNumbers
from .ui.common_dialog import CommonDialog
from .ui.rename_file_dialog import RenameFileDialog
from .ui.color_picker_dialog import ColorPickerDialog

# Highlight
from .highlight.md_highlighter import MdHighlighter
from .highlight.view_highlighter import ViewHighlighter

# Encrypt
from .encrypt.enc_helper import EncHelper
from .encrypt.enc_password import EncPassword
from .encrypt.enc_new_password_dialog import EncNewPasswordDialog
from .encrypt.enc_password_dialog import EncPasswordDialog
from .encrypt.enc_password_reset_dialog import EncPasswordResetDialog
from cryptography.fernet import InvalidToken, InvalidSignature

# Helpers
from .helpers.theme_helper import ThemeHelper
from .helpers.clipboard_helper import ClipboardHelper
from .helpers.update_helper import UpdateHelper
from .helpers.file_helper import res_path, size_f, save_file

# Lexemes
from .lexemes.lexemes import Lexemes

from PySide6.QtCore import Qt, QDir, QPoint, QTimer, QSize
from PySide6.QtCore import QRegularExpression, QItemSelectionModel, QFileSystemWatcher
from PySide6.QtGui import QGuiApplication, QIcon, QAction, QColor, QTextDocument, QShortcut
from PySide6.QtGui import QKeySequence, QTextCursor, QFont, QTextBlock, QDesktopServices, QPalette
from PySide6.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QSplitter, QListView, QTextBrowser
from PySide6.QtWidgets import QPlainTextEdit, QToolButton, QSizePolicy, QStatusBar, QCheckBox, QToolBar
from PySide6.QtWidgets import QLabel, QLineEdit, QPushButton, QMenu, QDialog, QMessageBox, QStyle
from PySide6.QtWidgets import QAbstractItemView, QFileSystemModel, QFileDialog

from qasync import asyncSlot, asyncClose

# Markdown library
import markdown
# Markdown library extensions
from markdown.extensions.codehilite import CodeHiliteExtension
# Custom markdown extension to process element tree
from .etree_extension import ElementTreeExtension

# Emojis support
import emoji

import os
import math
import asyncio

from typing import Union, Optional, Callable, List, Dict, Any

import logging

from .editor_state import EditorState, Mode, Source, Encryption

"""
To change content scale ratio use either:
    # View widget
    view_widget = self.get_view_widget()  # type: Union[ViewWidget, QTextBrowser]
    view_widget.setZoomFactor(float(self.scale))
Or
    os.environ["QT_SCALE_FACTOR"] = "1.2"
As it works better than: `body { transform: scale(%s); transform-origin: 0 0; }`
"""

"""
Template to apply to the view mode.
"""
HTML_TPL = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>%s</title>
        <style type="text/css">
        %s
        </style>
    </head>
    <body>
    %s
    </body>
    </html>
    """


class NotologEditor(QMainWindow):

    AREA_WEIGHT = 5
    AREA_WEIGHT_TREE = 1
    AREA_WEIGHT_EDIT = 4
    AREA_WEIGHT_VIEW = 4

    """
    Some extensions like `codehilite` extension will be included later.

    Extra contains:
    * Abbreviations
    * Attribute Lists
    * Definition Lists
    * Fenced Code Blocks
    * Footnotes
    * Tables
    * Markdown in HTML

    More info https://python-markdown.github.io/extensions/extra/
    """
    md_extensions = [
        'markdown.extensions.extra',  # Or 'extra'
    ]

    def __init__(self, parent = None, **kwargs):
        super(NotologEditor, self).__init__(parent=parent)

        self.logger = logging.getLogger('notolog')

        self.logging  = AppConfig.get_logging()
        self.debug = AppConfig.get_debug()

        self.settings = Settings(parent=self)
        self.settings.value_changed.connect(
            lambda v: self.settings_update_handler(v))
        """
        Set theme:
        self.settings.theme = 'bordo'
        """

        # Default language setup, change to settings value to modify it via UI
        self.lexemes = Lexemes(self.settings.app_language)

        self.screen = None
        if 'screen' in kwargs:
            self.screen = kwargs['screen']

        """
        The `self.devicePixelRatio()` is also available through the `app.devicePixelRatio()`
        """
        self.dpr = self.devicePixelRatio()
        self.dpi = int(self.screen.physicalDotsPerInch())
        self.logical_dpi = int(self.screen.logicalDotsPerInch())

        # Set up global font params
        self.init_font()

        """
        Most monitors range around 100-200 DPI(depending on the screen size)
        while smartphone screens are more condensed and range from 300-600 DPI.
        """
        self.scale = ('%.1f' % (self.dpi / 200))

        if self.logging:
            self.logger.info(
                'Screen resolution: %d x %d' %
                (QGuiApplication.primaryScreen().availableGeometry().width(),
                 QGuiApplication.primaryScreen().availableGeometry().height())
            )
            self.logger.info('Screen DPI %d and scale %s' % (self.dpi, self.scale))
            self.logger.info('Device pixel ratio %d' % self.dpr)

        # self.showMaximized()

        self.estate = EditorState(self)
        self.estate.value_changed.connect(
            # Process updates upon mode changes
            # lambda *v: self.editor_state_update_handler(v,))  # (v,)
            lambda v: self.editor_state_update_handler(v))  # v

        # Mode, either view or edit more
        mode = Mode(self.settings.mode) if self.settings.mode > 0 else Mode.VIEW
        self.set_mode(mode)

        # Source, from which source the current mode gets the content
        source = Source(self.settings.source) if self.settings.source > 0 else Source.HTML
        self.set_source(source)

        # Encryption (start up value, could be changed later on)
        self.set_encryption(Encryption.PLAIN)

        """
        Encryption helpers cache.
        It could be a few of them as file specific salt may differ.
        """
        self.encrypt_helpers = {}
        # Encryption password object for this session
        self.enc_password = None  # type: Union[EncPassword, None]
        # The number of how many times a password dialog was shown before success
        self.enc_password_dialog_cnt = None  # type: Union[int, None]

        # Theme helper
        self.theme_helper = ThemeHelper()

        # Average weight to px ratio before it was calculated
        self.weight_to_px_uno = 255

        # Local content state
        self.file_path = None  # type: Union[str, None]
        self.header = None  # type: Union[FileHeader, None]
        self.content = None  # type: string=None

        # Views fields
        self.editor_container = None  # type: Union[QVBoxLayout, None]
        self.text_view = None  # type: Union[ViewWidget, QTextBrowser,  None]
        self.view_doc = None  # type: Union[QTextDocument, None]
        self.text_edit = None  # type: Union[EditWidget, QPlainTextEdit, None]

        # Markdown instance
        self.md = None  # type: Union[markdown.Markdown, None]

        # Highlighters
        self.md_highlighter = None  # type: Union[MdHighlighter, None]
        self.view_highlighter = None  # type: Union[ViewHighlighter, None]

        # File tree and variable
        self.tree_container = None  # type: Union[QWidget, None]
        self.file_model = None  # type: Union[FileSystemModel, None]
        self.tree_view = None  # type: Union[QListView, None]
        self.tree_filter = None  # type: Union[QLineEdit, None]
        self.tree_proxy_model = None  # type: Union[SortFilterProxyModel, None]
        self.file_watcher = None  # type: Union[QFileSystemWatcher, None]

        # self.supported_file_types = ['*.md', '*.txt', '*.html', '*.enc']
        self.supported_file_extensions = ['md', 'txt', 'html', 'enc']

        # Line numbers within the document
        self.line_numbers = None  # type: Union[LineNumbers, None]

        # Toolbar
        self.toolbar = None  # type: Union[ToolBar, QToolBar, None]
        self.search_input = None  # type: Union[QLineEdit, None]
        self.btn_search_clear = None  # type: Union[QPushButton, None]
        self.btn_search_prev = None  # type: Union[QPushButton, None]
        self.btn_search_next = None  # type: Union[QPushButton, None]
        self.search_match_case = None  # type: Union[QCheckBox, None]

        # Statusbar
        self.statusbar = None  # type: Union[StatusBar, QStatusBar, None]

        # Current document's variables
        self.col_num = 0  # Column where cursor located at
        self.line_num = 0  # Machine-readable, starts from 0
        self.line_num_hr = 0  # Human-readable, starts from 1
        self.cursor_pos = 0  # Cursor position

        # Dialogs
        self.ai_assistant = None  # type: Union[QDialog, None]
        self.color_picker = None  # type: Union[QDialog, None]

        self.loop = asyncio.get_event_loop()

        """
        Dir and file to work with will be updated from settings.
        QDir.currentPath() or QDir.homePath() by default.
        """
        if not QDir.setCurrent(QDir.currentPath()):
            if self.logging:
                self.logger.info('Cannot change current path')

        # Init palette styles
        self.init_palette()

        # Init UI by setting up widgets and variables
        self.init_ui()

        # Run once again to refresh all dependant UI elements that have been initialized
        self.set_mode(mode)
        self.set_source(source)

        self.save_timer = QTimer(interval=15000, timeout=self.auto_save_file)
        self.save_timer.start()

        """
        Ctrl+S save current file.
        More info about the key enum: https://doc.qt.io/qt-6/qt.html#Key-enum
        More info about the keyboard modifier enum: https://doc.qt.io/qt-6/qt.html#KeyboardModifier-enum
        """
        shortcut_save = QShortcut(
            QKeySequence(Qt.KeyboardModifier.ControlModifier | Qt.Key.Key_S),
            self
        )
        # Reset 'allow save empty' dialog if save file action called explicitly
        shortcut_save.activated.connect(lambda: (self.estate.allow_save_empty_reset(), self.auto_save_file()))

        shortcut_search = QShortcut(
            QKeySequence(Qt.KeyboardModifier.ControlModifier | Qt.Key.Key_F),
            self
        )
        shortcut_search.activated.connect(self.search_text)

    def init_font(self):
        # Use default ratio
        font_size_ratio = 1.0
        font_size = int(self.settings.app_font_size * font_size_ratio)

        AppConfig.set_font_size(font_size)

        font = QFont()  # Accept args like "Sans Serif"
        font.setPointSize(font_size)

        if self.debug:
            self.logger.debug('Font point size set to %d, font size ratio %.2f'
                              % (font.pointSize(), font_size_ratio))
        self.setFont(font)

    def settings_update_handler(self, data: dict) -> None:
        """
        Perform actions upon settings change.
        Data comes in a view of a dictionary, where is the key is the setting name, and the value is the actual value.
        Can be resource greedy.

        @param data: dict, say {"show_line_numbers": True}
        @return: None
        """

        if self.debug:
            self.logger.debug('Settings update handler in use "%s"' % data)

        if 'show_line_numbers' in data and hasattr(self, 'line_numbers'):
            # Show / hide line numbers area
            self.line_numbers.update_numbers()

        if 'app_font_size' in data and hasattr(self, 'theme_helper'):
            # Set up global font params
            self.init_font()
            # Set up font to the view's document
            view_doc = self.get_view_doc()  # type: QTextDocument
            # Apply font from the main window to the widget
            view_doc.setDefaultFont(self.font())
            """
            # Or via view widget, also works
            view_widget = self.get_view_widget()  # type: Union[ViewWidget, QTextBrowser]
            view_widget.document().setDefaultFont(self.font())
            """
            # Edit widget
            edit_widget = self.get_edit_widget()  # type: Union[EditWidget, QPlainTextEdit]
            edit_widget.document().setDefaultFont(self.font())
            # Apply font from the main window to the widget
            self.tree_view.setFont(self.font())
            # Apply font from the main window to the widget
            self.tree_filter.setFont(self.font())
            # Update toolbar
            self.create_icons_toolbar(refresh=True)
            # Re-draw main menu
            self.draw_menu()
            # Update statusbar
            self.create_status_toolbar()
            # Refresh all dependant UI elements that have been initialized
            self.estate.refresh()
            self.statusbar['data_size_label'].setText("%s" % size_f(len(self.content)))
            # Update line numbers widget
            self.line_numbers.setFont(self.font())
            # Get app's global font size
            self.md_highlighter.font_size = AppConfig.get_font_size()
            # Re-highlight syntax if Mode.EDIT
            if self.get_mode() == Mode.EDIT:
                # Resource greedy syntax re-highlight
                self.md_highlighter.rehighlight()
                # Update line numbers widget width
                self.line_numbers.update_numbers()

        if 'app_language' in data and hasattr(self, 'lexemes'):
            # Reload lexemes with a new app language
            self.lexemes = Lexemes(self.settings.app_language)
            # Trigger editor state update
            self.estate.refresh()
            # Update window title
            self.set_app_title()  # Generic title without sub part
            # Update toolbar
            self.create_icons_toolbar(refresh=True)
            # Search field placeholder to empty
            self.search_input.setPlaceholderText(self.lexemes.get('search_input_placeholder_text', scope='toolbar'))
            # Re-draw main menu
            self.draw_menu()

        if 'app_theme' in data and hasattr(self, 'theme_helper'):
            self.theme_helper = ThemeHelper()
            # Update app's palette styles
            self.init_palette()
            # Tree container
            tree_container = self.get_tree_container()  # type: Union[QWidget]
            tree_container.setStyleSheet(self.theme_helper.get_css('tree_view'))  # Re-apply styles to the elements
            self.file_model.clear_highlights()
            # self.toolbar.setStyleSheet(self.theme_helper.get_css('toolbar'))
            self.create_icons_toolbar(refresh=True)  # Custom method to set up icon colors, etc.
            self.statusbar.setStyleSheet(self.theme_helper.get_css('statusbar'))
            # View document
            view_doc = self.get_view_doc()  # type: QTextDocument
            view_doc.setDefaultStyleSheet(self.theme_helper.get_css('styles'))  # Mind the setDefaultStyleSheet()
            # Edit widget
            edit_widget = self.get_edit_widget()  # type: Union[EditWidget, QPlainTextEdit]
            edit_widget.setStyleSheet(self.theme_helper.get_css('editor'))
            # View widget
            view_widget = self.get_view_widget()  # type: Union[ViewWidget, QTextBrowser]
            view_widget.setStyleSheet(self.theme_helper.get_css('viewer'))
            # Update code highlighter to reload color scheme
            self.md_highlighter = MdHighlighter(document=edit_widget.document())
            # Update view highlighter to reload color scheme
            self.view_highlighter = ViewHighlighter(document=view_doc)
            # Save any unsaved changes before calling file reload
            self.save_active_file(clear_after=False)
            # To allow view document reload highlighter styles
            self.reload_active_file()

        if 'show_main_menu' in data:
            # Re-draw main menu
            self.draw_menu()

        if (any(item in ['viewer_highlight_todos', 'viewer_process_emojis']  # Check item
                # Take item from the data
                for item in data)
                and self.get_mode() == Mode.VIEW):
            # To allow view document reload highlighter styles and other processing
            self.reload_active_file()

        if 'show_global_cursor_position' in data:
            # To allow to reload the statusbar
            self.estate.refresh()

        if 'viewer_open_link_confirmation' in data:
            # View widget
            view_widget = self.get_view_widget()  # type: Union[ViewWidget, QTextBrowser]
            # Disconnect previous lambda
            view_widget.anchorClicked.disconnect()
            # Set up connection again
            view_widget.anchorClicked.connect(self.open_link_dialog_proxy())

    def editor_state_update_handler(self, data: dict) -> None:
        """
        Perform actions belonging to the editor state changed, say mode toggle event.
        When switching between VIEW and EDIT mode some icons and texts may look differ, have different actions, etc.
        """

        if self.debug:
            self.logger.debug('Editor state update handler in use "%s"' % data)

        # Initially the elements may not exist, but apper later on
        if hasattr(self, 'statusbar'):
            if data['c'] == Mode:
                mode_label_text = self.lexemes.get(
                    'statusbar_mode_label_mode_%s' % Mode(self.get_mode()).name.lower(), scope='statusbar')
                self.statusbar['mode_label'].setText(mode_label_text)
            if data['c'] == Source:
                source_label_text = self.lexemes.get(
                    'statusbar_source_label_source_%s' % Source(self.get_source()).name.lower(), scope='statusbar')
                self.statusbar['source_label'].setText(source_label_text)
            if data['c'] == Encryption:
                encryption_symbol_encrypted = self.lexemes.get('statusbar_encryption_symbol_encrypted_label',
                                                               scope='statusbar')
                encryption_symbol_unencrypted = self.lexemes.get('statusbar_encryption_symbol_unencrypted_label',
                                                                 scope='statusbar')
                encryption_symbol = encryption_symbol_encrypted if self.get_encryption() == Encryption.ENCRYPTED\
                    else encryption_symbol_unencrypted
                encryption_status = self.lexemes.get('statusbar_encryption_label_encryption_%s'
                                              % Encryption(self.get_encryption()).name.lower(), scope='statusbar')
                encryption_label_text = self.lexemes.get('statusbar_encryption_label', scope='statusbar',
                                                         encryption=encryption_status, icon=encryption_symbol)
                self.statusbar['encryption_label'].setText(encryption_label_text)
            # Show cursor position data
            self.statusbar['cursor_label'].setText(self.get_cursor_label_text())
            # Restore litter bin state
            self.statusbar.set_litter_bin_visibility(visible=self.settings.show_deleted_files)

        # Switching between Mode.VIEW and Mode.EDIT
        if self.get_mode() == Mode.EDIT:
            # Hide element first. It helps to avoid visual glitches upon switching.
            if hasattr(self, 'text_view'):
                if data['c'] == Mode:
                    # Save cursor position (viewport for previous mode)
                    self.store_doc_cursor_pos(mode=data['pv'])  # Or just: self.get_prev_mode()
                # Hide widget
                self.text_view.hide()
            if hasattr(self, 'text_edit'):
                self.text_edit.show()
            # Clear search fields and statuses
            if hasattr(self, 'search_input'):
                self.action_search_clear()
        else:
            """
            Hide element first. It helps to avoid visual glitches upon switching.
            Switching from Mode.EDIT to Mode.VIEW | Mode.SOURCE
            """
            if hasattr(self, 'text_edit'):
                self.text_edit.hide()
            if hasattr(self, 'text_view'):
                self.text_view.show()
                # This re-set up helps to avoid weirdly collapsed content within the restored document.
                self.text_view.setDocument(self.text_view.document())
                # Just in case if needed: self.text_view.reload()
                if data['c'] == Mode:
                    # Save cursor position (for previous mode)
                    self.restore_doc_cursor_pos(mode=data['pv'], source_widget=self.text_view)
            # Clear search fields and statuses
            if hasattr(self, 'search_input'):
                self.action_search_clear()

        if hasattr(self, 'toolbar'):  # For updates only
            self.create_icons_toolbar(refresh=True)
            # Re-draw main menu as well, as some action set there
            self.draw_menu()

    def init_encrypt_helper(self, enc_password: EncPassword = None, salt: str = None, iterations: int = None) -> EncHelper:
        """
        Salt could be empty or file dependant.
        """
        self.enc_password = enc_password
        encrypt_helper = EncHelper(enc_password=self.enc_password, salt=salt, iterations=iterations)
        return self.set_encrypt_helper(salt, encrypt_helper)

    def reset_encrypt_helper(self, callback: Optional[Callable[..., Any]] = None):
        """
        Reset if a file encrypted with another key or when ever it needed
        """
        self.enc_password = None
        for salt, encrypt_helper in self.encrypt_helpers.items():
            self.set_encrypt_helper(salt, None)
        if callback is not None:
            callback()

    def set_encrypt_helper(self, salt, encrypt_helper: EncHelper = None) -> EncHelper:
        """
        Set either encrypt helper Object or None if header has been reset.
        """
        self.encrypt_helpers[salt] = encrypt_helper
        return encrypt_helper

    def get_encrypt_helper(self, salt: str, new_password: bool = False, hint: str = None,
                           iterations: int = None) -> EncHelper:
        """
        Encryption helper getter to allow cache the helper creation.
        """

        # Show enter password dialog if no password set
        if (not hasattr(self, 'enc_password')
                or self.enc_password is None
                or (self.enc_password and len(self.enc_password.password) == 0)):
            if new_password:
                self.enc_password = self.enc_new_password_dialog()
            else:
                self.enc_password = self.enc_password_dialog(hint=hint)

        # Try to retrieve the object from cache
        encrypt_helper = None
        if salt in self.encrypt_helpers:
            encrypt_helper = self.encrypt_helpers[salt]
        # Setup encrypt helper
        if encrypt_helper is None:
            # Important: can be initialised with no or wrong password!
            encrypt_helper = self.init_encrypt_helper(self.enc_password, salt, iterations)
        # Return initialised encrypt helper
        return encrypt_helper

    def init_md(self) -> None:
        """
        Init Markdown object and set it to variable.
        Add custom element tree extensions if needed.
        Add `codehilite` to make actual highlighter work (CodeHiliteExtension() or ['codehilite'])
        """
        extensions = self.md_extensions + [ElementTreeExtension(), CodeHiliteExtension(linenums=True)]
        # Init markdown object with the selected extensions
        self.md = markdown.Markdown(extensions=extensions)

    def convert_markdown_to_html(self, md_content: str) -> str:
        """
        Process Markdown syntax and convert it to html.
        """
        if not self.md:
            self.init_md()
        if self.settings.viewer_process_emojis:
            # Convert emojis.
            # TODO emojis language: language=self.settings.app_language
            md_content = self.convert_emojis(text_content=md_content)
        # Convert markdown to html
        html_content = self.md.convert(md_content)
        # Converted html data
        return html_content

    def convert_emojis(self, text_content: str, language: str = 'en') -> str:
        """
        Process emojis :cat: to 🐱 conversion
        """
        text_content = emoji.emojize(text_content, language=language)

        if self.debug:
            self.logger.debug('Emoji conversion called for language "%s"' % language)

        return text_content

    def init_ui(self) -> None:
        """
        Init main UI.
        """
        # Central widget
        container = QWidget(self)
        container.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(container)

        """
        Icon example based on system theme:
        app_icon = QIcon.fromTheme("edit-find", QIcon("..."))
        """
        app_icon = QIcon(self.theme_helper.get_app_icon_path())
        self.setWindowIcon(app_icon)

        # Layout for main widget either horizontal or vertical
        layout = QVBoxLayout()

        # App menu
        self.draw_menu()

        # Main icons toolbar
        self.create_icons_toolbar()

        # Main status toolbar
        self.create_status_toolbar()

        # Create a splitter and set its orientation to horizontal (widgets from left to right)
        splitter = QSplitter(self)
        splitter.setOrientation(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(7)
        splitter.splitterMoved.connect(self.splitter_moved_handler)

        # File navigation panel
        tree_container = self.create_navigation_panel()
        splitter.addWidget(tree_container)

        # The layout contains either document viewer or editor widget. One would be hidden.
        editor_layout = QVBoxLayout()  # type: QVBoxLayout
        editor_layout.setContentsMargins(0, 0, 0, 0)  # No padding within this layout

        # Editor widget
        text_edit = self.create_editor_panel()
        editor_layout.addWidget(text_edit)

        # View widget
        text_view = self.create_view_panel()
        editor_layout.addWidget(text_view)
        """
        With QGridLayout it can utilise frame weights, like:
        layout.addWidget(view_widget, 0, 1, 1, self.AREA_WEIGHT_VIEW)
        """

        # File navigation panel
        editor_container = self.get_editor_container()
        # Set layout to the widget to add it to the splitter then.
        editor_container.setLayout(editor_layout)
        splitter.addWidget(editor_container)

        # Show line numbers widget
        self.create_line_numbers(text_edit)

        layout.addWidget(splitter)

        # Set the layout for the main widget
        container.setLayout(layout)

        # Set up main window title
        self.set_app_title()

        # Screen geometry
        geo_screen = self.screen.availableGeometry()
        """
        Set app's window minimum size according to the screen size.
        Check setFixedSize() and setBaseSize() as well.
        """
        self.setMinimumSize(0.33 * geo_screen.size())
        # Restore size from settings
        if self.settings.ui_width > 0 and self.settings.ui_height > 0:
            self.resize(QSize(self.settings.ui_width, self.settings.ui_height))
        # Set maximum size equals the size of the screen
        self.setMaximumSize(geo_screen.size())
        # Frameless
        # self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setGeometry(
            QStyle.alignedRect(
                Qt.LayoutDirection.LeftToRight,
                # More info about the enum: https://doc.qt.io/qt-6/qt.html#AlignmentFlag-enum
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop,
                self.size(),
                geo_screen,
            )
        )
        """
        Move app window after alignment.
        If the app window is going to be outside the screen boundaries,
        system UI aligns it with right bottom screen position automatically.
        But keep the fallback check (0.99) anyway.
        """
        if (self.settings.ui_pos_x > 0 and self.settings.ui_pos_y > 0
                and self.settings.ui_pos_x / geo_screen.size().width() < 0.99
                and self.settings.ui_pos_y / geo_screen.size().height() < 0.99):
            self.move(self.settings.ui_pos_x, self.settings.ui_pos_y)
        else:
            # These are just default screen corner margin values that will be rewritten later.
            self.move(99, 77)

        self.load_default_page()

        # Show the main window
        self.show()

        # Update line numbers area geometry
        if hasattr(self, 'line_numbers'):
            self.line_numbers.update_numbers()

        if self.debug:
            self.logger.debug(f"Current splitter widgets proportions: {splitter.sizes()}")

        # Previous approach
        """
        # Editor container, contains edit and view widgets both
        editor_container = self.get_editor_container()
        editor_container.resize(self.weight_to_px_uno * self.AREA_WEIGHT_EDIT, ui_height)

        # Tree container
        tree_container = self.get_tree_container()
        tree_container.resize(self.weight_to_px_uno * self.AREA_WEIGHT_TREE, ui_height)

        # Keep the tree's minimum width
        self.tree_view.setMinimumWidth(self.weight_to_px_uno * self.AREA_WEIGHT_TREE)
        """

        position = self.settings.ui_splitter_pos
        # Set initial widget proportions for splitter
        if not position:
            # After app's UI width is completely set, or it may not work:
            splitter_width_col = int(
               (self.frameGeometry().width() - splitter.handleWidth() * (splitter.count() - 1)) / self.AREA_WEIGHT
            )  # Fallback to default proportions
            splitter.setSizes([self.AREA_WEIGHT_TREE * splitter_width_col, self.AREA_WEIGHT_EDIT * splitter_width_col])
        else:
            # Based on previously saved proportions
            total_size = sum(splitter.sizes())
            splitter.setSizes([position, total_size - position])

        if self.debug:
            self.logger.debug(f"Updated splitter widgets proportions: {splitter.sizes()}")

    def init_palette(self):
        # Optionally, customize the palette (Fusion, etc.) for a dark mode look
        app_palette = QPalette()
        conf_map = {
            QPalette.ColorRole.Window: self.theme_helper.get_color('color_palette_window'),
            QPalette.ColorRole.WindowText: self.theme_helper.get_color('color_palette_window_text'),
            QPalette.ColorRole.Base: self.theme_helper.get_color('color_palette_base'),  # For background
            # This alternate color is typically used to distinguish different sections or items within a widget,
            # particularly useful in views or lists where rows or items might benefit from alternating background colors
            # to improve readability and visual appeal.
            QPalette.ColorRole.AlternateBase: self.theme_helper.get_color('color_palette_alternate_base'),
            QPalette.ColorRole.ToolTipBase: self.theme_helper.get_color('color_palette_tooltip_base'),
            QPalette.ColorRole.ToolTipText: self.theme_helper.get_color('color_palette_tooltip_text'),
            QPalette.ColorRole.Text: self.theme_helper.get_color('color_palette_text'),
            QPalette.ColorRole.Button: self.theme_helper.get_color('color_palette_button'),
            QPalette.ColorRole.ButtonText: self.theme_helper.get_color('color_palette_button_text'),
            # The top and left sides (simulating light falling from the top/left)
            QPalette.ColorRole.Light: self.theme_helper.get_color('color_palette_light'),
            # The bottom and right sides (simulating shadow on the bottom/right)
            QPalette.ColorRole.Dark: self.theme_helper.get_color('color_palette_dark'),
            # For frames with a width greater than 1, to fill the middle part of the frame border
            QPalette.ColorRole.Mid: self.theme_helper.get_color('color_palette_mid'),
            # Located between the fully illuminated areas QPalette.Light and the middle tone areas QPalette.Mid
            QPalette.ColorRole.Midlight: self.theme_helper.get_color('color_palette_mid_light'),
            QPalette.ColorRole.Shadow: self.theme_helper.get_color('color_palette_shadow'),
            # Stand out against other text for emphasis and is typically used against darker backgrounds
            QPalette.ColorRole.BrightText: self.theme_helper.get_color('color_palette_bright_text'),
            QPalette.ColorRole.Link: self.theme_helper.get_color('color_palette_link'),  # For hyperlinks
            QPalette.ColorRole.LinkVisited: self.theme_helper.get_color('color_palette_link_visited'),  # For hyperlinks
            # This role defines the color used to indicate selected items or current focus in widgets
            QPalette.ColorRole.Highlight: self.theme_helper.get_color('color_palette_highlight'),
            # This role defines the color of the text that is used within selected items or items that have the focus
            QPalette.ColorRole.HighlightedText: self.theme_helper.get_color('color_palette_highlighted_text'),
            # For input field placeholder
            QPalette.ColorRole.PlaceholderText: self.theme_helper.get_color('color_palette_placeholder_text'),
            QPalette.ColorRole.Accent: self.theme_helper.get_color('color_palette_accent'),
            # QPalette.ColorRole.NoRole
            # QPalette.ColorRole.NColorRoles
        }

        # Apply color if set
        for role, color in conf_map.items():
            if color is not None:  # Check None as a color int value could be a zero
                app_palette.setColor(role, color)

        QGuiApplication.setPalette(app_palette)

    def splitter_moved_handler(self, width):
        if self.debug:
            self.logger.debug(f"Splitter moved: {width}")
        # Set splitter position equal to the width of the first widget
        self.settings.ui_splitter_pos = width

    def set_app_title(self, sub_title: str = None):
        max_sub_length = 256
        # Format sub-title
        sub_title_f = (sub_title[:max_sub_length - 3] + "..."
                       if sub_title and len(sub_title) > max_sub_length else sub_title)
        app_title = self.lexemes.get('app_title')
        # Title with a sub_title if exists
        if sub_title_f and len(sub_title_f) > 0:
            title = self.lexemes.get('app_title_with_sub', app_title=app_title, sub_title=sub_title_f)
        else:
            # App title
            title = app_title
        # Set up main window title
        self.setWindowTitle(title)

    def get_editor_container(self) -> QWidget:
        if hasattr(self, 'editor_container') and isinstance(self.editor_container, QWidget):
            return self.editor_container

        self.editor_container = QWidget(self)

        return self.editor_container

    def get_tree_container(self) -> Union[QWidget, None]:
        if hasattr(self, 'tree_container') and isinstance(self.tree_container, QWidget):
            return self.tree_container

        if self.logging:
            self.logger.warning('Trying to access tree container widget that was not created')

        return None

    def create_navigation_panel(self) -> QWidget:
        """
        Main navigation tree.
        """

        self.file_model = FileSystemModel()
        self.file_model.setRootPath(QDir.currentPath())  # Or it can be just a '.'
        """
        Also: QDir.AllEntries, QDir.Filter.NoDotAndDotDot
        """
        self.file_model.setFilter(QDir.Filter.NoDot | QDir.Filter.Dirs | QDir.Filter.Files)
        """
        Show only these files in the list (implemented via proxy sort model)
        filters = self.supported_file_types
        self.file_model.setNameFilters(filters)
        """
        # Do not show greyed filter results
        self.file_model.setNameFilterDisables(False)

        # Either QTreeView(self) or QListView(self) are working fine
        self.tree_view = QListView(self)
        # Apply font from the main window to the widget
        self.tree_view.setFont(self.font())
        """
        Use adjust_tree_current_root_index() to set up root index via proxy model instead of:
        self.tree_view.setModel(self.file_model)
        self.tree_view.setRootIndex(self.file_model.index(QDir.currentPath()))

        Other QTreeView methods that can be helpful here:
        self.tree_view.setColumnWidth(0, self.weight_to_px_uno)
        self.tree_view.setHeaderHidden(True)
        """

        """
        Choose NoSelection to prevent item being selected upon mouse right-click.
        The selection will appear later within self.set_current_path()

        More info about the enum: https://doc.qt.io/qt-6/qabstractitemview.html#SelectionMode-enum
        """
        self.tree_view.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

        self.tree_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(
            lambda pos: self.show_tree_context_menu(self.tree_view, pos)
        )

        # Connect the clicked event to handle file selection
        self.tree_view.clicked.connect(self.action_nav_select_file)

        self.tree_filter = QLineEdit(self, textChanged=self.on_tree_filter_text_changed)
        # Apply font from the main window to the widget
        self.tree_filter.setFont(self.font())
        self.tree_filter.setReadOnly(False)
        self.tree_filter.setMaxLength(256)
        self.tree_filter.setMinimumWidth(self.weight_to_px_uno)
        self.tree_filter.setAccessibleDescription(self.lexemes.get('tree_filter_accessible_desc'))

        self.tree_proxy_model = SortFilterProxyModel(
            extensions=self.supported_file_extensions,
            sourceModel=self.file_model,  # Or tree_proxy_model.setSourceModel(self.file_model)
            recursiveFilteringEnabled=True,
            # More info about the enum https://doc.qt.io/qt-6/qfilesystemmodel.html#Roles-enum
            filterRole=QFileSystemModel.Roles.FileNameRole | QFileSystemModel.Roles.FilePathRole,
            # To filter file names without case sensitivity
            # More info about the property https://doc.qt.io/qt-6/qsortfilterproxymodel.html#filterCaseSensitivity-prop
            filterCaseSensitivity=Qt.CaseSensitivity.CaseInsensitive)
        self.tree_proxy_model.sort(0, order=Qt.SortOrder.AscendingOrder)
        self.tree_view.setModel(self.tree_proxy_model)
        self.adjust_tree_current_root_index()

        self.file_watcher = QFileSystemWatcher()
        self.file_watcher.addPath(QDir.currentPath())  # Watch for changes in the current directory

        self.file_watcher.directoryChanged.connect(self.on_dir_changed)

        """
        More info about the QVBoxLayout: https://doc.qt.io/qt-6/qvboxlayout.html
        Inherits methods from QBoxLayout: https://doc.qt.io/qt-6/qboxlayout.html
        """
        tree_layout = QVBoxLayout()
        tree_layout.setContentsMargins(0, 0, 0, 0)
        tree_layout.addWidget(self.tree_filter)
        tree_layout.addWidget(self.tree_view)

        tree_container = QWidget(self)
        tree_container.setLayout(tree_layout)
        """
        More info about stylesheets: https://doc.qt.io/qt-6/stylesheet-reference.html
        """
        tree_container.setStyleSheet(self.theme_helper.get_css('tree_view'))

        # Save created object to the internal variable
        self.tree_container = tree_container

        return self.tree_container

    def on_dir_changed(self, path) -> None:
        """
        Method reserved for future use.
        @param path: QString path from the signal, more info https://doc.qt.io/qt-6/qfilesystemwatcher.html#signals
        @return: None
        """
        if self.debug:
            self.logger.debug('Dir changed "%s"' % path)

    def on_tree_filter_text_changed(self, text: str) -> None:
        """
        Actions to apply when tree filter has changed value.
        @param text: string, can be empty, for example when deleting a text
        @return: None
        """
        if text:
            self.tree_proxy_model.setFilterRegularExpression(r'.*?{}'.format(text))
            """
            Previous approach was:
            self.tree_proxy_model.setFilterWildcard("*{}*".format(text))
            """
        else:
            self.tree_proxy_model.setFilterRegularExpression(r'')

        self.adjust_tree_current_root_index()  # To re-set an actual file path and current dir for the tree.

    def adjust_tree_current_root_index(self) -> None:
        # dir_path = QDir.homePath()
        # dir_path = QDir.currentPath()
        dir_path = os.path.dirname(str(self.get_current_path()))
        root_index = self.file_model.index(dir_path)
        """
        More info about this mapping https://doc.qt.io/qt-6/qsortfilterproxymodel.html#mapFromSource
        """
        proxy_index = self.tree_proxy_model.mapFromSource(root_index)
        self.tree_view.setRootIndex(proxy_index)

    def get_current_path(self, is_base: bool = False) -> str:
        """
        Get current file path.
        """
        return os.path.dirname(self.file_path) if is_base else self.file_path

    def set_current_path(self, tree_path: str) -> None:
        """
        Set current file path and tree index.
        """
        # Path's index
        index = self.file_model.index(tree_path)
        if os.path.isfile(tree_path):
            # Set current file
            self.file_path = tree_path
            # Update current file index
            proxy_index = self.tree_proxy_model.mapFromSource(index)
            self.tree_view.scrollTo(proxy_index)
            self.tree_view.setCurrentIndex(proxy_index)

            selection_model = self.tree_view.selectionModel()
            # Reset selection as it persists if not
            selection_model.clearSelection()
            # Select actual tree item
            selection_model.setCurrentIndex(proxy_index, QItemSelectionModel.SelectionFlag.Select)

            # Adjust tree proxy model with file's dir
            self.adjust_tree_current_root_index()

            if self.file_watcher:
                self.file_watcher.addPath(self.file_path)
        else:
            # Dir
            proxy_dir_index = self.tree_proxy_model.mapFromSource(index)
            # Just remove proxy index if there is no proxy model and use index
            self.tree_view.setRootIndex(proxy_dir_index)

    def confirm_current_path(self) -> None:
        """
        Confirm current file params.
        It may be necessary to set params after encrypted file opened or so.
        """
        current_file_path = self.get_current_path()
        self.settings.file_path = current_file_path
        self.set_encryption(Encryption.ENCRYPTED if self.is_file_encrypted(current_file_path) else Encryption.PLAIN)

    def show_tree_context_menu(self, tree_view: QListView, pos: QPoint) -> None:
        """
        Context menu at file tree view.
        """

        if self.debug:
            self.logger.debug('Context menu for %s' % tree_view)

        # Save any unsaved changes
        self.save_active_file(clear_after=False)

        global_pos = tree_view.mapToGlobal(pos)
        tree_index = tree_view.indexAt(pos)
        tree_index_row = tree_view.indexAt(pos).row()
        # self.tree_view.currentIndex()

        # QSortFilterProxyModel self.tree_proxy_model | tree_view.model()
        file_index = self.tree_proxy_model.mapToSource(tree_index)
        file_path = self.file_model.filePath(file_index)

        if not os.path.isfile(file_path):
            self.logger.warning('Trying to create context menu on a file that does not exist "%s"' % file_path)
            return

        menu = QMenu(self)
        menu.setFont(self.font())
        rename_icon = self.theme_helper.get_icon(theme_icon='cursor-text.svg', system_icon='document-properties',
            color=QColor(self.theme_helper.get_color('main_tree_context_menu_rename')))
        menu.addAction(rename_icon, self.lexemes.get('menu_action_rename'),
                       lambda: self.rename_file_dialog(file_path))
        if self.is_file_safely_deleted(file_path):
            # Restore deleted file context action
            restore_icon = self.theme_helper.get_icon(theme_icon='box-arrow-up.svg', system_icon='edit-undo',
                color=QColor(self.theme_helper.get_color('main_tree_context_menu_restore')))
            menu.addAction(restore_icon, self.lexemes.get('menu_action_restore'),
                           lambda: self.restore_file_dialog(file_path))
            # Delete completely file context action
            delete_icon = self.theme_helper.get_icon(theme_icon='x-square-fill.svg', system_icon='edit-delete',
                color=QColor(self.theme_helper.get_color('main_tree_context_menu_delete_completely')))
            menu.addAction(delete_icon, self.lexemes.get('menu_action_delete_completely'),
                           lambda: self.delete_completely_file_dialog(file_path))
        else:
            # Delete file context action
            delete_icon = self.theme_helper.get_icon(theme_icon='x-square.svg', system_icon='edit-delete',
                color=QColor(self.theme_helper.get_color('main_tree_context_menu_delete')))
            menu.addAction(delete_icon, self.lexemes.get('menu_action_delete'),
                           lambda: self.delete_file_dialog(file_path))

        menu.exec(global_pos)

    def rename_file_dialog(self, file_path: str) -> None:
        """
        Rename file dialog.
        """
        file_path = os.path.abspath(str(file_path))
        file_name = os.path.basename(file_path)
        # QDir.currentPath()
        dir_name = os.path.dirname(file_path)

        dialog = RenameFileDialog(file_name=file_name, parent=self)

        """
        More info about the enum: https://doc.qt.io/qt-6/qdialog.html#DialogCode-enum
        Variants:
        * QDialog.DialogCode.Accepted
        * QDialog.DialogCode.Rejected
        """
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Save active file as UI may switch context after the action
            self.save_active_file(clear_after=True)
            # Get new name
            new_file_name = dialog.textValue()
            new_file_path = os.path.join(dir_name, new_file_name)
            self.rename_file_dialog_callback(from_file_path=file_path, to_file_path=new_file_path)
        else:
            if self.debug:
                self.logger.debug('Rename file cancellation')

        dialog.deleteLater()

    def rename_file_dialog_callback(self, callback: Optional[Callable[..., Any]] = None,
                                    from_file_path: str = None, to_file_path: str = None):
        """
        Actions to perform after file rename dialogue.
        """

        if self.debug:
            self.logger.debug('Rename file dialog callback with sub-callback %s' % callback)

        from_file_path = os.path.abspath(str(from_file_path))
        to_file_path = os.path.abspath(str(to_file_path))

        if self.debug:
            self.logger.debug('Rename file "%s" to "%s"' % (from_file_path, to_file_path))

        if not os.path.isfile(to_file_path):
            os.rename(from_file_path, to_file_path)
            self.load_file(to_file_path)
        else:
            if self.debug:
                self.logger.debug('File with the same name is already exists "%s"' % to_file_path)
            self.message_box(self.lexemes.get('dialog_file_rename_warning_exists'), icon_type=2)

        if callable(callback):
            callback()

    def delete_file_dialog(self, file_path: str) -> None:
        """
        Delete file dialog.
        """

        if self.debug:
            self.logger.debug('Delete file "%s" dialog' % file_path)

        file_path = os.path.abspath(str(file_path))
        file_name = os.path.basename(file_path)

        self.common_dialog(
            self.lexemes.get('dialog_file_delete_title'),
            self.lexemes.get(name='dialog_file_delete_text', file_name=file_name),
            callback=lambda dialog_callback: self.delete_file_dialog_callback(dialog_callback, file_path))

    def delete_file_dialog_callback(self, callback: Callable[..., Any], file_path: str) -> None:
        """
        Actions to perform after file delete dialogue.
        """

        if self.debug:
            self.logger.debug('Delete file "%s" dialog callback with sub-callback %s' % (file_path, callback))

        if os.path.isfile(file_path):
            del_filename_tpl = '%s.del%s'
            i = 0
            while ((del_file_path := res_path(del_filename_tpl % (file_path, i if i > 0 else '')))
                   and os.path.isfile(del_file_path)):
                i += 1
            if not os.path.isfile(del_file_path):
                os.rename(file_path, del_file_path)
                if self.debug:
                    self.logger.debug('File (reversibly) deleted to "%s"', del_file_path)
            else:
                if self.debug:
                    self.logger.debug('Cannot delete file, error occurred "%s"' % del_file_path)
                self.message_box(self.lexemes.get('dialog_file_delete_error'), icon_type=2)
            # Check deleted file was actually shown
            if self.get_current_path() == file_path:
                any_file_path = self.get_any_file()
                if any_file_path is not None:
                    self.load_file(any_file_path)
        else:
            if self.debug:
                self.logger.debug('File not found "%s"' % file_path)
            self.message_box(self.lexemes.get('dialog_file_delete_error_not_found'), 2)
        if callable(callback):
            callback()

    def delete_completely_file_dialog(self, file_path: str) -> None:
        """
        Delete file dialog.
        """

        if self.debug:
            self.logger.debug('Delete file completely "%s" dialog' % file_path)

        file_path = os.path.abspath(str(file_path))
        file_name = os.path.basename(file_path)

        self.common_dialog(
            self.lexemes.get('dialog_file_delete_completely_title'),
            self.lexemes.get(name='dialog_file_delete_completely_text', file_name=file_name),
            callback=lambda dialog_callback: self.delete_completely_file_dialog_callback(dialog_callback, file_path))

    def delete_completely_file_dialog_callback(self, callback: Callable[..., Any], file_path: str) -> None:
        """
        Actions to perform after file completely delete dialogue.
        """

        if self.debug:
            self.logger.debug('Delete file completely "%s" dialog callback with sub-callback %s' % (file_path, callback))

        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
                print(f"File {file_path} has been completely deleted.")
            except OSError as e:
                if self.logging:
                    self.logger.warning(f"Error: {e.strerror}. Could not delete {file_path}.")
                self.message_box(self.lexemes.get('dialog_file_delete_error'), icon_type=2)

            # Check deleted file was actually shown
            if self.get_current_path() == file_path:
                any_file_path = self.get_any_file()
                if any_file_path is not None:
                    self.load_file(any_file_path)
        else:
            if self.debug:
                self.logger.debug('File not found "%s"' % file_path)
            self.message_box(self.lexemes.get('dialog_file_delete_error_not_found'), 2)
        if callable(callback):
            callback()

    def is_file_safely_deleted(self, file_path: str) -> Union[str, None]:
        """
        Checks either the file is safely deleted or not.
        Mostly rely on extension, refactor it to use header.
        @param file_path: string file path
        @return: Union[str, None], either file extension if it was safely deleted or None
        """
        # As deleted file can have an extension differ from '.del', say with increment addon, like, '.del1',
        # hence try to find it with this regex pattern.
        re = QRegularExpression(r'^.*?(\.del[\d]*?)$')
        match = re.match(file_path)
        if match.capturedTexts() and match.captured(1):
            return match.captured(1)
        return None

    def restore_file_dialog(self, file_path: str) -> None:
        """
        Restore deleted file dialog.
        As the deletion means an additional extension of '.del' applied to file, hence it can be reverted back.
        """
        if self.debug:
            self.logger.debug('Restore file "%s" dialog' % file_path)

        file_path = os.path.abspath(str(file_path))
        file_name = os.path.basename(file_path)

        # Or: extension = file_path.split(".")[-1]
        file_extension = self.is_file_safely_deleted(file_path)
        if file_extension:
            new_file_path = file_path[:-len(file_extension)]
        else:
            if self.logging:
                self.logger.warning(f'Trying to restore file that has no proper extension set {file_path}')
            return

        self.common_dialog(
            self.lexemes.get('dialog_file_restore_title'),
            self.lexemes.get(name='dialog_file_restore_text', file_name=file_name),
            callback=lambda dialog_callback:
                self.restore_file_dialog_callback(dialog_callback,
                                                  from_file_path=file_path, to_file_path=new_file_path))

    def restore_file_dialog_callback(self, callback: Callable[..., Any],
                                     from_file_path: str = None, to_file_path: str = None) -> None:
        """
        Actions to perform after file restore dialogue.
        """
        if self.debug:
            self.logger.debug('Restore file dialog callback with sub-callback %s' % callback)

        from_file_path = os.path.abspath(str(from_file_path))
        to_file_path = os.path.abspath(str(to_file_path))

        if self.debug:
            self.logger.debug('Restore file "%s" to "%s"' % (from_file_path, to_file_path))

        if not os.path.isfile(to_file_path):
            os.rename(from_file_path, to_file_path)
            self.load_file(to_file_path)
        else:
            if self.debug:
                self.logger.debug(f'File with the name "{to_file_path}" is already exists')
            self.message_box(self.lexemes.get('dialog_file_restore_warning_exists', file_name=to_file_path), icon_type=2)

        if callable(callback):
            callback()

    def get_any_file(self) -> Union[str, None]:
        """
        Open any file from the tree.

        TODO: check the file is not the one to escape
        """

        # Get any file from root dir to show instead
        root_index = self.tree_view.rootIndex()
        if self.debug:
            self.logger.debug('Root files index "%s"', self.tree_proxy_model.data(root_index))
        # Search any file in dir
        entries_cnt = self.tree_proxy_model.rowCount(root_index)
        # QListView file/dir position 0...entries_cnt
        for file_pos in range(entries_cnt):
            tree_index = self.tree_proxy_model.index(file_pos, 0, root_index)
            any_file_index = self.tree_proxy_model.mapToSource(tree_index)
            any_file_path = self.file_model.filePath(any_file_index)
            if os.path.isfile(any_file_path):
                return any_file_path
        return None

    def message_box(self, text: str, icon_type: int = 0, frameless: bool = False, timer_sec: int = None) -> None:
        """
        Show popup message box

        Icon type enum:
        NoIcon(0) | Information(1) | Warning(2) | Critical(3) | Question(4)
        """

        box = QMessageBox(self)
        box.setFont(self.font())

        button_ok = None

        if frameless:
            # Frameless
            box.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
            # Remove all buttons
            box.setStandardButtons(QMessageBox.StandardButton.NoButton)
            box.setModal(False)
            box.setContentsMargins(0, 10, 20, 0)
        else:
            """
            More info about the enum: https://doc.qt.io/qt-6/qmessagebox.html#StandardButton-enum
            Variants:
            * QMessageBox.StandardButton.Yes
            * QMessageBox.StandardButton.No
            """
            box.setStandardButtons(QMessageBox.StandardButton.Ok)
            button_ok = box.button(QMessageBox.StandardButton.Ok)
            button_ok.setText(self.lexemes.get('dialog_message_box_button_ok'))
            # Set default button
            box.setDefaultButton(QMessageBox.StandardButton.Ok)

        """
        More info about the enum: https://doc.qt.io/qt-6/qmessagebox.html#Icon-enum
        Variants:
        * NoIcon(0)
        * Information(1)
        * Warning(2)
        * Critical(3)
        * Question(4)
        """
        box.setIcon(QMessageBox.Icon(icon_type))
        box.setWindowTitle(self.lexemes.get('dialog_message_box_title'))
        box.setText(text)

        box.setGeometry(QStyle.alignedRect(
                        Qt.LayoutDirection.LeftToRight,
                        Qt.AlignmentFlag.AlignCenter,
                        box.size(),
                        self.geometry()))

        # Engage timer before show the dialog
        if timer_sec is not None:
            QTimer.singleShot(timer_sec * 1000, lambda: box.accept())

        if frameless:
            # Use open() to show non-blocking message box
            box.open()
            return

        # Show dialog
        box.exec()

        if box.clickedButton() == button_ok:
            if self.debug:
                self.logger.debug('Message box button clicked')

    def enc_new_password_dialog(self) -> Union[EncPassword, None]:
        """
        Enter new password along with the other params (if required) dialog when creating new encrypted file.
        @return: Union[EncPassword, None]
        """

        dialog = EncNewPasswordDialog(self)

        """
        More info about the enum: https://doc.qt.io/qt-6/qdialog.html#DialogCode-enum
        Variants:
        * QDialog.DialogCode.Accepted
        * QDialog.DialogCode.Rejected
        """
        if dialog.exec() == QDialog.DialogCode.Accepted:
            if self.debug:
                self.logger.debug('Entering new password completed')
            password = dialog.password_edit.text()
            hint = dialog.hint_edit.text()
            # Create password object
            password_obj = EncPassword()
            password_obj.password = password
            password_obj.hint = hint
            return password_obj
        else:
            if self.debug:
                self.logger.debug('Entering password cancellation')
            return None

    def enc_password_dialog(self, hint: str = None) -> Union[EncPassword, None]:
        """
        Enter password dialog when trying to open an encrypted file.
        """

        if self.get_enc_password_dialog_cnt() is None:
            self.enc_password_dialog_cnt = 0

        self.enc_password_dialog_cnt += 1

        dialog = EncPasswordDialog(hint=hint, parent=self)  # or just `QInputDialog(self)`

        """
        More info about the enum: https://doc.qt.io/qt-6/qdialog.html#DialogCode-enum
        Variants:
        * QDialog.DialogCode.Accepted
        * QDialog.DialogCode.Rejected
        """
        if dialog.exec() == QDialog.DialogCode.Accepted:
            if self.debug:
                self.logger.debug('Entering password completed')
            password = dialog.password_edit.text()
            # Create password object
            password_obj = EncPassword()
            password_obj.password = password
            # Store hint to pass it to the next header
            password_obj.hint = hint
            return password_obj
        else:
            if self.debug:
                self.logger.debug('Entering password cancellation')
            return None

    def get_enc_password_dialog_cnt(self) -> Union[int, None]:
        return self.enc_password_dialog_cnt if hasattr(self, 'enc_password_dialog_cnt') else None

    def enc_password_reset_dialog(self) -> None:
        """
        Confirmation dialog when trying to open a file encrypted with different password/key.
        """

        if self.logging:
            self.logger.info('Reset encryption password dialog')

        dialog = EncPasswordResetDialog(callback=self.reset_encrypt_helper, parent=self)
        dialog.exec()

        """
        More info about: https://doc.qt.io/qt-6/qobject.html#deleteLater
        """
        dialog.deleteLater()

    def common_dialog(self, title: str, text: str, callback: Callable[..., Any]) -> None:
        """
        Generic dialog with settable texts and callback.
        """

        if self.debug:
            self.logger.debug('Common dialog "%s": "%s"' % (title, text))

        dialog = CommonDialog(title, text, callback, self)
        dialog.exec()

        """
        More info about: https://doc.qt.io/qt-6/qobject.html#deleteLater
        """
        dialog.deleteLater()

    def get_edit_widget(self) -> Union[EditWidget, None]:
        if hasattr(self, 'text_edit') and isinstance(self.text_edit, EditWidget):
            return self.text_edit

        if self.logging:
            self.logger.warning('Trying to access edit widget that was not created')

        return None

    def create_editor_panel(self) -> EditWidget:
        """
        File content edit mode area.
        """

        """
        More info about: https://doc.qt.io/qt-6/qplaintextedit.html#introduction-and-concepts
        """
        edit_widget = EditWidget()
        # Block widget's signals
        was_blocked = edit_widget.blockSignals(True)
        if self.debug:
            self.logger.debug(f'Creating view widget, signals was blocked "{was_blocked}"')
        # Apply font from the main window to the widget
        edit_widget.document().setDefaultFont(self.font())
        edit_widget.setContentsMargins(0, 0, 0, 0)

        """
        More info about the enum: https://doc.qt.io/qt-6/qsizepolicy.html#Policy-enum
        """
        edit_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        edit_widget.zoomIn(0)
        edit_widget.zoomOut(0)

        # Attach style to the QTextEdit
        edit_widget.setStyleSheet(self.theme_helper.get_css('editor'))

        edit_widget.textChanged.connect(self.on_text_changed)
        edit_widget.modificationChanged.connect(self.on_modification_changed)
        edit_widget.blockCountChanged.connect(self.on_block_count_changed)
        edit_widget.selectionChanged.connect(self.on_selection_changed)
        edit_widget.cursorPositionChanged.connect(self.on_cursor_position_changed)

        # This event is emitted when edit widget document has been set
        edit_widget.content_set.connect(lambda:
                                        # Restore cursor and asure text widget has a focus
                                        (self.restore_doc_cursor_pos(self.get_mode(), edit_widget),
                                         edit_widget.setFocus()))
        if self.debug:
            self.logger.debug('Edit widget geometry %d x %d' %
                              (edit_widget.frameGeometry().width(), edit_widget.frameGeometry().height()))

        # Could be synced with self.debug constant
        self.md_highlighter = MdHighlighter(document=edit_widget.document())

        # Restore widget's signals
        edit_widget.blockSignals(was_blocked)
        if self.debug:
            self.logger.debug(f'View widget created, signals was un-blocked "{was_blocked}"')

        # Save created object to the internal variable
        self.text_edit = edit_widget

        return self.text_edit

    def create_line_numbers(self, widget: Union[EditWidget, QPlainTextEdit]) -> None:
        """
        Init with a text edit.
        """
        self.line_numbers = LineNumbers(editor=widget)

    def open_link_dialog_proxy(self):
        if self.settings.viewer_open_link_confirmation:
            # Open a link after confirmation dialog only
            return lambda url: (
                # Check if the clicked anchor is an internal doc link starts with '#'
                self.get_view_widget().setSource(url) if url.toString().startswith('#') else self.common_dialog(
                    self.lexemes.get('dialog_open_link_title'),
                    self.lexemes.get(name='dialog_open_link_text',
                                     url=url.toString()),
                    # Open url with system browser
                    callback=lambda dialog_callback:
                    # Open link in a system browser and run dialog's callback
                    (QDesktopServices.openUrl(url), dialog_callback())))
        # Just open a link without a confirmation dialog
        return lambda url:(
            # Check if the clicked anchor is an internal doc link starts with '#'
            self.get_view_widget().setSource(url) if url.toString().startswith('#') else QDesktopServices.openUrl(url))

    def get_view_doc(self) -> QTextDocument:
        if not hasattr(self, 'view_doc') or not self.view_doc:
            self.view_doc = QTextDocument(self)
            # Apply font from the main window to the widget
            self.view_doc.setDefaultFont(self.font())
            # Set default styles
            self.view_doc.setDefaultStyleSheet(self.theme_helper.get_css('styles'))
        return self.view_doc

    def get_view_widget(self) -> Union[ViewWidget, QTextBrowser, None]:
        if hasattr(self, 'text_view') and isinstance(self.text_view, ViewWidget):
            return self.text_view

        if self.logging:
            self.logger.warning('Trying to access view widget that was not created')

        return None

    def create_view_panel(self) -> QTextBrowser:
        """
        File content view mode area.
        """

        # View document
        view_doc = self.get_view_doc()  # type: QTextDocument
        # View document highlighter
        self.view_highlighter = ViewHighlighter(document=view_doc)

        # Create main view widget to show Mode.VIEW content
        view_widget = ViewWidget(self)
        # Block widget's signals
        was_blocked = view_widget.blockSignals(True)
        if self.debug:
            self.logger.debug(f'Creating view widget, signals was blocked "{was_blocked}"')
        # Adjust font to match the size of the default or changed one
        view_widget.document().setDefaultFont(self.font())
        view_widget.setReadOnly(True)
        if isinstance(view_widget, QTextBrowser):
            # Process anchor click separately
            view_widget.setOpenLinks(False)
            view_widget.anchorClicked.connect(self.open_link_dialog_proxy())
        view_widget.setContentsMargins(0, 0, 0, 0)
        """
        More info about the enum: https://doc.qt.io/qt-6/qsizepolicy.html#Policy-enum
        """
        view_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        """
        For QTextEdit set the point size of the font:
        view_widget.setFontPointSize(self.font_size)
        """

        # Attach style to the QTextEdit
        view_widget.setStyleSheet(self.theme_helper.get_css('viewer'))

        # The same handler as for edit field as status bar shared
        view_widget.selectionChanged.connect(self.on_selection_changed)
        view_widget.cursorPositionChanged.connect(self.on_cursor_position_changed)

        # This event is emitted when edit widget document has been set
        view_widget.content_set.connect(lambda:
                                        # Restore cursor and asure text widget has a focus
                                        (self.restore_doc_cursor_pos(self.get_mode(), view_widget),
                                         view_widget.setFocus()))
        if self.debug:
            self.logger.debug('Web view geometry %d x %d' %
                              (view_widget.frameGeometry().width(), view_widget.frameGeometry().height()))

        # Set view document to the view widget
        view_widget.setDocument(view_doc)

        # Restore widget's signals
        view_widget.blockSignals(was_blocked)
        if self.debug:
            self.logger.debug(f'View widget created, signals was un-blocked "{was_blocked}"')

        # Save created object to the internal variable
        self.text_view = view_widget

        return self.text_view

    @asyncClose
    async def closeEvent(self, event):
        if self.logging:
            self.logger.info('Stopping events loop, closing the app... Sayonara!')

        # Cancel all pending tasks if exist
        if hasattr(self, 're_tasks'):
            tasks_total = len(self.re_tasks)
            for i, task in enumerate(self.re_tasks):
                if not task.done():
                    task_res = task.cancel()
                    if self.logging:
                        self.logger.info(f'[{i+1}/{tasks_total}] Pending task "{task.get_name()}" canceled with result "{task_res}"')

        if self.get_mode() == Mode.EDIT:
            # Save any unsaved changes
            self.save_active_file(clear_after=False)
        else:
            # Save cursor position (block start)
            self.store_doc_cursor_pos(self.get_mode())

        self.settings.mode = self.get_mode().value
        self.settings.source = self.get_source().value

        event.accept()

    @asyncSlot()
    async def rehighlight_in_queue(self, full_rehighlight: bool = False) -> None:
        """
        More info about asyncio tasks: https://docs.python.org/3/library/asyncio-task.html
        """

        # Create initial array if not exists
        if not hasattr(self, 're_tasks'):
            self.re_tasks = []

        if self.debug:
            self.logger.debug('Re-highlight %d tasks in queue' % len(self.re_tasks))

        postpone = False if len(self.re_tasks) == 0 else True
        if self.debug:
            self.logger.debug('Re-highlight is to postpone "%r"' % postpone)

        # To keep only a few tasks in queue
        if len(self.re_tasks) < 3:
            task = asyncio.ensure_future(self.rehighlight_async(full_rehighlight, postpone))
            # task = asyncio.create_task(self.rehighlight_async(full_rehighlight, postpone))
            task.add_done_callback(
                lambda _task:
                    (self.logger.info('%s from total %d completed with callback'
                                      % (_task.get_name(), len(self.re_tasks))) if self.debug else None,
                        self.re_tasks.remove(_task),
                        QTimer.singleShot(750,
                                          lambda: self.rehighlight_editor(True)) if len(self.re_tasks) == 0 else None)
            )
            self.re_tasks.append(task)

        done, pending = await asyncio.wait(
            self.re_tasks,
            return_when=asyncio.ALL_COMPLETED,
        )

        # Actually, there is only one task in queue
        for _task in self.re_tasks:
            if _task in pending:
                if self.debug:
                    self.logger.debug('Re-highlight task "%s" is pending' % _task.get_name())
            if _task in done:
                if self.debug:
                    self.logger.debug('Re-highlight task "%s" is done, from [%d]'
                                      % (_task.get_name(), len(self.re_tasks)))

    async def rehighlight_async(self, full_rehighlight: bool = False, postpone: bool = False) -> None:
        """
        Run this method not too often to avoid overwhelming the system.
        """
        # First of all check it's necessary
        if self.get_mode() == Mode.EDIT and self.get_source() == Source.MARKDOWN:
            # Postpone before re-highlighting if a few tasks
            if postpone:
                if self.debug:
                    self.logger.debug('Re-highlighting the text > postpone')
                # Keep this method particular amount of time to avoid overwhelming
                await asyncio.sleep(0.25, self.loop)
            # Re-highlight
            self.rehighlight_editor(full_rehighlight)
            if self.debug:
                self.logger.debug('Async re-highlighting queue task processed')
            # Postpone after re-highlighting to keep the queue busy
            if self.debug:
                self.logger.debug('Re-highlighting the text > wait to return')
            # Keep this method particular amount of time to avoid overwhelming
            await asyncio.sleep(0.5, self.loop)

    def rehighlight_editor(self, full_rehighlight: bool = False) -> None:
        # Edit widget
        edit_widget = self.get_edit_widget()  # type: Union[EditWidget, QPlainTextEdit]

        # Prevent QTextEdit's on_text_changed() method invocation by blocking signals
        was_blocked = edit_widget.blockSignals(True)
        if self.debug:
            self.logger.debug(f'Re-highlighting the text > signals was blocked "{was_blocked}"')
        # Re-highlight the whole document or a particular block
        if full_rehighlight:
            self.md_highlighter.rehighlight()
        else:
            block = edit_widget.get_current_block()
            self.md_highlighter.rehighlightBlock(block)
        # Restore QTextEdit's signals
        edit_widget.blockSignals(was_blocked)
        if self.debug:
            self.logger.debug('Re-highlighting the text > signals unblocked')

    def get_block_data_param(self, tag: str, param: Any) -> Any:
        # Edit widget
        edit_widget = self.get_edit_widget()  # type: Union[EditWidget, QPlainTextEdit]

        """
        Returns the data param stored within the block's QTextBlockUserData
        More info about:
        * https://doc.qt.io/qt-6/qtextblock.html#userData
        * https://doc.qt.io/qt-6/qtextblockuserdata.html
        """
        block = edit_widget.get_current_block()
        data_storage = block.userData()
        if data_storage is not None and hasattr(data_storage, 'block_number'):
            block_data = data_storage.get_one(tag)
            if block_data:
                if self.debug:
                    self.logger.debug('Current code block data [%d]~[%d] "%s", in:%r, o:%r, c:%r'
                                      % (block.blockNumber(), data_storage.block_number, tag, block_data['within'],
                                         block_data['opened'], block_data['closed']))
                return getattr(block_data, param) if hasattr(block_data, param) else None
        return None

    def on_text_changed(self) -> None:
        """
        When text is changed, or when formatting is applied.
        More info about the signal: https://doc.qt.io/qt-6/qplaintextedit.html#textChanged
        """

        if self.debug:
            self.logger.debug('Text changed signal from %s' % (self.sender()))

        # Make save button active at the toolbar, even if no changes to save resources with no check
        if hasattr(self, 'toolbar_save_button'):
            self.toolbar_save_button.setDisabled(False)

        full_rehighlight = (self.get_block_data_param('code', 'opened')
                            or self.get_block_data_param('code', 'closed'))

        # Schedule async whole doc re-highlighting task in queue
        self.rehighlight_in_queue(full_rehighlight)
        """
        Opposed way, synchronous highlighting direct call:
        self.rehighlight_editor(full_rehighlight)
        """

    def on_modification_changed(self, changed) -> None:
        """
        The content changes in a way that affects the modification state.
        More info about the signal: https://doc.qt.io/qt-6/qplaintextedit.html#modificationChanged
        """
        if self.debug:
            self.logger.debug('Modification changed (%s) signal from %s' % (changed, self.sender()))

        # Synchronous highlighting
        self.rehighlight_editor(True)

    def on_block_count_changed(self, new_block_count: int) -> None:
        """
        Whenever the block count changes, comes with a particular number of blocks.
        More info about the signal: https://doc.qt.io/qt-6/qplaintextedit.html#blockCountChanged
        """
        if self.debug:
            self.logger.debug('Block count (%d) changed signal from %s' % (new_block_count, self.sender()))

        if hasattr(self, 'line_numbers'):
            self.line_numbers.update_numbers()

    # TODO control B-I-U-S buttons
    def on_selection_changed(self) -> None:
        if self.debug:
            self.logger.debug('Text selection changed')

    def on_cursor_position_changed(self) -> None:
        """
        Cursor position changed.
        More info about the signal: https://doc.qt.io/qt-6/qtextedit.html#cursorPositionChanged
        """
        if self.get_mode() == Mode.EDIT:
            # Edit widget
            edit_widget = self.get_edit_widget()  # type: Union[EditWidget, QPlainTextEdit]
            cursor = edit_widget.textCursor()
        else:
            """
            These modes share the same widget (Mode.VIEW | Mode.SOURCE)
            """
            # View widget
            view_widget = self.get_view_widget()  # type: Union[ViewWidget, QTextBrowser]
            cursor = view_widget.textCursor()
        block = cursor.block()
        selected_text = cursor.selection().toPlainText()

        blk_num = block.blockNumber()
        blk_cursor_pos = block.position()
        """
        The firstLineNumber() returns either the first line number of the block or -1 if the block is invalid
        blk_line_num = block.firstLineNumber()
        blk_line_cnt = block.lineCount()
        """

        self.cursor_pos = cursor.position()
        self.col_num = self.cursor_pos - blk_cursor_pos
        self.line_num = blk_num
        self.line_num_hr = blk_num + 1

        if self.debug:
            self.logger.debug('cursor %d x %d' % (self.line_num_hr, self.col_num))

        if hasattr(self, 'statusbar') and hasattr(self.statusbar, 'cursor_label'):
            # Update text at statusbar
            self.statusbar['cursor_label'].setText(self.get_cursor_label_text(selected_text))

    def changeEvent(self, event) -> None:
        """
        Track change event.
        * https://doc.qt.io/qt-6/qwidget.html#changeEvent

        Event types
        * https://doc.qt.io/qt-6/qevent.html#Type-enum
        """
        super(NotologEditor, self).changeEvent(event)

        if self.debug:
            self.logger.debug('Change event %s' % event.type())
        # if event.type() == event.WindowStateChange:
        #    if self.debug:
        #        self.logger.debug('%s > event.WindowStateChange' % self . __class__ . __qualname__)

    def resizeEvent(self, event) -> None:
        """
        Tracking resize event.
        * https://doc.qt.io/qt-6/qwidget.html#resizeEvent
        """
        super(NotologEditor, self).resizeEvent(event)

        # self.frameGeometry() returns width and height with extra padding
        ui_width = self.size().width()
        ui_height = self.size().height()

        # View widget
        view_widget = self.get_view_widget()  # type: Union[ViewWidget, QTextBrowser]

        web_view_width = view_widget.frameGeometry().width()
        web_view_height = view_widget.frameGeometry().height()

        if self.debug:
            self.logger.debug('%s > App window geometry %d x %d'
                              % (self . __class__ . __qualname__, ui_width, ui_height))
            self.logger.debug('%s > Web view geometry  %d x %d'
                              % (self . __class__ . __qualname__, web_view_width, web_view_height))

        self.settings.ui_width = ui_width
        self.settings.ui_height = ui_height

        self.weight_to_px_uno = int(self.frameGeometry().width() / self.AREA_WEIGHT)
        if self.debug:
            self.logger.debug('Weight to px "%s"' % self.weight_to_px_uno)

        # Update line numbers area
        if hasattr(self, 'line_numbers'):
            self.line_numbers.update_numbers()

    def moveEvent(self, event) -> None:
        """
        Track move event
        * https://doc.qt.io/qt-6/qwidget.html#moveEvent

        Calling move() or setGeometry() inside moveEvent() can lead to infinite recursion.
        https://doc.qt.io/qt-6/qwidget.html#pos-prop
        """
        super(NotologEditor, self).moveEvent(event)

        ui_pos_x = self.pos().x()
        ui_pos_y = self.pos().y()

        if self.debug:
            self.logger.debug('%s > App window position %s' % (self . __class__ . __qualname__, self.pos()))

        self.settings.ui_pos_x = ui_pos_x
        self.settings.ui_pos_y = ui_pos_y

    def get_cursor_label_text(self, selected_text: str = None) -> str:
        if selected_text:
            if self.settings.show_global_cursor_position:
                # Show status with selected text length and global cursor position
                return self.lexemes.get('statusbar_cursor_label_selected_with_global',
                                        scope='statusbar', line=self.line_num_hr, column=self.col_num,
                                        position=self.cursor_pos, selected=len(selected_text))
            else:
                # Show status with selected text length
                return self.lexemes.get('statusbar_cursor_label_selected', scope='statusbar',
                                        line=self.line_num_hr, column=self.col_num, selected=len(selected_text))
        else:
            if self.settings.show_global_cursor_position:
                # Show status without selected text length but with global cursor position
                return self.lexemes.get('statusbar_cursor_label_with_global', scope='statusbar',
                                        line=self.line_num_hr, column=self.col_num, position=self.cursor_pos)
            else:
                # Show status without selected text length as not selection
                return self.lexemes.get('statusbar_cursor_label', scope='statusbar',
                                        line=self.line_num_hr, column=self.col_num)

    def get_menu_actions(self) -> List[Dict[str, Any]]:
        """
        Main menu items map grouped for convenience.
        """
        return [
            {'name': 'main_menu_group_file', 'text': self.lexemes.get('group_file_label', scope='main_menu'),
             'items': [
                {'type': 'action', 'name': 'actions_file_label_new_document',
                 'system_icon': 'document-new', 'theme_icon': 'file-earmark-plus-fill.svg',
                 'label': self.lexemes.get('actions_file_label_new_document', scope='main_menu'),
                 'accessible_name': self.lexemes.get('actions_file_accessible_name_new_document', scope='main_menu'),
                 'action': self.action_new_file},
                {'type': 'action', 'name': 'actions_file_label_open',
                 'system_icon': 'document-open', 'theme_icon': 'folder-fill.svg',
                 'label': self.lexemes.get('actions_file_label_open', scope='main_menu'),
                 'accessible_name': self.lexemes.get('actions_file_accessible_name_open', scope='main_menu'),
                 'action': self.action_open_file},
                {'type': 'action', 'name': 'actions_file_label_save',
                 'system_icon': 'media-floppy', 'theme_icon': 'floppy2-fill.svg',
                 'label': self.lexemes.get('actions_file_label_save', scope='main_menu'),
                 'accessible_name': self.lexemes.get('actions_file_accessible_name_save', scope='main_menu'),
                 'action': self.action_save_file, 'var_name': 'save_button'},
                {'type': 'action', 'name': 'actions_file_label_save_as',
                 'system_icon': 'media-floppy', 'theme_icon': 'floppy2.svg',
                 'label': self.lexemes.get('actions_file_label_save_as', scope='main_menu'),
                 'accessible_name': self.lexemes.get('actions_file_accessible_name_save_as', scope='main_menu'),
                 'action': self.action_save_as_file, 'var_name': 'save_as_button'},
                {'type': 'delimiter'},
                {'type': 'action', 'name': 'actions_file_label_exit',
                 'system_icon': 'application-exit', 'theme_icon': 'power.svg',
                 'label': self.lexemes.get('actions_file_label_exit', scope='main_menu'),
                 'accessible_name': self.lexemes.get('actions_file_accessible_name_exit', scope='main_menu'),
                 'action': self.action_exit},
            ]},
            {'name': 'main_menu_group_edit', 'text': self.lexemes.get('group_edit_label', scope='main_menu'),
             'items': [
                {'type': 'action', 'name': 'main_menu_edit_actions_edit_mode',
                 'system_icon': 'accessories-text-editor', 'theme_icon': 'pencil-square.svg',
                 'label': self.lexemes.get('edit_actions_edit_mode', scope='main_menu'),
                 'accessible_name': self.lexemes.get('edit_actions_accessible_name_edit_mode', scope='main_menu'),
                 'action': self.action_edit_file},
                {'type': 'action', 'name': 'main_menu_edit_actions_source_mode',
                 'system_icon': 'edit-find', 'theme_icon': 'code-slash.svg',
                 'label': self.lexemes.get('edit_actions_source_mode', scope='main_menu'),
                 'accessible_name': self.lexemes.get('edit_actions_accessible_name_source_mode', scope='main_menu'),
                 'action': self.action_source},
                {'type': 'delimiter'},
                {'type': 'action', 'name': 'main_menu_edit_actions_bold',
                 'system_icon': 'format-text-bold', 'theme_icon': 'type-bold.svg',
                 'label': self.lexemes.get('edit_actions_bold', scope='main_menu'),
                 'accessible_name': self.lexemes.get('edit_actions_accessible_name_bold', scope='main_menu'),
                 'action': self.action_text_bold, 'switched_off_check': lambda: self.get_mode() != Mode.EDIT},
                {'type': 'action', 'name': 'main_menu_edit_actions_italic',
                 'system_icon': 'format-text-italic', 'theme_icon': 'type-italic.svg',
                 'label': self.lexemes.get('edit_actions_italic', scope='main_menu'),
                 'accessible_name': self.lexemes.get('edit_actions_accessible_name_italic', scope='main_menu'),
                 'action': self.action_text_italic, 'switched_off_check': lambda: self.get_mode() != Mode.EDIT},
                {'type': 'action', 'name': 'main_menu_edit_actions_underline',
                 'system_icon': 'format-text-underline', 'theme_icon': 'type-underline.svg',
                 'label': self.lexemes.get('edit_actions_underline', scope='main_menu'),
                 'accessible_name': self.lexemes.get('edit_actions_accessible_name_underline', scope='main_menu'),
                 'action': self.action_text_underline, 'switched_off_check': lambda: self.get_mode() != Mode.EDIT},
                {'type': 'action', 'name': 'main_menu_edit_actions_strikethrough',
                 'system_icon': 'format-text-strikethrough', 'theme_icon': 'type-strikethrough.svg',
                 'label': self.lexemes.get('edit_actions_strikethrough', scope='main_menu'),
                 'accessible_name': self.lexemes.get('edit_actions_accessible_name_strikethrough', scope='main_menu'),
                 'action': self.action_text_strikethrough, 'switched_off_check': lambda: self.get_mode() != Mode.EDIT},
                {'type': 'action', 'name': 'main_menu_edit_actions_blockquote',
                 'system_icon': 'format-text-blockquote', 'theme_icon': 'quote.svg',
                 'label': self.lexemes.get('edit_actions_blockquote', scope='main_menu'),
                 'accessible_name': self.lexemes.get('edit_actions_accessible_name_blockquote', scope='main_menu'),
                 'action': self.action_text_blockquote, 'switched_off_check': lambda: self.get_mode() != Mode.EDIT},
            ]},
            {'name': 'main_menu_group_tools', 'text': self.lexemes.get('group_tools_label', scope='main_menu'),
             'items': [
                 {'type': 'action', 'name': 'main_menu_tools_actions_ai_assistant', 'theme_icon': 'robot.svg',
                  'label': self.lexemes.get('tools_actions_ai_assistant', scope='main_menu'),
                  'accessible_name': self.lexemes.get('tools_actions_accessible_name_ai_assistant', scope='main_menu'),
                  'action': self.action_ai_assistant},
                 {'type': 'action', 'name': 'main_menu_tools_actions_color_picker', 'theme_icon': 'eyedropper.svg',
                  'label': self.lexemes.get('tools_actions_color_picker', scope='main_menu'),
                  'accessible_name': self.lexemes.get('tools_actions_accessible_name_color_picker', scope='main_menu'),
                  'action': self.action_text_color_picker},
             ]},
            {'name': 'main_menu_group_help', 'text': self.lexemes.get('group_help_label', scope='main_menu'),
             'items': [
                {'type': 'action', 'name': 'actions_help_label_check_for_updates', 'theme_icon': 'arrow-clockwise.svg',
                 'label': self.lexemes.get('actions_help_label_check_for_updates', scope='main_menu'),
                 'accessible_name': self.lexemes.get('actions_help_accessible_name_check_for_updates',
                                                     scope='main_menu'),
                 'action': self.action_check_for_updates},
                {'type': 'action', 'name': 'actions_help_label_bug_report', 'theme_icon': 'bandaid.svg',
                 'label': self.lexemes.get('actions_help_label_bug_report', scope='main_menu'),
                 'accessible_name': self.lexemes.get('actions_help_accessible_name_bug_report', scope='main_menu'),
                 'action': self.action_bug_report},
                {'type': 'delimiter'},
                {'type': 'action', 'name': 'actions_help_label_about',
                 'system_icon': 'help-about', 'theme_icon': 'balloon.svg',
                 'label': self.lexemes.get('actions_help_label_about', scope='main_menu'),
                 'accessible_name': self.lexemes.get('actions_help_accessible_name_about', scope='main_menu'),
                 'action': self.action_about},

            ]},
        ]

    def draw_menu(self) -> None:
        """
        Main menu. The app is designed to fulfill the duties without the main menu, but as a respect to the old days
        the menu can be switched on back in the settings.
        """

        # Get the menu bar
        menubar = self.menuBar()
        # Clear all previously set menus every time to allow update or hide the actions
        menubar.clear()

        if not self.settings.show_main_menu:
            return

        """
        System icons (vary, depends on the platform)
        * https://specifications.freedesktop.org/icon-naming-spec/0.8/ar01s04.html
            e.g.: openIcon = QIcon.fromTheme("document-open", QIcon("file-open.png"))
        * https://doc.qt.io/qt-6/qstyle.html#StandardPixmap-enum
            e.g.: openIcon = self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogStart)
        """
        for group_item in self.get_menu_actions():
            menu_group = menubar.addMenu(group_item['text'])  # type: QMenu
            menu_group.setObjectName(group_item['name'])
            theme_icon_color = self.theme_helper.get_color('main_menu_icon_color')
            for item in group_item['items']:
                if item['type'] == 'action':
                    # Or: icon = QIcon.fromTheme(item['system_icon'], QIcon(item['theme_icon']))
                    icon = self.theme_helper.get_icon(theme_icon=item['theme_icon'],
                                                      system_icon=item['system_icon'] if 'system_icon' in item else None,
                                                      color=theme_icon_color)
                    icon_action = QAction(icon, item['label'], self)
                    # Align with the dialog font size
                    if hasattr(icon_action, 'setFont'):
                        icon_action.setFont(self.font())
                    icon_action.setObjectName(item['name'])
                    if item['action'] is not None:
                        icon_action.triggered.connect(item['action'])
                    if 'accessible_name' in item and item['accessible_name'] is not None:
                        icon_action.setStatusTip(item['accessible_name'])  # This can be read by some screen readers
                    menu_group.addAction(icon_action)
                    # If the action has a switched off check, check it here
                    if ('switched_off_check' in item
                            and callable(item['switched_off_check'])
                            and item['switched_off_check']()):
                        # Switch the action off
                        icon_action.setDisabled(True)
                elif item['type'] == 'delimiter':
                    menu_group.addSeparator()

    def get_toolbar_actions(self) -> List[Dict[str, Any]]:
        """
        Main toolbar items map for convenience.
        """
        return [
            {'type': 'action', 'weight': 1, 'name': 'toolbar_actions_label_new_document', 'system_icon': 'document-new',
             'theme_icon': 'file-earmark-plus-fill.svg', 'color': self.theme_helper.get_color('toolbar_icon_color_new'),
             'label': self.lexemes.get('actions_label_new_document', scope='toolbar'),
             'accessible_name': self.lexemes.get('actions_accessible_name_new_document', scope='toolbar'),
             'action': self.action_new_file},
            {'type': 'action', 'weight': 2, 'name': 'toolbar_actions_label_open', 'system_icon': 'document-open',
             'theme_icon': 'folder-fill.svg', 'color': self.theme_helper.get_color('toolbar_icon_color_open'),
             'label': self.lexemes.get('actions_label_open', scope='toolbar'),
             'accessible_name': self.lexemes.get('actions_accessible_name_open', scope='toolbar'),
             'action': self.action_open_file},
            {'type': 'action', 'weight': 3, 'name': 'toolbar_actions_label_save', 'system_icon': 'media-floppy',
             'theme_icon': 'floppy2-fill.svg', 'color': self.theme_helper.get_color('toolbar_icon_color_save'),
             'label': self.lexemes.get('actions_label_save', scope='toolbar'),
             'accessible_name': self.lexemes.get('actions_accessible_name_save', scope='toolbar'),
             'action': self.action_save_file, 'var_name': 'toolbar_save_button', 'switched_off_check': lambda: True},
            {'type': 'delimiter'},
            {'type': 'action', 'weight': 4, 'name': 'toolbar_actions_label_edit',
             'system_icon': 'accessories-text-editor', 'theme_icon': 'pencil-square.svg',
             'color': self.theme_helper.get_color('toolbar_icon_color_edit'),
             'label': self.lexemes.get('actions_label_edit', scope='toolbar'),
             'accessible_name': self.lexemes.get('actions_accessible_name_edit', scope='toolbar'),
             'action': self.action_edit_file, 'active_state_check': lambda: self.get_mode() != Mode.EDIT},
            # Active Edit Mode icon
            {'type': 'action', 'weight': 4, 'name': 'toolbar_actions_label_edit_act',
             'system_icon': 'accessories-text-editor', 'theme_icon': 'pencil-square.svg',
             'color': self.theme_helper.get_color('toolbar_icon_color_edit_act'),
             'label': self.lexemes.get('actions_label_edit', scope='toolbar'),
             'accessible_name': self.lexemes.get('actions_accessible_name_edit', scope='toolbar'),
             'action': self.action_edit_file, 'active_state_check': lambda: self.get_mode() == Mode.EDIT},
            {'type': 'action', 'weight': 5, 'name': 'toolbar_actions_label_source', 'system_icon': 'edit-find',
             'theme_icon': 'code-slash.svg', 'color': self.theme_helper.get_color('toolbar_icon_color_source'),
             'label': self.lexemes.get('actions_label_source', scope='toolbar'),
             'accessible_name': self.lexemes.get('actions_accessible_name_source', scope='toolbar'),
             'action': self.action_source, 'var_name': 'toolbar_source_button',
             'active_state_check': lambda: self.get_mode() != Mode.SOURCE},
            # Active Source Mode icon
            {'type': 'action', 'weight': 5, 'name': 'toolbar_actions_label_source_act', 'system_icon': 'edit-find',
             'theme_icon': 'code-slash.svg', 'color': self.theme_helper.get_color('toolbar_icon_color_source_act'),
             'label': self.lexemes.get('actions_label_source', scope='toolbar'),
             'accessible_name': self.lexemes.get('actions_accessible_name_source', scope='toolbar'),
             'action': self.action_source, 'var_name': 'toolbar_source_active_button',
             'active_state_check': lambda: self.get_mode() == Mode.SOURCE},
            {'type': 'action', 'weight': 6, 'name': 'toolbar_actions_label_encrypt', 'system_icon': 'security-low',
             'theme_icon': 'shield-lock.svg', 'color': self.theme_helper.get_color('toolbar_icon_color_encrypt'),
             'label': self.lexemes.get('actions_label_encrypt', scope='toolbar'),
             'accessible_name': self.lexemes.get('actions_accessible_name_encrypt', scope='toolbar'),
             'action': self.action_encrypt, 'var_name': 'toolbar_encrypt_button',
             'active_state_check': lambda: self.get_encryption() != Encryption.ENCRYPTED},
            # Active Encryption icon
            {'type': 'action', 'weight': 6, 'name': 'toolbar_actions_label_decrypt', 'system_icon': 'security-medium',
             'theme_icon': 'shield-lock-fill.svg', 'color': self.theme_helper.get_color('toolbar_icon_color_decrypt'),
             'label': self.lexemes.get('actions_label_decrypt', scope='toolbar'),
             'accessible_name': self.lexemes.get('actions_accessible_name_decrypt', scope='toolbar'),
             'action': self.action_decrypt, 'var_name': 'toolbar_decrypt_button',
             'active_state_check': lambda: self.get_encryption() == Encryption.ENCRYPTED},
            {'type': 'delimiter'},
            # Text format
            {'type': 'action', 'weight': 7, 'name': 'toolbar_toolbar_icon_color_bold',
             'system_icon': 'format-text-bold', 'theme_icon': 'type-bold.svg',
             'color': self.theme_helper.get_color('toolbar_icon_color_bold'),
             'label': self.lexemes.get('actions_label_bold', scope='toolbar'),
             'accessible_name': self.lexemes.get('actions_accessible_name_bold', scope='toolbar'),
             'action': self.action_text_bold, 'switched_off_check': lambda: self.get_mode() != Mode.EDIT},
            {'type': 'action', 'weight': 8, 'name': 'toolbar_actions_label_italic',
             'system_icon': 'format-text-italic', 'theme_icon': 'type-italic.svg',
             'color': self.theme_helper.get_color('toolbar_icon_color_italic'),
             'label': self.lexemes.get('actions_label_italic', scope='toolbar'),
             'accessible_name': self.lexemes.get('actions_accessible_name_italic', scope='toolbar'),
             'action': self.action_text_italic, 'switched_off_check': lambda: self.get_mode() != Mode.EDIT},
            {'type': 'action', 'weight': 9, 'name': 'toolbar_actions_label_underline',
             'system_icon': 'format-text-underline', 'theme_icon': 'type-underline.svg',
             'color': self.theme_helper.get_color('toolbar_icon_color_underline'),
             'label': self.lexemes.get('actions_label_underline', scope='toolbar'),
             'accessible_name': self.lexemes.get('actions_accessible_name_underline', scope='toolbar'),
             'action': self.action_text_underline, 'switched_off_check': lambda: self.get_mode() != Mode.EDIT},
            {'type': 'action', 'weight': 10, 'name': 'toolbar_actions_label_strikethrough',
             'system_icon': 'format-text-strikethrough', 'theme_icon': 'type-strikethrough.svg',
             'color': self.theme_helper.get_color('toolbar_icon_color_strikethrough'),
             'label': self.lexemes.get('actions_label_strikethrough', scope='toolbar'),
             'accessible_name': self.lexemes.get('actions_accessible_name_strikethrough', scope='toolbar'),
             'action': self.action_text_strikethrough, 'switched_off_check': lambda: self.get_mode() != Mode.EDIT},
            {'type': 'action', 'weight': 11, 'name': 'toolbar_actions_label_blockquote',
             'system_icon': 'format-text-blockquote', 'theme_icon': 'quote.svg',
             'color': self.theme_helper.get_color('toolbar_icon_color_blockquote'),
             'label': self.lexemes.get('actions_label_blockquote', scope='toolbar'),
             'accessible_name': self.lexemes.get('actions_accessible_name_blockquote', scope='toolbar'),
             'action': self.action_text_blockquote, 'switched_off_check': lambda: self.get_mode() != Mode.EDIT},
            {'type': 'delimiter'},
            {'type': 'action', 'weight': 12, 'name': 'toolbar_actions_label_ai_assistant',
             'theme_icon': 'robot.svg', 'color': self.theme_helper.get_color('toolbar_icon_color_ai_assistant'),
             'label': self.lexemes.get('actions_label_ai_assistant', scope='toolbar'),
             'accessible_name': self.lexemes.get('actions_accessible_name_ai_assistant', scope='toolbar'),
             'action': self.action_ai_assistant,
             'active_state_check': lambda: not hasattr(self, 'ai_assistant') or not self.ai_assistant},
            # Active AI Assistant icon
            {'type': 'action', 'weight': 12, 'name': 'toolbar_actions_label_ai_assistant_act',
             'theme_icon': 'robot.svg', 'color': self.theme_helper.get_color('toolbar_icon_color_ai_assistant_act'),
             'label': self.lexemes.get('actions_label_ai_assistant', scope='toolbar'),
             'accessible_name': self.lexemes.get('actions_accessible_name_ai_assistant', scope='toolbar'),
             'action': None,
             'active_state_check': lambda: hasattr(self, 'ai_assistant') and self.ai_assistant},
            {'type': 'action', 'weight': 13, 'name': 'toolbar_actions_label_color', 'theme_icon': 'eyedropper.svg',
             'color': self.theme_helper.get_color('toolbar_icon_color_color_picker'),
             'label': self.lexemes.get('actions_label_color_picker', scope='toolbar'),
             'accessible_name': self.lexemes.get('actions_accessible_name_color_picker', scope='toolbar'),
             'action': self.action_text_color_picker,
             'active_state_check': lambda: not hasattr(self, 'color_picker') or not self.color_picker},
            # Active Color Picker icon
            {'type': 'action', 'weight': 13, 'name': 'toolbar_actions_label_color_act', 'theme_icon': 'eyedropper.svg',
             'color': self.theme_helper.get_color('toolbar_icon_color_color_picker_act'),
             'label': self.lexemes.get('actions_label_color_picker', scope='toolbar'),
             'accessible_name': self.lexemes.get('actions_accessible_name_color_picker', scope='toolbar'),
             'action': None,
             'active_state_check': lambda: hasattr(self, 'color_picker') and self.color_picker},
            {'type': 'delimiter'},
            {'type': 'action', 'weight': 14, 'name': 'toolbar_actions_label_about',
             'theme_icon': 'balloon-fill.svg', 'color': self.theme_helper.get_color('toolbar_icon_color_about'),
             'label': self.lexemes.get('actions_label_about', scope='toolbar'),
             'accessible_name': self.lexemes.get('actions_accessible_name_about', scope='toolbar'),
             'action': self.action_about},
            {'type': 'action', 'weight': 15, 'name': 'toolbar_actions_label_exit',
             'theme_icon': 'power.svg', 'color': self.theme_helper.get_color('toolbar_icon_color_exit'),
             'label': self.lexemes.get('actions_label_exit', scope='toolbar'),
             'accessible_name': self.lexemes.get('actions_accessible_name_exit', scope='toolbar'),
             'action': self.action_exit},
            {'type': 'action', 'weight': 16, 'name': 'toolbar_actions_label_settings',
             'theme_icon': 'three-dots.svg', 'color': self.theme_helper.get_color('toolbar_icon_color_settings'),
             'label': self.lexemes.get('actions_label_settings', scope='toolbar'),
             'accessible_name': self.lexemes.get('actions_accessible_name_settings', scope='toolbar'),
             'action': self.action_settings},
        ]

    def get_toolbar_action_by_name(self, name):
        """
        Get particular action config by name.
        """
        for action in self.get_toolbar_actions():
            if 'name' in action and action['name'] == name:
                return action

    def get_toolbar_search_buttons(self) -> List[Dict[str, Any]]:
        """
        Toolbar's search buttons map.
        """
        return [
            {'type': 'action', 'name': 'search_clear', 'system_icon': 'window-close', 'theme_icon': 'x-circle-fill.svg',
             'action': self.action_search_clear, 'enabled': False, 'default': False,
             'tooltip': self.lexemes.get('search_buttons_label_clear', scope='toolbar'),
             'accessible_name': self.lexemes.get('search_buttons_accessible_name_clear', scope='toolbar'),
             'var_name': 'btn_search_clear', 'color': self.theme_helper.get_color('toolbar_search_button_clear')},
            {'type': 'action', 'name': 'search_prev', 'system_icon': 'go-up', 'theme_icon': 'caret-up-fill.svg',
             'action': self.action_search_prev, 'enabled': False, 'default': False,
             'tooltip': self.lexemes.get('search_buttons_label_prev', scope='toolbar'),
             'accessible_name': self.lexemes.get('search_buttons_accessible_name_prev', scope='toolbar'),
             'var_name': 'btn_search_prev', 'color': self.theme_helper.get_color('toolbar_search_button_prev')},
            {'type': 'action', 'name': 'search_next', 'system_icon': 'go-down', 'theme_icon': 'caret-down-fill.svg',
             'action': self.action_search_next, 'enabled': False, 'default': True,
             'tooltip': self.lexemes.get('search_buttons_label_next', scope='toolbar'),
             'accessible_name': self.lexemes.get('search_buttons_accessible_name_next', scope='toolbar'),
             'var_name': 'btn_search_next', 'color': self.theme_helper.get_color('toolbar_search_button_next')},
        ]

    def get_toolbar_search_button_by_name(self, name: str) -> Dict:
        """
        Get particular button config by name.
        """
        for button in self.get_toolbar_search_buttons():
            if 'name' in button and button['name'] == name:
                return button

    def create_icons_toolbar(self, refresh: bool = False) -> None:
        """
        Main toolbar with icons.
        """
        if refresh and hasattr(self, 'toolbar'):
            self.removeToolBar(self.toolbar)
        """
        Toolbar element:
        toolbar = self.addToolBar("Toolbar")
        Or create QToolBar object first
        """
        self.toolbar = ToolBar(
            parent=self,
            labels=self.get_toolbar_actions(),
            refresh=lambda: self.create_icons_toolbar(refresh=True)
        )
        self.addToolBar(self.toolbar)
        self.toolbar.setMovable(False)

        prev_type = None
        for icon in self.get_toolbar_actions():
            if icon['type'] == 'action':
                # Check visible icon is checked in settings
                if not (self.settings.toolbar_icons & pow(2, icon['weight'])):
                    # Skip if not checked in settings
                    continue
                # If the icon has an active state check, check it here
                if ('active_state_check' in icon
                        and callable(icon['active_state_check'])
                        and not icon['active_state_check']()):
                    # Skip if the icon isn't active
                    continue
                result_icon = self.create_toolbar_icon(
                    system_icon=icon['system_icon'] if 'system_icon' in icon else None,
                    theme_icon=icon['theme_icon'],
                    label=icon['label'],
                    action=icon['action'],
                    accessible_name=icon['accessible_name'],
                    color=icon['color'] if 'color' in icon else self.theme_helper.get_color('toolbar_icon_color_default'),
                    toolbar=self.toolbar
                )
                # Add internal variable to access the icon later, say for state toggle
                if 'var_name' in icon:
                    if self.debug and hasattr(self, icon['var_name']):
                        self.logger.debug('Variable "%s" is already set! Re-writing it...' % icon['var_name'])
                    setattr(self, icon['var_name'], result_icon)  # type: QToolButton
                # If the icon has a switched off check, check it here
                if ('switched_off_check' in icon
                        and callable(icon['switched_off_check'])
                        and icon['switched_off_check']()):
                    # Switch the icon off
                    result_icon.setDisabled(True)
            elif icon['type'] == 'delimiter' and prev_type != 'delimiter':
                self.toolbar.addSeparator()
            # Save prev type
            prev_type = icon['type']

        central_spacer = QWidget(self)
        central_spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.toolbar.addWidget(central_spacer)

        search_label = QLabel(self)
        # Apply font from the main window to the widget
        search_label.sizeHint()
        search_label.setText(self.lexemes.get('search_input_label', scope='toolbar'))
        search_label.setObjectName('search_input_label')  # To differentiate it at styles file
        self.toolbar.addWidget(search_label)

        self.search_input = QLineEdit(self)
        self.search_input.setObjectName('search_input')
        self.search_input.sizeHint()
        self.search_input.setReadOnly(False)
        self.search_input.setMaxLength(128)
        self.search_input.setMaximumWidth(self.weight_to_px_uno)
        self.search_input.setPlaceholderText(self.lexemes.get('search_input_placeholder_text', scope='toolbar'))
        self.search_input.setAccessibleDescription(self.lexemes.get('search_input_accessible_description', scope='toolbar'))
        self.search_input.textChanged.connect(self.action_search_on)
        self.search_input.returnPressed.connect(self.action_search_next)
        self.toolbar.addWidget(self.search_input)

        for button in self.get_toolbar_search_buttons():
            if button['type'] == 'action':
                result = self.create_toolbar_button(
                    system_icon=button['system_icon'],
                    theme_icon=button['theme_icon'],
                    action=button['action'],
                    tooltip=button['tooltip'],
                    default=button['default'],
                    enabled=button['enabled'],
                    accessible_name=button['accessible_name'],
                    color=button['color'] if 'color' in button else self.theme_helper.get_color('toolbar_icon_color_default'),
                    toolbar=self.toolbar
                )
                if 'var_name' in button:
                    if self.debug and hasattr(self, button['var_name']):
                        self.logger.debug('Variable "%s" is already set! Re-writing it...' % button['var_name'])
                    setattr(self, button['var_name'], result)  # type: QPushButton

        search_match_case_label = QLabel(self)
        search_match_case_label.sizeHint()
        search_match_case_label.setText(self.lexemes.get('search_case_sensitive', scope='toolbar'))
        search_match_case_label.setObjectName("search_case_sensitive")  # To differentiate it at styles file
        self.toolbar.addWidget(search_match_case_label)

        self.search_match_case = QCheckBox(self)
        self.search_match_case.sizeHint()
        self.search_match_case.setToolTip(self.lexemes.get('search_match_case_tooltip', scope='toolbar'))
        self.search_match_case.setCheckState(Qt.CheckState.Unchecked)
        self.toolbar.addWidget(self.search_match_case)

        """
        It can be done by setting inline styles, but this is not what can be convenient for customisation,
        hence the theme:
        """
        # self.toolbar.setStyleSheet("""QCheckBox {
        #    margin-right: 5px;
        # }""")
        self.toolbar.setStyleSheet(self.theme_helper.get_css('toolbar'))

    def create_toolbar_icon(self, **kwargs) -> QToolButton:
        """
        Helper to create, add to the toolbar and return button with an icon.
        """
        name = kwargs['name'] if 'name' in kwargs else None
        system_icon = kwargs['system_icon'] if 'system_icon' in kwargs else None
        theme_icon = kwargs['theme_icon'] if 'theme_icon' in kwargs else None
        theme_icon_color = QColor(kwargs['color']) if 'color' in kwargs and kwargs['color'] else None
        label = kwargs['label'] if 'label' in kwargs else None
        # Action triggered on click
        action = kwargs['action'] if 'action' in kwargs else None
        accessible_name = kwargs['accessible_name'] if 'accessible_name' in kwargs else  None
        icon_toolbar = kwargs['toolbar'] if 'toolbar' in kwargs else None
        # Theme icon with a fallback to a system one
        icon = self.theme_helper.get_icon(theme_icon=theme_icon, system_icon=system_icon, color=theme_icon_color)
        icon_action = QAction(icon, label, self)
        icon_button = QToolButton(self)
        icon_button.setObjectName(name)
        icon_button.setToolTip(label)
        # icon_button.setIconSize(QSize(16, 16));
        icon_button.setDefaultAction(icon_action)
        # icon_action.setChecked(True)
        if action is not None:
            icon_action.triggered.connect(action)
        if accessible_name is not None:
            icon_button.setAccessibleName(accessible_name)
        # Add the button to the toolbar
        if icon_toolbar is not None:
            icon_toolbar.addWidget(icon_button)
        # Return button as a result
        return icon_button

    def create_toolbar_button(self, **kwargs) -> QPushButton:
        """
        Helper to create and return toolbar push button.
        """
        system_icon = kwargs['system_icon'] if 'system_icon' in kwargs else None
        theme_icon = kwargs['theme_icon'] if 'theme_icon' in kwargs else None
        theme_icon_color = QColor(kwargs['color']) if 'color' in kwargs and kwargs['color'] else None
        # Action clicked
        action = kwargs['action'] if 'action' in kwargs else None
        accessible_name = kwargs['accessible_name'] if 'accessible_name' in kwargs else  None
        tooltip = kwargs['tooltip'] if 'tooltip' in kwargs else None
        default = kwargs['default'] if 'default' in kwargs else None
        enabled = kwargs['enabled'] if 'enabled' in kwargs else None
        icon_toolbar = kwargs['toolbar'] if 'toolbar' in kwargs else None
        # Theme icon with a fallback to a system one
        icon = self.theme_helper.get_icon(theme_icon=theme_icon, system_icon=system_icon, color=theme_icon_color)
        # Toolbar button with an icon
        icon_button = QPushButton(self)
        icon_button.setFont(self.font())
        if hasattr(self, 'search_input'):
            # Adjust size to maintain ratio
            size_hint = self.search_input.sizeHint()  # As a real height hint check the line edit height
            icon_button.setFixedSize(QSize(size_hint.height(), size_hint.height()))
            icon_height = int(size_hint.height() * 0.7)
            icon_button.setIconSize(QSize(icon_height, icon_height))
        icon_button.setIcon(icon)
        if action is not None:
            icon_button.clicked.connect(action)
        if accessible_name is not None:
            icon_button.setAccessibleName(accessible_name)
        if tooltip is not None:
            icon_button.setToolTip(tooltip)
        if default is not None:
            icon_button.setDefault(default)
        if enabled is not None:
            icon_button.setEnabled(enabled)
        # Add the button to the toolbar
        if icon_toolbar is not None:
            icon_toolbar.addWidget(icon_button)
        # Return button as a result
        return icon_button

    def create_status_toolbar(self) -> None:
        # Statusbar element
        self.statusbar = StatusBar(self)
        self.setStatusBar(self.statusbar)

    def action_new_file(self, content: str = None) -> bool:
        """
        Action: Create a new file.
        """
        if self.get_mode() == Mode.EDIT:
            # Save any unsaved changes
            self.save_active_file(clear_after=True)
        else:
            # Toggle mode first to start new file in EDIT mode
            self.toggle_mode()

        i = 1
        new_file_name_tpl = 'new-document-%d.md'

        # Find the file name that is not exist
        while (file_path := res_path(new_file_name_tpl % i)) and os.path.isfile(file_path):
            i += 1
            # Just to prevent never-ending cycle
            if i > 9999:
                return False

        # Default file content if none provided
        if not content:
            new_file_content_tpl = '# ' + self.lexemes.get('action_new_file_first_line_template_text') + ' %d\r\n'
            content = new_file_content_tpl % i

        if self.debug:
            self.logger.debug('New document "%s"' % file_path)

        header = FileHeader().get_new()
        content = header.pack(content)

        self.save_file_content(file_path, content)
        # Load new file content
        return self.load_file(file_path)

    def action_open_file(self) -> None:
        """
        Action: Open a new file.
        Changes current file path and therefore a dir path as well
        """

        """
        * https://doc.qt.io/qt-6/qfiledialog.html#details
        * https://doc.qt.io/qt-6/qfiledialog.html#getOpenFileName
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            caption=self.lexemes.get('action_open_file_dialog_caption'),
            # Also can be: os.path.expanduser("~") or QDir.currentPath()
            dir=os.path.expanduser(self.get_current_path(is_base=True)),
            # Filter accepts possible file types to show
            filter='Text Files (%s);;All Files (*)' % ' '.join(["*." + ext for ext in self.supported_file_extensions]),
            # QFileDialog.Option.ReadOnly
            # https://doc.qt.io/qt-6/qfiledialog.html#Option-enum
            options=QFileDialog.Option.DontUseCustomDirectoryIcons
        )
        if os.path.isfile(file_path):
            # Save any unsaved changes
            self.save_active_file(clear_after=True)
            # Load file for current mode
            self.load_file(file_path)

    def action_save_file(self, file_path: str = None) -> None:
        """
        Action: Save file.
        """
        # Choose currently open file if another one is not explicitly passed
        if file_path is None:
            file_path = self.get_current_path()

        if file_path is None:
            if self.logging:
                self.logger.warning('Cannot save file because of the file path is not set!')
            return

        # Save any unsaved changes, keep text edit field's content
        self.save_active_file(clear_after=False)

    def action_save_as_file(self) -> None:
        """
        Action: Save as a file.
        """
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            caption=self.lexemes.get('action_save_as_file_dialog_caption'),
            dir=os.path.expanduser(self.get_current_path(is_base=True)),
            # Filter accepts possible file types to show
            filter='Text Files (%s);;All Files (*)' % ' '.join(["*." + ext for ext in self.supported_file_extensions]),
            # https://doc.qt.io/qt-6/qfiledialog.html#Option-enum
            # options=QFileDialog.Option.DontUseNativeDialog
        )
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                # Edit widget
                edit_widget = self.get_edit_widget()  # type: Union[EditWidget, QPlainTextEdit]
                file.write(edit_widget.toPlainText())

    def action_edit_file(self) -> None:
        """
        Action: Edit/View mode toggle.
        """
        if self.debug:
            self.logger.debug('Edit file "%s"' % self.get_current_path())

        # Save any unsaved changes
        self.save_active_file(clear_after=True)

        # Toggle mode
        self.toggle_mode()

        # Reload content for current mode
        self.reload_active_file()

    def action_source(self) -> None:
        """
        Action: Show source code when mode set to SOURCE.
        """

        if self.debug:
            self.logger.debug("Source view requested from mode '%s', from source '%s';"
                              "previous states were '%s' and '%s' correspondingly"
                              % (Mode(self.get_mode()).name, Source(self.get_source()).name,
                                 Mode(self.get_prev_mode()).name, Source(self.get_prev_source()).name))

        if self.get_mode() == Mode.SOURCE:
            # Toggle mode to either VIEW or EDIT modes
            self.toggle_mode()
            # Reload content for current mode
            self.reload_active_file()
            return

        # Save any unsaved changes
        self.save_active_file(clear_after=True)

        # Next toggle will restore VIEW mode
        self.set_mode(Mode.SOURCE)

        self.load_source()

    def load_source(self):
        # View document
        view_doc = self.get_view_doc()  # type: QTextDocument

        # Show source according to which self.source set
        if self.get_source() == Source.MARKDOWN:
            # Show header data and source content.
            source_data = '%s\n%s' % (self.header, self.content)
        else:
            # Convert current content to html to show html source.
            source_data = self.convert_markdown_to_html(self.content)

        """
        Do not use `view_widget.setPlainText(html_data)` as it inherit styles from the prev view.
        """
        view_doc.setPlainText(source_data)

    def action_encrypt(self) -> None:
        """
        Action: Encrypt file data with symmetric encryption algorithm.
        """

        current_file_path = self.get_current_path()
        if self.debug:
            self.logger.debug('Encrypting file "%s"' % current_file_path)
        # Save active file data if needed
        self.save_active_file(clear_after=False)

        # The file is already encrypted
        if self.is_file_encrypted(current_file_path):
            self.message_box(self.lexemes.get('encrypt_file_warning_file_is_already_encrypted'), icon_type=2)
            return

        # TODO update when '.enc' extension is not in use anymore
        encrypted_file_path = current_file_path + '.enc'
        current_file_name = os.path.basename(current_file_path)
        self.common_dialog(
            self.lexemes.get('dialog_encrypt_file_title'),
            self.lexemes.get(name='dialog_encrypt_file_text', file_name=current_file_name),
            callback=lambda dialog_callback:
                self.encrypt_file_dialog_callback(dialog_callback, current_file_path, encrypted_file_path))

    def encrypt_file_dialog_callback(self, callback: Callable[..., Any] = None, from_file_path: str = None,
                                     to_file_path: str = None, ignore_existing_to_file: bool = False) -> None:
        """
        The callback method passed to the encrypt file dialog and executed upon completion.
        """

        if self.debug:
            self.logger.debug('Encrypt file dialog callback with sub-callback %s' % callback)

        if os.path.isfile(to_file_path) and not ignore_existing_to_file:
            self.common_dialog(
                self.lexemes.get('dialog_encrypt_file_rewrite_existing_title'),
                self.lexemes.get(name='dialog_encrypt_file_rewrite_existing_text', file_path=to_file_path),
                callback=lambda dialog_callback: self.encrypt_file_dialog_callback(
                    # Because of nested dialogs, and each has its own callback
                    # Rewrite file callback > then > Encrypt file callback
                    callback=lambda: (dialog_callback(), callback()),
                    from_file_path=from_file_path,
                    to_file_path=to_file_path,
                    ignore_existing_to_file=True))
            # This method will be called again with new params within "callback" set above
            return

        file_header, file_body = FileHeader().load_file(from_file_path)

        if (file_header is None  # File_header should exist at this point, but check if it is not None anyway
                or not file_header.is_valid()):
            # Create new file header
            file_header = FileHeader().get_new(is_enc=True)
        elif not file_header.is_file_encrypted():
            file_header.set_encrypted()

        # Check file header contains salt and the other params. May update migration params.
        # Only if the file is encrypted!
        try:
            file_header.validate_enc()
        except Exception as e:
            if self.logging:
                self.logger.error('File header cannot be validated "%s"' % e)

        # Update the header with new date
        file_header.refresh()

        # Get file specific salt if set
        file_salt = file_header.get_enc_param('slt')
        file_iterations = int(file_header.get_enc_param('itr'))

        # Encrypt
        encrypted_file_body_b = (self.get_encrypt_helper(
            salt=file_salt, new_password=True, iterations=file_iterations).encrypt_data(file_body.encode("utf-8")))
        if encrypted_file_body_b:
            encrypted_file_body = encrypted_file_body_b.decode("utf-8")
            # Check and adjust header params if needed
            if (not file_header.get_enc_param('hint')
                    and self.enc_password
                    and self.enc_password.hint):
                try:
                    file_header.set_enc_param('hint', self.enc_password.hint)
                except Exception as e:
                    if self.logging:
                        self.logger.error('File header cannot be updated "%s"' % e)
            # Pack file header and file body
            content = file_header.pack(encrypted_file_body)
            result = self.save_file_content(to_file_path, content)
        else:
            result = False

        # Switch to the new file
        if result:
            self.header = file_header
            self.content = file_body
            self.load_file(to_file_path)

        if callable(callback):
            callback()

    def action_decrypt(self) -> None:
        """
        Action: Decrypt encrypted file data.
        """

        current_file_path = self.get_current_path()
        if self.debug:
            self.logger.debug('Decrypting file "%s"' % current_file_path)
        # Save active file data if needed
        self.save_active_file(clear_after=False)

        # The file is encrypted
        if not self.is_file_encrypted(current_file_path):
            self.message_box(self.lexemes.get('decrypt_file_warning_file_is_not_encrypted'), icon_type=2)
            return

        # TODO update when '.enc' extension is not in use anymore
        decrypted_file_path = current_file_path[:-4]
        current_file_name = os.path.basename(current_file_path)
        self.common_dialog(
            self.lexemes.get('dialog_decrypt_file_title'),
            self.lexemes.get(name='dialog_decrypt_file_text', file_name=current_file_name),
            callback=lambda dialog_callback:
                self.decrypt_file_dialog_callback(dialog_callback, current_file_path, decrypted_file_path))

    def decrypt_file_dialog_callback(self, callback: Callable[..., Any] = None, from_file_path: str = None,
                                     to_file_path: str = None, ignore_existing_to_file: bool = False) -> None:
        """
        The callback method passed to the decrypt file dialog and executed upon completion.
        """
        if self.debug:
            self.logger.debug('Decrypt encrypted file dialog callback with sub-callback %s' % callback)

        if os.path.isfile(to_file_path) and not ignore_existing_to_file:
            self.common_dialog(
                self.lexemes.get('dialog_decrypt_file_rewrite_existing_title'),
                self.lexemes.get(name='dialog_decrypt_file_rewrite_existing_text', file_path=to_file_path),
                callback=lambda dialog_callback: self.decrypt_file_dialog_callback(
                    # Because of nested dialogs, and each has its own callback
                    # Rewrite file callback > then > Encrypt file callback
                    callback=lambda: (dialog_callback(), callback()),
                    from_file_path=from_file_path,
                    to_file_path=to_file_path,
                    ignore_existing_to_file=True))
            # This method will be called again with new params within "callback" set above
            return

        file_header, encrypted_file_body = FileHeader().load_file(from_file_path)
        # Check file header contains salt and the other params. May update migration params.
        # Only if the file is encrypted!
        try:
            file_header.validate_enc()
        except Exception as e:
            if self.logging:
                self.logger.error('File header cannot be validated "%s"' % e)
        # File specific salt should be set within encrypted file
        file_salt = file_header.get_enc_param('slt')
        file_iterations = int(file_header.get_enc_param('itr'))

        try:
            decrypted_file_body = self.get_encrypt_helper(
                salt=file_salt, iterations=file_iterations).decrypt_data(encrypted_file_body.encode("utf-8"))
            if decrypted_file_body:
                file_body = decrypted_file_body.decode("utf-8")
                # Write decrypted file
                new_header = FileHeader().get_new()
                content = new_header.pack(file_body)
                result = self.save_file_content(to_file_path, content)
            else:
                if self.debug:
                    self.logger.debug('Cannot decrypt file "%s"' % from_file_path)
                """
                * https://docs.python.org/3/reference/compound_stmts.html#the-try-statement
                """
                raise InvalidToken
        except (InvalidToken, InvalidSignature, TypeError):
            if self.logging:
                self.logger.warning('Cannot apply decryption password!')
            result = False

        # Switch to the new file
        if result:
            self.load_file(to_file_path)

        if callable(callback):
            callback()

    def action_text_bold(self) -> None:
        """
        Action: Text format BOLD.
        """

        # Edit widget
        edit_widget = self.get_edit_widget()  # type: Union[EditWidget, QPlainTextEdit]

        cursor = edit_widget.textCursor()
        if cursor.hasSelection():
            selected_text = cursor.selectedText()
            re = QRegularExpression(r'^(\*\*|__)(.*?)(\*\*|__)$')
            match = re.match(selected_text)
            if match.capturedTexts() and match.captured(2):
                cursor.insertText(match.captured(2))
            else:
                cursor.insertText('**' + selected_text + '**')

    def action_text_italic(self) -> None:
        """
        Action: Text format ITALIC.
        """

        # Edit widget
        edit_widget = self.get_edit_widget()  # type: Union[EditWidget, QPlainTextEdit]

        cursor = edit_widget.textCursor()
        if cursor.hasSelection():
            selected_text = cursor.selectedText()
            # r'^(?:\*|_)(.*?)(?:\*|_)$' causes symbols replacement
            re = QRegularExpression(r'^(\*|_)(.*?)(\*|_)$')
            match = re.match(selected_text)
            if match.capturedTexts() and match.captured(2):
                cursor.insertText(match.captured(2))
            else:
                cursor.insertText('*' + selected_text + '*')

    def action_text_underline(self) -> None:
        """
        Action: Text format UNDERLINE.
        """

        # Edit widget
        edit_widget = self.get_edit_widget()  # type: Union[EditWidget, QPlainTextEdit]

        cursor = edit_widget.textCursor()
        if cursor.hasSelection():
            selected_text = cursor.selectedText()
            re = QRegularExpression(r'^<u>(.*?)</u>$')
            match = re.match(selected_text)
            if match.capturedTexts() and match.captured(1):
                cursor.insertText(match.captured(1))
            else:
                cursor.insertText('<u>' + selected_text + '</u>')

    def action_text_strikethrough(self) -> None:
        """
        Action: Text format STRIKETHROUGH.
        """

        # Edit widget
        edit_widget = self.get_edit_widget()  # type: Union[EditWidget, QPlainTextEdit]

        cursor = edit_widget.textCursor()
        if cursor.hasSelection():
            selected_text = cursor.selectedText()
            re = QRegularExpression(r'^(~~)(.*?)(~~)$')
            match = re.match(selected_text)
            if match.capturedTexts() and match.captured(2):
                cursor.insertText(match.captured(2))
            else:
                cursor.insertText('~~' + selected_text + '~~')

    def action_text_blockquote(self) -> None:
        """
        Action: Text format BLOCKQUOTE.
        """

        # Edit widget
        edit_widget = self.get_edit_widget()  # type: Union[EditWidget, QPlainTextEdit]

        cursor = edit_widget.textCursor()
        if cursor.hasSelection():
            selected_text = cursor.selectedText()
            re = QRegularExpression(r'^\s*?\>+\s(.*?)$')
            match = re.match(selected_text)
            if match.capturedTexts() and match.captured(1):
                cursor.insertText(match.captured(1))
            else:
                # TODO for each line after a paragraph and the line starting with ' > '
                cursor.insertText('> ' + selected_text)

    def action_text_color_picker(self) -> None:
        """
        Action: Text format COLOR with a picker.
        """
        self.color_picker = ColorPickerDialog(self)
        self.color_picker.color_selected.connect(self.text_color_picker_handler)
        # To update icon within toolbar before dialog
        self.create_icons_toolbar(refresh=True)
        # Run dialog
        self.color_picker.exec()
        # Unset dialog var
        self.color_picker = None
        # To update icon within toolbar after dialog
        self.create_icons_toolbar(refresh=True)

    def text_color_picker_handler(self, color):
        # Targeting widget, either Edit or View one
        if self.get_mode() == Mode.EDIT:
            targeting_widget = self.get_edit_widget()  # type: Union[EditWidget, QPlainTextEdit]
        else:
            targeting_widget = self.get_view_widget()  # type: Union[ViewWidget, QTextBrowser]

        # Get cursor position to check any selected text there
        cursor = targeting_widget.textCursor()

        selected_text = ''  # Default
        if cursor.hasSelection():
            selected_text = cursor.selectedText()
            """
            # Make possible to undo selected text formatting:
            re = QRegularExpression(r'^(<span style="color:\s*?[a-zA-z]+;?">)(.*?)(<\/span>)$')
            match = re.match(selected_text)
            if match.capturedTexts() and match.captured(2):
                cursor.insertText(match.captured(2))
            """
        updated_text = f'<span style="color: {color}">{selected_text}</span>'

        if self.get_mode() == Mode.EDIT:
            # Set True to keep inserted fragment selected
            cursor.setKeepPositionOnInsert(True)
            # Replace selected text with formatted one
            cursor.insertText(updated_text)
            # Update cursor to show selected fragment
            targeting_widget.setTextCursor(cursor)
            targeting_widget.ensureCursorVisible()
        else:
            # Cope the text to the clipboard
            ClipboardHelper.set_text(updated_text)
            # Show frameless message box closing by timer as a tooltip
            self.message_box(self.lexemes.get('dialog_color_picker_color_copied_to_the_clipboard'),
                             frameless=True, timer_sec=2)

    def action_ai_assistant(self) -> None:
        """
        Action: AI assistant.
        """

        if self.debug:
            self.logger.debug('AI assistant')

        self.ai_assistant = AIAssistant(self)
        # To update icon within toolbar before dialog
        self.create_icons_toolbar(refresh=True)
        # Run dialog
        self.ai_assistant.exec()
        # Unset dialog var
        self.ai_assistant = None
        # To update icon within toolbar after dialog
        self.create_icons_toolbar(refresh=True)

    def action_settings(self):
        """
        Settings.
        """

        if self.debug:
            self.logger.debug('Settings dialog')

        settings = SettingsDialog(self)
        settings.exec()

    def action_check_for_updates(self) -> None:
        """
        Check the App updates here.
        """

        if self.debug:
            self.logger.debug('Checking for updates...')

        update_helper = UpdateHelper()
        update_helper.new_version_check_response.connect(self.check_for_updates_handler)
        update_helper.check_for_updates()

    def check_for_updates_handler(self, res_json: dict):
        # Show popup with update data
        if 'status' in res_json and 'msg' in res_json:
            self.message_box(res_json['msg'], icon_type=(1 if res_json['status'] == UpdateHelper.STATUS_OK else 2))
        else:
            if self.logging:
                self.logger.warning('Check for update response data in a wrong format')

    def action_bug_report(self) -> None:
        """
        Send bug report here.
        Or, redirect to the repository's page to create a task.
        """

        if self.debug:
            self.logger.debug('Sending bug report...')

        url = AppConfig.get_repository_github_bug_report_url()

        self.common_dialog(
            self.lexemes.get('dialog_open_link_title'),
            self.lexemes.get(name='dialog_open_link_text', url=url),
                # Open url with system browser
                callback=lambda dialog_callback:
                # Open link in a system browser and run dialog's callback
                (QDesktopServices.openUrl(url), dialog_callback()))

    def action_about(self) -> None:
        """
        Show about the App info.
        """

        if self.debug:
            self.logger.debug('About the App dialog')

        about = AboutPopup(self)
        about.exec()

    def action_exit(self) -> None:
        """
        Action: Exit from the app.
        """
        # Save any unsaved changes, keep content in place in case of pending tasks
        self.save_active_file(clear_after=False)

        if self.debug:
            self.logger.debug('Exiting...')

        # Correct way, to allow closeEvent() work, do not use sys.exit(0)
        self.close()

    def action_nav_select_file(self, index) -> None:
        """
        Action: Open file selected from the tree view.
        """

        # Save any unsaved changes
        self.save_active_file(clear_after=True)

        """
        Get file path by index:
            file_path = self.file_model.filePath(index)  # no proxy model
        Also, the file path can be obtained like this:
            file_path = self.tree_view.model().filePath(index)
        * https://doc.qt.io/qt-6/qsortfilterproxymodel.html#mapToSource
        """
        source_index = self.tree_proxy_model.mapToSource(index)
        file_path = self.file_model.filePath(source_index)
        if self.debug:
            self.logger.debug('Opening file path "%s"' % file_path)

        if not os.path.exists(file_path):
            if self.logging:
                self.logger.warning('Path selected within the tree is not found!')
            return

        if os.path.isfile(file_path):
            # Reset stored cursor values within settings
            self.reset_settings_cursor_pos()
            # Load file content
            self.load_file(file_path)
        if os.path.isdir(file_path):
            if self.debug:
                self.logger.debug("Dir selected within the tree '%s'" % file_path)
            self.set_current_path(file_path)

    def load_content(self, header: FileHeader, content: str) -> None:
        """
        Helper: Load content either into VIEW or EDIT areas.
        """

        # Set loader cursor whilst loading content
        # More cursor variants https://doc.qt.io/qt-6/qcursor.html#a-note-for-x11-users
        self.setCursor(Qt.CursorShape.WaitCursor)

        # Store current state
        self.content = content
        self.header = header
        # Update content size label
        if hasattr(self, 'statusbar'):
            self.statusbar['data_size_label'].setText("%s" % size_f(len(self.content)))
        if self.get_mode() == Mode.EDIT:
            self.load_content_edit(self.header, self.content)
            # Restore cursor applied later upon document 'content_set' event
        elif self.get_mode() == Mode.VIEW:
            self.load_content_html(self.header, self.content)
            # Restore viewport applied later upon document 'content_set' event
        elif self.get_mode() == Mode.SOURCE:
            self.load_source()
        else:
            if self.logging:
                self.logger.warning('Unrecognized mode %s' % self.get_mode())

        # Set cursor back
        self.setCursor(Qt.CursorShape.ArrowCursor)

    def load_file(self, file_path: str) -> bool:
        """
        Helper: Load content of the file.
        """

        # Current file path and a new one can be the same but the MODE can differ
        current_file_path = self.get_current_path()
        # Update the tree and related indexes
        self.set_current_path(file_path)

        if current_file_path is not None and file_path != current_file_path:
            # Highlight the file to switch from
            in_transit_color = self.theme_helper.get_color('main_tree_file_highlighted_in_transit', True)
            self.file_model.highlight(self.file_model.index(current_file_path), os.path.basename(current_file_path),
                                      color=in_transit_color)

        # Check is file encrypted
        if self.is_file_encrypted(file_path):
            file_header, file_body = FileHeader().load_file(file_path)
            # Check file header contains salt and the other params. May update migration params.
            # Only if the file is encrypted!
            try:
                file_header.validate_enc()
            except Exception as e:
                if self.logging:
                    self.logger.error('File header cannot be validated "%s"' % e)
            # File specific salt should be set within encrypted file
            file_salt = file_header.get_enc_param('slt')
            file_iterations = int(file_header.get_enc_param('itr'))

            try:
                decrypted_data = (
                    self.get_encrypt_helper(
                        salt=file_salt, hint=file_header.get_enc_param('hint'),
                        iterations=file_iterations).decrypt_data(file_body.encode("utf-8")))
                if decrypted_data:
                    file_body = decrypted_data.decode("utf-8")
                    self.set_encryption(Encryption.ENCRYPTED)
                else:
                    if self.logging:
                        self.logger.info('Cannot decrypt file "%s"' % file_path)
                    """
                    * https://docs.python.org/3/reference/compound_stmts.html#the-try-statement
                    """
                    raise InvalidToken
                # Reset encryption password dialogue count
                self.enc_password_dialog_cnt = 0
            except (InvalidToken, InvalidSignature, TypeError):
                if self.debug:
                    self.logger.debug('Cannot apply encryption password!')
                # Setup file's cursor position to a very beginning
                self.settings.line_num = 0
                self.settings.col_num = 0
                # If currently opened file is encrypted then offer to change the password
                if self.get_encryption() == Encryption.ENCRYPTED:
                    if self.debug:
                        self.logger.debug('Wrong encryption password but another encrypted file is opened')
                    if self.enc_password is not None:
                        # Show other file password mismatch message
                        self.message_box(self.lexemes.get('load_file_encryption_password_mismatch'), icon_type=2)
                        # If password not matched N-times, load default page then
                        if self.get_enc_password_dialog_cnt() >= 3:
                            # Reset encryption helper
                            self.reset_encrypt_helper()
                            # Reset encryption password dialogue count
                            self.enc_password_dialog_cnt = 0
                            # Mind possible recursion
                            return self.load_default_page(ignore_settings=True)
                        elif self.get_enc_password_dialog_cnt() > 0:
                            # Do not ask confirmation to reset the password as it has been confirmed already
                            self.reset_encrypt_helper()
                        else:
                            """
                            Ask to reset current password that in use by currently opened file.
                            Try to load the file by switch to it if the encryption password has been reset.
                            """
                            self.enc_password_reset_dialog()
                    else:
                        """
                        If no password set.
                        Remove saved start up page from settings
                        """
                        # Mind possible recursion
                        return self.load_default_page(ignore_settings=True)

                    if current_file_path is not None:
                        self.set_current_path(current_file_path)

                    # Try to re-load file if encryption password has been reset
                    if self.enc_password is None:
                        # Try to re-load file after encryption password reset
                        if file_path != current_file_path:
                            return self.load_file(file_path)
                # Show error message and reset password only if the password set
                elif self.enc_password is not None:
                    # Reset encryption helper and password
                    self.reset_encrypt_helper()
                    # Show file password mismatch message
                    self.message_box(self.lexemes.get('load_file_encryption_password_incorrect'), icon_type=3)
                    # If password not matched N-times, load default page then
                    if self.get_enc_password_dialog_cnt() >= 3:
                        # Reset encryption password dialogue count
                        self.enc_password_dialog_cnt = 0
                        # Mind possible recursion
                        return self.load_default_page(ignore_settings=True)
                    # Revert back the tree index if one was set previously
                    if (current_file_path is not None
                            # To avoid cycle between encrypted files when trying to return to a prev file
                            # with an empty password
                            and not self.is_file_encrypted(current_file_path)):
                        self.set_current_path(current_file_path)
                        # Try to re-load file after encryption password reset
                        if file_path != current_file_path:
                            return self.load_file(file_path)
                    else:
                        # Mind possible recursion
                        return self.load_default_page(ignore_settings=True)
                else:
                    self.reset_encrypt_helper() # Reset encryption helper and password
                    if self.debug:
                        self.logger.debug('Do nothing with the wrong password but check the loaded page')
                    """
                    Just to be sure the editor is not started on encrypted file
                    with cancelled password dialog on very beginning, or without any default file.
                    Revert back the tree index if one was set previously.
                    """
                    if (current_file_path is not None
                            # To avoid cycling between encrypted files when trying to return to a prev file
                            # with no or empty password.
                            and not self.is_file_encrypted(current_file_path)):
                        return self.load_file(current_file_path)
                    else:
                        # Mind possible recursion
                        return self.load_default_page(ignore_settings=True)

                if current_file_path is not None:
                    # Remove highlighted background
                    default_color = self.theme_helper.get_color('main_tree_background', True)
                    self.file_model.highlight(self.file_model.index(current_file_path),
                                              os.path.basename(current_file_path), color=default_color)

                return False
        # File is not encrypted
        else:
            # Load the file as usual
            file_header, file_body = FileHeader().load_file(file_path)

        # Load fields content
        if file_body is not None:  # There should be no valid situation with file_body equal to None
            self.load_content(file_header, file_body)
        else:
            self.message_box(self.lexemes.get('load_file_none_content_error'), icon_type=2)
            return False

        # Confirm current file path is set
        self.confirm_current_path()

        if current_file_path is not None:
            # Highlight the file was switched from
            prev_opened_color = self.theme_helper.get_color('main_tree_file_highlighted_prev_opened', True)
            self.file_model.highlight(self.file_model.index(current_file_path), os.path.basename(current_file_path),
                                      color=prev_opened_color)

        return True

    def is_file_encrypted(self, file_path: str) -> bool:
        """
        Check whether the file is encrypted.

        Previous approach was as simple as:
        True if file_path[-4:] == '.enc' else False
        """
        file_header, _ = FileHeader().load_file(file_path)
        return file_header.is_file_encrypted()

    def search_text(self) -> None:
        """
        Search text in the content view.
        If any text selected and Ctrl + F pressed autofill the search field with it.
        """
        if self.get_mode() == Mode.EDIT:
            # Edit widget
            edit_widget = self.get_edit_widget()  # type: Union[EditWidget, QPlainTextEdit]
            selected_text = edit_widget.textCursor().selectedText()
        else:
            # View widget
            view_widget = self.get_view_widget()  # type: Union[ViewWidget, QTextBrowser]
            selected_text = view_widget.textCursor().selectedText()

        if self.debug:
            self.logger.debug('Searching text "%s"' % selected_text)

        self.search_input.setText(selected_text)
        self.search_input.setFocus()
        self.action_search_next()

    def reload_active_file(self) -> None:
        """
        Re-load current file's content.
        Save any unsaved changes before calling this file reload method!
        """
        current_file_path = self.get_current_path()

        if self.debug:
            self.logger.debug('Re-loading current file content "%s"' % current_file_path)

        self.load_file(current_file_path)

    def auto_save_file(self, file_path: str = None) -> None:
        """
        Helper: Entry point to check and auto save file.
        """
        if self.debug:
            self.logger.debug('Check auto save possibility for the file "%s"' % file_path)

        self.action_save_file(file_path)

    def save_file_content(self, file_path: str, content: str) -> bool:
        """
        Helper: Save file content.
        """
        if self.debug:
            self.logger.debug('Saving file "%s"' % file_path)

        return save_file(file_path, content)

    def save_active_file(self, clear_after: bool = False, allow_save_empty_content: bool = None) -> None:
        """
        Helper: Save currently opened file.
        @param clear_after: bool, clear edit field after saving (when applicable, say switching view mode)
        @param allow_save_empty_content: bool, dialog answer of either to allow to save an empty file or not
        @return: None
        """

        # Save cursor position (line count starts from 0)
        self.store_doc_cursor_pos(self.get_mode())
        # Get current file path
        current_file_path = self.get_current_path()

        if self.get_mode() != Mode.EDIT:
            # Nothing to save
            if self.debug:
                self.logger.debug('Nothing to save in a non-edit mode')
            return

        # The dialog about empty content was shown at least once
        if allow_save_empty_content is not None:
            self.estate.allow_save_empty = allow_save_empty_content

        if self.debug:
            self.logger.debug(f"Save active file '{current_file_path}' (clear field after: '{clear_after}')")

        with open(current_file_path, 'r', encoding='utf-8') as file:
            # Edit widget
            edit_widget = self.get_edit_widget()  # type: Union[EditWidget, QPlainTextEdit]
            file_content = edit_widget.toPlainText()

            # If new content is empty ask confirmation to be sure
            if (not file_content
                    # Previous content not the same as a current one
                    and self.content != file_content
                    # Allow empty content dialog not answered
                    and (self.estate.allow_save_empty is None)):
                # Set this globally to avoid a lot of annoying dialogs
                self.estate.allow_save_empty = False
                # Dialog with a callback back to the file and closing dialog sub-callback
                self.common_dialog(
                    self.lexemes.get('dialog_save_empty_file_title'),
                    self.lexemes.get('dialog_save_empty_file_text'),
                    callback=lambda dialog_callback:
                        (self.save_active_file(clear_after=clear_after, allow_save_empty_content=True),
                         # Close dialog sub-callback
                         dialog_callback()))

            # Save if any changes
            if (file_content or self.estate.allow_save_empty) and self.content != file_content:
                # Show saving progress in the status bar
                if hasattr(self, 'statusbar'):
                    self.statusbar['save_progress_label'].setVisible(True)
                # Grayscale save button(s) at the toolbar
                if hasattr(self, 'toolbar_save_button'):
                    self.toolbar_save_button.setDisabled(True)

                    def restore_saving_ui_state() -> None:
                        if hasattr(self, 'statusbar'):
                            self.statusbar['save_progress_label'].setVisible(False)
                        # Keep it switched off to explicitly show the nothing to save state
                        # self.toolbar_save_button.setEnabled(True)
                    # Restore saving UI state automatically.
                    QTimer.singleShot(1500, restore_saving_ui_state)

                if self.header is None or not self.header.is_valid():
                    # Get empty file header here, it's needed for compatibility and will not be applied to the file
                    header = FileHeader()
                    if self.logging:
                        self.logger.info('File "%s" has no header info' % current_file_path)
                else:
                    header = self.header

                # Update the header with a new date
                header.refresh()

                # To keep initial content unencrypted
                content = file_content
                if self.get_encryption() == Encryption.ENCRYPTED:
                    # Check file header contains salt and the other params. May update migration params.
                    # Only if the file is encrypted!
                    try:
                        header.validate_enc()
                    except Exception as e:
                        if self.logging:
                            self.logger.error('File header cannot be validated "%s"' % e)
                    # Get file specific salt
                    file_salt = header.get_enc_param('slt')
                    file_iterations = int(header.get_enc_param('itr'))

                    # Encrypt
                    encrypted_content_b = self.get_encrypt_helper(
                        salt=file_salt, iterations=file_iterations).encrypt_data(content.encode("utf-8"))
                    if encrypted_content_b:
                        content = encrypted_content_b.decode("utf-8")

                content = header.pack(content)
                save_result = self.save_file_content(current_file_path, content)

                if save_result:
                    self.header = header
                    self.content = file_content
                    # Clear field's data
                    if clear_after:
                        edit_widget.clear()
                else:
                    self.message_box(self.lexemes.get('save_active_file_error_occurred'), icon_type=2)

            # Grayscale save button at the toolbar
            if hasattr(self, 'toolbar_save_button'):
                self.toolbar_save_button.setDisabled(True)

    def toggle_mode(self) -> None:
        """
        Helper: Switch between VIEW and EDIT modes to maintain actual state.
        """
        self.estate.toggle_mode()

    def set_mode(self, mode: Mode) -> None:
        """
        Setter: Set an actual mode (VIEW, EDIT, SOURCE, etc.)
        """
        self.estate.mode = mode

    def get_mode(self) -> Any:
        """
        Getter: Get an actual mode.
        """
        return self.estate.mode

    def get_prev_mode(self) -> Any:
        """
        Getter: Get a previous mode.
        """
        return self.estate.prev_mode

    def set_source(self, source: Source) -> None:
        """
        Setter: Set an actual source type (HTML, MARKDOWN, etc.)
        """
        self.estate.source = source

    def get_source(self) -> Any:
        """
        Getter: Get an actual source type.
        """
        return self.estate.source

    def get_prev_source(self) -> Any:
        """
        Getter: Get a previous source.
        """
        return self.estate.prev_source

    def set_encryption(self, encryption: Encryption) -> None:
        """
        Setter: Set an actual encryption state type (PLAIN, ENCRYPTED, etc.)
        """
        self.estate.encryption = encryption

    def get_encryption(self) -> Any:
        """
        Getter: Get an actual encryption state.
        """
        return self.estate.encryption

    def load_default_page(self, ignore_settings: bool = False) -> bool:
        """
        Helper: Default page when nothing else to show.
        """
        if (not ignore_settings
                and self.settings.file_path is not None
                and os.path.isfile(self.settings.file_path)):
            file_path = self.settings.file_path
        else:
            # Default file to open
            file_path = res_path('README.md')
        # If no file exist then try to load any file
        if file_path is not None and not os.path.isfile(file_path):
            file_path = self.get_any_file()
        if file_path is not None:
            return self.load_file(file_path)
        # The last fallback is try to create a new empty file
        return self.action_new_file()

    def load_content_html(self, header: FileHeader, content: str) -> None:
        """
        Load and setup content fields for VIEW mode
        """

        # View widget
        view_widget = self.get_view_widget()  # type: Union[ViewWidget, QTextBrowser]
        # View document
        view_doc = self.get_view_doc()  # type: QTextDocument

        # Set maximum page width to avoid long horizontal scrolls (check scaling)
        max_width = view_widget.frameGeometry().width()
        # CSS data
        css_data = 'body { max-width: %dpx; }' % max_width

        # Get file specific title if set
        title = header.get_param('title')
        if title:
            view_doc.setMetaInformation(QTextDocument.MetaInformation.DocumentTitle, title)
        # Set either default or extended title
        self.set_app_title(title)

        # Additional steps to make sure extensions work as expected
        if hasattr(self, 'md') and self.md:
            try:
                """
                Unregistering is not necessary when extension can be reset.
                self.md.postprocessors.deregister(name='footnote')
                self.md.inlinePatterns.deregister('footnote')
                """
                for _ext in self.md.registeredExtensions:
                    if _ext and 'FootnoteExtension' in str(_ext):
                        # Without this the extension tends to keep footnotes across the various notes
                        _ext.reset()
                        # To remove use: self.md.registeredExtensions.remove(_ext)
                        if self.debug:
                            self.logger.debug('Resetting extension "%s"' % _ext)
                        break
            except ValueError as e:
                if self.logging:
                    self.logger.warning('Extension error', e)

        """
        Convert data to html
        """
        html_data = self.convert_markdown_to_html(content)
        """
        Process raw content to modify it before any extra elements are being added to.
        """
        view_doc.setPlainText(html_data)  # This will set cursor position to the end of the content
        view_processor = ViewProcessor(highlighter=self.view_highlighter)
        # Connecting view's mouse press event to the view processor's method
        view_widget.mousePressEvent = view_processor.mouse_click_event
        # Processing changes of the document passed within
        view_processor.process()

        """
        There is also possible to update QTextEdit with html:
        view_widget.setHtml(HTML_TPL % (title, css_data, updated_doc.toHtml()))
        Or update and set up document itself:
        view_widget.setDocument(updated_doc)
        """
        view_doc.setHtml(HTML_TPL % (title, css_data, view_doc.toPlainText()))

        """
        View decorator to modify result text.
        Highlighter object holds the document and may pass it through indirectly.
        """
        vew_decorator = ViewDecorator(highlighter=self.view_highlighter)
        # Processing changes of the document passed within
        vew_decorator.process()

        # Set or restore cursor position here. View processors above should preserve the cursor state.
        cursor = view_widget.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Start)  # Or just: cursor.setPosition(0)
        view_widget.setTextCursor(cursor)

    def load_content_edit(self, header: FileHeader, content: str) -> None:
        """
        Load and setup content fields for EDIT mode.
        Keep in mind: document's content re-highlighting happens by event, e.g. at on_modification_changed()
        """

        # Edit widget
        edit_widget = self.get_edit_widget()  # type: Union[EditWidget, QPlainTextEdit]
        edit_widget.setReadOnly(True)

        # Get file specific title if set
        title = header.get_param('title')
        if title:
            edit_widget.document().setMetaInformation(QTextDocument.MetaInformation.DocumentTitle, title)
        # Set either default or extended title
        self.set_app_title(title)

        """
        Set content as an editable plain text
        More info about QPlainTextEdit and setPlainText() method https://doc.qt.io/qt-6/qplaintextedit.html#setPlainText
        """
        edit_widget.setPlainText(content)
        edit_widget.setReadOnly(False)

        # After resizing data updates
        self.line_numbers.update_numbers()

    def get_first_visible_block(self, view_widget: QTextBrowser) -> Union[QTextBlock, None]:
        cursor = view_widget.cursorForPosition(view_widget.viewport().rect().topLeft())
        cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
        return cursor.block()

    def store_doc_cursor_pos(self, mode: Mode) -> None:
        """
        Store cursor position for either modes.
        Explicitly pass mode as self.get_mode() may contain recently changed value.
        @param mode: Mode
        @return: None
        """
        if mode == Mode.EDIT:
            # Save cursor position (line count starts from 0)
            self.settings.line_num = self.line_num
            self.settings.col_num = self.col_num
            if self.debug:
                self.logger.debug('Storing document cursor position %d x %d ' % (self.line_num, self.col_num))
        else:
            # View widget
            view_widget = self.get_view_widget()  # type: Union[ViewWidget, QTextBrowser]
            self.settings.cursor_pos = self.cursor_pos
            self.settings.viewport_pos = [view_widget.horizontalScrollBar().value(),
                                          view_widget.verticalScrollBar().value()]

    def restore_doc_cursor_pos(self, mode: Mode, source_widget: Union[QPlainTextEdit, QTextBrowser]):
        """
        Move cursor to stored position or defaults.
        Make sure the method called once on startup or cursor will be moved again.
        """

        if mode == Mode.EDIT:
            text_cursor = source_widget.textCursor()
            text_cursor.setPosition(0)
            if self.debug:
                self.logger.debug('Restoring document cursor position %d x %d'
                                  % (self.settings.line_num, self.settings.col_num))
            # Move down to the desired line number (assuming line numbers start from 0)
            for _ in range(self.settings.line_num):
                if not text_cursor.movePosition(QTextCursor.MoveOperation.Down, QTextCursor.MoveMode.MoveAnchor):
                    # Break if the end of the document is reached
                    break
            text_cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.MoveAnchor,
                                     self.settings.col_num)
            source_widget.setTextCursor(text_cursor)
            source_widget.ensureCursorVisible()
        else:
            # Restore saved viewport scroll position
            if self.settings.viewport_pos:
                text_cursor = source_widget.textCursor()
                if 0 <= self.settings.cursor_pos <= len(source_widget.toPlainText()):
                    text_cursor.setPosition(self.settings.cursor_pos)
                else:
                    # This may happen if the position has been stored after collapsible blocks were expanded
                    if self.debug:
                        self.logger.debug("Cursor's setPosition(%d) is out of range" % self.settings.cursor_pos)
                source_widget.setTextCursor(text_cursor)
                if isinstance(self.settings.viewport_pos, list) and len(self.settings.viewport_pos) == 2:
                    _h, _v = self.settings.viewport_pos
                    source_widget.horizontalScrollBar().setValue(int(_h))
                    source_widget.verticalScrollBar().setValue(int(_v))

    def reset_settings_cursor_pos(self):
        self.settings.line_num = 0
        self.settings.col_num = 0
        self.settings.cursor_pos = 0
        self.settings.viewport_pos = [0, 0]

    def action_search_on(self) -> None:
        """
        Search: Started; related actions.
        Could be called upon input field's textChanged event.
        """
        text = self.search_input.text()

        if len(text) > 0:
            self.btn_search_clear.setEnabled(True)
            self.btn_search_next.setEnabled(True)
            self.btn_search_prev.setEnabled(True)
        else:
            self.action_search_clear()

    def action_search_off(self) -> None:
        """
        Search: Stopped; related actions.
        Could be called upon search clear action which could be called upon input field's 'textChanged' event
        in their turn.
        """
        self.btn_search_clear.setEnabled(False)
        self.btn_search_next.setEnabled(False)
        self.btn_search_prev.setEnabled(False)

    def action_search_clear(self) -> None:
        """
        Search field set to an empty text and reset the search state.
        """
        self.search_input.setText('')
        # Case-sensitive checkbox
        self.search_match_case.setCheckState(Qt.CheckState.Unchecked)
        # Reset buttons state
        self.action_search_off()
        # Get source of the search
        if self.get_mode() == Mode.EDIT:
            # Edit widget
            edit_widget = self.get_edit_widget()  # type: Union[EditWidget, QPlainTextEdit]
            search_source = edit_widget
        else:
            # View widget
            view_widget = self.get_view_widget()  # type: Union[ViewWidget, QTextBrowser]
            # Mode.VIEW | Mode.SOURCE
            search_source = view_widget
        """
        Start over again if not matches in this direction.
        Be careful with cursor position set as it may affect initial load of the document with editor_state_update_handler().
        This code may replace stored viewport or cursor positions, so avoid it here:
        search_source.moveCursor(QTextCursor.MoveOperation.Start)
        """
        search_source.find('')  # Search a void

    def action_search_prev(self) -> None:
        """
        Search: Previous occurrence of string in text (Backward search)
        * https://doc.qt.io/qt-6/qtextdocument.html#FindFlag-enum
        """
        text = self.search_input.text()
        check = self.search_match_case.isChecked()
        # Case-sensitive option
        if check:
            find_flags = (QTextDocument.FindFlag.FindBackward | QTextDocument.FindFlag.FindCaseSensitively)
        else:
            find_flags = QTextDocument.FindFlag.FindBackward
        # Find text with correct flags
        if self.get_mode() == Mode.EDIT:
            # Edit widget
            edit_widget = self.get_edit_widget()  # type: Union[EditWidget, QPlainTextEdit]
            search_source = edit_widget
        else:
            # View widget
            view_widget = self.get_view_widget()  # type: Union[ViewWidget, QTextBrowser]
            # Mode.VIEW | Mode.SOURCE
            search_source = view_widget
        # Apply search to the source
        res = search_source.find(text, find_flags)
        if self.debug:
            self.logger.debug('Search PREVIOUS result for "%s"', res)
        if not res:
            # Start over again if not matches in this direction
            search_source.moveCursor(QTextCursor.MoveOperation.End)
            search_source.find(text, find_flags)

    def action_search_next(self) -> None:
        """
        Search: Next occurrence of string in text (Forward search; Default)
        * https://doc.qt.io/qt-6/qtextdocument.html#FindFlag-enum
        """
        text = self.search_input.text()
        check = self.search_match_case.isChecked()
        # Case-sensitive option
        if check:
            find_flags = QTextDocument.FindFlag.FindCaseSensitively
        else:
            find_flags = QTextDocument.FindFlag(0)
        # Find text with correct flags
        if self.get_mode() == Mode.EDIT:
            # Edit widget
            edit_widget = self.get_edit_widget()  # type: Union[EditWidget, QPlainTextEdit]
            search_source = edit_widget
        else:
            # View widget
            view_widget = self.get_view_widget()  # type: Union[ViewWidget, QTextBrowser]
            # Mode.VIEW | Mode.SOURCE
            search_source = view_widget
        # Apply search to the source
        res = search_source.find(text, find_flags)
        if self.debug:
            self.logger.debug('Search NEXT result "%s"', res)
        if not res:
            # Start over again if not matches in this direction
            search_source.moveCursor(QTextCursor.MoveOperation.Start)
            search_source.find(text, find_flags)
