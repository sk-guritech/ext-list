from __future__ import annotations

import pytest

from ext_list import ExtList
from tests.conftest import Person


def test_raise_key_error_by_specific_invalid_key():
    ext_list_1 = ExtList([{'a': 1}, {'a': 2}, {'a': 3}])

    with pytest.raises(KeyError):
        ext_list_1.to_dict('b')


def test_raise_index_error_by_specific_invalid_index():
    ext_list_1 = ExtList([[1, 2], [3, 4], [5, 6]])

    with pytest.raises(IndexError):
        ext_list_1.to_dict(2)


def test_raise_attribute_error_by_specific_invalid_attribute():
    alice = Person(name='alice', age=25)

    ext_list_1 = ExtList([alice])
    with pytest.raises(AttributeError):
        ext_list_1.to_dict('hello')
