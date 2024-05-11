# tests/test_file_header.py

from notolog.file_header import FileHeader

from notolog.exceptions.file_header_empty_exception import FileHeaderEmptyException

from logging import Logger

import pytest


class TestFileHeader:

    @pytest.fixture(scope="function")
    def test_obj_file_header_empty(self):
        yield FileHeader()

    def test_file_header_get_empty(self, test_obj_file_header_empty):
        # Check initial params are exist
        assert isinstance(test_obj_file_header_empty.logger, Logger)

        # Check initial data
        assert test_obj_file_header_empty.header is None

        # Getter works well
        assert test_obj_file_header_empty.get_param('created') is None
        # Setter works well, with exception
        is_exception = False
        try:
            # Call the method that is expected to raise an exception
            test_obj_file_header_empty.set_param('created', 'Smth-to-Test')
        except Exception as e:
            is_exception = True
            assert isinstance(e, FileHeaderEmptyException)
        assert is_exception

        # Refresh the header
        test_obj_file_header_empty.refresh()
        assert test_obj_file_header_empty.get_param('updated') is None

        # Just to check the method reads first line of the file, check the current one
        assert test_obj_file_header_empty.read(__file__) == '# tests/test_file_header.py'

        # Is valid check works well
        assert not test_obj_file_header_empty.is_valid()

    @pytest.fixture(scope="function")
    def test_obj_file_header_new(self):
        yield FileHeader().get_new()

    def test_file_header_is_valid(self, test_obj_file_header_new):
        # Is valid check works well
        assert test_obj_file_header_new.is_valid()

    def test_file_header_get_new(self, test_obj_file_header_new):
        # Check initial params are exist
        assert isinstance(test_obj_file_header_new.logger, Logger)

        # Getter works well
        assert test_obj_file_header_new.get_param('created')
        # Setter works well
        assert test_obj_file_header_new.set_param('created', 'Smth-to-Test') is None
        assert test_obj_file_header_new.get_param('created') == 'Smth-to-Test'

        # Save created and updated params
        created = test_obj_file_header_new.get_param('created')
        updated = test_obj_file_header_new.get_param('updated')
        # Refresh the header
        test_obj_file_header_new.refresh()
        # Check update has changed
        assert test_obj_file_header_new.get_param('created') == created
        assert test_obj_file_header_new.get_param('updated') != updated

        # Save created and updated params
        created = test_obj_file_header_new.get_param('created')
        updated = test_obj_file_header_new.get_param('updated')
        # Reset created param
        test_obj_file_header_new.set_param('created', None)
        # Refresh the header
        test_obj_file_header_new.refresh()
        # Check update has changed
        assert test_obj_file_header_new.get_param('created') is not None
        assert test_obj_file_header_new.get_param('created') != created
        assert test_obj_file_header_new.get_param('updated') != updated

        # Just to check the method reads first line of the file, check the current one
        assert test_obj_file_header_new.read(__file__) == '# tests/test_file_header.py'

    @pytest.fixture(scope="function")
    def test_obj_file_header_load(self, request):
        # Get the parameter value from the request
        file_data = request.param

        _file_header, _file_content = FileHeader().load(file_data)

        yield _file_header, _file_content

    @pytest.fixture(scope="function")
    def test_exp_fixture(self, request):
        # Get the parameter value from the request
        param_value = request.param

        yield param_value

    @pytest.mark.parametrize(
        "test_obj_file_header_load, test_exp_fixture",
        [
            (
                '<!-- {"notolog.app": {"created": "2024-02-08 22:10:13.277826", "updated": "2024-02-08 22:10:13.277837"}} -->',
                '<!-- {"notolog.app": {"created": "2024-02-08 22:10:13.277826", "updated": "2024-02-08 22:10:13.277837"}} -->'
            ),
            (
                    # New line but nothing else
                    '<!-- {"notolog.app": {"created": "2024-02-08 22:10:13.277826", "updated": "2024-02-08 22:10:13.277837"}} -->\n',
                    '<!-- {"notolog.app": {"created": "2024-02-08 22:10:13.277826", "updated": "2024-02-08 22:10:13.277837"}} -->'
            ),
            (
                    # New line with return
                    '<!-- {"notolog.app": {"created": "2024-02-08 22:10:13.277826", "updated": "2024-02-08 22:10:13.277837"}} -->\n\r',
                    '<!-- {"notolog.app": {"created": "2024-02-08 22:10:13.277826", "updated": "2024-02-08 22:10:13.277837"}} -->\n'
            ),
            (
                '<!-- {"notolog.app": {"created": "2024-02-08 22:10:13.277826", "updated": "2024-02-08 22:10:13.277837"}} -->\ntest content',
                '<!-- {"notolog.app": {"created": "2024-02-08 22:10:13.277826", "updated": "2024-02-08 22:10:13.277837"}} -->\ntest content'
            ),
            (
                '<!-- {"notolog.app": {"created": "2024-02-08 22:10:13.277826", "updated": "2024-02-08 22:10:13.277837", "slt": "qwerty789ABC"}} -->',
                '<!-- {"notolog.app": {"created": "2024-02-08 22:10:13.277826", "updated": "2024-02-08 22:10:13.277837", "slt": "qwerty789ABC"}} -->'
            ),
            (
                '<!-- {"notolog.app": {"created": "2024-02-08 22:10:13.277826", "updated": "2024-02-08 22:10:13.277837", "smth123": "!!!"}} -->',
                '<!-- {"notolog.app": {"created": "2024-02-08 22:10:13.277826", "updated": "2024-02-08 22:10:13.277837", "smth123": "!!!"}} -->'
            ),
        ],
        indirect=True
    )
    def test_file_header_loaded(self, test_obj_file_header_load, test_exp_fixture):
        _file_header, _file_content = test_obj_file_header_load

        res_json = _file_header.pack(content=_file_content, encode=False)

        assert res_json == test_exp_fixture

        # Is valid check works well
        assert _file_header.is_valid()

    @pytest.fixture(scope="function")
    def test_exp_param_fixture(self, request):
        # Get the parameter value(s) from the request
        param_value = request.param

        yield param_value

    @pytest.fixture(scope="function")
    def test_exp_params_fixture(self, request):
        # Get the parameter value(s) from the request
        param_value1, param_value2 = request.param

        yield param_value1, param_value2

    @pytest.mark.parametrize(
        "test_obj_file_header_new, test_exp_param_fixture",
        [
            (None, None),
            (None, ''),
            (None, '1234567890'),
            (None, '<!-- {} -->'),
            (None, '<!-- None -->'),
            (None, '<!-- 123 -->'),
        ],
        indirect=True
    )
    def test_file_header_load_check_no_exception_raised(self, test_obj_file_header_new, test_exp_param_fixture):
        try:
            # Call the method that is not expected to raise any exception
            test_obj_file_header_new.load(test_exp_param_fixture)
        except Exception:
            pytest.fail("The method raised an unexpected exception")

    @pytest.mark.parametrize(
        "test_obj_file_header_new, test_exp_params_fixture",
        [
            (None, (None, False)),
            (None, ('', False)),
            (None, ('1234567890', False)),
            (None, ('<!-- {} -->', False)),
            (None, ('<!-- None -->', False)),
            (None, ('<!-- 123 -->', False)),
        ],
        indirect=True
    )
    def test_file_header_pack_check_no_exception_raised(self, test_obj_file_header_new, test_exp_params_fixture):
        try:
            content, encode = test_exp_params_fixture
            # Call the method that is not expected to raise any exception
            test_obj_file_header_new.pack(content=content, encode=encode)
        except Exception:
            pytest.fail("The method raised an unexpected exception")

    @pytest.mark.parametrize(
        "test_obj_file_header_load",
        [None, '', '1234567890', '<!-- {} -->', '<!-- None -->', '<!-- 123 -->'],
        indirect=True
    )
    def test_file_header_load_check_exception_raised(self, test_obj_file_header_load):
        try:
            # Call the method that is not expected to raise any exception
            _file_header, _file_content = test_obj_file_header_load
        except Exception:
            pytest.fail("The method raised an unexpected exception")

    @pytest.mark.parametrize(
        "test_obj_file_header_load, test_exp_fixture",
        [
            (
                    '<!-- {"notolog.app": {"created": "2024-02-08 22:10:13.277826", "updated": "2024-02-08 22:10:13.277837"}} -->',
                    False
            ),
            (
                    '<!-- {"notolog.app": {"created": "2024-02-08 22:10:13.277826", "updated": "2024-02-08 22:10:13.277837", "slt": "qwerty789ABC"}} -->',
                    False
            ),
            (
                    '<!-- {"notolog.app": {"created": "2024-02-08 22:10:13.277826", "updated": "2024-02-08 22:10:13.277837",'
                    '"enc": {"slt": "qwerty789ABC", "itr": "123456", "hint": "..."}}} -->',
                    True
            ),
        ],
        indirect=True
    )
    def test_file_header_is_file_encrypted(self, test_obj_file_header_load, test_exp_fixture):
        _file_header, _file_content = test_obj_file_header_load

        # Just in case
        assert _file_header.is_valid()

        # Is encrypted check works well
        assert _file_header.is_file_encrypted() == test_exp_fixture
