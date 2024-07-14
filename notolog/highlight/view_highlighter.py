"""
Notolog Editor
Open-source markdown editor developed in Python.

File Details:
- Purpose: View mode Syntax Highlighter class tailored for Notolog.
- Functionality: This module includes functionality specifically needed for view mode, such as detecting strikethrough
  and 'todo' elements.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QTextBlock

from .main_highlighter import MainHighlighter
from . import TextBlockData

from typing import TYPE_CHECKING

import re

if TYPE_CHECKING:
    from typing import Match  # noqa: F401


class ViewHighlighter(MainHighlighter):
    """
    Syntax highlighter class for the view mode
    """

    theme = {
        's': {'style': 'strikethrough'},
        'todo': {'color': 'darkCyan', 'bg': {'color': 'yellow', 'pattern': Qt.BrushStyle.Dense5Pattern}},
        'inv_sep': {'font_size_ratio': 0.1},
    }
    # Keep it consistent with ini-file name, say 'viewer.ini', item prefix 'viewer_color_h1_text'
    theme_ini_prefix = 'viewer'

    """
    Elements order is matter!
    Say, i* first, b** second, bi*** third one-by-one to override prev token.
      i_, b__, bi___
      code `...`, code ```...```

    nth 0 is a whole string
    nth > 1 calculates as: start = end - length

    (?!...) - Negative Lookahead assertion
    (?<!...) - Negative Lookbehind assertion
    """
    re_rules = [
        # strikethrough
        (r'(~~(?!~|\s)[^~]*?(?<!~|\s)~~)', 1, 's', 's', False, theme['s'], None),  # between
        (r'(^|\s)(?<!~~)(~~(?!~|\s)[^~]*?)$', 2, 's_open', 's', True, theme['s'], None),
        (r'^([^~]*?[^\s~]~~)(?!~~)(?:\s|[\W^~]|$)', 1, 's_close', 's', True, theme['s'], None),
        # todos highlighting
        (r'([\s]*?)(@todo)(?=\s)', 2, 'todo', 'todo', False, theme['todo'], None),
        # invisible separator
        (r'(​)', 0, 'inv_sep', 'inv_sep', False, theme['inv_sep'], None),
    ]

    def get_regex(self, pattern: re) -> re:
        """
        Get either QRegularExpression or raw Python regex
        """
        return pattern

    def get_open_close_token_map(self):
        return [
            {'group': 's', 'open': 's_open', 'close': 's_close', 'theme': 's'}
        ]

    def highlightBlock(self, text_str):  # noqa: C901 - consider simplifying this method
        """
        Apply a syntax highlighting to each line of the text.
        https://doc.qt.io/qt-6/qsyntaxhighlighter.html#highlightBlock
        """

        # Get the current block and associated user data
        current_block = self.currentBlock()

        line_number = current_block.blockNumber()
        # Line number as it appears in the editor
        line_number_log = line_number + 1

        user_data = current_block.userData()
        if user_data is not None and type(user_data) is TextBlockData:
            """
            Skip as the highlighter may re-process the data
            """
            return

        # Create block's data storage
        user_data = TextBlockData(line_number)

        # Each line is not formatted initially
        self.clear_formatted()

        # Keep all line numbers even if no tags there
        if line_number not in self.line_tokens:
            self.line_tokens[line_number] = {}

        # Groups of tokens for correction (they have similar approach in rules)
        # oct_groups = [r.get('group') for r in self.get_open_close_token_map()]
        open_tokens = [r.get('open') for r in self.get_open_close_token_map()]
        close_tokens = [r.get('close') for r in self.get_open_close_token_map()]

        for pattern, nth, tag, group, duple, cf_data, reckon in self.rules:
            """
            Regular Python regular expression operations instead of QRegularExpression, QRegularExpressionMatchIterator
            and QRegularExpressionMatch as sometimes it doesn't work properly.
            * https://docs.python.org/3/library/re.html
            * https://doc.qt.io/qt-6/qregularexpression.html
            """
            matches = re.finditer(pattern, text_str)

            for match in matches:  # type: Match[str]
                # Get regex result position into the text string
                start = match.start(nth)
                end = match.end(nth)
                length = end - start

                # Collect line tokens only when any of them matched
                if tag not in self.line_tokens[line_number]:
                    self.line_tokens[line_number][tag] = []
                if tag != 'code' or tag not in self.get_nl_closing_tokens():
                    # The line tokens data will be reset after re-highlighting, no need to check for duplicates
                    self.line_tokens[line_number][tag].append(
                        {'start': start, 'end': end, 'length': length})  # 'in_code':...

                # Set up the tag count
                if tag in self.tokens:
                    self.tokens[tag]['cnt'] += 1
                else:
                    self.tokens[tag] = {'cnt': 1, 'o': (True if duple and tag in open_tokens else None)}

                # If the tag is duple mark it either opened or closed
                if duple:
                    if tag in open_tokens:
                        self.tokens[tag]['o'] = True
                    elif tag in close_tokens:
                        for _r in self.get_open_close_token_map():
                            if _r['group'] == group and _r['close'] == tag and _r['open'] in self.tokens:
                                self.tokens[_r['open']]['o'] = False

                """
                Check is single token inside the open close block of the same group
                """
                opened_group_token = self.get_opened_group_token(group)
                if not duple and opened_group_token is not None:
                    # Have to be there if it is not None
                    self.tokens[opened_group_token]['o'] = False
                    self.tokens[opened_group_token]['cnt'] -= 1

                """
                Non-default encodings may appear, decode them with unknown replacement.
                Also, check `surrogateescape` option.
                match.captured(nth).encode('utf-8', 'replace').decode('utf-8')
                """
                if self.debug:
                    self.logger.debug(
                        'Tokens: "%s" > %s > %s (s:%d, l:%d, e:%d, n:%d)[%d] prev block state %d'
                        % (tag, self.tokens[tag], match.group(nth).encode('utf-8', 'replace'),
                           start, length, end, nth, line_number, self.previousBlockState())
                    )

                # Set as formatted to skip excess processing with a similar regex
                self.set_formatted(group)

                opened = (True if tag in open_tokens else False) and self.get_opened_group_token(group) is not None
                closed = (True if tag in close_tokens else False) and self.get_opened_group_token(group) is None
                user_data.put(tag=tag, opened=opened, within=False, closed=closed, start=start, end=end)

                # Save block's data
                self.set_block_data(current_block, user_data)

        for token_data in self.get_open_close_token_map():
            """
            Process the lines located between the tags those are do not have regex matches
            """
            # Not formatted elements within the multiline block
            if (not self.is_group_formatted(token_data['group'])
                    and token_data['open'] in self.tokens
                    and self.tokens[token_data['open']]['o'] is True):
                self.set_formatted(token_data['group'])
                if self.debug:
                    self.logger.debug(
                        '[%d] "%s", tag: "%s" opened: %r'
                        % (line_number_log, text_str, token_data['open'], self.tokens[token_data['open']]['o'])
                    )
                tag = ('%s_within' % token_data['group'])
                user_data.put(tag=tag, opened=False, within=True, closed=False, start=0, end=len(text_str))
                # Save block's data
                self.set_block_data(current_block, user_data)

    def set_block_data(self, block: QTextBlock, data: TextBlockData) -> None:
        try:
            """
            Try to save block data to allow future processing
            """
            block.setUserData(data)
        except (TypeError, RuntimeError, ValueError) as e:
            self.logger.error('Cannot setup block data "%s" as error "%s" occurred' % (data, e))
