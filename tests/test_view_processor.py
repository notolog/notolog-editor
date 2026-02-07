"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Contains unit tests for ViewProcessor admonition handling.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from PySide6.QtGui import QTextDocument, QFont

from notolog.highlight.view_highlighter import ViewHighlighter
from notolog.view_processor import ViewProcessor

import pytest


class TestViewProcessorAdmonition:
    """Tests for ViewProcessor admonition conversion to table format."""

    @pytest.fixture(scope="function")
    def test_obj_doc(self):
        """Create a QTextDocument for testing."""
        doc = QTextDocument()
        font = QFont("Sans Serif")
        doc.setDefaultFont(font)
        yield doc

    @pytest.fixture(scope="function")
    def test_obj_highlighter(self, test_obj_doc):
        """Create ViewHighlighter for testing."""
        yield ViewHighlighter(document=test_obj_doc)

    @pytest.fixture(scope="function")
    def test_obj_processor(self, test_obj_highlighter):
        """Create ViewProcessor for testing."""
        yield ViewProcessor(highlighter=test_obj_highlighter)

    def test_admonition_icons_mapping(self, test_obj_processor):
        """Test that ADMONITION_ICONS maps to SVG file names."""
        assert test_obj_processor.ADMONITION_ICONS['note'] == 'pencil-square.svg'
        assert test_obj_processor.ADMONITION_ICONS['warning'] == 'exclamation-triangle-fill.svg'
        assert test_obj_processor.ADMONITION_ICONS['info'] == 'info-circle-fill.svg'

    def test_admonition_color_keys_mapping(self, test_obj_processor):
        """Test that ADMONITION_COLOR_KEYS maps to theme keys."""
        assert test_obj_processor.ADMONITION_COLOR_KEYS['note'] == 'adm_note'
        assert test_obj_processor.ADMONITION_COLOR_KEYS['warning'] == 'adm_warning'
        assert test_obj_processor.ADMONITION_COLOR_KEYS['hint'] == 'adm_tip'

    def test_get_admonition_color_returns_valid_color(self, test_obj_processor):
        """Test color retrieval returns valid color format (hex or named)."""
        color = test_obj_processor.get_admonition_color('note')
        # Color should be either hex format (#XXXXXX) or a valid color name string
        assert color is not None
        assert isinstance(color, str)
        assert len(color) > 0

    def test_get_admonition_color_bg(self, test_obj_processor):
        """Test background color retrieval returns valid format."""
        bg_color = test_obj_processor.get_admonition_color('note', '_bg')
        # Background color should be a non-empty string (hex or named color)
        assert bg_color is not None
        assert isinstance(bg_color, str)
        assert len(bg_color) > 0

    def test_get_admonition_icon_svg_returns_img_tag(self, test_obj_processor):
        """Test SVG icon returns base64 img tag or empty string."""
        icon = test_obj_processor.get_admonition_icon_svg('note', '#00b8d4')
        if icon:
            assert '<img src="data:image/svg+xml;base64,' in icon

    def test_process_admonitions_note(self, test_obj_processor):
        """Test conversion of note admonition to table format."""
        input_html = '''<div class="admonition note">
<p class="admonition-title">Important Note</p>
<p>This is the content of the note.</p>
</div>'''

        result = test_obj_processor.process_admonitions(input_html)

        assert '<table class="_n_admonition">' in result
        assert '<th class="_n_admonition_title"' in result
        assert 'style="color:' in result
        assert 'background-color:' in result
        assert 'Important Note' in result
        assert '<td class="_n_admonition_content">' in result
        assert 'This is the content of the note.' in result
        assert '</table>' in result
        assert '<div class="admonition note">' not in result

    def test_process_admonitions_warning(self, test_obj_processor):
        """Test conversion of warning admonition to table format."""
        input_html = '''<div class="admonition warning">
<p class="admonition-title">Warning</p>
<p>Be careful!</p>
</div>'''

        result = test_obj_processor.process_admonitions(input_html)

        assert '<table class="_n_admonition">' in result
        assert 'Warning' in result

    def test_process_admonitions_preserves_html_content(self, test_obj_processor):
        """Test that HTML content within admonition is preserved."""
        input_html = '''<div class="admonition tip">
<p class="admonition-title">Tip</p>
<p>Use <code>record()</code> for <strong>tracking</strong>.</p>
</div>'''

        result = test_obj_processor.process_admonitions(input_html)

        assert '<code>record()</code>' in result
        assert '<strong>tracking</strong>' in result

    def test_process_admonitions_multiple_blocks(self, test_obj_processor):
        """Test processing multiple admonition blocks."""
        input_html = '''<div class="admonition note">
<p class="admonition-title">Note</p>
<p>Note content.</p>
</div>
<p>Some text between.</p>
<div class="admonition warning">
<p class="admonition-title">Warning</p>
<p>Warning content.</p>
</div>'''

        result = test_obj_processor.process_admonitions(input_html)

        assert result.count('_n_admonition') >= 2
        assert 'Some text between.' in result

    def test_process_admonitions_no_admonitions(self, test_obj_processor):
        """Test processing content with no admonitions."""
        input_html = '<p>Regular paragraph with no admonitions.</p>'

        result = test_obj_processor.process_admonitions(input_html)

        assert result == input_html

    def test_process_admonitions_all_types(self, test_obj_processor):
        """Test all supported admonition types are processed."""
        types = [
            'note', 'info', 'tip', 'hint', 'warning', 'caution',
            'danger', 'error', 'success', 'question', 'abstract',
            'summary', 'example', 'bug', 'quote', 'failure',
        ]

        for adm_type in types:
            input_html = f'''<div class="admonition {adm_type}">
<p class="admonition-title">Title</p>
<p>Content</p>
</div>'''

            result = test_obj_processor.process_admonitions(input_html)

            assert '<table class="_n_admonition">' in result, f"Failed for type: {adm_type}"
            assert 'Title' in result


