"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Regression coverage for Python-Markdown HTML and viewer enrichment.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from unittest.mock import Mock
from types import SimpleNamespace

import markdown
import pytest
from PySide6.QtCore import QObject
from PySide6.QtGui import QTextDocument
from PySide6.QtWidgets import QTextBrowser

from notolog.highlight.view_highlighter import ViewHighlighter
from notolog.notolog_editor import NotologEditor
from notolog.file_header import FileHeader
from notolog.fenced_code_extension import NestedFencesExtension


@pytest.mark.parametrize('prefix', ['    ', '> ', '>     '])
def test_unclosed_fences_do_not_rescan_each_remaining_line(prefix):
    class CountedLines(list):
        reads = 0

        def __getitem__(self, key):
            self.reads += 1
            return super().__getitem__(key)

    lines = CountedLines([prefix + '```python'] * 5000)
    md = markdown.Markdown(extensions=['extra', NestedFencesExtension()])
    assert md.preprocessors['fenced_code_block'].run(lines) == lines
    assert lines.reads < 5 * len(lines)


@pytest.mark.parametrize('source,expected', [
    ('    ```python\n    ~~~text\n    kept\n    ~~~',
     '<pre><code>```python\n</code></pre>\n<pre><code class="language-text">kept\n</code></pre>'),
    ('> ```python\nplain\n> ```',
     '<blockquote>\n<p><code>python\nplain</code></p>\n</blockquote>'),
    ('    ```python\n\n    kept\n    ```', '<pre><code class="language-python">\nkept\n</code></pre>'),
    ('~~~\n```\n~~~\nkept\n```',
     '<pre><code>```\n</code></pre>\n<p>kept\n```</p>'),
    ('~~~\n```\n~~~\n```\nkept\n```',
     '<pre><code>```\n</code></pre>\n<pre><code>kept\n</code></pre>'),
])
def test_fence_recovery_preserves_unfinished_text_and_container_boundaries(source, expected):
    assert markdown.markdown(source, extensions=['extra', NestedFencesExtension()]) == expected


@pytest.mark.parametrize('marker', ['1.', '-'])
@pytest.mark.parametrize('fence', ['```', '~~~'])
def test_nested_code_uses_application_renderer(marker, fence):
    host = SimpleNamespace(md_extensions=NotologEditor.md_extensions)
    NotologEditor.init_md(host)
    source = f'{marker} Item\n\n    {fence}python\n    print("<tag>")\n    {fence}\n\n{marker} Next'
    html = host.md.convert(source)
    assert 'codehilite' in html
    assert '&lt;tag&gt;' in html
    assert fence not in html
    assert html.index('<li>') < html.index('codehilite') < html.index('</li>')


@pytest.mark.parametrize('prefix', ['', '    ', '        ', '> ', '>     '])
@pytest.mark.parametrize('fence', ['```', '~~~'])
def test_fenced_code_has_only_one_highlighted_table(prefix, fence):
    host = SimpleNamespace(md_extensions=NotologEditor.md_extensions)
    NotologEditor.init_md(host)
    source = '\n'.join(prefix + line for line in [fence + 'sh', 'pip install "notolog[tts]"', fence])
    for _ in range(2):
        html = host.md.convert(source)
        assert html.count('class="codehilitetable"') == 1
        assert html.count('class="linenos"') == 1
        assert '"s2"' in html
        assert fence not in html


def test_title_refresh_preserves_current_title_and_avoids_duplicate_updates(qapp):
    from PySide6.QtWidgets import QMainWindow
    window = QMainWindow()
    window.header = FileHeader().get_new()
    window.header.set_param('title', 'Guide')
    window.lexemes = SimpleNamespace(get=lambda key, **kwargs: (
        f"Notolog - {kwargs['sub_title']}" if kwargs else 'Notolog'))
    changes = []
    window.windowTitleChanged.connect(changes.append)
    NotologEditor.set_app_title(window)
    NotologEditor.set_app_title(window)
    assert changes == ['Notolog - Guide']
    window.header = FileHeader()
    NotologEditor.set_app_title(window, '')
    assert changes == ['Notolog - Guide', 'Notolog']
    window.close()


@pytest.fixture
def viewer(qapp):
    class Host(QObject):
        HTML_TPL = NotologEditor.HTML_TPL

        def get_view_widget(self):
            return self.widget

        def get_view_doc(self):
            return self.document

        def convert_markdown_to_html(self, content):
            return self.md.convert(content)

    host = Host()
    host.widget = QTextBrowser()
    host.document = QTextDocument(host)
    host.widget.setDocument(host.document)
    host.md = markdown.Markdown(extensions=['extra'])
    host.view_highlighter = ViewHighlighter(document=host.document)
    host.statusbar = Mock()
    host.logger = Mock()
    host.set_app_title = Mock()
    host.process_document_images = Mock()
    yield host
    host.view_highlighter.setDocument(None)
    host.widget.close()


