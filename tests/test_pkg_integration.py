# tests/test_pkg_integration.py
import pytest

import emoji
import markdown


@pytest.fixture
def markdown_obj():
    # Fixture to create and return main Markdown instance
    extensions = ['markdown.extensions.extra']
    # Init markdown object with the selected extensions
    md = markdown.Markdown(extensions=extensions)
    yield md


def test_markdown_conversion(markdown_obj):

    md_content = "*Italic text*"
    "**Bold text**"
    "___Italic bold text___"

    # Convert markdown to HTML
    html_content = markdown_obj.convert(md_content)

    assert html_content == "<p><em>Italic text</em></p>"
    "<p><strong>Bold text</strong></p>"
    "<p><strong><em>Bold text</em></strong></p>"


def test_emoji_conversion():

    text_content = ":cat:"

    # Process emojis :cat: to 🐱 conversion
    emoji_content = emoji.emojize(text_content, language="en")

    assert emoji_content == "🐈"
