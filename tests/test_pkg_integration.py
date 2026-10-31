"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Contains unit and integration tests for the related functionality.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2026 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from pathlib import Path

import emoji
import markdown
import pytest
import tomli


@pytest.fixture
def markdown_obj():
    # Fixture to create and return main Markdown instance
    extensions = ['markdown.extensions.extra']
    # Init markdown object with the selected extensions
    md = markdown.Markdown(extensions=extensions)
    yield md


@pytest.mark.parametrize('source,expected', [
    ('*Italic text*', '<p><em>Italic text</em></p>'),
    ('**Bold text**', '<p><strong>Bold text</strong></p>'),
    ('___Italic bold text___', '<p><strong><em>Italic bold text</em></strong></p>'),
])
def test_markdown_conversion(markdown_obj, source, expected):
    assert markdown_obj.convert(source) == expected


def test_emoji_conversion():

    text_content = ":cat:"

    # Process emojis :cat: to 🐱 conversion
    emoji_content = emoji.emojize(text_content, language="en")

    assert emoji_content == "🐈"


def test_startup_readme_is_in_wheel_config():
    project_root = Path(__file__).resolve().parent.parent
    with (project_root / 'pyproject.toml').open('rb') as project_file:
        project = tomli.load(project_file)

    readme_include = next(
        item for item in project['tool']['poetry']['include']
        if isinstance(item, dict) and item.get('path') == 'README.md'
    )

    assert set(readme_include['format']) == {'sdist', 'wheel'}
