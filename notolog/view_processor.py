"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Document view processor to support additional modifications in the resulting text.
- Functionality: Supports expandable markdown blocks, such as <details> and <summary>.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import Qt, QUrl
from PySide6.QtWidgets import QTextBrowser
from PySide6.QtGui import QTextCursor, QSyntaxHighlighter, QTextCharFormat

import logging
import re
import base64

from typing import TYPE_CHECKING, Union

from .settings import Settings
from .highlight.view_highlighter import ViewHighlighter
from .lexemes.lexemes import Lexemes

if TYPE_CHECKING:
    from PySide6.QtCore import QObject  # noqa: F401


class ViewProcessor:
    """
    View mode pre-result procession by modifying loaded QTextDocument
    """

    zero_width_space = '\u200B'  # '&#8203;' or '​'

    def __init__(self, highlighter: Union[QSyntaxHighlighter, ViewHighlighter]):
        """
        Args:
            highlighter (Union[QSyntaxHighlighter, ViewHighlighter]):
            Highlighter that holds document to apply any modifications.
        """
        self.highlighter = highlighter
        self.doc = self.highlighter.document()

        self.settings = Settings()

        self.logger = logging.getLogger('view_processor')

        # Load lexemes for the selected language and scope
        self.lexemes = Lexemes(self.settings.app_language, default_scope='common')

        self.logger.debug('Characters count %d' % self.doc.characterCount())

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

    @staticmethod
    def replace_tags(content, replacements) -> str:
        """
        Function to perform replacements.

        Args:
            content (str): Source content.
            replacements (dict): Replacements mapping.
        """
        for pattern, replacement in replacements.items():
            content = re.sub(pattern, replacement, content)
        return content

    def pre_md_process(self, content: str):
        """
        Replaces expandable tokens from html-like to the meta-like,
        to avoid ignoring them upon markdown conversion.

        Args:
            content (str): Source content.

        Returns:
            str: Pre-processed content.
        """

        # Define the replacements in a dictionary with regex patterns
        forward_replacements = {
            r'<details([^>]*?)>': r'[details\1]',
            r'</details>': '[/details]',
            r'<summary([^>]*?)>': r'[summary\1]',
            r'</summary>': '[/summary]',
        }

        return self.replace_tags(content, forward_replacements)

    def post_md_process(self, content: str = None):
        """
        Revert the replacements of the expandable tokens from meta-like back to the html-like,
        to allow to recognize them upon html-rendering.

        Args:
            content (str, optional): Source content.

        Returns:
            str: Post-processed content.
        """

        # Whither to get the content from the doc or not
        doc_processing = True if content is None else False
        if doc_processing:
            content = self.doc.toPlainText()

        # Define the backward replacements in a dictionary
        backward_replacements = {
            r'\[details([^>]*?)\]': r'<details\1>',
            r'\[/details\]': '</details>',
            r'\[summary([^>]*?)\]': r'<summary\1>',
            r'\[/summary\]': '</summary>',
        }

        # Perform the replacements
        post_processed_text = self.replace_tags(content, backward_replacements)

        if doc_processing:
            self.doc.setPlainText(post_processed_text)

        return post_processed_text

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
                _open_start = match.start()
                _open_end = match.end()
                _open_length = _open_end - _open_start
                self.blocks_start.append((block.position() + _open_start, _open_length))
            pattern = r"</details>"
            # Find all matches of the pattern in provided string
            matches = re.finditer(pattern, block.text())
            for match in matches:
                _close_start = match.start()
                _close_end = match.end()
                _close_length = _close_end - _close_start
                self.blocks_end.append((block.position() + _close_start, _close_length))

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

        # Reset warning if exists
        self.doc.parent().statusbar.show_warning(visible=False)
        # Check open/close tokens match
        if len(self.blocks_start) != len(self.blocks_end):
            # Show error sign at status bar
            self.doc.parent().statusbar.show_warning(
                visible=True,
                tooltip=self.lexemes.get('expandable_block_open_close_tags_mismatch_warning'))

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

        self.logger.debug('Unsorted open-close mapping %s' % res)

        self.blocks = res

        if self.blocks:
            self.sort_blocks()
            self.collapse_blocks()

        # Restore original cursor position
        self.restore_cursor_pos()

    def sort_blocks(self):
        self.logger.debug('Sorting elements by group and nesting level...')

        self.blocks.sort(key=lambda x: x['o'] if 'o' in x and x['o'] is not None else 0)

        self.logger.debug('Sorted result of the open-close mapping %s' % self.blocks)

        group = 0
        for i, _data in enumerate(self.blocks):
            if not _data['l']:
                # Update group only for each root element
                group = i
                self.blocks[i].update({'g': group})
            # Iterate through remaining elements to find possible nesting
            for j, _other_data in enumerate(self.blocks[i + 1:], start=i + 1):
                if _data['o'] is None or _other_data['o'] is None or _data['c'] is None or _other_data['c'] is None:
                    # Show error sign at status bar
                    self.doc.parent().statusbar.show_warning(
                        visible=True,
                        tooltip=self.lexemes.get('expandable_block_open_close_tags_mismatch_warning'))
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

        self.logger.debug('Final result of the open-close mapping with nesting value %s' % self.blocks)

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

            If the previous nesting level is the same as a current one re-write the length correction then.
            """
            replacement_text_lengths[prev_level] = replacement_text_len

            if pair['o'] is None or pair['c'] is None:
                self.logger.debug('Notice: Incomplete open/close tag data %s' % pair)
                return

            """
            The most nested blocks being processed first, thus the close token correction,
            as the open token doesn't change its position.
            """
            pos_open = pair['o']
            pos_close = (pair['c'] + pair['cl']  # text + closing token together to get the very end of the text
                         # Combined length correction of all nested elements inside (previous level), say each ones:
                         # [0]...[1][2][/2][/1]...[1][/1]...[/0]
                         + (replacement_text_lengths[prev_level] if pos_level == 0
                            # Replacements on the same level shouldn't interfere each other
                            else (replacement_text_len if pos_level != prev_level else 0)))

            self.logger.debug('Cursor position open: %d, close: %d, level: %d ' % (pos_open, pos_close, pos_level))

            cursor.setPosition(pos_open)
            cursor.setPosition(pos_close, QTextCursor.MoveMode.KeepAnchor)
            selected_text = cursor.selectedText()
            if selected_text:
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
                # Post-processing converts meta-like tokens '[details]' back to their HTML-like equivalents '<details>'
                # before the actual encoding process.
                selected_text = self.post_md_process(selected_text)
                encoded_text = base64.b64encode(selected_text.encode('utf-8'))
                encoded_summary = base64.b64encode(summary.encode('utf-8'))
                """
                Insert as a TEXT here, not as an HTML or tags will be stripped after.
                Place extra spaces on each side to allow smooth anchor detection upon click.

                Note:
                    - Do not use id="..." it makes anchor detection unstable, use data attributes instead.
                    - Avoid using <div> as it produces extra <p> after conversion.
                """
                replacement_text = ('<p class="_ds_expand">{}'
                                    # <a>...</a> will be replaced with a table upon a click
                                    # zero-width space before expandable anchor to prevent never-ending anchor sequence
                                    '<a href="expandable:{}#{}" data-group="{}" data-level="{}">'
                                    '<span class="_ds_expand_pointer">▼</span>&nbsp;{}</a>'
                                    '</p>'
                                    .format(self.zero_width_space, encoded_text.decode('utf-8'),
                                            encoded_summary.decode('utf-8'), pos_group, pos_level, summary))
                replacement_text_len += len(replacement_text) - (pos_close - pos_open)
                cursor.insertText(replacement_text)
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
                return self.expandable_click_event(QUrl(anchor), cursor)
            elif anchor.startswith('collapsible'):
                return self.collapsible_click_event(QUrl(anchor), cursor)
            else:
                # cursor.select(QTextCursor.SelectionType.WordUnderCursor)
                # text = cursor.selectedText()
                # self.logger.debug(f'Click context: {text}')

                cursor.clearSelection()
                parent_widget.setTextCursor(cursor)

    def process_anchor_label(self, cursor):
        # Start from the clicked position
        cursor.select(QTextCursor.SelectionType.WordUnderCursor)

        self.logger.debug('Cursor data, pos: %d, anchor: %s, text: %s'
                          % (cursor.position(), cursor.anchor(), cursor.selectedText()))

        i = 0
        # Move to the anchor caption's start position
        prev_pos = cursor.position()
        while (cursor.charFormat().isAnchor()
               and (i := i + 1)
               # Ensure that zero-width spaces are not affected.
               and cursor.document().characterAt(cursor.position() - 1) != self.zero_width_space):
            cursor.movePosition(QTextCursor.MoveOperation.PreviousCharacter, QTextCursor.MoveMode.MoveAnchor)
            # Check the cursor position is changing
            if prev_pos == cursor.position():
                break
            prev_pos = cursor.position()

        # Move to the anchor caption's end position
        prev_pos = cursor.position()
        # 0 if the mouse is clicked on the very first character '​▼'
        while ((i >= 0 or cursor.charFormat().isAnchor())
               and cursor.document().characterAt(cursor.position() + 1) != self.zero_width_space):
            i -= 1
            cursor.movePosition(QTextCursor.MoveOperation.NextCharacter, QTextCursor.MoveMode.KeepAnchor)
            # Check the cursor position is changing
            if cursor.atBlockEnd() or prev_pos == cursor.position():
                break
            prev_pos = cursor.position()

        # Remove all trailing spaces and save the cursor position
        pre_cursor_char = cursor.document().characterAt(cursor.position() - 1)
        pattern = r"([\s]+)"
        match = re.search(pattern, pre_cursor_char, flags=re.DOTALL | re.UNICODE)
        if match and match.group(1):
            j = 0
            while j < len(match.group(1)):
                cursor.movePosition(QTextCursor.MoveOperation.PreviousCharacter, QTextCursor.MoveMode.KeepAnchor)
                j += 1

        self.logger.debug(f'Anchor summary text: "{cursor.selectedText()}"')

        cursor.removeSelectedText()

        return cursor

    def expandable_click_event(self, url: QUrl, cursor: QTextCursor):
        # cursor.charFormat().anchorHref()
        self.logger.debug('Expandable anchor clicked, scheme: %s, path: %s, fragment: %s'
                          % (url.scheme(), url.path(), url.fragment()))

        # This may cause left-right click issue when either the start or end position of token is clicked
        # cursor.movePosition(QTextCursor.MoveOperation.PreviousCharacter, QTextCursor.MoveMode.KeepAnchor)

        cursor = self.process_anchor_label(cursor)
        # start_pos = cursor.position()

        encoded_text = url.path()
        self.logger.debug('Text to decode: {%s}', encoded_text)

        decoded_text = (base64.b64decode(encoded_text.encode('utf-8'))
                        .decode('utf-8')
                        .strip())

        encoded_summary = url.fragment()
        self.logger.debug('Summary to decode: {%s}', encoded_summary)
        decoded_summary = (base64.b64decode(encoded_summary.encode('utf-8'))
                           .decode('utf-8')
                           .strip())

        self.logger.debug('Decoded text: {%s}' % decoded_text)

        # Set default format for inserted text
        default_format = QTextCharFormat()
        cursor.setCharFormat(default_format)
        """
        - Insert decoded text, new line either "\n" or "<br/>" depending on insertText() or insertHtml() correspondingly.
        - Allow extra space as space symbols could be stripped during conversion.
        - Avoiding invisible separator allows the whole block to be an anchor and being replaced at once.
        """
        collapsible_html = ('<table class="_n_details _ds_collapse">'
                            '<tr><th class="_n_details_summary">'
                            '<a href="collapsible:{}#{}" class="_ds_collapse_summary">'
                            '<span class="_ds_collapse_pointer">▲</span>&nbsp;{}</a></th></tr>'
                            '<tr><td class="_n_details_content">{}</td></tr>'
                            '</table>').format(encoded_text, encoded_summary, decoded_summary, decoded_text)
        cursor.insertHtml(collapsible_html)

        # The table's (<td>) tag and adjacent text are converted into a pseudo block,
        # enclosed between \uFDD0 and \uFDD1:
        # print(f'{ord(b'\xef\xb7\x90'.decode('utf-8')):04X}')  # \uFDD0
        # print(f'{ord(b'\xef\xb7\x91'.decode('utf-8')):04X}')  # \uFDD1
        # # The entire block above is processed as a single object:
        # cursor.setPosition(start_pos, QTextCursor.MoveMode.MoveAnchor)
        # cursor.movePosition(QTextCursor.MoveOperation.NextCharacter, QTextCursor.MoveMode.KeepAnchor)

    def collapsible_click_event(self, url: QUrl, cursor: QTextCursor):
        # cursor.charFormat().anchorHref()
        self.logger.debug('Collapsible anchor clicked, scheme: %s, path: %s' % (url.scheme(), url.path()))

        cursor = self.process_anchor_label(cursor)

        encoded_text = url.path()
        self.logger.debug('Text to decode: {%s}', encoded_text)

        encoded_summary = url.fragment()
        decoded_summary = (base64.b64decode(encoded_summary.encode('utf-8'))
                           .decode('utf-8')
                           .strip())

        # Set default format for inserted text
        default_format = QTextCharFormat()
        cursor.setCharFormat(default_format)

        cursor.insertHtml('<p class="_ds_expand">{}'
                          '<a href="expandable:{}#{}" data-group="{}" data-level="{}">'
                          '<span class="_ds_expand_pointer">▼</span>&nbsp;{}</a>'
                          '</p>'
                          # Group and level aren't set here as the blocks have been already rendered
                          .format(self.zero_width_space, encoded_text, encoded_summary, 0, 0, decoded_summary))
