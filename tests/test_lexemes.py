# tests/test_lexemes.py

from app.lexemes.lexemes import Lexemes

from logging import Logger

import pytest
import os


class TestLexemes:

    @pytest.fixture(scope="function", autouse=True)
    def test_obj_lexemes(self, mocker, request):
        """
        Testing object fixture.
        May contain minimal logic for testing purposes.
        """

        # Get the parameter value(s) from the request
        language, lexemes, lexemes_dir = request.param if hasattr(request, 'param') else None

        if lexemes:
            """
            If lexemes explicitly set return them.
            This is for test cases where the lexemes file read is not necessary.
            """
            mocker.patch.object(Lexemes, 'load_lexemes', return_value=lexemes)
        elif lexemes_dir:
            """
            If lexemes dir is set read lexemes from there.
            For test cases to check actual lexemes file read.
            """
            test_lexemes_dir = os.path.join(os.path.dirname(__file__), lexemes_dir)
            mocker.patch.object(Lexemes, 'get_lexemes_dir', return_value=test_lexemes_dir)
        else:
            """
            Return empty lexemes in the rest of the cases.
            """
            mocker.patch.object(Lexemes, 'load_lexemes', return_value={})

        yield Lexemes(language=language)

    @pytest.fixture(scope="function")
    def test_exp_params_fixture(self, request):
        """
        Fixture to pass params and get expected results.
        This method is used only for passing params via pytest fixture.
        """

        # Get the parameter value(s) from the request
        param_values = request.param

        yield param_values

    @pytest.mark.parametrize(
        "test_obj_lexemes, test_exp_params_fixture",
        [
            ((None, None, None), ('en', {})),
            (('', {}, None), ('en', {})),
            (('en', {123: 456}, None), ('en', {123: 456})),
            (('anyval', {'A': 'B', 'C': 'D'}, None), ('anyval', {'A': 'B', 'C': 'D'})),
        ],
        indirect=True
    )
    def test_lexemes_init(self, test_obj_lexemes, test_exp_params_fixture):
        """
        Test and check initial params are exist in the testing object.
        """
        assert isinstance(test_obj_lexemes.logger, Logger)

        exp_language, exp_lexemes = test_exp_params_fixture

        assert hasattr(test_obj_lexemes, 'language')
        assert test_obj_lexemes.language == exp_language
        assert hasattr(test_obj_lexemes, 'lexemes')
        assert test_obj_lexemes.lexemes == exp_lexemes

    @pytest.mark.parametrize(
        "test_obj_lexemes, test_exp_params_fixture",
        [
            ((None, None, None), (None, 'en')),
            (('', None, None), (None, 'en')),
            (('en', None, None), (None, 'en')),
            (('anyval', None, None), (None, 'anyval')),
            (('anyval', None, None), ('new', 'new')),
        ],
        indirect=True
    )
    def test_lexemes_set_language(self, test_obj_lexemes, test_exp_params_fixture):
        """
        Test language setting for lexemes after the one was initialized.
        """
        param_language, exp_language = test_exp_params_fixture

        if param_language:
            test_obj_lexemes.set_language(param_language)

        assert hasattr(test_obj_lexemes, 'language')
        assert test_obj_lexemes.language == exp_language

    @pytest.mark.parametrize(
        "test_obj_lexemes, test_exp_params_fixture",
        [
            ((None, None, None), 'en'),
            (('', None, None), 'en'),
            (('en', None, None), 'en'),
            (('any', None, None), 'any'),
            (('..', None, None), 'en'),
        ],
        indirect=True
    )
    def test_lexemes_get_lexemes_dir(self, mocker, test_obj_lexemes, test_exp_params_fixture):
        """
        Test lexemes target dir path.
        """
        exp_lexemes_dir = test_exp_params_fixture

        mocker.patch.object(os.path, 'dirname', return_value='')

        assert test_obj_lexemes.get_lexemes_dir() == exp_lexemes_dir

    @pytest.mark.parametrize(
        "test_obj_lexemes, test_exp_params_fixture",
        [
            ((None, None, None),
             ('en', {})),
            ((None, None, 'test_lexemes'),
             ('en', {'test_common': {'any': 'thing', 'hello': 'Hello World!', 'test': 'Passed'},
                     'test_scope': {123: 456, 'foo': 'bar', 'test': 'result'}})),
        ],
        indirect=True
    )
    def test_lexemes_load_lexemes(self, mocker, test_obj_lexemes, test_exp_params_fixture):
        """
        Test actual lexemes loaded.
        """
        exp_language, exp_lexemes = test_exp_params_fixture

        assert hasattr(test_obj_lexemes, 'lexemes')
        assert test_obj_lexemes.lexemes == exp_lexemes

    @pytest.mark.parametrize(
        "test_obj_lexemes, test_exp_params_fixture",
        [
            ((None, None, None), (None, None, None)),
            ((None, None, 'test_lexemes'), ('test_common', 'hello', 'Hello World!')),
            ((None, None, 'test_lexemes'), ('test_common', 'test', 'Passed')),
            ((None, None, 'test_lexemes'), ('test_scope', 123, 456)),
            ((None, None, 'test_lexemes'), ('test_scope', 'undefined_name', '')),
            ((None, None, 'test_lexemes'), ('test_scope_undefined', None, None)),
            ((None, None, 'test_lexemes'), ('test_scope_undefined', 'undefined_name', None)),
        ],
        indirect=True
    )
    def test_lexemes_get(self, test_obj_lexemes, test_exp_params_fixture):
        """
        Test getter for correctly loaded and really existent lexemes.
        """
        param_scope, param_name, exp_result = test_exp_params_fixture

        assert test_obj_lexemes.get(param_name, param_scope) == exp_result
