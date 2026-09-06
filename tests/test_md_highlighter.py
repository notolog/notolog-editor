"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Tests CommonMark boundaries and fenced-code syntax highlighting.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtGui import QColor, QTextCursor, QTextDocument
from pygments.token import Comment, Generic, Keyword, Name, Number, String

from notolog.highlight.md_highlighter import MdHighlighter

import pytest
import markdown


class TestMdHighlighter:

    @pytest.mark.parametrize('source', [
        '[page](https://example.com/_part)',
        '![image](https://example.com/_part.png)',
        '[page](local/_part)',
        '[page](https://example.com/path "_title")',
        'https://example.com/_part',
    ])
    def test_destination_syntax_does_not_open_emphasis(self, highlighter, source):
        self.highlight(highlighter, source + '\nplain following text')
        assert not highlighter.tokens.get('iu_open', {}).get('o')
        assert all(not r.format.fontItalic() for r in highlighter.document().lastBlock().layout().formats())

    @pytest.mark.parametrize('suffix', ['?', '.', ',', ';', ':', '!', "'"])
    @pytest.mark.parametrize('wrapper', ['[page]({url})', '<{url}>'])
    def test_explicit_urls_preserve_terminal_characters(self, highlighter, suffix, wrapper):
        url = 'https://example.com/path' + suffix
        source = wrapper.format(url=url)
        self.highlight(highlighter, source)
        token = highlighter.line_tokens[0]['link'][0]
        assert source[token['start']:token['end']] == url

    def test_theme_overrides_are_private_to_each_highlighter(self, qapp, mocker):
        from notolog.helpers.theme_helper import ThemeHelper
        get_color = mocker.patch.object(ThemeHelper, 'get_color', return_value=None)
        get_color.side_effect = lambda key, **kwargs: 'magenta' if key == 'md_color_a' else None
        first_doc = QTextDocument()
        first = MdHighlighter(first_doc)
        get_color.side_effect = lambda key, **kwargs: 'blue' if key == 'md_color_a' else None
        second_doc = QTextDocument()
        second = MdHighlighter(second_doc)
        assert first.theme['a']['color'] == 'magenta'
        assert second.theme['a']['color'] == 'blue'
        self.highlight(first, '[label](local)')
        assert self.foreground_at(first_doc.firstBlock(), 1) == QColor('magenta')
        first.setDocument(None)
        second.setDocument(None)

    def test_dense_emphasis_line_keeps_all_tokens(self, highlighter):
        source = '*a' * 50000
        self.highlight(highlighter, source)
        tokens = highlighter.line_tokens[0]['i']
        assert len(tokens) == 25000
        assert tokens[-1] == {'start': 99996, 'end': 99999, 'length': 3}

    def test_literal_destination_preserves_emphasis_in_link_label(self, highlighter):
        self.highlight(highlighter, '[*label*](https://example.com/_path)')
        assert 'i' in highlighter.line_tokens[0]
        assert not highlighter.tokens.get('iu_open', {}).get('o')
        formats = highlighter.document().firstBlock().layout().formats()
        assert next(r.format for r in formats if r.start <= 2 < r.start + r.length).fontItalic()

    @pytest.mark.parametrize('source, destinations', [
        ('![Example badge](https://example.com/badge.svg?color=green)', []),
        ('[Example link](https://example.org/page)', ['https://example.org/page']),
        ('[![Example badge](https://example.com/badge.svg)](https://example.org/page)',
         ['https://example.org/page']),
        ('[![First](https://example.com/one.svg)](https://example.org/one)'
         '[![Second](https://example.com/two.svg?color=green)](https://example.org/two)',
         ['https://example.org/one', 'https://example.org/two']),
        ('😀 [![Badge](badge.svg)](https://example.org/page)', ['https://example.org/page']),
    ])
    def test_images_and_link_destinations_have_distinct_styles(self, highlighter, source, destinations):
        self.highlight(highlighter, source)
        tokens = highlighter.line_tokens[0]
        assert len(tokens.get('img', [])) == source.count('![')
        assert [source[t['start']:t['end']] for t in tokens.get('link', [])] == destinations
        block = highlighter.document().firstBlock()
        for token in tokens.get('img', []):
            position = self.utf16_position(source, token['start'])
            assert self.foreground_at(block, position) == QColor(highlighter.theme['img']['color'])
            position = self.utf16_position(source, token['end'] - 2)
            assert self.foreground_at(block, position) == QColor(highlighter.theme['img']['color'])
        for token in tokens.get('link', []):
            position = self.utf16_position(source, token['start'])
            assert self.foreground_at(block, position) == QColor(highlighter.theme['link']['color'])

    def test_url_scanner_keeps_nested_parentheses_and_embedded_urls(self, highlighter):
        url = 'https://example.com/a_(b_(c))?next=https://example.org/page'
        self.highlight(highlighter, f'[{url}]')
        assert highlighter.line_tokens[0]['link'] == [{'start': 1, 'end': len(url) + 1, 'length': len(url)}]

    @pytest.mark.parametrize('source, url', [
        ("https://example.com/it's-valid", "https://example.com/it's-valid"),
        ("https://example.com/?name=it's-valid#part'one", "https://example.com/?name=it's-valid#part'one"),
        ("https://example.com/trailing'", "https://example.com/trailing'"),
        ("[page](https://example.com/trailing')", "https://example.com/trailing'"),
        ("<https://example.com/trailing'>", "https://example.com/trailing'"),
        ("'https://example.com/it's-valid'", "https://example.com/it's-valid"),
        ("See 'https://example.com/page'.", "https://example.com/page"),
        ('[page](https://example.com/it\'s-valid "Title"){:target="_blank"}',
         "https://example.com/it's-valid"),
        ("[page](https://example.com/path 'Title')", "https://example.com/path"),
        ('https://example.com/it%27s-valid', 'https://example.com/it%27s-valid'),
        ('[items](https://example.com/items?category=sample){:target="_blank"}',
         'https://example.com/items?category=sample'),
        ('[section](https://example.com/page#part){.external}', 'https://example.com/page#part'),
        ('[page](https://example.com/path "title")', 'https://example.com/path'),
        ('<https://example.com/?q=one>', 'https://example.com/?q=one'),
        ('See https://example.com/wiki/Thing_(example).', 'https://example.com/wiki/Thing_(example)'),
        ('(https://example.com/?q=(example))', 'https://example.com/?q=(example)'),
        ('https://[::1]:8080/path', 'https://[::1]:8080/path'),
    ])
    def test_url_style_stops_at_markdown_boundaries(self, highlighter, source, url):
        self.highlight(highlighter, source)
        token = highlighter.line_tokens[0]['link'][0]
        assert source[token['start']:token['end']] == url

    def test_link_attributes_do_not_start_italic(self, highlighter):
        source = '- [Example items](https://example.com/items?category=sample){:target="_blank"}'
        self.highlight(highlighter, source + '\nplain following text')
        token = highlighter.line_tokens[0]['link_attrs'][0]
        assert source[token['start']:token['end']] == '{:target="_blank"}'
        block = highlighter.document().firstBlock()
        position = source.index('_blank')
        formats = block.layout().formats()
        fmt = next(r.format for r in formats if r.start <= position < r.start + r.length)
        assert not fmt.fontItalic()
        assert fmt.foreground() == highlighter.cf(**highlighter.theme['html']).foreground()
        assert not highlighter.tokens.get('iu_open', {}).get('o')
        assert all(not r.format.fontItalic() for r in highlighter.document().lastBlock().layout().formats())

    @pytest.mark.parametrize('opening', ['*unfinished', '_unfinished', '**unfinished', '__unfinished'])
    @pytest.mark.parametrize('blank', ['', '   '])
    def test_emphasis_does_not_leak_into_todo_paragraph(self, highlighter, opening, blank):
        self.highlight(highlighter, f'{opening}\n{blank}\n@TODO plain text')
        block = highlighter.document().lastBlock()
        for fmt_range in block.layout().formats():
            assert not fmt_range.format.fontItalic()
            assert fmt_range.format.fontWeight() < 700
        assert 'todo' in highlighter.line_tokens[2]

    def test_todo_preserves_intended_multiline_italic(self, highlighter):
        self.highlight(highlighter, '*start\n@TODO continued\nend*')
        block = highlighter.document().findBlockByNumber(1)
        assert all(r.format.fontItalic() for r in block.layout().formats())

    @pytest.mark.parametrize('marker', ['@todo', '@TODO', '@ToDo'])
    @pytest.mark.parametrize('source', [
        '{marker}', '😀 {marker} next', '~~done {marker}~~',
        '~~done {marker} next~~', '~~start\n{marker} next\nend~~',
    ])
    def test_todo_case_and_strikethrough(self, highlighter, marker, source):
        source = source.format(marker=marker)
        self.highlight(highlighter, source)
        block = highlighter.document().find(marker).block()
        position = self.utf16_position(block.text(), block.text().index(marker))
        ranges = block.layout().formats()
        fmt = next(r.format for r in ranges if r.start <= position < r.start + r.length)
        assert fmt.background() == highlighter.cf(**highlighter.theme['todo']).background()
        assert fmt.fontStrikeOut() == source.startswith('~~')

    @pytest.mark.parametrize('source', ['name@TODO next', '@@TODO next', '@TODOS next', '`@TODO`'])
    def test_todo_boundaries_and_code(self, highlighter, source):
        self.highlight(highlighter, source)
        assert not highlighter.line_tokens[0].get('todo')

    def test_todo_preserves_heading_font(self, highlighter):
        self.highlight(highlighter, '# Title @TODO next')
        block = highlighter.document().firstBlock()
        formats = block.layout().formats()
        def at(position):
            return next(r.format for r in formats if r.start <= position < r.start + r.length)
        assert at(8).fontPointSize() == at(2).fontPointSize()
        assert at(8).fontWeight() == at(2).fontWeight()

    @pytest.fixture(scope='function')
    def highlighter(self, qapp):
        document = QTextDocument()
        highlighter = MdHighlighter(document=document)
        yield highlighter
        highlighter.setDocument(None)

    @staticmethod
    def highlight(highlighter, source):
        highlighter.document().setPlainText(source)
        highlighter.rehighlight()
        return highlighter

    @staticmethod
    def block(document, number):
        return document.findBlockByNumber(number)

    @staticmethod
    def foreground_at(block, position):
        for format_range in reversed(block.layout().formats()):
            if format_range.start <= position < format_range.start + format_range.length:
                foreground = format_range.format.foreground()
                if foreground.style():
                    return foreground.color()
        return QColor()

    @staticmethod
    def background_at(block, position):
        for format_range in reversed(block.layout().formats()):
            if format_range.start <= position < format_range.start + format_range.length:
                background = format_range.format.background()
                if background.style():
                    return background.color()
        return QColor()

    @staticmethod
    def utf16_position(source, position):
        return len(source[:position].encode('utf-16-le')) // 2

    def test_replacing_fence_with_large_line_resets_following_blocks(self, highlighter):
        self.highlight(highlighter, '```python\n# heading')
        document = highlighter.document()
        cursor = QTextCursor(document.firstBlock())
        cursor.select(QTextCursor.SelectionType.BlockUnderCursor)
        cursor.insertText('x' * (highlighter.max_inline_highlight_length + 1))
        highlighter.rehighlightBlock(document.firstBlock())
        assert document.firstBlock().userState() == 0
        assert not hasattr(document.lastBlock().userData(), 'markdown_fence')
        assert 'h1' in highlighter.line_tokens[1]

    @pytest.mark.parametrize('text, limit, expected', [
        (' > > text', None, (5, 2)),
        (' > > text', 1, (3, 1)),
        ('    > text', None, (0, 0)),
        ('>' * 10000 + 'text', None, (10000, 10000)),
    ])
    def test_container_prefix_boundaries(self, text, limit, expected):
        assert MdHighlighter._container_prefix(text, limit) == expected

    @pytest.mark.parametrize('source', [
        '```python\nprint(1)\n```',
        '~~~python\nprint(1)\n~~~',
        '````python\nprint(1)\n````',
        '``` {.python}\nprint(1)\n```',
        '```python hl_lines="1"\nprint(1)\n```',
        '> ```python\n> print(1)\n> ```',
        ' ```python\n print(1)\n ```',
        '```python invalid\nprint(1)\n```',
    ])
    def test_complete_fence_classification_matches_renderer(self, highlighter, source):
        from notolog.fenced_code_extension import NestedFencesExtension
        html = markdown.markdown(source, extensions=['extra', NestedFencesExtension()])
        self.highlight(highlighter, source)
        edit_fence = hasattr(highlighter.document().firstBlock().userData(), 'markdown_fence')
        assert edit_fence == ('<pre' in html)

    @pytest.mark.parametrize('source', [
        '#heading',
        '####### heading',
        '    # indented paragraph',
    ])
    def test_rejects_invalid_atx_headings(self, highlighter, source):
        self.highlight(highlighter, source)

        assert not any(tag.startswith('h') for tag in highlighter.line_tokens[0])

    def test_accepts_heading_inside_blockquote(self, highlighter):
        self.highlight(highlighter, '> ## quoted heading')

        assert 'blockquote' in highlighter.line_tokens[0]
        assert 'h2' in highlighter.line_tokens[0]
        assert 'h2_text' in highlighter.line_tokens[0]

    def test_unprefixed_list_item_continues_list_inside_blockquote(self, highlighter):
        source = (
            '> #### Also, multiline syntax is supported\n'
            '>\n'
            '> * First quoted item\n'
            '> * Second quoted item\n'
            '>\n'
            '* Unprefixed continuation item'
        )
        self.highlight(highlighter, source)
        final_block = self.block(highlighter.document(), 5)

        assert final_block.userData().get_param('blockquote', 'within') is True
        assert final_block.userData().get_param('list', 'within') is True
        assert self.background_at(final_block, 0) != QColor()

    def test_blank_line_ends_blockquote_before_list(self, highlighter):
        self.highlight(highlighter, '> * Quoted item\n\n* Outside item')
        outside_block = self.block(highlighter.document(), 2)

        assert outside_block.userData().get_param('blockquote', 'within') is not True
        assert outside_block.userData().get_param('list', 'within') is True

    @pytest.mark.parametrize('source', [
        '- # list heading',
        '> - ## quoted list heading',
    ])
    def test_accepts_heading_inside_list_containers(self, highlighter, source):
        self.highlight(highlighter, source)

        assert 'list' in highlighter.line_tokens[0]
        assert any(tag.startswith('h') for tag in highlighter.line_tokens[0])

    @pytest.mark.parametrize('source, expected', [
        ('* * *', True),
        ('---', True),
        ('_\t_\t_', True),
        ('-*_', False),
        ('--', False),
        ('    ---', False),
    ])
    def test_thematic_break_requires_matching_markers(self, highlighter, source, expected):
        self.highlight(highlighter, source)

        assert ('hr' in highlighter.line_tokens[0]) is expected

    def test_table_separator_does_not_require_outer_pipes_or_blank_line(self, highlighter):
        self.highlight(highlighter, 'Name | Value\n--- | ---\nA | 1')

        assert 'table_d' in highlighter.line_tokens[0]
        assert 'table_h' in highlighter.line_tokens[1]
        assert 'table_d' in highlighter.line_tokens[2]

    def test_table_separator_keeps_distinct_visual_style(self, highlighter):
        self.highlight(highlighter, 'Name | Value\n--- | ---\nA | 1')
        document = highlighter.document()

        assert self.background_at(self.block(document, 1), 0) == QColor(
            highlighter.theme['table_h']['bg']['color']
        )
        assert self.background_at(self.block(document, 2), 0) == QColor(
            highlighter.theme['table_d']['bg']['color']
        )

    def test_inline_code_uses_equal_length_delimiters_and_protects_content(self, highlighter):
        self.highlight(highlighter, '``code with ` and *marker*`` then *italic*')

        code_span = highlighter.line_tokens[0]['codel'][0]
        assert code_span == {'start': 0, 'end': 28, 'length': 28}
        assert all(token['start'] >= 34 for token in highlighter.line_tokens[0]['i'])

    @pytest.mark.parametrize('source, outer_tag', [
        ('*before `code` after*', 'i'),
        ('[label `code`](target)', 'a'),
    ])
    def test_inline_code_can_be_nested_in_outer_inline_markup(self, highlighter, source, outer_tag):
        self.highlight(highlighter, source)

        assert outer_tag in highlighter.line_tokens[0]
        assert 'codel' in highlighter.line_tokens[0]
        code_start = highlighter.line_tokens[0]['codel'][0]['start']
        assert self.foreground_at(highlighter.document().firstBlock(), code_start) == QColor(
            highlighter.theme['codel']['color']
        )

    def test_inline_code_inside_heading_keeps_its_code_style(self, highlighter):
        source = '### Bold `+` Italic'
        self.highlight(highlighter, source)

        code_start = self.utf16_position(source, source.index('`'))
        assert self.foreground_at(highlighter.document().firstBlock(), code_start) == QColor(
            highlighter.theme['codel']['color']
        )

    def test_delimiter_inside_inline_code_cannot_close_emphasis(self, highlighter):
        self.highlight(highlighter, '*outside `inside*`')

        assert 'i' not in highlighter.line_tokens[0]

    def test_backticks_inside_html_comment_are_literal(self, highlighter):
        self.highlight(highlighter, '<!-- `not code` -->')

        assert 'html_comment' in highlighter.line_tokens[0]
        assert 'codel' not in highlighter.line_tokens[0]

    def test_escaped_and_unpaired_backticks_remain_plain_text(self, highlighter):
        self.highlight(highlighter, r'\`escaped\` and `unclosed')

        assert 'codel' not in highlighter.line_tokens[0]

    def test_backslash_escaped_inline_markers_remain_plain_text(self, highlighter):
        self.highlight(highlighter, r'\*plain* \[label](url) \<span> \</span> \<u>plain\</u>')

        assert 'i' not in highlighter.line_tokens[0]
        assert 'a' not in highlighter.line_tokens[0]
        assert 'html' not in highlighter.line_tokens[0]
        assert 'u' not in highlighter.line_tokens[0]

    def test_even_backslashes_do_not_escape_emphasis(self, highlighter):
        self.highlight(highlighter, r'\\*emphasis*')

        assert highlighter.line_tokens[0]['i'] == [
            {'start': 2, 'end': 12, 'length': 10},
        ]

    def test_escaped_closing_delimiter_does_not_end_emphasis(self, highlighter):
        self.highlight(highlighter, r'*plain\*')

        assert 'i' not in highlighter.line_tokens[0]

    @pytest.mark.parametrize('source, tag', [
        ('* space before close *', 'i'),
        ('** space before close **', 'b'),
        ('*** space before close ***', 'bi'),
    ])
    def test_whitespace_cannot_touch_emphasis_delimiters(self, highlighter, source, tag):
        self.highlight(highlighter, source)

        assert tag not in highlighter.line_tokens[0]

    def test_escaped_asterisk_can_appear_inside_emphasis(self, highlighter):
        self.highlight(highlighter, r'*an escaped \* marker*')

        assert highlighter.line_tokens[0]['i'] == [
            {'start': 0, 'end': 22, 'length': 22},
        ]

    @pytest.mark.parametrize('source, tag', [
        ('(_italic_)', 'iu'),
        ('[__bold__]', 'boo'),
        ('{___both___}', 'biu'),
    ])
    def test_underscore_emphasis_accepts_punctuation_boundaries(
            self, highlighter, source, tag):
        self.highlight(highlighter, source)

        assert tag in highlighter.line_tokens[0]

    @pytest.mark.parametrize('source, tag', [
        ('word_inside_word', 'iu'),
        ('word__inside__word', 'boo'),
        ('word___inside___word', 'biu'),
    ])
    def test_underscore_emphasis_rejects_intraword_delimiters(
            self, highlighter, source, tag):
        self.highlight(highlighter, source)

        assert tag not in highlighter.line_tokens[0]

    @pytest.mark.parametrize('source, expected', [
        ('[label](path/to/file)', True),
        ('[label](path_(nested))', True),
        ('[label](<path/to/file>)', True),
        ('[label](path "Title")', True),
        ('[outer [inner]](path)', True),
        ('[label](path with spaces)', False),
    ])
    def test_inline_link_destination_boundaries(self, highlighter, source, expected):
        self.highlight(highlighter, source)

        assert ('a' in highlighter.line_tokens[0]) is expected

    @pytest.mark.parametrize('destination', ['guide.md', 'https://example.com/guide'])
    @pytest.mark.parametrize('title', ['', ' "Example title"'])
    def test_local_and_titled_links_keep_label_style(self, highlighter, destination, title):
        source = f'[Guide]({destination}{title})'
        self.highlight(highlighter, source)
        assert highlighter.line_tokens[0]['a'] == [{'start': 0, 'end': len(source), 'length': len(source)}]
        assert self.foreground_at(highlighter.document().firstBlock(), 1) == QColor(highlighter.theme['a']['color'])

    def test_definitions_only_match_at_block_start(self, highlighter):
        self.highlight(highlighter, 'prose [label]: target and *[HTML]: expansion')

        assert 'ref' not in highlighter.line_tokens[0]
        assert 'abbr' not in highlighter.line_tokens[0]

    def test_reference_definition_inside_blockquote(self, highlighter):
        self.highlight(highlighter, '> [label]: target')

        assert 'blockquote' in highlighter.line_tokens[0]
        assert 'ref' in highlighter.line_tokens[0]

    def test_todo_requires_a_word_boundary(self, highlighter):
        self.highlight(highlighter, 'name@todo no; @todo yes')

        assert highlighter.line_tokens[0]['todo'] == [
            {'start': 14, 'end': 19, 'length': 5},
        ]

    @pytest.mark.parametrize('source, expected', [
        ('1. item', True),
        ('1) item', True),
        ('123456789. item', True),
        ('1234567890. item', False),
        ('    - paragraph continuation', False),
    ])
    def test_list_marker_boundaries(self, highlighter, source, expected):
        self.highlight(highlighter, source)

        assert ('list' in highlighter.line_tokens[0]) is expected

    def test_nested_list_items_keep_marker_text_and_indent_tokens(self, highlighter):
        self.highlight(
            highlighter,
            '* Some\n    * Random\n        * Text\n\n1. One\n\t2. Two\n\t\t3. Three',
        )

        for line_number in (0, 1, 2, 4, 5, 6):
            assert 'list' in highlighter.line_tokens[line_number]
            assert 'list_text' in highlighter.line_tokens[line_number]
        assert highlighter.line_tokens[1]['list_indent'] == [
            {'start': 0, 'end': 4, 'length': 4},
        ]
        assert highlighter.line_tokens[2]['list_indent'] == [
            {'start': 0, 'end': 8, 'length': 8},
        ]
        assert highlighter.line_tokens[5]['list_indent'] == [
            {'start': 0, 'end': 1, 'length': 1},
        ]

        nested_block = self.block(highlighter.document(), 1)
        assert self.background_at(nested_block, 0) == QColor(
            highlighter.theme['list_indent']['bg']['color']
        )
        assert self.background_at(nested_block, 4) == QColor(
            highlighter.theme['list']['bg']
        )
        assert self.foreground_at(nested_block, 6) == QColor(
            highlighter.theme['list_text']['color']
        )

    def test_indented_marker_is_not_a_list_without_list_context(self, highlighter):
        self.highlight(highlighter, 'paragraph\n    - indented code')

        assert 'list' not in highlighter.line_tokens[1]

    def test_abbreviation_highlights_only_definition_prefix(self, highlighter):
        source = '*[HTML]: Hyper Text Markup Language'
        self.highlight(highlighter, source)
        block = highlighter.document().firstBlock()

        assert self.background_at(block, source.index(':')) == QColor(
            highlighter.theme['abbr']['bg']['color']
        )
        assert self.background_at(block, source.index('Hyper')) == QColor()

    def test_html_requires_a_valid_tag_shape(self, highlighter):
        self.highlight(highlighter, 'a < b > c and <span data-id="1">ok</span>')

        html_tokens = highlighter.line_tokens[0]['html']
        assert len(html_tokens) == 2
        assert html_tokens[0]['start'] == 14

    def test_multiline_html_comment_protects_markdown(self, highlighter):
        self.highlight(highlighter, '<!-- *not italic*\nstill **not bold** -->\n*italic*')

        assert 'i' not in highlighter.line_tokens[0]
        assert 'b' not in highlighter.line_tokens[1]
        assert 'i' in highlighter.line_tokens[2]

    def test_html_comment_ends_with_its_blockquote_container(self, highlighter):
        self.highlight(highlighter, '> <!-- unclosed\noutside *italic*')

        assert 'html_comment' in highlighter.line_tokens[0]
        assert 'html_comment' not in highlighter.line_tokens[1]
        assert 'i' in highlighter.line_tokens[1]

    def test_multiline_html_comment_preserves_blockquote_prefix(self, highlighter):
        self.highlight(highlighter, '> <!-- open\n> still a comment\n> -->')

        second_line = highlighter.line_tokens[1]
        assert second_line['blockquote'][0]['start'] == 0
        assert second_line['html_comment'][0]['start'] == 2

    def test_fence_type_and_exact_length_control_closing(self, highlighter):
        self.highlight(highlighter, '~~~~python\n# comment\n~~~\nvalue = 1\n~~~~~\nstill code\n~~~~\nafter')
        document = highlighter.document()

        assert self.block(document, 0).userData().get_param('code', 'opened') is True
        assert self.block(document, 2).userData().get_param('code', 'closed') is False
        assert self.block(document, 4).userData().get_param('code', 'closed') is False
        assert self.block(document, 6).userData().get_param('code', 'closed') is True
        assert self.block(document, 7).userData().get_param('code', 'within') is not True

    def test_legacy_pseudo_fence_supports_non_python_languages(self, highlighter):
        source = '    ::::json\n    {"value": 42}\n\nafter'
        self.highlight(highlighter, source)
        document = highlighter.document()

        assert self.block(document, 0).userData().markdown_pseudo_fence['language'] == 'json'
        assert self.block(document, 1).userData().get_param('code', 'within') is True
        assert not hasattr(self.block(document, 2).userData(), 'markdown_pseudo_fence')
        assert self.block(document, 3).userData().get_param('code', 'within') is not True

    def test_legacy_pseudo_fence_requires_document_start_or_blank_line(self, highlighter):
        self.highlight(highlighter, 'paragraph\n    ::::py\n    print("not a pseudo-fence")')

        assert not hasattr(self.block(highlighter.document(), 1).userData(), 'markdown_pseudo_fence')

    def test_non_bmp_emoji_does_not_shorten_heading_format(self, highlighter):
        source = '# Header 😀'
        self.highlight(highlighter, source)
        block = highlighter.document().firstBlock()
        utf16_length = self.utf16_position(source, len(source))

        assert any(
            format_range.start == 2
            and format_range.start + format_range.length == utf16_length
            and format_range.format.fontWeight() > 400
            for format_range in block.layout().formats()
        )

    def test_formatting_after_non_bmp_emoji_uses_qt_offsets(self, highlighter):
        source = '# 😀 `code`'
        self.highlight(highlighter, source)
        code_start = self.utf16_position(source, source.index('`'))

        assert self.foreground_at(highlighter.document().firstBlock(), code_start) == QColor(
            highlighter.theme['codel']['color']
        )

    def test_backtick_info_string_cannot_contain_backticks(self, highlighter):
        self.highlight(highlighter, '``` python `invalid`')

        assert highlighter.document().firstBlock().userData().get_param('code', 'opened') is not True

    def test_fenced_python_uses_pygments_token_colors(self, highlighter):
        self.highlight(highlighter, '```py\ndef hello():\n    return "ok"\n```')
        document = highlighter.document()

        keyword_color = QColor(highlighter.theme['coop4']['color'])
        string_color = QColor(highlighter.theme['coop2']['color'])
        assert self.foreground_at(self.block(document, 1), 0) == keyword_color
        assert self.foreground_at(self.block(document, 2), 11) == string_color

    @pytest.mark.parametrize('language, source, token, theme_key', [
        ('c', 'int main(void) { return 0; }', 'int', 'coop4'),
        ('js', 'function answer() { return 42; }', 'function', 'coop4'),
        ('php', 'function answer() { return 42; }', 'function', 'coop4'),
        ('json', '{"value": 42}', '42', 'coop5'),
        ('bash', 'printf "%s\\n" "$HOME"', '"%s\\n"', 'coop2'),
        ('xml', '<root id="value"/>', 'root', 'coop3'),
    ])
    def test_common_fence_languages_use_distinct_lexers(
            self, highlighter, language, source, token, theme_key):
        self.highlight(highlighter, f'```{language}\n{source}\n```')
        block = self.block(highlighter.document(), 1)

        assert self.foreground_at(block, source.index(token)) == QColor(
            highlighter.theme[theme_key]['color']
        )

    @pytest.mark.parametrize('language, source', [
        ('php', '# PHP comment'),
        ('php', '// PHP comment'),
        ('js', '// JavaScript comment'),
    ])
    def test_line_comments_are_finalized_at_qt_block_end(
            self, highlighter, language, source):
        self.highlight(highlighter, f'```{language}\n{source}\n```')
        block = self.block(highlighter.document(), 1)

        assert self.foreground_at(block, 0) == QColor(
            highlighter.theme['comment']['color']
        )

    def test_markdown_inside_fence_is_not_parsed_as_markdown(self, highlighter):
        self.highlight(highlighter, '```markdown\n# not a heading\n* not a list\n```')

        assert 'h1' not in highlighter.line_tokens[1]
        assert 'list' not in highlighter.line_tokens[2]

    @pytest.mark.parametrize('source, token, theme_key', [
        ('Some **bold** text', '**bold**', 'b'),
        ('Some __bold__ text', '__bold__', 'b'),
        ('Some *italic* text', '*italic*', 'i'),
        ('Some _italic_ text', '_italic_', 'i'),
        ('Some ***both*** text', '***both***', 'bi'),
        ('Some ___both___ text', '___both___', 'bi'),
    ])
    def test_markdown_fence_highlights_emphasis_as_code_syntax(
            self, highlighter, source, token, theme_key):
        self.highlight(highlighter, f'```markdown\n{source}\n```')
        block = self.block(highlighter.document(), 1)

        assert self.foreground_at(block, source.index(token)) == QColor(
            highlighter.theme[theme_key]['color']
        )

    def test_fence_cannot_start_on_list_marker_line(self, highlighter):
        self.highlight(highlighter, '- ```py')

        assert highlighter.document().firstBlock().userData().get_param('code', 'opened') is not True

    @pytest.mark.parametrize('prefix', ['    ', '        ', '> ', '>     ', '\t'])
    def test_nested_fence_preserves_code_and_closes(self, highlighter, prefix):
        self.highlight(highlighter, f'1. Item\n\n{prefix}```py\n{prefix}return "ok"\n'
                       f'{prefix}# heading\n{prefix}```\n**after**')
        document = highlighter.document()
        assert self.foreground_at(self.block(document, 3), len(prefix)) == QColor(
            highlighter.theme['coop4']['color'])
        assert self.block(document, 4).userData().get_param('code', 'within') is True
        assert self.block(document, 5).userData().get_param('code', 'closed') is True
        assert self.block(document, 6).userData().get_param('code', 'within') is not True
        assert 'b' in highlighter.line_tokens[6]

    def test_unfinished_nested_fence_ends_at_dedent(self, highlighter):
        self.highlight(highlighter, '1. Item\n\n    ```py\n    return 1\n2. **next**')
        block = self.block(highlighter.document(), 4)
        assert block.userData().get_param('code', 'within') is not True
        assert 'b' in highlighter.line_tokens[4]

    def test_pathological_single_line_skips_inline_regex_pass(self, highlighter):
        highlighter.max_inline_highlight_length = 16
        self.highlight(highlighter, '*' + ('x' * 20) + '*')

        assert 'i' not in highlighter.line_tokens[0]

    @pytest.mark.parametrize('token_type, expected', [
        (Comment.Single, 'comment'),
        (Keyword.Reserved, 'coop4'),
        (String.Double, 'coop2'),
        (Number.Integer, 'coop5'),
        (Generic.EmphStrong, 'bi'),
        (Generic.Strong, 'b'),
        (Generic.Emph, 'i'),
        (Name.Function, 'coop3'),
    ])
    def test_pygments_tokens_map_to_existing_theme(self, token_type, expected):
        assert MdHighlighter._code_theme_key(token_type) == expected

    @pytest.mark.parametrize('info, expected', [
        ('python', 'python'),
        ('py title="example"', 'python'),
        ('{.json #sample}', 'json'),
        ('unknown-language', ''),
    ])
    def test_code_language_normalization(self, info, expected):
        assert MdHighlighter._extract_code_language(info) == expected
