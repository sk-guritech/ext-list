from __future__ import annotations

from ext_list import ExtList
from tests.conftest import Person


def test():
    ext_list_1 = ExtList([{'a': 1, 'b': 4}, {'a': 2, 'b': 5}, {'a': 3, 'b': 6}])
    assert ext_list_1.to_dict_list(['a']) == [{'a': 1}, {'a': 2}, {'a': 3}]

    ext_list_2 = ExtList([[1, 2], [3, 4], [5, 6]])
    assert ext_list_2.to_dict_list([0]) == [{0: 1}, {0: 3}, {0: 5}]

    alice = Person(name='alice', age=25)
    bob = Person(name='bob', age=30)
    charlie = Person(name='charlie', age=35)
    ext_list_3 = ExtList([alice, bob, charlie])
    assert ext_list_3.to_dict_list([Person.name, Person.get_age_n_years_ago], [(), (5,)]) == [
        {'name': 'alice', 'get_age_n_years_ago': 20},
        {'name': 'bob', 'get_age_n_years_ago': 25},
        {'name': 'charlie', 'get_age_n_years_ago': 30},
    ]


def test_reference_getset_descriptor():
    ext_list_1 = ExtList([1, 2, 3])

    assert ext_list_1.to_dict_list([int.real]) == [{'real': 1}, {'real': 2}, {'real': 3}]


def test_reference_method_descriptor():
    ext_list_1 = ExtList([1, 2, 3])

    assert ext_list_1.to_dict_list([int.bit_length]) == [{'bit_length': 1}, {'bit_length': 2}, {'bit_length': 2}]
