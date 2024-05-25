# tests/test_enc_password.py

from notolog.encrypt.enc_password import EncPassword

import pytest


class TestEncPassword:

    @pytest.fixture(scope="function", autouse=True)
    def test_obj_enc_password(self, request):

        # Get the parameter value(s) from the request
        password, hint = request.param if hasattr(request, 'param') else None

        _enc_password = EncPassword()
        _enc_password.password = password
        _enc_password.hint = hint

        yield _enc_password

    @pytest.fixture(scope="function")
    def test_exp_params_fixture(self, request):
        # Get the parameter value(s) from the request
        password, hint = request.param

        yield password, hint

    @pytest.mark.parametrize(
        "test_obj_enc_password, test_exp_params_fixture",
        [
            ((None, None), (None, None)),
            (('some>pass>here', None), ('some>pass>here', None)),
            ((None, 'some-hint-here'), (None, 'some-hint-here')),
            (('some>pass>here', 'some-hint-here'), ('some>pass>here', 'some-hint-here')),
        ],
        indirect=True
    )
    def test_enc_password_init(self, test_obj_enc_password, test_exp_params_fixture):
        exp_password, exp_hint = test_exp_params_fixture

        assert hasattr(test_obj_enc_password, 'password')
        assert hasattr(test_obj_enc_password, 'hint')
        # Password and salt are expectedly set
        assert test_obj_enc_password.password == exp_password
        assert test_obj_enc_password.hint == exp_hint

    @pytest.fixture(scope="function")
    def test_exp_is_valid_fixture(self, request):
        # Get the parameter value from the request
        param_value = request.param

        yield param_value

    @pytest.mark.parametrize(
        "test_obj_enc_password, test_exp_is_valid_fixture",
        [
            ((None, None), False),
            (('>pass>', None), False),
            (('>pass>', 'some-hint-here'), False),
            (('01234567', None), True),
            (('some>pass>here', None), True),
            (('some>pass>here', 'some-hint-here'), True),
        ],
        indirect=True
    )
    def test_enc_password_is_valid(self, test_obj_enc_password: EncPassword, test_exp_is_valid_fixture):
        assert test_obj_enc_password.is_valid() == test_exp_is_valid_fixture
