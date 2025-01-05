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

from notolog.text_block_data import TextBlockData

import pytest


class TestTextBlockData:

    @pytest.fixture(scope="class", autouse=True)
    def test_object(self):
        """
        Fixture to pass storage between the methods below.
        The sequence is matter!
        * https://docs.pytest.org/en/7.4.x/explanation/fixtures.html
        * https://docs.pytest.org/en/latest/example/parametrize.html
        """
        if not hasattr(self, 'test_obj'):
            self.test_obj = TextBlockData(123)
        return self.test_obj

    def test_text_block_data_init(self, test_object, exp_block_number=123):
        assert test_object is not None
        assert test_object.block_number == exp_block_number
        assert isinstance(test_object.data, dict)
        assert test_object.data == {}

    @pytest.mark.parametrize(
        "tag, opened, within, closed, start, end, exp_cnt, exp_one_param, exp_one_val",
        [
            ('s', False, False, False, 1, 9, 1, 'end', 9),
            ('s', True, False, False, 19, 99, 2, 'end', 9),
            ('s', False, True, False, 79, 149, 3, 'start', 1),
            ('some_tag1', False, False, False, 11, 22, 1, 'start', 11),
            ('s', False, False, True, 129, 199, 4, 'end', 9),
            ('some_tag2', False, False, False, 123, 456, 1, 'start', 123),
        ]
    )
    def test_text_block_data_setter(self, test_object,
                                    tag, opened, within, closed, start, end, exp_cnt, exp_one_param, exp_one_val):
        # Put the data to the fixture object
        test_object.put(tag=tag, opened=opened, within=within, closed=closed, start=start, end=end)

        assert tag in test_object.data
        assert len(test_object.data[tag]) == exp_cnt
        assert test_object.get_one(tag)[exp_one_param] == exp_one_val

    @pytest.mark.parametrize("tag, exp_cnt", [('s', 4)])
    def test_text_block_data_get_all(self, test_object, tag, exp_cnt):
        assert tag in test_object.data
        assert len(test_object.data[tag]) == exp_cnt

        data = test_object.get_all(tag)
        assert len(data) == exp_cnt

    @pytest.mark.parametrize("tag, index, exp_start, exp_end", [('s', 2, 79, 149)])
    def test_text_block_data_get_one(self, test_object, tag, index, exp_start, exp_end):
        assert tag in test_object.data

        data = test_object.get_one(tag, index)
        assert data['start'] == exp_start
        assert data['end'] == exp_end

    @pytest.mark.parametrize("tag, param, exp_value", [('s', 'end', 9)])
    def test_text_block_data_get_param(self, test_object, tag, param, exp_value):
        assert tag in test_object.data

        param_value = test_object.get_param(tag, param)
        assert param_value == exp_value

    @pytest.mark.parametrize("tag, search_param, search_value, exp_param, exp_value",
                             [('s', 'start', 79, 'end', 149), ('s', 'end', 99, 'start', 19)])
    def test_text_block_data_search(self, test_object, tag, search_param, search_value, exp_param, exp_value):
        assert tag in test_object.data

        data = test_object.search(tag, search_param, search_value)
        assert data[search_param] == search_value
        assert data[exp_param] == exp_value

    @pytest.mark.parametrize("tag_to_drop, tag_to_keep", [('some_tag1', 'some_tag2'), ('some_tag2', 's')])
    def test_text_block_data_drop(self, test_object, tag_to_drop, tag_to_keep):
        assert tag_to_drop in test_object.data
        assert tag_to_keep in test_object.data

        data = test_object.drop(tag_to_drop)
        assert data is None
        assert tag_to_drop not in test_object.data
        assert tag_to_keep in test_object.data

    @pytest.mark.parametrize("tag, index, check_param, exp_end_before, exp_end_after, exp_cnt_before, exp_cnt_after",
                             [('s', 2, 'end', 149, 199, 4, 3),
                              ('s', 2, 'end', 199, None, 3, 2),
                              ('s', 1, 'end', 99, None, 2, 1),
                              ('s', 0, 'end', 9, None, 1, 0)])
    def test_text_block_data_drop_index(self, test_object,
                                        tag, index, check_param,
                                        exp_end_before, exp_end_after, exp_cnt_before, exp_cnt_after):
        assert tag in test_object.data

        data = test_object.get_one(tag, index)
        assert data is not None
        assert data[check_param] == exp_end_before
        assert len(test_object.data[tag]) == exp_cnt_before

        test_object.drop_index(tag, index)

        data = test_object.get_one(tag, index)
        # Below element has shifted up
        if exp_end_after:
            assert data is not None
            assert data[check_param] == exp_end_after
        else:
            # The last element deleted and nothing expected after it
            assert not data

        assert len(test_object.data[tag]) == exp_cnt_after
