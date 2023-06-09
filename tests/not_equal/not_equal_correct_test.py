from __future__ import annotations

from ext_list import ExtList
from tests.conftest import Person


def test():
    ext_list_1 = ExtList([{'a': 1, 'b': 2}, {'a': 3, 'b': 4}, {'a': 5, 'b': 6}])
    assert ext_list_1.not_equal('a', 1) == [{'a': 3, 'b': 4}, {'a': 5, 'b': 6}]

    ext_list_2 = ExtList([{'a': True, 'b': False}, {'a': False, 'b': True}, {'a': True, 'b': False}])
    assert ext_list_2.not_equal('a', False) == [{'a': True, 'b': False}, {'a': True, 'b': False}]

    alice = Person(name='alice', age=25)
    bob = Person(name='bob', age=30)
    charlie = Person(name='charlie', age=35)

    ext_list_3 = ExtList([alice, bob, charlie])
    assert ext_list_3.not_equal('name', 'alice') == [bob, charlie]
    assert ext_list_3.not_equal('age', 30) == [alice, charlie]
    assert ext_list_3.not_equal(Person.introduce, 'alice is 25 years old.') == [bob, charlie]
    assert ext_list_3.not_equal('introduce', 'alice is 25 years old.') == [bob, charlie]
    assert ext_list_3.not_equal(Person.get_age_n_years_ago, 20, 5) == [bob, charlie]
    assert ext_list_3.not_equal('get_age_n_years_ago', 20, 5) == [bob, charlie]


def test_reference_getset_discriptor():
    ext_list_1 = ExtList([1, 2, 3])

    assert ext_list_1.not_equal(int.real, 1) == [2, 3]


def test_reference_method_discriptor():
    ext_list_1 = ExtList([1, 2, 3])

    assert ext_list_1.not_equal(int.bit_length, 2) == [1]
