from __future__ import annotations

from ext_list import ExtList
from tests.conftest import Person


def test():
    ext_list_1 = ExtList([{'a': 1, 'b': 2}, {'a': 3, 'b': 4}, {'a': 5, 'b': 6}])
    assert ext_list_1.equals('a', 1) == [{'a': 1, 'b': 2}]

    ext_list_2 = ExtList([{'a': True, 'b': False}, {'a': False, 'b': True}, {'a': True, 'b': False}])
    assert ext_list_2.equals('a', False) == [{'a': False, 'b': True}]

    alice = Person(name='alice', age=25)
    bob = Person(name='bob', age=30)
    charlie = Person(name='charlie', age=35)

    ext_list_3 = ExtList([alice, bob, charlie])
    assert ext_list_3.equals('name', 'alice') == [alice]
    assert ext_list_3.equals('age', 30) == [bob]
    assert ext_list_3.equals(Person.introduce, 'alice is 25 years old.') == [alice]
    assert ext_list_3.equals('introduce', 'alice is 25 years old.') == [alice]
    assert ext_list_3.equals(Person.get_age_n_years_ago, 20, 5) == [alice]
    assert ext_list_3.equals('get_age_n_years_ago', 20, 5) == [alice]


def test_reference_getset_descriptor():
    ext_list_1 = ExtList([1, 2, 3])

    assert ext_list_1.equals(int.real, 1) == [1]


def test_reference_method_descriptor():
    ext_list_1 = ExtList([1, 2, 3])

    assert ext_list_1.equals(int.bit_length, 2) == [2, 3]
