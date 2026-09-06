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

from pygments.lexers import get_lexer_by_name
from pygments.token import Comment, Generic, Keyword, Name, Number, Operator, Punctuation, String
from pygments.util import ClassNotFound

from .main_highlighter import MainHighlighter
from . import TextBlockData

from typing import TYPE_CHECKING, Pattern

import re
import zlib

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

    # Keep edit-mode code highlighting deterministic and limited to common
    # languages. Pygments aliases are normalized here instead of guessing from
    # code, which can be expensive and surprising for an editor.
    code_lexer_aliases = {
        'bash': 'bash', 'console': 'console', 'sh': 'bash', 'shell': 'bash', 'zsh': 'bash',
        'c': 'c', 'h': 'c', 'cpp': 'cpp', 'c++': 'cpp', 'cc': 'cpp', 'hpp': 'cpp',
        'css': 'css', 'diff': 'diff', 'patch': 'diff', 'docker': 'docker', 'dockerfile': 'docker',
        'html': 'html', 'htm': 'html', 'ini': 'ini', 'javascript': 'javascript', 'js': 'javascript',
        'json': 'json', 'json5': 'json5', 'markdown': 'markdown', 'md': 'markdown',
        'php': 'php', 'python': 'python', 'py': 'python', 'sql': 'sql', 'toml': 'toml',
        'typescript': 'typescript', 'ts': 'typescript', 'xml': 'xml',
        'yaml': 'yaml', 'yml': 'yaml',
    }
    max_code_highlight_length = 200_000
    max_inline_highlight_length = 200_000
    escape_sensitive_tags = {
        'a', 'b', 'b_open', 'bi', 'bi_open', 'boo', 'boo_open',
        'biu', 'biu_open', 'html', 'i', 'i_open', 'img', 'iu',
        'iu_open', 's', 's_open', 'u', 'u_open',
    }
    closing_delimiter_lengths = {
        'b': 2, 'b_close': 2, 'bi': 3, 'bi_close': 3,
        'boo': 2, 'boo_close': 2, 'biu': 3, 'biu_close': 3,
        'i': 1, 'i_close': 1, 'iu': 1, 'iu_close': 1,
        's': 2, 's_close': 2, 'u': 4, 'u_close': 4,
    }
    block_container_prefix = (
        r'(?: {0,3}>[\t ]?)*'
        r'(?: {0,3}(?:[0-9]{1,9}[\.)]|[\*\+\-])[\t ]+)?'
    )

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
        (r'^((?: {0,3}>[\t ]?)+.*)$', 1, 'blockquote', 'blockquote', False, theme['blockquote'], None),
        # List
        (r'^((?: {0,3}>[\t ]?)*[\t ]*)([0-9]{1,9}[\.)]|[\*\+\-])(?=[\t ]+|$)',
         2, 'list', 'list', False, theme['list'], None),
        (r'^((?: {0,3}>[\t ]?)*[\t ]*)([0-9]{1,9}[\.)]|[\*\+\-])([\t ]+.*?)$',
         3, 'list_text', 'list', False, theme['list_text'], None),
        (r'^((?: {0,3}>[\t ]?)*[\t ]*)([0-9]{1,9}[\.)]|[\*\+\-])[\t ]+.*?$',
         1, 'list_indent', 'list', False, theme['list_indent'], None),
        # Fenced blocks are parsed statefully in highlightBlock(). Keep a
        # sentinel rule because the legacy inline pass expects the code group.
        (r'(?!)', 1, 'code', 'code', True, theme['code'], None),
        # Italic (asterisk)
        (r'(?<!\*)(\*(?![\s\*])(?:\\.|[^\*\\])*(?<!\s)\*)(?!\*)',
         1, 'i', 'i', False, theme['i'], None),  # between
        # \W to avoid character mention in a sequence like: *, ...
        (r'(^|\s)(\*[^\s\W\*][^\*]*?)(?!\*)$', 2, 'i_open', 'i', True, theme['i'], None),
        (r'^([^\*]+(?<!\s)\*)(?!\*)(?:\s|\W|$)', 1, 'i_close', 'i', True, theme['i'], None),
        # Italic (underline)
        # \W (non-word) characters are all characters apart from numbers, letters, and underscores.
        (r'(?<![\w_])(_(?![\s_])(?:\\.|[^_\\])*(?<!\s)_)(?![\w_])',
         1, 'iu', 'iu', False, theme['iu'], None),  # between
        (r'(^|[^\w_])(_[^\s\W_][^_]*?)$', 2, 'iu_open', 'iu', True, theme['iu'], None),
        (r'^([^_]*?(?<!_)[^\s_]_)(?!_)(?:\s|\W|$)', 1, 'iu_close', 'iu', True, theme['iu'], None),
        # Bold (asterisk)
        (r'(?<!\*)(\*{2}(?![\s\*])(?:\\.|[^\*\\]|\*(?!\*))*?(?<!\s)\*{2})(?!\*)',
         1, 'b', 'b', False, theme['b'], None),  # between
        (r'(^|\s)(\*{2}[^\s\*][^\*]*?)(?!\*)$', 2, 'b_open', 'b', True, theme['b'], None),
        (r'^([^\*]+(?<!\s)\*{2})(?!\*)(?:\s|\W|$)', 1, 'b_close', 'b', True, theme['b'], None),
        # Bold (underline)
        # \b doesn't work, only [^\s]
        (r'(?<![\w_])(__(?![\s_])(?:\\.|[^_\\]|_(?!_))*?(?<!\s)__)(?![\w_])',
         1, 'boo', 'boo', False, theme['boo'], None),  # between
        (r'(^|[^\w_])(__[^\s\W_][^_]*?)$', 2, 'boo_open', 'boo', True, theme['boo'], None),
        (r'^([^_]*?(?<!_)[^\s_]__)(?!__)(?:\s|\W|$)', 1, 'boo_close', 'boo', True, theme['boo'], None),
        # (r'(?<=__)([^\s].*?[^\s])(?=__)', 'b', 'b', 1, True, theme['b'], None),
        # Bold and Italic altogether (asterisk)
        (r'(?<!\*)(\*{3}(?![\s\*])(?:\\.|[^\*\\]|\*(?!\*)|\*{2}(?!\*))*?(?<!\s)\*{3})(?!\*)',
         1, 'bi', 'bi', False, theme['bi'], None),  # between
        (r'(^|\s)(\*{3}[^\s\*][^\*]*?)(?!\*)$', 2, 'bi_open', 'bi', True, theme['bi'], None),
        (r'^([^\*]+(?<!\s)\*{3})(?!\*)(?:\s|\W|$)', 1, 'bi_close', 'bi', True, theme['bi'], None),
        # Bold and Italic altogether (underline)
        (r'(?<![\w_])(___(?![\s_])(?:\\.|[^_\\]|_(?!_)|_{2}(?!_))*?(?<!\s)___)(?![\w_])',
         1, 'biu', 'biu', False, theme['biu'], None),  # between
        (r'(^|[^\w_])(___[^\s\W_][^_]*?)$', 2, 'biu_open', 'biu', True, theme['biu'], None),
        (r'^([^_]*?(?<!_)[^\s_]___)(?!___)(?:\s|\W|$)', 1, 'biu_close', 'biu', True, theme['biu'], None),
        # Strikethrough
        # ~~text~~ first to allow skip the open-close group as it may interference
        (r'(?<!~)(~~(?!~|\s)[^~]*?(?<!~|\s)~~)', 1, 's', 's', False, theme['s'], None),  # between
        (r'(^|\s)(?<!~~)(~~(?!~|\s)[^~]*?)$', 2, 's_open', 's', True, theme['s'], None),
        (r'^([^~]*?[^\s~]~~)(?!~~)(?:\s|[\W^~]|$)', 1, 's_close', 's', True, theme['s'], None),
        # Underline
        (r'(<u>.*?</u>)', 1, 'u', 'u', False, theme['u'], None),  # between
        (r'(<u>[^<>]*?)(?!</?u>)$', 1, 'u_open', 'u', True, theme['u'], None),
        (r'^([^<>]*?</u>)(?!</?u>)(?:\s|\W|$)', 1, 'u_close', 'u', True, theme['u'], None),
        # Code line within backticks
        # Inline code spans are parsed by delimiter-run length before the
        # remaining inline rules are evaluated.
        (r'(?!)', 1, 'codel', 'code', False, theme['codel'], None),
        # Header
        # (r'^(?:[\s\t]*?)(?<h1>#\s*?)(?<h1_text>.*)$', ['h1', 'h1_text'],
        # 'h1_text', 'h1', False, theme['h_text'], None),
        (rf'^{block_container_prefix}( {{0,3}}#)(?=[\t ]|$)',
         1, 'h1', 'h1', False, theme['h1'], None),
        (rf'^{block_container_prefix} {{0,3}}#[\t ]+(.*)$',
         1, 'h1_text', 'h1', False, theme['h1_text'], None),
        (rf'^{block_container_prefix}( {{0,3}}#{{2}})(?=[\t ]|$)',
         1, 'h2', 'h', False, theme['h2'], None),
        (rf'^{block_container_prefix} {{0,3}}#{{2}}[\t ]+(.*)$',
         1, 'h2_text', 'h', False, theme['h2_text'], None),
        (rf'^{block_container_prefix}( {{0,3}}#{{3}})(?=[\t ]|$)',
         1, 'h3', 'h', False, theme['h3'], None),
        (rf'^{block_container_prefix} {{0,3}}#{{3}}[\t ]+(.*)$',
         1, 'h3_text', 'h', False, theme['h3_text'], None),
        (rf'^{block_container_prefix}( {{0,3}}#{{4}})(?=[\t ]|$)',
         1, 'h4', 'h', False, theme['h4'], None),
        (rf'^{block_container_prefix} {{0,3}}#{{4}}[\t ]+(.*)$',
         1, 'h4_text', 'h', False, theme['h4_text'], None),
        (rf'^{block_container_prefix}( {{0,3}}#{{5}})(?=[\t ]|$)',
         1, 'h5', 'h', False, theme['h5'], None),
        (rf'^{block_container_prefix} {{0,3}}#{{5}}[\t ]+(.*)$',
         1, 'h5_text', 'h', False, theme['h5_text'], None),
        (rf'^{block_container_prefix}( {{0,3}}#{{6}})(?=[\t ]|$)',
         1, 'h6', 'h', False, theme['h6'], None),
        (rf'^{block_container_prefix} {{0,3}}#{{6}}[\t ]+(.*)$',
         1, 'h6_text', 'h', False, theme['h6_text'], None),
        # Table
        # Apply the structural separator last so its distinct style wins over
        # the deliberately broad table-row candidate.
        (r'^( {0,3}\|?.*\|.*\|?[\t ]*)$', 1, 'table_d', 'table', False, theme['table_d'], None),
        (r'^( {0,3}\|?[\t ]*:?-+:?[\t ]*(?:\|[\t ]*:?-+:?[\t ]*)+\|?[\t ]*)$',
         1, 'table_h', 'table', False, theme['table_h'], None),
        # Image
        (r'(!\[(?:\\.|[^\[\]\\]|\[(?:\\.|[^\[\]\\])*\])*\]\((?P<destination>'
         r'(?:<(?:\\.|[^<>\s\\])*>|(?:\\.|[^()\s\\]|\([^()\s]*\))*)'
         r'(?:[\t ]+(?:"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|\([^()]*\)))?[\t ]*)\))',
         1, 'img', 'img', False, theme['img'], None),
        (r'(?<!\\)(!\[(?:\\.|[^\[\]\\]|\[(?:\\.|[^\[\]\\])*\])*\]\[[^\]]*?\])',
         1, 'img', 'img', False, theme['img'], None),
        # reference either image or link, footnotes also
        (rf'^{block_container_prefix}( {{0,3}}\[(?:\\.|[^\]\\])+\]:)',
         1, 'ref', 'ref', False, theme['ref'], None),
        # (r'(\[[^\]]*?\]:)(\S*?)$', 2, 'ref_data', 'ref', False, theme['ref_data'], None),
        # abbreviations
        (r'^( {0,3}\*\[[^\]]+\]:)', 1, 'abbr', 'abbr', False, theme['abbr'], None),
        (r'^ {0,3}\*\[([^\]]+)\]:', 1, 'abbr_text', 'abbr', False, theme['abbr_text'], None),
        # hyperlinks (before the web links block to allow style overriding)
        (r'((?<!!)\[(?:\\.|[^\[\]\\]|\[(?:\\.|[^\[\]\\])*\])*\]\((?P<destination>'
         r'(?:<(?:\\.|[^<>\s\\])*>|(?:\\.|[^()\s\\]|\([^()\s]*\))*)'
         r'(?:[\t ]+(?:"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|\([^()]*\)))?[\t ]*)\))',
         1, 'a', 'a', False, theme['a'], None),
        # Scan URL candidates, then trim surrounding Markdown punctuation in
        # _url_end(). Query strings must not swallow link attributes or titles.
        (r'''(?<![\w])((?:https?|ftp)://[^\s<>{}"]+)''',
         1, 'link', 'link', False, theme['link'], None),
        # horizontal line
        (r'^(?: {0,3}>[\t ]?)*( {0,3}(?:(?:\*[\t ]*){3,}|(?:-[\t ]*){3,}|(?:_[\t ]*){3,}))$',
         1, 'hr', 'hr', False, theme['hr'], None),
        # Comments
        (r'^([\s\t]*?[#]{1,}\s*?.*)$', 1, 'comment', 'comment', False, theme['comment'],
         lambda s: s.is_in_code()),
        (r'^((?:\s*?)"""(?!").*?(?<!")""")(?:\s*?)$', 1, 'comment', 'comment', False, theme['comment'],
         lambda s: s.is_in_code()),
        (r'^(?:[\s\t]*?)(""")(?:[\s\t]*?)$', 1, 'cclop', 'comment', False, theme['comment'],
         lambda s: s.is_in_code()),
        (r'(\/\/.*?)$', 1, 'comment', 'comment', False, theme['comment'],
         lambda s: s.is_in_code()),
        # Inline HTML. Whitespace between '<' and the tag name is invalid;
        # accepting it makes ordinary comparisons such as "a < b > c" look
        # like markup.
        (r'(<[A-Za-z][A-Za-z0-9-]*(?:[\t ]+[A-Za-z_:][A-Za-z0-9_.:-]*'
         r'(?:[\t ]*=[\t ]*(?:"[^"]*"|\'[^\']*\'|[^\s"\'=<>`]+))?)*[\t ]*/?>)',
         1, 'html', 'html', False, theme['html_open'], None),
        (r'(</[A-Za-z][A-Za-z0-9-]*[\t ]*>)',
         1, 'html', 'html', False, theme['html_close'], None),
        (r'(?!)', 1, 'html_comment', 'html', False, theme['html_comment'], None),
        # emojis
        (r'(\:[a-zA-Z_]+\:)', 1, 'emoji', 'emoji', False, theme['emoji'], None),
        # To-do keywords
        (r'(?<![\w@])((?i:@todo))(?=\s|$|~~)', 1, 'todo', 'todo', False, theme['todo'], None),
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

    def get_regex(self, pattern: str) -> Pattern[str]:
        """
        Get either QRegularExpression or raw Python regex
        re = QRegularExpression(pattern)
        """
        return re.compile(pattern)

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
        return ['rn', 'blockquote', 'list']

    def cleanup_line_tokens(self):
        """
        Clean up old line_tokens to prevent memory leaks.
        Keep only a reasonable window of lines around the current position.
        """
        # Only cleanup when we have accumulated a significant number of entries
        token_count = len(self.line_tokens)
        if token_count > 1500:
            # Keep a window of 1000 lines centered around current position
            min_line_to_keep = max(0, self.line_number - 500)
            max_line_to_keep = self.line_number + 500
            # Collect keys to remove (avoid modifying dict during iteration)
            lines_to_remove = [
                line_num for line_num in self.line_tokens
                if line_num < min_line_to_keep or line_num > max_line_to_keep
            ]
            for line_num in lines_to_remove:
                del self.line_tokens[line_num]

    @staticmethod
    def _container_prefix(text_str: str, max_depth: int | None = None) -> tuple[int, int]:
        """Return the content offset and blockquote depth for a Markdown line."""
        offset = 0
        depth = 0
        prefix = re.compile(r' {0,3}>[\t ]?')
        while max_depth is None or depth < max_depth:
            match = prefix.match(text_str, offset)
            if match is None:
                break
            offset = match.end()
            depth += 1
        return offset, depth

    @staticmethod
    def _fence_state_id(state: dict) -> int:
        """Create a stable positive QTextBlock state for fence propagation."""
        value = '|'.join((
            state['fence_char'],
            str(state['fence_length']),
            state['language'],
            state.get('prefix', ''),
        ))
        return (zlib.crc32(value.encode('utf-8')) & 0x3fffffff) + 1

    @staticmethod
    def _utf16_offsets(text_str: str) -> list[int] | None:
        """Map Python string boundaries to the UTF-16 offsets expected by Qt."""
        if not any(ord(character) > 0xffff for character in text_str):
            return None

        offsets = [0]
        offset = 0
        for character in text_str:
            offset += 2 if ord(character) > 0xffff else 1
            offsets.append(offset)
        return offsets

    def _set_format(self, start: int, length: int, text_format, merge: bool = False) -> None:
        """Apply a Python-indexed source range to Qt's UTF-16 text layout."""
        text_length = len(self._format_text)
        start = min(max(start, 0), text_length)
        end = min(max(start + length, start), text_length)
        qt_start = self._format_offsets[start] if self._format_offsets is not None else start
        qt_end = self._format_offsets[end] if self._format_offsets is not None else end
        if merge:
            # Short overlays such as TODO markers keep the surrounding font
            # properties (including strikeout) while adding their own colors.
            for position in range(qt_start, qt_end):
                merged = self.format(position)
                merged.merge(text_format)
                super().setFormat(position, 1, merged)
            return
        super().setFormat(qt_start, qt_end - qt_start, text_format)

    @staticmethod
    def _url_end(text_str: str, start: int, end: int, explicit: bool = False) -> int:
        """Keep balanced URL parentheses/brackets, excluding outer markup."""
        stack = []
        for position in range(start, end):
            character = text_str[position]
            if character.isspace() or character in ('<', '>', '{', '}', '"'):
                end = position
                break
            if character in '([':
                stack.append(character)
            elif character in ')]':
                if not stack or stack[-1] != {')': '(', ']': '['}[character]:
                    end = position
                    break
                stack.pop()
        while not explicit and end > start and text_str[end - 1] in '.,;:!?':
            end -= 1
        # Apostrophes are valid URI characters. Only remove a final quote
        # when the surrounding text also supplied an opening quote; retain
        # apostrophes inside paths/queries and at explicit link boundaries.
        if start > 0 and text_str[start - 1] == "'" and end > start and text_str[end - 1] == "'":
            end -= 1
        return end

    def _url_matches(self, pattern, text_str: str):
        """Resume at each URL boundary, including adjacent linked images."""
        consumed = 0
        for scheme in re.finditer(r'(?<![\w])(?:https?|ftp)://', text_str):
            if scheme.start() < consumed:
                continue
            explicit = (scheme.start() > 0 and text_str[scheme.start() - 1] == '<') or any(
                start <= scheme.start() < end for start, end in self._link_syntax_ranges)
            end = self._url_end(text_str, scheme.start(), len(text_str), explicit=explicit)
            match = pattern.match(text_str, scheme.start(), end)
            if match is not None:
                yield match
            consumed = end

    def _collect_link_syntax(self, text_str: str) -> None:
        """Separate literal destinations/titles from labels and Extra attributes."""
        attributes = re.compile(r'''\{(?::)?(?:[^{}"'\r\n]|"[^"\r\n]*"|'[^'\r\n]*')*\}''')
        matches = (match for pattern, _, tag, *_ in self.rules if tag in ('a', 'img')
                   for match in pattern.finditer(text_str))
        for link in matches:
            if self._is_escaped(text_str, link.start()) or self._range_is_protected(link.start(), link.end()):
                continue
            if 'destination' in link.groupdict():
                self._link_syntax_ranges.append(link.span('destination'))
            match = attributes.match(text_str, link.end())
            if match is None or self._range_is_protected(match.start(), match.end()):
                continue
            start, end = match.span()
            self.line_tokens[self.line_number].setdefault('link_attrs', []).append(
                {'start': start, 'end': end, 'length': end - start})
            self._protected_ranges.append((start, end))

        url_pattern = next(pattern for pattern, _, tag, *_ in self.rules if tag == 'link')
        self._url_literal_ranges = [match.span(1) for match in self._url_matches(url_pattern, text_str)]

    def _list_match_is_valid(self, text_str: str, match) -> bool:
        """Distinguish contextual nested items from root indented code."""
        content_offset, _ = self._container_prefix(text_str)
        marker_start = match.start(2)
        indentation = text_str[content_offset:marker_start]
        indentation_width = len(indentation.expandtabs(4))
        if indentation_width <= 3:
            return True
        return bool(
            self.tokens.get('list', {}).get('o')
            or (self.user_data and self.user_data.get_param('list', 'within'))
            or (self.prev_user_data and self.prev_user_data.get_param('list', 'within'))
        )

    @classmethod
    def _extract_code_language(cls, info_string: str) -> str:
        """Extract a supported Pygments alias from a fence info string."""
        info_string = info_string.strip()
        if not info_string:
            return ''

        if info_string.startswith('{') and info_string.endswith('}'):
            attributes = info_string[1:-1].split()
            language = next((item[1:] for item in attributes if item.startswith('.')), '')
        else:
            language = info_string.split(maxsplit=1)[0].lstrip('.')

        return cls.code_lexer_aliases.get(language.casefold(), '')

    @staticmethod
    def _code_theme_key(token_type) -> str | None:
        """Map a Pygments token hierarchy to the existing Markdown theme."""
        if token_type in Comment:
            return 'comment'
        if token_type in Keyword:
            return 'coop4'
        if token_type in String:
            return 'coop2'
        if token_type in Number:
            return 'coop5'
        # Markdown lexers describe emphasis semantically. Reuse the editor's
        # inline emphasis styles, but keep the fenced content literal code.
        if token_type in Generic.EmphStrong:
            return 'bi'
        if token_type in Generic.Strong:
            return 'b'
        if token_type in Generic.Emph:
            return 'i'
        if token_type in Name.Function or token_type in Name.Class or token_type in Name.Tag:
            return 'coop3'
        if token_type in Name.Decorator or token_type in Name.Attribute:
            return 'coop3'
        if token_type in Operator or token_type in Punctuation:
            return 'coop1'
        return None

    def _highlight_code_syntax(self, text_str: str, language: str, offset: int = 0) -> None:
        """Apply language-aware Pygments tokens without retaining the source line."""
        if not language or len(text_str) > self.max_code_highlight_length:
            return

        if not hasattr(self, '_code_lexers'):
            self._code_lexers = {}
        try:
            lexer = self._code_lexers.get(language)
            if lexer is None:
                lexer_options = {
                    'stripnl': False,
                    'stripall': False,
                    'ensurenl': False,
                }
                # PHP fences conventionally omit ``<?php``. Pygments treats
                # such snippets as plain text unless inline mode is enabled.
                if language == 'php':
                    lexer_options['startinline'] = True
                lexer = get_lexer_by_name(language, **lexer_options)
                self._code_lexers[language] = lexer
        except ClassNotFound:
            return

        # QTextBlock omits its line separator. Some lexers, notably PHP,
        # finalize ``#`` and ``//`` comments only when they encounter a
        # newline. Add one for tokenization and clamp it out below.
        lexer_text = f'{text_str}\n'
        for start, token_type, value in lexer.get_tokens_unprocessed(lexer_text):
            if not value or (theme_key := self._code_theme_key(token_type)) is None:
                continue
            length = min(len(value), len(text_str) - start)
            if length <= 0:
                continue
            style = self.theme['code_content'].copy()
            style.update(self.theme[theme_key])
            self._set_format(offset + start, length, self.cf(**style))

    def _highlight_pseudo_fence(self, text_str: str) -> bool:
        """Highlight Notolog's legacy indented ``::::language`` block."""
        previous_state = getattr(self.prev_user_data, 'markdown_pseudo_fence', None)
        if previous_state:
            if not text_str:
                self.setCurrentBlockState(0)
                return False

            indentation = re.match(r'(?: {4,}|\t+)', text_str)
            content_offset = indentation.end() if indentation else 0
            self._set_format(0, len(text_str), self.cf(**self.theme['code_content']))
            if content_offset:
                self._set_format(0, content_offset, self.cf(**self.theme['code_indent']))
            self._highlight_code_syntax(
                text_str[content_offset:], previous_state['language'], content_offset,
            )
            self.user_data.markdown_pseudo_fence = previous_state
            self.user_data.put(
                tag='code', opened=False, within=True, closed=False,
                start=0, end=len(text_str),
            )
            self.setCurrentBlockState(self._fence_state_id(previous_state))
            self.set_formatted('code')
            return True

        opening = re.fullmatch(
            r'(?P<indent>(?: {4,}|\t+))(?P<marker>::::)(?P<info>\S*)[\t ]*',
            text_str,
        )
        if opening is None:
            return False
        if self.line_number and self.prev_block.text():
            return False

        info_string = opening.group('info')
        state = {
            'fence_char': ':',
            'fence_length': 4,
            'language': self._extract_code_language(info_string),
        }
        indent_start, indent_end = opening.span('indent')
        marker_start, marker_end = opening.span('marker')
        self.user_data.markdown_pseudo_fence = state
        self.user_data.put(
            tag='code', opened=True, within=True, closed=False,
            start=marker_start, end=marker_end,
        )
        self.line_tokens[self.line_number]['code_indent'] = [{
            'start': indent_start, 'end': indent_end, 'length': indent_end - indent_start,
        }]
        self.line_tokens[self.line_number]['code'] = [{
            'start': marker_start, 'end': marker_end, 'length': marker_end - marker_start,
        }]
        self._set_format(indent_start, indent_end - indent_start, self.cf(**self.theme['code_indent']))
        self._set_format(marker_start, marker_end - marker_start, self.cf(**self.theme['code']))
        if info_string:
            info_start, info_end = opening.span('info')
            self.line_tokens[self.line_number]['code_lang'] = [{
                'start': info_start, 'end': info_end, 'length': info_end - info_start,
            }]
            self._set_format(info_start, info_end - info_start, self.cf(**self.theme['code_lang']))
        self.setCurrentBlockState(self._fence_state_id(state))
        self.set_formatted('code')
        return True

    def _highlight_fenced_code(self, text_str: str) -> bool:
        """Highlight root and nested fences, preserving their container indentation."""
        previous_state = getattr(self.prev_user_data, 'markdown_fence', None)
        if previous_state:
            prefix = previous_state.get('prefix', '')
            if text_str.strip() and not text_str.startswith(prefix):
                # A dedented line ends the container, including an unfinished fence.
                previous_state = None
            else:
                offset = len(prefix) if text_str.startswith(prefix) else 0
                content = text_str[offset:]
                closing = re.fullmatch(
                    rf'{re.escape(previous_state["fence_char"])}'
                    rf'{{{previous_state["fence_length"]}}}[ ]*', content,
                )
                self._set_format(offset, len(content), self.cf(**self.theme['code_content']))
                if closing:
                    self._set_format(offset, len(content), self.cf(**self.theme['code']))
                    self.user_data.put(tag='code', opened=False, within=True, closed=True,
                                       start=offset, end=len(text_str))
                    self.setCurrentBlockState(0)
                else:
                    self._highlight_code_syntax(content, previous_state['language'], offset=offset)
                    self.user_data.markdown_fence = previous_state
                    self.user_data.put(tag='code', opened=False, within=True, closed=False,
                                       start=offset, end=len(text_str))
                    self.setCurrentBlockState(self._fence_state_id(previous_state))
                self.set_formatted('code')
                return True

        opening = re.fullmatch(
            r'([ \t]*(?:>[ \t]*)*)(`{3,}|~{3,})[ ]*('
            r'(?:\{[^\r\n]*\})|'
            r'(?:\.?[\w#.+-]+(?:[ ]+hl_lines=(?:"[^"]*"|\'[^\']*\'))?)?'
            r')[ ]*', text_str,
        )
        if opening is None:
            return False
        prefix, fence, info_string = opening.groups()
        offset = len(prefix)
        marker_end = offset + len(fence)
        state = {
            'prefix': prefix,
            'fence_char': fence[0],
            'fence_length': len(fence),
            'language': self._extract_code_language(info_string),
        }
        self.user_data.markdown_fence = state
        self.user_data.put(tag='code', opened=True, within=True, closed=False,
                           start=offset, end=marker_end)
        self._set_format(offset, len(fence), self.cf(**self.theme['code']))
        if info_string:
            self._set_format(marker_end, len(text_str) - marker_end, self.cf(**self.theme['code_lang']))
        self.setCurrentBlockState(self._fence_state_id(state))
        self.set_formatted('code')
        return True

    @staticmethod
    def _is_escaped(text_str: str, position: int) -> bool:
        backslashes = 0
        position -= 1
        while position >= 0 and text_str[position] == '\\':
            backslashes += 1
            position -= 1
        return backslashes % 2 == 1

    @classmethod
    def _backtick_runs(cls, text_str: str, start: int = 0):
        for match in re.finditer(r'`+', text_str[start:]):
            absolute_start = start + match.start()
            if not cls._is_escaped(text_str, absolute_start):
                yield absolute_start, start + match.end()

    def _highlight_inline_code(self, text_str: str) -> None:
        """Highlight exact-length CommonMark backtick delimiter pairs."""
        spans = []
        runs = list(self._backtick_runs(text_str))
        next_same_length = [None] * len(runs)
        next_by_length = {}
        for index in range(len(runs) - 1, -1, -1):
            start, end = runs[index]
            delimiter_length = end - start
            next_same_length[index] = next_by_length.get(delimiter_length)
            next_by_length[delimiter_length] = index

        run_index = 0
        while run_index < len(runs):
            opening_start, _ = runs[run_index]
            closing_index = next_same_length[run_index]
            if closing_index is None:
                run_index += 1
                continue
            _, closing_end = runs[closing_index]
            spans.append((opening_start, closing_end))
            run_index = closing_index + 1

        if not spans:
            return

        self.line_tokens[self.line_number]['codel'] = [
            {'start': start, 'end': end, 'length': end - start}
            for start, end in spans
        ]
        for start, end in spans:
            self._set_format(start, end - start, self.cf(**self.theme['codel']))
            self._protected_ranges.append((start, end))
        self.set_formatted('code')

    def _range_is_protected(self, start: int, end: int) -> bool:
        return any(range_start <= start and end <= range_end
                   for range_start, range_end in self._protected_ranges)

    def _delimiter_is_protected(self, start: int, end: int) -> bool:
        """Return whether either edge of a candidate is inside protected syntax."""
        return any(
            range_start <= start < range_end
            or range_start < end <= range_end
            for range_start, range_end in (
                *self._protected_ranges, *self._link_syntax_ranges, *self._url_literal_ranges)
        )

    def _restore_protected_formats(self) -> None:
        """Reapply nested code/comment styles after their parent styles."""
        for token_data in self.line_tokens[self.line_number].get('link_attrs', ()):
            self._set_format(token_data['start'], token_data['length'], self.cf(**self.theme['html']))
        for token_data in self.line_tokens[self.line_number].get('codel', ()):
            self._set_format(
                token_data['start'], token_data['length'],
                self.cf(**self.theme['codel']),
            )
        for token_data in self.line_tokens[self.line_number].get('html_comment', ()):
            self._set_format(
                token_data['start'], token_data['length'],
                self.cf(**self.theme['html_comment']),
            )

    def _highlight_html_comments(self, text_str: str) -> None:
        """Highlight HTML comments, including comments spanning text blocks."""
        spans = []
        content_offset, quote_depth = self._container_prefix(text_str)
        previous_state = getattr(self.prev_user_data, 'markdown_html_comment', None)
        previous_depth = (
            previous_state.get('quote_depth', 0)
            if isinstance(previous_state, dict) else 0
        )
        if previous_state and quote_depth < previous_depth:
            previous_state = None

        search_start = 0
        if previous_state:
            if previous_depth:
                content_offset, _ = self._container_prefix(text_str, previous_depth)
            else:
                content_offset = 0
            closing = text_str.find('-->', content_offset)
            if closing < 0:
                spans.append((content_offset, len(text_str)))
                self.user_data.markdown_html_comment = {
                    'quote_depth': previous_depth,
                }
                search_start = len(text_str)
            else:
                search_start = closing + 3
                spans.append((content_offset, search_start))

        while search_start < len(text_str):
            opening = text_str.find('<!--', search_start)
            if opening < 0:
                break
            if self._range_is_protected(opening, opening + 4):
                search_start = opening + 4
                continue
            closing = text_str.find('-->', opening + 4)
            if closing < 0:
                spans.append((opening, len(text_str)))
                self.user_data.markdown_html_comment = {
                    'quote_depth': quote_depth,
                }
                break
            spans.append((opening, closing + 3))
            search_start = closing + 3

        if not spans:
            return

        # HTML comments take precedence over Markdown code spans. Backticks in
        # a comment are literal, while a comment opener inside a code span was
        # already skipped above.
        code_spans = self.line_tokens[self.line_number].get('codel', [])
        if code_spans:
            code_spans = [
                token_data for token_data in code_spans
                if not any(
                    start <= token_data['start'] and token_data['end'] <= end
                    for start, end in spans
                )
            ]
            if code_spans:
                self.line_tokens[self.line_number]['codel'] = code_spans
            else:
                del self.line_tokens[self.line_number]['codel']
            self._protected_ranges = [
                (token_data['start'], token_data['end'])
                for token_data in code_spans
            ]
        self.line_tokens[self.line_number]['html_comment'] = [
            {'start': start, 'end': end, 'length': end - start}
            for start, end in spans
        ]
        for start, end in spans:
            self._set_format(start, end - start, self.cf(**self.theme['html_comment']))
            self._protected_ranges.append((start, end))
        self.set_formatted('html')

    def highlightBlock(self, text_str):  # noqa: C901 - consider simplifying this method
        """
        Apply a syntax highlighting to each line of the text.
        * https://doc.qt.io/qt-6/qsyntaxhighlighter.html#highlightBlock
        """

        # Regex and Pygments use Python code-point offsets, while Qt formatting
        # uses UTF-16 code units. Build one boundary map for this block.
        self._format_text = text_str
        self._format_offsets = self._utf16_offsets(text_str)

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
            Restore fenced-code state when a new text block appears.
            """
            if self.is_in_code(skip_data=True, force_tag='code'):
                self.user_data.put(tag='code', opened=False, within=True, closed=True)

        # A block may be highlighted repeatedly after edits. Replace its token
        # map so removed Markdown cannot leave stale parser context behind.
        self.line_tokens[self.line_number] = {}

        # Periodically clean up old line tokens to prevent memory leaks
        if self.line_number % 100 == 0:  # Check every 100 lines
            self.cleanup_line_tokens()

        # Each line is not formatted initially
        self.clear_formatted()
        self._protected_ranges = []
        self._link_syntax_ranges = []
        self._url_literal_ranges = []
        for state_attr in ('markdown_fence', 'markdown_pseudo_fence', 'markdown_html_comment'):
            if hasattr(self.user_data, state_attr):
                delattr(self.user_data, state_attr)
        self.user_data.drop('code')

        # Fences need their delimiter type, length, language and parent
        # blockquote context. QTextBlockUserData carries that state without
        # retaining document text or rescanning the entire document.
        if self._highlight_pseudo_fence(text_str) or self._highlight_fenced_code(text_str):
            self.current_block.setUserData(self.user_data)
            return

        # Markdown emphasis cannot continue across a paragraph boundary.
        # In particular, TODO overlays must not expose an unmatched italic
        # delimiter left open in a previous paragraph.
        if not text_str.strip():
            for tag in ('i_open', 'iu_open', 'b_open', 'boo_open', 'bi_open', 'biu_open'):
                if tag in self.tokens:
                    self.tokens[tag]['o'] = False

        # Avoid pathological regular-expression and token-storage costs for a
        # single enormous logical line. Block-state scans remain linear so a
        # following line can still recover correctly.
        if len(text_str) <= self.max_inline_highlight_length:
            self._highlight_inline_code(text_str)
        self._highlight_html_comments(text_str)
        if len(text_str) > self.max_inline_highlight_length:
            for state_tag in ('blockquote', 'list'):
                if state_tag in self.tokens:
                    self.tokens[state_tag]['o'] = False
            self.user_data.prune_inactive()
            self.current_block.setUserData(self.user_data)
            self.setCurrentBlockState(
                0x40000001 if getattr(self.user_data, 'markdown_html_comment', False) else 0)
            self._restore_protected_formats()
            return

        self._collect_link_syntax(text_str)

        # Python-Markdown keeps an unprefixed list item in the blockquote when
        # it continues a list which was opened inside that quote. This is the
        # structure used by the blockquote example in markdown-syntax.md.
        # Other unprefixed lines remain conservative because lazy paragraph
        # continuation requires more parser context than this line highlighter
        # retains.
        _, quote_depth = self._container_prefix(text_str)
        continues_quoted_list = (
            not quote_depth
            and self.tokens.get('list', {}).get('o') is True
            and re.match(r'^[\t ]*(?:[0-9]{1,9}[\.)]|[\*\+\-])(?=[\t ]+|$)', text_str)
        )
        if not quote_depth and not continues_quoted_list and 'blockquote' in self.tokens:
            self.tokens['blockquote']['o'] = False

        # Groups of tokens for correction
        oct_map = self.get_open_close_token_map()
        oct_groups = {r.get('group') for r in oct_map}
        open_tokens = {r.get('open') for r in oct_map}
        close_tokens = {r.get('close') for r in oct_map}
        nl_closing_tokens = set(self.get_nl_closing_tokens())

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
                self._set_format(0, len(text_str), self.cf(**self.theme['code_content']))
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
            * list
            Notice: Do not process it when located within a code block, like this:
            if self.is_in_code():
                continue
            Causing a "jumping" syntax, so better to leave the blocks within the code block
            but re-write their style accordingly.
            """
            if tag not in nl_closing_tokens:
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
            if match and tag == 'list' and not self._list_match_is_valid(text_str, match):
                match = None

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

                if ((tag in {'list'}
                     and (self.line_number == 0
                          # Check prev line is an empty line
                          or (self.line_number - 1 in self.line_tokens
                              and 'rn' in self.line_tokens[self.line_number - 1])))
                        # Blockquote and list may start without preliminary empty line
                        or not self.tokens[tag]['o']):
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
                        % (self.rehighlight_block, tag, self.line_number_log, self.is_in_code(),
                           self.previousBlockState())
                    )
                    """
                    Block tokens cannot be located on the same line, suppose to find them one per line
                    """
                    self.user_data.put(tag=tag, opened=False, within=True, closed=False)
                    if not self.is_any_formatted() and tag == 'blockquote':
                        self._set_format(0, len(text_str), self.cf(**self.theme['blockquote']))
                        self.set_formatted('blockquote')
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
        seen_line_tokens = {
            (tag, row['start'], row['end'])
            for tag, rows in self.line_tokens[self.line_number].items() for row in rows
        }
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
            matches = self._url_matches(pattern, text_str) if tag == 'link' else re.finditer(pattern, text_str)

            for match in matches:
                if group == 'list' and not self._list_match_is_valid(text_str, match):
                    continue
                # Get regex result position into the text string
                start = match.start(nth)
                end = match.end(nth)
                if tag == 'link' and any(
                        image['start'] <= start and end <= image['end']
                        for image in self.line_tokens[self.line_number].get('img', ())):
                    # An image destination keeps its image style, even when
                    # the image itself is the label of a clickable link.
                    continue
                length = end - start

                if self._range_is_protected(start, end):
                    continue
                if (group in {'i', 'iu', 'b', 'boo', 'bi', 'biu', 's', 'u', 'a', 'img', 'html'}
                        and self._delimiter_is_protected(start, end)):
                    continue
                if (tag in self.escape_sensitive_tags
                        and self._is_escaped(text_str, start)):
                    continue
                if (delimiter_length := self.closing_delimiter_lengths.get(tag)) is not None:
                    if self._is_escaped(text_str, end - delimiter_length):
                        continue

                # Collect line tokens only when any of them matched
                if tag not in self.line_tokens[self.line_number]:
                    self.line_tokens[self.line_number][tag] = []
                if tag != 'code' or tag not in nl_closing_tokens:
                    # Constant-time deduplication keeps dense emphasis lines
                    # from performing a growing list scan for every token.
                    line_token_data = {'start': start, 'end': end, 'length': length}
                    token_key = (tag, start, end)
                    if token_key not in seen_line_tokens:
                        seen_line_tokens.add(token_key)
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
                         and 'table_d' in self.line_tokens[self.line_number - 1])):
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
                        if tag in {'iu', 'boo', 'biu'}:
                            # If the end of the line than add extra one
                            if end == len(text_str):
                                length += 1
                        elif tag not in {'code_lang', 'codel',
                                         'i', 'i_open', 'iu_open',
                                         'b', 'b_open', 'boo_open',
                                         'bi', 'bi_open', 'biu_open',
                                         's', 's_open',
                                         'u', 'u_open'}:
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
                if tag in ('todo', 'a'):
                    cfc.setdefault('font_size_ratio', 0)
                tc_fmt = self.cf(**cfc)
                if tc_fmt is not None:
                    if tag not in format_map:
                        format_map[tag] = []
                    # To apply it later when all line tokens are collected and adjusted
                    format_map[tag].append({'group': group, 'start': start, 'length': length, 'fmt': tc_fmt})

        for tag, fmt_data in format_map.items():
            if tag == 'todo' or tag not in self.line_tokens[self.line_number]:
                continue
            for fd in fmt_data:
                self._set_format(fd['start'], fd['length'], fd['fmt'], merge=tag == 'a')
                self.set_formatted(fd['group'])

        # TODO uncomment later when such block processing will be updated
        # # If within a comment and no other formatting except the comment
        # if self.is_in_code() and self.is_in_code_comment():
        #    self.setFormat(0, len(text_str), self.cf(**self.theme['comment']))
        #    self.set_formatted('comment')

        for token_data in oct_map:
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
                self._set_format(0, len(text_str), self.cf(**self.theme[token_data['theme']]))
                self.set_formatted(token_data['group'])

        # Outer link formatting must not overwrite a nested image's style.
        for fd in format_map.get('img', []):
            self._set_format(fd['start'], fd['length'], fd['fmt'])

        # Overlay TODO colors after both inline and multiline font styling.
        for fd in format_map.get('todo', []):
            self._set_format(fd['start'], fd['length'], fd['fmt'], merge=True)
            self.set_formatted(fd['group'])

        if getattr(self.user_data, 'markdown_html_comment', False):
            self.setCurrentBlockState(0x40000001)

        self.user_data.prune_inactive()
        self._restore_protected_formats()

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
            if _data['start'] <= start and end <= _data['end']:
                # skip formatting within inline code block
                return True
        return False

    def adjust_pos_within_inline_code(self) -> bool:
        processed_res = False
        data_to_del = {}
        for _tag, _tag_data in self.line_tokens[self.line_number].items():
            if _tag == 'codel':
                continue
            data_to_del[_tag] = []
            for _data in _tag_data:
                if self.pos_within_inline_code(_data['start'], _data['end'], _data['length']):
                    data_to_del[_tag].append(_data)
                    processed_res = True
        # Remove entries in-place to avoid creating new lists
        tags_to_remove = []
        for _tag, _tag_data in data_to_del.items():
            if _tag_data:
                for _data in _tag_data:
                    self.line_tokens[self.line_number][_tag].remove(_data)
                # Mark empty tags for removal
                if not self.line_tokens[self.line_number][_tag]:
                    tags_to_remove.append(_tag)
        # Clean up empty tag entries
        for _tag in tags_to_remove:
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
        elif (not skip_data
              and self.currentBlockState() == 1):
            return True
        elif (not skip_data
              and self.user_data is not None
              and self.user_data.get_param('code', 'within')):
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
