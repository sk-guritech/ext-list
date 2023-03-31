from __future__ import annotations

import pytest

from ext_list import ExtList
from tests.conftest import Person


def test_raise_key_error_by_specific_invalid_key():
    ext_list_1 = ExtList([{'a': 1, 'b': 2}, {'a': 3, 'b': 4}])

    with pytest.raises(KeyError):
        ext_list_1.not_equals('c', 1)


def test_raise_index_error_by_specific_invalid_index():
    ext_list_1 = ExtList([[1, 2], [3, 4], [5, 6]])

    with pytest.raises(IndexError):
        ext_list_1.not_equals(2, 1)


def test_raise_attribute_error_by_specific_invalid_attribute():
    alice = Person(name='alice', age=25)
    bob = Person(name='bob', age=30)
    charlie = Person(name='charlie', age=35)

    ext_list_1 = ExtList([alice, bob, charlie])

    with pytest.raises(AttributeError):
        ext_list_1.not_equals('hello', 'hello')
