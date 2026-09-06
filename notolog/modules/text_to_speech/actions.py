"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Read-aloud actions for document and selection context menus.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

import re
from html import escape
from PySide6.QtGui import QColor, QTextCursor, QTextDocument, QTextFormat

from ...helpers.theme_helper import ThemeHelper
from .i18n import tr


def speech_action_icon(*, filled=False):
    theme = ThemeHelper()
    return theme.get_icon(theme_icon='volume-up-fill.svg' if filled else 'volume-up.svg',
                          color=QColor(theme.get_color('main_tree_context_menu_copy_file_path')))


def rendered_source(cursor):
    """Export viewer text and code semantics without Qt's font-based Markdown inference."""
    if not cursor.hasSelection():
        return ''
    document = QTextDocument()
    document.setDefaultFont(cursor.document().defaultFont())
    output = QTextCursor(document)
    output.insertFragment(cursor.selection())

    # Partial fragments can omit the first block's code properties.
    original = cursor.document().findBlock(cursor.selectionStart()).blockFormat()
    output.movePosition(QTextCursor.MoveOperation.Start)
    first = output.blockFormat()
    for key in (QTextFormat.Property.BlockNonBreakableLines, QTextFormat.Property.BlockCodeFence,
                QTextFormat.Property.BlockCodeLanguage):
        if original.hasProperty(key):
            first.setProperty(key, original.property(key))
    output.setBlockFormat(first)

    # Use explicit formats: resolving a default or missing font can otherwise turn
    # prose into Markdown code, or code into prose, depending on the platform.
    blocks = []
    in_code_block = False
    block = document.begin()
    while block.isValid():
        formatting = block.blockFormat()
        code_block = (formatting.nonBreakableLines() or formatting.hasProperty(QTextFormat.Property.BlockCodeFence)
                      or formatting.hasProperty(QTextFormat.Property.BlockCodeLanguage))
        heading = formatting.headingLevel()
        tag = 'pre' if code_block else (f'h{heading}' if 1 <= heading <= 6 else 'p')
        parts = []
        in_inline_code = False
        iterator = block.begin()
        while not iterator.atEnd():
            fragment = iterator.fragment()
            char_format = fragment.charFormat()
            text = (str(char_format.property(QTextFormat.Property.ImageAltText) or '')
                    if char_format.isImageFormat() else fragment.text())
            text = escape(text).replace('\u2028', '<br>')
            families = [name.casefold() for name in char_format.fontFamilies() or ()]
            inline_code = not code_block and (char_format.fontFixedPitch() or 'monospace' in families)
            if inline_code != in_inline_code:
                parts.append('<code>' if inline_code else '</code>')
                in_inline_code = inline_code
            parts.append(text)
            iterator += 1
        if in_inline_code:
            parts.append('</code>')
        if code_block:
            blocks.append('\n' if in_code_block else '<pre>')
            blocks.extend(parts)
        else:
            if in_code_block:
                blocks.append('</pre>')
            blocks.extend((f'<{tag}>', *parts, f'</{tag}>'))
        in_code_block = code_block
        block = block.next()
    if in_code_block:
        blocks.append('</pre>')
    return '<div>' + ''.join(blocks) + '</div>'


def selection_source(widget, *, rendered=False):
    cursor = widget.textCursor()
    if rendered:
        return rendered_source(cursor)
    source = cursor.selectedText()
    if not cursor.hasSelection():
        return source
    first = widget.document().findBlock(cursor.selectionStart())
    last = widget.document().findBlock(cursor.selectionEnd() - 1)
    first_fence = getattr(first.userData(), 'markdown_fence', None)
    last_fence = getattr(last.userData(), 'markdown_fence', None)
    if first_fence and first_fence == last_fence:
        # A selection entirely inside a fence need not include its opening marker.
        marker = '~' * max(3, max((len(m.group()) + 1 for m in re.finditer(r'~+', source)), default=3))
        return f'{marker}\n{source}\n{marker}'
    if first == last:
        line = first.text()
        start = len(line.encode('utf-16-le')[:(cursor.selectionStart() - first.position()) * 2].decode('utf-16-le'))
        end = start + len(source)
        for match in re.finditer(r'(?<!`)(`+)(?!`)(.+?)(?<!`)\1(?!`)', line):
            if match.start(2) <= start and end <= match.end(2):
                marker = '`' * (max((len(m.group()) for m in re.finditer(r'`+', source)), default=0) + 1)
                return f'{marker} {source} {marker}'
    return source


def cursor_source(widget, *, rendered=False, position=None):
    """Read to the document end without moving the visible cursor or selection."""
    cursor = widget.textCursor() if position is None else widget.cursorForPosition(position)
    cursor = QTextCursor(cursor)
    start = cursor.position()
    cursor.clearSelection()
    cursor.movePosition(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.KeepAnchor)
    if rendered:
        return rendered_source(cursor)
    source = cursor.selectedText().replace('\u2029', '\n')
    if not source:
        return ''
    block = widget.document().findBlock(start)
    line = block.text()
    offset = len(line.encode('utf-16-le')[:(start - block.position()) * 2].decode('utf-16-le'))
    fence = getattr(block.previous().userData(), 'markdown_fence', None)
    if fence:
        marker = fence['fence_char'] * fence['fence_length']
        if line.rstrip() == marker:
            return source.partition('\n')[2]
        if not any(part.rstrip() == marker for part in source.splitlines()):
            source += '\n' + marker
        return marker + '\n' + source
    for match in re.finditer(r'(?<!`)(`+)(?!`)(.+?)(?<!`)\1(?!`)', line):
        if match.start(2) <= offset < match.end(2):
            return match[1] + source
    if line.startswith(('    ', '\t')) and offset:
        source = '    ' + source
    return source


def append_selection_action(widget, menu, *, html=False, position=None):
    host = widget.window()
    if not hasattr(host, 'speech_enabled') or not host.speech_enabled():
        return
    source = selection_source(widget, rendered=html)
    menu.addSeparator()
    action = menu.addAction(speech_action_icon(), tr('module_text_to_speech_action_read_selection'))
    action.setIconVisibleInMenu(True)
    action.setEnabled(widget.textCursor().hasSelection())
    action.triggered.connect(lambda: host.action_read_aloud(source=source))
    remainder = cursor_source(widget, rendered=html, position=position)
    action = menu.addAction(speech_action_icon(filled=True), tr('module_text_to_speech_action_read_from_cursor'))
    action.setIconVisibleInMenu(True)
    action.setEnabled(bool(remainder.strip()))
    action.triggered.connect(lambda: host.action_read_aloud(source=remainder))
