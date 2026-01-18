"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Markdown Syntax Highlighter class tailored for Notolog.

Story:
This module combines regular expression patterns with integrated code logic to provide balanced results
and reduce reliance on complex regular expressions. This approach is particularly useful for processing multiline
blocks, such as code blocks, where stable detection is crucial for accurate visual representation. Inaccurate
detection may lead to "blinking highlighting." While the author has attempted to cover most cases, the primary
goal was to meet the common needs expected from a markdown editor.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtCore import Qt

from .main_highlighter import MainHighlighter
from . import TextBlockData

from typing import TYPE_CHECKING

import re

if TYPE_CHECKING:
    from typing import Union  # noqa: F401
    from PySide6.QtGui import QTextBlockUserData  # noqa: F401


class MdHighlighter(MainHighlighter):
    """
    Syntax highlighter class for the Markdown language
    """

    theme = {
        'rn': {},
        'a': {'color': 'darkBlue'},
        'b': {'color': 'blue', 'style': 'bold'},
        'boo': {'color': 'blue', 'style': 'bold'},
        'i': {'color': 'red', 'style': 'italic'},
        'iu': {'color': 'red', 'style': 'italic'},
        'bi': {'color': 'darkRed', 'style': {'bold', 'italic'}},
        'biu': {'color': 'darkRed', 'style': {'bold', 'italic'}},
        'h1': {'color': 'white', 'font_size_ratio': 2.4,
               'bg': {'color': 'darkCyan', 'pattern': Qt.BrushStyle.Dense2Pattern}},
        'h1_text': {'color': 'white', 'font_size_ratio': 2.4, 'style': 'bold',
                    'bg': {'color': 'darkCyan', 'pattern': Qt.BrushStyle.Dense4Pattern}},
        'h2': {'color': 'white', 'font_size_ratio': 2.1,
               'bg': {'color': 'darkCyan', 'pattern': Qt.BrushStyle.Dense3Pattern}},
        'h2_text': {'color': 'darkCyan', 'font_size_ratio': 2.1, 'style': 'bold',
                    'bg': {'color': 'darkCyan', 'pattern': Qt.BrushStyle.Dense6Pattern}},
        'h3': {'color': 'white', 'font_size_ratio': 1.8,
               'bg': {'color': 'darkCyan', 'pattern': Qt.BrushStyle.Dense4Pattern}},
        'h3_text': {'color': 'darkCyan', 'font_size_ratio': 1.8, 'style': 'bold'},
        'h4': {'color': 'white', 'font_size_ratio': 1.6,
               'bg': {'color': 'darkCyan', 'pattern': Qt.BrushStyle.Dense4Pattern}},
        'h4_text': {'color': 'darkCyan', 'font_size_ratio': 1.6, 'style': 'bold'},
        'h5': {'color': 'white', 'font_size_ratio': 1.4,
               'bg': {'color': 'darkCyan', 'pattern': Qt.BrushStyle.Dense4Pattern}},
        'h5_text': {'color': 'darkCyan', 'font_size_ratio': 1.4, 'style': 'bold'},
        'h6': {'color': 'white', 'font_size_ratio': 1.3,
               'bg': {'color': 'darkCyan', 'pattern': Qt.BrushStyle.Dense4Pattern}},
        'h6_text': {'color': 'darkCyan', 'font_size_ratio': 1.3, 'style': 'bold'},
        's': {'color': 'grey', 'style': 'strikethrough', 'alt_color': 'grey'},  # Alt color used for the strikethrough line
        'u': {'color': '', 'style': 'underline', 'alt_color': ''},  # Alt color here refers to the underline color
        'code': {'color': 'magenta', 'bg': {'color': 'magenta', 'pattern': Qt.BrushStyle.Dense6Pattern}},
        'codel': {'color': 'yellow', 'style': 'monospace',
                  'bg': {'color': 'darkMagenta', 'pattern': Qt.BrushStyle.Dense2Pattern}},
        'codelf': {'color': 'white', 'style': 'monospace',
                   'bg': {'color': 'magenta', 'pattern': Qt.BrushStyle.Dense2Pattern}},
        'code_lang': {'color': 'magenta', 'style': 'bold'},
        'code_indent': {'bg': {'color': 'pink', 'style': 'monospace', 'pattern': Qt.BrushStyle.Dense6Pattern}},
        'code_content': {'color': 'brown', 'style': 'monospace'},
        # Debug: 'bg': {'color': 'darkGrey', 'pattern': Qt.BrushStyle.Dense2Pattern}
        'wrong_indent': {'bg': {'color': 'red', 'pattern': Qt.BrushStyle.DiagCrossPattern}},
        'comment': {'color': 'grey', 'style': 'monospace',
                    'bg': {'color': 'lightGrey', 'pattern': Qt.BrushStyle.Dense6Pattern}},
        'table_h': {'style': ['bold', 'monospace'], 'bg': {'color': 'lightGrey'}},
        'table_d': {'style': 'monospace', 'bg': {'color': 'whiteSmoke'}},
        'img': {'color': 'green'},
        'ref': {'color': 'white', 'bg': {'color': 'green', 'pattern': Qt.BrushStyle.Dense3Pattern}},
        # 'ref_data': {'color': 'green', 'bg': {'color': 'yellow', 'pattern': Qt.BrushStyle.Dense6Pattern}},
        'abbr': {'color': 'white', 'bg': {'color': 'dodgerBlue', 'pattern': Qt.BrushStyle.SolidPattern}},
        'abbr_text': {'color': 'white', 'style': 'bold',
                      'bg': {'color': 'dodgerBlue', 'pattern': Qt.BrushStyle.SolidPattern}},
        'link': {'color': 'white', 'style': 'italic', 'bg': 'blue'},
        'list': {'color': 'white', 'bg': 'darkMagenta'},
        'list_text': {'color': 'darkMagenta'},
        'list_indent': {'bg': {'color': 'darkMagenta', 'pattern': Qt.BrushStyle.Dense6Pattern}},
        'hr': {'color': 'white', 'style': 'strikethrough', 'bg': {'color': 'darkOrange'}},
        'blockquote': {'color': 'white', 'bg': {'color': 'grey', 'pattern': Qt.BrushStyle.Dense2Pattern},
                       # Blockquote friendly elements inherited this background
                       'bg_inner': {'color': 'lightGrey', 'pattern': Qt.BrushStyle.Dense3Pattern}},
        'html': {'color': 'darkCyan', 'style': 'monospace'},
        'html_open': {'color': 'green', 'style': 'monospace'},
        'html_close': {'color': 'darkRed', 'style': 'monospace'},
        'html_comment': {'color': 'grey', 'style': 'monospace'},
        'emoji': {'color': 'white', 'bg': {'color': 'olive', 'pattern': Qt.BrushStyle.Dense3Pattern}},
        'todo': {'color': 'darkCyan', 'bg': {'color': 'yellow', 'pattern': Qt.BrushStyle.Dense5Pattern}},
        'coop1': {'color': 'red', 'style': 'monospace', 'bg': {'color': None}},
        'coop2': {'color': 'darkGreen', 'style': 'monospace', 'bg': {'color': None}},
        'coop3': {'color': 'darkOrange', 'style': 'monospace', 'bg': {'color': None}},
        'coop4': {'color': 'blue', 'style': 'monospace', 'bg': {'color': None}},
        'coop5': {'color': 'brown', 'style': 'monospace',
                  'bg': {'color': 'brown', 'pattern': Qt.BrushStyle.Dense7Pattern}},
    }
    # Keep it consistent with ini-file name, say 'md.ini', item prefix 'md_color_h1_text'
    theme_ini_prefix = 'md'

    """
    Elements order is matter.
    Say, i* first, b** second, bi*** third one-by-one to override prev token.
        i_, b__, bi___
        code `...`, code ```...```

    nth 0 is a whole string
    nth > 1 calculates as: start = end - length
    """
    re_rules = [
        # Empty line
        (r'^([\r\n]*?)$', 1, 'rn', 'rn', False, theme['rn'], None),
        # Blockquotes
        (r'^(\s*?)(\>+\s.*?)$', 2, 'blockquote', 'blockquote', False, theme['blockquote'], None),
        # List
        (r'^(\s+|\>{1}\s+|)([0-9]{1,}\.|[\*\+\-]{1})(?=\s)', 2, 'list', 'list', False, theme['list'], None),
        (r'^(\s+|\>{1}\s+|)([0-9]{1,}\.|[\*\+\-]{1})(\s.*?)$', 3, 'list_text', 'list', False, theme['list_text'], None),
        (r'^(\s+|\>{1}\s+|)([0-9]{1,}\.|[\*\+\-]{1})\s.*?$',
         1, 'list_indent', 'list', False, theme['list_indent'], None),
        # Code ``` (fenced)
        (r'(?:^|\s|\W|[^`\#])(?<!`)(```(?!`).*?(?<!`)```)(?!`)(?:\s|\W|[^`]|$)',
         1, 'codel', 'code', False, theme['codelf'], None),
        (r'^(?<!\#)((?:[\s]*?)```)[a-z\-_\+#\s\.{}]*?(?!```)$', 1, 'code', 'code', True, theme['code'], None),
        (r'^(?<!\#)((?:[\s]*?)```)(\s*?\{?[a-z\-_\+#\s\.^{}]+\}?)$',
         2, 'code_lang', 'code', False, theme['code_lang'], None),
        (r'^([\s]{1,})```([\S]+|)$', 1, 'wrong_indent', 'code', False, theme['wrong_indent'], None),
        # Code ::::
        (r'^(([\s]{4,}|[\t]{1,})(::::))[\S]*?\s*?$', 3, 'codec', 'code', False, theme['code'], None),
        (r'^(([\s]{4,}|[\t]{1,})::::)([\S]+)\s*?$', 3, 'code_lang', 'code', False, theme['code_lang'], None),
        (r'^([\s]{4,}|[\t]{1,})::::[\S]*?\s*?$', 1, 'code_indent', 'code', False, theme['code_indent'], None),
        # Italic (asterisk)
        (r'(?<!\*)(\*[^\s\*][^\*]*?[^\s]?\*)(?!\*)', 1, 'i', 'i', False, theme['i'], None),  # between
        # \W to avoid character mention in a sequence like: *, ...
        (r'(^|\s)(\*[^\s\W\*][^\*]*?)(?!\*)$', 2, 'i_open', 'i', True, theme['i'], None),
        (r'^([^\*]+(?<!\s)\*)(?!\*)(?:\s|\W|$)', 1, 'i_close', 'i', True, theme['i'], None),
        # Italic (underline)
        # \W (non-word) characters are all characters apart from numbers, letters, and underscores.
        (r'(^|\s)(_(?!\s|_).*?(?<!\s|_)_)(?:\s|[\W^_]|$)', 2, 'iu', 'iu', False, theme['iu'], None),  # between
        (r'(^|\s)(_[^\s\W_][^_]*?)$', 2, 'iu_open', 'iu', True, theme['iu'], None),
        (r'^([^_]*?(?<!_)[^\s_]_)(?!_)(?:\s|\W|$)', 1, 'iu_close', 'iu', True, theme['iu'], None),
        # Bold (asterisk)
        (r'(?<!\*)(\*{2}[^\s\*][^\*]*?[^\s]?\*{2})(?!\*)', 1, 'b', 'b', False, theme['b'], None),  # between
        (r'(^|\s)(\*{2}[^\s\*][^\*]*?)(?!\*)$', 2, 'b_open', 'b', True, theme['b'], None),
        (r'^([^\*]+(?<!\s)\*{2})(?!\*)(?:\s|\W|$)', 1, 'b_close', 'b', True, theme['b'], None),
        # Bold (underline)
        # \b doesn't work, only [^\s]
        (r'(^|\s)(__(?!\s|_).*?(?<!\s|_)__)(?:\s|[\W^_]|$)', 2, 'boo', 'boo', False, theme['boo'], None),  # between
        (r'(^|\s)(__[^\s\W_][^_]*?)$', 2, 'boo_open', 'boo', True, theme['boo'], None),
        (r'^([^_]*?(?<!_)[^\s_]__)(?!__)(?:\s|\W|$)', 1, 'boo_close', 'boo', True, theme['boo'], None),
        # (r'(?<=__)([^\s].*?[^\s])(?=__)', 'b', 'b', 1, True, theme['b'], None),
        # Bold and Italic altogether (asterisk)
        (r'(?<!\*)(\*{3}[^\s\*][^\*]*?[^\s]?\*{3})(?!\*)', 1, 'bi', 'bi', False, theme['bi'], None),  # between
        (r'(^|\s)(\*{3}[^\s\*][^\*]*?)(?!\*)$', 2, 'bi_open', 'bi', True, theme['bi'], None),
        (r'^([^\*]+(?<!\s)\*{3})(?!\*)(?:\s|\W|$)', 1, 'bi_close', 'bi', True, theme['bi'], None),
        # Bold and Italic altogether (underline)
        (r'(^|\s)(___(?!\s|_).*?(?<!\s|_)___)(?:\s|[\W^_]|$)', 2, 'biu', 'biu', False, theme['biu'], None),  # between
        (r'(^|\s)(___[^\s\W_][^_]*?)$', 2, 'biu_open', 'biu', True, theme['biu'], None),
        (r'^([^_]*?(?<!_)[^\s_]___)(?!___)(?:\s|\W|$)', 1, 'biu_close', 'biu', True, theme['biu'], None),
        # Strikethrough
        # ~~text~~ first to allow skip the open-close group as it may interference
        (r'(~~(?!~|\s)[^~]*?(?<!~|\s)~~)', 1, 's', 's', False, theme['s'], None),  # between
        (r'(^|\s)(?<!~~)(~~(?!~|\s)[^~]*?)$', 2, 's_open', 's', True, theme['s'], None),
        (r'^([^~]*?[^\s~]~~)(?!~~)(?:\s|[\W^~]|$)', 1, 's_close', 's', True, theme['s'], None),
        # Underline
        (r'(<u>.*?</u>)', 1, 'u', 'u', False, theme['u'], None),  # between
        (r'(<u>[^<>]*?)(?!</?u>)$', 1, 'u_open', 'u', True, theme['u'], None),
        (r'^([^<>]*?</u>)(?!</?u>)(?:\s|\W|$)', 1, 'u_close', 'u', True, theme['u'], None),
        # Code line within backticks
        (r'(?:^|\s|\W|[^`\#])(?<!`)(`(?!`).*?(?<!`)`)(?!`)(?:\s|\W|[^`]|$)',
         1, 'codel', 'code', False, theme['codel'], None),
        # Header
        # (r'^(?:[\s\t]*?)(?<h1>#\s*?)(?<h1_text>.*)$', ['h1', 'h1_text'],
        # 'h1_text', 'h1', False, theme['h_text'], None),
        (r'^((?:[\s\t]*?)#)\s*?.*?', 1, 'h1', 'h1', False, theme['h1'], None),
        (r'^((?:[\s\t]*?)#\s*?)(.*)$', 2, 'h1_text', 'h1', False, theme['h1_text'], None),
        (r'^((?:[\s\t]*?)[#]{2})\s*?.*?', 1, 'h2', 'h', False, theme['h2'], None),
        (r'^((?:[\s\t]*?)[#]{2}\s*?)(.*)$', 2, 'h2_text', 'h', False, theme['h2_text'], None),
        (r'^((?:[\s\t]*?)[#]{3})\s*?.*?', 1, 'h3', 'h', False, theme['h3'], None),
        (r'^((?:[\s\t]*?)[#]{3}\s*?)(.*)$', 2, 'h3_text', 'h', False, theme['h3_text'], None),
        (r'^((?:[\s\t]*?)[#]{4})\s*?.*?', 1, 'h4', 'h', False, theme['h4'], None),
        (r'^((?:[\s\t]*?)[#]{4}\s*?)(.*)$', 2, 'h4_text', 'h', False, theme['h4_text'], None),
        (r'^((?:[\s\t]*?)[#]{5})\s*?.*?', 1, 'h5', 'h', False, theme['h5'], None),
        (r'^((?:[\s\t]*?)[#]{5}\s*?)(.*)$', 2, 'h5_text', 'h', False, theme['h5_text'], None),
        (r'^((?:[\s\t]*?)[#]{6})\s*?.*?', 1, 'h6', 'h', False, theme['h6'], None),
        (r'^((?:[\s\t]*?)[#]{6}\s*?)(.*)$', 2, 'h6_text', 'h', False, theme['h6_text'], None),
        # Table
        (r'^(\|[\s\|\:\-]+?\|)$', 1, 'table_h', 'table', False, theme['table_h'], None),
        (r'^(\|(?=.*?[a-zA-Z0-9]).*?\|)$', 1, 'table_d', 'table', False, theme['table_d'], None),
        # Image
        (r'(!\[[^\]]*?\]\([^\)]*?\))', 1, 'img', 'img', False, theme['img'], None),
        (r'(!\[[^\]]*?\]\[[^\]]*?\])', 1, 'img', 'img', False, theme['img'], None),
        # reference either image or link, footnotes also
        (r'((?<!\*)\[[^\]]*?\]:)', 1, 'ref', 'ref', False, theme['ref'], None),
        # (r'(\[[^\]]*?\]:)(\S*?)$', 2, 'ref_data', 'ref', False, theme['ref_data'], None),
        # abbreviations
        (r'(\*\[.*?\]:.*?)', 1, 'abbr', 'abbr', False, theme['abbr'], None),
        (r'(\*\[(.*?)\]:.*?)', 2, 'abbr_text', 'abbr', False, theme['abbr_text'], None),
        # hyperlinks (before the web links block to allow style overriding)
        (r'((?<!!)\[.*?\]\(.*?\))', 1, 'a', 'a', False, theme['a'], None),
        # Web link
        # A word boundary \b matches the position between a word character (e.g., alphanumeric character or underscore)
        # and a non-word character (e.g., whitespace, punctuation, or the beginning/end of a string).
        # It allows you to match patterns only at the boundaries of words.
        # RFC 3986: uri = "[A-Za-z0-9\-._~:/?#\[\]@!$&\'()*+,;=%]"
        (r'((?:https?|ftp):\/\/(?:\S+(?::\S*)?@)?'
         r'(?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|(?!-)[A-Za-z0-9-]{1,63}(?:\.(?!-)[A-Za-z0-9-]{1,63})+)?(?:\:[0-9]+)?'
         r'(?:\/(?:[^\:\?#\s\/\)]+)?)*(?:\?[^\s]*)?(?:#[^\s]*)?)', 1, 'link', 'link', False, theme['link'], None),
        # horizontal line
        (r'^(?:[\s>]*?)([\-\*_]{3,}(?:[\s]*?))$', 1, 'hr', 'hr', False, theme['hr'], None),
        # Comments
        # TODO: Add syntax highlighting based on the code language.
        (r'^([\s\t]*?[#]{1,}\s*?.*)$', 1, 'comment', 'comment', False, theme['comment'],
         lambda s: s.is_in_code()),
        (r'^((?:\s*?)"""(?!").*?(?<!")""")(?:\s*?)$', 1, 'comment', 'comment', False, theme['comment'],
         lambda s: s.is_in_code()),
        (r'^(?:[\s\t]*?)(""")(?:[\s\t]*?)$', 1, 'cclop', 'comment', False, theme['comment'],
         lambda s: s.is_in_code()),
        (r'(\/\/.*?)$', 1, 'comment', 'comment', False, theme['comment'],
         lambda s: s.is_in_code()),
        # html tags
        (r'(<\s*?([a-zA-Z][^>]*?)\s*?>)', 1, 'html', 'html', True, theme['html_open'], None),
        (r'(<\s*?\/\s*?([a-zA-Z][^\s>]*?)\s*?>)', 1, 'html', 'html', True, theme['html_close'], None),
        (r'(<\s*?([a-zA-Z!][^\/]*?)\s*?(\/)?\s*?>)', 1, 'html', 'html', False, theme['html'], None),
        (r'(<!--(.*?)-->)', 1, 'html', 'html', False, theme['html_comment'], None),
        # emojis
        (r'(\:[a-zA-Z_]+\:)', 1, 'emoji', 'emoji', False, theme['emoji'], None),
        # To-do keywords
        (r'([\s]*?)(@todo)(?=\s|$)', 2, 'todo', 'todo', False, theme['todo'], None),
        # Excess indent at the end of the line
        # (r'([\s]+)$', 1, 'wrong_indent', 'general', False, theme['wrong_indent'], None),
        # Code operators, group 1
        (r'(class|exit|[\-\+\*\{\}]+)', 1, 'coop1', 'coop', False, theme['coop1'],
         lambda s: s.is_in_code() and not s.is_in_code_comment()),
        # Assignments, group 2. Can be extended to [\=\[\]\(\)]
        # (r'([\=]{1,})', 1, 'coop2', 'coop', False, theme['coop2'],
        # lambda s: s.is_in_code() and not s.is_in_code_comment()),
        # Functions and methods, group 3
        (r'(\b(?:\s*?)[a-zA-Z\.\_]+\b)\(.*?\)', 1, 'coop3', 'coop', False, theme['coop3'],
         lambda s: s.is_in_code() and not s.is_in_code_comment()),
        # Code operators and instructions, group 4
        (r'((?:^|\s)*?if|else|elif|for|while|switch|def|function|lambda|echo|self|return)[\s\W]{1,}',
         1, 'coop4', 'coop', False, theme['coop4'],
         lambda s: s.is_in_code() and not s.is_in_code_comment()),
        # Numbers in code, group 5
        # (r'([0-9]+)', 1, 'coop5', 'coop', False, theme['coop5'],
        # lambda s: s.is_in_code() and not s.is_in_code_comment()),
    ]

    def get_regex(self, pattern: re) -> re:
        """
        Get either QRegularExpression or raw Python regex
        re = QRegularExpression(pattern)
        """
        return pattern

    def get_open_close_token_map(self):
        return [
            {'group': 'i', 'open': 'i_open', 'close': 'i_close', 'theme': 'i'},
            {'group': 'iu', 'open': 'iu_open', 'close': 'iu_close', 'theme': 'iu'},
            {'group': 'b', 'open': 'b_open', 'close': 'b_close', 'theme': 'b'},
            {'group': 'boo', 'open': 'boo_open', 'close': 'boo_close', 'theme': 'boo'},
            {'group': 'bi', 'open': 'bi_open', 'close': 'bi_close', 'theme': 'bi'},
            {'group': 'biu', 'open': 'biu_open', 'close': 'biu_close', 'theme': 'biu'},
            {'group': 's', 'open': 's_open', 'close': 's_close', 'theme': 's'},
            {'group': 'u', 'open': 'u_open', 'close': 'u_close', 'theme': 'u'}
        ]

    def is_blockquote_inner(self, tag=str):
        return tag in {
            'i', 'i_open', 'i_close', 'iu', 'iu_open', 'iu_close',
            'b', 'b_open', 'b_close', 'boo', 'boo_open', 'boo_close',
            'bi', 'bi_open', 'bi_close', 'biu', 'biu_open', 'biu_close',
            's', 's_open', 's_close',
            'u', 'u_open', 'u_close',
            'list_text', 'list_indent',
            'emoji',
            'hr',
            'a'
        }

    def get_nl_closing_tokens(self):
        """
        Block open tokens closing with a new empty line.
        The order in the row is matter because of processing one-by-one.
        """
        return ['rn', 'codec', 'blockquote', 'list']

    def highlightBlock(self, text_str):  # noqa: C901 - consider simplifying this method
        """
        Apply a syntax highlighting to each line of the text.
        * https://doc.qt.io/qt-6/qsyntaxhighlighter.html#highlightBlock
        """

        # Get the current block and associated user data
        self.current_block = self.currentBlock()
        self.user_data = self.current_block.userData()  # type: Union[TextBlockData, QTextBlockUserData]

        self.prev_block = self.current_block.previous()
        self.prev_user_data = self.prev_block.userData()  # type: Union[TextBlockData, QTextBlockUserData]

        self.line_number = self.currentBlock().blockNumber()
        # Line number as it appears in the editor
        self.line_number_log = self.line_number + 1

        if self.user_data is None or not isinstance(self.user_data, TextBlockData):
            self.logger.debug('{%r} !!! Block data is not set at [%d*], is in code %d, prev state %d'
                              % (self.rehighlight_block, self.line_number_log,
                                 self.is_in_code(skip_data=True), self.previousBlockState()))
            self.user_data = TextBlockData(self.line_number)
            """
            Restore within a code block state, for example when a new line appears.
            Both 'code' and 'codec' have their own rules on how a code group works, so check them up separately.
            """
            if self.is_in_code(skip_data=True, force_tag='code'):
                self.user_data.put(tag='code', opened=False, within=True, closed=True)
            elif self.is_in_code(skip_data=True, force_tag='codec'):
                self.user_data.put(tag='codec', opened=False, within=True, closed=True)

        # Keep all line numbers even if no tags there
        if self.line_number not in self.line_tokens:
            self.line_tokens[self.line_number] = {}

        # Each line is not formatted initially
        self.clear_formatted()

        # Groups of tokens for correction (they have similar approach in rules)
        oct_groups = [r.get('group') for r in self.get_open_close_token_map()]
        open_tokens = [r.get('open') for r in self.get_open_close_token_map()]
        close_tokens = [r.get('close') for r in self.get_open_close_token_map()]

        pattern, nth, tag, group, duple, cf_data, reckon = (None,) * 7
        for pattern, nth, tag, group, duple, cf_data, reckon in self.rules:
            """
            Process code block tokens.
            """
            if tag == 'code':
                if duple and tag not in self.tokens:
                    self.tokens[tag] = {'cnt': 0, 'o': None}
                # Pass params below
                break

        if re is None:
            self.logger.debug('Notice: Regex pattern not found for the tag "%s"' % tag)
            return

        if self.rehighlight_block:
            if 'code' in self.tokens:
                # Opened and continues to apply for non-code blocks
                self.tokens['code']['o'] = (self.user_data.get_param('code', 'within')
                                            and not self.user_data.get_param('code', 'closed'))

        matches = re.finditer(pattern, text_str)
        match = next(matches, None)

        if match:
            # Get regex result position into the text string
            start = match.start(nth)
            end = match.end(nth)
            length = end - start

            # Collect line tokens only when any of them matched
            if tag not in self.line_tokens[self.line_number]:
                self.line_tokens[self.line_number][tag] = []
            # The line tokens data will be reset after re-highlighting, no need to check for duplicates
            line_token_data = {'start': start, 'end': end, 'length': length}
            if line_token_data not in self.line_tokens[self.line_number][tag]:
                self.line_tokens[self.line_number][tag].append(line_token_data)

            if self.rehighlight_block:
                if tag in self.tokens:
                    """
                    Recover state of an open token
                    """
                    self.tokens[tag]['o'] = (self.user_data.get_param(tag, 'within')
                                             and self.user_data.get_param(tag, 'opened'))
            elif not self.rehighlight_block:
                # Set up the tag count
                if tag in self.tokens:
                    self.tokens[tag]['cnt'] += 1
                # Because of the code token could be the same whether opened or closed.
                self.tokens[tag]['o'] = True if self.tokens[tag]['cnt'] % 2 > 0 else False

            self.logger.debug(
                'Current code block data [%d] rehi:%r, curr_blk_st:%d, prev_blk_st:%d, '
                'in_code:%r, in_code:%r(STRICT), inc:%r, o:[%r]~[%r], c:%r'
                % (self.line_number,
                   self.rehighlight_block,
                   self.currentBlockState(),
                   self.previousBlockState(),
                   self.is_in_code(),
                   self.is_in_code(skip_data=True),
                   self.user_data.get_param(tag, 'within'),
                   self.user_data.get_param(tag, 'opened'),
                   self.tokens[tag]['o'],
                   self.user_data.get_param(tag, 'closed')))

            # Set the correct state of the code block to update currentBlockState()
            self.check_and_set_in_code_state()

            # Check either tag opened or closed and set a relevant data
            if self.tokens[tag]['o']:
                self.logger.debug(
                    '{%r} >>> Open "%s" at [%d*], is in code %d, prev state %d'
                    % (self.rehighlight_block, tag, self.line_number_log, self.is_in_code(),
                       self.previousBlockState())
                )
                if not self.user_data.get_param(tag, 'opened'):
                    self.user_data.put(tag=tag, opened=True, within=True, closed=False)
            # If tag wasn't open it doesn't mean it was closed, check prev state
            elif self.prev_user_data and self.prev_user_data.get_param(tag, 'within'):
                self.logger.debug(
                    '{%r} <<< Close "%s" at [%d*], is in code %d, prev state %d'
                    % (self.rehighlight_block, tag, self.line_number_log, self.is_in_code(),
                       self.previousBlockState())
                )
                # Close the code block
                if not self.user_data.get_param(tag, 'closed'):
                    self.user_data.put(tag=tag, opened=False, within=True, closed=True)
            else:
                # Warning as such case is not expected here
                self.logger.debug(
                    'Notice: {%r} >~> Open token inside "%s" at [%d*]'
                    % (self.rehighlight_block, tag, self.line_number_log)
                )
        elif self.is_in_code(skip_data=True, force_tag='code'):
            self.user_data.put(tag=tag, opened=False, within=True, closed=False)
            self.setCurrentBlockState(1)
            if not self.is_any_formatted():
                self.setFormat(0, len(text_str), self.cf(**self.theme['code_content']))
                self.set_formatted('code')
            self.logger.debug(
                '{%r} >=< Inside "%s" at [%d*], is in code %d (STRICT), prev state %d'
                % (self.rehighlight_block, tag, self.line_number_log,
                   self.is_in_code(skip_data=True, force_tag='code'), self.previousBlockState())
            )
        else:
            # When new line within a code block appears have to check prev block state (within and not closed)
            if (self.is_in_code(force_tag='code')
                    and self.prev_user_data
                    and self.prev_user_data.get_param(tag, 'within')
                    and not self.prev_user_data.get_param(tag, 'closed')):
                self.user_data.put(tag=tag, opened=False, within=True, closed=False)
                self.setCurrentBlockState(1)
                self.logger.debug(
                    '{%r} >=< Inside "%s" [%d*], is in code %d (lenient), prev state %d'
                    % (self.rehighlight_block, tag, self.line_number_log, self.is_in_code(force_tag='code'),
                       self.previousBlockState())
                )
            else:
                self.user_data.put(tag=tag, opened=False, within=False, closed=False)
                self.setCurrentBlockState(0)
                self.logger.debug('{%r} ... No "%s" [%d*]' % (self.rehighlight_block, tag, self.line_number_log))

        for pattern, nth, tag, group, duple, cf_data, reckon in self.rules:
            """
            Process block tokens closing with a new line.
            * rn
            * blockquote
            * codec
            * list
            Notice: Do not processing it when located within a code block, like this:
            if (self.is_in_code() and tag not in {'codec'}):
                continue
            Causing a "jumping" syntax, so better to leave the blocks within the code block
            but re-write their style accordingly.
            """
            if tag not in self.get_nl_closing_tokens():
                continue

            if tag not in self.tokens:
                self.tokens[tag] = {'cnt': 0, 'o': False}

            if self.rehighlight_block:
                if tag in self.tokens:
                    """
                    Opened tokens continue to apply for the following inline parts
                    Logic slightly differ apart with open-close tokens approach.
                    """
                    self.tokens[tag]['o'] = self.user_data.get_param(tag, 'within')

            matches = re.finditer(pattern, text_str)
            match = next(matches, None)

            if match:
                # Get regex result position into the text string
                start = match.start(nth)
                end = match.end(nth)
                length = end - start

                # Collect line tokens only when any of them matched
                if tag not in self.line_tokens[self.line_number]:
                    self.line_tokens[self.line_number][tag] = []
                # The line tokens data will be reset after re-highlighting, no need to check for duplicates
                line_token_data = {'start': start, 'end': end, 'length': length}
                if line_token_data not in self.line_tokens[self.line_number][tag]:
                    self.line_tokens[self.line_number][tag].append(line_token_data)

                if tag == 'rn':
                    self.logger.debug(
                        '{%r}  %s  New line found "%s" at [%d*]'
                        % (self.rehighlight_block, b'\xe2\x86\xb5'.decode('utf-8'), tag, self.line_number_log)
                    )
                    continue

                if ((tag in {'codec', 'list'}
                     # Code block :::: has to start with empty line or at very beginning of the document.
                     and (self.line_number == 0
                          # Check prev line is an empty line
                          or (self.line_number - 1 in self.line_tokens
                              and 'rn' in self.line_tokens[self.line_number - 1])))
                        # Blockquote and list may start without preliminary empty line
                        or (tag not in {'codec'}
                            and not self.tokens[tag]['o'])):
                    # Mind the indents
                    self.tokens[tag]['cnt'] += 1
                    self.tokens[tag]['o'] = True
                    self.logger.debug(
                        '{%r} >>> Open "%s" at [%d*]'
                        % (self.rehighlight_block, tag, self.line_number_log)
                    )
                    """
                    Block tokens cannot be located on the same line, suppose to find them one per line
                    """
                    self.user_data.put(tag=tag, opened=True, within=True, closed=False)
                else:
                    self.logger.debug(
                        '{%r} >~> Open token inside "%s" at [%d*]'
                        % (self.rehighlight_block, tag, self.line_number_log)
                    )
                    """
                    Block tokens cannot be located on the same line, suppose to find them one per line
                    """
                    self.user_data.put(tag=tag, opened=False, within=self.tokens[tag]['o'], closed=False)
            elif self.tokens[tag]['o']:
                if 'rn' in self.line_tokens[self.line_number]:
                    # Close opened token then
                    self.tokens[tag]['o'] = False
                    self.logger.debug(
                        '{%r} <<< Close "%s" at [%d*] %s'
                        % (self.rehighlight_block, tag, self.line_number_log, self.line_tokens[self.line_number])
                    )
                    """
                    Block tokens cannot be located on the same line, suppose to find them one per line
                    """
                    self.user_data.put(tag=tag, opened=False, within=True, closed=True)
                # Some tokens like a 'list' may be located within no empty lines either above or below,
                # thus always an open tag.
                elif tag not in {'list'}:
                    self.logger.debug(
                        '{%r} >=< Inside "%s" at [%d*], is in code %d (lenient), prev state %d'
                        % (self.rehighlight_block, tag, self.line_number_log, self.is_in_code(force_tag='codec'),
                           self.previousBlockState())
                    )
                    """
                    Block tokens cannot be located on the same line, suppose to find them one per line
                    """
                    self.user_data.put(tag=tag, opened=False, within=True, closed=False)
                    if not self.is_any_formatted():
                        if tag == 'blockquote':
                            self.setFormat(0, len(text_str), self.cf(**self.theme['blockquote']))
                            self.set_formatted('blockquote')
                        elif (tag == 'codec'
                              and self.is_in_code(skip_data=True, force_tag='codec')):
                            self.setFormat(0, len(text_str), self.cf(**self.theme['code_content']))
                            self.set_formatted('code')
            else:
                self.user_data.put(tag=tag, opened=False, within=False, closed=False)
                self.logger.debug('{%r} ... No "%s" [%d*]' % (self.rehighlight_block, tag, self.line_number_log))

        try:
            """
            Try to save block data to allow future processing
            """
            self.current_block.setUserData(self.user_data)
        except (TypeError, RuntimeError, ValueError) as e:
            self.logger.error(f'Cannot setup block data "{self.user_data}", error occurred: {e}')

        format_map = {}  # To apply formatting after the whole line processed
        for pattern, nth, tag, group, duple, cf_data, reckon in self.rules:

            if self.is_in_code() and group not in {'code', 'comment', 'coop', 'rn'}:
                """
                Ignore non-code tags if within a code block
                """
                continue

            if reckon is not None and not reckon(self):
                """
                To check some additional conditions for the token, say:
                if not self.is_in_code() and group in {'comment'}: ...
                """
                continue

            if self.rehighlight_block:
                if tag in self.tokens:
                    """
                    Opened tokens continue to apply for the following inline parts
                    Logic slightly differ apart with open-close tokens approach.
                    """
                    self.tokens[tag]['o'] = self.user_data.get_param(tag, 'within')

            """
            Regular Python regular expression operations instead of QRegularExpression, QRegularExpressionMatchIterator
            and QRegularExpressionMatch as sometimes it doesn't work properly.
            * https://docs.python.org/3/library/re.html
            * https://doc.qt.io/qt-6/qregularexpression.html
            """
            matches = re.finditer(pattern, text_str)

            for match in matches:
                # Get regex result position into the text string
                start = match.start(nth)
                end = match.end(nth)
                length = end - start

                # Collect line tokens only when any of them matched
                if tag not in self.line_tokens[self.line_number]:
                    self.line_tokens[self.line_number][tag] = []
                if tag != 'code' or tag not in self.get_nl_closing_tokens():
                    # The line tokens data will be reset after re-highlighting, no need to check for duplicates
                    line_token_data = {'start': start, 'end': end, 'length': length}
                    if line_token_data not in self.line_tokens[self.line_number][tag]:
                        self.line_tokens[self.line_number][tag].append(line_token_data)

                # Check if current tag should be skipped
                if ('codel' in self.line_tokens[self.line_number]
                        and self.line_tokens[self.line_number]['codel']
                        and group not in {'code', 'comment'}
                        and self.pos_within_inline_code(start, end, length)):
                    # skip formatting within inline code block
                    continue

                # Adjust previously processed matches (if rules order is not working)
                if ('codel' in self.line_tokens[self.line_number]
                        and group not in {'code', 'comment'}):
                    self.adjust_pos_within_inline_code()

                # Skip inline code block located within the multi-line code block
                if tag == 'codel' and self.is_in_code():
                    continue

                if tag not in {'code'}:
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

                # Comment """ block
                if tag == 'cclop' and self.is_in_code():
                    if 'o' not in self.tokens[tag]:
                        self.tokens[tag]['o'] = True
                    elif self.tokens[tag]['o']:
                        self.tokens[tag]['o'] = False
                    else:
                        self.tokens[tag]['o'] = True

                # Table
                if (tag == 'table_h'
                    and (self.line_number - 1 in self.line_tokens
                         # Previous token is a table header
                         and (self.line_number - 1 in self.line_tokens
                              and 'table_d' in self.line_tokens[self.line_number - 1])
                         # The token before the table header either a new line or file's first line
                         and ((self.line_number - 2 in self.line_tokens
                              and 'rn' in self.line_tokens[self.line_number - 2])
                              # line number "1" as table header token earliest line is next to "0"
                              or self.line_number == 1))):
                    self.tokens['table_d']['o'] = True
                    # It will be highlighted after the next re-highlight
                    if self.prev_user_data:
                        self.prev_user_data.put(tag='table_d', opened=True, within=True, closed=False)
                elif 'table_d' in self.tokens and self.tokens['table_d']['o'] and tag != 'table_d':
                    self.tokens['table_d']['o'] = False
                    if self.prev_user_data:
                        self.prev_user_data.put(tag='table_d', opened=False, within=True, closed=True)
                elif tag == 'table_d' and self.tokens['table_d']['o']:
                    self.user_data.put(tag=tag, opened=False, within=True, closed=False)
                if (group == 'table'
                        # Skip if not in table context yet
                        and not (self.user_data.get_param('table_d', 'within')
                                 or ('table_d' in self.tokens and self.tokens['table_d']['o']))):
                    self.logger.debug('Skipping table block')
                    continue
                # Not saving the block's data here;
                # it will be automatically stored during the next block re-highlighting iteration.

                # Header tags correction (emoji)
                if group == 'h':
                    if end == len(text_str):
                        length += 1

                # Prevent passing reference of the dict
                cfc = cf_data.copy()

                # Within the code block
                if self.is_in_code():
                    # Search whether line within code block or not
                    # or True in [True if x['in_code'] else False for x in self.line_tokens[self.line_number][tag]]):
                    if tag == 'code_lang':
                        cfc = self.theme['code_lang']
                    elif tag == 'code_indent':
                        cfc = self.theme['code_indent']
                    # Highlight the wrong indent when detected
                    elif tag == 'wrong_indent':
                        cfc = self.theme['wrong_indent']
                    # Comment (to avoid overriding with code formatting)
                    elif group == 'comment' or self.is_in_code_comment():
                        cfc = self.theme['comment']
                    # elif group == 'coop':
                    #    self.logger.debug('Code operator match', self.line_number_log, match.group(1),
                    #                      start, end, length)
                else:
                    # To avoid highlighting code lang or code text content when not in code
                    # Note: Closing code tag may appear here
                    if (group in {'code', 'comment'}
                            # Closing tag is a valid case
                            and not (tag == 'code'
                                     and self.prev_user_data
                                     and self.prev_user_data.get_param('code', 'within'))
                            # Code line is a valid case of a "not in a code block" tag here
                            and tag not in {'codel'}):
                        # self.logger.debug('Code tag "%s" (group "%s") at [%d] within a non-code context'
                        #                   % (tag, group, self.line_number_log))
                        continue
                    """
                    May causing "jumping" when formatted lines become unformatted,
                    most likely because of compete rules.
                    """
                    if (group == 'list' and not self.is_in_list()
                            # Or list indent is located within a blockquote
                            or tag == 'list_indent' and self.is_in_blockquote()):
                        continue
                    if group == 'blockquote' and not self.is_in_blockquote():
                        continue

                    """
                    Open-close tokens correction.
                    It happens because of matched block started from zero point or so,
                    which is from where the not included element starts, hence the correction.
                    Include optional element within the match brackets to get an actual start position.
                    """
                    if start != 0 and (group in oct_groups or group == 'code'):
                        # Regex's result from 2nd nth
                        if (tag == 'iu'
                                or tag == 'boo'
                                or tag == 'biu'):
                            # If the end of the line than add extra one
                            if end == len(text_str):
                                length += 1
                        elif (tag == 'code_lang' or tag == 'codel' or tag == 'codec'
                              or tag == 'i' or tag == 'i_open' or tag == 'iu_open'
                              or tag == 'b' or tag == 'b_open' or tag == 'boo_open'
                              or tag == 'bi' or tag == 'bi_open' or tag == 'biu_open'
                              or tag == 's' or tag == 's_open'
                              or tag == 'u' or tag == 'u_open'):
                            start = start
                        else:
                            start += 1

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
                E.g. match.captured(nth).encode('utf-8', 'replace').decode('utf-8').
                Also, check match.capturedTexts()
                """
                self.logger.debug(
                    'Tokens: "%s" > %s > %s (s:%d, l:%d, e:%d, n:%d)[%d] prev block state %d'
                    % (tag, self.tokens[tag], match.group(nth).encode('utf-8', 'replace'),
                       start, length, end, nth, self.line_number_log, self.previousBlockState()))

                """
                Inheriting a bg color of the blockquote.
                To keep an element's background use:
                and 'bg' not in cfc
                """
                if (self.is_in_blockquote()
                        and self.is_blockquote_inner(tag)
                        and 'bg' in self.theme['blockquote']):
                    cfc['bg'] = self.theme['blockquote']['bg_inner']

                # QTextCharFormat
                tc_fmt = self.cf(**cfc)
                if tc_fmt is not None:
                    if tag not in format_map:
                        format_map[tag] = []
                    # To apply it later when all line tokens are collected and adjusted
                    format_map[tag].append({'group': group, 'start': start, 'length': length, 'fmt': tc_fmt})

        for tag, fmt_data in format_map.items():
            if tag not in self.line_tokens[self.line_number]:
                continue
            for fd in fmt_data:
                self.setFormat(fd['start'], fd['length'], fd['fmt'])
                self.set_formatted(fd['group'])

        # TODO uncomment later when such block processing will be updated
        # # If within a comment and no other formatting except the comment
        # if self.is_in_code() and self.is_in_code_comment():
        #    self.setFormat(0, len(text_str), self.cf(**self.theme['comment']))
        #    self.set_formatted('comment')

        for token_data in self.get_open_close_token_map():
            """
            Process the lines located between the tags
            """
            # Not formatted elements within the multiline block
            if (not self.is_any_formatted()
                    and not self.is_in_code()
                    # TODO Check and refactor as one group replaces all the others
                    # and not self.is_group_formatted(token_data['group'])
                    and token_data['open'] in self.tokens
                    and self.tokens[token_data['open']]['o'] is True):
                self.setFormat(0, len(text_str), self.cf(**self.theme[token_data['theme']]))
                self.set_formatted(token_data['group'])

    def check_and_set_in_code_state(self):
        if self.is_in_code(True):
            self.logger.debug('In code context')
            if self.currentBlockState() != 1:
                self.setCurrentBlockState(1)
                return True
        else:
            if self.currentBlockState() == 1:
                self.setCurrentBlockState(0)
                return True
        return False

    def pos_within_inline_code(self, start, end, length):
        """
        Check if args position intersects with inline code block.
        """
        for _data in self.line_tokens[self.line_number]['codel']:
            if (_data['start'] < start < _data['end']
                    or _data['start'] < (start + length) < _data['end']
                    or _data['start'] < end < _data['end']):
                # skip formatting within inline code block
                return True

    def adjust_pos_within_inline_code(self) -> bool:
        processed_res = False
        data_to_del = {}
        for _tag, _tag_data in self.line_tokens[self.line_number].items():
            data_to_del[_tag] = []
            for _data in _tag_data:
                if self.pos_within_inline_code(_data['start'], _data['end'], _data['length']):
                    data_to_del[_tag].append(_data)
                    processed_res = True
        for _tag, _tag_data in data_to_del.items():
            for _data in _tag_data:
                self.line_tokens[self.line_number][_tag] = \
                    [d for d in self.line_tokens[self.line_number][_tag] if d != _data]
                if not self.line_tokens[self.line_number][_tag]:
                    del self.line_tokens[self.line_number][_tag]
        # self.logger.debug('Adjusted line tokens:', self.line_tokens[self.line_number])
        return processed_res

    # Check if within a code block
    def is_in_code(self, skip_data=False, force_tag=None):
        if (force_tag
                and force_tag in self.tokens
                and self.tokens[force_tag]['o'] is True):
            return True
        if (not force_tag
                and 'code' in self.tokens
                and self.tokens['code']['o'] is True):
            return True
        elif (not force_tag
              and 'codec' in self.tokens
              and self.tokens['codec']['o'] is True):
            return True
        elif (not skip_data
              and self.currentBlockState() == 1):
            return True
        elif (not skip_data
              and self.user_data is not None
              and self.user_data.get_param('code', 'within')):
            return True
        elif (not skip_data
              and self.user_data is not None
              and self.user_data.get_param('codec', 'within')):
            return True
        else:
            return False

    def is_in_code_comment(self):
        """
        Check if within a comment block
        """
        if ((('comment' in self.tokens and self.tokens['comment']['o'] is True)
             # One line comments
             or 'comment' in self.line_tokens[self.line_number])
                and self.is_in_code()):
            return True
        elif ('cclop' in self.tokens
              and self.tokens['cclop']['o'] is True
              and self.is_in_code()):
            return True
        else:
            return False

    def is_in_blockquote(self, skip_data=False):
        """
        Check if within a blockquote block
        """
        if ('blockquote' in self.tokens
                and self.tokens['blockquote']['o'] is True
                and not self.is_in_code()):
            return True
        elif self.user_data is not None and self.user_data.get_param('blockquote', 'within') and not skip_data:
            return True
        else:
            return False

    def is_in_list(self, skip_data=False):
        """
        Check if within a list
        """
        if ('list' in self.tokens
                and self.tokens['list']['o'] is True
                and not self.is_in_code()):
            return True
        elif self.user_data is not None and self.user_data.get_param('list', 'within') and not skip_data:
            return True
        else:
            return False