class TestViewProcessorAdmonitionIntegration:
    """Integration tests for admonition processing in post_md_process flow."""

    @pytest.fixture(scope="function")
    def test_obj_doc(self):
        """Create a QTextDocument for testing."""
        doc = QTextDocument()
        font = QFont("Sans Serif")
        doc.setDefaultFont(font)
        yield doc

    @pytest.fixture(scope="function")
    def test_obj_highlighter(self, test_obj_doc):
        """Create ViewHighlighter for testing."""
        yield ViewHighlighter(document=test_obj_doc)

    @pytest.fixture(scope="function")
    def test_obj_processor(self, test_obj_highlighter):
        """Create ViewProcessor for testing."""
        yield ViewProcessor(highlighter=test_obj_highlighter)

    def test_post_md_process_converts_admonitions(self, test_obj_processor):
        """Test that post_md_process integrates admonition conversion."""
        input_html = '''<div class="admonition note">
<p class="admonition-title">Test</p>
<p>Content here.</p>
</div>'''

        result = test_obj_processor.post_md_process(input_html)

        assert '<table class="_n_admonition">' in result

    def test_post_md_process_handles_mixed_content(self, test_obj_processor):
        """Test post_md_process with expandable blocks and admonitions."""
        input_html = '''[details]
[summary]Expandable[/summary]
Hidden content
[/details]
<div class="admonition warning">
<p class="admonition-title">Warning</p>
<p>Be careful!</p>
</div>'''

        result = test_obj_processor.post_md_process(input_html)

        assert '<details>' in result
        assert '<summary>' in result
        assert '<table class="_n_admonition">' in result

    def test_get_valid_font_size_zero_fallback(self, test_obj_processor):
        """Test fallback when font pointSizeF returns 0 or negative."""
        font = QFont("Sans Serif")
        font.setPointSizeF(0)
        test_obj_processor.doc.setDefaultFont(font)

        result = test_obj_processor.get_valid_font_size()
        assert result >= 12.0, "Should fallback to minimum 12.0pt"
        assert isinstance(result, float)

    def test_get_valid_font_size_negative_fallback(self, test_obj_processor):
        """Test fallback when font size is negative."""
        font = QFont("Sans Serif")
        font.setPointSizeF(-5)
        test_obj_processor.doc.setDefaultFont(font)

        result = test_obj_processor.get_valid_font_size()
        assert result == 12.0, "Should use safe default of 12.0pt"
