from PySide6.QtCore import Qt, QObject, QUrl
from PySide6.QtWidgets import QTextBrowser
from PySide6.QtGui import QTextCursor, QSyntaxHighlighter, QTextCharFormat

import logging
import re
import base64

from typing import Union

from .settings import Settings
from .app_config import AppConfig
from .highlight.view_highlighter import ViewHighlighter
from .lexemes.lexemes import Lexemes


class ViewProcessor:
    """
    View mode pre-result procession by modifying loaded QTextDocument
    """

    def __init__(self, highlighter: Union[QSyntaxHighlighter, ViewHighlighter]):
        """
        Args:
            highlighter (Union[QSyntaxHighlighter, ViewHighlighter]):
            Highlighter that holds document to apply any modifications.
        """
        self.highlighter = highlighter
        self.doc = self.highlighter.document()

        self.logging = AppConfig().get_logging()
        self.debug = AppConfig().get_debug()

        self.settings = Settings()

        self.logger = logging.getLogger('view_processor')

        # Default language setup, change to settings value to modify it via UI
        self.lexemes = Lexemes(self.settings.app_language, default_scope='common')

        if self.debug:
            self.logger.info('Characters count %d' % self.doc.characterCount())

        self.blocks = []
        self.blocks_start = []
        self.blocks_end = []

        # self.doc.contentsChanged.connect(self.process)

        cursor = QTextCursor(self.doc)
        self.cursor_pos_orig = cursor.position()

    def restore_cursor_pos(self):
        cursor = QTextCursor(self.doc)
        # Restore original cursor position
        cursor.setPosition(self.cursor_pos_orig, QTextCursor.MoveMode.MoveAnchor)
        parent = self.doc.parent()  # type: QObject
        parent_widget = parent.get_view_widget()  # type: QTextBrowser
        parent_widget.setTextCursor(cursor)

    def process(self):
        self.blocks.clear()
        cursor = QTextCursor(self.doc)
        cursor.setPosition(0)

        def process_block(cursor_internal: QTextCursor) -> None:
            """
            Find open/close tokens in block.
            @param cursor_internal: active cursor
            @return: None
            """
            block = cursor_internal.block()
            pattern = r"<details.*?>"
            # Find all matches of the pattern in provided string
            matches = re.finditer(pattern, block.text())
            for match in matches:
                open_start = match.start()
                open_end = match.end()
                open_length = open_end - open_start
                self.blocks_start.append((block.position() + open_start, open_length))
            pattern = r"</details>"
            # Find all matches of the pattern in provided string
            matches = re.finditer(pattern, block.text())
            for match in matches:
                close_start = match.start()
                close_end = match.end()
                close_length = close_end - close_start
                self.blocks_end.append((block.position() + close_start, close_length))

        cursor.movePosition(QTextCursor.MoveOperation.Start)
        # Iterate through each block
        while not (cursor.atEnd()
                   # cursor.atEnd() not enough as the cursor unable to move next block at the very end
                   or (cursor.block().blockNumber() > 0
                       and cursor.block().blockNumber() == self.doc.blockCount() - 1)):
            # Process block
            process_block(cursor)
            # Move to the next block
            cursor.movePosition(QTextCursor.MoveOperation.NextBlock)

            # To avoid never ending cycle when only one block is available
            if self.doc.blockCount() == 1:
                break

        # Process block at the very end
        process_block(cursor)

        res = []
        self.blocks_start.reverse()
        # Enumerate by end token to find the closest start token
        for index, value in enumerate(self.blocks_end):
            close_start, close_length = value
            if index not in res:
                """
                Extra data allows independent processing of tokens and their content:
                o - open, start position
                ol - open length, start token length, say <details> length is 9
                c - close, close position
                cl - close length, close token length (the same approach as for open length)
                """
                res.insert(index, {'o': None, 'ol': None, 'c': close_start, 'cl': close_length, 'g': None, 'l': 0})
            # Enumerate start token list backward unsetting matched element
            for _index, _value in enumerate(self.blocks_start):
                open_start, open_length = _value
                if _value < value:
                    res[index].update({'o': open_start, 'ol': open_length})
                    del self.blocks_start[_index]
                    break

        if self.debug:
            self.logger.debug('Unsorted open-close mapping %s' % res)

        self.blocks = res

        if self.blocks:
            self.sort_blocks()
            self.collapse_blocks()

        # Restore original cursor position
        self.restore_cursor_pos()

    def sort_blocks(self):
        if self.debug:
            self.logger.debug('Sorting elements by group and nesting level...')

        self.blocks.sort(key=lambda x: x['o'] if 'o' in x and x['o'] is not None else 0)

        if self.debug:
            self.logger.info('Sorted result of the open-close mapping %s' % self.blocks)

        group = 0
        for i, _data in enumerate(self.blocks):
            if not _data['l']:
                # Update group only for each root element
                group = i
                self.blocks[i].update({'g': group})
            # Iterate through remaining elements to find possible nesting
            for j, _other_data in enumerate(self.blocks[i + 1:], start=i + 1):
                if _data['o'] is None or _other_data['o'] is None or _data['c'] is None or _other_data['c'] is None:
                    # TODO show error sign at status bar
                    return
                # Check if other element is nested within the current element
                if _data['o'] < _other_data['o'] and _data['c'] > _other_data['c']:
                    self.blocks[j].update({'l': (_data['l'] + 1 if 'l' in _data else 1), 'g': group})

        """
        Sort elements by:
        1. By group first (nested elements or singles)
        2. Nesting level (more means deeper nesting)
        3. Open token position (DESC order)
        """
        self.blocks.sort(key=lambda x: (-x['g'] if x['g'] is not None else 0,
                                        -x['l'] if x['l'] is not None else 0,
                                        -x['o'] if x['o'] is not None else 0))  # reverse=True

        if self.debug:
            self.logger.info('Final result of the open-close mapping with nesting value %s' % self.blocks)

    def collapse_blocks(self):
        cursor = QTextCursor(self.doc)
        # Keep prev states to check within a loop
        prev_group = None
        prev_level = 0
        replacement_text_len = 0
        replacement_text_lengths = {}
        for pair in self.blocks:
            """
            Blocks being processed in a particular order.
            The sorting applied at the end of the sort_blocks() method.
            """
            pos_group = pair['g']
            pos_level = pair['l']
            # When start processing another group of nested (or single) elements
            if pos_group != prev_group:
                prev_group = pos_group
                replacement_text_len = 0
                replacement_text_lengths = {}
            # Previous processed pair['l'] value have to be set
            if prev_level not in replacement_text_lengths:
                replacement_text_lengths[prev_level] = 0
            """
            Text has been replaced with a new one, different length. Include it in length calculation.
            The value is from the previous iteration but can be modified at this one if the conditions match.
            """
            replacement_text_lengths[prev_level] += replacement_text_len
            # If the previous nesting level is the same as a current one reset the length correction then
            if pos_level == prev_level:
                replacement_text_len = 0

            if pair['o'] is None or pair['c'] is None:
                if self.debug:
                    self.logger.warning('Error occurred! Incomplete open/close tag data %s' % pair)
                return

            """
            The most nested blocks being processed first, thus the close token correction,
            as the open token doesn't change its position.
            """
            pos_open = pair['o']
            pos_close = (pair['c'] + pair['cl']  # text + closing token together to get the very end of the text
                         # Combined length correction of all nested elements inside (previous level), say each ones:
                         # [0]...[1][2][/2][/1]...[1][/1]...[/0]
                         + (replacement_text_lengths[prev_level] if pos_level == 0 else replacement_text_len))

            if self.debug:
                self.logger.debug('Cursor position open: %d, close: %d, level: %d ' % (pos_open, pos_close, pos_level))

            cursor.setPosition(pos_open)
            cursor.setPosition(pos_close, QTextCursor.MoveMode.KeepAnchor)
            selected_text = cursor.selectedText()
            if selected_text:
                if self.debug:
                    self.logger.debug('Block text[%d][%d]: %s' % (pos_group, pos_level, selected_text))

                cursor.removeSelectedText()

                """
                Select extra space characters before and after to strip the cursor's text the way where the summary's
                content starts right after the details tag.
                """
                pattern = r"[\s]*?<summary.*?>(.*?)<\/summary>[\s]*?"
                match = re.search(pattern, selected_text, flags=re.DOTALL | re.MULTILINE | re.UNICODE)
                summary = self.lexemes.get('expandable_block_default_title')
                if match:
                    summary = f"{match.group(1).strip()}"
                    pos_open_summary = match.start()
                    pos_close_summary = match.end()
                    selected_text = selected_text[:pos_open_summary] + selected_text[pos_close_summary:]

                # There is a possible situation where the formatted html may become invalid.
                # Say, "<p>...\n<details> </p>\n\n<summary>".
                # That's because of markdown lib may process paragraph that way.
                # Double check it with a something like exp below, but keep in mind the open tag is also exists:
                # pattern = r"<details.*?>[\s]*?(</p>)"

                selected_text = selected_text.strip()
                encoded_text = base64.b64encode(selected_text.encode('utf-8'))
                """
                Insert as a TEXT here, not as an HTML or tags will be stripped after.
                Place extra spaces on each side to allow smooth anchor detection upon click.
                """
                # Do not use id="..." it makes anchor detection unstable, use data attributes instead
                replacement_text = ('<p class="_ds_expand">'
                                    # <a>...</a> will replaced with table upon click
                                    '<a href="expandable:{}" data-group="{}" data-level="{}">'
                                    '<span class="_ds_expand_pointer">▼</span>&nbsp;{}</a>'
                                    '</p>'
                                    .format(encoded_text.decode('utf-8'), pos_group, pos_level, summary))
                replacement_text_len += len(replacement_text) - (pos_close - pos_open)
                cursor.insertText(replacement_text)
                if self.debug:
                    self.logger.debug('Replacement text: %s' % replacement_text)

                # Save current group and level to check them over again within the next iteration.
                prev_group = pos_group
                prev_level = pos_level

    def mouse_click_event(self, event):
        parent = self.doc.parent()  # type: QObject
        parent_widget = parent.get_view_widget()  # type: QTextBrowser

        # Parent actions, like select text with a cursor
        QTextBrowser.mousePressEvent(parent_widget, event)

        cursor = parent_widget.cursorForPosition(event.pos())

        if event.button() == Qt.MouseButton.LeftButton:
            anchor = parent_widget.anchorAt(event.pos())
            if anchor.startswith('expandable'):
                return self.anchor_click_event(QUrl(anchor), cursor)
            elif anchor.startswith('collapsible'):
                # TODO collapsible block
                if self.debug:
                    self.logger.debug('Collapsible block clicked')
                pass
            else:
                if self.debug:
                    cursor.select(QTextCursor.SelectionType.WordUnderCursor)
                    text = cursor.selectedText()
                    self.logger.debug(f'Click context: {text}')

                cursor.clearSelection()
                parent_widget.setTextCursor(cursor)

    def anchor_click_event(self, url: QUrl, cursor: QTextCursor):
        if self.debug:
            # cursor.charFormat().anchorHref()
            self.logger.debug('Anchor clicked, scheme: %s, path: %s' % (url.scheme(), url.path()))

        # This may cause left-right click issue when either the start or end position of token is clicked
        # cursor.movePosition(QTextCursor.MoveOperation.PreviousCharacter, QTextCursor.MoveMode.KeepAnchor)

        cursor.select(QTextCursor.SelectionType.WordUnderCursor)

        if self.debug:
            self.logger.debug('Cursor data, pos: %d, anchor: %s, text: %s'
                              % (cursor.position(), cursor.anchor(), cursor.selectedText()))

        i = 0
        # Move to the anchor caption's start position
        while cursor.charFormat().isAnchor() and (i := i + 1):
            cursor.movePosition(QTextCursor.MoveOperation.PreviousCharacter, QTextCursor.MoveMode.MoveAnchor)
        # Move to the anchor caption's end position
        while i > 0 or cursor.charFormat().isAnchor():
            i -= 1
            cursor.movePosition(QTextCursor.MoveOperation.NextCharacter, QTextCursor.MoveMode.KeepAnchor)
            # Check it after, not in loop
            if cursor.atBlockEnd():
                break

        anchor_label = cursor.selectedText()
        if self.debug:
            self.logger.debug('Anchor text: %s' % anchor_label)

        cursor.removeSelectedText()
        to_decode = url.path()
        if self.debug:
            self.logger.debug('Text to decode: {%s}', to_decode)

        decoded_text = (base64.b64decode(to_decode.encode('utf-8'))
                        .decode('utf-8')
                        .strip())

        if self.debug:
            self.logger.debug('Decoded text: {%s}' % decoded_text)

        # Set default format for inserted text
        default_format = QTextCharFormat()
        cursor.setCharFormat(default_format)
        """
        Insert decoded text, new line either "\n" or "<br/>" depending on insertText() or insertHtml() correspondingly.
        Allow extra space as space symbols could be stripped during conversion.
        """
        cursor.insertHtml('<table class="_n_details">'
                          '<tr><td class="_n_details_summary"><span class="_ds_collapse">{}</span></td></tr>'
                          '<tr><td class="_n_details_content">{}</td></tr>'
                          '</table>'
                          # TODO make it collapsible with '▲'
                          .format(anchor_label.replace('▼', '≡').strip(), decoded_text))