@pytest.mark.parametrize('source, expected, struck', [
    ('Some ~~struck~~ text end', 'Some struck text end', 'struck'),
    ('First paragraph\n\nLast ~~struck~~ text', 'First paragraph\nLast struck text', 'struck'),
    ('😀 ~~struck 🚀~~ end', '😀 struck 🚀 end', 'struck 🚀'),
    ('~~one~~ and ~~two~~ @todo later', 'one and two @todo later', 'two'),
    ('~~one~~ and ~~two\n\ncontinued~~', 'one and two\ncontinued', 'continued'),
    ('~~before `code` after~~', 'before code after', 'after'),
])
def test_application_strikethrough_pipeline(viewer, source, expected, struck):
    NotologEditor.load_content_html(viewer, FileHeader(), source)
    # The application's HTML template adds a trailing space.
    assert viewer.document.toPlainText().rstrip() == expected
    assert viewer.document.find(struck).charFormat().fontStrikeOut()
    if '@todo' in expected:
        expected_format = viewer.view_highlighter.cf(**viewer.view_highlighter.theme['todo'])
        assert viewer.document.find('@todo').charFormat().background() == expected_format.background()


def test_nested_code_remains_literal_through_view_pipeline(viewer):
    viewer.md_extensions = NotologEditor.md_extensions
    NotologEditor.init_md(viewer)
    source = '1. Item\n\n    ```text\n    **literal** <tag> ~~code~~\n    ```\n\n2. Next'
    NotologEditor.load_content_html(viewer, FileHeader(), source)
    text = viewer.document.toPlainText()
    assert '**literal** <tag> ~~code~~' in text
    assert '```' not in text
    assert not viewer.document.find('code').charFormat().fontStrikeOut()


def test_edit_title_is_applied_after_content_and_cleared_for_untitled_file(qapp):
    from PySide6.QtWidgets import QPlainTextEdit
    editor = QPlainTextEdit()
    titles = []
    host = SimpleNamespace(get_edit_widget=lambda: editor, line_numbers=Mock(),
                           set_app_title=lambda title: titles.append((title, editor.toPlainText())))
    header = FileHeader().get_new()
    header.set_param('title', 'Guide')
    NotologEditor.load_content_edit(host, header, 'body')
    NotologEditor.load_content_edit(host, FileHeader(), 'next')
    assert titles == [('Guide', 'body'), ('', 'next')]
    assert editor.document().metaInformation(QTextDocument.MetaInformation.DocumentTitle) == ''
    editor.close()


@pytest.mark.parametrize('source', ['`~~code~~`', '```\n~~code~~\n```'])
def test_viewer_preserves_literal_code(viewer, source):
    NotologEditor.load_content_html(viewer, FileHeader(), source)
    assert viewer.document.toPlainText().strip() == '~~code~~'
    assert not viewer.document.find('code').charFormat().fontStrikeOut()


def test_loading_another_document_does_not_inherit_open_strikethrough(viewer):
    NotologEditor.load_content_html(viewer, FileHeader(), '~~unfinished')
    NotologEditor.load_content_html(viewer, FileHeader(), 'plain\n\nlast paragraph')
    assert viewer.document.toPlainText().rstrip() == 'plain\nlast paragraph'
    assert not viewer.document.find('plain').charFormat().fontStrikeOut()
    assert not viewer.document.find('last paragraph').charFormat().fontStrikeOut()


@pytest.mark.parametrize('marker', ['@todo', '@TODO', '@ToDo'])
@pytest.mark.parametrize('source', ['{marker}', '😀 {marker} next', '~~done {marker}~~'])
def test_viewer_todo_case_and_strikethrough(viewer, marker, source):
    source = source.format(marker=marker)
    NotologEditor.load_content_html(viewer, FileHeader(), source)
    fmt = viewer.document.find(marker).charFormat()
    assert fmt.background() == viewer.view_highlighter.cf(**viewer.view_highlighter.theme['todo']).background()
    assert fmt.fontStrikeOut() == source.startswith('~~')


@pytest.mark.parametrize('source', ['name@TODO next', '@@TODO next', '@TODOS next'])
def test_viewer_todo_boundaries(viewer, source):
    NotologEditor.load_content_html(viewer, FileHeader(), source)
    assert not viewer.view_highlighter.line_tokens[0].get('todo')


def test_viewer_todo_preserves_heading_font(viewer):
    NotologEditor.load_content_html(viewer, FileHeader(), '# Title @TODO next')
    title_format = viewer.document.find('Title').charFormat()
    todo_format = viewer.document.find('@TODO').charFormat()
    assert todo_format.fontPointSize() == title_format.fontPointSize()
    assert todo_format.fontWeight() == title_format.fontWeight()


def test_unmatched_closing_strike_markers_remain_literal(viewer):
    NotologEditor.load_content_html(viewer, FileHeader(), 'plain~~ text')
    assert viewer.document.toPlainText().rstrip() == 'plain~~ text'
    assert not viewer.document.find('plain').charFormat().fontStrikeOut()


@pytest.mark.parametrize('destination', ['guide.md', 'https://example.com/guide'])
@pytest.mark.parametrize('title', ['', ' "Example title"'])
def test_viewer_link_destination_and_title(viewer, destination, title):
    source = f'[Guide]({destination}{title})'
    NotologEditor.load_content_html(viewer, FileHeader(), source)
    assert viewer.document.toPlainText().strip() == 'Guide'
    fmt = viewer.document.find('Guide').charFormat()
    assert fmt.isAnchor()
    assert fmt.anchorHref() == destination
    if title:
        assert fmt.toolTip() == 'Example title'
