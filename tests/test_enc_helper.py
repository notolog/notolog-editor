"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Contains unit and integration tests for the related functionality.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2025 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from notolog.encrypt.enc_helper import EncHelper
from notolog.encrypt.enc_password import EncPassword

from cryptography.fernet import Fernet

from logging import Logger

import pytest


class TestEncHelper:

    @pytest.fixture(scope="function", autouse=True)
    def test_obj_enc_password(self, request):

        # Retrieve parameter values from the test request.
        password = request.param

        _enc_password = EncPassword()
        _enc_password.password = password
        _enc_password.hint = None

        yield _enc_password

    @pytest.fixture(scope="function", autouse=True)
    def test_obj_enc_helper(self, mocker, test_obj_enc_password, request):
        # Retrieve parameter values from the test request.
        salt, iterations = request.param

        # Force fallback default to avoid settings default
        mocker.patch.object(EncHelper, 'get_default_iterations', return_value=EncHelper.DEFAULT_ITERATIONS)

        mocker.patch('secrets.token_urlsafe', return_value='RANDOM_SALT')
        _helper = EncHelper(enc_password=test_obj_enc_password, salt=salt, iterations=iterations)

        yield _helper

    @pytest.fixture(scope="function")
    def test_exp_params_fixture(self, request):
        # Retrieve parameter values from the test request.
        password, salt, iterations = request.param

        yield password, salt, iterations

    @pytest.mark.parametrize(
        "test_obj_enc_password, test_obj_enc_helper, test_exp_params_fixture",
        [
            ((None), (None, None), (b'', b'RANDOM_SALT', EncHelper.DEFAULT_ITERATIONS)),
            (('some>pass>here'), ('some>salt>here', 8000), (b'some>pass>here', b'some>salt>here', 8000)),
            ((b'some>pass>here'), (b'some>salt>here', 16000), (b'some>pass>here', b'some>salt>here', 16000)),
        ],
        indirect=True
    )
    def test_enc_helper_init(self, test_obj_enc_password, test_obj_enc_helper, test_exp_params_fixture):
        # Check initial params are exist
        assert isinstance(test_obj_enc_helper.logger, Logger)

        exp_password, exp_salt, exp_iterations = test_exp_params_fixture

        assert hasattr(test_obj_enc_helper, 'enc_password')
        assert hasattr(test_obj_enc_helper, 'password')
        assert hasattr(test_obj_enc_helper, 'salt')
        assert hasattr(test_obj_enc_helper, 'iterations')
        # Password and salt are expectedly set
        assert test_obj_enc_helper.enc_password == test_obj_enc_password
        assert test_obj_enc_helper.password == exp_password
        assert test_obj_enc_helper.salt == exp_salt
        # Check expected iterations count
        assert test_obj_enc_helper.iterations == exp_iterations

        assert hasattr(test_obj_enc_helper, 'cipher_suite')
        assert isinstance(test_obj_enc_helper.cipher_suite, Fernet)

        assert hasattr(test_obj_enc_helper, 'key')
        assert test_obj_enc_helper.key is None

    @pytest.fixture(scope="function")
    def test_exp_param_fixture(self, request):
        # Get the parameter value from the request
        param_value = request.param

        yield param_value

    @pytest.mark.parametrize(
        "test_obj_enc_password, test_obj_enc_helper, test_exp_param_fixture",
        [
            ((None), (None, 1024), False),
            ((''), (None, 1024), False),
            ((b''), (None, 1024), False),
            (('some>pass>here'), (None, 1024), True),
            ((b'some>pass>here'), (None, 1024), True),
        ],
        indirect=True
    )
    def test_enc_helper_is_password_valid(self, test_obj_enc_helper, test_exp_param_fixture):
        assert test_obj_enc_helper.is_password_valid() == test_exp_param_fixture

    @pytest.mark.parametrize(
        "test_obj_enc_password, test_obj_enc_helper, test_exp_param_fixture",
        [
            ((None), (None, 1024), 11),  # 'RANDOM_SALT' len is 11, mocked above. Usual len is 43
        ],
        indirect=True
    )
    def test_enc_helper_generate_salt(self, test_obj_enc_helper, test_exp_param_fixture):
        _salt = EncHelper.generate_salt()
        assert len(_salt) == test_exp_param_fixture
        assert type(_salt) is str

    @pytest.mark.parametrize(
        "test_obj_enc_password, test_obj_enc_helper, test_exp_param_fixture",
        [
            ((None), (None, 16000),
             b'-TK3+?nJ\xe49\x08\x13\x13_\x1f\xd0\xc5\xa2\x89ZZ,\x0f\x99\xfe\xd9\xe2\xa3'
             b'j\xe8\xee\xc3'),  # 'RANDOM_SALT' mocked above
            ((b'some>pass>here'), (b'some>salt>here', 16000),
             b'#\xb4\xebj\x9a\xe3Zg\x1a=v\x1a\x17\x02\xeb\x95\x88B(Uv]E\xb2y\x91=\xbeF\x84Bl'),
        ],
        indirect=True
    )
    def test_enc_helper_generate_key(self, test_obj_enc_helper, test_exp_param_fixture):

        assert test_obj_enc_helper.generate_key_from_password() == test_exp_param_fixture

    @pytest.fixture(scope="function")
    def test_content_fixture(self, request):
        # Get the parameter value from the request
        content = request.param

        yield content

    @pytest.fixture(scope="function")
    def test_exp_content_fixture(self, request):
        # Get the parameter value from the request
        content = request.param

        yield content

    @pytest.mark.parametrize(
        "test_obj_enc_password, test_obj_enc_helper, test_content_fixture, test_exp_content_fixture",
        [
            ((b'some>pass>here'), (b'some>salt>here', 16000),
             'Lorem ipsum dolor sit amet'.encode("utf-8"),
             b'Lorem ipsum dolor sit amet'),
        ],
        indirect=True
    )
    def test_enc_helper_encrypt_decrypt(self, test_obj_enc_helper, test_content_fixture, test_exp_content_fixture):

        _encrypted_content = test_obj_enc_helper.encrypt_data(test_content_fixture)

        assert len(_encrypted_content) > 0
        assert type(_encrypted_content) is bytes

        _decrypted_content = test_obj_enc_helper.decrypt_data(_encrypted_content)

        assert len(_decrypted_content) > 0
        assert type(_decrypted_content) is bytes
        assert _decrypted_content == test_content_fixture
