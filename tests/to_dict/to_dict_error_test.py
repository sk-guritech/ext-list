from __future__ import annotations

import pytest

from ex_list import ExList
from tests.conftest import Person


def test_raise_key_error_by_specific_invalid_key():
    ex_list_1 = ExList([{'a': 1}, {'a': 2}, {'a': 3}])

    with pytest.raises(KeyError):
        ex_list_1.to_dict('b')


def test_raise_index_error_by_specific_invalid_index():
    ex_list_1 = ExList([[1, 2], [3, 4], [5, 6]])

    with pytest.raises(IndexError):
        ex_list_1.to_dict(2)


def test_raise_attribute_error_by_specific_invalid_attribute():
    alice = Person(name='alice', age=25)

    ex_list_1 = ExList([alice])
    with pytest.raises(AttributeError):
        ex_list_1.to_dict('hello')
