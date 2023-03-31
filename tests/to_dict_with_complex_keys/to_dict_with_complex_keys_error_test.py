from __future__ import annotations

import pytest

from ex_list import ExList
from tests.conftest import Person


def test_raise_key_error_by_specific_invalid_key():
    ex_list_1 = ExList([{'a': 1, 'b': 2}, {'a': 1, 'b': 3}, {'a': 2, 'b': 3}])

    with pytest.raises(KeyError):
        ex_list_1.to_dict_with_complex_keys(['a', 'c'])


def test_raise_index_error_by_specific_invalid_index():
    ex_list_1 = ExList([[1, 2], [3, 4], [5, 6]])

    with pytest.raises(IndexError):
        ex_list_1.to_dict_with_complex_keys([1, 2])


def test_raise_attribute_error_by_specific_invalid_attribute():
    alice = Person(name='alice', age=25)
    ex_list_1 = ExList([alice])

    with pytest.raises(AttributeError):
        ex_list_1.to_dict_with_complex_keys(['hello'])


def test_raise_type_error_by_assign_too_many_argument():
    alice = Person(name='alice', age=25)
    ex_list_1 = ExList([alice])

    with pytest.raises(TypeError):
        ex_list_1.to_dict_with_complex_keys([Person.introduce], ((0,),))
