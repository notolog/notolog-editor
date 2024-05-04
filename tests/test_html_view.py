# tests/test_html_view.py
from PySide6.QtGui import QTextDocument, QFont

from app.highlight.view_highlighter import ViewHighlighter
from app.view_processor import ViewProcessor
from app.view_decorator import ViewDecorator

import pytest


class TestHtmlView:

    @pytest.fixture(scope="function", autouse=True)
    def test_obj_doc(self, request):
        """
        Either setHtml() or setMarkdown() is required as param_func
        * https://doc.qt.io/qt-6/qtextedit.html
        """

        if not hasattr(self, '_doc'):
            self._doc = QTextDocument()
            """ To avoid errors like: QFont::setPixelSize: Pixel size <= 0 (-1) """
            font = QFont("Sans Serif")
            self._doc.setDefaultFont(font)

        # Get the parameter value(s) from the request
        param_value, param_func = request.param

        if callable(getattr(self._doc, param_func)):
            getattr(self._doc, param_func)(param_value)

        yield self._doc

    @pytest.fixture(scope="function", autouse=True)
    def test_obj_highlighter(self, test_obj_doc):
        yield ViewHighlighter(document=test_obj_doc)

    @pytest.fixture(scope="function", autouse=True)
    def test_obj_processor(self, test_obj_highlighter):
        yield ViewProcessor(highlighter=test_obj_highlighter)

    @pytest.fixture(scope="function", autouse=True)
    def test_obj_decorator(self, test_obj_highlighter):
        yield ViewDecorator(highlighter=test_obj_highlighter)

    @pytest.fixture(scope="function")
    def test_text_fixture(self, request):
        # Get the parameter value from the request
        param_value = request.param

        yield param_value

    @pytest.fixture(scope="function")
    def test_style_fixture(self, request):
        # Get the parameter value from the request
        param_value = request.param

        yield param_value

    @pytest.mark.parametrize(
        "test_obj_doc, test_text_fixture, test_style_fixture",
        [
            (("<b>Test text bold</b>", "setHtml"), "text", "bold"),
            (("<i>Test text italic</i>", "setHtml"), "text", "italic"),
            (("<u>Test text underline</u>", "setHtml"), "text", "underline"),
            (("<s>Test text strikethrough</s>", "setHtml"), "text", "strikeOut"),
            #(("~~Test text strikethrough~~", "setHtml"), "text", "strikeOut"), # TODO decorator result
            # Markdown is a proof of concept here as not in use for result render
            (("**Test text bold**", "setMarkdown"), "text", "bold"),
            (("*Test text bold*", "setMarkdown"), "text", "italic"),
            (("***Test text bold***", "setMarkdown"), "text", "bold"),
            (("***Test text bold***", "setMarkdown"), "text", "italic"),
            (("~~Test text strikethrough~~", "setMarkdown"), "text", "strikeOut"),
        ],
        indirect=True
    )
    def test_html_view_assertions(
            self, test_obj_doc, test_text_fixture, test_style_fixture, test_obj_processor, test_obj_decorator):
        """
        test_obj_doc.setHtml("<i>Test text italic</i>")
        test_obj_doc.setMarkdown('*Test text italic*')

        cursor = test_obj_doc.find(test_text_fixture)
        """

        """
        * https://doc.qt.io/qt-6/qtextdocument.html#find-1
        """
        cursor = test_obj_doc.find(test_text_fixture)

        format = cursor.charFormat()
        assert cursor.selectedText()
        """
        test_style_fixture is a method name
        * https://doc.qt.io/qt-6/qfont.html#bold
        * https://doc.qt.io/qt-6/qfont.html#italic
        * https://doc.qt.io/qt-6/qfont.html#strikeOut
        * ...
        """
        assert callable(getattr(format.font(), test_style_fixture))
        assert getattr(format.font(), test_style_fixture)()

        """
        Assertion like ',-1,-1,5,700,0,0,0,0,0,0,0,0,0,0,1'
        * https://doc.qt.io/qt-6/qfont.html#toString
        """
        #assert not format.font().toString() == '...'
